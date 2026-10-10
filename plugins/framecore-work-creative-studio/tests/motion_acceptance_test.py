"""Regression tests from the reviewed reel (2026-10-09): separate acceptance verdicts, contract-only scores, drift
mistaken for pacing, repeated wipes and photo rectangles. Media tests build small synthetic videos with Pillow and
ffmpeg and skip without them; nothing here needs a browser (the text audit's browser tests are in
motion-toolkit.test.mjs)."""
import copy
import importlib.util
import io
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
REVIEW = PLUGIN / 'skills/hyperframes-workflow/assets/motion-review'
PROOF = REVIEW / 'fixtures/search-to-cta.motion.json'


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


critique = module('critique', REVIEW / 'critique.py')
acceptance = module('acceptance', REVIEW / 'acceptance.py')


def have_media():
    try:
        import PIL  # noqa: F401
    except ImportError:
        return False
    return bool(shutil.which('ffmpeg') and shutil.which('ffprobe'))


def run(main, argv):
    out = io.StringIO()
    with redirect_stdout(out):
        code = main(argv)
    return code, json.loads(out.getvalue())


def small_contract(scenes, total, copy_map, width=270, height=480):
    return {'schema_version': 1, 'id': 'synthetic', 'revision': 1, 'fps': {'num': 30, 'den': 1}, 'totalFrames': total,
            'width': width, 'height': height, 'tokens': {'background': '#F3EFE7', 'foreground': '#151515'},
            'copy': copy_map, 'assets': [], 'scenes': scenes}


def write_video(path, frames, size=(270, 480)):
    """Pipe Pillow frames into ffmpeg as H.264, 30 fps."""
    process = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{size[0]}x{size[1]}', '-r', '30',
                                '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '12', str(path)], stdin=subprocess.PIPE)
    for frame in frames:
        process.stdin.write(frame.tobytes())
    process.stdin.close()
    assert process.wait() == 0


def drift_frames(beats):
    """7 s: a textured 'photo' drifting 4 px over 6 s with a static line of text; with beats, new blocks appear at 2 s and 4 s."""
    from PIL import Image, ImageDraw
    frames = []
    for n in range(210):
        image = Image.new('RGB', (270, 480), (0xF3, 0xEF, 0xE7))
        draw = ImageDraw.Draw(image)
        x = 60 + int(4 * min(n, 180) / 180)
        for i in range(0, 120, 6):
            draw.rectangle([x + i, 140, x + i + 3, 300], fill=(90 + i, 60, 40))
        draw.rectangle([40, 60, 230, 84], fill=(21, 21, 21))
        if beats:
            if n >= 60:
                draw.rectangle([40, 330, 230, 360], fill=(160, 20, 90))
            if n >= 120:
                draw.rectangle([40, 380, 230, 410], fill=(21, 21, 21))
        if n >= 180:
            image = Image.new('RGB', (270, 480), (21, 21, 21))
        frames.append(image)
    return frames


