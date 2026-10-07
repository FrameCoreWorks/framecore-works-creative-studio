"""Studio music composition: instruments, palettes per motion style and the arranger for a composed music bed.

Every style in ../motion-styles/styles.json describes a music texture (Meadow: nylon guitar, Rhodes, felt piano and
soft drums; Midnight: synths and a tight kick; Color block: punchy pop or house, and so on). A palette turns that
texture into instruments, voicings, patterns and a drum kit; the arranger plays a chord progression in it with the
energy each bar asks for, builds into the final reveal, lands the reveal on the tonic and lets it ring out. The
progression and the small variations come from a seed, so two videos do not share one bed, and the same contract
always gives the same audio. Stereo float arrays at synth.RATE, shape (samples, 2).
"""
import math

import numpy as np

import synth
from synth import RATE, adsr, band, colored_noise, fades, highpass, key_root, lowpass, midi_hz, modes, pad_voice, rng, saturate, seconds, shaped, stereo

# Chord loops as (chord root in semitones above the key, chord intervals above that root). Each loop ends on a
# chord that leads home, so the bar before the reveal resolves into the tonic. Voicing (inversions) is chosen when
# the chord is played, so the upper voices move as little as possible.
MAJOR, MINOR = [0, 4, 7], [0, 3, 7]
PROGRESSIONS = {
    'major': [
        [(0, MAJOR), (7, MAJOR), (9, MINOR), (5, MAJOR)],   # I V vi IV
        [(0, MAJOR), (9, MINOR), (5, MAJOR), (7, MAJOR)],   # I vi IV V
        [(9, MINOR), (5, MAJOR), (0, MAJOR), (7, MAJOR)],   # vi IV I V
        [(0, MAJOR), (5, MAJOR), (9, MINOR), (7, MAJOR)],   # I IV vi V
    ],
    'minor': [
        [(0, MINOR), (8, MAJOR), (3, MAJOR), (10, MAJOR)],  # i VI III VII
        [(0, MINOR), (5, MINOR), (8, MAJOR), (7, MAJOR)],   # i iv VI V
        [(0, MINOR), (8, MAJOR), (5, MINOR), (7, MAJOR)],   # i VI iv V
        [(0, MINOR), (10, MAJOR), (8, MAJOR), (10, MAJOR)],  # i VII VI VII
    ],
}

# What each style sounds like. pad: sustained layer; bass: bass voice and rhythm; lead: the moving part; kit: drums;
# sevenths: colour chords with sevenths; swing: delay of off-beat sixteenths as a fraction of a sixteenth.
PALETTES = {
    'studio': {'pad': 'warm', 'bass': 'round', 'lead': 'pluck', 'kit': 'studio', 'sevenths': False, 'swing': 0.08,
               'texture': 'warm pad, rounded bass, plucked arpeggio, kick, snare and swung hats'},
    'meadow': {'pad': 'soft', 'bass': 'round', 'lead': 'guitar', 'keys': 'rhodes', 'kit': 'soft', 'sevenths': True, 'swing': 0.1,
               'texture': 'nylon guitar picking, Rhodes chords, soft pad, brushes and a felt kick'},
    'warm-ink': {'pad': 'none', 'bass': 'electric', 'lead': 'rhodes-comp', 'kit': 'tight', 'sevenths': True, 'swing': 0.06,
                 'texture': 'muted electric piano comping, soft electric bass, tight dry kick, rim and hats'},
    'midnight': {'pad': 'synth', 'bass': 'synth', 'lead': 'synth-arp', 'kit': 'electronic', 'sevenths': False, 'swing': 0.0,
                 'texture': 'wide synth pad, filtered saw bass, sixteenth synth arpeggio, tight kick and clap'},
    'field-guide': {'pad': 'soft', 'bass': 'round', 'lead': 'guitar-strum', 'kit': 'organic', 'sevenths': False, 'swing': 0.12,
                    'texture': 'strummed acoustic guitar, soft pad, shaker, rim and a light kick in a room'},
    'paper-and-ink': {'pad': 'soft', 'bass': 'none', 'lead': 'piano', 'kit': 'sparse', 'sevenths': True, 'swing': 0.0,
                      'texture': 'sparse felt piano with space for the words, a quiet pad, almost no drums'},
    'color-block': {'pad': 'none', 'bass': 'synth', 'lead': 'stab', 'kit': 'house', 'sevenths': True, 'swing': 0.04,
                    'texture': 'house chord stabs, bouncing saw bass, four-on-the-floor kick, clap and open hats'},
}
STYLE_PALETTE = {'meadow': 'meadow', 'warm-ink': 'warm-ink', 'midnight': 'midnight', 'field-guide': 'field-guide',
                 'paper-and-ink': 'paper-and-ink', 'color-block': 'color-block'}


