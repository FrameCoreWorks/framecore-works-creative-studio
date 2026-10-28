#!/usr/bin/env python3
"""Import a locally downloaded Open Assets sound without another network request.

Provenance is a local record, not a cryptographic claim of legal clearance. This
checks the bytes and Earshot's narrower licence policy; audit.py still requires
an agent to read and record the source licence. No approval or listening is invented.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import shutil
from urllib.parse import urlsplit
import licences


def decode_audio(path):
    if not shutil.which('ffprobe') or not shutil.which('ffmpeg'):
        raise ValueError('FFprobe and FFmpeg are required at import')
    prefix = path.read_bytes()[:16]
    if not (prefix.startswith((b'ID3', b'OggS', b'fLaC')) or prefix[4:8] == b'ftyp'
            or prefix[:4] == b'RIFF' and prefix[8:12] == b'WAVE'
            or len(prefix) > 1 and prefix[0] == 255 and prefix[1] & 224 == 224):
        raise ValueError('Unsupported audio signature')
    flags = ['-protocol_whitelist', 'file,pipe', '-format_whitelist', 'mov,mp3,wav,ogg,flac,aac']
    probe = subprocess.run(['ffprobe', '-v', 'error', *flags, '-show_streams', '-show_format', '-of', 'json', str(path)],
                           capture_output=True, text=True, timeout=30)
    if probe.returncode:
        raise ValueError('Audio probe failed')
    data = json.loads(probe.stdout)
    streams = [x for x in data.get('streams', []) if not (x.get('disposition') or {}).get('attached_pic')]
    if not any(x.get('codec_type') == 'audio' for x in streams) or any(x.get('codec_type') == 'video' for x in streams):
        raise ValueError('Expected audio without a video stream')
    run = subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-xerror', '-threads', '2', *flags,
                          '-i', str(path), '-map', '0:a:0', '-f', 'null', '-'], capture_output=True, timeout=90)
    if run.returncode:
        raise ValueError('Audio decode failed')
    return {'kind': 'audio', 'full_decode': True, 'duration_seconds': data.get('format', {}).get('duration')}


def prepare(sidecar, root, need):
    root = Path(root).resolve()
    sidecar = Path(sidecar).resolve()
    if sidecar.stat().st_size > 1024 * 1024:
        raise ValueError('Sidecar exceeds 1 MiB')
    row = json.loads(sidecar.read_text())
    if row.get('technical_test_only') is not False or row.get('rights_status') != 'eligible':
        raise ValueError('Only production-eligible downloads may enter Earshot')
    if row.get('category') not in ('audio', 'music', 'sfx') or row.get('verification', {}).get('kind') != 'audio':
        raise ValueError('Expected a decoded audio asset')
    licence = row.get('license')
    url = urlsplit(str(row.get('license_url','')).replace('http://','https://',1))
    canonical = re.sub(r'/(?:deed|legalcode)(?:\.[a-zA-Z_-]+)?/?$', '', url.path).rstrip('/')
    permitted = {'/publicdomain/zero/1.0': 'CC0', '/publicdomain/mark/1.0': 'PDM', '/share-your-work/public-domain/pdm': 'PDM'}
    for version in ('2.0','2.5','3.0','4.0'):
        permitted['/licenses/by/'+version] = 'CC BY '+version
    if url.scheme != 'https' or url.hostname != 'creativecommons.org' or url.username or permitted.get(canonical) != licence:
        raise ValueError('Unrecognized or inconsistent licence label and URL')
    policy = licences.classify('Public Domain Mark 1.0' if licence == 'PDM' else licence)
    if policy['status'] != 'allowed':
        raise ValueError('Earshot licence policy rejects this asset')
    for key in ('provider', 'id', 'title', 'creator', 'source_page', 'license', 'license_url', 'attribution'):
        if not str(row.get(key) or '').strip():
            raise ValueError('Missing provenance: ' + key)
    path = Path(row['saved_path']).resolve()
    path.relative_to(root)
    if not path.is_file() or path.stat().st_size > 32 * 1024 * 1024:
        raise ValueError('Missing or oversized project audio')
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != row.get('sha256') or path.stat().st_size != row.get('bytes'):
        raise ValueError('Downloaded audio changed; verify it again')
    decoded = decode_audio(path)
    aid = 'oa-' + re.sub(r'[^a-zA-Z0-9_-]', '-', str(row['provider']) + '-' + str(row['id']))
    entry = {'id': aid, 'category': row['category'], 'file': path.relative_to(root).as_posix(),
             'title': row['title'], 'author': row['creator'], 'source': row['provider'],
             'page_url': row['source_page'], 'download_url': row['selected_variant']['url'],
             'license': 'Public Domain Mark 1.0' if licence == 'PDM' else row['license'], 'license_url': row['license_url'], 'attribution': row['attribution'],
             'need': need, 'rank': None, 'best_segment': None, 'analysis': {}, 'earshot': {},
             'sha256': digest, 'open_assets_sidecar': str(sidecar),
             'notes': 'Imported without re-downloading. Source licence reading, listening and task fit remain separate reviews.'}
    studio = {'schema_version': 1, 'project_id': root.name, 'assets': [{
        'id': aid, 'revision': digest[:12], 'kind': 'audio', 'role': need, 'state': 'present',
        'locator': str(path), 'sha256': digest, 'depends_on': [],
        'properties': {'requested': {}, 'verified': {
            'download_decode': {'value': decoded, 'method': 'Earshot importer local full audio decode', 'evidence': str(sidecar)},
            'byte_identity': {'value': digest, 'method': 'SHA-256 at Earshot import', 'evidence': str(sidecar)}},
            'unknown': ['creative_fit', 'listening_review']},
        'provenance': {'source': row['source_page'], 'rights': row['license'], 'license_url': row['license_url'],
                       'attribution': row['attribution'], 'provider': row['provider'], 'sidecar': str(sidecar)},
        'review': {'status': 'not_reviewed'}}], 'deliverables': []}
    return entry, studio


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sidecar', required=True, type=Path)
    parser.add_argument('--root', required=True, type=Path)
    parser.add_argument('--need', required=True)
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--studio-out', type=Path)
    args = parser.parse_args()
    try:
        outputs = [p for p in (args.out, args.studio_out) if p is not None]
        if len({p.resolve() for p in outputs}) != len(outputs) or any(p.exists() or p.is_symlink() for p in outputs):
            raise ValueError('Use distinct new output files')
        package = Path(__file__).resolve().parents[4]
        if any(p.resolve().is_relative_to(package) for p in outputs):
            raise ValueError('Write project output outside the plugin')
        entry, studio = prepare(args.sidecar, args.root, args.need)
        for path, data in ((args.out, [entry]), (args.studio_out, studio)):
            if path is not None:
                path.parent.mkdir(parents=True, exist_ok=True)
                with path.open('x') as handle:
                    json.dump(data, handle, indent=2); handle.write('\n')
        print(json.dumps({'status': 'PASS', 'sha256': entry['sha256'], 'manifest': str(args.out),
                          'studio_manifest': str(args.studio_out) if args.studio_out else None,
                          'scope': 'Local byte identity and provenance handoff; no licence-reading or creative acceptance claim'}))
        return 0
    except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({'status': 'FAIL', 'error': str(exc)})); return 2


if __name__ == '__main__':
    raise SystemExit(main())
