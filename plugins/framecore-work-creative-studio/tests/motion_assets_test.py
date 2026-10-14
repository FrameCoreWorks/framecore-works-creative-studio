"""Generated cut-out assets (hyperframes-workflow/assets/motion-assets/asset_check.py): check, difference matte, chroma key."""
import contextlib
import importlib.util
import io
import pathlib
import tempfile
import unittest

import numpy as np
from PIL import Image, ImageDraw

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
TOOL = PLUGIN / 'skills/hyperframes-workflow/assets/motion-assets/asset_check.py'
spec = importlib.util.spec_from_file_location('asset_check', TOOL)
ac = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ac)


def disc(size=400, radius=120, fill=(90, 90, 100, 255), background=(0, 0, 0, 0), mode='RGBA', offset=0):
    image = Image.new(mode, (size, size), background)
    c = size // 2 + offset
    ImageDraw.Draw(image).ellipse([c - radius, c - radius, c + radius, c + radius], fill=fill)
    return image


def glow_over(background, offset=0):
    """A soft red glow (partly transparent) composited over a flat background, as a generator would render it."""
    size = 300
    y, x = np.mgrid[:size, :size]
    a = np.clip(1 - np.hypot(x - 150 - offset, y - 150) / 110, 0, 1)[..., None]
    a[np.hypot(x - 150 - offset, y - 150) < 40] = 1.0            # an opaque core
    colour = np.array([230, 40, 30], dtype=np.float32)
    out = colour * a + np.array(background, dtype=np.float32) * (1 - a)
    return Image.fromarray(out.astype(np.uint8), 'RGB'), a[..., 0]


class Check(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = pathlib.Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def save(self, image, name):
        path = self.dir / name
        image.save(path)
        return str(path)

    def test_a_clean_cut_out_passes_and_size_is_checked_against_the_zoom(self):
        path = self.save(disc(), 'clean.png')
        self.assertEqual(ac.check_file(path)['verdict'], 'PASS')
        small = ac.check_file(path, screen_px=360, zoom=1.3)
        self.assertEqual(small['verdict'], 'REPAIR')
        self.assertIn('too small', small['problems'][0])

    def test_an_opaque_file_and_a_painted_checkerboard_are_not_transparency(self):
        self.assertIn('opaque', ac.check_file(self.save(disc(mode='RGB', background=(255, 255, 255)), 'flat.png'))['problems'][0])
        board = Image.new('RGB', (400, 400), (255, 255, 255))
        draw = ImageDraw.Draw(board)
        for i in range(0, 400, 16):
            for j in range(0, 400, 16):
                if (i // 16 + j // 16) % 2:
                    draw.rectangle([i, j, i + 15, j + 15], fill=(204, 204, 204))
        draw.ellipse([100, 100, 300, 300], fill=(90, 90, 100))
        report = ac.check_file(self.save(board, 'board.png'))
        self.assertIn('checkerboard', report['problems'][0])

    def test_a_crude_key_leaves_a_green_fringe_that_is_reported(self):
        image = disc(fill=(0, 230, 0, 255), radius=124)                     # a green rim left by a hard key
        ImageDraw.Draw(image).ellipse([200 - 120, 200 - 120, 200 + 120, 200 + 120], fill=(90, 90, 100, 255))
        report = ac.check_file(self.save(image, 'fringe.png'))
        self.assertEqual(report['verdict'], 'REPAIR')
        self.assertTrue(any('green fringe' in p for p in report['problems']))

    def test_difference_matte_recovers_partial_transparency(self):
        white, truth = glow_over((255, 255, 255))
        black, _ = glow_over((0, 0, 0))
        out = self.dir / 'glow.png'
        report = ac.difference_matte(self.save(white, 'w.png'), self.save(black, 'b.png'), str(out))
        self.assertEqual(report['verdict'], 'PASS')
        alpha = np.asarray(Image.open(out))[..., 3] / 255.0
        self.assertLess(float(np.abs(alpha - truth).mean()), 0.03)
        self.assertGreater(float(((alpha > 0.1) & (alpha < 0.9)).mean()), 0.05)   # soft glow kept, not a hard cut

    def test_a_subject_that_moved_between_the_versions_is_refused(self):
        white, _ = glow_over((255, 255, 255))
        black, _ = glow_over((0, 0, 0), offset=25)
        out = self.dir / 'moved.png'
        report = ac.difference_matte(self.save(white, 'w.png'), self.save(black, 'b.png'), str(out))
        self.assertEqual(report['verdict'], 'REPAIR')
        self.assertFalse(out.exists())

    def test_a_grey_subject_that_moved_is_refused_too(self):
        # Audit ASSET-01: a grey subject's difference has no colour, so only its edges show the move.
        white = disc(fill=(128, 128, 128, 255), background=(255, 255, 255, 255), mode='RGBA').convert('RGB')
        black = disc(fill=(128, 128, 128, 255), background=(0, 0, 0, 255), mode='RGBA', offset=20).convert('RGB')
        aligned = disc(fill=(128, 128, 128, 255), background=(0, 0, 0, 255), mode='RGBA').convert('RGB')
        moved = ac.difference_matte(self.save(white, 'w.png'), self.save(black, 'b.png'), str(self.dir / 'moved.png'))
        self.assertEqual(moved['verdict'], 'REPAIR')
        kept = ac.difference_matte(self.save(white, 'w2.png'), self.save(aligned, 'b2.png'), str(self.dir / 'kept.png'))
        self.assertEqual(kept['verdict'], 'PASS', kept)

    def test_a_fully_transparent_file_is_not_an_asset(self):
        report = ac.check_file(self.save(Image.new('RGBA', (200, 200), (0, 0, 0, 0)), 'empty.png'))
        self.assertEqual(report['verdict'], 'REPAIR')
        self.assertIn('nothing visible', report['problems'][0])

    def test_chroma_key_cuts_a_solid_subject_and_refuses_one_with_its_own_green(self):
        grey = self.save(disc(fill=(120, 120, 130, 255), background=(0, 255, 0, 255), mode='RGBA'), 'grey.png')
        out = self.dir / 'grey-cut.png'
        self.assertEqual(ac.chroma_key(grey, str(out))['verdict'], 'PASS')
        alpha = np.asarray(Image.open(out))[..., 3]
        self.assertEqual(alpha[5, 5], 0)
        self.assertEqual(alpha[200, 200], 255)
        self.assertEqual(ac.check_file(str(out))['verdict'], 'PASS')
        bottle = disc(fill=(120, 120, 130, 255), background=(0, 255, 0, 255))
        ImageDraw.Draw(bottle).rectangle([170, 170, 230, 230], fill=(30, 140, 40, 255))   # a green label on the subject
        report = ac.chroma_key(self.save(bottle, 'bottle.png'), str(self.dir / 'bottle-cut.png'))
        self.assertEqual(report['verdict'], 'REPAIR')

    def test_outputs_are_never_overwritten_and_bad_input_exits_2(self):
        grey = self.save(disc(background=(0, 255, 0, 255)), 'g.png')
        taken = self.save(disc(), 'taken.png')
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(ac.main(['key', grey, '--out', taken]), 2)
            self.assertEqual(ac.main(['check', str(self.dir / 'missing.png')]), 2)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(ac.main(['check', taken]), 0)


if __name__ == '__main__':
    unittest.main()
