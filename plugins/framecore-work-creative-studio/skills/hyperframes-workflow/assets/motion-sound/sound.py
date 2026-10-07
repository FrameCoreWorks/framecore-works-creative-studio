#!/usr/bin/env python3
"""FrameCore Works motion sound design: plan a sound track from a motion contract, render and master it, check it.

The plan comes from the same timing as the picture: the Python renderer's port of the scene engine
(../motion-render/render.py) tells when every line, item, card, tap, screen push, sweep and wipe happens and how
long each move lasts. Every event gets a designed sound from synth.py whose hit (or a whoosh's peak, or a riser's
end) lands exactly on its frame and whose length follows the move; a music bed is composed to the video's length
with its energy following the scenes. Everything is deterministic: the same contract gives the same audio.

  python sound.py plan video.motion.json --out video-r2.motion.json [--density minimal|standard|rich] [--no-music] [--table cues.md]
  python sound.py mix video-r2.motion.json --video video.mp4 --out video-sound.mp4 [--wav mix.wav] [--stems dir]
  python sound.py check effects.wav video-r2.motion.json

Requires Python 3.8+, numpy and ffmpeg (with loudnorm for loudness). Keep it with synth.py and
../motion-render/render.py. Exit code: 0 done, 1 problems found, 2 setup problem.
"""
import argparse
import importlib.util
import json
import math
import os
import re
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
try:
    import numpy as np
    import synth
except ImportError as error:  # pragma: no cover
    sys.stderr.write(f'numpy is required ({error})\n')
    sys.exit(2)

RATE = synth.RATE
DENSITIES = ('minimal', 'standard', 'rich')
SENDS = {'whoosh': 0.18, 'impact': 0.22, 'boom': 0.3, 'riser': 0.25, 'click': 0.05, 'release': 0.04, 'tick': 0.03, 'knock': 0.12, 'shimmer': 0.4}
MINOR_STYLES = {'midnight', 'warm-ink', 'brand-native'}


