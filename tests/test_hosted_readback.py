import copy
import io
import json
import pathlib
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
import check_hosted_readback as checker  # noqa: E402

SOURCE = json.loads((ROOT / 'config/install-sources.json').read_text())


def readback(hashes=True):
    data = {'version': SOURCE['version'], 'date': '2026-10-09', 'plugin_id': 'plugins_example', 'release_id': 'pluginrel_example',
            'scope': 'USER', 'audience': 'PRIVATE', 'source_commit': 'f' * 40,
            'inventory': [{'path': f['path'], 'size_bytes': f['bytes']} for f in SOURCE['files']]}
    if hashes:
        data['files'] = [{'path': f['path'], 'sha256': f['sha256']} for f in SOURCE['files']]
    return data


class HostedReadback(unittest.TestCase):
    def run_check(self, data, *extra):
        with tempfile.TemporaryDirectory() as temp:
            path = pathlib.Path(temp, 'readback.json')
            path.write_text(json.dumps(data))
            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                code = checker.main([str(path), *[a.replace('{temp}', temp) for a in extra]])
            return code, (json.loads(out.getvalue()) if out.getvalue() else None), err.getvalue(), temp

    def test_complete_readback_with_hashes_is_full_byte_parity(self):
        code, report, _, _ = self.run_check(readback())
        self.assertEqual((code, report['verdict']), (0, 'full_byte_parity'))
        self.assertEqual(report['hashed_and_matching'], len(SOURCE['files']))

    def test_sizes_without_every_hash_is_partial_parity(self):
        data = readback(hashes=False)
        data['files'] = [{'path': SOURCE['files'][0]['path'], 'sha256': SOURCE['files'][0]['sha256']}]
        code, report, _, _ = self.run_check(data)
        self.assertEqual((code, report['verdict']), (0, 'path_size_parity'))
        self.assertEqual(report['not_hashed'], len(SOURCE['files']) - 1)

    def test_missing_path_size_hash_or_version_is_a_mismatch(self):
        for change, expect in [
            (lambda d: d['inventory'].pop(), 'not in the saved plugin'),
            (lambda d: d['inventory'][0].update(size_bytes=1), 'another size'),
            (lambda d: d['files'][0].update(sha256='0' * 64), 'another SHA-256'),
            (lambda d: d.update(version='1.0.0'), 'saved version'),
        ]:
            data = readback()
            change(data)
            code, report, _, _ = self.run_check(data)
            self.assertEqual(code, 1)
            self.assertTrue(any(expect in p for p in report['problems']), report['problems'])

    def test_extra_saved_files_are_listed_not_failed(self):
        data = readback()
        data['inventory'].append({'path': 'skills/my-notes/SKILL.md', 'size_bytes': 10})
        code, report, _, _ = self.run_check(data)
        self.assertEqual((code, report['verdict'], report['extra']), (0, 'full_byte_parity', ['skills/my-notes/SKILL.md']))

    def test_record_is_written_once(self):
        code, _, _, temp = self.run_check(readback(), '--record', '{temp}/hosted.json')
        self.assertEqual(code, 0)
        with tempfile.TemporaryDirectory() as again:
            target = pathlib.Path(again, 'hosted.json')
            target.write_text('{}')
            code, _, err, _ = self.run_check(readback(), '--record', str(target))
            self.assertEqual(code, 2)
            self.assertIn('already exists', err)

    def test_readback_without_inventory_is_rejected(self):
        data = copy.deepcopy(readback())
        data['inventory'] = []
        code, _, err, _ = self.run_check(data)
        self.assertEqual(code, 2)
        self.assertIn('no inventory', err)


if __name__ == '__main__':
    unittest.main()
