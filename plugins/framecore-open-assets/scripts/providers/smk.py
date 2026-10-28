"""SMK OpenAPI search with explicit per-artwork public-domain evidence."""
from core import asset, variant, endpoint


def search(client, query, category, limit):
    data=client.json(endpoint('https://api.smk.dk/api/v1/art/search',keys=query,
        filters='[has_image:true],[public_domain:true]',rows=limit,lang='en'),
        'Search SMK public-domain works and retain each artwork rights URL')
    results=[]
    for row in data.get('items',[]):
        if row.get('public_domain') is not True:continue
        images=[variant(row[key],label) for key,label in [('image_thumbnail','provider thumbnail'),('image_native','native')]
                if row.get(key)]
        if not images:continue
        title=next((x.get('title') for x in row.get('titles',[]) if x.get('title')),row.get('object_number'))
        creator='; '.join(x.get('creator','') for x in row.get('production',[]))
        results.append(asset('smk',row['object_number'],title,creator,row['frontend_url'],images,
                             row.get('rights',''),category,warnings=['Credit: Statens Museum for Kunst (SMK).']))
    return results[:limit]
