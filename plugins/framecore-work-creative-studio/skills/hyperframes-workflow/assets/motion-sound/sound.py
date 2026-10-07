#!/usr/bin/env python3
"""FrameCore Works motion sound design: plan sound cues from a motion contract, mix them, check the timing.

The cues come from the same timing as the picture: the Python renderer's port of the scene engine
(../motion-render/render.py) computes when every line, item, card, tap, screen change, sweep and wipe
happens, and each event gets a sound from the bundled CC0 library (library.json) whose transient or peak
is placed exactly on that frame. Nothing is synthesized: every sound is a recording.

  python sound.py plan video.motion.json --out video-r2.motion.json [--density minimal|standard|rich] [--evidence "..."]
  python sound.py mix video.motion.json --video video.mp4 --out video-sound.mp4 [--wav mix.wav]
  python sound.py check mix.wav video.motion.json

Requires Python 3.8+ and ffmpeg (with the loudnorm filter for loudness); no Python packages. Keep this file
next to library.json, library/ and ../motion-render/render.py. Exit code: 0 done, 1 problems, 2 setup problem.
"""
import argparse
import array
import importlib.util
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
RATE = 48000
REFERENCE_DB = -20.0
DENSITIES = ('minimal', 'standard', 'rich')
DEFAULT_GAIN = {'whoosh': -4, 'thud': -2, 'knock': -10, 'ting': -10, 'click': -4, 'release': -12, 'tick': -16, 'switch': -8, 'scroll': -14}


