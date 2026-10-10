#!/usr/bin/env python3
"""Compose a static graphic with exact text: a background (generated, supplied or flat), the exact copy set in real fonts,
the real logo and price, at the exact size, as PNG, JPG and print PDF with bleed.

  python3 compose.py poster.static.json --out out/
  python3 compose.py poster.static.json --out out/ --formats png,pdf --strict
  python3 compose.py --presets                       # the named sizes this tool knows (dated, provisional)
  python3 compose.py --fonts-list                    # the bundled fonts and their names

The spec (`*.static.json`, see README.md) lists layers bottom to top: image, rect, gradient and text. Every text layer
is laid out before anything is drawn. The tool stops with exit code 4 and "status": "text_overflow" when a word is
wider than its box or the lines do not fit (after the optional shrink), and with "status": "missing_glyphs" when the
font has no glyph for a character; a cropped word or a box of tofu never reaches the client. It also measures the
contrast of every text layer against what is under it and reports the weakest; --strict makes a contrast below the
threshold an error (exit 5). Prints one JSON summary and writes <id>.audit.json next to the outputs.

Only Pillow is required. The PDF is an RGB raster at the print resolution with the bleed (and optional crop marks):
say so to a print shop; --icc converts to CMYK with an ICC profile the user supplies, nothing is converted silently.
"""
import argparse
import json
import math
import os
import re
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, features

VERSION = '1.0.0'
HERE = Path(__file__).resolve().parent
FONT_DIRS = [HERE.parent.parent.parent / 'pipeline-core/assets/fonts', HERE / 'fonts']
PRESETS = json.loads((HERE / 'presets.json').read_text(encoding='utf-8'))
MM_PER_INCH = 25.4
UNIT = r'(?:zł|gr|kg|km|cm|mm|ml|min|PLN|EUR|USD|[gmlhs])(?![^\W\d_])|%'
LAYOUT = ImageFont.Layout.RAQM if features.check('raqm') else ImageFont.Layout.BASIC


class SpecError(Exception):
    pass


# ------------------------------------------------------------------ text rules

def keep_together(text):
    """Polish typesetting, the same as the motion renderer's: a one-letter word never ends a line, digit groups stay together
    and a number stays with its unit. The inserted characters are no-break spaces, so the copy reads the same."""
    text = re.sub(r'(?<!\S)([^\W\d_]) +(?=\S)', '\\1\u00a0', str(text))
    text = re.sub(r'(\d) (?=\d{3}(?!\d))', '\\1\u00a0', text)
    return re.sub(r'(\d) (?=' + UNIT + ')', '\\1\u00a0', text)


def color(value, default=(0, 0, 0, 255)):
    if value is None:
        return default
    if isinstance(value, (list, tuple)):
        values = list(value) + [255] * (4 - len(value))
        return tuple(int(v) for v in values[:4])
    text = str(value).strip().lstrip('#')
    if len(text) in (3, 4):
        text = ''.join(c * 2 for c in text)
    if not re.fullmatch(r'[0-9a-fA-F]{6}([0-9a-fA-F]{2})?', text):
        raise SpecError(f'colour {value!r}: use #RRGGBB or #RRGGBBAA')
    rgb = tuple(int(text[i:i + 2], 16) for i in (0, 2, 4))
    return rgb + ((int(text[6:8], 16),) if len(text) == 8 else (255,))


