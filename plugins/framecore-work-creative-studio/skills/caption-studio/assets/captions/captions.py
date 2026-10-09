#!/usr/bin/env python3
"""Captions and subtitles for Studio videos: check, convert, build, import into a motion contract, burn in.

  python captions.py check captions.srt [--profile subtitles|social] [--language en|pl] [--audience adult|children] [--fps 30]
  python captions.py convert captions.srt --to vtt --out captions.vtt
  python captions.py build --words words.json --to srt --out captions.srt [--profile social] [--language pl]
  python captions.py build --segments segments.json --to vtt --out captions.vtt
  python captions.py contract captions.srt video.motion.json --out video-r2.motion.json [--prefix caption] [--replace]
  python captions.py burn video.mp4 captions.srt --out video-captioned.mp4 [--size 44] [--bottom 0.14]

`check`, `convert`, `build` and `contract` need only Python 3.8+. `burn` also needs Pillow and ffmpeg and draws the
captions exactly as the motion renderer does (../../../hyperframes-workflow/assets/motion-render/render.py, which must
sit there or next to this file). The limits come from ../../references/readability-defaults.md. Exit codes: 0 no
errors, 1 errors found, 2 the input could not be read or a tool is missing.
"""
import argparse
import importlib.util
import json
import math
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# Subtitle limits from the Netflix Timed Text Style Guide (general requirements; English (USA) and Polish guides),
# checked 2026-10-08: characters per second by language and audience. Other languages: Unknown until read.
READING_SPEED = {('en', 'adult'): 20, ('en', 'children'): 17, ('pl', 'adult'): 17, ('pl', 'children'): 13}
MAX_LINES = 2
MAX_CHARS = 42
SUBTITLE_MIN_S = 5 / 6
SUBTITLE_MAX_S = 7.0
# Studio's readable hold for burned-in captions, shared with check-score.mjs and critique.py (motion craft).
CHARACTERS_PER_SECOND, WORDS_PER_SECOND, SETTLE_SECONDS, MIN_READ_SECONDS = 13.0, 3.0, 0.5, 1.0
MIN_GAP_FRAMES = 2
# Words that should not end a line: articles, short prepositions and conjunctions; in Polish, also every
# one-letter word (a line ending in "w" or "i" reads as broken).
NO_LINE_END = {
    'en': {'a', 'an', 'the', 'to', 'of', 'in', 'on', 'at', 'for', 'with', 'by', 'from', 'and', 'or', 'but', 'as', 'if', 'my', 'your', 'our', 'his', 'her', 'its', 'their'},
    'pl': {'a', 'i', 'o', 'u', 'w', 'z', 'we', 'ze', 'na', 'do', 'od', 'po', 'za', 'ku', 'że', 'by', 'nie', 'się', 'oraz', 'albo', 'lub', 'ale'},
}
TIME = re.compile(r'^(?:(\d+):)?(\d{1,2}):(\d{2})[,.](\d{1,3})$')


def reading_seconds(text):
    """Studio's readable hold: the longer of 13 characters per second plus 0.5 s and 0.5 s plus a third of a second
    per word, at least 1 s (motion craft, readable holds)."""
    flat = ' '.join(str(text).split())
    words = len(flat.split()) if flat else 0
    return max(MIN_READ_SECONDS, len(flat) / CHARACTERS_PER_SECOND + SETTLE_SECONDS, SETTLE_SECONDS + words / WORDS_PER_SECOND)


# ---------------------------------------------------------------- files

def to_ms(value):
    match = TIME.match(value.strip())
    if not match:
        raise ValueError(f'Invalid subtitle time: {value.strip()}')
    h, m, s, ms = match.groups()
    return ((int(h or 0) * 60 + int(m)) * 60 + int(s)) * 1000 + int(ms.ljust(3, '0'))


