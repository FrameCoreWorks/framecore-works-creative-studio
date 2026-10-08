"""Design new sounds for one video: a recipe for every role, generated from the video's profile and seed.

Nothing is picked from a list of finished sounds. For each role (transition, landing, press, release, tick, impact,
boom, riser, accent) the generator chooses a kind of sound by the video's moods (a struck object, a tonal blip, a
small swish, a plucked string, a felt thump...), then designs it: material and its resonances, pitches tuned to the
music's key, band paths, envelopes, layers and their balance, each drawn from ranges that keep it at studio
standard. A new video, or a new variation of the same one, gets a new design. The recipes go into the contract
(soundDesign.recipes), where the host model or a person can read and reshape them; recipe.py renders them.
"""
import math

import numpy as np

from synth import key_root, midi_hz, rng

# Resonance ratios of materials (bars, plates, shells), perturbed for every design.
MATERIALS = {
    'wood': {'ratios': [1, 1.58, 2.31, 3.12, 4.18, 5.43, 7.1], 'decay': 0.09, 'freq': (140, 260), 'moods': {'organic': 0.9, 'calm': 0.5, 'editorial': 0.5}},
    'glass': {'ratios': [1, 2.76, 5.40, 8.93], 'decay': 0.35, 'freq': (700, 1400), 'moods': {'technical': 0.6, 'calm': 0.6, 'editorial': 0.3}},
    'metal': {'ratios': [1, 1.59, 2.14, 2.30, 2.65, 2.92, 3.16, 3.50], 'decay': 0.18, 'freq': (300, 700), 'moods': {'bold': 0.7, 'technical': 0.6}},
    'plastic': {'ratios': [1, 1.8, 2.9, 4.3], 'decay': 0.03, 'freq': (500, 1100), 'moods': {'playful': 0.8, 'technical': 0.6}},
    'ceramic': {'ratios': [1, 2.1, 3.6, 5.2, 7.4], 'decay': 0.12, 'freq': (400, 800), 'moods': {'editorial': 0.8, 'calm': 0.4}},
    'skin': {'ratios': [1, 1.59, 2.14, 2.30, 2.65], 'decay': 0.08, 'freq': (90, 180), 'moods': {'bold': 0.6, 'organic': 0.5, 'playful': 0.3}},
}
SCALES = {False: [0, 2, 4, 5, 7, 9, 11], True: [0, 2, 3, 5, 7, 8, 10]}
LEVELS = {'transition': ('peak', 0.8), 'landing': ('rms', 0.44), 'press': ('rms', 0.21), 'release': ('rms', 0.12), 'tick': ('rms', 0.11),
          'impact': ('rms', 0.63), 'boom': ('rms', 0.65), 'riser': ('peak', 0.7), 'accent': ('rms', 0.3)}