def luminance(rgb):
    def channel(c):
        c = c / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (channel(c) for c in rgb[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


# ------------------------------------------------------------------ fonts

def font_index(extra_dirs):
    """{'inter bold': path, ...} from fonts.json manifests and file names in the font folders."""
    index = {}
    for folder in [Path(d) for d in extra_dirs] + FONT_DIRS:
        manifest = folder / 'fonts.json'
        if manifest.is_file():
            for family in json.loads(manifest.read_text(encoding='utf-8'))['families']:
                for item in family['files']:
                    index.setdefault(f"{family['family']} {item['style']}".lower(), folder / item['file'])
                    if item['style'] == 'Regular':
                        index.setdefault(family['family'].lower(), folder / item['file'])
        if folder.is_dir():
            for path in sorted(folder.rglob('*.[ot]tf')):
                index.setdefault(path.stem.lower(), path)
    return index


def resolve_font(name, index, base):
    if not name:
        raise SpecError('a text layer needs "font"')
    candidate = (base / name) if not os.path.isabs(name) else Path(name)
    if candidate.suffix.lower() in ('.ttf', '.otf') and candidate.is_file():
        return candidate
    key = str(name).lower().replace('-', ' ').strip()
    for option in (str(name).lower(), key, key.replace(' ', '')):
        if option in index:
            return index[option]
    known = sorted({k for k in index if ' ' in k})
    raise SpecError(f'font {name!r} not found; bundled names: {", ".join(known[:40])}')


def glyph(font, char):
    box = font.getbbox(char)
    image = Image.new('L', (box[2] - box[0] + 2, box[3] - box[1] + 2), 0)
    ImageDraw.Draw(image).text((1 - box[0], 1 - box[1]), char, font=font, fill=255)
    return box, image.tobytes()


def missing_glyphs(font, text):
    """Characters the font draws as its .notdef box (compared with an unassigned code point)."""
    tofu = glyph(font, '\u0378')
    return [char for char in sorted(set(text)) if not (char.isspace() or char in '\u00a0\u200b') and glyph(font, char) == tofu]


# ------------------------------------------------------------------ layout

def line_width(font, text, tracking):
    if not text:
        return 0.0
    return font.getlength(text) + tracking * max(len(text) - 1, 0)


def wrap(text, font, width, tracking):
    """Greedy lines at ordinary spaces; no-break spaces and hard line breaks are kept. Returns (lines, too_wide_words)."""
    lines, wide = [], []
    for paragraph in text.split('\n'):
        words = paragraph.split(' ')
        line = ''
        for word in words:
            if line_width(font, word, tracking) > width + 0.5:
                wide.append(word.replace('\u00a0', ' '))
            trial = word if not line else line + ' ' + word
            if line and line_width(font, trial, tracking) > width + 0.5:
                lines.append(line)
                line = word
            else:
                line = trial
        lines.append(line)
    return lines, wide


def balanced(text, font, width, tracking):
    """The narrowest width that keeps the greedy line count: no lonely short last line in a headline."""
    lines, wide = wrap(text, font, width, tracking)
    if len(lines) < 2 or wide:
        return lines, wide
    low, high = width * 0.5, width
    for _ in range(14):
        middle = (low + high) / 2
        trial, trial_wide = wrap(text, font, middle, tracking)
        if len(trial) == len(lines) and not trial_wide:
            high = middle
        else:
            low = middle
    return wrap(text, font, high, tracking)


class TextLayout:
    def __init__(self, layer, font_path, scale):
        self.layer = layer
        self.text = layer['text']
        shown = keep_together(self.text)
        if layer.get('uppercase'):
            shown = shown.upper()
        self.shown = shown
        self.font_path = font_path
        box = [v * scale for v in layer['box']]
        self.x, self.y, self.w, self.h = box
        self.size = layer['size'] * scale
        self.min_size = layer.get('min_size', layer['size']) * scale
        self.fit = layer.get('fit', 'none')
        self.line_height = float(layer.get('line_height', 1.15))
        self.tracking_em = float(layer.get('tracking', 0)) / 1000  # thousandths of an em, as in design tools
        self.max_lines = layer.get('max_lines')
        self.balance = layer.get('balance', layer['size'] >= 40)
        self.layout()

    def font_at(self, size):
        return ImageFont.truetype(str(self.font_path), max(1, round(size)), layout_engine=LAYOUT)

    def try_size(self, size):
        font = self.font_at(size)
        tracking = self.tracking_em * size
        lines, wide = (balanced if self.balance else wrap)(self.shown, font, self.w, tracking)
        ascent, descent = font.getmetrics()
        height = ascent + descent + (len(lines) - 1) * size * self.line_height
        fits = not wide and height <= self.h + 0.5 and (not self.max_lines or len(lines) <= self.max_lines)
        return font, tracking, lines, wide, height, fits

    def layout(self):
        size = self.size
        while True:
            font, tracking, lines, wide, height, fits = self.try_size(size)
            if fits or self.fit != 'shrink' or size <= self.min_size:
                break
            size = max(self.min_size, size * 0.96)
        self.font, self.tracking, self.lines, self.wide, self.height, self.fits = font, tracking, lines, wide, height, fits
        self.final_size = size
        self.missing = missing_glyphs(font, self.shown)

    def overflow(self, scale):
        if self.fits:
            return None
        reasons = []
        if self.wide:
            reasons.append(f'words wider than the box: {self.wide}')
        if self.height > self.h + 0.5:
            reasons.append(f'{len(self.lines)} lines need {self.height / scale:.0f} px, the box is {self.h / scale:.0f} px high')
        if self.max_lines and len(self.lines) > self.max_lines:
            reasons.append(f'{len(self.lines)} lines, max_lines {self.max_lines}')
        return {'layer': self.layer.get('id'), 'text': self.text, 'size': round(self.final_size / scale, 1), 'reasons': reasons}

    def draw(self, canvas, fill, shadow=None):
        mask = Image.new('L', canvas.size, 0)
        draw = ImageDraw.Draw(mask)
        ascent, descent = self.font.getmetrics()
        valign = self.layer.get('valign', 'top')
        top = self.y + {'top': 0, 'middle': (self.h - self.height) / 2, 'bottom': self.h - self.height}[valign]
        align = self.layer.get('align', 'left')
        for index, line in enumerate(self.lines):
            baseline = top + ascent + index * self.final_size * self.line_height
            width = line_width(self.font, line, self.tracking)
            left = self.x + {'left': 0, 'center': (self.w - width) / 2, 'right': self.w - width}[align]
            if self.tracking:
                for i, char in enumerate(line):
                    draw.text((left + self.font.getlength(line[:i]) + i * self.tracking, baseline), char, font=self.font, fill=255, anchor='ls')
            else:
                draw.text((left, baseline), line, font=self.font, fill=255, anchor='ls')
        if shadow:
            offset = shadow.get('offset', [0, 4])
            blur = shadow.get('blur', 8)
            shade = ImageChops.offset(mask, round(offset[0]), round(offset[1])).filter(ImageFilter.GaussianBlur(blur))
            layer = Image.new('RGBA', canvas.size, color(shadow.get('color', '#00000080'))[:3] + (0,))
            alpha = shade.point(lambda v, a=color(shadow.get('color', '#00000080'))[3]: v * a // 255)
            layer.putalpha(alpha)
            canvas.alpha_composite(layer)
        paint = Image.new('RGBA', canvas.size, fill[:3] + (0,))
        paint.putalpha(mask.point(lambda v, a=fill[3]: v * a // 255))
        canvas.alpha_composite(paint)
        return mask


# ------------------------------------------------------------------ drawing

def place_image(path, box, fit, focus, scale):
    image = Image.open(path)
    image.load()
    image = image.convert('RGBA')
    x, y, w, h = [round(v * scale) for v in box]
    sw, sh = image.size
    if fit == 'stretch':
        factor_x, factor_y = w / sw, h / sh
        placed = image.resize((w, h), Image.LANCZOS)
        return placed, (x, y), max(factor_x, factor_y)
    factor = max(w / sw, h / sh) if fit == 'cover' else min(w / sw, h / sh)
    resized = image.resize((max(1, round(sw * factor)), max(1, round(sh * factor))), Image.LANCZOS)
    if fit == 'cover':
        fx, fy = focus
        left = round((resized.width - w) * fx)
        top = round((resized.height - h) * fy)
        return resized.crop((left, top, left + w, top + h)), (x, y), factor
    anchor = focus
    return resized, (x + round((w - resized.width) * anchor[0]), y + round((h - resized.height) * anchor[1])), factor


def gradient(size, start, end, direction):
    w, h = size
    ramp = Image.linear_gradient('L')  # 256 x 256, black at the top
    if direction in ('left', 'right'):
        ramp = ramp.rotate(90 if direction == 'left' else -90, expand=True)
    elif direction == 'up':
        ramp = ramp.rotate(180)
    ramp = ramp.resize((max(1, w), max(1, h)), Image.BILINEAR)
    a = Image.new('RGBA', (w, h), start)
    b = Image.new('RGBA', (w, h), end)
    return Image.composite(b, a, ramp)


def resolve_canvas(spec):
    canvas = dict(spec.get('canvas') or {})
    preset = canvas.pop('preset', None) or spec.get('preset')
    safe_area = spec.get('safe_area') or (PRESETS['sizes'].get(preset, {}).get('safe_area') if preset else None)
    if preset:
        if preset not in PRESETS['sizes']:
            raise SpecError(f'unknown preset {preset!r}; run --presets')
        found = PRESETS['sizes'][preset]
        if 'px' in found:
            canvas.setdefault('width', found['px'][0])
            canvas.setdefault('height', found['px'][1])
        else:
            spec.setdefault('print', {})
            spec['print'].setdefault('width_mm', found['mm'][0])
            spec['print'].setdefault('height_mm', found['mm'][1])
            spec['print'].setdefault('bleed_mm', found.get('bleed_mm', PRESETS['print_defaults']['bleed_mm']))
    printing = spec.get('print')
    if printing:
        dpi = printing.get('dpi', PRESETS['print_defaults']['dpi'])
        bleed = printing.get('bleed_mm', PRESETS['print_defaults']['bleed_mm'])
        trim = (round(printing['width_mm'] / MM_PER_INCH * dpi), round(printing['height_mm'] / MM_PER_INCH * dpi))
        bleed_px = math.ceil(bleed / MM_PER_INCH * dpi - 1e-9)  # never less bleed than asked
        # Layout coordinates are in the design's own units: trim width = canvas width (default: the trim in pixels).
        design_w = canvas.get('width', trim[0])
        scale = trim[0] / design_w
        return {'design': (design_w, canvas.get('height', round(trim[1] / scale))), 'trim': trim, 'bleed_px': bleed_px, 'scale': scale,
                'dpi': dpi, 'bleed_mm': bleed, 'trim_mm': (printing['width_mm'], printing['height_mm']), 'background': canvas.get('background', '#FFFFFF'),
                'crop_marks': bool(printing.get('crop_marks')), 'safe_mm': printing.get('safe_margin_mm', PRESETS['print_defaults']['safe_margin_mm'])}
    if 'width' not in canvas or 'height' not in canvas:
        raise SpecError('canvas needs width and height, a preset, or a print block')
    size = (int(canvas['width']), int(canvas['height']))
    return {'design': size, 'trim': size, 'bleed_px': 0, 'scale': 1.0, 'dpi': canvas.get('dpi', 72), 'background': canvas.get('background', '#FFFFFF'),
            'safe_area': safe_area}


def safe_rect(frame):
    """Where text belongs, in canvas pixels: 5 mm inside the trim for print, the placement's safe area for a preset that has one."""
    bleed, (w, h) = frame['bleed_px'], frame['trim']
    if frame.get('safe_mm') is not None:
        margin = frame['safe_mm'] / MM_PER_INCH * frame['dpi']
        return (bleed + margin, bleed + margin, bleed + w - margin, bleed + h - margin), f"{frame['safe_mm']} mm inside the trim"
    area = frame.get('safe_area')
    if area:
        return (w * area.get('sides', 0), h * area.get('top', 0), w * (1 - area.get('sides', 0)), h * (1 - area.get('bottom', 0))), 'the placement safe area'
    return None, None


def bleed_box(box, frame, bleed_design):
    """A layer marked "bleed": true that touches an edge is extended into the bleed on that side."""
    x, y, w, h = box
    W, H = frame
    if x <= 0:
        x, w = x - bleed_design, w + bleed_design
    if y <= 0:
        y, h = y - bleed_design, h + bleed_design
    if x + w >= W:
        w += bleed_design
    if y + h >= H:
        h += bleed_design
    return [x, y, w, h]


def compose(spec, base, font_dirs, allow_overflow=False):
    frame = resolve_canvas(spec)
    scale, bleed = frame['scale'], frame['bleed_px']
    full = (frame['trim'][0] + 2 * bleed, frame['trim'][1] + 2 * bleed)
    bleed_design = bleed / scale
    index = font_index(font_dirs)
    texts, overflows, missing, warnings = [], [], [], []
    layouts = {}
    for number, layer in enumerate(spec['layers']):
        if layer.get('type') != 'text':
            continue
        if not isinstance(layer.get('text'), str) or not layer['text'].strip():
            raise SpecError(f'text layer {layer.get("id", number)} has no text')
        layout = TextLayout(layer, resolve_font(layer.get('font'), index, base), scale)
        layouts[number] = layout
        problem = layout.overflow(scale)
        if problem:
            overflows.append(problem)
        if layout.missing:
            missing.append({'layer': layer.get('id'), 'font': layout.font_path.name, 'characters': layout.missing})
    status = 'missing_glyphs' if missing else 'text_overflow' if overflows and not allow_overflow else 'ok'
    if status != 'ok':
        return None, frame, {'status': status, 'text_overflow': overflows, 'missing_glyphs': missing}
    canvas = Image.new('RGBA', full, color(frame['background']))
    contrast = []
    safe, safe_label = safe_rect(frame)
    for number, layer in enumerate(spec['layers']):
        kind = layer.get('type')
        opacity = float(layer.get('opacity', 1.0))
        box = layer.get('box', [0, 0, *frame['design']])
        if layer.get('bleed', kind in ('image', 'rect', 'gradient') and box[:2] == [0, 0]):
            box = bleed_box(box, frame['design'], bleed_design)
        shifted = [box[0] + bleed_design, box[1] + bleed_design, box[2], box[3]]
        if kind == 'image':
            source = base / layer['src']
            if not source.is_file():
                raise SpecError(f'image {layer["src"]} not found next to the spec')
            placed, at, factor = place_image(source, shifted, layer.get('fit', 'cover'), layer.get('focus', [0.5, 0.5]), scale)
            if factor > 1.02:
                effective = frame['dpi'] / factor if spec.get('print') else None
                warnings.append(f'{layer.get("id", layer["src"])}: enlarged {factor:.2f}x' + (f'; effective {effective:.0f} ppi' if effective else '') + '; a sharper source is better')
            if opacity < 1:
                placed.putalpha(placed.getchannel('A').point(lambda v: round(v * opacity)))
            sheet = Image.new('RGBA', full, (0, 0, 0, 0))
            sheet.paste(placed, at)
            canvas.alpha_composite(sheet)
        elif kind in ('rect', 'gradient'):
            x, y, w, h = [round(v * scale) for v in shifted]
            if kind == 'rect':
                fill = color(layer.get('fill', '#000000'))
                fill = fill[:3] + (round(fill[3] * opacity),)
                sheet = Image.new('RGBA', full, (0, 0, 0, 0))
                ImageDraw.Draw(sheet).rounded_rectangle([x, y, x + w - 1, y + h - 1], radius=round(layer.get('radius', 0) * scale), fill=fill)
            else:
                sheet = Image.new('RGBA', full, (0, 0, 0, 0))
                sheet.paste(gradient((w, h), color(layer.get('from', '#00000000')), color(layer.get('to', '#000000FF')), layer.get('direction', 'down')), (x, y))
            canvas.alpha_composite(sheet)
        elif kind == 'text':
            layout = layouts[number]
            layout.x, layout.y = shifted[0] * scale, shifted[1] * scale
            fill = color(layer.get('color', '#000000'))
            behind = canvas.copy()
            mask = layout.draw(canvas, fill, layer.get('shadow'))
            contrast.append(measure_contrast(layer, layout, behind, mask, fill, scale))
            ink = mask.getbbox()
            if safe and ink and (ink[0] < safe[0] - 0.5 or ink[1] < safe[1] - 0.5 or ink[2] > safe[2] + 0.5 or ink[3] > safe[3] + 0.5):
                warnings.append(f'{layer.get("id", "text")}: text reaches outside {safe_label}')
            texts.append({'layer': layer.get('id'), 'text': layer['text'], 'set_as': layout.shown.replace('\u00a0', ' '), 'lines': [l.replace('\u00a0', ' ') for l in layout.lines],
                          'font': layout.font_path.name, 'size': round(layout.final_size / scale, 1), 'requested_size': layer['size'],
                          'shrunk': layout.final_size < layout.size - 0.01, 'locked': bool(layer.get('locked', True))})
        else:
            raise SpecError(f'layer {number}: unknown type {kind!r} (image, rect, gradient, text)')
    return canvas, frame, {'status': 'ok', 'texts': texts, 'contrast': contrast, 'warnings': warnings, 'text_overflow': overflows}


def measure_contrast(layer, layout, behind, mask, fill, scale):
    """Contrast of the text colour against the background right around the letters; reports the weakest tenth."""
    grown = mask.filter(ImageFilter.MaxFilter(5))
    ring = ImageChops.subtract(grown, mask)
    box = ring.getbbox()
    if not box:
        return {'layer': layer.get('id'), 'ratio': None}
    region = behind.crop(box).convert('RGB')
    ring = ring.crop(box)
    step = max(1, int(math.sqrt(region.width * region.height / 40000)))
    samples = [region.getpixel((x, y)) for y in range(0, region.height, step) for x in range(0, region.width, step) if ring.getpixel((x, y)) > 128]
    if not samples:
        return {'layer': layer.get('id'), 'ratio': None}
    ratios = sorted(contrast_ratio(fill, pixel) for pixel in samples)
    weakest = ratios[len(ratios) // 10]
    large = layout.final_size / scale >= 48 or (layout.final_size / scale >= 36 and layer.get('bold', False))
    need = float(layer.get('min_contrast', 3.0 if large else 4.5))
    return {'layer': layer.get('id'), 'ratio': round(weakest, 2), 'median': round(ratios[len(ratios) // 2], 2), 'needed': need, 'pass': weakest >= need}


def crop_marks(image, frame):
    """Adds a 10 mm slug with trim marks around the bleed."""
    slug = round(10 / MM_PER_INCH * frame['dpi'])
    W, H = image.size
    sheet = Image.new('RGBA', (W + 2 * slug, H + 2 * slug), (255, 255, 255, 255))
    sheet.paste(image, (slug, slug))
    draw = ImageDraw.Draw(sheet)
    bleed = frame['bleed_px']
    gap = round(2 / MM_PER_INCH * frame['dpi'])
    length = slug - gap
    width = max(1, round(0.25 / MM_PER_INCH * frame['dpi']))
    left, top = slug + bleed, slug + bleed
    right, bottom = left + frame['trim'][0], top + frame['trim'][1]
    for x in (left, right):
        draw.line([(x, 0), (x, length)], fill='black', width=width)
        draw.line([(x, sheet.height - length), (x, sheet.height)], fill='black', width=width)
    for y in (top, bottom):
        draw.line([(0, y), (length, y)], fill='black', width=width)
        draw.line([(sheet.width - length, y), (sheet.width, y)], fill='black', width=width)
    return sheet


def save(image, frame, spec, out, formats, icc):
    out.mkdir(parents=True, exist_ok=True)
    name = spec.get('id', 'design')
    rgb = image.convert('RGB')
    files = []
    dpi = (frame['dpi'], frame['dpi'])
    bleed = frame['bleed_px']
    trimmed = rgb.crop((bleed, bleed, bleed + frame['trim'][0], bleed + frame['trim'][1])) if bleed else rgb
    if 'png' in formats:
        path = out / f'{name}.png'
        trimmed.save(path, dpi=dpi, optimize=True)
        files.append({'file': path.name, 'size': list(trimmed.size), 'note': 'trim size, no bleed' if bleed else 'exact size'})
    if 'jpg' in formats:
        path = out / f'{name}.jpg'
        trimmed.save(path, dpi=dpi, quality=int(spec.get('jpg_quality', 92)), optimize=True, subsampling=0)
        files.append({'file': path.name, 'size': list(trimmed.size)})
    if 'pdf' in formats:
        page = crop_marks(image, frame).convert('RGB') if frame.get('crop_marks') else rgb
        note = 'RGB raster PDF'
        if icc:
            from PIL import ImageCms
            profile = ImageCms.getOpenProfile(str(icc))
            page = ImageCms.profileToProfile(page, ImageCms.createProfile('sRGB'), profile, outputMode='CMYK', renderingIntent=ImageCms.Intent.RELATIVE_COLORIMETRIC)
            note = f'CMYK raster PDF converted with {Path(icc).name}'
        path = out / f'{name}.pdf'
        page.save(path, resolution=frame['dpi'])
        files.append({'file': path.name, 'size': list(page.size), 'note': note + (f', {frame["bleed_mm"]} mm bleed' if bleed else '') + (', crop marks in a 10 mm slug' if frame.get('crop_marks') else '')})
    return files


def main(argv=None):
    parser = argparse.ArgumentParser(description='Compose a static graphic with exact text (PNG, JPG, print PDF).')
    parser.add_argument('spec', nargs='?')
    parser.add_argument('--out', default='.')
    parser.add_argument('--formats', default='png', help='comma list of png, jpg, pdf')
    parser.add_argument('--fonts', action='append', default=[], help='extra font folder (fonts.json or *.ttf/*.otf)')
    parser.add_argument('--icc', help='CMYK ICC profile for the PDF (for example the print shop\'s FOGRA39 or PSO Coated v3)')
    parser.add_argument('--allow-overflow', action='store_true', help='draw even when text does not fit (never for client finals)')
    parser.add_argument('--strict', action='store_true', help='contrast below the threshold is an error (exit 5)')
    parser.add_argument('--presets', action='store_true')
    parser.add_argument('--fonts-list', action='store_true')
    args = parser.parse_args(argv)
    if args.presets:
        print(json.dumps(PRESETS, indent=2, ensure_ascii=False))
        return 0
    if args.fonts_list:
        print('\n'.join(sorted(k for k in font_index(args.fonts) if ' ' in k)))
        return 0
    if not args.spec:
        parser.error('give a *.static.json spec')
    spec_path = Path(args.spec)
    summary = {'tool': 'static-render', 'version': VERSION, 'spec': spec_path.name}
    try:
        spec = json.loads(spec_path.read_text(encoding='utf-8'))
        image, frame, result = compose(spec, spec_path.parent, args.fonts, args.allow_overflow)
    except (SpecError, KeyError, ValueError, OSError) as error:
        summary.update(status='invalid_spec', detail=str(error))
        print(json.dumps(summary, ensure_ascii=False))
        return 3
    summary.update(result)
    if result['status'] != 'ok':
        print(json.dumps(summary, ensure_ascii=False))
        return 4
    summary['size'] = list(frame['trim'])
    if spec.get('print'):
        summary['print'] = {'trim_mm': frame['trim_mm'], 'bleed_mm': frame['bleed_mm'], 'dpi': frame['dpi']}
    formats = {f.strip() for f in args.formats.split(',') if f.strip()}
    summary['files'] = save(image, frame, spec, Path(args.out), formats, args.icc)
    weak = [c for c in result['contrast'] if c.get('pass') is False]
    summary['status'] = 'low_contrast' if weak and args.strict else 'ok'
    audit = Path(args.out) / f"{spec.get('id', 'design')}.audit.json"
    audit.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    summary['audit'] = audit.name
    print(json.dumps(summary, ensure_ascii=False))
    return 5 if summary['status'] == 'low_contrast' else 0


if __name__ == '__main__':
    sys.exit(main())
