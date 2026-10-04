#!/usr/bin/env python3
"""Build and verify the complete, portable Studio source inventory."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugins' / 'framecore-work-creative-studio'
MANIFEST = ROOT / 'config' / 'install-sources.json'
IDENTITY_BEGIN = '<!-- BEGIN PACKAGE IDENTITY -->'
IDENTITY_END = '<!-- END PACKAGE IDENTITY -->'


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


def sync_package_identity(root=PLUGIN):
    """Explicit release-authoring step; build/verify/install remain read-only."""
    files_at(root)  # Reject symlinks before any write.
    plugin = json.loads((root / 'plugin.json').read_text())
    compatibility = json.loads((root / '.codex-plugin/plugin.json').read_text())
    identity = {key: plugin[key] for key in ('name', 'version')}
    if any(compatibility.get(key) != value for key, value in identity.items()):
        raise ValueError('Resolve manifest identity mismatch before synchronizing the entry')
    entry = root / 'skills/workflow-orchestrator/SKILL.md'
    text = entry.read_text()
    if text.count(IDENTITY_BEGIN) != 1 or text.count(IDENTITY_END) != 1:
        raise ValueError('Expected exactly one package identity block')
    start = text.index(IDENTITY_BEGIN) + len(IDENTITY_BEGIN)
    end = text.index(IDENTITY_END)
    if end < start:
        raise ValueError('Package identity markers are out of order')
    projected = text[:start] + '\n' + json.dumps(identity, separators=(',', ':')) + '\n' + text[end:]
    if projected != text:
        entry.write_text(projected)


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
    sync_package_identity()
    MANIFEST.parent.mkdir(exist_ok=True)
    MANIFEST.write_text(json.dumps(build(), indent=2) + '\n')
    print(str(MANIFEST))
