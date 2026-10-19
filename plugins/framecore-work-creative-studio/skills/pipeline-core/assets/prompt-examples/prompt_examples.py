#!/usr/bin/env python3
"""Search and print worked prompt examples for named generators, always with their licence and attribution.

  python3 prompt_examples.py list --model seedance-2.0            # id, aspect, category and title
  python3 prompt_examples.py search "portrait" --surface image     # matches title, summary, category, tags and prompt
  python3 prompt_examples.py show cinematic-route-navigation-guide # the prompt verbatim and its credit line
  python3 prompt_examples.py show <id> --json
  python3 prompt_examples.py excluded                              # what was left out of the source and why

Reads examples.json next to this file; runs nothing and calls no generator.
Exit codes: 0 printed, 1 nothing matched or unknown id, 2 bad data file.
"""
import argparse
import json
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent / 'examples.json'
LICENCE_URLS = {'CC-BY-4.0': 'https://creativecommons.org/licenses/by/4.0/',
                'Apache-2.0': 'https://www.apache.org/licenses/LICENSE-2.0', 'MIT': 'https://opensource.org/license/mit'}


def load(path=DATA):
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    for record in data['records']:
        source = record.get('source') or {}
        if source.get('license') not in LICENCE_URLS or not source.get('author') or not source.get('url'):
            raise ValueError(f"{record.get('id')}: needs an open licence, an author and a source url")
    return data


def credit(record):
    """The attribution line to keep wherever the prompt is reused (CC BY 4.0 requires it, with the changes made)."""
    s = record['source']
    return (f"\"{record['title']}\" by {s['author']} ({s['url']}), via {s['repo']}, licensed {s['license']} "
            f"({LICENCE_URLS[s['license']]}). {record['changes']}")


def matches(record, args):
    if args.surface and record['surface'] != args.surface:
        return False
    if args.model and record['model'] != args.model:
        return False
    if args.category and args.category.lower() not in str(record.get('category', '')).lower():
        return False
    if getattr(args, 'query', None):
        text = ' '.join([record['title'], record.get('summary', ''), str(record.get('category', '')),
                         ' '.join(record.get('tags') or []), record['prompt']]).lower()
        return all(word in text for word in args.query.lower().split())
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(description='Worked prompt examples with licence and attribution; runs nothing.')
    parser.add_argument('action', choices=['list', 'search', 'show', 'excluded'])
    parser.add_argument('query', nargs='?', help='search words, or the id for show')
    for flag in ('--surface', '--model', '--category'):
        parser.add_argument(flag)
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--data', default=str(DATA), help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    try:
        data = load(args.data)
    except (OSError, ValueError, KeyError) as error:
        print(f'prompt_examples: bad data: {error}', file=sys.stderr)
        return 2
    if args.action == 'excluded':
        for item in data['excluded']:
            print(f"{item['id']}: {item['reason']}")
        return 0
    if args.action == 'show':
        record = next((r for r in data['records'] if r['id'] == args.query), None)
        if not record:
            print(f'prompt_examples: no example {args.query}', file=sys.stderr)
            return 1
        if args.json:
            print(json.dumps({**record, 'credit': credit(record)}, indent=2, ensure_ascii=False))
        else:
            print(f"{record['title']} ({record['model']}, {record['aspect']}, {record.get('category')})\n")
            print(record['prompt'])
            print(f"\nCredit: {credit(record)}")
        return 0
    if args.action == 'search' and not args.query:
        print('prompt_examples: search needs words', file=sys.stderr)
        return 1
    found = [r for r in data['records'] if matches(r, args)]
    if args.json:
        print(json.dumps([{k: r[k] for k in ('id', 'surface', 'model', 'aspect', 'category', 'title', 'summary') if k in r}
                          for r in found], indent=2, ensure_ascii=False))
    else:
        for r in found:
            print(f"{r['id']}  [{r['model']}, {r['aspect']}, {r.get('category')}]  {r['title']}")
    return 0 if found else 1


if __name__ == '__main__':
    sys.exit(main())
