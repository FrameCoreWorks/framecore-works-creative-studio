#!/usr/bin/env python3
"""Motion activity: how much of a rendered video stands still.

A frame check can pass a film whose motion stops after the first second. This tool samples the
encoded video, measures the change between samples and reports the share of still time and the
longest still stretch, outside the holds the plan declares (an end card, a deliberate pause).

    python3 motion_activity.py film.mp4
    python3 motion_activity.py film.mp4 --hold 12.5-15 --json

Needs Python 3.8+, numpy and ffmpeg. It measures pixels, not meaning: a slow drift counts as
motion, and a still that the idea needs is declared with --hold. Exit code 1 when a limit fails.
"""
import argparse
import json
import subprocess
import sys

import numpy as np

SAMPLE_FPS = 6
SIZE = (64, 114)          # width, height of the grey thumbnail; enough to see any visible change
STILL_DIFF = 0.6          # mean absolute grey change per sample below which a sample counts as still
MAX_STILL_SHARE = 0.40    # more than this share of undeclared still time fails
MAX_STILL_SECONDS = 2.5   # an undeclared still longer than this fails


def samples(path, fps=SAMPLE_FPS, size=SIZE):
    width, height = size
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-vf', f'fps={fps},scale={width}:{height},format=gray',
                          '-f', 'rawvideo', '-'], capture_output=True, check=True).stdout
    frames = np.frombuffer(raw, np.uint8)
    if frames.size < 2 * width * height:
        raise ValueError(f'{path}: fewer than two frames decoded')
    return frames[: frames.size // (width * height) * width * height].reshape(-1, height, width).astype(np.int16)


def parse_hold(text):
    start, end = (float(part) for part in text.split('-', 1))
    if end <= start:
        raise argparse.ArgumentTypeError(f'hold {text}: end must be after start')
    return start, end


def measure(frames, fps=SAMPLE_FPS, holds=(), still_diff=STILL_DIFF):
    change = np.abs(np.diff(frames, axis=0)).mean(axis=(1, 2))
    times = (np.arange(change.size) + 1) / fps            # each change ends at this sample time
    held = np.zeros(change.size, bool)
    for start, end in holds:
        held |= (times > start) & (times <= end)
    still = (change < still_diff) & ~held
    counted = (~held).sum()
    longest = run = 0
    longest_end = 0.0
    for index, value in enumerate(still):
        run = run + 1 if value else 0
        if run > longest:
            longest, longest_end = run, float(times[index])
    return {
        'seconds': round(frames.shape[0] / fps, 2),
        'still_share': round(float(still.sum() / counted), 3) if counted else 0.0,
        'longest_still_seconds': round(longest / fps, 2),
        'longest_still_ends_at': round(longest_end, 2),
        'mean_change': round(float(change.mean()), 2),
        'declared_holds': [list(hold) for hold in holds],
    }


def verdict(report, max_share=MAX_STILL_SHARE, max_seconds=MAX_STILL_SECONDS):
    problems = []
    if report['still_share'] > max_share:
        problems.append(f"{report['still_share']:.0%} of the undeclared time stands still (limit {max_share:.0%})")
    if report['longest_still_seconds'] > max_seconds:
        problems.append(f"a {report['longest_still_seconds']} s still ends at {report['longest_still_ends_at']} s (limit {max_seconds} s)")
    return problems


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('video')
    parser.add_argument('--hold', action='append', type=parse_hold, default=[], help='declared still, seconds START-END; repeatable')
    parser.add_argument('--max-share', type=float, default=MAX_STILL_SHARE)
    parser.add_argument('--max-still', type=float, default=MAX_STILL_SECONDS)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args(argv)
    report = measure(samples(args.video), holds=args.hold)
    problems = verdict(report, args.max_share, args.max_still)
    report['verdict'] = 'REVISE' if problems else 'PASS'
    report['problems'] = problems
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"{report['verdict']}: still {report['still_share']:.0%}, longest still {report['longest_still_seconds']} s, "
              f"mean change {report['mean_change']}" + ''.join(f"\n- {p}" for p in problems))
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
