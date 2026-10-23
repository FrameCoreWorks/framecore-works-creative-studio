"""earshot-audio launcher (scripts/runtime.py): pinned, verified installation and an allowlist of local commands. No network."""
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
spec = importlib.util.spec_from_file_location('earshot_runtime', PLUGIN / 'scripts/runtime.py')
runtime = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runtime)


def quiet(fn, *args):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = fn(*args)
    return code, out.getvalue(), err.getvalue()


class Allowlist(unittest.TestCase):
    def test_llm_and_mcp_are_refused_also_after_threads(self):
        for argv in (['llm', 'x.wav'], ['mcp'], ['--threads', '2', 'mcp'], ['--threads=2', 'llm']):
            with self.assertRaises(runtime.Refused):
                runtime.check_command(argv)
        with mock.patch.object(runtime.subprocess, 'run') as started:
            code, _, err = quiet(runtime.main, ['run', '--threads', '2', 'llm', 'film.mp4'])
        self.assertEqual(code, 2)
        self.assertIn('llm', err)
        started.assert_not_called()

    def test_unknown_command_is_refused(self):
        with mock.patch.object(runtime.subprocess, 'run') as started:
            self.assertEqual(quiet(runtime.main, ['run', 'serve'])[0], 2)
            self.assertEqual(quiet(runtime.main, ['run'])[0], 2)
        started.assert_not_called()

    def test_global_options_in_both_forms_are_skipped(self):
        self.assertEqual(runtime.real_command(['--threads=3', 'sfx', 'list']), 'sfx')
        self.assertEqual(runtime.real_command(['--threads', '3', 'measure', 'a.wav']), 'measure')
        self.assertIsNone(runtime.real_command(['--threads', '3']))

    def test_doctor_fetch_is_refused(self):
        with self.assertRaises(runtime.Refused):
            runtime.check_command(['doctor', '--fetch'])
        runtime.check_command(['doctor', '--load'])
        for name in ('measure', 'sfx', 'kit', 'forge', 'fit', 'describe', 'timeline', 'gallery'):
            runtime.check_command([name])


