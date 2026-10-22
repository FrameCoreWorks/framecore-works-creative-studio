"""Script-aware captions: alignment of a known script to timed speech, phrase-aware cue grouping and a caption-font glyph check.

Methods adapted from a review of MoneyPrinterTurbo (MIT): the script is the authority on spelling, speech recognition on timing,
and every guess is reported, never hidden."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
RUNTIME = PACKAGE / 'skills/opencut-video-studio/assets/framecut'
sys.path.insert(0, str(RUNTIME))
from fc_core import FrameCutError, commit_revision, read_json
from fc_media import ffmpeg, ingest
from framecut import project_init

CLI = RUNTIME / 'framecut.py'


def heard(text, start=0.5, step=0.45, length=0.35):
    return [{'id': f'h{i:03d}', 'text': word, 'start': round(start + i * step, 3), 'end': round(start + i * step + length, 3)}
            for i, word in enumerate(text.split())]


class Alignment(unittest.TestCase):
    def test_script_spelling_with_speech_timing_and_gaps_interpolated(self):
        from fc_align import align_script
        script = 'Pan Kowalski mieszka w Łodzi i lubi ćwiczyć.'
        words = heard('pan kowalsky mieszka w lodzi lubi cwiczyc')   # "i" was not heard; diacritics and a name misrecognised
        result = align_script(words, script)
        self.assertEqual([w['text'] for w in result['words']], script.split())
        self.assertGreaterEqual(result['report']['coverage'], 0.85)
        self.assertEqual(result['report']['unaligned'], [])
        starts = [w['start'] for w in result['words']]
        self.assertEqual(starts, sorted(starts))
        by_text = {w['text']: w for w in result['words']}
        self.assertEqual(by_text['Kowalski']['start'], words[1]['start'])
        self.assertEqual(by_text['Kowalski']['verbatim'], 'kowalsky')
        interpolated = by_text['i']
        self.assertEqual(interpolated['alignment'], 'interpolated')
        self.assertGreater(interpolated['start'], by_text['Łodzi']['end'] - 1e-9)
        self.assertLess(interpolated['end'], by_text['lubi']['start'] + 1e-9)

    def test_words_that_cannot_be_anchored_are_reported_not_guessed(self):
        from fc_align import align_script
        words = heard('dzień dobry państwu')
        result = align_script(words, 'Szanowni zebrani, dzień dobry państwu.')
        edge = result['words'][0]
        self.assertIsNone(edge['start'])
        self.assertEqual([x['text'] for x in result['report']['unaligned']][:1], ['Szanowni'])
        self.assertLess(result['report']['coverage'], 1.0)

    def test_a_script_that_does_not_match_the_speech_is_refused(self):
        from fc_align import align_script
        with self.assertRaises(FrameCutError) as caught:
            align_script(heard('zupełnie inna wypowiedź o pogodzie'), 'Dzisiaj omawiamy budżet na kolejny kwartał w naszym dziale.', minimum=0.6)
        self.assertEqual(caught.exception.code, 'qa_failed')
        self.assertIn('matched', str(caught.exception))

    def test_repeated_phrases_stay_in_order(self):
        from fc_align import align_script
        script = 'raz dwa trzy raz dwa trzy raz dwa trzy'
        result = align_script(heard(script), script)
        starts = [w['start'] for w in result['words']]
        self.assertEqual(starts, sorted(starts))
        self.assertEqual(result['report']['coverage'], 1.0)


class Command(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures = tempfile.TemporaryDirectory()
        cls.source = Path(cls.fixtures.name) / 'source.mp4'
        ffmpeg(['-f', 'lavfi', '-i', 'color=gray:s=320x180:r=30:d=6', '-f', 'lavfi', '-i', 'sine=frequency=300:sample_rate=48000:duration=6',
                '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', str(cls.source)])

    @classmethod
    def tearDownClass(cls):
        cls.fixtures.cleanup()

    def test_align_script_rewrites_the_analysis_with_the_scripts_spelling(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copy2(self.source, root / 'source.mp4')
            project = project_init(root / 'project.json', 'speech')
            project['assets']['a'] = ingest(root, 'source.mp4', 'a')
            words = heard('dzien dobry wszystkim dzisiaj pokaze wam nowy magazyn')
            project['analyses']['a'] = {'source_hash': project['assets']['a']['sha256'], 'engine': 'test', 'timing': 'asr_word', 'language': 'pl',
                                        'words': [{**w, 'verbatim': w['text'], 'speaker': None, 'confidence': None} for w in words],
                                        'segments': [], 'limitations': []}
            commit_revision(root / 'project.json', project, 1, 'asr')
            (root / 'script.txt').write_text('Dzień dobry wszystkim! Dzisiaj pokażę wam nowy magazyn.', encoding='utf-8')
            done = subprocess.run([sys.executable, '-B', str(CLI), 'align-script', str(root / 'project.json'), '--asset', 'a',
                                   '--script', str(root / 'script.txt'), '--base-revision', '2'], capture_output=True, text=True, timeout=120)
            self.assertEqual(done.returncode, 0, done.stderr)
            report = json.loads(done.stdout)
            self.assertEqual(report['status'], 'aligned')
            self.assertGreaterEqual(report['coverage'], 0.9)
            saved = read_json(root / 'project.json')
            self.assertEqual(saved['revision'], 3)
            self.assertEqual([w['text'] for w in saved['analyses']['a']['words']][:3], ['Dzień', 'dobry', 'wszystkim!'])

    def test_align_script_needs_word_timing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copy2(self.source, root / 'source.mp4')
            project = project_init(root / 'project.json', 'speech')
            project['assets']['a'] = ingest(root, 'source.mp4', 'a')
            project['analyses']['a'] = {'source_hash': project['assets']['a']['sha256'], 'engine': 'test', 'timing': 'segment', 'language': 'pl',
                                        'words': [], 'segments': [{'id': 's1', 'text': 'Dzień dobry', 'start': 0.5, 'end': 1.5}], 'limitations': []}
            commit_revision(root / 'project.json', project, 1, 'asr')
            (root / 'script.txt').write_text('Dzień dobry', encoding='utf-8')
            done = subprocess.run([sys.executable, '-B', str(CLI), 'align-script', str(root / 'project.json'), '--asset', 'a',
                                   '--script', str(root / 'script.txt'), '--base-revision', '2'], capture_output=True, text=True, timeout=120)
            self.assertEqual(done.returncode, 2)
            self.assertIn('word timing', done.stderr)


class Grouping(unittest.TestCase):
    def groups(self, text, language='pl', max_words=4):
        from fc_captions import project_captions
        words = [{'id': f'w{i:03d}', 'text': w, 'start': round(i * 0.4, 3), 'end': round(i * 0.4 + 0.3, 3)} for i, w in enumerate(text.split())]
        project = {'revision': 1, 'brief': {'language': language}, 'assets': {'a': {'probe': {'time_base': '1/1000', 'clock': {'num': 1, 'den': 1000},
                   'start_pts': 0, 'duration': 30, 'has_audio': True}, 'sha256': 'a' * 64}},
                   'analyses': {'a': {'source_hash': 'a' * 64, 'timing': 'aligned', 'words': words}}}
        seq = {'id': 'main', 'fps': {'num': 30, 'den': 1}, 'duration': 600, 'captions': {'enabled': True, 'max_words': max_words},
               'clips': [{'id': 'c1', 'asset': 'a', 'start': 0, 'duration': 600, 'source_in': 0}]}
        return [[w['text'] for w in group] for group in project_captions(project, seq)['groups']]

    def test_a_cue_never_ends_on_a_polish_one_letter_word(self):
        groups = self.groups('Rozmawiałem z kierownikiem w magazynie i okazało się że wszystko działa')
        for group in groups[:-1]:
            self.assertNotIn(group[-1].lower(), {'w', 'z', 'i', 'a', 'o', 'u'}, groups)

    def test_a_cue_breaks_at_the_comma_when_it_has_to_break(self):
        groups = self.groups('Najpierw przyjmujemy towar, potem go kontrolujemy i składujemy na półkach', max_words=5)
        self.assertTrue(any(group[-1].endswith(',') for group in groups), groups)


class Glyphs(unittest.TestCase):
    def test_missing_glyphs_are_found_and_polish_letters_are_not_flagged(self):
        from fc_captions import missing_glyphs
        from PIL import ImageFont
        path = subprocess.run(['fc-match', '-f', '%{file}', 'DejaVu Sans'], capture_output=True, text=True).stdout
        if not path or not Path(path).is_file():
            self.skipTest('DejaVu Sans is not installed')
        font = ImageFont.truetype(path, 40)
        self.assertEqual(missing_glyphs(font, 'Zażółć gęślą jaźń ĄĆĘŁŃÓŚŹŻ'), [])
        self.assertEqual(missing_glyphs(font, 'zażółć 漢'), ['漢'])


class FontWarning(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures = tempfile.TemporaryDirectory()
        cls.source = Path(cls.fixtures.name) / 'source.mp4'
        ffmpeg(['-f', 'lavfi', '-i', 'color=gray:s=320x180:r=30:d=3', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', str(cls.source)])

    @classmethod
    def tearDownClass(cls):
        cls.fixtures.cleanup()

    def project(self, root, text):
        from fc_render import compile_project
        shutil.copy2(self.source, root / 'source.mp4')
        project = project_init(root / 'project.json', 'font')
        project['assets']['a'] = ingest(root, 'source.mp4', 'a')
        project['analyses']['a'] = {'source_hash': project['assets']['a']['sha256'], 'timing': 'aligned', 'words': [
            {'id': 'w1', 'text': text, 'start': 0.2, 'end': 1.2}]}
        project['sequences'] = [{'id': 'main', 'fps': {'num': 30, 'den': 1}, 'duration': 60, 'captions': {'enabled': True},
                                 'clips': [{'id': 'c1', 'asset': 'a', 'start': 0, 'duration': 60, 'source_in': 0}]}]
        project['deliverables'] = [{'id': 'wide', 'sequence': 'main', 'width': 320, 'height': 180}]
        project['authorization'] = 'Authorized synthetic font test'
        return project, compile_project

    def test_a_caption_character_the_font_cannot_draw_is_reported_and_blocks_a_final(self):
        from fc_render import render
        if not shutil.which('fc-match'):
            self.skipTest('fontconfig is not installed')
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project, compile_project = self.project(root, 'Zażółć漢')
            warnings = [w for w in compile_project(project, root, 'wide')['warnings'] if w['code'] == 'font_missing_glyphs']
            self.assertEqual([w['chars'] for w in warnings], [['漢']])
            with self.assertRaises(FrameCutError) as caught:
                render(project, root, 'wide', 'final-out', mode='final', max_disk_mb=128)
            self.assertIn('font_missing_glyphs', str(caught.exception))

    def test_polish_letters_in_the_default_font_pass(self):
        if not shutil.which('fc-match'):
            self.skipTest('fontconfig is not installed')
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project, compile_project = self.project(root, 'Zażółć gęślą jaźń')
            codes = [w['code'] for w in compile_project(project, root, 'wide')['warnings']]
            self.assertNotIn('font_missing_glyphs', codes)


if __name__ == '__main__':
    unittest.main()
