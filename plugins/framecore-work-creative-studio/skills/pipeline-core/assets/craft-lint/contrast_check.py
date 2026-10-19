#!/usr/bin/env python3
"""WCAG 2.x contrast between two colours: the ratio and a verdict for body text, large text and interface parts.

  python3 contrast_check.py "#FFFFFF" "#777777"        # text colour, then background
  python3 contrast_check.py 1d1d1b f7f3ec --json
  python3 contrast_check.py --selftest                  # recompute the reference pairs below

Body text needs 4.5:1, large text (24 px regular or 18.5 px bold and up) and interface parts (borders, icons, focus
rings, chart segments) 3:1. The unrounded ratio is compared, so 4.498 fails 4.5 even though it prints as 4.50. Never
assert that a grey pair passes by eye: compute it. Text over a photo or gradient is checked at its worst spot.
Adapted from anti-slop's contrast-check.py (MIT). Standard library only.
Exit codes: 0 body text passes, 1 it fails, 2 bad input.
"""
import argparse
import json
import re
import sys

NAMED = {'black': (0, 0, 0), 'white': (255, 255, 255)}
REFERENCE = [('#000000', '#ffffff', 21.0), ('#ffffff', '#333333', 12.63), ('#ffffff', '#666666', 5.74),
             ('#777777', '#ffffff', 4.48), ('#777777', '#070707', 4.50), ('#ffffff', '#888888', 3.54),
             ('#ffffff', '#999999', 2.85), ('#555555', '#000000', 2.82)]


def parse(value):
    value = value.strip().lower()
    if value in NAMED:
        return NAMED[value]
    value = value.lstrip('#')
    if len(value) == 3:
        value = ''.join(c * 2 for c in value)
    if not re.fullmatch(r'[0-9a-f]{6}', value):
        raise ValueError(f'expected a colour like #1d1d1b, got {value!r}')
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def luminance(rgb):
    def channel(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (channel(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(fg, bg):
    a, b = sorted((luminance(parse(fg)), luminance(parse(bg))), reverse=True)
    return (a + 0.05) / (b + 0.05)


def verdict(fg, bg):
    r = ratio(fg, bg)
    return {'foreground': fg, 'background': bg, 'ratio': round(r, 2), 'body_text': r >= 4.5, 'large_text': r >= 3.0, 'ui_parts': r >= 3.0}


def main(argv=None):
    parser = argparse.ArgumentParser(description='WCAG contrast between two colours.')
    parser.add_argument('colours', nargs='*', help='foreground then background')
    parser.add_argument('--selftest', action='store_true')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args(argv)
    if args.selftest:
        bad = [(f, b, round(ratio(f, b), 2), e) for f, b, e in REFERENCE if abs(round(ratio(f, b), 2) - e) > 0.005]
        print('contrast_check: selftest ' + ('PASS' if not bad else f'FAIL {bad}'))
        return 1 if bad else 0
    if len(args.colours) != 2:
        print('contrast_check: give a foreground and a background colour', file=sys.stderr)
        return 2
    try:
        v = verdict(*args.colours)
    except ValueError as error:
        print(f'contrast_check: {error}', file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(v))
    else:
        mark = lambda ok: 'PASS' if ok else 'FAIL'
        print(f"{v['foreground']} on {v['background']}: {v['ratio']}:1  body text {mark(v['body_text'])} (4.5)  "
              f"large text {mark(v['large_text'])} (3.0)  interface parts {mark(v['ui_parts'])} (3.0)")
    return 0 if v['body_text'] else 1


if __name__ == '__main__':
    sys.exit(main())