class Readiness(unittest.TestCase):
    def test_status_without_venv_reports_unavailable_and_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp) / 'rt'
            report = runtime.status(root)
            self.assertEqual(report['state'], 'unavailable')
            self.assertFalse(root.exists())
            code, out, _ = quiet(runtime.main, ['status', '--root', str(root), '--json'])
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(out)['state'], 'unavailable')
            self.assertFalse(root.exists())

    def test_install_without_yes_prints_plan_and_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp) / 'rt'
            with mock.patch.object(runtime.subprocess, 'run') as started:
                code, out, _ = quiet(runtime.main, ['install', '--tier', 'light', '--root', str(root)])
            self.assertEqual(code, 0)
            self.assertFalse(root.exists())
            self.assertIn(runtime.PIN['commit'], out)
            self.assertIn('--yes', out)
            started.assert_not_called()

    def test_one_changed_file_stops_install_before_any_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = pathlib.Path(tmp) / 'src'
            (src / 'earshot').mkdir(parents=True)
            (src / 'pyproject.toml').write_text('[project]\nname = "earshot"\n')
            (src / 'earshot' / '__init__.py').write_text('VERSION = "0.4.0"\n')
            manifest = {p.relative_to(src).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in src.rglob('*') if p.is_file()}
            self.assertEqual(runtime.verify_tree(src, manifest), [])
            (src / 'earshot' / '__init__.py').write_text('VERSION = "0.4.0"  # changed\n')
            self.assertEqual(runtime.verify_tree(src, manifest), ['earshot/__init__.py'])
            (src / 'extra.py').write_text('x = 1\n')
            self.assertIn('extra.py', runtime.verify_tree(src, manifest))
            root = pathlib.Path(tmp) / 'rt'
            with mock.patch.object(runtime, 'fetch_source', return_value=src), \
                    mock.patch.object(runtime, 'load_manifest', return_value={'files': manifest}), \
                    mock.patch.object(runtime.subprocess, 'run') as started:
                code, _, err = quiet(runtime.main, ['install', '--tier', 'light', '--root', str(root), '--yes'])
            self.assertEqual(code, 1)
            self.assertIn('earshot/__init__.py', err)
            self.assertFalse((root / 'venv').exists())
            started.assert_not_called()

    def test_light_install_does_not_print_a_false_dependency_error(self):
        # 2026-10-22 container run: pip printed "ERROR ... requires torch" on a correct light install.
        with tempfile.TemporaryDirectory() as tmp:
            src = pathlib.Path(tmp) / 'src'
            src.mkdir()
            (src / 'pyproject.toml').write_text('x')
            manifest = {'pyproject.toml': hashlib.sha256(b'x').hexdigest()}
            root = pathlib.Path(tmp) / 'rt'
            with mock.patch.object(runtime, 'fetch_source', return_value=src), \
                    mock.patch.object(runtime, 'load_manifest', return_value={'files': manifest}), \
                    mock.patch.object(runtime, 'venv_python', return_value=pathlib.Path('/venv/bin/python')), \
                    mock.patch.object(runtime, 'status', return_value={}), \
                    mock.patch.object(runtime, 'engine_package', return_value=pathlib.Path(tmp)), \
                    mock.patch.object(runtime.subprocess, 'run') as started:
                self.assertEqual(quiet(runtime.main, ['install', '--tier', 'light', '--root', str(root), '--yes'])[0], 0)
            pip_calls = [c.args[0] for c in started.call_args_list if 'pip' in c.args[0]]
            self.assertTrue(pip_calls)
            for call in pip_calls:
                self.assertIn('--no-warn-conflicts', call)
            self.assertFalse(any('torch' in ' '.join(call) for call in pip_calls))

    def test_a_failed_download_is_one_line_not_a_traceback(self):
        # 2026-10-22 container run: the CPU PyTorch index was unreachable and install ended in a traceback.
        with tempfile.TemporaryDirectory() as tmp:
            src = pathlib.Path(tmp) / 'src'
            src.mkdir()
            (src / 'pyproject.toml').write_text('x')
            manifest = {'pyproject.toml': hashlib.sha256(b'x').hexdigest()}
            failing = runtime.subprocess.CalledProcessError(1, ['pip', 'install', 'torch>=2.6'])
            with mock.patch.object(runtime, 'fetch_source', return_value=src), \
                    mock.patch.object(runtime, 'load_manifest', return_value={'files': manifest}), \
                    mock.patch.object(runtime, 'venv_python', return_value=pathlib.Path('/venv/bin/python')), \
                    mock.patch.object(runtime.subprocess, 'run', side_effect=[None, None, None, failing]):
                code, _, err = quiet(runtime.main, ['install', '--tier', 'full', '--root', str(pathlib.Path(tmp) / 'rt'), '--yes'])
            self.assertEqual(code, 1)
            self.assertNotIn('Traceback', err)
            self.assertIn('torch', err)
            self.assertEqual(len(err.strip().splitlines()), 1)

    def test_fetch_models_needs_the_full_tier_first(self):
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(runtime, 'venv_python', return_value=pathlib.Path('/venv/bin/python')), \
                    mock.patch.object(runtime, 'status', return_value={'full_ready': False}), \
                    mock.patch.object(runtime.subprocess, 'run') as started:
                code, _, err = quiet(runtime.main, ['fetch-models', '--root', tmp, '--yes'])
            self.assertEqual(code, 1)
            self.assertIn('--tier full', err)
            started.assert_not_called()

    def test_status_does_not_trust_an_engine_it_cannot_identify(self):
        # Final review I4: a venv from the old 0.3 registry route has no engine.json yet imports fine.
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            with mock.patch.object(runtime, 'venv_python', return_value=pathlib.Path('/venv/bin/python')), \
                    mock.patch.object(runtime, '_python_ok', return_value=True):
                report = runtime.status(root)
                self.assertEqual(report['state'], 'unavailable')
                self.assertIn('reinstall', report['note'])
                (root / 'engine.json').write_text('{not json')
                self.assertEqual(runtime.status(root)['state'], 'unavailable')
                (root / 'engine.json').write_text(json.dumps({**runtime.PIN, 'tier': 'light'}))
                self.assertEqual(runtime.status(root)['state'], 'ready_light')

    def test_exec_applies_the_offline_cache_and_checks_earshot_commands(self):
        # Final review I2: scripts run with the bare venv interpreter missed EARSHOT_HOME and the offline flags.
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            with mock.patch.object(runtime, 'venv_python', return_value=pathlib.Path('/venv/bin/python')), \
                    mock.patch.object(runtime.subprocess, 'run', return_value=mock.Mock(returncode=0)) as started, \
                    mock.patch.dict(runtime.os.environ, {'GEMINI_API_KEY': 'x', 'GOOGLE_API_KEY': 'y'}):
                self.assertEqual(quiet(runtime.main, ['--root', tmp, 'exec', '-I', 'my_analysis.py', 'a.wav'])[0], 0)
                command, env = started.call_args.args[0], started.call_args.kwargs['env']
                self.assertEqual(command, ['/venv/bin/python', '-I', 'my_analysis.py', 'a.wav'])
                self.assertEqual(env['EARSHOT_HOME'], str(root / 'cache'))
                self.assertEqual(env['EARSHOT_OFFLINE'], '1')
                self.assertNotIn('GEMINI_API_KEY', env)
                self.assertNotIn('GOOGLE_API_KEY', env)
                started.reset_mock()
                self.assertEqual(quiet(runtime.main, ['--root', tmp, 'exec', '-m', 'earshot', '--threads', '2', 'llm', 'a.wav'])[0], 2)
                self.assertEqual(quiet(runtime.main, ['--root', tmp, 'exec', '-m', 'earshot.mcp_server'])[0], 2)
                started.assert_not_called()

    def test_install_removes_the_upload_and_server_modules_from_the_engine(self):
        # Final review I3: the CLI allowlist alone left api.llm_critique and the MCP server importable.
        with tempfile.TemporaryDirectory() as tmp:
            package = pathlib.Path(tmp) / 'site' / 'earshot'
            package.mkdir(parents=True)
            for name in ('llm.py', 'mcp_server.py', 'api.py'):
                (package / name).write_text('real = True\n')
            runtime.disable_remote_modules(package)
            for name in ('llm.py', 'mcp_server.py'):
                self.assertIn('earshot-audio', (package / name).read_text())
                self.assertIn('raise ImportError', (package / name).read_text())
            self.assertEqual((package / 'api.py').read_text(), 'real = True\n')

    def test_venv_python_on_windows_layout(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            exe = root / 'venv' / 'Scripts' / 'python.exe'
            exe.parent.mkdir(parents=True)
            exe.write_bytes(b'')
            self.assertEqual(runtime.venv_python(root), exe)
            posix = root / 'venv' / 'bin' / 'python'
            posix.parent.mkdir(parents=True)
            posix.write_bytes(b'')
            self.assertEqual(runtime.venv_python(root), posix)

    def test_real_sound_scripts_stay_inside_their_folder(self):
        with self.assertRaises(runtime.Refused):
            runtime.real_sound_script('../../scripts/runtime.py')
        with self.assertRaises(runtime.Refused):
            runtime.real_sound_script('/etc/passwd')


class RemoteStub(unittest.TestCase):
    def test_a_missing_engine_package_fails_the_install_instead_of_skipping_the_stub(self):
        # Review 2026-10-23: the upload stub must be applied or the install fails; it is never skipped silently.
        with self.assertRaises(OSError):
            runtime.disable_remote_modules(None)
        with tempfile.TemporaryDirectory() as d:
            pkg = pathlib.Path(d)
            (pkg / 'llm.py').write_text('upload')
            runtime.disable_remote_modules(pkg)
            self.assertIn('Removed by earshot-audio', (pkg / 'llm.py').read_text())
            self.assertIn('Removed by earshot-audio', (pkg / 'mcp_server.py').read_text())


if __name__ == '__main__':
    unittest.main()
