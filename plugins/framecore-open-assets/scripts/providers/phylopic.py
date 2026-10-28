from core import asset, variant, endpoint
from urllib.parse import urljoin

API = 'https://api.phylopic.org'
ACCEPT = 'application/vnd.phylopic.v2+json'


def search(client, query, category, limit):
    index = client.json(endpoint(API + '/nodes', filter_name=query),
                        'Discover the current PhyloPic build before requesting a paginated list', ACCEPT)
    data = client.json(endpoint(API + '/nodes', build=int(index['build']), filter_name=query, page=0, embed_items='true'),
                       'Test a page pinned to the API-returned current build instead of an unpinned page', ACCEPT)
    out = []
    for node in data.get('_embedded', {}).get('items', [])[:limit]:
        primary = node.get('_links', {}).get('primaryImage')
        if not primary:
            continue
        obj = client.json(urljoin(API, primary['href']), 'Read the selected silhouette rights and PNG variants', ACCEPT)
        links = obj['_links']
        files = links.get('rasterFiles', [])
        out.append(asset('phylopic', obj['uuid'], primary.get('title') or query,
                         obj.get('attribution') or links.get('contributor', {}).get('title'),
                         'https://www.phylopic.org/images/' + obj['uuid'],
                         [variant(x['href'], x.get('sizes', '') + ' PNG') for x in reversed(files)],
                         links.get('license', {}).get('href'), category))
    return out
