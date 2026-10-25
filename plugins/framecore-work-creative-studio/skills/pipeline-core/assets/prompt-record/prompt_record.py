#!/usr/bin/env python3
"""Studio prompt records: one structured planning record per image or video, checked and compiled per generator.

  python3 prompt_record.py check record.json              findings: errors (exit 1) and warnings
  python3 prompt_record.py compile record.json --to ideogram|flux2|prose        an image record
  python3 prompt_record.py compile record.json --to kling|sora|timestamps|prose a video record
  python3 prompt_record.py example image|video            a filled example record

A record is a planning object, not a model's API. `compile` writes the model's own form: Ideogram 4.x native JSON,
the FLUX.2 JSON template, Kling's custom multi-shot request fields, Sora's headed blocks, or ordered prose. Field
names follow the makers' documentation as read on 2026-10-25 (see structured-image-prompts.md and
structured-video-prompts.md). Standard library only; nothing is sent anywhere.
Exit codes: 0 done, 1 the record has errors, 2 bad input.
"""
import argparse
import json
import re
import sys

SETTING_WORDS = re.compile(r'\b(\d{1,2}\s*:\s*\d{1,2}\b|aspect ratio|\d+\s*(s|sec|seconds|sekund)\b|seed\b|1080p|4k\b|720p)', re.I)
NEGATIVE_WORDS = re.compile(r"\b(no|not|don't|do not|never|without|bez|nie)\b", re.I)
HEX = re.compile(r'^#[0-9a-fA-F]{6}$')


class RecordError(Exception):
    pass


def load(path):
    try:
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        raise RecordError(f'{path}: {e}')
    if not isinstance(data, dict) or data.get('kind') not in ('image', 'video'):
        raise RecordError(f'{path}: a record needs "kind": "image" or "video"')
    return data


def text_of(value):
    if isinstance(value, dict):
        return ', '.join(t for t in (text_of(v) for v in value.values()) if t)
    if isinstance(value, list):
        return ', '.join(t for t in (text_of(v) for v in value) if t)
    return str(value) if value is not None else ''


def check_image(r, model):
    errors, warnings = [], []
    if not str(r.get('summary', '')).strip():
        errors.append('summary is required: one sentence with subject, action, setting and medium')
    for i, t in enumerate(r.get('text') or []):
        if not isinstance(t, dict) or not str(t.get('text', '')).strip():
            errors.append(f'text[{i}] needs the exact string in "text"')
    if SETTING_WORDS.search(text_of({k: r.get(k) for k in ('summary', 'subjects', 'composition', 'style')})):
        warnings.append('size, aspect ratio, duration or seed appear in the prose fields: put them in params')
    palette = r.get('color_palette') or []
    if isinstance(palette, list) and len(palette) > 16:
        errors.append(f'{len(palette)} colours: Ideogram takes at most 16, Recraft at most 10')
    style = r.get('style') or {}
    if isinstance(style, dict) and style.get('photo') and style.get('art_style'):
        errors.append('style has both photo and art_style: choose one (Ideogram accepts only one)')
    for i, s in enumerate((r.get('subjects') or []) + (r.get('text') or [])):
        box = s.get('bbox') if isinstance(s, dict) else None
        if box is not None and not (isinstance(box, list) and len(box) == 4 and all(isinstance(v, (int, float)) and 0 <= v <= 1000 for v in box) and box[0] < box[2] and box[1] < box[3]):
            errors.append(f'element {i}: bbox must be [y_min, x_min, y_max, x_max] on a 0 to 1000 scale')
    if r.get('avoid') and model == 'flux2':
        warnings.append('FLUX.2 has no negative prompt: describe the wanted result instead of the avoid list')
    edit = r.get('edit') or {}
    if edit and not edit.get('change'):
        errors.append('edit needs "change": the target and what changes')
    if edit and len(text_of(edit.get('preserve'))) > 300:
        warnings.append('the preserve text is long: a detailed description of what must stay tends to make it drift; keep a short blanket clause')
    return errors, warnings


