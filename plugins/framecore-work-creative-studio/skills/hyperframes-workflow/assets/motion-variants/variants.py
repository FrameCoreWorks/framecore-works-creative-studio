#!/usr/bin/env python3
"""Brand and multiply a motion contract: apply a client's brand kit, then expand copy and language variants, each
with the render commands for every format the contract declares.

  python3 variants.py brand ad.motion.json --brand brand-kit.json --out ad-brand.motion.json
  python3 variants.py expand ad-brand.motion.json --matrix variants.json --out-dir variants/
  python3 variants.py templates                      # the bundled 9:16 ad templates

`brand` copies the kit's colours into tokens (background, foreground or text, muted, accent or primary) and, when its
headline font is a bundled font, declares that family's faces in `fonts` so the player and the renderer use the same
files; a kit font that is not bundled is named in the report for the user to supply. `expand` reads a matrix
{"variants": [{"id": "a", "copy": {...}, "tokens": {...}, "language": "pl"}], "formats": ["base", "9x16"]} and writes
one contract per variant (`<id>-<variant>.motion.json`, copyStatus "variant-draft", approval back to proposed when its
text or look changed; a brand kit that changes colours or type does the same) plus a `render-plan.json` with a check command per variant and a renderer command per variant and format. Copy overrides may only replace copy IDs the
contract already has, so a variant can never add text the layout was not checked for. Nothing is rendered here.
Exit codes: 0 written, 2 bad input or an output that exists.
"""
import re
import argparse
import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATES = HERE.parent / 'motion-scenes/templates'
FONTS = HERE.parents[2] / 'pipeline-core/assets/fonts/fonts.json'
STYLE_WEIGHTS = {'Thin': 100, 'ExtraLight': 200, 'Light': 300, 'Regular': 400, 'Medium': 500, 'SemiBold': 600, 'Bold': 700, 'ExtraBold': 800, 'Black': 900}


class InputError(Exception):
    pass


def load(path):
    try:
        return json.loads(Path(path).read_text(encoding='utf-8'))
    except (OSError, ValueError) as error:
        raise InputError(f'{path}: {error}')


def write_new(path, data):
    path = Path(path)
    if path.exists():
        raise InputError(f'Output file already exists: {path}')
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def bundled_faces(name):
    """The family and faces of a bundled font named like 'Archivo Condensed ExtraBold' or 'Inter'.

    Every plain style is declared at its weight; a special width (Condensed, Expanded) only when the kit names it, at
    the weight its last word gives (Condensed ExtraBold: 800), in place of a plain style of that weight."""
    manifest = json.loads(FONTS.read_text(encoding='utf-8'))
    for family in manifest['families']:
        if name == family['family'] or name.startswith(family['family'] + ' '):
            chosen = name[len(family['family']):].strip() or 'Regular'
            faces = {}
            for item in family['files']:
                style = item['style']
                if ' ' in style and style != chosen:
                    continue
                weight = STYLE_WEIGHTS.get(style.split(' ')[-1], 400)
                if weight not in faces or ' ' in style:
                    faces[weight] = {'family': family['family'], 'weight': weight, 'file': item['file']}
            return family['family'], [faces[w] for w in sorted(faces)], chosen
    return None, [], None