class ContractOnlyScores(unittest.TestCase):
    def test_contract_only_score_is_never_a_visual_verdict(self):
        with tempfile.TemporaryDirectory() as temp:
            code, result = run(critique.main, [str(PROOF), '--no-frames', '--out', os.path.join(temp, 'c')])
            self.assertEqual((code, result['status']), (0, 'contract_only'))
            self.assertEqual(result['score'], 100, 'the contract rules alone pass')
            self.assertEqual(result['verdicts']['layout'], 'not_verified')
            self.assertTrue(result['verdicts']['text_completeness'].startswith('not_checked'))
            args = acceptance.argparse.Namespace(critique=os.path.join(temp, 'c', 'critique.json'), review=None, text_audit=None, video=None,
                                                  playback='not_watched', source_review=None, temporal_review=None, composition_review=None, note=None)
            decided = acceptance.decide(json.loads(PROOF.read_text()), args)
        self.assertEqual(decided['verdicts']['C_composition']['status'], 'not_verified')
        self.assertIn('contract_only', ' '.join(decided['verdicts']['C_composition']['findings']))
        self.assertNotEqual(decided['overall'], 'accepted')

    def test_clean_checks_do_not_replace_a_persons_judgement_of_the_frames(self):
        audit = {'verdict': 'pass', 'summary': {'textsChecked': 8}, 'samples': [{'t': 1, 'hold': True, 'exceptions': [], 'issues': [],
                 'texts': [{'text': v, 'visible': 'complete'} for v in json.loads(PROOF.read_text())['copy'].values()]}]}
        with tempfile.TemporaryDirectory() as temp:
            path = os.path.join(temp, 'audit.json')
            pathlib.Path(path).write_text(json.dumps(audit))
            base = dict(critique=None, review=None, text_audit=path, video=None, playback='watched', source_review='pass', temporal_review='pass', note='owner')
            unjudged = acceptance.decide(json.loads(PROOF.read_text()), acceptance.argparse.Namespace(**base, composition_review=None))
            weak = acceptance.decide(json.loads(PROOF.read_text()), acceptance.argparse.Namespace(**base, composition_review='fail'))
        self.assertEqual(unjudged['verdicts']['C_composition']['status'], 'not_verified')
        self.assertEqual(unjudged['verdicts']['B_fidelity']['status'], 'pass', unjudged['verdicts']['B_fidelity'])
        self.assertEqual((weak['verdicts']['C_composition']['status'], weak['overall']), ('fail', 'blocked'))

    def test_text_audit_errors_block_a_technically_valid_export(self):
        audit = {'verdict': 'fail', 'summary': {'textsChecked': 2}, 'samples': [{'t': 1, 'hold': True, 'exceptions': [],
                 'issues': [{'severity': 'error', 'check': 'text-cut', 'element': 'div.floor-word', 'text': 'TWÓJ WYBÓR', 'detail': 'cut: WYBÓR (61.6% visible)'}],
                 'texts': [{'text': 'TWÓJ WYBÓR', 'visible': 'partial'}]}]}
        with tempfile.TemporaryDirectory() as temp:
            path = os.path.join(temp, 'audit.json')
            pathlib.Path(path).write_text(json.dumps(audit))
            args = acceptance.argparse.Namespace(critique=None, review=None, text_audit=path, video=None, playback='watched',
                                                  source_review='pass', temporal_review='pass', composition_review='pass', note='owner, phone')
            decided = acceptance.decide(json.loads(PROOF.read_text()), args)
        self.assertEqual(decided['verdicts']['C_composition']['status'], 'fail')
        self.assertEqual(decided['overall'], 'blocked')
        self.assertIn('WYBÓR', ' '.join(decided['verdicts']['C_composition']['findings']))


