#!/usr/bin/env python3
"""Check Polish copy against Studio's Polish copy standard and a channel's character limits.

  python3 pl_copy_check.py copy.txt                          # typography, numbers, dates, forms of address
  python3 pl_copy_check.py copy.txt --fix > fixed.txt        # apply only the safe typographic fixes
  python3 pl_copy_check.py --channel meta-headline "Miód lipowy prosto z pasieki"
  python3 pl_copy_check.py --channels                        # the channels and limits it knows (dated)
  echo "..." | python3 pl_copy_check.py - --json

Findings are "fix" (typography the --fix option corrects without changing a word) or "check" (a person decides:
mixed formats, forms of address, title case, a one-letter word at a line end). It never rewrites wording, never
judges tone and never decides whether a claim is true. Exit codes: 0 no findings, 1 findings, 2 text over a hard
channel limit, 3 bad input. Limits come from ../assets/channel-limits.json (see its check date).
"""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
LIMITS = json.loads((HERE.parent / 'assets/channel-limits.json').read_text(encoding='utf-8'))
NBSP = ' '
UNIT = r'(?:zł|gr|kg|km|cm|mm|ml|min|PLN|EUR|USD|[gmlhs])(?![^\W\d_])'
MONTHS = ('stycznia lutego marca kwietnia maja czerwca lipca sierpnia września października listopada grudnia '
          'styczeń luty marzec kwiecień maj czerwiec lipiec sierpień wrzesień październik listopad grudzień').split()
DAYS = 'poniedziałek wtorek środa czwartek piątek sobota niedziela poniedziałki wtorki środy czwartki piątki soboty niedziele'.split()
TY = re.compile(r'\b(ty|ciebie|cię|tobie|ci|twój|twoja|twoje|twojego|twojej|twoim|twoich|masz|możesz|chcesz|jesteś|sprawdź|kup|zamów|zobacz|dołącz|zapisz się|weź|odbierz|skorzystaj)\b', re.I)
PAN = re.compile(r'\b(Pan|Pani|Państwo|Pana|Panu|Panią|Państwa|Państwu|Panem)\b')
ONE_LETTER = re.compile(r'(?:^|\s)([aiouwzAIOUWZ])$')


def finding(code, kind, message, sample='', fix=None):
    item = {'code': code, 'kind': kind, 'message': message}
    if sample:
        item['sample'] = sample[:80]
    if fix is not None:
        item['fix'] = fix
    return item


def safe_fixes(text):
    """Typographic fixes that change no word: quotes, dash, ellipsis, spaces, no-break spaces."""
    out = re.sub(r'(?<![\w\d])"([^"\n]+)"', '„\\1”', text)                 # "x" -> „x”
    out = re.sub('“([^”\n]+)”', '„\\1”', out)                # “x” -> „x”
    out = re.sub(r'(?<=\S) - (?=\S)', ' – ', out)                                # word - word -> word – word
    out = re.sub(r'(?<!\.)\.\.\.(?!\.)', '…', out)                               # ... -> …
    out = re.sub(r'(?<=\S) {2,}(?=\S)', ' ', out)                                     # double spaces
    out = re.sub(r'(?<=\w) +([,;:!?]|\.(?=\s|$))', '\\1', out, flags=re.M)          # space before punctuation
    out = re.sub(r'(?<=[^\W\d_])([,;])(?=[^\W\d_])', '\\1 ', out)                     # missing space after a comma
    out = re.sub(r'(\d)(' + UNIT + ')', '\\1 \\2', out)                               # 5kg -> 5 kg
    out = re.sub(r'(?<!\S)([^\W\d_]) +(?=\S)', '\\1' + NBSP, out)                     # one-letter word + nbsp
    out = re.sub(r'(\d) (?=' + UNIT + '|%)', '\\1' + NBSP, out)                       # number + unit
    out = re.sub(r'(\d) (?=\d{3}(?!\d))', '\\1' + NBSP, out)                          # digit groups
    return out


