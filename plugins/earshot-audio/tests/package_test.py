"""earshot-audio package: one skill, upstream files copied byte for byte, consistent manifests, local only."""
import hashlib
import json
import pathlib
import re
import unittest

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
ROOT = PLUGIN.parent.parent
COMMIT = '591fa3e028032e6dce56620a20e932e35667e8d8'
TREE = 'd6f2dbc43f7b38b2147cfd04bbd7aa9055701f1a'


def manifest():
    return json.loads((PLUGIN / 'upstream.json').read_text(encoding='utf-8'))


class Package(unittest.TestCase):
    def test_exactly_one_skill(self):
        skills = sorted(p.relative_to(PLUGIN).as_posix() for p in PLUGIN.rglob('SKILL.md'))
        self.assertEqual(skills, ['skills/earshot/SKILL.md'])

    def test_copied_files_match_the_pin(self):
        data = manifest()
        self.assertEqual((data['commit'], data['tree'], data['tag']), (COMMIT, TREE, 'v0.4.0'))
        self.assertEqual(len(data['files']), 282)
        self.assertGreaterEqual(len(data['copied']), 30)
        for plugin_path, upstream_path in data['copied'].items():
            digest = hashlib.sha256((PLUGIN / plugin_path).read_bytes()).hexdigest()
            self.assertEqual(digest, data['files'][upstream_path], plugin_path)
        self.assertIn('skills/real-sound/scripts/licences.py', data['copied'].values())
        self.assertIn('skills/real-sound/references/process.md', data['copied'].values())

    def test_manifests_agree(self):
        versions = set()
        for path in ('plugin.json', '.claude-plugin/plugin.json', '.codex-plugin/plugin.json'):
            data = json.loads((PLUGIN / path).read_text(encoding='utf-8'))
            self.assertEqual(data['name'], 'earshot-audio', path)
            versions.add(data['version'])
        self.assertEqual(versions, {'1.0.0'})
        market = json.loads((ROOT / '.claude-plugin/marketplace.json').read_text(encoding='utf-8'))
        entries = {p['name']: p for p in market['plugins']}
        self.assertEqual(entries['earshot-audio']['source'], './plugins/earshot-audio')
        self.assertEqual(entries['earshot-audio']['version'], '1.0.0')
        studio = json.loads((ROOT / 'plugins/framecore-work-creative-studio/.claude-plugin/plugin.json').read_text(encoding='utf-8'))
        self.assertEqual(entries['framecore-work-creative-studio']['version'], studio['version'])

    def test_skill_is_local_only(self):
        text = (PLUGIN / 'skills/earshot/SKILL.md').read_text(encoding='utf-8')
        self.assertRegex(text, r'(?m)^name: earshot$')
        for needle in ('runtime.py', '--yes', 'Freesound', 'status', 'kit.lock.json', 'launch'):
            self.assertIn(needle, text)
        for banned in ('mcp add', '.mcp.json', 'GEMINI_API_KEY', 'pip install -e', 'llm_critique'):
            self.assertNotIn(banned, text)
        description = re.search(r'(?m)^description: (.+)$', text).group(1)
        self.assertLessEqual(len(description), 1024)

    def test_licence_and_notice(self):
        data = manifest()
        self.assertEqual(hashlib.sha256((PLUGIN / 'LICENSE').read_bytes()).hexdigest(), data['files']['LICENSE'])
        notice = (PLUGIN / 'NOTICE').read_text(encoding='utf-8')
        self.assertIn('Leon Lin', notice)
        self.assertIn(COMMIT, notice)

    def test_launcher_pin_matches_the_manifest(self):
        text = (PLUGIN / 'scripts/runtime.py').read_text(encoding='utf-8')
        self.assertIn(COMMIT, text)
        self.assertIn(TREE, text)


if __name__ == '__main__':
    unittest.main()
