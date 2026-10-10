"""Tests for skills/workflow-orchestrator/assets/environment-check: the tool list, statuses, capabilities and install steps."""
import importlib.util
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
FOLDER = PLUGIN / 'skills/workflow-orchestrator/assets/environment-check'
TOOL = FOLDER / 'check_environment.py'
SPEC = json.loads((FOLDER / 'tools.json').read_text(encoding='utf-8'))
CARD = json.loads((PLUGIN / 'skills/workflow-orchestrator/assets/capability-card.json').read_text(encoding='utf-8'))

spec = importlib.util.spec_from_file_location('check_environment', TOOL)
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)


def fake_program(folder, name, output):
    path = pathlib.Path(folder, name)
    path.write_text(f'#!/bin/sh\necho "{output}"\n')
    path.chmod(0o755)


def run_check(*args, path='', home=None, project=None):
    """Run the check in a clean environment: only the given PATH, a temporary HOME, no browser variables."""
    with tempfile.TemporaryDirectory() as temp:
        env = {'PATH': path, 'HOME': home or temp, 'PYTHONDONTWRITEBYTECODE': '1', 'SYSTEMROOT': os.environ.get('SYSTEMROOT', '')}
        # A fixed host keeps the result independent of the machine running the test (a /mnt/user-data folder, for example).
        host = [] if '--host' in args else ['--host', 'codex']
        done = subprocess.run([sys.executable, str(TOOL), '--json', '--project', project or temp, *host, *args], capture_output=True, text=True, env=env, timeout=120)
        return done.returncode, json.loads(done.stdout), sorted(os.listdir(temp))


def by_id(items):
    return {item['id']: item for item in items}


class ToolList(unittest.TestCase):
    def test_every_tool_maps_to_the_capability_card(self):
        values, capabilities = set(CARD['requirement_values']), {item['id'] for item in CARD['capabilities']}
        for tool in SPEC['tools']:
            self.assertNotIn('optional', tool, 'every tool belongs to the one required set')
            self.assertTrue(tool.get('requirement') in values or tool.get('capability') in capabilities or tool.get('pinned_by') or tool.get('used_by'), tool['id'])
            if tool.get('used_by'):
                self.assertTrue((PLUGIN / tool['used_by']).is_file(), tool['used_by'])
            if tool.get('capability'):
                self.assertIn(tool['capability'], capabilities)
            if tool.get('pinned_by'):
                self.assertTrue((PLUGIN / tool['pinned_by']).is_file(), tool['pinned_by'])
            self.assertTrue(tool['install'].get('any') or all(tool['install'].get(s) for s in ('linux', 'macos', 'windows')), tool['id'])

    def test_every_checkable_requirement_has_a_required_or_optional_tool(self):
        covered = {tool.get('requirement') for tool in SPEC['tools']}
        for need in ('python', 'pillow', 'numpy', 'cairosvg', 'ffmpeg', 'node', 'browser'):
            self.assertIn(need, covered)

    def test_versions_are_read_and_compared(self):
        self.assertEqual(check.version_of('v22.22.0'), '22.22.0')
        self.assertEqual(check.version_of('ffmpeg version 6.1.1-3ubuntu5 Copyright'), '6.1.1')
        self.assertEqual(check.version_of('Chromium 141.0.7390.37 '), '141.0.7390.37')
        self.assertTrue(check.older('3.13.16', '3.14.8'))
        self.assertFalse(check.older('24.21.0', '20'))
        self.assertFalse(check.older('unknown', None))


