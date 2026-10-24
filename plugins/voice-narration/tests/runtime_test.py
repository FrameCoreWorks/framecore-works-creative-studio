"""voice-narration launcher (scripts/runtime.py) and its modules. No network, no engine."""
import contextlib
import importlib.util
import io
import json
import pathlib
import sys
import tempfile
import unittest
from unittest import mock

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PLUGIN / 'scripts'))
spec = importlib.util.spec_from_file_location('narration_runtime', PLUGIN / 'scripts/runtime.py')
runtime = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runtime)


def quiet(fn, *args):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = fn(*args)
    return code, out.getvalue(), err.getvalue()


class Environment(unittest.TestCase):
    def test_cloud_markers(self):
        for env in ({'CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE': 'cloud_default'}, {'CLAUDE_CODE_REMOTE': 'true'},
                    {'CODEX_SANDBOX': 'seatbelt'}, {'CODEX_CLOUD': '1'}):
            self.assertEqual(runtime.detect_environment(env), 'cloud', env)
        self.assertEqual(runtime.detect_environment({}), 'local')
        self.assertEqual(runtime.detect_environment({'CLAUDE_CODE_REMOTE': 'false'}), 'local')

    def test_default_root_env_override(self):
        self.assertEqual(runtime.default_root({'VOICE_NARRATION_ROOT': '/x/y'}), pathlib.Path('/x/y'))
        self.assertEqual(runtime.default_root({}).parts[-3:], ('.framecore-studio', 'extensions', 'voxcpm'))

    def test_venv_python_windows_layout(self):
        root = pathlib.Path('/r')
        with mock.patch.object(runtime.os, 'name', 'nt'):
            self.assertEqual(runtime.venv_python(root), root / 'venv' / 'Scripts' / 'python.exe')
        with mock.patch.object(runtime.os, 'name', 'posix'):
            self.assertEqual(runtime.venv_python(root), root / 'venv' / 'bin' / 'python')


class Commands(unittest.TestCase):
    def test_unknown_command_refused(self):
        with mock.patch.object(runtime.subprocess, 'run') as run:
            code, _, err = quiet(runtime.main, ['mcp'])
        self.assertEqual(code, 2)
        self.assertIn('refused: mcp is not a voice-narration command', err)
        run.assert_not_called()

    def test_status_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp) / 'root'
            with mock.patch.object(runtime, 'probe_voicebox', return_value=False):
                code, out, _ = quiet(runtime.main, ['status', '--json', '--root', str(root)])
            self.assertEqual(code, 0)
            self.assertFalse(root.exists())
            data = json.loads(out)
            self.assertEqual(data['voxcpm_version'], 'unavailable')
            self.assertEqual(data['voicebox'], 'unavailable')
            self.assertFalse(data['weights_cached'])
            for key in ('environment', 'python', 'venv', 'ffmpeg', 'ffprobe', 'gpu'):
                self.assertIn(key, data)


if __name__ == '__main__':
    unittest.main()