class Designer:
    def __init__(self, profile, seed, key, forced=None):
        self.forced = dict(forced or {})
        self.moods = profile.get('moods') or {}
        self.pace = profile.get('pace', 'medium')
        self.r = rng(seed)
        self.root, self.minor = key_root(key)
        self.log = {}

    def u(self, low, high):
        return round(float(self.r.uniform(low, high)), 4)

    def pick(self, options, why_role=None):
        """Choose among {name: mood weights}: better-fitting kinds are likelier, never certain."""
        if why_role in self.forced:
            self.log[why_role] = f'{self.forced[why_role]}: set by the user'
            return self.forced[why_role]
        names = list(options)
        fit = np.array([sum(self.moods.get(m, 0) * w for m, w in options[n].items()) / (sum(options[n].values()) or 1) for n in names])
        p = np.exp(6 * fit)
        p /= p.sum()
        name = names[int(self.r.choice(len(names), p=p))]
        if why_role:
            leading = sorted(options[name], key=lambda m: -self.moods.get(m, 0) * options[name][m])[:2]
            self.log[why_role] = f'{name}: fits {" and ".join(leading)}'
        return name

    def tuned(self, octave, degrees=(0, 2, 4)):
        """A pitch in the music's key: a chosen scale degree in the given octave above the key root."""
        scale = SCALES[self.minor]
        degree = int(self.r.choice(degrees))
        return midi_hz(self.root + 12 * octave + scale[degree % 7])

    def material(self, role):
        name = self.pick({k: v['moods'] for k, v in MATERIALS.items()}, role + ' material')
        spec = MATERIALS[name]
        modes = [[round(ratio * (1 + self.u(-0.04, 0.04)) if i else 1.0, 4), round(spec['decay'] * self.u(0.7, 1.3) / (1 + 0.5 * i), 4), round(self.u(0.25, 1.0) if i else 1.0, 3)]
                 for i, ratio in enumerate(spec['ratios'])]
        return name, spec, modes

    def level(self, role):
        kind, value = LEVELS[role]
        return {'type': kind, 'value': value}

    # ------------------------------------------------------------ roles

    def transition(self):
        kind = self.pick({'air': {'calm': 0.6, 'organic': 0.5, 'editorial': 0.5}, 'tonal': {'technical': 0.8, 'bold': 0.4},
                          'whip': {'bold': 0.8, 'playful': 0.4}, 'flutter': {'playful': 0.7, 'organic': 0.4},
                          'crossing': {'technical': 0.5, 'editorial': 0.5}}, 'transition')
        d, p = 0.6, self.u(0.4, 0.62)
        lo, hi = self.u(170, 380), self.u(1700, 3600) * (1.15 if kind in ('whip', 'tonal') else 1.0)
        layers = [{'type': 'noise', 'color': self.u(-0.6, -0.3), 'path': [[0, lo], [p * d, hi], [d + 0.25, lo * 1.3]], 'width': self.u(0.9, 1.4),
                   'env': {'a': p * d, 'd': self.u(0.1, 0.22) * (0.6 if kind == 'whip' else 1.0), 'curve': self.u(2.0, 3.2) + (1.2 if kind == 'whip' else 0)},
                   'gain': 1.0, 'pan': [-0.7, 0.7]},
                  {'type': 'noise', 'color': 0.0, 'path': [[0, 6500], [p * d, 9500]], 'width': 0.8, 'env': {'a': p * d, 'd': 0.08, 'curve': 3}, 'gain': self.u(0.06, 0.14), 'pan': [-0.8, 0.8]}]
        if kind == 'tonal':
            f0 = self.tuned(0, (0, 4))
            layers.append({'type': 'tone', 'wave': 'saw', 'freq': [f0, f0 * self.u(2.0, 3.0)], 'glide': p * d, 'lowpass': 2200,
                           'env': {'a': p * d, 'd': 0.12, 'curve': 2.5}, 'gain': self.u(0.18, 0.3), 'pan': [-0.5, 0.5]})
        elif kind == 'flutter':
            layers[0]['tremolo'] = {'rate': self.u(14, 26), 'depth': self.u(0.4, 0.7), 'accel': self.u(1.0, 1.6)}
        elif kind == 'crossing':
            layers.append({'type': 'noise', 'color': -0.2, 'path': [[0, hi * 1.3], [p * d, lo * 2.2], [d + 0.25, lo * 1.5]], 'width': 0.7,
                           'env': {'a': p * d, 'd': 0.14, 'curve': 2.2}, 'gain': self.u(0.35, 0.55), 'pan': [0.6, -0.6]})
        elif kind == 'air':
            layers.append({'type': 'noise', 'color': -0.9, 'path': [[0, lo * 0.6], [p * d, lo * 1.4]], 'width': 1.2,
                           'env': {'a': p * d, 'd': 0.2, 'curve': 2}, 'gain': self.u(0.3, 0.5), 'pan': [-0.4, 0.4]})
        return {'role': 'transition', 'kind': kind, 'align': 'peak', 'length': d + 0.25, 'stretch': True, 'stretch_base': d,
                'pitch_bands': False, 'norm': self.level('transition'), 'layers': layers}

    def landing(self):
        kind = self.pick({'struck': {'organic': 0.8, 'editorial': 0.5, 'calm': 0.3, 'technical': 0.3},
                          'blip': {'playful': 0.9, 'technical': 0.5}, 'swish': {'bold': 0.7, 'technical': 0.4},
                          'pluck': {'organic': 0.6, 'calm': 0.6, 'playful': 0.2}, 'felt': {'calm': 0.8, 'editorial': 0.5},
                          'none': {'editorial': 0.35, 'calm': 0.15}}, 'landing')
        if kind == 'none':
            return {'role': 'landing', 'kind': 'none', 'align': 'onset', 'length': 0.1, 'norm': self.level('landing'), 'layers': []}
        if self.pace == 'fast' and kind == 'pluck':
            kind = 'blip'
        layers = []
        align = 'onset'
        if kind == 'struck':
            name, spec, modes = self.material('landing')
            f = self.u(*spec['freq'])
            layers += [{'type': 'modal', 'freq': f, 'modes': modes, 'exciter': {'ms': self.u(0.8, 2.5), 'cutoff': self.u(4000, 9000)}, 'gain': 0.85, 'env': {'a': 0.0003, 'd': 1.0}},
                       {'type': 'tone', 'wave': 'sine', 'freq': [self.u(100, 150), self.u(55, 80)], 'glide': 0.018, 'env': {'a': 0.0005, 'd': self.u(0.03, 0.06)}, 'gain': self.u(0.3, 0.6)},
                       {'type': 'noise', 'color': -0.2, 'path': [[0, self.u(2200, 4200)]], 'width': 1.0, 'env': {'a': 0.0002, 'd': self.u(0.003, 0.006)}, 'gain': self.u(0.4, 0.8)}]
        elif kind == 'blip':
            f = self.tuned(1, (0, 2, 4))
            layers += [{'type': 'tone', 'wave': {'partials': [[1, 1], [2, self.u(0.1, 0.4)], [3, self.u(0.0, 0.15)]]}, 'freq': [f, f * self.u(1.4, 2.4)], 'glide': self.u(0.008, 0.016),
                        'env': {'a': 0.0015, 'd': self.u(0.018, 0.035)}, 'gain': 1.0},
                       {'type': 'noise', 'color': -0.3, 'path': [[0, self.u(1400, 2400)]], 'width': 0.8, 'env': {'a': 0.0005, 'd': 0.004}, 'gain': self.u(0.15, 0.3)},
                       {'type': 'modal', 'freq': self.u(900, 1400), 'modes': [[1, 0.01, 1], [1.8, 0.006, 0.5]], 'exciter': {'ms': 0.6, 'cutoff': 9000}, 'gain': self.u(0.15, 0.3), 'env': {'a': 0.0002, 'd': 1}}]
        elif kind == 'swish':
            # A small whoosh as the text arrives: a pink-noise band rising to its brightest on the landing and falling
            # away, with a little air on top, moving across; no thump, so it never reads as a drum.
            align = 'peak'
            dur, p = self.u(0.16, 0.28), self.u(0.55, 0.7)
            lo, hi = self.u(300, 520), self.u(1700, 3000)
            layers += [{'type': 'noise', 'color': self.u(-0.6, -0.35), 'path': [[0, lo], [p * dur, hi], [dur + 0.12, lo * 1.4]], 'width': self.u(1.0, 1.3),
                        'env': {'a': p * dur, 'd': self.u(0.04, 0.08), 'curve': self.u(2.0, 2.8)}, 'gain': 1.0, 'pan': [-0.45, 0.45]},
                       {'type': 'noise', 'color': 0.0, 'path': [[0, 5000], [p * dur, 8000]], 'width': 0.8, 'env': {'a': p * dur, 'd': 0.03, 'curve': 3}, 'gain': self.u(0.05, 0.1), 'pan': [-0.6, 0.6]}]
        elif kind == 'pluck':
            f = self.tuned(1, (0, 2, 4))
            layers += [{'type': 'string', 'freq': f, 'brightness': self.u(0.3, 0.6), 'damping': self.u(0.985, 0.993), 'env': {'a': 0.001, 'd': self.u(0.08, 0.16)}, 'gain': 1.0},
                       {'type': 'tone', 'wave': 'sine', 'freq': [self.u(110, 140), 70], 'glide': 0.02, 'env': {'a': 0.0005, 'd': 0.04}, 'gain': self.u(0.2, 0.4)}]
        else:  # felt
            layers += [{'type': 'tone', 'wave': 'sine', 'freq': [self.u(100, 130), self.u(58, 72)], 'glide': 0.02, 'env': {'a': 0.001, 'd': self.u(0.05, 0.08)}, 'gain': 1.0},
                       {'type': 'modal', 'freq': self.u(160, 240), 'modes': [[1, 0.05, 1], [1.7, 0.035, 0.7], [2.3, 0.03, 0.6], [3.1, 0.02, 0.5], [3.9, 0.015, 0.4], [5.2, 0.01, 0.3]],
                        'exciter': {'ms': self.u(2.0, 3.5), 'cutoff': self.u(1800, 3200)}, 'gain': 0.4, 'env': {'a': 0.001, 'd': 1}},
                       {'type': 'noise', 'color': -0.4, 'path': [[0, self.u(500, 1000)]], 'width': 1.6, 'env': {'a': 0.0008, 'd': self.u(0.012, 0.025)}, 'gain': self.u(0.3, 0.5)},
                       {'type': 'noise', 'color': -0.3, 'path': [[0, self.u(1800, 3200)]], 'width': 1.2, 'env': {'a': 0.0005, 'd': 0.006}, 'gain': self.u(0.25, 0.4)}]
        if kind == 'swish':
            # A swell is levelled by its peak, like the transitions it belongs with, and sits below them.
            return {'role': 'landing', 'kind': kind, 'align': align, 'length': round(dur + 0.15, 4), 'width': self.u(0.1, 0.2),
                    'norm': {'type': 'peak', 'value': 0.6}, 'layers': layers}
        return {'role': 'landing', 'kind': kind, 'align': align, 'length': 0.32, 'drive': self.u(1.1, 1.5), 'width': self.u(0.04, 0.12),
                'norm': self.level('landing'), 'layers': layers}

    def press(self, softness=0.0):
        name, spec, modes = self.material('press')
        f = self.u(1700, 3200) if name not in ('skin', 'wood') else self.u(900, 1600)
        stiff = [[1, self.u(0.008, 0.014), 0.6], [round(self.u(1.5, 1.7), 3), 0.008, 0.45], [round(self.u(2.3, 2.6), 3), 0.005, 0.3]]
        self.press_design = (f, stiff)
        layers = [{'type': 'modal', 'freq': f, 'modes': stiff, 'exciter': {'ms': 0.5, 'cutoff': 12000 * (1 - 0.5 * softness)}, 'gain': 1.0, 'env': {'a': 0.0002, 'd': 1}},
                  {'type': 'tone', 'wave': 'sine', 'freq': [self.u(220, 320), self.u(150, 200)], 'glide': 0.006, 'env': {'a': 0.0003, 'd': self.u(0.008, 0.016)}, 'gain': self.u(0.25, 0.55) * (1 - softness * 0.5)}]
        self.log['press material'] = name
        return {'role': 'press', 'kind': name, 'align': 'onset', 'length': 0.09, 'drive': 1.3, 'norm': self.level('press'), 'layers': layers}

    def release(self):
        f, stiff = getattr(self, 'press_design', (2400, [[1, 0.01, 0.6], [1.6, 0.008, 0.45]]))
        layers = [{'type': 'modal', 'freq': f * 1.25, 'modes': [[r, d * 0.8, g] for r, d, g in stiff], 'exciter': {'ms': 0.7, 'cutoff': 7000}, 'gain': 0.8, 'env': {'a': 0.0002, 'd': 1}},
                  {'type': 'noise', 'color': -0.2, 'path': [[0, self.u(2500, 5000)]], 'width': 1.3, 'env': {'a': 0.0002, 'd': self.u(0.002, 0.004)}, 'gain': self.u(0.5, 0.8)}]
        return {'role': 'release', 'kind': 'press-release', 'align': 'onset', 'length': 0.07, 'norm': self.level('release'), 'layers': layers}

    def tick(self):
        f = self.u(3200, 5200)
        layers = [{'type': 'modal', 'freq': f, 'modes': [[1, self.u(0.004, 0.007), 1], [round(self.u(1.5, 1.8), 3), 0.004, 0.8], [round(self.u(2.4, 2.9), 3), 0.003, 0.5]], 'exciter': {'ms': 0.4, 'cutoff': 14000}, 'gain': 0.8, 'env': {'a': 0.0002, 'd': 1}},
                  {'type': 'noise', 'color': 0.0, 'path': [[0, f * 1.2]], 'width': 1.4, 'env': {'a': 0.0001, 'd': self.u(0.0015, 0.003)}, 'gain': 0.9}]
        return {'role': 'tick', 'kind': 'tick', 'align': 'onset', 'length': 0.05, 'norm': self.level('tick'), 'layers': layers}

    def impact(self, big=False):
        kind = 'boom' if big else self.pick({'sub-drop': {'bold': 0.6, 'technical': 0.5}, 'thud': {'organic': 0.6, 'calm': 0.4, 'editorial': 0.4},
                                             'metal-hit': {'bold': 0.8, 'technical': 0.5}, 'soft': {'calm': 0.8, 'editorial': 0.4}}, 'impact')
        f_hi, f_lo = self.u(130, 210), self.u(46, 62)
        decay = self.u(0.18, 0.32) * (2.2 if big else 1.0)
        layers = [{'type': 'tone', 'wave': 'sine', 'freq': [f_hi, f_lo], 'glide': self.u(0.025, 0.045), 'env': {'a': 0.0005, 'd': decay}, 'gain': 0.8 if kind != 'soft' else 0.6},
                  {'type': 'noise', 'color': -0.6, 'path': [[0, self.u(500, 1100)], [0.3, self.u(150, 300)]], 'width': 1.5, 'env': {'a': 0.0005, 'd': self.u(0.05, 0.12)}, 'gain': self.u(0.4, 0.7)},
                  {'type': 'noise', 'color': 0.0, 'path': [[0, self.u(2500, 4500)]], 'width': 1.2, 'env': {'a': 0.0001, 'd': 0.004}, 'gain': self.u(0.25, 0.5) * (0.4 if kind == 'soft' else 1.0)}]
        if kind == 'metal-hit':
            name, spec, modes = 'metal', MATERIALS['metal'], [[r, 0.25 / (1 + 0.3 * i), 0.6] for i, r in enumerate(MATERIALS['metal']['ratios'])]
            layers.append({'type': 'modal', 'freq': self.tuned(0, (0, 4)), 'modes': modes, 'exciter': {'ms': 1.5, 'cutoff': 6000}, 'gain': self.u(0.2, 0.35), 'env': {'a': 0.0005, 'd': 1}})
        elif kind == 'thud':
            layers.append({'type': 'modal', 'freq': self.u(80, 130), 'modes': [[r, 0.12 / (1 + 0.4 * i), 0.7] for i, r in enumerate(MATERIALS['skin']['ratios'])], 'exciter': {'ms': 3, 'cutoff': 2500}, 'gain': 0.5, 'env': {'a': 0.0005, 'd': 1}})
        if big:
            layers.append({'type': 'tone', 'wave': 'sine', 'freq': self.u(44, 50), 'env': {'a': 0.01, 'd': self.u(0.6, 0.8)}, 'gain': 0.35})
            layers.append({'type': 'noise', 'color': -0.8, 'path': [[0, 1600], [1.6, 180]], 'width': 1.4, 'env': {'a': 0.002, 'd': self.u(0.4, 0.7)}, 'gain': self.u(0.15, 0.3)})
        return {'role': 'boom' if big else 'impact', 'kind': kind, 'align': 'onset', 'length': 2.2 if big else 0.9, 'drive': self.u(1.4, 1.8),
                'width': 0.12, 'norm': self.level('boom' if big else 'impact'), 'layers': layers}

    def riser(self):
        interval = float(self.r.choice([1.5, 2.0, 2.0, 4.0]))
        f0 = self.tuned(0, (0, 4))
        layers = [{'type': 'noise', 'color': self.u(-0.4, -0.1), 'path': [[0, self.u(150, 300)], [1.2, self.u(4000, 8000)]], 'width': 0.8, 'env': {'a': 1.2, 'd': 0.01, 'curve': self.u(1.8, 2.8)}, 'gain': 1.0},
                  {'type': 'tone', 'wave': 'saw', 'freq': [f0, f0 * interval], 'glide': 0.5, 'lowpass': 3000, 'env': {'a': 1.2, 'd': 0.01, 'curve': 2.4}, 'gain': self.u(0.15, 0.3)}]
        if self.r.uniform() < 0.5:
            layers[0]['tremolo'] = {'rate': self.u(4, 8), 'depth': self.u(0.2, 0.5), 'accel': self.u(2.5, 4.0)}
        return {'role': 'riser', 'kind': f'climb x{interval:g}', 'align': 'end', 'length': 1.2, 'stretch': True, 'stretch_base': 1.2,
                'width': 0.35, 'norm': self.level('riser'), 'layers': layers}

    def accent(self):
        kind = self.pick({'bell': {'calm': 0.6, 'editorial': 0.5, 'organic': 0.3}, 'fm-bell': {'technical': 0.7, 'bold': 0.4},
                          'glass': {'technical': 0.5, 'calm': 0.5}, 'chime': {'playful': 0.8, 'calm': 0.3}}, 'accent')
        f = midi_hz(self.root + 24)
        if kind == 'fm-bell':
            layers = [{'type': 'fm', 'freq': f, 'ratio': float(self.r.choice([1.4, 2.76, 3.5])), 'index': [self.u(2, 5), 0.2], 'index_decay': self.u(0.1, 0.3), 'env': {'a': 0.001, 'd': self.u(0.5, 0.9)}, 'gain': 1.0}]
        else:
            spec = MATERIALS['glass']
            modes = [[1, 1.0, 1], [2.0, 0.6, 0.35], [2.76, 0.5, 0.25], [5.4, 0.25, 0.12]] if kind == 'bell' else [[r, spec['decay'] * 2 / (1 + 0.6 * i), 0.8 / (1 + i)] for i, r in enumerate(spec['ratios'])]
            layers = [{'type': 'modal', 'freq': f, 'modes': modes, 'exciter': {'ms': 0.8, 'cutoff': 10000}, 'gain': 1.0, 'env': {'a': 0.001, 'd': 2}, 'pan': -0.25},
                      {'type': 'modal', 'freq': f * self.u(1.002, 1.005), 'modes': [[r * self.u(0.99, 1.01), d * 0.8, g] for r, d, g in modes], 'exciter': {'ms': 0.8, 'cutoff': 10000}, 'gain': 0.8, 'env': {'a': 0.001, 'd': 2}, 'pan': 0.25},
                      {'type': 'fm', 'freq': f * 2, 'ratio': float(self.r.choice([1.4, 3.5])), 'index': [self.u(1.5, 3.0), 0.1], 'index_decay': 0.08, 'env': {'a': 0.001, 'd': self.u(0.2, 0.4)}, 'gain': self.u(0.2, 0.35)},
                      {'type': 'noise', 'color': 0.0, 'path': [[0, self.u(5000, 8000)]], 'width': 1.0, 'env': {'a': 0.0002, 'd': 0.003}, 'gain': 0.3}]
            if kind == 'chime':
                layers.append({'type': 'modal', 'freq': f * 1.5, 'modes': modes, 'exciter': {'ms': 0.8, 'cutoff': 10000}, 'delay': self.u(0.06, 0.12), 'gain': 0.6, 'env': {'a': 0.001, 'd': 2}, 'pan': 0.2})
        return {'role': 'accent', 'kind': kind, 'align': 'onset', 'length': 1.6, 'tuned': True, 'width': 0.15, 'norm': self.level('accent'), 'layers': layers}


