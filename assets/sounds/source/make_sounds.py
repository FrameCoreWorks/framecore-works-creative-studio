#!/usr/bin/env python3
"""Synthesize the FrameCore Works example sound library.

Every sound is made from oscillators and seeded noise in NumPy: no samples, no
recordings and no network. The same NumPy version gives the same WAV files.

    python3 make_sounds.py OUT_DIR

writes one 44.1 kHz stereo 16-bit WAV per sound into OUT_DIR. Encode them with
encode.sh (MP3 via ffmpeg). The output is released under CC0 1.0.
"""
from __future__ import annotations

import sys
import wave
from pathlib import Path

import numpy as np

SR = 44100
RNG = np.random.default_rng(20261031)


# ---------------------------------------------------------------- helpers
def t_axis(seconds: float) -> np.ndarray:
    return np.arange(int(seconds * SR)) / SR


def noise(seconds: float) -> np.ndarray:
    return RNG.standard_normal(int(seconds * SR))


def env_ad(n: int, attack: float, decay: float) -> np.ndarray:
    """Linear attack, exponential decay (decay = time constant in s)."""
    t = np.arange(n) / SR
    a = np.clip(t / max(attack, 1e-4), 0, 1)
    d = np.exp(-np.maximum(t - attack, 0) / decay)
    return a * d


def fade(x: np.ndarray, fin: float = 0.002, fout: float = 0.01) -> np.ndarray:
    x = x.copy()
    n_in, n_out = int(fin * SR), int(fout * SR)
    if n_in:
        x[:n_in] *= np.linspace(0, 1, n_in)
    if n_out:
        x[-n_out:] *= np.linspace(1, 0, n_out)
    return x


def fft_filter(x: np.ndarray, lo: float | None = None, hi: float | None = None, order: float = 4) -> np.ndarray:
    """Zero-phase Butterworth-shaped band filter applied in the frequency domain."""
    spec = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    gain = np.ones_like(f)
    if hi is not None:
        gain *= 1 / np.sqrt(1 + (f / hi) ** (2 * order))
    if lo is not None:
        gain *= 1 / np.sqrt(1 + (lo / np.maximum(f, 1e-6)) ** (2 * order))
    return np.fft.irfft(spec * gain, len(x))


def sweep_filter(x: np.ndarray, centers: np.ndarray, q: float = 2.0, block: int = 1024) -> np.ndarray:
    """Time-varying band-pass: overlap-add of short filtered blocks."""
    hop = block // 2
    win = np.hanning(block)
    out = np.zeros(len(x) + block)
    f = np.fft.rfftfreq(block, 1 / SR)
    for start in range(0, len(x), hop):
        seg = np.zeros(block)
        chunk = x[start:start + block]
        seg[:len(chunk)] = chunk
        c = centers[min(start + hop, len(centers) - 1)]
        bw = c / q
        gain = 1 / (1 + ((f - c) / (bw / 2)) ** 2)
        out[start:start + block] += np.fft.irfft(np.fft.rfft(seg * win) * gain, block)
    return out[:len(x)]


def reverb(x: np.ndarray, seconds: float = 2.0, mix: float = 0.25, damp: float = 4000, seed: int = 1) -> np.ndarray:
    """Convolution with decaying, low-passed stereo noise. Returns stereo (n + tail, 2)."""
    rng = np.random.default_rng(seed)
    n_ir = int(seconds * SR)
    tt = np.arange(n_ir) / SR
    decay = np.exp(-6.9 * tt / seconds)
    mono = x if x.ndim == 1 else x.mean(axis=1)
    dry = np.stack([x, x], axis=1) if x.ndim == 1 else x
    out_len = len(mono) + n_ir
    nfft = 1 << (out_len - 1).bit_length()
    wet = []
    for ch in range(2):
        ir = fft_filter(rng.standard_normal(n_ir) * decay, hi=damp, order=2)
        ir /= np.sqrt(np.sum(ir ** 2)) + 1e-12
        wet.append(np.fft.irfft(np.fft.rfft(mono, nfft) * np.fft.rfft(ir, nfft), nfft)[:out_len])
    wet = np.stack(wet, axis=1)
    out = np.zeros((out_len, 2))
    out[:len(dry)] += dry * (1 - mix)
    out += wet * mix
    return out


