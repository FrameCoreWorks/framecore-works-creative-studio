#!/usr/bin/env python3
"""Measure an actual raster output before review: size and ratio against the placement, effective resolution for
print, transparency, sharpness, and previews a reviewer should look at (phone width, thumbnail, greyscale, safe area).

  python3 image_probe.py poster.png --preset a3 --previews review/
  python3 image_probe.py post.jpg --preset instagram-feed-portrait --copy "Miód lipowy z pasieki" --previews review/
  python3 image_probe.py render.png --size 1080x1920 --json
  python3 image_probe.py reference.jpg --analyze --json     # measured palette, tones and subject position for a reconstruction

It reads the image and writes previews; it never edits the image. With --copy it compares the visible text with the
locked copy through OCR when pytesseract and the tesseract program are installed, and says "not_run" otherwise; OCR
misreads stylised lettering, so a mismatch is a reason to look, and a match does not replace reading the image.
Exit codes: 0 measured, 1 a size, ratio or resolution problem, 3 bad input. Presets come from the static compositor.
"""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageStat

HERE = Path(__file__).resolve().parent
PRESETS = json.loads((HERE.parents[1] / 'static-graphic-design-creator/assets/static-render/presets.json').read_text(encoding='utf-8'))
MM_PER_INCH = 25.4


def ratio_name(w, h):
    from math import gcd
    g = gcd(w, h)
    return f'{w // g}:{h // g}'


def nearest_presets(w, h):
    found = []
    for name, item in PRESETS['sizes'].items():
        pw, ph = item.get('px') or item['mm']
        diff = abs((w / h) / (pw / ph) - 1)
        if diff <= 0.01:
            found.append(name)
    return found


def sharpness(image):
    """Mean edge strength of a 512 px greyscale copy: a relative number for comparing versions, not an absolute grade."""
    grey = ImageOps.grayscale(image)
    grey.thumbnail((512, 512))
    return round(ImageStat.Stat(grey.filter(ImageFilter.FIND_EDGES)).mean[0], 2)


def normalise(text):
    text = unicodedata.normalize('NFC', text).lower()
    # Numbers keep their sign, decimals and per cent (-50%, 99,99), so a dropped sign or digit is a missing word.
    return re.findall(r'[-−]?\d+(?:[.,]\d+)?%?|[^\W\d_]+', text.replace('\u00a0', ' '))


def ocr_compare(image, copy):
    try:
        import pytesseract
        seen = pytesseract.image_to_string(image.convert('RGB'), lang='pol+eng')
    except Exception as error:  # missing module, program or language data
        return {'status': 'not_run', 'reason': str(error).splitlines()[0][:160] if str(error) else type(error).__name__}
    want, got = normalise(copy), normalise(seen)
    from collections import Counter
    have = Counter(got)
    missing = []
    for w in want:                      # each occurrence counts: a repeated word must appear as often
        if have[w] > 0:
            have[w] -= 1
        else:
            missing.append(w)
    extra = [w for w in got if w not in want and len(w) > 2]
    return {'status': 'match' if not missing else 'mismatch', 'missing_words': missing, 'unexpected_words': extra[:20], 'ocr_text': seen.strip()[:500]}


def percentile(histogram, share):
    total, running = sum(histogram), 0
    for value, count in enumerate(histogram):
        running += count
        if running >= share * total:
            return value
    return 255


