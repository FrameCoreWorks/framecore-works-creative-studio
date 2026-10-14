"""Release helper (scripts/release.py): dirty trees, publication commits and asset comparisons, Node test reporters."""
import importlib.util
import pathlib
import subprocess
import tempfile
import types
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('release', ROOT / 'scripts/release.py')
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)


class Release(unittest.TestCase):
    def test_node_counts_from_tap_and_spec_reporters(self):
        self.assertEqual(release.parse_checks('# tests 5\n# pass 4\n# skipped 1\n')['node'], {'tests': 5, 'pass': 4, 'skipped': 1})
        self.assertEqual(release.parse_checks('ℹ tests 218\nℹ pass 208\nℹ fail 2\n')['node'], {'tests': 218, 'pass': 208, 'fail': 2})

    def test_a_dirty_tree_stops_before_anything_is_written(self):
        original = release.git
        release.git = lambda *args, **kwargs: '?? unfinished-user-draft.txt' if args[:1] == ('status',) else original(*args, **kwargs)
        try:
            with self.assertRaisesRegex(release.ReleaseError, 'uncommitted changes'):
                release.prepare(types.SimpleNamespace(version='999.0.0'))
        finally:
            release.git = original

    def test_publish_refuses_a_dirty_tree(self):
        original = release.git
        release.git = lambda *args, **kwargs: ' M unfinished-user-draft.txt' if args[:1] == ('status',) else original(*args, **kwargs)
        try:
            with self.assertRaisesRegex(release.ReleaseError, 'uncommitted changes'):
                release.publish(types.SimpleNamespace(version='999.0.0', wait=0, min_runs=1, change_id='X', push=False))
        finally:
            release.git = original

    def test_a_failed_asset_comparison_stops_the_record(self):
        release.require_matches({'a.zip': True})
        with self.assertRaisesRegex(release.ReleaseError, 'inventory.json'):
            release.require_matches({'a.zip': True, 'a.zip.inventory.json': False})

    def test_the_publication_commit_holds_only_its_records(self):
        original = release.ROOT
        with tempfile.TemporaryDirectory() as tmp:
            repo = pathlib.Path(tmp)
            for command in (['init', '-q'], ['config', 'user.email', 't@t'], ['config', 'user.name', 't']):
                subprocess.run(['git', *command], cwd=repo, check=True)
            (repo / 'record.json').write_text('{}')
            (repo / 'draft.txt').write_text('unfinished')
            release.ROOT = repo
            try:
                release.commit('docs: record', 'body', 'X', 'abc', False, paths=['record.json'])
                files = release.git('show', '--name-only', '--format=', 'HEAD').split()
                self.assertEqual(files, ['record.json'])
                self.assertIn('draft.txt', release.git('status', '--porcelain'))
                (repo / 'other.txt').write_text('x')
                release.git('add', 'other.txt')
                (repo / 'record.json').write_text('{"a": 1}')
                with self.assertRaisesRegex(release.ReleaseError, 'other.txt'):
                    release.commit('docs: record', 'body', 'X', 'abc', False, paths=['record.json'])
            finally:
                release.ROOT = original

    def test_manifest_and_zip_skip_the_same_generated_files(self):
        # Audit INSTALL-03: one rule for both; a stray log or cache is declared nowhere.
        import sys
        sys.path.insert(0, str(ROOT / 'scripts'))
        try:
            import build_install_manifest as manifest
            import package_release as packer
        finally:
            sys.path.pop(0)
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / 'skills/x/__pycache__').mkdir(parents=True)
            (root / 'skills/x/SKILL.md').write_text('a')
            (root / 'skills/x/__pycache__/m.cpython-313.pyc').write_bytes(b'0')
            (root / 'build.log').write_text('log')
            (root / '.DS_Store').write_bytes(b'0')
            declared = [entry['path'] for entry in manifest.inventory(root)]
            packed = [path.relative_to(root).as_posix() for path in packer.inventory(root)]
        self.assertEqual(declared, ['skills/x/SKILL.md'])
        self.assertEqual(packed, declared)


if __name__ == '__main__':
    unittest.main()
