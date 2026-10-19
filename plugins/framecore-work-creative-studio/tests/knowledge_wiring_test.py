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
    # anti-slop and Open Design: design craft
    'pipeline-core/references/craft-rules.md': ['static-graphic-design-creator/SKILL.md', 'hyperframes-workflow/SKILL.md',
                                                'pipeline-core/SKILL.md', 'output-critic-iteration/SKILL.md',
                                                'workflow-orchestrator/references/routing-boundaries.md'],
    'pipeline-core/assets/craft-lint/README.md': ['static-graphic-design-creator/SKILL.md', 'hyperframes-workflow/SKILL.md',
                                                  'pipeline-core/SKILL.md', 'output-critic-iteration/SKILL.md'],
    'pipeline-core/assets/design-md/README.md': ['static-graphic-design-creator/SKILL.md', 'pipeline-core/SKILL.md',
                                                 'delivery-documentation/SKILL.md', 'workflow-orchestrator/references/brand-identity-workflow.md'],
    'pipeline-core/assets/prompt-examples/README.md': ['static-graphic-design-creator/SKILL.md', 'pipeline-core/SKILL.md'],
    # anti-slop: writing
    'copy-voice/references/ai-writing-patterns.md': ['copy-voice/SKILL.md', 'pipeline-core/references/loop-protocol.md'],
    'copy-voice/scripts/ai_writing_check.py': ['copy-voice/SKILL.md', 'humanizer/SKILL.md', 'pipeline-core/SKILL.md'],
    # huashu-art-motion and iso-glow: motion
    'hyperframes-workflow/references/art-and-explainer-motion-direction.md': ['hyperframes-workflow/SKILL.md'],
    'hyperframes-workflow/assets/reference-breakdown/README.md': ['hyperframes-workflow/SKILL.md',
                                                                  'workflow-orchestrator/references/routing-boundaries.md'],
    'hyperframes-workflow/assets/iso-glow/README.md': ['hyperframes-workflow/SKILL.md'],
    'hyperframes-workflow/assets/motion-sync/audio_envelope.py': ['hyperframes-workflow/SKILL.md'],
    # songs on screen
    'hyperframes-workflow/assets/motion-sync/README.md#lyric-timing': ['hyperframes-workflow/SKILL.md', 'caption-studio/SKILL.md',
                                                                       'creative-music-video-director/SKILL.md',
                                                                       'workflow-orchestrator/references/routing-boundaries.md'],
    'hyperframes-workflow/assets/reel-starters/README.md': ['hyperframes-workflow/SKILL.md', 'hyperframes-workflow/references/claude-code-reels.md'],
    # dense kinetic reels and the scene logic check (owner review 2026-10-19)
    'hyperframes-workflow/references/dense-kinetic-reels.md': ['hyperframes-workflow/SKILL.md', 'hyperframes-workflow/references/reel-board-system.md', 'storyboard-sequence-architect/SKILL.md',
                                                               'hyperframes-workflow/references/motion-development-review.md'],
    # upscayl: enlarging images
    'static-graphic-design-creator/references/upscaling.md': ['static-graphic-design-creator/SKILL.md',
                                                              'workflow-orchestrator/references/routing-boundaries.md',
                                                              'delivery-documentation/references/print-ready-pdf.md'],
    # research without a browsing tool
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
                     'audio_envelope.py', 'breakdown.py', 'lyric_timing.py', 'motion_activity.py', 'web_reach.py'):
            self.assertIn(tool, card)


if __name__ == '__main__':
    unittest.main(verbosity=2)