def check_text(text, lines_matter=False):
    found = []
    if re.search(r'(?<![\w\d])"[^"\n]+"', text):
        found.append(finding('QUOTES_ASCII', 'fix', 'Straight quotes: Polish uses „…” (and «…» inside)', re.search(r'"[^"\n]+"', text).group(0)))
    if re.search('“[^”\n]+”', text):
        found.append(finding('QUOTES_ENGLISH', 'fix', 'English quotes “…”: Polish opens low, „…”', re.search('“[^”\n]+”', text).group(0)))
    if re.search(r'(?<=\S) - (?=\S)', text):
        found.append(finding('HYPHEN_AS_DASH', 'fix', 'A hyphen between spaces: use the en dash (–)', re.search(r'\S+ - \S+', text).group(0)))
    if re.search(r'(?<!\.)\.\.\.(?!\.)', text):
        found.append(finding('ELLIPSIS', 'fix', 'Three dots: use the ellipsis character (…)'))
    if re.search(r'(?<=\S) {2,}(?=\S)', text):
        found.append(finding('DOUBLE_SPACE', 'fix', 'Double space'))
    match = re.search(r'\w +(?:[,;:!?]|\.(?=\s|$))', text, re.M)
    if match:
        found.append(finding('SPACE_BEFORE_PUNCTUATION', 'fix', 'A space before punctuation', match.group(0)))
    match = re.search(r'\d(' + UNIT + ')', text)
    if match:
        found.append(finding('UNIT_SPACE', 'fix', 'A number and its unit are separated by a (no-break) space: 5 kg, 10 zł', match.group(0)))
    match = re.search(r'[^\W\d_]? ?,(?=[^\W\d_])', text)
    if match:
        found.append(finding('SPACE_AFTER_COMMA', 'check', 'No space after a comma', match.group(0)))
    match = re.search(r'\b\d+\.\d{2}\s?(?:zł|PLN|EUR|€)', text)
    if match:
        found.append(finding('DECIMAL_POINT', 'check', 'Polish prices use a decimal comma: 39,90 zł', match.group(0)))
    match = re.search(r'(?:zł|PLN)\s?\d', text)
    if match:
        found.append(finding('CURRENCY_BEFORE_AMOUNT', 'check', 'The currency follows the amount: 39 zł', match.group(0)))
    if re.search(r'\bzł\b', text) and re.search(r'\bPLN\b', text):
        found.append(finding('MIXED_CURRENCY', 'check', 'Both zł and PLN: pick one (zł in consumer copy, PLN in tables and invoices)'))
    match = re.search(r'(?<![\d.,])\b\d{5,8}\b(?![.,]\d)(?=[ \u00a0]?(?:' + UNIT + r'|%|€|osób|sztuk|egz\.))', text)
    if match:
        found.append(finding('THOUSANDS', 'check', 'Group digits of numbers from 10 000 with a (no-break) space', match.group(0)))
    grouped = re.search(r'\b\d{1,3}[  ]\d{3}\b', text)
    plain4 = re.search(r'(?<!\d[ \u00a0])(?<![\d.,:/])\b(?!(?:19|20)\d{2}\b)\d{4}\b(?![.,:/]\d)(?![ \u00a0]\d{3})', text)
    if grouped and plain4:
        found.append(finding('THOUSANDS_MIXED', 'check', 'Four-digit numbers both grouped and not (1 299 and 1299): keep one style', plain4.group(0)))
    if re.search(r'\b\d{1,2}\.\d{1,2}\.\d{2,4}\b', text) and re.search(r'\b\d{1,2} (' + '|'.join(MONTHS[:12]) + r')\b', text):
        found.append(finding('DATE_FORMAT_MIXED', 'check', 'Dates written two ways (10.10.2026 and 10 października): keep one'))
    match = re.search(r'\b\d{1,2}/\d{1,2}/\d{2,4}\b', text)
    if match:
        found.append(finding('DATE_SLASH', 'check', 'Slashed dates read as US dates: use 10.10.2026 or 10 października 2026 r.', match.group(0)))
    if re.search(r'\b\d{1,2}:\d{2}\b', text) and re.search(r'\b(?:godz\.\s?)\d{1,2}\.\d{2}\b', text):
        found.append(finding('TIME_FORMAT_MIXED', 'check', 'Times written two ways (18:00 and godz. 18.00): keep one'))
    match = re.search(r'\b\d{1,2}\s?(?:AM|PM|am|pm)\b', text)
    if match:
        found.append(finding('TIME_12H', 'check', 'Polish copy uses the 24-hour clock', match.group(0)))
    if re.search(r'\d%', text) and re.search(r'\d[  ]%', text):
        found.append(finding('PERCENT_MIXED', 'check', 'Percent written as 30% and 30 %: keep one'))
    for word in re.findall(r'(?<![.!?:]\s)(?<!^)\b([A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+)\b', text, re.M):
        if word.lower() in MONTHS or word.lower() in DAYS:
            found.append(finding('CAPITALISED_DATE_WORD', 'check', 'Months and weekdays are lowercase in Polish', word))
            break
    for segment in re.split(r'[.!?:;\n–—]| - ', text):
        long_words = [w for w in re.findall(r'[^\W\d_]+', segment) if len(w) > 3]
        if len(long_words) >= 3 and all(w[0].isupper() for w in long_words) and not all(w.isupper() for w in long_words):
            found.append(finding('TITLE_CASE', 'check', 'English-style Title Case: Polish headlines use sentence case', segment.strip()))
            break
    if TY.search(text) and PAN.search(text):
        found.append(finding('ADDRESS_MIXED', 'check', 'Both "Ty" and "Pan/Pani/Państwo" forms: address the reader one way', f'{TY.search(text).group(0)} / {PAN.search(text).group(0)}'))
    if re.search(r'[!?]{2,}', text):
        found.append(finding('STACKED_PUNCTUATION', 'check', 'Repeated ! or ? reads as shouting in Polish copy', re.search(r'\S*[!?]{2,}', text).group(0)))
    if lines_matter:
        for line in text.splitlines():
            if ONE_LETTER.search(line.rstrip()):
                found.append(finding('ORPHAN_LETTER', 'check', 'A one-letter word ends a line: move it to the next line', line.strip()))
    return found


