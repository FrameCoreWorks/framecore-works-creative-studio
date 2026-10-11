"""Voice-over budget check (copy-voice/scripts/vo_budget.py) against the short-form timing card."""
import importlib.util
import json
import pathlib
import re
import subprocess
import sys
import tempfile
import unittest

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
TOOL = PLUGIN / 'skills/copy-voice/scripts/vo_budget.py'
CARD = PLUGIN / 'skills/pipeline-core/references/short-form-timing.md'
spec = importlib.util.spec_from_file_location('vo_budget', TOOL)
vo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vo)


def run(text, *args):
    with tempfile.TemporaryDirectory() as temp:
        path = pathlib.Path(temp, 'script.txt')
        path.write_text(text, encoding='utf-8')
        done = subprocess.run([sys.executable, '-B', str(TOOL), str(path), *map(str, args)], capture_output=True, text=True, timeout=60)
        return done.returncode, done.stdout, done.stderr


class Card(unittest.TestCase):
    def test_the_tool_and_the_card_give_the_same_budgets(self):
        table = [line for line in CARD.read_text(encoding='utf-8').splitlines() if re.match(r'^\| \d+ s \|', line)]
        self.assertEqual(len(table), 5)
        for line in table:
            cells = [c.strip() for c in line.strip('|').split('|')]
            length = int(cells[0].split()[0])
            for language, column in (('en', 3), ('pl', 4)):
                expected = [int(n) for n in cells[column].split(' / ')]
                got = [vo.budget(length, language, rate)['max_words'] for rate in ('calm', 'standard', 'fast')]
                self.assertEqual(got, expected, (length, language))


class Scripts(unittest.TestCase):
    FITS = '[muzyka, plan ogólny pasieki]\nMiód z Beskidów, prosto z pasieki.\nZamów słoik w przedsprzedaży.\n# super: -20% do niedzieli\nDostawa w 24 godziny.'

    def test_a_short_polish_script_fits_fifteen_seconds(self):
        code, out, err = run(self.FITS, '--length', 15, '--language', 'pl')
        self.assertEqual(code, 0, err)
        result = json.loads(out)
        self.assertEqual((result['lines'], result['words']), (3, 14))
        self.assertTrue(result['fits'])
        self.assertLess(result['seconds'], result['budget']['spoken_seconds'])

    def test_a_long_script_is_over_and_says_how_much_to_cut(self):
        long = ' '.join(['Nasz miód zbieramy ręcznie w małej pasiece w Beskidach, z dala od pól i dróg.'] * 4)
        code, out, _ = run(long, '--length', 15, '--language', 'pl')
        self.assertEqual(code, 1)
        result = json.loads(out)
        self.assertFalse(result['fits'])
        self.assertRegex(result['advice'], r'cut about \d+ words')

    def test_polish_syllables_and_numbers(self):
        self.assertEqual([vo.syllables(w, 'pl') for w in ('w', 'nie', 'przedsprzedaży', '24')], [0, 1, 4, 4])

    def test_bad_input(self):
        self.assertEqual(subprocess.run([sys.executable, '-B', str(TOOL), '--length', '15'], capture_output=True).returncode, 2)


if __name__ == '__main__':
    unittest.main(verbosity=1)
