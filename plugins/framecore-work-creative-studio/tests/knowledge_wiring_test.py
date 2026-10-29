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
    # hairline: rounded-solid line figures for video (owner request 2026-10-26)
    'hyperframes-workflow/assets/hairline/README.md': ['hyperframes-workflow/SKILL.md'],
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
    # earshot: hearing and placing sound
    'pipeline-core/references/companion-routing.md': ['pipeline-core/SKILL.md', 'audio-production-director/SKILL.md',
        'pipeline-core/references/open-assets-native-routing.md'],
    'delivery-documentation/scripts/companion_intake.py': ['delivery-documentation/SKILL.md', 'pipeline-core/references/companion-routing.md'],
    'hyperframes-workflow/assets/sound-listen/README.md': ['hyperframes-workflow/SKILL.md', 'audio-production-director/SKILL.md',
                                                           'hyperframes-workflow/assets/motion-sound/README.md'],
    'hyperframes-workflow/references/sound-listening-and-motion-sfx.md': ['hyperframes-workflow/SKILL.md', 'audio-production-director/SKILL.md',
                                                                          'hyperframes-workflow/assets/motion-sound/README.md'],
    # awesome-opus5-5-videos: the Opus 5.5 gallery and prompt guide (owner request 2026-10-24)
    'hyperframes-workflow/assets/motion-prompt-library/README.md#opus-55-gallery': ['hyperframes-workflow/SKILL.md', 'remotion-video-production/SKILL.md', 'storyboard-sequence-architect/SKILL.md',
                                                                                  'hyperframes-workflow/references/motion-quality-research.md'],
    'hyperframes-workflow/assets/motion-prompt-library/opus-gallery-shortlist.md': ['hyperframes-workflow/SKILL.md', 'storyboard-sequence-architect/SKILL.md',
                                                                      'hyperframes-workflow/assets/motion-prompt-library/README.md'],
    'hyperframes-workflow/assets/motion-prompt-library/README.md#writing-a-prompt-for-a-coded-film': ['hyperframes-workflow/SKILL.md'],
    # dated platform cards (roadmap 2026-10-24, references 2 and 3)
    'caption-studio/references/platform-caption-specs.md': ['caption-studio/SKILL.md', 'caption-studio/references/readability-defaults.md', 'ugc/SKILL.md'],
    'ugc/references/disclosure-by-platform-and-market.md': ['ugc/SKILL.md', 'ugc/references/formats-scripts-and-disclosure.md'],
    # English source versions of the client templates (review recommendation 4)
    'delivery-documentation/assets/handoff-letter.en.md': ['delivery-documentation/SKILL.md', 'delivery-documentation/references/client-handoff.md'],
    'delivery-documentation/assets/acceptance-protocol.en.md': ['delivery-documentation/SKILL.md', 'delivery-documentation/references/client-handoff.md'],
    'copy-voice/assets/client-emails.en.md': ['copy-voice/SKILL.md', 'brief-architect/references/client-offer-and-quote.md', 'pipeline-core/references/client-projects.md'],
    # method references for Brand Strategy and Video Producer (review recommendations 5 and 6)
    'marketing/references/positioning-and-audience-research.md': ['marketing/SKILL.md'],
    'creative-video-producer/references/production-worksheets.md': ['creative-video-producer/SKILL.md'],
    # structured (JSON) prompts and prompt records (owner request 2026-10-25)
    'image-prompt-architect/references/structured-image-prompts.md': ['image-prompt-architect/SKILL.md', 'pipeline-core/assets/prompt-record/README.md', 'static-graphic-design-creator/SKILL.md'],
    'video-prompt-architect/references/structured-video-prompts.md': ['video-prompt-architect/SKILL.md', 'pipeline-core/assets/prompt-record/README.md'],
    'pipeline-core/assets/prompt-record/README.md': ['image-prompt-architect/SKILL.md', 'video-prompt-architect/SKILL.md'],
    'image-prompt-architect/references/narrative-image-prompts.md': ['image-prompt-architect/SKILL.md', 'static-graphic-design-creator/SKILL.md'],
    'video-prompt-architect/references/narrative-video-prompts.md': ['video-prompt-architect/SKILL.md'],
    # taste-skill: frame, empty space and pictures; mockup look passes (owner request 2026-10-26)
    'pipeline-core/references/craft-rules.md#frame-empty-space-and-pictures': ['static-graphic-design-creator/SKILL.md', 'output-critic-iteration/references/review-and-repair.md'],
    'output-critic-iteration/references/review-and-repair.md#authored-design-review': ['static-graphic-design-creator/SKILL.md'],
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
                     'audio_envelope.py', 'hairline-kit.js', 'breakdown.py', 'lyric_timing.py', 'motion_activity.py', 'web_reach.py'):
            self.assertIn(tool, card)


if __name__ == '__main__':
    unittest.main(verbosity=2)
