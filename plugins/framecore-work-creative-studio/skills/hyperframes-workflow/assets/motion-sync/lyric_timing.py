#!/usr/bin/env python3
"""Lyric timing: word and line times for a song, matched to the supplied lyrics and the beat grid.

The lyrics the user supplies are the truth; speech recognition only says when each word is sung.
Recognised words are aligned to the lyric words (so a misheard word keeps its correct spelling),
missing words are interpolated between their neighbours, and each line gets a board cut that may
snap to the nearest half-beat when that is within --snap-ms. Words keep their own sung times for
highlights. Output: JSON, LRC (line, or enhanced with word times) and SRT.

    python3 lyric_timing.py song.mp3 lyrics.txt --out song.timing.json --lrc song.lrc --srt song.srt
    python3 lyric_timing.py song.mp3 lyrics.txt --words asr.json   # times from any recogniser

Recognisers, first one found is used unless --words is given (none ships with Studio):
  stable-ts (pip install stable-ts)        aligns the lyrics to the audio directly; best for songs
  whisperx (pip install whisperx)          transcription with phoneme-level word alignment
  faster-whisper (pip install faster-whisper)  word timestamps, then the alignment below
A vocal stem helps on dense mixes; Demucs pretrained weights are for research use only, so use a stem
the user supplies or a separator whose model licence allows the job. Beats come from beats.py next to
this file (needs ffmpeg).
"""
import argparse
import difflib
import json
import re
import sys
import unicodedata
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent


def norm(word):
    word = unicodedata.normalize('NFKD', word.lower().replace('ł', 'l'))
    return re.sub(r'[^0-9a-z]', '', ''.join(c for c in word if not unicodedata.combining(c)))


def read_lyrics(text):
    lines = [re.sub(r'\s+', ' ', line).strip() for line in text.splitlines()]
    lines = [line for line in lines if line and not re.fullmatch(r'\[.*\]', line)]   # drop [Chorus] labels
    return [{'text': line, 'words': [{'text': w} for w in line.split(' ')]} for line in lines]


def similarity(a, b):
    if not a or not b:
        return 0.0
    return 1.0 if a == b else difflib.SequenceMatcher(None, a, b).ratio()


def align(lyric_words, heard, threshold=0.6):
    """Global alignment (Needleman-Wunsch) of lyric words to recognised words; returns lyric index -> heard index."""
    n, m = len(lyric_words), len(heard)
    gap = -0.4
    score = [[0.0] * (m + 1) for _ in range(n + 1)]
    move = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        score[i][0], move[i][0] = i * gap, 1
    for j in range(1, m + 1):
        score[0][j], move[0][j] = j * gap, 2
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            s = similarity(lyric_words[i - 1], heard[j - 1])
            options = (score[i - 1][j - 1] + (2 * s - 1 if s >= threshold else -1.0), score[i - 1][j] + gap, score[i][j - 1] + gap)
            best = max(range(3), key=lambda k: options[k])
            score[i][j], move[i][j] = options[best], best
    pairs, i, j = {}, n, m
    while i > 0 or j > 0:
        step = move[i][j] if i > 0 and j > 0 else (1 if i > 0 else 2)
        if step == 0:
            if similarity(lyric_words[i - 1], heard[j - 1]) >= threshold:
                pairs[i - 1] = j - 1
            i, j = i - 1, j - 1
        elif step == 1:
            i -= 1
        else:
            j -= 1
    return pairs


def place(lines, heard_words, threshold=0.6):
    flat = [w for line in lines for w in line['words']]
    pairs = align([norm(w['text']) for w in flat], [norm(w['text']) for w in heard_words], threshold)
    for k, w in enumerate(flat):
        if k in pairs:
            h = heard_words[pairs[k]]
            w.update(start=float(h['start']), end=float(h['end']), matched=True)
    known = [k for k, w in enumerate(flat) if w.get('matched')]
    if not known:
        raise ValueError('no lyric word matched the recognised words; check the lyrics and the track')
    for k, w in enumerate(flat):                       # interpolate the rest by character length
        if w.get('matched'):
            continue
        before = max((x for x in known if x < k), default=None)
        after = min((x for x in known if x > k), default=None)
        a = flat[before]['end'] if before is not None else max(0.0, flat[after]['start'] - 0.4)
        b = flat[after]['start'] if after is not None else flat[before]['end'] + 0.4
        if b < a:                                      # the heard neighbours overlap: no room, check by ear
            b = a
            for x in flat[(before if before is not None else -1) + 1:(after if after is not None else len(flat))]:
                x['squeezed'] = True
        lo, hi = (before if before is not None else -1) + 1, (after if after is not None else len(flat))
        span = flat[lo:hi]
        total = sum(max(len(x['text']), 1) for x in span)
        t = a
        for x in span:
            d = (b - a) * max(len(x['text']), 1) / total
            x.update(start=round(t, 3), end=round(t + d, 3), matched=False)
            t += d
    for line in lines:
        line['start'], line['end'] = line['words'][0]['start'], line['words'][-1]['end']
        line['matched_share'] = round(sum(w['matched'] for w in line['words']) / len(line['words']), 2)
        line['needs_check'] = line['matched_share'] < 0.5 or any(w.pop('squeezed', False) for w in line['words'])
    return sum(w['matched'] for w in flat) / len(flat)


def beat_grid(audio):
    sys.path.insert(0, str(HERE))
    import beats                                      # the bundled, dependency-free beat finder
    env = beats.onset_envelope(beats.decode(audio))
    bpm, beat0 = beats.tempo(env)
    bpm, beat0 = beats.fit(env, bpm, beat0)
    return bpm, beat0


