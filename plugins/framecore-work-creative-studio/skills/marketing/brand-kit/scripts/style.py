"""Evidence parsing from fetched HTML and CSS: colours, fonts, logos, metadata and copy."""
import colorsys
import re
import urllib.parse
from html.parser import HTMLParser

METHOD = 'static-html-css'
NAMED = {'white': '#ffffff', 'black': '#000000'}
# Only CSS keywords and OS stacks; real families (Roboto, Arial) count when they come first in a stack.
GENERIC_FONTS = {
    'serif', 'sans-serif', 'monospace', 'cursive', 'fantasy', 'math', 'fangsong', 'emoji', 'system-ui',
    'ui-sans-serif', 'ui-serif', 'ui-monospace', 'ui-rounded', '-apple-system', 'blinkmacsystemfont',
    'apple color emoji', 'segoe ui emoji', 'segoe ui symbol', 'noto color emoji', 'inherit', 'initial', 'unset',
    'revert', 'revert-layer',
}
SOCIAL = ('instagram.com', 'facebook.com', 'tiktok.com', 'linkedin.com', 'youtube.com', 'x.com', 'twitter.com',
          'pinterest.', 'behance.net', 'dribbble.com', 'threads.net')
FONT_SERVICES = ('fonts.googleapis.com', 'use.typekit.net', 'fonts.bunny.net', 'p.typekit.net')
BUTTONISH = re.compile(r'btn|button|cta', re.I)
COPY_LIMIT = 2000
EVIDENCE_COPY_LIMIT = 4000

_COLOUR = re.compile(r'#[0-9a-fA-F]{3,8}\b|(?:rgba?|hsla?)\([^)]*\)|\b(?:white|black)\b', re.I)
_VAR = re.compile(r'var\(\s*(--[\w-]+)\s*(?:,\s*([^()]*(?:\([^()]*\))?[^()]*))?\)')
_BLOCK = re.compile(r'([^{}]+)\{([^{}]*)\}')
_URL = re.compile(r'url\([^)]*\)', re.I)
_DARK = re.compile(r'dark', re.I)
MIN_ALPHA = 0.3


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


def alpha(value):
    """Opacity of a CSS colour (1 when none is given)."""
    v = value.strip().lower()
    if v.startswith('#') and len(v) in (5, 9):
        digits = v[-1] * 2 if len(v) == 5 else v[-2:]
        return int(digits, 16) / 255
    m = re.search(r'(?:,|/)\s*([\d.]+)(%?)\s*\)$', v)
    if m and (v.startswith('rgba') or v.startswith('hsla') or '/' in v):
        return float(m.group(1)) / (100 if m.group(2) else 1)
    return 1.0


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


ICON_FONTS = re.compile(r'awesome|material (icons|symbols)|icomoon|glyphicons|dashicons|icon', re.I)


def families(value):
    """Named families in a font-family stack, generic keywords and icon fonts left out."""
    out = []
    for part in value.split(','):
        name = re.sub(r'\\(.)', r'\1', part.strip()).strip('"\'').strip()
        if (not name or name.lower() in GENERIC_FONTS or ICON_FONTS.search(name)
                or not re.fullmatch(r"[\w][\w .'-]*", name)):
            continue
        out.append(name)
    return out


def shorthand_families(value):
    """The family list of a `font` shorthand (after size[/line-height])."""
    m = re.search(r'(?:^|\s)[\d.]+(?:px|rem|em|%|pt|vw|vh|ch|ex)(?:\s*/\s*[\w.%]+)?\s+(.+)$', value)
    return families(m.group(1)) if m else []


def _strip_dark(css):
    """Remove @media blocks for a dark colour scheme, so theme overrides do not replace the default values."""
    out, i = [], 0
    for m in re.finditer(r'@media[^{]*prefers-color-scheme\s*:\s*dark[^{]*\{', css, re.I):
        if m.start() < i:
            continue
        out.append(css[i:m.start()])
        depth, j = 1, m.end()
        while j < len(css) and depth:
            depth += {'{': 1, '}': -1}.get(css[j], 0)
            j += 1
        i = j
    out.append(css[i:])
    return ''.join(out)


def _blocks(css):
    css = _strip_dark(re.sub(r'/\*.*?\*/', '', css or '', flags=re.S))
    return [(sel.strip().split(';')[-1].strip(), body) for sel, body in _BLOCK.findall(css)]


def css_variables(css):
    """Custom properties in default (not dark-theme) rules."""
    variables = {}
    for selector, body in _blocks(css):
        if _DARK.search(selector):
            continue
        for prop, value in _declarations(body):
            if prop.startswith('--'):
                variables[prop] = value
    return variables


def resolve(value, variables, depth=5):
    """Replace each var() by its own value, following chains, with the fallback when undefined."""
    def one(m):
        if m.group(1) in variables and depth > 0:
            return resolve(variables[m.group(1)], variables, depth - 1)
        return m.group(2) or ''
    return _VAR.sub(one, value) if depth > 0 else value


def _parts(selector):
    return [p.strip() for p in selector.split(',') if p.strip()] or [selector]


def _declarations(body):
    for decl in body.split(';'):
        if ':' in decl:
            prop, value = decl.split(':', 1)
            yield prop.strip().lower(), value.replace('!important', '').strip()


