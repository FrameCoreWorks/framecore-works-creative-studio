from core import asset, variant, endpoint, CC0


def search(client, query, category, limit):
    data = client.json(endpoint('https://ambientcg.com/api/v3/assets', q=query, type='material', limit=limit,
                               include='downloads'), 'Search ambientCG v3 material assets and advertised packages')
    return [asset('ambientcg', obj['id'], obj['id'], 'ambientCG', 'https://ambientcg.com/a/' + obj['id'],
                  [variant(v['url'], v.get('attributes', ''), bytes=v.get('size', 0))
                   for v in sorted(obj.get('downloads', []), key=lambda x: x.get('size', 0))
                   if v.get('extension') == 'zip'], CC0, category,
                  ['Material texture package; not a finished illustration or stock photo.'])
            for obj in data.get('assets', [])[:limit]]
