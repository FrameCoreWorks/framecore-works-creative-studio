"""Compose new music for one video: a music recipe designed from the video's profile and seed, and its renderer.

Nothing is a stored loop. For every video the composer writes a new chord progression with a grammar of harmonic
functions (tonic, subdominant, dominant), new rhythms for each part from Euclidean patterns shaped by energy and
pace, a short motif in the key, and new instruments: each part gets a timbre designed within the families its style
allows (an additive pad, FM keys, a plucked string, a felt piano, mallets, a filtered saw, a rounded bass), and the
drum kit is designed as recipes (kick, backbeat, hats). The style only constrains the families; the mood and seed
shape the rest. The recipe goes into the contract (soundDesign.music.recipe), so the host model or a person can read
and rewrite it, and render_music plays it to the video's bars, building into the reveal and resolving after it.
"""
import math

import numpy as np

import music
import recipe as recipes
import synth
from synth import RATE, adsr, fades, highpass, midi_hz, pad_voice, rng, saturate, seconds, shaped, stereo

# Families each style allows per part (None: the part is left out).
FAMILIES = {
    'studio': {'pad': ['additive'], 'bass': ['round', 'saw'], 'lead': ['mallet', 'fm', 'pluck'], 'kit': 'band'},
    'meadow': {'pad': ['additive-soft'], 'bass': ['round'], 'lead': ['string', 'fm', 'piano'], 'kit': 'soft'},
    'warm-ink': {'pad': [None, 'additive-soft'], 'bass': ['round'], 'lead': ['fm', 'piano'], 'kit': 'tight'},
    'midnight': {'pad': ['additive-bright'], 'bass': ['saw'], 'lead': ['saw', 'fm'], 'kit': 'electronic'},
    'field-guide': {'pad': ['additive-soft'], 'bass': ['round'], 'lead': ['string', 'mallet'], 'kit': 'organic'},
    'paper-and-ink': {'pad': ['additive-soft'], 'bass': [None, 'round'], 'lead': ['piano', 'mallet', 'fm'], 'kit': 'sparse'},
    'color-block': {'pad': [None, 'additive'], 'bass': ['saw'], 'lead': ['saw', 'fm', 'mallet'], 'kit': 'house'},
}
MAJOR_FUNCTIONS = {'I': (0, 'maj'), 'ii': (2, 'min'), 'iii': (4, 'min'), 'IV': (5, 'maj'), 'V': (7, 'maj'), 'vi': (9, 'min'), 'bVII': (10, 'maj')}
MAJOR_MOVES = {'I': ['IV', 'V', 'vi', 'ii', 'iii'], 'ii': ['V', 'IV'], 'iii': ['vi', 'IV'], 'IV': ['I', 'V', 'ii', 'vi'],
               'V': ['I', 'vi', 'IV'], 'vi': ['IV', 'ii', 'V', 'iii'], 'bVII': ['IV', 'I']}
MINOR_FUNCTIONS = {'i': (0, 'min'), 'iv': (5, 'min'), 'v': (7, 'min'), 'V': (7, 'maj'), 'VI': (8, 'maj'), 'III': (3, 'maj'), 'VII': (10, 'maj')}
MINOR_MOVES = {'i': ['VI', 'iv', 'VII', 'III'], 'iv': ['V', 'VII', 'i', 'VI'], 'VI': ['III', 'iv', 'VII', 'V'], 'III': ['VI', 'VII', 'iv'],
               'VII': ['i', 'III', 'VI'], 'V': ['i', 'VI'], 'v': ['VI', 'iv']}
QUALITY = {'maj': [0, 4, 7], 'min': [0, 3, 7]}
MALLETS = {'marimba': [1, 3.99, 10.65], 'vibes': [1, 3.93, 9.2], 'kalimba': [1, 5.4, 12.0]}


def euclid(hits, steps=16, rotate=0):
    """Hits spread as evenly as possible over the steps (Bjorklund), rotated."""
    hits = max(0, min(steps, hits))
    pattern = [1 if (i * hits) % steps < hits else 0 for i in range(steps)]
    return pattern[-rotate % steps:] + pattern[:-rotate % steps] if rotate else pattern


