from core import asset, variant, endpoint


def search(client, query, category, limit):
    data = client.json(endpoint('https://api.wellcomecollection.org/catalogue/v2/images', query=query, pageSize=limit),
                       'Search Wellcome image records with location-level rights')
    out = []
    for obj in data.get('results', [])[:limit]:
        for loc in obj.get('locations', []):
            if loc.get('locationType', {}).get('id') != 'iiif-image' or not loc.get('url', '').endswith('/info.json'):
                continue
            if not any(c.get('status', {}).get('id') == 'open' for c in loc.get('accessConditions', [])):
                continue
            source = obj.get('source', {})
            out.append(asset('wellcome', obj['id'], source.get('title'), loc.get('credit'),
                             'https://wellcomecollection.org/works/' + source['id'],
                             [variant(loc['url'][:-10] + '/full/800,/0/default.jpg', 'IIIF 800px JPEG')],
                             loc.get('license', {}).get('url'), category))
            break
    return out
