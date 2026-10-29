"""Version guard (scripts/check_version_bump.py): companion plugins must bump when they change after a release tag."""
import importlib.util
import json
import pathlib
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('check_version_bump', ROOT / 'scripts/check_version_bump.py')
bump = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bump)


class CompanionGuard(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name)
        self.git('init', '-q')
        self.git('config', 'user.email', 't@example.com')
        self.git('config', 'user.name', 't')
        self.write('plugins/framecore-work-creative-studio/plugin.json', {'version': '1.0.0'})
        self.write('plugins/brand-kit/plugin.json', {'version': '1.0.0'})
        (self.root / 'plugins/brand-kit/tool.py').write_text('a = 1\n')
        self.commit()
        self.git('tag', 'v1.0.0')

    def tearDown(self):
        self.tmp.cleanup()

    def git(self, *args):
        subprocess.run(['git', '-C', str(self.root), *args], check=True, capture_output=True)

    def write(self, path, data):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(data))

    def commit(self):
        self.git('add', '-A')
        self.git('commit', '-q', '-m', 'c')

    def test_an_unchanged_companion_passes(self):
        self.assertEqual(bump.companion_errors(self.root), [])

    def test_a_changed_companion_without_a_bump_fails(self):
        (self.root / 'plugins/brand-kit/tool.py').write_text('a = 2\n')
        self.commit()
        self.assertRegex(' '.join(bump.companion_errors(self.root)), 'plugins/brand-kit changed after v1.0.0')

    def test_a_changed_companion_with_a_bump_passes(self):
        (self.root / 'plugins/brand-kit/tool.py').write_text('a = 2\n')
        self.write('plugins/brand-kit/plugin.json', {'version': '1.0.1'})
        self.commit()
        self.assertEqual(bump.companion_errors(self.root), [])

    def test_a_new_companion_passes(self):
        self.write('plugins/new-one/plugin.json', {'version': '0.1.0'})
        self.commit()
        self.assertEqual(bump.companion_errors(self.root), [])

    def test_freezing_a_companion_with_only_a_deprecation_marker_passes(self):
        # 2026-10-29: frozen copies get DEPRECATED.md and keep their last released version.
        (self.root / 'plugins/brand-kit/DEPRECATED.md').write_text('frozen\n')
        self.commit()
        self.assertEqual(bump.companion_errors(self.root), [])

    def test_a_frozen_companion_that_changes_otherwise_still_fails(self):
        (self.root / 'plugins/brand-kit/DEPRECATED.md').write_text('frozen\n')
        (self.root / 'plugins/brand-kit/tool.py').write_text('a = 2\n')
        self.commit()
        self.assertRegex(' '.join(bump.companion_errors(self.root)), 'plugins/brand-kit changed')


if __name__ == '__main__':
    unittest.main()
