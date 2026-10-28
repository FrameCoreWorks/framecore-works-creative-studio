"""Portable package identity, discovery and provider reference checks."""
import json
from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]


class Package(unittest.TestCase):
    def test_manifests_agree(self):
        manifests=[json.loads((ROOT/p).read_text()) for p in
                   ('plugin.json','.claude-plugin/plugin.json','.codex-plugin/plugin.json')]
        self.assertEqual({m['name'] for m in manifests},{'framecore-open-assets'})
        self.assertEqual({m['version'] for m in manifests},{'0.2.0'})
        self.assertEqual({m['license'] for m in manifests},{'Apache-2.0'})
        self.assertIn('Apache License',(ROOT/'LICENSE').read_text())
        root=manifests[0]
        self.assertEqual(root['$schema'],'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json')
        interface=root['extensions']['com.openai']['interface']
        self.assertLessEqual(len(interface['shortDescription']),30)
        self.assertEqual(interface,manifests[2]['interface'])

    def test_discovery_and_local_references(self):
        self.assertEqual([p.relative_to(ROOT).as_posix() for p in ROOT.rglob('SKILL.md')],['skills/open-assets/SKILL.md'])
        skill=(ROOT/'skills/open-assets/SKILL.md').read_text()
        self.assertTrue(skill.startswith('---\nname: open-assets\n'))
        for p in ROOT.rglob('*.md'):
            for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
                if '://' not in target and not target.startswith('#'):
                    self.assertTrue((p.parent/target.split('#')[0]).exists(),(p,target))

    def test_every_candidate_has_policy_and_official_sources(self):
        data=json.loads((ROOT/'providers.json').read_text())
        self.assertEqual(len(data),18)
        for id,r in data.items():
            self.assertIn('Sources:',(ROOT/r['reference']).read_text())
            if r['policy']=='documented':
                self.assertTrue((ROOT/f'scripts/providers/{id}.py').is_file())
                self.assertTrue(r['allowed_domains'])
            else:
                self.assertTrue(r['reason']);self.assertIsNone(r['module'])

    def test_marketplace_identity(self):
        market=json.loads((ROOT.parents[1]/'.claude-plugin/marketplace.json').read_text())
        entry=next(x for x in market['plugins'] if x['name']=='framecore-open-assets')
        self.assertEqual(entry['source'],'./plugins/framecore-open-assets')
        self.assertEqual(entry['version'],'0.2.0')


if __name__=='__main__':unittest.main()
