import copy
import io
import json
import pathlib
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
import check_host_smoke  # noqa: E402

TEMPLATE = json.loads((ROOT / 'verification/host-smoke-template.json').read_text())


def filled():
    record = copy.deepcopy(TEMPLATE)
    record.update({'template': False, 'plugin_version': '1.42.0', 'version_read_back': 'asked in a new chat',
                   'date': '2026-10-09', 'tester': 'owner', 'client': 'ordinary ChatGPT, Android browser',
                   'reasoning_setting': 'high', 'code_execution': 'yes', 'web_search': 'yes'})
    for case in record['cases']:
        case.update({'result': 'PASS_REPORTED', 'observed': 'as expected', 'evidence': ['screenshot-1.png']})
    return record


class HostSmokeChecks(unittest.TestCase):
    def run_check(self, records):
        with tempfile.TemporaryDirectory() as temp:
            folder = pathlib.Path(temp)
            shutil.copy(ROOT / 'verification/host-smoke-template.json', folder)
            for name, record in records.items():
                (folder / name).write_text(json.dumps(record))
            out = io.StringIO()
            with redirect_stdout(out):
                code = check_host_smoke.main(['check_host_smoke.py', str(folder)])
            return code, out.getvalue()

    def test_repository_records_pass(self):
        out = io.StringIO()
        with redirect_stdout(out):
            self.assertEqual(check_host_smoke.main(['check_host_smoke.py']), 0, out.getvalue())

    def test_complete_record_passes(self):
        self.assertEqual(self.run_check({'host-smoke-1.42.0-chatgpt-2026-10-09.json': filled()})[0], 0)

    def test_missing_client_or_reasoning_fails(self):
        record = filled(); record['reasoning_setting'] = ''
        code, out = self.run_check({'host-smoke-x.json': record})
        self.assertEqual(code, 1); self.assertIn('reasoning_setting is empty', out)

    def test_a_run_case_needs_observation_and_evidence(self):
        record = filled(); record['cases'][4]['evidence'] = []
        code, out = self.run_check({'host-smoke-x.json': record})
        self.assertEqual(code, 1); self.assertIn('SM5: name the evidence', out)

    def test_unknown_result_and_missing_case_fail(self):
        record = filled(); record['cases'][0]['result'] = 'PASS'
        self.assertIn('result must be one of', self.run_check({'host-smoke-x.json': record})[1])
        record = filled(); record['cases'].pop()
        self.assertIn('SM1 to SM8', self.run_check({'host-smoke-x.json': record})[1])

    def test_not_run_needs_a_reason(self):
        record = filled(); record['cases'][7].update({'result': 'NOT_RUN', 'notes': ''})
        self.assertIn('SM8: a case that did not run needs the reason', self.run_check({'host-smoke-x.json': record})[1])


if __name__ == '__main__':
    unittest.main()
