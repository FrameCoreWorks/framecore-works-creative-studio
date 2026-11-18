"""Local brand kit catalog: one folder per brand, numbered immutable revisions, an index and a field diff."""
import datetime
import hashlib
import json
import os
import pathlib
import re
import unicodedata

# The top-level fields of Studio's pipeline-core/assets/brand-kit.template.json (checked by package_test).
REQUIRED = ('schema_version', 'name', 'spelling', 'colours', 'fonts', 'logo', 'voice', 'claims', 'legal_lines',
            'do_not')


def default_root():
    return pathlib.Path(os.environ.get('BRAND_KIT_ROOT') or pathlib.Path.home() / '.framecore-studio/brand-kits')


def slugify(text):
    ascii_ = unicodedata.normalize('NFKD', text.replace('ł', 'l').replace('Ł', 'L'))
    ascii_ = ascii_.encode('ascii', 'ignore').decode()
    slug = re.sub(r'[^a-z0-9]+', '-', ascii_.lower()).strip('-')[:60].strip('-')
    if slug:
        return slug
    letters = re.sub(r'\W+', '', text.casefold())
    if not letters:
        raise ValueError(f'no usable brand name in {text!r}')
    return 'brand-' + hashlib.sha256(letters.encode('utf-8')).hexdigest()[:8]


def _same_name(a, b):
    norm = lambda s: re.sub(r'\W+', '', str(s).casefold())
    return norm(a) == norm(b)


def validate(kit):
    if not isinstance(kit, dict):
        raise ValueError('a brand kit is a JSON object')
    missing = [k for k in REQUIRED if k not in kit]
    if missing:
        raise ValueError('brand kit is missing: ' + ', '.join(missing))


def _index_path(root, brand):
    return pathlib.Path(root) / slugify(brand) / 'index.json'


def _index(root, brand):
    path = _index_path(root, brand)
    if not path.is_file():
        return {'brand': slugify(brand), 'revisions': []}
    return json.loads(path.read_text(encoding='utf-8'))


def save(kit, brand, root=None, note=''):
    """Write the next revision; never overwrite one. Returns the revision number."""
    validate(kit)
    root = pathlib.Path(root or default_root())
    folder = root / slugify(brand)
    folder.mkdir(parents=True, exist_ok=True)
    index = _index(root, brand)
    on_disk = [int(m.group(1)) for m in (re.fullmatch(r'rev-(\d+)\.json', p.name) for p in folder.iterdir()) if m]
    rev = max([r['rev'] for r in index['revisions']] + on_disk, default=0) + 1
    data = (json.dumps(kit, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    path = folder / f'rev-{rev:04d}.json'
    with open(path, 'xb') as handle:
        handle.write(data)
    index.setdefault('name', kit.get('name'))
    index['revisions'].append({'rev': rev, 'name': kit.get('name'), 'file': path.name, 'note': note, 'sha256': hashlib.sha256(data).hexdigest(),
                               'saved': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')})
    tmp = _index_path(root, brand).with_suffix('.tmp')
    tmp.write_text(json.dumps(index, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    os.replace(tmp, _index_path(root, brand))
    return rev


def name_mismatch(kit, brand, root=None):
    """The brand's saved name when the kit carries a different one (a rebrand or a wrong --brand), else None."""
    index = _index(pathlib.Path(root or default_root()), brand)
    saved = index.get('name')
    if saved and not _same_name(saved, kit.get('name', '')):
        return saved
    return None


def list_brands(root=None):
    root = pathlib.Path(root or default_root())
    out = []
    for index_file in sorted(root.glob('*/index.json')):
        index = json.loads(index_file.read_text(encoding='utf-8'))
        if index['revisions']:
            last = index['revisions'][-1]
            out.append({'brand': index['brand'], 'latest': last['rev'], 'saved': last['saved'], 'note': last['note']})
    return out


def show(brand, root=None, rev=None):
    root = pathlib.Path(root or default_root())
    index = _index(root, brand)
    if not index['revisions']:
        raise FileNotFoundError(f'no saved kit for {brand!r} in {root}')
    entry = index['revisions'][-1] if rev is None else next((r for r in index['revisions'] if r['rev'] == rev), None)
    if entry is None:
        raise FileNotFoundError(f'{brand!r} has no revision {rev}')
    return json.loads((root / slugify(brand) / entry['file']).read_text(encoding='utf-8'))


def diff(a, b, path=''):
    """Changed fields as 'dotted.path: old -> new' lines (JSON values)."""
    if isinstance(a, dict) and isinstance(b, dict):
        lines = []
        for key in list(a) + [k for k in b if k not in a]:
            sub = f'{path}.{key}' if path else str(key)
            if key not in a or key not in b:
                lines.append(f'{sub}: {_j(a.get(key))} -> {_j(b.get(key))}')
            else:
                lines += diff(a[key], b[key], sub)
        return lines
    return [] if a == b else [f'{path}: {_j(a)} -> {_j(b)}']


def _j(value):
    return json.dumps(value, ensure_ascii=False)
