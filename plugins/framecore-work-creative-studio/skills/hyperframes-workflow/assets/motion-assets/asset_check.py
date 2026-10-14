#!/usr/bin/env python3
"""Generated cut-out assets for a motion film: check them, matte them, key them.

    python3 asset_check.py check boombox.png hand.png --screen-px 900 --zoom 1.3   # alpha, fake checkerboard, fringe, resolution
    python3 asset_check.py matte neon-white.png neon-black.png --out neon.png      # difference matte from a white and a black version
    python3 asset_check.py key hand-green.png --out hand.png                       # soft chroma key with despill, for opaque matte subjects

`check` reports per file PASS or REPAIR with the reason and the fix; exit 0 all pass, 1 something to repair, 2 input problem.
`matte` recovers real partial transparency (glass, glow, smoke) from two aligned renders of the same subject on pure white and
pure black, and refuses a pair whose subject moved. `key` is for solid, opaque, non-reflective subjects only; glass, chrome,
smoke, sparks, hair and neon go to `matte` or are composited on black with a screen blend. Outputs are new files; an existing
file is never overwritten. Python 3.8+, Pillow and NumPy. See ../../references/generated-motion-assets.md.
"""
import argparse
import json
import os
import sys

import numpy as np
from PIL import Image

sys.dont_write_bytecode = True
EDGE_BAND = 3          # pixels on each side of the alpha edge examined for fringe
FRINGE_GREEN = 24      # G - max(R, B) above this on edge pixels counts as green spill
FRINGE_SHARE = 0.02    # share of edge pixels allowed to fringe before a repair is asked
MISALIGNED = 0.04      # share of subject pixels whose white and black versions differ in colour, not only in brightness


def load(path):
    if not os.path.isfile(path):
        raise FileNotFoundError(f'not found: {path}')
    try:
        image = Image.open(path)
        image.load()
    except Exception as error:
        raise ValueError(f'not a readable image: {path} ({error})')
    return image


def rgba(image):
    return np.asarray(image.convert('RGBA'), dtype=np.float32)


def write_new(array, out):
    if os.path.exists(out):
        raise FileExistsError(f'output exists, choose a new name: {out}')
    Image.fromarray(np.clip(array, 0, 255).astype(np.uint8), 'RGBA').save(out)


def dilate(mask, steps):
    out = mask.copy()
    for _ in range(steps):
        grown = out.copy()
        grown[1:, :] |= out[:-1, :]; grown[:-1, :] |= out[1:, :]
        grown[:, 1:] |= out[:, :-1]; grown[:, :-1] |= out[:, 1:]
        out = grown
    return out


def erode(mask, steps):
    return ~dilate(~mask, steps)


def checkerboard(rgb, alpha):
    """A painted 'transparent' background: the border is a regular two-tone grid instead of one flat colour."""
    if alpha is not None and (alpha < 250).mean() > 0.01:
        return False
    border = np.concatenate([rgb[:12].reshape(-1, 3), rgb[-12:].reshape(-1, 3), rgb[:, :12].reshape(-1, 3), rgb[:, -12:].reshape(-1, 3)])
    luma = border @ np.array([0.299, 0.587, 0.114])
    low, high = np.percentile(luma, 10), np.percentile(luma, 90)
    if high - low < 12 or high - low > 120:
        return False
    two_tone = ((np.abs(luma - low) < 6) | (np.abs(luma - high) < 6)).mean() > 0.9
    if not two_tone:
        return False
    row = rgb[:12].mean(axis=0) @ np.array([0.299, 0.587, 0.114])   # alternating squares along the top edge
    flips = np.count_nonzero(np.diff((row > (low + high) / 2).astype(int)))
    return flips >= 4


def check_file(path, screen_px=None, zoom=1.0):
    image = load(path)
    problems, fixes = [], []
    data = rgba(image)
    has_alpha = image.mode in ('RGBA', 'LA', 'PA') or (image.mode == 'P' and 'transparency' in image.info)
    alpha = data[..., 3] if has_alpha else None
    rgb = data[..., :3]
    width, height = image.size
    result = {'file': path, 'size': [width, height], 'alpha': bool(has_alpha and (alpha < 255).any())}
    if checkerboard(rgb, alpha):
        problems.append('a painted checkerboard, not real transparency')
        fixes.append('regenerate: on a model with real alpha use its transparent-background option; on Gemini generate on white, edit to black, then run matte')
    elif not result['alpha']:
        problems.append('opaque: no transparent pixels')
        fixes.append('use the transparency route for its generator (native alpha, matte from white and black, key for a solid subject on green, or screen-blend a light effect generated on black)')
    else:
        solid = alpha > 200
        clear = alpha < 30
        edge = dilate(solid, EDGE_BAND) & dilate(clear, EDGE_BAND)
        edge &= alpha > 30                                    # pixels that show in the composite
        result['edge_pixels'] = int(edge.sum())
        if edge.any():
            r, g, b = rgb[..., 0][edge], rgb[..., 1][edge], rgb[..., 2][edge]
            green = float(((g - np.maximum(r, b)) > FRINGE_GREEN).mean())
            inner = rgb[erode(solid, EDGE_BAND + 2)]
            luma_edge = float((rgb[edge] @ np.array([0.299, 0.587, 0.114])).mean())
            luma_in = float((inner @ np.array([0.299, 0.587, 0.114])).mean()) if inner.size else luma_edge
            result['green_fringe_share'] = round(green, 4)
            result['edge_luma_vs_inside'] = round(luma_edge - luma_in, 1)
            if green > FRINGE_SHARE:
                problems.append(f'green fringe on {green:.1%} of the edge')
                fixes.append('despill (clamp G to max(R, B)) and choke the edge 1 to 2 px, or matte instead of keying')
            if inner.size and abs(luma_edge - luma_in) > 60:
                problems.append(f'{"dark" if luma_edge < luma_in else "bright"} halo along the edge')
                fixes.append('choke the edge 1 to 2 px or regenerate on the right background for this material')
    if screen_px:
        need = screen_px * zoom
        result['needed_px'] = round(need)
        if max(width, height) < need:
            problems.append(f'too small: {max(width, height)} px for {round(need)} px on screen at the largest zoom')
            fixes.append('regenerate at a higher resolution, or plan a smaller size or a shallower push-in')
    result['verdict'] = 'REPAIR' if problems else 'PASS'
    result['problems'], result['fixes'] = problems, fixes
    return result


