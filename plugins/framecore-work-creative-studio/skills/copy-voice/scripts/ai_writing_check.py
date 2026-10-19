#!/usr/bin/env python3
"""Find the patterns that make English or Polish copy read as machine-made, and judge whether they cluster.

  python3 ai_writing_check.py draft.txt
  python3 ai_writing_check.py - --json < draft.md
  python3 ai_writing_check.py --text "Odkryj moc innowacyjnych rozwiązań. Mam nadzieję, że to pomoże!"

Patterns follow ../references/ai-writing-patterns.md: empty vocabulary, significance inflation, unproven social proof,
weasel attribution, authority tropes, chatbot closers, fake-candid openers, signposting, caps emphasis, negative
parallelism, forced threes, staccato runs, false ranges, generic CTAs, filler, stacked hedging, emoji headings, bold
and inline-header lists, and English em dashes in a cluster. One hit is not a verdict: `clean` (0-1 pattern kinds),
`check` (2), `cluster` (3 or more kinds, or one kind 3 or more times). It never rewrites text and never judges whether a
claim is true. Python standard library only.
Exit codes: 0 clean or check, 1 cluster, 3 bad input.
"""
import argparse
import json
import re
import sys
from pathlib import Path


def words(*items):
    return re.compile(r'(?<![\w-])(?:' + '|'.join(items) + r')(?![\w-])', re.I)


PATTERNS = [
    ('empty-vocabulary', 'tone', 'say what it does instead', words(
        'unlock(?:s|ing)?', 'elevate[sd]?', 'empower(?:s|ing)?', 'delve[sd]?', 'showcas(?:e|es|ing)', 'testament',
        'seamless(?:ly)?', 'cutting[- ]edge', 'revolutionary', 'game[- ]changer', 'next[- ]level', 'robust', 'synerg(?:y|ies)',
        'innowacyjn\\w*', 'kompleksow\\w*', 'rewolucyjn\\w*', 'przełomow\\w*', 'bezproblemow\\w*', 'holistyczn\\w*',
        'najwyższej jakości', 'odkryj moc', 'na wyższy poziom', 'synergi\\w*')),
    ('significance-inflation', 'tone', 'state the concrete effect', words(
        'the future of', 'a pivotal moment', 'a new era', 'ushering in', 'in today\'s (?:fast-paced|digital|dynamic) world',
        'w dzisiejszym (?:dynamicznym|cyfrowym|szybko zmieniającym się) świecie', 'w erze \\w+', 'nowa era', 'nową erę')),
    ('unproven-social-proof', 'honesty', 'name a real customer or number with its source, or cut it', words(
        'trusted by (?:thousands|millions|teams)', 'industry[- ]leading', 'world[- ]class', 'loved by (?:customers|teams|thousands)',
        'zaufały nam tysiące', 'zaufało nam', 'lider(?:em)? rynku', 'klasy światowej', 'pokochali nas')),
    ('weasel-attribution', 'honesty', 'name the source or cut the sentence', words(
        'experts (?:say|agree|believe)', 'studies show', 'research shows', 'industry observers', 'many believe',
        'eksperci (?:twierdzą|zgodnie|uważają)', 'badania pokazują', 'wielu uważa', 'mówi się, że')),
    ('authority-trope', 'tone', 'state the point directly', words(
        'at its core', 'the real question is', 'what really matters', 'the heart of the matter',
        'w gruncie rzeczy', 'prawdziwe pytanie brzmi', 'to, co naprawdę się liczy', 'sedno sprawy')),
    ('chatbot-closer', 'tone', 'end on the last concrete fact', words(
        'i hope this helps', 'let me know if you have any questions', 'would you like me to', 'feel free to reach out',
        'mam nadzieję, że to pomoże', 'daj znać, jeśli masz pytania', 'chętnie rozwinę', 'służę pomocą')),
    ('fake-candid-opener', 'tone', 'say the thing', words('honestly\\?', 'here\'s the thing', 'real talk', 'let\'s be honest',
                                                          'szczerze\\?', 'powiedzmy sobie szczerze')),
    ('signposting', 'tone', 'start with the content', words(
        'let\'s dive in(?:to)?', 'here\'s what you need to know', 'without further ado', 'in this article,? we\'ll',
        'zanurzmy się', 'oto wszystko, co musisz wiedzieć', 'bez zbędnych ceregieli', 'w tym artykule (?:omówimy|przyjrzymy)')),
    ('negative-parallelism', 'rhythm', 'state what it is', re.compile(
        r"\b(?:it'?s|this is) not (?:just|only) [^.!?]{1,60}[,;] it'?s\b|\bnot only\b[^.!?]{1,80}\bbut also\b|"
        r"\bto nie (?:tylko|jest tylko) [^.!?]{1,60}[,;–-] to\b|\bnie tylko\b[^.!?]{1,80}\b(?:ale|lecz) (?:też|także|również)\b", re.I)),
    ('false-range', 'rhythm', 'list what it actually covers', words('and everything in between', 'i wszystko pomiędzy',
                                                                     'from start to finish and beyond')),
    ('generic-cta', 'tone', 'name the action', re.compile(
        r'^\s*(?:[-*>]\s*)?\[?(?:learn more|get started|discover more|discover|explore|try (?:it )?now|find out more|'
        r'dowiedz się więcej|odkryj(?: więcej)?|zacznij(?: teraz)?|sprawdź(?: teraz)?|wypróbuj teraz)\]?\s*[!.→>]*\s*$', re.I | re.M)),
    ('filler-phrase', 'hygiene', 'cut the padding', words(
        'in order to', 'due to the fact that', 'at this point in time', 'it is important to note that', 'it\'s worth noting that',
        'w celu', 'z uwagi na fakt,? że', 'warto zauważyć,? że', 'należy podkreślić,? że', 'na chwilę obecną', 'w chwili obecnej')),
    ('stacked-hedging', 'hygiene', 'keep one qualifier', words(
        'could potentially', 'might possibly', 'may perhaps', 'could possibly', 'potencjalnie mogł\\w+', 'być może mogł\\w+')),
    ('generic-conclusion', 'honesty', 'end on a fact or a real plan', words(
        'the future looks bright', 'exciting times (?:lie )?ahead', 'a step in the right direction',
        'przyszłość rysuje się w jasnych barwach', 'to dopiero początek', 'ekscytujące czasy')),
]
EMOJI_LEAD = re.compile(r'^\s*(?:#{1,6}\s*|[-*]\s*)?[\U0001F300-\U0001FAFF☀-➿]', re.M)
INLINE_HEADER = re.compile(r'^\s*[-*]\s+\*\*[^*\n]{1,40}:\*\*', re.M)
BOLD = re.compile(r'\*\*[^*\n]{1,60}\*\*')
CAPS_RUN = re.compile(r'\b(?:[A-ZĄĆĘŁŃÓŚŹŻ]{2,}\s+){2,}[A-ZĄĆĘŁŃÓŚŹŻ]{2,}\b')
TRIPLE = re.compile(r'\b[\wąćęłńóśźż-]+(?: [\wąćęłńóśźż-]+)?, [\wąćęłńóśźż-]+(?: [\wąćęłńóśźż-]+)?,? (?:and|or|i|oraz|lub) [\wąćęłńóśźż-]+', re.I)