def check_video(r, model):
    errors, warnings = [], []
    settings = r.get('settings') or {}
    shots = r.get('shots') or []
    duration = settings.get('duration_s')
    if not shots:
        errors.append('shots[] is empty: at least one shot is needed')
    t = 0.0
    for i, s in enumerate(shots):
        start, end = s.get('start_s'), s.get('end_s')
        if not isinstance(start, (int, float)) or not isinstance(end, (int, float)) or end <= start:
            errors.append(f'shot {i + 1}: start_s and end_s must be numbers with end after start')
            continue
        if abs(start - t) > 1e-6:
            errors.append(f'shot {i + 1} starts at {start} s, the previous ends at {t} s: shots must touch without gaps or overlaps')
        t = end
        if isinstance(s.get('camera_move'), list) and len(s['camera_move']) > 1:
            warnings.append(f'shot {i + 1}: {len(s["camera_move"])} camera moves; one per shot reads better')
        words = sum(len(str(d.get('line', '')).split()) for d in s.get('dialogue') or [])
        if words and words > 3 * (end - start):
            warnings.append(f'shot {i + 1}: {words} spoken words in {end - start:g} s is likely too long to sync; shorten or split the shot')
        if NEGATIVE_WORDS.search(text_of([s.get('action'), s.get('beats')])) and model in ('veo', 'runway', 'seedance', 'timestamps', 'sora'):
            warnings.append(f'shot {i + 1}: negative wording in the action; describe what happens instead')
    if isinstance(duration, (int, float)) and shots and abs(t - duration) > 1e-6:
        errors.append(f'shots end at {t:g} s but settings.duration_s is {duration:g} s')
    if duration is None:
        warnings.append('settings.duration_s is missing: duration is a generator setting, not prose')
    ids = {s.get('id') for s in r.get('subjects') or []}
    for i, s in enumerate(shots):
        for d in s.get('dialogue') or []:
            if d.get('speaker') not in ids:
                errors.append(f'shot {i + 1}: speaker {d.get("speaker")!r} is not in subjects[]')
    if SETTING_WORDS.search(text_of([r.get('summary'), [s.get('action') for s in shots]])):
        warnings.append('duration, size or aspect ratio appear in the prose: set them in settings')
    if model == 'kling':
        if len(shots) > 6:
            errors.append(f'{len(shots)} shots: Kling custom multi-shot takes at most 6')
        for i, s in enumerate(shots):
            if isinstance(s.get('end_s'), (int, float)) and isinstance(s.get('start_s'), (int, float)) and s['end_s'] - s['start_s'] < 1:
                errors.append(f'shot {i + 1}: Kling shots last at least 1 s')
        if isinstance(duration, (int, float)) and not 3 <= duration <= 15:
            errors.append(f'duration {duration:g} s: Kling 3.0 takes 3 to 15 s')
    return errors, warnings


def check(r, model=None):
    model = model or (r.get('target') or {}).get('model')
    return (check_image if r['kind'] == 'image' else check_video)(r, model)


def subject_phrase(s):
    parts = [s.get('count') and f"{s['count']}x", s.get('description'), s.get('action') or s.get('pose'),
             s.get('expression'), s.get('clothing') and f"wearing {s['clothing']}", s.get('position') and f"at {s['position']}"]
    return ', '.join(str(p) for p in parts if p)


def compile_ideogram(r):
    style = r.get('style') or {}
    camera = r.get('camera') or {}
    sd = {k: v for k, v in {'aesthetics': style.get('mood'), 'lighting': text_of(r.get('lighting')) or None,
                            'photo': style.get('photo') or (text_of(camera) or None if not style.get('art_style') else None),
                            'art_style': style.get('art_style'), 'medium': style.get('medium'),
                            'color_palette': [c for c in (r.get('color_palette') or []) if HEX.match(str(c))] or None}.items() if v}
    elements = []
    for s in r.get('subjects') or []:
        e = {'type': 'obj', 'desc': subject_phrase(s)}
        if s.get('bbox'):
            e['bbox'] = s['bbox']
        elements.append(e)
    for t in r.get('text') or []:
        e = {'type': 'text', 'text': t['text'], 'desc': ', '.join(str(t[k]) for k in ('font', 'size', 'color', 'location') if t.get(k)) or 'text'}
        if t.get('bbox'):
            e['bbox'] = t['bbox']
        elements.append(e)
    out = {'high_level_description': r['summary']}
    if sd:
        out['style_description'] = sd
    out['compositional_deconstruction'] = {'background': text_of(r.get('background')) or 'plain background', 'elements': elements}
    return json.dumps(out, ensure_ascii=False, indent=2)


def compile_flux2(r):
    camera = r.get('camera') or {}
    out = {'scene': r['summary'],
           'subjects': [{k: v for k, v in {'description': s.get('description'), 'position': s.get('position'), 'action': s.get('action') or s.get('pose')}.items() if v} for s in r.get('subjects') or []],
           'style': text_of({k: v for k, v in (r.get('style') or {}).items() if k != 'mood'}) or None,
           'color_palette': r.get('color_palette') or None,
           'lighting': text_of(r.get('lighting')) or None,
           'mood': (r.get('style') or {}).get('mood'),
           'background': text_of(r.get('background')) or None,
           'composition': text_of(r.get('composition')) or None,
           'camera': {k: camera[k] for k in ('angle', 'lens', 'depth_of_field') if camera.get(k)} or None}
    out = {k: v for k, v in out.items() if v}
    texts = [f'the text "{t["text"]}"' + (f' in {t["font"]}' if t.get('font') else '') + (f', {t["color"]}' if t.get('color') else '') + (f', {t["location"]}' if t.get('location') else '') for t in r.get('text') or []]
    if texts:
        out['text'] = '; '.join(texts)
    return json.dumps(out, ensure_ascii=False, indent=2)