def parse(text):
    """SRT or WebVTT text to [{start_ms, end_ms, text}], as motion-sync/sync.mjs reads it: styling tags removed,
    line breaks kept, headers, notes and style blocks skipped."""
    cues = []
    text = text.lstrip('﻿').replace('\r\n', '\n').replace('\r', '\n')
    for block in re.split(r'\n{2,}', text):
        lines = [line for line in block.split('\n') if line.strip()]
        at = next((i for i, line in enumerate(lines) if '-->' in line), -1)
        if at < 0:
            continue
        start, rest = lines[at].split('-->', 1)
        end = rest.strip().split()[0]
        body = '\n'.join(filter(None, (re.sub(r'\{\\[^}]*\}', '', re.sub(r'<[^>]*>', '', line)).strip() for line in lines[at + 1:])))
        if body:
            cues.append({'start_ms': to_ms(start), 'end_ms': to_ms(end), 'text': body})
    return cues


def read_cues(path):
    with open(path, encoding='utf-8') as handle:
        return parse(handle.read())


def stamp(ms, kind):
    h, rest = divmod(int(round(ms)), 3600000)
    m, rest = divmod(rest, 60000)
    s, ms = divmod(rest, 1000)
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}' if kind == 'srt' else f'{h:02d}:{m:02d}:{s:02d}.{ms:03d}'


def write(cues, kind):
    """SRT (numbered cues, comma before milliseconds) or WebVTT (header, full stop before milliseconds), UTF-8."""
    if kind == 'srt':
        blocks = [f"{i}\n{stamp(c['start_ms'], 'srt')} --> {stamp(c['end_ms'], 'srt')}\n{c['text']}" for i, c in enumerate(cues, 1)]
        return '\n\n'.join(blocks) + '\n'
    blocks = ['WEBVTT'] + [f"{stamp(c['start_ms'], 'vtt')} --> {stamp(c['end_ms'], 'vtt')}\n{c['text']}" for c in cues]
    return '\n\n'.join(blocks) + '\n'


# ---------------------------------------------------------------- check

PROFILES = ('subtitles', 'social', 'text')


def limits(profile, language, audience):
    """subtitles: dialogue or translation subtitles, the published limits are errors. social: captions burned into a
    short-form video and timed to its speech; the same limits are warnings. text: on-screen text with no speech to
    follow (supers, motion captions); Studio's readable hold applies."""
    speed = READING_SPEED.get((language, audience))
    timed = profile in ('subtitles', 'social')
    return {'profile': profile, 'language': language, 'audience': audience, 'max_lines': MAX_LINES, 'max_chars': MAX_CHARS,
            'max_cps': speed if timed else None, 'min_seconds': SUBTITLE_MIN_S if timed else MIN_READ_SECONDS,
            'max_seconds': SUBTITLE_MAX_S if timed else None, 'hold_rule': profile == 'text'}


def wanted_seconds(text, rules):
    """How long a caption should stay: the readable hold for on-screen text; otherwise its length at the language's
    reading speed (17 characters per second when the speed is Unknown), at least the minimum duration."""
    flat = ' '.join(str(text).split())
    if rules['hold_rule']:
        return reading_seconds(flat)
    return max(rules['min_seconds'], len(flat) / (rules['max_cps'] or 17))