def stereo(x: np.ndarray, pan: float | np.ndarray = 0.0) -> np.ndarray:
    """Constant-power pan, -1 left .. +1 right."""
    p = (np.asarray(pan) + 1) * np.pi / 4
    return np.stack([x * np.cos(p), x * np.sin(p)], axis=1)


def normalize(x: np.ndarray, peak_db: float = -1.0) -> np.ndarray:
    return x / (np.max(np.abs(x)) + 1e-12) * 10 ** (peak_db / 20)


def soft_clip(x: np.ndarray, drive: float = 1.5) -> np.ndarray:
    return np.tanh(x * drive) / np.tanh(drive)


def osc(freq, seconds: float, shape: str = "sine", phase0: float = 0.0) -> np.ndarray:
    n = int(seconds * SR)
    f = np.broadcast_to(np.asarray(freq, dtype=float), (n,))
    ph = phase0 + 2 * np.pi * np.cumsum(f) / SR
    if shape == "sine":
        return np.sin(ph)
    if shape == "tri":
        return 2 / np.pi * np.arcsin(np.sin(ph))
    if shape == "saw":
        # band-limited enough for these low notes: additive with 1/k partials below Nyquist
        out = np.zeros(n)
        fmax = float(np.max(f))
        for k in range(1, int(16000 / max(fmax, 1)) + 1):
            out += np.sin(k * ph) / k
        return out * 2 / np.pi
    raise ValueError(shape)


def midi(m: float) -> float:
    return 440.0 * 2 ** ((m - 69) / 12)


def place(buf: np.ndarray, x: np.ndarray, at: float) -> None:
    i = int(round(at * SR))
    j = min(len(buf), i + len(x))
    if j > i:
        buf[i:j] += x[:j - i]


# ---------------------------------------------------------------- effects
def whoosh() -> np.ndarray:
    dur = 1.3
    n = int(dur * SR)
    tt = np.arange(n) / SR
    shape = np.sin(np.pi * np.clip(tt / dur, 0, 1)) ** 2.2
    centers = 300 + 2600 * np.sin(np.pi * np.clip(tt / dur, 0, 1)) ** 1.5
    body = sweep_filter(noise(dur), centers, q=1.6) * shape
    air = fft_filter(noise(dur), lo=4000, order=2) * shape ** 3 * 0.12
    x = body + air
    pan = np.linspace(-0.7, 0.7, n)
    return normalize(stereo(fade(x, 0.01, 0.05), pan), -1.5)


def ui_click() -> np.ndarray:
    dur = 0.12
    n = int(dur * SR)
    tick = fft_filter(noise(dur), lo=2500, hi=9000) * env_ad(n, 0.0003, 0.004)
    tone = np.sin(2 * np.pi * 3200 * t_axis(dur)) * env_ad(n, 0.0002, 0.012) * 0.5
    body = np.sin(2 * np.pi * 900 * t_axis(dur)) * env_ad(n, 0.0005, 0.008) * 0.35
    return normalize(stereo(fade(tick + tone + body, 0.0, 0.02)), -3.0)


def pop() -> np.ndarray:
    dur = 0.3
    n = int(dur * SR)
    tt = t_axis(dur)
    f = 280 + 900 * (1 - np.exp(-tt / 0.012))
    tone = osc(f, dur) * env_ad(n, 0.001, 0.045)
    click = fft_filter(noise(dur), lo=1500, hi=7000) * env_ad(n, 0.0002, 0.002) * 0.4
    x = tone + click
    return normalize(reverb(fade(x, 0.0, 0.03), 0.5, mix=0.12, seed=3)[:n + int(0.15 * SR)], -1.5)


def riser() -> np.ndarray:
    dur = 3.0
    n = int(dur * SR)
    tt = t_axis(dur)
    prog = tt / dur
    amp = prog ** 2.2
    base = 110 * 2 ** (2.5 * prog ** 1.6)
    tones = sum(osc(base * r * (1 + d), dur, "saw") for r, d in [(1, 0), (1, 0.006), (1.5, -0.004), (2, 0.003)])
    tones = sweep_filter(tones, 400 + 5000 * prog ** 2, q=0.9) * 0.6
    hiss = sweep_filter(noise(dur), 800 + 9000 * prog ** 1.5, q=1.2) * 0.8
    x = (tones + hiss) * amp
    x[-int(0.01 * SR):] *= np.linspace(1, 0, int(0.01 * SR))
    wet = reverb(x, 1.5, mix=0.2, seed=4)
    return normalize(wet[: n + int(0.6 * SR)], -2.0)


