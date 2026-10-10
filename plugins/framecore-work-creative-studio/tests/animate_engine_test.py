"""Tests for the bundled Animate engine: byte identity with the pinned source, no second skill, and a demo that builds."""
import json
import pathlib
import shutil
import subprocess
import tempfile
import unittest
import hashlib

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
ENGINE = PLUGIN / 'skills/hyperframes-workflow/assets/animate-engine'
MANIFEST = json.loads((PLUGIN / 'integrations/animate/source-manifest.json').read_text(encoding='utf-8'))


def git_blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()


class Provenance(unittest.TestCase):
    def test_every_bundled_file_matches_the_pinned_source(self):
        listed = {item['path']: item['git_blob_sha'] for item in MANIFEST['bundled_files']}
        self.assertEqual(len(listed), 107)
        for path, blob in listed.items():
            self.assertEqual(git_blob(ENGINE / path), blob, path)
        added = {str(pathlib.Path(p).relative_to('skills/hyperframes-workflow/assets/animate-engine')) for p in MANIFEST['studio_added_files']}
        present = {str(p.relative_to(ENGINE)) for p in ENGINE.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
        self.assertEqual(present, set(listed) | added, 'only manifest files and the Studio-added pins are bundled')
        self.assertEqual(git_blob(PLUGIN / 'integrations/animate/LICENSE'), MANIFEST['retained_files'][0]['git_blob_sha'])

    def test_the_engine_is_not_a_second_skill(self):
        self.assertFalse(list(ENGINE.rglob('SKILL.md')), 'SKILL.md is bundled as ENGINE.md')
        self.assertTrue((ENGINE / 'ENGINE.md').read_text(encoding='utf-8').startswith('---\nname: animate\n'))

    def test_workspace_pin_and_lockfile_agree(self):
        package = json.loads((ENGINE / 'package.json').read_text(encoding='utf-8'))
        lock = json.loads((ENGINE / 'package-lock.json').read_text(encoding='utf-8'))
        self.assertEqual(package['dependencies'], {'playwright': '1.56.1'})
        self.assertEqual(lock['packages']['node_modules/playwright']['version'], '1.56.1')


@unittest.skipUnless(shutil.which('node'), 'needs Node.js')
class Build(unittest.TestCase):
    def test_a_style_demo_builds_into_one_self_contained_file(self):
        with tempfile.TemporaryDirectory() as temp:
            piece = pathlib.Path(temp, 'pieces/riso-demo')
            shutil.copytree(ENGINE / 'styles/riso/demo', piece)
            done = subprocess.run(['node', str(ENGINE / 'tools/build.mjs'), str(piece)], capture_output=True, text=True, timeout=120)
            self.assertEqual(done.returncode, 0, done.stderr)
            self.assertIn('no external assets', done.stdout)
            html = (piece / 'index.html').read_text(encoding='utf-8')
            self.assertIn('<canvas', html)
            self.assertNotIn('Math.random()', html.replace('// never Math.random()', ''))


if __name__ == '__main__':
    unittest.main(verbosity=1)
