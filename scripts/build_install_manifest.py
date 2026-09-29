#!/usr/bin/env python3
"""Build and verify the complete, portable Studio source inventory."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugins' / 'framecore-work-creative-studio'
MANIFEST = ROOT / 'config' / 'install-sources.json'


def files_at(root):
    result = []
    for path in sorted(root.rglob('*')):
        if path.is_symlink():
            raise ValueError('Symlink in source: ' + str(path))
        if path.is_file():
            if path.name == '.env' or path.name.startswith('.env.'):
                raise ValueError('Environment file in source')
            result.append(path)
        elif not path.is_dir():
            raise ValueError('Non-regular source path')
    return result


def inventory(root):
    return [{'path': p.relative_to(root).as_posix(), 'bytes': p.stat().st_size,
             'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
            for p in files_at(root)]


def build():
    plugin = json.loads((PLUGIN / 'plugin.json').read_text())
    entries = sorted(p.parent.name for p in (PLUGIN / 'skills').glob('*/SKILL.md'))
    return {'schema_version': 1,
            'repository': 'FrameCoreWorks/framecore-works-creative-studio',
            'version': plugin['version'], 'plugin_name': plugin['name'],
            'source_dir': PLUGIN.relative_to(ROOT).as_posix(),
            'source_ref_rule': 'Resolve main or a requested release to one full commit; read this inventory and every source at that commit.',
            'installation_unit': 'complete-plugin-bundle',
            'entrypoints': entries, 'files': inventory(PLUGIN)}


def verify_source():
    declared = json.loads(MANIFEST.read_text())
    if declared != build():
        raise ValueError('Source inventory mismatch; resolve the source before installing or packaging')
    return declared


if __name__ == '__main__':
    MANIFEST.parent.mkdir(exist_ok=True)
    MANIFEST.write_text(json.dumps(build(), indent=2) + '\n')
    print(str(MANIFEST))