KINDS = {'landing': ['struck', 'blip', 'swish', 'pluck', 'felt', 'none'], 'transition': ['air', 'tonal', 'whip', 'flutter', 'crossing'],
         'impact': ['sub-drop', 'thud', 'metal-hit', 'soft'], 'accent': ['bell', 'fm-bell', 'glass', 'chime']}
ROLE_OF = {'whoosh': 'transition', 'landing': 'landing', 'knock': 'landing', 'tap': 'landing', 'pop': 'landing', 'swish': 'landing',
           'click': 'press', 'release': 'release', 'tick': 'tick', 'impact': 'impact', 'boom': 'boom', 'riser': 'riser', 'shimmer': 'accent'}


# The largest share of energy above 150 Hz that one third of an octave may hold. A sound above it is close to a
# single pure tone (a toy beep, or a hollow one-note drum) and is designed again.
PURITY_LIMIT = {'landing': 0.7, 'press': 0.72, 'release': 0.8, 'tick': 0.85, 'impact': 0.75, 'boom': 0.75, 'accent': 0.85}


def purity(audio, rate=48000):
    mono = np.mean(audio, axis=1)
    power = np.abs(np.fft.rfft(mono)) ** 2
    freqs = np.fft.rfftfreq(len(mono), 1 / rate)
    keep = freqs >= 150
    power, freqs = power[keep], freqs[keep]
    total = power.sum() + 1e-20
    return max(power[(freqs >= c / 2 ** (1 / 6)) & (freqs < c * 2 ** (1 / 6))].sum() / total for c in np.geomspace(160, 16000, 120))