def analyze(image):
    """Measured facts for reconstructing an image in a prompt: the dominant colour fields with their share, the tonal
    range, and (on a plain background) where the subject sits. Figures describe the stored file, not the scene's true
    colours: light, the colour profile and compression shape them, so a reconstruction gives colours roles."""
    rgb = image.convert('RGB')
    small = rgb.copy()
    small.thumbnail((256, 256))
    quantized = small.quantize(colors=8, method=Image.Quantize.MEDIANCUT)
    palette, counts = quantized.getpalette(), sorted(quantized.getcolors(), reverse=True)
    total = sum(c for c, _ in counts)
    colours = [{'hex': '#{:02X}{:02X}{:02X}'.format(*palette[i * 3:i * 3 + 3]), 'share': round(c / total, 3)} for c, i in counts if c / total >= 0.01]
    grey = ImageOps.grayscale(small).histogram()
    p = {k: percentile(grey, v) for k, v in (('p01', 0.01), ('p05', 0.05), ('p50', 0.5), ('p95', 0.95), ('p99', 0.99))}
    pixels = sum(grey)
    tones = {**p, 'contrast_p05_p95': p['p95'] - p['p05'], 'shadows_clipped': round(sum(grey[:4]) / pixels, 3),
             'highlights_clipped': round(sum(grey[252:]) / pixels, 3),
             'key': 'low' if p['p50'] < 85 else 'high' if p['p50'] > 170 else 'middle'}
    result = {'palette': colours, 'tones': tones, 'colour_basis': 'stored RGB values' + (' with an embedded ICC profile' if image.info.get('icc_profile') else ', no colour profile: interpret as sRGB, Unknown otherwise')}
    # Subject position, only where the border is one plain colour (studio, poster field): x from the left, y from the top.
    w, h = small.size
    band = max(1, min(w, h) // 50)
    border = [small.getpixel((x, y)) for x in range(w) for y in (*range(band), *range(h - band, h))] + \
             [small.getpixel((x, y)) for y in range(h) for x in (*range(band), *range(w - band, w))]
    median = tuple(sorted(c[i] for c in border)[len(border) // 2] for i in range(3))
    spread = sum(1 for c in border if max(abs(c[i] - median[i]) for i in range(3)) > 24) / len(border)
    if spread > 0.1:
        result['subject'] = {'status': 'not_measured', 'reason': 'the border is not one plain colour; place the subject by eye and say the position is approximate'}
        return result
    mask = [[max(abs(small.getpixel((x, y))[i] - median[i]) for i in range(3)) > 40 for x in range(w)] for y in range(h)]
    points = [(x, y) for y in range(h) for x in range(w) if mask[y][x]]
    if not points or len(points) / (w * h) < 0.005:
        result['subject'] = {'status': 'not_measured', 'reason': 'nothing stands out from the plain background'}
        return result
    xs, ys = [x for x, _ in points], [y for _, y in points]
    cx, cy = sum(xs) / len(xs) / w, sum(ys) / len(ys) / h
    thirds = min(((a, b) for a in (1 / 3, 2 / 3) for b in (1 / 3, 2 / 3)), key=lambda t: (t[0] - cx) ** 2 + (t[1] - cy) ** 2)
    result['subject'] = {'status': 'measured', 'background_hex': '#{:02X}{:02X}{:02X}'.format(*median),
                         'box_percent': {'left': round(100 * min(xs) / w), 'top': round(100 * min(ys) / h), 'right': round(100 * (max(xs) + 1) / w), 'bottom': round(100 * (max(ys) + 1) / h)},
                         'centre_percent': {'x': round(100 * cx), 'y': round(100 * cy)}, 'area_share': round(len(points) / (w * h), 3),
                         'nearest_third': {'x': round(100 * thirds[0]), 'y': round(100 * thirds[1])},
                         'note': 'everything that differs from the background, taken together; separate objects are placed by eye'}
    return result


def probe(path, args):
    image = Image.open(path)
    image.load()
    w, h = image.size
    report = {'file': Path(path).name, 'size': [w, h], 'ratio': ratio_name(w, h), 'mode': image.mode, 'format': image.format,
              'dpi_tag': [round(v) for v in image.info['dpi']] if 'dpi' in image.info else None, 'problems': [], 'notes': []}
    alpha = image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info)
    if alpha:
        lowest = image.convert('RGBA').getchannel('A').getextrema()[0]
        report['transparency'] = 'used' if lowest < 255 else 'channel present, fully opaque'
    else:
        report['transparency'] = 'none'
    report['icc_profile'] = bool(image.info.get('icc_profile'))
    report['sharpness'] = sharpness(image)
    report['matching_presets'] = nearest_presets(w, h)
    target = None
    if args.preset:
        item = PRESETS['sizes'].get(args.preset)
        if not item:
            raise ValueError(f'unknown preset {args.preset}')
        target = item
    if args.size:
        tw, th = (int(v) for v in args.size.lower().split('x'))
        target = {'px': [tw, th]}
    if args.print_mm:
        tw, th = (float(v) for v in args.print_mm.lower().split('x'))
        target = {'mm': [tw, th], 'dpi': args.dpi}
    if target and 'px' in target:
        tw, th = target['px']
        if (w, h) != (tw, th):
            if abs((w / h) / (tw / th) - 1) > 0.005:
                report['problems'].append(f'ratio {report["ratio"]} does not match the target {ratio_name(tw, th)} ({tw} x {th}); the placement will crop or letterbox it')
            elif w < tw:
                report['problems'].append(f'{w} x {h} is smaller than the target {tw} x {th}; it will be enlarged')
            else:
                report['notes'].append(f'{w} x {h} has the target ratio; export at {tw} x {th}')
        report['target'] = {'px': [tw, th]}
    if target and 'mm' in target:
        tw, th = target['mm']
        bleed = args.bleed_mm
        need = args.dpi or target.get('dpi') or PRESETS['print_defaults']['dpi']
        full = (tw + 2 * bleed, th + 2 * bleed)
        ppi = min(w / (full[0] / MM_PER_INCH), h / (full[1] / MM_PER_INCH))
        report['target'] = {'mm': [tw, th], 'bleed_mm': bleed, 'needed_ppi': need}
        report['effective_ppi'] = round(ppi)
        if abs((w / h) / (full[0] / full[1]) - 1) > 0.01:
            report['problems'].append(f'ratio {w / h:.3f} does not match {full[0]:g} x {full[1]:g} mm' + (' with bleed' if bleed else '') + f' ({full[0] / full[1]:.3f})')
        if ppi < need * 0.95:
            report['problems'].append(f'effective {ppi:.0f} ppi at {full[0]:g} x {full[1]:g} mm, below the {need} ppi this print needs')
        if image.mode == 'CMYK':
            report['notes'].append('CMYK image: check the profile with the print shop')
        else:
            report['notes'].append('RGB image: the print shop converts to CMYK unless a profile conversion was agreed')
    if args.copy:
        report['ocr'] = ocr_compare(image, args.copy)
    if getattr(args, 'analyze', False):
        report['analysis'] = analyze(image)
    if args.previews:
        out = Path(args.previews)
        out.mkdir(parents=True, exist_ok=True)
        stem = Path(path).stem
        rgb = image.convert('RGB')
        previews = []
        for label, width in (('phone', 360), ('thumb', 120)):
            small = rgb.copy()
            small.thumbnail((width, width * h // max(w, 1) + 1), Image.LANCZOS)
            target_path = out / f'{stem}-{label}.png'
            small.save(target_path)
            previews.append(target_path.name)
        grey = ImageOps.grayscale(rgb)
        grey.thumbnail((720, 720 * h // max(w, 1) + 1))
        grey.save(out / f'{stem}-grey.png')
        previews.append(f'{stem}-grey.png')
        area = (target or {}).get('safe_area')
        if area:
            sheet = rgb.copy()
            draw = ImageDraw.Draw(sheet, 'RGBA')
            box = (w * area.get('sides', 0), h * area.get('top', 0), w * (1 - area.get('sides', 0)), h * (1 - area.get('bottom', 0)))
            for zone in ((0, 0, w, box[1]), (0, box[3], w, h), (0, box[1], box[0], box[3]), (box[2], box[1], w, box[3])):
                draw.rectangle(zone, fill=(255, 0, 80, 70))
            draw.rectangle(box, outline=(255, 0, 80, 255), width=max(2, w // 300))
            sheet.thumbnail((720, 720 * h // max(w, 1) + 1))
            sheet.save(out / f'{stem}-safe.png')
            previews.append(f'{stem}-safe.png')
        report['previews'] = previews
        report['notes'].append('Look at the previews: the phone and thumbnail sizes show whether the message reads at a glance; the greyscale shows value contrast')
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description='Measure a raster output for review; never edits it.')
    parser.add_argument('images', nargs='+')
    parser.add_argument('--preset', help='a static compositor preset name (see compose.py --presets)')
    parser.add_argument('--size', help='target pixels, for example 1080x1350')
    parser.add_argument('--print-mm', help='target print size in millimetres, for example 297x420')
    parser.add_argument('--bleed-mm', type=float, default=0.0, help='bleed included in the image, per side')
    parser.add_argument('--dpi', type=int, help='resolution the print needs (default from the preset or 300)')
    parser.add_argument('--copy', help='the locked visible text, for an OCR comparison when OCR is installed')
    parser.add_argument('--previews', help='folder for phone, thumbnail, greyscale and safe-area previews')
    parser.add_argument('--analyze', action='store_true', help='measured palette, tones and subject position, for reconstructing the image in a prompt')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args(argv)
    reports, code = [], 0
    for path in args.images:
        try:
            report = probe(path, args)
        except (OSError, ValueError) as error:
            print(json.dumps({'file': path, 'error': str(error)}), file=sys.stderr)
            return 3
        reports.append(report)
        if report['problems'] or (report.get('ocr') or {}).get('status') == 'mismatch':
            code = 1
    if args.json:
        print(json.dumps(reports if len(reports) > 1 else reports[0], indent=2, ensure_ascii=False))
    else:
        for r in reports:
            line = f"{r['file']}: {r['size'][0]} x {r['size'][1]} ({r['ratio']}), {r['mode']}, transparency {r['transparency']}, sharpness {r['sharpness']}"
            if 'effective_ppi' in r:
                line += f", {r['effective_ppi']} ppi effective"
            print(line)
            for problem in r['problems']:
                print('  problem: ' + problem)
            for note in r['notes']:
                print('  note: ' + note)
            if r.get('analysis'):
                a = r['analysis']
                print('  palette: ' + ', '.join(f"{c['hex']} {c['share']:.0%}" for c in a['palette']))
                t = a['tones']
                print(f"  tones: {t['key']} key, 5-95 % range {t['p05']}-{t['p95']}, median {t['p50']}, clipped shadows {t['shadows_clipped']:.1%}, highlights {t['highlights_clipped']:.1%}")
                sub = a['subject']
                print('  subject: ' + (f"centre x {sub['centre_percent']['x']} %, y {sub['centre_percent']['y']} %, box {sub['box_percent']}, on {sub['background_hex']}" if sub['status'] == 'measured' else sub['reason']))
            if r.get('ocr'):
                print(f"  ocr: {r['ocr']['status']}" + (f" missing {r['ocr'].get('missing_words')}" if r['ocr'].get('missing_words') else ''))
    return code


if __name__ == '__main__':
    sys.exit(main())
