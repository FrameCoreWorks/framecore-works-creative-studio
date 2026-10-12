#!/usr/bin/env python3
"""Print PDF: page boxes, output intent, a preflight report and a render comparison for a print shop.

    python3 print_pdf.py finish poster.pdf --trim-mm 148x210 --bleed-mm 3 --out poster-print.pdf
    python3 print_pdf.py finish poster.pdf --trim-mm 148x210 --bleed-mm 3 --icc PSOcoated_v3.icc \
        --condition "PSO Coated v3 (FOGRA51)" --out poster-print.pdf
    python3 print_pdf.py check poster-print.pdf --bleed-mm 3 --min-ppi 300 --max-tac 300 --require cmyk
    python3 print_pdf.py compare poster-v02.pdf poster-v03.pdf --region 10,20,90,60

`finish` centres a TrimBox (the finished size) and a BleedBox (trim plus bleed) on each page, so
imposition and preflight read the sizes from the file, and with --icc embeds the printer's profile
as an output intent. It does not convert colours and does not claim PDF/X conformance.

`check` walks each page and the form XObjects drawn on it and reports boxes, bleed, effective image
resolution, the colour spaces of images and vector paint (RGB, CMYK, grey, spot colours), total ink
of CMYK images and vector colours, transparency (soft masks, blend modes, alpha), the thinnest
stroked line, fonts and their embedding, embedded files (including /AF, where C2PA manifests sit),
the output intent, the declared PDF/X version, Trapped, the producer and the file's SHA-256. It exits
1 when a limit fails. --require cmyk adds RGB, a missing output intent and embedded files as
problems; --require x1a also forbids transparency and PDF versions above 1.4. Declarations in the
file are reported, never trusted: this is a preflight, not PDF/X validation, and the printer's
preflight or proof remains the gate. Patterns, shadings inside patterns and annotation appearances
are not inspected.

`compare` renders both files with pdftoppm (poppler) and reports per page the share and the box of
changed pixels, in mm from the top-left of the page; changes outside --region exit 1.

Needs pikepdf (pip install pikepdf, MPL-2.0); numpy and Pillow for total ink and comparison.
"""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pikepdf

PT_PER_MM = 72 / 25.4
SLACK = 0.1 * PT_PER_MM  # pixel rounding in exported artwork
IDENTITY = [1, 0, 0, 1, 0, 0]
DEVICE = {'/DeviceCMYK': 'CMYK', '/DeviceRGB': 'RGB', '/DeviceGray': 'Gray', '/Pattern': 'Pattern'}
NOT_CMYK = ('RGB', 'Lab', 'CalRGB', 'ICC')
STROKES = ('S', 's', 'B', 'B*', 'b', 'b*')


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


def multiply(m, ctm):
    a, b, c, d, e, f = m
    A, B, C, D, E, F = ctm
    return [a * A + b * C, a * B + b * D, c * A + d * C, c * B + d * D, e * A + f * C + E, e * B + f * D + F]


def space_name(cs, resources):
    """A colour space (object or resource name) as CMYK, RGB, Gray, 'Spot <name>', DeviceN, Lab, Pattern."""
    if cs is None:
        return 'mask'
    if isinstance(cs, pikepdf.Name) and str(cs) not in DEVICE:
        cs = resources.get('/ColorSpace', {}).get(str(cs), cs)
    if isinstance(cs, pikepdf.Name):
        return DEVICE.get(str(cs), str(cs).lstrip('/'))
    if isinstance(cs, pikepdf.Array) and len(cs):
        kind = str(cs[0])
        if kind == '/ICCBased':
            return {4: 'CMYK', 3: 'RGB', 1: 'Gray'}.get(int(cs[1].get('/N', 0)), 'ICC')
        if kind == '/Separation':
            return 'Spot ' + str(cs[1]).lstrip('/')
        if kind == '/DeviceN':
            return 'DeviceN ' + '+'.join(str(n).lstrip('/') for n in cs[1])
        if kind == '/Indexed':
            return space_name(cs[1], resources)
        return DEVICE.get(kind, kind.lstrip('/'))
    return 'Unknown'


