"""Finna API: image-level rights, not the CC0 metadata licence."""
from urllib.parse import urlencode, urljoin
from core import asset, variant, validate_url, Refused


def search(client, query, category, limit):
    pairs=[('lookfor',query),('limit',limit),('filter[]','online_boolean:1'),
           ('filter[]','format:"0/Image/"'),('filter[]','~usage_rights_ext_str_mv:"0/A Free/"')]
    pairs += [('field[]',f) for f in ('id','title','imagesExtended','nonPresenterAuthors','recordPage')]
    data=client.json('https://api.finna.fi/v1/search?'+urlencode(pairs),
                     'Search online Finna images with free-use filtering, then inspect each image rights record')
    results=[]
    for row in data.get('records',[]):
        for index,image in enumerate(row.get('imagesExtended',[])):
            rights=image.get('rights',{})
            variants=[]
            for file in image.get('highResolution',{}).get('original',[]):
                url=file.get('url','')
                try:validate_url(url,client.policy['allowed_domains'])
                except Refused:continue
                variants.append(variant(url,'original'))
            for label,url in image.get('urls',{}).items():
                variants.append(variant(urljoin('https://api.finna.fi/',url),label))
            if not variants:continue
            authors=row.get('nonPresenterAuthors',[])
            creator='; '.join(a.get('name','') if isinstance(a,dict) else str(a) for a in authors)
            credits='; '.join(x.get('name','') for x in rights.get('rightsHolders',[]))
            item=asset('finna',str(row['id'])+':'+str(index),row.get('title'),creator,
                urljoin('https://www.finna.fi/',row.get('recordPage') or 'Record/'+row['id']),
                variants,rights.get('link',''),category,
                warnings=['Finna aggregation: image rights apply separately from metadata; source institution: '+credits])
            item['attribution']+=' Source: Finna.fi; '+credits
            results.append(item)
            if len(results)>=limit:return results
    return results
