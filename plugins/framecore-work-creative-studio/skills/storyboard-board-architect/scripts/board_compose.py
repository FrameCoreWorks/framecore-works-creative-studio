#!/usr/bin/env python3
"""Lay out a storyboard as pages (PNG) and one PDF: frames in a grid with exact labels under each.

  python3 board_compose.py board.json --out-dir boards/        # board-p1.png, board-p2.png, board.pdf

board.json (image paths are relative to it):
  {"title": "Miód z Beskidów: storyboard v2", "subtitle": "Pasieka Lipa · 2026-10-11 · for approval",
   "frame": "9:16", "columns": 4, "page": "A4-landscape", "fit": "contain",
   "panels": [{"id": "S01", "time": "0:00–0:02", "camera": "MCU, push in", "image": "frames/s01.png",
               "action": "...", "audio": "VO: ...", "super": "Miód z Beskidów"}],
   "notes": "Assumptions: ...", "placeholder": "frame to come"}

Frames are drawn as given (contain, or cover with --fit) or as a marked placeholder when a panel has no image yet; the
labels are set in Studio's bundled Inter with every word kept: text wraps and rows move to the next page, nothing is cut.
Needs Pillow. Exit codes: 0 written, 2 bad input, a missing image or font, or an output that exists.
"""
import argparse
import json
import re
import sys
from pathlib import Path

FONTS = Path(__file__).resolve().parents[2] / 'pipeline-core/assets/fonts/inter'
PAGES = {'A4-landscape': (1754, 1240), 'A4-portrait': (1240, 1754), 'screen': (1920, 1080)}
FRAMES = {'16:9': 16 / 9, '9:16': 9 / 16, '1:1': 1.0, '4:5': 4 / 5, '2.39:1': 2.39, '4:3': 4 / 3}
LABELS = (('action', None), ('audio', 'Audio'), ('super', 'Super'))


UNIT = r'(?:zł|gr|kg|km|cm|mm|ml|min|PLN|EUR|USD|[gmlhs])(?![^\W\d_])|%'


def keep_together(text):
    """Polish typesetting, as in the motion renderer: a one-letter word never ends a line, and digit groups and a number
    with its unit stay together (the space becomes a no-break space)."""
    text = re.sub(r'(?<!\S)([^\W\d_]) +(?=\S)', '\\1\u00a0', str(text))
    text = re.sub(r'(\d) (?=\d{3}(?!\d))', '\\1\u00a0', text)
    return re.sub(r'(\d) (?=' + UNIT + ')', '\\1\u00a0', text)


class InputError(Exception):
    pass


