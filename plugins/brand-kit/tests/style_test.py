"""brand-kit evidence parsing: colours, fonts, page items. No network."""
import pathlib
import sys
import unittest

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PLUGIN / 'scripts'))
import style  # noqa: E402

FIX = pathlib.Path(__file__).resolve().parent / 'fixtures'
HOME = (FIX / 'home.html').read_text(encoding='utf-8')
CSS = (FIX / 'site.css').read_text(encoding='utf-8')


def collected():
    return {'start_url': 'https://lipa.example/',
            'pages': [{'url': 'https://lipa.example/', 'status': 200, 'html': HOME},
                      {'url': 'https://lipa.example/menu', 'status': 'robots-disallowed', 'html': ''}],
            'stylesheets': [{'url': 'https://lipa.example/css/site.css', 'status': 200, 'css': CSS}]}


class Colours(unittest.TestCase):
    def test_normalise(self):
        cases = {'#ABC': '#aabbcc', '#11223344': '#112233', 'rgb(29, 59, 42)': '#1d3b2a',
                 'rgba(0,0,0,.5)': '#000000', 'hsl(0,100%,50%)': '#ff0000', 'rgb(29 59 42 / 50%)': '#1d3b2a',
                 'white': '#ffffff', 'transparent': None, 'inherit': None, '#12': None}
        for raw, expected in cases.items():
            self.assertEqual(style.normalise_colour(raw), expected, raw)


class Css(unittest.TestCase):
    def setUp(self):
        self.parsed = style.parse_css(CSS, 'site.css')

    def test_variables_and_resolution(self):
        self.assertEqual(self.parsed['variables']['--brand-green'], '#1D3B2A')
        heading = [c for c in self.parsed['colours'] if c['selector'].startswith('h1')]
        self.assertEqual(heading[0]['hex'], '#1d3b2a')
        self.assertEqual(heading[0]['variable'], '--brand-green')

    def test_uses(self):
        uses = {(c['hex'], c['use']) for c in self.parsed['colours']}
        self.assertIn(('#f7f3ec', 'background'), uses)
        self.assertIn(('#1d1d1b', 'text'), uses)
        self.assertIn(('#1d3b2a', 'border'), uses)
        self.assertIn(('#1d3b2a', 'button'), uses)

    def test_fonts(self):
        families = {(f['family'], f['role']) for f in self.parsed['fonts']}
        self.assertIn(('Fraunces', 'heading'), families)
        self.assertIn(('Inter', 'body'), families)
        self.assertIn(('Inter', 'button'), families)
        self.assertEqual(self.parsed['font_faces'][0]['family'], 'Fraunces')

    def test_empty(self):
        self.assertEqual(style.parse_css('', 'x'), {'colours': [], 'variables': {}, 'fonts': [], 'font_faces': []})


class Html(unittest.TestCase):
    def setUp(self):
        self.page = style.parse_html(HOME, 'https://lipa.example/')

    def test_items(self):
        self.assertEqual(self.page['meta']['title'], 'Kawiarnia Lipa | Kawa z sąsiedztwa')
        self.assertEqual(self.page['meta']['site_name'], 'Kawiarnia Lipa')
        self.assertEqual(self.page['meta']['lang'], 'pl')
        self.assertIn('Zamów online', self.page['ctas'])
        self.assertIn('Zarezerwuj stolik', self.page['ctas'])
        self.assertEqual(self.page['nav'][:2], ['Menu', 'O nas'])
        self.assertEqual(self.page['headings'][0], {'level': 1, 'text': 'Kawa, którą znasz z sąsiedztwa'})
        self.assertIn('https://fonts.googleapis.com/css2?family=Fraunces:wght@900&family=Inter&display=swap',
                      self.page['font_links'])
        self.assertIn('https://www.instagram.com/kawiarnialipa', self.page['social'])
        self.assertIn('Pieczemy codziennie rano.', self.page['copy_sample'])
        self.assertLessEqual(len(self.page['copy_sample']), 2000)
        self.assertIn('.promo', self.page['inline_css'])

    def test_logos(self):
        kinds = {(l['kind'], l['url']) for l in self.page['logos']}
        self.assertIn(('header-img', 'https://lipa.example/img/logo-lipa.svg'), kinds)
        self.assertIn(('og:image', 'https://lipa.example/img/og.jpg'), kinds)
        self.assertIn(('apple-touch-icon', 'https://lipa.example/apple-touch-icon.png'), kinds)


class Evidence(unittest.TestCase):
    def test_aggregate(self):
        ev = style.build_evidence(collected())
        self.assertEqual(ev['method'], 'static-html-css')
        top = ev['colours'][0]
        self.assertEqual(top['hex'], '#1d3b2a')
        self.assertGreaterEqual(top['count'], 4)
        self.assertIn('button', top['uses'])
        fonts = {f['family']: f for f in ev['fonts']}
        self.assertIn('heading', fonts['Fraunces']['roles'])
        self.assertIn('body', fonts['Inter']['roles'])
        self.assertNotIn('Arial', fonts)  # generic fallbacks are not brand fonts
        self.assertEqual([p['status'] for p in ev['pages']], [200, 'robots-disallowed'])
        self.assertIn('#f2c14e', [c['hex'] for c in ev['colours']])  # inline <style>
        self.assertNotIn('html', ev['pages'][0])

    def test_no_css(self):
        data = collected()
        data['stylesheets'] = []
        data['pages'][0]['html'] = '<html><body><h1>Hi</h1></body></html>'
        ev = style.build_evidence(data)
        self.assertEqual(ev['colours'], [])
        self.assertEqual(ev['fonts'], [])


if __name__ == '__main__':
    unittest.main()