def compile_image_prose(r):
    """Ordered prose (narrative card): summary, purpose, subjects, setting, composition and camera, light, style, exact text, constraints."""
    lines = [r['summary'].rstrip('.') + '.']
    if r.get('use_context'):
        lines.append(f'For {text_of(r["use_context"])}.')
    lines += [subject_phrase(s).capitalize() + '.' for s in r.get('subjects') or []]
    for k in ('background', 'composition', 'camera', 'lighting', 'style'):
        if r.get(k):
            lines.append(f'{k.capitalize()}: {text_of(r[k])}.')
    if r.get('color_palette'):
        lines.append('Colours: ' + ', '.join(map(str, r['color_palette'])) + '.')
    for t in r.get('text') or []:
        lines.append(f'The text "{t["text"]}"' + ''.join(f', {t[k]}' for k in ('font', 'size', 'color', 'location') if t.get(k)) + ', spelled exactly.')
    edit = r.get('edit') or {}
    if edit.get('change'):
        lines.append(f'Change: {edit["change"]}. ' + (f'Keep {edit["preserve"]}.' if edit.get('preserve') else 'Keep everything else unchanged.'))
    return '\n'.join(lines)


def cap(text):
    return text[:1].upper() + text[1:]


def ts(seconds):
    return f'{int(seconds // 60):02d}:{seconds % 60:05.2f}'.replace('.00', '')


def shot_prose(s, subjects):
    """One shot in the narrative order: shot, action as beats, one camera move, sound, then dialogue last."""
    parts = [', '.join(str(s[k]) for k in ('framing', 'lens') if s.get(k)), s.get('action'), '; then '.join(s.get('beats') or []), s.get('camera_move')]
    text = '. '.join(cap(p.strip().rstrip('.')) for p in parts if p) + '.'
    if s.get('sfx'):
        text += ' Sound: ' + ', '.join(s['sfx']) + '.'
    for d in s.get('dialogue') or []:
        name = subjects.get(d.get('speaker'), d.get('speaker'))
        text += f' {cap(str(name))}' + (f' ({d["delivery"]})' if d.get('delivery') else '') + f': "{d["line"]}"'
    return text


def compile_video(r, to):
    subjects = {s.get('id'): s.get('anchors') or s.get('id') for s in r.get('subjects') or []}
    shots = r.get('shots') or []
    head = [cap(f'{text_of(r["style"])}.') if r.get('style') else '', r.get('summary', '')]
    head = [h for h in head if h]
    for k in ('setting', 'lighting'):
        if r.get(k):
            head.append(f'{k.capitalize()}: {text_of(r[k])}.')
    if to == 'kling':
        settings = r.get('settings') or {}
        payload = {'multi_shot': len(shots) > 1, 'shot_type': 'customize' if len(shots) > 1 else None,
                   'multi_prompt': [{'index': i + 1, 'prompt': shot_prose(s, subjects), 'duration': int(round(s['end_s'] - s['start_s']))} for i, s in enumerate(shots)] if len(shots) > 1 else None,
                   'prompt': ' '.join(head) if len(shots) > 1 else ' '.join(head + [shot_prose(shots[0], subjects)]),
                   'duration': int(settings['duration_s']) if settings.get('duration_s') else None,
                   'aspect_ratio': settings.get('aspect_ratio')}
        return json.dumps({k: v for k, v in payload.items() if v is not None}, ensure_ascii=False, indent=2)
    if to == 'sora':
        out = [' '.join(head), '', 'Cinematography:']
        out += [f'- {s.get("framing", "shot")} {ts(s["start_s"])}-{ts(s["end_s"])}: {s.get("lens", "")} {s.get("camera_move", "")}'.rstrip() for s in shots]
        out += ['', 'Actions:'] + [f'- {s.get("action", "")}' for s in shots if s.get('action')]
        lines = [(subjects.get(d.get('speaker'), d.get('speaker')), d) for s in shots for d in s.get('dialogue') or []]
        if lines:
            out += ['', 'Dialogue:'] + [f'- {n}' + (f' ({d["delivery"]})' if d.get('delivery') else '') + f': "{d["line"]}"' for n, d in lines]
        audio = text_of(r.get('audio'))
        if audio:
            out += ['', f'Background Sound: {audio}']
        return '\n'.join(out)
    if to == 'timestamps':
        out = [' '.join(head)] + [f'[{ts(s["start_s"])}-{ts(s["end_s"])}] {shot_prose(s, subjects)}' for s in shots]
        if r.get('audio'):
            out.append(f'Audio: {text_of(r["audio"])}.')
        return '\n'.join(out)
    text = ' '.join(head) + ' ' + ' Then '.join(shot_prose(s, subjects) for s in shots)
    if r.get('audio'):
        text += f' Audio: {text_of(r["audio"])}.'
    return text


