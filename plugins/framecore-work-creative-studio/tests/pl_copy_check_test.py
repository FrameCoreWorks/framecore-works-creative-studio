"""Tests for the Polish copy checker and the dated channel limits."""
import importlib.util
import json
import pathlib
import re
import subprocess
import sys
import unittest

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
TOOL = PLUGIN / 'skills/copy-voice/scripts/pl_copy_check.py'
spec = importlib.util.spec_from_file_location('pl_copy_check', TOOL)
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)


def codes(text, lines=False):
    return {item['code'] for item in check.check_text(text, lines)}


class Findings(unittest.TestCase):
    def test_typography_is_found_and_fixed_without_changing_a_word(self):
        text = 'Kup "Miód lipowy" - teraz... 5kg za 39 zł , super'
        self.assertTrue({'QUOTES_ASCII', 'HYPHEN_AS_DASH', 'ELLIPSIS', 'UNIT_SPACE', 'SPACE_BEFORE_PUNCTUATION'} <= codes(text))
        fixed = check.safe_fixes(text)
        self.assertEqual(fixed.replace(' ', ' '), 'Kup „Miód lipowy” – teraz… 5 kg za 39 zł, super')
        self.assertEqual(re.findall(r'[^\W\d_]+', fixed), re.findall(r'[^\W\d_]+', text.replace('5kg', '5 kg')))
        self.assertEqual(codes(fixed) & {'QUOTES_ASCII', 'HYPHEN_AS_DASH', 'ELLIPSIS', 'UNIT_SPACE', 'SPACE_BEFORE_PUNCTUATION'}, set())

    def test_formats_and_forms_of_address_are_left_to_a_person(self):
        found = check.check_text('Najlepsze Ceny W Mieście!! Kup teraz za 39.90 zł albo 12000 zł, zapraszamy Państwa w Poniedziałek 10/10/2026 o 6 PM.')
        kinds = {item['code']: item['kind'] for item in found}
        for code in ('TITLE_CASE', 'STACKED_PUNCTUATION', 'DECIMAL_POINT', 'THOUSANDS', 'ADDRESS_MIXED', 'CAPITALISED_DATE_WORD', 'DATE_SLASH', 'TIME_12H'):
            self.assertEqual(kinds.get(code), 'check', code)

    def test_clean_polish_copy_and_ordinary_numbers_raise_nothing(self):
        for text in ('Zamów miód lipowy z pasieki w Beskidach.', 'Spotkanie 10 października 2026 r. o 18:00, kod 31-123, tel. 123456789.',
                     'Cena 1 299 zł, rabat 30%. Najniższa cena z 30 dni: 1 499 zł.', 'Państwa zamówienie wyślemy jutro.'):
            self.assertEqual(codes(text), set(), text)

    def test_a_one_letter_word_at_a_line_end_is_reported_only_for_final_lines(self):
        text = 'Miód z pasieki w\nBeskidach'
        self.assertIn('ORPHAN_LETTER', codes(text, lines=True))
        self.assertNotIn('ORPHAN_LETTER', codes(text))


class Channels(unittest.TestCase):
    def test_limits_are_dated_and_match_the_snapshot(self):
        limits = json.loads((PLUGIN / 'skills/copy-voice/assets/channel-limits.json').read_text(encoding='utf-8'))
        snapshot = (PLUGIN / limits['snapshot']).read_text(encoding='utf-8')
        self.assertIn(f"Snapshot date: {limits['checked']}.", snapshot)
        self.assertEqual(limits['channels']['google-rsa-headline'], {'visible': 30, 'hard': 30, 'label': 'Google Ads RSA headline'})

    def test_over_a_hard_limit_exits_2(self):
        done = subprocess.run([sys.executable, str(TOOL), '--channel', 'google-rsa-headline', '--json', 'Miód lipowy prosto z pasieki w Beskidach'],
                              capture_output=True, text=True, timeout=60)
        self.assertEqual(done.returncode, 2)
        self.assertEqual(json.loads(done.stdout)['channel']['status'], 'over_hard_limit')
        done = subprocess.run([sys.executable, str(TOOL), '--channel', 'meta-primary-text', 'Miód lipowy z pasieki.'], capture_output=True, text=True, timeout=60)
        self.assertEqual(done.returncode, 0, done.stdout)


if __name__ == '__main__':
    unittest.main(verbosity=1)
