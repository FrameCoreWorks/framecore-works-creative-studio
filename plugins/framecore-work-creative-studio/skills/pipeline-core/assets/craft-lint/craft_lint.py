#!/usr/bin/env python3
"""Flag machine-made design tells in HTML, CSS and SVG artifacts: the checkable part of craft-rules.md.

  python3 craft_lint.py page.html                 # findings, P0 (must fix) first
  python3 craft_lint.py deck.html styles.css logo.svg --json
  python3 craft_lint.py page.html --allow ai-default-indigo   # the brand kit really uses indigo

P0: ai-default-indigo, purple-gradient, trust-gradient, emoji-icon, sans-display, left-accent-card, invented-metric,
filler-copy. P1: all-caps-no-tracking, raw-hex, accent-overuse, placeholder-image. Colours defined as custom properties
(`--accent: #6366f1`) are the brand's tokens and are not flagged; hard-coded uses are. Copy checks read visible text in
English and Polish. A finding is a prompt to look, not a verdict: `--allow ID` records a deliberate exception.

Adapted from Open Design's lint-artifact (Apache-2.0), whose rules adapt refero_skill (MIT). Python standard library only.
Exit codes: 0 no P0 finding, 1 at least one P0 finding, 2 unreadable input.
"""
import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

INDIGO = ['#6366f1', '#4f46e5', '#4338ca', '#3730a3', '#8b5cf6', '#7c3aed', '#a855f7']
PURPLE = INDIGO + ['#9333ea', '#6d28d9', '#581c87', '#a78bfa', '#c4b5fd', '#312e81', '#818cf8', '#a5b4fc']
BLUE = ['#3b82f6', '#2563eb', '#1d4ed8', '#1e40af', '#1e3a8a', '#60a5fa', '#93c5fd', '#0ea5e9', '#0284c7', '#0369a1', '#38bdf8']
CYAN = ['#06b6d4', '#0891b2', '#0e7490', '#155e75', '#22d3ee', '#67e8f9']
EMOJI = ['✨', '🚀', '🎯', '⚡', '🔥', '💡', '📈', '🎨', '🛡', '🌟', '💪', '🎉', '👋', '🙌', '✅', '⭐', '🏆']
SYSTEM_SANS = re.compile(r'^\s*["\']?(?:Inter|Roboto|Arial|Helvetica|-apple-system|system-ui|SF Pro)\b', re.I)
METRICS = [r'\b\d+\s*[×x]\s+(?:faster|better|easier|more (?:productive|efficient))\b', r'\b99[.,]\d+\s*%\s+uptime\b',
           r'\bzero[- ]downtime\b', r'\b\d+\s*[×x]\s+(?:szybciej|lepiej|łatwiej|wydajniej|więcej)\b',
           r'\b99[.,]\d+\s*%\s+(?:dostępności|niezawodności)\b']
FILLER = [r'\blorem\s+ipsum\b', r'\bdolor\s+sit\s+amet\b', r'\bfeature\s+(?:one|two|three|[123])\b', r'\bplaceholder\s+text\b',
          r'\bsample\s+content\b', r'\btekst\s+zastępczy\b', r'\bprzykładowa\s+treść\b', r'\bfunkcja\s+(?:pierwsza|druga|trzecia|[123])\b']
PLACEHOLDER_HOSTS = ['placehold.co', 'placeholder.com', 'picsum.photos', 'placekitten.com', 'source.unsplash.com', 'dummyimage.com']
ICON_TAGS = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'button', 'li'}


class Page(HTMLParser):
    """Visible text, text per icon-bearing tag, inline styles and <style> blocks."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text, self.css, self.icon_text, self.stack, self.skip = [], [], [], [], 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ('script', 'style'):
            self.skip += 1
            self.stack.append((tag, False))
            return
        if attrs.get('style'):
            self.css.append(f'inline {{{attrs["style"]}}}')
        iconish = tag in ICON_TAGS or 'icon' in (attrs.get('class') or '').lower()
        if tag not in ('br', 'img', 'input', 'meta', 'link', 'hr', 'source'):
            self.stack.append((tag, iconish))

    def handle_endtag(self, tag):
        while self.stack:
            name, _ = self.stack.pop()
            if name in ('script', 'style'):
                self.skip -= 1
            if name == tag:
                break

    def handle_data(self, data):
        if self.skip:
            if self.stack and self.stack[-1][0] == 'style':
                self.css.append(data)
            return
        self.text.append(data)
        if any(iconish for _, iconish in self.stack):
            self.icon_text.append(data)


def rules(css):
    """(selector, body) pairs from CSS, comments removed."""
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    return [(m.group(1).strip(), m.group(2)) for m in re.finditer(r'([^{}]*)\{([^{}]*)\}', css)]


def strip_tokens(text):
    """Remove custom-property definitions: a brand's own tokens are not hard-coded colours."""
    return re.sub(r'--[\w-]+\s*:[^;{}]*;?', '', text)


def size_px(body):
    m = re.search(r'font-size\s*:\s*([\d.]+)(px|rem)\b', body)
    return float(m.group(1)) * (16 if m.group(2) == 'rem' else 1) if m else None


def caps_tracking_ok(body):
    m = re.search(r'letter-spacing\s*:\s*(-?[\d.]+)(em|rem|px)\b', body)
    if not m:
        return False
    value, unit = float(m.group(1)), m.group(2)
    if unit == 'em':
        return value >= 0.06 - 1e-9
    px = value * 16 if unit == 'rem' else value
    size = size_px(body)
    return px >= (size * 0.06 if size else 1.0) - 1e-9


