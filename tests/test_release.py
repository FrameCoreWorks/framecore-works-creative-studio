"""Release helper (scripts/release.py): dirty trees, publication commits and asset comparisons, Node test reporters."""
import importlib.util
import pathlib
import subprocess
import tempfile
import types
import unittest
from unittest import mock

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

    def test_a_notes_heading_fix_after_the_tag_clears_only_the_notes_workflow(self):
        # 1.122.0 and 1.124.0: the notes refresh failed on the tag commit and a notes-only commit on main fixed it.
        notes = {'name': 'Refresh current release notes', 'conclusion': 'failure', 'html_url': 'u1'}
        checks = {'name': 'Check Studio sources', 'conclusion': 'failure', 'html_url': 'u2'}
        later = [('c2', ['RELEASE_NOTES.md'])]
        ok = lambda sha: [{'name': 'Refresh current release notes', 'conclusion': 'success', 'id': 7, 'head_sha': sha}]
        left, correction = release.notes_correction([notes], later, ok)
        self.assertEqual(left, [])
        self.assertEqual(correction['commit'], 'c2')
        left, correction = release.notes_correction([notes, checks], later, ok)
        self.assertEqual(left, [checks])
        # a later commit that also changed other files, or a refresh that failed again, does not count
        self.assertEqual(release.notes_correction([notes], [('c3', ['RELEASE_NOTES.md', 'README.md'])], ok), ([notes], None))
        bad = lambda sha: [{'name': 'Refresh current release notes', 'conclusion': 'failure', 'id': 8, 'head_sha': sha}]
        self.assertEqual(release.notes_correction([notes], later, bad), ([notes], None))

    def test_publish_fetches_the_tag_before_choosing_the_commit(self):
        # 1.124.0: without the tag locally, publish fell back to HEAD (a later commit) and waited on its workflows.
        calls = []

        def fake_git(*args, **kwargs):
            calls.append(args)
            if args[:1] == ('status',):
                return ''
            if args[:1] == ('rev-list',):
                raise SystemExit('stop after choosing the commit')
            return ''
        original = release.git
        release.git = fake_git
        try:
            with self.assertRaises(SystemExit):
                release.publish(types.SimpleNamespace(version='9.9.9', wait=0, min_runs=3, change_id='X', push=False))
        finally:
            release.git = original
        fetched = [i for i, c in enumerate(calls) if c[:1] == ('fetch',) and any('refs/tags/v9.9.9' in a for a in c)]
        chosen = [i for i, c in enumerate(calls) if c[:1] == ('rev-list',)]
        self.assertTrue(fetched and chosen and fetched[0] < chosen[0])

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

    def test_commit_uses_the_current_development_surface(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = pathlib.Path(tmp)
            for command in (['init', '-q'], ['config', 'user.email', 't@t'], ['config', 'user.name', 't']):
                subprocess.run(['git', *command], cwd=repo, check=True)
            (repo / 'record.json').write_text('{}')
            with mock.patch.object(release, 'ROOT', repo), mock.patch.dict(release.os.environ, {'STUDIO_ORIGIN_AGENT': 'chatgpt-work'}):
                release.commit('docs: evidence', 'Measured sandbox recovery', 'CW-TEST', 'abc', False, paths=['record.json'])
                body = release.git('log', '-1', '--format=%B')
            self.assertIn('Origin-Agent: chatgpt-work', body)
            self.assertNotIn('Origin-Agent: cloud-code', body)
            self.assertIn('ChatGPT-Work-Sync: pending', body)
        with mock.patch.dict(release.os.environ, {'STUDIO_ORIGIN_AGENT': 'unknown'}):
            with self.assertRaises(release.ReleaseError):
                release.origin_agent()

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
