"""Offline tests for the host-eval harness: suite loading and the deterministic checks. Spends nothing."""
import importlib.util
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('host_eval', ROOT / 'scripts/host_eval.py')
host_eval = importlib.util.module_from_spec(spec)
spec.loader.exec_module(host_eval)


def turn(reply, tools=()):
    return {'reply': reply, 'tools': list(tools)}


class Suite(unittest.TestCase):
    def test_cases_resolve_and_every_check_is_known(self):
        suite = host_eval.load_suite()
        ids = [case['id'] for case in suite['cases']]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(ids), 15)
        self.assertTrue(any(case.get('gate') for case in suite['cases']))
        for case in suite['cases']:
            self.assertTrue(case['turns'], case['id'])
            for step in case['turns']:
                self.assertTrue(step['prompt'].strip(), case['id'])
                for check in step.get('checks', []):
                    self.assertEqual(len(check), 1, case['id'])
                    host_eval.check(check, turn('x'))  # raises on an unknown check

    def test_sourced_cases_take_the_request_from_the_package_evals(self):
        cases = {case['id']: case for case in host_eval.load_suite()['cases']}
        self.assertTrue(cases['D01']['turns'][0]['prompt'].startswith('@FrameCore Works Creative Studio Podaj dokładnie trzy'))
        self.assertTrue(cases['D01']['rubric'])


class Checks(unittest.TestCase):
    def test_welcome_must_be_byte_identical(self):
        welcome = host_eval.WELCOME['pl'].read_text(encoding='utf-8')
        self.assertTrue(host_eval.check({'welcome': 'pl'}, turn(welcome.rstrip('\n')))[0])
        self.assertFalse(host_eval.check({'welcome': 'pl'}, turn(welcome.replace('Jestem', 'Jestem tu'))) [0])
        self.assertFalse(host_eval.check({'not_welcome': True}, turn('Hej\n\n' + welcome))[0])

    def test_a_question_mark_inside_requested_copy_is_not_a_question_to_the_user(self):
        reply = '1. Pierwszy raz z gliną? Zacznij w sobotę.\n2. Glina w cenie.\n3. „Ulepisz to?” Tak.'
        self.assertTrue(host_eval.check({'max_user_questions': 0}, turn(reply))[0])
        self.assertFalse(host_eval.check({'max_user_questions': 0}, turn(reply + '\n\nKtóre wybierasz?'))[0])
        self.assertEqual(host_eval.check({'items': 3}, turn(reply))[0], True)

    def test_skills_and_commands_come_from_the_tool_calls(self):
        tools = [{'name': 'Skill', 'input': {'skill': 'framecore-work-creative-studio:caption-studio'}},
                 {'name': 'Bash', 'input': {'command': 'python3 find_skills.py "ui sounds"'}}]
        self.assertTrue(host_eval.check({'skills': ['caption-studio']}, turn('', tools))[0])
        self.assertTrue(host_eval.check({'command': 'find_skills'}, turn('', tools))[0])
        self.assertFalse(host_eval.check({'no_command': 'find_skills'}, turn('', tools))[0])

    def test_language_and_version_placeholder(self):
        self.assertEqual(host_eval.language_of('To jest odpowiedź po polsku i nie ma w niej angielskiego.'), 'pl')
        self.assertEqual(host_eval.language_of('This is the answer and you can use it for the workshop.'), 'en')
        version = json.loads((host_eval.PLUGIN / 'plugin.json').read_text(encoding='utf-8'))['version']
        self.assertTrue(host_eval.check({'contains': ['{version}']}, turn(f'Wersja {version}.'))[0])


if __name__ == '__main__':
    unittest.main()
