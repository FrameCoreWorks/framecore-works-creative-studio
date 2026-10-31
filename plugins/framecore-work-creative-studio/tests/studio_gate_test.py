"""Delivery gate (delivery-documentation/scripts/studio_gate.py) and its Stop hook (hooks/studio_gate_hook.py).

Trigger: owner request 2026-10-31 after an outside review: the quality review was only an instruction, so a weak file
could still be handed over. These cases fix that a measured fault blocks delivery and that the hook enforces it.
"""
import importlib.util
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
GATE = PLUGIN / 'skills/delivery-documentation/scripts/studio_gate.py'
HOOK = PLUGIN / 'hooks/studio_gate_hook.py'
FFMPEG = shutil.which('ffmpeg') and shutil.which('ffprobe')


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


gate = load('studio_gate', GATE)
sys.modules['studio_gate'] = gate
hook = load('studio_gate_hook', HOOK)


def ffmpeg(*args):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *args], check=True, timeout=120)


def good_video(path, size='540x960', seconds=4):
    ffmpeg('-f', 'lavfi', '-i', f'testsrc2=s={size}:r=30:d={seconds}', '-f', 'lavfi', '-i', f'sine=f=440:d={seconds},volume=-12dB',
           '-shortest', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', str(path))


class Base(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temp.name)
        self.export = self.root / 'export'
        self.export.mkdir()

    def tearDown(self):
        self.temp.cleanup()


@unittest.skipUnless(FFMPEG, 'needs ffmpeg and ffprobe')
class VideoAudio(Base):
    def test_good_video_passes_and_report_is_bound_to_the_file(self):
        film = self.export / 'reel.mp4'
        good_video(film)
        report = gate.gate(film)
        self.assertEqual(report['verdict'], 'PASS', report['checks'])
        self.assertEqual({c['id'] for c in report['checks']}, {'file', 'format', 'black', 'still', 'flash', 'loudness'})
        self.assertEqual(gate.file_state(film), 'PASS')
        with open(film, 'ab') as handle:
            handle.write(b'\0')
        self.assertEqual(gate.file_state(film), 'CHANGED')

    def test_black_stretch_and_silent_sound_fail(self):
        film = self.export / 'bad.mp4'
        ffmpeg('-f', 'lavfi', '-i', "testsrc2=s=540x960:r=30:d=5,drawbox=c=black:t=fill:enable='between(t,1.5,3.5)'",
               '-f', 'lavfi', '-i', 'anullsrc=d=5', '-shortest', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', str(film))
        report = gate.gate(film)
        failed = {c['id'] for c in report['checks'] if c['result'] == 'FAIL'}
        self.assertEqual(report['verdict'], 'FAIL')
        self.assertTrue({'black', 'loudness'} <= failed, report['checks'])

    def test_fade_from_black_at_the_start_is_not_a_fault(self):
        film = self.export / 'fade.mp4'
        ffmpeg('-f', 'lavfi', '-i', 'testsrc2=s=540x960:r=30:d=4,fade=in:st=0:d=1.2', '-f', 'lavfi', '-i', 'sine=d=4,volume=-12dB',
               '-shortest', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', str(film))
        checks = {c['id']: c['result'] for c in gate.gate(film)['checks']}
        self.assertEqual(checks['black'], 'PASS')

    def test_spec_from_the_brief_is_enforced(self):
        film = self.export / 'reel.mp4'
        good_video(film)
        (self.root / 'gate.json').write_text(json.dumps({'schema': 'studio-gate-spec/1', 'defaults': {
            'width': 1080, 'height': 1920, 'fps': 25, 'duration_min': 10, 'lufs': -14, 'audio': 'required'}}))
        report = gate.gate(film)
        detail = next(c['detail'] for c in report['checks'] if c['id'] == 'format')
        self.assertEqual(report['verdict'], 'FAIL')
        for part in ('width 540', 'height 960', '25', 'shorter than 10'):
            self.assertIn(part, detail)
        self.assertEqual(report['spec'], str(self.root / 'gate.json'))

    def test_spec_skip_needs_a_reason_and_is_recorded(self):
        film = self.export / 'bad.mp4'
        ffmpeg('-f', 'lavfi', '-i', "testsrc2=s=540x960:r=30:d=5,drawbox=c=black:t=fill:enable='between(t,1.5,3.5)'",
               '-an', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', str(film))
        (self.root / 'gate.json').write_text(json.dumps({'schema': 'studio-gate-spec/1',
                                                         'files': {'bad.*': {'skip': {'black': 'the brief asks for a 2 s blackout beat'}}}}))
        report = gate.gate(film)
        black = next(c for c in report['checks'] if c['id'] == 'black')
        self.assertEqual(black['result'], 'SKIPPED')
        self.assertIn('blackout beat', black['detail'])

    def test_a_checker_that_cannot_run_blocks_instead_of_passing(self):
        film = self.export / 'reel.mp4'
        good_video(film)
        with mock.patch.dict(gate.TOOLS, {'flash_check': self.root / 'missing.py'}):
            report = gate.gate(film)
        self.assertEqual(report['verdict'], 'BLOCKED')
        self.assertEqual(gate.file_state(film), 'BLOCKED')

    def test_cli_exit_codes(self):
        film = self.export / 'reel.mp4'
        good_video(film)
        run = lambda *a: subprocess.run([sys.executable, '-B', str(GATE), *a], capture_output=True, text=True, timeout=300).returncode
        self.assertEqual(run('check', str(film)), 0)
        self.assertEqual(run('status', str(self.export)), 0)
        (self.export / 'notes.txt').write_text('x')
        self.assertEqual(run('status', str(self.export)), 1)
        self.assertEqual(run('check', str(self.root / 'nope.mp4')), 2)


class ImageText(Base):
    def test_blank_image_fails_and_real_image_passes_with_size(self):
        from PIL import Image, ImageDraw
        blank = self.export / 'blank.png'
        Image.new('RGB', (1080, 1350), 'white').save(blank)
        self.assertEqual(gate.gate(blank)['verdict'], 'FAIL')
        real = self.export / 'post.png'
        image = Image.new('RGB', (1080, 1350), 'white')
        ImageDraw.Draw(image).rectangle((100, 100, 900, 700), fill='black')
        image.save(real)
        (self.root / 'gate.json').write_text(json.dumps({'schema': 'studio-gate-spec/1', 'files': {'post.png': {'width': 1080, 'height': 1350}}}))
        self.assertEqual(gate.gate(real)['verdict'], 'PASS', gate.gate(real)['checks'])
        (self.root / 'gate.json').write_text(json.dumps({'schema': 'studio-gate-spec/1', 'files': {'post.png': {'width': 1080, 'height': 1920}}}))
        self.assertEqual(gate.gate(real)['verdict'], 'FAIL')

    def test_text_checks_and_length_limit(self):
        copy = self.export / 'post.txt'
        copy.write_text('Krótki, konkretny opis nowej kolekcji kubków z naszej pracowni.\n', encoding='utf-8')
        (self.root / 'gate.json').write_text(json.dumps({'schema': 'studio-gate-spec/1', 'defaults': {'language': 'pl', 'max_chars': 40}}))
        report = gate.gate(copy)
        checks = {c['id']: c['result'] for c in report['checks']}
        self.assertEqual(checks['length'], 'FAIL')
        self.assertIn('pl_copy', checks)
        self.assertIn('ai_writing', checks)
        (self.export / 'empty.txt').write_text('')
        self.assertEqual(gate.gate(self.export / 'empty.txt')['verdict'], 'FAIL')

    def test_waiver_needs_a_reason_and_clears_the_file(self):
        blank = self.export / 'blank.png'
        from PIL import Image
        Image.new('RGB', (64, 64), 'white').save(blank)
        gate.gate(blank)
        with self.assertRaises(ValueError):
            gate.waive(blank, 'ok')
        report = gate.waive(blank, 'the user wants a plain white placeholder card')
        self.assertEqual(report['verdict'], 'WAIVED')
        self.assertEqual(report['waived_checks'][0]['id'], 'blank')
        self.assertEqual(gate.file_state(blank), 'WAIVED')


class StopHook(Base):
    def event(self, active=False, session='s1'):
        return {'cwd': str(self.root), 'session_id': session, 'stop_hook_active': active, 'hook_event_name': 'Stop'}

    def setUp(self):
        super().setUp()
        patcher = mock.patch.dict(os.environ, {'PLUGIN_DATA': str(self.root / '.data')})
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_unchecked_file_blocks_the_turn_and_names_the_fix(self):
        (self.export / 'post.txt').write_text('Tekst.\n', encoding='utf-8')
        out = hook.decide(self.event())
        self.assertEqual(out['decision'], 'block')
        self.assertIn('post.txt (UNCHECKED)', out['reason'])
        self.assertIn('studio_gate.py', out['reason'])

    def test_cleared_files_and_old_projects_stay_silent(self):
        old = self.export / 'old.png'
        old.write_bytes(b'x')
        past = time.time() - 3 * 86400
        os.utime(old, (past, past))
        self.assertIsNone(hook.decide(self.event()))
        (self.export / gate.REPORT_DIR).mkdir()          # an adopted export folder: every file counts
        self.assertEqual(hook.decide(self.event())['decision'], 'block')
        gate.waive(old, 'the user delivers the legacy file as it is')
        self.assertIsNone(hook.decide(self.event()))

    def test_nested_export_folder_is_found_and_hidden_or_vendor_folders_are_not(self):
        nested = self.root / 'projekty' / 'klient' / 'export'
        nested.mkdir(parents=True)
        (nested / 'cut.mp4').write_bytes(b'x')
        vendor = self.root / 'node_modules' / 'pkg' / 'export'
        vendor.mkdir(parents=True)
        (vendor / 'a.mp4').write_bytes(b'x')
        out = hook.decide(self.event())
        self.assertIn('cut.mp4', out['reason'])
        self.assertNotIn('node_modules', out['reason'])

    def test_loop_guard_lets_the_turn_end_with_a_warning(self):
        (self.export / 'post.txt').write_text('Tekst.\n', encoding='utf-8')
        results = [hook.decide(self.event(active=i > 0)) for i in range(3)]
        self.assertEqual([('decision' in r) for r in results], [True, True, False])
        self.assertIn('NOT PASSED', results[2]['systemMessage'])

    def test_hook_process_prints_json_only_and_survives_bad_input(self):
        (self.export / 'post.txt').write_text('Tekst.\n', encoding='utf-8')
        env = {**os.environ, 'PLUGIN_DATA': str(self.root / '.data')}
        done = subprocess.run([sys.executable, '-B', str(HOOK)], input=json.dumps(self.event()), capture_output=True, text=True, env=env, timeout=60)
        self.assertEqual(done.returncode, 0)
        self.assertEqual(json.loads(done.stdout)['decision'], 'block')
        done = subprocess.run([sys.executable, '-B', str(HOOK)], input='not json', capture_output=True, text=True, env=env, timeout=60)
        self.assertEqual(done.returncode, 0)
        self.assertIn('systemMessage', json.loads(done.stdout))

    def test_hooks_json_registers_only_the_stop_gate(self):
        config = json.loads((PLUGIN / 'hooks/hooks.json').read_text())
        self.assertEqual(list(config['hooks']), ['Stop'])
        command = config['hooks']['Stop'][0]['hooks'][0]
        self.assertEqual(command['type'], 'command')
        self.assertIn('${CLAUDE_PLUGIN_ROOT}/hooks/studio_gate_hook.py', command['command'])


if __name__ == '__main__':
    unittest.main()
