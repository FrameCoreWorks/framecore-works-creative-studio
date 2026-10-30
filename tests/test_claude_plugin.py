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
        # Studio plus companions in this repository; Open Assets is standalone and pinned to its own repository (2026-10-29).
        # Earshot comes only through FrameCore Works Toolbox, which has its own marketplace: no earshot-audio entry here.
        entries = {e['name']: e for e in MARKET['plugins']}
        self.assertNotIn('earshot-audio', entries)
        entry = entries[PORTABLE['name']]
        self.assertEqual(entry['version'], PORTABLE['version'])
        self.assertEqual((ROOT / entry['source']).resolve(), PLUGIN.resolve())
        assets = entries['framecore-open-assets']['source']
        self.assertEqual((assets['source'], assets['url'], assets['path']),
                         ('git-subdir', 'https://github.com/FrameCoreWorks/framecore-open-assets.git', 'plugins/framecore-open-assets'))
        self.assertRegex(assets['sha'], r'^[0-9a-f]{40}$')
        # Owner question 2026-10-30: installing Studio from this marketplace in Claude Code also installs Toolbox and
        # Open Assets. Same-marketplace dependencies need no cross-marketplace allowlist; they sit in the marketplace
        # entry, not in plugin.json, so an uploaded or synced copy without these entries still loads.
        toolbox = entries['toolbox']['source']
        self.assertEqual((toolbox['source'], toolbox['url'], toolbox['path']),
                         ('git-subdir', 'https://github.com/FrameCoreWorks/framecore-works-toolbox.git', 'plugins/toolbox'))
        self.assertRegex(toolbox['sha'], r'^[0-9a-f]{40}$')
        self.assertEqual(entry['dependencies'], ['toolbox', 'framecore-open-assets'])
        self.assertNotIn('dependencies', CLAUDE)
        self.assertNotIn('allowCrossMarketplaceDependenciesOn', MARKET)
        for item in MARKET['plugins']:
            if isinstance(item['source'], dict):
                continue
            self.assertTrue(item['source'].startswith('./') and '..' not in item['source'], item['name'])
            manifest = json.loads((ROOT / item['source'] / '.claude-plugin/plugin.json').read_text(encoding='utf-8'))
            self.assertEqual((manifest['name'], manifest['version']), (item['name'], item['version']))

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

    def test_install_guide_runs_from_the_shell_and_handles_a_synced_copy(self):
        guide = (ROOT / 'CLAUDE_INSTALL.md').read_text()
        prompt = guide.split('## Paste this prompt', 1)[1].split('```text', 1)[1].split('```', 1)[0]
        for phrase in ('CLAUDE_INSTALL.md', 'claude plugin list', 'Synced from claude.ai', '37 skills', 'ask me once'):
            self.assertIn(phrase, prompt)
        for phrase in ('command -v claude', 'framecore-work-creative-studio@synced', 'claude plugin disable framecore-work-creative-studio@synced',
                       'releases/latest', 'only in the terminal CLI'):
            self.assertIn(phrase, guide)
        self.assertIn('CLAUDE_INSTALL.md#paste-this-prompt', (ROOT / 'README.md').read_text())
        self.assertIn('CLAUDE_INSTALL.md#6-update-and-remove', (ROOT / 'UPDATE.md').read_text())
        for case in ('CI-01', 'CI-02', 'CI-03', 'CI-04', 'CI-05'):
            self.assertIn(case, (ROOT / 'docs/host-evals.md').read_text())


class Guides(unittest.TestCase):
    def test_installation_flows_into_the_same_companion_setup_on_every_host(self):
        # Owner request 2026-10-23: no extra "Configure Studio" in Claude; the same Superpowers and Earshot offer everywhere.
        guide = (ROOT / 'CLAUDE_INSTALL.md').read_text()
        prompt = guide.split('## Paste this prompt', 1)[1].split('```text', 1)[1].split('```', 1)[0]
        self.assertIn('first\ncompanion setup', prompt)
        for name in ('CODEX_INSTALL.md', 'CHATGPT_INSTALL.md', 'CLAUDE_INSTALL.md'):
            text = (ROOT / name).read_text()
            self.assertIn('Right after the final check, in the same conversation', text, name)
            earshot = text.split('## Second recommended companion: FrameCore Works Toolbox', 1)[1].split('\n## ', 1)[0]
            for needle in ('plain words', 'full (recommended, about 2.6 GB', 'light (about 200 MB)', 'install --tier <full|light>',
                           'fetch-models --yes', 'status --json', '*.hf.co', 'capabilities/earshot/scripts/runtime.py', 'candidates'):
                self.assertIn(needle, earshot, name)

    def test_every_install_guide_offers_toolbox_for_earshot_after_superpowers(self):
        # Owner decisions 2026-10-29: Earshot comes only through FrameCore Works Toolbox, second after Superpowers;
        # the old earshot-audio plugin is named only in the step that removes it, and Open Assets is standalone.
        for guide in ('CODEX_INSTALL.md', 'CHATGPT_INSTALL.md', 'CLAUDE_INSTALL.md'):
            text = (ROOT / guide).read_text()
            self.assertLess(text.index('Superpowers'), text.index('FrameCore Works Toolbox'), guide)
            self.assertIn('FrameCoreWorks/framecore-works-toolbox', text, guide)
            self.assertIn('runtime.py status', text, guide)
            self.assertNotIn('plugins/earshot-audio', text, guide)
            self.assertNotIn('earshot-audio:earshot', text, guide)
            rest = text.split('### Moving from Earshot Audio', 1)
            self.assertEqual(len(rest), 2, guide)
            self.assertNotIn('earshot-audio', rest[0], guide)
            self.assertIn('FrameCoreWorks/framecore-open-assets', text, guide)
        self.assertIn('toolbox@framecore-works-toolbox', (ROOT / 'CLAUDE_INSTALL.md').read_text())
        self.assertIn('Plugin Creator', (ROOT / 'CHATGPT_INSTALL.md').read_text().split('FrameCore Works Toolbox', 1)[1])

    def test_installation_ends_with_the_final_check_and_updates_with_the_update_check(self):
        for guide in ('CODEX_INSTALL.md', 'CHATGPT_INSTALL.md', 'CLAUDE_INSTALL.md'):
            self.assertIn('--final --host', (ROOT / guide).read_text(), guide)
        for guide in ('CODEX_UPDATE.md', 'CHATGPT_UPDATE.md', 'CLAUDE_INSTALL.md', 'UPDATE.md'):
            self.assertIn('--update --host', (ROOT / guide).read_text(), guide)


@unittest.skipUnless(shutil.which('claude'), 'the claude command is not installed')
class ClaudeValidator(unittest.TestCase):
    def test_claude_plugin_validate_passes_for_plugin_and_marketplace(self):
        for target in (PLUGIN, ROOT):
            done = subprocess.run(['claude', 'plugin', 'validate', str(target), '--strict'], capture_output=True, text=True, timeout=120)
            self.assertEqual(done.returncode, 0, done.stdout + done.stderr)


if __name__ == '__main__':
    unittest.main()
