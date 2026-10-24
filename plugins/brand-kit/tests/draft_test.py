"""brand-kit draft: evidence mapped onto Studio's brand kit template, with a source ledger."""
import json
import pathlib
import sys
import unittest

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
ROOT = PLUGIN.parent.parent
sys.path.insert(0, str(PLUGIN / 'scripts'))
import draft  # noqa: E402
import style  # noqa: E402
from style_test import collected  # noqa: E402

TEMPLATE = ROOT / 'plugins/framecore-work-creative-studio/skills/pipeline-core/assets/brand-kit.template.json'


class Draft(unittest.TestCase):
    def setUp(self):
        self.kit, self.ledger = draft.draft(style.build_evidence(collected()))
        self.by_field = {row['field']: row for row in self.ledger}

    def test_keys_match_studio_template(self):
        template = json.loads(TEMPLATE.read_text(encoding='utf-8'))
        self.assertEqual(list(self.kit), list(template))
        self.assertEqual(set(self.kit['colours']), set(template['colours']))
        self.assertEqual(set(self.kit['voice']), set(template['voice']))

    def test_colour_roles(self):
        c = self.kit['colours']
        self.assertEqual(c['primary']['hex'], '#1d3b2a')
        self.assertEqual(c['accent']['hex'], '#f2c14e')
        self.assertEqual(c['background']['hex'], '#f7f3ec')
        self.assertEqual(c['text']['hex'], '#1d1d1b')
        self.assertEqual(self.by_field['colours.primary']['status'], 'inferred')

    def test_fonts_and_logo(self):
        self.assertEqual(self.kit['fonts']['headline'], {'font': 'Fraunces', 'licence': 'Unknown'})
        self.assertEqual(self.kit['fonts']['body']['font'], 'Inter')
        self.assertEqual(self.kit['logo']['files']['colour'], 'https://lipa.example/img/logo-lipa.svg')
        self.assertEqual(self.kit['logo']['min_width_px'], 'Unknown')
        self.assertIn('url-not-downloaded', self.by_field['logo.files.colour']['note'])

    def test_name_and_voice_left_to_people(self):
        self.assertEqual(self.kit['name'], 'Kawiarnia Lipa')
        self.assertEqual(self.kit['voice']['tone'], [])
        self.assertEqual(self.kit['voice']['address'], 'Unknown')
        self.assertEqual(self.kit['claims'], {'approved': [], 'banned': []})
        self.assertEqual(self.by_field['voice']['status'], 'unknown')

    def test_title_fallback_and_no_colours(self):
        ev = style.build_evidence(collected())
        ev['meta']['site_name'] = ''
        ev['colours'], ev['fonts'], ev['logos'] = [], [], []
        kit, ledger = draft.draft(ev)
        self.assertEqual(kit['name'], 'Kawiarnia Lipa')
        for role in ('primary', 'accent', 'text', 'background'):
            self.assertEqual(kit['colours'][role]['hex'], 'Unknown', role)
        self.assertEqual(kit['fonts']['headline']['font'], 'Unknown')
        self.assertEqual(kit['logo']['files']['colour'], 'Unknown')

    def test_helpers(self):
        self.assertTrue(draft.is_saturated('#1d3b2a'))
        self.assertFalse(draft.is_saturated('#f7f3ec'))
        self.assertGreater(draft.luminance('#ffffff'), draft.luminance('#1d1d1b'))


if __name__ == '__main__':
    unittest.main()
