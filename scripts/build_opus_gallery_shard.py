"""Build the Opus 5.5 gallery shard of the motion prompt library from a pinned awesome-opus5-5-videos checkout.

    python3 -I scripts/build_opus_gallery_shard.py <awesome-opus5-5-videos checkout>          # write the shard
    python3 -I scripts/build_opus_gallery_shard.py <awesome-opus5-5-videos checkout> --check  # report drift only

The checkout must be at REVIEWED_COMMIT. Only metadata is projected (author, links, category, tags, title); creator
prompt text is never copied, because the gallery's credits leave every prompt with its creator. Each record carries
the Studio-written note for its slug from scripts/data/opus-gallery-notes.json. A slug without a note stops the
build; an existing record whose slug left the gallery is kept and marked retired (package paths and IDs are permanent).
To move the pin: check out the new commit, run --check, write notes for the new slugs, update REVIEWED_COMMIT and the
notes file's reviewed_commit together, then build.
"""
import json
import subprocess
import sys
from pathlib import Path

REPO, REVIEWED_COMMIT = 'yihui-dev/awesome-opus5-5-videos', '92aee2f586ac0715cb3cbcb6384834f98a33383d'
ROOT = Path(__file__).resolve().parent.parent
NOTES = ROOT / 'scripts/data/opus-gallery-notes.json'
OUT = ROOT / 'plugins/framecore-work-creative-studio/skills/hyperframes-workflow/assets/motion-prompt-library/specimen-opus-gallery.json'
CATEGORIES = {'motion': 'motion', 'explainer': 'explainers', '3d': '3d', 'interactive': 'interactive'}
LABELS = {'motion': 'Motion', 'explainers': 'Explainer', '3d': '3D', 'interactive': 'Interactive'}
RIGHTS = 'Third-party creator rights; text not redistributed. The gallery compilation is MIT; each prompt and video belongs to its creator.'
VERIFICATION = 'curator_reported_video_exists; not reproduced by Studio'


def head(path):
    return subprocess.run(['git', '-C', str(path), 'rev-parse', 'HEAD'], capture_output=True, text=True, check=True).stdout.strip()


def record(row, note):
    category = CATEGORIES[row['category']]
    entry = {
        'id': 'OPUS-' + row['slug'],
        'category': category,
        'title': row.get('title') or f"{LABELS[category]} reference by @{row['author']}",
        'author': row['author'],
        'tags': row['tech_tags'],
        'source_url': row['post_url'],
        'prompt_source_url': f"https://github.com/{REPO}/blob/{REVIEWED_COMMIT}/prompts/{row['slug']}.md",
        'gallery_url': row['skillry_url'],
        'prompt_origin': 'creator_prompt_link_only',
        'prompt_text': None,
        'prompt_partial': row['prompt_partial'],
        'has_remake': row['has_remake'],
        'mechanism': note['mechanism'],
        'brief_types': note['brief_types'],
        'rights': RIGHTS,
        'verification': VERIFICATION,
        # Games and interactive pieces are related references, not coded-video recipes: opt-in like Specimen's.
        'default_motion_search': category != 'interactive',
        'upstream_commit': REVIEWED_COMMIT,
    }
    if note.get('caution'):
        entry['caution'] = note['caution']
    return entry


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    source, check = Path(argv[1]), '--check' in argv[2:]
    if head(source) != REVIEWED_COMMIT:
        print(f'checkout is at {head(source)}, not the reviewed {REVIEWED_COMMIT}', file=sys.stderr)
    rows = json.loads((source / 'data/videos.json').read_text(encoding='utf-8'))
    notes_file = json.loads(NOTES.read_text(encoding='utf-8'))
    notes = notes_file['notes']
    old = {e['id']: e for e in json.loads(OUT.read_text(encoding='utf-8'))['entries']} if OUT.exists() else {}
    slugs = [r['slug'] for r in rows]
    new = [s for s in slugs if s not in notes]
    gone = sorted(i for i in old if i.removeprefix('OPUS-') not in set(slugs) and not old[i].get('retired'))
    print(json.dumps({'upstream': len(rows), 'notes': len(notes), 'without_note': new, 'left_gallery': gone}, indent=1))
    if check:
        return 1 if new or gone else 0
    if new:
        sys.exit('write a note for every new slug before building')
    if notes_file.get('reviewed_commit') != REVIEWED_COMMIT:
        sys.exit('notes file reviewed_commit differs from REVIEWED_COMMIT')
    entries = [record(r, notes[r['slug']]) for r in rows]
    for i in gone:
        entries.append({**old[i], 'retired': True, 'default_motion_search': False})
    shard = {'schema_version': 1, 'source': f'https://github.com/{REPO}', 'reviewed_commit': REVIEWED_COMMIT,
             'retrieved': '2026-10-24', 'category': 'mixed', 'entries': entries}
    # One record per line keeps the 703-record file small and its diffs readable.
    body = ',\n'.join(json.dumps(e, ensure_ascii=False) for e in entries)
    head_ = json.dumps({k: v for k, v in shard.items() if k != 'entries'}, ensure_ascii=False)[:-1]
    OUT.write_text(head_ + ', "entries": [\n' + body + '\n]}\n', encoding='utf-8')
    print(f'wrote {len(entries)} records to {OUT.relative_to(ROOT)}')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
