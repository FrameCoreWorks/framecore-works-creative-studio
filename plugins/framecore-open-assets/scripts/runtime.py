#!/usr/bin/env python3
"""FrameCore Open Assets CLI. Local execution; public read-only provider APIs."""
import argparse
import hashlib
import hmac
import importlib
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile

from core import ROOT, REGISTRY, VERSION, Refused, Client, download, utc

HOSTS = ('chatgpt_work', 'claude_code', 'claude_apps', 'codex')


def fingerprint():
    digest = hashlib.sha256()
    paths = [ROOT / 'providers.json', *sorted((ROOT / 'scripts').rglob('*.py'))]
    for p in paths:
        digest.update(p.relative_to(ROOT).as_posix().encode()); digest.update(p.read_bytes())
    return digest.hexdigest()


def state_key(state):
    path = Path(state) / 'result-signing.key'
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            with os.fdopen(fd, 'wb') as f:
                f.write(os.urandom(32))
        except FileExistsError:
            pass
    return path.read_bytes()


def seal(payload, state):
    raw = json.dumps(payload, sort_keys=True, separators=(',', ':')).encode()
    return {'payload': payload, 'signature': hmac.new(state_key(state), raw, hashlib.sha256).hexdigest()}


def unseal(bundle, state):
    payload = bundle['payload']
    if not (Path(state) / 'result-signing.key').is_file():
        raise Refused('untrusted_result', 'No local provenance key; run a fresh search')
    expected = seal(payload, state)['signature']
    if not hmac.compare_digest(expected, bundle.get('signature', '')) or payload.get('fingerprint') != fingerprint():
        raise Refused('untrusted_result', 'Search result was changed, came from another state directory, or predates this runtime')
    from datetime import datetime, timezone
    age = (datetime.now(timezone.utc) - datetime.fromisoformat(payload['utc'])).total_seconds()
    if not 0 <= age <= 86400:
        raise Refused('stale_result', 'Search again; this result is older than one day')
    return payload


def save_new(path, obj):
    path = Path(path)
    if ROOT == path.resolve() or ROOT in path.resolve().parents:
        raise Refused('package_output', 'Write operational output outside the plugin package')
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open('x') as f:
            json.dump(obj, f, indent=2); f.write('\n')
    except FileExistsError:
        raise Refused('output_exists', 'Output already exists: ' + str(path))


def search_one(client, query, category, limit):
    module = client.policy['module']
    if category not in client.policy['categories']:
        raise Refused('unsupported_category', 'This provider does not implement that category')
    results = importlib.import_module('providers.' + module).search(client, query, category, limit)
    for r in results:
        for v in r['variants']:
            from core import validate_url
            validate_url(v['url'], client.policy['allowed_domains'])
    return results


def proof_path(state, host, provider, category):
    return Path(state) / f'verified-{host}-{provider}-{category}.json'


