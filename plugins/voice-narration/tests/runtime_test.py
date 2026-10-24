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
        with mock.patch.object(runtime.subprocess, 'run') as run, \
                mock.patch.object(runtime.shutil, 'which', return_value='/usr/bin/ffmpeg'):
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
        self.assertEqual(line['wav'], 'a.stretched.wav')


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


def wav_bytes(seconds):
    with tempfile.TemporaryDirectory() as tmp:
        return write_wav(pathlib.Path(tmp) / 'x.wav', seconds).read_bytes()


class FakeVoicebox:
    """A local stand-in for Voicebox's REST API: POST /generate, SSE status, GET /audio/{id}."""

    def __init__(self, fail_texts=(), body=None):
        import http.server
        import threading
        fake = self
        self.requests = []

        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def send(self, code, body, kind):
                self.send_response(code)
                self.send_header('Content-Type', kind)
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def do_GET(self):
                if self.path == '/health':
                    return self.send(200, b'{}', 'application/json')
                if self.path.endswith('/status'):
                    gen = self.path.split('/')[2]
                    state = 'failed' if gen in fake.failed else 'completed'
                    error = 'engine error' if state == 'failed' else None
                    data = json.dumps({'id': gen, 'status': state, 'error': error})
                    return self.send(200, f'data: {data}\n\n'.encode(), 'text/event-stream')
                if self.path.startswith('/audio/'):
                    return self.send(200, fake.body if fake.body is not None else wav_bytes(1.0), 'audio/wav')
                self.send(404, b'{}', 'application/json')

            def do_POST(self):
                payload = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                fake.requests.append(payload)
                gen = f'g{len(fake.requests)}'
                if payload['text'] in fake.fail_texts:
                    fake.failed.add(gen)
                self.send(200, json.dumps({'id': gen, 'status': 'generating'}).encode(), 'application/json')

        self.fail_texts, self.failed, self.body = set(fail_texts), set(), body
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        self.url = f'http://127.0.0.1:{self.server.server_address[1]}'
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def close(self):
        self.server.shutdown()
        self.server.server_close()


