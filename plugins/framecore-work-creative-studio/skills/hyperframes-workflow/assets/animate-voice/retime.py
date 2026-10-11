#!/usr/bin/env python3
"""Word timing for an Animate voice-over in Polish or another language, after the engine's own voice tool.

The bundled Animate engine stays byte-identical to its source, and its tools/voice.mjs recognises English only
(faster-whisper `small.en`, and a word match that drops letters outside a-z, such as ą, ę, ł, ż). Run voice.mjs first,
then this tool on the same piece; it rewrites the word times in <piece>/voice.json and leaves every line time alone:

  node tools/voice.mjs pieces/<name>                       # lines, voice.wav and first word times
  python3 retime.py pieces/<name> --language pl            # Polish word times (then rebuild the piece)
  python3 retime.py pieces/<name> --language pl --heard words.json   # times you already have, e.g. from the TTS service
  python3 retime.py pieces/<name> --language pl --estimate           # no recogniser: estimate from syllables

Word times come from, in order: --heard (a JSON list of {w|word|text, t0|start, t1|end} in seconds), faster-whisper with
a multilingual model (`small` by default) and the language given, or an estimate that spreads each line's time over its
words by syllables and holds a short pause after a comma or a full stop. Matching keeps every letter (ą, ł, ż and the
rest), so recognised words land on the script's words; words the recogniser missed are filled in between their matched
neighbours and marked "est". Prints one JSON summary. Exit codes: 0 written, 2 bad input.
"""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

VOWELS = {'pl': 'aąeęioóuy', 'en': 'aeiouy', 'de': 'aäeioöuüy', 'es': 'aáeéiíoóuúü', 'fr': 'aàâeéèêëiîïoôuùûüyÿ', 'it': 'aàeèéiìoòóuù'}
PAUSE_AFTER = {',': 0.6, ';': 0.8, ':': 0.8, '.': 1.2, '!': 1.2, '?': 1.2, '…': 1.2}  # in syllables of time


def norm(word):
    """Lower-case letters and digits of any script; Polish letters stay (ł has no ASCII decomposition)."""
    return ''.join(ch for ch in unicodedata.normalize('NFC', word.lower()) if ch.isalnum())


def syllables(word, language):
    vowels = VOWELS.get(language, VOWELS['en'])
    groups = re.findall(f'[{vowels}]+', word.lower())
    if language == 'pl':
        # "i" before another vowel only softens the consonant (sie-dem, nie, cie-pło): it is not a syllable of its own.
        groups = [g[1:] if len(g) > 1 and g[0] == 'i' else g for g in groups]
    digits = sum(ch.isdigit() for ch in word)
    # A number is read out (24: dwadzieścia cztery), about two syllables a digit; w and z have none of their own.
    return 2 * digits if digits else len(groups)


def estimate(line, language):
    """Spread the line's time over its words by syllables, with pauses after punctuation."""
    words = [w for w in line['text'].split() if norm(w)]
    weights = [syllables(w, language) + 0.3 for w in words]
    pauses = [PAUSE_AFTER.get(w[-1:], 0) if i < len(words) - 1 else 0 for i, w in enumerate(words)]
    total = sum(weights) + sum(pauses) or 1
    unit = (line['t1'] - line['t0']) / total
    out, t = [], line['t0']
    for word, weight, pause in zip(words, weights, pauses):
        out.append({'w': word, 't0': round(t, 3), 't1': round(t + weight * unit, 3), 'est': True})
        t += (weight + pause) * unit
    return out


