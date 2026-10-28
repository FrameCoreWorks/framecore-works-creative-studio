from core import asset, variant, endpoint, CC0


def search(client, query, category, limit):
    data = client.json(endpoint('https://openaccess-api.clevelandart.org/api/artworks/',
                               q=query, cc0=1, has_image=1, limit=limit),
                       'Find Cleveland images and inspect share_license_status')
    out = []
    for obj in data.get('data', [])[:limit]:
        if obj.get('share_license_status') != 'CC0':
            continue
        links = [variant(obj['images'][k]['url'], k) for k in ('web', 'print', 'full')
                 if obj.get('images', {}).get(k, {}).get('url')]
        out.append(asset('cleveland', obj['id'], obj.get('title'),
                         '; '.join(x.get('description', '') for x in obj.get('creators', [])),
                         obj.get('url') or 'https://www.clevelandart.org/art/' + obj['accession_number'],
                         links, CC0, category))
    return out
