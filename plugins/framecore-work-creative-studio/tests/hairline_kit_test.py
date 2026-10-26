"""Hairline kit (hyperframes-workflow/assets/hairline): rounded solids and time functions for seekable line-figure video."""
import json
import pathlib
import shutil
import subprocess
import unittest

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
KIT = PLUGIN / 'skills/hyperframes-workflow/assets/hairline'
EXAMPLE = KIT / 'examples/spice-rack'


def run(js):
    script = f"const H = require({json.dumps(str(KIT / 'hairline-kit.js'))});\n{js}"
    return json.loads(subprocess.run(['node', '-e', script], capture_output=True, text=True, check=True).stdout)


class Files(unittest.TestCase):
    def test_the_example_carries_an_identical_kit_and_both_render_routes(self):
        self.assertEqual((KIT / 'hairline-kit.js').read_bytes(), (EXAMPLE / 'hairline-kit.js').read_bytes())
        page = (EXAMPLE / 'index.html').read_text()
        for needle in ('<script src="hairline-kit.js"></script>', 'window.renderFrame = renderFrame', "window.__timelines['main']",
                       'data-composition-id="main"', 'data-duration="8"'):
            self.assertIn(needle, page)
        for source in (page, (KIT / 'hairline-kit.js').read_text()):
            self.assertNotIn('requestAnimationFrame(', source)
            self.assertNotIn('performance.now(', source)
            self.assertNotIn('setTimeout(', source)
        self.assertNotIn('filter', page.split('<script>')[1], 'the figure has no glow or filter')
        self.assertIn('Lucas Marques', (KIT / 'LICENSE.upstream').read_text())


@unittest.skipUnless(shutil.which('node'), 'needs Node.js')
class Kernel(unittest.TestCase):
    def test_the_spring_step_starts_at_rest_overshoots_little_and_settles(self):
        r = run('const xs = Array.from({length: 401}, (_, i) => H.springStep(i / 100));'
                'console.log(JSON.stringify({ zero: H.springStep(0), neg: H.springStep(-1), max: Math.max(...xs), end: xs[400],'
                ' crit: H.springStep(1, 100, 20, 1), over: H.springStep(1, 100, 40, 1) }))')
        self.assertEqual(r['zero'], 0)
        self.assertEqual(r['neg'], 0)
        self.assertGreater(r['max'], 1)
        self.assertLess(r['max'], 1.01)
        self.assertAlmostEqual(r['end'], 1, places=4)
        self.assertGreater(r['crit'], 0.99)
        self.assertLess(r['over'], r['crit'])

    def test_spring_and_tween_are_pure_functions_of_time(self):
        r = run('const ch = [{t: 0.5, to: 10}, {t: 1.2, to: -4}, {t: 2, to: 3}];'
                'const a = [0.4, 0.9, 1.5, 2.3, 9].map(t => H.springAt(t, 1, ch)), b = [9, 2.3, 1.5, 0.9, 0.4].map(t => H.springAt(t, 1, ch)).reverse();'
                'const c = [0.4, 0.9, 1.5, 2.3, 9].map(t => H.tweenAt(t, 1, ch));'
                'console.log(JSON.stringify({ a, b, c, mid: H.easeOut(0.5), ends: [H.easeOut(0), H.easeOut(1)] }))')
        self.assertEqual(r['a'], r['b'], 'seeking backwards gives the same values')
        self.assertEqual(r['a'][0], 1)
        self.assertAlmostEqual(r['a'][-1], 3, places=4)
        self.assertEqual(r['c'][0], 1)
        self.assertAlmostEqual(r['c'][-1], 3, places=6)
        self.assertGreater(r['mid'], 0.9, 'cubic-bezier(.32, .72, 0, 1) is a strong ease-out')
        self.assertEqual(r['ends'], [0, 1])

    def test_a_tween_redirected_mid_move_starts_from_where_it_was(self):
        r = run('const ch = [{t: 0, to: 10}, {t: 0.35, to: 0}];'
                'console.log(JSON.stringify([H.tweenAt(0.35, 0, [{t: 0, to: 10}]), H.tweenAt(0.35, 0, ch), H.tweenAt(0.3501, 0, ch)]))')
        self.assertAlmostEqual(r[0], r[1], places=6)
        self.assertLess(abs(r[2] - r[1]), 0.05, 'no jump when the target changes')

    def test_stagger_and_falloff_clamp(self):
        r = run('console.log(JSON.stringify([H.stagger(5, 2), H.stagger(2, 5), H.falloff(0, 1), H.falloff(50, 1), H.falloff(50, 1, 0)]))')
        self.assertAlmostEqual(r[0], 0.135)
        self.assertEqual(r[0], r[1])
        self.assertEqual(r[2], 1)
        self.assertEqual(r[3], 0.09)
        self.assertEqual(r[4], 0)

    def test_a_rounded_solid_is_one_closed_silhouette_and_one_open_crease(self):
        r = run('const K = H.frame(0, 0, 1);'
                'const box = H.solid(K.P, {x: 0, y: 0, w: 40, d: 20, h: 10, r: 4}), jar = H.solid(K.P, {x: 0, y: 0, w: 20, d: 20, h: 30, r: 10});'
                'const hull = H.hull([[0,0],[2,0],[1,1],[1,0.2],[0,2],[2,2]]);'
                'const ring = H.rrect(0, 0, 10, 10, 99); const r = ring.map(([x, y]) => Math.hypot(x - 5, y - 5));'
                'const dim = H.frame(0, 0, 1, "dimetric").P(1, 0, 0);'
                'console.log(JSON.stringify({ box, jar, hull: hull.length, rmin: Math.min(...r), rmax: Math.max(...r), dim }))')
        for shape in (r['box'], r['jar']):
            self.assertTrue(shape['sil'].startswith('M') and shape['sil'].endswith('Z'))
            self.assertTrue(shape['crease'].startswith('M') and not shape['crease'].endswith('Z'))
        self.assertEqual(r['hull'], 4)
        self.assertAlmostEqual(r['rmin'], 5)
        self.assertAlmostEqual(r['rmax'], 5)
        self.assertAlmostEqual(r['dim'][1] / r['dim'][0], 0.5)

    def test_the_tour_names_the_last_stop_reached(self):
        r = run('const T = [{t: 0, at: null}, {t: 1, at: 3}, {t: 2, at: null}];'
                'console.log(JSON.stringify([0.5, 1, 1.9, 2.5].map(t => H.tourAt(t, T))))')
        self.assertEqual(r, [None, 3, 3, None])


if __name__ == '__main__':
    unittest.main(verbosity=2)
