#!/usr/bin/env python3
"""Ears for a film Studio made but cannot hear: measure, time-align, check and score sound with numbers, using only
NumPy and FFmpeg (Pillow draws the sheet).

  python listen.py measure film.mp4                       loudness, true peak, spectrum, stereo, onsets, tempo, key
  python listen.py timeline film.mp4 [--video v.mp4] [--cues cues.json]   what sounds when, next to the cuts
  python listen.py sync film.mp4 [--cues cues.json]        sound against every cut or cue: the ones with no sound
  python listen.py check hit.wav                          audit one sound: clicks, cut tail, clipping, DC, glide
  python listen.py critique film.mp4 [--profile p.json]   scorecard against launch-film ranges, with timed fixes
  python listen.py ab a.wav b.wav                         two sounds compared in numbers and words
  python listen.py profile refs/*.mp4 -o refs.json        your own reference ranges
  python listen.py sheet film.mp4 -o sheet.png            an annotated picture of the soundtrack
  python listen.py describe|match|rank|find|compare|realness|llm|forge|fit|sfx|kit|gallery|doctor|mcp ...
                                                          the models and the sound bank: the earshot extension

Every command prints a plain summary first; --json prints the whole result. Nothing here uses a model, so it
measures and never says what a sound "is": that is `describe` or `match` in the earshot extension, found by
`--earshot PATH`, the EARSHOT_BIN variable, ~/.framecore-studio/extensions/earshot/venv/bin/earshot or PATH.
Exit codes: 0 done, 1 a problem was found (critique or check), 3 bad input, 4 the earshot extension is needed.

Adapted from earshot by Leon Lin (MIT, notice in integrations/earshot/): its definitions of salient hits,
stop-downs, the picture-event detector, the launch scorecard and the sound audit, rewritten in Studio's own code
without SciPy, librosa or models. Where the two disagree, earshot's own numbers are the reference.
"""
import argparse
import json
import math
import os
import shutil
import subprocess
import sys

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view as windows

SR = 48000
HOP = 240                       # 5 ms analysis hop for onsets
BANDS = {'sub': (20, 60), 'low': (60, 250), 'lowmid': (250, 1000), 'mid': (1000, 4000),
         'presence': (4000, 8000), 'air': (8000, 16000), 'top': (16000, 24000)}
NOTES = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
KK_MAJ = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
KK_MIN = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
KWEIGHT = 'highshelf=f=1681.974:g=3.99984:t=q:w=0.7071752,highpass=f=38.13547:poles=2:t=q:w=0.5003270'
EARSHOT_COMMANDS = ('describe', 'match', 'rank', 'find', 'compare', 'realness', 'llm', 'forge', 'fit', 'sfx', 'kit',
                    'gallery', 'doctor', 'mcp')


class InputError(Exception):
    pass


def db(v, floor=1e-12):
    return 20 * math.log10(max(float(v), floor))


def run(cmd, **kw):
    try:
        return subprocess.run(cmd, capture_output=True, **kw)
    except FileNotFoundError:
        raise InputError(f'{cmd[0]} is not installed; this tool needs FFmpeg')


def probe(path):
    if not os.path.isfile(path):
        raise InputError(f'{path}: no such file')
    p = run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_type,codec_name,r_frame_rate,duration:format=duration',
             '-of', 'json', path])
    if p.returncode != 0:
        raise InputError(f'{path}: FFmpeg cannot read it ({p.stderr.decode(errors="replace").strip()[-160:]})')
    info = json.loads(p.stdout or '{}')
    streams = info.get('streams', [])
    audio = next((s for s in streams if s.get('codec_type') == 'audio'), None)
    video = next((s for s in streams if s.get('codec_type') == 'video'), None)
    fps = None
    if video and video.get('r_frame_rate', '0/0') != '0/0':
        a, b = video['r_frame_rate'].split('/')
        fps = float(a) / float(b) if float(b) else None
    return {'has_audio': audio is not None, 'has_video': video is not None, 'fps': fps,
            'codec': (audio or {}).get('codec_name'), 'lossy': (audio or {}).get('codec_name') in ('aac', 'mp3', 'opus', 'vorbis'),
            'duration': float(info.get('format', {}).get('duration') or 0)}


