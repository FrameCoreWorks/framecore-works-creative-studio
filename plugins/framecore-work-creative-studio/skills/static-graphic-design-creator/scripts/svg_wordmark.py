#!/usr/bin/env python3
"""Set a wordmark as outlined SVG paths from a bundled or supplied font: no live text, no embedded raster.

  python3 svg_wordmark.py --text "Fachowiec Bis" --font archivo/Archivo-Bold.ttf --colour "#1D3B2A" --out-dir logo/
  python3 svg_wordmark.py wordmark.json --out-dir logo/

wordmark.json:
  {"text": "Pasieka Lipa", "font": "fraunces/Fraunces-Black.ttf", "tracking": 10, "case": "upper", "language": "pl",
   "colour": "#1D3B2A", "background": "#F7F3EC",
   "tagline": {"text": "miód z Beskidów", "font": "inter/Inter-SemiBold.ttf", "scale": 0.32, "tracking": 120, "align": "center"}}

A font given as folder/file or file name is looked up in Studio's bundled OFL fonts (pipeline-core/assets/fonts); any
other path is a supplied font. Glyphs are the font's own outlines, spaced by its own kerning (GPOS pair kerning or a kern
table) plus tracking in thousandths of an em; "language": "pl" uses the font's Polish letterforms (locl) where it has
them. Every character must exist in the font: a missing glyph is an error, never a fallback box.

Writes wordmark.svg (colour), wordmark-black.svg and wordmark-white.svg, PNG renders of the three (wordmark.png,
wordmark-black.png, wordmark-white.png, 400 px high, transparent), wordmark-preview.png (on light and dark grounds, clear
space marked, small sizes for the minimum-size check) and wordmark.json (font, licence, hash, metrics, clear space,
kerning and substitutions used, and a readback of the SVG files). A wordmark set from a stock typeface is a starting
point: the letterforms are the font's, the licence is the font's, and distinctiveness or trademark clearance is not
established here. Needs fontTools and Pillow. Exit codes: 0 written, 2 bad input, a missing glyph, font or library,
or an output folder that exists.
"""
import argparse
import hashlib
import json
import math
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

FONTS = Path(__file__).resolve().parents[2] / 'pipeline-core/assets/fonts'
HEX = re.compile(r'^#[0-9A-Fa-f]{6}$')
CASES = ('as_is', 'upper', 'lower')
SVG_NS = 'http://www.w3.org/2000/svg'


class InputError(Exception):
    pass


def resolve_font(name):
    path = Path(str(name))
    if path.is_file():
        return path
    if (FONTS / path).is_file():
        return FONTS / path
    hits = sorted(FONTS.glob(f'*/{path.name}'))
    if len(hits) == 1:
        return hits[0]
    bundled = ', '.join(sorted(p.relative_to(FONTS).as_posix() for p in FONTS.glob('*/*.ttf')))
    raise InputError(f'font not found: {name} (bundled fonts: {bundled})')


def licence_of(path):
    if (path.parent / 'OFL.txt').is_file():
        return 'SIL Open Font License 1.1 (OFL.txt beside the font): logo use is allowed; the font itself may not be sold alone'
    return 'Unknown: no licence file beside the font; confirm the licence allows logo use before delivery'


def rgb(value):
    return tuple(int(value[i:i + 2], 16) for i in (1, 3, 5))