def main(argv=None):
    parser = argparse.ArgumentParser(description='Compose a storyboard into PNG pages and a PDF with exact labels.')
    parser.add_argument('board')
    parser.add_argument('--out-dir', required=True)
    parser.add_argument('--fit', choices=['contain', 'cover'])
    parser.add_argument('--font-dir', help='folder with Inter-Regular.ttf and Inter-Bold.ttf (default: the bundled fonts)')
    args = parser.parse_args(argv)
    try:
        try:
            from PIL import Image, ImageDraw, ImageFont, ImageOps
        except ImportError:
            raise InputError('the storyboard compositor needs Pillow (pip install pillow)')
        source = Path(args.board)
        board = json.loads(source.read_text(encoding='utf-8'))
        panels = board.get('panels')
        if not isinstance(panels, list) or not panels:
            raise InputError('the board needs a list of panels')
        page_w, page_h = PAGES.get(board.get('page', 'A4-landscape'), (0, 0))
        if not page_w:
            raise InputError(f"page must be one of {', '.join(PAGES)}")
        aspect = FRAMES.get(str(board.get('frame', '16:9')))
        if not aspect:
            raise InputError(f"frame must be one of {', '.join(FRAMES)}")
        columns = int(board.get('columns') or (6 if aspect < 1 else 3))
        fit = args.fit or board.get('fit', 'contain')
        font_dir = Path(args.font_dir) if args.font_dir else FONTS
        try:
            fonts = {k: ImageFont.truetype(str(font_dir / f'Inter-{style}.ttf'), size) for k, (style, size) in
                     {'title': ('Bold', 34), 'subtitle': ('Regular', 20), 'head': ('Bold', 19), 'body': ('Regular', 17), 'notes': ('Regular', 18)}.items()}
        except OSError:
            raise InputError(f'Inter-Regular.ttf and Inter-Bold.ttf are needed in {font_dir}')
        stem = re.sub(r'(\.(example|motion-score|motion|shot-plan|shots|edit|board|prompts|plan|static))*\.json$', '', source.name)
        folder = Path(args.out_dir)

        margin, gutter, line = 60, 26, 23
        cell_w = (page_w - 2 * margin - (columns - 1) * gutter) / columns
        frame_w, frame_h = int(cell_w), int(cell_w / aspect)

        def wrap(text, font, width):
            if any(font.getlength(char) > width for char in text if not char.isspace()):
                raise ValueError('a glyph is wider than the text box')
            lines = []
            for paragraph in keep_together(text).split('\n'):
                line_text = ''
                for word in paragraph.split(' '):
                    trial = word if not line_text else f'{line_text} {word}'
                    if line_text and font.getlength(trial) > width:
                        while font.getlength(line_text) > width:
                            cut = max(1, next((n for n in range(len(line_text), 0, -1) if font.getlength(line_text[:n]) <= width), 1))
                            lines.append(line_text[:cut])
                            line_text = line_text[cut:]
                        lines.append(line_text)
                        line_text = word
                    else:
                        line_text = trial
                while font.getlength(line_text) > width:  # one word wider than the panel breaks by characters
                    cut = max(1, next((n for n in range(len(line_text), 0, -1) if font.getlength(line_text[:n]) <= width), 1))
                    lines.append(line_text[:cut])
                    line_text = line_text[cut:]
                lines.append(line_text)
            return lines

        def caption(panel):
            head = ' · '.join(str(panel[k]) for k in ('id', 'time', 'camera') if panel.get(k))
            out = [(l, fonts['head']) for l in wrap(head, fonts['head'], frame_w)] if head else []
            for key, label in LABELS:
                if panel.get(key):
                    text = f'„{panel[key]}”' if key == 'super' else str(panel[key])
                    out += [(l, fonts['body']) for l in wrap(f'{label}: {text}' if label else text, fonts['body'], frame_w)]
            return out

        def frame(panel):
            box = Image.new('RGB', (frame_w, frame_h), (232, 232, 232))
            if panel.get('image'):
                path = (source.parent / panel['image']).resolve()
                if not path.is_file():
                    raise InputError(f"panel {panel.get('id', '?')}: image not found: {panel['image']}")
                image = ImageOps.exif_transpose(Image.open(path)).convert('RGB')
                if fit == 'cover':
                    image = ImageOps.fit(image, (frame_w, frame_h), Image.LANCZOS)
                    box.paste(image, (0, 0))
                else:
                    image.thumbnail((frame_w, frame_h), Image.LANCZOS)
                    box.paste(image, ((frame_w - image.width) // 2, (frame_h - image.height) // 2))
            else:
                draw = ImageDraw.Draw(box)
                draw.line([(0, 0), (frame_w, frame_h)], fill=(205, 205, 205), width=2)
                draw.line([(0, frame_h), (frame_w, 0)], fill=(205, 205, 205), width=2)
                label = f"{panel.get('id', '')}: {board.get('placeholder', 'frame to come')}".strip(': ')
                width = fonts['body'].getlength(label)
                draw.rectangle([(frame_w - width) / 2 - 8, frame_h / 2 - 16, (frame_w + width) / 2 + 8, frame_h / 2 + 16], fill=(232, 232, 232))
                draw.text(((frame_w - width) / 2, frame_h / 2 - 11), label, font=fonts['body'], fill=(90, 90, 90))
            ImageDraw.Draw(box).rectangle([0, 0, frame_w - 1, frame_h - 1], outline=(60, 60, 60), width=2)
            return box

        captions = [caption(p) for p in panels]
        rows = [list(range(i, min(i + columns, len(panels)))) for i in range(0, len(panels), columns)]
        header_h = 110 if board.get('subtitle') else 80
        notes = wrap(board['notes'], fonts['notes'], page_w - 2 * margin) if board.get('notes') else []
        pages, current, y = [], None, 0

        def new_page():
            image = Image.new('RGB', (page_w, page_h), 'white')
            draw = ImageDraw.Draw(image)
            draw.text((margin, margin - 20), str(board.get('title', stem)), font=fonts['title'], fill=(15, 15, 15))
            if board.get('subtitle'):
                draw.text((margin, margin + 24), str(board['subtitle']), font=fonts['subtitle'], fill=(90, 90, 90))
            pages.append(image)
            return image, margin + header_h

        current, y = new_page()
        for row in rows:
            height = frame_h + 12 + max(len(captions[i]) for i in row) * line
            if y + height > page_h - margin:
                if height > page_h - 2 * margin - header_h:
                    raise InputError('one row of panels is taller than a page: use more columns, a smaller frame or shorter labels')
                current, y = new_page()
            draw = ImageDraw.Draw(current)
            for slot, i in enumerate(row):
                x = int(margin + slot * (cell_w + gutter))
                current.paste(frame(panels[i]), (x, int(y)))
                for k, (text, font) in enumerate(captions[i]):
                    draw.text((x, y + frame_h + 10 + k * line), text, font=font, fill=(20, 20, 20))
            y += height + gutter
        if notes:
            needed = len(notes) * 26 + 20
            if y + needed > page_h - margin:
                current, y = new_page()
            draw = ImageDraw.Draw(current)
            for k, text in enumerate(notes):
                draw.text((margin, y + 10 + k * 26), text, font=fonts['notes'], fill=(40, 40, 40))
        for n, image in enumerate(pages, 1):
            ImageDraw.Draw(image).text((page_w - margin - 70, page_h - margin + 18), f'{n} / {len(pages)}', font=fonts['body'], fill=(110, 110, 110))
        targets = [folder / f'{stem}-p{n}.png' for n in range(1, len(pages) + 1)] + [folder / f'{stem}.pdf']
        existing = [str(p) for p in targets if p.exists()]
        if existing:
            raise InputError(f'output exists: {", ".join(existing)}')
        folder.mkdir(parents=True, exist_ok=True)
        for image, path in zip(pages, targets):
            image.save(path)
        pages[0].save(targets[-1], 'PDF', resolution=150, save_all=True, append_images=pages[1:])
    except (OSError, ValueError, InputError) as error:
        sys.stderr.write(f'{error}\n')
        return 2
    print(json.dumps({'pages': len(pages), 'panels': len(panels), 'files': [str(p) for p in targets]}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
