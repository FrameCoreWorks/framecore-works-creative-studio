#!/usr/bin/env python3
"""Build Studio's bundled fonts: static instances of pinned Google Fonts sources, subset to Latin with Polish.

  python3 scripts/build_fonts.py SOURCE_DIR        # SOURCE_DIR/<family>/<file> downloaded from google/fonts at COMMIT

Needs fontTools (pip install fonttools==4.60.1). Writes the TTF files, each family's OFL.txt and fonts.json into the
package's shared font folder. Every source in this list is OFL 1.1 without a Reserved Font Name, so a subset static
instance may keep its family name; fonts.json records the source commit, the source and output SHA-256, the axis
coordinates and the character ranges. Run it again only to change the set; the result is byte-stable for the same
sources and fontTools version.
"""
import hashlib
import json
import sys
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'plugins/framecore-work-creative-studio/skills/pipeline-core/assets/fonts'
COMMIT = 'bd8f81ddb5c74d5c8897b36ad88b440266245103'
SOURCE_URL = 'https://github.com/google/fonts/blob/{commit}/ofl/{folder}/{file}'
# Latin, Latin-1, Latin Extended-A (Polish and the rest of Central Europe), Romanian comma letters, spacing accents,
# general punctuation (dashes, „” quotes, ellipsis, thin and non-breaking spaces), currency, letterlike, arrows, math, shapes, fi/fl.
UNICODES = ('U+0020-007E,U+00A0-017F,U+0218-021B,U+02C6-02DD,U+2000-206F,U+20A0-20CF,U+2100-214F,'
            'U+2190-21FF,U+2212,U+2215,U+2219,U+221E,U+2248,U+2260,U+2264,U+2265,U+25A0-25FF,U+FB01-FB02')

FAMILIES = [
    {'family': 'Inter', 'folder': 'inter', 'file': 'Inter[opsz,wght].ttf', 'role': 'neutral sans for interfaces, body text, prices and small print',
     'instances': [('Inter-Regular', 'Regular', {'wght': 400, 'opsz': 14}), ('Inter-SemiBold', 'SemiBold', {'wght': 600, 'opsz': 14}),
                   ('Inter-Bold', 'Bold', {'wght': 700, 'opsz': 32}), ('Inter-Black', 'Black', {'wght': 900, 'opsz': 32})]},
    {'family': 'Archivo', 'folder': 'archivo', 'file': 'Archivo[wdth,wght].ttf', 'role': 'grotesque with condensed and expanded widths for posters and sale headlines',
     'instances': [('Archivo-Regular', 'Regular', {'wght': 400, 'wdth': 100}), ('Archivo-Bold', 'Bold', {'wght': 700, 'wdth': 100}),
                   ('Archivo-CondensedExtraBold', 'Condensed ExtraBold', {'wght': 800, 'wdth': 62}),
                   ('Archivo-ExpandedBlack', 'Expanded Black', {'wght': 900, 'wdth': 125})]},
    {'family': 'Bricolage Grotesque', 'folder': 'bricolagegrotesque', 'file': 'BricolageGrotesque[opsz,wdth,wght].ttf',
     'role': 'characterful display grotesque for lifestyle, events and friendly brands',
     'instances': [('BricolageGrotesque-Regular', 'Regular', {'wght': 400, 'wdth': 100, 'opsz': 14}),
                   ('BricolageGrotesque-Bold', 'Bold', {'wght': 700, 'wdth': 100, 'opsz': 96}),
                   ('BricolageGrotesque-CondensedExtraBold', 'Condensed ExtraBold', {'wght': 800, 'wdth': 75, 'opsz': 96})]},
    {'family': 'Fraunces', 'folder': 'fraunces', 'file': 'Fraunces[SOFT,WONK,opsz,wght].ttf', 'role': 'soft display serif for food, craft, culture and premium',
     'instances': [('Fraunces-Regular', 'Regular', {'wght': 400, 'opsz': 72, 'SOFT': 0, 'WONK': 0}),
                   ('Fraunces-SemiBold', 'SemiBold', {'wght': 600, 'opsz': 72, 'SOFT': 50, 'WONK': 0}),
                   ('Fraunces-Black', 'Black', {'wght': 900, 'opsz': 144, 'SOFT': 100, 'WONK': 1})]},
    {'family': 'Anton', 'folder': 'anton', 'file': 'Anton-Regular.ttf', 'role': 'tall condensed impact face for one-word headlines and prices',
     'instances': [('Anton-Regular', 'Regular', {})]},
    {'family': 'Source Serif 4', 'folder': 'sourceserif4', 'file': 'SourceSerif4[opsz,wght].ttf', 'role': 'reading serif for long copy, menus, programmes and print body text',
     'instances': [('SourceSerif4-Regular', 'Regular', {'wght': 400, 'opsz': 16}), ('SourceSerif4-SemiBold', 'SemiBold', {'wght': 600, 'opsz': 16}),
                   ('SourceSerif4-Bold', 'Bold', {'wght': 700, 'opsz': 36})]},
]


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def rename(font, family, style):
    """Keep the family; give each static instance its own style, full and PostScript names."""
    names = font['name']
    postscript = (family.replace(' ', '') + '-' + style.replace(' ', ''))
    plain = style in ('Regular', 'Bold')
    for record_id, value in ((1, family if plain else f'{family} {style}'), (2, style if plain else 'Regular'),
                             (4, f'{family} {style}'), (6, postscript), (16, family), (17, style)):
        names.setName(value, record_id, 3, 1, 0x409)
    names.names = [n for n in names.names if not (n.platformID == 1)]  # drop legacy Mac names
    for record_id in (25,):  # variations PostScript prefix no longer applies
        names.removeNames(nameID=record_id)


