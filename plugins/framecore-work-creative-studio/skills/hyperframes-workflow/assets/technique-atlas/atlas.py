"""Look up a motion technique by name: what it does, when to use it, what pairs with it, HyperFrames registry candidates.

    python3 atlas.py "morph match cut"            # best matches for a name a brief or a client used
    python3 atlas.py --family transitions --purpose attention --media "short form"
    python3 atlas.py match-cut --json              # one entry as JSON

The atlas is an English projection of gongnyang/awesome-ai-motion (MIT) at a pinned commit; see README.md.
"""
import argparse
import difflib
import json
import re
import sys
from pathlib import Path

ATLAS = Path(__file__).resolve().parent / 'atlas.json'


def load():
    return json.loads(ATLAS.read_text(encoding='utf-8'))


def words(s):
    return set(re.findall(r'[a-z0-9]+', s.lower()))


def score(query, t):
    """Best of exact slug, word overlap and fuzzy similarity against the name, slug and aliases."""
    q = query.lower().strip()
    if q in (t['slug'], t['name'].lower()):
        return 1.0
    best = 0.0
    for label in [t['name'], t['slug'].replace('-', ' ')] + t['aka']:
        lw, qw = words(label), words(q)
        overlap = len(lw & qw) / len(lw | qw) if lw and qw else 0.0
        best = max(best, overlap, difflib.SequenceMatcher(None, q, label.lower()).ratio() * 0.9)
    return best


def find(atlas, query=None, family=None, purpose=None, media=None, limit=5):
    pool = [t for t in atlas['techniques']
            if (not family or t['family'] == family) and (not purpose or purpose in t['purposes'])
            and (not media or media in t['media'])]
    if not query:
        return pool[:limit]
    ranked = sorted(((score(query, t), t['slug'], t) for t in pool), key=lambda x: (-x[0], x[1]))
    return [t for s, _, t in ranked[:limit] if s >= 0.35]


def card_url(atlas, slug):
    return atlas['source']['card'].replace('<slug>', slug)


def show(atlas, t):
    lines = [f"{t['name']} ({t['slug']}; {t['family']}, {t['level']})", f"  does: {t['does']}"]
    lines += [f'  use when: {u}' for u in t['use_when']]
    lines.append(f"  pairs with: {', '.join(t['pairs'])}")
    lines.append(f"  registry candidates: {', '.join(t['registry']) or 'none by name; search npx hyperframes catalog'}")
    lines.append(f"  card{' and clip' if t['clip'] else ''}: {card_url(atlas, t['slug'])}")
    return '\n'.join(lines)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument('query', nargs='?', help='a technique name, alias or slug')
    p.add_argument('--family'); p.add_argument('--purpose'); p.add_argument('--media')
    p.add_argument('--limit', type=int, default=5)
    p.add_argument('--json', action='store_true')
    a = p.parse_args(argv)
    atlas = load()
    if a.family and a.family not in atlas['families']:
        p.error(f"unknown family; one of: {', '.join(atlas['families'])}")
    found = find(atlas, a.query, a.family, a.purpose, a.media, a.limit)
    if not found:
        print('no technique matches; describe the motion in plain words or search npx hyperframes catalog', file=sys.stderr)
        return 1
    print(json.dumps(found, ensure_ascii=False, indent=1) if a.json else '\n\n'.join(show(atlas, t) for t in found))
    return 0


if __name__ == '__main__':
    sys.exit(main())
