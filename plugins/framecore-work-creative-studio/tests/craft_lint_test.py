"""Craft lint (pipeline-core/assets/craft-lint) and the prompt examples (pipeline-core/assets/prompt-examples)."""
import contextlib
import importlib.util
import io
import json
import pathlib
import tempfile
import unittest

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
ASSETS = PLUGIN / 'skills/pipeline-core/assets'


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


lint = module('craft_lint', ASSETS / 'craft-lint/craft_lint.py')
examples = module('prompt_examples', ASSETS / 'prompt-examples/prompt_examples.py')

BAD = '''<!doctype html><html lang="pl"><head><style>
:root { --accent: #6366f1; --font-display: "Fraunces", serif; }
h1 { font-family: Inter, sans-serif; }
.hero { background: linear-gradient(90deg, #7c3aed, #3b82f6); }
.cta { background: linear-gradient(90deg, #3b82f6, #06b6d4); }
.card { border-left: 4px solid var(--accent); border-radius: 12px; }
.eyebrow { text-transform: uppercase; letter-spacing: 0.02em; }
.btn { color: #4f46e5 }
</style></head><body><h1>✨ Szybciej</h1><p>Działa 10× szybciej. Lorem ipsum dolor sit amet.</p>
<img src="https://picsum.photos/200"><li>🚀 start</li></body></html>'''

GOOD = '''<!doctype html><html lang="pl"><head><style>
:root { --accent: #6366f1; --bg: #f7f3ec; --font-display: "Fraunces", serif; }
h1 { font-family: var(--font-display); letter-spacing: -0.02em; font-size: 56px }
.eyebrow { text-transform: uppercase; letter-spacing: 0.08em; font-size: 12px }
.label { text-transform: uppercase; letter-spacing: 1px; font-size: 13px }
</style></head><body><p class="eyebrow">Kawiarnia</p><h1>Kawa z Lipy</h1><p>Palimy co tydzień ✨</p></body></html>'''


def run(mod, *args):
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
        code = mod.main(list(args))
    return code, out.getvalue()


class CraftLint(unittest.TestCase):
    def test_every_tell_fires_once(self):
        ids = [f['id'] for f in lint.lint(BAD)]
        expected = ['ai-default-indigo', 'purple-gradient', 'trust-gradient', 'emoji-icon', 'sans-display', 'left-accent-card',
                    'invented-metric', 'filler-copy', 'all-caps-no-tracking', 'placeholder-image']
        self.assertEqual(sorted(ids), sorted(expected))
        self.assertEqual([f['severity'] for f in lint.lint(BAD)][:8], ['P0'] * 8)

    def test_tokens_running_text_emoji_and_tracked_caps_pass(self):
        self.assertEqual(lint.lint(GOOD), [])

    def test_caps_tracking_converts_px_with_the_rule_font_size(self):
        self.assertTrue(lint.caps_tracking_ok('letter-spacing: 3px; font-size: 48px'))
        self.assertFalse(lint.caps_tracking_ok('letter-spacing: 1px; font-size: 48px'))
        self.assertFalse(lint.caps_tracking_ok('font-size: 12px'))

    def test_raw_hex_and_accent_overuse(self):
        css = '<style>' + ''.join(f'.c{i} {{ color: #{i:02x}{i:02x}{i:02x} }}' for i in range(13)) + '</style>'
        body = '<p style="color: var(--accent)">a</p>' * 6
        ids = {f['id'] for f in lint.lint(f'<html><head>{css}</head><body>{body}</body></html>')}
        self.assertEqual(ids, {'raw-hex', 'accent-overuse'})

    def test_allow_and_exit_codes(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad, good = pathlib.Path(tmp, 'bad.html'), pathlib.Path(tmp, 'good.html')
            bad.write_text(BAD, encoding='utf-8')
            good.write_text(GOOD, encoding='utf-8')
            self.assertEqual(run(lint, str(bad))[0], 1)
            self.assertEqual(run(lint, str(good))[0], 0)
            code, out = run(lint, str(bad), '--json', '--allow', 'ai-default-indigo')
            report = json.loads(out)
            self.assertNotIn('ai-default-indigo', {f['id'] for f in report['findings']})
            self.assertEqual(report['p0'], 7)
            self.assertEqual(run(lint, str(pathlib.Path(tmp, 'missing.html')))[0], 2)

    def test_a_plain_css_file_is_linted(self):
        ids = {f['id'] for f in lint.lint('.x { background: linear-gradient(blue, cyan) } .y { text-transform: uppercase }')}
        self.assertEqual(ids, {'trust-gradient', 'all-caps-no-tracking'})


class PromptExamples(unittest.TestCase):
    data = examples.load()

    def test_every_record_is_openly_licensed_attributed_and_unique(self):
        records = self.data['records']
        self.assertEqual(len(records), 87)
        self.assertEqual(len({r['id'] for r in records}), 87)
        for r in records:
            self.assertIn(r['source']['license'], {'CC-BY-4.0', 'Apache-2.0', 'MIT'})
            self.assertTrue(r['source']['author'] and r['source']['url'].startswith('https://'))
            self.assertNotIn('previewImageUrl', r)
            self.assertIn(r['model'], {'gpt-image-2', 'seedance-2.0', 'hyperframes-html'})

    def test_excluded_records_stay_out(self):
        excluded = {e['id'] for e in self.data['excluded']}
        self.assertEqual(len(excluded), 19)
        kept = {r['id'] for r in self.data['records']}
        self.assertFalse(excluded & kept)
        text = json.dumps(self.data['records'], ensure_ascii=False)
        for name in ('Zelda', 'Pokémon', 'Disney', 'Elon Musk', 'PSG', 'MacBook'):
            self.assertNotIn(name, text)

    def test_show_prints_the_credit_and_search_filters(self):
        code, out = run(examples, 'show', 'wasteland-factory-chase')
        self.assertEqual(code, 0)
        self.assertIn('Credit: "Wasteland Factory Chase" by', out)
        self.assertIn('https://creativecommons.org/licenses/by/4.0/', out)
        code, out = run(examples, 'list', '--model', 'hyperframes-html')
        self.assertEqual(code, 0)
        self.assertEqual(len(out.strip().splitlines()), 12)
        self.assertEqual(run(examples, 'show', 'nothing')[0], 1)
        self.assertEqual(run(examples, 'search', 'zzzz-nothing')[0], 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
