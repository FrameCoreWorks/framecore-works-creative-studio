"""A moment the user marks on supplied footage must sound (motion-sound/generate.py, sound.py).

Found in the 2026-10-16 test reel: two of three sound designs chose a silent landing, so the landing the user marked
on the hook rendered nothing and the mix failed its timing check as missing."""
import pathlib
import sys
import unittest

SOUND = pathlib.Path(__file__).resolve().parent.parent / 'skills/hyperframes-workflow/assets/motion-sound'
sys.path.insert(0, str(SOUND))
import generate  # noqa: E402

EDITORIAL = {'moods': {'editorial': 1.0, 'calm': 0.45, 'technical': 0.3}, 'pace': 'medium'}


def landing_kinds(audible, seeds=range(60)):
    return {generate.design_effects(EDITORIAL, seed, 'A major', None, None, audible)[0]['landing']['kind'] for seed in seeds}


class MarkedLanding(unittest.TestCase):
    def test_an_editorial_video_can_choose_a_silent_landing(self):
        self.assertIn('none', landing_kinds(()))

    def test_a_marked_landing_is_never_designed_silent(self):
        kinds = landing_kinds({'landing'})
        self.assertNotIn('none', kinds)
        self.assertTrue(kinds)


if __name__ == '__main__':
    unittest.main()