def polish(text):
    return len(re.findall(r'[ąćęłńóśźż]', text, re.I)) >= 3 or bool(re.search(r'\b(?:się|jest|nie|oraz|które)\b', text, re.I))


def sentences(text):
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+|\n+', text) if s.strip()]


def check(text):
    found = {}

    def add(pid, category, fix, sample):
        item = found.setdefault(pid, {'id': pid, 'category': category, 'fix': fix, 'count': 0, 'examples': []})
        item['count'] += 1
        if len(item['examples']) < 3:
            item['examples'].append(sample.strip()[:80])

    for pid, category, fix, rx in PATTERNS:
        for m in rx.finditer(text):
            add(pid, category, fix, m.group(0))
    for m in CAPS_RUN.finditer(text):
        line = text[text.rfind('\n', 0, m.start()) + 1: text.find('\n', m.end()) if '\n' in text[m.end():] else len(text)]
        if re.search(r'[a-ząćęłńóśźż]{3,}', line):            # caps inside running text, not a caps headline
            add('caps-emphasis', 'tone', 'write the emphasis into the sentence', m.group(0))
    triples = TRIPLE.findall(text)
    if len(triples) >= 3:
        for t in triples:
            add('forced-three', 'rhythm', 'use as many items as the content has', t)
    run = []
    for s in sentences(text):
        if len(s.split()) <= 3 and not s.endswith(':'):
            run.append(s)
            if len(run) == 3:
                add('staccato-run', 'rhythm', 'merge into one sentence that says it', ' '.join(run))
        else:
            run = []
    for m in EMOJI_LEAD.finditer(text):
        add('emoji-heading', 'hygiene', 'drop the emoji from headings and bullets', m.group(0))
    headers = INLINE_HEADER.findall(text)
    if len(headers) >= 2:
        for h in headers:
            add('inline-header-list', 'hygiene', 'write the items as sentences', h)
    bolds = BOLD.findall(text)
    if len(bolds) >= max(4, len(text.split()) // 60):
        add('bold-overuse', 'hygiene', 'bold one thing or none', f'{len(bolds)} bold phrases')
    if not polish(text):
        dashes = re.findall(r'\S\s?—\s?\S| -- ', text)
        if len(dashes) >= 2:
            add('em-dash', 'hygiene', 'in English prefer a comma, colon, full stop or parentheses unless the brand uses dashes',
                f'{len(dashes)} em dashes')
    kinds = list(found.values())
    repeated = any(k['count'] >= 3 for k in kinds if k['id'] not in ('forced-three', 'inline-header-list', 'staccato-run'))
    verdict = 'cluster' if len(kinds) >= 3 or repeated else 'check' if len(kinds) == 2 else 'clean'
    return {'language': 'pl' if polish(text) else 'en', 'verdict': verdict, 'kinds': len(kinds),
            'findings': sorted(kinds, key=lambda k: -k['count'])}


def main(argv=None):
    parser = argparse.ArgumentParser(description='Find machine-made writing patterns in English or Polish copy.')
    parser.add_argument('file', nargs='?', help="a text or Markdown file, or - for standard input")
    parser.add_argument('--text', help='check this text instead of a file')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args(argv)
    try:
        if args.text is not None:
            text = args.text
        elif args.file == '-':
            text = sys.stdin.read()
        elif args.file:
            text = Path(args.file).read_text(encoding='utf-8')
        else:
            raise ValueError('give a file, - or --text')
    except (OSError, UnicodeDecodeError, ValueError) as error:
        print(f'ai_writing_check: {error}', file=sys.stderr)
        return 3
    report = check(text)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        for f in report['findings']:
            print(f"{f['id']} x{f['count']} ({f['category']}): {' | '.join(f['examples'])} -> {f['fix']}")
        print(f"ai_writing_check: {report['verdict']} ({report['kinds']} pattern kinds, {report['language']})")
    return 1 if report['verdict'] == 'cluster' else 0


if __name__ == '__main__':
    sys.exit(main())
