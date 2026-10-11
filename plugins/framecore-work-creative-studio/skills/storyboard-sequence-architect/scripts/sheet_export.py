#!/usr/bin/env python3
"""Export a shot list or an AV script as a spreadsheet (XLSX and CSV) and a printable PDF, with exact text.

  python3 sheet_export.py shot-plan.json --out-dir export/            # shot-plan.xlsx, .csv and .pdf
  python3 sheet_export.py av-script.json --out-dir export/ --formats xlsx,pdf

Input, detected from its keys:
  shot plan   {"shots": [{"id", "start_s", "end_s", "action", "camera"?, "audio"?, "notes"?, "required_refs"?}]}
  AV script   {"title", "rows": [{"time", "video", "super", "audio", "music"}]}
  any table   {"title", "columns": ["A", "B"], "rows": [["a1", "b1"]]}

The XLSX is written with the standard library (Office Open XML, text cells, bold wrapped header, frozen first row);
the PDF uses Pillow and Studio's bundled Inter font, so Polish letters print exactly; text is wrapped, never cut.
Exit codes: 0 written, 2 bad input, a missing font or an output that exists.
"""
import argparse
import csv
import io
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

FONTS = Path(__file__).resolve().parents[2] / 'pipeline-core/assets/fonts/inter'


UNIT = r'(?:zł|gr|kg|km|cm|mm|ml|min|PLN|EUR|USD|[gmlhs])(?![^\W\d_])|%'


def keep_together(text):
    """Polish typesetting, as in the motion renderer: a one-letter word never ends a line, and digit groups and a number
    with its unit stay together (the space becomes a no-break space)."""
    text = re.sub(r'(?<!\S)([^\W\d_]) +(?=\S)', '\\1\u00a0', str(text))
    text = re.sub(r'(\d) (?=\d{3}(?!\d))', '\\1\u00a0', text)
    return re.sub(r'(\d) (?=' + UNIT + ')', '\\1\u00a0', text)


class InputError(Exception):
    pass


def seconds(value):
    return f'{int(value // 60)}:{value % 60:05.2f}'.rstrip('0').rstrip('.') if isinstance(value, (int, float)) else str(value or '')


def table(data, name):
    if isinstance(data.get('shots'), list):
        columns = ['Shot', 'In', 'Out', 'Seconds', 'Action', 'Camera', 'Audio', 'Notes', 'References']
        rows = []
        for shot in data['shots']:
            start, end = shot.get('start_s'), shot.get('end_s')
            length = round(end - start, 3) if isinstance(start, (int, float)) and isinstance(end, (int, float)) else ''
            notes = shot.get('notes') or ' / '.join(x for x in (shot.get('entry_state'), shot.get('exit_state')) if x)
            rows.append([shot.get('id', ''), seconds(start), seconds(end), length, shot.get('action', ''), shot.get('camera', ''), shot.get('audio', ''), notes,
                         ', '.join(shot.get('required_refs') or [])])
        return data.get('title') or f'{name}: shot list', 'Shot list', columns, rows
    if isinstance(data.get('rows'), list) and all(isinstance(r, dict) for r in data['rows']):
        keys = [('time', 'Time'), ('video', 'Video'), ('super', 'Super (on screen)'), ('audio', 'Audio: voice-over or dialogue'), ('music', 'Music and sound')]
        return data.get('title') or f'{name}: AV script', 'AV script', [label for _, label in keys], [[row.get(k, '') for k, _ in keys] for row in data['rows']]
    if isinstance(data.get('columns'), list) and isinstance(data.get('rows'), list):
        if any(not isinstance(r, list) or len(r) != len(data['columns']) for r in data['rows']):
            raise InputError('every row needs one value per column')
        return data.get('title') or name, str(data.get('sheet') or 'Sheet1')[:31], [str(c) for c in data['columns']], data['rows']
    raise InputError('expected a shot plan ("shots"), an AV script ("rows" of objects) or a table ("columns" and "rows")')


def cell_ref(col, row):
    letters = ''
    col += 1
    while col:
        col, rem = divmod(col - 1, 26)
        letters = chr(65 + rem) + letters
    return f'{letters}{row}'