class Generate(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = pathlib.Path(self.tmp.name)
        self.out = self.dir / 'out'
        self.cues = write_json(self.dir / 'cues.json', [{'id': 'a', 'text': 'FrameCore first', 'max_seconds': 2},
                                                        {'id': 'b', 'text': 'second line', 'max_seconds': 0.5}])
        self.lexicon = write_json(self.dir / 'lexicon.json', {'FrameCore': 'frejm kor'})

    def tearDown(self):
        self.tmp.cleanup()

    def voicebox(self, fake, *extra):
        argv = ['generate', '--engine', 'voicebox', '--cues', str(self.cues), '--out', str(self.out),
                '--lexicon', str(self.lexicon), '--profile', 'p1', '--language', 'pl', '--voicebox-url', fake.url, *extra]
        return quiet(runtime.main, argv, {})

    def lock(self):
        return json.loads((self.out / 'narration.lock.json').read_text(encoding='utf-8'))

    def test_voicebox_roundtrip(self):
        fake = FakeVoicebox()
        try:
            code, out, _ = self.voicebox(fake)
        finally:
            fake.close()
        self.assertEqual(code, 0)
        self.assertEqual(fake.requests[0], {'text': 'frejm kor first', 'profile_id': 'p1', 'language': 'pl'})
        line = self.lock()['lines']['a']
        self.assertEqual((line['status'], line['engine'], line['text_sent']), ('ok', 'voicebox', 'frejm kor first'))
        import audio
        self.assertEqual(line['sha256'], audio.sha256(self.out / 'a.wav'))
        self.assertEqual(self.lock()['lines']['b']['verdict'], 'over')
        self.assertIn('b: 1.00s / 0.50s over', out)

    def test_voicebox_failed_line_keeps_others(self):
        fake = FakeVoicebox(fail_texts={'second line'})
        try:
            code, _, _ = self.voicebox(fake)
        finally:
            fake.close()
        self.assertEqual(code, 1)
        lines = self.lock()['lines']
        self.assertEqual(lines['a']['status'], 'ok')
        self.assertEqual((lines['b']['status'], lines['b']['error']), ('failed', 'engine error'))

    def test_only_regenerates_selected(self):
        fake = FakeVoicebox()
        try:
            self.voicebox(fake)
            before = self.lock()['lines']['a']['sha256']
            (self.out / 'a.wav').write_bytes(wav_bytes(0.3))
            code, _, _ = self.voicebox(fake, '--only', 'b')
        finally:
            fake.close()
        self.assertEqual(code, 0)
        self.assertEqual(len(fake.requests), 3)
        self.assertEqual(fake.requests[-1]['text'], 'second line')
        self.assertEqual(self.lock()['lines']['a']['sha256'], before)

    def test_non_wav_without_ffmpeg_one_line(self):
        fake = FakeVoicebox(body=b'ID3fake-mp3')
        try:
            with mock.patch.object(runtime.shutil, 'which', return_value=None):
                code, _, _ = self.voicebox(fake)
        finally:
            fake.close()
        self.assertEqual(code, 1)
        self.assertIn('non-WAV', self.lock()['lines']['a']['error'])

    def test_voicebox_needs_profile(self):
        code, _, err = quiet(runtime.main, ['generate', '--engine', 'voicebox', '--cues', str(self.cues),
                                            '--out', str(self.out)], {})
        self.assertEqual(code, 2)
        self.assertIn('--profile', err)

    def test_voicebox_unreachable_no_fallback(self):
        with mock.patch.object(runtime.subprocess, 'run') as run:
            code, _, err = quiet(runtime.main, ['generate', '--engine', 'voicebox', '--cues', str(self.cues),
                                                '--out', str(self.out), '--profile', 'p1',
                                                '--voicebox-url', 'http://127.0.0.1:9'], {})
        self.assertEqual(code, 1)
        self.assertIn("user's own computer", err)
        run.assert_not_called()
        self.assertFalse(self.out.exists())

    def test_clone_needs_consent(self):
        ref = write_wav(self.dir / 'ref.wav', 1.0)
        with mock.patch.object(runtime.subprocess, 'run') as run:
            code, _, err = quiet(runtime.main, ['generate', '--engine', 'voxcpm', '--cues', str(self.cues),
                                                '--out', str(self.out), '--reference-wav', str(ref)], {})
        self.assertEqual(code, 2)
        self.assertIn('--consent', err)
        run.assert_not_called()

    def install_fake_voxcpm(self, root):
        python = runtime.venv_python(root)
        python.parent.mkdir(parents=True)
        python.touch()
        (runtime.hf_cache(root) / 'hub' / 'models--openbmb--VoxCPM2' / 'snapshots' / 'abc').mkdir(parents=True)

    def test_voxcpm_missing_hint(self):
        root = self.dir / 'root'
        argv = ['generate', '--engine', 'voxcpm', '--cues', str(self.cues), '--out', str(self.out), '--root', str(root)]
        code, _, err = quiet(runtime.main, argv, {})
        self.assertEqual(code, 1)
        self.assertIn('install voxcpm --yes', err)
        self.install_fake_voxcpm(root)
        import shutil as sh
        sh.rmtree(runtime.hf_cache(root))
        code, _, err = quiet(runtime.main, argv, {})
        self.assertEqual(code, 1)
        self.assertIn('fetch-models --yes', err)

    def test_voxcpm_worker_jobs(self):
        root = self.dir / 'root'
        self.install_fake_voxcpm(root)
        seen = {}

        def fake_worker(argv, **kwargs):
            job = json.loads(pathlib.Path(argv[-1]).read_text(encoding='utf-8'))
            seen.update(job=job, env=kwargs['env'], argv=argv)
            lines = []
            for item in job['jobs']:
                write_wav(pathlib.Path(item['out']), 0.4)
                lines.append(json.dumps({'id': item['id'], 'status': 'ok'}))
            return mock.Mock(returncode=0, stdout='\n'.join(lines) + '\n', stderr='')
        ref = write_wav(self.dir / 'ref.wav', 1.0)
        with mock.patch.object(runtime.subprocess, 'run', side_effect=fake_worker), \
                mock.patch.object(runtime, 'voxcpm_version', return_value='2.0.3'):
            code, _, _ = quiet(runtime.main, ['generate', '--engine', 'voxcpm', '--cues', str(self.cues),
                                              '--out', str(self.out), '--root', str(root), '--lexicon', str(self.lexicon),
                                              '--reference-wav', str(ref), '--consent', 'speaker agreed in writing 2026-10-24'], {})
        self.assertEqual(code, 0)
        self.assertTrue(seen['argv'][-2].endswith('voxcpm_worker.py'))
        self.assertEqual(seen['env']['HF_HUB_OFFLINE'], '1')
        self.assertEqual(seen['job']['jobs'][0]['text'], 'frejm kor first')
        line = self.lock()['lines']['a']
        self.assertEqual((line['engine'], line['engine_version'], line['model']), ('voxcpm', '2.0.3', 'openbmb/VoxCPM2'))
        self.assertEqual(line['consent'], 'speaker agreed in writing 2026-10-24')
        self.assertTrue(line['voice_source'].startswith('reference:'))
        self.assertEqual(line['lexicon_sha256'], __import__('hashlib').sha256(self.lexicon.read_bytes()).hexdigest())
        self.assertNotIn('lexicon_sha256', self.lock())


class Worker(unittest.TestCase):
    def test_failed_job_does_not_stop_others(self):
        import types
        written = []

        class Model:
            tts_model = types.SimpleNamespace(sample_rate=48000)

            def generate(self, **options):
                if options['text'] == 'bad':
                    raise RuntimeError('oom')
                self.last = options
                return [0.0]
        model = Model()
        fake_vox = types.SimpleNamespace(VoxCPM=types.SimpleNamespace(from_pretrained=lambda *a, **k: model))
        fake_sf = types.SimpleNamespace(write=lambda path, wav, rate, subtype: written.append((path, rate, subtype)))
        with tempfile.TemporaryDirectory() as tmp:
            job = write_json(pathlib.Path(tmp) / 'job.json', {'model': 'openbmb/VoxCPM2', 'jobs': [
                {'id': 'a', 'text': 'bad', 'out': 'a.wav', 'seed': 1},
                {'id': 'b', 'text': 'good', 'out': 'b.wav', 'seed': 1, 'reference_wav': 'ref.wav'}]})
            worker_spec = importlib.util.spec_from_file_location('worker', PLUGIN / 'scripts/voxcpm_worker.py')
            worker = importlib.util.module_from_spec(worker_spec)
            worker_spec.loader.exec_module(worker)
            with mock.patch.dict(sys.modules, {'voxcpm': fake_vox, 'soundfile': fake_sf}):
                code, out, _ = quiet(worker.main, str(job))
        self.assertEqual(code, 1)
        results = [json.loads(line) for line in out.splitlines()]
        self.assertEqual([(r['id'], r['status']) for r in results], [('a', 'failed'), ('b', 'ok')])
        self.assertEqual(written, [('b.wav', 48000, 'PCM_16')])
        self.assertEqual(model.last['reference_wav_path'], 'ref.wav')


class ReviewFixes(unittest.TestCase):
    """Final review findings 1-6 (2026-10-24)."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = pathlib.Path(self.tmp.name)
        self.out = self.dir / 'out'
        self.cues = write_json(self.dir / 'cues.json', [{'id': 'a', 'text': 'Core one', 'max_seconds': 2},
                                                        {'id': 'b', 'text': 'two', 'max_seconds': 2}])

    def tearDown(self):
        self.tmp.cleanup()

    def voicebox(self, url, *extra):
        return quiet(runtime.main, ['generate', '--engine', 'voicebox', '--cues', str(self.cues), '--out', str(self.out),
                                    '--profile', 'p1', '--voicebox-url', url, *extra], {})

    def lock(self):
        return json.loads((self.out / 'narration.lock.json').read_text(encoding='utf-8'))

    def broken_server(self, generate_body, status_body=b'data: {"status": "completed"}\n\n'):
        import http.server
        import threading

        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def reply(self, body):
                self.send_response(200)
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def do_GET(self):
                self.reply(b'{}' if self.path == '/health' else status_body)

            def do_POST(self):
                self.rfile.read(int(self.headers['Content-Length']))
                self.reply(generate_body)
        server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        return f'http://127.0.0.1:{server.server_address[1]}'

    def test_1_bad_voicebox_answers_are_one_line_per_line(self):
        for generate_body, status_body in ((b'<html>proxy</html>', None), (b'{"status": "x"}', None),
                                           (b'{"id": "g1"}', b'data: {not json\n\n')):
            url = self.broken_server(generate_body, status_body or b'data: {"status": "completed"}\n\n')
            code, _, err = self.voicebox(url)
            self.assertEqual(code, 1, generate_body)
            self.assertNotIn('Traceback', err)
            lines = self.lock()['lines']
            self.assertEqual({lines['a']['status'], lines['b']['status']}, {'failed'})

    def test_2_failed_only_keeps_the_previous_take_truthful(self):
        fake = FakeVoicebox()
        try:
            self.voicebox(fake.url)
            before = self.lock()['lines']['a']
            fake.fail_texts.add('kor one')
            lexicon = write_json(self.dir / 'lexicon.json', {'Core': 'kor'})
            code, _, _ = self.voicebox(fake.url, '--only', 'a', '--lexicon', str(lexicon))
        finally:
            fake.close()
        self.assertEqual(code, 1)
        after = self.lock()['lines']['a']
        self.assertEqual(after['status'], 'failed')
        for key in ('text_sent', 'wav', 'sha256', 'lexicon_sha256', 'stretch_percent'):
            self.assertEqual(after[key], before[key], key)

    def test_3_only_keeps_other_lines_lexicon_hash(self):
        fake = FakeVoicebox()
        lexicon = write_json(self.dir / 'lexicon.json', {'Core': 'kor'})
        try:
            self.voicebox(fake.url, '--lexicon', str(lexicon))
            digest = self.lock()['lines']['b']['lexicon_sha256']
            self.voicebox(fake.url, '--only', 'a')
        finally:
            fake.close()
        self.assertIsNotNone(digest)
        self.assertEqual(self.lock()['lines']['b']['lexicon_sha256'], digest)
        self.assertIsNone(self.lock()['lines']['a']['lexicon_sha256'])

    def test_4_unsafe_ids_refused(self):
        import formats
        for bad in ('../escape', 'a/b', 'a:b', '..', '.hidden', 'a b'):
            path = write_json(self.dir / 'bad.json', [{'id': bad, 'text': 'x', 'max_seconds': 1}])
            with self.assertRaises(formats.CueError, msg=bad):
                formats.load_cues(path)
        ok = write_json(self.dir / 'ok.json', [{'id': 's01_intro-2.v1', 'text': 'x', 'max_seconds': 1}])
        self.assertEqual(formats.load_cues(ok)[0].id, 's01_intro-2.v1')

    def test_5_malformed_lock_is_one_line(self):
        self.out.mkdir()
        (self.out / 'narration.lock.json').write_text('{broken', encoding='utf-8')
        for argv in (['measure', '--cues', str(self.cues), '--out', str(self.out)],
                     ['stretch', 'a', '--percent', '2', '--cues', str(self.cues), '--out', str(self.out), '--yes']):
            with mock.patch.object(runtime.shutil, 'which', return_value='/usr/bin/ffmpeg'):
                write_wav(self.out / 'a.wav', 0.5)
                code, _, err = quiet(runtime.main, argv, {})
            self.assertEqual(code, 2, argv)
            self.assertIn('narration.lock.json', err)
            self.assertEqual(len(err.strip().splitlines()), 1)

    def test_6_lock_paths_survive_moving_the_folder(self):
        fake = FakeVoicebox()
        try:
            self.voicebox(fake.url)
        finally:
            fake.close()
        self.assertEqual(self.lock()['lines']['a']['wav'], 'a.wav')
        moved = self.dir / 'moved'
        self.out.rename(moved)
        code, out, _ = quiet(runtime.main, ['measure', '--cues', str(self.cues), '--out', str(moved), '--json'], {})
        self.assertEqual(code, 0)
        self.assertEqual({row['verdict'] for row in json.loads(out)}, {'fits'})


class Minors(unittest.TestCase):
    """Final review minors decided for 1.0.1 (2026-10-24)."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = pathlib.Path(self.tmp.name)
        self.cues = write_json(self.dir / 'cues.json', [{'id': 'a', 'text': 'x', 'max_seconds': 1}])

    def tearDown(self):
        self.tmp.cleanup()

    def test_ffmpeg_error_is_plain_text(self):
        import audio
        write_wav(self.dir / 'a.wav', 0.5)
        with mock.patch.object(audio.subprocess, 'run', return_value=mock.Mock(returncode=1, stderr='first\nbad filter\n')):
            with self.assertRaises(audio.AudioError) as caught:
                audio.stretch(self.dir / 'a.wav', 3, 'ffmpeg', self.dir / 'b.wav')
        self.assertEqual(str(caught.exception), 'FFmpeg failed: bad filter')

    def test_stretch_plan_checks_source_and_ffmpeg(self):
        argv = ['stretch', 'a', '--percent', '3', '--cues', str(self.cues), '--out', str(self.dir)]
        code, _, err = quiet(runtime.main, argv, {})
        self.assertEqual(code, 1)
        self.assertIn('does not exist', err)
        write_wav(self.dir / 'a.wav', 0.5)
        with mock.patch.object(runtime.shutil, 'which', return_value=None):
            code, _, err = quiet(runtime.main, argv, {})
        self.assertEqual(code, 1)
        self.assertIn('FFmpeg', err)

    def test_unreadable_wav_is_reported_not_raised(self):
        import audio
        write_wav(self.dir / 'a.wav', 0.5)
        with mock.patch.object(audio.wave, 'open', side_effect=PermissionError('denied')):
            code, out, err = quiet(runtime.main, ['measure', '--cues', str(self.cues), '--out', str(self.dir), '--json'], {})
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(out)[0]['verdict'], 'unreadable')

    def test_leading_space_keeps_description(self):
        import formats
        self.assertEqual(formats.apply_lexicon(' (Core voice)Core', {'Core': 'kor'}), ' (Core voice)kor')

    def test_case_colliding_lexicon_keys_refused(self):
        import formats
        path = write_json(self.dir / 'lexicon.json', {'AI': 'a i', 'ai': 'aj'})
        with self.assertRaises(formats.CueError) as caught:
            formats.load_lexicon(path)
        self.assertIn('AI', str(caught.exception))

    def test_silent_take_fails_generate(self):
        fake = FakeVoicebox(body=wav_bytes(0.0))
        try:
            code, _, err = quiet(runtime.main, ['generate', '--engine', 'voicebox', '--cues', str(self.cues),
                                                '--out', str(self.dir / 'out'), '--profile', 'p',
                                                '--voicebox-url', fake.url], {})
        finally:
            fake.close()
        self.assertEqual(code, 1)
        self.assertIn('silent: a', err)


if __name__ == '__main__':
    unittest.main()
