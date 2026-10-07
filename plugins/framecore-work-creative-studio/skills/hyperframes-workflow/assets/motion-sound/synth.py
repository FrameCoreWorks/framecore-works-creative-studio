"""Studio sound synthesis: layered sound effects and a composed music bed, rendered offline with numpy.

Each design builds a sound the way a sound designer layers one: band-limited noise shaped by moving filters for
air, pitched sub layers for weight, modal resonances for clicks, knocks and bells, saturation for density and a
shared convolution reverb for space. Durations come from the motion (a whoosh lasts as long as the move it
accompanies), pitched sounds follow the music's key, and every random source is seeded, so the same contract
always gives the same audio. Stereo float arrays at RATE, shape (samples, 2).
"""
import math

import numpy as np

RATE = 48000
NOTE_NAMES = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}


# ---------------------------------------------------------------- building blocks

def rng(seed):
    return np.random.default_rng(int(seed) & 0xFFFFFFFF)


def seconds(n):
    return np.arange(n) / RATE


def colored_noise(n, seed, slope=-0.5):
    """Noise whose power falls by `slope` per octave power-law (-0.5 pink, -1 brown, 0 white), unit RMS."""
    spectrum = np.fft.rfft(rng(seed).standard_normal(n))
    f = np.fft.rfftfreq(n, 1 / RATE)
    f[0] = f[1] if n > 1 else 1
    spectrum *= f ** slope
    out = np.fft.irfft(spectrum, n)
    return out / (np.sqrt(np.mean(out ** 2)) + 1e-12)


def shaped(x, response, size=2048, hop=512):
    """Time-varying filter by overlap-add STFT: response(time_s, freqs) -> magnitude per bin for that frame."""
    window = np.hanning(size)
    pad = np.concatenate([np.zeros(size), x, np.zeros(size)])
    out, norm = np.zeros_like(pad), np.zeros_like(pad)
    freqs = np.fft.rfftfreq(size, 1 / RATE)
    for start in range(0, len(pad) - size, hop):
        frame = pad[start:start + size] * window
        t = (start + size / 2 - size) / RATE
        spec = np.fft.rfft(frame) * response(t, freqs)
        out[start:start + size] += np.fft.irfft(spec, size) * window
        norm[start:start + size] += window ** 2
    out = out / np.maximum(norm, 1e-8)
    return out[size:size + len(x)]


def band(freqs, centre, octaves):
    """Gaussian band on a log-frequency axis."""
    with np.errstate(divide='ignore'):
        distance = np.log2(np.maximum(freqs, 1.0) / max(centre, 1.0))
    return np.exp(-0.5 * (distance / octaves) ** 2)


def lowpass(freqs, cutoff, order=2):
    return 1 / np.sqrt(1 + (freqs / cutoff) ** (2 * order))


def highpass(freqs, cutoff, order=2):
    f = np.maximum(freqs, 1e-3)
    return 1 / np.sqrt(1 + (cutoff / f) ** (2 * order))


def modes(n, partials, seed, detune=0.0):
    """Sum of exponentially decaying sinusoids [(freq, decay_s, gain)], each with a seeded phase."""
    t, r = seconds(n), rng(seed)
    out = np.zeros(n)
    for freq, decay, gain in partials:
        f = freq * (1 + detune * r.uniform(-1, 1))
        out += gain * np.exp(-t / decay) * np.sin(2 * np.pi * f * t + r.uniform(0, 2 * np.pi))
    return out


def saturate(x, drive):
    return np.tanh(drive * x) / np.tanh(drive)


def fades(x, fade_in=0.002, fade_out=0.02):
    n, a, b = len(x), int(fade_in * RATE), int(fade_out * RATE)
    env = np.ones(n)
    if a:
        env[:a] = np.linspace(0, 1, a) ** 2
    if b:
        env[-b:] *= np.linspace(1, 0, b) ** 2
    return x * (env[:, None] if x.ndim == 2 else env)


