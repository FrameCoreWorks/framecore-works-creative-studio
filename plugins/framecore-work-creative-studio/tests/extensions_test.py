"""Recommended extensions (workflow-orchestrator/assets/extensions): the registry is complete, pinned and per host."""
import contextlib
import copy
import importlib.util
import io
import json
import pathlib
import tempfile
import unittest

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
TOOL = PLUGIN / 'skills/workflow-orchestrator/assets/extensions/extensions.py'
spec = importlib.util.spec_from_file_location('extensions', TOOL)
ext = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ext)
DATA = json.loads((TOOL.parent / 'extensions.json').read_text(encoding='utf-8'))


def run(*args):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = ext.main(list(args))
    return code, out.getvalue(), err.getvalue()


class Registry(unittest.TestCase):
    def test_the_registry_is_valid_and_covers_the_same_hosts_as_the_environment_check(self):
        self.assertEqual(ext.validate(DATA), [])
        tools = json.loads((PLUGIN / 'skills/workflow-orchestrator/assets/environment-check/tools.json').read_text(encoding='utf-8'))
        self.assertEqual(sorted(DATA['hosts']), sorted(h['id'] for h in tools['hosts']))

    def test_an_unpinned_command_or_a_plan_without_a_dry_run_is_refused(self):
        bad = copy.deepcopy(DATA)
        bad['extensions'][0]['hosts']['codex']['install'] = 'npx -y rea-agents@latest setup --client codex --yes'
        bad['extensions'][0]['hosts']['claude_code']['plan'] = 'npx -y rea-agents@6.5.0 setup --client claude_code'
        problems = ' '.join(ext.validate(bad))
        self.assertIn('codex install must use the pinned', problems)
        self.assertIn('claude_code plan must be a dry run', problems)

    def test_an_unsupported_host_needs_a_reason_and_every_entry_states_rights(self):
        bad = copy.deepcopy(DATA)
        del bad['extensions'][0]['hosts']['chatgpt_work']['reason']
        del bad['extensions'][0]['rights']
        problems = ' '.join(ext.validate(bad))
        self.assertIn('chatgpt_work reason missing', problems)
        self.assertIn('rights missing', problems)

    def test_list_and_show_print_the_status_and_the_pinned_steps(self):
        code, out, _ = run('list', '--host', 'chatgpt_work')
        self.assertEqual(code, 0)
        self.assertIn('rea:', out)
        self.assertIn('not_supported', out)
        code, out, _ = run('show', 'rea', '--host', 'claude_code', '--json')
        report = json.loads(out)
        self.assertEqual(report['status'], 'native')
        self.assertIn('--dry-run', report['steps']['plan'])
        self.assertTrue(all('rea-agents@6.5.0' in report['steps'][k] for k in ('plan', 'install', 'verify', 'remove')))
        self.assertEqual(run('show', 'nothing', '--host', 'codex')[0], 1)
        self.assertEqual(run('list', '--host', 'mars')[0], 1)

    def test_a_broken_registry_exits_2(self):
        with tempfile.TemporaryDirectory() as temp:
            path = pathlib.Path(temp, 'bad.json')
            path.write_text('{"schema_version": 2}', encoding='utf-8')
            self.assertEqual(run('list', '--registry', str(path))[0], 2)

    def test_node_versions_are_checked_against_the_ranges(self):
        ranges = DATA['extensions'][0]['requires'][0]['ranges']
        fits = lambda v: any(ext.version_tuple(v) >= ext.version_tuple(lo) and (hi is None or ext.version_tuple(v) < ext.version_tuple(hi)) for lo, hi in ranges)
        self.assertTrue(fits('v22.22.0'))
        self.assertFalse(fits('v22.18.0'))
        self.assertFalse(fits('v23.1.0'))
        self.assertTrue(fits('v26.1.0'))


if __name__ == '__main__':
    unittest.main()