# ---------------------------------------------------------------- instruments (mono unless noted)

def guitar(n, freq, seed, brightness=0.5, damping=0.996):
    """A plucked nylon string (Karplus-Strong): a short noise burst circulating in a delay line one period long,
    softened each pass, so the tone decays and darkens like a real string."""
    period = max(2, int(round(RATE / freq - 0.5)))
    # The loop sounds at RATE / (period + 0.5); render a little long and resample so the note is exactly in tune.
    ratio = freq * (period + 0.5) / RATE
    length = int(n * ratio) + 2
    burst = colored_noise(period, seed, -0.2 - 0.8 * (1 - brightness))
    burst -= burst.mean()
    y = np.zeros(length + period + 1)
    y[1:period + 1] = burst
    for start in range(period + 1, len(y), period):
        end = min(start + period, len(y))
        y[start:end] = damping * 0.5 * (y[start - period:end - period] + y[start - period - 1:end - period - 1])
    out = np.interp(np.arange(n) * ratio, np.arange(length), y[1:length + 1])
    body = shaped(out, lambda t, f: 1 + 0.6 * band(f, 110, 0.5) + 0.3 * band(f, 220, 0.6), 1024, 256)
    return fades(body / (np.max(np.abs(body)) + 1e-9), 0.001, 0.05)


def rhodes(n, freq, seed, velocity=0.8):
    """An electric piano: FM with a decaying index for the bell-like attack, a quiet high tine, a soft tremolo."""
    t = seconds(n)
    r = rng(seed)
    index = (0.8 + 1.6 * velocity) * np.exp(-t / 0.35) + 0.25
    body = np.sin(2 * np.pi * freq * t + index * np.sin(2 * np.pi * freq * t + r.uniform(0, 6.28)))
    body *= np.exp(-t / (1.6 * (220 / freq) ** 0.35))
    tine = np.sin(2 * np.pi * freq * 14.0 * t) * np.exp(-t / 0.03) * 0.08 * velocity
    out = (body + tine) * (1 + 0.12 * np.sin(2 * np.pi * 4.2 * t + r.uniform(0, 6.28)))
    return fades(saturate(out * velocity, 1.2), 0.002, 0.06)


def piano(n, freq, seed, felt=True, velocity=0.8):
    """A piano note: stretched partials (string stiffness) from two slightly detuned strings that beat, brighter
    partials fading first, and a felt hammer thump."""
    t = seconds(n)
    r = rng(seed)
    out = np.zeros(n)
    stiffness = 0.0004
    k = 1
    while k <= 14:
        f = k * freq * math.sqrt(1 + stiffness * k * k)
        if f > 9000:
            break
        gain = k ** -1.3 * math.exp(-k * freq / (1700 if felt else 3800)) * (0.6 + 0.4 * velocity)
        decay = 2.6 * (220 / freq) ** 0.5 / (1 + 0.4 * (k - 1))
        for detune in (0.9995, 1.0005):
            out += gain * np.sin(2 * np.pi * f * detune * t + r.uniform(0, 6.28)) * np.exp(-t / decay)
        k += 1
    thump = shaped(colored_noise(n, seed, -0.8), lambda time, fr: lowpass(fr, 900)) * np.exp(-t / 0.01) * 0.25
    return fades((out / 2 + thump) * velocity, 0.002, 0.08)