def stereo(mono, pan=0.0, width=0.0, seed=0):
    """Equal-power pan of a mono signal; `width` adds a decorrelated side for space."""
    theta = (np.clip(pan, -1, 1) + 1) * np.pi / 4
    left, right = mono * np.cos(theta) * math.sqrt(2), mono * np.sin(theta) * math.sqrt(2)
    if width:
        side = shaped(mono, lambda t, f: np.exp(1j * rng(seed).uniform(0, 2 * np.pi, len(f))), 1024, 256)
        left, right = left + width * side, right - width * side
    return np.stack([left, right], axis=1)


def moving_pan(mono, start, end, curve=None):
    """Pan that travels from `start` to `end` over the sound (equal power, per sample)."""
    k = np.linspace(0, 1, len(mono)) if curve is None else curve
    theta = (np.clip(start + (end - start) * k, -1, 1) + 1) * np.pi / 4
    return np.stack([mono * np.cos(theta), mono * np.sin(theta)], axis=1) * math.sqrt(2)


def midi_hz(note):
    return 440.0 * 2 ** ((note - 69) / 12)


def key_root(key):
    """MIDI note of the key's root in octave 3 and whether it is minor, from text such as 'A minor' or 'Eb major'."""
    name, _, mode = (key or 'C major').partition(' ')
    return 48 + NOTE_NAMES.get(name.strip(), 0), mode.strip().lower().startswith('min')


# ---------------------------------------------------------------- sound effects

def whoosh(duration=0.6, peak=0.6, intensity=0.8, direction=1.0, brightness=1.0, seed=1):
    """Air moving past: pink and brown noise through a band that rises to its brightest at the peak and falls,
    an airy top layer, a slight tonal resonance, and a pan that travels with the move. Peak at `peak` of the duration."""
    tail = 0.25
    n = int((duration + tail) * RATE)
    t = seconds(n)
    tp = max(0.02, duration * peak)
    rise = np.clip(t / tp, 0, 1)
    fall = np.exp(-np.maximum(t - tp, 0) / max(0.05, 0.22 * duration))
    envelope = np.where(t < tp, rise ** 2.4, fall) * (t < duration + tail)
    lo, hi = 260.0, 2600.0 * brightness * (0.7 + 0.5 * intensity)
    def centre(time):
        k = min(1.0, time / tp) if time < tp else math.exp(-(time - tp) / max(0.05, 0.3 * duration))
        return lo * (hi / lo) ** k
    body = shaped(colored_noise(n, seed, -0.45) + 0.6 * colored_noise(n, seed + 1, -0.9),
                  lambda time, f: band(f, centre(time), 1.1) * highpass(f, 60))
    air = shaped(colored_noise(n, seed + 2, 0.0), lambda time, f: highpass(f, 4500, 2) * lowpass(f, 14000))
    tone = shaped(colored_noise(n, seed + 3, -0.3), lambda time, f: band(f, centre(time) * 0.5, 0.18))
    mono = envelope * (body + 0.1 * air * envelope + 0.3 * tone)
    curve = np.clip(t / (duration + 1e-6), 0, 1)
    curve = 0.5 - 0.5 * np.cos(np.pi * curve)
    out = moving_pan(mono, -0.7 * direction, 0.7 * direction, curve)
    out = fades(out * intensity / (np.max(np.abs(out)) + 1e-9), 0.005, 0.08)
    # Align on the loudest 10 ms actually rendered, not the designed envelope, so the peak lands on its frame.
    window = RATE // 100
    energy = np.convolve(np.mean(out, axis=1) ** 2, np.ones(window) / window, mode='same')
    return out, int(np.argmax(energy)) / RATE


