#!/usr/bin/env python3
"""Validate and package this repository locally, without network access."""
import hashlib
import json
from pathlib import Path
import shutil
import stat
import subprocess
import zipfile
from build_install_manifest import verify_source

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugins' / 'framecore-work-creative-studio'
DIST = ROOT / 'dist'
EXCLUDED_DIRS = {'.git', 'dist', 'node_modules', '__pycache__'}


def inventory(directory):
    files = []
    def walk(folder):
        for p in sorted(folder.iterdir()):
            if p.is_symlink():
                raise ValueError('Refusing symlink: ' + str(p.relative_to(directory)))
            if p.is_dir():
                if p.name not in EXCLUDED_DIRS:
                    walk(p)
            elif p.is_file():
                if p.name == '.DS_Store' or p.name.startswith('._') or p.suffix in {'.pyc', '.log'}:
                    continue
                if p.name == '.env' or p.name.startswith('.env.'):
                    raise ValueError('Refusing environment file: ' + str(p.relative_to(directory)))
                files.append(p)
            else:
                raise ValueError('Refusing non-regular path: ' + str(p.relative_to(directory)))
    walk(directory)
    return sorted(files, key=lambda p: p.relative_to(directory).as_posix())


def package(directory, prefix, archive_name):
    items = inventory(directory)
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
    verify_source()
    DIST.mkdir(exist_ok=True)
    outputs = []
    outputs.extend(package(PLUGIN, name, name + '-' + version + '.zip'))
    outputs.extend(package(ROOT, ROOT.name, 'framecore-works-creative-studio-' + version + '-repository.zip'))
    checksums = DIST / 'SHA256SUMS.txt'
    checksums.write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest() + '  ' + p.name + '\n' for p in outputs))
    print(json.dumps({'status': 'PACKAGED_LOCALLY', 'version': version, 'outputs': [str(p) for p in outputs] + [str(checksums)], 'published': False}, indent=2))


if __name__ == '__main__':
    main()