class Shaper:
    """cmap, Polish locl single substitutions and pair kerning, read with fontTools; nothing else is shaped."""

    def __init__(self, font, language=None):
        self.font = font
        self.cmap = font.getBestCmap()
        self.metrics = font['hmtx'].metrics
        self.substitutions = {}
        if language == 'pl':
            for lookup in self._feature_lookups('GSUB', 'locl', 'PLK '):
                for table in self._subtables(lookup, 7):
                    if lookup.LookupType in (1, 7) and hasattr(table, 'mapping'):
                        for source, target in table.mapping.items():
                            self.substitutions.setdefault(source, target)
        self.kern_lookups = [self._subtables(lookup, 9) for lookup in self._feature_lookups('GPOS', 'kern')]
        self.kern_table = {}
        if 'kern' in font:
            for table in font['kern'].kernTables:
                for pair, value in getattr(table, 'kernTable', {}).items():
                    self.kern_table.setdefault(pair, value)

    def _feature_lookups(self, tag, feature, language=None):
        if tag not in self.font:
            return []
        table = self.font[tag].table
        if not table.FeatureList or not table.LookupList:
            return []
        indices = []
        if language:
            for script in table.ScriptList.ScriptRecord:
                for record in script.Script.LangSysRecord:
                    if record.LangSysTag == language:
                        for i in record.LangSys.FeatureIndex:
                            feature_record = table.FeatureList.FeatureRecord[i]
                            if feature_record.FeatureTag == feature:
                                indices += feature_record.Feature.LookupListIndex
        else:
            for feature_record in table.FeatureList.FeatureRecord:
                if feature_record.FeatureTag == feature:
                    indices += feature_record.Feature.LookupListIndex
        return [table.LookupList.Lookup[i] for i in sorted(set(indices))]

    @staticmethod
    def _subtables(lookup, extension_type):
        if lookup.LookupType == extension_type:
            return [table.ExtSubTable for table in lookup.SubTable]
        return list(lookup.SubTable)

    def glyphs(self, text):
        names, missing, swapped = [], [], []
        for char in text:
            name = self.cmap.get(ord(char))
            if name is None:
                missing.append(char)
                continue
            if name in self.substitutions:
                swapped.append([char, name, self.substitutions[name]])
                name = self.substitutions[name]
            names.append(name)
        if missing:
            listed = ', '.join(f'{c!r} (U+{ord(c):04X})' for c in dict.fromkeys(missing))
            raise InputError(f'the font has no glyph for {listed}; choose a font that covers the text')
        return names, swapped

    def kerning(self, left, right):
        total = 0
        for subtables in self.kern_lookups:
            for table in subtables:
                if not hasattr(table, 'Coverage') or getattr(table, 'Format', None) not in (1, 2):
                    continue
                covered = table.Coverage.glyphs
                if left not in covered:
                    continue
                if table.Format == 1:
                    pairs = table.PairSet[covered.index(left)].PairValueRecord
                    record = next((r for r in pairs if r.SecondGlyph == right), None)
                    if record is None:
                        continue
                    total += getattr(record.Value1, 'XAdvance', 0) or 0 if record.Value1 else 0
                    break
                if table.Format == 2:
                    first = table.ClassDef1.classDefs.get(left, 0) if table.ClassDef1 else 0
                    second = table.ClassDef2.classDefs.get(right, 0) if table.ClassDef2 else 0
                    record = table.Class1Record[first].Class2Record[second]
                    total += getattr(record.Value1, 'XAdvance', 0) or 0 if record.Value1 else 0
                    break
        if not self.kern_lookups:
            total += self.kern_table.get((left, right), 0)
        return total


def set_line(font, text, tracking, language):
    """Glyph names with their x positions in font units, plus the kerning and substitutions used."""
    shaper = Shaper(font, language)
    names, swapped = shaper.glyphs(text)
    upm = font['head'].unitsPerEm
    x, placed, kerned = 0, [], []
    for i, name in enumerate(names):
        placed.append((name, x))
        x += shaper.metrics[name][0]
        if i + 1 < len(names):
            k = shaper.kerning(name, names[i + 1])
            if k:
                kerned.append([name, names[i + 1], k])
            x += k + tracking * upm / 1000
    return placed, x, kerned, swapped


def cap_height(font):
    value = getattr(font['OS/2'], 'sCapHeight', 0) if 'OS/2' in font else 0
    if value:
        return value
    from fontTools.pens.boundsPen import BoundsPen
    glyphset = font.getGlyphSet()
    pen = BoundsPen(glyphset)
    glyphset[font.getBestCmap()[ord('H')]].draw(pen)
    return pen.bounds[3]


