#!/usr/bin/env python3
"""Convert between a Studio brand kit and the DESIGN.md + tokens.css package that design agents read.

  python3 design_md.py export brand-kit.json --out-dir design/          # DESIGN.md, tokens.css, manifest.json
  python3 design_md.py import design/DESIGN.md --tokens design/tokens.css --out brand-kit.json

DESIGN.md is the brand contract used by Open Design and other agent design tools: prose sections an agent reads before
rendering, next to tokens.css with semantic custom properties (--bg, --fg, --accent, --font-display ...). Export writes
only what the kit holds: a missing value is written as "Not stated in the brand kit", never invented. Import fills
colours and fonts from tokens.css (or from `#hex` lines in DESIGN.md) and the do-not list from a Don'ts or
Anti-patterns section; every other field stays a template placeholder for the user, and brand_guide.py then needs
--draft until they are filled. The output files must not exist yet.
Exit codes: 0 written, 2 bad input or an output that exists.
"""
import argparse
import json
import re
import sys
from pathlib import Path

HEX = re.compile(r'^#[0-9A-Fa-f]{6}$')
TOKEN_FOR = {'background': '--bg', 'text': '--fg', 'accent': '--accent', 'primary': '--primary', 'surface': '--surface',
             'muted': '--muted', 'border': '--border'}
ROLE_FOR = {v: k for k, v in TOKEN_FOR.items()}
SERIFS = ('serif', 'fraunces', 'garamond', 'playfair', 'georgia', 'times', 'merriweather', 'lora', 'baskerville')
UNSTATED = 'Not stated in the brand kit.'


