"""Release identity generation checks; no host activation or model calls."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/build_install_manifest.py'
spec = importlib.util.spec_from_file_location('studio_inventory', SCRIPT)
inventory = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inventory)


class PackageIdentityChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.identity = {'name': 'framecore-work-creative-studio', 'version': '9.8.7'}
        (self.root / '.codex-plugin').mkdir()
        for relative in ['plugin.json', '.codex-plugin/plugin.json']:
            (self.root / relative).write_text(json.dumps(self.identity))
        self.entry = self.root / 'skills/workflow-orchestrator/SKILL.md'
        self.entry.parent.mkdir(parents=True)
        self.original = ('preserved before\n' + inventory.IDENTITY_BEGIN +
                         '\n{"name":"old","version":"0.0.0"}\n' +
                         inventory.IDENTITY_END + '\npreserved after\n')
        self.entry.write_text(self.original)

    def test_updates_only_projection_and_is_idempotent(self):
        inventory.sync_package_identity(self.root)
        expected = ('preserved before\n' + inventory.IDENTITY_BEGIN + '\n' +
                    json.dumps(self.identity, separators=(',', ':')) + '\n' +
                    inventory.IDENTITY_END + '\npreserved after\n')
        self.assertEqual(self.entry.read_text(), expected)
        before = self.entry.stat().st_mtime_ns
        inventory.sync_package_identity(self.root)
        self.assertEqual(self.entry.stat().st_mtime_ns, before)

    def test_missing_duplicate_and_reversed_markers_fail_before_write(self):
        for value in [self.original.replace(inventory.IDENTITY_BEGIN, ''),
                      self.original + inventory.IDENTITY_END,
                      inventory.IDENTITY_END + '\n' + inventory.IDENTITY_BEGIN]:
            with self.subTest(value=value):
                self.entry.write_text(value)
                with self.assertRaises(ValueError):
                    inventory.sync_package_identity(self.root)
                self.assertEqual(self.entry.read_text(), value)

    def test_conflicting_manifests_do_not_repair_silently(self):
        (self.root / '.codex-plugin/plugin.json').write_text(json.dumps({
            **self.identity, 'version': '9.8.6'}))
        with self.assertRaises(ValueError):
            inventory.sync_package_identity(self.root)
        self.assertEqual(self.entry.read_text(), self.original)

    def test_inventory_verification_does_not_rewrite_stale_entry(self):
        old = inventory.PLUGIN, inventory.MANIFEST, inventory.ROOT
        self.addCleanup(self.restore_roots, old)
        inventory.PLUGIN, inventory.MANIFEST, inventory.ROOT = (
            self.root, self.root / 'inventory.json', self.root)
        inventory.MANIFEST.write_text('{}')
        with self.assertRaises(ValueError):
            inventory.verify_source()
        self.assertEqual(self.entry.read_text(), self.original)

    @staticmethod
    def restore_roots(old):
        inventory.PLUGIN, inventory.MANIFEST, inventory.ROOT = old


if __name__ == '__main__':
    unittest.main()
