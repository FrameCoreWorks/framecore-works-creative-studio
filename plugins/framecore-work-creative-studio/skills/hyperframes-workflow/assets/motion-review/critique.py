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

# Reading time, the rule of references/motion-craft.md shared with check-score.mjs: the longer of 13 characters per
# second plus 0.5 s to settle and 0.5 s plus a third of a second per word, at least 1 s.
CHARACTERS_PER_SECOND = 13.0
WORDS_PER_SECOND = 3.0
SETTLE_SECONDS = 0.5
MIN_READ_SECONDS = 1.0
MIN_SCENE_SECONDS = 1.0
MAX_STILL_SCENE_SECONDS = 6.0
MAX_WORDS = {'vertical': 10, 'other': 14}
END_HOLD_SECONDS = 1.5
HOOK_SECONDS = 1.5
REELS_BOTTOM_ZONE = 0.14     # captions, buttons and the account name cover the bottom of a 9:16 feed
REELS_TOP_ZONE = 0.08
BALANCE = (0.3, 0.62)         # where the centre of a 9:16 frame's content should sit, as a share of the height
PENALTY = {'error': 15, 'warning': 5, 'note': 0}
PACE_SAMPLES_PER_SECOND = 4   # pacing looks at the picture four times a second
MICRO_CHANGE = 0.015          # under 1.5% of the frame changing between samples is micro-motion (drift), not a new beat
STATIC_ALLOWANCE = 1.5        # seconds of stillness allowed beyond the reading time of the copy on screen
APPEAR = 0.002                # content area growing or shrinking by 0.2% of the frame means something appeared or left
NO_COPY_STILL = 2.0           # seconds a scene without copy may stay visually unchanged
REPEATED_TRANSITION = 3       # the same full-frame wipe or mask at this many boundaries reads as a template


