#!/usr/bin/env python3
"""Build a verified update for a saved ChatGPT Work plugin from files read as text, without a release ZIP or network.

  python3 hosted_update.py plan --new NEW.json [--old OLD.json] [--saved DIR | --saved-readback READBACK.json]
                                [--prefix DIR] --out plan.json
  python3 hosted_update.py pack --new NEW.json [--prefix DIR] --plan plan.json --files DIR --out delta.zip

ChatGPT Work cannot download release assets and its update tool does not take a URL (owner report 2026-10-29). It can
read repository files as text through the GitHub connector and run Python offline, so the update is built there:

- NEW/OLD are the public inventories of the target and of the saved version: config/install-sources.json at those
  commits (path, bytes, sha256), or a GitHub git-tree listing (path, git blob sha) narrowed to the plugin with --prefix.
- plan compares the saved plugin (its files in DIR, or a readback JSON with sha256 hashes) three ways with OLD and
  NEW: files to read (changed upstream, new, or unknown), exact delete_paths (retired upstream and unchanged here),
  private overlays kept untouched, and paths needing review (edited here and changed upstream). Without OLD the
  baseline is unknown: nothing is deleted and every difference is reviewed.
- pack checks every read file (PATH, or PATH.b64 holding base64 for a binary file) against NEW and writes a ZIP with
  only those files plus DELTA.zip.json (delete_paths, review, hashes). Any missing or altered file stops it: nothing
  is written. The update tool overlays the ZIP on the saved release, so omitted files are kept.
Standard library only. Exit codes: 0 done, 1 verification failed, 2 bad input.
"""
import argparse
import base64
import hashlib
import json
import pathlib
import sys
import zipfile


def digest(algo, data):
    if algo == 'git':
        return hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()
    return hashlib.sha256(data).hexdigest()


def load_inventory(data, prefix=''):
    """{path: (algo, hex digest, bytes or None)} from install-sources.json or a GitHub git-tree listing."""
    prefix = prefix.strip('/') + '/' if prefix.strip('/') else ''
    out = {}
    if 'tree' in data:
        for item in data['tree']:
            if item.get('type') == 'blob' and item['path'].startswith(prefix):
                out[item['path'][len(prefix):]] = ('git', item['sha'].lower(), item.get('size'))
    else:
        for item in data['files']:
            if item['path'].startswith(prefix):
                out[item['path'][len(prefix):]] = ('sha256', item['sha256'].lower(), item.get('bytes'))
    return out


def saved_from_files(files):
    """{path: {'sha256', 'git'}} for saved file bytes."""
    return {p: {'sha256': digest('sha256', d), 'git': digest('git', d)} for p, d in files.items()}


def saved_from_dir(root):
    root = pathlib.Path(root)
    return saved_from_files({p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob('*') if p.is_file()})


def saved_from_readback(readback):
    """Saved state from a Plugin Creator readback (CHATGPT_UPDATE.md): inventory paths, sha256 where it was hashed."""
    saved = {str(i['path']): {} for i in readback.get('inventory') or []}
    for key in ('files', 'checks', 'hashes'):
        for item in readback.get(key) or []:
            if item.get('sha256'):
                saved.setdefault(str(item['path']), {})['sha256'] = str(item['sha256']).lower()
    return saved


def same(saved_entry, inv_entry):
    """True/False when the saved copy's hash is known, None when it was not hashed."""
    if saved_entry is None or inv_entry is None:
        return False
    have = saved_entry.get(inv_entry[0])
    return None if have is None else have == inv_entry[1]


