"""Map website evidence onto Studio's brand kit template and keep a ledger of where each value came from."""
import colorsys
import re

UNKNOWN = 'Unknown'
ROLE_NOTES = {
    'primary': 'headlines, buttons', 'accent': 'highlights', 'text': 'body text', 'background': 'backgrounds',
}


def _rgb(hex_):
    return [int(hex_[i:i + 2], 16) / 255 for i in (1, 3, 5)]


def luminance(hex_):
    """WCAG relative luminance, 0 (black) to 1 (white)."""
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in _rgb(hex_)]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def is_saturated(hex_):
    r, g, b = _rgb(hex_)
    _, lightness, saturation = colorsys.rgb_to_hls(r, g, b)
    return saturation >= 0.25 and (max(r, g, b) - min(r, g, b)) >= 0.1 and 0.08 < lightness < 0.92


def distinct(a, b):
    """True when two colours differ by more than a shade: hue at least 20 degrees or lightness 0.2 apart."""
    ha, la, _ = colorsys.rgb_to_hls(*_rgb(a))
    hb, lb, _ = colorsys.rgb_to_hls(*_rgb(b))
    hue = abs(ha - hb) * 360
    return min(hue, 360 - hue) >= 20 or abs(la - lb) >= 0.2


def _pick(colours, test, prefer=()):
    """Most used colour passing `test`; colours with a preferred use come first."""
    candidates = [c for c in colours if test(c)]
    candidates.sort(key=lambda c: (not any(u in c['uses'] for u in prefer), -c['count']))
    return candidates[0] if candidates else None


def _name(meta):
    if meta.get('site_name'):
        return meta['site_name'].strip()
    title = re.split(r'\s+[|–—:-]\s+', meta.get('title', '').strip())[0]
    return title or UNKNOWN


def draft(evidence):
    """Return (kit, ledger). The kit has exactly the template's fields; nothing about tone or rights is guessed."""
    ledger = []

    def note(field, value, status, evidence_text='', extra=''):
        ledger.append({'field': field, 'value': value, 'status': status, 'evidence': evidence_text, 'note': extra})

    meta = evidence.get('meta', {})
    name = _name(meta)
    note('name', name, 'observed' if name != UNKNOWN else 'unknown',
         f"og:site_name or <title> on {meta.get('url', evidence.get('start_url'))}")

    colours, used = evidence.get('colours', []), set()

    def role(field, test, prefer):
        chosen = _pick([c for c in colours if c['hex'] not in used], test, prefer)
        if not chosen:
            note(f'colours.{field}', UNKNOWN, 'unknown', 'no matching colour in the inspected CSS')
            return {'hex': UNKNOWN, 'role': ROLE_NOTES[field]}
        used.add(chosen['hex'])
        source = f"{chosen['count']} uses ({', '.join(chosen['uses'])}) in {', '.join(chosen['sources'][:3])}"
        if chosen['variables']:
            source += f"; CSS variable {', '.join(chosen['variables'])}"
        note(f'colours.{field}', chosen['hex'], 'inferred', source, 'CSS value, not a pixel sample')
        return {'hex': chosen['hex'], 'role': ROLE_NOTES[field]}

    kit_colours = {}
    kit_colours['background'] = role('background', lambda c: luminance(c['hex']) > 0.6 and
                                     {'page-background', 'background'} & set(c['uses']), ('page-background',))
    kit_colours['text'] = role('text', lambda c: luminance(c['hex']) < 0.2 and
                               {'body-text', 'text'} & set(c['uses']), ('body-text',))
    kit_colours['primary'] = role('primary', lambda c: is_saturated(c['hex']), ('button', 'link'))
    primary = kit_colours['primary']['hex']
    kit_colours['accent'] = role('accent', lambda c: is_saturated(c['hex']) and
                                 (primary == UNKNOWN or distinct(c['hex'], primary)), ())
    if kit_colours['background']['hex'] == UNKNOWN and any(
            luminance(c['hex']) < 0.2 and 'page-background' in c['uses'] for c in colours):
        note('colours.background', UNKNOWN, 'unknown', 'the page background is dark',
             'a dark-themed site: confirm the background and text roles with the user')
    kit_colours = {k: kit_colours[k] for k in ('primary', 'accent', 'text', 'background')}

    fonts = evidence.get('fonts', [])

    def font(field, wanted):
        chosen = next((f for f in fonts if wanted in f['roles']), None)
        if not chosen:
            note(f'fonts.{field}', UNKNOWN, 'unknown', f'no font-family on {wanted} selectors')
            return {'font': UNKNOWN, 'licence': UNKNOWN}
        served = [l for l in evidence.get('font_links', []) if chosen['family'].replace(' ', '+') in l]
        note(f'fonts.{field}', chosen['family'], 'observed', f"font-family on {wanted} selectors in "
             f"{', '.join(chosen['sources'][:3])}" + (f'; served by {served[0]}' if served else ''),
             'declared font, not a verified rendered face; licence Unknown')
        return {'font': chosen['family'], 'licence': UNKNOWN}

    kit_fonts = {'headline': font('headline', 'heading'), 'body': font('body', 'body')}

    logos = evidence.get('logos', [])
    main = next((l for l in logos if l['kind'] in ('header-img', 'logo-img') and l.get('url')), None)
    mark = next((l for l in logos if l['kind'] == 'apple-touch-icon'), None)
    files = {'colour': UNKNOWN, 'white': UNKNOWN, 'mark': UNKNOWN}
    if main:
        files['colour'] = main['url']
        note('logo.files.colour', main['url'], 'observed', f"{main['kind']} on {main.get('page')}",
             'url-not-downloaded; rights, clear space and minimum size Unknown')
    elif any(l['kind'] == 'header-svg' for l in logos):
        note('logo.files.colour', UNKNOWN, 'unknown', 'inline SVG in the header', 'export the SVG from the page')
    else:
        note('logo.files.colour', UNKNOWN, 'unknown', 'no logo image found')
    if mark:
        files['mark'] = mark['url']
        note('logo.files.mark', mark['url'], 'inferred', 'apple-touch-icon', 'url-not-downloaded; an icon, '
             'confirm it is the brand mark')
    note('logo.files.white', UNKNOWN, 'unknown', '', 'a white version is rarely on the page; ask the user')

    note('voice', UNKNOWN, 'unknown', 'copy sample in evidence.json',
         'tone, address and phrases are written by the model from quoted copy and approved by the user')
    note('claims', UNKNOWN, 'unknown', 'website copy', 'observed wording is not an approved claim')

    kit = {
        'schema_version': 1,
        'name': name,
        'spelling': UNKNOWN,
        'colours': kit_colours,
        'fonts': kit_fonts,
        'logo': {'files': files, 'min_width_px': UNKNOWN, 'clear_space': UNKNOWN},
        'voice': {'address': UNKNOWN, 'tone': [], 'use': [], 'avoid': []},
        'claims': {'approved': [], 'banned': []},
        'legal_lines': [],
        'do_not': [],
    }
    return kit, ledger