def check(cues, profile='social', language='en', audience='adult', fps=30.0):
    """Errors break the file or a published limit of the subtitles profile; warnings are limits of the other
    profiles and heuristics to look at."""
    rules, errors, warnings = limits(profile, language, audience), [], []
    strict = errors if profile == 'subtitles' else warnings
    if profile != 'text' and rules['max_cps'] is None:
        warnings.append(f'reading speed for {language} ({audience}) is Unknown; read that language\'s subtitle guide before relying on this check')
    if not cues:
        errors.append('no cues found')
    previous = None
    for i, cue in enumerate(cues, 1):
        where = f'cue {i} ({stamp(cue["start_ms"], "srt")})'
        seconds = (cue['end_ms'] - cue['start_ms']) / 1000
        lines = cue['text'].split('\n')
        flat = ' '.join(cue['text'].split())
        if seconds <= 0:
            errors.append(f'{where}: ends before it starts')
            continue
        if previous and cue['start_ms'] < previous['end_ms']:
            errors.append(f'{where}: overlaps the previous cue by {previous["end_ms"] - cue["start_ms"]} ms')
        elif previous:
            gap = (cue['start_ms'] - previous['end_ms']) / 1000 * fps
            if 0 < gap < MIN_GAP_FRAMES - 1e-6:
                warnings.append(f'{where}: a gap of {gap:.1f} frames after the previous cue reads as a flicker; close it or leave at least {MIN_GAP_FRAMES} frames')
        if len(lines) > rules['max_lines']:
            errors.append(f'{where}: {len(lines)} lines; at most {rules["max_lines"]}')
        for n, line in enumerate(lines, 1):
            if len(line) > rules['max_chars']:
                errors.append(f'{where}: line {n} has {len(line)} characters; at most {rules["max_chars"]}')
        if rules['hold_rule']:
            need = reading_seconds(flat)
            if seconds + 0.001 < need:
                warnings.append(f'{where}: held {seconds:.2f} s; reading it needs about {need:.2f} s')
        else:
            if rules['max_cps'] and len(flat) / seconds > rules['max_cps'] + 0.05:
                strict.append(f'{where}: {len(flat) / seconds:.1f} characters per second; at most {rules["max_cps"]} for {language} ({audience})')
            if seconds + 0.001 < rules['min_seconds']:
                strict.append(f'{where}: {seconds:.2f} s; at least {rules["min_seconds"]:.3f} s (5/6 s)')
            if seconds > rules['max_seconds'] + 0.001:
                strict.append(f'{where}: {seconds:.2f} s; at most {rules["max_seconds"]:.0f} s')
        for line in lines[:-1]:
            tail = line.split()[-1].lower().strip('.,;:!?…"\'') if line.split() else ''
            if tail in NO_LINE_END.get(language, set()):
                warnings.append(f'{where}: a line ends on "{tail}"; move it to the next line')
        previous = cue
    return {'status': 'FAIL' if errors else 'PASS', 'cues': len(cues), 'rules': rules, 'errors': errors, 'warnings': warnings}


# ---------------------------------------------------------------- build

def break_lines(text, language='en', max_chars=MAX_CHARS):
    """One line when it fits; otherwise two lines broken after punctuation or before a conjunction or preposition,
    never after a word that should not end a line, as balanced as those rules allow. None when two lines cannot hold it."""
    words = text.split()
    flat = ' '.join(words)
    if len(flat) <= max_chars:
        return flat
    avoid, best = NO_LINE_END.get(language, set()), None
    for i in range(1, len(words)):
        top, bottom = ' '.join(words[:i]), ' '.join(words[i:])
        if len(top) > max_chars or len(bottom) > max_chars:
            continue
        tail = words[i - 1].lower().strip('.,;:!?…"\'')
        cost = abs(len(top) - len(bottom))
        if tail in avoid:
            cost += 1000
        if words[i - 1][-1:] in ',.;:!?…':
            cost -= 15
        if best is None or cost < best[0]:
            best = (cost, top + '\n' + bottom)
    return best[1] if best else None


def load_json(path, key):
    with open(path, encoding='utf-8') as handle:
        data = json.load(handle)
    items = data.get(key) if isinstance(data, dict) else data
    if not isinstance(items, list):
        raise ValueError(f'{path}: expected a list or an object with "{key}"')
    return items


def words_from(items):
    out = []
    for item in items:
        word = str(item.get('word', item.get('text', ''))).strip()
        if word:
            out.append({'word': word, 'start': float(item['start']), 'end': float(item['end'])})
    if any(b['start'] < a['start'] for a, b in zip(out, out[1:])):
        raise ValueError('word timings must be in order')
    return out


def cut_point(group, language):
    """Where to end a cue that has grown too long: after the last punctuation that keeps at least half of it, else
    before the last word that may start a line (not after an article, preposition or one-letter word)."""
    avoid = NO_LINE_END.get(language, set())
    length = len(' '.join(w['word'] for w in group))
    for i in range(len(group) - 1, 0, -1):
        if group[i - 1]['word'][-1:] in ',.;:!?…' and len(' '.join(w['word'] for w in group[:i])) >= length / 2:
            return i
    for i in range(len(group) - 1, 0, -1):
        if group[i - 1]['word'].lower().strip('.,;:!?…"\'') not in avoid:
            return i
    return len(group)


