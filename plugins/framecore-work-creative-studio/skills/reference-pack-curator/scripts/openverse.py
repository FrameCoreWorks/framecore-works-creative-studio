#!/usr/bin/env python3
"""Search Openverse (openly licensed images and audio, https://openverse.org) and return each work with its licence.

  python3 openverse.py "bakery interior"                      # images usable commercially and modifiable, as JSON
  python3 openverse.py "rain on window" --media audio --count 5
  python3 openverse.py "old map" --any-licence                # every licence, NC and ND included
  python3 openverse.py "door slam" --media audio --licence cc0,by   # only these licences (Earshot's policy)

No key or installation: the anonymous API allows about 20 requests a minute and 200 a day. Each result carries the
title, creator, licence, source page, file URL and a ready attribution line for the asset manifest, plus warnings
(share-alike, unknown creator). Openverse does not verify licences: check the source page before client use.
Exit codes: 0 results, 1 no results, 2 rate limit, 3 Openverse unreachable (the reply then gives a search link to
open by hand).
"""
import argparse
import http.client
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

API = 'https://api.openverse.org/v1/'
SITE = 'https://openverse.org/search/'


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


def search(query, media='image', count=10, any_licence=False, opener=urllib.request.urlopen, licence=None):
    params = {'q': query, 'page_size': count}
    if licence:
        params['license'] = licence
    elif not any_licence:
        params['license_type'] = 'commercial,modification'
    request = urllib.request.Request(f'{API}{"audio" if media == "audio" else "images"}/?{urllib.parse.urlencode(params)}',
                                     headers={'User-Agent': 'FrameCore-Studio-openverse/1'})
    # audio searches can take up to a minute
    with opener(request, timeout=90) as response:
        data = json.load(response)
    if not isinstance(data, dict):
        raise ValueError('unexpected reply')
    return {'query': query, 'media': media, 'result_count': data.get('result_count', 0),
            'results': [work(item) for item in data.get('results') or []],
            'note': 'Openverse does not verify licences; check each source page before client use.'}


def unreachable(args, why):
    print(json.dumps({'error': f'Openverse unreachable from here ({why}); search by hand',
                      'link': search_link(args.query, args.media)}))
    return 3


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('query')
    parser.add_argument('--media', choices=('image', 'audio'), default='image')
    parser.add_argument('--count', type=int, default=10, choices=range(1, 21), metavar='1-20')
    parser.add_argument('--any-licence', action='store_true', help='include NC and ND licences')
    parser.add_argument('--licence', help='only these licences, comma-separated (for example cc0,by)')
    args = parser.parse_args(argv)
    try:
        found = search(args.query, args.media, args.count, args.any_licence, licence=args.licence)
    except urllib.error.HTTPError as error:
        if error.code != 429:
            return unreachable(args, f'HTTP {error.code}')
        print(json.dumps({'error': 'Openverse rate limit reached (anonymous: about 20 a minute, 200 a day); '
                          'try later or search by hand', 'link': search_link(args.query, args.media)}))
        return 2
    # OSError covers URLError, timeouts and resets; ValueError a reply that is not the API's JSON
    except (OSError, ValueError, http.client.HTTPException) as error:
        return unreachable(args, error)
    print(json.dumps(found, ensure_ascii=False, indent=2))
    return 0 if found['results'] else 1


if __name__ == '__main__':
    sys.exit(main())