def align(line, heard):
    """Match the script's words to the heard words (edit distance on normalised tokens) and take the matched times;
    fill the rest between their matched neighbours."""
    words = line['words']
    near = [h for h in heard if line['t0'] - 0.15 <= (h['t0'] + h['t1']) / 2 <= line['t1'] + 0.15]
    a, b = [norm(w['w']) for w in words], [norm(h['w']) for h in near]
    n, m = len(a), len(b)
    D = [[i if j == 0 else j if i == 0 else 0 for j in range(m + 1)] for i in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            D[i][j] = min(D[i - 1][j] + 1, D[i][j - 1] + 1, D[i - 1][j - 1] + (a[i - 1] != b[j - 1]))
    matched, i, j = 0, n, m
    while i > 0 and j > 0:
        if D[i][j] == D[i - 1][j - 1] + (a[i - 1] != b[j - 1]):
            if a[i - 1] == b[j - 1]:
                words[i - 1].update(t0=near[j - 1]['t0'], t1=near[j - 1]['t1'])
                words[i - 1].pop('est', None)
                matched += 1
            i, j = i - 1, j - 1
        elif D[i][j] == D[i - 1][j] + 1:
            i -= 1
        else:
            j -= 1
    k = 0
    while k < len(words):
        if not words[k].get('est'):
            k += 1
            continue
        end = k
        while end < len(words) and words[end].get('est'):
            end += 1
        start_t = words[k - 1]['t1'] if k > 0 else line['t0']
        end_t = words[end]['t0'] if end < len(words) else line['t1']
        span = end - k
        for q in range(span):
            words[k + q].update(t0=round(start_t + (end_t - start_t) * q / span, 3), t1=round(start_t + (end_t - start_t) * (q + 1) / span, 3))
        k = end
    return matched


def load_heard(path):
    items = json.loads(Path(path).read_text(encoding='utf-8'))
    out = []
    for item in items:
        word = str(item.get('w', item.get('word', item.get('text', '')))).strip()
        if word:
            out.append({'w': word, 't0': float(item.get('t0', item.get('start'))), 't1': float(item.get('t1', item.get('end')))})
    return out


def recognise(wav, language, model):
    from faster_whisper import WhisperModel  # optional, local; no API
    segments, _ = WhisperModel(model, device='cpu', compute_type='int8').transcribe(str(wav), word_timestamps=True, vad_filter=False, beam_size=5, language=language)
    return [{'w': w.word.strip(), 't0': round(w.start, 3), 't1': round(w.end, 3)} for s in segments for w in s.words or []]


def main(argv=None):
    parser = argparse.ArgumentParser(description='Word times for an Animate voice-over in Polish or another language.')
    parser.add_argument('piece', help='the piece folder (with voice.json and voice/voice.wav from tools/voice.mjs)')
    parser.add_argument('--language', default='pl', help='language of the voice-over (pl, en, de, ...)')
    parser.add_argument('--model', default='small', help='faster-whisper model; a multilingual one, not *.en, for other languages')
    parser.add_argument('--heard', help='JSON list of word times you already have, in seconds on the voice.wav timeline')
    parser.add_argument('--estimate', action='store_true', help='skip recognition and estimate from syllables')
    args = parser.parse_args(argv)
    piece = Path(args.piece)
    try:
        voice = json.loads((piece / 'voice.json').read_text(encoding='utf-8'))
        lines = voice['lines']
        if not lines or not all({'text', 't0', 't1'} <= set(line) for line in lines):
            raise ValueError('voice.json needs lines with text, t0 and t1 (run tools/voice.mjs first)')
    except (OSError, ValueError, KeyError) as error:
        sys.stderr.write(f'{error}\n')
        return 2
    heard, source = None, 'estimated from syllables'
    if args.heard:
        try:
            heard, source = load_heard(args.heard), f'from {Path(args.heard).name}'
        except (OSError, ValueError, TypeError) as error:
            sys.stderr.write(f'{args.heard}: {error}\n')
            return 2
    elif not args.estimate:
        wav = piece / 'voice' / 'voice.wav'
        try:
            heard, source = recognise(wav, args.language, args.model), f'heard by faster-whisper {args.model} ({args.language})'
        except ImportError:
            source = 'estimated from syllables (faster-whisper is not installed: pip install faster-whisper)'
        except Exception as error:  # a missing or unreadable voice.wav: the estimate still places every word
            source = f'estimated from syllables (recognition failed: {error})'
    matched = total = 0
    for line in lines:
        line['words'] = estimate(line, args.language)
        total += len(line['words'])
        if heard:
            matched += align(line, heard)
    voice['wordTiming'] = {'language': args.language, 'source': source, 'matched': matched, 'words': total}
    (piece / 'voice.json').write_text(json.dumps(voice, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(json.dumps({'voice': str(piece / 'voice.json'), **voice['wordTiming']}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
