from core import asset, variant, endpoint, CC0


def search(client, query, category, limit):
    data = client.json(endpoint('https://collectionapi.metmuseum.org/public/collection/v1.1/search',
                               q=query, hasImages='true', limit=limit), 'Search the documented paginated Met v1.1 API')
    out = []
    for id in (data.get('objectIDs') or [])[:limit]:
        obj = client.json(f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{int(id)}',
                          'Inspect the object public-domain flag and actual image links')
        if obj.get('isPublicDomain') is True and obj.get('primaryImage'):
            links = [variant(obj.get('primaryImageSmall'), 'small')] if obj.get('primaryImageSmall') else []
            links.append(variant(obj['primaryImage'], 'primary'))
            out.append(asset('met', id, obj.get('title'), obj.get('artistDisplayName'),
                             obj.get('objectURL'), links, CC0, category))
    return out
