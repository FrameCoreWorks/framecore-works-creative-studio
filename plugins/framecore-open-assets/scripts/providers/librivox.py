from core import asset, variant, endpoint


def search(client, query, category, limit):
    data = client.json(endpoint('https://librivox.org/api/feed/audiobooks', title=query, format='json',
                               limit=limit, extended=1), 'Search LibriVox and obtain public chapter URLs')
    out = []
    for book in data.get('books', [])[:limit]:
        for section in book.get('sections', [])[:1]:
            authors = '; '.join((a.get('first_name', '') + ' ' + a.get('last_name', '')).strip()
                                for a in book.get('authors', []))
            readers = '; '.join(a.get('display_name', '') for a in section.get('readers', []))
            out.append(asset('librivox', book['id'] + ':' + section['id'], section.get('title'),
                             authors + '; read by ' + readers, book.get('url_librivox'),
                             [variant(section['listen_url'], 'chapter MP3')],
                             'https://librivox.org/pages/public-domain/', category,
                             ['US public-domain claim only. Check both text and recording rights in the target jurisdiction.'],
                             review='review_jurisdiction'))
    return out