def build_from_words(words, profile='social', language='en', audience='adult', max_chars=MAX_CHARS, fps=30.0, cue_chars=None):
    """Group timed words into cues: a cue closes at a sentence end, after a comma once it holds half its length, at a
    pause of 0.7 s or more, or when the next word would pass the cue length (social and text: one line of `max_chars`;
    subtitles: two lines) or the maximum duration; a cue that grew too long ends at a natural break. End times then
    extend toward the wanted duration; gaps under two frames are closed."""
    rules = limits(profile, language, audience)
    max_seconds = rules['max_seconds'] or 7.0
    cue_chars = cue_chars or (2 * max_chars if profile == 'subtitles' else max_chars)
    groups, current = [], []
    for word in words:
        if current:
            text = ' '.join(w['word'] for w in current)
            trial = text + ' ' + word['word']
            last = current[-1]['word'][-1:]
            if word['start'] - current[-1]['end'] >= 0.7 or (last in '.!?…' and current[-1]['end'] - current[0]['start'] >= 0.8) \
                    or (last in ',;:' and len(text) >= cue_chars / 2):
                groups.append(current)
                current = []
            elif len(trial) > cue_chars or break_lines(trial, language, max_chars) is None or word['end'] - current[0]['start'] > max_seconds:
                at = cut_point(current, language)
                groups.append(current[:at])
                current = current[at:]
        current.append(word)
    if current:
        groups.append(current)
    cues = []
    for group in groups:
        joined = ' '.join(w['word'] for w in group)
        cues.append({'start_ms': round(group[0]['start'] * 1000), 'end_ms': round(group[-1]['end'] * 1000), 'text': break_lines(joined, language, max_chars) or joined})
    gap_ms = math.ceil(MIN_GAP_FRAMES / fps * 1000)
    for i, cue in enumerate(cues):
        limit = cues[i + 1]['start_ms'] - gap_ms if i + 1 < len(cues) else None
        target = cue['start_ms'] + math.ceil(min(wanted_seconds(cue['text'], rules), max_seconds) * 1000)
        if target > cue['end_ms']:
            cue['end_ms'] = target if limit is None else max(cue['end_ms'], min(target, limit))
        if limit is not None and 0 < cues[i + 1]['start_ms'] - cue['end_ms'] < gap_ms:
            cue['end_ms'] = cues[i + 1]['start_ms']
    return cues


def build_from_segments(items, language='en', max_chars=MAX_CHARS):
    """One cue per timed segment; a segment too long for two lines is split at word boundaries with time shared
    by length."""
    cues = []
    for item in items:
        text, start, end = ' '.join(str(item['text']).split()), float(item['start']), float(item['end'])
        if not text or end <= start:
            continue
        parts, words = [], text.split()
        while words:
            take = len(words)
            while take > 1 and break_lines(' '.join(words[:take]), language, max_chars) is None:
                take -= 1
            parts.append(' '.join(words[:take]))
            words = words[take:]
        total, at = sum(len(p) for p in parts), start
        for part in parts:
            share = (end - start) * len(part) / total
            cues.append({'start_ms': round(at * 1000), 'end_ms': round((at + share) * 1000), 'text': break_lines(part, language, max_chars) or part})
            at += share
    return cues


# ---------------------------------------------------------------- motion contract

def frame_at(ms, score):
    return round(ms * score['fps']['num'] / (1000 * score['fps']['den']))


def import_captions(score, cues, prefix='caption', replace=False):
    """Captions into a motion contract as motion-sync/sync.mjs imports them: exact text into copy as <prefix>-N,
    timing in master frames; overlaps start at the previous end; cues past the end are cut or skipped."""
    if score.get('captions') and not replace:
        raise ValueError('The contract already has captions; pass --replace to swap them')
    result = json.loads(json.dumps(score))
    result['copy'] = dict(result.get('copy') or {})
    for old in score.get('captions') or []:
        result['copy'].pop(old['copy'], None)
    result['captions'], warnings = [], []
    for i, cue in enumerate(cues, 1):
        cid = f'{prefix}-{i}'
        if cid in result['copy']:
            raise ValueError(f'Copy ID {cid} is already used; choose another prefix')
        start, end = frame_at(cue['start_ms'], score), frame_at(cue['end_ms'], score)
        if start >= score['totalFrames']:
            warnings.append(f'{cid} starts at frame {start}, after the last frame; skipped')
            continue
        if end > score['totalFrames']:
            warnings.append(f'{cid} ends at frame {end}; cut to {score["totalFrames"]}')
            end = score['totalFrames']
        previous = result['captions'][-1] if result['captions'] else None
        if previous and start < previous['end']:
            warnings.append(f'{cid} overlaps {previous["id"]}; it now starts at frame {previous["end"]}')
            start = previous['end']
        if end <= start:
            warnings.append(f'{cid} has no frames left after rounding; skipped')
            continue
        result['copy'][cid] = cue['text']
        result['captions'].append({'id': cid, 'start': start, 'end': end, 'copy': cid})
    return result, warnings


