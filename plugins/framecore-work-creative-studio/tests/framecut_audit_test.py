"""Regressions for the defects found by the 2026-10-22 FrameCut audit (real-media, robustness and board reviews)."""
import copy
import csv
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
RUNTIME = PACKAGE / 'skills/opencut-video-studio/assets/framecut'
sys.path.insert(0, str(RUNTIME))
sys.path.insert(0, str(PACKAGE / 'skills/opencut-video-studio/scripts'))
from fc_core import FrameCutError, apply_operations, atomic_json, commit_revision, read_json, validate
from fc_media import ffmpeg, ingest, inspect_media, probe
from fc_captions import sidecars
from fc_render import compile_project, render, verify_delivery
from framecut import project_init, export_edit

CLI = RUNTIME / 'framecut.py'


def cli(*args, cwd=None):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    return subprocess.run([sys.executable, '-B', str(CLI), *map(str, args)], capture_output=True, text=True, cwd=cwd, env=env, timeout=300)


def sequence(**extra):
    base = {'id': 'main', 'fps': {'num': 30, 'den': 1}, 'duration': 60, 'clips': [{'id': 'c1', 'asset': 'a', 'start': 0, 'duration': 60, 'source_in': 0}]}
    base.update(extra)
    return base


class Fixture(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures = tempfile.TemporaryDirectory()
        cls.source = Path(cls.fixtures.name) / 'source.mp4'
        ffmpeg(['-f', 'lavfi', '-i', 'color=red:s=320x180:r=30:d=3', '-f', 'lavfi', '-i', 'sine=frequency=440:sample_rate=48000:duration=3',
                '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', str(cls.source)])
        cls.short = Path(cls.fixtures.name) / 'short.mp4'
        ffmpeg(['-f', 'lavfi', '-i', 'color=blue:s=320x180:r=30:d=0.4', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', str(cls.short)])

    @classmethod
    def tearDownClass(cls):
        cls.fixtures.cleanup()

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        shutil.copy2(self.source, self.root / 'source.mp4')
        self.p = project_init(self.root / 'project.json', 'audit')
        self.p['assets']['a'] = ingest(self.root, 'source.mp4', 'a')
        self.p['sequences'] = [sequence()]
        self.p['deliverables'] = [{'id': 'wide', 'sequence': 'main', 'width': 320, 'height': 180}]
        self.p['authorization'] = 'Authorized synthetic audit test'

    def tearDown(self):
        self.tmp.cleanup()


class EditSemantics(Fixture):
    def test_partial_set_captions_keeps_the_other_settings(self):
        self.p['sequences'][0]['captions'] = {'enabled': True, 'mode': 'sentence', 'size': 0.05}
        result, _ = apply_operations(self.p, [{'op': 'set_captions', 'sequence': 'main', 'value': {'size': 0.08}}])
        captions = result['sequences'][0]['captions']
        self.assertEqual((captions['enabled'], captions['mode'], captions['size']), (True, 'sentence', 0.08))

    def test_an_explicit_disable_still_disables(self):
        self.p['sequences'][0]['captions'] = {'enabled': True, 'mode': 'sentence'}
        result, _ = apply_operations(self.p, [{'op': 'set_captions', 'sequence': 'main', 'value': {'enabled': False}}])
        self.assertFalse(result['sequences'][0]['captions']['enabled'])


class Captions(Fixture):
    def words(self, **timing):
        words = [{'id': 'w1', 'text': 'Hello', 'start': 0.1, 'end': 0.5}, {'id': 'w2', 'text': 'there', **timing},
                 {'id': 'w3', 'text': 'friend', 'start': 1.2, 'end': 1.6}]
        self.p['analyses']['a'] = {'source_hash': self.p['assets']['a']['sha256'], 'timing': 'aligned', 'words': words}
        self.p['sequences'][0]['captions'] = {'enabled': True, 'mode': 'kinetic'}

    def test_a_spoken_word_without_timing_blocks_the_final(self):
        self.words(start=None, end=None)
        with self.assertRaises(FrameCutError) as caught:
            render(self.p, self.root, 'wide', 'final-bundle', mode='final', max_disk_mb=128)
        self.assertEqual(caught.exception.code, 'qa_failed')
        self.assertIn('unknown_timing', str(caught.exception))
        self.assertFalse((self.root / 'final-bundle').exists())

    def test_the_same_word_is_only_a_warning_in_a_preview(self):
        self.words(start=None, end=None)
        codes = [w['code'] for w in compile_project(self.p, self.root, 'wide')['warnings']]
        self.assertIn('unknown_timing', codes)

    def test_an_unwrappable_token_is_a_typed_layout_error_not_a_crash(self):
        projection = {'fps': {'num': 30, 'den': 1}, 'words': [{'id': 'w', 'text': 'x' * 300, 'start': 0, 'end': 30, 'kind': 'word'}],
                      'groups': [[{'id': 'w', 'text': 'x' * 300, 'start': 0, 'end': 30, 'kind': 'word'}]]}
        try:
            result = sidecars(projection)
        except FrameCutError:
            return
        self.assertIn('x' * 300, result['srt'])


class Analysis(Fixture):
    def test_analyze_handles_a_clip_shorter_than_its_thumbnail_grid(self):
        shutil.copy2(self.short, self.root / 'short.mp4')
        asset = ingest(self.root, 'short.mp4', 'short')
        result = inspect_media(self.root, asset, self.root / 'analysis-short')
        self.assertTrue(result['thumbnails'])
        for item in result['thumbnails']:
            self.assertTrue((self.root / 'analysis-short' / item['file']).is_file())

    def test_a_failed_analysis_leaves_no_directory_behind(self):
        asset = copy.deepcopy(self.p['assets']['a'])
        asset['sha256'] = '0' * 64
        with self.assertRaises(FrameCutError):
            inspect_media(self.root, asset, self.root / 'analysis-bad')
        self.assertFalse((self.root / 'analysis-bad').exists())


class Audio(Fixture):
    def test_unity_speed_adds_no_tempo_stage_and_others_chain_correctly(self):
        from fc_render import tempo_filters
        self.assertEqual(tempo_filters(1), [])
        self.assertEqual(tempo_filters(2), ['atempo=2.0'])
        self.assertEqual(tempo_filters(4), ['atempo=2', 'atempo=2.0'])
        self.assertEqual(tempo_filters(0.25), ['atempo=0.5', 'atempo=0.5'])
        self.assertEqual(tempo_filters(1.5), ['atempo=1.5'])

    def test_unity_speed_keeps_audio_onsets_where_the_source_has_them(self):
        import array
        import wave
        beeps = self.root / 'beeps.wav'
        ffmpeg(['-f', 'lavfi', '-i', "aevalsrc='if(lt(mod(t\\,1)\\,0.05)\\,sin(2*PI*1000*t)*0.8\\,0)':s=48000:d=4", '-ar', '48000', '-c:a', 'pcm_s16le', str(beeps)])
        movie = self.root / 'beep.mp4'
        ffmpeg(['-f', 'lavfi', '-i', 'color=gray:s=320x180:r=30:d=4', '-i', str(beeps), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-shortest', str(movie)])
        self.p['assets']['b'] = ingest(self.root, 'beep.mp4', 'b')
        self.p['sequences'] = [sequence(duration=90, clips=[{'id': 'c1', 'asset': 'b', 'start': 0, 'duration': 90, 'source_in': 0}])]
        self.p = commit_revision(self.root / 'project.json', self.p, 1, 'beep')
        render(self.p, self.root, 'wide', 'beep-out', mode='preview', max_disk_mb=128)
        decoded = self.root / 'decoded.wav'
        ffmpeg(['-i', str(self.root / 'beep-out/video.mp4'), '-vn', '-ar', '48000', '-ac', '1', '-c:a', 'pcm_s16le', str(decoded)])
        with wave.open(str(decoded)) as handle:
            samples = array.array('h', handle.readframes(handle.getnframes()))
        onsets, last = [], -48000
        for index, value in enumerate(samples):
            if abs(value) > 3000 and index - last > 12000:
                onsets.append(index / 48000)
                last = index
        for expected, found in zip((1.0, 2.0), onsets[1:3]):
            self.assertLess(abs(found - expected), 0.012, onsets)


class Limits(Fixture):
    def test_a_revision_over_the_read_limit_is_refused_before_it_is_written(self):
        self.p = commit_revision(self.root / 'project.json', self.p, 1, 'assemble')
        huge = copy.deepcopy(self.p)
        huge['brief'] = {'notes': 'x' * (17 * 1024 * 1024)}
        with self.assertRaises(FrameCutError) as caught:
            commit_revision(self.root / 'project.json', huge, self.p['revision'], 'too big')
        self.assertEqual(caught.exception.code, 'resource_limit')
        self.assertEqual(read_json(self.root / 'project.json')['revision'], self.p['revision'])


class ProbeValidation(Fixture):
    def test_probe_fields_that_reach_filter_graphs_must_be_plain_numbers(self):
        for field, value in [('audio_index', '0]anull[x1];amovie=/etc/hostname[x2];[x2]anullsink;[x1]anullsink;[1:0'),
                             ('video_index', '0,movie=/etc/hostname'), ('width', '320;x'), ('height', True), ('fps', 'abc'),
                             ('pix_fmt', 'yuv420p;movie=x')]:
            project = copy.deepcopy(self.p)
            if field in project['assets']['a']['probe'] or field == 'audio_index':
                project['assets']['a']['probe'][field] = value
            with self.subTest(field=field):
                with self.assertRaises(FrameCutError):
                    validate(project)

    def test_a_genuine_probe_still_validates(self):
        validate(self.p, self.root, True)


class Readiness(Fixture):
    REVIEW = {'reviewer': 'audit test', 'scope': 'fixture', 'observations': 'recording only', 'outcome': 'pass',
              'picture_watched': True, 'audio_heard': True, 'coverage': 'full'}

    def test_a_preview_bundle_is_never_ready(self):
        self.p = commit_revision(self.root / 'project.json', self.p, 1, 'assemble')
        render(self.p, self.root, 'wide', 'preview-bundle', mode='preview', max_disk_mb=128)
        atomic_json(self.root / 'preview-bundle/review-evidence.json', {
            'project_hash': read_receipt(self.root / 'preview-bundle')['project_hash'], 'project_revision': self.p['revision'],
            'technical': 'PASS', 'evidence': self.REVIEW, 'video_hash': __import__('fc_core').file_hash(self.root / 'preview-bundle/video.mp4')})
        verified = verify_delivery(self.p, self.root, 'preview-bundle')
        self.assertNotEqual(verified['delivery_readiness']['status'], 'READY')
        self.assertEqual(verified['delivery_readiness']['status'], 'PREVIEW_ONLY')


def read_receipt(folder):
    return read_json(Path(folder) / 'receipt.json')


class Export(Fixture):
    def project_with_hostile_names(self, name, note):
        shutil.copy2(self.source, self.root / name)
        self.p['assets']['h'] = ingest(self.root, name, 'h')
        self.p['sequences'] = [sequence(clips=[{'id': 'c1', 'asset': 'h', 'start': 0, 'duration': 60, 'source_in': 0, 'note': note}])]
        return self.p

    def test_file_names_and_notes_cannot_forge_edl_lines_or_csv_formulas(self):
        name = 'x.mp4\n002  EVIL     V     C        00:00:00:00 00:00:02:00 01:00:00:00 01:00:02:00\n* FROM CLIP NAME: PWNED.mov'
        project = self.project_with_hostile_names(name, '=HYPERLINK("http://evil","x")\n003  EVIL2')
        export_edit(project, self.root, 'main', 'out')
        edl = (self.root / 'out/picture.edl').read_text()
        self.assertNotIn('\n002  EVIL', edl)
        self.assertNotIn('\n003  EVIL2', edl)
        self.assertEqual(sum(1 for line in edl.splitlines() if line.startswith('001 ')), 1)
        self.assertEqual(sum(1 for line in edl.splitlines() if line[:3].isdigit()), 1)
        with (self.root / 'out/shots.csv').open(newline='') as handle:
            for row in csv.DictReader(handle):
                for value in row.values():
                    self.assertFalse(value[:1] in '=+-@' and value[:1] != '', value)

    def test_an_unsupported_frame_rate_is_a_typed_error_and_leaves_nothing(self):
        self.p['sequences'] = [sequence(fps={'num': 25, 'den': 2}, duration=30, clips=[{'id': 'c1', 'asset': 'a', 'start': 0, 'duration': 30, 'source_in': 0}])]
        self.p = commit_revision(self.root / 'project.json', self.p, 1, 'slow')
        done = cli('export', self.root / 'project.json', '--sequence', 'main', '--out', 'ex')
        self.assertEqual(done.returncode, 2, done.stderr)
        self.assertNotIn('Traceback', done.stderr)
        self.assertFalse((self.root / 'ex').exists())


class Paths(Fixture):
    def test_a_relative_project_path_with_parent_segments_works(self):
        sub = self.root / 'sub'
        sub.mkdir()
        done = cli('validate', '../project.json', cwd=sub)
        self.assertEqual(done.returncode, 0, done.stderr)

    def test_outputs_cannot_land_in_the_reserved_namespace(self):
        self.p = commit_revision(self.root / 'project.json', self.p, 1, 'assemble')
        for out in ('.framecut/audit/history/r2.json', 'project.json.lock', '.framecut/audit/render.lock'):
            done = cli('compile', self.root / 'project.json', '--deliverable', 'wide', '--out', out)
            with self.subTest(out=out):
                self.assertEqual(done.returncode, 2, done.stdout)
        done = cli('apply', self.root / 'project.json', '--ops', self.root / 'ops.json', '--base-revision', '2', '--reason', 'x')
        self.assertNotIn('Revision history conflict', done.stderr)

    def test_a_caption_font_cannot_start_with_a_dash(self):
        self.p['sequences'][0]['captions'] = {'enabled': True, 'font': '-s'}
        with self.assertRaises(FrameCutError):
            validate(self.p)


class Crashes(Fixture):
    def test_malformed_but_parseable_documents_are_typed_errors(self):
        broken = copy.deepcopy(self.p)
        broken['analyses'] = {'a': None}
        with self.assertRaises(FrameCutError):
            validate(broken)
        with self.assertRaises(FrameCutError):
            apply_operations(self.p, [{'op': 'replace_clip', 'sequence': 'main', 'id': 'c1', 'value': 'oops'}])
        with self.assertRaises(FrameCutError):
            apply_operations(self.p, [{'op': 'set_sequence', 'sequence': 'main', 'value': 3}])

    def test_the_cli_never_prints_a_traceback_for_deep_json(self):
        (self.root / 'ops.json').write_text('[' * 5000 + ']' * 5000)
        done = cli('apply', self.root / 'project.json', '--ops', self.root / 'ops.json', '--base-revision', '2', '--reason', 'x')
        self.assertEqual(done.returncode, 2)
        self.assertNotIn('Traceback', done.stderr)


class Locks(Fixture):
    def lock_path(self):
        return self.root / '.framecut/audit/render.lock'

    def test_a_lock_left_by_a_dead_process_is_reclaimed(self):
        self.p = commit_revision(self.root / 'project.json', self.p, 1, 'assemble')
        self.lock_path().parent.mkdir(parents=True, exist_ok=True)
        self.lock_path().write_text(json.dumps({'pid': 2 ** 22 - 3, 'process_token': '1', 'job': None}))
        result = render(self.p, self.root, 'wide', 'after-kill', mode='preview', max_disk_mb=128)
        self.assertEqual(result['status'], 'render_complete')
        self.assertFalse(self.lock_path().exists())

    def test_a_lock_held_by_a_running_process_names_its_owner(self):
        from fc_jobs import process_token
        self.p = commit_revision(self.root / 'project.json', self.p, 1, 'assemble')
        self.lock_path().parent.mkdir(parents=True, exist_ok=True)
        self.lock_path().write_text(json.dumps({'pid': os.getpid(), 'process_token': process_token(os.getpid()), 'job': None}))
        with self.assertRaises(FrameCutError) as caught:
            render(self.p, self.root, 'wide', 'blocked', mode='preview', max_disk_mb=128)
        self.assertEqual(caught.exception.code, 'busy')
        self.assertIn('render.lock', str(caught.exception))
        self.assertIn(str(os.getpid()), str(caught.exception))
        self.assertTrue(self.lock_path().exists())

    def test_sigterm_stops_a_render_and_the_next_one_runs(self):
        import signal
        import time
        self.p = commit_revision(self.root / 'project.json', self.p, 1, 'assemble')
        shim = self.root / 'shim'
        shim.mkdir()
        for tool in ('ffmpeg',):
            real = shutil.which(tool)
            (shim / tool).write_text(f'#!/bin/sh\nsleep 8\nexec {real} "$@"\n')
            (shim / tool).chmod(0o755)
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PATH=f'{shim}:{os.environ["PATH"]}')
        proc = subprocess.Popen([sys.executable, '-B', str(CLI), 'render', str(self.root / 'project.json'), '--deliverable', 'wide', '--out', 'killed'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
        deadline = time.time() + 30
        while not self.lock_path().exists() and time.time() < deadline:
            time.sleep(.1)
        self.assertTrue(self.lock_path().exists())
        proc.send_signal(signal.SIGTERM)
        _, err = proc.communicate(timeout=30)
        self.assertNotIn('Traceback', err)
        self.assertFalse(self.lock_path().exists(), err)
        self.assertFalse((self.root / 'killed').exists())


class CachePoisoning(Fixture):
    def test_a_source_swapped_during_a_stage_is_not_stored_as_that_stage(self):
        import fc_render
        self.p = commit_revision(self.root / 'project.json', self.p, 1, 'assemble')
        original = fc_render.Cache.stage

        def tampering(cache, label, settings, suffix, build):
            def swapped(output):
                build(output)
                with (self.root / 'source.mp4').open('ab') as handle:
                    handle.write(b'swapped during the render')
            return original(cache, label, settings, suffix, swapped)

        fc_render.Cache.stage = tampering
        try:
            with self.assertRaises(FrameCutError) as caught:
                render(self.p, self.root, 'wide', 'poisoned', mode='preview', max_disk_mb=128)
        finally:
            fc_render.Cache.stage = original
        self.assertEqual(caught.exception.code, 'stale_source')
        self.assertEqual(list((self.root / '.framecut/audit/cache').glob('*.json')), [])


if __name__ == '__main__':
    unittest.main()
