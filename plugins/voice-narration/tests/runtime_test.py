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


def write_wav(path, tone_seconds, silence_seconds=0.0, rate=24000, amplitude=12000, channels=1):
    import array
    import math
    import wave
    frames = array.array('h')
    for i in range(int(tone_seconds * rate)):
        value = int(amplitude * math.sin(2 * math.pi * 440 * i / rate))
        frames.extend([value] * channels)
    frames.extend([0] * int(silence_seconds * rate) * channels)
    with wave.open(str(path), 'wb') as out:
        out.setnchannels(channels)
        out.setsampwidth(2)
        out.setframerate(rate)
        out.writeframes(frames.tobytes())
    return path


class Measure(unittest.TestCase):
    def setUp(self):
        import audio
        self.a = audio
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = pathlib.Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def cues(self, *lines):
        return write_json(self.dir / 'cues.json', [{'id': i, 'text': 'x', 'max_seconds': m} for i, m in lines])

    def test_trailing_silence_excluded(self):
        path = write_wav(self.dir / 'a.wav', 1.0, 0.5)
        self.assertAlmostEqual(self.a.spoken_duration(path), 1.0, delta=0.02)
        stereo = write_wav(self.dir / 's.wav', 0.5, 0.5, channels=2)
        self.assertAlmostEqual(self.a.spoken_duration(stereo), 0.5, delta=0.02)

    def test_all_silence_is_silent(self):
        path = write_wav(self.dir / 'a.wav', 0.0, 1.0)
        self.assertEqual(self.a.spoken_duration(path), 0.0)
        self.assertEqual(self.a.verdict(0.0, 2.0), 'silent')

    def test_over_by(self):
        write_wav(self.dir / 'a.wav', 2.4)
        write_wav(self.dir / 'b.wav', 1.0)
        import formats
        rows = {r['id']: r for r in self.a.measure_all(formats.load_cues(self.cues(('a', 2.0), ('b', 2.0))), self.dir)}
        self.assertEqual(rows['a']['verdict'], 'over')
        self.assertAlmostEqual(rows['a']['over_by'], 0.4, delta=0.02)
        self.assertEqual(rows['b']['verdict'], 'fits')

    def test_missing_file_reported(self):
        code, out, _ = quiet(runtime.main, ['measure', '--cues', str(self.cues(('a', 2.0))), '--out', str(self.dir), '--json'])
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(out)[0]['verdict'], 'missing')

    def test_measure_updates_lock(self):
        write_wav(self.dir / 'a.wav', 1.0)
        code, _, _ = quiet(runtime.main, ['measure', '--cues', str(self.cues(('a', 2.0))), '--out', str(self.dir)])
        self.assertEqual(code, 0)
        line = json.loads((self.dir / 'narration.lock.json').read_text())['lines']['a']
        self.assertEqual(line['verdict'], 'fits')
        self.assertEqual(line['max_seconds'], 2.0)

    def test_8bit_wav_rejected(self):
        import wave
        path = self.dir / 'a.wav'
        with wave.open(str(path), 'wb') as out:
            out.setnchannels(1); out.setsampwidth(1); out.setframerate(8000); out.writeframes(bytes(800))
        with self.assertRaises(self.a.AudioError):
            self.a.spoken_duration(path)

    def stretch(self, *extra):
        write_wav(self.dir / 'a.wav', 1.0)
        return quiet(runtime.main, ['stretch', 'a', '--cues', str(self.cues(('a', 0.9))), '--out', str(self.dir), *extra])

    def test_stretch_limit_refused(self):
        for percent in ('6', '0', '-1'):
            code, _, err = self.stretch('--percent', percent, '--yes')
            self.assertEqual(code, 2, percent)
        self.assertFalse((self.dir / 'a.stretched.wav').exists())

    def test_stretch_without_yes_writes_nothing(self):
        with mock.patch.object(runtime.subprocess, 'run') as run:
            code, out, _ = self.stretch('--percent', '4')
        self.assertEqual(code, 0)
        self.assertIn('--yes', out)
        run.assert_not_called()
        self.assertFalse((self.dir / 'narration.lock.json').exists())

    def test_stretch_without_ffmpeg_one_line(self):
        with mock.patch.object(runtime.shutil, 'which', return_value=None):
            code, _, err = self.stretch('--percent', '4', '--yes')
        self.assertEqual(code, 1)
        self.assertEqual(len(err.strip().splitlines()), 1)
        self.assertIn('FFmpeg', err)

    def test_stretch_records_percent(self):
        def fake_run(argv, **kwargs):
            write_wav(pathlib.Path(argv[-1]), 0.97)
            return mock.Mock(returncode=0)
        with mock.patch.object(runtime.shutil, 'which', return_value='/usr/bin/ffmpeg'), \
                mock.patch.object(runtime.subprocess, 'run', side_effect=fake_run) as run:
            code, _, _ = self.stretch('--percent', '3', '--yes')
        self.assertEqual(code, 0)
        self.assertIn('atempo=1.03', ' '.join(run.call_args[0][0]))
        line = json.loads((self.dir / 'narration.lock.json').read_text())['lines']['a']
        self.assertEqual(line['stretch_percent'], 3.0)
        self.assertTrue(line['wav'].endswith('a.stretched.wav'))


