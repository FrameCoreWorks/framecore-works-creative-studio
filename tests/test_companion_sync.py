"""Frozen companion copies during the Toolbox/Open Assets move (temporary, until the copies are removed in Stage 5).

The earshot-audio and framecore-open-assets folders in this repository stay as they were released, carry a
deprecation marker, and no Studio route, marketplace entry or skill points at them.
"""
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugins/framecore-work-creative-studio'
FROZEN = {'earshot-audio': '1.1.0', 'framecore-open-assets': '0.2.1'}


class FrozenCopies(unittest.TestCase):
    def test_each_copy_is_marked_deprecated_at_its_last_version(self):
        for name, version in FROZEN.items():
            folder = ROOT / 'plugins' / name
            manifest = json.loads((folder / '.claude-plugin/plugin.json').read_text(encoding='utf-8'))
            self.assertEqual(manifest['version'], version, name)
            marker = (folder / 'DEPRECATED.md').read_text(encoding='utf-8')
            self.assertIn('frozen', marker, name)
            self.assertIn('github.com/FrameCoreWorks/', marker, name)

    def test_no_marketplace_entry_or_studio_file_points_at_a_frozen_copy(self):
        market = json.loads((ROOT / '.claude-plugin/marketplace.json').read_text(encoding='utf-8'))
        sources = [e['source'] for e in market['plugins'] if isinstance(e['source'], str)]
        for name in FROZEN:
            self.assertNotIn(f'./plugins/{name}', sources)
        hits = [str(p.relative_to(PLUGIN)) for p in (PLUGIN / 'skills').rglob('*')
                if p.is_file() and p.suffix in ('.md', '.json', '.py')
                and any(f'plugins/{n}/' in p.read_text(encoding='utf-8', errors='ignore') for n in FROZEN)]
        self.assertEqual(hits, [])


if __name__ == '__main__':
    unittest.main()