class QualityGates(unittest.TestCase):
    """Phase 0 of the 2026-10 plan: the gates see cut words, empty vertical frames and every picture error."""

    def test_any_critique_picture_error_blocks_composition(self):
        found = {'status': 'issues', 'score': 85, 'frames': 'checked', 'findings': [
            {'severity': 'error', 'area': 'readability', 'where': 'desktop', 'message': '5 words held 2.00 s', 'fix': 'hold longer'}]}
        with tempfile.TemporaryDirectory() as temp:
            path = os.path.join(temp, 'critique.json')
            pathlib.Path(path).write_text(json.dumps(found))
            args = acceptance.argparse.Namespace(critique=path, review=None, text_audit=None, video=None, playback='watched',
                                                  source_review='pass', temporal_review='pass', composition_review='pass', note='owner')
            decided = acceptance.decide(json.loads(PROOF.read_text()), args)
        self.assertEqual((decided['verdicts']['C_composition']['status'], decided['overall']), ('fail', 'blocked'))

    @unittest.skipUnless(have_media(), 'needs Pillow and ffmpeg')
    def test_renderer_refuses_a_word_wider_than_its_column(self):
        scene = {'id': 'big', 'kind': 'line-reveal', 'start': 0, 'end': 30, 'holds': [[10, 30]], 'params': {'lines': ['w'], 'sizes': [200], 'weights': [700]}}
        contract = small_contract([scene], 30, {'w': 'Najnowocześniejszy'}, width=1080, height=1920)
        with tempfile.TemporaryDirectory() as temp:
            path = os.path.join(temp, 'c.json')
            pathlib.Path(path).write_text(json.dumps(contract, ensure_ascii=False))
            done = subprocess.run([sys.executable, '-B', str(PLUGIN / 'skills/hyperframes-workflow/assets/motion-render/render.py'), path, os.path.join(temp, 'c.mp4')],
                                  capture_output=True, text=True)
            self.assertEqual(done.returncode, 4, done.stderr)
            self.assertEqual(json.loads(done.stdout)['text_overflow'][0]['text'], 'Najnowocześniejszy')
            self.assertFalse(os.path.exists(os.path.join(temp, 'c.mp4')), 'nothing is rendered')

    def test_typography_keeps_one_letter_words_and_units_together(self):
        render = module('render', PLUGIN / 'skills/hyperframes-workflow/assets/motion-render/render.py')
        self.assertEqual(render.keep_together('Dostawa w godzinę za 90 zł, a 10 kg i 50 % z rabatem'),
                         'Dostawa w\u00a0godzinę za 90\u00a0zł, a\u00a010\u00a0kg i\u00a050\u00a0% z\u00a0rabatem')
        node = shutil.which('node')
        if node:
            engine = PLUGIN / 'skills/hyperframes-workflow/assets/motion-scenes/motion-scenes.mjs'
            for text in ('Dostawa w godzinę za 90 zł', 'I am a fan', 'Ż ó ł', '5 mln zł i 3 s.', 'A\nb c', 'Tylko 1 299 zł', '12 000 osób, 1 2345'):
                script = f'import({json.dumps(engine.as_uri())}).then(m => process.stdout.write(JSON.stringify(m.keepTogether(process.argv[1]))))'
                js = subprocess.run([node, '-e', script, text], capture_output=True, text=True, check=True).stdout
                self.assertEqual(json.loads(js), render.keep_together(text), text)

    def test_moving_average_matches_the_direct_convolution(self):
        try:
            import numpy as np
        except ImportError:
            self.skipTest('needs numpy')
        sys.path.insert(0, str(PLUGIN / 'skills/hyperframes-workflow/assets/motion-sound'))
        try:
            synth = module('synth_ma', PLUGIN / 'skills/hyperframes-workflow/assets/motion-sound/synth.py')
        finally:
            sys.path.pop(0)
        r = np.random.default_rng(3)
        for n, w in ((1000, 7), (5000, 480), (60000, 48000), (10, 48000), (4800, 4800), (5, 1)):
            x = r.random(n)
            for mode in ('valid', 'same', 'full'):
                self.assertTrue(np.allclose(synth.moving_average(x, w, mode), np.convolve(x, np.ones(w) / w, mode=mode), rtol=1e-9, atol=1e-12), (n, w, mode))

    @unittest.skipUnless(have_media(), 'needs Pillow and ffmpeg')
    def test_critique_flags_an_empty_vertical_frame(self):
        scene = {'id': 'tiny', 'kind': 'line-reveal', 'start': 0, 'end': 90, 'holds': [[20, 90]], 'params': {'lines': ['a'], 'sizes': [60], 'weights': [700]}}
        contract = small_contract([scene], 90, {'a': 'Say it'}, width=540, height=960)
        with tempfile.TemporaryDirectory() as temp:
            path = os.path.join(temp, 'c.json')
            pathlib.Path(path).write_text(json.dumps(contract))
            code, report = run(critique.main, [path])
        errors = [f for f in report['findings'] if f['area'] == 'composition' and f['severity'] == 'error']
        self.assertTrue(errors, report['findings'])
        self.assertEqual(len(errors), 1, 'reported once per scene and format')


