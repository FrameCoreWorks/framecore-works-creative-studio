"""Sound recipes: a small language for designing a sound from layers, and the renderer that plays it.

A recipe is JSON, so Studio's generator, the host model or a person can write and edit it:

  {"role": "landing", "align": "onset", "length": 0.3, "drive": 1.3, "width": 0.1,
   "norm": {"type": "rms", "value": 0.44}, "stretch": false,
   "layers": [
     {"type": "modal", "freq": 180, "modes": [[1, 0.1, 1], [1.58, 0.07, 0.6]], "exciter": {"ms": 2, "cutoff": 4000}, "gain": 0.8},
     {"type": "tone", "freq": [120, 70], "glide": 0.02, "wave": "sine", "env": {"a": 0.001, "d": 0.05}, "gain": 0.5},
     {"type": "noise", "color": -0.2, "path": [[0, 2600]], "width": 0.9, "env": {"a": 0, "d": 0.003}, "gain": 0.4}]}

Layer types:
  tone    a waveform (sine, triangle, saw, square, or "partials": [[ratio, gain], ...]) whose frequency glides from
          freq[0] to freq[1] with time constant `glide`; optional vibrato {rate, depth in semitones}
  fm      a carrier at `freq` modulated at freq * `ratio`, the index falling from index[0] to index[1] with `index_decay`
  noise   noise of `color` (0 white, -0.5 pink, -1 brown) through a band `width` octaves wide whose centre follows
          `path` ([[seconds, hz], ...], log-interpolated); optional `highpass` and `lowpass`
  modal   resonant modes [[ratio, decay s, gain], ...] above `freq`, struck by a noise burst {ms, cutoff, color}
  string  a plucked string at `freq` (Karplus-Strong, tuned exactly) with `brightness` and `damping`
Every layer has `gain`, `env` {a: attack s, h: hold s, d: decay time constant s, curve: attack power}, optional
`tremolo` {rate, depth, accel}, `delay` s, `pan` (a number or [start, end], moving with the sound) and `lowpass` / `highpass` in Hz.

`align` says which instant lands on the cue's frame: the onset (the first sample at half the attack's peak, measured),
the measured loudest 10 ms ("peak") or the end.
`norm` sets the level the role needs in the mix, so a newly designed sound keeps the approved balance.
A recipe is a design for one role in one video; `instantiate` fits it to each cue (its duration, pitch step and
direction) before rendering.
"""
import copy
import math

import numpy as np

import synth
from synth import RATE, band, colored_noise, highpass, lowpass, moving_pan, rng, saturate, seconds, shaped

TIME_KEYS = ('a', 'h', 'd')


def envelope(n, env):
    env = env or {}
    a, h, d, curve = env.get('a', 0.002), env.get('h', 0.0), env.get('d', 0.2), env.get('curve', 2.0)
    t = seconds(n)
    rise = np.clip(t / max(a, 1e-5), 0, 1) ** curve
    fall = np.exp(-np.maximum(t - a - h, 0) / max(d, 1e-4))
    return rise * fall