def bass_impact() -> np.ndarray:
    dur = 2.6
    n = int(dur * SR)
    tt = t_axis(dur)
    f = 42 + 90 * np.exp(-tt / 0.05)
    sub = osc(f, dur) * env_ad(n, 0.002, 0.7)
    knock = fft_filter(noise(dur), lo=60, hi=1800) * env_ad(n, 0.0005, 0.03) * 0.9
    boom = fft_filter(noise(dur), hi=220, order=3) * env_ad(n, 0.005, 0.45) * 1.2
    x = soft_clip(sub * 1.2 + knock + boom, 1.4)
    wet = reverb(fade(x, 0.0, 0.2), 2.2, mix=0.18, damp=1500, seed=5)
    return normalize(wet[: n + int(0.8 * SR)], -1.5)


def ding() -> np.ndarray:
    dur = 1.8
    n = int(dur * SR)
    tt = t_axis(dur)
    f0 = 1318.5  # E6
    partials = [(1.0, 1.0, 1.1), (2.0, 0.45, 0.6), (2.76, 0.3, 0.45), (5.4, 0.12, 0.2), (0.5, 0.15, 1.2)]
    x = sum(a * np.sin(2 * np.pi * f0 * r * tt) * env_ad(n, 0.001, d) for r, a, d in partials)
    strike = fft_filter(noise(dur), lo=3000) * env_ad(n, 0.0002, 0.003) * 0.3
    wet = reverb(fade(x + strike, 0.0, 0.1), 1.6, mix=0.2, seed=6)
    return normalize(wet[: n + int(0.4 * SR)], -1.5)


def keypress(strength: float, bright: float) -> np.ndarray:
    dur = 0.09
    n = int(dur * SR)
    click = fft_filter(noise(dur), lo=1800 * bright, hi=8000) * env_ad(n, 0.0002, 0.003)
    thock = fft_filter(noise(dur), lo=150, hi=900) * env_ad(n, 0.0008, 0.012) * 0.8
    release = np.zeros(n)
    k = int(0.045 * SR)
    release[k:] = (fft_filter(noise(dur), lo=2500, hi=7000) * env_ad(n, 0.0002, 0.002))[: n - k] * 0.35
    return (click + thock + release) * strength


def typing() -> np.ndarray:
    dur = 3.4
    buf = np.zeros(int(dur * SR))
    t = 0.12
    words = [5, 3, 6, 4, 7, 2, 5]
    for w in words:
        for _ in range(w):
            if t > dur - 0.2:
                break
            kp = keypress(RNG.uniform(0.6, 1.0), RNG.uniform(0.8, 1.3))
            place(buf, kp, t)
            t += RNG.uniform(0.06, 0.12)
        # space bar: deeper, a touch longer pause
        place(buf, keypress(1.0, 0.6) * 1.1, t)
        t += RNG.uniform(0.16, 0.26)
    room = reverb(buf, 0.35, mix=0.1, damp=3000, seed=7)[: len(buf)]
    room[-int(0.05 * SR):] *= np.linspace(1, 0, int(0.05 * SR))[:, None]
    # tame the click peaks so the keys sit at a usable loudness
    return normalize(soft_clip(normalize(room, 0.0), 2.5), -3.0)


def glitch() -> np.ndarray:
    dur = 0.7
    n = int(dur * SR)
    tt = t_axis(dur)
    src = osc(220 * 2 ** np.floor(np.sin(2 * np.pi * 7 * tt) * 3), dur, "saw") * 0.5 + noise(dur) * 0.3
    # bit-crush and sample-rate reduction
    levels = 2 ** 4
    crushed = np.round(src * levels) / levels
    hold = 6
    crushed = np.repeat(crushed[::hold], hold)[:n]
    # stutter gate: random 20-60 ms slices on/off with repeats
    out = np.zeros(n)
    pos = 0
    while pos < n:
        sl = int(RNG.uniform(0.02, 0.06) * SR)
        if RNG.random() < 0.7:
            seg = crushed[pos:pos + sl]
            reps = 1 if RNG.random() < 0.6 else 2
            for r in range(reps):
                a = pos + r * len(seg)
                b = min(n, a + len(seg))
                out[a:b] = seg[: b - a] * (1 - 0.3 * r)
        pos += sl * (2 if RNG.random() < 0.3 else 1)
    out = fft_filter(out, lo=120, hi=9000, order=2)
    pan = np.sign(np.sin(2 * np.pi * 11 * tt)) * 0.5
    return normalize(stereo(fade(out, 0.002, 0.03), pan), -1.5)


