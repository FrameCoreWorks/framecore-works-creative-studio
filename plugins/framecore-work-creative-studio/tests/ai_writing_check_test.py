"""AI writing pattern check (copy-voice/scripts/ai_writing_check.py): finds clusters in English and Polish, leaves plain copy alone."""
import contextlib
import importlib.util
import io
import json
import pathlib
import unittest

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
TOOL = PLUGIN / 'skills/copy-voice/scripts/ai_writing_check.py'
spec = importlib.util.spec_from_file_location('ai_writing_check', TOOL)
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)

POLISH_SLOP = ('W dzisiejszym dynamicznym świecie nasza innowacyjna platforma to nie tylko narzędzie, to rewolucja. '
               'Eksperci twierdzą, że to przełomowe rozwiązanie. Mam nadzieję, że to pomoże!\nDowiedz się więcej')
ENGLISH_SLOP = ("Unlock seamless collaboration and elevate your team's journey. It's not just a tool, it's a partner. "
                'No templates. No defaults. No limits. Experts say it changes everything. I hope this helps!')


def ids(text):
    return {f['id'] for f in check.check(text)['findings']}


def run(*args):
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
        return check.main(list(args)), out.getvalue()


class AiWritingCheck(unittest.TestCase):
    def test_polish_slop_is_a_cluster(self):
        report = check.check(POLISH_SLOP)
        self.assertEqual(report['language'], 'pl')
        self.assertEqual(report['verdict'], 'cluster')
        self.assertTrue({'empty-vocabulary', 'significance-inflation', 'weasel-attribution', 'chatbot-closer',
                         'negative-parallelism', 'generic-cta'} <= ids(POLISH_SLOP))

    def test_english_slop_is_a_cluster(self):
        found = ids(ENGLISH_SLOP)
        self.assertTrue({'empty-vocabulary', 'negative-parallelism', 'staccato-run', 'weasel-attribution', 'chatbot-closer'} <= found)
        self.assertEqual(check.check(ENGLISH_SLOP)['verdict'], 'cluster')

    def test_plain_copy_is_clean_and_single_tells_are_not_a_verdict(self):
        self.assertEqual(check.check('Palimy kawę co tydzień w Gdyni. Ziarno z Etiopii, wypał jasny. Zajrzyj w sobotę.')['verdict'], 'clean')
        self.assertEqual(check.check('Our bakery opens at 7. The oven was built in 1932 — and it still runs.')['verdict'], 'clean')
        self.assertEqual(check.check('Pracownia jest innowacyjna w podejściu do lnu. Rezerwacje w piątki.')['verdict'], 'clean')

    def test_dashes_are_not_flagged_in_polish(self):
        text = 'Kawa – jasna, owocowa – prosto z palarni. Ciasto – codziennie świeże – z naszej kuchni.'
        self.assertNotIn('em-dash', ids(text))
        self.assertIn('em-dash', ids('Our policy — announced today — changes pricing. The team — all five — agreed.'))

    def test_caps_threes_headers_and_emoji(self):
        self.assertIn('caps-emphasis', ids('This is our last chance and WE MUST ACT NOW before they leave.'))
        self.assertNotIn('caps-emphasis', ids('WIELKIE OTWARCIE PRACOWNI\nZapraszamy w sobotę.'))
        threes = 'Speed, quality and trust. Talks, panels and networking. Innovation, inspiration and insights.'
        self.assertIn('forced-three', ids(threes))
        md = '- **Speed:** faster.\n- **Security:** encrypted.\n## 🚀 Launch\n'
        self.assertTrue({'inline-header-list', 'emoji-heading'} <= ids(md))

    def test_cli_exit_codes_and_json(self):
        self.assertEqual(run('--text', POLISH_SLOP)[0], 1)
        code, out = run('--text', 'Zarezerwuj stolik na sobotę.', '--json')
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)['verdict'], 'clean')
        self.assertEqual(run('/nonexistent/file.txt')[0], 3)
        self.assertEqual(run()[0], 3)


if __name__ == '__main__':
    unittest.main(verbosity=2)
