"""Bounded, identified public HTTP reads and evidence-based media handling."""
import contextlib
import datetime as dt
import hashlib
import html
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile

VERSION = '0.1.0'
ROOT = Path(__file__).resolve().parents[1]
CC0 = 'https://creativecommons.org/publicdomain/zero/1.0/'
PDM = 'https://creativecommons.org/publicdomain/mark/1.0/'
MAX_FILE = 32 * 1024 * 1024
REGISTRY = json.loads((ROOT / 'providers.json').read_text())


class Refused(Exception):
    def __init__(self, kind, message):
        super().__init__(message)
        self.kind = kind


def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def clean(value):
    return html.unescape(re.sub(r'<[^>]+>', '', str(value or ''))).strip()[:4000]


def endpoint(base, **params):
    return base + '?' + urllib.parse.urlencode(params)


def https(url):
    # Preserve provider-returned host/path; never invent a CDN or fallback host.
    return urllib.parse.quote(str(url).replace('http://', 'https://', 1), safe=':/?&=%+,;@!$()')


def validate_url(url, domains):
    p = urllib.parse.urlsplit(url)
    try:
        port = p.port
    except ValueError:
        raise Refused('unsafe_url', 'Invalid port')
    if (p.scheme != 'https' or p.username or p.password or port not in (None, 443)
            or p.fragment or any(ord(c) < 33 for c in url)):
        raise Refused('unsafe_url', 'Only public HTTPS provider URLs without credentials are allowed')
    host = (p.hostname or '').lower()
    if not any(host == d or (d.startswith('.') and host.endswith(d)) for d in domains):
        raise Refused('unapproved_host', 'Provider returned an unreviewed host: ' + host)
    return url


def classify(status, headers):
    if headers.get('cf-mitigated') == 'challenge':
        return 'cloudflare_challenge'
    if status in (401, 403):
        return 'access_denied'
    if status == 429:
        return 'rate_limited'
    if status >= 500:
        return 'server_error'
    return 'http_error'


