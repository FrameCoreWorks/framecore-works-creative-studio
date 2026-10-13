"""Release helper (scripts/release.py): it refuses a dirty working tree and reads both Node test reporters."""
import importlib.util
import pathlib
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


if __name__ == '__main__':
    unittest.main()