class Composer:
    def __init__(self, profile, seed, key, palette, forced=None):
        self.forced = dict(forced or {})
        self.moods = profile.get('moods') or {}
        self.pace = profile.get('pace', 'medium')
        self.r = rng(seed)
        self.key = key
        self.minor = key.lower().endswith('minor')
        self.palette = palette if palette in FAMILIES else 'studio'

    def u(self, low, high):
        return round(float(self.r.uniform(low, high)), 4)

    def choice(self, items):
        return items[int(self.r.integers(len(items)))]

    def progression(self, length=4):
        functions, moves = (MINOR_FUNCTIONS, MINOR_MOVES) if self.minor else (MAJOR_FUNCTIONS, MAJOR_MOVES)
        tonic = 'i' if self.minor else 'I'
        enders = ['V', 'VII', 'iv'] if self.minor else ['V', 'IV', 'ii']
        starts = [tonic, 'VI'] if self.minor else [tonic, 'vi', 'IV']
        if not self.minor and self.moods.get('bold', 0) > 0.6:
            moves = dict(moves, I=moves['I'] + ['bVII'])
        for _ in range(200):
            chords = [self.choice(starts)]
            while len(chords) < length:
                chords.append(self.choice(moves[chords[-1]]))
            if chords[-1] in enders and len(set(chords)) >= 3 and all(a != b for a, b in zip(chords, chords[1:])):
                break
        else:
            chords = [tonic, 'VI', 'III', 'VII'] if self.minor else ['I', 'V', 'vi', 'IV']
        colour = self.choice(['triad', 'seventh', 'add9', 'sus2']) if self.moods.get('editorial', 0) + self.moods.get('calm', 0) + self.moods.get('technical', 0) > 1.0 \
            else self.choice(['triad', 'triad', 'seventh', 'add9'])
        return [{'name': c, 'root': functions[c][0], 'quality': functions[c][1]} for c in chords], colour

    def timbre(self, part):
        family = self.forced.get(part) or self.choice(FAMILIES[self.palette][part])
        if family is None:
            return None
        if family.startswith('additive'):
            bright = {'additive': (2600, 3800), 'additive-soft': (1800, 2600), 'additive-bright': (4200, 6200)}[family]
            return {'family': 'additive', 'warmth': self.u(*bright), 'motion': self.u(0.15, 0.5), 'level': self.u(0.08, 0.11)}
        if family == 'fm':
            return {'family': 'fm', 'ratio': float(self.choice([1.0, 1.0, 2.0, 3.0, 0.5])), 'index': self.u(0.8, 2.6), 'index_decay': self.u(0.2, 0.6),
                    'decay': self.u(0.8, 2.0), 'tine': self.u(0.0, 0.12), 'level': self.u(0.05, 0.08)}
        if family in ('string', 'pluck'):
            return {'family': 'string', 'brightness': self.u(0.35, 0.75), 'damping': self.u(0.993, 0.998), 'level': self.u(0.1, 0.15)}
        if family == 'piano':
            return {'family': 'piano', 'felt': bool(self.r.uniform() < 0.7), 'level': self.u(0.13, 0.18)}
        if family == 'mallet':
            name = self.choice(list(MALLETS))
            return {'family': 'mallet', 'ratios': [round(x * (1 + self.u(-0.02, 0.02)), 3) if i else 1 for i, x in enumerate(MALLETS[name])],
                    'decay': self.u(0.4, 1.1), 'kind': name, 'level': self.u(0.08, 0.12)}
        if family == 'saw':
            return {'family': 'saw', 'cutoff': [self.u(1600, 4200), self.u(250, 700)], 'tau': self.u(0.04, 0.14), 'square': self.u(0.0, 0.5), 'level': self.u(0.04, 0.06)}
        return {'family': 'round', 'bright': self.u(0.6, 1.1), 'level': self.u(0.3, 0.4)}

    def rhythms(self):
        fast = self.pace == 'fast'
        bass_hits = int(self.r.integers(3, 6 if not fast else 8))
        lead_mode = self.choice(['arp', 'arp', 'comp', 'motif'])
        return {
            'bass': euclid(bass_hits, 16, int(self.r.integers(0, 3))),
            'lead': euclid(int(self.r.integers(4, 9 if fast else 7)), 16, int(self.r.integers(0, 4))),
            'lead_mode': lead_mode,
            'arp_order': self.choice(['up', 'down', 'updown', 'walk']),
            'arp_rate': 16 if fast or self.moods.get('technical', 0) > 0.7 else 8,
            'hats': [round(self.u(0.25, 0.5) if i % 2 else self.u(0.6, 1.0), 2) for i in range(16)],
            'kick': [1, 0, 0, 0] * 4 if FAMILIES[self.palette]['kit'] in ('house', 'electronic') else
                    [1 if i == 0 else v for i, v in enumerate(euclid(int(self.r.integers(2, 5)), 16, int(self.r.integers(0, 3))))],
            'backbeat': [0] * 8 + [1] + [0] * 7 if (self.pace == 'slow' and self.r.uniform() < 0.5) else [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            'swing': self.u(0.0, 0.14) if FAMILIES[self.palette]['kit'] not in ('house', 'electronic') else self.u(0.0, 0.05),
        }

    def motif(self):
        steps = [0, 2, 4, 5, 7, 9, 11] if not self.minor else [0, 2, 3, 5, 7, 8, 10]
        degrees, current = [], int(self.choice([0, 2, 4]))
        for _ in range(int(self.r.integers(4, 7))):
            degrees.append(current)
            current = max(-2, min(9, current + int(self.choice([-2, -1, 1, 1, 2, 3]))))
        positions = [i for i, v in enumerate(euclid(len(degrees), 16, int(self.r.integers(0, 4)))) if v]
        return {'degrees': degrees, 'positions': positions, 'scale': steps}

    def kit(self):
        kit = FAMILIES[self.palette]['kit']
        deep = kit in ('electronic', 'house')
        kick = {'role': 'kick', 'align': 'onset', 'length': 0.45, 'drive': self.u(1.3, 1.7), 'norm': {'type': 'peak', 'value': 1.0}, 'layers': [
            {'type': 'tone', 'wave': 'sine', 'freq': [self.u(95, 150), self.u(44, 56)], 'glide': self.u(0.02, 0.04), 'env': {'a': 0.0005, 'd': self.u(0.12, 0.26) if deep else self.u(0.08, 0.16)}, 'gain': 1.0},
            {'type': 'noise', 'color': 0.0, 'path': [[0, self.u(2500, 4500)]], 'width': 0.7, 'env': {'a': 0.0001, 'd': 0.0025}, 'gain': self.u(0.1, 0.45)}]}
        # The backbeat is designed on a continuum: a body tone, a noise band, and one to four bursts (a clap).
        bursts = int(self.r.integers(1, 5)) if kit in ('house', 'band', 'electronic') else int(self.r.integers(1, 3))
        band_centre = self.u(1100, 3800)
        layers = [{'type': 'tone', 'wave': 'sine', 'freq': [self.u(200, 330), self.u(160, 220)], 'glide': 0.012, 'env': {'a': 0.0005, 'd': self.u(0.03, 0.07)}, 'gain': self.u(0.0, 0.6)}]
        for b in range(bursts):
            layers.append({'type': 'noise', 'color': self.u(-0.2, 0.0), 'path': [[0, band_centre * self.u(0.9, 1.1)]], 'width': self.u(0.8, 1.4), 'delay': 0.008 * b,
                           'env': {'a': 0.0005, 'd': self.u(0.006, 0.012) if b < bursts - 1 else self.u(0.04, 0.14)}, 'gain': 0.8, 'pan': self.u(-0.3, 0.3)})
        backbeat = {'role': 'backbeat', 'align': 'onset', 'length': 0.35, 'drive': 1.2, 'width': self.u(0.1, 0.35), 'norm': {'type': 'peak', 'value': 1.0}, 'layers': layers}
        f = self.u(180, 260)
        hat = {'role': 'hat', 'align': 'onset', 'length': 0.08, 'norm': {'type': 'peak', 'value': 1.0}, 'layers': [
            {'type': 'tone', 'wave': {'partials': [[1, 1], [1.48, 1], [1.8, 1], [2.54, 1], [2.63, 1], [3.9, 1]]}, 'freq': f * 20, 'highpass': 6500, 'env': {'a': 0.0002, 'd': self.u(0.012, 0.03)}, 'gain': self.u(0.2, 0.5)},
            {'type': 'noise', 'color': 0.0, 'path': [[0, self.u(8000, 11000)]], 'width': 0.9, 'env': {'a': 0.0002, 'd': self.u(0.012, 0.03)}, 'gain': 1.0}]}
        return {'kit': kit, 'kick': kick, 'backbeat': backbeat, 'hat': hat, 'shaker': kit in ('soft', 'organic', 'sparse')}


LEAD_FAMILIES = ['string', 'fm', 'piano', 'mallet', 'saw']


def generate_music(profile, seed, key, palette, forced=None):
    """A new music recipe for one video; `forced` ({'lead': family}) fixes the lead's instrument family."""
    c = Composer(profile, seed, key, palette, forced)
    chords, colour = c.progression()
    return {'palette': c.palette, 'key': key, 'progression': chords, 'colour': colour,
            'parts': {'pad': c.timbre('pad'), 'bass': c.timbre('bass'), 'lead': c.timbre('lead')},
            'rhythm': c.rhythms(), 'motif': c.motif(), 'drums': c.kit(),
            'ending': c.choice(['strike', 'arpeggio', 'motif'])}


# ---------------------------------------------------------------- rendering

def chord_tones(chord, colour, root_note, centre):
    base = root_note + chord['root']
    tones = [base + i for i in QUALITY[chord['quality']]]
    if colour == 'seventh':
        tones.append(base + (10 if chord['quality'] == 'min' or chord['root'] in (7, 10) else 11))
    elif colour == 'add9':
        tones.append(base + 14)
    elif colour == 'sus2':
        tones[1] = base + 2
    return sorted(centre - 7 + (t - (centre - 7)) % 12 for t in tones)


def play_note(timbre, n, freq, seed, velocity=0.8, release_at=None):
    family = timbre['family']
    release_at = n / RATE if release_at is None else release_at
    if family == 'additive':
        env = adsr(n, 0.3, 1.2, 0.75, max(0.0, release_at - 0.05), 0.5)[:, None]
        return pad_voice(n, freq, seed, timbre['warmth'], timbre['motion']) * env
    if family == 'fm':
        t = seconds(n)
        index = (timbre['index'] * velocity) * np.exp(-t / timbre['index_decay']) + 0.2
        x = np.sin(2 * np.pi * freq * t + index * np.sin(2 * np.pi * freq * timbre['ratio'] * t))
        x = x * np.exp(-t / timbre['decay']) + timbre['tine'] * np.sin(2 * np.pi * freq * 14 * t) * np.exp(-t / 0.03)
        return fades(x * adsr(n, 0.002, 10, 1, release_at, 0.06) * velocity, 0.002, 0.04)
    if family == 'string':
        return music.guitar(n, freq, seed, timbre['brightness'], timbre['damping']) * velocity
    if family == 'piano':
        return music.piano(n, freq, seed, timbre['felt'], velocity)
    if family == 'mallet':
        t = seconds(n)
        x = sum(np.sin(2 * np.pi * freq * ratio * t) * np.exp(-t / (timbre['decay'] / (1 + 2.5 * i))) * (1 / (1 + i)) for i, ratio in enumerate(timbre['ratios']) if freq * ratio < RATE / 2.2)
        hit = shaped(synth.colored_noise(n, seed, -0.3), lambda tt, f: synth.lowpass(f, 3000)) * np.exp(-t / 0.002) * 0.3
        return fades((x + hit) * velocity, 0.0005, 0.03)
    if family == 'saw':
        saw = music.saw_note(n, freq, timbre['cutoff'][0], timbre['cutoff'][1], timbre['tau'], 0.003, 0.2, 0.5, release_at, 0.05)
        if timbre.get('square'):
            saw = saw + timbre['square'] * music.saw_note(n, freq * 2, timbre['cutoff'][0], timbre['cutoff'][1], timbre['tau'], 0.003, 0.2, 0.5, release_at, 0.05) * 0.5
        return saturate(saw * velocity, 1.3)
    return music.round_bass(n, freq, release_at, timbre.get('bright', 1.0)) * velocity


def arp_sequence(tones, order, count, r):
    up = tones + [tones[0] + 12]
    if order == 'down':
        seq = up[::-1]
    elif order == 'updown':
        seq = up + up[-2:0:-1]
    elif order == 'walk':
        seq, i = [], 0
        for _ in range(count):
            seq.append(up[i])
            i = max(0, min(len(up) - 1, i + int(r.choice([-1, 1, 1]))))
        return seq
    else:
        seq = up
    return [seq[i % len(seq)] for i in range(count)]


def render_music(spec, total_s, bpm, energies, seed=11, reveal_bar=None, end_bar=None):
    """Play a music recipe over the video's bars; same structure rules as music.compose_bed. With `end_bar` the music
    plays on through the reveal (marked by a cymbal) and resolves at `end_bar` instead."""
    n_total = int(total_s * RATE) + RATE
    bed = music.Bed(n_total)
    beat = 60.0 / bpm
    bar, sixteenth = 4 * beat, beat / 4
    root, minor = synth.key_root(spec['key'])
    centre = root + 18
    prog, colour, rhythm, parts, drums = spec['progression'], spec['colour'], spec['rhythm'], spec['parts'], spec['drums']
    r = rng(seed)
    swing = rhythm.get('swing', 0.0)
    kicks = [recipes.render(drums['kick'], seed + i)[0] for i in range(3)]
    backbeats = [recipes.render(drums['backbeat'], seed + 10 + i)[0] for i in range(3)]
    hats = [recipes.render(drums['hat'], seed + 20 + i)[0] for i in range(4)]
    kit = drums['kit']

    def at(start, step):
        return start + int((step + (swing if step % 2 else 0)) * sixteenth * RATE)

    for b, energy in enumerate(energies):
        start = int(round(b * bar * RATE))
        if start >= n_total:
            break
        resolve_at = end_bar if end_bar is not None else reveal_bar
        if resolve_at is not None and b >= resolve_at:
            if b == resolve_at:
                render_ending(bed, spec, start, root, centre, beat, seed, energies[b - 1] if b else 1)
            continue
        if end_bar is not None and b == reveal_bar and kit not in ('soft', 'sparse', 'organic') and energies[b - 1] >= 2:
            bed.place(start, synth.crash(seed + 5), 0.28)
        chord = prog[(b - reveal_bar) % len(prog) if reveal_bar is not None else b % len(prog)]
        if end_bar is not None and b == end_bar - 1 and b > reveal_bar:
            chord = prog[-1]  # the chord that leads home, into the resolution
        tones = chord_tones(chord, colour, root, centre)
        into_reveal = reveal_bar is not None and b == reveal_bar - 1
        length = min(n_total - start, int((bar + 0.8) * RATE))
        if parts.get('pad'):
            for i, note in enumerate(tones + [tones[0] + 12]):
                v = play_note(parts['pad'], length, midi_hz(note), seed + 31 * b + i, release_at=bar - (0.25 if into_reveal else 0.0))
                bed.place(start, v, parts['pad']['level'] * (1.0 if energy else 0.75), bus='pads')
        if parts.get('bass') and energy >= 1:
            pattern = rhythm['bass'] if energy >= 2 else [1 if i in (0, 8) else 0 for i in range(16)]
            hits = [i for i, v in enumerate(pattern) if v]
            for k, step in enumerate(hits):
                nxt = hits[k + 1] if k + 1 < len(hits) else 16
                m = int((nxt - step) * sixteenth * RATE * 0.9)
                note = root - 12 + chord['root']
                bed.place(at(start, step), play_note(parts['bass'], m, midi_hz(note), seed + 7 * b + k, release_at=0.85 * m / RATE), parts['bass']['level'])
        if parts.get('lead') and energy >= (1 if parts['lead']['family'] in ('string', 'piano') else 2):
            lead = parts['lead']
            if rhythm['lead_mode'] == 'motif':
                mot = spec['motif']
                for k, (deg, step) in enumerate(zip(mot['degrees'], mot['positions'])):
                    note = root + 24 + mot['scale'][deg % 7] + 12 * (deg // 7)
                    bed.place(at(start, step), play_note(lead, int(1.2 * RATE), midi_hz(note), seed + 13 * b + k, 0.75), lead['level'], -0.2 + 0.1 * k)
            elif rhythm['lead_mode'] == 'comp':
                for k, step in enumerate(i for i, v in enumerate(rhythm['lead']) if v):
                    m = int(2.5 * sixteenth * RATE)
                    for i, note in enumerate(tones):
                        bed.place(at(start, step), play_note(lead, m, midi_hz(note + 12), seed + 17 * b + 5 * k + i, 0.6, 0.8 * m / RATE), lead['level'] * 0.7, -0.4 + 0.27 * i)
            else:
                rate = rhythm['arp_rate']
                count = 16 if rate == 16 else 8
                seq = arp_sequence([t + 12 for t in tones[:3]], rhythm['arp_order'], count, r)
                for k in range(count):
                    step = k if rate == 16 else 2 * k
                    m = int((0.3 if rate == 16 else 0.6) * RATE)
                    bed.place(at(start, step), play_note(lead, m, midi_hz(seq[k]), seed + 19 * b + k, 0.8 if k % 4 == 0 else 0.6, 0.7 * m / RATE), lead['level'], 0.35 * math.sin(k * 0.9))
        if energy >= 2:
            if drums['shaker']:
                for s in range(0, 16, 1 if energy >= 3 else 2):
                    bed.place(at(start, s), music.shaker(seed + 3 * s + b), 0.045 * rhythm['hats'][s], 0.35)
            else:
                for s in range(0, 16, 1 if energy >= 3 else 2):
                    if not (into_reveal and s >= 12):
                        bed.place(at(start, s), hats[s % 4], 0.07 * rhythm['hats'][s], 0.25 if s % 2 else 0.1)
        if energy >= 3 or (kit == 'house' and energy >= 2):
            for s, v in enumerate(rhythm['kick']):
                if v and not (kit == 'sparse' and s):
                    bed.place(at(start, s), kicks[s % 3], 0.4 if kit not in ('soft', 'sparse', 'organic') else 0.3)
                    bed.duck(at(start, s), 1.0 if kit in ('electronic', 'house') else 0.7)
            for s, v in enumerate(rhythm['backbeat']):
                if v:
                    bed.place(at(start, s), backbeats[(s + b) % 3], 0.24 if kit not in ('soft', 'sparse', 'organic') else 0.16)
        if into_reveal and energy >= 3:
            for i in range(4):
                bed.place(start + int((3 + i / 4) * beat * RATE), backbeats[i % 3], 0.08 + 0.04 * i)
        if into_reveal and energy >= 2:
            swell = synth.crash(seed + 3, beat * 1.5)[::-1]
            bed.place(int(round((b + 1) * bar * RATE)) - len(swell), fades(swell * np.linspace(0, 1, len(swell))[:, None] ** 2, 0.2, 0.004),
                      0.2 if kit not in ('soft', 'sparse', 'organic') else 0.1)
    out = bed.pads * (1 - 0.45 * bed.kick_env)[:, None] + bed.rhythm
    out = out[:int(total_s * RATE)]
    for ch in range(2):
        out[:, ch] = shaped(out[:, ch], lambda t, f: highpass(f, 35, 2), 4096, 1024)
    out = music.level_match(out)
    tail = min(int(0.5 * RATE), len(out) // 4) if reveal_bar is not None else min(int(1.2 * RATE), len(out) // 4)
    return fades(out, 0.012, tail / RATE)


def render_ending(bed, spec, start, root, centre, beat, seed, before):
    """The reveal: the tonic struck in the video's own instruments and left to ring, closed the way the recipe asks."""
    remaining = bed.n - start
    ring = max(1.0, remaining / RATE / 2.5)
    tonic = {'root': 0, 'quality': 'min' if spec['key'].lower().endswith('minor') else 'maj'}
    tones = chord_tones(tonic, spec['colour'], root, centre)
    pad = spec['parts'].get('pad') or {'family': 'additive', 'warmth': 2200, 'motion': 0.2, 'level': 0.07}
    env = adsr(remaining, 0.03, 0.8, 0.6, 0.0, ring)[:, None]
    for i, note in enumerate(tones + [tones[0] + 12]):
        bed.place(start, pad_voice(remaining, midi_hz(note), seed + 7001 + i, pad.get('warmth', 2600), pad.get('motion', 0.2)) * env, pad['level'] * 1.1, bus='pads')
    if spec['parts'].get('bass'):
        bed.place(start, synth.bass_note(remaining, midi_hz(root - 12), 0.004, 0.6, 0.35, 0.0, ring), 0.4)
    if spec['drums']['kit'] not in ('soft', 'sparse', 'organic') and before >= 2:
        bed.place(start, synth.crash(seed + 5), 0.28)
    lead = spec['parts'].get('lead')
    if not lead:
        return
    m = min(remaining, int(2.5 * RATE))
    if spec['ending'] == 'motif':
        mot = spec['motif']
        tail = mot['degrees'][-3:] + [7]
        notes = [root + 24 + mot['scale'][d % 7] + 12 * (d // 7) for d in tail]
    else:
        notes = [t + 12 for t in tones] + [tones[0] + 24]
    for i, note in enumerate(notes):
        offset = 0 if spec['ending'] == 'strike' else int(i * beat / 2 * RATE)
        bed.place(start + offset, play_note(lead, m, midi_hz(note), seed + 920 + i, 0.75 - 0.06 * i), lead['level'], -0.3 + 0.2 * i)