def impact(weight=0.6, brightness=0.6, seed=2):
    """A hit: a sub tone that drops in pitch, a filtered noise body, a short bright transient, saturated together.
    Weight lowers and lengthens it. Onset at 0."""
    length = 0.35 + 1.1 * weight
    n = int(length * RATE)
    t = seconds(n)
    f_end, f_start = 52 - 10 * weight, 150 + 60 * weight
    freq = f_end + (f_start - f_end) * np.exp(-t / 0.035)
    sub = np.sin(2 * np.pi * np.cumsum(freq) / RATE) * np.exp(-t / (0.18 + 0.45 * weight))
    body = shaped(colored_noise(n, seed, -0.6), lambda time, f: lowpass(f, 700 + 1400 * brightness, 2) * highpass(f, 70)) * np.exp(-t / (0.05 + 0.06 * weight))
    snap = shaped(colored_noise(n, seed + 1, 0.0), lambda time, f: highpass(f, 2500, 2)) * np.exp(-t / 0.004)
    mono = saturate(0.95 * sub + 0.55 * body + 0.35 * brightness * snap, 1.6)
    return fades(stereo(mono, 0.0, 0.12 * weight, seed), 0.0005, 0.05), 0.0


def riser(duration=1.2, intensity=0.7, seed=3):
    """Tension before a reveal: noise through a band climbing from low to bright, a quiet tone sweeping up an octave,
    rising in level to its end, where the reveal lands. Aligned at its end."""
    n = int(duration * RATE)
    t = seconds(n)
    k = t / duration
    noise = shaped(colored_noise(n, seed, -0.3), lambda time, f: band(f, 220 * (30 ** min(1, time / duration)), 0.8))
    glide = 220 * 2 ** k
    tone = sum(np.sin(2 * np.pi * np.cumsum(glide * ratio) / RATE + i) * gain for i, (ratio, gain) in enumerate([(1, 0.5), (1.5, 0.25), (2, 0.2)]))
    envelope = k ** 2.2
    mono = envelope * (noise + 0.25 * tone)
    out = stereo(mono, 0.0, 0.35, seed)
    return fades(out * intensity / (np.max(np.abs(out)) + 1e-9), 0.01, 0.004), duration


def click(pitch=1.0, softness=0.0, seed=4):
    """A mechanical click: a 1 ms bright excitation ringing a few stiff high modes and a short low 'thock'. Onset at 0."""
    n = int(0.09 * RATE)
    excite = shaped(colored_noise(n, seed, 0.0), lambda time, f: highpass(f, 1800)) * np.exp(-seconds(n) / 0.0012)
    ring = modes(n, [(2300 * pitch, 0.012, 0.6), (3700 * pitch, 0.008, 0.45), (5600 * pitch, 0.005, 0.3), (190 * pitch, 0.014, 0.5 * (1 - softness))], seed, 0.03)
    mono = saturate(0.9 * excite + ring, 1.3) * (1 - 0.5 * softness)
    return fades(stereo(mono), 0.0002, 0.01), 0.0


def tick(pitch=1.0, seed=5):
    """A small, dry tick for counters and steps."""
    n = int(0.05 * RATE)
    excite = shaped(colored_noise(n, seed, 0.0), lambda time, f: highpass(f, 3000)) * np.exp(-seconds(n) / 0.0008)
    ring = modes(n, [(4200 * pitch, 0.006, 0.5), (6900 * pitch, 0.004, 0.3)], seed, 0.02)
    return fades(stereo(excite + ring), 0.0002, 0.008), 0.0


def knock(pitch=1.0, seed=6):
    """A soft wooden landing for text and cards: low inharmonic wood modes with a muted noise excitation."""
    n = int(0.25 * RATE)
    excite = shaped(colored_noise(n, seed, -0.4), lambda time, f: lowpass(f, 2500) * highpass(f, 120)) * np.exp(-seconds(n) / 0.003)
    ring = modes(n, [(210 * pitch, 0.07, 0.8), (470 * pitch, 0.04, 0.45), (830 * pitch, 0.022, 0.3), (1450 * pitch, 0.012, 0.2)], seed, 0.02)
    return fades(stereo(saturate(0.6 * excite + ring, 1.2), 0.0, 0.05, seed), 0.0003, 0.03), 0.0