@unittest.skipIf(os.name == 'nt', 'uses shell scripts as stand-in programs')
class Environment(unittest.TestCase):
    def test_empty_path_reports_missing_tools_and_what_studio_delivers_instead(self):
        code, report, created = run_check()
        tools, capabilities = by_id(report['tools']), by_id(report['capabilities'])
        self.assertEqual(code, 0)
        self.assertEqual(tools['node']['status'], 'missing')
        self.assertEqual(tools['browser']['status'], 'missing')
        self.assertEqual(tools['hyperframes']['status'], 'missing')
        self.assertEqual(tools['remotion']['status'], 'missing', 'the Studio workspace is part of the required set')
        self.assertEqual(report['final']['verdict'], 'fail')
        self.assertEqual(capabilities['motion_frame_review']['status'], 'missing')
        self.assertTrue(capabilities['motion_frame_review']['when_missing'])
        self.assertIn('node', {step['id'] for step in report['install']})
        self.assertTrue(report['installs_nothing'])
        self.assertEqual(created, [], 'the check must not create files')

    def test_strict_and_final_fail_when_the_required_set_is_incomplete(self):
        self.assertEqual(run_check('--strict')[0], 1)
        code, report, _ = run_check('--final')
        self.assertEqual((code, report['final']['verdict']), (1, 'fail'))
        self.assertIn('hyperframes', {f['id'] for f in report['final']['failing']})

    def test_versions_against_minimum_and_newest(self):
        with tempfile.TemporaryDirectory() as bin_dir:
            fake_program(bin_dir, 'node', 'v18.0.0')
            fake_program(bin_dir, 'ffmpeg', 'ffmpeg version 9.0.2 Copyright')
            fake_program(bin_dir, 'ffprobe', 'ffprobe version 9.0.2 Copyright')
            fake_program(bin_dir, 'chromium', 'Chromium 120.0.6099.0')
            _, report, _ = run_check(path=bin_dir)
        tools, steps = by_id(report['tools']), by_id(report['install'])
        self.assertEqual((tools['node']['status'], tools['node']['version']), ('below_minimum', '18.0.0'))
        self.assertEqual(tools['ffmpeg']['status'], 'ok')
        self.assertEqual(tools['browser']['status'], 'behind')
        self.assertIsNone(tools['browser']['note'], 'a browser on PATH is found by Studio\'s tools too')
        self.assertEqual((steps['node']['action'], steps['node']['below']), ('update', True))
        self.assertIn('hyperframes_engine', {c['id'] for c in report['capabilities'] if 'node>=22' in c['missing']})

    def test_workspace_starters_and_hyperframes_skills(self):
        def install(workspace, tool_id, change=None):
            tool = by_id(SPEC['tools'])[tool_id]
            manifest = json.loads((PLUGIN / tool['pinned_by']).read_text())
            pathlib.Path(workspace, tool['workspace_name']).mkdir(parents=True, exist_ok=True)
            lock = (PLUGIN / tool['pinned_by'].replace('package.json', 'package-lock.json')).read_bytes()
            pathlib.Path(workspace, tool['workspace_name'], 'package-lock.json').write_bytes(lock + (b' ' if change == 'stale' else b''))
            for name, version in {**manifest.get('dependencies', {}), **manifest.get('devDependencies', {})}.items():
                folder = pathlib.Path(workspace, tool['workspace_name'], 'node_modules', name)
                folder.mkdir(parents=True)
                (folder / 'package.json').write_text(json.dumps({'name': name, 'version': change.get(name, version) if isinstance(change, dict) else version}))
        with tempfile.TemporaryDirectory() as project, tempfile.TemporaryDirectory() as workspace:
            install(workspace, 'remotion')
            install(workspace, 'gsap', {'gsap': '3.12.0'})
            install(workspace, 'remotion_three', 'stale')
            skill = pathlib.Path(project, '.agents/skills/hyperframes')
            skill.mkdir(parents=True)
            (skill / 'SKILL.md').write_text('---\nname: hyperframes\n---\n')
            _, report, _ = run_check('--workspace', workspace, project=project)
        tools = by_id(report['tools'])
        self.assertEqual((tools['remotion']['status'], tools['remotion']['pinned']['remotion']), ('ok', '4.0.530'))
        self.assertEqual(tools['gsap']['status'], 'wrong_version')
        self.assertIn('gsap 3.12.0 (lockfile 3.15.0)', tools['gsap']['note'])
        self.assertEqual(tools['motion_toolkit']['status'], 'missing')
        self.assertEqual(tools['remotion_three']['status'], 'wrong_version', 'a workspace installed from an older plugin version is stale')
        self.assertIn('lockfile changed', tools['remotion_three']['note'])
        self.assertEqual(tools['hyperframes']['status'], 'ok')
        self.assertTrue(tools['hyperframes']['skills'][0].endswith('hyperframes'))
        commands = by_id(report['install'])
        self.assertIn('npm ci', commands['motion_toolkit']['command'])
        self.assertNotIn('<plugin>', commands['motion_toolkit']['command'], 'the command names the real plugin folder')
        self.assertIn('rm -rf', commands['remotion_three']['command'], 'a stale copy is replaced, not nested')
        self.assertIn(workspace, commands['remotion_three']['command'])