def saw_note(n, freq, cutoff_start, cutoff_end, tau, attack=0.004, decay=0.25, sustain=0.6, release_at=None, release=0.06):
    """A band-limited saw through a resonant-free low-pass whose cutoff falls from cutoff_start to cutoff_end."""
    t = seconds(n)
    cutoff = cutoff_end + (cutoff_start - cutoff_end) * np.exp(-t / tau)
    out = np.zeros(n)
    h = 1
    while freq * h < 12000 and h <= 64:
        out += np.sin(2 * np.pi * freq * h * t) / h / np.sqrt(1 + (freq * h / cutoff) ** 4)
        h += 1
    env = adsr(n, attack, decay, sustain, release_at if release_at is not None else n / RATE, release)
    return out * env


def round_bass(n, freq, release_at, bright=1.0):
    t = seconds(n)
    tone = sum(g * np.sin(2 * np.pi * freq * h * t) for h, g in ((1, 1.0), (2, 0.5 * bright), (3, 0.28 * bright), (4, 0.12 * bright)))
    return saturate(tone * adsr(n, 0.006, 0.18, 0.55, release_at, 0.08) * 0.45, 1.6)


def shaker(seed, length=0.09):
    n = int(length * RATE)
    t = seconds(n)
    env = np.minimum(t / 0.012, 1) * np.exp(-np.maximum(t - 0.012, 0) / 0.03)
    return shaped(colored_noise(n, seed, 0.0), lambda time, f: band(f, 7000, 0.7)) * env


def rim(seed):
    n = int(0.12 * RATE)
    t = seconds(n)
    click = shaped(colored_noise(n, seed, 0.0), lambda time, f: band(f, 2500, 0.8)) * np.exp(-t / 0.002)
    return modes(n, [(1720, 0.018, 0.6), (820, 0.025, 0.35), (3100, 0.008, 0.2)], seed) + 0.5 * click


def brush(seed):
    n = int(0.3 * RATE)
    t = seconds(n)
    env = np.minimum(t / 0.006, 1) * np.exp(-t / 0.11)
    return shaped(colored_noise(n, seed, -0.2), lambda time, f: band(f, 3200, 1.4)) * env


def kick(seed, kind='studio'):
    """Kicks per kit: studio, soft (felt), tight (short and dry), electronic (long sub), house (punchy)."""
    low, high, glide, decay, beater = {'studio': (48, 120, 0.03, 0.16, 0.35), 'soft': (52, 95, 0.025, 0.12, 0.1),
                                       'tight': (55, 130, 0.02, 0.09, 0.3), 'electronic': (45, 140, 0.035, 0.24, 0.3),
                                       'house': (50, 150, 0.028, 0.18, 0.45)}[kind]
    n = int(0.45 * RATE)
    t = seconds(n)
    freq = low + (high - low) * np.exp(-t / glide)
    body = np.sin(2 * np.pi * np.cumsum(freq) / RATE) * np.exp(-t / decay)
    click = shaped(colored_noise(n, seed, 0.0), lambda time, f: band(f, 3500, 0.7)) * np.exp(-t / 0.0025)
    return fades(saturate(body + beater * click, 1.5), 0.0003, 0.05)


def clap(seed):
    n = int(0.3 * RATE)
    bursts = np.zeros(n)
    for k, offset in enumerate((0, 0.009, 0.019)):
        o = int(offset * RATE)
        bursts[o:] += np.exp(-seconds(n - o) / (0.006 if k < 2 else 0.07))
    return shaped(colored_noise(n, seed, 0.0), lambda time, f: band(f, 1400, 1.0)) * bursts


# ---------------------------------------------------------------- arranger

