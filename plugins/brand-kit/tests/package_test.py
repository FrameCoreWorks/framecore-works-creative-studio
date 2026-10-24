"""brand-kit package: one skill, consistent manifests, Studio's kit schema, existing Studio owners in the routes."""
import json
import pathlib
import re
import sys
import unittest

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
ROOT = PLUGIN.parent.parent
STUDIO = ROOT / 'plugins/framecore-work-creative-studio'
SKILL = PLUGIN / 'skills/brand'
VERSION = '1.0.0'
sys.path.insert(0, str(PLUGIN / 'scripts'))
import catalog  # noqa: E402


def load(path):
    return json.loads((PLUGIN / path).read_text(encoding='utf-8'))


class Package(unittest.TestCase):
    def test_manifests_agree(self):
        versions = set()
        for path in ('plugin.json', '.claude-plugin/plugin.json', '.codex-plugin/plugin.json'):
            data = load(path)
            self.assertEqual(data['name'], 'brand-kit', path)
            versions.add(data['version'])
        self.assertEqual(versions, {VERSION})
        self.assertEqual(load('.codex-plugin/plugin.json')['interface']['displayName'], 'Brand Kit')
        self.assertEqual(load('.codex-plugin/plugin.json')['skills'], './skills')
        market = json.loads((ROOT / '.claude-plugin/marketplace.json').read_text(encoding='utf-8'))
        entries = {p['name']: p for p in market['plugins']}
        self.assertEqual(entries['brand-kit']['source'], './plugins/brand-kit')
        self.assertEqual(entries['brand-kit']['version'], VERSION)

    def test_exactly_one_skill_with_metadata(self):
        skills = sorted(p.relative_to(PLUGIN).as_posix() for p in PLUGIN.rglob('SKILL.md'))
        self.assertEqual(skills, ['skills/brand/SKILL.md'])
        meta = (SKILL / 'agents/openai.yaml').read_text(encoding='utf-8')
        self.assertIn('display_name: "Brand Kit"', meta)
        short = re.search(r'short_description: "(.+)"', meta).group(1)
        self.assertTrue(25 <= len(short) <= 64, short)

    def test_skill_rules_present(self):
        text = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
        self.assertRegex(text, r'(?m)^name: brand$')
        self.assertLessEqual(len(text.encode('utf-8')), 7000)
        description = re.search(r'(?m)^description: (.+)$', text).group(1)
        self.assertLessEqual(len(description), 1024)
        for needle in ('extract', 'draft', 'save', 'Unknown', 'brand-audit.md', 'references/directions.md',
                       'references/audit-template.md', 'robots', 'not a pixel sample', 'approved claim',
                       'Save only after the user agrees', 'brand-kit.template.json'):
            self.assertIn(needle, text)
        for ref in ('references/directions.md', 'references/audit-template.md'):
            self.assertTrue((SKILL / ref).is_file(), ref)

    def test_catalog_fields_match_studio_template(self):
        template = json.loads((STUDIO / 'skills/pipeline-core/assets/brand-kit.template.json').read_text(encoding='utf-8'))
        self.assertEqual(list(catalog.REQUIRED), list(template))

    def test_directions_name_existing_owners(self):
        text = (SKILL / 'references/directions.md').read_text(encoding='utf-8')
        owners = set(re.findall(r'`([a-z][a-z-]+)`', text)) - {'framecore-work-creative-studio:'}
        self.assertTrue(owners)
        for owner in owners:
            self.assertTrue((STUDIO / 'skills' / owner / 'SKILL.md').is_file(), owner)
        self.assertIn('voice-narration:narrate', text)
        self.assertTrue((ROOT / 'plugins/voice-narration/skills/narrate/SKILL.md').is_file())
        for path in re.findall(r'`([a-z-]+/(?:references|assets)/[\w./-]+)`', text):
            self.assertTrue((STUDIO / 'skills' / path).exists(), path)

    def test_no_client_data_or_secrets(self):
        for path in PLUGIN.rglob('*'):
            if path.is_file() and '__pycache__' not in path.parts and path.name != 'package_test.py':
                text = path.read_text(encoding='utf-8', errors='ignore')
                self.assertNotIn('API_KEY', text, path)
                self.assertNotIn('mcpServers', text, path)
        self.assertEqual(sorted(p.name for p in (PLUGIN / 'tests/fixtures').iterdir()), ['home.html', 'site.css'])


if __name__ == '__main__':
    unittest.main()
