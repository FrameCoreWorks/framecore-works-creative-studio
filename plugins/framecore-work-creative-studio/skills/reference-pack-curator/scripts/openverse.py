#!/usr/bin/env python3
"""Search Openverse (openly licensed images and audio, https://openverse.org) and return each work with its licence.

  python3 openverse.py "bakery interior"                      # images usable commercially and modifiable, as JSON
  python3 openverse.py "rain on window" --media audio --count 5
  python3 openverse.py "old map" --any-licence                # every licence, NC and ND included
  python3 openverse.py "door slam" --media audio --licence cc0,by   # only these licences (Earshot's policy)

No key or installation: the anonymous API allows about 20 requests a minute and 200 a day. Each result carries the
title, creator, licence, source page, file URL and a ready attribution line for the asset manifest, plus warnings
(share-alike, unknown creator). Openverse does not verify licences: check the source page before client use.
Exit codes: 0 results, 1 no results, 2 rate limit, 3 any other failure. A failure prints JSON with `error_type`
(cloudflare_challenge, access_denied, rate_limited, server_error, timeout, connection_error, invalid_response),
`http_status`, `cf_ray`, `content_type`, `retryable` and `suggested_action`, never a secret or the challenge page.
Server errors, timeouts and short rate-limit waits are retried a few times; a Cloudflare challenge never is.
"""
import argparse
import http.client
import json
import sys
import time
from datetime import datetime, timezone
import urllib.error
import urllib.parse
import urllib.request

API = 'https://api.openverse.org/v1/'
SITE = 'https://openverse.org/search/'
ATTEMPTS = 3
BACKOFF = (2, 5)


class Failure(Exception):
    """One classified failure: the fields a workflow needs to decide whether to retry, wait or block the stage."""
    def __init__(self, error_type, retryable, status=None, headers=None, detail=''):
        super().__init__(detail or error_type)
        headers = headers or {}
        self.info = {'error_type': error_type, 'http_status': status, 'retryable': retryable,
                     'content_type': headers.get('Content-Type'), 'cf_mitigated': headers.get('cf-mitigated'),
                     'cf_ray': headers.get('cf-ray'), 'retry_after': headers.get('Retry-After'), 'detail': detail}


def classify(status, headers, detail=''):
    # email.message headers are case-insensitive, so cf-mitigated matches any spelling
    if (headers.get('cf-mitigated') or '').lower() == 'challenge':
        return Failure('cloudflare_challenge', False, status, headers, 'Cloudflare answered with a challenge page instead of API data')
    if status in (401, 403):
        return Failure('access_denied', False, status, headers, detail)
    if status == 429:
        return Failure('rate_limited', True, status, headers, detail)
    if status and status >= 500:
        return Failure('server_error', True, status, headers, detail)
    return Failure('invalid_response', False, status, headers, detail)


def search_link(query, media):
    return SITE + ('audio' if media == 'audio' else 'image') + '?' + urllib.parse.urlencode(
        {'q': query, 'license_type': 'commercial,modification'})


def work(item):
    warnings = []
    if (item.get('license') or '').endswith('-sa'):
        warnings.append('share-alike: a work made from it must carry the same licence')
    if not item.get('creator'):
        warnings.append('creator unknown: attribution is incomplete, check the source page')
    return {key: item.get(key) for key in ('title', 'creator', 'license', 'license_version', 'license_url', 'source',
                                           'foreign_landing_url', 'url', 'attribution', 'duration')
            if item.get(key) is not None} | {'warnings': warnings}


def search(query, media='image', count=10, any_licence=False, opener=None, licence=None):
    opener = opener or urllib.request.urlopen
    params = {'q': query, 'page_size': count}
    if licence:
        params['license'] = licence
    elif not any_licence:
        params['license_type'] = 'commercial,modification'
    request = urllib.request.Request(f'{API}{"audio" if media == "audio" else "images"}/?{urllib.parse.urlencode(params)}',
                                     headers={'User-Agent': 'FrameCore-Studio-openverse/1'})
    try:
        # audio searches can take up to a minute
        with opener(request, timeout=120) as response:
            headers = response.headers if hasattr(response, 'headers') else {}
            if (headers.get('cf-mitigated') or '').lower() == 'challenge':
                raise classify(getattr(response, 'status', None), headers)
            try:
                data = json.load(response)
            except ValueError:
                raise Failure('invalid_response', False, getattr(response, 'status', None), headers,
                              'the reply was not JSON (an HTML page or a cut body)')
    except urllib.error.HTTPError as error:
        raise classify(error.code, error.headers or {}, error.reason)
    except TimeoutError as error:
        raise Failure('timeout', True, detail=str(error))
    except urllib.error.URLError as error:
        kind = 'timeout' if isinstance(error.reason, TimeoutError) else 'connection_error'
        raise Failure(kind, True, detail=str(error.reason))
    except (ConnectionError, http.client.HTTPException) as error:
        raise Failure('connection_error', True, detail=str(error))
    if not isinstance(data, dict):
        raise Failure('invalid_response', False, detail='the reply was JSON but not an API object')
    return {'query': query, 'media': media, 'result_count': data.get('result_count', 0),
            'results': [work(item) for item in data.get('results') or []],
            'note': 'Openverse does not verify licences; check each source page before client use.'}


ACTIONS = {
    'cloudflare_challenge': 'Openverse is blocked from this network by a Cloudflare check; do not retry. If the brief requires Openverse, mark that stage blocked and continue the rest; otherwise name the other permitted source you use.',
    'access_denied': 'Openverse refused access (no Cloudflare check); check credentials or report the status.',
    'rate_limited': 'Openverse rate limit; wait for Retry-After or try later.',
    'server_error': 'Openverse server error; try again later.',
    'timeout': 'Openverse did not answer in time; try again later or with a smaller page.',
    'connection_error': 'No connection to Openverse from this network.',
    'invalid_response': 'Openverse sent an unexpected reply; try again later.',
}


def failure(args, info):
    print(json.dumps({'error': ACTIONS[info['error_type']], **{k: v for k, v in info.items() if v not in (None, '')},
                      'media': args.media, 'endpoint': API + ('audio/' if args.media == 'audio' else 'images/'),
                      'observed_at_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
                      'suggested_action': ACTIONS[info['error_type']], 'link': search_link(args.query, args.media)}))
    return 2 if info['error_type'] == 'rate_limited' else 3


def main(argv=None, sleep=time.sleep):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('query')
    parser.add_argument('--media', choices=('image', 'audio'), default='image')
    parser.add_argument('--count', type=int, default=10, choices=range(1, 21), metavar='1-20')
    parser.add_argument('--any-licence', action='store_true', help='include NC and ND licences')
    parser.add_argument('--licence', help='only these licences, comma-separated (for example cc0,by)')
    args = parser.parse_args(argv)
    for attempt in range(ATTEMPTS):
        try:
            found = search(args.query, args.media, args.count, args.any_licence, licence=args.licence)
            break
        except Failure as error:
            info = error.info
            wait = BACKOFF[min(attempt, len(BACKOFF) - 1)]
            if info['error_type'] == 'rate_limited':
                # wait only for a short, stated Retry-After; a long one is reported, not slept through
                wait = int(info['retry_after']) if (info['retry_after'] or '').isdigit() else None
            if not info['retryable'] or wait is None or wait > 30 or attempt == ATTEMPTS - 1:
                return failure(args, info)
            sleep(wait)
    print(json.dumps(found, ensure_ascii=False, indent=2))
    return 0 if found['results'] else 1


if __name__ == '__main__':
    sys.exit(main())