def image_tac(obj):
    try:
        import numpy as np
        image = pikepdf.PdfImage(obj).as_pil_image()
        if image.mode != 'CMYK':
            return None
        ink = np.asarray(image, dtype=np.uint16).sum(axis=2) * (100 / 255)
        return round(float(ink.max()), 1), round(float(np.percentile(ink, 99.9)), 1)
    except Exception:
        return None


class Scan:
    """What one page paints, collected across its content stream and nested forms."""

    def __init__(self):
        self.images, self.paint, self.fonts = {}, {}, {}
        self.transparency, self.vector_tac, self.min_line = set(), 0.0, None

    def colour(self, space, values=None):
        self.paint[space] = self.paint.get(space, 0) + 1
        if space == 'CMYK' and values and len(values) == 4:
            self.vector_tac = max(self.vector_tac, round(sum(float(v) for v in values) * 100, 1))

    def image(self, key, name, obj, ctm, space):
        width_pt, height_pt = (ctm[0] ** 2 + ctm[1] ** 2) ** 0.5, (ctm[2] ** 2 + ctm[3] ** 2) ** 0.5
        px_w, px_h = int(obj.get('/Width', 0) or 0), int(obj.get('/Height', 0) or 0)
        ppi = round(min(px_w / (width_pt / 72), px_h / (height_pt / 72))) if width_pt and height_pt and px_w else None
        entry = self.images.get(key)
        if entry is None:
            entry = self.images[key] = {'image': name, 'pixels': [px_w, px_h], 'effective_ppi': ppi, 'colour': space}
            if space == 'CMYK' and isinstance(obj, pikepdf.Stream):
                entry['tac_max_and_p99_9'] = image_tac(obj)
            if obj.get('/SMask') is not None:
                self.transparency.add('image soft mask')
        elif ppi is not None and (entry['effective_ppi'] is None or ppi < entry['effective_ppi']):
            entry['effective_ppi'] = ppi