def checked(make, role, seed):
    """Design a role until it passes the quality gate (at most six designs; the richest one is kept)."""
    import recipe as renderer
    best = None
    for attempt in range(6):
        design = make(attempt)
        if not design['layers'] or role not in PURITY_LIMIT:
            return design, None
        audio, _ = renderer.render(renderer.instantiate(design, {'duration': 0.5} if design.get('stretch') else {}), seed + attempt)
        score = purity(audio)
        if best is None or score < best[1]:
            best = (design, score)
        if score <= PURITY_LIMIT[role]:
            break
    return best[0], round(float(best[1]), 3)


def design_effects(profile, seed, key, character=None, forced=None):
    """New recipes for every role for this video, with a short log of what was designed and why. `forced`
    ({role: kind}) fixes the kind of sound for a role; the design itself is still new. Every design passes a
    quality gate against near-pure tones before it is kept."""
    softness = (character or {}).get('clickSoftness', 0.0)
    log, recipes, quality = {}, {}, {}
    shared = {}

    def role_maker(role):
        def make(attempt):
            d = Designer(profile, seed + 7919 * attempt + hash_role(role), key, forced)
            if role == 'release':
                d.press_design = shared.get('press')
            design = {'transition': d.transition, 'landing': d.landing, 'press': lambda: d.press(softness), 'release': d.release, 'tick': d.tick,
                      'impact': d.impact, 'boom': lambda: d.impact(big=True), 'riser': d.riser, 'accent': d.accent}[role]()
            if role == 'press':
                shared['press'] = d.press_design
            make.log = d.log
            return design
        return make

    for role in ('transition', 'landing', 'press', 'release', 'tick', 'impact', 'boom', 'riser', 'accent'):
        maker = role_maker(role)
        recipes[role], score = checked(maker, role, seed)
        log.update(getattr(maker, 'log', {}))
        if score is not None:
            quality[role] = score
    log['quality'] = 'largest one-third-octave share above 150 Hz per sound: ' + ', '.join(f'{role} {value}' for role, value in quality.items())
    return recipes, log


def hash_role(role):
    return sum(ord(c) * (i + 1) for i, c in enumerate(role))