def shimmer(note=76, seed=7, length=1.6):
    """A bright, tuned accent: inharmonic bell partials with long decays, slightly detuned left and right."""
    n = int(length * RATE)
    f0 = midi_hz(note)
    partials = [(1.0, 1.2, 0.7), (2.0, 0.8, 0.35), (2.76, 0.6, 0.25), (4.07, 0.35, 0.15), (5.43, 0.22, 0.1)]
    left = modes(n, [(f0 * r * 1.0007, d * length / 1.6, g) for r, d, g in partials], seed)
    right = modes(n, [(f0 * r * 0.9993, d * length / 1.6, g) for r, d, g in partials], seed + 1)
    excite = shaped(colored_noise(n, seed + 2, 0.0), lambda time, f: highpass(f, 5000)) * np.exp(-seconds(n) / 0.002) * 0.3
    return fades(np.stack([left + excite, right + excite], axis=1), 0.0005, 0.2), 0.0


def boom(seed=8):
    """The biggest hit, for a final reveal: a heavy impact with a long sub tail."""
    hit, _ = impact(1.0, 0.45, seed)
    n = int(2.2 * RATE)
    t = seconds(n)
    tail = np.sin(2 * np.pi * 41 * t) * np.exp(-t / 0.9) * 0.45
    out = np.zeros((n, 2))
    out[:len(hit)] += hit
    out += np.stack([tail, tail], axis=1)
    return fades(out, 0.0, 0.2), 0.0


DESIGNS = {
    'whoosh': ('air past the frame: scene changes, sweeps, wipes, pushes, camera moves', 'peak'),
    'impact': ('a hit with weight: a card, logo or device landing', 'onset'),
    'boom': ('the biggest hit, once per video: the final reveal', 'onset'),
    'riser': ('tension climbing into a reveal; ends on the reveal frame', 'end'),
    'click': ('a tap or button press', 'onset'),
    'release': ('the release of a press', 'onset'),
    'tick': ('counter steps and fast repeated steps', 'onset'),
    'knock': ('a soft landing of a line, caption or item', 'onset'),
    'shimmer': ('a bright tuned accent on a final value, highlight or end card', 'onset'),
}