CLOUD = {'CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE': 'cloud_default'}


class Install(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name) / 'root'

    def tearDown(self):
        self.tmp.cleanup()

    def run_main(self, argv, env=None):
        return quiet(runtime.main, argv + ['--root', str(self.root)], env or {})

    def test_install_plan_writes_nothing(self):
        with mock.patch.object(runtime.subprocess, 'run') as run:
            code, out, _ = self.run_main(['install', 'voxcpm'])
        self.assertEqual(code, 0)
        self.assertIn('voxcpm==2.0.3', out)
        self.assertIn('--yes', out)
        self.assertFalse(self.root.exists())
        run.assert_not_called()

    def test_cloud_plan_leads_with_warning(self):
        code, out, _ = self.run_main(['install', 'voxcpm'], CLOUD)
        self.assertEqual(code, 0)
        self.assertTrue(out.startswith('warning: this is a cloud environment'))

    def test_cloud_install_refused_without_allow_cloud(self):
        for argv in (['install', 'voxcpm', '--yes'], ['fetch-models', '--yes']):
            with mock.patch.object(runtime.subprocess, 'run') as run:
                code, _, err = self.run_main(argv, CLOUD)
            self.assertEqual(code, 2, argv)
            self.assertIn('--allow-cloud', err)
            run.assert_not_called()
            self.assertFalse(self.root.exists())

    def test_install_runs_pinned_pip(self):
        with mock.patch.object(runtime.subprocess, 'run', return_value=mock.Mock(returncode=0, stdout='', stderr='')) as run, \
                mock.patch.object(runtime, 'voxcpm_version', return_value='2.0.3'):
            code, _, _ = self.run_main(['install', 'voxcpm', '--yes'])
        self.assertEqual(code, 0)
        calls = [c[0][0] for c in run.call_args_list]
        self.assertEqual(calls[0][1:3], ['-m', 'venv'])
        self.assertEqual(calls[-1][-2:], ['voxcpm==2.0.3', 'soundfile'])

    def test_install_allowed_in_cloud_with_flag(self):
        with mock.patch.object(runtime.subprocess, 'run', return_value=mock.Mock(returncode=0, stdout='', stderr='')), \
                mock.patch.object(runtime, 'voxcpm_version', return_value='2.0.3'):
            code, _, _ = self.run_main(['install', 'voxcpm', '--yes', '--allow-cloud'], CLOUD)
        self.assertEqual(code, 0)

    def test_failed_pip_is_one_line(self):
        error = runtime.subprocess.CalledProcessError(1, ['pip'], stderr='ERROR: No matching distribution\n')
        with mock.patch.object(runtime.subprocess, 'run', side_effect=[mock.Mock(returncode=0), error]):
            code, _, err = self.run_main(['install', 'voxcpm', '--yes'])
        self.assertEqual(code, 1)
        self.assertEqual(len(err.strip().splitlines()), 1)

    def test_fetch_models_needs_install_first(self):
        with mock.patch.object(runtime.subprocess, 'run') as run:
            code, _, err = self.run_main(['fetch-models', '--yes'])
        self.assertEqual(code, 1)
        self.assertIn('install voxcpm --yes', err)
        run.assert_not_called()

    def test_fetch_models_plan_and_run(self):
        code, out, _ = self.run_main(['fetch-models'])
        self.assertEqual(code, 0)
        self.assertIn('huggingface.co', out)
        python = runtime.venv_python(self.root)
        python.parent.mkdir(parents=True)
        python.touch()
        with mock.patch.object(runtime.subprocess, 'run', return_value=mock.Mock(returncode=0)) as run:
            code, _, _ = self.run_main(['fetch-models', '--yes'])
        self.assertEqual(code, 0)
        argv, kwargs = run.call_args[0][0], run.call_args[1]
        self.assertIn("snapshot_download('openbmb/VoxCPM2')", argv[-1])
        self.assertEqual(kwargs['env']['HF_HOME'], str(self.root / 'hf-cache'))


if __name__ == '__main__':
    unittest.main()