class Client:
    def __init__(self, provider, state, host, model, fresh=False):
        if provider not in REGISTRY:
            raise Refused('unknown_provider', provider)
        self.provider, self.policy = provider, REGISTRY[provider]
        if self.policy['policy'] != 'documented':
            raise Refused('policy_hold', self.policy['reason'])
        if not model.strip() or any(ord(c) < 32 for c in model):
            raise Refused('invalid_model', 'Supply the actual agent model identifier')
        self.state, self.host, self.fresh = Path(state), host, fresh
        if ROOT == self.state.resolve() or ROOT in self.state.resolve().parents:
            raise Refused('package_output', 'Keep operational state outside the plugin package')
        self.state.mkdir(parents=True, exist_ok=True)
        self.ua = (f'FrameCoreOpenAssets/{VERSION} '
                   '(https://github.com/FrameCoreWorks/framecore-works-creative-studio; '
                   f'host={host}; model={model})')
        self.trace = []
        self.requests = 0

    @contextlib.contextmanager
    def serial(self):
        lock = self.state / (self.provider + '.lock')
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError:
            raise Refused('busy', 'Another request owns this provider lock; do not run concurrent requests')
        try:
            os.write(fd, str(os.getpid()).encode())
            stamp = self.state / (self.provider + '.last')
            last = float(stamp.read_text()) if stamp.exists() else 0
            delay = self.policy['min_interval_seconds'] - (time.time() - last)
            if delay > 0:
                time.sleep(min(delay, 5))
            yield
        finally:
            (self.state / (self.provider + '.last')).write_text(str(time.time()))
            os.close(fd)
            lock.unlink()

    def get(self, url, hypothesis, cap=8 * 1024 * 1024, accept='application/json'):
        url = validate_url(https(url), self.policy['allowed_domains'])
        if not hypothesis:
            raise Refused('missing_hypothesis', 'Name what this request tests')
        if self.requests >= 30:
            raise Refused('request_budget', 'This command reached its 30-request budget')
        self.requests += 1
        event = {'utc': utc(), 'provider': self.provider, 'url': url, 'hypothesis': hypothesis,
                 'request_headers': {'User-Agent': self.ua, 'Accept': accept}, 'redirects': []}
        cache_key = hashlib.sha256((url + accept).encode()).hexdigest()
        cache = self.state / (cache_key + '.cache.json')
        cached = None
        if cache.exists() and not self.fresh:
            try:
                cached = json.loads(cache.read_text())
                if cached['expires'] > time.time():
                    event.update({'cache_hit': True, 'http_status': None, 'headers': cached['headers']})
                    self.trace.append(event)
                    return cached['body'].encode(), cached['headers']
            except (ValueError, KeyError):
                cached = None
        # No cookies, browser headers, credentials, proxy rotation or hidden retries.
        owner = self
        class Redirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, req, fp, code, msg, headers, newurl):
                validate_url(newurl, owner.policy['allowed_domains'])
                if len(event['redirects']) >= 5:
                    raise Refused('redirect_limit', 'Too many redirects')
                event['redirects'].append({'status': code, 'url': newurl})
                return super().redirect_request(req, fp, code, msg, headers, newurl)
        headers = dict(event['request_headers'])
        if cached and cached.get('etag') and not self.fresh:
            headers['If-None-Match'] = cached['etag']
        import sys
        print(json.dumps({'next_request': event}), file=sys.stderr, flush=True)
        try:
            with self.serial():
                start = time.monotonic()
                opener = urllib.request.build_opener(Redirect())
                try:
                    response = opener.open(urllib.request.Request(url, headers=headers), timeout=25)
                except urllib.error.HTTPError as exc:
                    response = exc
                with response:
                    h = {k.lower(): v for k, v in response.headers.items() if k.lower() in
                         ('content-type', 'content-length', 'cache-control', 'etag', 'last-modified',
                          'retry-after', 'cf-mitigated', 'cf-ray')}
                    event.update({'http_status': response.status, 'headers': h, 'final_url': response.url})
                    if response.status == 304 and cached:
                        event['revalidated'] = True
                        return cached['body'].encode(), cached['headers']
                    if response.status != 200:
                        raise Refused(classify(response.status, h), 'HTTP ' + str(response.status) + '; stop this provider')
                    if h.get('cf-mitigated') == 'challenge':
                        raise Refused('cloudflare_challenge', 'Stop this provider')
                    if int(h.get('content-length', '0')) > cap:
                        raise Refused('size_limit', 'Advertised file exceeds the byte budget')
                    chunks, size = [], 0
                    while True:
                        part = response.read(min(65536, cap + 1 - size))
                        if not part:
                            break
                        chunks.append(part)
                        size += len(part)
                        if size > cap or time.monotonic() - start > 60:
                            raise Refused('size_or_time_limit', 'Response exceeded its byte or time budget')
                    body = b''.join(chunks)
                    event.update({'bytes': size, 'sha256': hashlib.sha256(body).hexdigest()})
                    if body.lstrip()[:100].lower().startswith((b'<!doctype html', b'<html')) or 'text/html' in h.get('content-type', ''):
                        raise Refused('html_response', 'Received HTML instead of the requested data')
                    cc = h.get('cache-control', '').lower()
                    ttl = re.search(r'(?:^|[, ])max-age=(\d+)', cc)
                    # Cache only JSON; no-store/no-cache/private prohibit reuse here.
                    if accept != '*/*' and ttl and not any(x in cc for x in ('no-store', 'no-cache', 'private')):
                        try:
                            text = body.decode(); json.loads(text)
                            cache.write_text(json.dumps({'expires': time.time() + min(int(ttl[1]), 86400),
                                                         'body': text, 'headers': h, 'etag': h.get('etag')}))
                        except (ValueError, UnicodeError):
                            pass
                    elif cache.exists():
                        cache.unlink()
                    return body, h
        except Refused as exc:
            event['error'] = exc.kind
            raise
        except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
            event['error'] = type(exc).__name__
            raise Refused('transport_error', str(exc)) from exc
        finally:
            event['ended_utc'] = utc()
            self.trace.append(event)

    def json(self, url, hypothesis, accept='application/json'):
        body, _ = self.get(url, hypothesis, accept=accept)
        try:
            data = json.loads(body)
        except (ValueError, UnicodeError) as exc:
            raise Refused('invalid_json', 'Provider did not return JSON') from exc
        if isinstance(data, dict) and data.get('error'):
            raise Refused('api_error', clean(data['error']))
        return data