def build(source_dir):
    source_dir = Path(source_dir)
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {'schema_version': 1, 'source': 'google/fonts', 'source_commit': COMMIT, 'licence': 'SIL Open Font License 1.1 (each family folder holds its OFL.txt); no Reserved Font Name in any source',
                'modification': 'static instances of the variable sources at the listed coordinates, subset to the listed characters keeping kerning, ligatures, marks, localized forms, fractions and the figure, case and superscript features; hinting removed',
                'unicodes': UNICODES, 'families': []}
    options = subset.Options()
    options.layout_features = list(options.layout_features) + ['tnum', 'lnum', 'pnum', 'onum', 'case', 'zero', 'sups', 'subs', 'ordn']
    options.name_IDs = ['*']
    options.name_languages = ['*']
    options.hinting = False
    options.notdef_outline = True
    options.glyph_names = False
    options.drop_tables += ['DSIG', 'STAT']
    unicodes = subset.parse_unicodes(UNICODES)
    for spec in FAMILIES:
        source = source_dir / spec['folder'] / spec['file']
        licence = (source_dir / spec['folder'] / 'OFL.txt').read_bytes()
        if b'Reserved Font Name "' in licence:
            raise SystemExit(f'{spec["family"]} has a Reserved Font Name; a modified version would need a new name')
        folder = OUT / spec['folder']
        folder.mkdir(exist_ok=True)
        (folder / 'OFL.txt').write_bytes(licence)
        entry = {'family': spec['family'], 'role': spec['role'], 'folder': spec['folder'],
                 'source': SOURCE_URL.format(commit=COMMIT, folder=spec['folder'], file=spec['file']).replace('[', '%5B').replace(']', '%5D').replace(',', '%2C'),
                 'source_sha256': sha256(source.read_bytes()), 'licence_sha256': sha256(licence), 'files': []}
        for name, style, axes in spec['instances']:
            font = TTFont(source)
            if axes:
                font = instancer.instantiateVariableFont(font, axes, updateFontNames=False)
            rename(font, spec['family'], style)
            subsetter = subset.Subsetter(options)
            subsetter.populate(unicodes=unicodes)
            subsetter.subset(font)
            target = folder / f'{name}.ttf'
            font.save(target, reorderTables=True)
            data = target.read_bytes()
            entry['files'].append({'file': f'{spec["folder"]}/{name}.ttf', 'style': style, 'axes': axes, 'bytes': len(data), 'sha256': sha256(data),
                                   'glyphs': len(TTFont(target).getGlyphOrder())})
        manifest['families'].append(entry)
    (OUT / 'fonts.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    total = sum(f['bytes'] for fam in manifest['families'] for f in fam['files'])
    print(json.dumps({'families': len(manifest['families']), 'files': sum(len(f['files']) for f in manifest['families']), 'bytes': total}))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    build(sys.argv[1])
