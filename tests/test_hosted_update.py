import hashlib
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest
import zipfile
import base64

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCRIPT = ROOT / 'scripts' / 'hosted_update.py'
sys.path.insert(0, str(ROOT / 'scripts'))
import hosted_update  # noqa: E402


def sha(data):
    return hashlib.sha256(data).hexdigest()


def blob(data):
    return hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()


def inventory(files, version):
    return {'version': version, 'files': [{'path': p, 'bytes': len(d), 'sha256': sha(d)} for p, d in sorted(files.items())]}


OLD = {'a.md': b'a1\n', 'b.md': b'b1\n', 'gone.md': b'g\n', 'overlay.md': b'o1\n', 'clash.md': b'c1\n', 'logo.png': b'\x89PNG\x00\x01'}
NEW = {'a.md': b'a1\n', 'b.md': b'b2\n', 'new.md': b'n\n', 'overlay.md': b'o1\n', 'clash.md': b'c2\n', 'logo.png': b'\x89PNG\x00\x02'}
SAVED = {'a.md': b'a1\n', 'b.md': b'b1\n', 'gone.md': b'g\n', 'overlay.md': b'private\n', 'clash.md': b'private clash\n',
         'logo.png': b'\x89PNG\x00\x01', 'private/key.md': b'mine\n'}


class PlanTest(unittest.TestCase):
    def setUp(self):
        self.plan = hosted_update.plan(hosted_update.load_inventory(inventory(NEW, '2.0.0')),
                                       hosted_update.saved_from_files(SAVED),
                                       hosted_update.load_inventory(inventory(OLD, '1.0.0')))

    def test_three_way_plan(self):
        p = self.plan
        self.assertEqual(p['fetch'], ['b.md', 'clash.md', 'logo.png', 'new.md'])
        self.assertEqual(p['delete_paths'], ['gone.md'])
        self.assertEqual(p['review'], [{'path': 'clash.md', 'reason': 'saved copy differs from old and new public source'}])
        self.assertEqual(p['overlay_kept'], ['overlay.md'])
        self.assertEqual(p['private_kept'], ['private/key.md'])
        self.assertFalse(p['baseline_unknown'])
        self.assertFalse(p['already_current'])

    def test_unknown_baseline_deletes_nothing_and_reviews_differences(self):
        p = hosted_update.plan(hosted_update.load_inventory(inventory(NEW, '2.0.0')), hosted_update.saved_from_files(SAVED), None)
        self.assertTrue(p['baseline_unknown'])
        self.assertEqual(p['delete_paths'], [])
        self.assertIn('overlay.md', p['fetch'])
        self.assertIn('overlay.md', [r['path'] for r in p['review']])

    def test_already_current(self):
        saved = dict(NEW, **{'private/key.md': b'mine\n'})
        p = hosted_update.plan(hosted_update.load_inventory(inventory(NEW, '2.0.0')), hosted_update.saved_from_files(saved),
                               hosted_update.load_inventory(inventory(OLD, '1.0.0')))
        self.assertTrue(p['already_current'])
        self.assertEqual(p['fetch'], [])

    def test_private_file_at_new_public_path_is_reviewed(self):
        saved = dict(SAVED, **{'new.md': b'mine\n'})
        p = hosted_update.plan(hosted_update.load_inventory(inventory(NEW, '2.0.0')), hosted_update.saved_from_files(saved),
                               hosted_update.load_inventory(inventory(OLD, '1.0.0')))
        self.assertIn({'path': 'new.md', 'reason': 'a private file sits at a new public path'}, p['review'])

    def test_readback_json_as_saved_state(self):
        readback = {'inventory': [{'path': p, 'size_bytes': len(d)} for p, d in SAVED.items()],
                    'files': [{'path': p, 'sha256': sha(d)} for p, d in SAVED.items() if p != 'gone.md']}
        saved = hosted_update.saved_from_readback(readback)
        p = hosted_update.plan(hosted_update.load_inventory(inventory(NEW, '2.0.0')), saved, hosted_update.load_inventory(inventory(OLD, '1.0.0')))
        self.assertEqual(p['delete_paths'], [])
        self.assertIn({'path': 'gone.md', 'reason': 'saved copy not hashed; delete only after confirming it equals the old public file'}, p['review'])


