"""Knowledge adapted from outside repositories is wired into the skills that must use it, not only stored.

Each row names a shared reference or tool and the entry files (a SKILL.md or a routing reference) that must link it,
so a model loading that owner reaches it in one hop. Add a row when a new reference or tool is integrated.
"""
import os
import pathlib
import unittest

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
S = 'skills/'

WIRING = {
    # Motion-module rows moved to FrameMotion with Studio 1.178.0.
    'pipeline-core/references/craft-rules.md': ['static-graphic-design-creator/SKILL.md', 'pipeline-core/SKILL.md', 'output-critic-iteration/SKILL.md', 'workflow-orchestrator/references/routing-boundaries.md'],
    'pipeline-core/assets/craft-lint/README.md': ['static-graphic-design-creator/SKILL.md', 'pipeline-core/SKILL.md', 'output-critic-iteration/SKILL.md'],
    'pipeline-core/assets/design-md/README.md': ['static-graphic-design-creator/SKILL.md', 'pipeline-core/SKILL.md', 'delivery-documentation/SKILL.md', 'workflow-orchestrator/references/brand-identity-workflow.md'],
    'pipeline-core/assets/prompt-examples/README.md': ['static-graphic-design-creator/SKILL.md', 'pipeline-core/SKILL.md'],
    'copy-voice/references/ai-writing-patterns.md': ['copy-voice/SKILL.md', 'pipeline-core/references/loop-protocol.md'],
    'copy-voice/scripts/ai_writing_check.py': ['copy-voice/SKILL.md', 'humanizer/SKILL.md', 'pipeline-core/SKILL.md'],
    'static-graphic-design-creator/references/upscaling.md': ['static-graphic-design-creator/SKILL.md', 'workflow-orchestrator/references/routing-boundaries.md', 'delivery-documentation/references/print-ready-pdf.md'],
    'pipeline-core/references/companion-routing.md': ['pipeline-core/SKILL.md', 'audio-production-director/SKILL.md', 'pipeline-core/references/open-assets-native-routing.md'],
    'delivery-documentation/scripts/companion_intake.py': ['delivery-documentation/SKILL.md', 'pipeline-core/references/companion-routing.md'],
    'ugc/references/disclosure-by-platform-and-market.md': ['ugc/SKILL.md', 'ugc/references/formats-scripts-and-disclosure.md'],
    'delivery-documentation/assets/handoff-letter.en.md': ['delivery-documentation/SKILL.md', 'delivery-documentation/references/client-handoff.md'],
    'delivery-documentation/assets/acceptance-protocol.en.md': ['delivery-documentation/SKILL.md', 'delivery-documentation/references/client-handoff.md'],
    'copy-voice/assets/client-emails.en.md': ['copy-voice/SKILL.md', 'brief-architect/references/client-offer-and-quote.md', 'pipeline-core/references/client-projects.md'],
    'marketing/references/positioning-and-audience-research.md': ['marketing/SKILL.md'],
    'creative-video-producer/references/production-worksheets.md': ['creative-video-producer/SKILL.md'],
    'image-prompt-architect/references/structured-image-prompts.md': ['image-prompt-architect/SKILL.md', 'pipeline-core/assets/prompt-record/README.md', 'static-graphic-design-creator/SKILL.md'],
    'video-prompt-architect/references/structured-video-prompts.md': ['video-prompt-architect/SKILL.md', 'pipeline-core/assets/prompt-record/README.md'],
    'pipeline-core/assets/prompt-record/README.md': ['image-prompt-architect/SKILL.md', 'video-prompt-architect/SKILL.md'],
    'image-prompt-architect/references/narrative-image-prompts.md': ['image-prompt-architect/SKILL.md', 'static-graphic-design-creator/SKILL.md'],
    'video-prompt-architect/references/narrative-video-prompts.md': ['video-prompt-architect/SKILL.md'],
    'pipeline-core/references/craft-rules.md#frame-empty-space-and-pictures': ['static-graphic-design-creator/SKILL.md', 'output-critic-iteration/references/review-and-repair.md'],
    'output-critic-iteration/references/review-and-repair.md#authored-design-review': ['static-graphic-design-creator/SKILL.md'],
    'research-evidence/assets/web-reach/README.md': ['research-evidence/SKILL.md'],
}


class KnowledgeWiring(unittest.TestCase):
    def test_every_integrated_reference_is_linked_from_its_owners(self):
        missing = []
        for target, entries in WIRING.items():
            self.assertTrue((PLUGIN / S / target.partition('#')[0]).exists(), target)
            for entry in entries:
                text = (PLUGIN / S / entry).read_text(encoding='utf-8')
                own, _, anchor = target.partition('#')
                rel = os.path.relpath(own, pathlib.Path(entry).parent).replace(os.sep, '/')
                # a link to the file, or to a heading in it, counts; a named anchor must be linked as named
                needles = ['(' + rel + '#' + anchor + ')'] if anchor else ['(' + rel + ')', '(' + rel + '#']
                if not any(n in text for n in needles):
                    missing.append(f'{entry} does not link {target}')
        self.assertEqual(missing, [], '\n'.join(missing))

    def test_the_capability_card_names_every_wired_tool(self):
        card = (PLUGIN / S / 'workflow-orchestrator/assets/capability-card.json').read_text(encoding='utf-8')
        for tool in ('craft_lint.py', 'contrast_check.py', 'design_md.py', 'prompt_examples.py', 'ai_writing_check.py',
                     'web_reach.py'):
            self.assertIn(tool, card)


if __name__ == '__main__':
    unittest.main(verbosity=2)
