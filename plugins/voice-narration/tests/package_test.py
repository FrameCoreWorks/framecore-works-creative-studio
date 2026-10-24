"""voice-narration package: one skill, consistent manifests, no vendored engine, no key or server route."""
import json
import pathlib
import unittest

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
ROOT = PLUGIN.parent.parent
VERSION = '1.0.0'


def load(path):
    return json.loads((PLUGIN / path).read_text(encoding='utf-8'))


class Package(unittest.TestCase):
    def test_manifests_agree(self):
        versions = set()
        for path in ('plugin.json', '.claude-plugin/plugin.json', '.codex-plugin/plugin.json'):
            data = load(path)
            self.assertEqual(data['name'], 'voice-narration', path)
            versions.add(data['version'])
        self.assertEqual(versions, {VERSION})
        self.assertEqual(load('.codex-plugin/plugin.json')['interface']['displayName'], 'Voice And Narration')
        self.assertEqual(load('.codex-plugin/plugin.json')['skills'], './skills')
        market = json.loads((ROOT / '.claude-plugin/marketplace.json').read_text(encoding='utf-8'))
        entries = {p['name']: p for p in market['plugins']}
        self.assertEqual(entries['voice-narration']['source'], './plugins/voice-narration')
        self.assertEqual(entries['voice-narration']['version'], VERSION)

    def test_no_vendored_engine(self):
        for path in PLUGIN.rglob('*'):
            if '__pycache__' in path.parts:
                continue
            self.assertNotIn(path.suffix, ('.safetensors', '.pt', '.bin'), path)
            self.assertFalse(path.is_dir() and path.name == 'voxcpm', path)
            if path.is_file() and path.name != 'package_test.py':
                text = path.read_text(encoding='utf-8', errors='ignore')
                self.assertNotIn('ELEVENLABS_API_KEY', text, path)
                self.assertNotIn('mcpServers', text, path)


if __name__ == '__main__':
    unittest.main()