def proof_valid(state, host, provider, category):
    path = proof_path(state, host, provider, category)
    if not path.exists():
        return False
    try:
        proof = unseal(json.loads(path.read_text()), state)
        return proof.get('status') == 'PASS' and proof.get('host') == host and proof.get('provider') == provider and proof.get('category') == category
    except (Refused, ValueError, KeyError, TypeError, OSError):
        return False


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--state', default=os.environ.get('FRAMECORE_OPEN_ASSETS_STATE',
                        str(Path.home() / '.framecore-open-assets')))
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('status', help='Read local capabilities and provider policy; no network')
    for name in ('search', 'verify', 'download'):
        p = sub.add_parser(name)
        p.add_argument('--host', choices=HOSTS, required=True, help='Actual executing host; never substitute another host label')
        p.add_argument('--model', required=True, help='Actual agent model identifier for honest User-Agent')
        p.add_argument('--out', required=True)
        if name == 'search':
            p.add_argument('--provider', choices=[*REGISTRY, 'all'], required=True)
            p.add_argument('--category', choices=['photos', 'graphics', 'audio', 'music', 'sfx', 'video'], required=True)
            p.add_argument('--query', required=True)
            p.add_argument('--limit', type=int, default=3)
            p.add_argument('--fresh', action='store_true')
        else:
            p.add_argument('--results', required=True)
            p.add_argument('--index', type=int, default=0)
            p.add_argument('--variant', type=int, default=0)
            p.add_argument('--accept-sa', action='store_true')
            p.add_argument('--rights-review-note', help='Item-specific review evidence, intended use and jurisdiction, supplied by the user')
            if name == 'verify':
                p.add_argument('--technical-only', action='store_true',
                               help='Test transport/decoder only; media remains excluded from production reuse')
    args = parser.parse_args(argv)
    clients = []
    try:
        if args.command == 'status':
            import importlib.util
            output = {'version': VERSION, 'fingerprint': fingerprint(), 'python': sys.version.split()[0],
                      'python_ready': sys.version_info >= (3, 10),
                      'pillow': importlib.util.find_spec('PIL') is not None,
                      'ffprobe': bool(shutil.which('ffprobe')), 'ffmpeg': bool(shutil.which('ffmpeg')),
                      'network': 'NOT_RUN', 'providers': REGISTRY,
                      'host_results': {h: {p: {c: 'PASS' if proof_valid(args.state, h, p, c) else 'NOT_RUN'
                                                for c in row['categories']} for p, row in REGISTRY.items()}
                                       for h in HOSTS}}
        elif args.command == 'search':
            if not 1 <= args.limit <= 5 or not 1 <= len(args.query.strip()) <= 240:
                raise Refused('input_limit', 'Use 1-5 results and a query of 1-240 characters')
            if Path(args.out).exists():
                raise Refused('output_exists', 'Choose a new result file before making network calls')
            selected = [args.provider] if args.provider != 'all' else [p for p, row in REGISTRY.items()
                        if row['policy'] == 'documented' and args.category in row['categories']]
            items = []
            for provider in selected:
                client = Client(provider, args.state, args.host, args.model, args.fresh)
                clients.append(client)
                items.extend(search_one(client, args.query, args.category, args.limit))
            payload = {'utc': utc(), 'fingerprint': fingerprint(), 'host': args.host,
                       'query': args.query, 'category': args.category, 'items': items,
                       'trace': [event for c in clients for event in c.trace]}
            output = seal(payload, args.state)
            save_new(args.out, output)
        else:
            if Path(args.results).stat().st_size > 8 * 1024 * 1024:
                raise Refused('result_size', 'Result JSON exceeds 8 MiB')
            payload = unseal(json.loads(Path(args.results).read_text()), args.state)
            if payload['host'] != args.host:
                raise Refused('host_mismatch', 'Run a fresh search in the actual target host')
            if args.index < 0 or args.variant < 0:
                raise Refused('invalid_index', 'Indices start at zero')
            item = payload['items'][args.index]
            provider, category = item['provider'], item['category']
            if args.command == 'download' and not proof_valid(args.state, args.host, provider, category):
                raise Refused('host_not_verified', 'Use verify for the first selected asset on this host/category')
            client = Client(provider, args.state, args.host, args.model, fresh=True); clients.append(client)
            output = download(client, item, args.out, args.variant, args.accept_sa, args.rights_review_note,
                              technical_only=getattr(args, 'technical_only', False))
            output['trace'] = client.trace
            if args.command == 'verify':
                proof = {'utc': utc(), 'fingerprint': fingerprint(), 'host': args.host, 'provider': provider,
                         'category': category, 'status': 'PASS', 'sha256': output['sha256'],
                         'rights_status': item['rights_status'], 'technical_test_only': output['technical_test_only'], 'scope': 'One actual search-to-decoded-file path; not universal rights clearance'}
                path = proof_path(args.state, args.host, provider, category)
                # Replace only this command's readiness record, never user media or result files.
                with tempfile.NamedTemporaryFile('w', dir=path.parent, delete=False) as f:
                    json.dump(seal(proof, args.state), f); temp = f.name
                os.replace(temp, path)
        print(json.dumps(output, indent=2))
        return 0
    except Exception as exc:
        # This is the CLI boundary: malformed provider shapes, decoder failures and corrupt
        # archives must produce a failed result, never a traceback that looks like success.
        print(json.dumps({'status': 'FAIL', 'error': getattr(exc, 'kind', 'invalid_input_or_response'),
                          'message': str(exc), 'trace': [e for c in clients for e in c.trace],
                          'next_action': 'Report this failure and ask before switching provider or route.'}, indent=2))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
