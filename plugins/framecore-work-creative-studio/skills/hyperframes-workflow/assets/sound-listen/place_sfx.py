#!/usr/bin/env python3
"""Lay sound samples on a video's frames by their attack and mix them with its own sound: NumPy and FFmpeg only.

  python place_sfx.py --video film.mp4 --cues cues.json --out film-sound.mp4 [--keep-audio] [--bed bed.wav]
                      [--target-lufs -14] [--ceiling -1] [--stem effects.wav] [--json]

cues.json is a list (or {"cues": [...]}) of objects, file paths relative to the JSON file:
  {"t": 3.38, "file": "kit/hit.wav", "align": "onset", "gain_db": -3, "pan": 0, "duck_db": 4, "label": "hammer"}
  t         the second of the picture the sound belongs to (a frame number works too: "frame": 101, "fps": 30)
  align     what lands on t: onset (default; the first millisecond within 20 dB of the sample's peak, like an
            editor lining up an attack), peak (the loudest moment: a whoosh's apex), start, or end (a riser's end)
  gain_db   level of this cue (default 0); pan -1 (left) .. 1 (right), equal power
  duck_db   dip the bed by this many dB under the sound (default 0), eased in and out over 40 ms

Any WAV, FLAC, MP3 or similar that the user has the right to use works: samples rendered by the earshot sound bank
(`earshot sfx render ... --dur --apex`, `earshot kit render`), the user's own licensed recordings, or Studio's own
designed sounds. The bed is the video's own sound (--keep-audio), a file (--bed), or silence. The mix is
normalised to --target-lufs (default off), trimmed so its true peak stays under --ceiling, and muxed over the
untouched picture. Each cue is checked: rendered alone and measured again, its onset or peak must sit within
5 ms of t (10 ms for peak alignment; sounds closer than 40 ms to a neighbour are flagged: they mask each other). Exit codes: 0 done, 1 a cue could not be placed on time, 3 bad input.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import listen  # noqa: E402

SR = listen.SR


def alignment_offsets(sample):
    """seconds from the start of a stereo sample to its onset, peak and end"""
    mono = sample.mean(axis=1)
    h = int(0.002 * SR)
    n = len(mono) // h
    if n == 0:
        return {'onset': 0.0, 'peak': 0.0, 'start': 0.0, 'end': len(mono) / SR}
    env = 20 * np.log10(np.sqrt((mono[: n * h].reshape(n, h) ** 2).mean(axis=1)) + 1e-9)
    onset = int(np.argmax(env >= env.max() - 20)) * 0.002
    smooth = np.convolve(env, np.ones(5) / 5, mode='same')
    return {'onset': onset, 'peak': int(np.argmax(smooth)) * 0.002, 'start': 0.0, 'end': len(mono) / SR}


def load_cues(path):
    if not os.path.isfile(path):
        raise listen.InputError(f'{path}: no such file')
    data = json.load(open(path, encoding='utf-8'))
    items = data.get('cues', data) if isinstance(data, dict) else data
    base = os.path.dirname(os.path.abspath(path))
    cues = []
    for i, c in enumerate(items):
        if 'file' not in c:
            raise listen.InputError(f'cue {i}: "file" is missing')
        t = c.get('t', c.get('time'))
        if t is None and 'frame' in c:
            t = float(c['frame']) / float(c.get('fps') or (data.get('fps') if isinstance(data, dict) else None) or 30)
        if t is None:
            raise listen.InputError(f'cue {i}: give "t" (seconds) or "frame"')
        f = c['file'] if os.path.isabs(c['file']) else os.path.join(base, c['file'])
        if not os.path.isfile(f):
            raise listen.InputError(f'cue {i}: {c["file"]} does not exist')
        if c.get('align', 'onset') not in ('onset', 'peak', 'start', 'end'):
            raise listen.InputError(f'cue {i}: align must be onset, peak, start or end')
        cues.append({'t': float(t), 'file': f, 'align': c.get('align', 'onset'), 'gain_db': float(c.get('gain_db', 0)),
                     'pan': max(-1.0, min(1.0, float(c.get('pan', 0)))), 'duck_db': float(c.get('duck_db', 0)), 'label': c.get('label', os.path.basename(f))})
    if not cues:
        raise listen.InputError(f'{path}: no cues')
    return sorted(cues, key=lambda c: c['t'])


def duck_curve(length, windows):
    """gain per sample for the bed: 1 everywhere, dipped by each (start s, end s, dB) over eased 40 ms edges"""
    g = np.ones(length)
    ramp = int(0.04 * SR)
    for a, b, depth in windows:
        i0, i1 = max(0, int(a * SR)), min(length, int(b * SR))
        if i1 <= i0:
            continue
        lin = 10 ** (-depth / 20)
        shape = np.full(i1 - i0, lin)
        r = min(ramp, (i1 - i0) // 2)
        if r > 0:
            ease = 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, r))
            shape[:r] = 1 - (1 - lin) * ease
            shape[-r:] = 1 - (1 - lin) * ease[::-1]
        g[i0:i1] = np.minimum(g[i0:i1], shape)
    return g


_CACHE = {}


def sample_of(path):
    if path not in _CACHE:
        _CACHE[path] = listen.decode(path)
    return _CACHE[path]


def place(cues, length):
    """(effects buffer, report rows): each sample placed so that its alignment point lands on its cue time"""
    fx = np.zeros((length, 2))
    rows = []
    for c in cues:
        sample = sample_of(c['file'])
        off = alignment_offsets(sample)[c['align']]
        start = int(round((c['t'] - off) * SR))
        gain = 10 ** (c['gain_db'] / 20)
        angle = (c['pan'] + 1) * np.pi / 4
        pan = np.array([np.cos(angle), np.sin(angle)]) * np.sqrt(2) if c['pan'] else np.array([1.0, 1.0])
        s = sample * gain * pan
        a0 = max(0, -start)
        a1 = min(len(s), length - start)
        if a1 <= a0:
            rows.append({'label': c['label'], 't': c['t'], 'placed': False, 'why': 'falls outside the video'})
            continue
        fx[start + a0:start + a1] += s[a0:a1]
        rows.append({'label': c['label'], 't': round(c['t'], 3), 'align': c['align'], 'starts_at': round(start / SR, 4),
                     'point_in_sample_s': round(off, 4), 'cut_head_s': round(a0 / SR, 4), 'placed': True, 'end_at': round((start + a1) / SR, 3),
                     'duck': (max(0.0, start / SR - 0.05), (start + a1) / SR, c['duck_db']) if c['duck_db'] else None})
    return fx, rows


def measured_point(buf, align, t):
    """where the placed sound's attack or peak sits in a solo render, measured again from the audio alone:
    onset = the first 2 ms frame within 20 dB of the local peak, peak = the loudest 10 ms (seconds), None when silent"""
    mono = buf.mean(axis=1)
    a, b = max(0, int((t - 0.3) * SR)), min(len(mono), int((t + 1.5) * SR))
    seg = mono[a:b]
    if not len(seg) or np.abs(seg).max() < 1e-6:
        return None
    if align == 'peak':
        h = int(0.01 * SR)
        env = np.sqrt(np.convolve(seg ** 2, np.ones(h) / h, mode='same'))
        return (a + int(np.argmax(env))) / SR
    if align == 'end':
        nz = np.where(np.abs(seg) > 1e-4 * np.abs(seg).max())[0]
        return (a + int(nz[-1]) + 1) / SR
    h = int(0.002 * SR)
    n = len(seg) // h
    env = 20 * np.log10(np.sqrt((seg[: n * h].reshape(n, h) ** 2).mean(axis=1)) + 1e-9)
    return (a + int(np.argmax(env >= env.max() - 20)) * h) / SR if align == 'onset' else (a + int(np.argmax(np.abs(seg) > 1e-4 * np.abs(seg).max()))) / SR


def verify(cues, rows, length, tol=0.005):
    """each cue is rendered alone and measured again: its attack (or peak, or end) must sit within `tol` of its time;
    sounds that overlap a neighbour within 40 ms are listed, since their attacks mask each other in the mix"""
    ok = True
    for c, r in zip(cues, rows):
        if not r.get('placed'):
            ok = False
            continue
        solo, _ = place([c], length)
        got = measured_point(solo, c['align'], c['t'])
        r['landed_ms'] = None if got is None else round((got - c['t']) * 1000, 1)
        r['on_time'] = got is not None and abs(got - c['t']) <= tol + (0.005 if c['align'] == 'peak' else 0)
        ok = ok and r['on_time']
    stamps = sorted((c['t'], c['label']) for c in cues)
    for (t0, l0), (t1, l1) in zip(stamps, stamps[1:]):
        if t1 - t0 < 0.04:
            for r in rows:
                if r['label'] in (l0, l1):
                    r.setdefault('masks', []).append(f'{l0} / {l1} {round((t1 - t0) * 1000)} ms apart')
    return ok


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0], formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--video', required=True)
    ap.add_argument('--cues', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--keep-audio', action='store_true', help="mix with the video's own sound")
    ap.add_argument('--bed', help='mix with this audio file instead (music, ambience)')
    ap.add_argument('--target-lufs', type=float, help='normalise the whole mix to this integrated loudness')
    ap.add_argument('--ceiling', type=float, default=-1.0, help='true-peak ceiling in dBTP (default -1)')
    ap.add_argument('--stem', help='also write the effects alone to this WAV')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args(argv)
    try:
        info = listen.probe(args.video)
        if not info['has_video']:
            raise listen.InputError(f'{args.video}: it has no picture')
        length = int(round(info['duration'] * SR))
        cues = load_cues(args.cues)
        fx, rows = place(cues, length)
        bed = np.zeros((length, 2))
        if args.bed:
            b = listen.decode(args.bed)[:length]
            bed[:len(b)] = b
        elif args.keep_audio and info['has_audio']:
            b = listen.decode(args.video)[:length]
            bed[:len(b)] = b
        windows = [r['duck'] for r in rows if r.get('duck')]
        if windows:
            bed = bed * duck_curve(length, windows)[:, None]
        mix = bed + fx
        with tempfile.TemporaryDirectory() as tmp:
            if args.stem:
                write_wav(fx, args.stem)
            ok = verify(cues, rows, length)
            gain_note = None
            if args.target_lufs is not None:
                cur = listen.integrated_lufs(kweight(mix))
                mix = mix * 10 ** ((args.target_lufs - cur) / 20)
                gain_note = round(args.target_lufs - cur, 2)
            mix_path = os.path.join(tmp, 'mix.wav')
            margin = 0.6
            for _ in range(5):
                write_wav(limit(mix, args.ceiling - margin), mix_path)
                tp = listen.true_peak_dbtp(mix_path)
                if tp > args.ceiling + 0.05:
                    mix = mix * 10 ** ((args.ceiling - 0.2 - tp) / 20)
                    continue
                mux(args.video, mix_path, args.out)
                final_tp = listen.true_peak_dbtp(args.out)
                if final_tp <= args.ceiling + 0.05:
                    break
                margin += final_tp - args.ceiling + 0.2   # the AAC encode overshot the limiter; leave more room
        result = {'out': args.out, 'cues': rows, 'all_on_time': ok, 'gain_to_target_db': gain_note, 'true_peak_dbtp': round(final_tp, 1),
                  'lufs_i': round(listen.integrated_lufs(listen.decode(args.out, weighted=True)), 1)}
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            late = [r for r in rows if not r.get('on_time', r.get('placed'))]
            print(f'{args.out}: {len(rows)} sounds placed, {result["lufs_i"]} LUFS, true peak {result["true_peak_dbtp"]} dBTP; '
                  + ('every sound measured within its alignment tolerance (5 ms, or 10 ms for peak) when played alone' if ok else f'{len(late)} off time: ' + ', '.join(r['label'] for r in late)))
        return 0 if ok else 1
    except listen.InputError as e:
        print(f'place_sfx: error: {e}', file=sys.stderr)
        return 3


def limit(x, ceiling_db):
    """a look-ahead peak limiter (FFmpeg alimiter) so a peaky effects mix can reach its loudness target"""
    lin = 10 ** (ceiling_db / 20)
    p = subprocess.run(['ffmpeg', '-v', 'error', '-nostdin', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', '-af',
                        f'alimiter=limit={lin:.4f}:attack=3:release=80:level=disabled', '-f', 'f32le', '-'],
                       input=np.clip(x, -4, 4).astype(np.float32).tobytes(), capture_output=True)
    if p.returncode != 0 or not p.stdout:
        return x
    return np.frombuffer(p.stdout, np.float32).reshape(-1, 2).astype(np.float64)


def kweight(x):
    p = subprocess.run(['ffmpeg', '-v', 'error', '-nostdin', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', '-af', listen.KWEIGHT, '-f', 'f32le', '-'],
                       input=x.astype(np.float32).tobytes(), capture_output=True)
    return np.frombuffer(p.stdout, np.float32).reshape(-1, 2).astype(np.float64)


def write_wav(x, path):
    p = subprocess.run(['ffmpeg', '-v', 'error', '-y', '-nostdin', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', '-c:a', 'pcm_f32le', path],
                       input=np.clip(x, -4, 4).astype(np.float32).tobytes(), capture_output=True)
    if p.returncode != 0:
        raise listen.InputError(f'FFmpeg could not write {path}: {p.stderr.decode(errors="replace")[-160:]}')


def mux(video, wav, out):
    p = subprocess.run(['ffmpeg', '-v', 'error', '-y', '-nostdin', '-i', video, '-i', wav, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                        '-c:a', 'aac', '-b:a', '192k', '-shortest', out], capture_output=True)
    if p.returncode != 0:
        raise listen.InputError(f'FFmpeg could not write {out}: {p.stderr.decode(errors="replace")[-160:]}')


if __name__ == '__main__':
    sys.exit(main())
