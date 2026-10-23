"""Recommended extensions (workflow-orchestrator/assets/extensions): the registry is complete, pinned and per host."""
import contextlib
import copy
import importlib.util
import io
import json
import pathlib
import tempfile
import unittest

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
TOOL = PLUGIN / 'skills/workflow-orchestrator/assets/extensions/extensions.py'
spec = importlib.util.spec_from_file_location('extensions', TOOL)
ext = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ext)
DATA = json.loads((TOOL.parent / 'extensions.json').read_text(encoding='utf-8'))


def run(*args):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = ext.main(list(args))
    return code, out.getvalue(), err.getvalue()


class Registry(unittest.TestCase):
    def companion_registry(self):
        data = copy.deepcopy(DATA)
        entry = copy.deepcopy(data['extensions'][0])
        entry.update(id='test-companion', recommendation_priority='first')
        entry.pop('package', None)
        entry['hosts'] = {host: {
            'status': 'catalog_manual', 'manual_steps': 'Search the host plugin catalog; the user installs.',
            'writes': 'The host manages the separate plugin.', 'verify': 'Read an actual installed skill.',
            'after': 'Refresh only through the supported host flow.', 'remove': 'Use the host plugin controls.'
        } for host in data['hosts']}
        data['extensions'] = [entry]
        return data

    def test_catalog_manual_needs_no_fake_shell_plan_or_pinned_catalog_version(self):
        data = self.companion_registry()
        self.assertEqual(ext.validate(data), [])
        row = ext.catalog(data, 'chatgpt')[0]
        self.assertEqual(row['recommendation_priority'], 'first')
        self.assertEqual(set(row['how']), {'manual_steps', 'writes', 'verify', 'after', 'remove'})
        report = ext.show(data['extensions'][0], 'chatgpt', check=False)
        self.assertEqual(report['recommendation_priority'], 'first')

    def test_setup_targets_existing_owner_and_direct_owners_reach_shared_support(self):
        for relative in ('plugin.json', '.codex-plugin/plugin.json'):
            manifest = json.loads((PLUGIN / relative).read_text())
            self.assertEqual(manifest.get('extensions', {}).get('com.openai', {}).get('onboardingSkill'),
                             './skills/workflow-orchestrator/SKILL.md')
        policy = (PLUGIN / 'skills/pipeline-core/references/studio-integration-policy.md').read_text()
        self.assertIn('superpowers-native-routing.md', policy)
        for skill in (PLUGIN / 'skills').glob('*/SKILL.md'):
            self.assertIn('studio-integration-policy.md', skill.read_text(), str(skill))
        for owner in ('workflow-orchestrator', 'pipeline-core', 'hyperframes-workflow',
                      'remotion-video-production', 'opencut-video-studio', 'static-graphic-design-creator'):
            self.assertIn('superpowers-native-routing.md', (PLUGIN / 'skills' / owner / 'SKILL.md').read_text())

    def test_catalog_manual_rejects_executable_installers_and_missing_verification(self):
        data = self.companion_registry()
        entry = data['extensions'][0]
        entry['hosts']['codex']['install'] = 'install ' + entry['reviewed_commit']
        del entry['hosts']['chatgpt']['verify']
        problems = ' '.join(ext.validate(data))
        self.assertIn('catalog_manual cannot contain plan or install', problems)
        self.assertIn('chatgpt verify missing', problems)

    def test_first_recommendation_is_unique_and_has_a_known_priority(self):
        data = self.companion_registry()
        other = copy.deepcopy(data['extensions'][0])
        other['id'] = 'other-companion'
        data['extensions'].append(other)
        self.assertIn('only one first recommendation', ' '.join(ext.validate(data)))
        other['recommendation_priority'] = 'urgent'
        self.assertIn('unknown recommendation_priority', ' '.join(ext.validate(data)))

    def test_second_recommendation_is_unique(self):
        data = self.companion_registry()
        for name in ('second-a', 'second-b'):
            other = copy.deepcopy(data['extensions'][0])
            other.update(id=name, recommendation_priority='second')
            data['extensions'].append(other)
        self.assertIn('only one second recommendation', ' '.join(ext.validate(data)))
        data['extensions'].pop()
        self.assertEqual(ext.validate(data), [])

    def test_earshot_is_the_second_setup_recommendation(self):
        # Owner request 2026-10-23: first configuration offers earshot-audio after Superpowers.
        entry = next(e for e in DATA['extensions'] if e['id'] == 'earshot')
        self.assertEqual(entry['recommendation_priority'], 'second')
        code, out, _ = run('show', 'earshot', '--host', 'claude_code')
        self.assertEqual(code, 0)
        self.assertIn('recommendation: second', out)
        setup = (PLUGIN / 'skills/workflow-orchestrator/references/extensions.md').read_text()
        section = setup.split('## First companion setup', 1)[1].split('\n## ', 1)[0]
        self.assertIn('recommendation_priority: second', section)
        self.assertIn('earshot-audio:earshot', section)
        self.assertLess(section.index('Superpowers'), section.index('earshot-audio'))

    def test_earshot_light_tier_text_matches_the_engine(self):
        # End-to-end run 2026-10-23: timeline needs the CLAP model even at --detail low.
        entry = next(e for e in DATA['extensions'] if e['id'] == 'earshot')
        for host in ('codex', 'claude_code'):
            after = entry['hosts'][host]['after']
            self.assertNotIn('timeline without models', after)
            self.assertIn('timeline, sheet', after)

    def test_a_listed_earshot_without_its_engine_asks_with_both_routes(self):
        # Owner decision 2026-10-23 (option A): no silent fallback to Studio's engine, no install before the answer.
        routing = (PLUGIN / 'skills/pipeline-core/references/earshot-native-routing.md').read_text()
        motion = (PLUGIN / 'skills/hyperframes-workflow/SKILL.md').read_text()
        for text in (routing, motion):
            self.assertIn('about 200 MB', text)
            self.assertIn('run neither before the answer', text.replace('Run neither', 'run neither'))
        self.assertIn('never fall back silently', routing)

    def test_effects_are_chosen_by_listening_with_readings(self):
        # Owner report 2026-10-23: a preset's hit had a metallic debris tail.
        routing = (PLUGIN / 'skills/pipeline-core/references/earshot-native-routing.md').read_text()
        motion = (PLUGIN / 'skills/hyperframes-workflow/SKILL.md').read_text()
        self.assertIn('chosen by listening', motion)
        self.assertIn("never accept a preset's take unchecked", motion)
        for needle in ('likely confusions', 'onsets per second', 'speaker-audible bands'):
            self.assertIn(needle, routing)

    def test_superpowers_is_first_optional_catalog_companion_for_every_host(self):
        entries = [e for e in DATA['extensions'] if e['id'] == 'superpowers']
        self.assertEqual(len(entries), 1)
        entry = entries[0]
        self.assertEqual(entry['recommendation_priority'], 'first')
        self.assertEqual(entry['repository'], 'https://github.com/obra/superpowers')
        for host in DATA['hosts']:
            self.assertEqual(entry['hosts'][host]['status'], 'catalog_manual')
            for action in ('list', 'show', 'catalog'):
                args = (action, 'superpowers') if action == 'show' else (action,)
                code, out, err = run(*args, '--host', host, '--json')
                self.assertEqual((code, err), (0, ''))
                report = json.loads(out)
                row = report if action == 'show' else next(r for r in report['extensions'] if r['id'] == 'superpowers')
                self.assertEqual(row['recommendation_priority'], 'first')
                self.assertNotIn('installed', row)

    def test_human_catalog_and_list_make_first_recommendation_visible_without_reordering(self):
        for action in ('list', 'catalog', 'show'):
            args = (action, 'superpowers') if action == 'show' else (action,)
            code, out, _ = run(*args, '--host', 'chatgpt')
            self.assertEqual(code, 0)
            self.assertIn('recommendation: first', out)
        code, out, _ = run('list', '--host', 'codex', '--json')
        self.assertEqual(json.loads(out)['extensions'][0]['id'], DATA['extensions'][0]['id'])

    def test_the_registry_is_valid_and_covers_the_same_hosts_as_the_environment_check(self):
        self.assertEqual(ext.validate(DATA), [])
        tools = json.loads((PLUGIN / 'skills/workflow-orchestrator/assets/environment-check/tools.json').read_text(encoding='utf-8'))
        self.assertEqual(sorted(DATA['hosts']), sorted(h['id'] for h in tools['hosts']))

    def test_an_unpinned_command_or_a_plan_without_a_dry_run_is_refused(self):
        bad = copy.deepcopy(DATA)
        bad['extensions'][0]['hosts']['codex']['install'] = 'npx -y rea-agents@latest setup --client codex --yes'
        bad['extensions'][0]['hosts']['claude_code']['plan'] = 'npx -y rea-agents@6.5.0 setup --client claude_code'
        problems = ' '.join(ext.validate(bad))
        self.assertIn('codex install must use the pinned', problems)
        self.assertIn('claude_code plan must be a dry run', problems)

    def test_an_unsupported_host_needs_a_reason_and_every_entry_states_rights(self):
        bad = copy.deepcopy(DATA)
        del bad['extensions'][0]['hosts']['chatgpt_work']['reason']
        del bad['extensions'][0]['rights']
        problems = ' '.join(ext.validate(bad))
        self.assertIn('chatgpt_work reason missing', problems)
        self.assertIn('rights missing', problems)

    def test_an_archive_pin_needs_a_checksum_in_every_command_and_a_listing_plan(self):
        iso = next(e for e in DATA['extensions'] if e['id'] == 'iso-glow')
        sha = iso['archive']['sha256']
        for host in ('codex', 'claude_code'):
            steps = iso['hosts'][host]
            self.assertIn(sha, steps['plan'])
            self.assertIn(sha, steps['install'])
            self.assertIn('unzip -l', steps['plan'])
        bad = copy.deepcopy(DATA)
        broken = next(e for e in bad['extensions'] if e['id'] == 'iso-glow')
        broken['hosts']['codex']['install'] = 'curl -fsSL https://isoglow.dev/iso-glow.zip | tar -xz -C ~/.agents/skills'
        broken['archive']['sha256'] = 'latest'
        problems = ' '.join(ext.validate(bad))
        self.assertIn('iso-glow: archive needs an https url and a SHA-256', problems)
        self.assertIn('codex install must use the pinned', problems)

    def test_the_catalog_gives_every_entry_with_its_description_and_the_steps_for_this_host(self):
        code, out, _ = run('catalog', '--host', 'claude_code', '--json')
        self.assertEqual(code, 0)
        rows = {r['id']: r for r in json.loads(out)['extensions']}
        self.assertEqual(set(rows), {e['id'] for e in DATA['extensions']})
        self.assertTrue({'huashu-art-motion', 'iso-glow'} <= set(rows))
        huashu = rows['huashu-art-motion']
        self.assertEqual(huashu['status'], 'native')
        self.assertEqual(list(huashu['how']), ['plan', 'install', 'verify', 'after', 'remove'])
        self.assertIn('--list', huashu['how']['plan'])
        self.assertTrue(huashu['gives'] and huashu['studio_uses'] and huashu['license'])
        code, out, _ = run('catalog', '--host', 'chatgpt')
        self.assertEqual(code, 0)
        self.assertIn('manual_steps:', out)
        self.assertIn('https://isoglow.dev/', out)
        self.assertEqual(run('catalog')[0], 1)

    def test_list_and_show_print_the_status_and_the_pinned_steps(self):
        code, out, _ = run('list', '--host', 'chatgpt_work')
        self.assertEqual(code, 0)
        self.assertIn('rea:', out)
        self.assertIn('not_supported', out)
        code, out, _ = run('show', 'rea', '--host', 'claude_code', '--json')
        report = json.loads(out)
        self.assertEqual(report['status'], 'native')
        self.assertIn('--dry-run', report['steps']['plan'])
        self.assertTrue(all('rea-agents@6.5.0' in report['steps'][k] for k in ('plan', 'install', 'verify', 'remove')))
        self.assertEqual(run('show', 'nothing', '--host', 'codex')[0], 1)
        self.assertEqual(run('list', '--host', 'mars')[0], 1)

    def test_git_pinned_entries_check_out_the_reviewed_commit_and_keep_confirmation(self):
        entries = {e['id']: e for e in DATA['extensions']}
        self.assertTrue({'animate', 'motion-designer', 'meta-ads-designer'} <= set(entries))
        animate = entries['animate']['hosts']['claude_code']
        self.assertIn('checkout ' + entries['animate']['reviewed_commit'], animate['plan'])
        self.assertIn(entries['animate']['reviewed_commit'], animate['install'])
        self.assertNotIn('plugin install', animate['plan'])
        bad = copy.deepcopy(DATA)
        meta = next(e for e in bad['extensions'] if e['id'] == 'meta-ads-designer')
        meta['hosts']['codex']['install'] += ' -y'
        meta['hosts']['claude_code']['plan'] = meta['hosts']['claude_code']['install']
        problems = ' '.join(ext.validate(bad))
        self.assertIn("codex install must keep the installer's own confirmation", problems)
        self.assertIn('claude_code plan must be a dry run', problems)

    def test_a_manual_host_gives_steps_and_an_unsupported_one_a_reason(self):
        meta = next(e for e in DATA['extensions'] if e['id'] == 'meta-ads-designer')
        self.assertEqual(meta['hosts']['chatgpt_work']['status'], 'manual')
        self.assertIn(meta['reviewed_commit'], meta['hosts']['chatgpt_work']['manual_steps'])
        designer = next(e for e in DATA['extensions'] if e['id'] == 'motion-designer')
        self.assertIn('YAML', designer['hosts']['codex']['reason'])

    def test_every_entry_has_a_category_and_the_catalog_groups_by_it(self):
        self.assertTrue(all(e.get('category') for e in DATA['extensions']))
        code, out, _ = run('catalog', '--host', 'claude_code')
        self.assertEqual(code, 0)
        headings = [line for line in out.splitlines() if line.startswith('[')]
        self.assertEqual(headings, sorted({f"[{e['category']}]" for e in DATA['extensions']}))

    def test_the_voice_engines_form_one_choice_described_in_the_audio_guide(self):
        tts = [e for e in DATA['extensions'] if e.get('category') == 'tts']
        self.assertEqual(sorted(e['id'] for e in tts), ['moss-tts', 'moss-ttsd', 'omnivoice', 'voicebox', 'voxcpm'])
        guide = (PLUGIN / 'skills/audio-production-director/references/local-tts-engines.md').read_text(encoding='utf-8')
        for name in ('Voicebox', 'OmniVoice', 'VoxCPM2', 'MOSS-TTS', 'MOSS-TTSD'):
            self.assertIn(name, guide)
        for entry in tts:
            self.assertIn('permission', entry['rights'])
            for host in ('chatgpt', 'chatgpt_work'):
                self.assertEqual(entry['hosts'][host]['status'], 'not_supported')
        code, out, _ = run('list', '--category', 'tts', '--host', 'codex')
        self.assertEqual(code, 0)
        self.assertEqual(sum(1 for line in out.splitlines() if line and not line.startswith(' ')), 5)
        voxcpm = next(e for e in tts if e['id'] == 'voxcpm')
        self.assertIn('voxcpm==2.0.3', voxcpm['hosts']['claude_code']['install'])

    def test_logo_design_is_pinned_optional_and_separates_trademark_rights(self):
        entry = next(e for e in DATA['extensions'] if e['id'] == 'logo-design')
        for host in DATA['hosts']:
            code, out, err = run('show', 'logo-design', '--host', host, '--json')
            self.assertEqual((code, err), (0, ''))
            report = json.loads(out)
            self.assertEqual(report['reviewed_commit'], entry['reviewed_commit'])
            self.assertIn('trademark', report['rights'])
        for host in ('codex', 'claude_code'):
            spec = entry['hosts'][host]
            self.assertEqual(spec['status'], 'native')
            self.assertIn(entry['reviewed_commit'], spec['plan'])
            self.assertIn(entry['reviewed_commit'], spec['install'])
            self.assertNotIn('plugin install', spec['plan'])
        self.assertIn('--list', entry['hosts']['codex']['plan'])
        node = next(r for r in entry['requires'] if r['tool'] == 'node')
        self.assertEqual(node['ranges'], [['22.20.0', None]])
        self.assertIn('TRADEMARKS.md', entry['hosts']['codex']['install'])
        for host in ('claude_apps', 'chatgpt', 'chatgpt_work'):
            self.assertEqual(entry['hosts'][host]['status'], 'manual')
            self.assertIn(entry['reviewed_commit'], entry['hosts'][host]['manual_steps'])
        self.assertIn('not_run', entry['observed'])
        self.assertTrue((PLUGIN / 'integrations/logo-design-skill/LICENSE').is_file())
        self.assertFalse((PLUGIN / 'skills/logo-design').exists())

    def test_logo_craft_uses_the_existing_owner_without_importing_renderer_defaults(self):
        skill = (PLUGIN / 'skills/static-graphic-design-creator/SKILL.md').read_text(encoding='utf-8')
        section = skill.split('## Logo concept and craft pass\n', 1)[1].split('\n## ', 1)[0]
        for phrase in ('preserve the requested medium', 'actual intended sizes',
                       'approved geometry', 'existing review budget', 'advisory',
                       'not trademark clearance', 'bundled'):
            self.assertIn(phrase, section)
        profile = (PLUGIN / 'skills/workflow-orchestrator/references/brand-identity-workflow.md').read_text(encoding='utf-8')
        self.assertIn('SKILL.md#logo-concept-and-craft-pass', profile)
        provenance = json.loads((PLUGIN / 'integrations/logo-design-skill/source-manifest.json').read_text(encoding='utf-8'))
        entry = next(e for e in DATA['extensions'] if e['id'] == 'logo-design')
        self.assertEqual(provenance['commit'], entry['reviewed_commit'])

    def test_a_broken_registry_exits_2(self):
        with tempfile.TemporaryDirectory() as temp:
            path = pathlib.Path(temp, 'bad.json')
            path.write_text('{"schema_version": 2}', encoding='utf-8')
            self.assertEqual(run('list', '--registry', str(path))[0], 2)

    def test_anatomy_bundle_and_original_extension_have_separate_runtime_requirements(self):
        entry = next(e for e in DATA['extensions'] if e['id'] == 'anatomy')
        manifest = json.loads((PLUGIN / 'integrations/anatomy/source-manifest.json').read_text())
        self.assertEqual(entry['reviewed_commit'], manifest['commit'])
        self.assertEqual(len([f for f in manifest['files'] if f['source_path'].startswith('kit/')]), 15)
        for host in DATA['hosts']:
            self.assertEqual(run('show', 'anatomy', '--host', host)[0], 0)
        for host in ('codex', 'claude_code'):
            self.assertIn('--list', entry['hosts'][host]['plan'])
            self.assertIn(entry['reviewed_commit'], entry['hosts'][host]['install'])
        skill = (PLUGIN / 'skills/hyperframes-workflow/SKILL.md').read_text()
        self.assertIn('no separate Anatomy install', skill)
        self.assertFalse((PLUGIN / 'skills/anatomy/SKILL.md').exists())

    def test_node_versions_are_checked_against_the_ranges(self):
        ranges = DATA['extensions'][0]['requires'][0]['ranges']
        fits = lambda v: any(ext.version_tuple(v) >= ext.version_tuple(lo) and (hi is None or ext.version_tuple(v) < ext.version_tuple(hi)) for lo, hi in ranges)
        self.assertTrue(fits('v22.22.0'))
        self.assertFalse(fits('v22.18.0'))
        self.assertFalse(fits('v23.1.0'))
        self.assertTrue(fits('v26.1.0'))


    def test_open_design_entry_pins_0_26_0(self):
        entry = next(e for e in DATA['extensions'] if e['id'] == 'open-design')
        self.assertEqual(entry['reviewed_commit'], 'bfee093942f8578c8b6ec7f26862e96f81026a89')
        hashes = ('ff7a1181b83aca664b85b7da0a5df740c99cf34bdce203d5276022ee72946d76',
                  'f2fc313eb5b62c207621b5f15e83aa135c69a04e9cbae25fce94da2d99c346ee',
                  '4c0697a53177753072593b44133f44cca76421a102a4da1b4229d5e643569b00')
        for host, data in entry['hosts'].items():
            text = data.get('manual_steps') or data.get('reason', '')
            self.assertNotIn('0.25.0', text, host)
            if data['status'] == 'manual':
                for needle in ('open-design-v0.26.0', '--print', '--uninstall', 'curl | sh', 'delete', *hashes):
                    self.assertIn(needle, text, f'{host}: {needle}')
        self.assertIn('Share', entry['not_for'])
        self.assertNotIn('0.25.0', json.dumps(entry['requires']))
        folder = PLUGIN / 'integrations/open-design'
        self.assertTrue((folder / 'LICENSE').read_text(encoding='utf-8').lstrip().startswith('Apache License'))
        self.assertTrue((folder / 'README.md').is_file())


    def test_every_owner_names_the_superpowers_skills_it_must_load(self):
        # Host evaluation 2026-10-22 (companion suite C01, C07): an owner that only links the routing reference never
        # loads Superpowers in a single-turn run; naming the skill in the owner's own SKILL.md does.
        skills = PLUGIN / 'skills'
        for path in sorted(skills.glob('*/SKILL.md')):
            text = path.read_text(encoding='utf-8')
            if path.parent.name == 'workflow-orchestrator':   # it routes to the owners and keeps its byte budget
                self.assertIn('superpowers-native-routing.md', text)
                continue
            for name in ('superpowers:systematic-debugging', 'superpowers:verification-before-completion'):
                self.assertIn(name, text, f'{path.parent.name} does not name {name}')


    def test_footage_films_reach_framecut_from_the_producer_too(self):
        # Host evaluation 2026-10-22 (companion C08): without the Studio name the host picks Creative Video Producer by its
        # description; it must send the user's own footage to FrameCut as the orchestrator does, with one question.
        text = (PLUGIN / 'skills/creative-video-producer/SKILL.md').read_text(encoding='utf-8')
        self.assertIn("A film from the user's own footage", text)
        self.assertIn('(../opencut-video-studio/SKILL.md): load it before answering, and ask at most one question', text)


    def test_earshot_works_with_or_without_the_separate_native_plugin(self):
        # Owner handover 2026-10-22: a separate earshot-audio plugin, local CLI/Python only, no MCP and no Gemini.
        # Claude Code and Codex users without that plugin keep the pinned CLI route; owners name the skill they load.
        entry = next(e for e in DATA['extensions'] if e['id'] == 'earshot')
        commit = '591fa3e028032e6dce56620a20e932e35667e8d8'   # v0.4.0, the public earshot-audio plugin's pin
        self.assertEqual(entry['reviewed_commit'], commit)
        for host in ('claude_code', 'codex'):
            steps = entry['hosts'][host]
            self.assertEqual(steps['status'], 'native')
            self.assertIn(f'earshot/archive/{commit}.zip', steps['install'])
            self.assertIn('earshot-audio:earshot', steps.get('after', '') + steps.get('verify', ''))
        self.assertIn('/plugin install earshot-audio --marketplace FrameCoreWorks/framecore-works-creative-studio', entry['hosts']['claude_code']['after'])
        self.assertNotIn('925ebe5', json.dumps(entry['hosts']))
        text = json.dumps(entry, ensure_ascii=False)
        self.assertIn('earshot-audio:earshot', entry['studio_uses'])
        for allowed in ('upload audio after consent', 'explicitly authorized optional LLM upload', 'requires explicit consent'):
            self.assertNotIn(allowed, text)
        self.assertIn('no Gemini', entry['not_for'])
        routing = (PLUGIN / 'skills/pipeline-core/references/earshot-native-routing.md').read_text(encoding='utf-8')
        self.assertIn('`llm` and `mcp`', routing)
        for owner in ('hyperframes-workflow', 'opencut-video-studio', 'audio-production-director', 'remotion-video-production'):
            body = (PLUGIN / 'skills' / owner / 'SKILL.md').read_text(encoding='utf-8')
            self.assertIn('earshot-audio:earshot', body, owner)
            self.assertIn('earshot-native-routing.md', body, owner)
        for path in ('skills/pipeline-core/references/studio-integration-policy.md', 'skills/pipeline-core/references/loop-protocol.md'):
            self.assertIn('earshot-native-routing.md', (PLUGIN / path).read_text(encoding='utf-8'), path)
        cases = json.loads((PLUGIN / 'evals/native-earshot-cases.json').read_text(encoding='utf-8'))
        self.assertGreaterEqual(len(cases['cases']), 8)
        for overlay in ('motion-runtime', 'engine-runtime', 'media-runtime', 'session-runtimes'):
            for owner in ('hyperframes-workflow', 'opencut-video-studio', 'audio-production-director', 'remotion-video-production'):
                self.assertNotIn(overlay, (PLUGIN / 'skills' / owner / 'SKILL.md').read_text(encoding='utf-8'), f'private overlay {overlay} in {owner}')


if __name__ == '__main__':
    unittest.main()
