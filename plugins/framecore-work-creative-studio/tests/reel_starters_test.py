"""Reel starters (hyperframes-workflow/assets/reel-starters): HyperFrames contract and copy slots."""
import pathlib
import re
import unittest

STARTERS = pathlib.Path(__file__).resolve().parent.parent / 'skills/hyperframes-workflow/assets/reel-starters'


class ReelStartersTest(unittest.TestCase):
    def test_each_starter_is_a_hyperframes_composition_with_slots(self):
        pages = sorted(STARTERS.glob('*/index.html'))
        self.assertTrue(pages)
        for page in pages:
            html = page.read_text()
            root = re.search(r'<div id="root"([^>]*)>', html).group(1)
            for attribute in ('data-composition-id="main"', 'data-start="0"', 'data-duration=', 'data-width="1080"', 'data-height="1920"'):
                self.assertIn(attribute, root, page)
            self.assertIn('gsap.timeline({ paused: true })', html)
            self.assertIn("window.__timelines['main'] = tl", html)
            self.assertNotIn('Math.random', html)          # deterministic: same frame for the same time
            slots = set(re.findall(r'data-copy="(\w+)"', html))
            copy = re.search(r'const COPY = \{(.*?)\};', html, re.S).group(1)
            for slot in slots:
                self.assertRegex(copy, rf'\b{slot}:', f'{page}: slot {slot} has no COPY entry')
            duration = float(re.search(r'data-duration="([\d.]+)"', root).group(1))
            ends = [float(x) for x in re.findall(r"\['#b\d+', [\d.]+, ([\d.]+)\]", html)]
            self.assertEqual(max(ends), duration, page)

    def test_readme_lists_every_starter(self):
        readme = (STARTERS / 'README.md').read_text()
        for page in STARTERS.glob('*/index.html'):
            self.assertIn(f'({page.parent.name}/index.html)', readme)


if __name__ == '__main__':
    unittest.main()
