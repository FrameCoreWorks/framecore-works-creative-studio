#!/usr/bin/env python3
"""Flash check: photosensitivity screening of a rendered video.

Fast full-frame flicker can trigger seizures in people with photosensitive epilepsy. This tool
samples the encoded video at 24 to 30 fps, converts each small frame to relative luminance and
counts flashes: pairs of opposing luminance changes of at least 0.10 whose darker side is below
0.80, over at least a quarter of the frame. More than 3 flashes in any one-second window fails,
and the report names the worst second.

    python3 flash_check.py film.mp4
    python3 flash_check.py film.mp4 --fps 24 --json

Needs Python 3.8+, numpy and ffmpeg. This is screening only, not WCAG, Harding or broadcast
conformance: it ignores saturated red flashes and patterns, and a small sample frame can miss
flicker in a small area. Exit code 1 when the limit fails, 2 when the video cannot be read.
"""
import argparse
import hashlib
import json
import subprocess
import sys

import numpy as np

SAMPLE_FPS = 30
SIZE = (64, 114)        # width, height of the sample frame
MIN_DELTA = 0.10        # relative luminance change that counts
DARK_LIMIT = 0.80       # the darker side of a counted change is below this
MIN_AREA = 0.25         # share of the frame that must change together
MAX_FLASHES = 3         # flashes allowed in any one-second window
SCREENING = 'Photosensitivity screening only; not WCAG, Harding or broadcast conformance.'


def fps_value(text):
    value = float(text)
    if not 24 <= value <= 30:
        raise argparse.ArgumentTypeError('--fps must be between 24 and 30')
    return value


def samples(path, fps=SAMPLE_FPS, size=SIZE):
    width, height = size
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-vf', f'fps={fps},scale={width}:{height},format=rgb24',
                          '-f', 'rawvideo', '-'], capture_output=True, check=True).stdout
    frame_bytes = width * height * 3
    if len(raw) < 2 * frame_bytes:
        raise ValueError(f'{path}: fewer than two frames decoded')
    rgb = np.frombuffer(raw[: len(raw) // frame_bytes * frame_bytes], np.uint8).reshape(-1, height, width, 3)
    # sRGB to linear through a 256-entry table on the 8-bit values, in float32, so long films stay small in memory.
    level = np.arange(256, dtype=np.float64) / 255.0
    table = np.where(level <= 0.04045, level / 12.92, ((level + 0.055) / 1.055) ** 2.4).astype(np.float32)
    weights = np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
    return table[rgb] @ weights


def measure(frames, fps=SAMPLE_FPS):
    before, after = frames[:-1], frames[1:]
    delta = after - before
    counted = np.minimum(before, after) < DARK_LIMIT
    up = ((delta >= MIN_DELTA) & counted).mean(axis=(1, 2)) >= MIN_AREA
    down = ((delta <= -MIN_DELTA) & counted).mean(axis=(1, 2)) >= MIN_AREA
    transitions, last = [], 0
    for index in range(delta.shape[0]):
        direction = 1 if up[index] else -1 if down[index] else 0
        if direction and direction != last:          # a slow ramp in one direction is one change
            transitions.append((index + 1) / fps)
            last = direction
    worst, worst_start = 0, 0.0
    for start in transitions:
        count = sum(1 for time in transitions if start <= time < start + 1)
        if count // 2 > worst:
            worst, worst_start = count // 2, start
    return {
        'seconds': round(frames.shape[0] / fps, 2),
        'fps': fps,
        'max_flashes_per_second': worst,
        'worst_second_start': round(worst_start, 2),
        'transitions': len(transitions),
        'screening': SCREENING,
    }


def verdict(report, max_flashes=MAX_FLASHES):
    if report['max_flashes_per_second'] > max_flashes:
        return [f"{report['max_flashes_per_second']} flashes in the second from {report['worst_second_start']} s "
                f"(limit {max_flashes}); slow the flicker, shrink its area or lower its contrast"]
    return []


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('video')
    parser.add_argument('--fps', type=fps_value, default=SAMPLE_FPS, help='sampling rate, 24 to 30')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args(argv)
    try:                                   # an input problem exits 2, never 1, which means REVISE
        frames = samples(args.video, args.fps)
    except (subprocess.CalledProcessError, ValueError) as error:
        print(f'cannot read video {args.video}: ' + (error.stderr.decode(errors='replace').strip().splitlines() or ['not a video'])[-1]
              if isinstance(error, subprocess.CalledProcessError) else str(error), file=sys.stderr)
        return 2
    report = measure(frames, args.fps)
    digest = hashlib.sha256()
    with open(args.video, 'rb') as handle:   # binds the result to this exact encoded file
        for block in iter(lambda: handle.read(1 << 20), b''):
            digest.update(block)
    report['video_sha256'] = digest.hexdigest()
    problems = verdict(report)
    report['verdict'] = 'REVISE' if problems else 'PASS'
    report['problems'] = problems
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"{report['verdict']}: at most {report['max_flashes_per_second']} flashes per second "
              f"(screening, not conformance)" + ''.join(f"\n- {p}" for p in problems))
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
