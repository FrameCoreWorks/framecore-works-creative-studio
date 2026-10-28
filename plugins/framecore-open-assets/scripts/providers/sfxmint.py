from core import asset, variant, endpoint, CC0


def search(client, query, category, limit):
    data = client.json(endpoint('https://sfxmint.com/api/v1/search', q=query, response='structured', limit=limit,
                               format='wav'), 'Search only the anonymous SFXMint library, never paid generation')
    out = []
    for obj in data.get('candidates', [])[:limit]:
        if obj.get('license') != 'CC0':
            continue
        variants = []
        for fmt in ('wav', 'mp3', 'ogg'):
            meta = obj.get('format_metadata', {}).get(fmt, {})
            if obj.get(fmt + '_url'):
                variants.append(variant(obj[fmt + '_url'], fmt, sha256=meta.get('sha256'), bytes=meta.get('bytes', 0)))
        out.append(asset('sfxmint', obj['slug'], obj.get('title'), 'SFXMint', obj.get('page_url'), variants,
                         CC0, category, ['Synthetic/AI library sound; not a field recording.',
                                         '20 distinct files/day/network; generation and account routes are excluded.']))
    return out