def lint(source, name='input', allow=()):
    is_html = bool(re.search(r'<(?:html|body|div|section|svg|style|p|h[1-6])\b', source, re.I))
    page = Page()
    if is_html:
        page.feed(source)
    css = '\n'.join(page.css) if is_html else source
    text = ' '.join(page.text) if is_html else ''
    raw = strip_tokens(source.lower())
    found = []

    def add(severity, rule, message, evidence=''):
        if rule not in allow:
            found.append({'file': name, 'severity': severity, 'id': rule, 'message': message, 'evidence': evidence[:160]})

    hit = next((h for h in INDIGO if h in raw), None)
    if hit:
        add('P0', 'ai-default-indigo', 'Default Tailwind indigo/violet hard-coded; use the brand accent token', hit)
    for grad in re.findall(r'(?:linear|radial|conic)-gradient\([^;{}]*\)', raw):
        if any(h in grad for h in PURPLE) or re.search(r'\b(?:purple|violet|indigo)\b', grad):
            add('P0', 'purple-gradient', 'Purple or indigo gradient: the most common generated look', grad)
        elif (any(h in grad for h in BLUE) or re.search(r'\bblue\b', grad)) and (any(h in grad for h in CYAN) or re.search(r'\bcyan\b', grad)):
            add('P0', 'trust-gradient', 'Blue-to-cyan "trust" gradient; use a flat surface and type hierarchy', grad)
    icons = ''.join(page.icon_text)
    emoji = [e for e in EMOJI if e in icons]
    if emoji:
        add('P0', 'emoji-icon', 'Emoji used as icons in headings, buttons, list items or icon slots; use monoline SVG', ' '.join(emoji))
    names_display = re.search(r'--font-display\s*:', source) or re.search(r'@font-face', source)
    for selector, body in rules(css):
        sel = selector.lower()
        if names_display and re.search(r'(?:^|[\s,>+~])h[1-3]\b|\.(?:display|hero|headline)', sel):
            fam = re.search(r'font-family\s*:\s*([^;]+)', body)
            if fam and SYSTEM_SANS.match(fam.group(1)):
                add('P0', 'sans-display', 'Display heading hard-coded to a system sans while a display face is defined', f'{selector} {{ font-family: {fam.group(1).strip()} }}')
        if re.search(r'border-left\s*:\s*[2-9]\d*px\s+solid', body) and re.search(r'border-radius\s*:\s*[1-9]', body):
            add('P0', 'left-accent-card', 'Rounded card with a coloured left border: the generated dashboard tile', selector)
        if re.search(r'text-transform\s*:\s*uppercase', body) and not caps_tracking_ok(body):
            add('P1', 'all-caps-no-tracking', 'ALL CAPS needs letter-spacing of at least 0.06em', selector or 'inline style')
    for rule, patterns, message in (('invented-metric', METRICS, 'Unsourced performance claim; use a sourced number or a labelled placeholder'),
                                    ('filler-copy', FILLER, 'Filler copy; solve the empty section with composition or real copy')):
        hits = [m.group(0) for m in (re.search(p, text, re.I) for p in patterns) if m]
        if hits:
            add('P0', rule, message, '; '.join(hits))
    outside_root = strip_tokens(re.sub(r':root\s*\{[^}]*\}', '', css))
    hexes = re.findall(r'#[0-9a-fA-F]{3,8}\b', outside_root)
    if len(hexes) > 12:
        add('P1', 'raw-hex', f'{len(hexes)} raw hex colours outside the token block; use tokens', ' '.join(sorted(set(hexes))[:8]))
    body_only = re.sub(r'<style\b.*?</style>', '', source, flags=re.S | re.I) if is_html else ''
    uses = len(re.findall(r'var\(--accent\)', body_only))
    if uses >= 6:
        add('P1', 'accent-overuse', f'The accent is used {uses} times in the markup; keep it to about two per screen', f'{uses} uses')
    host = next((h for h in PLACEHOLDER_HOSTS if h in source.lower()), None)
    if host:
        add('P1', 'placeholder-image', 'Placeholder image service; use the real image or a local labelled placeholder', host)
    order = {'P0': 0, 'P1': 1}
    return sorted(found, key=lambda f: order[f['severity']])


def main(argv=None):
    parser = argparse.ArgumentParser(description='Flag machine-made design tells in HTML, CSS and SVG.')
    parser.add_argument('files', nargs='+')
    parser.add_argument('--allow', action='append', default=[], help='a rule id the brief deliberately breaks')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args(argv)
    findings = []
    for name in args.files:
        try:
            source = Path(name).read_text(encoding='utf-8')
        except (OSError, UnicodeDecodeError) as error:
            print(f'craft_lint: cannot read {name}: {error}', file=sys.stderr)
            return 2
        findings += lint(source, name, set(args.allow))
    p0 = sum(f['severity'] == 'P0' for f in findings)
    if args.json:
        print(json.dumps({'p0': p0, 'p1': len(findings) - p0, 'allowed': args.allow, 'findings': findings}, indent=2, ensure_ascii=False))
    else:
        for f in findings:
            print(f"[{f['severity']}] {f['id']} ({f['file']}): {f['message']}" + (f" - {f['evidence']}" if f['evidence'] else ''))
        print(f'craft_lint: {p0} P0, {len(findings) - p0} P1' + (f"; allowed: {', '.join(args.allow)}" if args.allow else ''))
    return 1 if p0 else 0


if __name__ == '__main__':
    sys.exit(main())