class Line:
    """One set line: glyphs, the transform from font units to the shared drawing space, and its bounds."""

    def __init__(self, font, text, tracking, language, scale, x0, baseline):
        self.font, self.text = font, text
        self.glyphset = font.getGlyphSet()
        self.placed, self.advance, self.kerned, self.swapped = set_line(font, text, tracking, language)
        self.scale, self.x0, self.baseline = scale, x0, baseline

    def transform(self, x):
        return (self.scale, 0, 0, -self.scale, self.x0 + x * self.scale, self.baseline)

    def bounds(self):
        from fontTools.pens.boundsPen import BoundsPen
        from fontTools.pens.transformPen import TransformPen
        box = None
        for name, x in self.placed:
            pen = BoundsPen(self.glyphset)
            self.glyphset[name].draw(TransformPen(pen, self.transform(x)))
            if pen.bounds:
                b = pen.bounds
                box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3]))
        if box is None:
            raise InputError('the text has no visible glyphs')
        return box

    def path(self):
        from fontTools.pens.svgPathPen import SVGPathPen
        from fontTools.pens.transformPen import TransformPen
        pen = SVGPathPen(self.glyphset, ntos=lambda v: ('%.2f' % v).rstrip('0').rstrip('.'))
        for name, x in self.placed:
            self.glyphset[name].draw(TransformPen(pen, self.transform(x)))
        return pen.getCommands()

    def contours(self, scale, dx, dy, steps=10):
        from fontTools.pens.basePen import BasePen

        class Flatten(BasePen):
            def __init__(self, glyphset, matrix):
                super().__init__(glyphset)
                self.matrix, self.found, self.points = matrix, [], None

            def map(self, point):
                a, b, c, d, e, f = self.matrix
                return ((a * point[0] + c * point[1] + e) * scale + dx, (b * point[0] + d * point[1] + f) * scale + dy)

            def _moveTo(self, point):
                self.points = [self.map(point)]
                self.found.append(self.points)

            def _lineTo(self, point):
                self.points.append(self.map(point))

            def _curveToOne(self, p1, p2, p3):
                p0 = self._getCurrentPoint()
                for i in range(1, steps + 1):
                    t = i / steps
                    u = 1 - t
                    self.points.append(self.map((u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
                                                 u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])))

            def _qCurveToOne(self, p1, p2):
                p0 = self._getCurrentPoint()
                for i in range(1, steps + 1):
                    t = i / steps
                    u = 1 - t
                    self.points.append(self.map((u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0], u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1])))

            def _closePath(self):
                self.points = None

            def _endPath(self):
                self.points = None

        out = []
        for name, x in self.placed:
            pen = Flatten(self.glyphset, self.transform(x))
            self.glyphset[name].draw(pen)
            out += [c for c in pen.found if len(c) > 2]
        return out


def rasterize(contours, size, Image):
    """Nonzero-winding scanline fill (the TrueType rule) of flattened contours into an L mask; self-intersecting and
    overlapping contours, common in fonts made from variable masters, fill correctly."""
    width, height = size
    edges = []
    for points in contours:
        for i in range(len(points)):
            (x0, y0), (x1, y1) = points[i - 1], points[i]
            if y0 == y1:
                continue
            direction = 1 if y1 > y0 else -1
            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            edges.append((y0, y1, x0, (x1 - x0) / (y1 - y0), direction))
    edges.sort()
    buffer = bytearray(width * height)
    active, k = [], 0
    for row in range(height):
        centre = row + 0.5
        while k < len(edges) and edges[k][0] <= centre:
            active.append(edges[k])
            k += 1
        active = [e for e in active if e[1] > centre]
        crossings = sorted((e[2] + (centre - e[0]) * e[3], e[4]) for e in active)
        winding, start = 0, 0.0
        for x, direction in crossings:
            before, winding = winding, winding + direction
            if before == 0 and winding != 0:
                start = x
            elif before != 0 and winding == 0:
                a, b = max(0, math.ceil(start - 0.5)), min(width, math.ceil(x - 0.5))
                if b > a:
                    buffer[row * width + a:row * width + b] = b'\xff' * (b - a)
    return Image.frombytes('L', size, bytes(buffer))


