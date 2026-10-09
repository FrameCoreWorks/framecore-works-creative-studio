#!/usr/bin/env python3
"""Compare a ChatGPT Work readback of the saved Studio plugin with the release's source inventory.

  python3 scripts/check_hosted_readback.py hosted-readback.json [--source config/install-sources.json]
          [--record verification/hosted-release-1.43.0.json]

The readback is the JSON that Plugin Creator writes after a guarded update (CHATGPT_UPDATE.md, "Readback record"):
plugin and release IDs, the saved version, an inventory of every saved path with its size, SHA-256 hashes for the files
it could read and the paths it could not read. Sizes and hashes are compared with config/install-sources.json, which
lists every packaged file of the release with its size and hash.

Verdicts: full_byte_parity (every source path saved with the same size and hash), path_size_parity (every path and size
matches and every hash given matches, but some files were not hashed), mismatch (a missing path, another size or
hash, or another version). Extra saved paths are listed, not failed: an overlay update cannot delete files, and a user
may add their own. Exit codes: 0 for either parity, 1 for a mismatch, 2 when an input cannot be read.
"""
import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def load(path):
    with open(path, encoding='utf-8') as handle:
        return json.load(handle)


def entries(readback):
    """({path: {'size', 'sha256'}}, [hashed paths missing from the inventory]): the inventory decides what was saved."""
    saved = {}
    for item in readback.get('inventory') or []:
        size = item.get('size_bytes', item.get('bytes'))
        saved[str(item['path'])] = {'size': int(size) if size is not None else None, 'sha256': (str(item['sha256']).lower() if item.get('sha256') else None)}
    orphans = set()
    for key in ('files', 'checks', 'hashes'):
        for item in readback.get(key) or []:
            if not item.get('sha256'):
                continue
            path = str(item['path'])
            if path in saved:
                saved[path]['sha256'] = str(item['sha256']).lower()
            else:
                orphans.add(path)
    return saved, sorted(orphans)


def compare(readback, source):
    expected = {item['path']: item for item in source['files']}
    saved, orphans = entries(readback)
    missing = sorted(set(expected) - set(saved))
    extra = sorted(set(saved) - set(expected))
    size_mismatch, hash_mismatch, hashed = [], [], 0
    for path in sorted(set(expected) & set(saved)):
        want, got = expected[path], saved[path]
        if got['size'] is not None and got['size'] != want['bytes']:
            size_mismatch.append({'path': path, 'source_bytes': want['bytes'], 'saved_bytes': got['size']})
        if got['sha256']:
            hashed += 1
            if got['sha256'] != want['sha256']:
                hash_mismatch.append({'path': path, 'source_sha256': want['sha256'], 'saved_sha256': got['sha256']})
    unsized = sorted(path for path in set(expected) & set(saved) if saved[path]['size'] is None)
    version = readback.get('version')
    problems = []
    if version != source['version']:
        problems.append(f'saved version {version!r} is not the source version {source["version"]!r}')
    if missing:
        problems.append(f'{len(missing)} source paths are not in the saved plugin')
    if size_mismatch:
        problems.append(f'{len(size_mismatch)} saved files have another size')
    if hash_mismatch:
        problems.append(f'{len(hash_mismatch)} saved files have another SHA-256')
    if unsized:
        problems.append(f'{len(unsized)} saved files have no size in the inventory')
    if orphans:
        problems.append(f'{len(orphans)} hashed paths are not in the inventory')
    if problems:
        verdict = 'mismatch'
    elif hashed == len(expected):
        verdict = 'full_byte_parity'
    else:
        verdict = 'path_size_parity'
    return {
        'verdict': verdict,
        'problems': problems,
        'source_version': source['version'],
        'saved_version': version,
        'source_files': len(expected),
        'saved_files': len(saved),
        'hashed_and_matching': hashed - len(hash_mismatch),
        'not_hashed': len(expected) - hashed if not missing else None,
        'missing': missing,
        'extra': extra,
        'size_mismatch': size_mismatch,
        'hash_mismatch': hash_mismatch,
        'unsized': unsized,
        'hashed_not_in_inventory': orphans,
        'unreadable_reported': sorted(str(p) for p in readback.get('unreadable') or []),
    }


def record(readback, report):
    """A hosted-release record in the repository's format, with the comparison as its evidence."""
    return {
        'version': readback.get('version'),
        'date': readback.get('date'),
        'plugin_id': readback.get('plugin_id'),
        'release_id': readback.get('release_id'),
        'scope': readback.get('scope'),
        'audience': readback.get('audience'),
        'source_commit': readback.get('source_commit'),
        'readback_by': readback.get('readback_by', 'ChatGPT Work Plugin Creator, reported by the owner'),
        'summary': {key: report[key] for key in ('verdict', 'source_files', 'saved_files', 'hashed_and_matching', 'not_hashed')},
        'missing': report['missing'],
        'extra': report['extra'],
        'size_mismatch': report['size_mismatch'],
        'hash_mismatch': report['hash_mismatch'],
        'unreadable_reported': report['unreadable_reported'],
        'host_behavior': 'NOT_RUN: a readback shows saved files, not how the client behaves',
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description='Compare a hosted plugin readback with the release inventory.')
    parser.add_argument('readback')
    parser.add_argument('--source', default=str(ROOT / 'config/install-sources.json'))
    parser.add_argument('--record', help='write a hosted-release record here (never overwrites)')
    args = parser.parse_args(argv)
    try:
        readback, source = load(args.readback), load(args.source)
        if not isinstance(readback.get('inventory'), list) or not readback['inventory']:
            raise ValueError('the readback has no inventory of saved paths')
        report = compare(readback, source)
        if args.record:
            out = pathlib.Path(args.record)
            if out.exists():
                raise ValueError(f'Output file already exists: {out}')
            out.write_text(json.dumps(record(readback, report), indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    except (OSError, ValueError, KeyError, TypeError) as error:
        sys.stderr.write(f'{error}\n')
        return 2
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if report['verdict'] == 'mismatch' else 0


if __name__ == '__main__':
    sys.exit(main())
