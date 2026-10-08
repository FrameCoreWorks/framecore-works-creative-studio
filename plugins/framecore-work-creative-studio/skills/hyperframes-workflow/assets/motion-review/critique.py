#!/usr/bin/env python3
"""FrameCore Works motion critique: score a motion contract and its rendered frames against Studio's craft rubric.

The rubric turns a motion designer's judgement into numbers any model can act on: can every line be read in the
time it is held, does something worth watching happen in the first second, does the pace hold, does the ending land,
is there too much text per scene, does text keep clear of the edges and of the phone's interface zones, is the
contrast enough. Every finding comes with a concrete fix (often a ready `revise.mjs extend` command). It renders the
review frames with the bundled Python renderer and writes one contact sheet to look at. Python 3.8+ and Pillow;
no browser, no network.

  python critique.py video.motion.json --out critique            # report, findings and contact sheet
  python critique.py video.motion.json --out critique --no-frames  # timing and text rules only
  python critique.py video.motion.json --video video.mp4 --out critique  # judge the delivered video's own frames

Exit code: 0 no errors, 1 errors found, 2 setup problem. Errors must be fixed before delivery; warnings are fixed
unless the brief asks for the effect on purpose (say which and why).
"""
import argparse
import importlib.util
import json
import math
import os
import re
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))

WORDS_PER_SECOND = 3.0       # comfortable reading speed for short on-screen lines
PERCEPTION_SECONDS = 0.4     # time to notice that text has arrived
MIN_SCENE_SECONDS = 1.0
MAX_STILL_SCENE_SECONDS = 6.0
MAX_WORDS = {'vertical': 10, 'other': 14}
END_HOLD_SECONDS = 1.5
HOOK_SECONDS = 1.5
REELS_BOTTOM_ZONE = 0.14     # captions, buttons and the account name cover the bottom of a 9:16 feed
REELS_TOP_ZONE = 0.08
BALANCE = (0.3, 0.62)         # where the centre of a 9:16 frame's content should sit, as a share of the height
PENALTY = {'error': 15, 'warning': 5, 'note': 0}


def load_renderer():
    for path in (os.path.join(HERE, '..', 'motion-render', 'render.py'), os.path.join(HERE, 'render.py')):
        if os.path.exists(path):
            spec = importlib.util.spec_from_file_location('studio_render', path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
    raise RuntimeError('render.py (the motion renderer) must sit in ../motion-render/ or next to critique.py')


def luminance(hex_colour):
    value = str(hex_colour or '#000000').lstrip('#')
    if len(value) == 3:
        value = ''.join(c * 2 for c in value)
    r, g, b = (int(value[i:i + 2], 16) / 255 for i in (0, 2, 4))
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in (r, g, b)]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def scene_copy(scene, score):
    """Copy IDs the scene shows: its `copy` list and any params value naming a copy ID."""
    copy = score.get('copy') or {}
    ids = list(scene.get('copy') or [])

    def walk(value):
        if isinstance(value, str) and value in copy and value not in ids:
            ids.append(value)
        elif isinstance(value, list):
            for item in value:
                walk(item)
        elif isinstance(value, dict):
            for item in value.values():
                walk(item)
    walk(scene.get('params') or {})
    return [copy[i] for i in ids if isinstance(copy.get(i), str)]


def words(texts):
    """Words as a reader counts them: whitespace-separated tokens with a letter or digit (a URL is one word)."""
    return sum(sum(1 for token in text.split() if re.search(r'\w', token)) for text in texts)


def content_balance(mask, width, height, side=0.25, edge=0.05):
    """Where the content sits vertically, ignoring corner and edge decorations: (centre, extent) as shares of the
    height, from the rows of the frame's central column (the middle half of the width, where copy and the main visual
    stand); None when that column is empty."""
    from PIL import Image
    x0, y0 = int(width * side), int(height * edge)
    inner = mask.crop((x0, y0, width - x0, height - y0))
    rows = list(inner.resize((1, inner.height), Image.BOX).tobytes())
    total = sum(rows)
    if total < 255 * 0.002 * inner.height:
        return None
    centre = sum(i * v for i, v in enumerate(rows)) / total
    filled = [i for i, v in enumerate(rows) if v > 255 * 0.01]
    extent = (filled[-1] - filled[0]) / height if filled else 0
    return (y0 + centre) / height, extent


