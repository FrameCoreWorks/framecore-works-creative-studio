#!/usr/bin/env python3
"""Turn an Edit Pack's edit decision list into files an editor can import: a CMX 3600 EDL, an OpenTimelineIO
(.otio) timeline and a CSV shot list.

  python3 edit_export.py edit.json --out-dir export/          # spot.edl, spot.otio, spot-shots.csv

edit.json:
  {"title": "Spot 15s", "fps": 30, "start": "00:00:00:00",
   "clips": [{"source": "A001.mp4", "in": 1.0, "out": 3.5, "name": "hook", "note": "product in hand"},
             {"source": "B002.mov", "in": "00:00:10:12", "out": "00:00:13:00", "record_in": 2.5}]}

Times are seconds or timecodes (HH:MM:SS:FF) at the edit's frame rate; `record_in` places a clip on the timeline
(default: right after the previous one; a later start leaves a gap). Integer rates are exact; 23.976, 29.97 and 59.94
are written with their nominal timebase as non-drop-frame timecode, as editors expect for an EDL. Only standard library;
nothing is uploaded. Exit codes: 0 written, 2 bad input or an output that exists.
"""
import argparse
import csv
import io
import json
import math
import re
import sys
from pathlib import Path

NOMINAL = {23.976: 24, 29.97: 30, 59.94: 60}


class InputError(Exception):
    pass


def timebase(fps):
    for real, nominal in NOMINAL.items():
        if abs(fps - real) < 0.01:
            return nominal
    if abs(fps - round(fps)) > 1e-6 or fps <= 0:
        raise InputError(f'unsupported frame rate {fps}; use an integer rate or 23.976, 29.97, 59.94')
    return int(round(fps))


def to_frames(value, base, fps, what):
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if value < 0:
            raise InputError(f'{what}: negative time')
        return int(round(value * fps))
    match = re.fullmatch(r'(\d{2}):(\d{2}):(\d{2})[:;](\d{2})', str(value).strip())
    if not match:
        raise InputError(f'{what}: {value!r} is neither seconds nor HH:MM:SS:FF')
    h, m, s, f = map(int, match.groups())
    if f >= base:
        raise InputError(f'{what}: frame {f} is not below the timebase {base}')
    return ((h * 60 + m) * 60 + s) * base + f


def timecode(frames, base):
    f = frames % base
    s = frames // base
    return f'{s // 3600:02d}:{s // 60 % 60:02d}:{s % 60:02d}:{f:02d}'


def reel_name(source, used):
    """EDL reel names: up to 8 letters, digits or underscores, unique in the list."""
    stem = re.sub(r'[^A-Za-z0-9_]', '', Path(source).stem.upper())[:8] or 'AX'
    name, n = stem, 1
    while used.get(name, source) != source:
        n += 1
        name = f'{stem[:8 - len(str(n))]}{n}'
    used[name] = source
    return name


def build(edit):
    try:
        fps = float(edit['fps'])
        clips = edit['clips']
    except (KeyError, TypeError, ValueError):
        raise InputError('the edit needs fps and a list of clips')
    if not clips:
        raise InputError('the edit has no clips')
    base = timebase(fps)
    start = to_frames(edit.get('start', '00:00:00:00'), base, fps, 'start')
    events, position, reels = [], 0, {}
    for i, clip in enumerate(clips, 1):
        where = f'clip {i}'
        if not str(clip.get('source', '')).strip():
            raise InputError(f'{where}: source file name missing')
        src_in, src_out = to_frames(clip.get('in', 0), base, fps, f'{where} in'), to_frames(clip.get('out'), base, fps, f'{where} out') if clip.get('out') is not None else None
        if src_out is None or src_out <= src_in:
            raise InputError(f'{where}: out must come after in')
        record = to_frames(clip['record_in'], base, fps, f'{where} record_in') if clip.get('record_in') is not None else position
        if record < position:
            raise InputError(f'{where}: record_in overlaps the previous clip; one video track has no overlaps')
        length = src_out - src_in
        events.append({'n': i, 'source': clip['source'], 'reel': reel_name(clip['source'], reels), 'name': clip.get('name', ''), 'note': clip.get('note', ''),
                       'src_in': src_in, 'src_out': src_out, 'rec_in': record, 'rec_out': record + length})
        position = record + length
    return {'title': str(edit.get('title') or 'Edit'), 'fps': fps, 'base': base, 'start': start, 'events': events, 'length': position}


def one_line(text):
    """EDL is line-oriented: a control character or line break in a name or note could forge an event."""
    return re.sub(r'[\x00-\x1f\x7f\u2028\u2029]+', ' ', str(text)).strip()


