"""Pixel-look effects for FrameCut: pixelate, posterize and ordered dither (methods adapted from a review of pixel-mcp, MIT).

Ordered dither is stateless per pixel, so it is frame-stable on video; error diffusion is not and is deliberately absent."""
import subprocess
import sys
import unittest
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
RUNTIME = PACKAGE / 'skills/opencut-video-studio/assets/framecut'
sys.path.insert(0, str(RUNTIME))
from fc_core import FrameCutError
from fc_effects import catalogue, check_fixtures, picture, resolve
from fc_picture import pillow

Image = pillow()


def apply(image, effect_id, **params):
    return picture(image, [{'id': effect_id, 'version': 1, 'params': params}])


def gradient(width, height):
    image = Image.new('RGBA', (width, height))
    image.putdata([(x * 255 // max(1, width - 1), y * 255 // max(1, height - 1), (x + y) % 256, 255) for y in range(height) for x in range(width)])
    return image


class Catalogue(unittest.TestCase):
    def test_the_three_effects_are_versioned_and_their_fixtures_pass(self):
        for name in ('pixelate', 'posterize', 'ordered_dither'):
            self.assertIn((name, 1), catalogue())
        checked = check_fixtures()
        self.assertEqual(checked['status'], 'PASS')
        self.assertTrue({'pixelate', 'posterize', 'ordered_dither'} <= {c['id'] for c in checked['checks']})

    def test_defaults_leave_a_clip_unchanged(self):
        source = gradient(37, 23)
        for name in ('pixelate', 'posterize', 'ordered_dither'):
            self.assertEqual(list(apply(source, name).getdata()), list(source.getdata()), name)

    def test_out_of_range_parameters_are_refused(self):
        with self.assertRaises(FrameCutError):
            resolve({'id': 'pixelate', 'version': 1, 'params': {'block': 0}}, 'picture')
        with self.assertRaises(FrameCutError):
            resolve({'id': 'posterize', 'version': 1, 'params': {'levels': 1}}, 'picture')


class Pixelate(unittest.TestCase):
    def test_every_block_is_one_flat_colour_and_the_size_is_kept(self):
        result = apply(gradient(20, 13), 'pixelate', block=8)
        self.assertEqual(result.size, (20, 13))
        for top in range(0, 13, 8):
            for left in range(0, 20, 8):
                block = {result.getpixel((x, y)) for y in range(top, min(top + 8, 13)) for x in range(left, min(left + 8, 20))}
                self.assertEqual(len(block), 1, (left, top))

    def test_alpha_is_untouched(self):
        source = gradient(16, 16)
        source.putalpha(Image.linear_gradient('L').resize((16, 16)))
        self.assertEqual(list(apply(source, 'pixelate', block=4).getchannel('A').getdata()), list(source.getchannel('A').getdata()))


class Posterize(unittest.TestCase):
    def test_levels_limit_the_values_per_channel(self):
        result = apply(gradient(64, 64), 'posterize', levels=4)
        for channel in range(3):
            values = {pixel[channel] for pixel in result.getdata()}
            self.assertLessEqual(len(values), 4, values)
            self.assertTrue(values <= {0, 85, 170, 255}, values)


class OrderedDither(unittest.TestCase):
    def test_a_flat_grey_becomes_a_stable_checker_of_the_two_levels(self):
        source = Image.new('RGBA', (16, 16), (128, 128, 128, 255))
        first = apply(source, 'ordered_dither', levels=2)
        second = apply(source, 'ordered_dither', levels=2)
        self.assertEqual(list(first.getdata()), list(second.getdata()))
        values = [pixel[0] for pixel in first.getdata()]
        self.assertEqual(set(values), {0, 255})
        self.assertTrue(112 <= values.count(255) <= 144, values.count(255))   # about half, from the 4x4 Bayer tile

    def test_the_pattern_is_pinned_to_screen_coordinates(self):
        source = Image.new('RGBA', (16, 16), (100, 100, 100, 255))
        whole = apply(source, 'ordered_dither', levels=2)
        again = apply(source.copy(), 'ordered_dither', levels=2)
        for y in range(16):
            for x in range(16):
                self.assertEqual(whole.getpixel((x, y)), again.getpixel((x, y)))


class Cli(unittest.TestCase):
    def test_effects_check_passes_from_the_command_line(self):
        done = subprocess.run([sys.executable, '-B', str(RUNTIME / 'framecut.py'), 'effects', '--check'], capture_output=True, text=True, timeout=60)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn('"PASS"', done.stdout)


class Render(unittest.TestCase):
    def test_pixelate_reaches_the_rendered_film(self):
        import shutil
        import tempfile
        from fc_core import commit_revision
        from fc_media import ffmpeg, ingest
        from fc_render import render
        from framecut import project_init
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ffmpeg(['-f', 'lavfi', '-i', 'testsrc=s=320x180:r=30:d=2', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', str(root / 'src.mp4')])
            project = project_init(root / 'project.json', 'pixel')
            project['assets']['a'] = ingest(root, 'src.mp4', 'a')
            project['sequences'] = [{'id': 'main', 'fps': {'num': 30, 'den': 1}, 'duration': 45, 'clips': [
                {'id': 'c1', 'asset': 'a', 'start': 0, 'duration': 45, 'source_in': 0,
                 'effects': [{'id': 'pixelate', 'version': 1, 'params': {'block': 16}}]}]}]
            project['deliverables'] = [{'id': 'wide', 'sequence': 'main', 'width': 320, 'height': 180}]
            project = commit_revision(root / 'project.json', project, 1, 'pixel look')
            render(project, root, 'wide', 'out', mode='preview', max_disk_mb=128)
            ffmpeg(['-i', str(root / 'out/video.mp4'), '-vf', 'select=eq(n\\,10)', '-frames:v', '1', str(root / 'frame.png')])
            from PIL import Image as PILImage
            frame = PILImage.open(root / 'frame.png').convert('RGB')
            flat = 0
            for top in range(0, 160, 16):
                for left in range(0, 320, 16):
                    a, b = frame.getpixel((left + 2, top + 2)), frame.getpixel((left + 13, top + 13))
                    flat += all(abs(x - y) <= 12 for x, y in zip(a, b))
            self.assertGreater(flat / (10 * 20), 0.9, flat)


if __name__ == '__main__':
    unittest.main()