# ---------------------------------------------------------------- burn-in

def load_renderer():
    for path in (os.path.join(HERE, '..', '..', '..', 'hyperframes-workflow', 'assets', 'motion-render', 'render.py'), os.path.join(HERE, 'render.py')):
        if os.path.exists(path):
            spec = importlib.util.spec_from_file_location('studio_render', path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
    raise RuntimeError('render.py (the motion renderer) must sit in hyperframes-workflow/assets/motion-render/ or next to captions.py')


def probe(video):
    if not shutil.which('ffprobe'):
        raise RuntimeError('ffprobe is not available; burning in needs ffmpeg and ffprobe')
    run = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,r_frame_rate,nb_frames:format=duration',
                          '-of', 'json', video], capture_output=True, text=True, check=True)
    data = json.loads(run.stdout)
    stream, num_den = data['streams'][0], data['streams'][0]['r_frame_rate'].split('/')
    fps = {'num': int(num_den[0]), 'den': int(num_den[1]) if len(num_den) > 1 else 1}
    duration = float(data.get('format', {}).get('duration') or 0)
    frames = int(stream.get('nb_frames') or 0) or round(duration * fps['num'] / fps['den'])
    return {'width': int(stream['width']), 'height': int(stream['height']), 'fps': fps, 'totalFrames': frames}


def burn(video, cues, out, size=44, bottom=0.14, background=None, colour=None, font=None, font_bold=None, crf=18):
    """Draw each caption on the frames it covers with the motion renderer's caption style and re-encode the
    picture (H.264); the source audio is copied unchanged. Returns a summary."""
    if os.path.exists(out):
        raise ValueError(f'Output file already exists: {out}')
    r = load_renderer()
    from PIL import Image  # noqa: E402  (Pillow is needed only here)
    info = probe(video)
    score = dict(info, tokens={'captions': {'size': size, 'bottom': bottom}}, copy={}, captions=[], scenes=[])
    if background:
        score['tokens']['captions']['background'] = background
    if colour:
        score['tokens']['captions']['color'] = colour
    score, warnings = import_captions(score, cues)
    fonts = r.Fonts((score.get('tokens') or {}).get('fontFamily'), font, font_bold)
    drawer = r.Captions(score, fonts)
    w, h = score['width'], score['height']
    rate = f"{score['fps']['num']}/{score['fps']['den']}"
    decode = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', video, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    encode = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{w}x{h}', '-r', rate, '-i', '-',
                               '-i', video, '-map', '0:v', '-map', '1:a?', '-c:v', 'libx264', '-preset', 'medium', '-crf', str(crf),
                               '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    size_bytes, frame, drawn = w * h * 3, 0, 0
    try:
        while True:
            raw = decode.stdout.read(size_bytes)
            if len(raw) < size_bytes:
                break
            if any(c['start'] <= frame < c['end'] for c in score['captions']):
                image = Image.frombytes('RGB', (w, h), raw).convert('RGBA')
                drawer.draw(image, frame)
                raw = image.convert('RGB').tobytes()
                drawn += 1
            encode.stdin.write(raw)
            frame += 1
    finally:
        encode.stdin.close()
        decode.stdout.close()
        decode.wait()
        encode.wait()
    if encode.returncode != 0 or decode.returncode != 0:
        raise RuntimeError('ffmpeg failed while burning in the captions')
    return {'out': out, 'frames': frame, 'frames_with_captions': drawn, 'captions': len(score['captions']), 'warnings': warnings,
            'style': {'size': size, 'bottom': bottom}, 'status': 'rendered; watch it before calling it final'}


# ---------------------------------------------------------------- command line

