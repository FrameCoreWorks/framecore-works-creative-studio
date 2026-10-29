#!/usr/bin/env python3
"""Beat sheet: check a kinetic film's structure in beats and turn it into seconds.

    python3 beat_sheet.py beat-sheets.json --template teaser-24s
    python3 beat_sheet.py beat-sheets.json --template teaser-24s --bpm 170 --drop-seconds 10.74 --json
    python3 beat_sheet.py my-sheet.json

A sheet has bpm, beats, drop_beat and blocks of {start, end, job, ...} in beats. Blocks must start at
beat 0, follow each other without gaps or overlaps and end on the last beat; the drop must start a block.
With --drop-seconds (where the track's drop falls, from beats.py) it prints the music offset that lands
that drop on the planned beat. Needs Python 3.8+ only. Exit 1 when the sheet has errors, 2 on bad input.
"""
import argparse
import json
import sys


def check(sheet):
    """Structural errors of one sheet, as sentences; an empty list means it is valid."""
    errors = []
    bpm, beats, blocks = sheet.get('bpm'), sheet.get('beats'), sheet.get('blocks') or []
    if not isinstance(bpm, (int, float)) or bpm <= 0:
        errors.append('bpm must be a positive number')
    if not isinstance(beats, (int, float)) or beats <= 0:
        errors.append('beats must be a positive number')
    if not blocks:
        return errors + ['the sheet has no blocks']
    if blocks[0].get('start') != 0:
        errors.append(f"the first block must start at beat 0, not {blocks[0].get('start')}")
    for i, block in enumerate(blocks):
        start, end = block.get('start'), block.get('end')
        if not isinstance(start, (int, float)) or not isinstance(end, (int, float)) or end <= start:
            errors.append(f'block {i + 1} needs a start before its end')
            continue
        if i:
            previous = blocks[i - 1].get('end')
            if isinstance(previous, (int, float)) and start > previous:
                errors.append(f'gap between beat {previous} and beat {start} before block {i + 1}')
            elif isinstance(previous, (int, float)) and start < previous:
                errors.append(f'block {i + 1} starts at beat {start} and overlaps the block that ends at beat {previous}')
    last = blocks[-1].get('end')
    if isinstance(beats, (int, float)) and last != beats:
        errors.append(f'the last block ends at beat {last}, but the film has {beats} beats')
    drop = sheet.get('drop_beat')
    if drop is not None and drop not in [b.get('start') for b in blocks]:
        errors.append(f'the drop at beat {drop} does not start a block: put the biggest change on the drop')
    return errors


def timing(sheet, bpm=None, drop_seconds=None):
    """Seconds for every block at the sheet's tempo (or bpm), and the music offset for a measured drop."""
    tempo = bpm or sheet['bpm']
    beat = 60 / tempo
    plan = {'id': sheet.get('id', ''), 'bpm': tempo, 'beat_seconds': beat, 'beats': sheet['beats'],
            'duration': sheet['beats'] * beat, 'drop_beat': sheet.get('drop_beat'), 'warnings': [], 'blocks': []}
    for block in sheet['blocks']:
        plan['blocks'].append({**block, 'start_s': block['start'] * beat, 'end_s': block['end'] * beat,
                               'seconds': (block['end'] - block['start']) * beat})
    if drop_seconds is not None and plan['drop_beat'] is not None:
        offset = drop_seconds - plan['drop_beat'] * beat
        plan['music_offset'] = offset
        if offset < 0:
            plan['warnings'].append(f'the track drops {-offset:.3f} s earlier than the film needs: '
                                    'choose a later drop, a longer intro or move the planned drop beat')
    return plan


def load(path, template):
    data = json.load(open(path, encoding='utf-8'))
    if 'templates' in data:
        ids = [t.get('id') for t in data['templates']]
        if template is None:
            raise SystemExit(f'choose a template with --template: {", ".join(ids)}')
        for t in data['templates']:
            if t.get('id') == template:
                return t
        raise ValueError(f'no template {template!r}; templates: {", ".join(ids)}')
    return data


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('sheet')
    parser.add_argument('--template')
    parser.add_argument('--bpm', type=float, help="the measured tempo, used unrounded; default the sheet's")
    parser.add_argument('--drop-seconds', type=float, help="where the track's drop falls, in seconds")
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args(argv)
    try:
        sheet = load(args.sheet, args.template)
    except (OSError, ValueError) as error:
        print(f'beat_sheet: {error}', file=sys.stderr)
        return 2
    errors = check(sheet)
    if errors:
        for error in errors:
            print(f'ERROR {error}')
        return 1
    plan = timing(sheet, args.bpm, args.drop_seconds)
    if args.json:
        print(json.dumps(plan, indent=2, ensure_ascii=False))
        return 0
    print(f"{plan['id']}: {plan['bpm']:g} BPM, beat {plan['beat_seconds']:.4f} s, {plan['beats']} beats = {plan['duration']:.2f} s")
    for block in plan['blocks']:
        drop = '  <- drop' if block['start'] == plan['drop_beat'] else ''
        print(f"  beats {block['start']:>5g}-{block['end']:<5g} {block['start_s']:7.3f}-{block['end_s']:7.3f} s  {block.get('job', '')}{drop}")
    if 'music_offset' in plan:
        print(f"music offset: start the track at {plan['music_offset']:.3f} s")
    for warning in plan['warnings']:
        print(f'WARNING {warning}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