def plan(new, saved, old=None):
    fetch, review, overlay_kept, delete_paths = [], [], [], []
    for path in sorted(new):
        if path not in saved:
            fetch.append(path)
            continue
        if same(saved[path], new[path]):
            continue
        if old is not None and path in old:
            was_old = same(saved[path], old[path])
            if was_old:
                fetch.append(path)
                continue
            if was_old is False and old[path][1] == new[path][1]:
                overlay_kept.append(path)
                continue
            fetch.append(path)
            review.append({'path': path, 'reason': 'saved copy not hashed; fetched public file replaces it' if was_old is None
                           else 'saved copy differs from old and new public source'})
            continue
        fetch.append(path)
        review.append({'path': path, 'reason': 'baseline unknown: saved copy differs from new public source' if old is None
                       else 'a private file sits at a new public path'})
    if old is not None:
        for path in sorted(set(old) - set(new)):
            if path not in saved:
                continue
            was_old = same(saved[path], old[path])
            if was_old:
                delete_paths.append(path)
            elif was_old is None:
                review.append({'path': path, 'reason': 'saved copy not hashed; delete only after confirming it equals the old public file'})
            else:
                review.append({'path': path, 'reason': 'retired upstream but edited here; kept'})
    public = set(new) | set(old or {})
    return {'fetch': fetch, 'delete_paths': delete_paths, 'review': review, 'overlay_kept': overlay_kept,
            'private_kept': sorted(set(saved) - public), 'baseline_unknown': old is None,
            'already_current': not fetch and not delete_paths}


def pack(new, plan_data, files_dir, out):
    files_dir, out = pathlib.Path(files_dir), pathlib.Path(out)
    errors, verified = [], {}
    for path in plan_data['fetch']:
        if path not in new:
            errors.append(f'{path}: not in the new inventory')
            continue
        plain, b64 = files_dir / path, files_dir / (path + '.b64')
        if plain.is_file():
            data = plain.read_bytes()
        elif b64.is_file():
            data = base64.b64decode(b64.read_text(encoding='ascii'), validate=False)
        else:
            errors.append(f'{path}: not read (save it as {path}, or {path}.b64 for a binary file)')
            continue
        algo, want, size = new[path]
        if digest(algo, data) != want or (size is not None and size != len(data)):
            errors.append(f'{path}: content differs from the source ({len(data)} bytes, {algo} {digest(algo, data)[:12]}, '
                          f'expected {size} bytes, {want[:12]}); read it again unchanged or as base64')
            continue
        verified[path] = data
    if errors:
        return {'ok': False, 'errors': errors}
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(verified):
            info = zipfile.ZipInfo(path, date_time=(1980, 1, 1, 0, 0, 0))
            info.external_attr = 0o644 << 16
            archive.writestr(info, verified[path], zipfile.ZIP_DEFLATED)
    summary = {'ok': True, 'zip': out.name, 'zip_sha256': digest('sha256', out.read_bytes()), 'verified': len(verified),
               'files': sorted(verified), 'delete_paths': plan_data.get('delete_paths', []), 'review': plan_data.get('review', [])}
    pathlib.Path(str(out) + '.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    return summary


def read_json(path):
    with open(path, encoding='utf-8') as handle:
        return json.load(handle)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('plan')
    p.add_argument('--new', required=True)
    p.add_argument('--old')
    p.add_argument('--prefix', default='')
    group = p.add_mutually_exclusive_group()
    group.add_argument('--saved', help='directory holding the saved plugin files')
    group.add_argument('--saved-readback', help='readback JSON of the saved plugin')
    p.add_argument('--out', required=True)
    k = sub.add_parser('pack')
    k.add_argument('--new', required=True)
    k.add_argument('--prefix', default='')
    k.add_argument('--plan', required=True)
    k.add_argument('--files', required=True)
    k.add_argument('--out', required=True)
    args = parser.parse_args(argv)
    try:
        new = load_inventory(read_json(args.new), args.prefix)
        if args.command == 'plan':
            old = load_inventory(read_json(args.old), args.prefix) if args.old else None
            saved = saved_from_dir(args.saved) if args.saved else saved_from_readback(read_json(args.saved_readback)) if args.saved_readback else {}
            result = plan(new, saved, old)
            pathlib.Path(args.out).write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
            print(json.dumps({k: (len(v) if isinstance(v, list) else v) for k, v in result.items()}))
            return 0
        result = pack(new, read_json(args.plan), args.files, args.out)
    except (OSError, ValueError, KeyError) as error:
        print(f'hosted_update: {error}', file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    sys.exit(main())
