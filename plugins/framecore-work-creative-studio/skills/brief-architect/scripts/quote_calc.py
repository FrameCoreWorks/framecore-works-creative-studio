#!/usr/bin/env python3
"""Price a creative offer from the user's own rates: packages, extras, discount, VAT or exemption, advance payment.

  python3 quote_calc.py offer.quote.json                     # totals as JSON
  python3 quote_calc.py offer.quote.json --markdown offer.md # the offer document in the spec's language (pl or en)
  python3 quote_calc.py --example > offer.quote.json         # a starting spec to edit

Every rate, price, VAT status and term comes from the spec, which the user fills in; the tool holds no prices of its
own. Amounts are computed with decimal arithmetic and rounded half up to the grosz per line. It checks the spec and
stops with exit code 3 and the reasons when something is missing or contradictory (an hourly item without an hourly
rate, a VAT exemption without its legal basis, an advance above 100 %). It does not give tax or legal advice: the VAT
status, the exemption basis, the licence wording and the payment terms are the user's decisions.
"""
import argparse
import json
import sys
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

GROSZ = Decimal('0.01')
LABELS = {
    'pl': {'title': 'Oferta', 'package': 'Pakiet', 'item': 'Pozycja', 'qty': 'Ilość', 'unit_price': 'Cena jedn. netto', 'net': 'Netto',
           'vat': 'VAT', 'gross': 'Brutto', 'total': 'Razem', 'revisions': 'Rundy poprawek w cenie', 'timeline': 'Termin realizacji',
           'days': 'dni roboczych', 'licence': 'Licencja i pola eksploatacji', 'extras': 'Opcje dodatkowe', 'discount': 'Rabat',
           'payment': 'Płatność', 'advance': 'zaliczka', 'after': 'po odbiorze', 'terms': 'termin płatności', 'valid': 'Oferta ważna do',
           'exempt': 'zw.', 'hours': 'godz.', 'not_included': 'Poza zakresem', 'assumptions': 'Założenia', 'change': 'Zmiany zakresu',
           'change_rule': 'Prace poza zakresem i rundy poprawek ponad liczbę w cenie wyceniamy osobno przed ich rozpoczęciem.',
           'counsel': 'Treść licencji i warunki umowy wymagają akceptacji obu stron; nie stanowią porady prawnej.'},
    'en': {'title': 'Offer', 'package': 'Package', 'item': 'Item', 'qty': 'Qty', 'unit_price': 'Unit price (net)', 'net': 'Net',
           'vat': 'VAT', 'gross': 'Gross', 'total': 'Total', 'revisions': 'Revision rounds included', 'timeline': 'Delivery time',
           'days': 'working days', 'licence': 'Licence and fields of use', 'extras': 'Options', 'discount': 'Discount',
           'payment': 'Payment', 'advance': 'advance', 'after': 'on acceptance', 'terms': 'payment term', 'valid': 'Valid until',
           'exempt': 'exempt', 'hours': 'h', 'not_included': 'Not included', 'assumptions': 'Assumptions', 'change': 'Changes of scope',
           'change_rule': 'Work outside this scope and revision rounds beyond those included are quoted separately before they start.',
           'counsel': 'The licence text and contract terms need both parties\' agreement; this is not legal advice.'},
}


class SpecError(Exception):
    pass


def money(value):
    return Decimal(str(value)).quantize(GROSZ, rounding=ROUND_HALF_UP)


def fmt(amount, currency, lang):
    """1 299,00 zł in Polish, PLN 1,299.00 in English."""
    q = money(amount)
    whole, frac = f'{abs(q):.2f}'.split('.')
    groups = []
    while whole:
        groups.insert(0, whole[-3:])
        whole = whole[:-3]
    sign = '-' if q < 0 else ''
    if lang == 'pl':
        symbol = 'zł' if currency == 'PLN' else currency
        nbsp = ' '  # outside the f-string expression for Python 3.11
        return sign + nbsp.join(groups) + ',' + frac + nbsp + symbol
    return f"{sign}{currency} {','.join(groups)}.{frac}"