def license_policy(value):
    p = urllib.parse.urlsplit(str(value).replace('http://', 'https://', 1))
    path = p.path.rstrip('/')
    if p.scheme == 'https' and p.hostname == 'creativecommons.org' and not p.username:
        if path == '/publicdomain/zero/1.0':
            return 'CC0', 'eligible'
        if path in ('/publicdomain/mark/1.0', '/share-your-work/public-domain/pdm'):
            return 'PDM', 'eligible'
        m = re.fullmatch(r'/licenses/(by|by-sa)/(1\.0|2\.0|2\.5|3\.0|4\.0)', path)
        if m:
            return 'CC ' + m[1].upper() + ' ' + m[2], 'review_sa' if m[1] == 'by-sa' else 'eligible'
    return clean(value) or 'Unknown', 'blocked'


def asset(provider, id, title, creator, source, variants, license_url, category, warnings=None, review=None):
    license_name, status = license_policy(license_url)
    if review:
        status = review
    if license_name.startswith('CC BY') and not clean(creator):
        status = 'blocked'
    return {'schema_version': 1, 'provider': provider, 'id': str(id), 'title': clean(title),
            'creator': clean(creator), 'source_page': source, 'license': license_name,
            'license_url': license_url, 'rights_status': status, 'category': category,
            'variants': [v for v in variants if v.get('url')], 'warnings': warnings or [],
            'attribution': f'{clean(title)} — {clean(creator) or provider}. {source}. {license_name}: {license_url}',
            'retrieved_utc': utc()}


def variant(url, label='', **extra):
    return {'url': https(url), 'label': label, **extra}


def decode(path):
    prefix = path.read_bytes()[:16]
    if prefix.startswith((b'\xff\xd8', b'\x89PNG', b'GIF8', b'RIFF')) and not prefix[8:12] == b'WAVE':
        try:
            from PIL import Image
            Image.MAX_IMAGE_PIXELS = 40_000_000
            with Image.open(path) as im:
                if im.width * im.height > 40_000_000:
                    raise Refused('pixel_limit', 'Image exceeds 40 million pixels')
                im.load()
                return {'kind': 'image', 'format': im.format, 'width': im.width, 'height': im.height}
        except ImportError:
            raise Refused('decoder_missing', 'Pillow is required to verify images')
    if prefix.startswith(b'PK\x03\x04'):
        from PIL import Image
        Image.MAX_IMAGE_PIXELS = 40_000_000
        count, unverified = 0, []
        with zipfile.ZipFile(path) as z:
            members = z.infolist()
            if len(members) > 100 or sum(x.file_size for x in members) > 128 * 1024 * 1024:
                raise Refused('archive_limit', 'Archive expands beyond its budget')
            for info in members:
                if info.is_dir():
                    continue
                if info.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                    with Image.open(io.BytesIO(z.read(info))) as im:
                        if im.width * im.height > 40_000_000:
                            raise Refused('pixel_limit', 'Archive image exceeds 40 million pixels')
                        im.load(); count += 1
                elif info.filename.lower().endswith(('.blend', '.usdc', '.usda', '.mtlx', '.tres')):
                    unverified.append(info.filename)
                elif not info.filename.lower().endswith(('.txt', '.json', '.xml', '.md')):
                    raise Refused('unsupported_archive', 'Archive contains an unsupported member')
            if not count:
                raise Refused('not_media', 'No decodable images in archive')
            if z.testzip() is not None:
                raise Refused('archive_crc', 'Archive CRC verification failed')
        return {'kind': 'image_package', 'decoded_images': count, 'extracted': False,
                'crc_verified': True, 'unverified_project_members': unverified,
                'warning': 'Only raster images decoded; project files are not executed or approved for execution.'}
    if not shutil.which('ffprobe') or not shutil.which('ffmpeg'):
        raise Refused('decoder_missing', 'FFprobe and FFmpeg are required to verify audio/video')
    if not (prefix.startswith((b'ID3', b'OggS', b'fLaC', b'\x1aE\xdf\xa3'))
            or prefix[4:8] == b'ftyp' or prefix[:4] == b'RIFF' and prefix[8:12] == b'WAVE'
            or len(prefix) > 1 and prefix[0] == 255 and prefix[1] & 224 == 224):
        raise Refused('unsupported_media', 'No supported audio/video signature; playlists and active documents are refused')
    # Local files only; no playlist/network protocols or executable SVG/HTML payloads.
    formats = 'mov,matroska,mp3,wav,ogg,flac,aac'
    probe = subprocess.run(['ffprobe', '-v', 'error', '-protocol_whitelist', 'file,pipe', '-format_whitelist', formats,
                            '-show_streams', '-show_format', '-of', 'json', str(path)],
                           capture_output=True, text=True, timeout=30)
    if probe.returncode:
        raise Refused('not_media', 'FFprobe could not parse the downloaded file')
    data = json.loads(probe.stdout)
    streams = [s for s in data.get('streams', []) if s.get('codec_type') in ('audio', 'video')]
    if not streams:
        raise Refused('not_media', 'No audio or video stream')
    run = subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-xerror', '-threads', '2',
                          '-protocol_whitelist', 'file,pipe', '-format_whitelist', formats,
                          '-i', str(path), '-f', 'null', '-'],
                         capture_output=True, timeout=90)
    if run.returncode:
        raise Refused('decode_failed', 'Full media decode failed')
    return {'kind': 'video' if any(s['codec_type'] == 'video' for s in streams) else 'audio',
            'duration_seconds': data.get('format', {}).get('duration'),
            'codecs': [s.get('codec_name') for s in streams], 'full_decode': True}


