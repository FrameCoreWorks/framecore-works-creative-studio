"""Offline tests for the host-eval harness: suite loading and the deterministic checks. Spends nothing."""
import importlib.util
import json
import tempfile
import subprocess
import shutil
import pathlib
import types
import unittest
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('host_eval', ROOT / 'scripts/host_eval.py')
host_eval = importlib.util.module_from_spec(spec)
spec.loader.exec_module(host_eval)


def turn(reply, tools=()):
    return {'reply': reply, 'tools': list(tools)}


class EarshotCommands(unittest.TestCase):
    def test_toolbox_launcher_runs_count_as_earshot_operations(self):
        # 2026-10-29: Earshot runs through FrameCore Works Toolbox's launcher.
        argv = ['python3.12', '/x/plugins/toolbox/capabilities/earshot/scripts/runtime.py', 'run', 'rank', 'a.wav']
        self.assertEqual(host_eval.earshot_operation(argv), ['rank', 'a.wav'])
        self.assertEqual(host_eval.earshot_operation(['python3', '/x/other/scripts/runtime.py', 'run', 'rank']), [])


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


class CandidateSnapshot(unittest.TestCase):
    def test_snapshot_detects_dirty_edits_and_ignores_caches(self):
        import tempfile
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            (root / 'SKILL.md').write_text('first')
            first = host_eval.candidate_snapshot(root)
            (root / 'SKILL.md').write_text('second')
            second = host_eval.candidate_snapshot(root)
            self.assertNotEqual(first['sha256'], second['sha256'])
            (root / '__pycache__').mkdir()
            (root / '__pycache__/cached.pyc').write_bytes(b'cache')
            self.assertEqual(second, host_eval.candidate_snapshot(root))


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


