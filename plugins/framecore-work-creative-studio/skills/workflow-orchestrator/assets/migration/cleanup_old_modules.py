#!/usr/bin/env python3
"""Find and, on request, remove what an older Creative Studio left inside an updated Studio plugin folder.

Studio 1.178.0 and 1.179.0 deleted the motion module (now the FrameMotion plugin) and the editing and captions module
(now the FrameCut plugin); 1.153.0 deleted old Earshot and Open Assets copies. A host that replaces the whole plugin
folder on update (Claude Code, Codex) leaves nothing behind, but a host that writes the new files over the old folder
(for example a plugin saved again in ChatGPT Work) can keep the old ones, and the model may still read them.

A file is removed only when all of these hold:
  * its path is one of the deleted package files in removed-files.json, and
  * its bytes equal a version Studio actually shipped (Git blob SHA-1), so a file the user changed is kept, and
  * it is not inside a folder the user or another installer added (anything not listed is never touched: runtime
    folders such as motion-runtime, engine-runtime, media-runtime or an installed animate-engine stay).

  python3 cleanup_old_modules.py [--plugin-root DIR] [--json]          # report only (default)
  python3 cleanup_old_modules.py [--plugin-root DIR] --apply [--json]  # remove the safe files, then report

Exit code 0: nothing left to remove; 1: removable leftovers found (report only); 2: error. Nothing outside the plugin
root is read or written, and nothing is uploaded.
"""
import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_ROOT = HERE.parents[3]  # <plugin>/skills/workflow-orchestrator/assets/migration -> <plugin>


def blob_sha(path):
    data = path.read_bytes()
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def scan(root, listing):
    removable, changed = [], []
    for rel, info in listing['files'].items():
        target = root / rel
        if target.is_symlink() or not target.is_file():
            continue
        (removable if blob_sha(target) in info['blobs'] else changed).append(rel)
    # Folders of the deleted modules that still hold anything after the listed files: reported, never removed.
    tops = listing.get('removed_folders', [])
    kept_folders = []
    for top in tops:
        folder = root / top
        if not folder.is_dir():
            continue
        others = [p for p in folder.rglob('*') if p.is_file() and str(p.relative_to(root)) not in listing['files']]
        if others:
            kept_folders.append({'folder': top, 'files_not_from_studio': len(others)})
    return sorted(removable), sorted(changed), kept_folders


def remove(root, rels):
    removed, dirs = [], set()
    for rel in rels:
        target = root / rel
        target.unlink()
        removed.append(rel)
        dirs.update(target.parents)
    # Remove folders left empty by this run, deepest first, never the plugin root or anything above it.
    for folder in sorted((d for d in dirs if root in d.parents), key=lambda d: len(d.parts), reverse=True):
        try:
            folder.rmdir()
        except OSError:
            pass
    return removed


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--plugin-root', default=str(DEFAULT_ROOT), help='the installed Studio plugin folder')
    parser.add_argument('--apply', action='store_true', help='remove the files that are safe to remove')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--listing', default=str(HERE / 'removed-files.json'), help=argparse.SUPPRESS)  # tests only
    args = parser.parse_args()
    root = Path(args.plugin_root).expanduser().resolve()
    try:
        listing = json.loads(Path(args.listing).read_text(encoding='utf-8'))
        manifest = json.loads((root / 'plugin.json').read_text(encoding='utf-8'))
    except (OSError, ValueError) as error:
        print(f'cleanup_old_modules: {error}', file=sys.stderr)
        return 2
    if manifest.get('name') != 'framecore-work-creative-studio':
        print(f'cleanup_old_modules: {root} is not a Creative Studio plugin folder', file=sys.stderr)
        return 2
    removable, changed, kept = scan(root, listing)
    removed = remove(root, removable) if args.apply and removable else []
    report = {
        'plugin_root': str(root),
        'studio_version': manifest.get('version'),
        'mode': 'apply' if args.apply else 'report',
        'removable': [] if args.apply else removable,
        'removed': removed,
        'kept_changed': changed,
        'kept_folders': kept,
    }
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        if removed:
            print(f'Removed {len(removed)} files left by an older Studio:')
            print('\n'.join(f'  {p}' for p in removed))
        elif removable:
            print(f'{len(removable)} files left by an older Studio can be removed (run again with --apply):')
            print('\n'.join(f'  {p}' for p in removable[:50]) + (f'\n  ... and {len(removable) - 50} more' if len(removable) > 50 else ''))
        else:
            print('No files left by an older Studio.')
        if changed:
            print(f'Kept {len(changed)} files at old paths whose content differs from every Studio release (changed by someone):')
            print('\n'.join(f'  {p}' for p in changed))
        for item in kept:
            print(f"Kept {item['folder']}: {item['files_not_from_studio']} files that Studio never shipped (for example an installed runtime).")
    return 1 if removable and not args.apply else 0


if __name__ == '__main__':
    sys.exit(main())