def need(condition, problems, message):
    if not condition:
        problems.append(message)


def validate(spec):
    problems = []
    need(spec.get('language', 'pl') in LABELS, problems, 'language must be pl or en')
    need(isinstance(spec.get('currency', 'PLN'), str) and len(spec.get('currency', 'PLN')) == 3, problems, 'currency is a three-letter code such as PLN')
    vat = spec.get('vat')
    need(isinstance(vat, dict), problems, 'vat: give {"rate": 23} or {"exempt": true, "basis": "..."} (the user decides which applies)')
    if isinstance(vat, dict):
        if vat.get('exempt'):
            need(bool(str(vat.get('basis', '')).strip()), problems, 'vat.exempt needs the legal basis the user relies on, for example "art. 113 ust. 1 ustawy o VAT"')
        else:
            need(isinstance(vat.get('rate'), (int, float)) and 0 <= vat['rate'] <= 100, problems, 'vat.rate is a percentage from 0 to 100')
    need(spec.get('prices', 'net') in ('net', 'gross'), problems, 'prices is "net" or "gross"')
    rates = spec.get('rates', {})
    packages = spec.get('packages')
    need(isinstance(packages, list) and packages, problems, 'packages: at least one package')
    for p_index, package in enumerate(packages or []):
        where = f'packages[{p_index}] {package.get("name", "")}'.strip()
        need(bool(package.get('name')), problems, f'{where}: name')
        need(isinstance(package.get('items'), list) and package['items'], problems, f'{where}: items')
        for i_index, item in enumerate(package.get('items') or []):
            label = f'{where} item {i_index + 1}'
            kinds = [k for k in ('price', 'hours', 'days') if k in item]
            need(len(kinds) == 1, problems, f'{label}: give exactly one of price, hours or days')
            if 'hours' in item:
                need('hour' in rates, problems, f'{label}: an hourly item needs rates.hour')
            if 'days' in item:
                need('day' in rates, problems, f'{label}: a day item needs rates.day')
            for key in ('price', 'hours', 'days', 'qty'):
                if key in item:
                    need(isinstance(item[key], (int, float)) and item[key] >= 0, problems, f'{label}: {key} must be a number of zero or more')
        need(isinstance(package.get('revisions', 0), int) and package.get('revisions', 0) >= 0, problems, f'{where}: revisions is a whole number')
    for extra in spec.get('extras', []):
        need(('price' in extra) != ('surcharge_pct' in extra), problems, f'extra {extra.get("name", "")}: price or surcharge_pct')
    discount = spec.get('discount', {})
    if discount:
        need(0 < discount.get('pct', 0) < 100, problems, 'discount.pct between 0 and 100')
    payment = spec.get('payment', {})
    need(0 <= payment.get('advance_pct', 0) <= 100, problems, 'payment.advance_pct from 0 to 100')
    return problems


def line_amount(item, rates):
    qty = Decimal(str(item.get('qty', 1)))
    if 'price' in item:
        unit = Decimal(str(item['price']))
    elif 'hours' in item:
        unit = Decimal(str(item['hours'])) * Decimal(str(rates['hour']))
    else:
        unit = Decimal(str(item['days'])) * Decimal(str(rates['day']))
    return money(unit), money(unit * qty)


def split(amount, vat, prices):
    """(net, vat, gross) of one line amount entered as net or gross."""
    if vat.get('exempt'):
        return amount, money(0), amount
    rate = Decimal(str(vat['rate'])) / 100
    if prices == 'net':
        tax = money(amount * rate)
        return amount, tax, amount + tax
    net = money(amount / (1 + rate))
    return net, amount - net, amount


