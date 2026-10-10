#!/usr/bin/env python3
"""FrameCore Works motion renderer: draws a motion contract frame by frame and encodes an MP4.

A Python port of the scene engine (../motion-scenes/motion-scenes.mjs): the same scene kinds,
params, easings, holds, exits, captions and formats, drawn with Pillow and encoded by ffmpeg
(H.264, yuv420p, no audio). Every visual value comes from the contract, so the same script and
the same fonts give the same frames for the same contract, and a revision changes only what its
contract changes. Requires Python 3.8+, Pillow and an ffmpeg executable (on PATH or from the
imageio-ffmpeg package); without ffmpeg it can still write stills.

  python render.py video.motion.json video.mp4
  python render.py video.motion.json video.mp4 --check-dir video-check
  python render.py video.motion.json --stills 0,78,93 --stills-dir stills
  python render.py video.motion.json video-9x16.mp4 --format 9x16 --font MyFont-Regular.ttf --font-bold MyFont-Bold.ttf
  python render.py video.motion.json video.mp4 --blur 8
  python render.py video.motion.json --check-dir phone-check --stills-width 360

Prints one JSON summary line (renderer version, frames, size, fonts used, encoder, files).
Exit code: 0 done, 1 render or encode failure, 2 setup problem.
"""
import argparse
import base64
import glob
import io
import json
import math
import re
import os
import shutil
import subprocess
import sys
from decimal import Decimal, ROUND_HALF_UP

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:  # pragma: no cover
    sys.stderr.write('Pillow is required: pip install pillow\n')
    sys.exit(2)

VERSION = '1.4.1'
RENDERER = f'FrameCore render.py {VERSION}'


def jround(value):
    """JavaScript Math.round: halves round up."""
    return math.floor(value + 0.5)


def bezier(x1, y1, x2, y2):
    def ease(x):
        if x <= 0 or x >= 1:
            return min(1.0, max(0.0, x))
        lo, hi, u = 0.0, 1.0, x
        for _ in range(30):
            u = (lo + hi) / 2
            bx = 3 * (1 - u) * (1 - u) * u * x1 + 3 * (1 - u) * u * u * x2 + u * u * u
            if bx < x:
                lo = u
            else:
                hi = u
        return 3 * (1 - u) * (1 - u) * u * y1 + 3 * (1 - u) * u * u * y2 + u * u * u
    return ease


EASINGS = {
    'easeOutCubic': bezier(0.33, 1, 0.68, 1),
    'easeOutQuart': bezier(0.25, 1, 0.5, 1),
    'easeOutExpo': bezier(0.16, 1, 0.3, 1),
    'easeInOutCubic': bezier(0.65, 0, 0.35, 1),
    'easeInCubic': bezier(0.32, 0, 0.67, 0),
    'linear': lambda x: min(1.0, max(0.0, x)),
}
KINDS = ('line-reveal', 'item-stagger', 'end-card', 'counter', 'quote', 'logo-reveal', 'device')


def progress(frame, start, duration, easing='linear'):
    return EASINGS[easing]((frame - start) / duration)


# ---------------------------------------------------------------- contract helpers (as in the engine)

def scale(score):
    return min(score['width'], score['height']) / 1080


def px(score, value):
    return jround(value * scale(score))


def motion(score):
    base = {'entryFrames': 15, 'exitFrames': 10, 'lineStaggerFrames': 6, 'itemStaggerFrames': 8,
            'entryEasing': 'easeOutCubic', 'exitEasing': 'easeInCubic', 'resolveEasing': 'easeOutExpo'}
    base.update(score.get('motion') or {})
    return base


def tokens(score):
    return score.get('tokens') or {}


def margin(score):
    return jround(score['width'] * tokens(score).get('marginRatio', 0.08))


def as_list(value):
    return value if isinstance(value, list) else [] if value is None else [value]


UNIT = r'(?:zł|gr|kg|km|cm|mm|ml|min|PLN|EUR|USD|[gmlhs])(?![^\W\d_])|%'


def keep_together(text):
    """The scene engine's typography: a one-letter word never ends a line, digit groups and a number with its unit stay together."""
    text = re.sub(r'(?<!\S)([^\W\d_]) +(?=\S)', '\\1\u00a0', str(text))
    text = re.sub(r'(\d) (?=\d{3}(?!\d))', '\\1\u00a0', text)
    return re.sub(r'(\d) (?=' + UNIT + ')', '\\1\u00a0', text)


def copy_text(score, key):
    return keep_together((score.get('copy') or {}).get(key, '')) if key is not None else ''


def exit_mode(scene, score):
    params = scene.get('params') or {}
    value = params['exit'] if 'exit' in params else scene['end'] < score['totalFrames']
    return 'none' if value is False else 'sweep' if value == 'sweep' else 'lift'


def safe_padding(score):
    area = tokens(score).get('safeArea')
    if not area:
        return 0, 0
    return jround(score['height'] * area.get('top', 0)), jround(score['height'] * area.get('bottom', 0))


def vertical(scene, score):
    direction = (scene.get('params') or {}).get('direction', 'auto')
    return direction == 'column' or (direction == 'auto' and score['width'] < score['height'] * 1.3)


def resolve_format(score, format_id):
    if format_id in (None, '', 'base'):
        return score
    fmt = next((item for item in score.get('formats') or [] if item.get('id') == format_id), None)
    if fmt is None:
        raise ValueError(f'Unknown format: {format_id}')
    params = fmt.get('params') or {}
    out = dict(score, format=fmt['id'], width=fmt['width'], height=fmt['height'], viewing=fmt.get('viewing', score.get('viewing')))
    out['tokens'] = dict(tokens(score), **(fmt.get('tokens') or {}))
    out['scenes'] = [dict(scene, params=dict(scene.get('params') or {}, **params[scene['id']])) if scene['id'] in params else scene
                     for scene in score['scenes']]
    return out


