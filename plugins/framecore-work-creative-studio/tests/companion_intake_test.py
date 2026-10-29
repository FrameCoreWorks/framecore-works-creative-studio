"""Companion results (delivery-documentation/scripts/companion_intake.py): a framecore-task-result/1 from Toolbox or
Open Assets is checked against the shared schema, the companion registry and the actual file bytes before Studio uses it."""
import contextlib
import hashlib
import importlib.util
import io
import json
import pathlib
import tempfile
import unittest
from unittest import mock

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
TOOL = PLUGIN / 'skills/delivery-documentation/scripts/companion_intake.py'
spec = importlib.util.spec_from_file_location('companion_intake', TOOL)
intake = importlib.util.module_from_spec(spec)
spec.loader.exec_module(intake)
FIXTURES = PLUGIN / 'tests/fixtures/companion'
SCHEMA = PLUGIN / 'skills/pipeline-core/assets/companion-contract.schema.json'


def run(*args):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = intake.main(list(args))
    return code, out.getvalue(), err.getvalue()


class Intake(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = pathlib.Path(self.tmp.name)
        (self.dir / 'hit.wav').write_bytes(b'wav')

    def tearDown(self):
        self.tmp.cleanup()

    def result(self, name='toolbox-earshot-result.json', **change):
        doc = json.loads((FIXTURES / name).read_text())
        for item in doc['outputs']:
            item['path'] = str(self.dir / item['path'])
        doc.update(change)
        path = self.dir / ('r-' + name)
        path.write_text(json.dumps(doc))
        return path, doc

    def test_schema_is_the_shared_contract_byte_for_byte(self):
        self.assertEqual(hashlib.sha256(SCHEMA.read_bytes()).hexdigest(),
                         'e7cc0f4e612395768e8c8c6cf2a033a555bc69b4c8ea5ca45c4db019a342897a')

    def test_both_companions_pass_and_outputs_are_recorded_not_reviewed(self):
        for name in ('toolbox-earshot-result.json', 'open-assets-result.json'):
            path, _ = self.result(name)
            code, out, _ = run('check', str(path), '--json')
            report = json.loads(out)
            self.assertEqual((code, report['status']), (0, 'PASS'), report)
            entry = report['ledger_entry']
            self.assertEqual(entry['outputs'][0]['review'], 'not_reviewed')
            self.assertEqual(entry['outputs'][0]['sha256'], hashlib.sha256(b'wav').hexdigest())

    def test_changed_or_missing_output_bytes_fail(self):
        path, _ = self.result()
        (self.dir / 'hit.wav').write_bytes(b'changed')
        code, out, _ = run('check', str(path), '--json')
        self.assertEqual(code, 1)
        self.assertIn('HASH_MISMATCH', [e['code'] for e in json.loads(out)['errors']])
        (self.dir / 'hit.wav').unlink()
        code, out, _ = run('check', str(path), '--json')
        self.assertIn('OUTPUT_MISSING', [e['code'] for e in json.loads(out)['errors']])

    def test_unknown_companion_or_capability_fails(self):
        for provider in ({'plugin': 'earshot-audio', 'capability': 'earshot', 'operation': 'run'},
                         {'plugin': 'toolbox', 'capability': 'voice', 'operation': 'run'}):
            path, _ = self.result(provider=provider)
            code, out, _ = run('check', str(path), '--json')
            self.assertEqual(code, 1)
            self.assertIn('UNKNOWN_PROVIDER', [e['code'] for e in json.loads(out)['errors']])

    def test_schema_violation_fails(self):
        path, _ = self.result(status='completed')
        code, out, _ = run('check', str(path), '--json')
        self.assertEqual(code, 1)
        self.assertIn('SCHEMA', [e['code'] for e in json.loads(out)['errors']])

    def test_warnings_and_unexecuted_checks_are_carried_into_the_ledger(self):
        path, _ = self.result(warnings=['ran on an unlocked legacy runtime'])
        report = json.loads(run('check', str(path), '--json')[1])
        self.assertEqual(report['ledger_entry']['warnings'], ['ran on an unlocked legacy runtime'])
        self.assertEqual(report['ledger_entry']['unexecuted_checks'][0]['check'], 'listening_review')

    def test_a_non_success_result_is_recorded_but_places_nothing(self):
        for status in ('needs_consent', 'failed'):
            path, _ = self.result(status=status)
            code, out, _ = run('check', str(path), '--json')
            report = json.loads(out)
            self.assertEqual((code, report['status']), (0, 'PASS'), status)
            self.assertFalse(report['ledger_entry']['placeable'], status)

    def test_a_verified_success_is_placeable(self):
        path, _ = self.result()
        self.assertTrue(json.loads(run('check', str(path), '--json')[1])['ledger_entry']['placeable'])

    def test_relative_outputs_resolve_against_the_folder_the_companion_ran_in(self):
        doc = json.loads((FIXTURES / 'toolbox-earshot-result.json').read_text())
        (self.dir / 'out').mkdir()
        path = self.dir / 'out' / 'r.json'
        path.write_text(json.dumps(doc))
        code, out, _ = run('check', str(path), '--base', str(self.dir), '--json')
        report = json.loads(out)
        self.assertEqual(code, 0, report)
        self.assertEqual(report['ledger_entry']['outputs'][0]['path'], str((self.dir / 'hit.wav').resolve()))

    def test_declared_size_must_match_the_file(self):
        doc = json.loads((FIXTURES / 'toolbox-earshot-result.json').read_text())
        doc['outputs'][0].update(path=str(self.dir / 'hit.wav'), bytes=999)
        path = self.dir / 'r.json'; path.write_text(json.dumps(doc))
        code, out, _ = run('check', str(path), '--json')
        self.assertEqual(code, 1)
        self.assertIn('SIZE_MISMATCH', [e['code'] for e in json.loads(out)['errors']])

    def test_recorded_paths_are_normalised(self):
        doc = json.loads((FIXTURES / 'toolbox-earshot-result.json').read_text())
        (self.dir / 'sub').mkdir()
        doc['outputs'][0]['path'] = str(self.dir / 'sub' / '..' / 'hit.wav')
        path = self.dir / 'r.json'; path.write_text(json.dumps(doc))
        report = json.loads(run('check', str(path), '--json')[1])
        self.assertEqual(report['ledger_entry']['outputs'][0]['path'], str((self.dir / 'hit.wav').resolve()))

    def test_a_hash_with_a_trailing_newline_is_a_schema_error(self):
        path, _ = self.result(inputs=[{'path': 'a.wav', 'sha256': 'a' * 64 + '\n', 'bytes': 1}])
        self.assertIn('SCHEMA', [e['code'] for e in json.loads(run('check', str(path), '--json')[1])['errors']])

    def test_a_release_other_than_the_reviewed_one_is_warned_not_refused(self):
        path, _ = self.result(provider={'plugin': 'toolbox', 'version': '0.0.1', 'capability': 'earshot',
                                        'operation': 'run', 'command': 'sfx'})
        code, out, _ = run('check', str(path), '--json')
        report = json.loads(out)
        self.assertEqual(code, 0)
        self.assertTrue(any('reviewed 1.2.1' in w for w in report['ledger_entry']['intake_warnings']))

    def test_an_unreadable_output_is_reported(self):
        path, _ = self.result()
        with mock.patch.object(intake, 'sha256', side_effect=PermissionError('denied')):
            code, out, _ = run('check', str(path), '--json')
        self.assertEqual(code, 1)
        self.assertIn('OUTPUT_UNREADABLE', [e['code'] for e in json.loads(out)['errors']])

    def test_unreadable_input_is_exit_2(self):
        bad = self.dir / 'bad.json'; bad.write_text('{not json')
        self.assertEqual(run('check', str(bad))[0], 2)


if __name__ == '__main__':
    unittest.main()
