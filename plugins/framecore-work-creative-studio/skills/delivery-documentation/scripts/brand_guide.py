#!/usr/bin/env python3
"""Lay out a brand guide as PNG pages and one PDF from the client's brand kit, with exact text.

  python3 brand_guide.py brand-kit.json --out-dir guide/                     # brand-guide.pdf, brand-guide-p1.png ...
  python3 brand_guide.py brand-kit.json --logo-dir logo/ --out-dir guide/    # logo renders from svg_wordmark.py
  python3 brand_guide.py brand-kit.json --out-dir guide/ --draft             # allowed with unfilled {placeholders}

The kit follows pipeline-core/assets/brand-kit.template.json (paths inside it are relative to it); a "version" field is
printed on the cover. Sections: cover, logo (colour, reversed and black versions, clear space, proposed minimum size),
colours (HEX, RGB, CMYK only where the kit gives it, WCAG contrast against the background and white), typography
(samples set in the named font when it is bundled or supplied as "file"), voice and claims, and the kit's own
"do not" list. Labels are English or Polish (--language pl, or "language": "pl" in the kit). Nothing is invented: a missing logo, font or value is printed as missing. Unfilled template placeholders
stop the run unless --draft marks every page DRAFT. Text is set in the bundled Inter with Polish no-break rules,
wraps and continues on the next page; nothing is cut. Needs Pillow.
Exit codes: 0 written, 2 bad input, unfilled placeholders without --draft, a missing file or an output that exists.
"""
import argparse
import datetime
import json
import re
import sys
from pathlib import Path

FONTS = Path(__file__).resolve().parents[2] / 'pipeline-core/assets/fonts'
PAGE = (1754, 1240)
MARGIN = 90
HEX = re.compile(r'^#[0-9A-Fa-f]{6}$')
PLACEHOLDER = re.compile(r'\{[^{}]+\}')
UNIT = r'(?:zł|gr|kg|km|cm|mm|ml|min|PLN|EUR|USD|px|[gmlhs])(?![^\W\d_])|%'
LABELS = {
    'en': {'guide': 'Brand guide', 'version': 'version', 'continued': 'continued', 'logo': 'Logo', 'colours': 'Colours',
           'typography': 'Typography', 'voice': 'Voice and claims', 'do_not': 'Do not', 'on_ground': 'On the background colour',
           'reversed': 'Reversed, on the primary colour', 'black': 'One colour, black', 'no_file': 'file not supplied',
           'clear': 'Clear space: {}.', 'min': 'Minimum width: {} px proposed; confirm it at the real sizes and on the real media.',
           'cmyk_unknown': "CMYK: Unknown until converted with the printer's profile", 'contrast': 'Contrast (WCAG ratio; 4.5 for body text, 3 for large text):',
           'on': '{} on {}', 'white_on': 'white on {}', 'body_ok': 'body text', 'large_ok': 'large text only', 'not_text': 'not for text',
           'licence': 'licence', 'no_licence': 'licence: not stated', 'not_named': 'not named',
           'no_sample': 'Sample not set: the font file is neither bundled nor supplied ("file" in the kit).',
           'name': 'Name', 'address': 'Address', 'tone': 'Tone', 'says': 'The brand says', 'never': 'The brand never says',
           'approved': 'Approved claims and where each is proven:', 'source': 'source', 'unstated': 'not stated',
           'banned': 'Claims the brand must not make:', 'legal': 'Required lines:', 'draft': 'DRAFT',
           'no_logo': 'No logo file was supplied; this guide shows no logo.', 'logo_missing': 'Logo file not found: {} ({}).',
           'wordmark': 'Wordmark set in {} {} ({}), outlined vector paths in wordmark.svg.', 'cap': 'the cap height of the wordmark on every side'},
    'pl': {'guide': 'Księga znaku', 'version': 'wersja', 'continued': 'ciąg dalszy', 'logo': 'Znak', 'colours': 'Kolory',
           'typography': 'Typografia', 'voice': 'Język i deklaracje', 'do_not': 'Czego nie robić', 'on_ground': 'Na kolorze tła',
           'reversed': 'W kontrze, na kolorze głównym', 'black': 'Jednobarwny, czarny', 'no_file': 'brak pliku',
           'clear': 'Pole ochronne: {}.', 'min': 'Minimalna szerokość: {} px (propozycja); sprawdź w rzeczywistych rozmiarach i na docelowych nośnikach.',
           'cmyk_unknown': 'CMYK: nieznany do czasu konwersji profilem drukarni', 'contrast': 'Kontrast (współczynnik WCAG; 4,5 dla tekstu, 3 dla dużego tekstu):',
           'on': '{} na {}', 'white_on': 'biały na {}', 'body_ok': 'tekst', 'large_ok': 'tylko duży tekst', 'not_text': 'nie do tekstu',
           'licence': 'licencja', 'no_licence': 'licencja: nie podano', 'not_named': 'nie podano',
           'no_sample': 'Próbka nie złożona: pliku fontu nie ma w pakiecie ani w zestawie („file” w zestawie marki).',
           'name': 'Nazwa', 'address': 'Forma zwracania się', 'tone': 'Ton', 'says': 'Marka mówi', 'never': 'Marka nigdy nie mówi',
           'approved': 'Zatwierdzone deklaracje i ich potwierdzenie:', 'source': 'źródło', 'unstated': 'nie podano',
           'banned': 'Deklaracje, których marka nie składa:', 'legal': 'Wymagane informacje:', 'draft': 'WERSJA ROBOCZA',
           'no_logo': 'Nie dostarczono pliku znaku; ta księga go nie pokazuje.', 'logo_missing': 'Nie znaleziono pliku znaku: {} ({}).',
           'wordmark': 'Logotyp złożony krojem {} {} ({}), wektorowe krzywe w wordmark.svg.', 'cap': 'wysokość wersaliki logotypu z każdej strony'},
}
SAMPLE = ('Aa Bb Ćć Ęę Łł Ńń Óó Śś Źź Żż 0123456789', 'Zażółć gęślą jaźń. „Cudzysłów”, półpauza – i 1 999,00 zł')


