"""Build the motion technique atlas from awesome-ai-motion and the HyperFrames registry, both at pinned commits.

    python3 scripts/build_technique_atlas.py <awesome-ai-motion checkout> <hyperframes checkout>

The first checkout must be at ATLAS_COMMIT, the second at REGISTRY_COMMIT (registry/*/*/registry-item.json is
enough, e.g. a sparse checkout). Only the English, MIT-licensed card text is projected; no card code is copied.
"""
import glob
import json
import re
import subprocess
import sys
from pathlib import Path

ATLAS_REPO, ATLAS_COMMIT = 'gongnyang/awesome-ai-motion', '1e3c249073c61b42ceb556d7800f628d565d9312'
REGISTRY_REPO, REGISTRY_COMMIT = 'heygen-com/hyperframes', '86521b94f592bcf0ca86aba63068893cf658af16'
OUT = Path(__file__).resolve().parent.parent / 'plugins/framecore-work-creative-studio/skills/hyperframes-workflow/assets/technique-atlas/atlas.json'
PURPOSES = {'주목 끌기': 'attention', '설명': 'explain', '비교': 'compare', '순서·흐름': 'sequence', '강조': 'emphasis',
            '전환': 'transition', '데이터 증명': 'data proof', '피드백': 'feedback', '분위기': 'mood', '브랜딩': 'branding'}
MEDIA = {'설명 영상': 'explainer video', '숏폼': 'short form', '스크롤덱': 'scroll deck', '발표': 'presentation',
         '제품 시연': 'product demo', '데이터 스토리': 'data story', '웹 UI': 'web UI'}
LEVELS = {'기본': 'basic', '중급': 'intermediate', '고급': 'advanced'}
STOP = set('the and with for from text reveal effect motion loop transition card'.split())


def tokens(s):
    return {t for t in re.findall(r'[a-z0-9]+', s.lower()) if t not in STOP and len(t) > 2}


def head(path):
    return subprocess.run(['git', '-C', str(path), 'rev-parse', 'HEAD'], capture_output=True, text=True, check=True).stdout.strip()


def candidates(effect, registry):
    """Registry items whose name or title contains every word of the technique's slug or English name."""
    names = [tokens(effect['slug'].replace('-', ' ')), tokens(effect['en'])]
    found = []
    for item in registry:
        words = tokens(item['name'].replace('-', ' ')) | tokens(item.get('title', ''))
        if any(n and n <= words for n in names):
            exact = item['name'] == effect['slug']
            found.append((not exact, len(words), item['name']))
    return [name for _, _, name in sorted(found)[:4]]


def main(argv):
    aam, hf = Path(argv[0]), Path(argv[1])
    for path, want in ((aam, ATLAS_COMMIT), (hf, REGISTRY_COMMIT)):
        if head(path) != want:
            sys.exit(f'{path} is not at the pinned commit {want}')
    index = json.loads((aam / 'index.json').read_text(encoding='utf-8'))
    registry = [json.loads(Path(p).read_text(encoding='utf-8')) for p in sorted(glob.glob(str(hf / 'registry/*/*/registry-item.json')))]
    techniques = []
    for e in sorted(index['effects'], key=lambda x: x['slug']):
        techniques.append({
            'slug': e['slug'], 'name': e['en'],
            'aka': sorted({a for a in e['aka'] if a.isascii() and a.lower() != e['en'].lower()}),
            'family': e['family'], 'level': LEVELS[e['level']],
            'purposes': [PURPOSES[p] for p in e['purposes']], 'media': [MEDIA[m] for m in e['media']],
            'does': e['oneLinerEn'], 'use_when': e['useWhenEn'], 'pairs': e['pairsWith'],
            'clip': e['render'] == 'done', 'registry': candidates(e, registry)})
    atlas = {
        'source': {'repo': ATLAS_REPO, 'commit': ATLAS_COMMIT, 'license': 'MIT, Copyright (c) 2026 gongnyang',
                   'card': f'https://github.com/{ATLAS_REPO}/tree/{ATLAS_COMMIT}/effects/<slug>'},
        'registry': {'repo': REGISTRY_REPO, 'commit': REGISTRY_COMMIT, 'items': len(registry),
                     'note': 'name matches only; confirm with npx hyperframes catalog before use'},
        'families': {k: v['descEn'] for k, v in sorted(index['families'].items())},
        'techniques': techniques}
    lines = [json.dumps({k: v for k, v in atlas.items() if k != 'techniques'}, ensure_ascii=False)[:-1] + ', "techniques": [']
    lines += [json.dumps(t, ensure_ascii=False) + (',' if i < len(techniques) - 1 else '') for i, t in enumerate(techniques)]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text('\n'.join(lines) + '\n]}\n', encoding='utf-8')
    print(f'{len(techniques)} techniques, {sum(bool(t["registry"]) for t in techniques)} with registry candidates -> {OUT}')


if __name__ == '__main__':
    main(sys.argv[1:])
