#!/usr/bin/env python3
"""Print PDF: page boxes, output intent and a preflight report for a print shop.

    python3 print_pdf.py finish poster.pdf --trim-mm 148x210 --bleed-mm 3 --out poster-print.pdf
    python3 print_pdf.py finish poster.pdf --trim-mm 148x210 --bleed-mm 3 --icc PSOcoated_v3.icc \
        --condition "PSO Coated v3 (FOGRA51)" --out poster-print.pdf
    python3 print_pdf.py check poster-print.pdf --bleed-mm 3 --min-ppi 300 --max-tac 300 --require cmyk

`finish` centres a TrimBox (the finished size) and a BleedBox (trim plus bleed) on each page, so
imposition and preflight read the sizes from the file, and with --icc embeds the printer's profile
as an output intent. It does not convert colours and does not claim PDF/X conformance: confirm
with the printer's own preflight. `check` reports boxes, bleed, effective image resolution,
colour spaces, total ink coverage of CMYK images, font embedding and the output intent, and
exits 1 when a limit fails. It reads images and fonts placed directly on the page, not inside form
XObjects, and does not inspect vector colour operators; the printer's preflight remains the gate.
Needs pikepdf (pip install pikepdf, MPL-2.0); numpy and Pillow for TAC.
"""
import argparse
import json
import sys

import pikepdf

PT_PER_MM = 72 / 25.4
SLACK = 0.1 * PT_PER_MM  # pixel rounding in exported artwork


def mm(points):
    return round(points / PT_PER_MM, 2)


def box(page, name):
    value = page.obj.get('/' + name)
    return [float(v) for v in value] if value is not None else None


def centred(media, width, height):
    x0, y0, x1, y1 = media
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    return [round(cx - width / 2, 3), round(cy - height / 2, 3), round(cx + width / 2, 3), round(cy + height / 2, 3)]


def icc_components(data):
    space = data[16:20]
    return {b'CMYK': 4, b'RGB ': 3, b'GRAY': 1}.get(space)


def finish(args):
    trim_w, trim_h = (float(v) * PT_PER_MM for v in args.trim_mm.lower().split('x'))
    bleed = args.bleed_mm * PT_PER_MM
    pdf = pikepdf.open(args.pdf)
    for number, page in enumerate(pdf.pages, 1):
        media = [float(v) for v in page.mediabox]
        bleed_box = centred(media, trim_w + 2 * bleed, trim_h + 2 * bleed)
        if bleed_box[0] < media[0] - SLACK or bleed_box[1] < media[1] - SLACK:
            sys.exit(f'page {number}: the page ({mm(media[2] - media[0])} x {mm(media[3] - media[1])} mm) is smaller than '
                     f'trim plus bleed; export the artwork with its bleed first')
        bleed_box = [max(bleed_box[0], media[0]), max(bleed_box[1], media[1]), min(bleed_box[2], media[2]), min(bleed_box[3], media[3])]
        page.obj['/TrimBox'] = pikepdf.Array(centred(media, trim_w, trim_h))
        page.obj['/BleedBox'] = pikepdf.Array(bleed_box)
    if args.icc:
        with open(args.icc, 'rb') as handle:
            data = handle.read()
        n = icc_components(data)
        if n is None:
            sys.exit(f'{args.icc}: not an RGB, CMYK or grey ICC profile')
        profile = pikepdf.Stream(pdf, data)
        profile['/N'] = n
        intent = pikepdf.Dictionary(Type=pikepdf.Name.OutputIntent, S=pikepdf.Name.GTS_PDFX,
                                    OutputConditionIdentifier=args.condition, Info=args.condition,
                                    RegistryName='http://www.color.org', DestOutputProfile=profile)
        pdf.Root.OutputIntents = pikepdf.Array([intent])
    pdf.docinfo['/Trapped'] = pikepdf.Name.False_
    pdf.save(args.out)
    print(f'{args.out}: TrimBox {args.trim_mm} mm, bleed {args.bleed_mm} mm'
          + (f', output intent {args.condition}' if args.icc else '') + '; colours unchanged')
    return 0


def placements(page):
    """Image name -> placed width and height in points, from the content stream's matrices."""
    found, stack, ctm = {}, [], [1, 0, 0, 1, 0, 0]
    for operands, operator in pikepdf.parse_content_stream(page):
        op = str(operator)
        if op == 'q':
            stack.append(ctm)
        elif op == 'Q' and stack:
            ctm = stack.pop()
        elif op == 'cm':
            a, b, c, d, e, f = (float(v) for v in operands)
            A, B, C, D, E, F = ctm
            ctm = [a * A + b * C, a * B + b * D, c * A + d * C, c * B + d * D, e * A + f * C + E, e * B + f * D + F]
        elif op == 'Do':
            found[str(operands[0])] = ((ctm[0] ** 2 + ctm[1] ** 2) ** 0.5, (ctm[2] ** 2 + ctm[3] ** 2) ** 0.5)
    return found