# ---------------------------------------------------------------- music
def loopable(x: np.ndarray, length: int) -> np.ndarray:
    """Fold the tail past `length` back onto the start so the file loops seamlessly."""
    out = x[:length].copy()
    tail = x[length:]
    out[: len(tail)] += tail[: length]
    return out


def calm_pad() -> np.ndarray:
    """32 s, four chords of 8 s each (Cmaj9 - Am9 - Fmaj9 - G6/9), slow pad, soft bells."""
    chord_len = 8.0
    chords = [[48, 55, 59, 62, 64], [45, 52, 55, 59, 60], [41, 48, 52, 55, 57], [43, 50, 52, 57, 59]]
    total = chord_len * len(chords)
    n_total = int(total * SR)
    buf = np.zeros(n_total + int(chord_len * SR))
    for i, ch in enumerate(chords):
        seg_dur = chord_len + 2.5
        n = int(seg_dur * SR)
        tt = t_axis(seg_dur)
        env = np.clip(tt / 2.5, 0, 1) * np.clip((seg_dur - tt) / 2.5, 0, 1)
        voice = np.zeros(n)
        for m in ch:
            f = midi(m + 12)
            for det in (-0.004, 0.0, 0.005):
                voice += osc(f * (1 + det) * (1 + 0.002 * np.sin(2 * np.pi * 0.2 * tt)), seg_dur, "tri",
                             phase0=RNG.uniform(0, 6.28)) * 0.25
        voice = fft_filter(voice, hi=1800, order=2) * env
        # a deep root under the chord
        voice += osc(midi(ch[0]), seg_dur) * env * 0.5
        place(buf, voice, i * chord_len - 1.25 if i else 0.0)
    # soft bell melody, one note every 2 s, from the pentatonic set
    notes = [76, 79, 74, 72, 76, 81, 79, 74, 72, 74, 76, 79, 81, 79, 76, 74]
    for k, m in enumerate(notes):
        dur = 3.0
        n = int(dur * SR)
        tt = t_axis(dur)
        bell = (np.sin(2 * np.pi * midi(m) * tt) + 0.2 * np.sin(2 * np.pi * midi(m) * 2.0 * tt)) * env_ad(n, 0.01, 0.9)
        place(buf, bell * 0.18, k * 2.0 + 0.5)
    wet = reverb(buf, 4.0, mix=0.35, damp=3500, seed=9)
    looped = loopable(wet, n_total)
    return normalize(looped, -3.0)


def kick(dur: float = 0.45) -> np.ndarray:
    n = int(dur * SR)
    tt = t_axis(dur)
    f = 48 + 110 * np.exp(-tt / 0.035)
    body = osc(f, dur) * env_ad(n, 0.001, 0.16)
    click = fft_filter(noise(dur), lo=1500, hi=6000) * env_ad(n, 0.0002, 0.002) * 0.3
    return soft_clip(body + click, 1.6)


def hat(open_: bool = False) -> np.ndarray:
    dur = 0.25 if open_ else 0.06
    n = int(dur * SR)
    return fft_filter(noise(dur), lo=7000, order=3) * env_ad(n, 0.0005, 0.09 if open_ else 0.012) * 0.35


def snare() -> np.ndarray:
    dur = 0.3
    n = int(dur * SR)
    tone = osc(190 * (1 + 0.3 * np.exp(-t_axis(dur) / 0.01)), dur) * env_ad(n, 0.001, 0.05)
    rattle = fft_filter(noise(dur), lo=1500, hi=9000, order=2) * env_ad(n, 0.001, 0.07)
    return (tone * 0.6 + rattle * 0.5)


def clap() -> np.ndarray:
    dur = 0.3
    n = int(dur * SR)
    burst = np.zeros(n)
    for k, off in enumerate((0.0, 0.009, 0.018)):
        nb = np.zeros(n)
        i = int(off * SR)
        nb[i:] = env_ad(n - i, 0.0005, 0.006 if k < 2 else 0.08)
        burst += nb
    return fft_filter(noise(dur), lo=900, hi=5000, order=2) * burst * 0.6