class ContractRules(unittest.TestCase):
    def scenes(self):
        return [{'id': f's{i}', 'start': i * 60, 'end': (i + 1) * 60, 'holds': [[i * 60 + 10, i * 60 + 50]], 'copy': ['line'],
                 'transition': 'full-screen wipe to the next card'} for i in range(4)]

    def test_repeated_full_frame_wipes_are_flagged(self):
        c = critique.Critique(small_contract(self.scenes(), 240, {'line': 'Jeden zapach'}))
        c.timing()
        self.assertTrue(any(f['area'] == 'transitions' and 'wipe' in f['message'] for f in c.findings))

    def test_varied_carrier_transitions_are_not_flagged(self):
        scenes = self.scenes()
        for scene, transition in zip(scenes, ['bottle carries into the search field', 'search result grows into the product', 'cut on the price', 'end']):
            scene['transition'] = transition
        c = critique.Critique(small_contract(scenes, 240, {'line': 'Jeden zapach'}))
        c.timing()
        self.assertFalse(any(f['area'] == 'transitions' for f in c.findings))

    def test_opaque_photo_on_another_background_is_flagged(self):
        score = small_contract(self.scenes()[:1], 60, {'line': 'Jeden zapach'})
        score['assets'] = [{'id': 'bottle', 'file': 'bottle.jpg', 'background': '#FFFFFF', 'authority': 'client'}]
        score['scenes'][0]['assets'] = ['bottle']
        c = critique.Critique(score)
        c.timing()
        self.assertTrue(any(f['area'] == 'integration' and 'rectangle' in f['message'] for f in c.findings))
        score['scenes'][0]['params'] = {'background': '#FFFFFF'}
        c = critique.Critique(score)
        c.timing()
        self.assertFalse(any(f['area'] == 'integration' for f in c.findings))


@unittest.skipUnless(have_media(), 'needs Pillow, ffmpeg and ffprobe')
class Pacing(unittest.TestCase):
    def check(self, beats):
        score = small_contract([{'id': 'shelf', 'kind': 'line-reveal', 'params': {'lines': ['line']}, 'start': 0, 'end': 180, 'holds': [[10, 175]], 'copy': ['line']},
                                {'id': 'end', 'kind': 'end-card', 'params': {'text': 'end'}, 'start': 180, 'end': 210, 'holds': [[185, 210]], 'copy': ['end']}],
                               210, {'line': 'Jeden zapach?', 'end': 'Sklep'})
        with tempfile.TemporaryDirectory() as temp:
            video, contract = os.path.join(temp, 'v.mp4'), os.path.join(temp, 'v.motion.json')
            write_video(video, drift_frames(beats))
            pathlib.Path(contract).write_text(json.dumps(score))
            _, result = run(critique.main, [contract, '--video', video, '--out', os.path.join(temp, 'c')])
        return result

    def test_tiny_drift_is_not_counted_as_a_beat(self):
        result = self.check(beats=False)
        pace = [f for f in result['findings'] if f['area'] == 'pace' and f['where'] == 'shelf']
        self.assertTrue(pace and 'drift is not a new beat' in pace[0]['message'], result['findings'])
        shelf = next(p for p in result['pacing'] if p['scene'] == 'shelf')
        self.assertGreater(shelf['longest_still_s'], shelf['allowed_s'])
        self.assertGreater(shelf['largest_change_in_it'], 0, 'pixels did move: it is drift, not a frozen frame')

    def test_new_information_breaks_the_still_stretch(self):
        result = self.check(beats=True)
        self.assertFalse([f for f in result['findings'] if f['area'] == 'pace' and f['where'] == 'shelf'], result['findings'])

    def test_keyframes_are_saved_at_full_size_and_phone_scale(self):
        result = self.check(beats=True)
        labels = {k['label'] for k in result['keyframes']}
        self.assertTrue({'opening', 'densest', 'ending'} <= labels)
        self.assertTrue(all(k['phone'].endswith('-phone.png') for k in result['keyframes']))


@unittest.skipUnless(have_media(), 'needs Pillow, ffmpeg and ffprobe')
class Technical(unittest.TestCase):
    def test_export_is_checked_against_the_contract(self):
        score = json.loads(PROOF.read_text())
        with tempfile.TemporaryDirectory() as temp:
            video = os.path.join(temp, 'v.mp4')
            subprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i', 'color=c=0xF3EFE7:s=1080x1920:r=30:d=20', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', video], check=True)
            good = acceptance.technical(score, video)
            other = copy.deepcopy(score)
            other['width'], other['height'] = 1920, 1080
            wrong = acceptance.technical(other, video)
        self.assertEqual(good['status'], 'pass', good)
        self.assertEqual(wrong['status'], 'fail')


if __name__ == '__main__':
    unittest.main()
