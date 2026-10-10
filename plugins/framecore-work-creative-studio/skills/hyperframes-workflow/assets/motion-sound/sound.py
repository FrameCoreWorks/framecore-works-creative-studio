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
import zlib

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
try:
    import numpy as np
    import compose
    import direction as directing
    import generate
    import music
    import recipe as recipes
    import synth
except ImportError as error:  # pragma: no cover
    sys.stderr.write(f'numpy is required ({error})\n')
    sys.exit(2)

RATE = synth.RATE
DENSITIES = ('minimal', 'standard', 'rich')
SENDS = {'landing': 0.12, 'whoosh': 0.18, 'impact': 0.22, 'boom': 0.3, 'riser': 0.25, 'click': 0.05, 'release': 0.04, 'tick': 0.03, 'knock': 0.12,
         'tap': 0.06, 'pop': 0.1, 'swish': 0.15, 'shimmer': 0.4}
PACE_POSITION = {'fast': 0.75, 'medium': 0.5, 'slow': 0.25}
MINOR_STYLES = {'midnight', 'warm-ink', 'brand-native'}
STYLE_BPM = {'meadow': 100, 'field-guide': 96, 'paper-and-ink': 104, 'warm-ink': 110, 'midnight': 122, 'color-block': 122,
             'sale-poster': 124, 'editorial-serif': 96, 'product-light': 114, 'bold-grotesque': 122}
# The music dips under the hits that must read clearly: (depth in dB, release in seconds).
DUCKS = {'boom': (5.0, 0.45), 'impact': (3.0, 0.3), 'click': (1.5, 0.12)}
# Gains for moments the user marks in supplied footage, matching the levels the planner gives the same sounds.
FOOTAGE_GAINS = {'impact': -8, 'boom': -6, 'click': -8, 'release': -16, 'tick': -16, 'landing': -12, 'whoosh': -14, 'riser': -10, 'shimmer': -14}


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


def final_reveal(score, r, m=None):
    """The frame the closing end card or logo settles on, or None when the video ends without one."""
    source = score.get('source') or {}
    if source.get('kind') == 'footage':
        return source.get('reveal')
    scenes = score['scenes']
    last = scenes[-1] if scenes else None
    if not last or last['kind'] not in ('end-card', 'logo-reveal'):
        return None
    m = m or r.motion(score)
    duration = (last.get('params') or {}).get('duration', 30)
    return first_frame(last['start'], last['end'], lambda f: r.progress(f, last['start'], duration, m['resolveEasing']) >= 0.9)


# ---------------------------------------------------------------- planning

def sound_direction(score, overrides=None):
    """Analyse this video and choose its sounds and music from the sound base (see direction.py)."""
    profile = directing.analyze(score, engine=load_engine())
    fixed = music.STYLE_PALETTE.get(score.get('style'))
    return directing.direct(score, profile, content_seed(score), fixed_palette=fixed, overrides=overrides)