def load_spec(args):
    spec = {}
    if args.spec:
        spec = json.loads(Path(args.spec).read_text(encoding='utf-8'))
        if not isinstance(spec, dict):
            raise InputError('the wordmark spec must be a JSON object')
    for key in ('text', 'font', 'tracking', 'case', 'language', 'colour', 'background'):
        value = getattr(args, key)
        if value is not None:
            spec[key] = value
    if not str(spec.get('text', '')).strip():
        raise InputError('the wordmark needs its text (--text or "text")')
    if not spec.get('font'):
        raise InputError('name a font (--font or "font"), for example archivo/Archivo-Bold.ttf')
    spec.setdefault('tracking', 0)
    spec.setdefault('case', 'as_is')
    spec.setdefault('colour', '#1A1A1A')
    spec.setdefault('background', '#FFFFFF')
    if spec['case'] not in CASES:
        raise InputError(f"case must be one of {', '.join(CASES)}")
    for key in ('colour', 'background'):
        if not HEX.match(str(spec[key])):
            raise InputError(f'{key} must be a #RRGGBB colour')
    tagline = spec.get('tagline')
    if tagline is not None:
        if not isinstance(tagline, dict) or not str(tagline.get('text', '')).strip():
            raise InputError('a tagline needs its text')
        tagline.setdefault('font', spec['font'])
        tagline.setdefault('scale', 0.32)
        tagline.setdefault('tracking', 80)
        tagline.setdefault('align', 'center')
        if tagline['align'] not in ('center', 'left') or not 0.1 <= float(tagline['scale']) <= 1:
            raise InputError('tagline align must be center or left and scale between 0.1 and 1')
    return spec


def cased(text, case):
    return text.upper() if case == 'upper' else text.lower() if case == 'lower' else text


def svg_document(paths, box, colour, title):
    x0, y0, x1, y1 = box
    width, height = x1 - x0, y1 - y0
    fmt = lambda v: ('%.2f' % v).rstrip('0').rstrip('.')
    body = ''.join(f'<path fill="{colour}" d="{d}"/>' for d in paths)
    safe = title.replace('&', '&amp;').replace('<', '&lt;').replace('"', '&quot;')
    return (f'<svg xmlns="{SVG_NS}" viewBox="{fmt(x0)} {fmt(y0)} {fmt(width)} {fmt(height)}" '
            f'width="{fmt(width / height * 200)}" height="200" role="img" aria-label="{safe}"><title>{safe}</title>{body}</svg>\n')


def readback(path):
    """Parse a written SVG and report what a print shop would check: outlines only, no text, raster or links."""
    root = ET.parse(path).getroot()
    tags = [element.tag.split('}')[-1] for element in root.iter()]
    links = [k for element in root.iter() for k in element.attrib if k.endswith('href')]
    return {'paths': tags.count('path'), 'live_text': 'text' in tags or 'tspan' in tags, 'embedded_raster': 'image' in tags,
            'external_references': bool(links), 'viewBox': root.attrib.get('viewBox')}


