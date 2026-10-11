"""Polish word timing for Animate voice-overs (animate-voice/retime.py): heard times land on the script's words with
Polish letters, missing words are filled in, and without a recogniser the estimate follows syllables and pauses."""
import importlib.util
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
TOOL = PLUGIN / 'skills/hyperframes-workflow/assets/animate-voice/retime.py'
spec = importlib.util.spec_from_file_location('retime', TOOL)
retime = importlib.util.module_from_spec(spec)
spec.loader.exec_module(retime)
LINES = [{'id': 'open', 'text': 'Miód z Beskidów, prosto z pasieki.', 't0': 0.8, 't1': 3.2, 'take': 'voice/open.wav'},
         {'id': 'offer', 'text': 'Zamów słoik w przedsprzedaży już dziś.', 't0': 3.6, 't1': 6.4, 'take': 'voice/offer.wav'}]


def piece(folder):
    path = pathlib.Path(folder, 'piece')
    path.mkdir()
    (path / 'voice.json').write_text(json.dumps({'duration': 7.9, 'lead': 0.8, 'tail': 1.5, 'lines': LINES}, ensure_ascii=False), encoding='utf-8')
    return path


def run(*args):
    done = subprocess.run([sys.executable, '-B', str(TOOL), *map(str, args)], capture_output=True, text=True, timeout=120)
    return done.returncode, done.stdout, done.stderr


class Retime(unittest.TestCase):
    def test_polish_letters_survive_matching(self):
        self.assertEqual(retime.norm('Słoik,'), 'słoik')
        self.assertEqual(retime.norm('PRZEDSPRZEDAŻY.'), 'przedsprzedaży')
        self.assertEqual([retime.syllables(w, 'pl') for w in ('w', 'nie', 'siedem', 'pociąg', 'przedsprzedaży', 'Beskidów')], [0, 1, 2, 2, 4, 3])

    def test_the_estimate_follows_syllables_and_pauses(self):
        with tempfile.TemporaryDirectory() as temp:
            path = piece(temp)
            code, out, err = run(path, '--language', 'pl', '--estimate')
            self.assertEqual(code, 0, err)
            voice = json.loads((path / 'voice.json').read_text(encoding='utf-8'))
            self.assertEqual(voice['wordTiming']['matched'], 0)
            first, second = voice['lines']
            self.assertEqual([w['w'] for w in first['words']], ['Miód', 'z', 'Beskidów,', 'prosto', 'z', 'pasieki.'])
            for line in voice['lines']:
                self.assertTrue(all(w['est'] for w in line['words']))
                self.assertTrue(line['t0'] <= line['words'][0]['t0'] and line['words'][-1]['t1'] <= line['t1'] + 0.001)
                self.assertTrue(all(a['t1'] <= b['t0'] + 0.001 for a, b in zip(line['words'], line['words'][1:])))
            span = {w['w']: w['t1'] - w['t0'] for w in second['words']}
            self.assertGreater(span['przedsprzedaży'], 3 * span['w'])
            # The comma after "Beskidów," holds a short pause before "prosto".
            words = first['words']
            self.assertGreater(words[3]['t0'] - words[2]['t1'], 0.05)

    def test_heard_times_land_on_the_script_and_gaps_are_filled(self):
        heard = [{'word': 'miód', 'start': 0.85, 'end': 1.2}, {'word': 'z', 'start': 1.22, 'end': 1.3}, {'word': 'beskidów', 'start': 1.32, 'end': 1.95},
                 {'word': 'prosto', 'start': 2.2, 'end': 2.55}, {'word': 'pasieki', 'start': 2.65, 'end': 3.15},
                 {'word': 'zamów', 'start': 3.62, 'end': 4.0}, {'word': 'słoik', 'start': 4.05, 'end': 4.4}, {'word': 'w', 'start': 4.42, 'end': 4.48},
                 {'word': 'przedsprzedarzy', 'start': 4.5, 'end': 5.4}, {'word': 'już', 'start': 5.5, 'end': 5.75}, {'word': 'dziś', 'start': 5.8, 'end': 6.3}]
        with tempfile.TemporaryDirectory() as temp:
            path = piece(temp)
            heard_file = pathlib.Path(temp, 'words.json')
            heard_file.write_text(json.dumps(heard, ensure_ascii=False), encoding='utf-8')
            code, out, err = run(path, '--language', 'pl', '--heard', heard_file)
            self.assertEqual(code, 0, err)
            summary = json.loads(out)
            self.assertEqual((summary['matched'], summary['words']), (10, 12))
            first, second = json.loads((path / 'voice.json').read_text(encoding='utf-8'))['lines']
            self.assertEqual((first['words'][2]['t0'], first['words'][2]['t1']), (1.32, 1.95))
            self.assertEqual((second['words'][1]['w'], second['words'][1]['t0']), ('słoik', 4.05))
            # "z" before "pasieki" was not heard: it fills the gap between its neighbours and stays marked.
            self.assertEqual(first['words'][4], {'w': 'z', 't0': 2.55, 't1': 2.65, 'est': True})
            # A misheard word (rz for ż) is filled between its neighbours too.
            self.assertEqual((second['words'][3]['t0'], second['words'][3]['t1'], second['words'][3]['est']), (4.48, 5.5, True))

    def test_missing_voice_json_is_an_input_error(self):
        with tempfile.TemporaryDirectory() as temp:
            code, _, err = run(pathlib.Path(temp, 'nothing'), '--estimate')
            self.assertEqual(code, 2)
            self.assertIn('voice.json', err)

    def test_without_a_recogniser_it_says_it_estimated(self):
        if importlib.util.find_spec('faster_whisper'):
            self.skipTest('faster-whisper is installed here')
        with tempfile.TemporaryDirectory() as temp:
            path = piece(temp)
            code, out, err = run(path, '--language', 'pl')
            self.assertEqual(code, 0, err)
            self.assertIn('faster-whisper is not installed', json.loads(out)['source'])


if __name__ == '__main__':
    unittest.main(verbosity=1)