def xlsx(columns, rows, sheet):
    widths = [min(60, max([len(str(c))] + [max((len(line) for line in str(r[i]).split('\n')), default=0) for r in rows]) + 2) for i, c in enumerate(columns)]

    def cell(value, col, row, style):
        ref = cell_ref(col, row)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return f'<c r="{ref}" s="{style}"><v>{value}</v></c>'
        text = escape(str(value))
        return f'<c r="{ref}" s="{style}" t="inlineStr"><is><t xml:space="preserve">{text}</t></is></c>'

    body = ''.join(f'<row r="{r + 1}">' + ''.join(cell(v, c, r + 1, 1 if r == 0 else 2) for c, v in enumerate(values)) + '</row>'
                   for r, values in enumerate([columns] + rows))
    cols = ''.join(f'<col min="{i + 1}" max="{i + 1}" width="{w}" customWidth="1"/>' for i, w in enumerate(widths))
    sheet_xml = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                 '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
                 '<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>'
                 f'<cols>{cols}</cols><sheetData>{body}</sheetData></worksheet>')
    styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
              '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
              '<fonts count="2"><font><sz val="11"/><name val="Calibri"/></font><font><b/><sz val="11"/><name val="Calibri"/></font></fonts>'
              '<fills count="2"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill></fills>'
              '<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
              '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
              '<cellXfs count="3"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>'
              '<xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1" applyAlignment="1"><alignment wrapText="1" vertical="top"/></xf>'
              '<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0" applyAlignment="1"><alignment wrapText="1" vertical="top"/></xf></cellXfs>'
              '<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>'
              '</styleSheet>')
    parts = {
        '[Content_Types].xml': '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                               '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
                               '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
                               '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
                               '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/></Types>',
        '_rels/.rels': '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                       '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>',
        'xl/workbook.xml': '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
                           'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
                           f'<sheets><sheet name="{escape(sheet)}" sheetId="1" r:id="rId1"/></sheets></workbook>',
        'xl/_rels/workbook.xml.rels': '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                                      '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
                                      '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>',
        'xl/worksheets/sheet1.xml': sheet_xml,
        'xl/styles.xml': styles,
    }
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name, text in parts.items():
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, text)
    return buffer.getvalue()


def csv_text(columns, rows):
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(columns)
    writer.writerows(rows)
    return '﻿' + out.getvalue()  # the BOM makes Excel read Polish letters correctly