def load_renderer():
    for path in (os.path.join(HERE, '..', 'motion-render', 'render.py'), os.path.join(HERE, 'render.py')):
        if os.path.exists(path):
            spec = importlib.util.spec_from_file_location('studio_render', path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
    raise RuntimeError('render.py (the motion renderer) must sit in ../motion-render/ or next to critique.py')


def hex_rgb(hex_colour):
    value = str(hex_colour or '#000000').lstrip('#')
    if len(value) in (3, 4):
        value = ''.join(c * 2 for c in value)
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def luminance(hex_colour):
    r, g, b = (c / 255 for c in hex_rgb(hex_colour))
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


def scene_assets(scene, score):
    """Assets the scene shows: its `assets` list and any params value naming an asset ID."""
    known = {a.get('id'): a for a in score.get('assets') or [] if isinstance(a, dict)}
    ids = [i for i in scene.get('assets') or [] if i in known]

    def walk(value):
        if isinstance(value, str) and value in known and value not in ids:
            ids.append(value)
        elif isinstance(value, list):
            for item in value:
                walk(item)
        elif isinstance(value, dict):
            for item in value.values():
                walk(item)
    walk(scene.get('params') or {})
    return [known[i] for i in ids]


def words(texts):
    """Words as a reader counts them: whitespace-separated tokens with a letter or digit (a URL is one word)."""
    return sum(sum(1 for token in text.split() if re.search(r'\w', token)) for text in texts)


def reading_seconds(texts):
    """Seconds needed to read the texts shown together (joined by spaces, as check-score.mjs joins a scene's copy)."""
    shown = ' '.join(texts)
    return max(MIN_READ_SECONDS, len(shown) / CHARACTERS_PER_SECOND + SETTLE_SECONDS, SETTLE_SECONDS + words(texts) / WORDS_PER_SECOND)


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
    """The review frames of a delivered video, for hosts whose own renderer drew it. The video must have the contract's
    size, frame rate and length; only the frames under review are decoded, so a long or large video does not fill memory."""

    def __init__(self, path, score, wanted):
        import shutil
        import subprocess
        from PIL import Image
        ffmpeg, ffprobe = shutil.which('ffmpeg'), shutil.which('ffprobe')
        if not ffmpeg or not ffprobe:
            raise RuntimeError('ffmpeg and ffprobe are needed to read frames from a video')
        if not os.path.isfile(path):
            raise RuntimeError(f'video not found: {path}')
        self.size = (score['width'], score['height'])
        probe = json.loads(subprocess.run([ffprobe, '-v', 'error', '-select_streams', 'v:0', '-count_packets', '-show_entries',
                                           'stream=width,height,r_frame_rate,nb_read_packets', '-of', 'json', path],
                                          capture_output=True, text=True, check=True).stdout)['streams'][0]
        num, _, den = probe['r_frame_rate'].partition('/')
        fps, expected = float(num) / float(den or 1), score['fps']['num'] / score['fps']['den']
        frames = int(probe.get('nb_read_packets') or 0)
        problems = []
        if (probe['width'], probe['height']) != self.size:
            problems.append(f"size {probe['width']}x{probe['height']}, contract {self.size[0]}x{self.size[1]}")
        if abs(fps - expected) > 0.01:
            problems.append(f'{fps:.3f} fps, contract {expected:.3f}')
        if abs(frames - score['totalFrames']) > 1:
            problems.append(f"{frames} frames, contract {score['totalFrames']}")
        if problems:
            raise RuntimeError('the video does not match its contract (' + '; '.join(problems) + '); judge the matching revision')
        self.wanted = sorted({max(0, min(frames - 1, int(n))) for n in wanted})
        select = '+'.join(f'eq(n\\,{n})' for n in self.wanted)
        raw = subprocess.run([ffmpeg, '-v', 'error', '-i', path, '-vf', f'select={select}', '-fps_mode', 'passthrough',
                              '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
        frame_bytes = self.size[0] * self.size[1] * 3
        if len(raw) != frame_bytes * len(self.wanted):
            raise RuntimeError(f'decoded {len(raw) // frame_bytes} of {len(self.wanted)} review frames')
        self.frames = {n: raw[i * frame_bytes:(i + 1) * frame_bytes] for i, n in enumerate(self.wanted)}
        self.last = frames - 1
        self.image = Image

    def frame(self, n):
        return self.image.frombytes('RGB', self.size, self.frames[max(0, min(self.last, int(n)))])


class Critique:
    def __init__(self, score):
        self.score = score
        self.fps = score['fps']['num'] / score['fps']['den']
        self.findings = []
        self.pacing_report = []
        self.keyframes = []

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
                need = reading_seconds(texts)
                have = self.s(held) if held else self.s(length) * 0.6
                if have + 1e-6 < need:
                    short = self.frames(need - have)
                    self.add('error' if have < 0.85 * need else 'warning', 'readability', sid, f'{count} words held {have:.2f} s; reading needs about {need:.1f} s',
                             f'lengthen the scene by {short} frames: node revise.mjs extend <contract> --scene {sid} --frames {short} --out <next revision>, '
                             f'or cut the copy to {max(1, int((have - SETTLE_SECONDS) * WORDS_PER_SECOND))} words')
                if count > limit:
                    self.add('warning', 'text amount', sid, f'{count} words in one scene; a {"vertical" if vertical else "wide"} video reads best with at most {limit}',
                             'split the line across two scenes or cut it; one idea per scene')
            if self.s(length) < MIN_SCENE_SECONDS and count:
                self.add('warning', 'pace', sid, f'scene lasts {self.s(length):.2f} s, too short to register',
                         f'lengthen it to at least {MIN_SCENE_SECONDS} s or merge it with a neighbour')
            reading = reading_seconds(texts) if count else 0
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
        # Transitions: the same full-frame wipe, mask or slide at many boundaries is a template, not a choice.
        kinds = {}
        for scene in scenes[:-1]:
            p = scene.get('params') or {}
            label = str(scene.get('transition') or '').strip().lower()
            family = next((w for w in ('wipe', 'mask', 'slide', 'swipe', 'push', 'sweep') if w in label), None)
            if p.get('exit') == 'sweep':
                family = 'sweep'
            if family:
                kinds.setdefault(family, []).append(scene['id'])
        for family, ids in kinds.items():
            if len(ids) >= REPEATED_TRANSITION:
                self.add('warning', 'transitions', ', '.join(ids), f'{len(ids)} boundaries use the same {family}; repeated full-frame wipes separate slides instead of carrying the story',
                         'let an element carry the change (the product, a search field, a selection mark) where the scenes are connected, and keep the wipe for one real break')
        # Photographs with their own opaque background show as rectangles on a different scene colour.
        for scene in scenes:
            background = (scene.get('params') or {}).get('background') or tokens.get('background')
            for asset in scene_assets(scene, score):
                own = asset.get('background')
                if not own or own == 'transparent' or not background:
                    continue
                if sum((x - y) ** 2 for x, y in zip(hex_rgb(own), hex_rgb(background))) ** 0.5 > 12:
                    self.add('warning', 'integration', scene['id'], f'asset {asset.get("id")} has an opaque {own} background on a {background} scene; its rectangle will show',
                             f'set the scene background to {own}, or use an isolated (transparent) version of the asset, then check the encoded frames')
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
            width, height = score['width'], score['height']
            frames = set(r.check_frames(score))
            for scene in score['scenes']:
                for a, b in scene.get('holds') or []:
                    frames.add((a + b) // 2)
            keys = self.key_frames(score)
            frames.update(keys.values())
            # Pacing samples (base format only: formats share one timeline): the picture four times a second.
            step = max(1, round(self.fps / PACE_SAMPLES_PER_SECOND))
            pace_frames = {n for scene in score['scenes'] for n in range(scene['start'], scene['end'], step)} if format_id == 'base' else set()
            renderer = VideoFrames(video, score, frames | pace_frames) if video else r.Renderer(score)
            pace_images = {}
            for n in sorted(frames | pace_frames):
                image = renderer.frame(n)
                if n in pace_frames:
                    pace_images[n] = image.convert('L').resize((max(1, width // 4), max(1, height // 4)))
                for label, frame in keys.items():
                    if frame == n and out:
                        self.save_keyframe(out, format_id, label, n, image)
                if n not in frames:
                    continue
                feed = score['height'] > score['width'] or bool(score.get('strategy')) or re.search(r'feed|reel|tiktok|shorts|stories', str(score.get('viewing') or ''), re.I)
                if n == 0 and format_id == 'base' and feed:
                    first_bg = (score['scenes'][0].get('params') or {}).get('background') or (score.get('tokens') or {}).get('background') or '#000000'
                    blank = ImageChops.difference(image, Image.new('RGB', image.size, r.color(first_bg)[:3])).convert('L').point(lambda v: 255 if v > 28 else 0).getbbox()
                    if blank is None:
                        self.add('warning', 'hook', score['scenes'][0]['id'], 'the first frame is empty; it is the thumbnail and the first impression in a feed',
                                 'start with the product, the question or the mark already visible (shorten or remove the entry of the first element)')
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
            if pace_images:
                self.pacing(score, pace_images)
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

    def key_frames(self, score):
        """The frames to judge at full size and phone scale before a film is expanded: the opening, the densest
        readable moment and the ending."""
        scenes, last = score['scenes'], score['totalFrames'] - 1
        keys = {'opening': 0, 'ending': last}
        held = [(len(' '.join(scene_copy(scene, score))), scene, hold) for scene in scenes for hold in scene.get('holds') or []]
        if held:
            _, scene, (a, b) = max(held, key=lambda item: item[0])
            keys['densest'] = (a + b) // 2
        first_hold = min((a for scene in scenes for a, _ in scene.get('holds') or []), default=None)
        if first_hold is not None:
            keys['first-read'] = first_hold
        return keys

    def save_keyframe(self, out, format_id, label, n, image):
        folder = os.path.join(out, 'keyframes')
        os.makedirs(folder, exist_ok=True)
        name = f'{format_id}-{label}-f{n}'
        image.save(os.path.join(folder, name + '.png'))
        phone = image.copy()
        phone.thumbnail((360, 360 * image.height // max(1, image.width)))
        phone.save(os.path.join(folder, name + '-phone.png'))
        self.keyframes.append({'format': format_id, 'label': label, 'frame': n, 'full': f'keyframes/{name}.png', 'phone': f'keyframes/{name}-phone.png'})

    def pacing(self, score, images):
        """Find stretches where the picture stays the same, or changes only by a small drift, for longer than the copy
        on screen needs. Drift keeps pixels moving but gives the viewer nothing new, so it does not count as a beat."""
        from PIL import ImageChops
        order = sorted(images)

        def content(image):
            # Share of the frame that differs from its dominant (background) tone: grows when something appears.
            histogram = image.histogram()
            mode = max(range(256), key=histogram.__getitem__)
            return sum(v for i, v in enumerate(histogram) if abs(i - mode) > 24) / (image.width * image.height)
        area = {n: content(images[n]) for n in order}
        change, still = {}, {}
        for a, b in zip(order, order[1:]):
            diff = ImageChops.difference(images[a], images[b]).point(lambda v: 255 if v > 24 else 0)
            change[b] = sum(diff.histogram()[255:]) / (diff.width * diff.height)
            # Still: little of the frame changes and nothing appears or disappears. A drifting photo keeps its area;
            # a new line, product or price adds area, so it counts as a beat even when it is small.
            still[b] = change[b] < MICRO_CHANGE and abs(area[b] - area[a]) < APPEAR
        for index, scene in enumerate(score['scenes']):
            samples = [n for n in order if scene['start'] <= n < scene['end']]
            texts = scene_copy(scene, score)
            allowed = (reading_seconds(texts) + STATIC_ALLOWANCE) if words(texts) else NO_COPY_STILL
            if index == len(score['scenes']) - 1:
                allowed += END_HOLD_SECONDS
            longest, run, run_start, drift, best = 0.0, [], None, 0.0, (None, None, 0.0)
            for n in samples[1:]:
                if still.get(n, False):
                    run_start = run_start if run_start is not None else order[order.index(n) - 1]
                    run.append(change[n])
                    length = self.s(n - run_start)
                    if length > longest:
                        longest, best = length, (run_start, n, max(run))
                else:
                    run, run_start = [], None
            entry = {'scene': scene['id'], 'longest_still_s': round(longest, 2), 'allowed_s': round(allowed, 2),
                     'largest_change_in_it': round(best[2], 4), 'from_frame': best[0], 'to_frame': best[1]}
            self.pacing_report.append(entry)
            if longest > allowed + 1e-6:
                moving = best[2] > 0
                self.add('warning', 'pace', scene['id'],
                         f'{longest:.1f} s ({self.s(best[0]):.1f}-{self.s(best[1]):.1f} s) where ' +
                         (f'only a small drift changes (at most {best[2]:.1%} of the frame between samples); drift is not a new beat'
                          if moving else 'the picture does not change') + f'; the copy needs about {allowed:.1f} s',
                         'shorten the stretch, or let it reveal something new (the next product, the search result, the price, the action)')

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
            except Exception as error:  # the timing rules still stand, but the picture was not inspected
                frames_status = f'not_run: {error}'
        result = critique.report()
        result['frames'] = frames_status
        result['contact_sheet'] = sheet
        # The status says what the score covers: a contract checked without frames certifies no video, and frames that
        # were asked for but could not be read leave the review incomplete, whatever the score.
        if args.no_frames:
            result['status'] = 'contract_only'
        elif frames_status.startswith('not_run'):
            result['status'] = 'incomplete'
        else:
            result['status'] = 'issues' if result['errors'] else 'checked'
        # The score is a number of rule penalties, never a visual verdict. Composition is judged only from frames, and
        # normal-speed playback is never observed by this tool, so its temporal verdict stays not_verified.
        pictured = result['status'] in ('checked', 'issues')
        visual = [f for f in critique.findings if f['area'] in ('layout', 'composition', 'contrast', 'integration')]
        result['score_scope'] = 'contract rules and inspected frames' if pictured else 'contract rules only; no picture inspected'
        # Pixels cannot show a word cut by a mask: the clip hides the overflow, so the frame looks tidy. Text
        # completeness is checked only by the text audit (text-audit.mjs, also inside review-frames.mjs).
        result['verdicts'] = {
            'layout': ('fail' if any(f['severity'] == 'error' for f in visual) else 'needs_review' if any(f['severity'] == 'warning' for f in visual) else 'pass_in_reviewed_frames') if pictured else 'not_verified',
            'text_completeness': 'not_checked_here: run text-audit.mjs or review-frames.mjs',
            'pacing_samples': 'checked' if critique.pacing_report else 'not_run',
            'temporal_playback': 'not_verified',
        }
        result['pacing'] = critique.pacing_report
        result['keyframes'] = critique.keyframes
        if args.out:
            with open(os.path.join(args.out, 'critique.json'), 'w', encoding='utf-8') as handle:
                handle.write(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
        print(json.dumps(result, indent=2, ensure_ascii=False))
        if result['status'] == 'incomplete':
            return 3
        return 1 if result['errors'] else 0
    except (OSError, ValueError, KeyError, RuntimeError, ImportError) as error:
        sys.stderr.write(f'{error}\n')
        return 2


if __name__ == '__main__':
    sys.exit(main())