def luminance(hex_colour):
    value = hex_colour.lstrip('#')
    if len(value) == 3:
        value = ''.join(c * 2 for c in value)
    channels = [int(value[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    r, g, b = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    """WCAG contrast ratio of two #RRGGBB colours, or None when either is not one."""
    try:
        high, low = sorted((luminance(a), luminance(b)), reverse=True)
    except (ValueError, AttributeError):
        return None
    return round((high + 0.05) / (low + 0.05), 2)


def colour(kit, *roles):
    for role in roles:
        entry = (kit.get('colours') or {}).get(role)
        if entry:
            return entry['hex'] if isinstance(entry, dict) else entry
    return None


def apply_brand(score, kit):
    out = copy.deepcopy(score)
    tokens = dict(out.get('tokens') or {})
    report = {'brand': kit.get('name'), 'tokens': {}, 'fonts': None, 'notes': []}
    for token, roles in (('background', ('background',)), ('foreground', ('foreground', 'text')), ('muted', ('muted', 'secondary_text')), ('accent', ('accent', 'primary'))):
        value = colour(kit, *roles)
        if value:
            tokens[token] = value
            report['tokens'][token] = value
    headline = ((kit.get('fonts') or {}).get('headline') or {})
    name = headline.get('font') if isinstance(headline, dict) else headline
    if name:
        family, faces, chosen = bundled_faces(str(name))
        if faces:
            # The engine sets one family; the kit's headline family carries the type, with its bundled weights.
            tokens['fontFamily'] = f'{family}, Arial, sans-serif'
            out['fonts'] = faces
            report['fonts'] = {'family': family, 'faces': [f"{f['weight']} {f['file']}" for f in faces], 'headline_style': chosen}
        else:
            report['notes'].append(f'The headline font {name} is not bundled: ask the client for the font files and their licence, then declare them in "fonts".')
    out['tokens'] = tokens
    if tokens != (score.get('tokens') or {}) or out.get('fonts') != score.get('fonts'):
        # A changed look was not what the client approved: back to proposed until the branded version is approved.
        out['approval'] = {'status': 'proposed', 'revision': None, 'evidence': None}
    # Text is checked at 4.5:1 and the muted and accent colours at 3:1 against the background (WCAG large text).
    for token, needed in (('foreground', 4.5), ('muted', 3.0), ('accent', 3.0)):
        ratio = contrast(tokens.get(token), tokens.get('background'))
        if ratio is not None:
            report.setdefault('contrast', {})[token] = ratio
            if ratio < needed:
                report['notes'].append(f'{token} {tokens[token]} on background {tokens["background"]} has contrast {ratio}:1, below {needed}:1; choose another kit colour for this role or set the token by hand.')
    decisions = out.setdefault('decisions', {})
    decisions.setdefault('confirmed', [])
    note = f"Brand kit {kit.get('name', '')} applied to colours and type".strip()
    if note not in decisions['confirmed']:
        decisions['confirmed'].append(note)
    return out, report


def expand(score, matrix, stem):
    formats = matrix.get('formats') or ['base']
    known = {'base'} | {f.get('id') for f in score.get('formats') or []}
    unknown = [f for f in formats if f not in known]
    if unknown:
        raise InputError(f'formats not in the contract: {unknown}; it has {sorted(known)}')
    variants = matrix.get('variants') or []
    if not variants:
        raise InputError('the matrix needs at least one variant')
    contracts, checks, plan, seen = [], [], [], set()
    for variant in variants:
        vid = str(variant.get('id', '')).strip()
        if not vid or not vid.replace('-', '').isalnum() or vid in seen:
            raise InputError(f'variant id missing, invalid or repeated: {vid!r}; use letters, digits and hyphens')
        seen.add(vid)
        extra = set(variant.get('copy') or {}) - set(score.get('copy') or {})
        if extra:
            raise InputError(f'variant {vid}: copy IDs not in the contract: {sorted(extra)}; a variant replaces text, it does not add any')
        out = copy.deepcopy(score)
        out['id'] = f"{score.get('id', stem)}-{vid}"
        out['copy'] = {**(score.get('copy') or {}), **(variant.get('copy') or {})}
        out['tokens'] = {**(score.get('tokens') or {}), **(variant.get('tokens') or {})}
        out['copyStatus'] = 'variant-draft'
        # New words or a new look need their own approval: the variant goes back to proposed until the client approves it.
        if variant.get('copy') or out['tokens'] != (score.get('tokens') or {}):
            out['approval'] = {'status': 'proposed', 'revision': None, 'evidence': None}
        if variant.get('language'):
            out['language'] = variant['language']
        name = f'{stem}-{vid}.motion.json'
        contracts.append((name, out))
        checks.append({'variant': vid, 'contract': name, 'command': ['node', 'check-score.mjs', name, '--storyboard']})
        for fmt in formats:
            suffix = '' if fmt == 'base' else f'-{fmt}'
            command = ['python3', 'render.py', name, f'{stem}-{vid}{suffix}.mp4'] + ([] if fmt == 'base' else ['--format', fmt])
            plan.append({'variant': vid, 'format': fmt, 'contract': name, 'command': command})
    return contracts, checks, plan


def main(argv=None):
    parser = argparse.ArgumentParser(description='Apply a brand kit and expand copy and language variants of a motion contract.')
    sub = parser.add_subparsers(dest='command', required=True)
    b = sub.add_parser('brand')
    b.add_argument('contract')
    b.add_argument('--brand', required=True)
    b.add_argument('--out', required=True)
    e = sub.add_parser('expand')
    e.add_argument('contract')
    e.add_argument('--matrix', required=True)
    e.add_argument('--out-dir', required=True)
    sub.add_parser('templates')
    args = parser.parse_args(argv)
    try:
        if args.command == 'templates':
            print(json.dumps([{'file': p.name, 'goal': load(p).get('goal'), 'style': load(p).get('style')} for p in sorted(TEMPLATES.glob('*.motion-score.json'))], ensure_ascii=False, indent=2))
            return 0
        score = load(args.contract)
        if args.command == 'brand':
            out, report = apply_brand(score, load(args.brand))
            write_new(args.out, out)
            print(json.dumps({'out': args.out, **report}, ensure_ascii=False))
            return 0
        folder = Path(args.out_dir)
        if folder.exists():
            raise InputError(f'Output folder already exists: {folder}')
        stem = re.sub(r'(\.(example|motion-score|motion|shot-plan|shots|edit|board|prompts|plan|static))*\.json$', '', Path(args.contract).name)
        contracts, checks, plan = expand(score, load(args.matrix), stem)
        folder.mkdir(parents=True)
        for name, data in contracts:
            write_new(folder / name, data)
        write_new(folder / 'render-plan.json', {'note': 'Run each check first (check-score.mjs from the motion starter), review the preview, get the variant text approved, then render with the bundled render.py.', 'checks': checks, 'renders': plan})
        print(json.dumps({'out_dir': str(folder), 'contracts': [n for n, _ in contracts], 'renders': len(plan)}, ensure_ascii=False))
        return 0
    except InputError as error:
        sys.stderr.write(f'{error}\n')
        return 2


if __name__ == '__main__':
    sys.exit(main())
