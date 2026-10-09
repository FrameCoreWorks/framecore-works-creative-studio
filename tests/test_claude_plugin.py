"""The repository as a Claude plugin marketplace: manifests, documented naming rules and limits, and Claude's own
validator when the `claude` command is installed."""
import json
import pathlib
import re
import shutil
import subprocess
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
PLUGIN = ROOT / 'plugins/framecore-work-creative-studio'
MARKET = json.loads((ROOT / '.claude-plugin/marketplace.json').read_text())
CLAUDE = json.loads((PLUGIN / '.claude-plugin/plugin.json').read_text())
PORTABLE = json.loads((PLUGIN / 'plugin.json').read_text())
RESERVED = {'claude-plugins-official', 'claude-code-plugins', 'anthropic-plugins', 'agent-skills', 'claude-community', 'github', 'gh', 'npm', 'pip', 'uv', 'cargo'}


class Manifests(unittest.TestCase):
    def test_claude_manifest_matches_the_package_identity(self):
        for key in ('name', 'version', 'description', 'author', 'keywords'):
            self.assertEqual(CLAUDE[key], PORTABLE[key], key)
        self.assertEqual(CLAUDE['license'], 'Apache-2.0')

    def test_marketplace_lists_the_package_by_relative_source(self):
        self.assertEqual(MARKET['name'], 'framecore-works')
        self.assertTrue(MARKET['owner']['name'])
        [entry] = MARKET['plugins']
        self.assertEqual((entry['name'], entry['version']), (PORTABLE['name'], PORTABLE['version']))
        self.assertTrue(entry['source'].startswith('./') and '..' not in entry['source'])
        self.assertEqual((ROOT / entry['source']).resolve(), PLUGIN.resolve())

    def test_documented_naming_rules(self):
        self.assertRegex(MARKET['name'], r'^[A-Za-z0-9][A-Za-z0-9._-]*$')
        self.assertNotIn(MARKET['name'].lower(), RESERVED)
        self.assertFalse(MARKET['name'].startswith('claudeai-'))
        self.assertRegex(CLAUDE['name'], r'^[a-z0-9]+(-[a-z0-9]+)*$')
        self.assertFalse(re.match(r'^(claude-|anthropic-|anthropics-|cc-plugin-)', CLAUDE['name']))
        for skill in (PLUGIN / 'skills').glob('*/SKILL.md'):
            name = skill.parent.name
            self.assertTrue(len(name) <= 64 and re.fullmatch(r'[a-z0-9-]+', name) and 'claude' not in name and 'anthropic' not in name, name)

    def test_documented_limits_of_the_claude_apps(self):
        files = [p for p in PLUGIN.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
        self.assertLess(len(files), 5000)
        self.assertLess(sum(p.stat().st_size for p in files), 200 * 1024 * 1024)
        self.assertFalse((PLUGIN / 'bin').exists(), 'a top-level bin/ folder makes the Claude apps refuse the plugin')

    def test_install_guide_names_the_marketplace_and_plugin(self):
        guide = (ROOT / 'CLAUDE_INSTALL.md').read_text()
        self.assertIn('/plugin marketplace add FrameCoreWorks/framecore-works-creative-studio', guide)
        self.assertIn('framecore-work-creative-studio@framecore-works', guide)
        self.assertIn('[CLAUDE_INSTALL.md](CLAUDE_INSTALL.md)', (ROOT / 'INSTALL.md').read_text())


@unittest.skipUnless(shutil.which('claude'), 'the claude command is not installed')
class ClaudeValidator(unittest.TestCase):
    def test_claude_plugin_validate_passes_for_plugin_and_marketplace(self):
        for target in (PLUGIN, ROOT):
            done = subprocess.run(['claude', 'plugin', 'validate', str(target), '--strict'], capture_output=True, text=True, timeout=120)
            self.assertEqual(done.returncode, 0, done.stdout + done.stderr)


if __name__ == '__main__':
    unittest.main()