def device_layout(scene, score):
    """Port of deviceLayout(): whole-pixel geometry of the device, its screen and the caption area."""
    p, W, H, m = scene.get('params') or {}, score['width'], score['height'], margin(score)
    area = tokens(score).get('safeArea') or {}
    top, bottom = jround(H * area.get('top', 0)), H - jround(H * area.get('bottom', 0))
    phone, browser = p.get('frame', 'phone') == 'phone', p.get('frame') == 'browser'
    shots = as_list(p.get('screens'))
    first = next((a for a in score.get('assets') or [] if shots and a.get('id') == shots[0].get('asset')), {})
    aspect = first['width'] / first['height'] if (first.get('width') or 0) > 0 and (first.get('height') or 0) > 0 else 9 / 19.5 if phone else 16 / 10
    has_caption, portrait, gap = len(as_list(p.get('caption'))) > 0, H > W, px(score, 24)
    box, caption = {'x': m, 'y': top, 'w': W - 2 * m, 'h': bottom - top}, None
    if has_caption and portrait:
        ch = jround((bottom - top) * 0.28)
        caption = {'x': m, 'y': top, 'w': W - 2 * m, 'h': ch}
        box = {'x': m, 'y': top + ch, 'w': W - 2 * m, 'h': bottom - top - ch}
    elif has_caption:
        half = jround(W / 2)
        left = {'x': m, 'y': top, 'w': half - gap - m, 'h': bottom - top}
        right = {'x': half + gap, 'y': top, 'w': W - m - half - gap, 'h': bottom - top}
        caption, box = (left, right) if p.get('side', 'left') == 'left' else (right, left)
    bezel, bar = (px(score, 14), 0) if phone else (0, px(score, 58 if browser else 40))
    if phone:
        sh = jround(box['h'] * 0.84); sw = jround(sh * aspect)
        if sw + 2 * bezel > box['w'] * 0.9:
            sw = jround(box['w'] * 0.9 - 2 * bezel); sh = jround(sw / aspect)
    else:
        sw = jround(box['w'] * 0.92); sh = jround(sw / aspect)
        if sh + bar > box['h'] * 0.84:
            sh = jround(box['h'] * 0.84 - bar); sw = jround(sh * aspect)
    dw, dh = sw + 2 * bezel, sh + 2 * bezel + bar
    field = px(score, 34)
    return {'phone': phone, 'browser': browser, 'tap': px(score, 28),
            'address': {'x': px(score, 96), 'y': jround((bar - field) / 2), 'w': dw - px(score, 96) - px(score, 20), 'h': field} if browser else None,
            'portrait': portrait, 'caption': caption, 'bezel': bezel, 'bar': bar, 'sw': sw, 'sh': sh, 'dw': dw, 'dh': dh,
            'radius': jround(sw * 0.14) if phone else px(score, 14),
            'dx': jround(box['x'] + (box['w'] - dw) / 2), 'dy': jround(box['y'] + (box['h'] - dh) / 2),
            'island': {'x': jround((dw - sw * 0.3) / 2), 'y': bezel + px(score, 14), 'w': jround(sw * 0.3), 'h': px(score, 30)} if phone else None}


def device_frame(scene, score, frame):
    """Port of deviceFrame(): entry, camera focus and each screen's offset and opacity."""
    p, m, d = scene.get('params') or {}, motion(score), device_layout(scene, score)
    entry = progress(frame, scene['start'], m['entryFrames'] + 10, m['resolveEasing'])
    focus = {'s': 1.0, 'x': 0.5, 'y': 0.5}
    for key in as_list(p.get('focus')):
        k = progress(frame, scene['start'] + key.get('at', 0), key.get('frames', 24), 'easeInOutCubic')
        if k <= 0:
            break
        to = {'s': key.get('scale', 1), 'x': key.get('x', 0.5), 'y': key.get('y', 0.5)}
        focus = {name: focus[name] + (to[name] - focus[name]) * k for name in focus}
    shots, mode, tf = as_list(p.get('screens')), p.get('transition', 'push'), p.get('transitionFrames', 12)
    current = 0
    for i, shot in enumerate(shots):
        if frame >= scene['start'] + shot.get('at', 0):
            current = i
    k = 1 if current == 0 or mode == 'cut' else progress(frame, scene['start'] + shots[current].get('at', 0), tf, 'easeInOutCubic')
    screens = []
    for i in range(len(shots)):
        if i == current:
            screens.append({'opacity': 1, 'x': jround((1 - k) * d['sw']) if mode == 'push' else 0, 'alpha': k if mode == 'fade' else 1})
        elif i == current - 1 and k < 1:
            screens.append({'opacity': 1, 'x': -jround(k * d['sw']) if mode == 'push' else 0, 'alpha': 1})
        else:
            screens.append({'opacity': 0, 'x': 0, 'alpha': 1})
    taps = []
    for tap in as_list(p.get('taps')):
        at = scene['start'] + tap.get('at', 0)
        arrive = progress(frame, at - 4, 4, 'easeOutCubic')
        press = progress(frame, at, 3, 'easeInCubic') - progress(frame, at + 3, 5, 'easeOutCubic')
        spread = progress(frame, at, 14, 'easeOutCubic')
        taps.append({'opacity': arrive * (1 - progress(frame, at + 8, 6, 'linear')), 'scale': (1.3 - 0.3 * arrive) * (1 - 0.15 * press),
                     'ripple': 1 - spread if frame >= at else 0, 'rippleScale': 1 + spread, 'x': tap.get('x', 0.5), 'y': tap.get('y', 0.5)})
    px0, py0 = d['bezel'] + focus['x'] * d['sw'], d['bezel'] + d['bar'] + focus['y'] * d['sh']
    return {'layout': d, 'entry': entry, 'focus': focus, 'screens': screens, 'taps': taps,
            'tx': px0 * (1 - focus['s']), 'ty': py0 * (1 - focus['s']) + (1 - entry) * px(score, 60)}


def ring_image(diameter, ring, ring_rgba, fill_rgba=None, supersample=4):
    """A circle with a border of `ring` pixels (CSS border-box, background clipped to the padding box)."""
    size = diameter * supersample
    outer, inner = Image.new('L', (size, size), 0), Image.new('L', (size, size), 0)
    ImageDraw.Draw(outer).ellipse([0, 0, size - 1, size - 1], fill=255)
    pad = ring * supersample
    ImageDraw.Draw(inner).ellipse([pad, pad, size - 1 - pad, size - 1 - pad], fill=255)
    outer, inner = outer.resize((diameter, diameter), Image.LANCZOS), inner.resize((diameter, diameter), Image.LANCZOS)
    band = Image.composite(Image.new('L', outer.size, 0), outer, inner)
    image = tinted(band, ring_rgba)
    if fill_rgba:
        image.alpha_composite(tinted(inner, fill_rgba))
    return image