class Bed:
    """Stereo buses for one composed bed: sustained parts (ducked by the kick) and rhythmic parts."""

    def __init__(self, n):
        self.n = n
        self.pads = np.zeros((n, 2))
        self.rhythm = np.zeros((n, 2))
        self.kick_env = np.zeros(n)

    def place(self, at, audio, gain=1.0, pan=0.0, bus='rhythm', width=0.0, seed=0):
        if at >= self.n or at + len(audio) <= 0 or gain == 0:
            return
        a = max(0, at)
        m = min(self.n - a, len(audio) - (a - at))
        if m <= 0:
            return
        piece = audio[a - at:a - at + m]
        piece = piece if piece.ndim == 2 else stereo(piece, pan, width, seed)
        (self.pads if bus == 'pads' else self.rhythm)[a:a + m] += piece * gain

    def duck(self, at, depth=1.0):
        m = min(self.n - at, int(0.25 * RATE))
        if m > 0:
            self.kick_env[at:at + m] = np.maximum(self.kick_env[at:at + m], depth * np.exp(-seconds(m) / 0.08))


def voicing(base, chord, sevenths, degree, minor_key, centre):
    """Chord tones of the chord on `base`, each moved by octaves into the window just around `centre`, so successive
    chords share tones and move by steps. With `sevenths` a seventh adds colour: a minor seventh on minor chords
    and on the dominant (V, or VII in a minor key), a major seventh otherwise."""
    tones = [base + c for c in chord]
    if sevenths:
        dominant = degree == 7 or (minor_key and degree == 10)
        tones.append(base + (10 if 3 in chord or dominant else 11))
    return sorted(centre - 7 + (t - (centre - 7)) % 12 for t in tones)


def play_pad(bed, palette, start, length, notes, energy, seed, release, strike=False):
    kind = palette['pad']
    if kind == 'none' and not strike:
        return
    warmth, motion, level = {'warm': (3200, 0.3, 0.11), 'soft': (2200, 0.25, 0.075), 'synth': (5200, 0.45, 0.085), 'none': (2600, 0.2, 0.06)}[kind]
    level *= 1.0 if energy else 0.75
    attack = 0.03 if strike else (0.6 if kind == 'soft' else 0.35)
    env = adsr(length, attack, 1.2, 0.75, (length / RATE) - release - 0.05 if not strike else 0.0, release)[:, None]
    for i, note in enumerate(notes):
        bed.place(start, pad_voice(length, midi_hz(note), seed + i, warmth, motion) * env, level, bus='pads')


def play_bass(bed, palette, start, beat, root_note, energy, seed, bar_index):
    kind = palette['bass']
    if kind == 'none' or energy < 1:
        return
    f = midi_hz(root_note)
    if kind == 'round':
        hits = [(0, 0.6)] + ([(2, 0.6)] if energy == 1 else [(1.5, 0.45), (2, 0.6), (3.5, 0.45)])
        for h, dur in hits:
            m = int(dur * beat * RATE)
            bed.place(start + int(h * beat * RATE), round_bass(m, f, 0.85 * dur * beat), 0.36)
    elif kind == 'electric':
        hits = [(0, 0.9), (1.5, 0.4), (2, 0.9), (3.5, 0.4)] if energy >= 2 else [(0, 1.8), (2, 1.8)]
        for h, dur in hits:
            m = int(dur * beat * RATE)
            bed.place(start + int(h * beat * RATE), round_bass(m, f, 0.85 * dur * beat, 0.7), 0.3)
    else:  # synth: filtered saw; eighths at energy 2, off-beat pumping at 3
        steps = [0, 2] if energy == 1 else range(8)
        for s in steps:
            if energy >= 3 and s % 2 == 0 and palette['kit'] == 'house':
                continue  # house bass sits on the off-beats, the kick on the beats
            m = int((0.45 if energy >= 2 else 1.8) * beat * RATE)
            note = saw_note(m, f, 1400 if energy >= 2 else 900, 220, 0.08, release_at=0.85 * m / RATE)
            bed.place(start + int(s * beat / 2 * RATE), saturate(note * 0.6, 1.3), 0.24)


