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
    f_end, f_start = 56 - 8 * weight, 150 + 60 * weight
    freq = f_end + (f_start - f_end) * np.exp(-t / 0.035)
    sub = np.sin(2 * np.pi * np.cumsum(freq) / RATE) * np.exp(-t / (0.15 + 0.3 * weight))
    body = shaped(colored_noise(n, seed, -0.6), lambda time, f: lowpass(f, 700 + 1400 * brightness, 2) * highpass(f, 70)) * np.exp(-t / (0.05 + 0.06 * weight))
    snap = shaped(colored_noise(n, seed + 1, 0.0), lambda time, f: highpass(f, 2500, 2)) * np.exp(-t / 0.004)
    mono = saturate(0.75 * sub + 0.6 * body + 0.45 * brightness * snap, 1.6)
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
    tail = np.sin(2 * np.pi * 46 * t) * np.exp(-t / 0.7) * 0.28
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


def oversampled_peak(x, factor=4, chunk=16384, margin=512):
    """Per-sample peak of a stereo signal after FFT oversampling, so peaks between samples are seen too. Works in
    overlapping chunks, keeping only each chunk's centre, so long mixes stay fast."""
    n = len(x)
    peak = np.max(np.abs(x), axis=1)
    for a in range(0, n, chunk):
        lo, hi = max(0, a - margin), min(n, a + chunk + margin)
        size = hi - lo
        for c in range(x.shape[1]):
            spec = np.fft.rfft(x[lo:hi, c])
            up = np.fft.irfft(np.concatenate([spec, np.zeros((factor - 1) * size // 2 + 1)]), factor * size) * factor
            local = np.abs(up[:factor * size]).reshape(size, factor).max(axis=1)[a - lo:a - lo + min(chunk, n - a)]
            peak[a:a + len(local)] = np.maximum(peak[a:a + len(local)], local)
    return peak


def limit(x, ceiling_db=-1.0, release=0.08, lookahead=0.003):
    """Look-ahead true-peak limiter without latency (offline): the gain ramps down smoothly over the look-ahead
    before each peak (between samples included) and recovers smoothly, so short clicks are not squared off."""
    ceiling = 10 ** (ceiling_db / 20)
    need = np.minimum(1.0, ceiling / np.maximum(oversampled_peak(x), 1e-12))
    ahead = max(1, int(lookahead * RATE))
    # A forward minimum over the look-ahead, then a backward average over it: the ramp reaches each peak's gain in time.
    padded = np.concatenate([need, np.ones(ahead - 1)])
    floor = np.lib.stride_tricks.sliding_window_view(padded, ahead).min(axis=1)[:len(need)]
    ramp = np.convolve(np.concatenate([np.ones(ahead - 1), floor]), np.ones(ahead) / ahead, mode='valid')[:len(need)]
    gain = np.empty_like(ramp)
    coeff = math.exp(-1 / (release * RATE))
    level = 1.0
    for i, target in enumerate(ramp):
        level = target if target < level else target + (level - target) * coeff
        gain[i] = level
    return x * gain[:, None]


def compress(x, threshold_db, ratio=2.5, attack=0.012, release=0.3):
    """A gentle bus compressor: above the threshold the level rises by 1/ratio. The gain follows the 10 ms RMS
    level, computed per millisecond, with a smooth attack and a slow release, so loud hits are tamed before the
    limiter instead of being clipped by it."""
    step = RATE // 1000
    power = np.convolve(np.mean(x ** 2, axis=1), np.ones(RATE // 100) / (RATE // 100), mode='same')
    level = 10 * np.log10(power[::step] + 1e-12)
    want = -np.maximum(level - threshold_db, 0) * (1 - 1 / ratio)
    gain = np.empty_like(want)
    up, down = math.exp(-0.001 / attack), math.exp(-0.001 / release)
    g = 0.0
    for i, target in enumerate(want):
        g = target + (g - target) * (up if target < g else down)
        gain[i] = g
    curve = np.interp(np.arange(len(x)), np.arange(len(gain)) * step, gain)
    return x * (10 ** (curve / 20))[:, None]


def true_peak_db(x):
    """Peak after 4x oversampling (FFT), close to the BS.1770 true peak."""
    if len(x) == 0:
        return -120.0
    return 20 * math.log10(float(oversampled_peak(x).max()) + 1e-12)


# ---------------------------------------------------------------- music

def pad_voice(n, freq, seed, warmth=3200.0, motion=0.3):
    """A warm pad note: additive saw-like partials in three detuned voices (left, centre, right). Its brightness
    breathes with a slow, seeded filter movement, so a held chord never sounds static."""
    t = seconds(n)
    r = rng(seed)
    bright = warmth * (1 + motion * np.sin(2 * np.pi * r.uniform(0.07, 0.15) * t + r.uniform(0, 2 * np.pi)))
    left, right = np.zeros(n), np.zeros(n)
    h = 1
    while freq * h < 9000 and h <= 28:
        gain = h ** -1.1 * np.exp(-freq * h / bright)
        phase = r.uniform(0, 2 * np.pi)
        centre = 0.6 * np.sin(2 * np.pi * freq * h * t + phase)
        left += gain * (np.sin(2 * np.pi * freq * h * 1.0035 * t + phase + 0.4) + centre)
        right += gain * (np.sin(2 * np.pi * freq * h * 0.9965 * t + phase + 1.1) + centre)
        h += 1
    return np.stack([left, right], axis=1) / 1.17


def adsr(n, attack, decay, sustain, release_at, release):
    t = seconds(n)
    env = np.where(t < attack, t / max(attack, 1e-4), sustain + (1 - sustain) * np.exp(-(t - attack) / max(decay, 1e-4)))
    env = np.where(t > release_at, env * np.exp(-(t - release_at) / max(release, 1e-4)), env)
    return env


def bass_note(n, freq, attack=0.006, decay=0.18, sustain=0.55, release_at=1.0, release=0.08):
    """A rounded bass note with upper harmonics, so the line still reads on phone speakers that cannot play its root."""
    t = seconds(n)
    tone = sum(g * np.sin(2 * np.pi * freq * h * t) for h, g in ((1, 1.0), (2, 0.5), (3, 0.28), (4, 0.12)))
    return saturate(tone * adsr(n, attack, decay, sustain, release_at, release) * 0.45, 1.6)


def pluck(n, freq):
    t = seconds(n)
    return sum(math.exp(-0.45 * (h - 1)) * np.sin(2 * np.pi * freq * h * t) * np.exp(-t / (0.35 / h)) for h in range(1, 7))


def snare(seed):
    """A snare and clap layer: a tuned shell, bright wires and three quick hand bursts."""
    n = int(0.3 * RATE)
    t = seconds(n)
    shell = modes(n, [(185, 0.045, 0.6), (330, 0.03, 0.3)], seed)
    wires = shaped(colored_noise(n, seed + 1, -0.1), lambda time, f: band(f, 3800, 1.1)) * np.exp(-t / 0.075)
    bursts = np.zeros(n)
    for k, offset in enumerate((0, 0.009, 0.019)):
        o = int(offset * RATE)
        bursts[o:] += np.exp(-seconds(n - o) / (0.006 if k < 2 else 0.06))
    clap = shaped(colored_noise(n, seed + 2, 0.0), lambda time, f: band(f, 1400, 1.0)) * bursts
    return fades(0.5 * shell + 0.45 * wires + 0.5 * clap, 0.0002, 0.04)


def hat(seed, open_hat=False):
    """A metallic hi-hat: six inharmonic square oscillators and noise, high-passed; open hats ring longer."""
    n = int((0.34 if open_hat else 0.07) * RATE)
    t = seconds(n)
    r = rng(seed)
    metal = sum(np.sign(np.sin(2 * np.pi * f * t + r.uniform(0, 2 * np.pi))) for f in (205.3, 304.4, 369.6, 522.7, 540.0, 800.0)) / 6
    x = shaped(0.6 * metal + colored_noise(n, seed, 0.0), lambda time, f: highpass(f, 6500, 2) * lowpass(f, 15000))
    return fades(x * np.exp(-t / (0.12 if open_hat else 0.018)), 0.0002, 0.01)


def crash(seed, length=2.6):
    """A crash cymbal: bright noise and dense inharmonic metal modes with a long decay, wide in stereo."""
    n = int(length * RATE)
    t = seconds(n)
    r = rng(seed)
    metal = modes(n, [(r.uniform(3000, 11000), r.uniform(0.4, 1.1), r.uniform(0.2, 0.5)) for _ in range(24)], seed)
    noise = shaped(colored_noise(n, seed + 1, 0.0), lambda time, f: highpass(f, 2800, 2) * lowpass(f, 15000 - 6000 * min(1, time / length)))
    mono = (noise / 3 + metal / 6) * np.exp(-t / (0.32 * length))
    return fades(stereo(mono, 0.0, 0.6, seed), 0.001, 0.3)


def compose_bed(total_s, bpm, key, energies, seed=11, reveal_bar=None, palette='studio', progression=0):
    """A composed music bed; see music.compose_bed (instruments, style palettes and the arranger live in music.py)."""
    import music
    return music.compose_bed(total_s, bpm, key, energies, seed, reveal_bar, palette, progression)
