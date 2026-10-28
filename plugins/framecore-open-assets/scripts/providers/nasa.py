from core import asset, variant, endpoint


def search(client, query, category, limit):
    kind = {'photos': 'image', 'audio': 'audio', 'video': 'video'}[category]
    data = client.json(endpoint('https://images-api.nasa.gov/search', q=query, media_type=kind, page_size=limit),
                       'Search NASA Image and Video Library records and their media manifests')
    out = []
    for row in data.get('collection', {}).get('items', [])[:limit]:
        obj = row['data'][0]
        manifest = client.json(row['href'], 'Read the asset manifest and choose a real media rendition')
        extensions = {'image': ('.jpg', '.png'), 'audio': ('.mp3', '.wav'), 'video': ('.mp4',)}[kind]
        urls = [u for u in manifest if isinstance(u, str) and u.lower().endswith(extensions)]
        urls.sort(key=lambda u: (0 if '~preview.' in u else 1 if '~small.' in u else 2, u))
        from urllib.parse import quote
        out.append(asset('nasa', obj['nasa_id'], obj.get('title'), obj.get('photographer') or obj.get('center'),
                         'https://images.nasa.gov/details/' + quote(obj['nasa_id'], safe=''),
                         [variant(u, u.rsplit('/', 1)[-1]) for u in urls],
                         'https://www.nasa.gov/nasa-brand-center/images-and-media/', category,
                         ['NASA is not a blanket CC0 source. Review third-party credits, people, logos and endorsement restrictions.',
                          obj.get('description', '')], review='review_nasa'))
    return out