def load_engine():
    """The Python port of the scene engine, so cues use exactly the picture's timing."""
    for path in (os.path.join(HERE, '..', 'motion-render', 'render.py'), os.path.join(HERE, 'render.py')):
        if os.path.exists(path):
            sys.dont_write_bytecode = True
            spec = importlib.util.spec_from_file_location('studio_render', path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
    raise RuntimeError('render.py (the motion renderer) must sit in ../motion-render/ or next to sound.py')


def load_library(path=None):
    path = path or os.path.join(HERE, 'library.json')
    with open(path, encoding='utf-8') as handle:
        library = json.load(handle)
    library['_dir'] = os.path.dirname(os.path.abspath(path))
    return library


# ---------------------------------------------------------------- planning

def first_frame(start, end, test):
    """The first frame in [start, end) for which test(frame) holds, or None."""
    for frame in range(start, end):
        if test(frame):
            return frame
    return None


def plan_cues(score, density='standard'):
    """Sound cues for every visible event, as [{frame, sound, gain, pan, event}], in frame order."""
    if density not in DENSITIES:
        raise ValueError(f'density must be one of {", ".join(DENSITIES)}')
    r = load_engine()
    level = DENSITIES.index(density)
    m, fps_num, total = r.motion(score), score['fps'], score['totalFrames']
    cues = []

    def add(frame, sound, event, gain=None, pan=0.0, at_least=0):
        if level >= at_least and frame is not None and 0 <= frame < total:
            cues.append({'frame': int(frame), 'sound': sound, 'gain': DEFAULT_GAIN[sound] if gain is None else gain, 'pan': round(pan, 2), 'event': event})

    def landed(start, duration, easing, end, limit=0.9):
        return first_frame(start, end, lambda f: r.progress(f, start, duration, easing) >= limit)

    scenes = score['scenes']
    for index, scene in enumerate(scenes):
        p, sid, start, end = scene.get('params') or {}, scene['id'], scene['start'], scene['end']
        mode = r.exit_mode(scene, score)
        previous = scenes[index - 1] if index else None
        # Scene changes: a wipe of the scene's canvas, else a whoosh on the entry unless a sweep already covers it.
        wipe = p.get('backgroundWipe', 'none') if p.get('background') else 'none'
        if wipe != 'none':
            pan = {'left': -0.5, 'right': 0.5, 'up': 0.0, 'down': 0.0}[wipe]
            add(start + p.get('backgroundFrames', 12) // 2, 'whoosh', f'{sid}: canvas wipes in from the {wipe}', -2, pan)
        elif previous is not None and r.exit_mode(previous, score) != 'sweep' and start > 0:
            add(start + 1, 'whoosh', f'{sid}: scene enters', -6)
        if mode == 'sweep':
            sweep = p.get('sweepFrames', m['exitFrames'] + 12)
            add(end - sweep + sweep // 2, 'whoosh', f'{sid}: line sweeps across', -2)
        elif mode == 'lift':
            add(end - m['exitFrames'], 'whoosh', f'{sid}: content lifts out', -16, at_least=2)
        kind = scene['kind']
        if kind == 'line-reveal':
            for i, _ in enumerate(r.as_list(p.get('lines'))):
                begin = start + i * m['lineStaggerFrames']
                add(landed(begin, m['entryFrames'], m['entryEasing'], end), 'knock', f'{sid}: line {i + 1} lands', -10 - 3 * i, at_least=1)
        elif kind == 'item-stagger':
            items = r.as_list(p.get('items'))
            for i, _ in enumerate(items):
                begin = start + i * m['itemStaggerFrames']
                add(landed(begin, m['entryFrames'], m['entryEasing'], end), 'knock', f'{sid}: item {i + 1} lands', -8 - min(4, i), (i - (len(items) - 1) / 2) * 0.25, at_least=1)
            if p.get('connector', True) is not False:
                add(start + 6, 'scroll', f'{sid}: connector grows', at_least=2)
        elif kind == 'end-card':
            frame = landed(start, p.get('duration', 30), m['resolveEasing'], end)
            add(frame, 'thud', f'{sid}: end card settles')
            add(frame, 'ting', f'{sid}: end card accent', -14, at_least=2)
        elif kind == 'counter':
            count_start, duration = start + m['entryFrames'], p.get('duration', 45)
            last_text, step = None, -10 ** 6
            for frame in range(count_start, min(end, count_start + duration)):
                k = r.progress(frame, count_start, duration, p.get('easing', 'easeOutCubic'))
                text = r.number_text(p, p.get('from', 0) + (p.get('to', 0) - p.get('from', 0)) * k)
                # A tick when the shown number changes, at most every 4 frames, quieter as the count slows.
                if text != last_text and frame - step >= 4:
                    add(frame, 'tick', f'{sid}: number changes', -14 - round(6 * k), at_least=1)
                    step = frame
                last_text = text
            add(min(end - 1, count_start + duration), 'ting', f'{sid}: final value', -8)
        elif kind == 'quote':
            add(landed(start, m['entryFrames'] + 5, m['entryEasing'], end), 'knock', f'{sid}: quote lands', -10, at_least=1)
            if p.get('attribution'):
                begin = start + p.get('attributionDelay', 30)
                add(landed(begin, m['entryFrames'], m['entryEasing'], end), 'knock', f'{sid}: attribution lands', -14, at_least=2)
        elif kind == 'logo-reveal':
            add(start, 'whoosh', f'{sid}: mark opens', -8)
            frame = landed(start, p.get('duration', 30), m['resolveEasing'], end)
            add(frame, 'thud', f'{sid}: mark settles')
            add(frame, 'ting', f'{sid}: mark accent', -12, at_least=2)
        elif kind == 'device':
            add(landed(start, m['entryFrames'] + 10, m['resolveEasing'], end), 'thud', f'{sid}: device settles', -12, at_least=1)
            shots, mode_screen, tf = r.as_list(p.get('screens')), p.get('transition', 'push'), p.get('transitionFrames', 12)
            for i, shot in enumerate(shots[1:], 1):
                at = start + shot.get('at', 0)
                if mode_screen == 'push':
                    add(at + tf // 2, 'whoosh', f'{sid}: screen {i + 1} pushes in', -12, 0.3, at_least=1)
                elif mode_screen == 'fade':
                    add(at, 'switch', f'{sid}: screen {i + 1} fades in', -14, at_least=1)
            for i, tap in enumerate(r.as_list(p.get('taps'))):
                at = start + tap.get('at', 0)
                pan = (tap.get('x', 0.5) - 0.5) * 0.6
                add(at, 'click', f'{sid}: tap {i + 1}', pan=pan)
                add(at + 4, 'release', f'{sid}: tap {i + 1} releases', pan=pan, at_least=1)
            for i, key in enumerate(r.as_list(p.get('focus'))):
                add(start + key.get('at', 0) + key.get('frames', 24) // 2, 'whoosh', f'{sid}: camera moves {i + 1}', -18, at_least=2)
            for i, _ in enumerate(r.as_list(p.get('caption'))):
                begin = start + 10 + i * m['lineStaggerFrames']
                add(landed(begin, m['entryFrames'], m['entryEasing'], end), 'knock', f'{sid}: caption line {i + 1} lands', -12 - 3 * i, at_least=1)
    # Keep one cue per family within two frames (the louder one), so nothing doubles or machine-guns.
    cues.sort(key=lambda cue: (cue['frame'], -cue['gain']))
    kept = []
    for cue in cues:
        clash = next((c for c in kept if c['sound'] == cue['sound'] and abs(c['frame'] - cue['frame']) <= 2), None)
        if clash is None:
            kept.append(cue)
    return sorted(kept, key=lambda cue: (cue['frame'], cue['sound']))


def cue_table(score, cues):
    fps = score['fps']['num'] / score['fps']['den']
    rows = ['| Frame | Time | Sound | Gain | Pan | Event |', '| ---: | ---: | --- | ---: | ---: | --- |']
    rows += [f"| {c['frame']} | {c['frame'] / fps:.2f} s | {c['sound']} | {c['gain']} dB | {c['pan']} | {c.get('event', '')} |" for c in cues]
    return '\n'.join(rows) + '\n'


# ---------------------------------------------------------------- mixing

def decode(path, channels=2):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', str(channels), '-ar', str(RATE), '-f', 'f32le', '-'],
                         check=True, capture_output=True).stdout
    samples = array.array('f')
    samples.frombytes(raw)
    return samples


def choose(library, cues):
    """Resolve each cue to a recording: an exact id, or the family's variants in turn (round robin, no randomness)."""
    by_id = {s['id']: s for s in library['sounds']}
    families = {}
    for sound in library['sounds']:
        families.setdefault(sound['family'], []).append(sound)
    turn, chosen = {}, []
    for cue in cues:
        name = cue['sound']
        if name in by_id:
            chosen.append(by_id[name])
        elif name in families:
            variants = families[name]
            chosen.append(variants[turn.get(name, 0) % len(variants)])
            turn[name] = turn.get(name, 0) + 1
        else:
            raise ValueError(f'Unknown sound {name}; use a family ({", ".join(families)}) or a sound id from library.json')
    return chosen


def align_ms(sound):
    return sound['peak_ms'] if sound.get('align') == 'peak' else sound['onset_ms']


def mix(score, base_dir, library, cues):
    """The stereo mix as interleaved float samples, and the start sample of every cue's audible hit."""
    fps = score['fps']['num'] / score['fps']['den']
    length = round(score['totalFrames'] / fps * RATE)
    out = array.array('f', bytes(8 * length))
    cache, hits = {}, []
    for cue, sound in zip(cues, choose(library, cues)):
        if sound['file'] not in cache:
            cache[sound['file']] = decode(os.path.join(library['_dir'], sound['file']))
        data = cache[sound['file']]
        hit = round(cue['frame'] / fps * RATE)
        start = hit - round(align_ms(sound) / 1000 * RATE)
        gain = 10 ** ((REFERENCE_DB + cue.get('gain', 0) - sound['level_db']) / 20)
        theta = (max(-1.0, min(1.0, cue.get('pan', 0))) + 1) * math.pi / 4
        left, right = gain * math.cos(theta) * math.sqrt(2), gain * math.sin(theta) * math.sqrt(2)
        for i in range(0, len(data) // 2):
            n = start + i
            if n < 0:
                continue
            if n >= length:
                break
            out[2 * n] += data[2 * i] * left
            out[2 * n + 1] += data[2 * i + 1] * right
        hits.append(hit)
    for key, duck_db in (('music', -8.0), ('voiceover', 0.0)):
        source = (score.get(key) or {}).get('src')
        if not source:
            continue
        path = os.path.join(base_dir, source)
        if not os.path.exists(path):
            raise RuntimeError(f'{key}.src {source} not found next to the contract')
        data, volume = decode(path), float((score.get(key) or {}).get('volume', 1))
        spans = [(round(c['start'] / fps * RATE), round(c['end'] / fps * RATE)) for c in score.get('captions') or []] if key == 'music' and (score.get('voiceover') or {}).get('src') else []
        ramp = RATE // 10
        for i in range(0, min(len(data) // 2, length)):
            g = volume
            if spans:
                # Duck the music under the voice-over's caption intervals, with 100 ms ramps.
                inside = max((min(1.0, (i - a + ramp) / ramp, (b + ramp - i) / ramp) for a, b in spans if a - ramp <= i < b + ramp), default=0.0)
                g *= 10 ** (duck_db * max(0.0, inside) / 20)
            out[2 * i] += data[2 * i] * g
            out[2 * i + 1] += data[2 * i + 1] * g
    return out, hits


def loudness(path):
    """Integrated loudness and true peak from ffmpeg's loudnorm analysis, or None without that filter."""
    run = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', path, '-af', 'loudnorm=I=-16:TP=-1.5:print_format=json', '-f', 'null', '-'],
                         capture_output=True, text=True)
    found = re.search(r'\{[^{}]*"input_i"[^{}]*\}', run.stderr)
    if run.returncode != 0 or not found:
        return None
    data = json.loads(found.group(0))
    return float(data['input_i']), float(data['input_tp'])


def write_mix(samples, path, target_lufs=-16.0, true_peak=-1.5):
    """Write a 48 kHz stereo WAV, linearly gained to the target loudness without passing the true-peak ceiling."""
    with tempfile.TemporaryDirectory() as tmp:
        raw, probe = os.path.join(tmp, 'mix.f32'), os.path.join(tmp, 'probe.wav')
        with open(raw, 'wb') as handle:
            samples.tofile(handle)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(RATE), '-ac', '2', '-i', raw, '-c:a', 'pcm_f32le', probe], check=True)
        measured = loudness(probe)
        if measured:
            integrated, peak = measured
            gain = min(target_lufs - integrated, true_peak - peak) if integrated > -70 else 0.0
            note = {'input_lufs': integrated, 'input_true_peak': peak, 'gain_db': round(gain, 2), 'method': 'loudnorm analysis, linear gain'}
        else:
            peak = max((abs(v) for v in samples), default=0.0)
            gain = (true_peak - 20 * math.log10(peak)) if peak > 0 else 0.0
            note = {'gain_db': round(gain, 2), 'method': 'sample peak (ffmpeg has no loudnorm filter)'}
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', probe, '-af', f'volume={gain:.4f}dB', '-c:a', 'pcm_s24le', path], check=True)
    after = loudness(path)
    if after:
        note.update(output_lufs=after[0], output_true_peak=after[1])
    return note


# ---------------------------------------------------------------- checking

def check(wav, score, library, cues):
    """Find each cue's audible hit in a mix (the first sample above half the local peak) and its offset from the frame."""
    fps = score['fps']['num'] / score['fps']['den']
    data = decode(wav, channels=1)
    report, chosen = [], choose(library, cues)
    hits = [round(c['frame'] / fps * RATE) for c in cues]
    for index, (cue, sound) in enumerate(zip(cues, chosen)):
        expected = round(cue['frame'] / fps * RATE)
        before = round(align_ms(sound) / 1000 * RATE) + RATE // 200
        lo, hi = max(0, expected - before), min(len(data), expected + RATE // 50)
        window = data[lo:hi]
        if not window:
            continue
        if sound.get('align') == 'peak':
            size = RATE // 100
            energies = [sum(v * v for v in window[i:i + size]) for i in range(0, max(1, len(window) - size), size // 2)]
            found = lo + max(range(len(energies)), key=energies.__getitem__) * (size // 2) + size // 2 if energies else lo
            tolerance = 10.0
        else:
            peak = max(abs(v) for v in window)
            found = lo + next((i for i, v in enumerate(window) if abs(v) >= 0.5 * peak), 0)
            tolerance = 2.0
        offset = (found - expected) / RATE * 1000
        # Another cue within 50 ms masks this one in the mix; report it without judging it.
        masked = any(j != index and abs(h - expected) <= RATE // 20 for j, h in enumerate(hits))
        report.append({'frame': cue['frame'], 'sound': sound['id'], 'offset_ms': round(offset, 2), 'ok': True if masked else abs(offset) <= tolerance, 'masked': masked})
    return report


# ---------------------------------------------------------------- command line

def next_revision(score, evidence):
    revision = (score.get('revision') or 0) + 1
    out = dict(score, revision=revision)
    out['approval'] = {'status': 'approved', 'revision': revision, 'evidence': evidence} if evidence else {'status': 'proposed', 'revision': None, 'evidence': None}
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(description='Plan, mix and check motion sound design.')
    sub = parser.add_subparsers(dest='command', required=True)
    plan = sub.add_parser('plan', help='write the contract with an sfx cue list')
    plan.add_argument('contract')
    plan.add_argument('--out', required=True)
    plan.add_argument('--density', default='standard', choices=DENSITIES)
    plan.add_argument('--evidence', help="the user's request, quoted, when it approves the sound design")
    plan.add_argument('--table', help='also write the cue table as Markdown')
    do_mix = sub.add_parser('mix', help='mix the cues (and music or voice-over) and mux them into a video')
    do_mix.add_argument('contract')
    do_mix.add_argument('--video', help='the rendered MP4; the picture is copied unchanged')
    do_mix.add_argument('--out', help='output MP4 (needs --video)')
    do_mix.add_argument('--wav', help='also write the mix as WAV')
    do_mix.add_argument('--library')
    do_mix.add_argument('--lufs', type=float, default=-16.0)
    test = sub.add_parser('check', help='measure where each cue lands in a mix')
    test.add_argument('wav')
    test.add_argument('contract')
    test.add_argument('--library')
    args = parser.parse_args(argv)
    try:
        with open(args.contract, encoding='utf-8') as handle:
            score = json.load(handle)
        if args.command == 'plan':
            if os.path.exists(args.out):
                raise ValueError(f'Output file already exists: {args.out}')
            cues = plan_cues(score, args.density)
            result = next_revision(score, args.evidence)
            result['soundDesign'] = {'library': 'studio-cc0-1', 'density': args.density, 'status': 'planned'}
            result['sfx'] = cues
            with open(args.out, 'w', encoding='utf-8') as handle:
                handle.write(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
            if args.table:
                with open(args.table, 'w', encoding='utf-8') as handle:
                    handle.write(cue_table(score, cues))
            counts = {}
            for cue in cues:
                counts[cue['sound']] = counts.get(cue['sound'], 0) + 1
            print(json.dumps({'cues': len(cues), 'by_sound': counts, 'density': args.density, 'out': args.out}))
            return 0
        library = load_library(args.library)
        cues = score.get('sfx') or []
        if args.command == 'check':
            report = check(args.wav, score, library, cues)
            worst = max((abs(r['offset_ms']) for r in report if not r['masked']), default=0.0)
            print(json.dumps({'cues': len(report), 'masked': sum(r['masked'] for r in report), 'max_offset_ms': worst, 'all_ok': all(r['ok'] for r in report), 'late_or_early': [r for r in report if not r['ok']]}))
            return 0 if all(r['ok'] for r in report) else 1
        if not shutil.which('ffmpeg'):
            raise RuntimeError('ffmpeg is required')
        if args.out and not args.video:
            raise ValueError('--out needs --video')
        for path in (args.out, args.wav):
            if path and os.path.exists(path):
                raise ValueError(f'Output file already exists: {path}')
        samples, _ = mix(score, os.path.dirname(os.path.abspath(args.contract)), library, cues)
        with tempfile.TemporaryDirectory() as tmp:
            wav = args.wav or os.path.join(tmp, 'mix.wav')
            note = write_mix(samples, wav, args.lufs)
            summary = {'cues': len(cues), 'loudness': note, 'wav': args.wav}
            if args.out:
                duration = score['totalFrames'] * score['fps']['den'] / score['fps']['num']
                subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', args.video, '-i', wav, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                                '-c:a', 'aac', '-b:a', '192k', '-t', f'{duration:.6f}', args.out], check=True)
                summary['out'] = args.out
        print(json.dumps(summary))
        return 0
    except (OSError, ValueError, RuntimeError, KeyError, subprocess.CalledProcessError) as error:
        sys.stderr.write(f'{error}\n')
        return 2


if __name__ == '__main__':
    sys.exit(main())
