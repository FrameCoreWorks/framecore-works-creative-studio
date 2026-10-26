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

GOOD = '''<!doctype html><html lang="pl"><head><meta name="viewport" content="width=device-width"><style>
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
                    'invented-metric', 'filler-copy', 'all-caps-no-tracking', 'placeholder-image', 'viewport-missing']
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
        ids = {f['id'] for f in lint.lint(f'<html><head><meta name="viewport" content="width=device-width">{css}</head><body>{body}</body></html>')}
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

    def test_anti_slop_rules_for_interface_honesty_and_layout(self):
        page = """<!doctype html><html><head><meta name="viewport" content="width=device-width"><style>
        a { outline: none } .muted { color: #999999; background: #ffffff }
        .n { backdrop-filter: blur(8px) } .c { backdrop-filter: blur(8px) } .m { backdrop-filter: blur(8px) }
        .g1 { box-shadow: 0 0 40px #7dd3fc } .g2 { box-shadow: 0 0 24px rgba(56,189,248,.6) } .g3 { text-shadow: 0 0 20px #f0abfc }
        .p1 { border-radius: 9999px } .p2 { border-radius: 9999px } .p3 { border-radius: 999px } .p4 { border-radius: 9999px }
        .hero { height: 100vh } .wrap { width: 1280px }
        .bg { background: linear-gradient(90deg, #eee 1px, transparent 1px), linear-gradient(#eee 1px, transparent 1px); background-size: 24px 24px }
        </style></head><body><a href="#">Pricing</a><a href="https://x.pl">Start →</a><button>Plan →</button><button>Demo →</button>
        <button>Learn more</button><p>AI-powered and seamless. Contact John Doe.</p></body></html>"""
        ids = {f['id'] for f in lint.lint(page)}
        for rule in ('focus-outline-removed', 'low-contrast', 'glass-overuse', 'glow-overuse', 'pill-everything', 'full-height-section',
                     'fixed-width', 'background-grid', 'dead-link', 'button-arrows', 'generic-cta', 'buzzword', 'fake-person'):
            self.assertIn(rule, ids)
        calm = """<!doctype html><html><head><meta name="viewport" content="width=device-width"><style>
        a:focus-visible { outline: 2px solid #1d1d1b } a { outline: none } .t { color: #1d1d1b; background: #f7f3ec }
        .wrap { width: 1280px; max-width: 100% } .hero { min-height: 60dvh }
        </style></head><body><a href="/cennik">Zobacz cennik</a><button>Zarezerwuj stolik</button><p>Jan pali kawę.</p></body></html>"""
        self.assertEqual(lint.lint(calm), [])

    def test_contrast_check_matches_the_reference_pairs(self):
        contrast = module('contrast_check', ASSETS / 'craft-lint/contrast_check.py')
        self.assertEqual(run(contrast, '--selftest')[0], 0)
        self.assertEqual(run(contrast, '#777777', '#070707')[0], 1)        # 4.498 prints 4.5 and still fails
        code, out = run(contrast, '1d1d1b', 'f7f3ec', '--json')
        self.assertEqual(code, 0)
        self.assertGreater(json.loads(out)['ratio'], 15)
        self.assertEqual(run(contrast, 'zzz', '#fff')[0], 2)

    def test_studio_video_compositions_raise_nothing(self):
        for rel in ('skills/hyperframes-workflow/assets/reel-starters/local-service/index.html',
                    'skills/hyperframes-workflow/assets/iso-glow/examples/bass-speaker/index.html'):
            self.assertEqual(lint.lint((PLUGIN / rel).read_text(encoding='utf-8')), [], rel)
        self.assertTrue(lint.caps_tracking_ok('letter-spacing: 0.06em'))


class TasteRules(unittest.TestCase):
    HEAD = '<!doctype html><html><head><meta name="viewport" content="width=device-width"><style>{css}</style></head><body>{body}</body></html>'

    def ids(self, css='', body=''):
        return {f['id'] for f in lint.lint(self.HEAD.format(css=css, body=body))}

    def test_headline_length(self):
        self.assertIn('headline-length', self.ids(body='<h1>Everything your small team needs to plan, ship and celebrate every week</h1>'))
        self.assertNotIn('headline-length', self.ids(body='<h1>Kawa z Lipy</h1><h2>Palimy co tydzień w Krakowie</h2>'))

    def test_index_numbering_outside_a_list(self):
        body = '<div><span>01</span><p>a</p></div><div><span>02</span></div><div><span>03</span></div>'
        self.assertIn('index-numbering', self.ids(body=body))
        self.assertNotIn('index-numbering', self.ids(body='<ol><li><span>01</span></li><li><span>02</span></li><li><span>03</span></li></ol>'))

    def test_eyebrow_is_a_dose_cap(self):
        one = '<p class="eyebrow">Kawiarnia</p><h1>Kawa</h1>'
        self.assertNotIn('eyebrow-cluster', self.ids(body=one))
        many = one + '<p class="kicker">A</p><h2>B</h2><p class="eyebrow">C</p><h2>D</h2>'
        self.assertIn('eyebrow-cluster', self.ids(body=many))

    def test_micro_labels_mono_and_motion(self):
        css = ''.join(f'.l{i} {{ text-transform: uppercase; font-size: 11px; letter-spacing: 0.12em }}' for i in range(3))
        css += ' .lead { font-family: "JetBrains Mono", monospace } code { font-family: monospace } .b { transition: all .3s }'
        ids = self.ids(css=css)
        self.assertTrue({'micro-label-cluster', 'mono-prose', 'motion-tells'} <= ids, ids)
        self.assertEqual(self.ids(css='code, pre { font-family: Menlo, monospace } .b { transition: opacity .2s }'), set())

    def test_cream_terracotta_only_when_hard_coded(self):
        self.assertIn('cream-terracotta', self.ids(css='body { background: #f6efe3 } .cta { background: #c4623a }'))
        self.assertNotIn('cream-terracotta', self.ids(css=':root { --bg: #f6efe3; --accent: #c4623a } body { background: var(--bg) }'))

    def test_table_figures(self):
        rows = ''.join(f'<tr><td>Q{i}</td><td>{i * 1234} zł</td><td>{i * 7}%</td></tr>' for i in range(1, 4))
        self.assertIn('table-figures', self.ids(body=f'<table>{rows}</table>'))
        self.assertNotIn('table-figures', self.ids(css='td { font-variant-numeric: tabular-nums }', body=f'<table>{rows}</table>'))

    def test_more_placeholder_people(self):
        self.assertIn('fake-person', self.ids(body='<p>Trusted by Acme Inc. Write to hello@example.com</p>'))

    def test_the_sample_details_note_is_not_filler(self):
        # owner decision 2026-10-26: mockups may carry samples under this note; the note itself must pass the lint
        note = '<p>Sample details, to be confirmed</p><p>Przykładowe dane do potwierdzenia</p><p>Chleb żytni na zakwasie, 14 zł</p>'
        self.assertEqual(self.ids(body='<h1>Piekarnia</h1>' + note), set())
        self.assertIn('filler-copy', self.ids(body='<p>Sample content</p>'))


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