def render_design(name, params, seed, key='C major'):
    """Render a design; returns (stereo, alignment offset in seconds)."""
    p = dict(params or {})
    root, minor = key_root(key)
    if name == 'whoosh':
        return whoosh(p.get('duration', 0.6), p.get('peak', 0.6), p.get('intensity', 0.8), p.get('direction', 1.0), p.get('brightness', 1.0), seed)
    if name == 'impact':
        return impact(p.get('weight', 0.6), p.get('brightness', 0.6), seed)
    if name == 'boom':
        return boom(seed)
    if name == 'riser':
        return riser(p.get('duration', 1.2), p.get('intensity', 0.7), seed)
    if name == 'click':
        return click(p.get('pitch', 1.0), p.get('softness', 0.0), seed)
    if name == 'release':
        return click(p.get('pitch', 1.25), 0.7, seed)
    if name == 'tick':
        return tick(p.get('pitch', 1.0), seed)
    if name == 'knock':
        return knock(p.get('pitch', 1.0), seed)
    if name == 'shimmer':
        degree = p.get('degree', 0)
        scale = [0, 2, 3, 5, 7, 8, 10] if minor else [0, 2, 4, 5, 7, 9, 11]
        note = root + 24 + scale[degree % 7] + 12 * (degree // 7)
        return shimmer(note, seed, p.get('length', 1.6))
    raise ValueError(f'Unknown sound design: {name}')


# ---------------------------------------------------------------- reverb and mastering

def reverb_ir(length=1.6, seed=9, damping=3500.0, predelay=0.012):
    """A stereo room: decorrelated noise with an exponential decay that darkens over time."""
    n = int(length * RATE)
    t = seconds(n)
    channels = []
    for c in range(2):
        noise = colored_noise(n, seed + c, -0.2) * np.exp(-t * 6.9 / length)
        channels.append(shaped(noise, lambda time, f: lowpass(f, max(600.0, damping * math.exp(-time * 1.5)), 1) * highpass(f, 150), 1024, 256))
    ir = np.stack(channels, axis=1)
    ir = np.concatenate([np.zeros((int(predelay * RATE), 2)), ir])
    return ir / (np.sqrt(np.sum(ir ** 2, axis=0, keepdims=True)) + 1e-12)


def convolve(x, ir):
    n = len(x) + len(ir) - 1
    size = 1 << (n - 1).bit_length()
    out = np.zeros((n, 2))
    for c in range(2):
        out[:, c] = np.fft.irfft(np.fft.rfft(x[:, c], size) * np.fft.rfft(ir[:, c], size), size)[:n]
    return out


def limit(x, ceiling_db=-1.0, release=0.08, lookahead=0.003):
    """Look-ahead peak limiter without latency (offline): the gain dips before each peak and recovers smoothly."""
    ceiling = 10 ** (ceiling_db / 20)
    peak = np.max(np.abs(x), axis=1)
    need = np.minimum(1.0, ceiling / np.maximum(peak, 1e-12))
    ahead = int(lookahead * RATE)
    if ahead > 1:
        padded = np.concatenate([need, np.ones(ahead)])
        windows = np.lib.stride_tricks.sliding_window_view(padded, ahead + 1)
        need = windows.min(axis=1)[:len(need)]
    gain = np.empty_like(need)
    coeff = math.exp(-1 / (release * RATE))
    level = 1.0
    for i, target in enumerate(need):
        level = target if target < level else target + (level - target) * coeff
        gain[i] = level
    return x * gain[:, None]


def true_peak_db(x):
    """Peak after 4x oversampling (FFT), close to the BS.1770 true peak."""
    n = len(x)
    if n == 0:
        return -120.0
    size = 1 << (n - 1).bit_length()
    peaks = []
    for c in range(x.shape[1]):
        spec = np.fft.rfft(x[:, c], size)
        up = np.fft.irfft(np.concatenate([spec, np.zeros(3 * size // 2)]), 4 * size) * 4
        peaks.append(np.max(np.abs(up[:4 * n])))
    return 20 * math.log10(max(peaks) + 1e-12)


# ---------------------------------------------------------------- music

def pad_voice(n, freq, seed, warmth=2600.0):
    """A warm pad note: additive saw-like partials, gently lowpassed, two detuned voices spread left and right."""
    t = seconds(n)
    left, right = np.zeros(n), np.zeros(n)
    r = rng(seed)
    h = 1
    while freq * h < 7000 and h <= 24:
        gain = (1 / h ** 1.1) * math.exp(-freq * h / warmth)
        phase = r.uniform(0, 2 * np.pi)
        left += gain * np.sin(2 * np.pi * freq * h * 1.0035 * t + phase)
        right += gain * np.sin(2 * np.pi * freq * h * 0.9965 * t + phase + 0.7)
        h += 1
    return np.stack([left, right], axis=1)


def adsr(n, attack, decay, sustain, release_at, release):
    t = seconds(n)
    env = np.where(t < attack, t / max(attack, 1e-4), sustain + (1 - sustain) * np.exp(-(t - attack) / max(decay, 1e-4)))
    env = np.where(t > release_at, env * np.exp(-(t - release_at) / max(release, 1e-4)), env)
    return env


def compose_bed(total_s, bpm, key, energies, seed=11):
    """A music bed: bars of a four-chord progression in `key`; `energies` gives each bar a level from 0 to 3.
    0: a soft pad; 1: pad and bass; 2: plus a plucked arpeggio and hats; 3: plus kick and clap, with the pad and
    bass ducking under the kick. Returns stereo audio of total_s seconds starting on bar 1."""
    n_total = int(total_s * RATE) + RATE
    out = np.zeros((n_total, 2))
    beat = 60.0 / bpm
    bar = 4 * beat
    root, minor = key_root(key)
    progression = [(0, [0, 3, 7]), (8, [-4, 0, 3]), (3, [0, 4, 7]), (10, [-3, 0, 4])] if minor else [(0, [0, 4, 7]), (7, [0, 4, 7]), (9, [0, 3, 7]), (5, [0, 4, 7])]
    kick_env = np.zeros(n_total)
    pads, rhythm = np.zeros((n_total, 2)), np.zeros((n_total, 2))
    for b, energy in enumerate(energies):
        start = int(b * bar * RATE)
        if start >= n_total:
            break
        degree, chord = progression[b % 4]
        base = root + degree
        # Pad: the chord, voiced around middle C, held for the bar with an overlapping release.
        length = min(n_total - start, int((bar + 0.8) * RATE))
        env = adsr(length, 0.35, 1.2, 0.75, bar - 0.05, 0.6)[:, None]
        for i, interval in enumerate(chord + [12]):
            voice = pad_voice(length, midi_hz(base + 12 + interval), seed + 31 * b + i)
            pads[start:start + length] += voice * env * (0.11 if energy else 0.08)
        if energy >= 1:
            hits = [0, 2] if energy == 1 else [0, 1.5, 2, 3.5] if energy == 2 else [0, 0.5, 1.5, 2, 2.5, 3.5]
            for h in hits:
                s = start + int(h * beat * RATE)
                m = min(n_total - s, int(0.6 * beat * RATE))
                if m <= 0:
                    continue
                t = seconds(m)
                f = midi_hz(base - 12)
                tone = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t) + 0.12 * np.sin(6 * np.pi * f * t)
                e = adsr(m, 0.006, 0.18, 0.55, 0.5 * beat, 0.08)
                bass = saturate(tone * e * 0.5, 1.4)
                rhythm[s:s + m] += np.stack([bass, bass], axis=1) * 0.55
        if energy >= 2:
            notes = [base + 12 + c for c in chord] + [base + 24 + chord[0]]
            for step in range(8):
                s = start + int(step * beat / 2 * RATE)
                m = min(n_total - s, int(0.9 * RATE))
                if m <= 0:
                    continue
                t = seconds(m)
                f = midi_hz(notes[[0, 1, 2, 3, 2, 1, 2, 3][step]] + 12)
                pluck = sum(math.exp(-0.45 * (h - 1)) * np.sin(2 * np.pi * f * h * t) * np.exp(-t / (0.35 / h)) for h in range(1, 7))
                velocity = 0.10 if step % 2 == 0 else 0.07
                rhythm[s:s + m] += stereo(pluck * velocity, -0.35 if step % 2 == 0 else 0.35)
                hat_len = min(n_total - s, int(0.05 * RATE))
                if step % 2 == 1 and hat_len > 0:
                    hat = shaped(colored_noise(hat_len, seed + 977 * b + step, 0.0), lambda time, fr: highpass(fr, 7000, 2)) * np.exp(-seconds(hat_len) / 0.012)
                    rhythm[s:s + hat_len] += stereo(hat * 0.06, 0.25)
        if energy >= 3:
            for h in range(4):
                s = start + int(h * beat * RATE)
                kick, _ = impact(0.35, 0.25, seed + 13 * b + h)
                m = min(n_total - s, len(kick))
                rhythm[s:s + m] += kick[:m] * 0.5
                kick_env[s:s + min(m, int(0.25 * RATE))] = np.maximum(kick_env[s:s + min(m, int(0.25 * RATE))], np.exp(-seconds(min(m, int(0.25 * RATE))) / 0.08))
                if h in (1, 3):
                    clap_len = min(n_total - s, int(0.25 * RATE))
                    if clap_len > 0:
                        bursts = np.zeros(clap_len)
                        for k_, offset in enumerate((0, 0.009, 0.019)):
                            o = int(offset * RATE)
                            bursts[o:] += np.exp(-seconds(clap_len - o) / (0.006 if k_ < 2 else 0.06))
                        clap = shaped(colored_noise(clap_len, seed + 5 * b + h, 0.0), lambda time, fr: band(fr, 1400, 1.0)) * bursts
                        rhythm[s:s + clap_len] += stereo(clap * 0.18, 0.0, 0.3, seed)
    duck = 1 - 0.45 * kick_env
    out += pads * duck[:, None] + rhythm
    return out[:int(total_s * RATE)]
