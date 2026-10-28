from core import asset, variant, endpoint, CC0
from urllib.parse import quote


def search(client, query, category, limit):
    data = client.json(endpoint('https://api.polyhaven.com/search', q=query, t='textures', limit=limit),
                       'Search Poly Haven texture catalogue with identifying User-Agent')
    out = []
    for row in data.get('results', [])[:limit]:
        id = row['slug']
        files = client.json('https://api.polyhaven.com/files/' + quote(id, safe=''),
                            'Read the exact texture renditions returned by Poly Haven')
        variants = []
        for channel, resolutions in files.items():
            if channel.lower() not in ('diffuse', 'diff', 'albedo'):
                continue
            for size, formats in resolutions.items():
                for fmt, f in formats.items():
                    if fmt in ('jpg', 'png') and isinstance(f, dict) and f.get('url'):
                        variants.append(variant(f['url'], channel + ' ' + size + ' ' + fmt, bytes=f.get('size', 0)))
        out.append(asset('polyhaven', id, id, 'Poly Haven', 'https://polyhaven.com/a/' + quote(id, safe=''),
                         sorted(variants, key=lambda v: v.get('bytes', 0)), CC0, category,
                         ['Assets provided by Poly Haven (https://polyhaven.com). Display this service credit with results.']))
    return out