def parse_css(css, source, variables=None):
    """Colours and fonts in one stylesheet; `variables` adds custom properties defined in other sheets."""
    blocks = _blocks(css)
    own = css_variables(css)
    known = dict(variables or {}, **own)
    result = {'colours': [], 'variables': own, 'fonts': [], 'font_faces': []}
    for selector, body in blocks:
        decls = dict(_declarations(body))
        if selector.lower().startswith('@font-face'):
            src = re.search(r'url\(\s*["\']?([^"\')]+)', decls.get('src', ''))
            result['font_faces'].append({'family': (families(decls.get('font-family', '')) or ['Unknown'])[0],
                                         'src': src.group(1) if src else None, 'source': source})
            continue
        if _DARK.search(selector):
            continue
        for prop, value in decls.items():
            if prop.startswith('--'):
                continue
            ref = _VAR.search(value)
            variable = ref.group(1) if ref else None
            value = _URL.sub(' ', resolve(value, known))
            if prop in ('font-family', 'font'):
                stack = families(value) if prop == 'font-family' else shorthand_families(value)
                for role in _unique([_font_role(p) for p in _parts(selector)]) if stack else []:
                    result['fonts'].append({'family': stack[0], 'role': role, 'selector': selector,
                                            'source': source})
                continue
            for raw in _COLOUR.findall(value):
                hex_ = normalise_colour(raw)
                if not hex_ or alpha(raw) < MIN_ALPHA:
                    continue
                for use in _unique([_use(prop, p) for p in _parts(selector)]):
                    result['colours'].append({'hex': hex_, 'use': use, 'property': prop, 'selector': selector,
                                              'variable': variable, 'source': source})
    return result


class _Page(HTMLParser):
    def __init__(self, url):
        super().__init__(convert_charrefs=True)
        self.url = url
        self.meta = {'title': '', 'description': '', 'site_name': '', 'lang': ''}
        self.headings, self.nav, self.ctas, self.logos, self.font_links, self.social = [], [], [], [], [], []
        self.paragraphs, self.inline_css = [], []
        self.stack, self.header_depth, self.nav_depth, self.svg_depth = [], 0, 0, 0

    def _abs(self, href):
        return urllib.parse.urljoin(self.url, href)

    def handle_starttag(self, tag, attrs):
        a = {k: v or '' for k, v in attrs}
        if a.get('style'):
            selector = tag + ''.join('.' + c for c in a.get('class', '').split())
            self.inline_css.append(f"{selector} {{{a['style']}}}")
        if tag == 'svg':
            self.svg_depth += 1
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
            src = a.get('src') or a.get('data-src') or (a.get('srcset') or a.get('data-srcset') or '').split(' ')[0]
            if src.startswith('data:') and a.get('data-src'):
                src = a['data-src']
            if src and (self.header_depth or 'logo' in hint):
                kind = 'header-img' if self.header_depth else 'logo-img'
                self.logos.append({'kind': kind, 'url': self._abs(src), 'alt': a.get('alt', '')})
        elif tag == 'svg' and self.header_depth and not any(l['kind'] == 'header-svg' for l in self.logos):
            self.logos.append({'kind': 'header-svg', 'url': None, 'note': 'inline SVG in the header'})
        elif tag == 'a' and a.get('href'):
            href = self._abs(a['href'])
            if any(s in urllib.parse.urlsplit(href).netloc for s in SOCIAL):
                self.social.append(href)
        if tag in ('header', 'nav'):
            self.header_depth += tag == 'header'
            self.nav_depth += tag == 'nav'
        if tag == 'title' and self.svg_depth:
            return
        if tag in ('title', 'h1', 'h2', 'h3', 'p', 'button', 'a', 'style'):
            klass = a.get('class', '') + ' ' + a.get('role', '')
            self.stack.append((tag, BUTTONISH.search(klass) is not None, []))

    def handle_endtag(self, tag):
        if tag == 'svg' and self.svg_depth:
            self.svg_depth -= 1
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
            self.meta['title'] = self.meta['title'] or text
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
    inline_css, pages, logos, social, font_links, headings, ctas, nav, copy = [], [], [], [], [], [], [], [], []
    meta = None
    for page in collected.get('pages', []):
        pages.append({'url': page['url'], 'status': page['status']})
        if not page.get('html'):
            continue
        item = parse_html(page['html'], page['url'])
        meta = meta or dict(item['meta'], url=page['url'])
        inline_css.append((item['inline_css'], page['url'] + '#inline-style'))
        seen = {(l['kind'], l['url']) for l in logos}
        logos += [dict(l, page=page['url']) for l in item['logos'] if (l['kind'], l['url']) not in seen]
        social += item['social']
        font_links += item['font_links']
        headings += [dict(h, page=page['url']) for h in item['headings']]
        ctas += item['ctas']
        nav += item['nav']
        copy.append(item['copy_sample'])
    sheets, sources = [], []
    for sheet in collected.get('stylesheets', []):
        sheets.append({'url': sheet['url'], 'status': sheet['status']})
        if sheet.get('css'):
            sources.append((sheet['css'], sheet['url']))
    inline = [(c, s) for c, s in inline_css if c]
    shared = {}
    for css, _ in sources + inline:
        shared.update(css_variables(css))
    parsed_css = [parse_css(css, source, shared) for css, source in sources + inline]
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