class VideoFrames:
    """Frames of a delivered video, for hosts whose own renderer drew it: decoded with ffmpeg at the contract's size."""

    def __init__(self, path, score):
        import shutil
        import subprocess
        from PIL import Image
        ffmpeg = shutil.which('ffmpeg')
        if not ffmpeg:
            raise RuntimeError('ffmpeg is needed to read frames from a video')
        self.size = (score['width'], score['height'])
        raw = subprocess.run([ffmpeg, '-v', 'error', '-i', path, '-vf', f'scale={self.size[0]}:{self.size[1]}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                             capture_output=True, check=True).stdout
        frame_bytes = self.size[0] * self.size[1] * 3
        self.frames = [raw[i:i + frame_bytes] for i in range(0, len(raw) - frame_bytes + 1, frame_bytes)]
        self.image = Image

    def frame(self, n):
        n = max(0, min(len(self.frames) - 1, int(n)))
        return self.image.frombytes('RGB', self.size, self.frames[n])


class Critique:
    def __init__(self, score):
        self.score = score
        self.fps = score['fps']['num'] / score['fps']['den']
        self.findings = []

    def add(self, severity, area, where, message, fix):
        self.findings.append({'severity': severity, 'area': area, 'where': where, 'message': message, 'fix': fix})

    def s(self, frames):
        return frames / self.fps

    def frames(self, seconds):
        return int(math.ceil(seconds * self.fps))

    def timing(self):
        score, scenes = self.score, self.score['scenes']
        vertical = score['width'] < score['height']
        limit = MAX_WORDS['vertical' if vertical else 'other']
        for scene in scenes:
            sid, length = scene['id'], scene['end'] - scene['start']
            texts = scene_copy(scene, score)
            count = words(texts)
            held = sum(b - a for a, b in scene.get('holds') or [])
            if count:
                need = max(0.8, count / WORDS_PER_SECOND + PERCEPTION_SECONDS)
                have = self.s(held) if held else self.s(length) * 0.6
                if have + 1e-6 < need:
                    short = self.frames(need - have)
                    self.add('error' if have < 0.85 * need else 'warning', 'readability', sid, f'{count} words held {have:.2f} s; reading needs about {need:.1f} s',
                             f'lengthen the scene by {short} frames: node revise.mjs extend <contract> --scene {sid} --frames {short} --out <next revision>, '
                             f'or cut the copy to {max(1, int((have - PERCEPTION_SECONDS) * WORDS_PER_SECOND))} words')
                if count > limit:
                    self.add('warning', 'text amount', sid, f'{count} words in one scene; a {"vertical" if vertical else "wide"} video reads best with at most {limit}',
                             'split the line across two scenes or cut it; one idea per scene')
            if self.s(length) < MIN_SCENE_SECONDS and count:
                self.add('warning', 'pace', sid, f'scene lasts {self.s(length):.2f} s, too short to register',
                         f'lengthen it to at least {MIN_SCENE_SECONDS} s or merge it with a neighbour')
            reading = count / WORDS_PER_SECOND + PERCEPTION_SECONDS if count else 0
            if self.s(length) > max(MAX_STILL_SCENE_SECONDS, 1.8 * reading) and scene.get('kind') not in ('device',):
                self.add('warning', 'pace', sid, f'scene lasts {self.s(length):.1f} s with one idea; attention drops',
                         'shorten it, or add a second beat (a stagger, a camera move, a counter) inside it')
        first_hold = min((a for scene in scenes for a, _ in scene.get('holds') or []), default=None)
        if first_hold is not None and self.s(first_hold) > HOOK_SECONDS:
            self.add('warning', 'hook', scenes[0]['id'], f'the first readable moment comes at {self.s(first_hold):.1f} s; a feed decides in the first second',
                     'bring the first line in sooner (shorter first entry or an earlier first scene), or open on a moving mark')
        last = scenes[-1] if scenes else None
        if last:
            holds = last.get('holds') or []
            end_hold = self.s(holds[-1][1] - holds[-1][0]) if holds else self.s(last['end'] - last['start']) * 0.6
            if last.get('kind') in ('end-card', 'logo-reveal') and end_hold < END_HOLD_SECONDS:
                extra = self.frames(END_HOLD_SECONDS - end_hold)
                self.add('warning', 'ending', last['id'], f'the end card holds {end_hold:.2f} s; viewers need about {END_HOLD_SECONDS} s to read and remember it',
                         f'node revise.mjs extend <contract> --scene {last["id"]} --frames {extra} --out <next revision>')
            if last.get('kind') not in ('end-card', 'logo-reveal'):
                self.add('note', 'ending', last['id'], 'the video ends without an end card or logo; fine for a loop, weaker for a call to action',
                         'add an end-card scene with the name or the action, if the brief has one')
        m = score.get('motion') or {}
        stagger = m.get('lineStaggerFrames')
        if stagger is not None and stagger < 3:
            self.add('warning', 'motion', 'motion', f'lines arrive {stagger} frames apart; they read as one block', 'set lineStaggerFrames to 4 to 8')
        if stagger is not None and self.s(stagger) > 0.5:
            self.add('warning', 'motion', 'motion', f'lines arrive {self.s(stagger):.2f} s apart; the scene feels slow', 'set lineStaggerFrames so lines arrive 0.1 to 0.3 s apart')
        tokens = score.get('tokens') or {}
        if tokens.get('foreground') and tokens.get('background'):
            ratio = contrast(tokens['foreground'], tokens['background'])
            if ratio < 4.5:
                self.add('error', 'contrast', 'tokens', f'text contrast {ratio:.1f}:1 is below 4.5:1', 'darken or lighten foreground or background until the ratio is at least 4.5:1')
        lengths = [self.s(sc['end'] - sc['start']) for sc in scenes[:-1]]
        if len(lengths) >= 4:
            mean = sum(lengths) / len(lengths)
            spread = (sum((x - mean) ** 2 for x in lengths) / len(lengths)) ** 0.5 / mean
            if spread < 0.06:
                self.add('note', 'pace', 'scenes', 'every scene lasts the same time; the rhythm may feel mechanical', 'give the key line or the reveal a longer beat')

    def pictures(self, out, formats, video=None):
        """Render the review frames (or read them from the delivered video), check content against edges, interface
        zones and balance, write a contact sheet."""
        from PIL import Image, ImageChops, ImageDraw
        r = load_renderer()
        sections = []
        if video:
            formats = ['base']
        for format_id in formats:
            sheet_tiles = []
            sections.append(sheet_tiles)
            score = r.resolve_format(self.score, format_id) if format_id != 'base' else self.score
            renderer = VideoFrames(video, score) if video else r.Renderer(score)
            width, height = score['width'], score['height']
            frames = set(r.check_frames(score))
            for scene in score['scenes']:
                for a, b in scene.get('holds') or []:
                    frames.add((a + b) // 2)
            for n in sorted(frames):
                image = renderer.frame(n)
                scene = next((sc for sc in score['scenes'] if sc['start'] <= n < sc['end']), None)
                in_hold = scene is not None and any(a <= n < b for a, b in scene.get('holds') or [])
                if in_hold:
                    background = (scene.get('params') or {}).get('background') or (score.get('tokens') or {}).get('background') or '#000000'
                    bg = Image.new('RGB', image.size, r.color(background)[:3])
                    diff = ImageChops.difference(image, bg).convert('L').point(lambda v: 255 if v > 28 else 0)
                    box = diff.getbbox()
                    where = f'{scene["id"]} frame {n}' + (f' ({format_id})' if format_id != 'base' else '')
                    if box is None:
                        self.add('error', 'layout', where, 'nothing is visible while the scene should be read', 'check the scene params and copy IDs; re-render')
                    else:
                        x0, y0, x1, y1 = box
                        edge = 0.02
                        full_bleed = x0 <= 1 and y0 <= 1 and x1 >= width - 1 and y1 >= height - 1
                        p = scene.get('params') or {}
                        camera = scene.get('kind') == 'device' and any(
                            scene['start'] + k.get('at', 0) <= n for k in r.as_list(p.get('focus')))
                        if not full_bleed and not camera and (x0 < width * edge or y0 < height * edge or x1 > width * (1 - edge) or y1 > height * (1 - edge)):
                            self.add('error', 'layout', where, f'content reaches the frame edge (box {x0},{y0} to {x1},{y1})',
                                     'reduce the text size or the line length, or raise tokens.marginRatio')
                        if height > width * 1.5:
                            balance = content_balance(diff, width, height)
                            if balance and not BALANCE[0] <= balance[0] <= BALANCE[1] and balance[1] < 0.6:
                                centre = balance[0]
                                self.add('warning', 'composition', where, f'the content block is centred at {centre:.0%} of the height; '
                                         f'{"the lower" if centre < BALANCE[0] else "the upper"} part of the frame is left empty',
                                         'centre the block near 45% of the height, or fill the empty part with the scene\'s visual (a device, a chart, the mark)')
                        if not full_bleed and height > width * 1.5:
                            if y1 > height * (1 - REELS_BOTTOM_ZONE):
                                self.add('warning', 'layout', where, f'content reaches the bottom {int(REELS_BOTTOM_ZONE * 100)}% of a 9:16 frame, where Reels and TikTok show captions and buttons',
                                         'set tokens.safeArea.bottom to 0.14 or move the block up')
                            if y0 < height * REELS_TOP_ZONE:
                                self.add('warning', 'layout', where, f'content reaches the top {int(REELS_TOP_ZONE * 100)}% of a 9:16 frame, under the app bar',
                                         'set tokens.safeArea.top to 0.08 or move the block down')
                tile = image.copy()
                tile.thumbnail((270, 270 * height // width) if width >= height else (200, 200 * height // width))
                label = ImageDraw.Draw(tile)
                label.rectangle([0, 0, tile.width, 16], fill=(0, 0, 0))
                label.text((4, 2), f'{format_id} f{n} {n / self.fps:.2f}s{" hold" if in_hold else ""}', fill=(255, 255, 255))
                sheet_tiles.append(tile)
        sections = [tiles for tiles in sections if tiles]
        if sections and out:
            # One grid per format, stacked, so wide and tall frames each keep their own tile size.
            grids = []
            for tiles in sections:
                w, h = max(t.width for t in tiles), max(t.height for t in tiles)
                columns = 6 if w >= h else 8
                rows = math.ceil(len(tiles) / columns)
                grid = Image.new('RGB', (columns * (w + 6) + 6, rows * (h + 6) + 6), (40, 40, 40))
                for i, tile in enumerate(tiles):
                    grid.paste(tile, (6 + (i % columns) * (w + 6), 6 + (i // columns) * (h + 6)))
                grids.append(grid)
            sheet = Image.new('RGB', (max(g.width for g in grids), sum(g.height for g in grids)), (40, 40, 40))
            y = 0
            for grid in grids:
                sheet.paste(grid, (0, y))
                y += grid.height
            path = os.path.join(out, 'contact-sheet.png')
            sheet.save(path)
            return path
        return None

    def report(self):
        points = max(0, 100 - sum(PENALTY[f['severity']] for f in self.findings))
        by_area = {}
        for f in self.findings:
            by_area[f['area']] = by_area.get(f['area'], 0) + 1
        return {'score': points, 'errors': sum(f['severity'] == 'error' for f in self.findings),
                'warnings': sum(f['severity'] == 'warning' for f in self.findings), 'by_area': by_area, 'findings': self.findings}


def main(argv=None):
    parser = argparse.ArgumentParser(description='Score a motion contract and its frames against the Studio craft rubric.')
    parser.add_argument('contract')
    parser.add_argument('--out', help='folder for critique.json and contact-sheet.png; never overwritten')
    parser.add_argument('--no-frames', action='store_true', help='timing and text rules only; no rendering')
    parser.add_argument('--video', help='judge the frames of this delivered video instead of rendering them (for a custom renderer)')
    args = parser.parse_args(argv)
    try:
        with open(args.contract, encoding='utf-8') as handle:
            score = json.load(handle)
        if args.out:
            if os.path.exists(args.out):
                raise ValueError(f'Output folder already exists: {args.out}')
            os.makedirs(args.out)
        critique = Critique(score)
        critique.timing()
        sheet = None
        frames_status = 'not_run: --no-frames'
        if not args.no_frames:
            formats = ['base'] + [f['id'] for f in score.get('formats') or [] if f.get('id')]
            try:
                sheet = critique.pictures(args.out, formats, args.video)
                frames_status = 'checked in the delivered video' if args.video else 'checked'
            except Exception as error:  # the timing rules still stand when a frame cannot be drawn here
                frames_status = f'not_run: {error}'
        result = critique.report()
        result['frames'] = frames_status
        result['contact_sheet'] = sheet
        if args.out:
            with open(os.path.join(args.out, 'critique.json'), 'w', encoding='utf-8') as handle:
                handle.write(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 1 if result['errors'] else 0
    except (OSError, ValueError, KeyError, RuntimeError, ImportError) as error:
        sys.stderr.write(f'{error}\n')
        return 2


if __name__ == '__main__':
    sys.exit(main())
