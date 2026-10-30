"""Recommended extensions (workflow-orchestrator/assets/extensions): the registry is complete, pinned and per host."""
import contextlib
import copy
import importlib.util
import io
import json
import pathlib
import re
import tempfile
import unittest

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
TOOL = PLUGIN / 'skills/workflow-orchestrator/assets/extensions/extensions.py'
spec = importlib.util.spec_from_file_location('extensions', TOOL)
ext = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ext)
DATA = json.loads((TOOL.parent / 'extensions.json').read_text(encoding='utf-8'))
# Native entries the registry held before owner decision 2026-10-29 moved third-party tools to FrameCore Works
# Toolbox; kept only as fixtures for the validator and the command line, never offered by Studio.
NATIVE = json.loads((PLUGIN / 'tests/fixtures/extensions-native-entries.json').read_text(encoding='utf-8'))['extensions']
STUDIO_OWN = {'voice-narration', 'framecore-works-toolbox', 'superpowers', 'awesome-opus-videos', 'brand-kit',
              'framecore-open-assets'}


def with_native():
    data = copy.deepcopy(DATA)
    data['extensions'] += copy.deepcopy(NATIVE)
    return data


def run(*args):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = ext.main(list(args))
    return code, out.getvalue(), err.getvalue()


class Registry(unittest.TestCase):
    def run_native(self, *args):
        with tempfile.TemporaryDirectory() as temp:
            path = pathlib.Path(temp, 'registry.json')
            path.write_text(json.dumps(with_native()), encoding='utf-8')
            return run(*args, '--registry', str(path))

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

    def test_toolbox_is_the_second_setup_recommendation(self):
        # Owner decisions 2026-10-29: Earshot comes only through FrameCore Works Toolbox, so Studio keeps no earshot entry.
        # Owner request 2026-10-30: Open Assets first, then Toolbox with one numbered list (Superpowers is an item of it).
        entry = next(e for e in DATA['extensions'] if e['id'] == 'framecore-works-toolbox')
        self.assertEqual(entry['recommendation_priority'], 'second')
        self.assertNotIn('earshot', {e['id'] for e in DATA['extensions']})
        code, out, _ = run('show', 'framecore-works-toolbox', '--host', 'claude_code')
        self.assertEqual(code, 0)
        self.assertIn('recommendation: second', out)
        setup = (PLUGIN / 'skills/workflow-orchestrator/references/extensions.md').read_text()
        section = setup.split('## First companion setup', 1)[1].split('\n## ', 1)[0]
        self.assertIn('recommendation_priority: second', section)
        self.assertIn('toolbox:toolbox', section)
        self.assertLess(section.index('framecore-open-assets:open-assets'), section.index('toolbox:toolbox'))
        self.assertLess(section.index('toolbox:toolbox'), section.index('Superpowers (helps plan'))
        oa = next(e for e in DATA['extensions'] if e['id'] == 'framecore-open-assets')
        self.assertEqual(oa['recommendation_priority'], 'first')
        for needle in ('recommendation_priority: first', 'numbered list', 'works right away in a session', 'needs your computer',
                       'Which numbers do you want?', 'never show a command unless asked', 'Dodać Open Assets?'):
            self.assertIn(needle, section)

    def test_setup_offers_the_earshot_engine_in_plain_words_with_a_tier_choice(self):
        # Owner request 2026-10-23: the same offer on every host, plain words, full or light chosen at setup and installed.
        setup = (PLUGIN / 'skills/workflow-orchestrator/references/extensions.md').read_text()
        section = setup.split('## First companion setup', 1)[1].split('\n## ', 1)[0]
        for needle in ('same words on every host', 'Explain it plainly', 'about 2.6 GB', 'about 360 MB', 'not now',
                       'The answer is the consent', 'claude plugin install toolbox@framecore-works', 'Plugin Creator',
                       'install --tier <choice>', 'fetch-models --yes', 'status --json', '*.hf.co', '*.pytorch.org',
                       'Pełny', 'Lekki', 'nie wysyła Twoich plików', 'projekt Leona Lina', 'github.com/Leonxlnx/earshot',
                       '~/.framecore-works/earshot', 'candidates', 'fetch-models --from'):
            self.assertIn(needle, section)
        for gone in ('earshot-audio', 'Do not run `runtime.py install`'):
            self.assertNotIn(gone, section)
        self.assertIn("installation guides' last step enters this setup", section)

    def test_one_earshot_route_and_superpowers_for_its_code(self):
        # Owner request 2026-10-23: one current Earshot description, routed with Superpowers and Studio.
        sp = (PLUGIN / 'skills/pipeline-core/references/superpowers-native-routing.md').read_text()
        self.assertIn('### Sound with Earshot', sp)
        motion = (PLUGIN / 'skills/hyperframes-workflow/SKILL.md').read_text()
        for name in ('test-driven-development', 'systematic-debugging', 'verification-before-completion'):
            self.assertIn(f'superpowers:{name}', motion)
            self.assertIn(name, sp.split('### Sound with Earshot', 1)[1].split('###', 1)[0])
        integration = (PLUGIN / 'integrations/earshot/README.md').read_text()
        self.assertIn('Earshot itself is not part of Studio', integration)
        self.assertTrue((PLUGIN / 'integrations/earshot/LICENSE').is_file())   # listen.py adapts its code
        listen_doc = (PLUGIN / 'skills/hyperframes-workflow/assets/sound-listen/README.md').read_text()
        self.assertIn('252', listen_doc)
        self.assertNotIn('201', listen_doc)
        apd = (PLUGIN / 'skills/audio-production-director/SKILL.md').read_text()
        self.assertNotIn("uploads audio and runs only with the user's own key", apd)
        for path in ('skills/hyperframes-workflow/SKILL.md', 'skills/audio-production-director/SKILL.md',
                     'skills/pipeline-core/references/companion-routing.md', 'skills/pipeline-core/references/studio-integration-policy.md'):
            body = (PLUGIN / path).read_text()
            for stale in ('pinned `earshot` command', 'command-line extension'):
                self.assertNotIn(stale, body, path)
        for owner in ('hyperframes-workflow', 'audio-production-director'):
            self.assertNotIn('the pinned `earshot` [extension]', (PLUGIN / 'skills' / owner / 'SKILL.md').read_text(), owner)

        # End-to-end run 2026-10-23: timeline needs the CLAP model even at --detail low.
        entry = next(e for e in DATA['extensions'] if e['id'] == 'framecore-works-toolbox')
        for host in ('codex', 'claude_code', 'chatgpt_work'):
            steps = entry['hosts'][host]['manual_steps']
            self.assertNotIn('timeline without models', steps)
            self.assertIn('timeline, sheet', steps)

    def test_a_listed_earshot_without_its_engine_asks_with_both_routes(self):
        # Owner decision 2026-10-23 (option A): no silent fallback to Studio's engine, no install before the answer.
        routing = (PLUGIN / 'skills/pipeline-core/references/companion-routing.md').read_text()
        motion = (PLUGIN / 'skills/hyperframes-workflow/SKILL.md').read_text()
        for text in (routing, motion):
            self.assertIn('about 360 MB', text)
            self.assertIn('run neither before the answer', text.replace('Run neither', 'run neither'))
            # 2026-10-30 install test: light also makes and places sounds (sfx, kit); it does not choose by listening.
            self.assertNotIn('measures only', text)
        self.assertIn('never fall back silently', routing)

    def test_effects_are_chosen_by_listening_with_readings(self):
        # Owner report 2026-10-23: a preset's hit had a metallic debris tail.
        routing = (PLUGIN / 'skills/pipeline-core/references/companion-routing.md').read_text()
        motion = (PLUGIN / 'skills/hyperframes-workflow/SKILL.md').read_text()
        self.assertIn('chosen by listening', motion)
        self.assertIn("never accept a preset's take unchecked", motion)
        for needle in ('likely confusions', 'onsets per second', 'speaker-audible bands'):
            self.assertIn(needle, routing)

    def test_superpowers_is_an_optional_catalog_companion_for_every_host(self):
        # Owner request 2026-10-30: Superpowers is an item of the setup's numbered list, no longer the first offer.
        entries = [e for e in DATA['extensions'] if e['id'] == 'superpowers']
        self.assertEqual(len(entries), 1)
        entry = entries[0]
        self.assertNotIn('recommendation_priority', entry)
        self.assertEqual(entry['repository'], 'https://github.com/obra/superpowers')
        for host in DATA['hosts']:
            self.assertEqual(entry['hosts'][host]['status'], 'catalog_manual')
            for action in ('list', 'show', 'catalog'):
                args = (action, 'superpowers') if action == 'show' else (action,)
                code, out, err = run(*args, '--host', host, '--json')
                self.assertEqual((code, err), (0, ''))
                report = json.loads(out)
                row = report if action == 'show' else next(r for r in report['extensions'] if r['id'] == 'superpowers')
                self.assertIsNone(row['recommendation_priority'])
                self.assertNotIn('installed', row)

    def test_human_catalog_and_list_make_first_recommendation_visible_without_reordering(self):
        for action in ('list', 'catalog', 'show'):
            args = (action, 'framecore-open-assets') if action == 'show' else (action,)
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
        bad = with_native()
        rea = next(e for e in bad['extensions'] if e['id'] == 'rea')
        self.assertEqual(ext.validate(bad), [])
        rea['hosts']['codex']['install'] = 'npx -y rea-agents@latest setup --client codex --yes'
        rea['hosts']['claude_code']['plan'] = 'npx -y rea-agents@6.5.0 setup --client claude_code'
        problems = ' '.join(ext.validate(bad))
        self.assertIn('codex install must use the pinned', problems)
        self.assertIn('claude_code plan must be a dry run', problems)

    def test_an_unsupported_host_needs_a_reason_and_every_entry_states_rights(self):
        bad = copy.deepcopy(DATA)
        del bad['extensions'][0]['hosts']['chatgpt']['reason']
        del bad['extensions'][0]['rights']
        problems = ' '.join(ext.validate(bad))
        self.assertIn('chatgpt reason missing', problems)
        self.assertIn('rights missing', problems)

    def test_an_archive_pin_needs_a_checksum_in_every_command_and_a_listing_plan(self):
        iso = next(e for e in NATIVE if e['id'] == 'iso-glow')
        sha = iso['archive']['sha256']
        for host in ('codex', 'claude_code'):
            steps = iso['hosts'][host]
            self.assertIn(sha, steps['plan'])
            self.assertIn(sha, steps['install'])
            self.assertIn('unzip -l', steps['plan'])
        bad = with_native()
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
        self.assertTrue(all(r['gives'] and r['studio_uses'] and r['license'] for r in rows.values()))
        code, out, _ = self.run_native('catalog', '--host', 'claude_code', '--json')
        huashu = {r['id']: r for r in json.loads(out)['extensions']}['huashu-art-motion']
        self.assertEqual(huashu['status'], 'native')
        self.assertEqual(list(huashu['how']), ['plan', 'install', 'verify', 'after', 'remove'])
        self.assertIn('--list', huashu['how']['plan'])
        code, out, _ = self.run_native('catalog', '--host', 'chatgpt')
        self.assertEqual(code, 0)
        self.assertIn('manual_steps:', out)
        self.assertIn('https://isoglow.dev/', out)
        self.assertEqual(run('catalog')[0], 1)

    def test_list_and_show_print_the_status_and_the_pinned_steps(self):
        code, out, _ = self.run_native('list', '--host', 'chatgpt_work')
        self.assertEqual(code, 0)
        self.assertIn('rea:', out)
        self.assertIn('not_supported', out)
        code, out, _ = self.run_native('show', 'rea', '--host', 'claude_code', '--json')
        report = json.loads(out)
        self.assertEqual(report['status'], 'native')
        self.assertIn('--dry-run', report['steps']['plan'])
        self.assertTrue(all('rea-agents@6.5.0' in report['steps'][k] for k in ('plan', 'install', 'verify', 'remove')))
        self.assertEqual(run('show', 'rea', '--host', 'codex')[0], 1)   # no longer a Studio entry
        self.assertEqual(run('show', 'nothing', '--host', 'codex')[0], 1)
        self.assertEqual(run('list', '--host', 'mars')[0], 1)

    def test_git_pinned_entries_check_out_the_reviewed_commit_and_keep_confirmation(self):
        entries = {e['id']: e for e in NATIVE}
        animate = entries['animate']['hosts']['claude_code']
        self.assertIn('checkout ' + entries['animate']['reviewed_commit'], animate['plan'])
        self.assertIn(entries['animate']['reviewed_commit'], animate['install'])
        self.assertNotIn('plugin install', animate['plan'])
        bad = with_native()
        meta = next(e for e in bad['extensions'] if e['id'] == 'meta-ads-designer')
        meta['hosts']['codex']['install'] += ' -y'
        meta['hosts']['claude_code']['plan'] = meta['hosts']['claude_code']['install']
        problems = ' '.join(ext.validate(bad))
        self.assertIn("codex install must keep the installer's own confirmation", problems)
        self.assertIn('claude_code plan must be a dry run', problems)

    def test_a_manual_host_gives_steps_and_an_unsupported_one_a_reason(self):
        for entry in DATA['extensions']:
            for host, spec in entry['hosts'].items():
                if spec['status'] in ('manual', 'catalog_manual'):
                    self.assertTrue(spec.get('manual_steps'), f"{entry['id']} {host}")
                if spec['status'] == 'not_supported':
                    self.assertTrue(spec.get('reason'), f"{entry['id']} {host}")

    def test_every_entry_has_a_category_and_the_catalog_groups_by_it(self):
        self.assertTrue(all(e.get('category') for e in DATA['extensions']))
        code, out, _ = run('catalog', '--host', 'claude_code')
        self.assertEqual(code, 0)
        headings = [line for line in out.splitlines() if line.startswith('[')]
        self.assertEqual(headings, sorted({f"[{e['category']}]" for e in DATA['extensions']}))

    def test_the_erased_voice_engines_are_gone_and_two_routes_remain(self):
        # Owner decision 2026-10-29: Voicebox moved to Toolbox as an app note; OmniVoice, VoxCPM2 (as a Studio
        # recommendation), MOSS-TTS and MOSS-TTSD were erased from Studio.
        self.assertFalse([e for e in DATA['extensions'] if e.get('category') == 'tts'])
        guide = (PLUGIN / 'skills/audio-production-director/references/local-tts-engines.md').read_text(encoding='utf-8')
        apd = (PLUGIN / 'skills/audio-production-director/SKILL.md').read_text(encoding='utf-8')
        registry = (TOOL.parent / 'extensions.json').read_text(encoding='utf-8')
        guides = [(PLUGIN.parent.parent / name).read_text(encoding='utf-8')
                  for name in ('CLAUDE_INSTALL.md', 'CODEX_INSTALL.md', 'CHATGPT_INSTALL.md', 'README.md')]
        for text in (guide, apd, registry, *guides):
            for gone in ('OmniVoice', 'MOSS-TTS', 'MOSS-TTSD'):
                self.assertNotIn(gone, text)
        for kept in ('voice-narration', 'Voicebox', 'toolbox-catalog'):
            self.assertIn(kept, guide)
        folder = PLUGIN / 'integrations/tts-engines'
        self.assertEqual(sorted(p.name for p in folder.iterdir()), ['LICENSE-voicebox', 'README.md'])


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
        self.assertEqual(provenance['commit'], '0ecf52e9a4b3ac92b714f7cc6e3148ab8c774134')
        self.assertTrue((PLUGIN / 'integrations/logo-design-skill/LICENSE').is_file())
        self.assertFalse((PLUGIN / 'skills/logo-design').exists())

    def test_a_broken_registry_exits_2(self):
        with tempfile.TemporaryDirectory() as temp:
            path = pathlib.Path(temp, 'bad.json')
            path.write_text('{"schema_version": 2}', encoding='utf-8')
            self.assertEqual(run('list', '--registry', str(path))[0], 2)

    def test_anatomy_bundle_needs_no_separate_install_and_the_original_is_in_toolbox(self):
        manifest = json.loads((PLUGIN / 'integrations/anatomy/source-manifest.json').read_text())
        self.assertEqual(len([f for f in manifest['files'] if f['source_path'].startswith('kit/')]), 15)
        skill = (PLUGIN / 'skills/hyperframes-workflow/SKILL.md').read_text()
        self.assertIn('no separate Anatomy install', skill)
        self.assertIn('`anatomy` plugin from [FrameCore Works Toolbox]', skill)
        self.assertFalse((PLUGIN / 'skills/anatomy/SKILL.md').exists())

    def test_node_versions_are_checked_against_the_ranges(self):
        ranges = next(e for e in NATIVE if e['id'] == 'rea')['requires'][0]['ranges']
        fits = lambda v: any(ext.version_tuple(v) >= ext.version_tuple(lo) and (hi is None or ext.version_tuple(v) < ext.version_tuple(hi)) for lo, hi in ranges)
        self.assertTrue(fits('v22.22.0'))
        self.assertFalse(fits('v22.18.0'))
        self.assertFalse(fits('v23.1.0'))
        self.assertTrue(fits('v26.1.0'))


    def test_third_party_tools_live_in_the_toolbox_catalog_not_in_studio(self):
        # Owner decision 2026-10-29: Studio's registry keeps only its own companions and knowledge sources; option 4
        # shows them and then the Toolbox catalog.
        self.assertEqual({e['id'] for e in DATA['extensions']}, STUDIO_OWN)
        self.assertIn('FrameCore Works Toolbox', DATA['policy'])
        guide = (PLUGIN / 'skills/workflow-orchestrator/references/extensions.md').read_text(encoding='utf-8')
        self.assertIn('## Toolbox catalog', guide)
        listing = guide.split('## Recommended repositories list', 1)[1].split('\n## ', 1)[0]
        self.assertIn('[Toolbox catalog](#toolbox-catalog)', listing)
        self.assertIn('GitHub repositories recommended by FrameCore Works', listing)
        self.assertNotIn('Openverse', guide)
        moved = ('anatomy', 'hairline', 'huashu-art-motion', 'iso-glow', 'taste-skill', 'rea', 'pixel-plugin', 'upscayl',
                 'opencreator', 'agent-reach', 'adobe-skills', 'moneyprinterturbo', 'logo-design', 'open-design')
        menus = (PLUGIN / 'skills/workflow-orchestrator/references/startup-and-creative-menus.md').read_text(encoding='utf-8')
        self.assertIn('extensions.md#toolbox-catalog', menus)
        stale = []
        for path in [*(PLUGIN / 'skills').rglob('*.md'), *(PLUGIN / 'skills').rglob('*.py'), *(PLUGIN / 'integrations').rglob('*.md')]:
            for number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
                lowered = line.lower()
                for name in moved:
                    if f'extensions.py show {name}' in line or f'pinned `{name}` [extension]' in line:
                        stale.append(f'{path.relative_to(PLUGIN)}:{number}: {name}')
                    elif re.search(rf'(?<![\w-]){re.escape(name)}(?![\w-])', lowered) and ('optional extension' in lowered or "registry's" in lowered
                                              or f'registry entry `{name}`' in line):
                        stale.append(f'{path.relative_to(PLUGIN)}:{number}: {name}')
        self.assertEqual(stale, [])
        folder = PLUGIN / 'integrations/open-design'
        self.assertTrue((folder / 'LICENSE').read_text(encoding='utf-8').lstrip().startswith('Apache License'))
        self.assertIn('entry `open-design`', (folder / 'README.md').read_text(encoding='utf-8'))


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


    def test_earshot_runs_only_through_toolbox(self):
        # Owner handover 2026-10-22: local CLI/Python only, no MCP and no Gemini. Owner decisions 2026-10-29: Earshot is
        # built into FrameCore Works Toolbox; Studio keeps no earshot entry, no earshot plugin and no engine route.
        toolbox = next(e for e in DATA['extensions'] if e['id'] == 'framecore-works-toolbox')
        self.assertEqual(toolbox['repository'], 'https://github.com/FrameCoreWorks/framecore-works-toolbox')
        for host in ('claude_code', 'codex', 'chatgpt_work'):
            steps = toolbox['hosts'][host]['manual_steps']
            for needle in ('capabilities/earshot/scripts/runtime.py', 'status --json', 'install --tier', 'fetch-models', 'toolbox:toolbox'):
                self.assertIn(needle, steps, host)
        self.assertIn('claude plugin install toolbox@framecore-works-toolbox', toolbox['hosts']['claude_code']['manual_steps'])
        hosts = json.dumps(toolbox['hosts'])
        for second_route in ('pip install', 'archive/', '.zip', 'download.pytorch.org'):
            self.assertNotIn(second_route, hosts)
        current = [{k: v for k, v in e.items() if k != 'observed'} for e in DATA['extensions']]   # history stays
        registry = json.dumps(current, ensure_ascii=False)
        for gone in ('earshot-audio:earshot', 'plugins/earshot-audio', 'earshot-audio@'):
            self.assertNotIn(gone, registry)
        for allowed in ('upload audio after consent', 'explicitly authorized optional LLM upload', 'requires explicit consent'):
            self.assertNotIn(allowed, json.dumps(toolbox, ensure_ascii=False))
        routing = (PLUGIN / 'skills/pipeline-core/references/companion-routing.md').read_text(encoding='utf-8')
        self.assertIn('## Sound through Toolbox', routing)
        self.assertIn('`llm` and `mcp`', routing)
        self.assertIn('framecore-task-request/1', routing)
        link = 'companion-routing.md#sound-through-toolbox'
        for owner in ('hyperframes-workflow', 'opencut-video-studio', 'audio-production-director', 'remotion-video-production'):
            body = (PLUGIN / 'skills' / owner / 'SKILL.md').read_text(encoding='utf-8')
            self.assertIn('toolbox:toolbox', body, owner)
            self.assertIn(link, body, owner)
        for path in ('skills/pipeline-core/references/studio-integration-policy.md', 'skills/pipeline-core/references/loop-protocol.md'):
            self.assertIn(link, (PLUGIN / path).read_text(encoding='utf-8'), path)
        stale = [str(p.relative_to(PLUGIN)) for p in PLUGIN.rglob('*')
                 if p.is_file() and p.suffix in ('.md', '.json', '.py', '.yaml') and 'tests' not in p.parts and p.name not in ('release-history.md', 'CHANGELOG.md')
                 and any(gone in p.read_text(encoding='utf-8', errors='ignore')
                         for gone in ('earshot-audio:earshot', 'earshot-native-routing', 'native-earshot-cases'))]
        self.assertEqual(stale, [])
        # Owner decision 2026-10-29: the Openverse and Earshot files are physically removed from the package.
        for gone in ('integrations/openverse', 'skills/reference-pack-curator/scripts/openverse.py',
                     'skills/pipeline-core/references/earshot-native-routing.md', 'evals/native-earshot-cases.json'):
            self.assertFalse((PLUGIN / gone).exists(), gone)
        for overlay in ('motion-runtime', 'engine-runtime', 'media-runtime', 'session-runtimes'):
            for owner in ('hyperframes-workflow', 'opencut-video-studio', 'audio-production-director', 'remotion-video-production'):
                self.assertNotIn(overlay, (PLUGIN / 'skills' / owner / 'SKILL.md').read_text(encoding='utf-8'), f'private overlay {overlay} in {owner}')


    def test_every_update_offers_the_missing_companions(self):
        # Owner question 2026-10-29: one Studio update must also lead to Toolbox and Open Assets when they are missing.
        guide = (PLUGIN / 'skills/workflow-orchestrator/references/extensions.md').read_text(encoding='utf-8')
        section = guide.split('## Companion check after an update', 1)[1].split('\n## ', 1)[0]
        for needle in ('toolbox:toolbox', 'framecore-open-assets:open-assets', 'install both', 'The answer is the consent',
                       'claude plugin install toolbox@framecore-works-toolbox', 'framecore-open-assets@framecore-works',
                       'Plugin Creator', 'install_codex.py', 'never touch an existing engine folder'):
            self.assertIn(needle, section)
        self.assertIn('#companion-check-after-an-update',
                      (PLUGIN / 'skills/workflow-orchestrator/SKILL.md').read_text(encoding='utf-8'))
        root = PLUGIN.parent.parent
        for name in ('CHATGPT_UPDATE.md', 'CODEX_UPDATE.md', 'CLAUDE_INSTALL.md'):
            self.assertIn('companion-check-after-an-update', (root / name).read_text(encoding='utf-8'), name)
        prompt = (root / 'CHATGPT_UPDATE.md').read_text(encoding='utf-8').split('```text', 1)[1].split('```', 1)[0]
        self.assertIn('FrameCore Open Assets is missing here', prompt)

if __name__ == '__main__':
    unittest.main()
