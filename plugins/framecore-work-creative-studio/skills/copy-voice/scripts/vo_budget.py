#!/usr/bin/env python3
"""Does a voice-over script fit its length? Word and syllable counts against the short-form timing card.

  python3 vo_budget.py script.txt --length 15 --language pl            # standard rate, 2 s end card
  python3 vo_budget.py script.txt --length 30 --language en --rate calm --end-card 2.5
  python3 vo_budget.py --table --language pl                           # the card's budget table

The script is plain text: one spoken line per line; lines in [brackets] and lines starting with # are directions and are
not counted. The estimate uses the planning rates of pipeline-core/references/short-form-timing.md (words per second, and
syllables per second for Polish, whichever is longer) and adds the pause after punctuation. It is a planning check, not a
measurement: time the real read before locking the edit. Prints JSON (or Markdown with --markdown).
Exit codes: 0 fits, 1 over the budget, 2 bad input.
"""
import argparse
import json
import math
import re
import sys
from pathlib import Path

RATES = {'en': {'calm': 2.2, 'standard': 2.6, 'fast': 3.0}, 'pl': {'calm': 1.8, 'standard': 2.1, 'fast': 2.4}}
SYLLABLES_PER_SECOND = {'pl': {'calm': 4.5, 'standard': 5.0, 'fast': 5.6}}
VOWELS = {'pl': 'aąeęioóuy', 'en': 'aeiouy'}
PAUSES = {',': 0.15, ';': 0.25, ':': 0.25, '—': 0.2, '–': 0.2, '.': 0.35, '!': 0.35, '?': 0.35, '…': 0.4}
END_CARD = {6: 0.5, 15: 2.0, 20: 2.0, 30: 2.5, 60: 3.0}
LEAD_IN = 0.5


def spoken_lines(text):
    return [line.strip() for line in text.splitlines() if line.strip() and not line.strip().startswith('#') and not re.fullmatch(r'\[.*\]', line.strip())]


def words_of(line):
    return [w for w in line.split() if any(ch.isalnum() for ch in w)]


def syllables(word, language):
    digits = sum(ch.isdigit() for ch in word)
    if digits:
        return 2 * digits  # a number is read out
    groups = re.findall(f"[{VOWELS.get(language, VOWELS['en'])}]+", word.lower())
    if language == 'pl':
        groups = [g[1:] if len(g) > 1 and g[0] == 'i' else g for g in groups]  # "nie", "siedem": i only softens
    return len(groups)


def end_card_for(length):
    """The card's end-card hold for its lengths; between them, the nearest shorter one."""
    known = sorted(END_CARD)
    return END_CARD[max([k for k in known if k <= length] or [known[0]])]


def estimate(text, language, rate):
    lines = spoken_lines(text)
    words = [w for line in lines for w in words_of(line)]
    syl = sum(syllables(w, language) for w in words)
    by_words = len(words) / RATES[language][rate]
    by_syllables = syl / SYLLABLES_PER_SECOND[language][rate] if language in SYLLABLES_PER_SECOND else 0
    pauses = sum(PAUSES.get(w[-1:], 0) for w in words[:-1]) + 0.3 * max(0, len(lines) - 1)
    return {'lines': len(lines), 'words': len(words), 'syllables': syl, 'seconds': round(max(by_words, by_syllables) + pauses, 2)}


def budget(length, language, rate, end_card=None):
    hold = end_card_for(length) if end_card is None else end_card
    spoken = max(0.0, length - LEAD_IN - hold)
    return {'length': length, 'end_card': hold, 'spoken_seconds': spoken, 'max_words': math.floor(spoken * RATES[language][rate] + 1e-9)}


def main(argv=None):
    parser = argparse.ArgumentParser(description='Check a voice-over script against the short-form timing card.')
    parser.add_argument('script', nargs='?')
    parser.add_argument('--length', type=float, help='video length in seconds')
    parser.add_argument('--language', choices=sorted(RATES), default='pl')
    parser.add_argument('--rate', choices=['calm', 'standard', 'fast'], default='standard')
    parser.add_argument('--end-card', type=float, help='seconds held silent at the end (default from the card)')
    parser.add_argument('--table', action='store_true', help='print the budget table for 6, 15, 20, 30 and 60 s')
    parser.add_argument('--markdown', action='store_true')
    args = parser.parse_args(argv)
    if args.table:
        rows = [{**budget(n, args.language, r), 'rate': r} for n in (6, 15, 20, 30, 60) for r in ('calm', 'standard', 'fast')]
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0
    if not args.script or not args.length or args.length <= 0:
        sys.stderr.write('give a script file and --length in seconds (or --table)\n')
        return 2
    try:
        text = Path(args.script).read_text(encoding='utf-8')
    except OSError as error:
        sys.stderr.write(f'{error}\n')
        return 2
    est, plan = estimate(text, args.language, args.rate), budget(args.length, args.language, args.rate, args.end_card)
    fits = est['seconds'] <= plan['spoken_seconds'] + 1e-9
    over = max(0.0, est['seconds'] - plan['spoken_seconds'])
    result = {'language': args.language, 'rate': args.rate, **est, 'budget': plan, 'fits': fits,
              'advice': 'fits; time the real read before locking the edit' if fits else
              f"about {over:.1f} s too long: cut about {math.ceil(over * RATES[args.language][args.rate])} words, use a faster read only if the brand voice allows, or lengthen the video"}
    if args.markdown:
        print(f"| Script | Words | Estimated | Spoken time available | Verdict |\n| --- | --- | --- | --- | --- |\n"
              f"| {Path(args.script).name} | {est['words']} (budget {plan['max_words']}) | {est['seconds']} s | {plan['spoken_seconds']} s of {args.length:g} s | {'fits' if fits else 'too long'} |")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if fits else 1


if __name__ == '__main__':
    sys.exit(main())
