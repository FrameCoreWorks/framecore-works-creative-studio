"""earshot-audio package: one skill, upstream files copied byte for byte, consistent manifests, local only."""
import hashlib
import json
import pathlib
import re
import unittest

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
ROOT = PLUGIN.parent.parent
COMMIT = '591fa3e028032e6dce56620a20e932e35667e8d8'
TREE = 'd6f2dbc43f7b38b2147cfd04bbd7aa9055701f1a'


def manifest():
    return json.loads((PLUGIN / 'upstream.json').read_text(encoding='utf-8'))


class Package(unittest.TestCase):
    def test_exactly_one_skill(self):
        skills = sorted(p.relative_to(PLUGIN).as_posix() for p in PLUGIN.rglob('SKILL.md'))
        self.assertEqual(skills, ['skills/earshot/SKILL.md'])

    def test_copied_files_match_the_pin(self):
        data = manifest()
        self.assertEqual((data['commit'], data['tree'], data['tag']), (COMMIT, TREE, 'v0.4.0'))
        self.assertEqual(len(data['files']), 282)
        self.assertGreaterEqual(len(data['copied']), 30)
        for plugin_path, upstream_path in data['copied'].items():
            digest = hashlib.sha256((PLUGIN / plugin_path).read_bytes()).hexdigest()
            self.assertEqual(digest, data['files'][upstream_path], plugin_path)
        self.assertIn('skills/real-sound/scripts/licences.py', data['copied'].values())
        self.assertIn('skills/real-sound/references/process.md', data['copied'].values())

    def test_manifests_agree(self):
        versions = set()
        for path in ('plugin.json', '.claude-plugin/plugin.json', '.codex-plugin/plugin.json'):
            data = json.loads((PLUGIN / path).read_text(encoding='utf-8'))
            self.assertEqual(data['name'], 'earshot-audio', path)
            versions.add(data['version'])
        self.assertEqual(versions, {'1.0.9'})
        market = json.loads((ROOT / '.claude-plugin/marketplace.json').read_text(encoding='utf-8'))
        entries = {p['name']: p for p in market['plugins']}
        self.assertEqual(entries['earshot-audio']['source'], './plugins/earshot-audio')
        self.assertEqual(entries['earshot-audio']['version'], '1.0.9')
        studio = json.loads((ROOT / 'plugins/framecore-work-creative-studio/.claude-plugin/plugin.json').read_text(encoding='utf-8'))
        self.assertEqual(entries['framecore-work-creative-studio']['version'], studio['version'])

    def test_skill_is_local_only(self):
        text = (PLUGIN / 'skills/earshot/SKILL.md').read_text(encoding='utf-8')
        self.assertRegex(text, r'(?m)^name: earshot$')
        for needle in ('runtime.py', '--yes', 'Freesound', 'status', 'kit.lock.json', 'launch'):
            self.assertIn(needle, text)
        for banned in ('mcp add', '.mcp.json', 'GEMINI_API_KEY', 'pip install -e', 'llm_critique'):
            self.assertNotIn(banned, text)
        self.assertIn('at most one question', text)
        # final review I2/I3: every engine call goes through the launcher's environment; no bare venv interpreter
        self.assertIn('`{{PY}}` means `python3 <runtime> exec`', text)
        self.assertNotIn('write one short script run with the venv', text)   # companion C12 2026-10-22: five scene questions at once
        description = re.search(r'(?m)^description: (.+)$', text).group(1)
        self.assertLessEqual(len(description), 1024)

    def test_written_critique_replaces_the_upload_with_local_evidence(self):
        # Owner decision 2026-10-23: a review in words written by the host model from local readings, instead of
        # upstream's Gemini upload; free, no key, nothing leaves the machine.
        skill = (PLUGIN / 'skills/earshot/SKILL.md').read_text(encoding='utf-8')
        self.assertIn('references/written-critique.md', skill)
        self.assertIn('A review in words', skill)
        ref = (PLUGIN / 'skills/earshot/references/written-critique.md').read_text(encoding='utf-8')
        for needle in ('timeline', 'sheet', 'critique', 'measure', 'describe', 'sync', 'realism', 'mix', 'loudness',
                       'cheap', 'not a measurement', 'did not hear'):
            self.assertIn(needle, ref)
        self.assertNotIn('Gemini', ref.split('## Why not an upload')[0])

    def test_light_tier_promises_only_what_runs_without_models(self):
        # End-to-end run 2026-10-23: timeline and sheet stopped on the missing CLAP model in a light install;
        # measure, critique --fast, sfx and kit ran.
        skill = (PLUGIN / 'skills/earshot/SKILL.md').read_text(encoding='utf-8')
        light = re.search(r'`light_ready` \(([^)]*)\)', skill).group(1)
        for needle in ('measure', 'critique --fast', 'sfx', 'kit'):
            self.assertIn(needle, light)
        for needle in ('timeline', 'sheet'):
            self.assertNotIn(needle, light)
        full = re.search(r'`full_ready` with `models_cached` \(([^)]*)\)', skill).group(1)
        for needle in ('timeline', 'sheet'):
            self.assertIn(needle, full)
        self.assertIn('../../scripts/runtime.py', skill)
        ref = (PLUGIN / 'skills/earshot/references/written-critique.md').read_text(encoding='utf-8')
        self.assertIn('critique --fast', ref)
        self.assertNotIn('steps 1 to 4 still run', ref)
        handoff = (PLUGIN / 'skills/earshot/references/studio-handoff.md').read_text(encoding='utf-8')
        self.assertIn('light tier', handoff)

    def test_a_missing_engine_offers_both_routes(self):
        # Owner decision 2026-10-23 (option A): ChatGPT Work fell back to Studio's engine without asking.
        skill = (PLUGIN / 'skills/earshot/SKILL.md').read_text(encoding='utf-8')
        self.assertIn("`sound.py`), offer them in the same", skill)
        self.assertIn('run neither before the answer', skill)

    def test_every_effect_is_chosen_by_listening(self):
        # Owner report 2026-10-23: a kit preset's hit had a metallic debris tail; the system must pick the fitting sound.
        skill = (PLUGIN / 'skills/earshot/SKILL.md').read_text(encoding='utf-8')
        section = skill.split('**Choose every effect by listening', 1)[1].split('**Make or fit', 1)[0]
        for needle in ('rank "<description>"', '--alts <confusions>', 'onsets per second', 'phone', 'rejected',
                       'gates, not trade-offs', 'also when nothing passes'):
            self.assertIn(needle, section)

    def test_superpowers_is_the_method_for_the_code_around_earshot(self):
        # Owner request 2026-10-23: Superpowers fully supports Earshot's code.
        skill = (PLUGIN / 'skills/earshot/SKILL.md').read_text(encoding='utf-8')
        for name in ('writing-plans', 'test-driven-development', 'systematic-debugging', 'verification-before-completion'):
            self.assertIn(f'superpowers:{name}', skill)

    def test_earshot_is_credited_to_leon_lin_everywhere_users_see_it(self):
        # Owner decision 2026-10-23: Earshot keeps its name and is plainly marked as Leon Lin's repository.
        for path in ('plugin.json', '.claude-plugin/plugin.json', '.codex-plugin/plugin.json'):
            data = json.loads((PLUGIN / path).read_text(encoding='utf-8'))
            self.assertTrue(data['description'].startswith('Earshot by Leon Lin (github.com/Leonxlnx/earshot'), path)
        self.assertIn('Leon Lin', (PLUGIN / '.codex-plugin/plugin.json').read_text(encoding='utf-8').split('displayName')[1][:40])

    def test_licence_and_notice(self):
        data = manifest()
        self.assertEqual(hashlib.sha256((PLUGIN / 'LICENSE').read_bytes()).hexdigest(), data['files']['LICENSE'])
        notice = (PLUGIN / 'NOTICE').read_text(encoding='utf-8')
        self.assertIn('Leon Lin', notice)
        self.assertIn(COMMIT, notice)

    def test_launcher_pin_matches_the_manifest(self):
        text = (PLUGIN / 'scripts/runtime.py').read_text(encoding='utf-8')
        self.assertIn(COMMIT, text)
        self.assertIn(TREE, text)


if __name__ == '__main__':
    unittest.main()