class ExecutionEvidence(unittest.TestCase):
    def parsed(self, records):
        events = []
        for index, record in enumerate(records):
            name, payload, ok, output = record
            ident = str(index)
            events += [{'type': 'assistant', 'message': {'content': [
                {'type': 'tool_use', 'id': ident, 'name': name, 'input': payload}]}},
                       {'type': 'user', 'message': {'content': [
                {'type': 'tool_result', 'tool_use_id': ident, 'is_error': not ok, 'content': output}]}}]
        return host_eval.parse_events(events, {'result': 'Zrobione, testy PASS.'})

    def evidence(self):
        return [
            ('Write', {'file_path': '/w/test_cues.py', 'content': 'test'}, True, 'created'),
            ('Bash', {'command': 'python3 -m unittest test_cues.py'}, False,
             'FAIL: test_onset (test_cues.TestCues)\nAssertionError: 48000 != 47900\nRan 1 test in 0.01s\nFAILED (failures=1)'),
            ('Write', {'file_path': '/w/place_cues.py', 'content': 'code'}, True, 'created'),
            ('Bash', {'command': 'python3 -m unittest test_cues.py'}, True,
             'Ran 1 test in 0.01s\n\nOK')]

    def test_failed_tool_results_preserve_output_and_order(self):
        parsed = self.parsed(self.evidence())
        failed = parsed['tools'][1]
        self.assertFalse(failed['ok'])
        self.assertIn('AssertionError', failed['result'])
        self.assertLess(failed['result_order'], parsed['tools'][2]['call_order'])
        self.assertEqual(len(failed['result_sha256']), 64)
        long = self.parsed([('Bash', {'command': 'python3 x.py'}, True, 'x'*50000)])['tools'][0]
        self.assertLessEqual(len(long['result']), 16384)
        self.assertEqual(long['result_chars'], 50000)

    def test_tdd_requires_a_real_relevant_ordered_red_edit_green(self):
        rule = {'test_red_green': {'test_pattern': 'cue|onset|sample|timing'}}
        self.assertTrue(host_eval.check(rule, self.parsed(self.evidence()))[0])
        bads = [[], self.evidence()[1:], self.evidence()[:2]+self.evidence()[3:],
                list(reversed(self.evidence()))]
        for output in ('Permission denied', 'ModuleNotFoundError: no module',
                       'FAILED (failures=1)', 'echo AssertionError'):
            records = self.evidence()
            records[1] = ('Bash', records[1][1], False, output)
            bads.append(records)
        records = self.evidence()
        records[-1] = ('Bash', {'command': 'python3 -m unittest test_other.py'}, True, 'Ran 1 test in 0.01s\nOK')
        bads.append(records)
        records = self.evidence()
        records[1] = ('Bash', {'command': 'echo "python3 -m unittest test_cues.py"'}, False, records[1][3])
        bads.append(records)
        for records in bads:
            with self.subTest(records=records):
                self.assertFalse(host_eval.check(rule, self.parsed(records))[0])

    def test_c17_and_c20_cannot_pass_with_claims_and_skill_loads_only(self):
        for case in host_eval.load_suite('companion')['cases']:
            if case['id'] not in ('C17', 'C20'):
                continue
            checks = case['turns'][0]['checks']
            loaded = [{'name': 'Skill', 'input': {'skill': s}, 'ok': True}
                      for s in ('earshot-audio:earshot', 'superpowers:test-driven-development')]
            reply = 'Wybrałem kandydatów, odrzuciłem metaliczny ogon, z = 2.4. Test najpierw FAIL, potem PASS.'
            self.assertFalse(all(host_eval.check(c, turn(reply, loaded))[0] for c in checks), case['id'])

    def test_artifacts_and_command_result_are_observed_not_claimed(self):
        rule = {'artifact': {'suffix': '.mp4', 'min_bytes': 64}}
        self.assertFalse(host_eval.check(rule, turn('film.mp4 gotowy'))[0])
        self.assertTrue(host_eval.check(rule, {**turn('done'), 'artifacts': [
            {'path': 'film.mp4', 'bytes': 120, 'sha256': 'a'*64, 'changed': True} ]})[0])
        command = {'command_result': {'command': 'earshot', 'output': 'z.?score|similarity'}}
        record = ('Bash', {'command': 'python3 earshot.py rank a.wav --text hit'}, True, '{"similarity":0.8}')
        self.assertTrue(host_eval.check(command, self.parsed([record]))[0])
        self.assertFalse(host_eval.check(command, self.parsed([
            ('Bash', {'command': 'echo "python3 earshot.py rank"'}, True, '{"similarity":0.8}')]))[0])


    def test_direct_commands_accept_quoted_and_escaped_literal_paths(self):
        for command in (
            "python3 '/Volumes/Codex&Claude/test_cues.py'",
            'python3 "/Volumes/Codex&Claude/test_cues.py"',
            r'python3 /Volumes/Codex\&Claude/test_cues.py',
        ):
            self.assertEqual(host_eval.executable_command(command)[1], '/Volumes/Codex&Claude/test_cues.py')
        for command in ('python3 x.py; echo ok', 'python3 x.py && true', 'python3 x.py | cat',
                        'python3 "$(touch /tmp/x)"', 'python3 x.py > result', 'python3 -c "print(1)"'):
            self.assertEqual(host_eval.executable_command(command), [], command)

    def media_turn(self, root):
        (root/'cues.json').write_text(json.dumps({'cues': [
            {'file': 'a.wav', 't': 1.2}, {'file': 'b.wav', 't': 3.0}]}))
        rank = {'query': 'clean effect', 'n_files': 2, 'results': [
            {'path': 'a.wav', 'z': 2.3, 'cosine': .6},
            {'path': 'b.wav', 'z': 2.1, 'cosine': .5}]}
        mix = {'out': 'final.mp4', 'all_on_time': True, 'cues': [
            {'t': 1.2, 'placed': True, 'on_time': True},
            {'t': 3.0, 'placed': True, 'on_time': True}]}
        timeline = {'file': 'final.mp4', 'sync': {'cues': {'items': [
            {'t': 1.2, 'offset_ms': 2, 'status': 'OK'}, {'t': 3.0, 'offset_ms': 0, 'status': 'peak'}]}}}
        parsed = self.parsed([
            ('Bash', {'command': 'python3 -m earshot rank a.wav b.wav --query "clean effect" --json'}, True, json.dumps(rank)),
            ('Bash', {'command': 'python3 /plugin/assets/sound-listen/place_sfx.py --video logo.mp4 --cues cues.json --out final.mp4 --json'}, True, json.dumps(mix)),
            ('Bash', {'command': 'python3 -m earshot timeline final.mp4 --cues cues.json --json'}, True, json.dumps(timeline))])
        parsed.update(workspace=str(root), artifacts=[{'path': 'final.mp4', 'changed': True, 'bytes': 200, 'sha256': 'a'*64},
                                               {'path': 'logo.mp4', 'changed': False, 'sha256': 'b'*64}])
        return parsed

    def test_media_execution_binds_rank_mix_and_encoded_timeline(self):
        rule = {'media_execution': {'input': 'logo.mp4', 'duration': 6, 'fps': 30, 'cues': [1.2, 3.0]}}
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            with mock.patch.object(host_eval, 'probe_media', return_value={'duration': 6, 'streams': ['audio', 'video']}):
                self.assertTrue(host_eval.check(rule, self.media_turn(root))[0])
                for mutation in ('name', 'rank', 'output', 'cue', 'offset', 'order', 'unchanged', 'missing', 'wrong_video', 'changed_input'):
                    candidate = self.media_turn(root)
                    if mutation == 'name':
                        candidate['tools'][0]['input']['command'] = 'python3 status.py --label earshot'
                    elif mutation == 'rank':
                        candidate['tools'][0]['result_data']['results'][0]['path'] = 'not-selected.wav'
                    elif mutation == 'output':
                        candidate['tools'][2]['result_data']['file'] = 'different.mp4'
                    elif mutation == 'cue':
                        candidate['tools'][2]['result_data']['sync']['cues']['items'][0]['t'] = 2.5
                    elif mutation == 'offset':
                        candidate['tools'][2]['result_data']['sync']['cues']['items'][0]['offset_ms'] = 100
                    elif mutation == 'order':
                        candidate['tools'][2]['call_order'] = 0
                    elif mutation == 'unchanged':
                        candidate['artifacts'][0]['changed'] = False
                    elif mutation == 'wrong_video':
                        candidate['tools'][1]['input']['command'] = candidate['tools'][1]['input']['command'].replace('logo.mp4','other.mp4')
                    elif mutation == 'changed_input':
                        candidate['artifacts'][1]['changed'] = True
                    else:
                        candidate['tools'][0]['result_data'] = {}
                    self.assertFalse(host_eval.check(rule, candidate)[0], mutation)
            for media in ({}, {'duration': 6, 'streams': ['video']}, {'duration': 7, 'streams': ['video','audio']}):
                with mock.patch.object(host_eval, 'probe_media', return_value=media):
                    self.assertFalse(host_eval.check(rule, self.media_turn(root))[0], media)

    @unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'), 'requires FFmpeg and ffprobe')
    def test_probe_rejects_text_and_detects_actual_audio_video_streams(self):
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            fake = root/'fake.mp4'
            fake.write_text('video audio CLAP ' * 20)
            self.assertEqual(host_eval.probe_media(fake), {})
            video = root/'video.mp4'
            subprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i', 'color=s=32x32:r=30:d=0.2',
                            '-f', 'lavfi', '-i', 'sine=frequency=440:duration=0.2', '-c:v', 'mpeg4',
                            '-c:a', 'aac', '-shortest', str(video)], check=True)
            self.assertEqual(set(host_eval.probe_media(video)['streams']), {'video', 'audio'})


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

    def test_questions_in_a_list_count_when_they_ask_the_user(self):
        # Audit WF-01: three numbered questions are not three slogans.
        asked = '1. Jaki produkt reklamujemy?\n2. Do kogo kierujesz reklamę?\n3. Czy masz logo?'
        self.assertFalse(host_eval.check({'max_user_questions': 0}, turn(asked))[0])
        self.assertFalse(host_eval.check({'max_user_questions': 1}, turn(asked + '\n4. What is the budget?'))[0])
        self.assertTrue(host_eval.check({'max_user_questions': 0}, turn('1. Masz dość czekania? Zamów dziś.\n2. Chleb z rana.\n3. Ciepły do drzwi.'))[0])

    def test_a_failed_tool_call_is_not_a_loaded_skill(self):
        # Audit WF-02: the call is paired with its result; an error or a missing result does not count.
        def events(is_error):
            call = {'type': 'assistant', 'message': {'content': [{'type': 'tool_use', 'id': 't1', 'name': 'Skill',
                                                                  'input': {'skill': 'framecore-work-creative-studio:workflow-orchestrator'}}]}}
            answer = {'type': 'user', 'message': {'content': [{'type': 'tool_result', 'tool_use_id': 't1', 'is_error': is_error,
                                                                'content': 'Skill not found' if is_error else 'ok'}]}}
            return [call, answer] if is_error is not None else [call]
        result = {'type': 'result', 'result': 'Hej'}
        for is_error, loaded in ((False, ['workflow-orchestrator']), (True, []), (None, [])):
            parsed = host_eval.parse_events(events(is_error), result)
            self.assertEqual(host_eval.skills_of(parsed['tools']), loaded, is_error)
            self.assertEqual(host_eval.check({'skills': ['workflow-orchestrator']}, parsed)[0], bool(loaded))

    def test_an_api_key_stops_the_runs_unless_the_owner_allows_it(self):
        # Audit WF-03: names only, never values; a plan or host-managed sign-in has none of these.
        self.assertEqual(host_eval.billing_variables({'ANTHROPIC_API_KEY': 'x', 'HOME': '/h'}), ['ANTHROPIC_API_KEY'])
        self.assertEqual(host_eval.billing_variables({'ANTHROPIC_BASE_URL': 'https://proxy', 'HOME': '/h'}), [])
        with mock.patch.dict(host_eval.os.environ, {'ANTHROPIC_API_KEY': 'FAKE_OFFLINE_MARKER'}), \
                mock.patch.object(host_eval.shutil, 'which', return_value='/bin/claude'), mock.patch.object(host_eval, 'run_case') as runner:
            self.assertEqual(host_eval.main(['--cases', 'W01']), 2)
            runner.assert_not_called()

    def test_a_companion_plugin_is_loaded_beside_studio(self):
        # The pair Studio + Superpowers must be testable in Claude Code: an isolated config never loads a user plugin.
        done = types.SimpleNamespace(stdout=json.dumps({'type': 'result', 'result': 'ok', 'session_id': 's'}), stderr='', returncode=0)
        args = types.SimpleNamespace(model='m', max_turns=1, turn_budget_usd=0.1, timeout=5, with_plugin=['/x/superpowers'])
        with mock.patch.object(host_eval.subprocess, 'run', return_value=done) as runner:
            host_eval.run_turn('hi', '/w', '/c', args, ['Skill'])
        command = runner.call_args[0][0]
        self.assertEqual(command[command.index('--plugin-dir'):command.index('--plugin-dir') + 4],
                         ['--plugin-dir', str(host_eval.PLUGIN), '--plugin-dir', '/x/superpowers'])

    def test_a_relative_companion_path_is_made_absolute(self):
        # 2026-10-23: claude runs in the case's temporary workspace, so a relative --plugin-dir silently loaded nothing.
        done = types.SimpleNamespace(stdout=json.dumps({'type': 'result', 'result': 'ok', 'session_id': 's'}), stderr='', returncode=0)
        args = types.SimpleNamespace(model='m', max_turns=1, turn_budget_usd=0.1, timeout=5, with_plugin=['plugins/voice-narration'])
        with mock.patch.object(host_eval.subprocess, 'run', return_value=done) as runner:
            host_eval.run_turn('hi', '/w', '/c', args, ['Skill'])
        command = runner.call_args[0][0]
        self.assertIn(str(pathlib.Path('plugins/voice-narration').resolve()), command)

    def test_a_suite_that_needs_a_companion_refuses_to_run_without_it(self):
        with mock.patch.object(host_eval.shutil, 'which', return_value='/bin/claude'), mock.patch.object(host_eval, 'run_case') as runner, \
                mock.patch.dict(host_eval.os.environ, {}, clear=False):
            for name in host_eval.billing_variables():
                host_eval.os.environ.pop(name, None)
            self.assertEqual(host_eval.main(['--suite', 'companion']), 2)
            runner.assert_not_called()

    def test_an_event_whose_message_is_text_is_skipped_not_fatal(self):
        events = [{'type': 'system', 'message': 'hook output as plain text'},
                  {'type': 'assistant', 'message': {'content': [{'type': 'tool_use', 'id': 't1', 'name': 'Skill', 'input': {'skill': 'x'}}]}}]
        parsed = host_eval.parse_events(events, {'result': 'ok', 'session_id': 's'})
        self.assertEqual([t['name'] for t in parsed['tools']], ['Skill'])

    def test_files_written_by_the_host_are_checked(self):
        tools = [{'name': 'Write', 'input': {'file_path': '/w/docs/superpowers/specs/2026-10-22-reel-design.md'}, 'ok': True}]
        self.assertFalse(host_eval.check({'no_write': ['docs/superpowers/']}, turn('ok', tools))[0])
        self.assertTrue(host_eval.check({'no_write': ['docs/superpowers/']}, turn('ok', []))[0])

    def test_a_failed_later_turn_keeps_the_finished_turns_and_their_usage(self):
        # Audit WF-04.
        first = {'reply': 'ok', 'is_error': False, 'subtype': 'success', 'session': 's', 'tokens': {'input': 101, 'output': 202, 'cache_read': 303, 'cache_write': 404},
                 'turns': 1, 'models': ['m'], 'seconds': 7.0, 'tools': []}
        case = {'id': 'T', 'title': 't', 'turns': [{'prompt': 'a', 'checks': []}, {'prompt': 'b', 'checks': []}]}
        args = types.SimpleNamespace(keep_chars=100, judge=False)
        with mock.patch.object(host_eval, 'run_turn', side_effect=[first, host_eval.EvalError('boom')]):
            outcome = host_eval.run_case(case, args)
        self.assertEqual(outcome['verdict'], 'ERROR')
        self.assertEqual(len(outcome['turns']), 1)
        self.assertEqual(outcome['tokens']['output'], 202)
        self.assertEqual(outcome['seconds'], 7.0)
        self.assertIn('turn 2', outcome['detail'])

    def creative(self, case_id):
        return next(c for c in json.loads((ROOT / 'tests/host-evals/creative.json').read_text(encoding='utf-8'))['cases'] if c['id'] == case_id)['turns'][0]['checks']

    def passes(self, checks, reply):
        return all(host_eval.check(spec, turn(reply))[0] for spec in checks if list(spec)[0] not in ('not_welcome', 'language', 'contains_any'))

    def test_one_template_answer_does_not_pass_every_brief(self):
        # Creativity audit 2026-10-15: the same three coloured squares passed all 11 briefs.
        squares = ('### Kierunek 1\nCzerwony kwadrat wjeżdża na środek, potem nazwa firmy.\n\n'
                   '### Kierunek 2\nZielony kwadrat wjeżdża na środek, potem nazwa firmy.\n\n'
                   '### Kierunek 3\nPomarańczowy kwadrat wjeżdża na środek, potem nazwa firmy.\n\nOdrzuciłem typowe motywy. Plakat, rolka 9:16 i animacja logo.')
        cases = [c['id'] for c in json.loads((ROOT / 'tests/host-evals/creative.json').read_text(encoding='utf-8'))['cases']]
        self.assertEqual(len(cases), 11)
        for case_id in cases:
            self.assertFalse(self.passes(self.creative(case_id), squares), case_id)

    def test_a_changed_offer_fails_and_the_count_of_directions_is_exact(self):
        good = ('### Kierunek 1\nGabinet „Uśmiech” w Poznaniu: -20% na pierwszy przegląd, kalendarz wizyt odlicza dni do otwarcia.\n\n'
                '### Kierunek 2\nPlakat jak karta pacjenta stomatologa, pierwszy przegląd z rabatem -20%, adres w Poznaniu.\n\n'
                '### Kierunek 3\nMapa Poznania z jednym punktem: nowy gabinet i -20% na pierwszy przegląd.')
        checks = self.creative('C02')
        facts = [c for c in checks if list(c)[0] in ('regex', 'not_regex', 'directions')]
        self.assertTrue(all(host_eval.check(c, turn(good))[0] for c in facts))
        wrong = good.replace('-20% na pierwszy', '+20% na drugi').replace('Poznaniu', 'Warszawie').replace('Poznania', 'Warszawy').replace('w Poznaniu', 'w Warszawie')
        self.assertFalse(all(host_eval.check(c, turn(wrong))[0] for c in facts))
        four = good + '\n\n### Kierunek 4\nUśmiech pacjenta z gabinetu w Poznaniu.'
        self.assertFalse(host_eval.check({'directions': {'count': 3, 'each_mentions': 'gabinet'}}, turn(four))[0])

    def test_not_only_is_not_a_negation_and_variant_labels_are_directions(self):
        self.assertTrue(host_eval.stock_in('kłos', 'Nie tylko kłosy zajmują cały kadr'))
        self.assertFalse(host_eval.stock_in('kłos', 'Bez kłosów: sam bochenek'))
        labelled = '**Wariant A**\nBochenek.\n\n**Wariant B**\nPiec.\n\n**Wariant C**\nDrzwi piekarni.'
        self.assertEqual(len(host_eval.sections(labelled)), 3)
        self.assertEqual(len(host_eval.sections('**1. Piec**\nx\n\n**2. Drzwi**\ny\n\n**Trasa pracy:** kod.')), 2)

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
        samples = {'welcome': 'pl', 'language': 'pl', 'regex': 'x', 'not_regex': 'x', 'command': 'x', 'no_command': 'x', 'code_block': True, 'not_welcome': True,
                   'max_sections_matching': {'pattern': 'x', 'max': 1}, 'directions': {'count': 3},
                   'artifact': {'suffix': '.mp4'}, 'command_result': {'command': 'x', 'output': 'x'},
                   'test_red_green': {'test_pattern': 'test'}}
        for kind in host_eval.CHECK_KINDS:
            value = samples.get(kind, 1 if kind.startswith(('max_', 'min_')) or kind == 'items' else ['x'])
            host_eval.check({kind: value}, turn('x'))
        with self.assertRaises(host_eval.EvalError):
            host_eval.check({'unknown_kind': 1}, turn('x'))

    def test_directions_are_found_in_headings_bold_labels_or_numbers(self):
        spec = {'max_sections_matching': {'pattern': 'kłosy|pszenic', 'max': 1, 'min_sections': 3}}
        headed = 'Intro\n### 1. Kłosy w wietrze\ntext\n### 2. Rozkład jazdy pieca\ntext\n### 3. Okruchy\ntext'
        bold = 'Intro\n**Kierunek A: pszenica** opis\n**Kierunek B: zegar pieca** opis\n**Kierunek C: kłosy** opis'
        numbered = 'Intro\n1. Ciasto, które rośnie jak wykres\n   1. scena\n2. Rozkład jazdy pieca\n3. Okruchy jako czcionka'
        self.assertTrue(host_eval.check(spec, turn(headed))[0])
        self.assertFalse(host_eval.check(spec, turn(bold))[0])
        self.assertTrue(host_eval.check(spec, turn(numbered))[0])
        self.assertFalse(host_eval.check(spec, turn('Jeden kierunek: kłosy.'))[0])
        titled = '# Kłos: 3 kierunki\n## Kierunek A: zegar\nx\n## Kierunek B: okruchy\nx\n## Kierunek C: rozkład\nx\n## Porównanie\nkłosy, pszenica, kłosy'
        self.assertEqual(len(host_eval.sections(titled)), 3)
        self.assertTrue(host_eval.check(spec, turn(titled))[0])

    def test_a_negated_motif_is_not_counted_as_used(self):
        self.assertFalse(host_eval.stock_in('filiżan|zęb', 'Plakat bez filiżanki i bez pary.'))
        self.assertFalse(host_eval.stock_in('filiżan|zęb', 'Uśmiech osoby; nie pokazujemy zębów z bliska.'))
        self.assertTrue(host_eval.stock_in('filiżan', 'Na końcu pierwsza filiżanka i logo.'))

    def test_language_and_version_placeholder(self):
        self.assertEqual(host_eval.language_of('To jest odpowiedź po polsku i nie ma w niej angielskiego.'), 'pl')
        self.assertEqual(host_eval.language_of('This is the answer and you can use it for the workshop.'), 'en')
        version = json.loads((host_eval.PLUGIN / 'plugin.json').read_text(encoding='utf-8'))['version']
        self.assertTrue(host_eval.check({'contains': ['{version}']}, turn(f'Wersja {version}.'))[0])


if __name__ == '__main__':
    unittest.main()
