"""LoC: bounded Gottlieb photographic collection with explicit PD dedication."""
from core import asset, variant, endpoint, https

COLLECTION='https://www.loc.gov/collections/jazz-photography-of-william-p-gottlieb/'
RIGHTS=COLLECTION+'about-this-collection/rights-and-access/'


def search(client, query, category, limit):
    data=client.json(endpoint(COLLECTION,fo='json',q=query,c=limit),
                     'Search the documented Gottlieb collection, whose photographs have an explicit public-domain dedication')
    results=[]
    for row in data.get('results',[]):
        if row.get('access_restricted') or not any('photo' in f.lower() for f in row.get('original_format',[])):continue
        detail=client.json(endpoint(https(row['id']),fo='json',at='item'),
            'Read photograph-specific rights; the collection also includes uncleared newspaper clippings')
        record=detail.get('item',{})
        advisory=record.get('rights_advisory',[])
        advisory=' '.join(advisory) if isinstance(advisory,list) else str(advisory)
        if not ('mr. gottlieb has dedicated these works to the public domain' in advisory.lower()
                and not any(x in advisory.lower() for x in ('not in the public domain','permission is required','all rights reserved'))):continue
        urls=[u.split('#')[0] for u in row.get('image_url',[]) if '.jpg' in u.lower()]
        if not urls:continue
        item=asset('loc',record.get('id') or row['id'],row.get('title'),
            '; '.join(row.get('contributor',[])),row['id'],[variant(u,'provider JPEG') for u in reversed(urls)],
            RIGHTS,category,warnings=[advisory,'Limited to Gottlieb photographs; privacy/publicity and intended-use review still apply.'])
        item.update(license='Public domain (Gottlieb dedication)',rights_status='eligible')
        item['attribution']=f"{item['title']} — {item['creator']}. {item['source_page']}. {item['license']}: {RIGHTS}"
        results.append(item)
    return results[:limit]
