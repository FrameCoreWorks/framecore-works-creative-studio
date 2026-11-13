"""Cleanup of files an older Studio left in an updated plugin folder (owner request 2026-11-13): only listed paths,
only bytes Studio shipped, never runtime folders or changed files; the shipped list matches the release records."""
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[1]
ROOT = PLUGIN.parents[1]
KIT = PLUGIN / 'skills/workflow-orchestrator/assets/migration'
TOOL = KIT / 'cleanup_old_modules.py'


def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


class Cleanup(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / 'plugin'
        self.root.mkdir()
        (self.root / 'plugin.json').write_text(json.dumps({'name': 'framecore-work-creative-studio', 'version': '9.9.9'}))
        shipped, other = b'shipped motion reference\n', b'an older shipped version\n'
        self.listing = Path(self.tmp.name) / 'listing.json'
        self.listing.write_text(json.dumps({'removed_folders': ['skills/caption-studio', 'skills/hyperframes-workflow'], 'files': {
            'skills/hyperframes-workflow/SKILL.md': {'removed_in': '1.178.0', 'blobs': [blob(shipped), blob(other)]},
            'skills/hyperframes-workflow/references/a.md': {'removed_in': '1.178.0', 'blobs': [blob(shipped)]},
            'skills/caption-studio/SKILL.md': {'removed_in': '1.179.0', 'blobs': [blob(shipped)]},
        }}))
        self.write('skills/hyperframes-workflow/SKILL.md', other)
        self.write('skills/hyperframes-workflow/references/a.md', b'the user changed this\n')
        self.write('skills/hyperframes-workflow/assets/motion-runtime/node_modules/x/index.js', b'runtime')
        self.write('skills/workflow-orchestrator/assets/media-runtime/bin/tool', b'runtime')
        self.write('skills/caption-studio/SKILL.md', shipped)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, rel, data):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def run_tool(self, *extra):
        result = subprocess.run([sys.executable, str(TOOL), '--plugin-root', str(self.root), '--listing', str(self.listing), '--json', *extra],
                                capture_output=True, text=True)
        return result.returncode, json.loads(result.stdout)

    def test_report_changes_nothing_and_names_what_can_go(self):
        code, report = self.run_tool()
        self.assertEqual(code, 1)
        self.assertEqual(report['removable'], ['skills/caption-studio/SKILL.md', 'skills/hyperframes-workflow/SKILL.md'])
        self.assertEqual(report['kept_changed'], ['skills/hyperframes-workflow/references/a.md'])
        self.assertTrue((self.root / 'skills/caption-studio/SKILL.md').exists())

    def test_apply_removes_only_shipped_listed_files(self):
        code, report = self.run_tool('--apply')
        self.assertEqual(code, 0)
        self.assertEqual(report['removed'], ['skills/caption-studio/SKILL.md', 'skills/hyperframes-workflow/SKILL.md'])
        self.assertFalse((self.root / 'skills/caption-studio').exists(), 'an emptied old folder goes too')
        for kept in ('skills/hyperframes-workflow/references/a.md', 'skills/hyperframes-workflow/assets/motion-runtime/node_modules/x/index.js',
                     'skills/workflow-orchestrator/assets/media-runtime/bin/tool', 'plugin.json'):
            self.assertTrue((self.root / kept).exists(), kept)
        self.assertEqual(report['kept_folders'], [{'folder': 'skills/hyperframes-workflow', 'files_not_from_studio': 1}])
        code, report = self.run_tool()
        self.assertEqual((code, report['removable']), (0, []))

    def test_refuses_a_folder_that_is_not_studio(self):
        (self.root / 'plugin.json').write_text(json.dumps({'name': 'something-else'}))
        result = subprocess.run([sys.executable, str(TOOL), '--plugin-root', str(self.root), '--listing', str(self.listing), '--apply'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertTrue((self.root / 'skills/caption-studio/SKILL.md').exists())

    def test_the_installed_package_has_no_leftovers(self):
        result = subprocess.run([sys.executable, str(TOOL), '--json'], capture_output=True, text=True)  # default root: this plugin
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_listing_matches_the_release_records(self):
        listing = json.loads((KIT / 'removed-files.json').read_text())
        expected = set()
        for version in listing['releases']:
            expected.update(json.loads((ROOT / f'verification/scope-{version}.json').read_text())['removed'])
        self.assertEqual(set(listing['files']), expected)
        for rel, info in listing['files'].items():
            self.assertTrue(info['blobs'], rel)
            self.assertFalse((PLUGIN / rel).exists(), rel)
        for folder in listing['removed_folders']:
            self.assertFalse((PLUGIN / folder).exists(), folder)
        self.assertIn('skills/hyperframes-workflow', listing['removed_folders'])


if __name__ == '__main__':
    unittest.main()
