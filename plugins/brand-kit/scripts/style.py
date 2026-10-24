"""Evidence parsing from fetched HTML and CSS: colours, fonts, logos, metadata and copy."""
import colorsys
import re
import urllib.parse
from html.parser import HTMLParser

METHOD = 'static-html-css'
NAMED = {'white': '#ffffff', 'black': '#000000'}
GENERIC_FONTS = {
    'serif', 'sans-serif', 'monospace', 'cursive', 'fantasy', 'system-ui', 'ui-sans-serif', 'ui-serif',
    'ui-monospace', '-apple-system', 'blinkmacsystemfont', 'segoe ui', 'roboto', 'helvetica', 'helvetica neue',
    'arial', 'georgia', 'times', 'times new roman', 'courier', 'courier new', 'verdana', 'tahoma',
    'apple color emoji', 'segoe ui emoji', 'noto color emoji', 'inherit', 'initial', 'unset', 'var',
}
SOCIAL = ('instagram.com', 'facebook.com', 'tiktok.com', 'linkedin.com', 'youtube.com', 'x.com', 'twitter.com',
          'pinterest.', 'behance.net', 'dribbble.com', 'threads.net')
FONT_SERVICES = ('fonts.googleapis.com', 'use.typekit.net', 'fonts.bunny.net', 'p.typekit.net')
BUTTONISH = re.compile(r'btn|button|cta', re.I)
COPY_LIMIT = 2000
EVIDENCE_COPY_LIMIT = 4000

_COLOUR = re.compile(r'#[0-9a-fA-F]{3,8}\b|(?:rgba?|hsla?)\([^)]*\)|\b(?:white|black)\b', re.I)
_VAR = re.compile(r'var\(\s*(--[\w-]+)\s*(?:,[^)]*)?\)')
_BLOCK = re.compile(r'([^{}]+)\{([^{}]*)\}')


def normalise_colour(value):
    """Return lowercase #rrggbb for a CSS colour, or None when it is not a concrete colour."""
    v = value.strip().lower()
    if v in NAMED:
        return NAMED[v]
    if v.startswith('#'):
        h = v[1:]
        if len(h) in (3, 4):
            h = ''.join(c * 2 for c in h[:3])
        elif len(h) in (6, 8):
            h = h[:6]
        else:
            return None
        return '#' + h if re.fullmatch(r'[0-9a-f]{6}', h) else None
    m = re.fullmatch(r'(rgba?|hsla?)\((.*)\)', v)
    if not m:
        return None
    nums = re.findall(r'[-\d.]+%?', m.group(2))[:3]
    if len(nums) < 3:
        return None
    try:
        if m.group(1).startswith('rgb'):
            rgb = [float(n[:-1]) * 2.55 if n.endswith('%') else float(n) for n in nums]
        else:
            hue = float(nums[0]) / 360
            sat, light = (float(n.rstrip('%')) / 100 for n in nums[1:])
            rgb = [c * 255 for c in colorsys.hls_to_rgb(hue % 1, light, sat)]
    except ValueError:
        return None
    return '#' + ''.join(f'{max(0, min(255, round(c))):02x}' for c in rgb)


def _use(prop, selector):
    page = re.search(r'(^|[\s,])(html|body|:root)\s*($|,)', selector) is not None
    if prop == 'color':
        if re.search(r'(^|[\s,>])a([\s,:.\[]|$)', selector):
            return 'link'
        return 'body-text' if page else 'text'
    if prop.startswith('background'):
        if BUTTONISH.search(selector):
            return 'button'
        return 'page-background' if page else 'background'
    if prop.startswith('border') or prop.startswith('outline'):
        return 'border'
    return 'other'


def _font_role(selector):
    s = selector.lower()
    if re.search(r'\bh[1-6]\b|heading|title|display', s):
        return 'heading'
    if BUTTONISH.search(s):
        return 'button'
    if re.search(r'(^|[\s,])(html|body|:root)\b', s):
        return 'body'
    return 'other'


def families(value):
    out = []
    for part in value.split(','):
        name = part.strip().strip('"\'').strip()
        if name and name.lower() not in GENERIC_FONTS and not name.lower().startswith('var('):
            out.append(name)
    return out


def _declarations(body):
    for decl in body.split(';'):
        if ':' in decl:
            prop, value = decl.split(':', 1)
            yield prop.strip().lower(), value.replace('!important', '').strip()


