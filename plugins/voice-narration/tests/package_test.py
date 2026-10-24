"""voice-narration package: one skill, consistent manifests, no vendored engine, no key or server route."""
import json
import pathlib
import re
import unittest

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
ROOT = PLUGIN.parent.parent
VERSION = '1.0.0'


def load(path):
    return json.loads((PLUGIN / path).read_text(encoding='utf-8'))


class Package(unittest.TestCase):
    def test_manifests_agree(self):
        versions = set()
        for path in ('plugin.json', '.claude-plugin/plugin.json', '.codex-plugin/plugin.json'):
            data = load(path)
            self.assertEqual(data['name'], 'voice-narration', path)
            versions.add(data['version'])
        self.assertEqual(versions, {VERSION})
        self.assertEqual(load('.codex-plugin/plugin.json')['interface']['displayName'], 'Voice And Narration')
        self.assertEqual(load('.codex-plugin/plugin.json')['skills'], './skills')
        market = json.loads((ROOT / '.claude-plugin/marketplace.json').read_text(encoding='utf-8'))
        entries = {p['name']: p for p in market['plugins']}
        self.assertEqual(entries['voice-narration']['source'], './plugins/voice-narration')
        self.assertEqual(entries['voice-narration']['version'], VERSION)

    def test_no_vendored_engine(self):
        for path in PLUGIN.rglob('*'):
            if '__pycache__' in path.parts:
                continue
            self.assertNotIn(path.suffix, ('.safetensors', '.pt', '.bin'), path)
            self.assertFalse(path.is_dir() and path.name == 'voxcpm', path)
            if path.is_file() and path.name != 'package_test.py':
                text = path.read_text(encoding='utf-8', errors='ignore')
                self.assertNotIn('ELEVENLABS_API_KEY', text, path)
                self.assertNotIn('mcpServers', text, path)


    def test_exactly_one_skill(self):
        skills = sorted(p.relative_to(PLUGIN).as_posix() for p in PLUGIN.rglob('SKILL.md'))
        self.assertEqual(skills, ['skills/narrate/SKILL.md'])

    def skill(self):
        return (PLUGIN / 'skills/narrate/SKILL.md').read_text(encoding='utf-8')

    def test_skill_rules_present(self):
        text = self.skill()
        self.assertRegex(text, r'(?m)^name: narrate$')
        for needle in ('status --json', '--allow-cloud', '--consent', 'measure', 'narration.lock.json',
                       'own computer', 'credits', 'Copy Voice', 'FrameCut', 'references/elevenlabs-connector.md',
                       'references/formats.md', '--yes'):
            self.assertIn(needle, text)
        description = re.search(r'(?m)^description: (.+)$', text).group(1)
        self.assertLessEqual(len(description), 1024)
        for path in ('references/elevenlabs-connector.md', 'references/formats.md'):
            self.assertTrue((PLUGIN / 'skills/narrate' / path).is_file(), path)

    def test_skill_has_no_key_route(self):
        for path in (PLUGIN / 'skills').rglob('*.md'):
            text = path.read_text(encoding='utf-8')
            for banned in ('API_KEY', 'mcp add', '.mcp.json', 'xi-api-key'):
                self.assertNotIn(banned, text, path)

    def test_openai_yaml_format(self):
        text = (PLUGIN / 'skills/narrate/agents/openai.yaml').read_text(encoding='utf-8')
        name = re.search(r'(?m)^  display_name: "([^"]+)"$', text).group(1)
        short = re.search(r'(?m)^  short_description: "([^"]+)"$', text).group(1)
        self.assertEqual(name, 'Voice And Narration')
        self.assertTrue(all(word[0].isupper() for word in name.split()))
        self.assertTrue(25 <= len(short) <= 64, short)


if __name__ == '__main__':
    unittest.main()