def main(argv=None):
    parser = argparse.ArgumentParser(description='Set a wordmark as outlined SVG paths with renders, a preview and a report.')
    parser.add_argument('spec', nargs='?', help='wordmark JSON (options given on the command line override it)')
    parser.add_argument('--text')
    parser.add_argument('--font')
    parser.add_argument('--tracking', type=float, help='extra space between letters in thousandths of an em')
    parser.add_argument('--case', choices=CASES)
    parser.add_argument('--language', choices=['pl'], help="use the font's Polish letterforms where it has them")
    parser.add_argument('--colour')
    parser.add_argument('--background', help='light ground for the preview (#RRGGBB)')
    parser.add_argument('--out-dir', required=True)
    args = parser.parse_args(argv)
    try:
        try:
            from fontTools.ttLib import TTFont
            from PIL import Image, ImageDraw, ImageFont
        except ImportError as error:
            raise InputError(f'the wordmark tool needs fontTools and Pillow ({error.name} is missing): python3 -m pip install fonttools pillow')
        spec = load_spec(args)
        out = Path(args.out_dir)
        if out.exists():
            raise InputError(f'output folder exists: {out}')
        font_path = resolve_font(spec['font'])
        font = TTFont(str(font_path))
        upm = font['head'].unitsPerEm
        text = cased(str(spec['text']).strip(), spec['case'])
        main_line = Line(font, text, float(spec['tracking']), spec.get('language'), 1.0, 0, 0)
        cap = cap_height(font)
        lines, report_tagline = [main_line], None
        box = main_line.bounds()
        tagline = spec.get('tagline')
        if tagline:
            t_path = resolve_font(tagline['font'])
            t_font = font if t_path == font_path else TTFont(str(t_path))
            t_scale = float(tagline['scale']) * cap / cap_height(t_font)
            t_text = cased(str(tagline['text']).strip(), spec['case'] if tagline.get('case') is None else tagline['case'])
            probe = Line(t_font, t_text, float(tagline['tracking']), spec.get('language'), t_scale, 0, 0)
            t_box = probe.bounds()
            gap = 0.5 * cap
            baseline = box[3] + gap + (-t_box[1])
            x0 = box[0] - t_box[0] if tagline['align'] == 'left' else (box[0] + box[2]) / 2 - (t_box[0] + t_box[2]) / 2
            t_line = Line(t_font, t_text, float(tagline['tracking']), spec.get('language'), t_scale, x0, baseline)
            lines.append(t_line)
            t_bounds = t_line.bounds()
            box = (min(box[0], t_bounds[0]), min(box[1], t_bounds[1]), max(box[2], t_bounds[2]), max(box[3], t_bounds[3]))
            report_tagline = {'text': t_text, 'font': t_path.name, 'font_sha256': hashlib.sha256(t_path.read_bytes()).hexdigest(),
                              'licence': licence_of(t_path), 'kerning_pairs': len(t_line.kerned), 'polish_letterforms': t_line.swapped}
        paths = [line.path() for line in lines]
        title = text + (f" - {report_tagline['text']}" if report_tagline else '')
        variants = {'wordmark': spec['colour'], 'wordmark-black': '#000000', 'wordmark-white': '#FFFFFF'}

        # Renders: supersampled nonzero fill of the same outlines the SVG holds.
        height = box[3] - box[1]

        def render(target_h, colour, ground=None, ss=4):
            scale = target_h * ss / height
            w = max(1, math.ceil((box[2] - box[0]) * scale))
            h = max(1, math.ceil(height * scale))
            contours = [c for line in lines for c in line.contours(scale, -box[0] * scale, -box[1] * scale)]
            mask = rasterize(contours, (w, h), Image).resize((max(1, round(w / ss)), max(1, round(h / ss))), Image.LANCZOS)
            image = Image.new('RGBA', mask.size, (*rgb(ground), 255) if ground else (0, 0, 0, 0))
            ink = Image.new('RGBA', mask.size, (*rgb(colour), 255))
            image.paste(ink, (0, 0), mask)
            return image, mask

        out.mkdir(parents=True)
        files = []
        for stem, colour in variants.items():
            (out / f'{stem}.svg').write_text(svg_document(paths, box, colour, title), encoding='utf-8')
            image, _ = render(400, colour)
            image.save(out / f'{stem}.png')
            files += [f'{stem}.svg', f'{stem}.png']

        # Preview sheet: light and dark grounds with clear space, then small sizes.
        try:
            label = ImageFont.truetype(str(FONTS / 'inter/Inter-Regular.ttf'), 22)
        except OSError:
            label = ImageFont.load_default()
        large, _ = render(160, spec['colour'])
        reverse, _ = render(160, '#FFFFFF')
        clear = cap * 160 / height
        pad = 40
        tile_w, tile_h = int(large.width + 2 * clear + 2 * pad), int(large.height + 2 * clear + 2 * pad)
        smalls = [(px, render(px, spec['colour'])[0]) for px in (16, 24, 32, 48)]
        sheet_w = max(2 * tile_w + 3 * pad, sum(i.width for _, i in smalls) + pad * (len(smalls) + 1))
        sheet = Image.new('RGB', (sheet_w, tile_h + 220), (236, 236, 236))
        draw = ImageDraw.Draw(sheet)
        dark = rgb(spec['colour']) if sum(rgb(spec['colour'])) < 300 else (26, 26, 26)
        for k, (art, ground) in enumerate(((large, rgb(spec['background'])), (reverse, dark))):
            x, y = pad + k * (tile_w + pad), pad
            draw.rectangle([x, y, x + tile_w, y + tile_h], fill=ground)
            ax, ay = int(x + pad + clear), int(y + pad + clear)
            sheet.paste(art, (ax, ay), art)
            line_colour = (200, 60, 60) if k == 0 else (255, 150, 150)
            box_xy = [ax - clear, ay - clear, ax + art.width + clear, ay + art.height + clear]
            for i in range(int(box_xy[0]), int(box_xy[2]), 12):
                draw.line([(i, box_xy[1]), (min(i + 6, box_xy[2]), box_xy[1])], fill=line_colour, width=2)
                draw.line([(i, box_xy[3]), (min(i + 6, box_xy[2]), box_xy[3])], fill=line_colour, width=2)
            for j in range(int(box_xy[1]), int(box_xy[3]), 12):
                draw.line([(box_xy[0], j), (box_xy[0], min(j + 6, box_xy[3]))], fill=line_colour, width=2)
                draw.line([(box_xy[2], j), (box_xy[2], min(j + 6, box_xy[3]))], fill=line_colour, width=2)
        y = tile_h + 2 * pad
        draw.text((pad, y - 34), 'Clear space (dashed): the cap height on every side. Small sizes, wordmark height in px:', font=label, fill=(60, 60, 60))
        x = pad
        for px, art in smalls:
            sheet.paste(art, (x, y + 10), art)
            draw.text((x, y + 10 + art.height + 8), f'{px} px', font=label, fill=(90, 90, 90))
            x += art.width + pad
        sheet.save(out / 'wordmark-preview.png')
        files.append('wordmark-preview.png')

        name = font['name']
        report = {
            'text': text, 'case': spec['case'], 'language': spec.get('language'),
            'font': {'file': font_path.name, 'bundled': FONTS in font_path.parents, 'family': name.getDebugName(16) or name.getDebugName(1),
                     'style': name.getDebugName(17) or name.getDebugName(2), 'version': name.getDebugName(5),
                     'sha256': hashlib.sha256(font_path.read_bytes()).hexdigest(), 'licence': licence_of(font_path)},
            'tracking_per_mille_em': float(spec['tracking']), 'units_per_em': upm,
            'kerning_pairs': main_line.kerned, 'polish_letterforms': main_line.swapped,
            'ligatures_and_other_features': 'not applied: glyphs are set one per character with pair kerning only',
            'tagline': report_tagline,
            'bounds_font_units': [round(v, 2) for v in box], 'cap_height_font_units': cap,
            'clear_space': {'unit': 'cap height', 'font_units': cap, 'share_of_wordmark_height': round(cap / height, 3)},
            'minimum_size': 'proposed only: judge the 16, 24, 32 and 48 px renders on the preview at the real sizes and contexts',
            'colours': variants, 'files': files,
            'svg_readback': {stem: readback(out / f'{stem}.svg') for stem in variants},
            'scope': 'outlined vector geometry from the font; not a trademark search, not a custom drawing, not print-verified',
        }
        bad = [stem for stem, r in report['svg_readback'].items() if r['live_text'] or r['embedded_raster'] or r['external_references'] or not r['paths']]
        if bad:
            raise InputError(f'readback failed for {bad}')
        (out / 'wordmark.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    except (OSError, ValueError, KeyError, InputError) as error:
        sys.stderr.write(f'{error}\n')
        return 2
    print(json.dumps({'out_dir': str(out), 'files': files + ['wordmark.json'], 'kerning_pairs': len(main_line.kerned),
                      'polish_letterforms': len(main_line.swapped)}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