def bass_note(m: int, dur: float) -> np.ndarray:
    n = int(dur * SR)
    tt = t_axis(dur)
    x = osc(midi(m), dur, "saw") * 0.6 + osc(midi(m - 12), dur) * 0.6
    x = sweep_filter(x, 300 + 1500 * np.exp(-tt / 0.06), q=0.8)
    return soft_clip(x * env_ad(n, 0.003, dur * 0.6), 1.3)


def stab(ms: list[int], dur: float) -> np.ndarray:
    n = int(dur * SR)
    x = sum(osc(midi(m) * (1 + d), dur, "saw") for m in ms for d in (-0.005, 0.005))
    x = fft_filter(x, hi=3000, order=2) * env_ad(n, 0.002, 0.09)
    return x * 0.12


def energetic_beat() -> np.ndarray:
    """120 BPM, 16 bars (32 s). Am - F - C - G, kick, clap, hats, bass, off-beat stabs, rising arp."""
    bpm = 120
    beat = 60 / bpm
    bars = 16
    total = bars * 4 * beat
    n_total = int(total * SR)
    drums = np.zeros(n_total + SR * 2)
    music = np.zeros(n_total + SR * 2)
    prog = [(45, [57, 60, 64]), (41, [57, 60, 65]), (48, [55, 60, 64]), (43, [55, 59, 62])]
    k_s, h_s, ho_s, c_s = kick(), hat(), hat(True), clap() + snare()
    for bar in range(bars):
        root, ch = prog[bar % 4]
        t0 = bar * 4 * beat
        intro = bar < 2
        for b in range(4):
            place(drums, k_s, t0 + b * beat)
            if not intro:
                place(drums, h_s * 0.8, t0 + b * beat + beat / 2)
                place(drums, h_s * 0.35, t0 + b * beat + beat / 4)
                place(drums, h_s * 0.35, t0 + b * beat + 3 * beat / 4)
            if b in (1, 3) and not intro:
                place(drums, c_s, t0 + b * beat)
        if bar % 4 == 3 and not intro:
            place(drums, ho_s, t0 + 3.5 * beat)
        # bass on eighths with octave jumps
        for e in range(8):
            m = root + (12 if e in (3, 7) else 0)
            place(music, bass_note(m, beat / 2 * 0.95) * 0.55, t0 + e * beat / 2)
        # off-beat chord stabs
        if not intro:
            for b in range(4):
                place(music, stab(ch, beat / 2), t0 + b * beat + beat / 2)
        # arp in the second half
        if bar >= 8:
            arp = ch + [ch[0] + 12]
            for s in range(16):
                m = arp[s % 4] + 12
                place(music, osc(midi(m), 0.12, "tri") * env_ad(int(0.12 * SR), 0.002, 0.05) * 0.18,
                      t0 + s * beat / 4)
    music = reverb(music, 1.2, mix=0.15, seed=11)
    # side-chain style pumping on the music bus
    tt = np.arange(len(music)) / SR
    pump = 1 - 0.45 * np.exp(-((tt % beat) / 0.09))
    music *= pump[:, None]
    mix = music
    mix[: len(drums)] += np.stack([drums, drums], axis=1) * 1.6
    looped = loopable(mix, n_total)
    return normalize(soft_clip(looped / np.max(np.abs(looped)) * 1.1, 1.2), -1.5)


SOUNDS = {
    "01-whoosh": whoosh,
    "02-ui-click": ui_click,
    "03-pop": pop,
    "04-riser": riser,
    "05-bass-impact": bass_impact,
    "06-ding": ding,
    "07-typing": typing,
    "08-glitch": glitch,
    "09-music-calm": calm_pad,
    "10-music-energetic": energetic_beat,
}


def write_wav(path: Path, x: np.ndarray) -> None:
    if x.ndim == 1:
        x = np.stack([x, x], axis=1)
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: make_sounds.py OUT_DIR", file=sys.stderr)
        return 2
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    for name, fn in SOUNDS.items():
        x = fn()
        write_wav(out / f"{name}.wav", x)
        print(f"{name}.wav  {len(x) / SR:.2f} s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