class FinalCheck(unittest.TestCase):
    def results(self, **statuses):
        return [{'id': tool, 'status': status} for tool, status in statuses.items()]

    def test_verdicts(self):
        self.assertEqual(check.final_verdict(self.results(python='ok', ffmpeg='behind'), 'codex', 'shell')['verdict'], 'pass')
        self.assertEqual(check.final_verdict(self.results(python='ok', manim='missing'), 'claude_code', 'shell')['verdict'], 'fail')
        self.assertEqual(check.final_verdict(self.results(gsap='wrong_version'), 'codex', 'shell')['verdict'], 'fail')
        limited = check.final_verdict(self.results(python='ok', cairosvg='missing', remotion='not_on_this_host'), 'chatgpt_work', 'code_execution')
        self.assertEqual((limited['verdict'], limited['not_on_this_host']), ('limited', ['remotion']))
        self.assertEqual(check.final_verdict(self.results(remotion='not_on_this_host'), 'chatgpt', 'code_execution')['verdict'], 'pass')
        self.assertEqual(check.final_verdict(self.results(python='ok'), None, None)['verdict'], 'unknown_host')

    def test_update_verdict_lists_newer_versions(self):
        results = [{'id': 'python', 'status': 'ok'}, {'id': 'node', 'status': 'behind', 'version': '22.22.0', 'latest': '24.21.0'}]
        verdict = check.final_verdict(results, 'codex', 'shell', update=True)
        self.assertEqual((verdict['verdict'], verdict['updates'][0]['id']), ('pass_with_updates', 'node'))
        self.assertEqual(check.final_verdict(results, 'codex', 'shell')['verdict'], 'pass', 'the installation check does not require the newest versions')
        stale = check.final_verdict(results + [{'id': 'gsap', 'status': 'wrong_version'}], 'codex', 'shell', update=True)
        self.assertEqual(stale['verdict'], 'fail')

    def test_update_exit_codes(self):
        with mock.patch.object(check, 'report', return_value={'final': {'verdict': 'pass_with_updates'}, 'tools': []}), mock.patch.object(check, 'text', return_value=''), mock.patch('builtins.print'):
            self.assertEqual(check.main(['--update', '--host', 'codex']), 4)