def walk(owner, resources, ctm, scan, chain=()):
    """Follows the graphics state through one content stream and every form XObject it draws."""
    state, stack = {'ctm': ctm, 'w': 1.0, 'fill': 'Gray', 'stroke': 'Gray'}, []
    for operands, operator in pikepdf.parse_content_stream(owner):
        op = str(operator)
        if op == 'q':
            stack.append(dict(state))
        elif op == 'Q' and stack:
            state = stack.pop()
        elif op == 'cm':
            state['ctm'] = multiply([float(v) for v in operands], state['ctm'])
        elif op == 'w':
            state['w'] = float(operands[0])
        elif op in STROKES:
            a, b, c, d = state['ctm'][:4]
            width = round(state['w'] * abs(a * d - b * c) ** 0.5, 3)
            scan.min_line = width if scan.min_line is None else min(scan.min_line, width)
        elif op in ('k', 'K'):
            state['fill' if op == 'k' else 'stroke'] = 'CMYK'
            scan.colour('CMYK', operands)
        elif op in ('rg', 'RG', 'g', 'G'):
            space = 'RGB' if op in ('rg', 'RG') else 'Gray'
            state['fill' if op.islower() else 'stroke'] = space
            scan.colour(space)
        elif op in ('cs', 'CS'):
            state['fill' if op == 'cs' else 'stroke'] = space = space_name(operands[0], resources)
            scan.colour(space)
        elif op in ('sc', 'scn', 'SC', 'SCN'):
            space = state['fill' if op.islower() else 'stroke']
            if space == 'CMYK':
                scan.colour('CMYK', [v for v in operands if not isinstance(v, pikepdf.Name)])
        elif op == 'sh':
            shading = resources.get('/Shading', {}).get(str(operands[0]))
            if shading is not None:
                scan.colour(space_name(shading.get('/ColorSpace'), resources))
        elif op == 'gs':
            ext = resources.get('/ExtGState', {}).get(str(operands[0]))
            if ext is not None:
                if ext.get('/SMask') is not None and str(ext.get('/SMask')) != '/None':
                    scan.transparency.add('soft mask')
                blend = ext.get('/BM')
                blend = str(blend[0] if isinstance(blend, pikepdf.Array) else blend) if blend is not None else '/Normal'
                if blend not in ('/Normal', '/Compatible'):
                    scan.transparency.add('blend mode ' + blend.lstrip('/'))
                if any(ext.get(k) is not None and float(ext.get(k)) < 1 for k in ('/ca', '/CA')):
                    scan.transparency.add('alpha')
        elif op == 'Tf':
            font = resources.get('/Font', {}).get(str(operands[0]))
            if font is not None:
                descriptor = font.get('/FontDescriptor') or (font.get('/DescendantFonts') or [{}])[0].get('/FontDescriptor')
                embedded = str(font.get('/Subtype')) == '/Type3' or (
                    bool(descriptor) and any(k in descriptor for k in ('/FontFile', '/FontFile2', '/FontFile3')))
                scan.fonts[str(font.get('/BaseFont'))] = embedded
        elif op == 'Do':
            name = str(operands[0])
            obj = resources.get('/XObject', {}).get(name)
            if obj is None:
                continue
            if obj.get('/Subtype') == '/Image':
                scan.image(obj.objgen if obj.is_indirect else name, name, obj, state['ctm'],
                           space_name(obj.get('/ColorSpace'), {}))
            elif obj.get('/Subtype') == '/Form' and obj.objgen not in chain and len(chain) < 16:
                matrix = [float(v) for v in obj.get('/Matrix', IDENTITY)]
                walk(obj, obj.get('/Resources', resources), multiply(matrix, state['ctm']), scan, chain + (obj.objgen,))
        elif op == 'INLINE IMAGE':
            image = operands[0]
            space = space_name(pikepdf.Name(image.colorspace), resources) if image.colorspace else 'mask'
            scan.image(('inline', len(scan.images)), 'inline image', {'/Width': image.width, '/Height': image.height},
                       state['ctm'], space)


def embedded_files(pdf):
    found = [f'{name} (EmbeddedFiles)' for name in pdf.attachments.keys()]
    catalog_af = pdf.Root.get('/AF')
    if catalog_af is not None:
        found += [f'{spec.get("/UF", spec.get("/F", "?"))} (catalog /AF)' for spec in catalog_af]
    for number, page in enumerate(pdf.pages, 1):
        if page.obj.get('/AF') is not None:
            found.append(f'page {number} /AF')
        for annot in page.obj.get('/Annots', []):
            if annot.get('/Subtype') == '/FileAttachment':
                found.append(f'page {number} file attachment annotation')
    return sorted(set(str(f) for f in found))


