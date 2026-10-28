from core import asset, variant, endpoint, PDM


def search(client, query, category, limit):
    kind = 'audio' if category in ('audio', 'music', 'sfx') else 'video' if category == 'video' else 'bitmap'
    data = client.json(endpoint('https://commons.wikimedia.org/w/api.php', action='query', format='json',
                               generator='search', gsrsearch=query + ' filetype:' + kind,
                               gsrnamespace=6, gsrlimit=limit, prop='imageinfo',
                               iiprop='url|extmetadata|mime', iiurlwidth=800, maxlag=5),
                       'Search Commons file records with creator and file-specific licence metadata')
    out = []
    for page in data.get('query', {}).get('pages', {}).values():
        for info in page.get('imageinfo', [])[:1]:
            meta = info.get('extmetadata', {})
            field = lambda key: meta.get(key, {}).get('value', '')
            licence = field('LicenseUrl')
            if not licence and field('LicenseShortName') == 'Public domain' and field('Copyrighted') == 'False':
                licence = PDM
            links = []
            if kind == 'bitmap' and info.get('thumburl'):
                links.append(variant(info['thumburl'], 'thumbnail'))
            if info.get('url'):
                links.append(variant(info['url'], 'original'))
            warnings = [field('Restrictions')] if field('Restrictions') else []
            out.append(asset('commons', page['pageid'], page['title'], field('Artist'),
                             info.get('descriptionurl'), links, licence, category, warnings,
                             review='blocked' if warnings else None))
    return out