class Hosts(unittest.TestCase):
    def test_every_tool_has_a_status_for_every_host(self):
        hosts = [h['id'] for h in SPEC['hosts']]
        self.assertEqual(sorted(hosts), ['chatgpt', 'chatgpt_work', 'claude_apps', 'claude_code', 'codex'])
        for tool in SPEC['tools']:
            self.assertEqual(sorted(tool['hosts']), sorted(hosts), tool['id'])
            for host, entry in tool['hosts'].items():
                self.assertIn(entry['status'], SPEC['host_statuses'])
                if entry['status'] in ('observed', 'not_supported'):
                    self.assertTrue(entry.get('note'), f"{tool['id']} on {host}")

    def test_readme_table_is_the_generated_matrix(self):
        readme = (FOLDER / 'README.md').read_text(encoding='utf-8')
        table = readme.split('<!-- BEGIN HOST MATRIX -->\n', 1)[1].split('\n<!-- END HOST MATRIX -->', 1)[0]
        self.assertEqual(table, check.matrix(SPEC, markdown=True))

    def test_named_host_marks_unsupported_tools_as_not_on_this_host(self):
        # A temporary HOME and project keep skills installed on the machine running the test out of the result.
        with tempfile.TemporaryDirectory() as temp, mock.patch.dict(os.environ, {'HOME': temp, 'CODEX_HOME': temp, 'XDG_CONFIG_HOME': temp}):
            args = check.argparse.Namespace(online=False, project=temp, browser=None, host='chatgpt', workspace=temp)
            with mock.patch.object(check.urllib.request, 'urlopen', side_effect=AssertionError('network used')):
                data = check.report(args)
        tools = by_id(data['tools'])
        self.assertEqual(data['host'], 'chatgpt')
        self.assertEqual(tools['remotion']['status'], 'not_on_this_host')
        self.assertEqual(tools['ffmpeg']['on_host']['status'], 'observed')
        self.assertIn('hyperframes', by_id(data['capabilities'])['hyperframes_engine']['missing'])

    def test_studio_own_hyperframes_workflow_skill_is_not_hyperframes(self):
        with tempfile.TemporaryDirectory() as home, tempfile.TemporaryDirectory() as project:
            for root in (pathlib.Path(home, '.agents/skills'), pathlib.Path(project, '.codex/skills')):
                (root / 'hyperframes-workflow').mkdir(parents=True)
                (root / 'hyperframes-workflow/SKILL.md').write_text('---\nname: hyperframes-workflow\n---\n')
            plugin = pathlib.Path(home, '.codex/plugins/cache/framecore-work-creative-studio/skills/hyperframes-workflow')
            plugin.mkdir(parents=True)
            _, report, _ = run_check(home=home, project=project)
            self.assertEqual(by_id(report['tools'])['hyperframes']['status'], 'missing', "Studio's own skill is not HyperFrames")
            real = pathlib.Path(home, '.agents/skills/hyperframes')
            real.mkdir()
            (real / 'SKILL.md').write_text('---\nname: hyperframes\n---\n')
            _, report, _ = run_check(home=home, project=project)
            tool = by_id(report['tools'])['hyperframes']
            self.assertEqual((tool['status'], tool['skills']), ('ok', [str(real)]))

    def test_host_is_detected_from_documented_traces(self):
        with mock.patch.dict(check.os.environ, {'CLAUDECODE': '1'}, clear=True):
            self.assertEqual(check.detect_host(SPEC)[0], 'claude_code')
        with mock.patch.dict(check.os.environ, {'CODEX_HOME': '/x'}, clear=True):
            self.assertEqual(check.detect_host(SPEC)[0], 'codex')


class Network(unittest.TestCase):
    def args(self, online):
        return check.argparse.Namespace(online=online, project='.', browser=None, host='auto', workspace=tempfile.gettempdir())

    def test_offline_never_opens_a_connection(self):
        with mock.patch.object(check.urllib.request, 'urlopen', side_effect=AssertionError('network used')):
            data = check.report(self.args(False))
        self.assertEqual(data['latest_from'], 'snapshot of ' + SPEC['checked'])
        self.assertIsNone(data['requirements']['network'])

    def test_failed_online_lookup_keeps_the_snapshot_and_says_so(self):
        with mock.patch.object(check.urllib.request, 'urlopen', side_effect=OSError('offline')):
            data = check.report(self.args(True))
        self.assertIn('online lookup failed', data['latest_from'])
        self.assertIs(data['requirements']['network'], False)
        self.assertEqual(by_id(data['tools'])['numpy']['latest'], by_id(SPEC['tools'])['numpy']['known_latest'])


if __name__ == '__main__':
    unittest.main()
