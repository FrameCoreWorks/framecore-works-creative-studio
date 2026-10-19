#!/usr/bin/env python3
"""A per-frame loudness envelope of one frequency band, and its hits, for audio-reactive motion.

  python3 audio_envelope.py song.mp3 --out bass.json                      # bass below 120 Hz at 30 fps
  python3 audio_envelope.py song.mp3 --band 2000:8000 --fps 25 --out hats.json
  python3 audio_envelope.py song.mp3 --start 40 --duration 23.4 --inject index.html

The envelope is what a speaker cone, a glowing ring or a pulsing light follows: one value from 0 to 1 per video
frame, with a fast attack and a slower release so it reads as a push, not as flicker. Hits are the moments the band
jumps (kicks in the bass band, snares or hats higher up), for one-shot effects such as a ring of air.

Output JSON: {"fps", "start", "duration", "band", "attack", "release", "env": [...], "kicks": [seconds...]}.
`--inject FILE` writes the same object between the lines `/* BEGIN ENVELOPE */` and `/* END ENVELOPE */` of a
composition, as `const ENVELOPE = {...};`, so the render needs no network or file reads, and sets `data-duration` on
the composition root and on a music clip (`data-timeline-role="music"`) to the envelope's length. Needs Python 3 and FFmpeg
only, so it also runs in a code-execution sandbox. The user supplies the track and confirms the right to use it.
Exit codes: 0 written, 1 bad input, 2 FFmpeg failed.
"""
import argparse
import array
import json
import math
import re
import subprocess
import sys
from pathlib import Path

SR = 8000
BEGIN, END = '/* BEGIN ENVELOPE */', '/* END ENVELOPE */'


def decode(path, band, start=None, duration=None, sr=SR):
    """Mono float samples of one band; `band` is (low, high) in Hz, either may be None."""
    low, high = band
    filters = ([f'highpass=f={low}'] * 2 if low else []) + ([f'lowpass=f={high}'] * 2 if high else [])
    cmd = ['ffmpeg', '-v', 'error']
    if start:
        cmd += ['-ss', str(start)]
    if duration:
        cmd += ['-t', str(duration)]
    cmd += ['-i', str(path), '-ac', '1', '-ar', str(sr)] + (['-af', ','.join(filters)] if filters else []) + ['-f', 'f32le', '-']
    raw = subprocess.run(cmd, check=True, capture_output=True).stdout
    samples = array.array('f')
    samples.frombytes(raw[:len(raw) // 4 * 4])
    return samples


def envelope(samples, fps, sr=SR, attack=0.75, release=0.18, ceiling=0.97):
    """RMS per video frame, scaled so the `ceiling` quantile is 1, then smoothed: rises by `attack`, falls by `release`."""
    hop = sr / fps
    count = round(len(samples) / hop)          # the resampler may drop a few samples at the end
    rms = []
    for i in range(count):
        a, b = int(i * hop), int((i + 1) * hop)
        chunk = samples[a:b]
        rms.append(math.sqrt(sum(v * v for v in chunk) / max(1, len(chunk))))
    if not rms:
        return []
    top = sorted(rms)[min(len(rms) - 1, int(ceiling * len(rms)))] or 1.0
    out, level = [], 0.0
    for value in rms:
        target = min(1.0, value / top)
        level += (target - level) * (attack if target > level else release)
        out.append(round(level, 3))
    return out


def hits(env, fps, rise=0.22, gap=0.18):
    """Times where the envelope jumps by `rise` within two frames, at least `gap` seconds apart."""
    found, last = [], -1e9
    before = lambda i: env[i] if i >= 0 else 0.0     # silence before the first frame, so a hit at 0 s counts
    for i in range(len(env)):
        if env[i] - min(before(i - 1), before(i - 2)) >= rise and env[i] >= before(i - 1) and i / fps - last >= gap:
            last = i / fps
            found.append(round(max(0.0, (i - 1) / fps), 3))
    return found


def band_of(text):
    match = re.fullmatch(r'(\d*):(\d*)', text or '')
    if not match or not any(match.groups()):
        raise ValueError('--band is LOW:HIGH in Hz, either side may be empty, for example :120 or 2000:8000')
    low, high = (int(v) if v else None for v in match.groups())
    if low and high and low >= high:
        raise ValueError('--band low must be below high')
    return low, high


def inject(path, data):
    text = Path(path).read_text(encoding='utf-8')
    a, b = text.find(BEGIN), text.find(END)
    if a < 0 or b < a:
        raise ValueError(f'{path}: needs the lines {BEGIN} and {END}')
    line = f"{BEGIN}\n      const ENVELOPE = {json.dumps(data, separators=(',', ':'))};\n      "
    text = text[:a] + line + text[b:]

    def set_duration(tag):
        tag = tag.group(0)
        if 'data-composition-id=' in tag or 'data-timeline-role="music"' in tag:
            tag = re.sub(r'data-duration="[^"]*"', f'data-duration="{data["duration"]:g}"', tag)
        return tag
    Path(path).write_text(re.sub(r'<(?:div|audio)\b[^>]*>', set_duration, text), encoding='utf-8')


def main(argv=None):
    parser = argparse.ArgumentParser(description='Per-frame band envelope and hits for audio-reactive motion.')
    parser.add_argument('audio')
    parser.add_argument('--band', default=':120', help='LOW:HIGH in Hz (default :120, the bass)')
    parser.add_argument('--fps', type=float, default=30)
    parser.add_argument('--start', type=float, help='seconds into the track')
    parser.add_argument('--duration', type=float, help='seconds to read')
    parser.add_argument('--attack', type=float, default=0.75, help='share of a rise taken per frame (0-1)')
    parser.add_argument('--release', type=float, default=0.18, help='share of a fall taken per frame (0-1)')
    parser.add_argument('--rise', type=float, default=0.22, help='jump that counts as a hit')
    parser.add_argument('--out', help='write JSON here (default: print)')
    parser.add_argument('--inject', help='write the envelope into this composition between the ENVELOPE markers')
    args = parser.parse_args(argv)
    try:
        band = band_of(args.band)
        if args.fps <= 0 or not (0 < args.attack <= 1 and 0 < args.release <= 1):
            raise ValueError('--fps must be positive; --attack and --release between 0 and 1')
        if not Path(args.audio).is_file():
            raise ValueError(f'{args.audio}: no such file')
    except ValueError as error:
        print(f'audio_envelope: {error}', file=sys.stderr)
        return 1
    try:
        samples = decode(args.audio, band, args.start, args.duration)
    except (OSError, subprocess.CalledProcessError) as error:
        print(f'audio_envelope: FFmpeg could not read {args.audio}: {error}', file=sys.stderr)
        return 2
    env = envelope(samples, args.fps, attack=args.attack, release=args.release)
    data = {'fps': args.fps, 'start': args.start or 0, 'duration': round(len(env) / args.fps, 3),
            'band': args.band, 'attack': args.attack, 'release': args.release, 'env': env,
            'kicks': hits(env, args.fps, rise=args.rise)}
    try:
        if args.inject:
            inject(args.inject, data)
    except (OSError, ValueError) as error:
        print(f'audio_envelope: {error}', file=sys.stderr)
        return 1
    text = json.dumps(data, separators=(',', ':'))
    if args.out:
        Path(args.out).write_text(text + '\n', encoding='utf-8')
    elif not args.inject:
        print(text)
    loud = sum(1 for v in env if v > 0.5) / max(1, len(env))
    print(f'audio_envelope: {len(env)} frames at {args.fps:g} fps, {len(data["kicks"])} hits, band {args.band} Hz, '
          f'above half level {loud:.0%} of the time', file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