def main(argv=None):
    parser = argparse.ArgumentParser(description='Check, convert, build, import and burn in captions.')
    sub = parser.add_subparsers(dest='command', required=True)
    c = sub.add_parser('check')
    c.add_argument('file')
    for p in (c,):
        p.add_argument('--profile', choices=PROFILES, default='social')
        p.add_argument('--audience', choices=('adult', 'children'), default='adult')
        p.add_argument('--fps', type=float, default=30.0)
    v = sub.add_parser('convert')
    v.add_argument('file')
    v.add_argument('--to', choices=('srt', 'vtt'), required=True)
    v.add_argument('--out', required=True)
    b = sub.add_parser('build')
    source = b.add_mutually_exclusive_group(required=True)
    source.add_argument('--words')
    source.add_argument('--segments')
    b.add_argument('--to', choices=('srt', 'vtt'), required=True)
    b.add_argument('--out', required=True)
    b.add_argument('--profile', choices=PROFILES, default='social')
    b.add_argument('--audience', choices=('adult', 'children'), default='adult')
    b.add_argument('--max-chars', type=int, default=MAX_CHARS, help='characters per line')
    b.add_argument('--cue-chars', type=int, help='characters per caption (social and text: one line, subtitles: two lines)')
    b.add_argument('--fps', type=float, default=30.0)
    k = sub.add_parser('contract')
    k.add_argument('file')
    k.add_argument('contract')
    k.add_argument('--out', required=True)
    k.add_argument('--prefix', default='caption')
    k.add_argument('--replace', action='store_true')
    u = sub.add_parser('burn')
    u.add_argument('video')
    u.add_argument('file')
    u.add_argument('--out', required=True)
    u.add_argument('--size', type=int, default=44, help='text size at 1080 px on the short side (scaled for other sizes)')
    u.add_argument('--bottom', type=float, default=0.14, help='distance from the bottom as a share of the height (0.14 keeps 9:16 captions above the controls)')
    u.add_argument('--background')
    u.add_argument('--color')
    u.add_argument('--font')
    u.add_argument('--font-bold')
    for p in (c, b):
        p.add_argument('--language', default='en', help='en or pl have reading-speed limits; other languages are checked without them')
    args = parser.parse_args(argv)
    try:
        if args.command == 'check':
            report = check(read_cues(args.file), args.profile, args.language, args.audience, args.fps)
            print(json.dumps(report, ensure_ascii=False, indent=2))
            return 1 if report['errors'] else 0
        if args.command in ('convert', 'build', 'contract') and os.path.exists(args.out):
            raise ValueError(f'Output file already exists: {args.out}')
        if args.command == 'convert':
            cues = read_cues(args.file)
            with open(args.out, 'w', encoding='utf-8') as handle:
                handle.write(write(cues, args.to))
            print(json.dumps({'cues': len(cues), 'out': args.out}))
            return 0
        if args.command == 'build':
            if args.words:
                cues = build_from_words(words_from(load_json(args.words, 'words')), args.profile, args.language, args.audience, args.max_chars, args.fps, args.cue_chars)
            else:
                cues = build_from_segments(load_json(args.segments, 'segments'), args.language, args.max_chars)
            with open(args.out, 'w', encoding='utf-8') as handle:
                handle.write(write(cues, args.to))
            report = check(cues, args.profile, args.language, args.audience, args.fps)
            print(json.dumps({'cues': len(cues), 'out': args.out, 'check': report['status'], 'errors': report['errors'], 'warnings': report['warnings']}, ensure_ascii=False))
            return 1 if report['errors'] else 0
        if args.command == 'contract':
            with open(args.contract, encoding='utf-8') as handle:
                score = json.load(handle)
            result, warnings = import_captions(score, read_cues(args.file), args.prefix, args.replace)
            with open(args.out, 'w', encoding='utf-8') as handle:
                handle.write(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
            print(json.dumps({'captions': len(result['captions']), 'warnings': warnings, 'out': args.out}, ensure_ascii=False))
            return 0
        summary = burn(args.video, read_cues(args.file), args.out, args.size, args.bottom, args.background, args.color, args.font, args.font_bold)
        print(json.dumps(summary, ensure_ascii=False))
        return 0
    except (OSError, ValueError, RuntimeError, KeyError, subprocess.CalledProcessError) as error:
        sys.stderr.write(f'{error}\n')
        return 2


if __name__ == '__main__':
    sys.exit(main())