def background_wipe(scene, score, frame):
    """Port of backgroundWipe(): CSS inset() lengths [top, right, bottom, left] of the scene canvas, or None."""
    p, side = scene.get('params') or {}, (scene.get('params') or {}).get('backgroundWipe', 'none')
    if not p.get('background') or side == 'none':
        return None
    k = progress(frame, scene['start'], p.get('backgroundFrames', 12), 'easeInOutCubic')
    x, y = jround((1 - k) * score['width']), jround((1 - k) * score['height'])
    return {'left': [0, x, 0, 0], 'right': [0, 0, 0, x], 'up': [y, 0, 0, 0], 'down': [0, 0, y, 0]}[side]


def rounded_mask(width, height, radii, supersample=4):
    """An antialiased rounded-rectangle mask; radii are (top-left, top-right, bottom-right, bottom-left)."""
    big = Image.new('L', (width * supersample, height * supersample), 255)
    draw = ImageDraw.Draw(big)
    for i, r in enumerate(radii):
        if r <= 0:
            continue
        r = r * supersample
        corner = Image.new('L', (r, r), 0)
        ImageDraw.Draw(corner).pieslice([0, 0, 2 * r - 1, 2 * r - 1], 180, 270, fill=255)
        corner = corner.rotate(-90 * i, expand=False)
        x = 0 if i in (0, 3) else big.width - r
        y = 0 if i in (0, 1) else big.height - r
        big.paste(corner, (x, y))
    return big.resize((width, height), Image.LANCZOS)


def cover(image, width, height):
    """CSS object-fit: cover."""
    scale_by = max(width / image.width, height / image.height)
    resized = image.resize((max(1, jround(image.width * scale_by)), max(1, jround(image.height * scale_by))), Image.LANCZOS)
    left, top = (resized.width - width) // 2, (resized.height - height) // 2
    return resized.crop((left, top, left + width, top + height))


# ---------------------------------------------------------------- colors and fonts

def color(value, fallback=(0, 0, 0, 255)):
    if not value or value == 'transparent':
        return fallback
    value = value.strip()
    if value.startswith('#'):
        h = value[1:]
        if len(h) in (3, 4):
            h = ''.join(c * 2 for c in h)
        parts = [int(h[i:i + 2], 16) for i in range(0, len(h), 2)]
        return tuple(parts + [255]) if len(parts) == 3 else tuple(parts)
    if value.startswith('rgb'):
        nums = [float(n) for n in value[value.index('(') + 1:value.rindex(')')].replace('/', ',').replace(' ', ',').split(',') if n]
        alpha = nums[3] if len(nums) > 3 else 1
        return tuple(jround(n) for n in nums[:3]) + (jround(alpha * 255),)
    named = {'white': (255, 255, 255, 255), 'black': (0, 0, 0, 255)}
    return named.get(value.lower(), fallback)


FONT_DIRS = ['/usr/share/fonts', '/usr/local/share/fonts', os.path.expanduser('~/.fonts'), os.path.expanduser('~/.local/share/fonts'),
             '/Library/Fonts', '/System/Library/Fonts', os.path.join(os.environ.get('WINDIR', 'C:/Windows'), 'Fonts')]
ALIASES = {
    'sans-serif': ['Arial', 'LiberationSans', 'Arimo', 'Helvetica', 'DejaVuSans'],
    'serif': ['TimesNewRoman', 'LiberationSerif', 'Tinos', 'DejaVuSerif'],
    'monospace': ['CourierNew', 'LiberationMono', 'Cousine', 'DejaVuSansMono'],
}
for name in ('arial', 'helvetica', 'helveticaneue', 'system-ui', '-apple-system', 'segoeui', 'blinkmacsystemfont'):
    ALIASES[name] = ALIASES['sans-serif']
ALIASES['timesnewroman'] = ALIASES['times'] = ALIASES['serif']


def font_files():
    dirs = list(FONT_DIRS)
    try:
        import matplotlib
        dirs.append(os.path.join(os.path.dirname(matplotlib.__file__), 'mpl-data', 'fonts', 'ttf'))
    except Exception:
        pass
    files = []
    for folder in dirs:
        if os.path.isdir(folder):
            files += [f for f in glob.glob(os.path.join(folder, '**', '*'), recursive=True) if f.lower().endswith(('.ttf', '.otf'))]
    return sorted(set(files))


def find_font(family, bold, files):
    key = family.replace(' ', '').replace('-', '').lower()
    styles_bold = ('bold',)
    for path in files:
        stem = os.path.splitext(os.path.basename(path))[0]
        base, _, style = stem.partition('-')
        compact = stem.replace(' ', '').replace('-', '').replace('_', '').lower()
        name = base.replace(' ', '').replace('_', '').lower()
        style = style.lower()
        if not (name == key or compact in (key, key + 'bold', key + 'regular', key + 'bd', key + 'b')):
            continue
        is_bold = style in styles_bold or compact in (key + 'bold', key + 'bd', key + 'b')
        italic = 'italic' in style or 'oblique' in style
        if italic or is_bold != bold:
            continue
        if not bold and style not in ('', 'regular', 'book', 'roman', 'normal'):
            continue
        return path
    return None


class Fonts:
    def __init__(self, css_family, regular=None, bold=None):
        files = None
        self.paths = {}
        for weight, override in (('regular', regular), ('bold', bold)):
            if override:
                self.paths[weight] = override
                continue
            files = files if files is not None else font_files()
            names = []
            for item in (css_family or 'sans-serif').split(','):
                item = item.strip().strip('"\'')
                names += ALIASES.get(item.replace(' ', '').lower(), [item])
            names += ALIASES['sans-serif']
            path = next((p for p in (find_font(n, weight == 'bold', files) for n in names) if p), None)
            if path is None and weight == 'bold':
                path = self.paths.get('regular')
            if path is None:
                raise RuntimeError(f'No font file found for "{css_family}"; pass --font (and --font-bold) with a .ttf file')
            self.paths[weight] = path
        self.cache = {}

    def get(self, size, weight=400):
        key = ('bold' if int(weight) >= 600 else 'regular', size)
        if key not in self.cache:
            self.cache[key] = ImageFont.truetype(self.paths[key[0]], size)
        return self.cache[key]


# ---------------------------------------------------------------- text blocks

def wrap(text, font, width):
    lines = []
    for paragraph in str(text).split('\n'):
        words, line = paragraph.split(' '), ''
        for word in words:
            trial = word if not line else line + ' ' + word
            if line and font.getlength(trial) > width:
                lines.append(line)
                line = word
            else:
                line = trial
        lines.append(line)
    return lines


