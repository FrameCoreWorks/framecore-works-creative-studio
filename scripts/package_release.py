#!/usr/bin/env python3
"""Validate and package this repository locally, without network access."""
import hashlib
import json
from pathlib import Path
import shutil
import stat
import subprocess
import zipfile
from build_install_manifest import EXCLUDED_DIRS, excluded, verify_source

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugins' / 'framecore-work-creative-studio'
DIST = ROOT / 'dist'
# Repository-ZIP only: host-evaluation candidate snapshots (about 18 MB each) stay in Git as evidence but are not
# shipped to users; each one is a copy of the plugin at a past commit.
REPOSITORY_ONLY_EXCLUDED = ('verification/host-evals/candidates/',)


def inventory(directory, skip=()):
    files = []
    def walk(folder):
        for p in sorted(folder.iterdir()):
            if p.is_symlink():
                raise ValueError('Refusing symlink: ' + str(p.relative_to(directory)))
            if p.is_dir():
                if p.name not in EXCLUDED_DIRS:
                    walk(p)
            elif p.is_file():
                if excluded(p, directory) or p.relative_to(directory).as_posix().startswith(skip):
                    continue
                if p.name == '.env' or p.name.startswith('.env.'):
                    raise ValueError('Refusing environment file: ' + str(p.relative_to(directory)))
                files.append(p)
            else:
                raise ValueError('Refusing non-regular path: ' + str(p.relative_to(directory)))
    walk(directory)
    return sorted(files, key=lambda p: p.relative_to(directory).as_posix())


def package(directory, prefix, archive_name, skip=()):
    items = inventory(directory, skip)
    archive = DIST / archive_name
    temporary = archive.with_suffix(archive.suffix + '.tmp')
    entries = []
    try:
        with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for p in items:
                relative = p.relative_to(directory).as_posix()
                data = p.read_bytes()
                entry = zipfile.ZipInfo(prefix + '/' + relative, date_time=(2026, 1, 1, 0, 0, 0))
                entry.create_system = 3
                entry.external_attr = (stat.S_IFREG | 0o644) << 16
                entry.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(entry, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
                entries.append({'path': relative, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
        temporary.replace(archive)
    finally:
        if temporary.exists():
            temporary.unlink()
    index = DIST / (archive_name + '.inventory.json')
    index.write_text(json.dumps({'archive': archive.name, 'files': entries}, indent=2) + '\n')
    return archive, index


def main():
    node = shutil.which('node')
    if not node:
        raise SystemExit('Node.js is required for existing structural validation.')
    run = subprocess.run([node, str(PLUGIN / 'scripts/validate-studio.mjs')], cwd=PLUGIN, check=False, capture_output=True, text=True)
    if run.returncode:
        raise SystemExit(run.stdout + run.stderr)
    manifest = json.loads((PLUGIN / 'plugin.json').read_text())
    version, name = manifest['version'], manifest['name']
    if '/' in version or '\\' in version or name != PLUGIN.name:
        raise SystemExit('Unsafe or inconsistent manifest identity')
    declared = verify_source()
    DIST.mkdir(exist_ok=True)
    outputs = []
    outputs.extend(package(PLUGIN, name, name + '-' + version + '.zip'))
    # The archive must hold exactly the declared files: paths, sizes and hashes.
    # (Compared by path: the two inventories may list the same files in a different order.)
    packed = {entry['path']: entry for entry in json.loads(outputs[1].read_text())['files']}
    if packed != {entry['path']: entry for entry in declared['files']}:
        raise SystemExit('The plugin ZIP differs from config/install-sources.json; rebuild the manifest from a clean tree')
    outputs.extend(package(ROOT, ROOT.name, 'framecore-works-creative-studio-' + version + '-repository.zip',
                           REPOSITORY_ONLY_EXCLUDED))
    # The motion player: the single-file preview template, byte for byte, as a standalone download.
    player = DIST / ('framecore-motion-player-' + version + '.html')
    player.write_bytes((PLUGIN / 'skills/hyperframes-workflow/assets/single-file-preview/motion-preview.html').read_bytes())
    outputs.append(player)
    checksums = DIST / 'SHA256SUMS.txt'
    checksums.write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest() + '  ' + p.name + '\n' for p in outputs))
    print(json.dumps({'status': 'PACKAGED_LOCALLY', 'version': version, 'outputs': [str(p) for p in outputs] + [str(checksums)], 'published': False}, indent=2))


if __name__ == '__main__':
    main()