def play_lead(bed, palette, start, beat, notes, energy, seed, bar_index, swing):
    kind = palette['lead']
    upper = [n_ + 12 for n_ in notes]
    if kind == 'pluck' and energy >= 2:
        arp = sorted(upper[:3]) + [upper[0] + 12]
        for step in range(8):
            m = int(0.9 * RATE)
            t = seconds(m)
            f = midi_hz(arp[[0, 1, 2, 3, 2, 1, 2, 3][step]] + 12)
            pl = sum(math.exp(-0.45 * (h - 1)) * np.sin(2 * np.pi * f * h * t) * np.exp(-t / (0.35 / h)) for h in range(1, 7))
            bed.place(start + int(step * beat / 2 * RATE), pl, 0.10 if step % 2 == 0 else 0.07, -0.35 if step % 2 == 0 else 0.35)
    elif kind == 'guitar' and energy >= 1:
        # Travis-style picking: bass note on the beats, chord tones between.
        pattern = [0, 2, 1, 3, 0, 2, 1, 3] if energy >= 2 else [0, None, 2, None, 0, None, 1, None]
        tones = [notes[0] - 12, notes[1], notes[2], notes[0] + 12]
        for step, which in enumerate(pattern):
            if which is None:
                continue
            at = start + int((step + (swing if step % 2 else 0)) * beat / 2 * RATE)
            m = int(1.6 * RATE)
            bed.place(at, guitar(m, midi_hz(tones[which]), seed + 17 * bar_index + step), 0.16 if step % 2 == 0 else 0.12, -0.25 + 0.15 * which)
    elif kind == 'guitar-strum' and energy >= 1:
        strokes = [(0, 1), (1, -1), (1.5, -1), (2.5, -1), (3, 1), (3.5, -1)] if energy >= 2 else [(0, 1), (2, 1)]
        strings = [notes[0] - 12, notes[0], notes[1], notes[2], notes[0] + 12]
        for k, (pos, direction) in enumerate(strokes):
            order = strings if direction > 0 else strings[::-1][:3]
            at = start + int(pos * beat * RATE)
            for i, note in enumerate(order):
                m = int(1.4 * RATE)
                bed.place(at + int(i * 0.012 * RATE), guitar(m, midi_hz(note), seed + 31 * bar_index + 7 * k + i, 0.65 if direction > 0 else 0.8),
                          (0.07 if direction > 0 else 0.05), -0.3 + 0.15 * i)
    elif kind == 'rhodes-comp' and energy >= 1:
        hits = [0, 1.5, 2.5, 3.5] if energy >= 2 else [0, 2]
        for k, pos in enumerate(hits):
            m = int((0.7 if energy >= 2 else 1.6) * beat * RATE)
            for i, note in enumerate(upper):
                env = adsr(m, 0.003, 0.3, 0.6, 0.8 * m / RATE, 0.05)
                bed.place(start + int(pos * beat * RATE), rhodes(m, midi_hz(note - 12), seed + 13 * k + i, 0.6) * env, 0.055, -0.45 + 0.3 * i, width=0.3, seed=seed + i)
    elif kind == 'piano':
        # Sparse: the chord's lowest tone on one, two upper tones answering later, leaving space for words.
        if energy >= 1:
            phrases = [(0, [notes[0]]), (1.5, [upper[1]]), (2.5, [upper[2]])] if energy >= 2 else [(0, [notes[0]]), (2, [upper[1]])]
            for k, (pos, chord_notes) in enumerate(phrases):
                for i, note in enumerate(chord_notes):
                    m = int(2.2 * RATE)
                    bed.place(start + int(pos * beat * RATE), piano(m, midi_hz(note), seed + 11 * bar_index + k + i, True, 0.7), 0.17, -0.1 + 0.2 * k)
    elif kind == 'synth-arp' and energy >= 2:
        arp = sorted(upper[:3]) + [upper[0] + 12]
        order = [0, 1, 2, 3, 2, 1, 2, 3, 0, 1, 2, 3, 2, 3, 1, 2]
        for step in range(16):
            m = int(0.22 * RATE)
            note = saw_note(m, midi_hz(arp[order[step]]), 3800, 700, 0.05, 0.002, 0.08, 0.3, 0.15, 0.04)
            bed.place(start + int(step * beat / 4 * RATE), note, 0.045 if step % 4 else 0.06, 0.3 * math.sin(step * 0.8))
    elif kind == 'stab' and energy >= 1:
        hits = [0.5, 1.5, 2.5, 3.5] if energy >= 2 else [0, 2]
        for k, pos in enumerate(hits):
            m = int(0.24 * RATE)
            for i, note in enumerate(upper):
                bed.place(start + int(pos * beat * RATE), saw_note(m, midi_hz(note), 3400, 600, 0.05, 0.002, 0.1, 0.25, 0.16, 0.05), 0.035, -0.5 + 0.33 * i, width=0.35, seed=seed + i)
    if palette.get('keys') == 'rhodes' and energy >= 1:
        m = int(4 * beat * RATE)
        for i, note in enumerate(upper):
            bed.place(start, rhodes(m, midi_hz(note - 12), seed + 101 * bar_index + i, 0.45), 0.04, -0.2 + 0.13 * i, bus='pads')