def pdf(title, columns, rows, font_dir):
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        raise InputError('the PDF needs Pillow (pip install pillow); export --formats xlsx,csv without it')
    regular, bold = font_dir / 'Inter-Regular.ttf', font_dir / 'Inter-Bold.ttf'
    if not regular.is_file() or not bold.is_file():
        raise InputError(f'the PDF needs Inter-Regular.ttf and Inter-Bold.ttf in {font_dir} (Studio bundles them in pipeline-core/assets/fonts/inter)')
    W, H, margin, pad = 1754, 1240, 70, 10  # A4 landscape at 150 dpi
    body, head, top = ImageFont.truetype(str(regular), 20), ImageFont.truetype(str(bold), 20), ImageFont.truetype(str(bold), 30)
    line_h = 27
    texts = [[str(v) for v in r] for r in rows]
    # Column widths follow the longest line of each column, within limits, scaled to the page.
    natural = [min(520, max(70, max([head.getlength(c)] + [max((body.getlength(line) for line in t[i].split('\n')), default=0) for t in texts]) + 2 * pad)) for i, c in enumerate(columns)]
    scale = (W - 2 * margin) / sum(natural)
    widths = [w * scale for w in natural]

    def wrap(text, font, width):
        lines = []
        for paragraph in keep_together(text).split('\n'):
            words, line = paragraph.split(' '), ''
            for word in words:
                trial = word if not line else line + ' ' + word
                if line and font.getlength(trial) > width:
                    lines.append(line)
                    line = word
                else:
                    line = trial
            while font.getlength(line) > width:  # a single word longer than the column breaks by characters
                cut = max(1, next((n for n in range(len(line), 0, -1) if font.getlength(line[:n]) <= width), 1))
                lines.append(line[:cut])
                line = line[cut:]
            lines.append(line)
        return lines

    header = [wrap(c, head, w - 2 * pad) for c, w in zip(columns, widths)]
    header_h = max(len(h) for h in header) * line_h + 2 * pad
    pages, page, y = [], None, 0

    def new_page():
        image = Image.new('RGB', (W, H), 'white')
        draw = ImageDraw.Draw(image)
        draw.text((margin, margin - 10), title, font=top, fill=(20, 20, 20))
        yy = margin + 40
        draw.rectangle([margin, yy, W - margin, yy + header_h], fill=(235, 235, 235))
        x = margin
        for lines, w in zip(header, widths):
            for k, line in enumerate(lines):
                draw.text((x + pad, yy + pad + k * line_h), line, font=head, fill=(0, 0, 0))
            x += w
        pages.append(image)
        return image, draw, yy + header_h

    image, draw, y = new_page()
    for r, values in enumerate(texts):
        cells = [wrap(v, body, w - 2 * pad) for v, w in zip(values, widths)]
        row_h = max(len(c) for c in cells) * line_h + 2 * pad
        if y + row_h > H - margin:
            if row_h > H - 2 * margin - header_h - 60:
                raise InputError(f'row {r + 1} is taller than a page; split its text')
            image, draw, y = new_page()
        x = margin
        for lines, w in zip(cells, widths):
            for k, line in enumerate(lines):
                draw.text((x + pad, y + pad + k * line_h), line, font=body, fill=(0, 0, 0))
            x += w
        draw.line([margin, y + row_h, W - margin, y + row_h], fill=(200, 200, 200), width=1)
        y += row_h
    for n, image in enumerate(pages, 1):
        ImageDraw.Draw(image).text((W - margin - 80, H - margin + 20), f'{n} / {len(pages)}', font=body, fill=(90, 90, 90))
    buffer = io.BytesIO()
    pages[0].save(buffer, 'PDF', resolution=150, save_all=True, append_images=pages[1:])
    return buffer.getvalue(), len(pages)


def main(argv=None):
    parser = argparse.ArgumentParser(description='Export a shot list or AV script as XLSX, CSV and PDF.')
    parser.add_argument('input')
    parser.add_argument('--out-dir', required=True)
    parser.add_argument('--formats', default='xlsx,csv,pdf')
    parser.add_argument('--font-dir', help='folder with Inter-Regular.ttf and Inter-Bold.ttf (default: the bundled fonts)')
    args = parser.parse_args(argv)
    try:
        source = Path(args.input)
        stem = source.name.split('.')[0]
        title, sheet, columns, rows = table(json.loads(source.read_text(encoding='utf-8')), stem)
        wanted = [f.strip() for f in args.formats.split(',') if f.strip()]
        if not wanted or any(f not in ('xlsx', 'csv', 'pdf') for f in wanted):
            raise InputError('formats are xlsx, csv and pdf')
        folder = Path(args.out_dir)
        targets = {f: folder / f'{stem}.{f}' for f in wanted}
        existing = [str(p) for p in targets.values() if p.exists()]
        if existing:
            raise InputError(f'output exists: {", ".join(existing)}')
        outputs, report = {}, {'title': title, 'rows': len(rows), 'files': []}
        if 'xlsx' in targets:
            outputs['xlsx'] = xlsx(columns, rows, sheet)
        if 'csv' in targets:
            outputs['csv'] = csv_text(columns, rows).encode('utf-8')
        if 'pdf' in targets:
            outputs['pdf'], report['pdf_pages'] = pdf(title, columns, rows, Path(args.font_dir) if args.font_dir else FONTS)
        folder.mkdir(parents=True, exist_ok=True)
        for kind, data in outputs.items():
            targets[kind].write_bytes(data)
            report['files'].append(str(targets[kind]))
    except (OSError, ValueError, InputError) as error:
        sys.stderr.write(f'{error}\n')
        return 2
    print(json.dumps(report, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