class TextBlock:
    """Wrapped text with a CSS-like line box: line height, half-leading above each line."""

    # Lines wider than their column, collected while scenes are laid out: such a word would be cropped silently.
    overflows = []

    def __init__(self, text, font, max_width, line_height=None, align='left', tabular=False):
        self.font, self.align, self.tabular = font, align, tabular
        ascent, descent = font.getmetrics()
        self.ascent = ascent
        self.line_height = line_height if line_height is not None else ascent + descent
        self.half_leading = (self.line_height - (ascent + descent)) / 2
        self.lines = wrap(text, font, max_width) if text != '' else ['']
        self.widths = [self.measure(line) for line in self.lines]
        if max_width < 10 ** 5:
            for line, width in zip(self.lines, self.widths):
                if width > max_width + 1:
                    TextBlock.overflows.append({'text': line.replace('\u00a0', ' '), 'width': jround(width), 'max_width': jround(max_width)})
        # One line shrinks to its text; wrapped text fills the available width, as a CSS block does.
        self.width = min(self.widths[0], max_width) if len(self.lines) == 1 else max_width
        self.height = self.line_height * len(self.lines)

    def digit_width(self):
        return max(self.font.getlength(d) for d in '0123456789')

    def measure(self, line):
        if not self.tabular:
            return self.font.getlength(line)
        cell = self.digit_width()
        return sum(cell if ch.isdigit() else self.font.getlength(ch) for ch in line)

    def mask(self, box_width=None):
        width = max(1, math.ceil(box_width if box_width is not None else self.width))
        height = max(1, math.ceil(self.height))
        image = Image.new('L', (width, height), 0)
        draw = ImageDraw.Draw(image)
        for i, line in enumerate(self.lines):
            x = 0
            if self.align == 'center':
                x = (width - self.widths[i]) / 2
            elif self.align == 'right':
                x = width - self.widths[i]
            baseline = i * self.line_height + self.half_leading + self.ascent
            if self.tabular:
                cell = self.digit_width()
                for ch in line:
                    advance = cell if ch.isdigit() else self.font.getlength(ch)
                    offset = (cell - self.font.getlength(ch)) / 2 if ch.isdigit() else 0
                    draw.text((x + offset, baseline), ch, font=self.font, fill=255, anchor='ls')
                    x += advance
            else:
                draw.text((x, baseline), line, font=self.font, fill=255, anchor='ls')
        return image


def solid(size, rgba):
    return Image.new('RGBA', (max(1, math.ceil(size[0])), max(1, math.ceil(size[1]))), rgba)


