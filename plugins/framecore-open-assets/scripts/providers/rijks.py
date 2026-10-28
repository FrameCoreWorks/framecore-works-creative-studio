"""Current keyless Linked Art search and rights on each digital image object."""
from core import asset, variant, endpoint, license_policy


def search(client, query, category, limit):
    data=client.json(endpoint('https://data.rijksmuseum.nl/search/collection',title=query,imageAvailable='true'),
                     'Search the current keyless Rijksmuseum title index',accept='application/ld+json')
    results=[]
    for hit in data.get('orderedItems',[])[:limit]:
        row=client.json(hit['id'],'Resolve Linked Art metadata and image-specific rights',accept='application/ld+json')
        names=[x.get('content','') for x in row.get('identified_by',[]) if x.get('type')=='Name']
        title=next((x for x in names if x),hit['id'])
        production=row.get('produced_by',{})
        people=production.get('carried_out_by',[])
        for part in production.get('part',[]):people += part.get('carried_out_by',[])
        creator='; '.join(x.get('_label','') for x in people)
        for statement in row.get('subject_of',[]):
            for digital in statement.get('digitally_carried_by',[]):
                rights=next((x.get('content','') for x in digital.get('referred_to_by',[])
                             if 'creativecommons.org/' in x.get('content','')),'')
                for point in digital.get('access_point',[]):
                    url=point.get('id','')
                    if not url.startswith('https://iiif.micr.io/'):continue
                    small=url.replace('/full/max/','/full/800,/')
                    item=asset('rijks',row['id'].rsplit('/',1)[-1],title,creator,row['id'],
                        [variant(small,'800px JPEG'),variant(url,'full resolution')],rights,category,
                        warnings=['Credit Rijksmuseum; the rights of this digital image apply, not the metadata licence.'],
                        review='blocked' if license_policy(rights)[0] not in ('CC0','PDM') else None)
                    results.append(item)
                    if len(results)>=limit:return results
    return results