def wave_partials(wave):
    if isinstance(wave, dict):
        return [tuple(p) for p in wave.get('partials', [[1, 1]])]
    if wave == 'saw':
        return [(k, 1 / k) for k in range(1, 40)]
    if wave == 'square':
        return [(k, 1 / k) for k in range(1, 40, 2)]
    if wave == 'triangle':
        return [(k, (-1) ** ((k - 1) // 2) / k ** 2) for k in range(1, 40, 2)]
    return [(1, 1.0)]


def render_tone(n, layer, seed):
    t = seconds(n)
    f = layer.get('freq', 440)
    f0, f1 = (f, f) if not isinstance(f, (list, tuple)) else (f[0], f[-1])
    freq = f1 + (f0 - f1) * np.exp(-t / max(layer.get('glide', 0.05), 1e-4))
    vib = layer.get('vibrato')
    if vib:
        freq = freq * 2 ** (vib.get('depth', 0.1) / 12 * np.sin(2 * np.pi * vib.get('rate', 5) * t))
    phase = 2 * np.pi * np.cumsum(freq) / RATE
    r = rng(seed)
    out = np.zeros(n)
    for ratio, gain in wave_partials(layer.get('wave', 'sine')):
        if f0 * ratio < RATE / 2.2 and f1 * ratio < RATE / 2.2:
            out += gain * np.sin(phase * ratio + r.uniform(0, 2 * np.pi))
    return out


def render_fm(n, layer, seed):
    t = seconds(n)
    f = layer.get('freq', 440)
    i0, i1 = layer.get('index', [2.0, 0.3])
    index = i1 + (i0 - i1) * np.exp(-t / max(layer.get('index_decay', 0.2), 1e-4))
    modulator = np.sin(2 * np.pi * f * layer.get('ratio', 1.0) * t + rng(seed).uniform(0, 6.28))
    return np.sin(2 * np.pi * f * t + index * modulator)


def path_value(path, time):
    if time <= path[0][0]:
        return path[0][1]
    for (t0, h0), (t1, h1) in zip(path, path[1:]):
        if time <= t1:
            k = (time - t0) / max(t1 - t0, 1e-6)
            return h0 * (h1 / h0) ** k
    return path[-1][1]


def render_noise(n, layer, seed):
    path = [tuple(p) for p in layer.get('path', [[0, 1000]])]
    width = layer.get('width', 1.0)
    return shaped(colored_noise(n, seed, layer.get('color', -0.3)), lambda time, f: band(f, path_value(path, time), width))


def render_modal(n, layer, seed):
    f = layer.get('freq', 200)
    partials = [(f * ratio, decay, gain) for ratio, decay, gain in layer.get('modes', [[1, 0.1, 1]]) if f * ratio < RATE / 2.2]
    exciter = layer.get('exciter') or {}
    body = synth.struck(n, partials, seed, exciter.get('ms', 2.0), exciter.get('cutoff', 5000))
    return body / (np.max(np.abs(body)) + 1e-9)


def render_string(n, layer, seed):
    import music
    return music.guitar(n, layer.get('freq', 220), seed, layer.get('brightness', 0.5), layer.get('damping', 0.996))


RENDERERS = {'tone': render_tone, 'fm': render_fm, 'noise': render_noise, 'modal': render_modal, 'string': render_string}


def render(recipe, seed=1):
    """Render a recipe; returns (stereo audio, alignment offset in seconds)."""
    n = max(1, int(recipe.get('length', 0.5) * RATE))
    mix = np.zeros((n, 2))
    for i, layer in enumerate(recipe.get('layers', [])):
        kind = layer.get('type')
        if kind not in RENDERERS:
            raise ValueError(f'unknown layer type: {kind}')
        start = int(layer.get('delay', 0) * RATE)
        m = n - start
        if m <= 0:
            continue
        x = RENDERERS[kind](m, layer, seed + 101 * i)
        if layer.get('highpass') or layer.get('lowpass'):
            hp, lp = layer.get('highpass'), layer.get('lowpass')
            x = shaped(x, lambda t, f: (highpass(f, hp, 2) if hp else 1) * (lowpass(f, lp, 2) if lp else 1), 1024, 256)
        x = x / (np.max(np.abs(x)) + 1e-9) * envelope(m, layer.get('env')) * layer.get('gain', 1.0)
        trem = layer.get('tremolo')
        if trem:  # amplitude flutter; `accel` multiplies the rate by the end of the layer
            t = seconds(m)
            rate = trem.get('rate', 12) * (1 + (trem.get('accel', 1.0) - 1) * t / max(t[-1], 1e-6))
            x = x * (1 - trem.get('depth', 0.5) * 0.5 * (1 + np.sin(2 * np.pi * np.cumsum(rate) / RATE)))
        pan = layer.get('pan', 0.0)
        p0, p1 = (pan, pan) if not isinstance(pan, (list, tuple)) else (pan[0], pan[-1])
        mix[start:] += moving_pan(x, p0, p1)
    if recipe.get('drive'):
        mix = saturate(mix, recipe['drive'])
    if recipe.get('width'):
        side = synth.stereo(np.mean(mix, axis=1), 0.0, recipe['width'], seed)
        mix = mix + (side - np.stack([np.mean(mix, axis=1)] * 2, axis=1))
    mix = synth.fades(mix, 0.0003, min(0.05, recipe.get('length', 0.5) / 4))
    norm = recipe.get('norm') or {'type': 'peak', 'value': 0.8}
    if norm['type'] == 'rms':
        # The level of the 100 ms that start at the attack's peak (not at the file's first sample, which a slow swell
        # leaves nearly silent and would push far too loud).
        mono = np.mean(mix, axis=1)
        start = int(np.argmax(np.abs(mono[:int(0.3 * RATE)])))
        head = mono[start:start + int(0.1 * RATE)]
        mix *= norm['value'] / (np.sqrt(np.mean(head ** 2)) + 1e-9)
    else:
        mix *= norm['value'] / (np.max(np.abs(mix)) + 1e-9)
    # Whatever the design, no sound leaves the renderer above a sample peak of 1.4 (about +3 dB).
    peak = np.max(np.abs(mix))
    if peak > 1.4:
        mix *= 1.4 / peak
    align = recipe.get('align', 'onset')
    if align == 'end':
        return mix, n / RATE
    if align == 'peak':
        window = RATE // 100
        energy = np.convolve(np.mean(mix, axis=1) ** 2, np.ones(window) / window, mode='same')
        return mix, int(np.argmax(energy)) / RATE
    # Onset: the first sample at half the attack's peak, measured on the rendered sound, so a soft attack still lands
    # its audible start on the frame.
    head = np.abs(np.mean(mix[:int(0.03 * RATE)], axis=1))
    return mix, (int(np.argmax(head >= 0.5 * head.max())) / RATE) if head.max() > 0 else 0.0


def scale_times(layer, factor):
    if layer.get('env'):
        layer['env'] = {k: (v * factor if k in TIME_KEYS else v) for k, v in layer['env'].items()}
    if layer.get('path'):
        layer['path'] = [[t * factor, hz] for t, hz in layer['path']]
    if 'delay' in layer:
        layer['delay'] *= factor
    if 'glide' in layer:
        layer['glide'] *= factor


def instantiate(recipe, params=None):
    """Fit a role's recipe to one cue: `duration` stretches a stretchable sound (a transition, a riser), `pitch`
    multiplies every frequency, `direction` turns the pan (1 left to right, -1 right to left, 0 centred), and
    `intensity` scales the level."""
    params = params or {}
    out = copy.deepcopy(recipe)
    if out.get('stretch') and params.get('duration'):
        factor = params['duration'] / max(out.get('stretch_base', out['length']), 1e-3)
        out['length'] = out['length'] * factor
        for layer in out['layers']:
            scale_times(layer, factor)
    pitch = params.get('pitch')
    if pitch:
        for layer in out['layers']:
            if 'freq' in layer:
                f = layer['freq']
                layer['freq'] = [v * pitch for v in f] if isinstance(f, (list, tuple)) else f * pitch
            if layer.get('path') and layer.get('type') == 'noise' and out.get('pitch_bands', True):
                layer['path'] = [[t, hz * math.sqrt(pitch)] for t, hz in layer['path']]
    if 'direction' in params:
        d = params['direction']
        for layer in out['layers']:
            pan = layer.get('pan', 0.0)
            layer['pan'] = [p * d for p in pan] if isinstance(pan, (list, tuple)) else pan * d
    if 'intensity' in params and out.get('norm'):
        out['norm'] = dict(out['norm'], value=out['norm']['value'] * params['intensity'] / 0.8)
    return out