def price(spec):
    vat, prices, rates = spec['vat'], spec.get('prices', 'net'), spec.get('rates', {})
    discount = Decimal(str(spec.get('discount', {}).get('pct', 0))) / 100
    result = []
    for package in spec['packages']:
        lines, sums = [], [Decimal(0)] * 3
        for item in package['items']:
            unit, amount = line_amount(item, rates)
            if discount:
                amount = money(amount * (1 - discount))
            net, tax, gross = split(amount, vat, prices)
            sums = [sums[0] + net, sums[1] + tax, sums[2] + gross]
            lines.append({'name': item['name'], 'qty': item.get('qty', 1), 'unit': item.get('unit', ''), 'hours': item.get('hours'), 'days': item.get('days'),
                          'unit_amount': str(unit), 'net': str(net), 'vat': str(tax), 'gross': str(gross)})
        advance = Decimal(str(spec.get('payment', {}).get('advance_pct', 0))) / 100
        total_gross = sums[2]
        result.append({'name': package['name'], 'lines': lines, 'net': str(sums[0]), 'vat': str(sums[1]), 'gross': str(total_gross),
                       'advance': str(money(total_gross * advance)), 'after_acceptance': str(total_gross - money(total_gross * advance)),
                       'revisions': package.get('revisions', 0), 'timeline_days': package.get('timeline_days'), 'licence': package.get('licence', ''),
                       'not_included': package.get('not_included', [])})
    extras = []
    for extra in spec.get('extras', []):
        if 'price' in extra:
            net, tax, gross = split(money(extra['price']), vat, prices)
            extras.append({'name': extra['name'], 'net': str(net), 'vat': str(tax), 'gross': str(gross)})
        else:
            extras.append({'name': extra['name'], 'surcharge_pct': extra['surcharge_pct']})
    return {'currency': spec.get('currency', 'PLN'), 'prices_entered': prices,
            'vat': {'exempt': True, 'basis': vat['basis']} if vat.get('exempt') else {'rate': vat['rate']},
            'discount_pct': spec.get('discount', {}).get('pct'), 'packages': result, 'extras': extras}


def markdown(spec, totals):
    lang = spec.get('language', 'pl')
    t, cur = LABELS[lang], totals['currency']
    vat_label = f"{t['vat']} {t['exempt']} ({totals['vat']['basis']})" if totals['vat'].get('exempt') else f"{t['vat']} {totals['vat']['rate']}%"
    out = [f"# {t['title']}: {spec.get('title', '')}".rstrip(': '), '']
    if spec.get('client') or spec.get('provider'):
        out += [f"{spec.get('provider', '')}  \n{spec.get('client', '')}".strip(), '']
    if spec.get('summary'):
        out += [spec['summary'], '']
    for package in totals['packages']:
        out += [f"## {t['package']}: {package['name']}", '', f"| {t['item']} | {t['qty']} | {t['unit_price']} | {t['net']} | {vat_label} | {t['gross']} |", '| --- | --- | --- | --- | --- | --- |']
        for line in package['lines']:
            qty = f"{line['qty']} {line['unit']}".strip()
            if line['hours'] is not None:
                qty = f"{line['hours']} {t['hours']}"
            out.append(f"| {line['name']} | {qty} | {fmt(line['unit_amount'], cur, lang)} | {fmt(line['net'], cur, lang)} | {fmt(line['vat'], cur, lang)} | {fmt(line['gross'], cur, lang)} |")
        out.append(f"| **{t['total']}** | | | **{fmt(package['net'], cur, lang)}** | **{fmt(package['vat'], cur, lang)}** | **{fmt(package['gross'], cur, lang)}** |")
        out.append('')
        facts = [f"- {t['revisions']}: {package['revisions']}"]
        if package['timeline_days']:
            facts.append(f"- {t['timeline']}: {package['timeline_days']} {t['days']}")
        if package['licence']:
            facts.append(f"- {t['licence']}: {package['licence']}")
        if package['not_included']:
            facts.append(f"- {t['not_included']}: " + '; '.join(package['not_included']))
        out += facts + ['']
    if totals['extras']:
        out += [f"## {t['extras']}", '']
        for extra in totals['extras']:
            value = f"+{extra['surcharge_pct']}%" if 'surcharge_pct' in extra else f"{fmt(extra['net'], cur, lang)} {t['net'].lower()} / {fmt(extra['gross'], cur, lang)} {t['gross'].lower()}"
            out.append(f"- {extra['name']}: {value}")
        out.append('')
    payment = spec.get('payment', {})
    if payment:
        parts = []
        if payment.get('advance_pct'):
            parts.append(f"{payment['advance_pct']}% {t['advance']}, {100 - payment['advance_pct']}% {t['after']}")
        if payment.get('terms_days'):
            parts.append(f"{t['terms']} {payment['terms_days']} dni" if lang == 'pl' else f"{t['terms']} {payment['terms_days']} days")
        out += [f"**{t['payment']}:** " + '; '.join(parts), '']
    if spec.get('valid_until'):
        out += [f"**{t['valid']}:** {spec['valid_until']}", '']
    if spec.get('assumptions'):
        out += [f"## {t['assumptions']}", ''] + [f'- {a}' for a in spec['assumptions']] + ['']
    out += [f"## {t['change']}", '', t['change_rule'], '', f"_{t['counsel']}_", '']
    return '\n'.join(out)