def parse_css(css, source):
    css = re.sub(r'/\*.*?\*/', '', css or '', flags=re.S)
    blocks = [(sel.strip().split(';')[-1].strip(), body) for sel, body in _BLOCK.findall(css)]
    variables = {}
    for _, body in blocks:
        for prop, value in _declarations(body):
            if prop.startswith('--'):
                variables[prop] = value
    result = {'colours': [], 'variables': variables, 'fonts': [], 'font_faces': []}
    for selector, body in blocks:
        decls = dict(_declarations(body))
        if selector.lower().startswith('@font-face'):
            src = re.search(r'url\(\s*["\']?([^"\')]+)', decls.get('src', ''))
            result['font_faces'].append({'family': (families(decls.get('font-family', '')) or ['Unknown'])[0],
                                         'src': src.group(1) if src else None, 'source': source})
            continue
        for prop, value in decls.items():
            if prop.startswith('--'):
                continue
            variable = None
            ref = _VAR.search(value)
            if ref and ref.group(1) in variables:
                variable, value = ref.group(1), _VAR.sub(variables[ref.group(1)], value)
            if prop == 'font-family':
                for family in families(value):
                    result['fonts'].append({'family': family, 'role': _font_role(selector), 'selector': selector,
                                            'source': source})
                continue
            for raw in _COLOUR.findall(value):
                hex_ = normalise_colour(raw)
                if hex_:
                    result['colours'].append({'hex': hex_, 'use': _use(prop, selector), 'property': prop,
                                              'selector': selector, 'variable': variable, 'source': source})
    return result


class _Page(HTMLParser):
    def __init__(self, url):
        super().__init__(convert_charrefs=True)
        self.url = url
        self.meta = {'title': '', 'description': '', 'site_name': '', 'lang': ''}
        self.headings, self.nav, self.ctas, self.logos, self.font_links, self.social = [], [], [], [], [], []
        self.paragraphs, self.inline_css = [], []
        self.stack, self.text, self.header_depth, self.nav_depth = [], None, 0, 0

    def _abs(self, href):
        return urllib.parse.urljoin(self.url, href)

    def handle_starttag(self, tag, attrs):
        a = {k: v or '' for k, v in attrs}
        if tag == 'html':
            self.meta['lang'] = a.get('lang', '')
        elif tag == 'meta':
            key = (a.get('property') or a.get('name') or '').lower()
            if key == 'description':
                self.meta['description'] = a.get('content', '')
            elif key == 'og:site_name':
                self.meta['site_name'] = a.get('content', '')
            elif key == 'og:image' and a.get('content'):
                self.logos.append({'kind': 'og:image', 'url': self._abs(a['content'])})
        elif tag == 'link' and a.get('href'):
            rel = a.get('rel', '').lower()
            if 'apple-touch-icon' in rel:
                self.logos.append({'kind': 'apple-touch-icon', 'url': self._abs(a['href'])})
            elif 'icon' in rel.split():
                self.logos.append({'kind': 'icon', 'url': self._abs(a['href'])})
            elif any(s in a['href'] for s in FONT_SERVICES):
                self.font_links.append(self._abs(a['href']))
        elif tag == 'img':
            hint = ' '.join(a.get(k, '') for k in ('class', 'id', 'alt', 'src')).lower()
            if self.header_depth or 'logo' in hint:
                kind = 'header-img' if self.header_depth else 'logo-img'
                self.logos.append({'kind': kind, 'url': self._abs(a.get('src', '')), 'alt': a.get('alt', '')})
        elif tag == 'svg' and self.header_depth and not any(l['kind'] == 'header-svg' for l in self.logos):
            self.logos.append({'kind': 'header-svg', 'url': None, 'note': 'inline SVG in the header'})
        elif tag == 'a' and a.get('href'):
            href = self._abs(a['href'])
            if any(s in urllib.parse.urlsplit(href).netloc for s in SOCIAL):
                self.social.append(href)
        if tag in ('header', 'nav'):
            self.header_depth += tag == 'header'
            self.nav_depth += tag == 'nav'
        if tag in ('title', 'h1', 'h2', 'h3', 'p', 'button', 'a', 'style'):
            klass = a.get('class', '') + ' ' + a.get('role', '')
            self.stack.append((tag, BUTTONISH.search(klass) is not None, []))

    def handle_endtag(self, tag):
        if tag == 'header' and self.header_depth:
            self.header_depth -= 1
        if tag == 'nav' and self.nav_depth:
            self.nav_depth -= 1
        if not self.stack or self.stack[-1][0] != tag:
            return
        _, buttonish, parts = self.stack.pop()
        text = ' '.join(''.join(parts).split())
        if self.stack and tag != 'style':
            self.stack[-1][2].append(' ' + text + ' ')
        if tag == 'style':
            self.inline_css.append(''.join(parts))
        elif not text:
            return
        elif tag == 'title':
            self.meta['title'] = text
        elif tag in ('h1', 'h2', 'h3'):
            self.headings.append({'level': int(tag[1]), 'text': text})
        elif tag == 'p':
            self.paragraphs.append(text)
        elif tag == 'button' or (tag == 'a' and buttonish):
            self.ctas.append(text)
        elif tag == 'a' and self.nav_depth:
            self.nav.append(text)

    def handle_data(self, data):
        if self.stack:
            self.stack[-1][2].append(data)