def tinted(mask, rgba):
    image = Image.new('RGBA', mask.size, rgba[:3] + (0,))
    alpha = mask if rgba[3] == 255 else mask.point(lambda v: v * rgba[3] // 255)
    image.putalpha(alpha)
    return image


def faded(image, opacity):
    if opacity >= 1:
        return image
    out = image.copy()
    out.putalpha(image.getchannel('A').point(lambda v: jround(v * max(0.0, opacity))))
    return out


class Element:
    """A positioned RGBA image inside a scene, with its own per-frame style."""

    def __init__(self, image, x, y):
        self.image, self.x, self.y = image, x, y


def place(layer, image, x, y, opacity=1.0):
    if image is None or opacity <= 0:
        return
    image = faded(image, opacity)
    x, y = jround(x), jround(y)
    canvas = Image.new('RGBA', layer.size, (0, 0, 0, 0))
    canvas.paste(image, (x, y))
    layer.alpha_composite(canvas)


def number_text(params, value):
    decimals = int(params.get('decimals', 0))
    quantum = Decimal(1).scaleb(-decimals)
    amount = Decimal(repr(float(value))).quantize(quantum, rounding=ROUND_HALF_UP)
    negative = amount < 0
    whole, _, fraction = f'{abs(amount):f}'.partition('.')
    locale = str(params.get('locale', 'en-US')).lower()
    group, point, min_group = {'pl': ('\u00a0', ',', 2), 'de': ('.', ',', 1), 'fr': ('\u202f', ',', 1), 'es': ('.', ',', 2), 'it': ('.', ',', 1)}.get(locale[:2], (',', '.', 1))
    if len(whole) >= 4 + (min_group - 1):
        parts = []
        while len(whole) > 3:
            parts.insert(0, whole[-3:])
            whole = whole[:-3]
        whole = group.join([whole] + parts)
    text = whole + (point + fraction if decimals > 0 else '')
    return f"{params.get('prefix', '')}{'-' if negative and amount != 0 else ''}{text}{params.get('suffix', '')}"


def load_asset(src, base_dir, width):
    """A logo as RGBA at the given width: a PNG/JPEG/WebP file or data URI, or SVG through cairosvg when installed."""
    from urllib.parse import unquote_to_bytes
    if src.startswith('data:'):
        header, _, payload = src.partition(',')
        data = base64.b64decode(payload) if header.endswith(';base64') else unquote_to_bytes(payload)
        is_svg = 'svg' in header
    elif '://' in src:
        raise RuntimeError(f'Asset {src} is a URL; supply the file next to the contract or as a data URI')
    else:
        with open(os.path.join(base_dir, src), 'rb') as handle:
            data = handle.read()
        is_svg = src.lower().endswith('.svg')
    if is_svg:
        try:
            import cairosvg
        except ImportError:
            raise RuntimeError('An SVG logo needs the cairosvg package; install it or supply a PNG of the same mark')
        data = cairosvg.svg2png(bytestring=data, output_width=width * 2)
    image = Image.open(io.BytesIO(data)).convert('RGBA')
    return image.resize((width, jround(image.height * width / image.width)), Image.LANCZOS)


# ---------------------------------------------------------------- scenes

class Scene:
    def __init__(self, scene, score, fonts, base_dir):
        if scene.get('kind') not in KINDS:
            raise ValueError(f"Scene {scene.get('id')} declares no supported kind ({', '.join(KINDS)})")
        self.scene, self.score, self.fonts, self.base_dir = scene, score, fonts, base_dir
        self.p, self.t, self.m = scene.get('params') or {}, tokens(score), motion(score)
        self.fg = color(self.t.get('foreground'), (255, 255, 255, 255))
        self.muted = color(self.t.get('muted') or self.t.get('foreground'), self.fg)
        self.accent = color(self.t.get('accent'), self.fg)
        self.left = margin(score)
        self.column_width = score['width'] - 2 * self.left
        self.pad_top, self.pad_bottom = safe_padding(score)
        self.mode = exit_mode(scene, score)
        self.layout()

    def stack(self, heights, gaps):
        total = sum(heights) + sum(gaps)
        y = self.pad_top + (self.score['height'] - self.pad_top - self.pad_bottom - total) / 2
        tops = []
        for height, gap in zip(heights, gaps):
            y += gap
            tops.append(y)
            y += height
        return tops

    def x_for(self, width, align):
        return self.left + (self.column_width - width) / 2 if align == 'center' else self.left

    def block(self, text, size, weight, max_width=None, line_height=None, align='left', tabular=False):
        font = self.fonts.get(size, weight)
        return TextBlock(text, font, max_width or self.column_width, line_height, align, tabular)

    def layout(self):
        s, p, score = self.scene, self.p, self.score
        kind = s['kind']
        self.parts = {}
        if kind == 'line-reveal':
            sizes, weights = p.get('sizes') or [132, 96], p.get('weights') or [700, 400]
            align = p.get('align', 'left')
            blocks = []
            for i, key in enumerate(as_list(p.get('lines'))):
                size = px(score, sizes[i] if i < len(sizes) else sizes[-1])
                weight = weights[i] if i < len(weights) else weights[-1]
                blocks.append(self.block(copy_text(score, key), size, weight, line_height=size * 1.1))
            tops = self.stack([b.height for b in blocks], [0] * len(blocks))
            self.lines = []
            for block, top in zip(blocks, tops):
                width = block.width if align == 'center' else self.column_width
                self.lines.append((tinted(block.mask(block.width), self.fg), self.x_for(block.width, align), top, block.height, width))
        elif kind == 'item-stagger':
            size, weight = px(score, p.get('size', 104)), p.get('weight', 700)
            pad_v, pad_h = px(score, 12), px(score, 36)
            background = color(self.t.get('background'), (0, 0, 0, 0))
            items = []
            for key in as_list(p.get('items')):
                block = self.block(copy_text(score, key), size, weight, max_width=self.column_width - 2 * pad_h)
                image = solid((block.width + 2 * pad_h, block.height + 2 * pad_v), background)
                image.alpha_composite(tinted(block.mask(block.width), self.fg), (pad_h, pad_v))
                items.append(image)
            self.down = vertical(s, score)
            gap = px(score, p.get('gap', 56))
            if self.down:
                row_h = sum(i.height for i in items) + gap * max(0, len(items) - 1)
                row_top = self.stack([row_h], [0])[0]
                y, placed = row_top, []
                for image in items:
                    placed.append((image, self.left + (self.column_width - image.width) / 2, y))
                    y += image.height + gap
                self.connector = (self.left + self.column_width / 2 - px(score, 3), row_top, px(score, 6), row_h)
            else:
                row_h = max([i.height for i in items] or [0])
                row_top = self.stack([row_h], [0])[0]
                free = self.column_width - sum(i.width for i in items)
                step = free / (len(items) - 1) if len(items) > 1 else 0
                x, placed = self.left, []
                for image in items:
                    placed.append((image, x, row_top + (row_h - image.height) / 2))
                    x += image.width + step
                self.connector = (self.left, row_top + row_h / 2, self.column_width, px(score, 6))
            self.items = placed
        elif kind == 'end-card':
            block = self.block(copy_text(score, p.get('text')), px(score, p.get('size', 120)), p.get('weight', 700), align='center')
            heights, gaps = [block.height], [0]
            if p.get('rule', True) is not False:
                heights.append(px(score, 6))
                gaps.append(px(score, 28))
            tops = self.stack(heights, gaps)
            self.text = (tinted(block.mask(block.width), self.fg), self.x_for(block.width, 'center'), tops[0])
            self.rule = (self.left + (self.column_width - px(score, 160)) / 2, tops[1], px(score, 160), px(score, 6)) if len(tops) > 1 else None
        elif kind == 'counter':
            self.align = p.get('align', 'center')
            self.number_size = px(score, p.get('size', 220))
            heights, gaps = [self.number_size], [0]
            self.label = None
            if p.get('label'):
                label = self.block(copy_text(score, p.get('label')), px(score, p.get('labelSize', 48)), 400)
                heights.append(label.height)
                gaps.append(px(score, 24))
            tops = self.stack(heights, gaps)
            self.number_top = tops[0]
            if p.get('label'):
                self.label = (tinted(label.mask(label.width), self.muted), self.x_for(label.width, self.align), tops[1])
            self.number_cache = {}
        elif kind == 'quote':
            align = p.get('align', 'left')
            size = px(score, p.get('size', 72))
            block = self.block(copy_text(score, p.get('quote')), size, 400, max_width=self.column_width * 0.78, line_height=size * 1.25)
            heights, gaps = [block.height], [0]
            attribution = None
            if p.get('attribution'):
                attribution = self.block(copy_text(score, p.get('attribution')), px(score, 40), 400)
                heights.append(attribution.height)
                gaps.append(px(score, 36))
            tops = self.stack(heights, gaps)
            self.quote = (tinted(block.mask(block.width), self.fg), self.x_for(block.width, align), tops[0])
            self.attribution = (tinted(attribution.mask(attribution.width), self.muted), self.x_for(attribution.width, align), tops[1]) if attribution else None
        elif kind == 'device':
            d = self.device = device_layout(s, score)
            body_color = color(p.get('deviceColor') or ('#111214' if d['phone'] else '#E9E9EC'))
            self.shots = []
            for shot in as_list(p.get('screens')):
                asset = next((a for a in score.get('assets') or [] if a.get('id') == shot.get('asset')), None)
                if not asset or not asset.get('src'):
                    raise ValueError(f"Scene {s['id']}: screen asset {shot.get('asset')} has no src")
                self.shots.append(cover(load_asset(asset['src'], self.base_dir, asset.get('width') or d['sw']), d['sw'], d['sh']))
            outer = d['radius'] + d['bezel'] if d['phone'] else d['radius']
            self.body_mask = rounded_mask(d['dw'], d['dh'], (outer,) * 4)
            self.body = Image.new('RGBA', (d['dw'], d['dh']), body_color)
            self.screen_mask = rounded_mask(d['sw'], d['sh'], (d['radius'],) * 4) if d['phone'] else None
            overlay = Image.new('RGBA', (d['dw'], d['dh']), (0, 0, 0, 0))
            if d['phone']:
                i = d['island']
                overlay.alpha_composite(tinted(rounded_mask(i['w'], i['h'], (jround(i['h'] / 2),) * 4), body_color), (i['x'], i['y']))
            else:
                size = px(score, 14)
                for n, dot in enumerate(('#FF5F57', '#FEBC2E', '#28C840')):
                    overlay.alpha_composite(tinted(rounded_mask(size, size, (px(score, 7),) * 4), color(dot)), (px(score, 20) + n * px(score, 22), jround((d['bar'] - size) / 2)))
                if d['browser']:
                    a = d['address']
                    field = tinted(rounded_mask(a['w'], a['h'], (jround(a['h'] / 2),) * 4), (255, 255, 255, 255))
                    url = TextBlock(copy_text(score, p.get('url')), self.fonts.get(px(score, 20), 400), 10 ** 6, a['h'])
                    text = tinted(url.mask(max(1, math.ceil(url.widths[0]))), color('#5F6368'))
                    clip = Image.new('RGBA', field.size, (0, 0, 0, 0))
                    clip.paste(text, (px(score, 14), 0))
                    clip.putalpha(Image.composite(clip.getchannel('A'), Image.new('L', clip.size, 0), field.getchannel('A')))
                    field.alpha_composite(clip)
                    overlay.alpha_composite(field, (a['x'], a['y']))
            self.overlay = overlay
            r, ring = d['tap'], px(score, 3)
            self.tap_marker = ring_image(2 * r, ring, (0, 0, 0, jround(0.35 * 255)), (255, 255, 255, jround(0.75 * 255)))
            self.tap_ripple = ring_image(2 * r, ring, color(self.t.get('accent'), (255, 255, 255, 255)))
            self.captions = []
            if d['caption']:
                area = d['caption']
                sizes, weights = p.get('captionSizes') or [72, 40], p.get('captionWeights') or [700, 400]
                align = 'center' if d['portrait'] else 'left'
                blocks = []
                for i, key in enumerate(as_list(p.get('caption'))):
                    size = px(score, sizes[i] if i < len(sizes) else sizes[-1])
                    weight = weights[i] if i < len(weights) else weights[-1]
                    blocks.append(TextBlock(copy_text(score, key), self.fonts.get(size, weight), area['w'], size * 1.2, align))
                total = sum(b.height for b in blocks)
                y = area['y'] + (area['h'] - total) / 2
                for block in blocks:
                    x = area['x'] + (area['w'] - block.width) / 2 if d['portrait'] else area['x']
                    self.captions.append((tinted(block.mask(block.width), self.fg), x, y, block.height))
                    y += block.height
        elif kind == 'logo-reveal':
            asset = next((a for a in score.get('assets') or [] if a.get('id') == p.get('asset')), None)
            if not asset or not asset.get('src'):
                raise ValueError(f"Scene {s['id']}: logo asset {p.get('asset')} has no src")
            width = px(score, p.get('width', 360))
            self.logo = load_asset(asset['src'], self.base_dir, width)
            height = self.logo.height
            top = self.stack([height], [0])[0]
            self.logo_pos = (self.left + (self.column_width - width) / 2, top)

    def number_image(self, text):
        if text not in self.number_cache:
            block = self.block(text, self.number_size, 700, line_height=self.number_size, tabular=True)
            self.number_cache[text] = (tinted(block.mask(block.width), self.fg), block.width)
        return self.number_cache[text]

    def draw(self, frame_image, frame):
        s, p, m, score = self.scene, self.p, self.m, self.score
        layer = Image.new('RGBA', frame_image.size, (0, 0, 0, 0))
        kind = s['kind']
        if kind == 'line-reveal':
            for i, (image, x, top, height, _) in enumerate(self.lines):
                k = progress(frame, s['start'] + i * m['lineStaggerFrames'], m['entryFrames'], m['entryEasing'])
                box = Image.new('RGBA', (image.width, max(1, math.ceil(height))), (0, 0, 0, 0))
                box.paste(image, (0, jround((1 - k) * 1.1 * height)))  # translateY(110%) inside the mask
                place(layer, box, x, top)
        elif kind == 'item-stagger':
            n = len(self.items)
            last_end = s['start'] + (n - 1) * m['itemStaggerFrames'] + m['entryFrames']
            if p.get('connector', True) is not False and n:
                k = progress(frame, s['start'] + 6, last_end - s['start'] - 6, 'linear')
                x, y, w, h = self.connector
                if self.down and h * k > 0:
                    place(layer, solid((w, h * k), self.accent), x, y)
                elif not self.down and w * k > 0:
                    place(layer, solid((w * k, h), self.accent), x, y)
            for i, (image, x, y) in enumerate(self.items):
                k = progress(frame, s['start'] + i * m['itemStaggerFrames'], m['entryFrames'], m['entryEasing'])
                place(layer, image, x, y + (1 - k) * px(score, 32), k)
        elif kind == 'end-card':
            k = progress(frame, s['start'], p.get('duration', 30), m['resolveEasing'])
            image, x, y = self.text
            factor = 0.94 + 0.06 * k
            if k > 0:
                scaled = image if factor == 1 else image.resize((max(1, jround(image.width * factor)), max(1, jround(image.height * factor))), Image.BICUBIC)
                place(layer, scaled, x + (image.width - scaled.width) / 2, y + (image.height - scaled.height) / 2, k)
            if self.rule:
                rx, ry, rw, rh = self.rule
                if rw * k >= 0.5:
                    place(layer, solid((rw * k, rh), self.accent), rx + rw * (1 - k) / 2, ry)
        elif kind == 'counter':
            label_k = progress(frame, s['start'], m['entryFrames'], m['entryEasing'])
            k = progress(frame, s['start'] + m['entryFrames'], p.get('duration', 45), p.get('easing', 'easeOutCubic'))
            value = p.get('from', 0) + (p.get('to', 0) - p.get('from', 0)) * k
            image, width = self.number_image(number_text(p, value))
            place(layer, image, self.x_for(width, self.align), self.number_top, label_k)
            if self.label:
                image, x, y = self.label
                place(layer, image, x, y + (1 - label_k) * px(score, 16), label_k)
        elif kind == 'quote':
            k = progress(frame, s['start'], m['entryFrames'] + 5, m['entryEasing'])
            image, x, y = self.quote
            place(layer, image, x, y + (1 - k) * px(score, 24), k)
            if self.attribution:
                image, x, y = self.attribution
                place(layer, image, x, y, progress(frame, s['start'] + p.get('attributionDelay', 30), m['entryFrames'], m['entryEasing']))
        elif kind == 'device':
            f, d = device_frame(s, score, frame), self.device
            screen = Image.new('RGBA', (d['sw'], d['sh']), (0, 0, 0, 255))
            for shot, state in zip(self.shots, f['screens']):
                if state['opacity'] * state['alpha'] > 0 and -d['sw'] < state['x'] < d['sw']:
                    layer_shot = Image.new('RGBA', screen.size, (0, 0, 0, 0))
                    layer_shot.paste(shot.convert('RGBA'), (state['x'], 0))
                    screen.alpha_composite(faded(layer_shot, state['alpha']))
            r = d['tap']
            for tap in f['taps']:
                cx, cy = jround(tap['x'] * d['sw']), jround(tap['y'] * d['sh'])
                for image, opacity, scale_by in ((self.tap_ripple, tap['ripple'], tap['rippleScale']), (self.tap_marker, tap['opacity'], tap['scale'])):
                    if opacity <= 0:
                        continue
                    size = max(1, jround(2 * r * scale_by))
                    scaled = image if size == 2 * r else image.resize((size, size), Image.BICUBIC)
                    place(screen, scaled, cx - size / 2, cy - size / 2, opacity)
            if self.screen_mask is not None:
                screen.putalpha(Image.composite(screen.getchannel('A'), Image.new('L', screen.size, 0), self.screen_mask))
            device = self.body.copy()
            device.alpha_composite(screen, (d['bezel'], d['bezel'] + d['bar']))
            device.alpha_composite(self.overlay)
            device.putalpha(Image.composite(device.getchannel('A'), Image.new('L', device.size, 0), self.body_mask))
            scale_by = f['focus']['s']
            if abs(scale_by - 1) > 1e-9:
                device = device.resize((max(1, jround(d['dw'] * scale_by)), max(1, jround(d['dh'] * scale_by))), Image.BICUBIC)
            place(layer, device, d['dx'] + f['tx'], d['dy'] + f['ty'], f['entry'])
            for i, (image, x, top, height) in enumerate(self.captions):
                k = progress(frame, s['start'] + 10 + i * m['lineStaggerFrames'], m['entryFrames'], m['entryEasing'])
                box = Image.new('RGBA', (image.width, max(1, math.ceil(height))), (0, 0, 0, 0))
                box.paste(image, (0, jround((1 - k) * 1.1 * height)))
                place(layer, box, x, top)
        elif kind == 'logo-reveal':
            k = progress(frame, s['start'], p.get('duration', 30), m['resolveEasing'])
            logo = self.logo.copy()
            mask = Image.new('L', logo.size, 0)
            if p.get('reveal') == 'wipe':
                ImageDraw.Draw(mask).rectangle([0, 0, jround(logo.width * k) - 1, logo.height], fill=255)
            else:
                radius = k * 0.75 * math.hypot(logo.width, logo.height) / math.sqrt(2)
                cx, cy = logo.width / 2, logo.height / 2
                ImageDraw.Draw(mask).ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=255)
            logo.putalpha(Image.composite(logo.getchannel('A'), Image.new('L', logo.size, 0), mask))
            place(layer, logo, *self.logo_pos)
        # Container exit: fade with a lift, or with a slide left under a sweeping line.
        sweep_frames = p.get('sweepFrames', m['exitFrames'] + 12)
        exit_start = s['end'] - sweep_frames if self.mode == 'sweep' else s['end'] - m['exitFrames']
        e = 0 if self.mode == 'none' else progress(frame, exit_start, m['exitFrames'], m['exitEasing'])
        dx, dy = (-px(score, 150) * e, 0) if self.mode == 'sweep' else (0, -px(score, 24) * e)
        if e > 0 or dx or dy:
            shifted = Image.new('RGBA', layer.size, (0, 0, 0, 0))
            shifted.paste(layer, (jround(dx), jround(dy)))
            layer = faded(shifted, 1 - e)
        # params.background: the scene draws on its own canvas, which can wipe in; without it, straight onto the frame.
        target = frame_image
        if p.get('background'):
            target = Image.new('RGBA', frame_image.size, color(p['background'])[:3] + (255,))
        if 1 - e > 0:
            target.alpha_composite(layer)
        if self.mode == 'sweep':
            k = progress(frame, exit_start, sweep_frames, 'easeInOutCubic')
            if 0 < k < 1:
                start, end = margin(score), score['width'] - margin(score)
                x = jround(start + (end - start) * k) - px(score, 3)
                top, bottom = jround(score['height'] * 0.16), score['height'] - jround(score['height'] * 0.16)
                line_color = color(p.get('sweepColor') or self.t.get('accent') or self.t.get('foreground'), self.fg)
                place(target, solid((px(score, 6), bottom - top), line_color), x, top)
        if target is not frame_image:
            wipe = background_wipe(s, score, frame)
            if wipe:
                top_, right, bottom_, left = wipe
                mask = Image.new('L', target.size, 0)
                if score['width'] - right > left and score['height'] - bottom_ > top_:
                    ImageDraw.Draw(mask).rectangle([left, top_, score['width'] - right - 1, score['height'] - bottom_ - 1], fill=255)
                target.putalpha(Image.composite(target.getchannel('A'), Image.new('L', target.size, 0), mask))
            frame_image.alpha_composite(target)