def check(args):
    pdf = pikepdf.open(args.pdf)
    problems, notes, pages = [], [], []
    for number, page in enumerate(pdf.pages, 1):
        media, trim, bleed_box = [float(v) for v in page.mediabox], box(page, 'TrimBox'), box(page, 'BleedBox')
        info = {'page': number, 'media_mm': [mm(media[2] - media[0]), mm(media[3] - media[1])]}
        if not trim or not bleed_box:
            problems.append(f'page {number}: no TrimBox or BleedBox (run finish)')
        else:
            info['trim_mm'] = [mm(trim[2] - trim[0]), mm(trim[3] - trim[1])]
            sides = [trim[0] - bleed_box[0], trim[1] - bleed_box[1], bleed_box[2] - trim[2], bleed_box[3] - trim[3]]
            info['bleed_mm_left_bottom_right_top'] = [mm(s) for s in sides]
            info['bleed_mm'] = round(mm(min(sides)), 2)
            if info['bleed_mm'] + 0.1 < args.bleed_mm:
                problems.append(f'page {number}: bleed {info["bleed_mm"]} mm, printer asks for {args.bleed_mm} mm')
        scan = Scan()
        walk(page, page.resources, list(IDENTITY), scan)
        info['images'] = list(scan.images.values())
        info['vector_colour_spaces'] = scan.paint
        info['vector_tac_max'] = scan.vector_tac or None
        info['thinnest_line_pt'] = scan.min_line
        info['transparency'] = sorted(scan.transparency)
        info['fonts'] = [{'font': name, 'embedded': embedded} for name, embedded in scan.fonts.items()]
        for entry in info['images']:
            if entry['effective_ppi'] is not None and entry['effective_ppi'] < args.min_ppi:
                problems.append(f'page {number}: {entry["image"]} at {entry["effective_ppi"]} ppi effective (minimum {args.min_ppi})')
            if args.require != 'any' and entry['colour'] in NOT_CMYK:
                problems.append(f'page {number}: {entry["image"]} is {entry["colour"]}; the printer asks for CMYK')
            if entry.get('tac_max_and_p99_9') and entry['tac_max_and_p99_9'][1] > args.max_tac:
                problems.append(f'page {number}: {entry["image"]} total ink {entry["tac_max_and_p99_9"][1]} % (limit {args.max_tac} %)')
        vector_rgb = sorted(s for s in scan.paint if s in NOT_CMYK)
        if args.require != 'any' and vector_rgb:
            problems.append(f'page {number}: vector colour in {", ".join(vector_rgb)}; the printer asks for CMYK')
        if scan.vector_tac > args.max_tac:
            problems.append(f'page {number}: vector colour reaches total ink {scan.vector_tac} % (limit {args.max_tac} %)')
        spots = sorted(s for s in scan.paint if s.startswith(('Spot', 'DeviceN')) and s not in ('Spot All', 'Spot None'))
        if spots:
            notes.append(f'page {number}: {", ".join(spots)}; confirm each was ordered, otherwise convert to process colour')
        if scan.min_line is not None and scan.min_line < args.min_line:
            problems.append(f'page {number}: a stroked line of {scan.min_line} pt (minimum {args.min_line} pt; 0 is a device hairline)')
        if scan.transparency:
            (problems if args.require == 'x1a' else notes).append(
                f'page {number}: transparency ({", ".join(sorted(scan.transparency))})'
                + ('; PDF/X-1a needs it flattened' if args.require == 'x1a' else '; check it with the printer or flatten it'))
        for name, embedded in scan.fonts.items():
            if not embedded:
                problems.append(f'page {number}: font {name} is not embedded')
        pages.append(info)
    intents = pdf.Root.get('/OutputIntents')
    intent = str(intents[0].get('/OutputConditionIdentifier')) if intents else None
    if args.require != 'any' and not intent:
        problems.append('no output intent; embed the printer\'s profile with finish --icc')
    attachments = embedded_files(pdf)
    if attachments:
        (problems if args.require != 'any' else notes).append(
            'embedded files (' + '; '.join(attachments) + '); remove them, PDF/X and most printers do not take them')
    declared = {k.lstrip('/'): str(pdf.docinfo.get(k)) for k in
                ('/GTS_PDFXVersion', '/GTS_PDFXConformance', '/Trapped', '/Producer', '/Creator', '/Title')
                if pdf.docinfo.get(k) is not None}
    if 'Trapped' not in declared:
        notes.append('Trapped is not set (PDF/X requires True or False; finish sets False)')
    if declared.get('GTS_PDFXVersion'):
        notes.append(f'the file declares {declared["GTS_PDFXVersion"]}'
                     + (f' / {declared["GTS_PDFXConformance"]}' if declared.get('GTS_PDFXConformance') else '')
                     + '; a declaration is not validation')
    if args.require == 'x1a' and pdf.pdf_version > '1.4':
        problems.append(f'PDF {pdf.pdf_version}; PDF/X-1a uses PDF 1.3 or 1.4')
    digest = hashlib.sha256(Path(args.pdf).read_bytes()).hexdigest()
    report = {'pdf': args.pdf, 'sha256': digest, 'pdf_version': pdf.pdf_version, 'output_intent': intent,
              'declared': declared, 'embedded_files': attachments, 'pages': pages,
              'verdict': 'REVISE' if problems else 'PASS', 'problems': problems, 'notes': notes}
    if args.json:
        print(json.dumps(report, indent=1, ensure_ascii=False))
    else:
        print(f"{report['verdict']}: {len(pages)} page(s), output intent {intent or 'none'}, sha256 {digest[:16]}"
              + ''.join(f'\n- {p}' for p in problems) + ''.join(f'\n  note: {n}' for n in notes))
    return 1 if problems else 0


