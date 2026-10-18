#!/usr/bin/env python3
"""Break a reference animation into a map you can build from: cuts, their beat grid, transition frames and what moves.

  python3 breakdown.py --video reference.mp4 --out breakdown/ [--thresh 5] [--debounce 12]

Writes, under --out:
  cuts.json            cut start frames and seconds, and the grid they fit (start = t0 + k * step, residual, BPM candidates)
  sheet_N.jpg          contact sheets at 4 fps, 30 frames each, with timestamps
  transitions/TNN.jpg  each cut from 2 frames before its start, every 2nd frame, 15 cells: the mechanism is read here
  motion-heatmap.jpg   per segment, the largest per-pixel frame difference in red over the first frame, with the moving area
  keyframes.jpg        the last clean frame of each segment (3 frames before the next cut): the composition map
  ref/segNN.png        the same frames at full resolution, as composition references
Thresholds: a still segment has a mean frame difference under 2 and a transition 10 to 40; the defaults (5, debounce 12
frames) suit most edits; tune them per film. A large movement inside a shot can register as a cut, so the grid fit
allows 20 % outliers and reports them.

Adapted from scripts/analyze/breakdown.py in huashu-art-motion by alchaincyf (MIT, see LICENSE.upstream). Needs FFmpeg,
NumPy and Pillow. Analyse only footage the user owns or may study; learn the mechanism, never copy the frames.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


def probe(video):
    out = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,r_frame_rate',
                          '-of', 'json', str(video)], capture_output=True, text=True, check=True).stdout
    stream = json.loads(out)['streams'][0]
    num, den = stream['r_frame_rate'].split('/')
    return stream['width'], stream['height'], float(num) / float(den)


def frames(video, w, h, gray=False):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(video), '-vf', f'scale={w}:{h}', '-f', 'rawvideo',
                          '-pix_fmt', 'gray' if gray else 'rgb24', '-'], capture_output=True, check=True).stdout
    shape = (-1, h, w) if gray else (-1, h, w, 3)
    return np.frombuffer(raw, np.uint8).reshape(shape)


def cut_starts(diff, thresh, debounce):
    """First frame of each new shot: diff[i] compares frames i and i + 1."""
    starts = []
    for i in range(1, len(diff)):
        if diff[i] > thresh and diff[i - 1] <= thresh and (not starts or i + 1 - starts[-1] > debounce):
            starts.append(i + 1)
    return starts


def fit_grid(starts, fps):
    """The largest step such that at least 80 % of cut starts fall within 1.5 frames of t0 + k * step.
    The largest step wins because a small enough step can fit any set of points."""
    if len(starts) < 4:
        return None
    s = np.array(starts, float)
    best = None
    for step in np.arange(4.0, np.diff(s).max() + 0.01, 0.01):
        for t0 in s[:3]:
            k = np.round((s - t0) / step)
            inliers = np.abs(s - (t0 + k * step)) <= 1.5
            if inliers.mean() < 0.8:
                continue
            t0f = t0 + (s - (t0 + k * step))[inliers].mean()
            residual = s - (t0f + k * step)
            score = (step, int(inliers.sum()))
            if best is None or score > best[0]:
                best = (score, step, t0f, k.astype(int).tolist(), float(np.abs(residual[inliers]).max()), (~inliers).nonzero()[0].tolist())
    if not best:
        return None
    _, step, t0, units, worst, outliers = best
    return {'t0_frame': round(float(t0), 2), 'step_frames': round(float(step), 3), 'max_residual_frames': round(worst, 2),
            'units_per_cut': units, 'outlier_cut_index': outliers,
            'bpm_if_step_is_eighth': round(float(60 * fps / step / 2), 2), 'bpm_if_step_is_quarter': round(float(60 * fps / step), 2)}


def grid_image(images, cols, cell, labels=None, pad=0):
    w, h = cell
    rows = (len(images) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * w, rows * (h + pad)), 'white')
    draw = ImageDraw.Draw(sheet)
    for i, image in enumerate(images):
        x, y = (i % cols) * w, (i // cols) * (h + pad)
        sheet.paste(image, (x, y + pad))
        if labels:
            draw.text((x + 4, y + 2), labels[i], fill='black' if pad else 'yellow')
    return sheet


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--video', required=True)
    parser.add_argument('--out', required=True)
    parser.add_argument('--thresh', type=float, default=5)
    parser.add_argument('--debounce', type=int, default=12)
    args = parser.parse_args(argv)
    if not Path(args.video).is_file():
        print(f'breakdown: {args.video}: no such file', file=sys.stderr)
        return 1
    out = Path(args.out)
    (out / 'transitions').mkdir(parents=True, exist_ok=True)
    (out / 'ref').mkdir(exist_ok=True)
    try:
        width, height, fps = probe(args.video)
        gray = frames(args.video, 192, 108, gray=True).astype(np.float32)
        small = frames(args.video, 480, 270)
        mid = frames(args.video, 384, 216)
    except (OSError, subprocess.CalledProcessError, KeyError, IndexError, ValueError) as error:
        print(f'breakdown: FFmpeg could not read {args.video}: {error}', file=sys.stderr)
        return 2

    diff = np.abs(np.diff(gray, axis=0)).mean(axis=(1, 2))
    starts = cut_starts(diff, args.thresh, args.debounce)
    grid = fit_grid(starts, fps)
    report = {'fps': fps, 'size': [width, height], 'frames': int(len(small)), 'cuts_frames': starts,
              'cuts_sec': [round(s / fps, 3) for s in starts], 'grid': grid,
              'mean_diff_still_under_2': round(float((diff < 2).mean()), 3)}
    (out / 'cuts.json').write_text(json.dumps(report, indent=1), encoding='utf-8')

    every = max(1, round(fps / 4))
    picks = list(range(0, len(small), every))
    for n in range(0, len(picks), 30):
        sub = picks[n:n + 30]
        grid_image([Image.fromarray(small[f]) for f in sub], 6, (480, 270), [f'{f / fps:.2f}s' for f in sub], pad=18).save(out / f'sheet_{n // 30}.jpg', quality=85)

    for n, s in enumerate(starts):
        cells = [f for f in range(s - 2, s + 28, 2) if 0 <= f < len(mid)]
        grid_image([Image.fromarray(mid[f]) for f in cells], 5, (384, 216), [f'f{f} {f / fps:.3f}s' for f in cells], pad=14).save(out / 'transitions' / f'T{n + 1:02d}.jpg', quality=85)

    bounds = [0] + starts + [len(small)]
    heat, keys, moving = [], [], []
    for i in range(len(bounds) - 1):
        a0 = bounds[i] + (round(0.35 * fps) if i else 0)    # skip the tail of the previous transition
        b0 = bounds[i + 1] - 2
        ref = min(max(bounds[i], bounds[i + 1] - 3), len(small) - 1)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(args.video), '-vf', f'select=eq(n\\,{ref})', '-frames:v', '1',
                        str(out / 'ref' / f'seg{i + 1:02d}.png')], check=False)
        keys.append(Image.fromarray(small[ref]))
        if b0 - a0 < 4:
            continue
        seq = small[a0:b0].astype(np.float32)
        peak = np.abs(np.diff(seq, axis=0)).mean(axis=3).max(axis=0)
        share = float((peak > 25).mean())
        moving.append({'segment': i + 1, 'frames': [a0, b0], 'moving_area': round(share, 3)})
        base = Image.fromarray(seq[0].astype(np.uint8)).convert('L').convert('RGB')
        red = np.zeros((270, 480, 3), np.uint8)
        red[..., 0] = np.clip(peak * 4, 0, 255)
        image = Image.blend(base, Image.fromarray(red), 0.6)
        ImageDraw.Draw(image).text((4, 4), f'segment {i + 1} f{a0}-{b0} moving {share * 100:.1f}%', fill='yellow')
        heat.append(image)
    if heat:
        grid_image(heat, 4, (480, 270)).save(out / 'motion-heatmap.jpg', quality=85)
    grid_image(keys, 4, (480, 270)).save(out / 'keyframes.jpg', quality=85)
    report['segments_moving_area'] = moving
    (out / 'cuts.json').write_text(json.dumps(report, indent=1), encoding='utf-8')
    print(f'breakdown: {len(starts)} cuts at {report["cuts_sec"]}')
    print(f'breakdown: grid {grid}' if grid else 'breakdown: no beat grid (fewer than 4 cuts or no regular spacing)')
    print(f'breakdown: wrote {out}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