def slug(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-') or 'brand'


def family(font_name):
    """'Fraunces Black' -> ('Fraunces', 'serif'); the weight words are not part of the family."""
    name = re.sub(r'\s+(?:Thin|Light|Regular|Medium|SemiBold|Semibold|Bold|ExtraBold|Black|Italic)\b.*$', '', font_name.strip())
    return name, 'serif' if any(s in name.lower() for s in SERIFS) and 'sans' not in name.lower() else 'sans-serif'


def bullets(items):
    real = [i for i in items or [] if i and not re.fullmatch(r'\{[^{}]*\}', str(i))]
    return '\n'.join(f'- {i}' for i in real) if real else UNSTATED


def export(kit):
    name = kit.get('name') or 'Brand'
    colours = {k: v for k, v in (kit.get('colours') or {}).items() if isinstance(v, dict) and HEX.match(str(v.get('hex', '')))}
    fonts = {k: v for k, v in (kit.get('fonts') or {}).items() if isinstance(v, dict) and v.get('font')}
    voice, claims, logo = kit.get('voice') or {}, kit.get('claims') or {}, kit.get('logo') or {}
    tokens = [f'/* tokens.css for {name}, exported from its Studio brand kit. Semantic names; values from the kit only. */', ':root {']
    for role, c in colours.items():
        tokens.append(f"  {TOKEN_FOR.get(role, '--color-' + slug(role))}: {c['hex'].lower()};")
    for role, f in fonts.items():
        fam, generic = family(f['font'])
        token = {'headline': '--font-display', 'display': '--font-display', 'body': '--font-body'}.get(role, '--font-' + slug(role))
        tokens.append(f'  {token}: "{fam}", {generic};')
    tokens.append('}')
    colour_lines = '\n'.join(f"- **{role.capitalize()}:** `{c['hex'].upper()}` ({TOKEN_FOR.get(role, '--color-' + slug(role))})"
                             + (f" — {c['role']}" if c.get('role') else '') for role, c in colours.items()) or UNSTATED
    font_lines = '\n'.join(f"- **{role.capitalize()}:** {f['font']}" + (f" (licence: {f['licence']})" if f.get('licence') else ' (licence: not stated)')
                           for role, f in fonts.items()) or UNSTATED
    tone = ', '.join(t for t in voice.get('tone') or [] if not str(t).startswith('{'))
    approved = [f"{c.get('text')} (source: {c.get('source') or 'not stated'})" for c in claims.get('approved') or [] if isinstance(c, dict)]
    logo_bits = [f"Files: {', '.join(f'{k}: {v}' for k, v in (logo.get('files') or {}).items())}" if logo.get('files') else '',
                 f"Minimum width: {logo['min_width_px']} px (proposed)" if logo.get('min_width_px') else '',
                 f"Clear space: {logo['clear_space']}" if logo.get('clear_space') else '']
    md = f"""# {name}

> Category: Brand kit export
> Exported from the {name} Studio brand kit. Values come from the kit; anything the kit does not state is marked so.

## 1. Visual Theme & Atmosphere

{('Tone: ' + tone + '.') if tone else UNSTATED} Spelling: {kit.get('spelling') if kit.get('spelling') and not str(kit.get('spelling')).startswith('{') else 'not stated'}.

## 2. Color Palette & Roles

{colour_lines}

Use the tokens, never new hex values. Neutrals carry most of the surface; the accent appears at most twice per screen.

## 3. Typography Rules

{font_lines}

ALL CAPS takes letter-spacing of 0.06em or more; display sizes take slightly negative tracking (Latin scripts only); at most two typefaces.

## 4. Logo

{bullets([b for b in logo_bits if b])}

## 5. Voice & Brand

- Form of address: {voice.get('address') or 'not stated'}
- Uses: {', '.join(u for u in voice.get('use') or [] if not str(u).startswith('{')) or 'not stated'}
- Avoids: {', '.join(u for u in voice.get('avoid') or [] if not str(u).startswith('{')) or 'not stated'}

## 6. Claims & Legal Lines

Approved claims:

{bullets(approved)}

Banned claims:

{bullets(claims.get('banned'))}

Required lines:

{bullets(kit.get('legal_lines'))}

## 7. Do's and Don'ts

The brand never uses or does:

{bullets(kit.get('do_not'))}

## 8. Agent Prompt Guide

Read tokens.css before rendering and use only its custom properties for colour and type. Quote brand copy, claims and legal lines exactly; never invent a claim, a metric or a logo. When something this file does not state is needed, ask instead of guessing.
"""
    manifest = {'schemaVersion': 'od-design-system-project/v1', 'id': slug(name), 'name': name, 'category': 'Brand kit export',
                'description': f'{name} design contract exported from its Studio brand kit.',
                'source': {'type': 'user', 'origin': 'FrameCore Works Creative Studio brand kit export'},
                'files': {'design': 'DESIGN.md', 'tokens': 'tokens.css'}}
    return md, '\n'.join(tokens) + '\n', manifest


def parse_tokens(css):
    return {m.group(1): m.group(2).strip() for m in re.finditer(r'(--[\w-]+)\s*:\s*([^;]+);', re.sub(r'/\*.*?\*/', '', css, flags=re.S))}


def import_design(md, css=None):
    # Every field starts as a placeholder: the template's example values are not this brand's data.
    kit = {'schema_version': 1, 'name': '{Brand name}', 'spelling': '{How the name is written and declined}',
           'colours': {'primary': {'hex': '{#RRGGBB}', 'role': '{role}'}},
           'fonts': {'headline': {'font': '{headline font}', 'licence': '{licence}'}, 'body': {'font': '{body font}', 'licence': '{licence}'}},
           'logo': {'files': {'colour': '{logo file}'}, 'min_width_px': '{px}', 'clear_space': '{clear space}'},
           'voice': {'address': '{Ty or Państwo}', 'tone': ['{three adjectives}'], 'use': ['{phrases the brand uses}'], 'avoid': ['{phrases the brand never uses}']},
           'claims': {'approved': [{'text': '{claim}', 'source': '{where it is proven}'}], 'banned': ['{claims the brand must not make}']},
           'legal_lines': ['{required lines}'], 'do_not': ['{things the brand never does}']}
    title = re.search(r'^#\s+(.+)$', md, re.M)
    kit['name'] = title.group(1).strip() if title else kit['name']
    tokens = parse_tokens(css) if css else {}
    colours, fonts = {}, {}
    for token, value in tokens.items():
        if HEX.match(value):
            role = ROLE_FOR.get(token) or (token[8:] if token.startswith('--color-') else None)
            if role:
                colours[role] = {'hex': value.upper(), 'role': f'from {token}'}
        if token in ('--font-display', '--font-body'):
            first = value.split(',')[0].strip().strip('"\'')
            fonts['headline' if token == '--font-display' else 'body'] = {'font': first, 'licence': '{licence: check before use}'}
    if not colours:
        for m in re.finditer(r'\*\*([^*:]+):?\*\*:?\s*`?(#[0-9A-Fa-f]{6})\b`?\s*(?:\(--[\w-]+\)\s*)?(?:[—-]+\s*(.+))?', md):
            role = slug(m.group(1)).replace('-', '_')
            colours.setdefault(role, {'hex': m.group(2).upper(), 'role': (m.group(3) or '').strip()[:120] or 'from DESIGN.md'})
    if colours:
        kit['colours'] = colours
    kit['fonts'].update(fonts)          # a role the tokens do not name stays a placeholder
    donts = re.search(r"^##[^\n]*(?:Don'?ts|Anti-patterns|Do not)[^\n]*\n(.*?)(?=^## |\Z)", md, re.M | re.S | re.I)
    if donts:
        items = [re.sub(r'\*\*|`', '', b).strip() for b in re.findall(r'^\s*[-*]\s+(.+)$', donts.group(1), re.M)]
        items = [i for i in items if i != UNSTATED]
        if items:
            kit['do_not'] = items[:30]
    kit['imported_from'] = 'DESIGN.md' + (' and tokens.css' if css else '')
    return kit


def main(argv=None):
    parser = argparse.ArgumentParser(description='Brand kit <-> DESIGN.md and tokens.css.')
    sub = parser.add_subparsers(dest='action', required=True)
    e = sub.add_parser('export')
    e.add_argument('kit')
    e.add_argument('--out-dir', required=True)
    i = sub.add_parser('import')
    i.add_argument('design')
    i.add_argument('--tokens')
    i.add_argument('--out', required=True)
    args = parser.parse_args(argv)
    try:
        if args.action == 'export':
            kit = json.loads(Path(args.kit).read_text(encoding='utf-8'))
            out = Path(args.out_dir)
            targets = [out / 'DESIGN.md', out / 'tokens.css', out / 'manifest.json']
            if any(t.exists() for t in targets):
                raise ValueError(f'{out} already holds a DESIGN.md, tokens.css or manifest.json')
            md, css, manifest = export(kit)
            out.mkdir(parents=True, exist_ok=True)
            targets[0].write_text(md, encoding='utf-8')
            targets[1].write_text(css, encoding='utf-8')
            targets[2].write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
            print(f'design_md: wrote {", ".join(str(t) for t in targets)}')
        else:
            out = Path(args.out)
            if out.exists():
                raise ValueError(f'{out} exists')
            md = Path(args.design).read_text(encoding='utf-8')
            css = Path(args.tokens).read_text(encoding='utf-8') if args.tokens else None
            kit = import_design(md, css)
            out.write_text(json.dumps(kit, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
            print(f"design_md: wrote {out} ({len(kit['colours'])} colours, {len(kit['fonts'])} fonts); fill the {{placeholders}} before a final guide")
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f'design_md: {error}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