class PackTest(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, '-I', str(SCRIPT), *map(str, args)], capture_output=True, text=True)

    def write(self, root, files):
        for path, data in files.items():
            target = root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)

    def test_pack_verifies_text_and_base64_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = pathlib.Path(tmp)
            (tmp / 'new.json').write_text(json.dumps(inventory(NEW, '2.0.0')))
            (tmp / 'old.json').write_text(json.dumps(inventory(OLD, '1.0.0')))
            self.write(tmp / 'saved', SAVED)
            r = self.run_cli('plan', '--new', tmp / 'new.json', '--old', tmp / 'old.json', '--saved', tmp / 'saved', '--out', tmp / 'plan.json')
            self.assertEqual(r.returncode, 0, r.stderr)
            fetched = {p: NEW[p] for p in ['b.md', 'clash.md', 'new.md']}
            self.write(tmp / 'fetched', fetched)
            (tmp / 'fetched' / 'logo.png.b64').write_text(base64.b64encode(NEW['logo.png']).decode())
            r = self.run_cli('pack', '--new', tmp / 'new.json', '--plan', tmp / 'plan.json', '--files', tmp / 'fetched', '--out', tmp / 'delta.zip')
            self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
            with zipfile.ZipFile(tmp / 'delta.zip') as z:
                self.assertEqual(sorted(z.namelist()), ['b.md', 'clash.md', 'logo.png', 'new.md'])
                self.assertEqual(z.read('logo.png'), NEW['logo.png'])
            summary = json.loads((tmp / 'delta.zip.json').read_text())
            self.assertEqual(summary['delete_paths'], ['gone.md'])
            self.assertEqual(summary['verified'], 4)
            self.assertEqual(summary['zip_sha256'], sha((tmp / 'delta.zip').read_bytes()))

    def test_pack_refuses_altered_or_missing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = pathlib.Path(tmp)
            (tmp / 'new.json').write_text(json.dumps(inventory(NEW, '2.0.0')))
            (tmp / 'plan.json').write_text(json.dumps({'fetch': ['b.md', 'new.md'], 'delete_paths': [], 'review': []}))
            self.write(tmp / 'fetched', {'b.md': b'b2\r\n'})
            r = self.run_cli('pack', '--new', tmp / 'new.json', '--plan', tmp / 'plan.json', '--files', tmp / 'fetched', '--out', tmp / 'delta.zip')
            self.assertEqual(r.returncode, 1)
            self.assertIn('b.md', r.stdout)
            self.assertIn('new.md', r.stdout)
            self.assertFalse((tmp / 'delta.zip').exists())

    def test_git_tree_inventory_verifies_blob_hashes_under_prefix(self):
        files = {'plugins/x/plugin.json': b'{}\n', 'plugins/x/skills/s/SKILL.md': b'hi\n', 'README.md': b'r\n'}
        tree = {'sha': 'f' * 40, 'tree': [{'path': p, 'type': 'blob', 'sha': blob(d), 'size': len(d)} for p, d in files.items()]
                + [{'path': 'plugins/x', 'type': 'tree', 'sha': 'e' * 40}]}
        inv = hosted_update.load_inventory(tree, prefix='plugins/x')
        self.assertEqual(sorted(inv), ['plugin.json', 'skills/s/SKILL.md'])
        with tempfile.TemporaryDirectory() as tmp:
            tmp = pathlib.Path(tmp)
            (tmp / 'tree.json').write_text(json.dumps(tree))
            self.write(tmp / 'fetched', {'plugin.json': b'{}\n', 'skills/s/SKILL.md': b'hi\n'})
            (tmp / 'plan.json').write_text(json.dumps({'fetch': ['plugin.json', 'skills/s/SKILL.md'], 'delete_paths': [], 'review': []}))
            r = self.run_cli('pack', '--new', tmp / 'tree.json', '--prefix', 'plugins/x', '--plan', tmp / 'plan.json', '--files', tmp / 'fetched', '--out', tmp / 'd.zip')
            self.assertEqual(r.returncode, 0, r.stderr + r.stdout)

    def test_verify_saved_plugin_after_direct_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = pathlib.Path(tmp)
            self.write(tmp / 'saved', {'a.md': b'a1\n', 'b.md': b'b2\n'})
            (tmp / 'ok.json').write_text(json.dumps({'a.md': sha(b'a1\n'), 'b.md': blob(b'b2\n')}))
            r = self.run_cli('verify', '--expect', tmp / 'ok.json', '--saved', tmp / 'saved', '--absent', 'gone.md')
            self.assertEqual(r.returncode, 0, r.stdout)
            (tmp / 'bad.json').write_text(json.dumps({'a.md': sha(b'other'), 'c.md': sha(b'c')}))
            r = self.run_cli('verify', '--expect', tmp / 'bad.json', '--saved', tmp / 'saved', '--absent', 'b.md')
            self.assertEqual(r.returncode, 1)
            for word in ('a.md', 'c.md', 'b.md: still present'):
                self.assertIn(word, r.stdout)

    def test_plan_without_saved_state_fetches_everything(self):
        p = hosted_update.plan(hosted_update.load_inventory(inventory(NEW, '2.0.0')), {}, None)
        self.assertEqual(p['fetch'], sorted(NEW))


if __name__ == '__main__':
    unittest.main()