def plan_cues(score, density='standard', direction=None, designed=None):
    """Sound cues for every visible event: [{frame, sound, gain, pan, params, event}] in frame order. `direction`
    (from sound_direction) sets how text lands and the character of whooshes and clicks for this video."""
    if density not in DENSITIES:
        raise ValueError(f'density must be one of {", ".join(DENSITIES)}')
    r = load_engine()
    level, m, total = DENSITIES.index(density), r.motion(score), score['totalFrames']
    fps = score['fps']['num'] / score['fps']['den']
    cues = []

    landing_kind = ((designed or {}).get('landing') or {}).get('kind', 'knock')
    character = (direction or {}).get('character') or {}
    shift = 2 ** (character.get('pitchSemitones', 0) / 12)

    def add(frame, sound, event, gain, pan=0.0, params=None, at_least=0):
        params = dict(params or {})
        if sound == 'knock':  # a landing: designed for this video (or none), a knock without a design
            if landing_kind == 'none':
                return
            sound = 'landing' if designed else 'knock'
            params['pitch'] = round(params.get('pitch', 1.0) * shift, 4)
        elif sound == 'whoosh' and character:
            params['brightness'] = round(params.get('brightness', 1.0) * character['whooshBrightness'], 3)
            params['intensity'] = round(params.get('intensity', 0.8) * character['whooshIntensity'], 3)
        elif sound == 'click' and character:
            params['softness'] = character['clickSoftness']
        if level >= at_least and frame is not None and 0 <= frame < total:
            cues.append({'frame': int(frame), 'sound': sound, 'gain': gain, 'pan': round(pan, 2), 'params': params, 'event': event})

    def landed(start, duration, easing, end, limit=0.9):
        return first_frame(start, end, lambda f: r.progress(f, start, duration, easing) >= limit)

    def seconds_of(frames, low, high):
        return round(min(high, max(low, frames / fps)), 3)

    source = score.get('source') or {}
    if source.get('kind') == 'footage':
        # Supplied footage has no scene kinds to read: sound follows the cuts, the moments the user marked and the reveal.
        for i, cut in enumerate(source.get('cuts') or []):
            add(cut, 'whoosh', f'cut {i + 1}', -18, 0, {'duration': 0.4, 'peak': 0.5, 'direction': 1 if i % 2 == 0 else -1, 'brightness': 0.8, 'intensity': 0.55}, at_least=2)
        for hit in source.get('hits') or []:
            gain, params = FOOTAGE_GAINS.get(hit['sound'], -12), {'duration': 1.0} if hit['sound'] == 'riser' else {}
            add(hit['frame'], hit['sound'], hit.get('label') or f"{hit['sound']} marked by the user", gain, 0, params)
        reveal = source.get('reveal')
        if reveal is not None:
            if level >= 2:
                add(reveal, 'riser', 'tension into the reveal', -10, 0, {'duration': 1.2})
            add(reveal, 'boom' if level >= 2 else 'impact', 'the reveal settles', -6 if level >= 2 else -8, 0, {'weight': 0.8})
            add(reveal, 'shimmer', 'reveal accent', -16, 0, {'degree': 4}, at_least=1)
        cues.sort(key=lambda cue: (cue['frame'], -cue['gain']))
        return cues
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
            frame = final_reveal(score, r, m) if final else landed(start, duration, m['resolveEasing'], end)
            if kind == 'logo-reveal':
                add(start + duration // 4, 'whoosh', f'{sid}: mark opens', -16, 0, {'duration': seconds_of(duration * 0.8, 0.4, 1.0), 'peak': 0.4, 'direction': 0, 'brightness': 0.9})
            if final and level >= 2 and frame is not None:
                gap = frame - (scenes[index - 1]['start'] if index else 0)
                add(frame, 'riser', f'{sid}: tension into the reveal', -10, 0, {'duration': seconds_of(min(gap, 45), 0.6, 1.5)})
            add(frame, 'boom' if final and level >= 2 else 'impact', f'{sid}: {"end card" if kind == "end-card" else "mark"} settles', -6 if final and level >= 2 else -7 if final else -8, 0, {'weight': 0.8 if final else 0.5})
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


def style_tempo(style):
    """The style's tempo range from ../motion-styles/styles.json, or None when the style or the file is missing."""
    path = os.path.join(HERE, '..', 'motion-styles', 'styles.json')
    try:
        with open(path, encoding='utf-8') as handle:
            styles = json.load(handle)['styles']
        low, high = next(item['music']['bpm'] for item in styles if item['id'] == style)
        return float(low), float(high)
    except (OSError, ValueError, KeyError, StopIteration, TypeError):
        return None


def content_seed(score):
    """A stable number from the video's own content, so each video gets its own progression and variations."""
    text = json.dumps([score.get('title'), score.get('copy'), [scene.get('id') for scene in score['scenes']]], sort_keys=True, ensure_ascii=False)
    return zlib.crc32(text.encode('utf-8'))


def fit_tempo(target, reveal_s, starts, spread=0.08, low=None, high=None):
    """A tempo near the style's that puts the reveal on a downbeat: bar N of the music begins exactly on the reveal.
    Candidates lie within `spread` of the target and inside the style's range [low, high] when given; the one closest
    to the target that also keeps scene starts nearest to beats wins. Returns (bpm, reveal_bar), or (target, None)."""
    best = None
    for bars in range(1, 129):
        bpm = 240.0 * bars / reveal_s
        if abs(bpm / target - 1) > spread or (low and bpm < low - 1e-6) or (high and bpm > high + 1e-6):
            continue
        beat = 60.0 / bpm
        drift = sum(abs((t / beat + 0.5) % 1 - 0.5) for t in starts) / len(starts) if starts else 0.0
        cost = 6 * abs(math.log(bpm / target)) + drift
        if best is None or cost < best[0]:
            best = (cost, bpm, bars)
    return (best[1], best[2]) if best else (float(target), None)


def plan_music(score, r=None, direction=None):
    """A composed bed: tempo from the contract's music grid or style, fitted so the final reveal lands on a downbeat;
    key from the style's mood; energy per bar from the scenes, building into the reveal and resolving after it."""
    r = r or load_engine()
    fps = score['fps']['num'] / score['fps']['den']
    total_s = score['totalFrames'] / fps
    style = score.get('style')
    grid = (score.get('music') or {}).get('bpm')
    tempo_range = style_tempo(style) or (None, None)
    pace = ((direction or {}).get('profile') or {}).get('pace', 'medium')
    if grid:
        target = grid
    elif tempo_range[0]:
        target = tempo_range[0] + PACE_POSITION[pace] * (tempo_range[1] - tempo_range[0])
    else:
        target = STYLE_BPM.get(style, 108) * {'fast': 1.06, 'medium': 1.0, 'slow': 0.94}[pace]
    key = (direction or {}).get('key') or ('A minor' if style in MINOR_STYLES else 'D major')
    scenes = score['scenes']
    reveal = final_reveal(score, r)
    starts = [scene['start'] / fps for scene in scenes if scene['start'] > 0]
    bpm, reveal_bar = float(target), None
    if reveal:
        if grid:
            # A beat grid the picture was cut to stays as it is; the reveal is anchored only if it already sits on a bar.
            bars = round(reveal / fps / (240.0 / grid))
            reveal_bar = bars if bars >= 1 and abs(reveal / fps - bars * 240.0 / grid) <= 1.0 / fps else None
        else:
            bpm, reveal_bar = fit_tempo(target, reveal / fps, starts, 0.08, *tempo_range)
            if reveal_bar is None:
                bpm, reveal_bar = fit_tempo(target, reveal / fps, starts, 0.08)
    bar = 4 * 60 / bpm
    final = scenes[-1] if scenes and scenes[-1]['kind'] in ('end-card', 'logo-reveal') else None
    bars = int(math.ceil(total_s / bar - 1e-9))
    lead_in = 3 if total_s >= 8 else 2
    end_bar = resolution_bar(reveal_bar, bars, bar, total_s)
    energies = []
    for b in range(bars):
        t0, t1 = b * bar * fps, (b + 1) * bar * fps
        if end_bar is not None and reveal_bar <= b < end_bar:
            # A reveal well before the end: the music carries on through it and eases only into the last bar.
            energies.append(2 if b == end_bar - 1 and b > reveal_bar else lead_in)
        elif reveal_bar is not None and b >= reveal_bar:
            energies.append(1)
        elif reveal_bar is not None and b == reveal_bar - 1:
            energies.append(3 if total_s >= 8 else 2)
        elif t1 >= score['totalFrames'] and b > 0:
            energies.append(0)
        elif final and t0 >= final['start']:
            energies.append(3 if t0 < final['start'] + bar * fps else 1)
        elif final and t1 > final['start'] - bar * fps:
            energies.append(3 if total_s >= 8 else 2)
        elif t1 <= scenes[0]['end']:
            energies.append(1)
        else:
            energies.append(2)
    seed = content_seed(score)
    palette = (direction or {}).get('palette') or music.STYLE_PALETTE.get(style, 'studio')
    backbeat = (((direction or {}).get('choices') or {}).get('backbeat') or {}).get('option')
    plan = {'compose': True, 'bpm': round(bpm, 4), 'key': key, 'palette': palette, 'progression': seed % len(music.PROGRESSIONS['major']),
            'seed': 11 + seed % 997, 'energies': energies, 'gain': -9}
    if backbeat:
        plan['backbeat'] = backbeat
    if reveal_bar is not None:
        plan.update(revealBar=reveal_bar, revealFrame=reveal)
    if end_bar is not None:
        plan['endBar'] = end_bar
    return plan


def resolution_bar(reveal_bar, bars, bar, total_s):
    """The bar where the music resolves when a reveal comes well before the end, or None to resolve on the reveal.
    A reveal followed by more than 1.5 bars and 3 s would leave the music ringing out over a long, empty tail (the
    owner's Bounce Party test, 2026-10-08), so the music plays on and resolves in the last bar that leaves the ending
    at least 1 s, or half a bar, to ring."""
    if reveal_bar is None:
        return None
    last = bars - 1
    if total_s - last * bar < max(1.0, 0.5 * bar):
        last -= 1
    tail = total_s - reveal_bar * bar
    return last if last > reveal_bar and tail > max(3.0, 1.5 * bar) else None


def cue_table(score, cues):
    fps = score['fps']['num'] / score['fps']['den']
    rows = ['| Frame | Time | Sound | Gain | Pan | Event |', '| ---: | ---: | --- | ---: | ---: | --- |']
    rows += [f"| {c['frame']} | {c['frame'] / fps:.2f} s | {c['sound']} | {c['gain']} dB | {c['pan']} | {c.get('event', '')} |" for c in cues]
    return '\n'.join(rows) + '\n'


# ---------------------------------------------------------------- rendering

def align_of(score, cue):
    """Which instant of a cue's sound lands on its frame: from its recipe when the video has designed sounds."""
    designed = (score.get('soundDesign') or {}).get('recipes') or {}
    role = generate.ROLE_OF.get(cue['sound'])
    if role in designed:
        return designed[role].get('align', 'onset')
    return synth.DESIGNS[cue['sound']][1]


def render_cue(score, cue, seed, key):
    """A cue's sound: its role's recipe designed for this video, fitted to the cue, or the built-in design."""
    designed = (score.get('soundDesign') or {}).get('recipes') or {}
    role = generate.ROLE_OF.get(cue['sound'])
    if role not in designed:
        return synth.render_design(cue['sound'], cue.get('params'), seed, key)
    p, params = cue.get('params') or {}, {}
    if role in ('transition', 'riser') and p.get('duration'):
        params['duration'] = p['duration']
    if role == 'transition':
        params.update(direction=p.get('direction', 1), intensity=p.get('intensity', 0.8))
    if role in ('landing', 'press', 'release', 'tick') and p.get('pitch'):
        params['pitch'] = p['pitch']
    if role == 'accent':
        root, minor = synth.key_root(key)
        scale = [0, 2, 3, 5, 7, 8, 10] if minor else [0, 2, 4, 5, 7, 9, 11]
        degree = int(p.get('degree', 0))
        params['pitch'] = 2 ** ((scale[degree % 7] + 12 * (degree // 7)) / 12)
    return recipes.render(recipes.instantiate(designed[role], params), seed)


def render_effects(score, cues, indexes=None):
    """The effects bus and its reverb send, and each cue's hit sample with its alignment kind. `indexes` gives each cue's
    position in the contract's full cue list when only some cues are rendered, so every cue keeps the seed of the mix."""
    fps = score['fps']['num'] / score['fps']['den']
    length = round(score['totalFrames'] / fps * RATE)
    key = ((score.get('soundDesign') or {}).get('music') or {}).get('key', 'D major')
    dry, send, hits = np.zeros((length, 2)), np.zeros((length, 2)), []
    for position, cue in enumerate(cues):
        index = indexes[position] if indexes is not None else position
        seed = 1000 + ((score.get('soundDesign') or {}).get('seed') or 0) % 9973 + 7 * index
        audio, offset = render_cue(score, cue, seed, key)
        hit = round(cue['frame'] / fps * RATE)
        start = hit - round(offset * RATE)
        gain = 10 ** (cue.get('gain', 0) / 20)
        theta = (max(-1.0, min(1.0, cue.get('pan', 0))) + 1) * math.pi / 4
        audio = audio * gain * np.array([math.cos(theta), math.sin(theta)]) * math.sqrt(2)
        a, b = max(0, start), min(length, start + len(audio))
        if b > a:
            dry[a:b] += audio[a - start:b - start]
            send[a:b] += audio[a - start:b - start] * SENDS.get(cue['sound'], 0.1)
        hits.append((hit, align_of(score, cue), start))
    return dry, send, hits


def master(mix, target_lufs, ceiling_db=-1.0):
    """High-pass, glue the loudest moments, limit, set loudness with ffmpeg's loudnorm analysis, limit again. Returns (audio, notes)."""
    spec_len = len(mix)
    for c in range(2):
        mix[:, c] = synth.shaped(mix[:, c], lambda t, f: synth.highpass(f, 28, 2), 4096, 1024)
    # Glue: the loudest moments (a final hit over the music) are brought 6 dB closer to the rest at 2.5:1.
    power = np.convolve(np.mean(mix ** 2, axis=1), np.ones(RATE // 100) / (RATE // 100), mode='same')
    if power.max() > 0:
        mix = synth.compress(mix, 10 * math.log10(power.max()) - 6, 2.5)
    out = synth.limit(mix, ceiling_db - 0.5)
    notes = {}
    for _ in range(3):
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
        notes.update(lufs=measured[0], true_peak_db=round(synth.true_peak_db(out), 2), method='loudnorm analysis, bus glue and true-peak limiter')
    return out[:spec_len], notes


def mux(video, wav, out, score):
    duration = score['totalFrames'] * score['fps']['den'] / score['fps']['num']
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', video, '-i', wav, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                    '-c:a', 'aac', '-b:a', '256k', '-t', f'{duration:.6f}', out], check=True)


def deliver(video, wav, out, score, mastered, tmp, ceiling_db=-1.0):
    """Mux the master into the MP4 with the picture copied, then measure the delivered AAC itself: encoding can raise
    peaks between samples, so when the file's true peak passes the ceiling the master is trimmed by the excess (plus a
    margin) and muxed again. Returns what the delivered file measures."""
    mux(video, wav, out, score)
    decoded = read_wav(out)
    peak = synth.true_peak_db(decoded)
    trimmed = 0.0
    if peak > ceiling_db:
        trimmed = round(peak - ceiling_db + 0.2, 2)
        trimmed_wav = os.path.join(tmp, 'trimmed.wav')
        write_wav(mastered * 10 ** (-trimmed / 20), trimmed_wav)
        mux(video, trimmed_wav, out, score)
        decoded = read_wav(out)
        peak = synth.true_peak_db(decoded)
    measured = loudness_of(decoded)
    return {'lufs': measured[0] if measured else None, 'true_peak_db': round(peak, 2), 'trimmed_db': trimmed, 'measured_on': 'the delivered AAC'}


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
    bed_track = np.zeros((length, 2))
    source = (score.get('music') or {}).get('src')
    if source:
        track = read_wav(os.path.join(base_dir, source))[:length]
        bed_track[:len(track)] = track * float((score.get('music') or {}).get('volume', 1))
    elif music_plan.get('compose'):
        if music_plan.get('recipe'):
            bed = compose.render_music(music_plan['recipe'], length / RATE, music_plan['bpm'], music_plan['energies'], music_plan.get('seed', 11), music_plan.get('revealBar'),
                                           music_plan.get('endBar'))
        else:
            bed = music.compose_bed(length / RATE, music_plan['bpm'], music_plan['key'], music_plan['energies'], music_plan.get('seed', 11),
                                    music_plan.get('revealBar'), music_plan.get('palette', 'studio'), music_plan.get('progression', 0),
                                    music_plan.get('backbeat'), music_plan.get('endBar'))
        bed_track[:len(bed)] = bed[:length] * 10 ** (music_plan.get('gain', -9) / 20)
        send[:len(bed)] += bed[:length] * 10 ** (music_plan.get('gain', -9) / 20) * 0.12
    voice, under = np.zeros((length, 2)), []
    if (score.get('voiceover') or {}).get('src'):
        track = read_wav(os.path.join(base_dir, score['voiceover']['src']))[:length]
        voice[:len(track)] = track * float(score['voiceover'].get('volume', 1))
        under += score.get('captions') or []
    original = (score.get('source') or {}).get('originalAudio') or {}
    if original.get('src'):
        # Supplied footage keeps its own sound; the music ducks under the stretches where that sound is present.
        track = read_wav(os.path.join(base_dir, original['src']))[:length]
        voice[:len(track)] += track * float(original.get('volume', 1))
        under += (score.get('source') or {}).get('duck') or []
    if under:
        ramp, duck = RATE // 10, np.ones(length)
        for span in under:
            a, b = round(span['start'] / fps * RATE), round(span['end'] / fps * RATE)
            duck[max(0, a - ramp):min(length, b + ramp)] = 10 ** (-8 / 20)
        bed_track *= synth.moving_average(duck, ramp, 'same')[:, None]
    bed_track *= hit_ducking(score, length)[:, None]
    wet = synth.convolve(send, synth.reverb_ir())[:length]
    return dry + bed_track + voice + 0.6 * wet, dry, hits, bed_track


def hit_ducking(score, length):
    """Music gain that dips briefly under booms, louder impacts and clicks, so each hit reads clearly without the
    music pumping: the dip starts 5 ms before the hit, holds 60 ms and recovers smoothly."""
    fps = score['fps']['num'] / score['fps']['den']
    gain = np.ones(length)
    for cue in score.get('sfx') or []:
        depth, release = DUCKS.get(cue['sound'], (0, 0))
        if not depth or cue.get('gain', 0) < -10:
            continue
        hit = round(cue['frame'] / fps * RATE)
        a, hold = max(0, hit - RATE // 200), hit + int(0.06 * RATE)
        n = min(length, hold + int(4 * release * RATE)) - a
        if n <= 0:
            continue
        k, floor, pre = np.arange(n), 10 ** (-depth / 20), max(1, hit - a)
        recover = 1 - (1 - floor) * np.exp(-np.maximum(k - (hold - a), 0) / (release * RATE))
        curve = np.where(k < pre, 1 - (1 - floor) * k / pre, np.where(k < hold - a, floor, recover))
        gain[a:a + n] = np.minimum(gain[a:a + n], curve)
    return gain


# ---------------------------------------------------------------- checking

# About -80 dBFS: below this a cue window holds no sound to measure.
SIGNAL_FLOOR = 1e-4


def check_hits(effects, hits):
    """Where each hit landed in an effects track: the first sample above half the local peak, or a whoosh's loudest
    10 ms. Risers end on their frame by construction and are not measured; a transient within 50 ms of another cue, or a
    swell whose 250 ms window another sound plays into (from its start to 150 ms past its hit), is reported as masked
    rather than judged. A cue with no signal above SIGNAL_FLOOR in its window is reported as missing: never as measured,
    never as on time."""
    mono = np.mean(effects, axis=1)
    report = []
    hits = [h if len(h) == 3 else (h[0], h[1], h[0]) for h in hits]
    for index, (expected, align, _) in enumerate(hits):
        reach = RATE // 4 if align == 'peak' else RATE // 20
        if align == 'peak':
            # A swell is judged only when no other sound plays in its window: from that sound's start to 150 ms past its hit.
            masked = any(j != index and start < expected + reach and h + int(0.15 * RATE) > expected - reach for j, (h, _, start) in enumerate(hits))
        else:
            masked = any(j != index and abs(h - expected) <= reach for j, (h, _, _) in enumerate(hits))
        if align == 'end':
            report.append({'sample': expected, 'kind': align, 'offset_ms': 0.0, 'ok': True, 'masked': masked, 'measured': False})
            continue
        if align == 'peak':
            lo, hi = max(0, expected - RATE // 4), min(len(mono), expected + RATE // 4)
            env = np.convolve(mono[lo:hi] ** 2, np.ones(RATE // 100) / (RATE // 100), mode='same') if hi > lo else np.zeros(1)
            level = math.sqrt(float(env.max()))
            found = lo + int(np.argmax(env))
            tolerance = 15.0
        else:
            lo, hi = max(0, expected - RATE // 200), min(len(mono), expected + RATE // 50)
            window = np.abs(mono[lo:hi]) if hi > lo else np.zeros(1)
            level = float(window.max())
            found = lo + int(np.argmax(window >= 0.5 * level))
            tolerance = 2.0
        if level < SIGNAL_FLOOR:
            report.append({'sample': expected, 'kind': align, 'offset_ms': None, 'ok': False, 'masked': masked, 'measured': False, 'missing': True})
            continue
        offset = (found - expected) / RATE * 1000
        report.append({'sample': expected, 'kind': align, 'offset_ms': round(offset, 2), 'ok': True if masked else abs(offset) <= tolerance, 'masked': masked, 'measured': True})
    return report


def timing_check(score):
    """Check every cue in a solo render: its own sound alone on the timeline, with the seed it has in the mix, so no
    neighbour can mask it. Every transient and swell is judged; risers end on their frame by construction."""
    cues = score.get('sfx') or []
    report = []
    for index, cue in enumerate(cues):
        effects, _, hits = render_effects(score, [cue], [index])
        report += check_hits(effects, hits)
    return summarize(report)


def summarize(report):
    """Counts and a status that says what the timing claim covers: `checked` (every transient and swell judged),
    `partly_judged` or `not_judged` (some or all sat too close to another cue to be measured in one track), `missing`
    (a cue window holds no sound) or `by_construction` (risers only)."""
    measurable = [r for r in report if r['kind'] != 'end']
    judged = [r for r in measurable if r['measured'] and not r['masked']]
    missing = sum(1 for r in report if r.get('missing'))
    if missing:
        status = 'missing'
    elif not measurable:
        status = 'by_construction'
    elif len(judged) == len(measurable):
        status = 'checked'
    else:
        status = 'partly_judged' if judged else 'not_judged'
    return {'cues': len(report), 'judged': len(judged), 'not_judged': len(measurable) - len(judged) - missing, 'by_construction': len(report) - len(measurable),
            'missing': missing, 'max_offset_ms': max((abs(r['offset_ms']) for r in judged), default=0.0),
            'all_ok': not missing and all(r['ok'] for r in report), 'status': status}


def timing_exit(summary):
    """0 when every cue is on its frame and the claim is complete, 1 when a cue is off its frame or missing, 3 when the
    claim is incomplete (cues that could not be judged), as the craft critique does."""
    if not summary['all_ok']:
        return 1
    return 0 if summary['status'] in ('checked', 'by_construction') else 3


# ---------------------------------------------------------------- command line

def next_revision(score, evidence):
    revision = (score.get('revision') or 0) + 1
    out = dict(score, revision=revision)
    out['approval'] = {'status': 'approved', 'revision': revision, 'evidence': evidence} if evidence else {'status': 'proposed', 'revision': None, 'evidence': None}
    return out


def design_video(score, args):
    """Direct this video's sound and design its effects anew: (direction, seed, recipes, design log, fixed lead)."""
    fixed = overrides(args, score)
    kinds = {role: fixed.pop(role) for role in list(fixed) if role in generate.KINDS}
    lead = fixed.pop('lead', None)
    chosen = sound_direction(score, fixed)
    # Every choice the user fixed is recorded with the others, so the contract shows what came from the user.
    for role, kind in kinds.items():
        chosen['choices'][role] = {'option': kind, 'why': 'set by the user'}
    if lead:
        chosen['choices']['lead'] = {'option': lead, 'why': 'set by the user'}
    seed = (content_seed(score) + 104729 * getattr(args, 'variation', 0)) % 100000
    designed, log = generate.design_effects(chosen['profile'], seed, chosen['key'], chosen['character'], kinds)
    return chosen, seed, designed, log, lead


def compose_music(chosen, seed, lead, log):
    """Compose this video's music recipe anew and add a one-line summary to the design log."""
    composed = compose.generate_music(chosen['profile'], seed + 17, chosen['key'], chosen['palette'], {'lead': lead} if lead else None)
    parts = ', '.join(f"{part} {spec['family']}" for part, spec in composed['parts'].items() if spec)
    log['music'] = (f"{' '.join(chord['name'] for chord in composed['progression'])} ({composed['colour']}), {parts}, "
                    f"lead plays {composed['rhythm']['lead_mode']}, {composed['drums']['kit']} kit, ends with "
                    f"{ {'strike': 'a struck chord', 'arpeggio': 'a rising arpeggio', 'motif': 'the motif'}[composed['ending']] }")
    return composed


def overrides(args, score=None):
    """Choices the user fixed, checked against the sound base: those recorded in the contract as set by the user
    (so planning again after a revision keeps them), then the command line, which wins."""
    roles = directing.load_base()['roles']
    allowed = {name: list(r['options']) for name, r in roles.items()}
    allowed.update(generate.KINDS, lead=compose.LEAD_FAMILIES)
    recorded = (((score or {}).get('soundDesign') or {}).get('direction') or {}).get('choices') or {}
    kept = [f'{role}={choice["option"]}' for role, choice in recorded.items()
            if isinstance(choice, dict) and choice.get('why') == 'set by the user' and role != 'palette']
    fixed = {}
    if isinstance(recorded.get('palette'), dict) and recorded['palette'].get('why') == 'set by the user':
        fixed['palette'] = recorded['palette']['option']
    if getattr(args, 'palette', None):
        fixed['palette'] = args.palette
    for item in kept + (getattr(args, 'set', None) or []):
        role, _, option = item.partition('=')
        role, option = role.strip(), option.strip()
        if role == 'key':
            name, _, mode = option.partition(' ')
            if name not in synth.NOTE_NAMES or mode not in ('major', 'minor'):
                raise ValueError(f'--set {item}: a key is a note and major or minor, for example key="E minor"')
        elif role not in allowed or option not in allowed[role]:
            known = '; '.join(f'{name}: {"/".join(options)}' for name, options in allowed.items())
            raise ValueError(f'--set {item}: unknown role or option ({known}; or key="E minor")')
        fixed[role] = option
    return fixed


def main(argv=None):
    parser = argparse.ArgumentParser(description='Plan, render and check motion sound design.')
    sub = parser.add_subparsers(dest='command', required=True)
    plan = sub.add_parser('plan')
    plan.add_argument('contract')
    plan.add_argument('--out', required=True)
    plan.add_argument('--density', default='standard', choices=DENSITIES)
    plan.add_argument('--no-music', action='store_true', help='effects only (a supplied music.src is always used instead of composing)')
    for command in (plan, sub.add_parser('analyze', help="print this video's sound profile and the choices made for it")):
        if command is not plan:
            command.add_argument('contract')
        command.add_argument('--palette', choices=sorted(music.PALETTES), help="music palette instead of the chosen one")
        command.add_argument('--set', action='append', default=[], metavar='ROLE=OPTION',
                             help='fix a choice: palette=midnight, key="E minor", landing=blip, transition=whip, impact=thud, accent=bell, lead=piano')
        command.add_argument('--variation', type=int, default=0, help='a new design for the same video (0 is the first)')
    plan.add_argument('--evidence')
    plan.add_argument('--table')
    mix = sub.add_parser('mix')
    mix.add_argument('contract')
    mix.add_argument('--video')
    mix.add_argument('--out')
    mix.add_argument('--wav')
    mix.add_argument('--stems', help='folder for the dry effects.wav and music.wav stems, before reverb and mastering')
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
            chosen, seed, designed, log, lead = design_video(score, args)
            cues = plan_cues(score, args.density, chosen, designed)
            result = next_revision(score, args.evidence)
            design = {'engine': 'studio-generative-1', 'density': args.density, 'status': 'planned', 'seed': seed, 'variation': args.variation,
                      'direction': {'profile': chosen['profile'], 'choices': chosen['choices'], 'character': chosen['character'], 'designed': log},
                      'recipes': designed}
            if not args.no_music and not (score.get('music') or {}).get('src'):
                design['music'] = plan_music(score, direction=chosen)
                design['music']['seed'] = 11 + seed % 997
                composed = compose_music(chosen, seed, lead, log)
                design['music']['recipe'] = composed
                design['music']['palette'] = composed['palette']
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
            planned_music = design.get('music', {})
            print(json.dumps({'cues': len(cues), 'by_sound': counts, 'density': args.density, 'music': planned_music.get('bpm'), 'palette': planned_music.get('palette'),
                              'key': chosen['key'], 'designed': log, 'seed': seed, 'out': args.out}, ensure_ascii=False))
            return 0
        if args.command == 'analyze':
            chosen, seed, designed, log, lead = design_video(score, args)
            compose_music(chosen, seed, lead, log)
            print(json.dumps({'profile': chosen['profile'], 'choices': chosen['choices'], 'character': chosen['character'], 'designed': log, 'seed': seed},
                             indent=2, ensure_ascii=False))
            return 0
        if args.command == 'check':
            fps = score['fps']['num'] / score['fps']['den']
            cues = score.get('sfx') or []
            hits = [(round(c['frame'] / fps * RATE), align_of(score, c)) for c in cues]
            summary = summarize(check_hits(read_wav(args.wav), hits))
            if summary['status'] in ('partly_judged', 'not_judged'):
                summary['note'] = (f"{summary['not_judged']} of {summary['cues']} cues sit too close to another cue to be judged in one track. "
                                   'For a mix made by sound.py, report the mix timing, which judges every cue in a solo render.')
            print(json.dumps(summary))
            return timing_exit(summary)
        if (score.get('soundDesign') or {}).get('status') == 'stale':
            raise ValueError('The sound design is stale: ' + (score['soundDesign'].get('staleReason') or 'the timing changed') + '. Run sound.py plan on this contract first; it keeps the choices the user fixed.')
        if args.out and not args.video:
            raise ValueError('--out needs --video')
        for path in (args.out, args.wav):
            if path and os.path.exists(path):
                raise ValueError(f'Output file already exists: {path}')
        mixed, effects, hits, music_stem = full_mix(score, os.path.dirname(os.path.abspath(args.contract)))
        timing = timing_check(score)
        mastered, notes = master(mixed, args.lufs)
        summary = {'cues': len(score.get('sfx') or []), 'timing': timing, 'loudness': notes}
        with tempfile.TemporaryDirectory() as tmp:
            wav = args.wav or os.path.join(tmp, 'mix.wav')
            write_wav(mastered, wav)
            if args.stems:
                os.makedirs(args.stems, exist_ok=True)
                write_wav(effects, os.path.join(args.stems, 'effects.wav'), 'pcm_f32le')
                write_wav(music_stem, os.path.join(args.stems, 'music.wav'), 'pcm_f32le')
            if args.out:
                summary['out'] = args.out
                summary['delivered'] = deliver(args.video, wav, args.out, score, mastered, tmp)
        summary['wav'] = args.wav
        print(json.dumps(summary))
        return 0 if timing_exit(timing) == 0 else 1
    except (OSError, ValueError, RuntimeError, KeyError, subprocess.CalledProcessError) as error:
        sys.stderr.write(f'{error}\n')
        return 2


if __name__ == '__main__':
    sys.exit(main())
