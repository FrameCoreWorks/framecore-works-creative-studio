#!/usr/bin/env python3
"""Build an uploadable Claude plugin ZIP from the shared package, without network access.

The Claude manifest (.claude-plugin/plugin.json) is generated from the shared
package's plugin.json and exists only inside the archive, so the shared package
inventory stays identical to the saved ChatGPT package. Upload the result in
Claude Desktop under Customize > Plugins > Add > Upload plugin.
"""
import hashlib
import json
from pathlib import Path
import re
import stat
import sys
import zipfile
from package_release import DIST, PLUGIN, inventory

MAX_BYTES = 50 * 1024 * 1024
FRONTMATTER = re.compile(r'^---\n(.*?)\n---\n', re.S)


def manifest():
    source = json.loads((PLUGIN / 'plugin.json').read_text())
    return {
        'name': source['name'],
        'version': source['version'],
        'description': source['description'],
        'author': source['author'],
        'keywords': source['keywords'],
    }


def check_skills():
    names = []
    for skill in sorted((PLUGIN / 'skills').glob('*/SKILL.md')):
        match = FRONTMATTER.match(skill.read_text())
        if not match:
            raise ValueError('Missing frontmatter: ' + skill.parent.name)
        fields = dict(re.findall(r'^([a-z_-]+):\s*(.*)$', match.group(1), re.M))
        if fields.get('name') != skill.parent.name:
            raise ValueError('Skill name does not match its folder: ' + skill.parent.name)
        if not 0 < len(fields.get('description', '')) <= 1024:
            raise ValueError('Description missing or longer than 1024 characters: ' + skill.parent.name)
        names.append(skill.parent.name)
    return names


def main():
    data = manifest()
    skills = check_skills()
    DIST.mkdir(exist_ok=True)
    archive = DIST / f"{data['name']}-claude-{data['version']}.zip"
    temporary = archive.with_suffix('.zip.tmp')
    entries = [('.claude-plugin/plugin.json', (json.dumps(data, indent=2) + '\n').encode())]
    entries += [(p.relative_to(PLUGIN).as_posix(), p.read_bytes()) for p in inventory(PLUGIN)]
    try:
        with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for relative, content in entries:
                entry = zipfile.ZipInfo(relative, date_time=(2026, 1, 1, 0, 0, 0))
                entry.create_system = 3
                entry.external_attr = (stat.S_IFREG | 0o644) << 16
                entry.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(entry, content, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        temporary.replace(archive)
    finally:
        if temporary.exists():
            temporary.unlink()
    size = archive.stat().st_size
    if size > MAX_BYTES:
        raise SystemExit(f'{archive.name} is {size} bytes; the upload limit is {MAX_BYTES}')
    print(json.dumps({
        'archive': str(archive.relative_to(DIST.parent)),
        'version': data['version'],
        'files': len(entries),
        'skills': len(skills),
        'bytes': size,
        'sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
    }, indent=2))


if __name__ == '__main__':
    sys.exit(main())
