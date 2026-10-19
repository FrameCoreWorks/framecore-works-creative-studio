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


if __name__ == '__main__':
    unittest.main()