def play_drums(bed, palette, start, beat, energy, seed, bar_index, swing, into_reveal, hats):
    kit = palette['kit']
    sixteenth = beat / 4

    def at(step):  # sixteenth step with swing on the off-beat sixteenths
        return start + int((step + (swing if step % 2 else 0)) * sixteenth * RATE)

    def k(step, gain=0.42):
        bed.place(at(step), kick(seed + 13 * bar_index + step, 'studio' if kit == 'studio' else kit if kit in ('soft', 'tight', 'electronic', 'house') else 'soft'), gain)
        bed.duck(at(step), 1.0 if kit in ('electronic', 'house') else 0.7)

    if kit == 'studio':
        if energy == 2:
            for s in range(0, 16, 2):
                bed.place(at(s), hats[(s // 2) % 4], 0.07 if s % 4 else 0.035, 0.25)
        if energy >= 3:
            for b in range(4):
                k(4 * b)
                if b in (1, 3):
                    bed.place(at(4 * b), synth.snare(seed + 5 * bar_index + b), 0.3, 0.0, width=0.3, seed=seed)
            for s in range(16):
                if s == 14:
                    bed.place(at(s), hats[4], 0.06, 0.3)
                elif s < 12 or not into_reveal:
                    bed.place(at(s), hats[s % 4], (0.075, 0.03, 0.055, 0.03)[s % 4], 0.25 if s % 2 else 0.15)
    elif kit in ('soft', 'organic', 'sparse'):
        if energy >= 2 or (kit == 'organic' and energy >= 1):
            for s in range(0, 16, 1 if kit == 'organic' and energy >= 2 else 2):
                bed.place(at(s), shaker(seed + 3 * s + bar_index), (0.06 if s % 4 == 2 else 0.035) * (0.7 if kit == 'sparse' else 1.0), 0.35)
        if energy >= 3:
            for b in range(4):
                if kit != 'sparse' or b == 0:
                    if b in (0, 2) or kit == 'soft':
                        k(4 * b, 0.34 if kit == 'soft' else 0.3)
                if b in (1, 3):
                    if kit == 'soft':
                        bed.place(at(4 * b), brush(seed + 7 * b + bar_index), 0.22, 0.05)
                    else:
                        bed.place(at(4 * b), rim(seed + 7 * b + bar_index), 0.16, -0.1)
    elif kit == 'tight':
        if energy >= 2:
            for s in range(0, 16, 2):
                bed.place(at(s), hats[(s // 2) % 4], 0.05 if s % 4 else 0.03, 0.2)
        if energy >= 3:
            for s in (0, 6, 8, 11):
                k(s, 0.36)
            for b in (1, 3):
                bed.place(at(4 * b), rim(seed + b + bar_index), 0.22, -0.05)
    elif kit in ('electronic', 'house'):
        if energy >= 2:
            for s in range(16):
                if kit == 'house' and s % 4 == 2:
                    bed.place(at(s), hats[4], 0.055, 0.3)
                else:
                    bed.place(at(s), hats[s % 4], (0.06, 0.025, 0.045, 0.025)[s % 4], 0.2 if s % 2 else -0.1)
        if energy >= 3 or (kit == 'house' and energy >= 2):
            for b in range(4):
                k(4 * b, 0.45)
                if b in (1, 3):
                    bed.place(at(4 * b), clap(seed + b + bar_index), 0.2, 0.0, width=0.35, seed=seed)
    if into_reveal and energy >= 3:
        if kit in ('studio', 'electronic', 'house', 'tight'):
            for i in range(4):
                bed.place(start + int((3 + i / 4) * beat * RATE), synth.snare(seed + 701 + i), 0.12 + 0.05 * i, 0.0, width=0.3, seed=seed)
        else:
            for i in range(8):
                bed.place(start + int((2 + i / 4) * beat * RATE), shaker(seed + 801 + i), 0.03 + 0.012 * i, 0.3)


def resolve(bed, palette, start, root, prog, before, beat, seed):
    """The reveal bar: the tonic struck on the palette's own instruments and left to ring out to the end."""
    remaining = bed.n - start
    ring = max(1.0, remaining / RATE / 2.5)
    degree, chord = prog[0]
    base = root + degree
    notes = voicing(base, chord, palette['sevenths'], degree, False, root + 18) + [base + 24]
    play_pad(bed, dict(palette, pad=palette['pad'] if palette['pad'] != 'none' else 'soft'), start, remaining, notes, 1, seed + 7001, ring, strike=True)
    if palette['bass'] != 'none':
        bed.place(start, synth.bass_note(remaining, midi_hz(base - 12), 0.004, 0.6, 0.35, 0.0, ring), 0.4)
    lead, cymbals = palette['lead'], palette['kit'] in ('studio', 'electronic', 'house', 'tight')
    if cymbals and before >= 2:
        bed.place(start, synth.crash(seed + 5), 0.32 if palette['kit'] != 'tight' else 0.2)
    m = min(remaining, int(2.5 * RATE))
    top = [base + 24 + c for c in chord] + [base + 36]
    if lead in ('guitar', 'guitar-strum'):
        for i, note in enumerate([base - 12 + 12, base + 12 + chord[1], base + 12 + chord[2], base + 24]):
            bed.place(start + int(i * 0.018 * RATE), guitar(m, midi_hz(note), seed + 900 + i, 0.7), 0.13, -0.3 + 0.2 * i)
    elif lead in ('rhodes-comp',) or palette.get('keys') == 'rhodes':
        for i, note in enumerate(notes):
            bed.place(start, rhodes(m, midi_hz(note), seed + 910 + i, 0.8), 0.06, -0.2 + 0.13 * i)
    elif lead == 'piano':
        for i, note in enumerate([base, base + 12 + chord[1], base + 12 + chord[2], base + 24]):
            bed.place(start + int(i * 0.5 * beat * RATE), piano(m, midi_hz(note), seed + 920 + i, True, 0.75 - 0.08 * i), 0.18, -0.15 + 0.1 * i)
    elif lead in ('synth-arp', 'stab'):
        for i, note in enumerate(top):
            bed.place(start + int(i * 0.25 * beat * RATE), saw_note(int(0.5 * RATE), midi_hz(note), 4200, 900, 0.12, 0.003, 0.2, 0.3, 0.35, 0.1), 0.05, -0.3 + 0.2 * i)
    if lead == 'pluck' and before >= 2:
        for i, note in enumerate(top):
            t = seconds(int(1.6 * RATE))
            f = midi_hz(note)
            pl = sum(math.exp(-0.45 * (h - 1)) * np.sin(2 * np.pi * f * h * t) * np.exp(-t / (0.35 / h)) for h in range(1, 7))
            bed.place(start + int(i * beat / 2 * RATE), pl, 0.09 - 0.012 * i, -0.3 + 0.2 * i)


def compose_bed(total_s, bpm, key, energies, seed=11, reveal_bar=None, palette='studio', progression=0):
    """A music bed in a style's palette: bars of a chord progression in `key`, each played at the energy given in
    `energies` (0 a quiet pad, 1 the core of the palette, 2 its moving parts and light percussion, 3 full drums).
    With `reveal_bar` the progression is placed so the bar before closes the loop and leads in (a fill, a swell),
    and the reveal lands on the tonic and rings out to the end. Faded in and out, never cut off."""
    style = PALETTES.get(palette, PALETTES['studio'])
    n_total = int(total_s * RATE) + RATE
    bed = Bed(n_total)
    beat = 60.0 / bpm
    bar = 4 * beat
    root, minor = key_root(key)
    loops = PROGRESSIONS['minor' if minor else 'major']
    prog = loops[progression % len(loops)]
    hats = [synth.hat(seed + 41 * i) for i in range(4)] + [synth.hat(seed + 97, True)]
    for b, energy in enumerate(energies):
        start = int(round(b * bar * RATE))
        if start >= n_total:
            break
        if reveal_bar is not None and b >= reveal_bar:
            if b == reveal_bar:
                resolve(bed, style, start, root, prog, energies[b - 1] if b else 1, beat, seed)
            continue
        degree, chord = prog[(b - reveal_bar) % 4 if reveal_bar is not None else b % 4]
        base = root + degree
        into_reveal = reveal_bar is not None and b == reveal_bar - 1
        notes = voicing(base, chord, style['sevenths'], degree, minor, root + 18)
        length = min(n_total - start, int((bar + 0.8) * RATE))
        play_pad(bed, style, start, length, notes + [notes[0] + 12], energy, seed + 31 * b, 0.25 if into_reveal else 0.6)
        play_bass(bed, style, start, beat, base - 12, energy, seed + 3 * b, b)
        play_lead(bed, style, start, beat, notes, energy, seed + 7 * b, b, style['swing'])
        play_drums(bed, style, start, beat, energy, seed, b, style['swing'], into_reveal, hats)
        if into_reveal and energy >= 2:
            swell = synth.crash(seed + 3, beat * 1.5)[::-1] if style['kit'] in ('studio', 'electronic', 'house', 'tight') else \
                np.stack([pad_voice(int(beat * 1.5 * RATE), midi_hz(root + 24 + 7), seed + 3, 4000, 0.0)[:, 0]] * 2, axis=1) * 0.25
            bed.place(int(round((b + 1) * bar * RATE)) - len(swell), fades(swell * np.linspace(0, 1, len(swell))[:, None] ** 2, 0.2, 0.004), 0.25)
    out = bed.pads * (1 - 0.45 * bed.kick_env)[:, None] + bed.rhythm
    out = out[:int(total_s * RATE)]
    for c in range(2):  # nothing useful lives below 35 Hz in a bed under effects; it only costs headroom
        out[:, c] = shaped(out[:, c], lambda t, f: highpass(f, 35, 2), 4096, 1024)
    out = level_match(out)
    tail = min(int(0.5 * RATE), len(out) // 4) if reveal_bar is not None else min(int(1.2 * RATE), len(out) // 4)
    return fades(out, 0.012, tail / RATE)


REFERENCE_LEVEL_DB = -17.0


def level_match(out):
    """Every palette sits at the same level in the mix: the loudest second's RMS is set to REFERENCE_LEVEL_DB, the
    level of the approved studio bed, so a change of style never changes the balance against the effects."""
    window = RATE
    if len(out) < window:
        return out
    power = np.convolve(np.mean(out ** 2, axis=1), np.ones(window) / window, mode='valid')
    loudest = 10 * math.log10(power.max() + 1e-12)
    return out * 10 ** ((REFERENCE_LEVEL_DB - loudest) / 20) if loudest > -90 else out