def render(pdf, dpi, folder, prefix):
    tool = shutil.which('pdftoppm')
    if not tool:
        sys.exit('compare needs pdftoppm from poppler (brew install poppler, apt install poppler-utils)')
    subprocess.run([tool, '-r', str(dpi), '-png', str(pdf), str(folder / prefix)], check=True)
    return sorted(folder.glob(prefix + '-*.png'))


def compare(args):
    from PIL import Image, ImageChops
    region = [float(v) for v in args.region.split(',')] if args.region else None
    pages, outside = [], False
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        before, after = render(args.before, args.dpi, folder, 'a'), render(args.after, args.dpi, folder, 'b')
        if len(before) != len(after):
            outside = True
        for number, (path_a, path_b) in enumerate(zip(before, after), 1):
            a, b = Image.open(path_a).convert('RGB'), Image.open(path_b).convert('RGB')
            if a.size != b.size:
                pages.append({'page': number, 'size_changed': [a.size, b.size]})
                outside = True
                continue
            diff = ImageChops.difference(a, b).convert('L').point(lambda v: 255 if v > args.tolerance else 0)
            changed = diff.histogram()[255]
            entry = {'page': number, 'changed_share_percent': round(changed * 100 / (a.width * a.height), 3)}
            bbox = diff.getbbox()
            if bbox:
                entry['changed_box_mm'] = [round(v * 25.4 / args.dpi, 1) for v in bbox]
                x0, y0, x1, y1 = entry['changed_box_mm']
                if not region or x0 < region[0] or y0 < region[1] or x1 > region[2] or y1 > region[3]:
                    outside = True
            pages.append(entry)
    changed = any('changed_box_mm' in p or 'size_changed' in p for p in pages) or len(before) != len(after)
    verdict = 'CHANGED_OUTSIDE' if outside else ('CHANGED_INSIDE' if changed else 'SAME')
    report = {'before': args.before, 'after': args.after, 'pages_before': len(before), 'pages_after': len(after),
              'region_mm': region, 'pages': pages, 'verdict': verdict}
    print(json.dumps(report, indent=1))
    return 1 if outside else 0


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest='command', required=True)
    f = sub.add_parser('finish')
    f.add_argument('pdf'); f.add_argument('--trim-mm', required=True, help='finished size, e.g. 148x210')
    f.add_argument('--bleed-mm', type=float, default=3.0); f.add_argument('--icc'); f.add_argument('--condition', default='Custom')
    f.add_argument('--out', required=True)
    c = sub.add_parser('check')
    c.add_argument('pdf'); c.add_argument('--bleed-mm', type=float, default=3.0); c.add_argument('--min-ppi', type=int, default=300)
    c.add_argument('--max-tac', type=float, default=300); c.add_argument('--min-line', type=float, default=0.25, help='points')
    c.add_argument('--require', choices=('any', 'cmyk', 'x1a'), default='any'); c.add_argument('--json', action='store_true')
    d = sub.add_parser('compare')
    d.add_argument('before'); d.add_argument('after'); d.add_argument('--dpi', type=int, default=100)
    d.add_argument('--region', help='allowed change box in mm from the top-left of the page: x0,y0,x1,y1')
    d.add_argument('--tolerance', type=int, default=8, help='per-pixel difference ignored (0 to 255)')
    args = p.parse_args(argv)
    return {'finish': finish, 'check': check, 'compare': compare}[args.command](args)


if __name__ == '__main__':
    sys.exit(main())
