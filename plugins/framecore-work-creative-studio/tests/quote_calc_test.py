"""Tests for the offer calculator: the user's rates in, exact Polish money out, contradictions refused."""
import importlib.util
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
TOOL = PLUGIN / 'skills/brief-architect/scripts/quote_calc.py'
spec = importlib.util.spec_from_file_location('quote_calc', TOOL)
quote = importlib.util.module_from_spec(spec)
spec.loader.exec_module(quote)


def offer(**changes):
    data = {'language': 'pl', 'title': 'Test', 'currency': 'PLN', 'prices': 'net', 'vat': {'rate': 23}, 'rates': {'hour': 150, 'day': 1000},
            'packages': [{'name': 'A', 'items': [{'name': 'Logo', 'price': 1800}, {'name': 'Retusz', 'hours': 3}, {'name': 'Sesja', 'days': 0.5, 'qty': 2}],
                          'revisions': 2, 'timeline_days': 10}],
            'payment': {'advance_pct': 50, 'terms_days': 14}}
    data.update(changes)
    return data


class Pricing(unittest.TestCase):
    def test_net_prices_with_vat(self):
        package = quote.price(offer())['packages'][0]
        # 1800 + 3 x 150 + 2 x 0.5 x 1000 = 3250 net; VAT 23 % = 747.50; gross 3997.50; advance 1998.75
        self.assertEqual((package['net'], package['vat'], package['gross'], package['advance']), ('3250.00', '747.50', '3997.50', '1998.75'))
        self.assertEqual(Decimal(package['advance']) + Decimal(package['after_acceptance']), Decimal(package['gross']))

    def test_gross_prices_are_split_back_to_net(self):
        package = quote.price(offer(prices='gross', packages=[{'name': 'A', 'items': [{'name': 'Plakat', 'price': 1230}]}]))['packages'][0]
        self.assertEqual((package['net'], package['vat'], package['gross']), ('1000.00', '230.00', '1230.00'))

    def test_exemption_needs_its_basis_and_charges_no_vat(self):
        self.assertIn('vat.exempt needs the legal basis', ' '.join(quote.validate(offer(vat={'exempt': True}))))
        package = quote.price(offer(vat={'exempt': True, 'basis': 'art. 113 ust. 1 ustawy o VAT'}))['packages'][0]
        self.assertEqual((package['vat'], package['net'], package['gross']), ('0.00', '3250.00', '3250.00'))

    def test_discount_rounds_each_line_half_up(self):
        package = quote.price(offer(discount={'pct': 10}, packages=[{'name': 'A', 'items': [{'name': 'X', 'price': 99.99}]}]))['packages'][0]
        self.assertEqual(package['net'], '89.99')  # 89.991 -> 89.99

    def test_contradictions_are_refused(self):
        problems = quote.validate(offer(rates={}, payment={'advance_pct': 120}))
        joined = ' '.join(problems)
        self.assertIn('needs rates.hour', joined)
        self.assertIn('needs rates.day', joined)
        self.assertIn('advance_pct from 0 to 100', joined)
        self.assertIn('give exactly one of price, hours or days', ' '.join(quote.validate(offer(packages=[{'name': 'A', 'items': [{'name': 'X', 'price': 1, 'hours': 2}]}]))))

    def test_the_example_has_no_prices_of_its_own(self):
        example = quote.EXAMPLE
        self.assertEqual(example['rates'], {'hour': 0, 'day': 0})
        self.assertTrue(all(item.get('price', 0) == 0 for p in example['packages'] for item in p['items']))


class Document(unittest.TestCase):
    def test_polish_money_format_and_document(self):
        self.assertEqual(quote.fmt('1299', 'PLN', 'pl'), '1 299,00 zł')
        self.assertEqual(quote.fmt('1299', 'PLN', 'en'), 'PLN 1,299.00')
        with tempfile.TemporaryDirectory() as temp:
            path = pathlib.Path(temp, 'offer.quote.json')
            path.write_text(json.dumps(offer(), ensure_ascii=False), encoding='utf-8')
            done = subprocess.run([sys.executable, str(TOOL), str(path), '--markdown', str(pathlib.Path(temp, 'offer.md'))], capture_output=True, text=True, timeout=60)
            self.assertEqual(done.returncode, 0, done.stdout)
            text = pathlib.Path(temp, 'offer.md').read_text(encoding='utf-8')
            self.assertIn('3 997,50 zł', text)
            self.assertIn('Rundy poprawek w cenie: 2', text)
            self.assertIn('50% zaliczka', text)
            self.assertIn('nie stanowią porady prawnej', text)

    def test_bad_spec_exits_3_with_reasons(self):
        with tempfile.TemporaryDirectory() as temp:
            path = pathlib.Path(temp, 'bad.json')
            path.write_text(json.dumps({'packages': []}), encoding='utf-8')
            done = subprocess.run([sys.executable, str(TOOL), str(path)], capture_output=True, text=True, timeout=60)
            self.assertEqual(done.returncode, 3)
            self.assertEqual(json.loads(done.stdout)['status'], 'invalid_spec')


if __name__ == '__main__':
    unittest.main(verbosity=1)
