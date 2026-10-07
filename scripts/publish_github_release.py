#!/usr/bin/env python3
"""Publish already-built release assets from GitHub Actions after digest checks."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REPO = 'FrameCoreWorks/framecore-works-creative-studio'


def api(path, payload=None, method='POST', missing_ok=False):
    cmd = ['gh', 'api', 'repos/' + REPO + '/' + path]
    if payload is not None:
        cmd += ['--method', method, '--input', '-']
    result = subprocess.run(cmd, input=json.dumps(payload) if payload is not None else None,
                            capture_output=True, text=True, timeout=45, check=False)
    if result.returncode:
        if missing_ok and 'HTTP 404' in result.stderr:
            return None
        raise RuntimeError(result.stderr)
    return json.loads(result.stdout)


def main():
    if os.environ.get('GITHUB_ACTIONS') != 'true' or os.environ.get('GITHUB_REPOSITORY') != REPO:
        raise SystemExit('Run only in the authorized repository release workflow')
    commit = os.environ['GITHUB_SHA']
    if not re.fullmatch('[0-9a-f]{40}', commit):
        raise SystemExit('Invalid source commit')
    version = json.loads((ROOT / 'plugins/framecore-work-creative-studio/plugin.json').read_text())['version']
    if not re.fullmatch(r'\d+\.\d+\.\d+', version):
        raise SystemExit('This workflow publishes stable semantic versions only')
    tag = 'v' + version
    assets = [ROOT / 'dist' / name for name in (
        f'framecore-work-creative-studio-{version}.zip',
        f'framecore-work-creative-studio-{version}.zip.inventory.json',
        f'framecore-works-creative-studio-{version}-repository.zip',
        f'framecore-works-creative-studio-{version}-repository.zip.inventory.json',
        f'framecore-motion-player-{version}.html',
        'SHA256SUMS.txt',
    )]
    expected = {p.name: 'sha256:' + hashlib.sha256(p.read_bytes()).hexdigest() for p in assets}
    releases = api('releases?per_page=100')
    matching = [r for r in releases if r['tag_name'] == tag]
    if len(matching) > 1:
        raise RuntimeError('Ambiguous release state')
    release = matching[0] if matching else None
    existing_tag = api('git/ref/tags/' + tag, missing_ok=True)
    if existing_tag and (existing_tag['object']['type'] != 'commit' or existing_tag['object']['sha'] != commit):
        raise RuntimeError('Existing immutable tag belongs to another commit; no replacement performed')
    if release is not None and release['target_commitish'] != commit:
        raise RuntimeError('Existing release has a different source; inspect before recovery')
    if release is None:
        release = api('releases', {
            'tag_name': tag, 'target_commitish': commit,
            'name': 'FrameCore Works Creative Studio ' + version,
            'body': (ROOT / 'RELEASE_NOTES.md').read_text(), 'draft': True, 'prerelease': False,
        })
    remote = {a['name']: a for a in release['assets']}
    if set(remote) - set(expected):
        raise RuntimeError('Unexpected release assets; preserved for review')
    for asset in assets:
        saved = remote.get(asset.name)
        if saved:
            if saved['state'] != 'uploaded' or saved['digest'] != expected[asset.name]:
                raise RuntimeError('Existing asset differs: ' + asset.name)
        else:
            if not release['draft']:
                raise RuntimeError('Published release is incomplete; no blind modification')
            subprocess.run(['gh', 'release', 'upload', tag, str(asset), '--repo', REPO],
                           check=True, timeout=90)
    release = api('releases/' + str(release['id']))
    if len(release['assets']) != len(expected) or any(
            a['state'] != 'uploaded' or a['digest'] != expected.get(a['name'])
            for a in release['assets']):
        raise RuntimeError('Uploaded-asset verification failed; release remains a draft')
    if release['draft']:
        release = api('releases/' + str(release['id']), {
            'draft': False, 'prerelease': False, 'make_latest': 'true',
        }, method='PATCH')
    saved_tag = api('git/ref/tags/' + tag)
    if release['draft'] or not release['published_at'] or saved_tag['object']['sha'] != commit:
        raise RuntimeError('Publication readback mismatch')
    print(json.dumps({'status': 'PUBLISHED_AND_VERIFIED', 'url': release['html_url'],
                      'commit': commit, 'verified_assets': len(expected)}, indent=2))


if __name__ == '__main__':
    main()