def _unique(items):
    out = []
    for item in items:
        if item not in out:
            out.append(item)
    return out


def parse_html(html, url):
    page = _Page(url)
    page.feed(html or '')
    return {'meta': page.meta, 'headings': page.headings, 'nav': _unique(page.nav), 'ctas': _unique(page.ctas),
            'copy_sample': ' '.join(page.paragraphs)[:COPY_LIMIT], 'logos': page.logos,
            'font_links': _unique(page.font_links), 'social': _unique(page.social),
            'inline_css': '\n'.join(page.inline_css)}


def build_evidence(collected):
    """Aggregate parsed pages and stylesheets into one evidence document."""
    parsed_css, pages, logos, social, font_links, headings, ctas, nav, copy = [], [], [], [], [], [], [], [], []
    meta = None
    for page in collected.get('pages', []):
        pages.append({'url': page['url'], 'status': page['status']})
        if not page.get('html'):
            continue
        item = parse_html(page['html'], page['url'])
        meta = meta or dict(item['meta'], url=page['url'])
        parsed_css.append(parse_css(item['inline_css'], page['url'] + '#inline-style'))
        seen = {(l['kind'], l['url']) for l in logos}
        logos += [dict(l, page=page['url']) for l in item['logos'] if (l['kind'], l['url']) not in seen]
        social += item['social']
        font_links += item['font_links']
        headings += [dict(h, page=page['url']) for h in item['headings']]
        ctas += item['ctas']
        nav += item['nav']
        copy.append(item['copy_sample'])
    sheets = []
    for sheet in collected.get('stylesheets', []):
        sheets.append({'url': sheet['url'], 'status': sheet['status']})
        if sheet.get('css'):
            parsed_css.append(parse_css(sheet['css'], sheet['url']))
    colours, fonts, variables, faces = {}, {}, {}, []
    for css in parsed_css:
        variables.update(css['variables'])
        faces += css['font_faces']
        for c in css['colours']:
            entry = colours.setdefault(c['hex'], {'hex': c['hex'], 'count': 0, 'uses': [], 'variables': [],
                                                  'sources': []})
            entry['count'] += 1
            for key, value in (('uses', c['use']), ('variables', c['variable']), ('sources', c['source'])):
                if value and value not in entry[key]:
                    entry[key].append(value)
        for f in css['fonts']:
            entry = fonts.setdefault(f['family'], {'family': f['family'], 'count': 0, 'roles': [], 'sources': []})
            entry['count'] += 1
            for key, value in (('roles', f['role']), ('sources', f['source'])):
                if value not in entry[key]:
                    entry[key].append(value)
    return {
        'method': METHOD,
        'start_url': collected.get('start_url'),
        'pages': pages,
        'stylesheets': sheets,
        'meta': meta or {},
        'colours': sorted(colours.values(), key=lambda c: -c['count']),
        'variables': variables,
        'fonts': sorted(fonts.values(), key=lambda f: -f['count']),
        'font_faces': faces,
        'font_links': _unique(font_links),
        'logos': logos,
        'headings': headings,
        'nav': _unique(nav),
        'ctas': _unique(ctas),
        'copy_sample': ' '.join(c for c in copy if c)[:EVIDENCE_COPY_LIMIT],
        'social': _unique(social),
    }