def decode(path, weighted=False, start=None, end=None):
    """float32 array (n, 2) at 48 kHz; mono sources are duplicated, K-weighted for loudness work on request"""
    cmd = ['ffmpeg', '-v', 'error', '-nostdin']
    if start:
        cmd += ['-ss', str(start)]
    if end:
        cmd += ['-to', str(end)]
    cmd += ['-i', path, '-vn', '-ac', '2', '-ar', str(SR)]
    if weighted:
        cmd += ['-af', KWEIGHT]
    cmd += ['-f', 'f32le', '-']
    p = run(cmd)
    if p.returncode != 0 or not p.stdout:
        raise InputError(f'{path}: no audio could be decoded ({p.stderr.decode(errors="replace").strip()[-160:]})')
    x = np.frombuffer(p.stdout, np.float32)
    return x[: len(x) // 2 * 2].reshape(-1, 2).astype(np.float64)


def true_peak_dbtp(path):
    """peak of the 4x oversampled signal (FFmpeg resamples to 192 kHz), read in chunks"""
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-nostdin', '-i', path, '-vn', '-ac', '2', '-af', 'aresample=192000',
                          '-f', 'f32le', '-'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    peak = 0.0
    while True:
        chunk = p.stdout.read(1 << 24)
        if not chunk:
            break
        a = np.frombuffer(chunk[: len(chunk) // 4 * 4], np.float32)
        if len(a):
            peak = max(peak, float(np.abs(a).max()))
    p.wait()
    return db(peak)


def loudness_curve(kx, win, hop):
    """(centres, LUFS) of sliding blocks of K-weighted audio: win 0.4 momentary, 3.0 short-term"""
    w, h = int(win * SR), int(hop * SR)
    p = np.cumsum(np.concatenate([np.zeros((1, 2)), kx ** 2]), axis=0)
    if len(kx) < w:
        ms = (p[-1] - p[0]) / max(1, len(kx))
        return np.array([len(kx) / SR / 2]), np.array([-0.691 + 10 * np.log10(ms.sum() + 1e-20)])
    st = np.arange(0, len(kx) - w + 1, h)
    ms = (p[st + w] - p[st]) / w
    return (st + w / 2) / SR, -0.691 + 10 * np.log10(ms.sum(axis=1) + 1e-20)


def energy_mean(levels):
    levels = np.asarray(levels, float)
    return float(10 * np.log10(np.mean(10 ** (levels / 10)))) if len(levels) else None


def integrated_lufs(kx):
    _, level = loudness_curve(kx, 0.4, 0.1)
    level = level[level > -70]
    if not len(level):
        return -70.0
    rel = energy_mean(level) - 10
    kept = level[level > rel]
    return float(energy_mean(kept)) if len(kept) else float(rel + 10)


def lra(kx):
    _, short = loudness_curve(kx, 3.0, 0.1)
    short = short[short > -70]
    if len(short) < 2:
        return 0.0
    rel = energy_mean(short) - 20
    kept = short[short > rel]
    return float(np.percentile(kept, 95) - np.percentile(kept, 10)) if len(kept) > 1 else 0.0


def stft_power(mono, n_fft=4096, hop=2048):
    if len(mono) < n_fft:
        mono = np.concatenate([mono, np.zeros(n_fft - len(mono))])
    frames = windows(mono, n_fft)[::hop] * np.hanning(n_fft)
    return np.abs(np.fft.rfft(frames, axis=1)) ** 2


def key_of(mono):
    """the key by Krumhansl-Schmuckler correlation of a chroma vector built from 55 Hz to 2 kHz"""
    power = stft_power(mono[: SR * 120], 8192, 4096).sum(axis=0)
    freqs = np.fft.rfftfreq(8192, 1 / SR)
    sel = (freqs >= 55) & (freqs <= 2000)
    pitch = np.round(12 * np.log2(freqs[sel] / 440.0) + 69).astype(int) % 12
    chroma = np.bincount(pitch, weights=power[sel], minlength=12)
    if chroma.sum() <= 0:
        return None, 0.0
    best = (None, -2.0)
    for mode, prof in (('major', KK_MAJ), ('minor', KK_MIN)):
        for k in range(12):
            r = float(np.corrcoef(chroma, np.roll(prof, k))[0, 1])
            if r > best[1]:
                best = (f'{NOTES[k]} {mode}', r)
    return best


def onset_envelope(mono):
    """half-wave rectified log-spectral flux, one value per 5 ms"""
    n_fft = 1024
    padded = np.concatenate([np.zeros(n_fft // 2), mono, np.zeros(n_fft)])
    frames = windows(padded, n_fft)[::HOP] * np.hanning(n_fft)
    mag = np.log1p(30 * np.abs(np.fft.rfft(frames, axis=1)))
    flux = np.maximum(0.0, np.diff(mag, axis=0, prepend=mag[:1])).sum(axis=1)
    return flux


def smooth(v, n):
    return np.convolve(v, np.ones(n) / n, mode='same') if n > 1 else v


def level_2ms(mono):
    h = int(0.002 * SR)
    n = len(mono) // h
    if n == 0:
        return np.array([-120.0])
    f = mono[: n * h].reshape(n, h)
    return 20 * np.log10(np.sqrt((f ** 2).mean(axis=1)) + 1e-9)


def attack_times(times, e2, h=0.002):
    """move onset times to the attack: the steepest rise of the 2 ms level between 60 ms before and 20 ms after"""
    out = []
    for t in times:
        a, b = max(1, int((t - 0.06) / h)), min(len(e2) - 1, int((t + 0.02) / h) + 1)
        if b - a < 2:
            out.append(float(t))
            continue
        out.append(round((a + int(np.argmax(e2[a:b + 1] - e2[a - 1:b]))) * h, 4))
    return np.array(out)


def detect_onsets(mono, min_gap=0.03, k=3.0):
    """onset times: peaks of the flux that stand k robust deviations above the surrounding 2 s, moved to the attack"""
    flux = onset_envelope(mono)
    if len(flux) < 8:
        return np.zeros(0), flux
    w = 400
    pad = np.pad(flux, w // 2, mode='edge')
    local = windows(pad, w + 1)[: len(flux)] if len(pad) > w else flux[None, :]
    med = np.median(local, axis=1)
    mad = np.median(np.abs(local - med[:, None]), axis=1) * 1.4826 + 1e-6
    z = (flux - med) / mad
    peaks = np.where((z > k) & (flux >= np.roll(flux, 1)) & (flux >= np.roll(flux, -1)))[0]
    times, last = [], -1.0
    for i in peaks:
        t = i * HOP / SR
        if t - last >= min_gap:
            times.append(t)
            last = t
    moved = attack_times(times, level_2ms(mono))
    keep = [t for i, t in enumerate(moved) if i == 0 or t - moved[i - 1] >= min_gap]   # two onsets can move onto one attack
    return np.array(keep), flux


def salient_hits(tf, lf, lufs, jump=6.0, rel=-8.0):
    """100 ms loudness jumps of at least `jump` dB within 80 ms that land within `rel` LU of the integrated level"""
    if len(lf) < 20:
        return np.zeros(0)
    h = float(tf[1] - tf[0])
    a, b = int(round(0.2 / h)), int(round(0.08 / h))
    n = len(lf)
    pre = windows(np.concatenate([np.full(a, lf[0]), lf]), a).min(axis=1)[:n]
    post = windows(np.concatenate([lf, np.full(b - 1, lf[-1])]), b).max(axis=1)[:n]
    idx = np.where((post - pre >= jump) & (post >= lufs + rel))[0]
    out = []
    for run_ in np.split(idx, np.where(np.diff(idx) > 2)[0] + 1) if len(idx) else []:
        t = float(tf[run_[0]]) + 0.03
        if not out or t - out[-1] > 0.1:
            out.append(t)
    return np.array(out)


def stopdowns(tf, lf, drop=10.0, back=3.0, min_s=0.15, max_s=1.5):
    """(start, length, depth) of short dips before a hit: at least `drop` dB under the median of the 2 s before"""
    if len(lf) < 3:
        return []
    h = float(tf[1] - tf[0])
    w = int(round(2.0 / h))
    if len(lf) <= w:
        return []
    ref = np.concatenate([np.full(w, np.nan), np.median(windows(lf, w), axis=1)[:len(lf) - w]])
    out, i, n = [], w, len(lf)
    while i < n:
        r = ref[i]
        if lf[i] < r - drop:
            j = i
            while j < n and lf[j] < r - drop:
                j += 1
            length = (j - i) * h
            if min_s <= length <= max_s and j < n and lf[j:j + int(round(0.3 / h)) + 1].max() >= r - back:
                out.append((round(float(tf[i]) - 0.05, 3), round(length, 3), round(float(r - lf[i:j].min()), 1)))
            i = j + int(round(0.5 / h))
        else:
            i += 1
    return out


def swells(tf, lf, min_rise=6.0, min_len=0.25):
    """peaks of slow build-ups (a whoosh or riser): a rise of at least `min_rise` dB over at least `min_len` s, then a fall"""
    h = float(tf[1] - tf[0])
    n = int(round(min_len / h))
    out = []
    for i in range(n, len(lf) - 1):
        if lf[i] >= lf[i - 1] and lf[i] > lf[i + 1] and lf[i] - lf[i - n:i].min() >= min_rise:
            t = float(tf[i])
            if not out or t - out[-1] > 0.3:
                out.append(t)
    return np.array(out)


def longest_run(mask):
    best = cur = 0
    for flag in mask:
        cur = cur + 1 if flag else 0
        best = max(best, cur)
    return best


def edge(e2, t, first=True, h=0.002):
    """refine the start or end of sound found on a 100 ms block: the first or last 2 ms frame within 20 dB of the block's loudest"""
    a, b = max(0, int((t - 0.05) / h)), min(len(e2), int((t + 0.05) / h) + 1)
    if b <= a:
        return max(0.0, t)
    ref = e2[a:min(len(e2), a + int(0.15 / h))].max() if first else e2[max(0, b - int(0.15 / h)):b].max()
    ok = np.where(e2[a:b] >= ref - 20)[0]
    if not len(ok):
        return max(0.0, t)
    return round((a + (ok[0] if first else ok[-1] + 1)) * h, 3)


def tempo_of(flux, lo=70, hi=180):
    """tempo by autocorrelation of the onset envelope, and the beat grid fitted to it"""
    if len(flux) < 400:
        return None, []
    env = flux - flux.mean()
    ac = np.correlate(env, env, 'full')[len(env) - 1:]
    fps = SR / HOP
    lags = np.arange(int(fps * 60 / hi), int(fps * 60 / lo) + 1)
    lags = lags[lags < len(ac)]
    if not len(lags):
        return None, []
    best = lags[int(np.argmax(ac[lags]))]
    half = best // 2
    if half in lags and ac[half] >= 0.85 * ac[best]:   # the pulse is as clear at double the tempo: take the faster, the felt tempo
        best = half
    bpm = 60 * fps / best
    clarity = float(ac[best] / (ac[0] + 1e-9))
    if clarity < 0.08:
        return None, []
    period = fps * 60 / bpm
    scores = [flux[np.round(np.arange(phase, len(flux), period)).astype(int)].sum() for phase in np.arange(0, period, 0.5)]
    phase = float(np.argmax(scores)) * 0.5
    beats = (np.arange(phase, len(flux), period) * HOP / SR).tolist()
    return round(float(bpm), 1), beats


def near_frac(events, targets, tol):
    events, targets = np.asarray(events, float), np.sort(np.asarray(targets, float))
    if not len(events):
        return None
    if not len(targets):
        return 0.0
    i = np.searchsorted(targets, events)
    d = np.minimum(np.abs(targets[np.clip(i, 0, len(targets) - 1)] - events),
                   np.abs(targets[np.clip(i - 1, 0, len(targets) - 1)] - events))
    return float(np.mean(d <= tol))


def chance_frac(events, targets, tol, dur, shifts=(0.37, 0.71, 1.13, 1.57, 2.03, 2.59, 3.11, 3.67)):
    events = np.asarray(events, float)
    if not len(events) or dur <= 0:
        return None
    return float(np.mean([near_frac((events + s) % dur, targets, tol) for s in shifts]))


def picture_events(path, ratio=4.0, floor=0.012, big=0.15, gap=0.12):
    """cuts and big picture changes: a frame-difference spike at least 4x the median around it, or a change of 15 % of grey"""
    info = probe(path)
    if not info['has_video']:
        return [], info['fps']
    w, h = 96, 54
    p = run(['ffmpeg', '-v', 'error', '-nostdin', '-i', path, '-an', '-vf', f'scale={w}:{h}:flags=area,format=gray',
             '-f', 'rawvideo', '-'])
    fr = np.frombuffer(p.stdout, np.uint8)
    fr = fr[: len(fr) // (w * h) * w * h].reshape(-1, h, w).astype(np.float32)
    if len(fr) < 3:
        return [], info['fps']
    d = np.concatenate([[0.0], np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2)) / 255])
    fps = info['fps'] or 30.0
    size = int(round(fps)) | 1
    med = np.median(windows(np.pad(d, size // 2, mode='edge'), size), axis=1)[:len(d)]
    loc = np.maximum(np.maximum(d, np.roll(d, 1)), np.roll(d, -1))
    out = []
    for i in np.where((d == loc) & (((d > floor) & (d > ratio * med + 0.004)) | (d >= big)))[0]:
        if i == 0:
            continue
        if out and i - out[-1] < gap * fps:
            if d[i] > d[out[-1]]:
                out[-1] = int(i)
            continue
        out.append(int(i))
    return [round(i / fps, 3) for i in out], fps


def read_cues(path):
    """cue times in seconds from a JSON file: a list of numbers, of {t} / {time} / {frame, fps} objects, or {cues: [...]}"""
    if not os.path.isfile(path):
        raise InputError(f'{path}: no such file')
    data = json.load(open(path, encoding='utf-8'))
    items = data.get('cues', data.get('events', data)) if isinstance(data, dict) else data
    out = []
    for c in items:
        if isinstance(c, (int, float)):
            out.append(float(c))
        elif isinstance(c, dict):
            if 't' in c:
                out.append(float(c['t']))
            elif 'time' in c:
                out.append(float(c['time']))
            elif 'frame' in c:
                out.append(float(c['frame']) / float(c.get('fps') or data.get('fps') or 30))
    if not out:
        raise InputError(f'{path}: no cue times found')
    return sorted(out)


def analyse(path, video=None, cues=None, start=None, end=None):
    """everything the commands share: levels, events, hits, beats and the picture events or cues to compare with"""
    info = probe(path)
    if not info['has_audio']:
        raise InputError(f'{path}: it has no audio track')
    x = decode(path, start=start, end=end)
    kx = decode(path, weighted=True, start=start, end=end)
    dur = len(x) / SR
    mono = x.mean(axis=1)
    a = {'path': path, 'info': info, 'duration': dur}
    a['lufs'] = integrated_lufs(kx)
    a['lra'] = lra(kx)
    a['tf'], a['lf'] = loudness_curve(kx, 0.1, 0.02)
    a['tm'], a['lm'] = loudness_curve(kx, 0.4, 0.1)
    a['ts'], a['ls'] = loudness_curve(kx, 3.0, 0.1)
    a['e2'] = level_2ms(mono)
    a['onsets'], flux = detect_onsets(mono)
    a['tempo'], a['beats'] = tempo_of(flux)
    a['hits'] = salient_hits(a['tf'], a['lf'], a['lufs'])
    a['stopdowns'] = stopdowns(a['tf'], a['lf'])
    a['swells'] = swells(a['tf'], a['lf'])
    a['x'], a['mono'] = x, mono
    if cues is not None:
        a['targets'], a['target_kind'], a['fps'] = list(cues), 'cue', None
    else:
        src = video or (path if info['has_video'] else None)
        if src:
            a['targets'], a['fps'] = picture_events(src)
            a['target_kind'] = 'cut'
            a['video'] = src
        else:
            a['targets'], a['target_kind'], a['fps'] = [], None, None
    if start:
        a['targets'] = [t - start for t in a['targets'] if start <= t <= (end or 1e9)]
    a['targets'] = [t for t in a['targets'] if 0 <= t < dur]
    return a


def measure_of(a, full=True):
    """the objective numbers of one analysed file"""
    x, mono, dur = a['x'], a['mono'], a['duration']
    lufs, tf, lf, tm, lm, ts, ls = a['lufs'], a['tf'], a['lf'], a['tm'], a['lm'], a['ts'], a['ls']
    m = {'duration_s': round(dur, 3), 'lufs_i': round(lufs, 1), 'lra': round(a['lra'], 1),
         'peak_dbfs': round(db(np.abs(x).max()), 1), 'rms_dbfs': round(db(np.sqrt((x ** 2).mean())), 1),
         'clipped_samples': int((np.abs(x) >= 0.999).sum()), 'dc': round(float(mono.mean()), 6)}
    m['true_peak'] = round(true_peak_dbtp(a['path']), 1) if full else None
    e20 = 20 * np.log10(np.sqrt(windows(mono, int(0.02 * SR))[::int(0.02 * SR)].__pow__(2).mean(axis=1)) + 1e-9) if len(mono) > int(0.02 * SR) else np.array([-120.0])
    m['noise_floor_dbfs'] = round(float(np.percentile(e20, 10)), 1)
    mid, side = (x[:, 0] + x[:, 1]) / 2, (x[:, 0] - x[:, 1]) / 2
    ms, ss = float((mid ** 2).mean()), float((side ** 2).mean())
    m['side_to_mid_db'] = None if ss < 1e-14 else round(10 * math.log10(ss / (ms + 1e-20)), 1)
    m['mono'] = ss < 1e-14
    m['correlation'] = round(float(np.corrcoef(x[:, 0], x[:, 1])[0, 1]), 2) if ss >= 1e-14 else 1.0
    power = stft_power(mono)
    freqs = np.fft.rfftfreq(4096, 1 / SR)
    total = power.sum() + 1e-20
    m['bands_db'] = {name: round(10 * math.log10(power[:, (freqs >= lo) & (freqs < hi)].sum() / total + 1e-20), 1)
                     for name, (lo, hi) in BANDS.items()}
    centroid = (np.sqrt(power) * freqs).sum(axis=1) / (np.sqrt(power).sum(axis=1) + 1e-20)   # magnitude-weighted: tracks perceived brightness
    active = power.sum(axis=1) > power.sum(axis=1).max() * 1e-4
    m['brightness_hz'] = int(np.median(centroid[active])) if active.any() else None
    m['onsets_per_s'] = round(len(a['onsets']) / dur, 2) if dur > 0 else None
    m['hits_per_s'] = round(len(a['hits']) / dur, 2) if dur > 0 else None
    m['tempo_bpm'] = a['tempo']
    key, r = key_of(mono) if dur >= 4 else (None, 0.0)
    m['key'] = key if r > 0.5 else None
    short = ls.max() - lufs if len(ls) > 1 else None
    m['crest_lu'] = None if short is None else round(float(short), 1)
    loud = np.where(lf > lufs - 20)[0]
    audible = np.where(lf > lufs - 30)[0]
    t_end = dur
    if len(loud):
        m['first_sound_s'] = edge(a['e2'], float(tf[loud[0]]), True)
    if len(audible):
        t_end = min(dur, edge(a['e2'], float(tf[audible[-1]]), False))
        m['end_silence_s'] = round(max(0.0, dur - t_end), 3)
        full_level = np.where((lm >= lufs - 6) & (tm <= t_end))[0]
        if len(full_level):
            m['fade_s'] = round(max(0.0, t_end - float(tm[full_level[-1]]) - 0.2), 2)
        first = m.get('first_sound_s') or 0.0
        inside = (tf >= first) & (tf <= t_end)
        m['max_gap_s'] = round(longest_run(lf[inside] < lufs - 30) * float(tf[1] - tf[0]), 2) if inside.sum() > 1 else 0.0
        last = (tm >= t_end - 3.0) & (tm <= t_end)
        if last.any():
            m['final_lu'] = round(float(lm[last].max()) - lufs, 1)
    if len(lm) > 2:
        m['intro_lu'] = round(energy_mean(lm[tm <= max(0.1 * dur, 0.5)]) - lufs, 1)
        m['end_lu'] = round(energy_mean(lm[tm >= dur - max(0.1 * dur, 0.5)]) - lufs, 1)
    if len(ls) > 1 and dur >= 6:
        m['peak_pos'] = round(float(ts[int(np.argmax(ls))]) / dur, 2)
    m['stopdowns_per_min'] = round(len(a['stopdowns']) / dur * 60, 1) if dur >= 6 else None
    return m


def sync_of(a, tol=0.1):
    """each cut or cue against the sound that answers it: offset in ms (sound minus picture), and a verdict"""
    fps = a.get('fps') or 30.0
    frame = max(0.04, 1.0 / fps + 0.006)
    onsets, hits, swl = a['onsets'], a['hits'], a['swells']
    tf, lf = a['tf'], a['lf']
    rows = []
    for t in a['targets']:
        row = {'t': round(t, 3)}
        d = onsets - t if len(onsets) else np.zeros(0)
        near = int(np.argmin(np.abs(d))) if len(d) else None
        if near is not None and abs(d[near]) <= tol:
            row.update(offset_ms=round(float(d[near]) * 1000), verdict='OK' if abs(d[near]) <= frame else 'near')
        elif len(swl) and np.min(np.abs(swl - t)) <= 0.3:
            row.update(offset_ms=round(float(swl[np.argmin(np.abs(swl - t))] - t) * 1000), verdict='swell')
        else:
            sel = (tf >= t - 0.15) & (tf <= t + 0.15)
            ref = (lf[(tf >= t - 0.6) & (tf < t - 0.2)] if ((tf >= t - 0.6) & (tf < t - 0.2)).any() else lf).mean()
            if sel.any() and lf[sel].max() - ref >= 3.0:
                row.update(offset_ms=None, verdict='peak')
            else:
                row.update(offset_ms=None, verdict='no sound')
        rows.append(row)
    targets = a['targets']
    out = {'rows': rows, 'tolerance_ms': int(tol * 1000), 'frame_ms': round(frame * 1000, 1)}
    if len(targets) >= 3:
        out['with_onset'] = round(near_frac(targets, onsets, tol), 2)
        out['with_onset_chance'] = round(chance_frac(targets, onsets, tol, a['duration']) or 0, 2)
        out['with_hit'] = round(near_frac(targets, a['hits'], tol), 2) if len(a['hits']) else 0.0
        out['on_frame'] = round(near_frac(targets, onsets, frame), 2)
        if a['beats']:
            out['on_beat'] = round(near_frac(targets, a['beats'], 0.07), 2)
    out['no_sound'] = [r['t'] for r in rows if r['verdict'] == 'no sound']
    out['no_new_attack'] = [r['t'] for r in rows if r['verdict'] in ('peak', 'swell', 'no sound')]
    return out


def fmt_t(t):
    return f'{int(t // 60)}:{t % 60:05.2f}'


def times(ts, k=8):
    s = ', '.join(fmt_t(t) for t in ts[:k])
    return s + (f' (+{len(ts) - k} more)' if len(ts) > k else '')


def measure_text(path, m):
    parts = [f'{os.path.basename(path)}: {m["duration_s"]} s, peak {m["peak_dbfs"]} dBFS'
             + (f' (true peak {m["true_peak"]} dBTP)' if m.get('true_peak') is not None else ''),
             f'{m["lufs_i"]} LUFS, LRA {m["lra"]} LU']
    if m.get('crest_lu') is not None:
        parts.append(f'loudest 3 s {m["crest_lu"]} LU above the average')
    if m.get('first_sound_s') is not None:
        parts.append(f'first sound {m["first_sound_s"]} s, {m.get("end_silence_s", 0)} s of silence at the end')
    if m.get('brightness_hz'):
        parts.append(f'brightness {m["brightness_hz"]} Hz')
    parts.append('bands ' + ' '.join(f'{k} {v}' for k, v in m['bands_db'].items()) + ' dB')
    if m['mono']:
        parts.append('mono (identical channels)')
    elif m.get('side_to_mid_db') is not None:
        parts.append(f'stereo: side {m["side_to_mid_db"]} dB under mid, correlation {m["correlation"]}')
    parts.append(f'{m["onsets_per_s"]} onsets/s, {m["hits_per_s"]} salient hits/s'
                 + (f', {m["tempo_bpm"]} BPM' if m.get('tempo_bpm') else '') + (f', {m["key"]}' if m.get('key') else ''))
    if m['clipped_samples']:
        parts.append(f'{m["clipped_samples"]} samples at full scale')
    return '; '.join(parts) + '.'


# the launch scorecard: key -> (weight, tolerance, sides, practice window, why it matters)
SPEC = {
    'lufs_i': (3, 1.0, 'both', (-16.0, -9.0), 'how loud the film plays next to other launch videos: autoplay on X, LinkedIn and websites does not normalise'),
    'true_peak': (2, 0.5, 'upper', (None, -1.0), 'a master above -1 dBTP clips once encoded to AAC or MP3 (decoded lossy audio above 0 dBTP already clips)'),
    'cuts_with_sound': (2, 0.05, 'lower', None, 'a cut or big visual change with no sound under it feels dead'),
    'lra': (2, 1.0, 'both', None, 'how much the loudness swings: launch films keep the body consistently strong'),
    'crest_lu': (2, 0.5, 'both', None, 'how far the loudest 3 s stick out above the average'),
    'first_sound_s': (2, 0.1, 'upper', None, 'silence at the start loses autoplay viewers'),
    'end_silence_s': (2, 0.25, 'upper', None, 'dead air after the sound stops makes the ending feel unfinished'),
    'max_gap_s': (2, 0.25, 'upper', None, 'a silent hole mid-film reads as a mistake unless it is a deliberate stop-down'),
    'final_lu': (2, 1.5, 'both', None, 'the logo or end-card moment should land at body level or above'),
    'onsets_per_s': (2, 0.3, 'both', None, 'rhythmic activity: too sparse feels empty, too dense feels cluttered'),
    'hits_per_s': (2, 0.2, 'both', None, 'punch: salient hits mark the key moments; without them nothing lands'),
    'intro_lu': (1, 1.5, 'both', None, 'how the film opens relative to its body'),
    'end_lu': (1, 1.5, 'both', None, 'how the last 10 % sit against the body'),
    'fade_s': (1, 0.5, 'both', None, 'launch films end on a sting or a hard out; long fade-outs lose the button'),
    'band_sub': (1, 1.5, 'both', None, 'sub weight (20-60 Hz)'), 'band_low': (1, 1.5, 'both', None, 'low-end body (60-250 Hz)'),
    'band_lowmid': (1, 1.5, 'both', None, 'low-mids (250 Hz-1 kHz): too much is muddy, too little hollow'),
    'band_mid': (1, 1.5, 'both', None, 'mids (1-4 kHz): where clicks and voice cut through phone speakers'),
    'band_presence': (1, 1.5, 'both', None, 'presence (4-8 kHz): the bite of transients'),
    'band_air': (1, 1.5, 'both', None, 'air (8-16 kHz): missing air sounds muffled or low-bitrate'),
    'side_to_mid_db': (1, 1.0, 'both', None, 'stereo width: near-mono sounds small'),
}
BAND_FIX = {
    'band_sub': ('thin bottom: add a sub layer (a sub drop under reveals) or music with real low end', 'too much 20-60 Hz rumble eats headroom: high-pass effects at 30-40 Hz and trim the music sub by 2-4 dB'),
    'band_low': ('weak low end: use a fuller bed or add a low layer', 'boomy: cut 100-200 Hz on the bed and heavy effects by 2-3 dB'),
    'band_lowmid': ('hollow: lift 250 Hz-1 kHz on the bed', 'muddy: cut 300-500 Hz on the bed and roomy effects by 2-3 dB'),
    'band_mid': ('recessed mids: clicks and voice will not cut through phone speakers; lift 1-3 kHz on effects', 'harsh mids: cut 1-3 kHz on the loudest layer by 2 dB'),
    'band_presence': ('dull: brighten the effects', 'harsh: cut 5-7 kHz on the brightest layer'),
    'band_air': ('no air: it sounds muffled; use full-band sources without a low-pass', 'fizzy: low-pass or de-noise the noisiest layer'),
}
# ranges of the seven launch films earshot measured (p10 / median / p90, min / max); a reference, not a law
LAUNCH = {
    'lufs_i': (-22.2, -14.8, -7.3), 'true_peak': (-0.8, 0.6, 2.0), 'lra': (1.7, 5.5, 12.2), 'crest_lu': (1.1, 2.3, 3.5),
    'first_sound_s': (0.04, 0.13, 0.48), 'end_silence_s': (0.02, 0.04, 1.9), 'max_gap_s': (0.0, 0.02, 1.66),
    'final_lu': (-2.2, 0.2, 5.6), 'onsets_per_s': (2.46, 5.66, 8.22), 'hits_per_s': (0.1, 1.25, 1.66),
    'intro_lu': (-17.5, -1.1, 2.2), 'end_lu': (-14.3, -3.0, -0.3), 'fade_s': (0.08, 0.27, 2.54),
    'band_sub': (-16.2, -6.6, -4.1), 'band_low': (-6.7, -4.2, -2.1), 'band_lowmid': (-16.8, -5.3, -1.7),
    'band_mid': (-19.1, -12.4, -10.5), 'band_presence': (-30.3, -17.8, -13.1), 'band_air': (-34.2, -23.6, -11.2),
    'side_to_mid_db': (-14.5, -8.5, -5.0), 'cuts_with_sound': (0.5, 0.81, 1.0),
}
UNITS = {'lufs_i': 'LUFS', 'true_peak': 'dBTP', 'lra': 'LU', 'crest_lu': 'LU', 'first_sound_s': 's', 'end_silence_s': 's',
         'max_gap_s': 's', 'final_lu': 'LU', 'onsets_per_s': '/s', 'hits_per_s': '/s', 'intro_lu': 'LU', 'end_lu': 'LU',
         'fade_s': 's', 'side_to_mid_db': 'dB', 'cuts_with_sound': 'share'}


def metric_values(m, sy):
    v = {k: m.get(k) for k in ('lufs_i', 'true_peak', 'lra', 'crest_lu', 'first_sound_s', 'end_silence_s', 'max_gap_s', 'final_lu',
                              'onsets_per_s', 'hits_per_s', 'intro_lu', 'end_lu', 'fade_s')}
    for b in ('sub', 'low', 'lowmid', 'mid', 'presence', 'air'):
        v['band_' + b] = m['bands_db'][b]
    v['side_to_mid_db'] = -40.0 if m['mono'] else m.get('side_to_mid_db')
    v['cuts_with_sound'] = sy.get('with_onset') if sy else None
    return v


def window_of(key, ref, lossy):
    weight, tol, sides, practice, _ = SPEC[key]
    if key == 'true_peak' and lossy:
        return None, 0.0
    if practice:
        return practice
    lo, med, hi = ref[key]
    lo, hi = round(lo - tol, 2), round(hi + tol, 2)
    if lo <= 0 and UNITS.get(key) in ('s', '/s', 'share'):
        lo = None
    return (lo if sides in ('both', 'lower') else None), (hi if sides in ('both', 'upper') else None)


def critique_of(a, m, sy, ref=None):
    ref = ref or LAUNCH
    lossy = bool(a['info']['lossy'])
    vals = metric_values(m, sy)
    rows, issues = [], []
    for key, (weight, tol, sides, practice, why) in SPEC.items():
        v = vals.get(key)
        lo, hi = window_of(key, ref, lossy) if key in ref or practice else (None, None)
        if v is None:
            status = 'n.a.'
        elif lo is not None and v < lo:
            status = 'low'
        elif hi is not None and v > hi:
            status = 'high'
        else:
            status = 'ok'
        rows.append({'key': key, 'value': v, 'low': lo, 'high': hi, 'median': ref.get(key, (None, None, None))[1] if key in ref else None,
                     'weight': {3: 'critical', 2: 'major', 1: 'minor'}[weight], 'status': status, 'why': why})
        if status in ('low', 'high'):
            issues.append((key, status, v, lo, hi, weight))
    scored = [r for r in rows if r['status'] != 'n.a.']
    got = sum({3: 3, 2: 2, 1: 1}[SPEC[r['key']][0]] for r in scored if r['status'] == 'ok')
    total = sum({3: 3, 2: 2, 1: 1}[SPEC[r['key']][0]] for r in scored) or 1
    share = got / total
    critical = any(w == 3 for *_, w in issues)
    verdict = ('launch-grade' if share >= 0.9 and not critical else 'close' if share >= 0.75 and not critical
               else 'needs work' if share >= 0.5 else 'not launch-grade')
    actions = []
    for key, status, v, lo, hi, w in sorted(issues, key=lambda i: -i[5]):
        weight = {3: 'critical', 2: 'major', 1: 'minor'}[w]
        if key == 'cuts_with_sound':
            quiet, soft = sy['no_sound'], [t for t in sy['no_new_attack'] if t not in sy['no_sound']]
            text = (f'{round(100 * v)} % of the {len(sy["rows"])} {a["target_kind"]}s have an onset within +-100 ms (refs 50 % to 100 %)')
            if quiet:
                text += f'; no sound at all at {times(quiet)}: add a whoosh into the transition (peak on the cut), a hit or a click there'
            if soft:
                text += f'; sound plays through {len(soft)} of them with no new attack: add an accent on the ones that matter'
            actions.append((weight, text))
        elif key in BAND_FIX:
            actions.append((weight, f'{key.replace("band_", "")} band {v} dB ({"below" if status == "low" else "above"} the references\' {lo} to {hi}): ' + BAND_FIX[key][0 if status == 'low' else 1]))
        elif key == 'lufs_i':
            actions.append((weight, f'integrated loudness {v} LUFS ({"too quiet" if status == "low" else "too loud"}): master to about -14 LUFS (web window -16 to -9)'))
        elif key == 'true_peak':
            actions.append((weight, f'true peak {v} dBTP: leave the master at -1 dBTP or lower before encoding'))
        elif key == 'first_sound_s':
            actions.append((weight, f'the first sound is at {v} s: start the sound at once; autoplay viewers leave a silent open'))
        elif key == 'end_silence_s':
            actions.append((weight, f'{v} s of dead air after the sound: end the track on the last frame'))
        elif key == 'max_gap_s':
            actions.append((weight, f'a silent hole of {v} s inside the film: fill it or make it a deliberate stop-down before a hit'))
        elif key == 'final_lu':
            actions.append((weight, f'the last 3 s sit {v} LU against the body (refs -3.7 to 7.1): land the end card at body level or above'))
        elif key == 'end_lu':
            actions.append((weight, f'the ending is {v} LU against the body ({"quieter" if status == "low" else "louder"} than the references): bring it {"up" if status == "low" else "down"} or move the body'))
        else:
            actions.append((weight, f'{key} is {v} {UNITS.get(key, "")} (references {lo} to {hi}): {SPEC[key][4]}'))
    return {'verdict': verdict, 'score': round(100 * share), 'critical': critical, 'rows': rows,
            'actions': [f'[{w}] {t}' for w, t in actions],
            'tips': ([f'no stop-downs: 4 of 7 references drop the sound out for 0.2 to 1 s right before a big hit'] if not a['stopdowns'] and a['duration'] >= 6 else []),
            'partial': 'realness and music presence need the earshot extension; this verdict is partial'}


def check_of(path):
    """audit one sound: findings with times; 'clean' when none"""
    x = decode(path)
    mono = x.mean(axis=1)
    dur = len(mono) / SR
    findings = []
    peak = float(np.abs(x).max())
    if peak < 1e-4:
        return {'duration_s': round(dur, 3), 'findings': [{'kind': 'silent', 'at': 0.0, 'text': 'the file is silent'}], 'clean': False}
    clipped = int((np.abs(x) >= 0.999).sum())
    if clipped:
        findings.append({'kind': 'clipping', 'at': None, 'text': f'{clipped} samples at full scale'})
    dc = abs(float(mono.mean()))
    if dc > 0.003 * max(peak, 0.1):
        findings.append({'kind': 'dc', 'at': None, 'text': f'DC offset {dc:.4f}'})
    d2 = np.abs(np.diff(mono, 2))
    if len(d2) > 200:
        local = np.convolve(d2, np.ones(401) / 401, mode='same') + 1e-6
        spikes = np.where((d2 > 8 * local) & (d2 > 0.05 * peak))[0]
        merged = []
        for i in spikes:
            if not merged or i - merged[-1] > 48:
                merged.append(int(i))
        for i in merged[:6]:
            findings.append({'kind': 'click', 'at': round(i / SR, 4), 'text': f'a discontinuity (click) at {i / SR:.3f} s'})
    tail = float(np.sqrt((mono[-int(0.005 * SR):] ** 2).mean()))
    if dur > 0.05 and db(tail) > db(peak) - 40:
        findings.append({'kind': 'cut tail', 'at': round(dur, 3), 'text': f'the last 5 ms are only {db(peak) - db(tail):.0f} dB under the peak: the tail is cut off; fade it out'})
    head = float(np.sqrt((mono[:int(0.002 * SR)] ** 2).mean()))
    if head > 0.3 * peak:
        findings.append({'kind': 'cut start', 'at': 0.0, 'text': 'the sound starts at near full level on the first samples: a click on playback; fade in over 1 ms'})
    # a tonal sound that climbs more than 4 semitones: the rising "synth whip" that reads cheap
    n_fft, hop = 4096, 1200
    if len(mono) > n_fft * 2:
        frames = windows(mono, n_fft)[::hop] * np.hanning(n_fft)
        mag = np.abs(np.fft.rfft(frames, axis=1))
        freqs = np.fft.rfftfreq(n_fft, 1 / SR)
        sel = (freqs > 80) & (freqs < 6000)
        top = freqs[sel][np.argmax(mag[:, sel], axis=1)]
        tonal = mag[:, sel].max(axis=1) > 6 * np.median(mag[:, sel], axis=1)
        loud = 20 * np.log10(mag.max(axis=1) + 1e-9) > 20 * math.log10(mag.max() + 1e-9) - 25
        ok = tonal & loud
        if ok.sum() >= 4:
            semis = 12 * np.log2(top[ok] / top[ok][0])
            if semis.max() - semis[:1].min() > 4 and np.all(np.diff(semis) > -1.0) and semis[-1] - semis[0] > 4:
                findings.append({'kind': 'rising glide', 'at': None, 'text': f'a tonal pitch climbs {semis[-1] - semis[0]:.1f} semitones: the rising synth whip; use noise or an unpitched sweep'})
    onsets, _ = detect_onsets(mono, min_gap=0.005)
    if len(onsets) >= 2 and onsets[1] - onsets[0] < 0.04 and dur < 1.5:
        findings.append({'kind': 'stacked attacks', 'at': round(float(onsets[1]), 3), 'text': f'two attacks {1000 * (onsets[1] - onsets[0]):.0f} ms apart: a hit should be one attack'})
    return {'duration_s': round(dur, 3), 'peak_dbfs': round(db(peak), 1), 'findings': findings, 'clean': not findings}


def ab_of(pa, pb):
    ma, mb = [measure_of(analyse(p), full=False) for p in (pa, pb)]
    lines = []

    def diff(label, key, unit, fmt='{:+.1f}', thr=0.0):
        va, vb = ma.get(key), mb.get(key)
        if va is None or vb is None:
            return
        if abs(vb - va) > thr:
            lines.append(f'{label}: A {va} {unit}, B {vb} {unit} ({fmt.format(vb - va)})')
    diff('length', 'duration_s', 's', '{:+.2f}', 0.02)
    diff('loudness', 'lufs_i', 'LUFS', thr=0.5)
    diff('peak', 'peak_dbfs', 'dBFS', thr=0.5)
    diff('brightness', 'brightness_hz', 'Hz', '{:+.0f}', 100)
    for band in ma['bands_db']:
        va, vb = ma['bands_db'][band], mb['bands_db'][band]
        if abs(vb - va) >= 2.0:
            lines.append(f'{band} band: A {va} dB, B {vb} dB (B is {"stronger" if vb > va else "weaker"} by {abs(vb - va):.1f} dB)')
    words = [l.split(':')[0] for l in lines]
    return {'a': ma, 'b': mb, 'differences': lines,
            'summary': ('A and B measure alike within the tolerances' if not lines else f'B differs from A in {", ".join(words)}')}


def profile_of(paths):
    films = []
    for p in paths:
        a = analyse(p)
        sy = sync_of(a) if a['targets'] else None
        films.append(metric_values(measure_of(a), sy))
    out = {'version': 1, 'n': len(films), 'metrics': {}}
    for key in SPEC:
        vals = [f[key] for f in films if f.get(key) is not None]
        if vals:
            out['metrics'][key] = {'n': len(vals), 'min': round(min(vals), 2), 'p10': round(float(np.percentile(vals, 10)), 2),
                                   'median': round(float(np.median(vals)), 2), 'p90': round(float(np.percentile(vals, 90)), 2),
                                   'max': round(max(vals), 2)}
    return out


def ref_from_profile(profile):
    return {k: (v['min'], v['median'], v['max']) for k, v in profile['metrics'].items()}


def timeline_text(a, m, sy):
    lines = [f'{os.path.basename(a["path"])}: {m["duration_s"]} s, {m["lufs_i"]} LUFS, LRA {m["lra"]} LU'
             + (f', {m["tempo_bpm"]} BPM' if m.get('tempo_bpm') else '')]
    events = []
    for t in a['onsets']:
        sel = (a['tf'] >= t - 0.01) & (a['tf'] <= t + 0.09)
        pre = (a['tf'] >= t - 0.25) & (a['tf'] < t - 0.03)
        level = float(a['lf'][sel].max()) if sel.any() else None
        bed = float(a['lf'][pre].min()) if pre.any() else None
        events.append((float(t), level, None if level is None or bed is None else level - bed, 'hit' if any(abs(h - t) < 0.12 for h in a['hits']) else 'onset'))
    for s in a['swells']:
        events.append((float(s), None, None, 'swell peak'))
    cuts = {round(t, 3): 'cut' for t in a['targets']}
    lines.append('time      what                level   over bed   next to the ' + (a['target_kind'] or 'picture'))
    shown = 0
    for t, level, over, kind in sorted(events):
        near = [c for c in a['targets'] if abs(c - t) <= 0.15]
        mark = f'{a["target_kind"]} {fmt_t(near[0])} ({round((t - near[0]) * 1000):+d} ms)' if near else ''
        if shown < 400:
            lines.append(f'{fmt_t(t):>8}  {kind:<18} {("%.1f" % level) if level is not None else "":>6}  {("%+.1f dB" % over) if over is not None else "":>9}  {mark}')
            shown += 1
    if a['stopdowns']:
        lines.append('stop-downs: ' + ', '.join(f'{fmt_t(s)} ({ln} s, {d} dB)' for s, ln, d in a['stopdowns']))
    if sy and sy['rows']:
        lines.append(f'sync against {len(sy["rows"])} {a["target_kind"]}s: '
                     + (f'{round(100 * sy["with_onset"])} % with an onset within +-{sy["tolerance_ms"]} ms (chance {round(100 * sy["with_onset_chance"])} %)'
                        if 'with_onset' in sy else 'too few to score'))
        if sy['no_sound']:
            lines.append(f'{a["target_kind"]}s with no sound at all: ' + times(sy['no_sound']))
    return '\n'.join(lines)


def sheet_png(a, m, sy, out):
    from PIL import Image, ImageDraw
    W, H = 1600, 760
    dur = a['duration']
    img = Image.new('RGB', (W, H), (18, 18, 22))
    d = ImageDraw.Draw(img)
    left, right = 70, W - 20

    def px(t):
        return left + (right - left) * t / dur
    d.text((10, 8), f'{os.path.basename(a["path"])}  {dur:.1f} s  {m["lufs_i"]} LUFS  LRA {m["lra"]} LU  true peak {m.get("true_peak")} dBTP', fill=(235, 235, 235))
    # waveform
    top, hgt = 40, 150
    mono = a['mono']
    n = right - left
    seg = max(1, len(mono) // n)
    cols = np.abs(mono[: n * seg]).reshape(-1, seg).max(axis=1)[:n] if len(mono) >= n else np.abs(mono)
    for i, v in enumerate(cols):
        h = int(v * hgt / 2 / max(float(np.abs(mono).max()), 1e-6))
        d.line([(left + i, top + hgt // 2 - h), (left + i, top + hgt // 2 + h)], fill=(90, 160, 255))
    d.text((8, top + 4), 'wave', fill=(150, 150, 160))
    # spectrogram (log frequency)
    top2, hgt2 = 210, 250
    n_fft, hop = 2048, max(256, int(dur * SR / n))
    if len(mono) > n_fft:
        frames = windows(mono, n_fft)[::hop] * np.hanning(n_fft)
        mag = 20 * np.log10(np.abs(np.fft.rfft(frames, axis=1)) + 1e-9)
        freqs = np.fft.rfftfreq(n_fft, 1 / SR)
        edges = np.searchsorted(freqs, np.geomspace(40, 16000, hgt2 + 1))
        rows = np.stack([mag[:, edges[i]:max(edges[i + 1], edges[i] + 1)].max(axis=1) for i in range(hgt2)], axis=0)[::-1]
        lo = rows.max() - 80
        grid = np.clip((rows - lo) / 80, 0, 1)
        rgb = np.stack([np.clip(grid * 2.0, 0, 1) * 255, np.clip(grid * 2.0 - 0.6, 0, 1) * 255, np.clip(grid * 1.2, 0, 1) * 180], axis=-1).astype(np.uint8)
        spec = Image.fromarray(rgb).resize((n, hgt2))
        img.paste(spec, (left, top2))
    d.text((8, top2 + 4), 'spectrum', fill=(150, 150, 160))
    # loudness curve
    top3, hgt3 = 480, 130
    tm, lm = a['tm'], a['lm']
    lo3, hi3 = max(-60.0, float(lm.min())), float(lm.max()) + 3
    pts = [(px(t), top3 + hgt3 - (min(max(v, lo3), hi3) - lo3) / (hi3 - lo3) * hgt3) for t, v in zip(tm, lm)]
    if len(pts) > 1:
        d.line(pts, fill=(250, 200, 80), width=2)
    iy = top3 + hgt3 - (a['lufs'] - lo3) / (hi3 - lo3) * hgt3
    d.line([(left, iy), (right, iy)], fill=(120, 120, 60))
    d.text((8, top3 + 4), 'loudness', fill=(150, 150, 160))
    # events, hits, cuts
    top4, hgt4 = 630, 100
    for t in a['onsets']:
        d.line([(px(t), top4 + 40), (px(t), top4 + 60)], fill=(160, 160, 170))
    for t in a['hits']:
        d.line([(px(t), top4 + 20), (px(t), top4 + 70)], fill=(255, 110, 90), width=2)
    verdict = {r['t']: r['verdict'] for r in (sy or {}).get('rows', [])}
    for t in a['targets']:
        v = verdict.get(round(t, 3), '')
        colour = (90, 220, 120) if v in ('OK', 'near') else (240, 190, 60) if v in ('swell', 'peak') else (240, 70, 70)
        d.line([(px(t), top), (px(t), top4 + 90)], fill=colour)
        d.text((px(t) + 2, top4 + 76), f'{t:.1f}', fill=colour)
    d.text((8, top4 + 4), 'events', fill=(150, 150, 160))
    d.text((left, H - 14), 'grey tick = onset, red = salient hit, vertical line = ' + (a['target_kind'] or 'picture event') + ' (green: sound within 100 ms, amber: a swell or level peak, red: no sound)', fill=(150, 150, 160))
    img.save(out)
    return out


def find_earshot(explicit=None):
    for c in (explicit, os.environ.get('EARSHOT_BIN'),
              os.path.expanduser('~/.framecore-studio/extensions/earshot/venv/bin/earshot'),
              os.path.expanduser('~/.framecore-studio/extensions/earshot/venv/Scripts/earshot.exe'), shutil.which('earshot')):
        if c and os.path.isfile(c):
            return c
    return None


def delegate(command, rest, explicit=None):
    exe = find_earshot(explicit)
    if not exe:
        print(f'listen: `{command}` needs the earshot extension (models and the sound bank), which is not installed here.\n'
              'It is a recommended repository: python3 <plugin>/skills/workflow-orchestrator/assets/extensions/extensions.py show earshot --host <host>\n'
              'The measurements and checks above run without it.', file=sys.stderr)
        return 4
    return subprocess.call([exe, command] + rest)


def emit(args, result, text):
    if getattr(args, 'json', False):
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
    else:
        print(text)
    if getattr(args, 'out', None) and getattr(args, 'cmd', '') not in ('sheet', 'profile'):
        json.dump(result, open(args.out, 'w', encoding='utf-8'), indent=2, ensure_ascii=False, default=str)


def public(a):
    return {k: v for k, v in a.items() if k not in ('x', 'mono', 'e2', 'tf', 'lf', 'tm', 'lm', 'ts', 'ls', 'onsets', 'hits', 'swells', 'beats')}


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] in EARSHOT_COMMANDS:
        explicit = None
        if '--earshot' in argv:
            i = argv.index('--earshot')
            explicit = argv[i + 1]
            del argv[i:i + 2]
        return delegate(argv[0], argv[1:], explicit)
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0], formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='cmd', required=True)

    def common(p, files=1):
        if files == 1:
            p.add_argument('file')
        p.add_argument('--json', action='store_true')
        p.add_argument('--out', help='also save the result as JSON')
    for name in ('measure', 'timeline', 'sync', 'critique', 'sheet'):
        p = sub.add_parser(name)
        common(p)
        if name != 'measure':
            p.add_argument('--video', help='the picture to compare with, when the sound is a separate file')
            p.add_argument('--cues', help='cue times (JSON) instead of the picture\'s cuts')
            p.add_argument('--from', dest='start', type=float)
            p.add_argument('--to', dest='end', type=float)
        if name == 'critique':
            p.add_argument('--profile', help='your own reference ranges from `profile`')
        if name == 'sheet':
            p.add_argument('-o', '--png', required=True)
    p = sub.add_parser('check')
    common(p)
    p = sub.add_parser('ab')
    p.add_argument('a')
    p.add_argument('b')
    p.add_argument('--json', action='store_true')
    p = sub.add_parser('profile')
    p.add_argument('files', nargs='+')
    p.add_argument('-o', '--out', required=True)
    args = parser.parse_args(argv)
    try:
        if args.cmd == 'check':
            r = check_of(args.file)
            emit(args, r, f'{os.path.basename(args.file)}: ' + ('clean' if r['clean'] else '; '.join(f['text'] for f in r['findings'])))
            return 0 if r['clean'] else 1
        if args.cmd == 'ab':
            r = ab_of(args.a, args.b)
            emit(args, r, r['summary'] + ('\n  ' + '\n  '.join(r['differences']) if r['differences'] else ''))
            return 0
        if args.cmd == 'profile':
            r = profile_of(args.files)
            json.dump(r, open(args.out, 'w', encoding='utf-8'), indent=2)
            print(f'profile of {r["n"]} films written to {args.out}')
            return 0
        cues = read_cues(args.cues) if getattr(args, 'cues', None) else None
        a = analyse(args.file, video=getattr(args, 'video', None), cues=cues, start=getattr(args, 'start', None), end=getattr(args, 'end', None))
        m = measure_of(a, full=getattr(args, 'start', None) is None)
        sy = sync_of(a) if a['targets'] else None
        if args.cmd == 'measure':
            emit(args, m, measure_text(args.file, m))
        elif args.cmd == 'sync':
            if not sy:
                raise InputError('no cuts or cues to compare with: give --video, --cues, or a file that has a picture')
            text = (f'{os.path.basename(args.file)}: {len(sy["rows"])} {a["target_kind"]}s, '
                    + (f'{round(100 * sy["with_onset"])} % with an onset within +-{sy["tolerance_ms"]} ms (chance {round(100 * sy["with_onset_chance"])} %), {round(100 * sy["on_frame"])} % within a frame' if 'with_onset' in sy else 'too few to score')
                    + '\n' + '\n'.join(f'  {fmt_t(r["t"])}  {r["verdict"]:<9}' + (f'{r["offset_ms"]:+d} ms' if r['offset_ms'] is not None else '') for r in sy['rows']))
            emit(args, sy, text)
        elif args.cmd == 'timeline':
            emit(args, {'measure': m, 'sync': sy, 'onsets': [round(float(t), 3) for t in a['onsets']], 'hits': [round(float(t), 3) for t in a['hits']],
                        'swells': [round(float(t), 3) for t in a['swells']], 'stopdowns': a['stopdowns'], 'beats': [round(b, 3) for b in a['beats']]},
                 timeline_text(a, m, sy))
        elif args.cmd == 'sheet':
            sheet_png(a, m, sy, args.png)
            print(f'sheet written to {args.png}')
        elif args.cmd == 'critique':
            ref = ref_from_profile(json.load(open(args.profile))) if args.profile else None
            c = critique_of(a, m, sy, ref)
            head = f'listen critique: {os.path.basename(args.file)} ({m["duration_s"]} s) against ' + ('your profile' if ref else 'the 7 launch films earshot measured')
            text = [head, f'VERDICT: {c["verdict"]} (partial) - score {c["score"]} %, ' + ('a critical issue' if c['critical'] else 'no critical issue')]
            if c['actions']:
                text.append('FIX FIRST:')
                text += [f'  {i}. {t}' for i, t in enumerate(c['actions'], 1)]
            text += [f'  tip: {t}' for t in c['tips']]
            text.append('SCORECARD                value        ok range            status')
            for r in c['rows']:
                if r['status'] == 'n.a.':
                    continue
                rng = f'{r["low"] if r["low"] is not None else ""} .. {r["high"] if r["high"] is not None else ""}'
                text.append(f'  {r["key"]:<20} {r["value"]!s:<12} {rng:<19} {r["status"]} ({r["weight"]})' if r['status'] != 'ok' else f'  {r["key"]:<20} {r["value"]!s:<12} {rng:<19} ok')
            text.append(f'NOT MEASURED HERE: {c["partial"]}')
            emit(args, {'measure': m, 'sync': sy, 'critique': c}, '\n'.join(text))
            return 1 if c['critical'] else 0
        return 0
    except InputError as e:
        print(f'listen {args.cmd}: error: {e}', file=sys.stderr)
        return 3


if __name__ == '__main__':
    sys.exit(main())