def load_engine():
    """The Python port of the scene engine, so the sound uses exactly the picture's timing."""
    for path in (os.path.join(HERE, '..', 'motion-render', 'render.py'), os.path.join(HERE, 'render.py')):
        if os.path.exists(path):
            spec = importlib.util.spec_from_file_location('studio_render', path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
    raise RuntimeError('render.py (the motion renderer) must sit in ../motion-render/ or next to sound.py')


def first_frame(start, end, test):
    for frame in range(start, end):
        if test(frame):
            return frame
    return None


# ---------------------------------------------------------------- planning

def plan_cues(score, density='standard'):
    """Sound cues for every visible event: [{frame, sound, gain, pan, params, event}] in frame order."""
    if density not in DENSITIES:
        raise ValueError(f'density must be one of {", ".join(DENSITIES)}')
    r = load_engine()
    level, m, total = DENSITIES.index(density), r.motion(score), score['totalFrames']
    fps = score['fps']['num'] / score['fps']['den']
    cues = []

    def add(frame, sound, event, gain, pan=0.0, params=None, at_least=0):
        if level >= at_least and frame is not None and 0 <= frame < total:
            cues.append({'frame': int(frame), 'sound': sound, 'gain': gain, 'pan': round(pan, 2), 'params': params or {}, 'event': event})

    def landed(start, duration, easing, end, limit=0.9):
        return first_frame(start, end, lambda f: r.progress(f, start, duration, easing) >= limit)

    def seconds_of(frames, low, high):
        return round(min(high, max(low, frames / fps)), 3)

    scenes = score['scenes']
    last = scenes[-1] if scenes else None
    for index, scene in enumerate(scenes):
        p, sid, start, end = scene.get('params') or {}, scene['id'], scene['start'], scene['end']
        mode, previous = r.exit_mode(scene, score), scenes[index - 1] if index else None
        side = 1 if index % 2 == 0 else -1
        wipe = p.get('backgroundWipe', 'none') if p.get('background') else 'none'
        if wipe != 'none':
            frames = p.get('backgroundFrames', 12)
            direction = {'left': 1, 'right': -1, 'up': 0, 'down': 0}[wipe]
            add(start + frames // 2, 'whoosh', f'{sid}: canvas wipes in from the {wipe}', -10, 0, {'duration': seconds_of(frames * 1.8, 0.35, 0.9), 'peak': 0.55, 'direction': direction, 'intensity': 0.9})
        elif previous is not None and r.exit_mode(previous, score) != 'sweep' and start > 0:
            add(start + m['entryFrames'] // 3, 'whoosh', f'{sid}: scene enters', -14, 0, {'duration': seconds_of(m['entryFrames'] * 2, 0.35, 0.7), 'peak': 0.5, 'direction': side, 'intensity': 0.7})
        if mode == 'sweep':
            sweep = p.get('sweepFrames', m['exitFrames'] + 12)
            add(end - sweep + sweep // 2, 'whoosh', f'{sid}: line sweeps across', -10, 0, {'duration': seconds_of(sweep, 0.4, 1.4), 'peak': 0.5, 'direction': 1, 'brightness': 1.0, 'intensity': 0.85})
        elif mode == 'lift':
            add(end - m['exitFrames'] + m['exitFrames'] // 2, 'whoosh', f'{sid}: content lifts out', -21, 0, {'duration': seconds_of(m['exitFrames'] * 2, 0.3, 0.6), 'peak': 0.5, 'direction': -side, 'brightness': 0.7, 'intensity': 0.5}, at_least=2)
        kind = scene['kind']
        final = scene is last and kind in ('end-card', 'logo-reveal')
        if kind == 'line-reveal':
            for i, _ in enumerate(r.as_list(p.get('lines'))):
                begin = start + i * m['lineStaggerFrames']
                add(landed(begin, m['entryFrames'], m['entryEasing'], end), 'knock', f'{sid}: line {i + 1} lands', -12 - 3 * i, 0, {'pitch': 1 + 0.12 * i}, at_least=1)
        elif kind == 'item-stagger':
            items = r.as_list(p.get('items'))
            steps = [1.0, 1.122, 1.26, 1.335, 1.498, 1.682]
            for i, _ in enumerate(items):
                begin = start + i * m['itemStaggerFrames']
                add(landed(begin, m['entryFrames'], m['entryEasing'], end), 'knock', f'{sid}: item {i + 1} lands', -10 - min(4, i), (i - (len(items) - 1) / 2) * 0.3, {'pitch': steps[i % len(steps)]}, at_least=1)
        elif kind in ('end-card', 'logo-reveal'):
            duration = p.get('duration', 30)
            frame = landed(start, duration, m['resolveEasing'], end)
            if kind == 'logo-reveal':
                add(start + duration // 4, 'whoosh', f'{sid}: mark opens', -16, 0, {'duration': seconds_of(duration * 0.8, 0.4, 1.0), 'peak': 0.4, 'direction': 0, 'brightness': 0.9})
            if final and level >= 2 and frame is not None:
                gap = frame - (scenes[index - 1]['start'] if index else 0)
                add(frame, 'riser', f'{sid}: tension into the reveal', -10, 0, {'duration': seconds_of(min(gap, 45), 0.6, 1.5)})
            add(frame, 'boom' if final and level >= 2 else 'impact', f'{sid}: {"end card" if kind == "end-card" else "mark"} settles', -3 if final else -6, 0, {'weight': 0.8 if final else 0.5})
            add(frame, 'shimmer', f'{sid}: accent', -16, 0, {'degree': 4}, at_least=1)
        elif kind == 'counter':
            count_start, duration = start + m['entryFrames'], p.get('duration', 45)
            last_text, last_tick = None, -10 ** 6
            for frame in range(count_start, min(end, count_start + duration)):
                k = r.progress(frame, count_start, duration, p.get('easing', 'easeOutCubic'))
                text = r.number_text(p, p.get('from', 0) + (p.get('to', 0) - p.get('from', 0)) * k)
                if text != last_text and frame - last_tick >= 3:
                    add(frame, 'tick', f'{sid}: number changes', -16 - round(6 * k), 0, {'pitch': round(1 + 0.5 * k, 3)}, at_least=1)
                    last_tick = frame
                last_text = text
            end_frame = min(end - 1, count_start + duration)
            add(end_frame, 'shimmer', f'{sid}: final value', -10, 0, {'degree': 4})
            add(end_frame, 'impact', f'{sid}: final value lands', -14, 0, {'weight': 0.3, 'brightness': 0.8})
        elif kind == 'quote':
            add(landed(start, m['entryFrames'] + 5, m['entryEasing'], end), 'knock', f'{sid}: quote lands', -12, 0, {'pitch': 0.9}, at_least=1)
            if p.get('attribution'):
                begin = start + p.get('attributionDelay', 30)
                add(landed(begin, m['entryFrames'], m['entryEasing'], end), 'knock', f'{sid}: attribution lands', -16, 0, {'pitch': 1.2}, at_least=2)
        elif kind == 'device':
            add(landed(start, m['entryFrames'] + 10, m['resolveEasing'], end), 'impact', f'{sid}: device settles', -14, 0, {'weight': 0.35, 'brightness': 0.4}, at_least=1)
            shots, screen_mode, tf = r.as_list(p.get('screens')), p.get('transition', 'push'), p.get('transitionFrames', 12)
            for i, shot in enumerate(shots[1:], 1):
                at = start + shot.get('at', 0)
                if screen_mode == 'push':
                    add(at + tf // 2, 'whoosh', f'{sid}: screen {i + 1} pushes in', -17, 0, {'duration': seconds_of(tf * 2, 0.3, 0.6), 'peak': 0.5, 'direction': -1, 'brightness': 0.85, 'intensity': 0.7}, at_least=1)
                elif screen_mode == 'fade':
                    add(at + tf // 2, 'whoosh', f'{sid}: screen {i + 1} fades in', -21, 0, {'duration': seconds_of(tf * 2, 0.3, 0.6), 'peak': 0.5, 'direction': 0, 'brightness': 0.6, 'intensity': 0.5}, at_least=1)
            for i, tap in enumerate(r.as_list(p.get('taps'))):
                at, pan = start + tap.get('at', 0), round((tap.get('x', 0.5) - 0.5) * 0.6, 2)
                add(at, 'click', f'{sid}: tap {i + 1}', -6, pan)
                add(at + 4, 'release', f'{sid}: tap {i + 1} releases', -16, pan, at_least=1)
            for i, key in enumerate(r.as_list(p.get('focus'))):
                frames = key.get('frames', 24)
                add(start + key.get('at', 0) + frames // 2, 'whoosh', f'{sid}: camera moves {i + 1}', -22, 0, {'duration': seconds_of(frames, 0.4, 1.2), 'peak': 0.5, 'direction': 0, 'brightness': 0.55, 'intensity': 0.5}, at_least=2)
            for i, _ in enumerate(r.as_list(p.get('caption'))):
                begin = start + 10 + i * m['lineStaggerFrames']
                add(landed(begin, m['entryFrames'], m['entryEasing'], end), 'knock', f'{sid}: caption line {i + 1} lands', -14 - 3 * i, 0, {'pitch': 1 + 0.12 * i}, at_least=1)
    cues.sort(key=lambda cue: (cue['frame'], -cue['gain']))
    kept = []
    for cue in cues:
        if not any(c['sound'] == cue['sound'] and abs(c['frame'] - cue['frame']) <= 2 for c in kept):
            kept.append(cue)
    return sorted(kept, key=lambda cue: (cue['frame'], cue['sound']))


def plan_music(score, r=None):
    """A composed bed: tempo from the contract's music grid or style, key from the style's mood, energy per bar from the scenes."""
    r = r or load_engine()
    fps = score['fps']['num'] / score['fps']['den']
    total_s = score['totalFrames'] / fps
    style = score.get('style')
    bpm = (score.get('music') or {}).get('bpm') or {'meadow': 100, 'field-guide': 96, 'paper-and-ink': 104, 'warm-ink': 110, 'midnight': 122, 'color-block': 122}.get(style, 108)
    key = 'A minor' if style in MINOR_STYLES else 'D major'
    bar = 4 * 60 / bpm
    scenes = score['scenes']
    final = scenes[-1] if scenes and scenes[-1]['kind'] in ('end-card', 'logo-reveal') else None
    energies = []
    for b in range(int(math.ceil(total_s / bar))):
        t0, t1 = b * bar * fps, (b + 1) * bar * fps
        if t1 >= score['totalFrames'] and b > 0:
            energies.append(0)
        elif final and t0 >= final['start']:
            energies.append(3 if t0 < final['start'] + bar * fps else 1)
        elif final and t1 > final['start'] - bar * fps:
            energies.append(3 if total_s >= 8 else 2)
        elif t1 <= scenes[0]['end']:
            energies.append(1)
        else:
            energies.append(2)
    return {'compose': True, 'bpm': round(float(bpm), 3), 'key': key, 'energies': energies, 'gain': -9}


def cue_table(score, cues):
    fps = score['fps']['num'] / score['fps']['den']
    rows = ['| Frame | Time | Sound | Gain | Pan | Event |', '| ---: | ---: | --- | ---: | ---: | --- |']
    rows += [f"| {c['frame']} | {c['frame'] / fps:.2f} s | {c['sound']} | {c['gain']} dB | {c['pan']} | {c.get('event', '')} |" for c in cues]
    return '\n'.join(rows) + '\n'


# ---------------------------------------------------------------- rendering

def render_effects(score, cues):
    """The effects bus and its reverb send, and each cue's hit sample with its alignment kind."""
    fps = score['fps']['num'] / score['fps']['den']
    length = round(score['totalFrames'] / fps * RATE)
    key = ((score.get('soundDesign') or {}).get('music') or {}).get('key', 'D major')
    dry, send, hits = np.zeros((length, 2)), np.zeros((length, 2)), []
    for index, cue in enumerate(cues):
        audio, offset = synth.render_design(cue['sound'], cue.get('params'), 1000 + 7 * index, key)
        hit = round(cue['frame'] / fps * RATE)
        start = hit - round(offset * RATE)
        gain = 10 ** (cue.get('gain', 0) / 20)
        theta = (max(-1.0, min(1.0, cue.get('pan', 0))) + 1) * math.pi / 4
        audio = audio * gain * np.array([math.cos(theta), math.sin(theta)]) * math.sqrt(2)
        a, b = max(0, start), min(length, start + len(audio))
        if b > a:
            dry[a:b] += audio[a - start:b - start]
            send[a:b] += audio[a - start:b - start] * SENDS.get(cue['sound'], 0.1)
        hits.append((hit, synth.DESIGNS[cue['sound']][1]))
    return dry, send, hits


def master(mix, target_lufs, ceiling_db=-1.0):
    """High-pass, limit, set loudness with ffmpeg's loudnorm analysis, limit again. Returns (audio, notes)."""
    spec_len = len(mix)
    for c in range(2):
        mix[:, c] = synth.shaped(mix[:, c], lambda t, f: synth.highpass(f, 28, 2), 4096, 1024)
    out = synth.limit(mix, ceiling_db - 0.5)
    notes = {}
    for _ in range(2):
        measured = loudness_of(out)
        if not measured:
            notes['method'] = 'peak only (ffmpeg has no loudnorm filter)'
            break
        integrated, _ = measured
        if integrated < -70:
            break
        out = synth.limit(out * 10 ** ((target_lufs - integrated) / 20), ceiling_db - 0.5)
    # The limiter watches samples; inter-sample peaks can still pass the ceiling, so trim by any true-peak excess.
    excess = synth.true_peak_db(out) - ceiling_db
    if excess > 0:
        out = out * 10 ** (-(excess + 0.05) / 20)
    measured = loudness_of(out)
    if measured:
        notes.update(lufs=measured[0], true_peak_db=round(synth.true_peak_db(out), 2), method='loudnorm analysis, gain and look-ahead limiter')
    return out[:spec_len], notes


def loudness_of(audio):
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, 'probe.wav')
        write_wav(audio, path, 'pcm_f32le')
        run = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', path, '-af', 'loudnorm=I=-14:TP=-1:print_format=json', '-f', 'null', '-'], capture_output=True, text=True)
    found = re.search(r'\{[^{}]*"input_i"[^{}]*\}', run.stderr)
    if run.returncode != 0 or not found:
        return None
    data = json.loads(found.group(0))
    return float(data['input_i']), float(data['input_tp'])


def write_wav(audio, path, codec='pcm_s24le'):
    with tempfile.TemporaryDirectory() as tmp:
        raw = os.path.join(tmp, 'audio.f32')
        audio.astype('<f4').tofile(raw)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(RATE), '-ac', '2', '-i', raw, '-c:a', codec, path], check=True)


def read_wav(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '2', '-ar', str(RATE), '-f', 'f32le', '-'], check=True, capture_output=True).stdout
    return np.frombuffer(raw, '<f4').reshape(-1, 2).astype(np.float64)


def full_mix(score, base_dir):
    """Effects, music (a supplied track, or the composed bed) and voice-over, with reverb, before mastering."""
    fps = score['fps']['num'] / score['fps']['den']
    length = round(score['totalFrames'] / fps * RATE)
    dry, send, hits = render_effects(score, score.get('sfx') or [])
    music_plan = (score.get('soundDesign') or {}).get('music') or {}
    music = np.zeros((length, 2))
    source = (score.get('music') or {}).get('src')
    if source:
        track = read_wav(os.path.join(base_dir, source))[:length]
        music[:len(track)] = track * float((score.get('music') or {}).get('volume', 1))
    elif music_plan.get('compose'):
        bed = synth.compose_bed(length / RATE, music_plan['bpm'], music_plan['key'], music_plan['energies'])
        music[:len(bed)] = bed[:length] * 10 ** (music_plan.get('gain', -9) / 20)
        send[:len(bed)] += bed[:length] * 10 ** (music_plan.get('gain', -9) / 20) * 0.12
    voice = np.zeros((length, 2))
    if (score.get('voiceover') or {}).get('src'):
        track = read_wav(os.path.join(base_dir, score['voiceover']['src']))[:length]
        voice[:len(track)] = track * float(score['voiceover'].get('volume', 1))
        ramp, duck = RATE // 10, np.ones(length)
        for caption in score.get('captions') or []:
            a, b = round(caption['start'] / fps * RATE), round(caption['end'] / fps * RATE)
            duck[max(0, a - ramp):min(length, b + ramp)] = 10 ** (-8 / 20)
        kernel = np.ones(ramp) / ramp
        music *= np.convolve(duck, kernel, mode='same')[:, None]
    wet = synth.convolve(send, synth.reverb_ir())[:length]
    return dry + music + voice + 0.6 * wet, dry, hits


# ---------------------------------------------------------------- checking

def check_hits(effects, hits):
    """Where each hit landed in an effects track: the first sample above half the local peak, or a whoosh's loudest
    10 ms. Risers end on their frame by construction and are not measured; a transient within 50 ms of another cue, or a
    whoosh within 250 ms of one, is reported as masked rather than judged."""
    mono = np.mean(effects, axis=1)
    report = []
    for index, (expected, align) in enumerate(hits):
        reach = RATE // 4 if align == 'peak' else RATE // 20
        masked = any(j != index and abs(h - expected) <= reach for j, (h, _) in enumerate(hits))
        if align == 'end':
            report.append({'sample': expected, 'kind': align, 'offset_ms': 0.0, 'ok': True, 'masked': masked, 'measured': False})
            continue
        if align == 'peak':
            lo, hi = max(0, expected - RATE // 4), min(len(mono), expected + RATE // 4)
            env = np.convolve(mono[lo:hi] ** 2, np.ones(RATE // 100) / (RATE // 100), mode='same')
            found = lo + int(np.argmax(env)) if hi > lo else expected
            tolerance = 15.0
        else:
            lo, hi = max(0, expected - RATE // 200), min(len(mono), expected + RATE // 50)
            window = np.abs(mono[lo:hi])
            found = lo + int(np.argmax(window >= 0.5 * window.max())) if hi > lo and window.max() > 0 else expected
            tolerance = 2.0
        offset = (found - expected) / RATE * 1000
        report.append({'sample': expected, 'kind': align, 'offset_ms': round(offset, 2), 'ok': True if masked else abs(offset) <= tolerance, 'masked': masked, 'measured': True})
    return report


def timing_check(score):
    """Check every cue on its own kind of track: transients without whooshes, whooshes without transients."""
    cues = score.get('sfx') or []
    report = []
    for kinds in (('onset',), ('peak', 'end')):
        group = [c for c in cues if synth.DESIGNS[c['sound']][1] in kinds]
        if group:
            effects, _, hits = render_effects(score, group)
            report += check_hits(effects, hits)
    return summarize(report)


def summarize(report):
    judged = [r for r in report if r['measured'] and not r['masked']]
    return {'cues': len(report), 'judged': len(judged), 'max_offset_ms': max((abs(r['offset_ms']) for r in judged), default=0.0), 'all_ok': all(r['ok'] for r in report)}


# ---------------------------------------------------------------- command line

def next_revision(score, evidence):
    revision = (score.get('revision') or 0) + 1
    out = dict(score, revision=revision)
    out['approval'] = {'status': 'approved', 'revision': revision, 'evidence': evidence} if evidence else {'status': 'proposed', 'revision': None, 'evidence': None}
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(description='Plan, render and check motion sound design.')
    sub = parser.add_subparsers(dest='command', required=True)
    plan = sub.add_parser('plan')
    plan.add_argument('contract')
    plan.add_argument('--out', required=True)
    plan.add_argument('--density', default='standard', choices=DENSITIES)
    plan.add_argument('--no-music', action='store_true', help='effects only (a supplied music.src is always used instead of composing)')
    plan.add_argument('--evidence')
    plan.add_argument('--table')
    mix = sub.add_parser('mix')
    mix.add_argument('contract')
    mix.add_argument('--video')
    mix.add_argument('--out')
    mix.add_argument('--wav')
    mix.add_argument('--stems', help='folder for effects.wav and music-free stems')
    mix.add_argument('--lufs', type=float, default=-14.0)
    test = sub.add_parser('check')
    test.add_argument('wav', help='an effects-only track, such as stems/effects.wav')
    test.add_argument('contract')
    args = parser.parse_args(argv)
    try:
        with open(args.contract, encoding='utf-8') as handle:
            score = json.load(handle)
        if args.command == 'plan':
            if os.path.exists(args.out):
                raise ValueError(f'Output file already exists: {args.out}')
            cues = plan_cues(score, args.density)
            result = next_revision(score, args.evidence)
            design = {'engine': 'studio-synth-1', 'density': args.density, 'status': 'planned'}
            if not args.no_music and not (score.get('music') or {}).get('src'):
                design['music'] = plan_music(score)
            result['soundDesign'] = design
            result['sfx'] = cues
            with open(args.out, 'w', encoding='utf-8') as handle:
                handle.write(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
            if args.table:
                with open(args.table, 'w', encoding='utf-8') as handle:
                    handle.write(cue_table(score, cues))
            counts = {}
            for cue in cues:
                counts[cue['sound']] = counts.get(cue['sound'], 0) + 1
            print(json.dumps({'cues': len(cues), 'by_sound': counts, 'density': args.density, 'music': design.get('music', {}).get('bpm'), 'out': args.out}))
            return 0
        if args.command == 'check':
            fps = score['fps']['num'] / score['fps']['den']
            cues = score.get('sfx') or []
            hits = [(round(c['frame'] / fps * RATE), synth.DESIGNS[c['sound']][1]) for c in cues]
            summary = summarize(check_hits(read_wav(args.wav), hits))
            print(json.dumps(summary))
            return 0 if summary['all_ok'] else 1
        if args.out and not args.video:
            raise ValueError('--out needs --video')
        for path in (args.out, args.wav):
            if path and os.path.exists(path):
                raise ValueError(f'Output file already exists: {path}')
        mixed, effects, hits = full_mix(score, os.path.dirname(os.path.abspath(args.contract)))
        timing = timing_check(score)
        mastered, notes = master(mixed, args.lufs)
        summary = {'cues': len(score.get('sfx') or []), 'timing': timing, 'loudness': notes}
        with tempfile.TemporaryDirectory() as tmp:
            wav = args.wav or os.path.join(tmp, 'mix.wav')
            write_wav(mastered, wav)
            if args.stems:
                os.makedirs(args.stems, exist_ok=True)
                write_wav(effects, os.path.join(args.stems, 'effects.wav'), 'pcm_f32le')
            if args.out:
                duration = score['totalFrames'] * score['fps']['den'] / score['fps']['num']
                subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', args.video, '-i', wav, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                                '-c:a', 'aac', '-b:a', '256k', '-t', f'{duration:.6f}', args.out], check=True)
                summary['out'] = args.out
        summary['wav'] = args.wav
        print(json.dumps(summary))
        return 0 if timing['all_ok'] else 1
    except (OSError, ValueError, RuntimeError, KeyError, subprocess.CalledProcessError) as error:
        sys.stderr.write(f'{error}\n')
        return 2


if __name__ == '__main__':
    sys.exit(main())