class Captions:
    def __init__(self, score, fonts):
        self.score, self.fonts, self.cache = score, fonts, {}
        t = tokens(score)
        self.style = t.get('captions') or {}
        self.bottom = max(jround(score['height'] * ((t.get('safeArea') or {}).get('bottom', 0))), jround(score['height'] * self.style.get('bottom', 0.08)))

    def draw(self, frame_image, frame):
        score = self.score
        caption = next((c for c in score.get('captions') or [] if c['start'] <= frame < c['end']), None)
        if not caption:
            return
        key = caption['copy']
        if key not in self.cache:
            size = px(score, self.style.get('size', 44))
            left = margin(score)
            pad_v, pad_h = px(score, 10), px(score, 22)
            block = TextBlock(copy_text(score, key), self.fonts.get(size, self.style.get('weight', 500)), score['width'] - 2 * left - 2 * pad_h, size * 1.3, 'center')
            box = Image.new('RGBA', (math.ceil(block.width + 2 * pad_h), math.ceil(block.height + 2 * pad_v)), (0, 0, 0, 0))
            ImageDraw.Draw(box).rounded_rectangle([0, 0, box.width - 1, box.height - 1], radius=px(score, 6), fill=color(self.style.get('background'), (0, 0, 0, 204)) if self.style.get('background') else (0, 0, 0, 204))
            box.alpha_composite(tinted(block.mask(block.width), color(self.style.get('color'), (255, 255, 255, 255))), (pad_h, pad_v))
            self.cache[key] = box
        box = self.cache[key]
        place(frame_image, box, (score['width'] - box.width) / 2, score['height'] - self.bottom - box.height)


