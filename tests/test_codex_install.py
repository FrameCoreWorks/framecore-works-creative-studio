"""Bounded filesystem checks; no native host activation or model evaluation."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/install_codex.py'
COMMIT = '1' * 40  # Synthetic source identity for isolated filesystem tests only.


class InstallationChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.skills = self.base / 'skills'
        self.bundle = self.base / 'data/studio'

    def run_helper(self, action, *, success=True, bundle=None):
        result = subprocess.run([
            sys.executable, str(SCRIPT), action, '--skills-dir', str(self.skills),
            '--bundle-dir', str(bundle or self.bundle), '--source-commit', COMMIT,
        ], capture_output=True, text=True,
           env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
        self.assertEqual(result.returncode == 0, success, result.stdout + result.stderr)
        return json.loads(result.stdout) if success else result.stderr

    def test_plan_is_read_only(self):
        result = self.run_helper('plan')
        self.assertEqual(result['modules'], 37)
        self.assertFalse(self.skills.exists())
        self.assertFalse(self.bundle.exists())

    def test_install_verify_and_repeat_preserve_every_byte(self):
        self.run_helper('install')
        self.assertEqual(self.run_helper('verify')['status'], 'FILES_VERIFIED')
        entry = self.skills / 'framecore-work-creative-studio/SKILL.md'
        before = entry.stat().st_mtime_ns
        self.assertIn(str(self.bundle / 'skills/workflow-orchestrator/SKILL.md'), entry.read_text())
        self.assertEqual(self.run_helper('install')['status'], 'already_up_to_date')
        self.assertEqual(before, entry.stat().st_mtime_ns)
        self.assertFalse(self.bundle.is_relative_to(self.skills))

    def test_local_edit_is_preserved_and_blocks_reinstall(self):
        self.run_helper('install')
        changed = self.bundle / 'skills/workflow-orchestrator/SKILL.md'
        changed.write_text(changed.read_text() + '\nPersonal addition.\n')
        self.run_helper('install', success=False)
        self.assertTrue(changed.read_text().endswith('Personal addition.\n'))

    def test_native_entry_carries_automatic_language_and_both_complete_sources(self):
        self.run_helper('install')
        entry = (self.skills / 'framecore-work-creative-studio/SKILL.md').read_text()
        for phrase in [
            'automatic language policy', 'actually supplied host response/UI language',
            'Do not require an\nexplicit translation request',
            'automatically translate the full English source',
            'switch the entire response when the language changes',
            'Localize later menus without changing reply tokens',
        ]:
            self.assertIn(phrase, entry)
        for locale in ['en', 'pl']:
            relative = Path('skills/workflow-orchestrator/assets') / ('startup-welcome.' + locale + '.md')
            self.assertIn(str(self.bundle / relative), entry)
            self.assertEqual((self.bundle / relative).read_bytes(), (ROOT / 'plugins/framecore-work-creative-studio' / relative).read_bytes())
        self.assertNotIn('explicit-language rule', entry)
        self.assertNotIn('entire fixed welcome', entry)

    def test_native_version_question_rereads_the_same_bundle_entry(self):
        self.run_helper('install')
        entry = (self.skills / 'framecore-work-creative-studio/SKILL.md').read_text()
        self.assertIn('plugin version or installation-status question, reread that entry', entry)
        self.assertIn('Do not infer the installed version from conversation history', entry)
        self.assertNotIn('BEGIN PACKAGE IDENTITY', entry)

    def test_existing_skill_identity_blocks_before_writes(self):
        existing = self.skills / 'my-custom-folder/SKILL.md'
        existing.parent.mkdir(parents=True)
        existing.write_text('---\nname: workflow-orchestrator\ndescription: Personal\n---\n')
        self.run_helper('install', success=False)
        self.assertFalse(self.bundle.exists())
        self.assertFalse((self.skills / 'framecore-work-creative-studio').exists())

    def test_yaml_identity_variants_block_plan_and_install_without_writes(self):
        existing = self.skills / 'my-custom-folder/SKILL.md'
        existing.parent.mkdir(parents=True)
        declarations = [
            'name: workflow-orchestrator # user preference',
            '"name": "workflow-orchestrator"',
            "'name': 'workflow-orchestrator' # personal",
            'name: "workflow-orchestrator" # personal',
            'name: workflow-orchestrator',
        ]
        for declaration in declarations:
            with self.subTest(declaration=declaration):
                content = '---\n' + declaration + '\ndescription: Personal\n---\nKeep my work.\n'
                existing.write_text(content)
                for action in ['plan', 'install']:
                    self.assertIn('Existing Studio/Workflow Kit', self.run_helper(action, success=False))
                    self.assertEqual(existing.read_text(), content)
                    self.assertFalse(self.bundle.exists())
                    self.assertFalse((self.skills / 'framecore-work-creative-studio').exists())

    def test_body_name_does_not_create_a_false_collision(self):
        existing = self.skills / 'personal/SKILL.md'
        existing.parent.mkdir(parents=True)
        content = '---\nname: personal-skill\ndescription: Personal\n---\nname: workflow-orchestrator\n'
        existing.write_text(content)
        self.assertEqual(self.run_helper('plan')['status'], 'READY')
        self.run_helper('install')
        self.assertEqual(existing.read_text(), content)

    def test_ambiguous_frontmatter_requires_review_before_writes(self):
        existing = self.skills / 'personal/SKILL.md'
        existing.parent.mkdir(parents=True)
        variants = [
            '---\nname: >-\n  workflow-orchestrator\n---\n',
            '---\nname: personal\nname: workflow-orchestrator\n---\n',
            '---\n{name: workflow-orchestrator}\n---\n',
            '---\nname: workflow-orchestrator\n',
        ]
        for content in variants:
            with self.subTest(content=content):
                existing.write_text(content)
                self.assertIn('requires review', self.run_helper('install', success=False))
                self.assertEqual(existing.read_text(), content)
                self.assertFalse(self.bundle.exists())
                self.assertFalse((self.skills / 'framecore-work-creative-studio').exists())

    def test_partial_installation_is_not_overwritten(self):
        self.bundle.mkdir(parents=True)
        sentinel = self.bundle / 'my-file.txt'
        sentinel.write_text('keep')
        self.run_helper('install', success=False)
        self.assertEqual(sentinel.read_text(), 'keep')
        self.assertFalse(self.skills.exists())

    def test_symlink_and_nested_discovery_are_rejected(self):
        self.skills.symlink_to(self.base / 'real-skills', target_is_directory=True)
        self.run_helper('plan', success=False)
        self.skills.unlink()
        self.run_helper('plan', bundle=self.skills / 'studio', success=False)
        self.assertFalse(self.skills.exists())

    def test_extra_saved_file_fails_verification(self):
        self.run_helper('install')
        (self.bundle / 'extra.txt').write_text('personal')
        self.run_helper('verify', success=False)
        self.assertEqual((self.bundle / 'extra.txt').read_text(), 'personal')


if __name__ == '__main__':
    unittest.main()