EXAMPLE = {
    'language': 'pl', 'title': 'Identyfikacja wizualna kawiarni', 'currency': 'PLN', 'prices': 'net',
    'vat': {'rate': 23}, 'rates': {'hour': 0, 'day': 0},
    'summary': 'Logo, podstawowe zasady identyfikacji i trzy materiały startowe dla nowej kawiarni.',
    'packages': [
        {'name': 'Podstawowy', 'items': [{'name': 'Logo: 2 kierunki, wybrany dopracowany', 'price': 0}, {'name': 'Karta marki (kolory, fonty, użycie logo)', 'price': 0}],
         'revisions': 2, 'timeline_days': 10, 'licence': 'przeniesienie autorskich praw majątkowych do logo na polach eksploatacji wymienionych w umowie, po zapłacie', 'not_included': ['druk', 'zdjęcia']},
        {'name': 'Rozszerzony', 'items': [{'name': 'Wszystko z pakietu Podstawowy', 'price': 0}, {'name': 'Menu A4, plakat A3, 3 grafiki do social mediów', 'price': 0}],
         'revisions': 3, 'timeline_days': 15, 'licence': 'jak w pakiecie Podstawowy, także dla materiałów'},
    ],
    'extras': [{'name': 'Dodatkowa runda poprawek', 'price': 0}, {'name': 'Tryb ekspresowy', 'surcharge_pct': 30}],
    'payment': {'advance_pct': 50, 'terms_days': 14}, 'valid_until': 'RRRR-MM-DD',
    'assumptions': ['Materiały (teksty, zdjęcia) dostarcza klient.'],
}


def main(argv=None):
    parser = argparse.ArgumentParser(description='Price a creative offer from the user\'s own rates.')
    parser.add_argument('spec', nargs='?')
    parser.add_argument('--markdown', help='write the offer document here')
    parser.add_argument('--example', action='store_true', help='print a starting spec with zero prices to fill in')
    args = parser.parse_args(argv)
    if args.example:
        print(json.dumps(EXAMPLE, indent=2, ensure_ascii=False))
        return 0
    if not args.spec:
        parser.error('give a quote spec or --example')
    try:
        spec = json.loads(Path(args.spec).read_text(encoding='utf-8'))
    except (OSError, ValueError) as error:
        print(json.dumps({'status': 'invalid_spec', 'problems': [str(error)]}, ensure_ascii=False))
        return 3
    problems = validate(spec)
    if problems:
        print(json.dumps({'status': 'invalid_spec', 'problems': problems}, indent=2, ensure_ascii=False))
        return 3
    totals = price(spec)
    if args.markdown:
        Path(args.markdown).write_text(markdown(spec, totals), encoding='utf-8')
        totals['document'] = args.markdown
    print(json.dumps({'status': 'ok', **totals}, indent=2, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
