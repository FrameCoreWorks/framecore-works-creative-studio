"""SVG wordmark (static-graphic-design-creator/scripts/svg_wordmark.py): outlined paths, the font's kerning, Polish
letterforms, a nonzero fill that matches the font rasterizer, honest errors."""
import importlib.util
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
TOOL = PLUGIN / 'skills/static-graphic-design-creator/scripts/svg_wordmark.py'
READY = all(importlib.util.find_spec(name) is not None for name in ('fontTools', 'PIL'))
spec = importlib.util.spec_from_file_location('svg_wordmark', TOOL)
svg_wordmark = importlib.util.module_from_spec(spec)
spec.loader.exec_module(svg_wordmark)


def run(*args):
    done = subprocess.run([sys.executable, '-B', str(TOOL), *args], capture_output=True, text=True, timeout=180)
    return done.returncode, done.stdout, done.stderr


@unittest.skipUnless(READY, 'fontTools and Pillow are needed (python3 -m pip install fonttools pillow)')
class Wordmark(unittest.TestCase):
    def test_transparent_white_edges_store_unpremultiplied_rgb(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as temp:
            out = pathlib.Path(temp, 'logo')
            code, _, err = run('--text', 'Frame', '--font', 'inter/Inter-Bold.ttf', '--out-dir', str(out))
            self.assertEqual(code, 0, err)
            with Image.open(out / 'wordmark-white.png') as image:
                edges = [pixel for pixel in image.getdata() if 0 < pixel[3] < 255]
                self.assertTrue(edges)
                self.assertTrue(all(pixel[:3] == (255, 255, 255) for pixel in edges))
                black = Image.new('RGBA', image.size, 'black')
                black.alpha_composite(image)
                for pixel, composed in zip(image.getdata(), black.getdata()):
                    if 0 < pixel[3] < 255:
                        self.assertEqual(composed[:3], (pixel[3],) * 3)

    def test_outlined_svg_files_renders_preview_and_report(self):
        with tempfile.TemporaryDirectory() as temp:
            spec_file = pathlib.Path(temp, 'wordmark.json')
            spec_file.write_text(json.dumps({'text': 'Pasieka Lipa', 'font': 'fraunces/Fraunces-Black.ttf', 'case': 'upper', 'colour': '#1D3B2A',
                                             'tagline': {'text': 'miód z Beskidów', 'font': 'inter/Inter-SemiBold.ttf'}}, ensure_ascii=False), encoding='utf-8')
            out = pathlib.Path(temp, 'logo')
            code, stdout, err = run(str(spec_file), '--out-dir', str(out))
            self.assertEqual(code, 0, err)
            for stem in ('wordmark', 'wordmark-black', 'wordmark-white'):
                root = ET.parse(out / f'{stem}.svg').getroot()
                tags = {element.tag.split('}')[-1] for element in root.iter()}
                self.assertTrue({'svg', 'path', 'title'} >= tags, tags)
                self.assertTrue((out / f'{stem}.png').is_file())
            colours = {p.attrib['fill'] for p in ET.parse(out / 'wordmark.svg').getroot().iter('{http://www.w3.org/2000/svg}path')}
            self.assertEqual(colours, {'#1D3B2A'})
            report = json.loads((out / 'wordmark.json').read_text(encoding='utf-8'))
            self.assertEqual(report['text'], 'PASIEKA LIPA')
            self.assertEqual(report['tagline']['text'], 'MIÓD Z BESKIDÓW')
            self.assertIn('Open Font License', report['font']['licence'])
            self.assertFalse(any(r['live_text'] or r['embedded_raster'] or r['external_references'] for r in report['svg_readback'].values()))
            self.assertEqual(report['clear_space']['unit'], 'cap height')
            from PIL import Image
            with Image.open(out / 'wordmark.png') as image:
                self.assertEqual(image.height, 400)
                self.assertGreater(sum(1 for a in image.getchannel('A').getdata() if a > 128), 1000)
            self.assertTrue((out / 'wordmark-preview.png').is_file())

    def test_kerning_and_advance_match_harfbuzz_where_pillow_has_raqm(self):
        from fontTools.ttLib import TTFont
        from PIL import ImageFont, features
        for name, text in (('inter/Inter-Bold.ttf', 'AVATAR Tywa'), ('archivo/Archivo-Bold.ttf', 'AV To'), ('sourceserif4/SourceSerif4-Bold.ttf', 'Yves Tower')):
            path = svg_wordmark.resolve_font(name)
            font = TTFont(str(path))
            placed, advance, kerned, _ = svg_wordmark.set_line(font, text, 0, None)
            self.assertTrue(kerned, name)
            if features.check('raqm'):
                upm = font['head'].unitsPerEm
                shaped = ImageFont.truetype(str(path), 1000, layout_engine=ImageFont.Layout.RAQM).getlength(text)
                self.assertAlmostEqual(advance * 1000 / upm, shaped, delta=1.0, msg=name)

    def test_nonzero_fill_matches_the_font_rasterizer_including_self_intersecting_glyphs(self):
        from fontTools.ttLib import TTFont
        from PIL import Image, ImageDraw, ImageFont, features
        for name, text in (('inter/Inter-Bold.ttf', 'Bóbr 08 &%'), ('fraunces/Fraunces-Black.ttf', 'Żółć gęślą'), ('anton/Anton-Regular.ttf', 'ŁÓDŹ 2026')):
            path = svg_wordmark.resolve_font(name)
            font = TTFont(str(path))
            line = svg_wordmark.Line(font, text, 0, None, 1.0, 0, 0)
            ascent, scale = font['hhea'].ascent, 200 / font['head'].unitsPerEm
            size = (int(line.advance * scale) + 40, int((ascent - font['hhea'].descent) * scale) + 40)
            ours = svg_wordmark.rasterize(line.contours(scale, 20, 20 + ascent * scale), size, Image)
            reference = Image.new('L', size, 0)
            drawing = ImageDraw.Draw(reference)
            raster_font = ImageFont.truetype(str(path), 200)
            if features.check('raqm'):
                drawing.text((20, 20 + ascent * scale), text, font=raster_font, fill=255, anchor='ls')
            else:
                # BASIC layout cannot supply the GPOS kerning being compared. Keep this
                # raster/contour test at the same glyph positions; the shaping test above
                # independently compares full-line advances when HarfBuzz is available.
                for char, (_, position) in zip(text, line.placed):
                    drawing.text((20 + position * scale, 20 + ascent * scale), char,
                                 font=raster_font, fill=255, anchor='ls')
            a = [v > 127 for v in ours.getdata()]
            b = [v > 127 for v in reference.getdata()]
            union = sum(1 for x, y in zip(a, b) if x or y)
            self.assertGreater(sum(1 for x, y in zip(a, b) if x and y) / union, 0.95, name)

    def test_polish_letterforms_and_tracking(self):
        from fontTools.ttLib import TTFont
        font = TTFont(str(svg_wordmark.resolve_font('archivo/Archivo-Regular.ttf')))
        _, _, _, swapped = svg_wordmark.set_line(font, 'Łódź Śródmieście', 0, 'pl')
        self.assertIn('ó', [s[0] for s in swapped])
        self.assertEqual(svg_wordmark.set_line(font, 'Łódź', 0, None)[3], [])
        narrow = svg_wordmark.set_line(font, 'Łódź', 0, None)[1]
        wide = svg_wordmark.set_line(font, 'Łódź', 100, None)[1]
        self.assertAlmostEqual(wide - narrow, 3 * 100 * font['head'].unitsPerEm / 1000)

    def test_missing_glyph_existing_folder_and_bad_input_fail_clearly(self):
        with tempfile.TemporaryDirectory() as temp:
            code, _, err = run('--text', 'Kawa ☕', '--font', 'inter/Inter-Bold.ttf', '--out-dir', str(pathlib.Path(temp, 'a')))
            self.assertEqual(code, 2)
            self.assertIn('U+2615', err)
            pathlib.Path(temp, 'b').mkdir()
            code, _, err = run('--text', 'Kawa', '--font', 'inter/Inter-Bold.ttf', '--out-dir', str(pathlib.Path(temp, 'b')))
            self.assertEqual(code, 2)
            self.assertIn('exists', err)
            code, _, err = run('--text', 'Kawa', '--font', 'nope.ttf', '--out-dir', str(pathlib.Path(temp, 'c')))
            self.assertEqual(code, 2)
            self.assertIn('bundled fonts', err)
            code, _, err = run('--text', 'Kawa', '--font', 'inter/Inter-Bold.ttf', '--colour', 'green', '--out-dir', str(pathlib.Path(temp, 'd')))
            self.assertEqual(code, 2)


if __name__ == '__main__':
    unittest.main()
