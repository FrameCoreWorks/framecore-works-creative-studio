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

    def test_routing_set_is_polish_and_checks_the_owner(self):
        self.assertIn('routing', host_eval.suite_names())
        suite = host_eval.load_suite('routing')
        owners = {p.name for p in (host_eval.PLUGIN / 'skills').iterdir() if (p / 'SKILL.md').is_file()}
        cases = suite['cases']
        self.assertGreaterEqual(len(cases), 20)
        named = [c for c in cases if c['turns'][0]['prompt'].startswith('@FrameCore Works Creative Studio')]
        self.assertTrue(0 < len(named) < len(cases), 'with and without the Studio name')
        for case in cases:
            prompt, checks = case['turns'][0]['prompt'], case['turns'][0]['checks']
            self.assertEqual(host_eval.language_of(prompt), 'pl', case['id'])
            routed = [c for c in checks if 'skills_any' in c or 'reads_any' in c]
            self.assertEqual(len(routed), 1, case['id'])
            for check in checks:
                for name in check.get('skills_any', []) + check.get('no_skills', []):
                    self.assertIn(name, owners, case['id'])
                host_eval.check(check, turn('x'))

    def test_sourced_cases_take_the_request_from_the_package_evals(self):
        cases = {case['id']: case for case in host_eval.load_suite()['cases']}
        self.assertTrue(cases['D01']['turns'][0]['prompt'].startswith('@FrameCore Works Creative Studio Podaj dokładnie trzy'))
        self.assertTrue(cases['D01']['rubric'])

    def test_every_suite_and_the_gate_fit_the_owner_case_limits(self):
        self.assertEqual(host_eval.CASE_LIMITS, {'full': 25, 'gate': 5})
        for name in host_eval.suite_names():
            cases = host_eval.load_suite(name)['cases']
            self.assertLessEqual(len(cases), host_eval.CASE_LIMITS['full'], name)
            self.assertLessEqual(len([c for c in cases if c.get('gate')]), host_eval.CASE_LIMITS['gate'], name)
        run, skipped = host_eval.within_limit([{'id': f'C{i}'} for i in range(7)], 5)
        self.assertEqual(([c['id'] for c in run], skipped), (['C0', 'C1', 'C2', 'C3', 'C4'], ['C5', 'C6']))


class Usage(unittest.TestCase):
    def test_tokens_sum_every_model_or_fall_back_to_usage(self):
        result = {'modelUsage': {'claude-sonnet-5-5': {'inputTokens': 10, 'outputTokens': 200, 'cacheReadInputTokens': 3000, 'cacheCreationInputTokens': 400},
                                 'claude-haiku-5-5': {'inputTokens': 5, 'outputTokens': 20}},
                  'usage': {'input_tokens': 1, 'output_tokens': 1}}
        self.assertEqual(host_eval.tokens_of(result), {'input': 15, 'output': 220, 'cache_read': 3000, 'cache_write': 400})
        self.assertEqual(host_eval.tokens_of({'usage': {'input_tokens': 7, 'output_tokens': 9, 'cache_read_input_tokens': 2}}),
                         {'input': 7, 'output': 9, 'cache_read': 2, 'cache_write': 0})
        self.assertEqual(host_eval.add_tokens({'input': 1, 'output': 2, 'cache_read': 3, 'cache_write': 4}, None),
                         {'input': 1, 'output': 2, 'cache_read': 3, 'cache_write': 4})

    def test_no_dollar_total_is_computed_or_recorded(self):
        source = (host_eval.ROOT / 'scripts/host_eval.py').read_text(encoding='utf-8')
        self.assertNotIn('total_cost_usd', source)
        self.assertNotIn('cost_usd', source.replace('--max-budget-usd', ''))


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

    def test_reads_any_accepts_a_reference_or_a_loaded_skill(self):
        read = [{'name': 'Read', 'input': {'file_path': '/x/skills/workflow-orchestrator/references/teacher-workflow.md'}}]
        skill = [{'name': 'Skill', 'input': {'skill': 'framecore-work-creative-studio:copy-voice'}}]
        wanted = {'reads_any': ['teacher-workflow.md', 'copy-voice/SKILL.md']}
        self.assertTrue(host_eval.check(wanted, turn('', read))[0])
        self.assertTrue(host_eval.check(wanted, turn('', skill))[0])
        self.assertFalse(host_eval.check(wanted, turn('', [{'name': 'Read', 'input': {'file_path': '/x/skills/ugc/SKILL.md'}}]))[0])

    def test_change_request_template_uses_the_harness_vocabulary(self):
        template = json.loads((host_eval.PLUGIN / 'skills/workflow-self-improvement/assets/change-request.template.json').read_text(encoding='utf-8'))
        self.assertEqual(template['check_vocabulary'], list(host_eval.CHECK_KINDS))
        self.assertEqual((template['status'], template['test']['result'], template['adoption']['explicit']), ('proposed', 'NOT_RUN', False))
        samples = {'welcome': 'pl', 'language': 'pl', 'regex': 'x', 'not_regex': 'x', 'command': 'x', 'no_command': 'x', 'code_block': True, 'not_welcome': True}
        for kind in host_eval.CHECK_KINDS:
            value = samples.get(kind, 1 if kind.startswith(('max_', 'min_')) or kind == 'items' else ['x'])
            host_eval.check({kind: value}, turn('x'))
        with self.assertRaises(host_eval.EvalError):
            host_eval.check({'unknown_kind': 1}, turn('x'))

    def test_language_and_version_placeholder(self):
        self.assertEqual(host_eval.language_of('To jest odpowiedź po polsku i nie ma w niej angielskiego.'), 'pl')
        self.assertEqual(host_eval.language_of('This is the answer and you can use it for the workshop.'), 'en')
        version = json.loads((host_eval.PLUGIN / 'plugin.json').read_text(encoding='utf-8'))['version']
        self.assertTrue(host_eval.check({'contains': ['{version}']}, turn(f'Wersja {version}.'))[0])


if __name__ == '__main__':
    unittest.main()