def difference_matte(white_path, black_path, out):
    white, black = rgba(load(white_path))[..., :3], rgba(load(black_path))[..., :3]
    if white.shape != black.shape:
        raise ValueError('the white and black versions differ in size; generate the black one as an edit of the white one')
    distance = np.sqrt(((white - black) ** 2).sum(axis=-1))
    alpha = np.clip(1.0 - distance / np.sqrt(3 * 255.0 ** 2), 0.0, 1.0)
    colour = np.where(alpha[..., None] > 1e-3, black / np.maximum(alpha[..., None], 1e-3), 0.0)
    # Aligned versions differ by the same amount in every channel (255 x (1 - alpha)); a subject that moved between them
    # leaves pixels where the difference has a colour of its own.
    difference = white - black
    spread = difference.max(axis=-1) - difference.min(axis=-1)
    subject = alpha > 0.05
    share = float((subject & (spread > 40)).sum()) / max(1, int(subject.sum()))
    opaque = alpha > 0.9
    report = {'out': out, 'opaque_share': round(float(opaque.mean()), 4), 'misaligned_share': round(share, 4)}
    if share > MISALIGNED:
        report['verdict'] = 'REPAIR'
        report['fix'] = 'the subject moved between the two versions; regenerate the black one as an edit that changes only the background, or key a solid subject instead'
        return report
    write_new(np.dstack([np.clip(colour, 0, 255), alpha * 255]), out)
    report['verdict'] = 'PASS'
    return report


def chroma_key(path, out, key=(0, 255, 0), choke=1, soft=(30.0, 100.0)):
    data = rgba(load(path))
    rgb = data[..., :3]
    key = np.array(key, dtype=np.float32)

    def chroma(c):          # Cb and Cr: distance in colour, not brightness, so shadows on the screen key too
        return np.stack([-0.1687 * c[..., 0] - 0.3313 * c[..., 1] + 0.5 * c[..., 2], 0.5 * c[..., 0] - 0.4187 * c[..., 1] - 0.0813 * c[..., 2]], axis=-1)
    distance = np.sqrt(((chroma(rgb) - chroma(key[None, None, :])) ** 2).sum(axis=-1))
    alpha = np.clip((distance - soft[0]) / (soft[1] - soft[0]), 0.0, 1.0)
    solid = alpha > 0.98
    # The subject's own green (a label, a dial, leaves): green pixels that are not the screen's colour and do not touch it.
    screen = distance < 25
    greenish = (rgb[..., 1] - np.maximum(rgb[..., 0], rgb[..., 2])) > 40
    own_green = greenish & ~screen & ~dilate(screen, 3)
    report = {'out': out, 'subject_share': round(float(solid.mean()), 4)}
    if (~screen).any() and own_green.sum() / (~screen).sum() > 0.01:
        report['verdict'] = 'REPAIR'
        report['fix'] = 'the subject has green of its own; matte it from a white and a black version instead of keying'
        return report
    if choke:
        alpha = np.where(erode(alpha > 0.5, choke) | (alpha >= 0.98), alpha, alpha * 0.5)
    spill = rgb.copy()
    spill[..., 1] = np.minimum(rgb[..., 1], np.maximum(rgb[..., 0], rgb[..., 2]))      # despill everywhere: reflections too
    write_new(np.dstack([spill, alpha * 255]), out)
    report['verdict'] = 'PASS'
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest='command', required=True)
    c = sub.add_parser('check', help='alpha, fake checkerboard, fringe and resolution of each asset')
    c.add_argument('files', nargs='+')
    c.add_argument('--screen-px', type=float, help='largest planned on-screen size of the asset in pixels')
    c.add_argument('--zoom', type=float, default=1.0, help='largest camera push-in on the asset (1.3 = 130 %%)')
    m = sub.add_parser('matte', help='difference matte from a white and a black version')
    m.add_argument('white'); m.add_argument('black'); m.add_argument('--out', required=True)
    k = sub.add_parser('key', help='soft chroma key with despill for a solid, opaque subject on green')
    k.add_argument('file'); k.add_argument('--out', required=True)
    k.add_argument('--key', default='00FF00', help='background colour as hex (default 00FF00)')
    k.add_argument('--choke', type=int, default=1, help='edge choke in pixels (default 1)')
    args = parser.parse_args(argv)
    try:
        if args.command == 'check':
            results = [check_file(f, args.screen_px, args.zoom) for f in args.files]
            print(json.dumps(results, ensure_ascii=False, indent=1))
            return 0 if all(r['verdict'] == 'PASS' for r in results) else 1
        if args.command == 'matte':
            result = difference_matte(args.white, args.black, args.out)
        else:
            hexa = args.key.lstrip('#')
            result = chroma_key(args.file, args.out, tuple(int(hexa[i:i + 2], 16) for i in (0, 2, 4)), args.choke)
        print(json.dumps(result, ensure_ascii=False, indent=1))
        return 0 if result['verdict'] == 'PASS' else 1
    except (FileNotFoundError, FileExistsError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