def colour_space(obj):
    cs = obj.get('/ColorSpace')
    if cs is None:
        return 'mask'
    if isinstance(cs, pikepdf.Array) and str(cs[0]) == '/ICCBased':
        return {4: 'CMYK', 3: 'RGB', 1: 'Gray'}.get(int(cs[1].get('/N', 0)), 'ICC')
    return str(cs).replace('/Device', '').lstrip('/')


def tac(obj):
    try:
        import numpy as np
        image = pikepdf.PdfImage(obj).as_pil_image()
        if image.mode != 'CMYK':
            return None
        ink = np.asarray(image, dtype=np.uint16).sum(axis=2) * (100 / 255)
        return round(float(ink.max()), 1), round(float(np.percentile(ink, 99.9)), 1)
    except Exception:
        return None


def check(args):
    pdf = pikepdf.open(args.pdf)
    problems, pages = [], []
    for number, page in enumerate(pdf.pages, 1):
        media, trim, bleed_box = [float(v) for v in page.mediabox], box(page, 'TrimBox'), box(page, 'BleedBox')
        info = {'page': number, 'media_mm': [mm(media[2] - media[0]), mm(media[3] - media[1])]}
        if not trim or not bleed_box:
            problems.append(f'page {number}: no TrimBox or BleedBox (run finish)')
        else:
            info['trim_mm'] = [mm(trim[2] - trim[0]), mm(trim[3] - trim[1])]
            sides = [trim[0] - bleed_box[0], trim[1] - bleed_box[1], bleed_box[2] - trim[2], bleed_box[3] - trim[3]]
            info['bleed_mm'] = round(mm(min(sides)), 2)
            if info['bleed_mm'] + 0.1 < args.bleed_mm:
                problems.append(f'page {number}: bleed {info["bleed_mm"]} mm, printer asks for {args.bleed_mm} mm')
        placed, images = placements(page), []
        xobjects = page.resources.get('/XObject', {})
        for name, obj in xobjects.items():
            if obj.get('/Subtype') != '/Image':
                continue
            w_pt, h_pt = placed.get(name, (0, 0))
            px_w, px_h = int(obj.get('/Width')), int(obj.get('/Height'))
            ppi = round(min(px_w / (w_pt / 72), px_h / (h_pt / 72))) if w_pt and h_pt else None
            space = colour_space(obj)
            entry = {'image': name, 'pixels': [px_w, px_h], 'effective_ppi': ppi, 'colour': space}
            if space == 'CMYK':
                entry['tac_max_and_p99_9'] = tac(obj)
            images.append(entry)
            if ppi is not None and ppi < args.min_ppi:
                problems.append(f'page {number}: {name} at {ppi} ppi effective (minimum {args.min_ppi})')
            if args.require == 'cmyk' and space not in ('CMYK', 'Gray', 'mask'):
                problems.append(f'page {number}: {name} is {space}; the printer asks for CMYK')
            if entry.get('tac_max_and_p99_9') and entry['tac_max_and_p99_9'][1] > args.max_tac:
                problems.append(f'page {number}: {name} total ink {entry["tac_max_and_p99_9"][1]} % (limit {args.max_tac} %)')
        info['images'] = images
        fonts = []
        for name, font in page.resources.get('/Font', {}).items():
            descriptor = font.get('/FontDescriptor') or (font.get('/DescendantFonts') or [{}])[0].get('/FontDescriptor')
            embedded = bool(descriptor) and any(k in descriptor for k in ('/FontFile', '/FontFile2', '/FontFile3'))
            fonts.append({'font': str(font.get('/BaseFont')), 'embedded': embedded})
            if not embedded:
                problems.append(f'page {number}: font {font.get("/BaseFont")} is not embedded')
        info['fonts'] = fonts
        pages.append(info)
    intents = pdf.Root.get('/OutputIntents')
    intent = str(intents[0].get('/OutputConditionIdentifier')) if intents else None
    if args.require == 'cmyk' and not intent:
        problems.append('no output intent; embed the printer\'s profile with finish --icc')
    report = {'pdf': args.pdf, 'pdf_version': pdf.pdf_version, 'output_intent': intent, 'pages': pages,
              'verdict': 'REVISE' if problems else 'PASS', 'problems': problems}
    if args.json:
        print(json.dumps(report, indent=1))
    else:
        print(f"{report['verdict']}: {len(pages)} page(s), output intent {intent or 'none'}"
              + ''.join(f'\n- {p}' for p in problems))
    return 1 if problems else 0


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest='command', required=True)
    f = sub.add_parser('finish')
    f.add_argument('pdf'); f.add_argument('--trim-mm', required=True, help='finished size, e.g. 148x210')
    f.add_argument('--bleed-mm', type=float, default=3.0); f.add_argument('--icc'); f.add_argument('--condition', default='Custom')
    f.add_argument('--out', required=True)
    c = sub.add_parser('check')
    c.add_argument('pdf'); c.add_argument('--bleed-mm', type=float, default=3.0); c.add_argument('--min-ppi', type=int, default=300)
    c.add_argument('--max-tac', type=float, default=300); c.add_argument('--require', choices=('any', 'cmyk'), default='any')
    c.add_argument('--json', action='store_true')
    args = p.parse_args(argv)
    return finish(args) if args.command == 'finish' else check(args)


if __name__ == '__main__':
    sys.exit(main())