EXAMPLES = {
    'image': {'kind': 'image', 'target': {'model': 'ideogram'},
              'summary': 'A poster for a summer jazz night: a saxophonist silhouetted against a low orange sun over a river',
              'subjects': [{'description': 'saxophonist in silhouette', 'position': 'lower left third', 'pose': 'playing, horn raised', 'bbox': [420, 80, 900, 420]}],
              'text': [{'text': 'JAZZ NAD WISŁĄ', 'font': 'bold condensed sans-serif', 'color': '#F6E7C1', 'location': 'top centre', 'bbox': [60, 120, 220, 880]},
                       {'text': '12.07 · 20:00', 'font': 'same family, regular', 'color': '#F6E7C1', 'location': 'below the title'}],
              'background': 'a wide river at dusk, the far bank as a dark line',
              'composition': 'vertical poster, large sky, text zone at the top kept clear',
              'lighting': {'conditions': 'low sun just above the horizon', 'direction': 'backlight', 'shadows': 'long, soft'},
              'color_palette': ['#E8742A', '#2B1B3D', '#F6E7C1'],
              'style': {'art_style': 'flat screen-print illustration with grain', 'medium': 'poster', 'mood': 'warm, unhurried'},
              'use_context': 'A3 event poster and a 4:5 social post', 'params': {'aspect_ratio': '2:3'}},
    'video': {'kind': 'video', 'target': {'model': 'kling'}, 'settings': {'duration_s': 8, 'aspect_ratio': '9:16', 'audio': 'on'},
              'summary': 'A baker opens her small bakery at dawn and sets out the first tray of bread.',
              'subjects': [{'id': 'baker', 'anchors': 'a woman in her forties with short grey hair, flour-dusted navy apron'}],
              'style': 'warm documentary look, soft grain, palette of cream, navy and golden crust',
              'setting': 'a narrow bakery with wooden shelves, just before sunrise', 'lighting': 'low warm window light, cool blue street light outside',
              'shots': [{'index': 1, 'start_s': 0, 'end_s': 4, 'framing': 'medium shot', 'lens': '35 mm', 'camera_move': 'slow push in',
                         'action': 'she unlocks the door and flips the sign to open', 'sfx': ['key in the lock', 'door bell']},
                        {'index': 2, 'start_s': 4, 'end_s': 8, 'framing': 'close-up', 'lens': '50 mm', 'camera_move': 'static',
                         'action': 'she slides a tray of loaves onto the shelf and smiles', 'dialogue': [{'speaker': 'baker', 'line': 'First batch is ready.', 'delivery': 'quietly, pleased'}]}],
              'audio': 'room tone of an oven humming, distant street'}}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    sub = ap.add_subparsers(dest='cmd', required=True)
    c = sub.add_parser('check')
    c.add_argument('record')
    c.add_argument('--model')
    c.add_argument('--json', action='store_true')
    k = sub.add_parser('compile')
    k.add_argument('record')
    k.add_argument('--to', required=True, choices=['ideogram', 'flux2', 'prose', 'kling', 'sora', 'timestamps'])
    e = sub.add_parser('example')
    e.add_argument('kind', choices=['image', 'video'])
    args = ap.parse_args(argv)
    try:
        if args.cmd == 'example':
            print(json.dumps(EXAMPLES[args.kind], ensure_ascii=False, indent=2))
            return 0
        r = load(args.record)
        if args.cmd == 'check':
            errors, warnings = check(r, args.model)
            if args.json:
                print(json.dumps({'errors': errors, 'warnings': warnings}, ensure_ascii=False, indent=2))
            else:
                print('\n'.join([f'error: {x}' for x in errors] + [f'warning: {x}' for x in warnings]) or 'clean')
            return 1 if errors else 0
        image_targets, video_targets = ('ideogram', 'flux2', 'prose'), ('kling', 'sora', 'timestamps', 'prose')
        if args.to not in (image_targets if r['kind'] == 'image' else video_targets):
            raise RecordError(f'--to {args.to} does not apply to a {r["kind"]} record')
        errors, warnings = check(r, args.to)
        if errors:
            print('\n'.join(f'error: {x}' for x in errors), file=sys.stderr)
            return 1
        for w in warnings:
            print(f'warning: {w}', file=sys.stderr)
        if r['kind'] == 'image':
            print({'ideogram': compile_ideogram, 'flux2': compile_flux2, 'prose': compile_image_prose}[args.to](r))
        else:
            print(compile_video(r, args.to))
        return 0
    except RecordError as err:
        print(f'prompt_record: {err}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