def edl(t):
    lines = [f"TITLE: {one_line(t['title'])[:70]}", 'FCM: NON-DROP FRAME', '']
    for e in t['events']:
        tc = lambda frames: timecode(frames, t['base'])
        lines.append(f"{e['n']:03d}  {e['reel']:<8} V     C        {tc(e['src_in'])} {tc(e['src_out'])} {tc(t['start'] + e['rec_in'])} {tc(t['start'] + e['rec_out'])}")
        lines.append(f"* FROM CLIP NAME: {one_line(Path(e['source']).name)}")
        if e['note'] or e['name']:
            lines.append(f"* COMMENT: {one_line(' - '.join(x for x in (e['name'], e['note']) if x))}")
        lines.append('')
    return '\n'.join(lines)


def rational(frames, rate):
    return {'OTIO_SCHEMA': 'RationalTime.1', 'rate': rate, 'value': float(frames)}


def otio(t):
    rate = float(t['fps'])
    children, position = [], 0
    for e in t['events']:
        if e['rec_in'] > position:
            children.append({'OTIO_SCHEMA': 'Gap.1', 'name': '', 'metadata': {}, 'effects': [], 'markers': [], 'enabled': True,
                             'source_range': {'OTIO_SCHEMA': 'TimeRange.1', 'start_time': rational(0, rate), 'duration': rational(e['rec_in'] - position, rate)}})
        children.append({'OTIO_SCHEMA': 'Clip.2', 'name': e['name'] or Path(e['source']).stem, 'metadata': {'framecore': {'note': e['note'], 'reel': e['reel']}},
                         'effects': [], 'markers': [], 'enabled': True,
                         'source_range': {'OTIO_SCHEMA': 'TimeRange.1', 'start_time': rational(e['src_in'], rate), 'duration': rational(e['src_out'] - e['src_in'], rate)},
                         'media_references': {'DEFAULT_MEDIA': {'OTIO_SCHEMA': 'ExternalReference.1', 'name': Path(e['source']).name, 'metadata': {},
                                                                'available_range': None, 'available_image_bounds': None, 'target_url': e['source']}},
                         'active_media_reference_key': 'DEFAULT_MEDIA'})
        position = e['rec_out']
    track = {'OTIO_SCHEMA': 'Track.1', 'name': 'V1', 'kind': 'Video', 'metadata': {}, 'effects': [], 'markers': [], 'enabled': True, 'source_range': None, 'children': children}
    return {'OTIO_SCHEMA': 'Timeline.1', 'name': t['title'], 'metadata': {}, 'global_start_time': rational(t['start'], rate),
            'tracks': {'OTIO_SCHEMA': 'Stack.1', 'name': 'tracks', 'metadata': {}, 'effects': [], 'markers': [], 'enabled': True, 'source_range': None, 'children': [track]}}


def shot_list(t):
    out = io.StringIO()
    writer = csv.writer(out)
    tc = lambda frames: timecode(frames, t['base'])
    writer.writerow(['#', 'record in', 'record out', 'seconds', 'source', 'source in', 'source out', 'name', 'note'])
    for e in t['events']:
        writer.writerow([e['n'], tc(t['start'] + e['rec_in']), tc(t['start'] + e['rec_out']), round((e['rec_out'] - e['rec_in']) / t['fps'], 3),
                         e['source'], tc(e['src_in']), tc(e['src_out']), e['name'], e['note']])
    return out.getvalue()


def main(argv=None):
    parser = argparse.ArgumentParser(description='Export an edit decision list as EDL, OTIO and a CSV shot list.')
    parser.add_argument('edit')
    parser.add_argument('--out-dir', required=True)
    parser.add_argument('--stem', help='file name stem (default: from the edit file name)')
    args = parser.parse_args(argv)
    try:
        timeline = build(json.loads(Path(args.edit).read_text(encoding='utf-8')))
        folder = Path(args.out_dir)
        stem = args.stem or re.sub(r'(\.(example|motion-score|motion|shot-plan|shots|edit|board|prompts|plan|static))*\.json$', '', Path(args.edit).name)
        files = {folder / f'{stem}.edl': edl(timeline), folder / f'{stem}.otio': json.dumps(otio(timeline), ensure_ascii=False, indent=2) + '\n',
                 folder / f'{stem}-shots.csv': shot_list(timeline)}
        existing = [str(p) for p in files if p.exists()]
        if existing:
            raise InputError(f'output exists: {", ".join(existing)}')
        folder.mkdir(parents=True, exist_ok=True)
        for path, text in files.items():
            path.write_text(text, encoding='utf-8', newline='')
    except (OSError, ValueError, InputError) as error:
        sys.stderr.write(f'{error}\n')
        return 2
    print(json.dumps({'files': [str(p) for p in files], 'events': len(timeline['events']), 'length_seconds': round(timeline['length'] / timeline['fps'], 3),
                      'timebase': timeline['base']}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