class Renderer:
    def __init__(self, score, base_dir='.', font=None, font_bold=None):
        self.score = score
        self.fonts = Fonts(tokens(score).get('fontFamily'), font, font_bold)
        self.background = color(tokens(score).get('background'), (0, 0, 0, 255))[:3] + (255,)
        TextBlock.overflows = []
        self.scenes = [Scene(scene, score, self.fonts, base_dir) for scene in score['scenes']]
        self.overflows = list(TextBlock.overflows)
        self.captions = Captions(score, self.fonts) if score.get('captions') else None

    def frame(self, n, blur=1):
        """Frame n; with blur > 1, the average of `blur` subframes over a 180-degree shutter (n to n + 0.5)."""
        if blur > 1:
            average = None
            for i in range(blur):
                sub = self.frame(n + 0.5 * i / blur)
                average = sub if average is None else Image.blend(average, sub, 1 / (i + 1))
            return average
        image = Image.new('RGBA', (self.score['width'], self.score['height']), self.background)
        for scene in self.scenes:
            if scene.scene['start'] <= n < scene.scene['end']:
                scene.draw(image, n)
        if self.captions:
            self.captions.draw(image, n)
        return image.convert('RGB')


def check_frames(score):
    """First and last frame, both sides of every scene boundary, hold starts and sweep middles."""
    frames = {0, score['totalFrames'] - 1}
    m = motion(score)
    for scene in score['scenes']:
        frames.update({scene['start'] - 1, scene['start'], scene['end'] - 1, scene['end']})
        for hold in scene.get('holds') or []:
            frames.add(hold[0])
        if exit_mode(scene, score) == 'sweep':
            frames.add(scene['end'] - (scene.get('params') or {}).get('sweepFrames', m['exitFrames'] + 12) // 2)
    return sorted(f for f in frames if 0 <= f < score['totalFrames'])


def find_ffmpeg():
    path = shutil.which('ffmpeg')
    if path:
        return path
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None


def encode(renderer, out, crf, blur=1):
    score = renderer.score
    ffmpeg = find_ffmpeg()
    if not ffmpeg:
        raise RuntimeError('No ffmpeg found (install it or the imageio-ffmpeg package); use --stills to write frames instead')
    if score['width'] % 2 or score['height'] % 2:
        raise RuntimeError('H.264 in yuv420p needs an even width and height')
    fps = score['fps']
    command = [ffmpeg, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f"{score['width']}x{score['height']}",
               '-r', f"{fps['num']}/{fps['den']}", '-i', '-', '-an', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', str(crf),
               '-preset', 'medium', '-movflags', '+faststart', out]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    try:
        for n in range(score['totalFrames']):
            process.stdin.write(renderer.frame(n, blur).tobytes())
    finally:
        process.stdin.close()
    if process.wait() != 0:
        raise RuntimeError('ffmpeg failed to encode the video')
    return 'libx264'


def main(argv=None):
    parser = argparse.ArgumentParser(description='Render a FrameCore motion contract to MP4 frames.')
    parser.add_argument('contract')
    parser.add_argument('out', nargs='?', help='output MP4 path; never overwritten')
    parser.add_argument('--format', help="format id from the contract's formats ('base' by default)")
    parser.add_argument('--font', help='regular font file (.ttf/.otf) instead of resolving tokens.fontFamily')
    parser.add_argument('--font-bold', help='bold font file')
    parser.add_argument('--stills', help='comma-separated frame numbers to save as PNG')
    parser.add_argument('--stills-dir', default='stills')
    parser.add_argument('--check-dir', help='save the frame-check frames (boundaries, hold starts, sweeps) as PNG here')
    parser.add_argument('--stills-width', type=int, help='scale stills to this width, for example 360 to review at phone size')
    parser.add_argument('--blur', type=int, default=1, help='motion blur: average this many subframes per frame (8 is typical; renders that many times slower)')
    parser.add_argument('--crf', type=int, default=18)
    parser.add_argument('--allow-overflow', action='store_true', help='render although a word is wider than its column (it will be cropped)')
    parser.add_argument('--version', action='version', version=RENDERER)
    args = parser.parse_args(argv)
    try:
        with open(args.contract, encoding='utf-8') as handle:
            score = resolve_format(json.load(handle), args.format)
        if not args.out and not args.stills and not args.check_dir:
            raise ValueError('Give an output MP4, --stills or --check-dir')
        if args.out and os.path.exists(args.out):
            raise ValueError(f'Output file already exists: {args.out}')
        renderer = Renderer(score, os.path.dirname(os.path.abspath(args.contract)), args.font, args.font_bold)
    except (OSError, ValueError, RuntimeError, KeyError) as error:
        sys.stderr.write(f'{error}\n')
        return 2
    summary = {'renderer': RENDERER, 'format': score.get('format', 'base'), 'width': score['width'], 'height': score['height'],
               'fps': score['fps'], 'frames': score['totalFrames'], 'blur': args.blur, 'fonts': renderer.fonts.paths, 'stills': []}
    if renderer.overflows:
        summary['text_overflow'] = renderer.overflows
        if not args.allow_overflow:
            words = '; '.join(f"\"{o['text']}\" {o['width']} px in {o['max_width']} px" for o in renderer.overflows)
            sys.stderr.write(f'Text wider than its column would be cropped: {words}. Reduce the size, shorten the copy '
                             'or split the line in the contract; nothing was rendered.\n')
            summary['status'] = 'text_overflow'
            print(json.dumps(summary, ensure_ascii=False))
            return 4
    try:
        wanted = []
        if args.stills:
            wanted += [(args.stills_dir, int(n)) for n in args.stills.split(',') if n.strip()]
        if args.check_dir:
            wanted += [(args.check_dir, n) for n in check_frames(score)]
        for folder, n in wanted:
            os.makedirs(folder, exist_ok=True)
            path = os.path.join(folder, f'frame-{n:05d}.png')
            image = renderer.frame(n, args.blur)
            if args.stills_width:
                image = image.resize((args.stills_width, jround(image.height * args.stills_width / image.width)), Image.LANCZOS)
            image.save(path)
            summary['stills'].append(path)
        if args.out:
            summary['encoder'] = encode(renderer, args.out, args.crf, args.blur)
            summary['out'] = args.out
    except (OSError, RuntimeError, ValueError) as error:
        sys.stderr.write(f'{error}\n')
        return 1
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
