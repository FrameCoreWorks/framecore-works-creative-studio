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


def write_json(path, data):
    path.write_text(json.dumps(data), encoding='utf-8')
    return path


class Formats(unittest.TestCase):
    def setUp(self):
        import formats
        self.f = formats
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = pathlib.Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_whole_words_only(self):
        lex = {'Core': 'kor'}
        self.assertEqual(self.f.apply_lexicon('Core value', lex), 'kor value')
        self.assertEqual(self.f.apply_lexicon('Hardcore fans', lex), 'Hardcore fans')

    def test_case_insensitive_longest_first(self):
        lex = {'Core': 'kor', 'FrameCore': 'frejm kor'}
        self.assertEqual(self.f.apply_lexicon('framecore wins', lex), 'frejm kor wins')

    def test_voice_description_kept(self):
        lex = {'FrameCore': 'frejm kor', 'calm': 'X'}
        self.assertEqual(self.f.apply_lexicon('(calm male voice)FrameCore', lex), '(calm male voice)frejm kor')

    def test_duplicate_id_named(self):
        path = write_json(self.dir / 'cues.json', [{'id': 'a1', 'text': 'x', 'max_seconds': 2},
                                                   {'id': 'a1', 'text': 'y', 'max_seconds': 2}])
        with self.assertRaises(self.f.CueError) as caught:
            self.f.load_cues(path)
        self.assertIn('a1', str(caught.exception))

    def test_missing_max_seconds_named(self):
        for bad in ({'id': 'b2', 'text': 'x'}, {'id': 'b2', 'text': 'x', 'max_seconds': 0}):
            path = write_json(self.dir / 'cues.json', [bad])
            with self.assertRaises(self.f.CueError) as caught:
                self.f.load_cues(path)
            self.assertIn('b2', str(caught.exception))

    def test_empty_text_named(self):
        path = write_json(self.dir / 'cues.json', [{'id': 'c3', 'text': '  ', 'max_seconds': 1}])
        with self.assertRaises(self.f.CueError) as caught:
            self.f.load_cues(path)
        self.assertIn('c3', str(caught.exception))

    def test_cues_load(self):
        path = write_json(self.dir / 'cues.json', [{'id': 'a', 'text': 'Hi', 'max_seconds': 1.5, 'voice_notes': 'warm'}])
        cue = self.f.load_cues(path)[0]
        self.assertEqual((cue.id, cue.text, cue.max_seconds, cue.voice_notes), ('a', 'Hi', 1.5, 'warm'))

    def test_lock_roundtrip_keeps_other_lines(self):
        lock = self.f.Lock.load(self.dir)
        lock.set_line('a', engine='voxcpm', status='ok')
        lock.save()
        lock = self.f.Lock.load(self.dir)
        lock.set_line('b', engine='voicebox', status='failed', error='boom')
        lock.save()
        data = json.loads((self.dir / 'narration.lock.json').read_text(encoding='utf-8'))
        self.assertEqual(data['version'], 1)
        self.assertEqual(data['lines']['a']['engine'], 'voxcpm')
        self.assertEqual(data['lines']['b']['error'], 'boom')

    def test_lexicon_hash_recorded(self):
        import hashlib
        path = write_json(self.dir / 'lexicon.json', {'FrameCore': 'frejm kor'})
        entries, digest = self.f.load_lexicon(path)
        self.assertEqual(entries, {'FrameCore': 'frejm kor'})
        self.assertEqual(digest, hashlib.sha256(path.read_bytes()).hexdigest())
        self.assertEqual(self.f.load_lexicon(None), ({}, None))
        lock = self.f.Lock.load(self.dir)
        lock.lexicon_sha256 = digest
        lock.save()
        self.assertEqual(self.f.Lock.load(self.dir).lexicon_sha256, digest)


if __name__ == '__main__':
    unittest.main()