def download(client, item, target, choice=0, accept_sa=False, review_note=None, max_bytes=MAX_FILE, technical_only=False):
    if item['provider'] != client.provider:
        raise Refused('provider_mismatch', 'Result belongs to another provider')
    status = item['rights_status']
    if technical_only and status in ('review_sa', 'review_nasa', 'review_jurisdiction'):
        pass
    elif status == 'review_sa' and accept_sa:
        pass
    elif status in ('review_nasa', 'review_jurisdiction') and review_note:
        pass
    elif status != 'eligible':
        raise Refused('rights_blocked', 'Resolve this asset rights gate before downloading: ' + status)
    target = Path(target)
    sidecar = Path(str(target) + '.asset.json')
    if target.exists() or sidecar.exists() or target.is_symlink():
        raise Refused('output_exists', 'Choose a new output path; existing files are never overwritten')
    if ROOT == target.resolve() or ROOT in target.resolve().parents:
        raise Refused('package_output', 'Save downloaded assets outside the plugin package')
    v = item['variants'][choice]
    if v.get('bytes', 0) and int(v['bytes']) > max_bytes:
        raise Refused('size_limit', 'Select a smaller provider rendition')
    if client.provider == 'sfxmint':
        # This local count is conservative; the provider additionally enforces the network-wide quota.
        with client.serial():
            quota = client.state / ('sfxmint-' + utc()[:10] + '.json')
            used = json.loads(quota.read_text()) if quota.exists() else []
            if item['id'] not in used and len(used) >= 20:
                raise Refused('daily_quota', '20 distinct SFXMint sounds reserved today; stop until UTC midnight')
            if item['id'] not in used:
                used.append(item['id']); quota.write_text(json.dumps(used))
    body, headers = client.get(v['url'], 'Download the selected rights-reviewed rendition and verify its media bytes',
                               cap=max_bytes, accept='*/*')
    digest = hashlib.sha256(body).hexdigest()
    if v.get('sha256') and digest != v['sha256']:
        raise Refused('hash_mismatch', 'Provider SHA-256 differs from downloaded bytes')
    if v.get('bytes') and len(body) != int(v['bytes']):
        raise Refused('size_mismatch', 'Provider byte count differs from downloaded bytes')
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=target.parent, suffix=target.suffix)
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(body)
        measured = decode(Path(tmp))
        if item['category'] in ('audio', 'music', 'sfx') and measured['kind'] != 'audio':
            raise Refused('wrong_media_type', 'Expected audio, received a different medium')
        if item['category'] == 'video' and measured['kind'] != 'video':
            raise Refused('wrong_media_type', 'Expected video, received a different medium')
        record = {**item, 'selected_variant': v, 'saved_path': str(target.resolve()),
                  'sha256': digest, 'bytes': len(body), 'response_headers': headers,
                  'verification': measured, 'rights_review_note': review_note,
                  'share_alike_accepted': accept_sa, 'technical_test_only': technical_only,
                  'downloaded_utc': utc()}
        created_target = created_sidecar = False
        try:
            with target.open('xb') as f:
                created_target = True
                f.write(body)
            with sidecar.open('x') as f:
                created_sidecar = True
                json.dump(record, f, indent=2); f.write('\n')
        except Exception:
            if created_sidecar:
                sidecar.unlink(missing_ok=True)
            if created_target:
                target.unlink(missing_ok=True)
            raise
        return record
    finally:
        Path(tmp).unlink(missing_ok=True)