def length(text):
    """Characters as most ad tools count them: NFC code points, line breaks included."""
    return len(unicodedata.normalize('NFC', text))


def channel_report(text, channel):
    spec = LIMITS['channels'][channel]
    n = length(text)
    status = 'over_hard_limit' if spec['hard'] and n > spec['hard'] else 'over_visible' if spec['visible'] and n > spec['visible'] else 'ok'
    return {'channel': channel, 'label': spec['label'], 'characters': n, 'visible': spec['visible'], 'hard': spec['hard'], 'status': status, 'checked': LIMITS['checked']}


def main(argv=None):
    parser = argparse.ArgumentParser(description='Check Polish copy (typography, formats, forms of address) and channel lengths.')
    parser.add_argument('source', nargs='?', help='a text file, "-" for standard input, or the text itself')
    parser.add_argument('--channel', choices=sorted(LIMITS['channels']), help='check the length against this channel')
    parser.add_argument('--channels', action='store_true', help='list the channels and limits')
    parser.add_argument('--lines', action='store_true', help='the line breaks are final (a headline or a layout): check line ends')
    parser.add_argument('--fix', action='store_true', help='print the text with the safe typographic fixes applied')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args(argv)
    if args.channels:
        print(json.dumps(LIMITS, indent=2, ensure_ascii=False))
        return 0
    if args.source is None:
        parser.error('give a file, "-" or the text')
    if args.source == '-':
        text = sys.stdin.read()
    elif Path(args.source).is_file():
        text = Path(args.source).read_text(encoding='utf-8')
    else:
        text = args.source
    if not text.strip():
        print('no text', file=sys.stderr)
        return 3
    if args.fix:
        sys.stdout.write(safe_fixes(text))
        return 0
    findings = check_text(text, args.lines)
    report = {'findings': findings, 'characters': length(text)}
    if args.channel:
        report['channel'] = channel_report(text.strip(), args.channel)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        for item in findings:
            print(f"{item['kind']:5} {item['code']}: {item['message']}" + (f" [{item['sample']}]" if item.get('sample') else ''))
        if args.channel:
            c = report['channel']
            print(f"{c['label']}: {c['characters']} characters (visible {c['visible']}, hard {c['hard']}; checked {c['checked']}): {c['status']}")
        if not findings and not args.channel:
            print('no findings')
    if args.channel and report['channel']['status'] == 'over_hard_limit':
        return 2
    return 1 if findings else 0


if __name__ == '__main__':
    sys.exit(main())