def snap(lines, bpm, beat0, snap_ms=80, lead_frames=1, fps=30):
    """Board cut per line: the line start minus a small lead, moved to the nearest half-beat if close."""
    half = 30.0 / bpm
    for line in lines:
        want = max(0.0, line['start'] - lead_frames / fps)    # a line sung from 0 s cuts at 0, never before
        nearest = beat0 + round((want - beat0) / half) * half
        snapped = abs(nearest - want) * 1000 <= snap_ms and 0.0 <= nearest <= line['start']
        line['cut'] = round(nearest if snapped else want, 3)
        line['cut_on_beat'] = snapped
        line['cut_frame'] = int(round(line['cut'] * fps))


def recognise(audio, lyrics_text, model):
    """Times from the first installed recogniser; returns a flat list of {text, start, end}."""
    try:
        import stable_whisper
        result = stable_whisper.load_model(model).align(audio, lyrics_text, language=None)
        return [{'text': w.word.strip(), 'start': w.start, 'end': w.end} for s in result.segments for w in s.words], 'stable-ts'
    except ImportError:
        pass
    try:
        import whisperx
        audio_data = whisperx.load_audio(audio)
        result = whisperx.load_model(model, 'cpu', compute_type='int8').transcribe(audio_data)
        align_model, meta = whisperx.load_align_model(language_code=result['language'], device='cpu')
        result = whisperx.align(result['segments'], align_model, meta, audio_data, 'cpu')
        return [{'text': w['word'], 'start': w['start'], 'end': w['end']} for w in result['word_segments'] if 'start' in w], 'whisperx'
    except ImportError:
        pass
    try:
        from faster_whisper import WhisperModel
        segments, _ = WhisperModel(model, compute_type='int8').transcribe(audio, word_timestamps=True, initial_prompt=lyrics_text[:800])
        return [{'text': w.word.strip(), 'start': w.start, 'end': w.end} for s in segments for w in s.words], 'faster-whisper'
    except ImportError:
        pass
    raise SystemExit('No recogniser installed. Install one (pip install stable-ts, recommended for songs), or pass --words '
                     'with word times from another tool (JSON list of {"text", "start", "end"} in seconds).')


def stamp(seconds):
    m, s = divmod(max(seconds, 0.0), 60)
    return f'{int(m):02d}:{s:05.2f}'


def to_lrc(lines, words=False):
    out = []
    for line in lines:
        body = ' '.join(f"<{stamp(w['start'])}>{w['text']}" for w in line['words']) if words else line['text']
        out.append(f"[{stamp(line['start'])}]{body}")
    return '\n'.join(out) + '\n'


def to_srt(lines):
    def t(x):
        ms = int(round(x * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
        return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'
    return ''.join(f"{i}\n{t(l['start'])} --> {t(l['end'])}\n{l['text']}\n\n" for i, l in enumerate(lines, 1))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument('audio')
    p.add_argument('lyrics', help='plain text, one sung line per line; [Section] labels are ignored')
    p.add_argument('--words', help='JSON word times from another recogniser instead of running one')
    p.add_argument('--model', default='large-v3', help='recogniser model name')
    p.add_argument('--bpm', type=float, help='known tempo instead of detecting it')
    p.add_argument('--offset', type=float, default=0.0, help='first beat in seconds, with --bpm')
    p.add_argument('--fps', type=Fraction, default=Fraction(30), help='frame rate, e.g. 25, 30 or 30000/1001')
    p.add_argument('--snap-ms', type=float, default=80)
    p.add_argument('--threshold', type=float, default=0.6, help='word similarity needed to count as the same word')
    p.add_argument('--out'); p.add_argument('--lrc'); p.add_argument('--lrc-words'); p.add_argument('--srt')
    a = p.parse_args(argv)
    problem = next((f'file not found: {f}' for f in (a.audio, a.lyrics, a.words) if f and not Path(f).is_file()), None)
    problem = problem or next((f'output file already exists: {f}' for f in (a.out, a.lrc, a.lrc_words, a.srt) if f and Path(f).exists()), None)
    if problem:                                   # input problems exit 2
        print(problem, file=sys.stderr)
        return 2
    text = Path(a.lyrics).read_text(encoding='utf-8')
    lines = read_lyrics(text)
    if a.words:
        try:
            heard, engine = json.loads(Path(a.words).read_text(encoding='utf-8')), 'supplied'
        except ValueError as error:
            print(f'{a.words} is not word-time JSON: {error}', file=sys.stderr)
            return 2
    else:
        heard, engine = recognise(a.audio, '\n'.join(l['text'] for l in lines), a.model)
    try:
        share = place(lines, heard, a.threshold)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 2
    bpm, beat0 = (a.bpm, a.offset) if a.bpm else beat_grid(a.audio)
    snap(lines, bpm, beat0, a.snap_ms, fps=float(a.fps))
    weak = [i + 1 for i, l in enumerate(lines) if l['needs_check']]
    report = {'audio': a.audio, 'engine': engine, 'fps': str(a.fps), 'bpm': round(bpm, 3), 'first_beat': round(beat0, 3),
              'matched_words': round(share, 3), 'check_lines': weak, 'lines': lines}
    for path, body in ((a.out, json.dumps(report, ensure_ascii=False, indent=1) + '\n'), (a.lrc, to_lrc(lines) if a.lrc else None),
                       (a.lrc_words, to_lrc(lines, True) if a.lrc_words else None), (a.srt, to_srt(lines) if a.srt else None)):
        if path:
            Path(path).write_text(body, encoding='utf-8')
    print(f'{engine}: {len(lines)} lines, {share:.0%} of lyric words matched, {bpm:.1f} BPM, '
          f"{sum(l['cut_on_beat'] for l in lines)} cuts on a half-beat" + (f'; check lines {weak} by ear' if weak else ''))
    return 0


if __name__ == '__main__':
    sys.exit(main())