class InputError(Exception):
    pass


def keep_together(text):
    """Polish typesetting, as in the other Studio compositors: no one-letter word at a line end, numbers kept with units."""
    text = re.sub(r'(?<!\S)([aiouwzAIOUWZ]) +(?=\S)', '\\1\u00a0', str(text))  # Polish one-letter words, not 'Wariant B'
    text = re.sub(r'(\d) (?=\d{3}(?!\d))', '\\1\u00a0', text)
    return re.sub(r'(\d) (?=' + UNIT + ')', '\\1\u00a0', text)


def rgb(value):
    return tuple(int(value[i:i + 2], 16) for i in (1, 3, 5))


def luminance(colour):
    def channel(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (channel(c) for c in colour)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def placeholders(value, where=''):
    found = []
    if isinstance(value, dict):
        for key, item in value.items():
            found += placeholders(item, f'{where}.{key}' if where else key)
    elif isinstance(value, list):
        for i, item in enumerate(value):
            found += placeholders(item, f'{where}[{i}]')
    elif isinstance(value, str) and PLACEHOLDER.search(value):
        found.append(where)
    return found


def font_file(entry, base):
    """A kit font as a file: "file" relative to the kit, else a bundled font whose file name matches the name."""
    if entry.get('file'):
        path = (base / entry['file']).resolve()
        return path if path.is_file() else None
    wanted = re.sub(r'[\s_-]+', '', str(entry.get('font', ''))).lower()
    for path in sorted(FONTS.glob('*/*.ttf')):
        if re.sub(r'[\s_-]+', '', path.stem).lower() == wanted:
            return path
    return None


def main(argv=None):
    parser = argparse.ArgumentParser(description='Compose a brand guide (PNG pages and a PDF) from a brand kit.')
    parser.add_argument('kit')
    parser.add_argument('--out-dir', required=True)
    parser.add_argument('--logo-dir', help='folder written by svg_wordmark.py; its renders replace the kit logo files')
    parser.add_argument('--draft', action='store_true', help='allow unfilled placeholders and mark every page DRAFT')
    parser.add_argument('--date', help='date on the cover (default: today)')
    parser.add_argument('--language', choices=sorted(LABELS), help='language of the guide labels (default: the kit\'s "language", else en)')
    args = parser.parse_args(argv)
    try:
        try:
            from PIL import Image, ImageDraw, ImageFont
        except ImportError:
            raise InputError('the brand guide needs Pillow (python3 -m pip install pillow)')
        source = Path(args.kit)
        kit = json.loads(source.read_text(encoding='utf-8'))
        if not isinstance(kit, dict) or not str(kit.get('name', '')).strip():
            raise InputError('the brand kit needs at least a name')
        base = source.parent
        L = LABELS[args.language or (kit.get('language') if kit.get('language') in LABELS else 'en')]
        unfilled = placeholders(kit)
        if unfilled and not args.draft:
            raise InputError('fill these fields or pass --draft: ' + ', '.join(unfilled))
        try:
            F = {k: ImageFont.truetype(str(FONTS / f'inter/Inter-{style}.ttf'), size) for k, (style, size) in {
                'cover': ('Black', 92), 'title': ('Bold', 40), 'head': ('Bold', 26), 'body': ('Regular', 24),
                'small': ('Regular', 20), 'mark': ('Bold', 20)}.items()}
        except OSError:
            raise InputError(f'Inter-Regular.ttf, Inter-Bold.ttf and Inter-Black.ttf are needed in {FONTS / "inter"}')
        colours = {}
        for name, entry in (kit.get('colours') or {}).items():
            value = entry.get('hex') if isinstance(entry, dict) else entry
            if not (isinstance(value, str) and HEX.match(value)):
                raise InputError(f'colour {name}: hex must be #RRGGBB')
            colours[name] = {'hex': value.upper(), 'rgb': rgb(value), 'role': (entry.get('role') if isinstance(entry, dict) else '') or '',
                             'cmyk': entry.get('cmyk') if isinstance(entry, dict) else None}
        ground = colours.get('background', {}).get('rgb', (255, 255, 255))
        ink = colours.get('text', {}).get('rgb', (20, 20, 20))
        primary = colours.get('primary', {}).get('rgb', ink)

        # Logo files: the wordmark folder, else the kit's own files; missing files are reported, never drawn.
        logo = kit.get('logo') or {}
        logos, logo_notes = {}, []
        if args.logo_dir:
            folder = Path(args.logo_dir)
            for key, stem in (('colour', 'wordmark'), ('white', 'wordmark-white'), ('black', 'wordmark-black')):
                if (folder / f'{stem}.png').is_file():
                    logos[key] = folder / f'{stem}.png'
            if (folder / 'wordmark.json').is_file():
                report = json.loads((folder / 'wordmark.json').read_text(encoding='utf-8'))
                logo_notes.append(L['wordmark'].format(report['font']['family'], report['font']['style'], report['font']['licence'].split(':')[0].split(' (')[0]))
                logo.setdefault('clear_space', L['cap'])
        for key, name in (logo.get('files') or {}).items():
            if key not in logos:
                path = base / name
                if path.is_file():
                    logos[key] = path
                else:
                    logo_notes.append(L['logo_missing'].format(name, key))
        if not logos:
            logo_notes.append(L['no_logo'])

        def load(key):
            return Image.open(logos[key]).convert('RGBA') if key in logos else None

        # ----------------------------------------------------------------- page machinery
        pages, missing_fonts = [], []
        width = PAGE[0] - 2 * MARGIN

        def wrap(text, font, limit):
            if any(font.getlength(char) > limit for char in text if not char.isspace()):
                raise ValueError('a glyph is wider than the text box')
            lines = []
            for paragraph in keep_together(text).split('\n'):
                current = ''
                for word in paragraph.split(' '):
                    trial = word if not current else f'{current} {word}'
                    if current and font.getlength(trial) > limit:
                        while font.getlength(current) > limit:
                            cut = max(1, next((n for n in range(len(current), 0, -1) if font.getlength(current[:n]) <= limit), 1))
                            lines.append(current[:cut])
                            current = current[cut:]
                        lines.append(current)
                        current = word
                    else:
                        current = trial
                while font.getlength(current) > limit:
                    cut = max(1, next((n for n in range(len(current), 0, -1) if font.getlength(current[:n]) <= limit), 1))
                    lines.append(current[:cut])
                    current = current[cut:]
                lines.append(current)
            return lines

        class Section:
            def __init__(self, title):
                self.title, self.page, self.y = title, None, 0
                self.new_page()

            def new_page(self, continued=False):
                image = Image.new('RGB', PAGE, 'white')
                draw = ImageDraw.Draw(image)
                draw.text((MARGIN, MARGIN - 30), str(kit['name']), font=F['small'], fill=(110, 110, 110))
                draw.text((MARGIN, MARGIN), self.title + (f" ({L['continued']})" if continued else ''), font=F['title'], fill=(15, 15, 15))
                pages.append(image)
                self.page, self.draw, self.y = image, draw, MARGIN + 80

            def room(self, height):
                if self.y + height > PAGE[1] - MARGIN - 30:
                    self.new_page(True)

            def text(self, value, font='body', colour=(30, 30, 30), gap=10, indent=0):
                for line in wrap(value, F[font], width - indent):
                    height = F[font].size + 10
                    self.room(height)
                    self.draw.text((MARGIN + indent, self.y), line, font=F[font], fill=colour)
                    self.y += height
                self.y += gap

            def bullets(self, items):
                for item in items:
                    lines = wrap(str(item), F['body'], width - 34)
                    for k, line in enumerate(lines):
                        self.room(34)
                        if k == 0:
                            self.draw.text((MARGIN, self.y), '•', font=F['body'], fill=(30, 30, 30))
                        self.draw.text((MARGIN + 34, self.y), line, font=F['body'], fill=(30, 30, 30))
                        self.y += 34
                self.y += 8

        # ----------------------------------------------------------------- cover
        cover = Image.new('RGB', PAGE, ground)
        draw = ImageDraw.Draw(cover)
        art = load('colour')
        if art:
            art.thumbnail((int(PAGE[0] * 0.5), int(PAGE[1] * 0.32)), Image.LANCZOS)
            cover.paste(art, ((PAGE[0] - art.width) // 2, int(PAGE[1] * 0.3)), art)
        else:
            name_w = F['cover'].getlength(str(kit['name']))
            draw.text(((PAGE[0] - name_w) / 2, PAGE[1] * 0.36), str(kit['name']), font=F['cover'], fill=ink)
        line = L['guide'] + (f" · {L['version']} {kit['version']}" if kit.get('version') else '') + f" · {args.date or datetime.date.today().isoformat()}"
        draw.text(((PAGE[0] - F['head'].getlength(line)) / 2, PAGE[1] * 0.74), line, font=F['head'], fill=ink)
        pages.append(cover)

        # ----------------------------------------------------------------- logo
        section = Section(L['logo'])
        tiles = [('colour', ground, L['on_ground']), ('white', primary, L['reversed']), ('black', (255, 255, 255), L['black'])]
        tile_w, tile_h, x = (width - 2 * 30) // 3, 330, MARGIN
        section.room(tile_h + 60)
        for key, fill, caption in tiles:
            section.draw.rectangle([x, section.y, x + tile_w, section.y + tile_h], fill=fill, outline=(210, 210, 210))
            art = load(key)
            if art:
                art.thumbnail((tile_w - 80, tile_h - 120), Image.LANCZOS)
                section.page.paste(art, (x + (tile_w - art.width) // 2, section.y + (tile_h - art.height) // 2), art)
            else:
                section.draw.text((x + 24, section.y + tile_h // 2 - 12), L['no_file'], font=F['small'], fill=(150, 150, 150))
            section.draw.text((x, section.y + tile_h + 10), caption, font=F['small'], fill=(80, 80, 80))
            x += tile_w + 30
        section.y += tile_h + 60
        if logo.get('clear_space'):
            section.text(L['clear'].format(logo['clear_space']))
        if logo.get('min_width_px'):
            section.text(L['min'].format(logo['min_width_px']))
        for note in logo_notes:
            section.text(note, font='small', colour=(90, 90, 90))

        # ----------------------------------------------------------------- colours
        section = Section(L['colours'])
        contrast_rows = []
        for name, c in colours.items():
            section.room(150)
            section.draw.rectangle([MARGIN, section.y, MARGIN + 220, section.y + 130], fill=c['rgb'], outline=(210, 210, 210))
            cmyk = f"CMYK {c['cmyk']}" if c['cmyk'] else L['cmyk_unknown']
            lines = [(f"{name}" + (f": {c['role']}" if c['role'] else ''), 'head'), (f"HEX {c['hex']} · RGB {c['rgb'][0]} {c['rgb'][1]} {c['rgb'][2]}", 'body'), (cmyk, 'small')]
            y = section.y + 8
            for text, font in lines:
                for part in wrap(text, F[font], width - 260):
                    section.draw.text((MARGIN + 250, y), part, font=F[font], fill=(30, 30, 30))
                    y += F[font].size + 10
            section.y = max(section.y + 150, y + 10)
            if name != 'background' and 'background' in colours:
                contrast_rows.append((L['on'].format(name, 'background'), contrast(c['rgb'], ground)))
            if name != 'background':
                contrast_rows.append((L['white_on'].format(name), contrast((255, 255, 255), c['rgb'])))
        if contrast_rows:
            section.text(L['contrast'], font='head', gap=4)
            section.bullets([f"{label}: {ratio:.2f}".replace('.', ',' if L is LABELS['pl'] else '.') + ", " + (L['body_ok'] if ratio >= 4.5 else L['large_ok'] if ratio >= 3 else L['not_text']) for label, ratio in contrast_rows])

        # ----------------------------------------------------------------- typography
        section = Section(L['typography'])
        for role, entry in (kit.get('fonts') or {}).items():
            entry = entry if isinstance(entry, dict) else {'font': entry}
            section.text(f"{role}: {entry.get('font', L['not_named'])}" + (f" · {L['licence']}: {entry['licence']}" if entry.get('licence') else f" · {L['no_licence']}"), font='head', gap=4)
            path = font_file(entry, base)
            if path:
                for size in (64, 30):
                    face = ImageFont.truetype(str(path), size)
                    for sample in SAMPLE[:1] if size == 64 else SAMPLE[1:]:
                        for part in wrap(sample, face, width):
                            section.room(size + 18)
                            section.draw.text((MARGIN, section.y), part, font=face, fill=ink)
                            section.y += size + 18
                section.y += 16
            else:
                missing_fonts.append(entry.get('font'))
                section.text(L['no_sample'], font='small', colour=(150, 60, 60))

        # ----------------------------------------------------------------- voice and claims
        voice, claims = kit.get('voice') or {}, kit.get('claims') or {}
        if voice or claims or kit.get('legal_lines') or kit.get('spelling'):
            section = Section(L['voice'])
            if kit.get('spelling'):
                section.text(f"{L['name']}: {kit['spelling']}")
            if voice.get('address'):
                section.text(f"{L['address']}: {voice['address']}")
            if voice.get('tone'):
                section.text(f"{L['tone']}: " + ', '.join(map(str, voice['tone'])))
            for key, label in (('use', L['says']), ('avoid', L['never'])):
                if voice.get(key):
                    section.text(label + ':', font='head', gap=4)
                    section.bullets(voice[key])
            if claims.get('approved'):
                section.text(L['approved'], font='head', gap=4)
                section.bullets([f"{c.get('text')} ({L['source']}: {c.get('source') or L['unstated']})" if isinstance(c, dict) else str(c) for c in claims['approved']])
            if claims.get('banned'):
                section.text(L['banned'], font='head', gap=4)
                section.bullets(claims['banned'])
            if kit.get('legal_lines'):
                section.text(L['legal'], font='head', gap=4)
                section.bullets(kit['legal_lines'])
        if kit.get('do_not'):
            section = Section(L['do_not'])
            section.bullets(kit['do_not'])

        for n, image in enumerate(pages, 1):
            d = ImageDraw.Draw(image)
            d.text((PAGE[0] - MARGIN - 80, PAGE[1] - MARGIN + 30), f'{n} / {len(pages)}', font=F['small'], fill=(120, 120, 120))
            if args.draft:
                d.text((PAGE[0] - MARGIN - F['mark'].getlength(L['draft']), MARGIN - 30), L['draft'], font=F['mark'], fill=(200, 40, 40))
        folder = Path(args.out_dir)
        targets = [folder / f'brand-guide-p{n}.png' for n in range(1, len(pages) + 1)] + [folder / 'brand-guide.pdf']
        existing = [str(p) for p in targets if p.exists()]
        if existing:
            raise InputError('output exists: ' + ', '.join(existing))
        folder.mkdir(parents=True, exist_ok=True)
        for image, path in zip(pages, targets):
            image.save(path)
        pages[0].save(targets[-1], 'PDF', resolution=150, save_all=True, append_images=pages[1:])
    except (OSError, ValueError, KeyError, InputError) as error:
        sys.stderr.write(f'{error}\n')
        return 2
    print(json.dumps({'pages': len(pages), 'files': [str(p) for p in targets], 'logo_files': {k: str(v) for k, v in logos.items()},
                      'fonts_without_sample': missing_fonts, 'unfilled': unfilled, 'draft': args.draft}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
