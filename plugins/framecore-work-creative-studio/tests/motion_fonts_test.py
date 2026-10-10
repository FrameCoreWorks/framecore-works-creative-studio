"""Contract fonts and content scale in the Python renderer: the same files and weights the player loads."""
import importlib.util
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
ASSETS = PLUGIN / 'skills/hyperframes-workflow/assets'
RENDER = ASSETS / 'motion-render/render.py'
EMBED = ASSETS / 'motion-render/embed_fonts.py'
spec = importlib.util.spec_from_file_location('render', RENDER)
render = importlib.util.module_from_spec(spec)
spec.loader.exec_module(render)
STYLES = {style['id']: style for style in json.loads((ASSETS / 'motion-styles/styles.json').read_text(encoding='utf-8'))['styles']}
BASE = json.loads((ASSETS / 'motion-scenes/examples/two-statements.motion-score.json').read_text(encoding='utf-8'))


def styled(style_id):
    style = STYLES[style_id]
    return {**BASE, 'style': style_id, 'tokens': {**BASE['tokens'], **style['tokens']}, 'motion': {**style['motion']}, 'fonts': style['fonts']}


def stills(contract, folder, *extra):
    path = pathlib.Path(folder, 'c.motion.json')
    path.write_text(json.dumps(contract, ensure_ascii=False), encoding='utf-8')
    done = subprocess.run([sys.executable, '-B', str(RENDER), str(path), '--stills', '60', '--stills-dir', str(pathlib.Path(folder, 'stills')), *extra],
                          capture_output=True, text=True, timeout=300)
    return done.returncode, (json.loads(done.stdout) if done.stdout.strip() else None), done.stderr


class WeightMatching(unittest.TestCase):
    def test_css_font_weight_matching(self):
        have = [400, 600, 800]
        self.assertEqual([render.match_weight(have, w) for w in (100, 400, 450, 500, 550, 700, 900)], [400, 400, 400, 400, 600, 800, 800])
        self.assertEqual(render.match_weight([300, 700], 450), 300)  # 400-500: nothing up to 500, then lighter first
        self.assertEqual(render.match_weight([700, 900], 300), 700)


class ContractFonts(unittest.TestCase):
    def test_every_commercial_style_names_bundled_files_for_its_first_family(self):
        for style_id in ('sale-poster', 'editorial-serif', 'product-light', 'bold-grotesque'):
            style = STYLES[style_id]
            family = style['tokens']['fontFamily'].split(',')[0].strip()
            self.assertTrue(all(face['family'] == family for face in style['fonts']), style_id)
            for face in style['fonts']:
                self.assertTrue((PLUGIN / 'skills/pipeline-core/assets/fonts' / face['file']).is_file(), face['file'])

    def test_the_renderer_uses_the_declared_files(self):
        with tempfile.TemporaryDirectory() as temp:
            code, summary, err = stills(styled('sale-poster'), temp)
            self.assertEqual(code, 0, err)
            self.assertEqual(sorted(summary['fonts']), ['400', '700', '800'])
            self.assertTrue(summary['fonts']['800'].endswith('archivo/Archivo-CondensedExtraBold.ttf'))
            self.assertTrue(pathlib.Path(summary['stills'][0]).is_file())

    def test_embedded_data_renders_the_same_frame(self):
        with tempfile.TemporaryDirectory() as temp:
            source = pathlib.Path(temp, 'a.motion.json')
            source.write_text(json.dumps(styled('editorial-serif'), ensure_ascii=False), encoding='utf-8')
            embedded = pathlib.Path(temp, 'b.motion.json')
            done = subprocess.run([sys.executable, '-B', str(EMBED), str(source), str(embedded)], capture_output=True, text=True, timeout=120)
            self.assertEqual(done.returncode, 0, done.stderr)
            data = json.loads(embedded.read_text(encoding='utf-8'))
            self.assertTrue(all(face['data'].startswith('data:font/ttf;base64,') and face['file'] for face in data['fonts']))
            only_data = {**data, 'fonts': [{k: v for k, v in face.items() if k != 'file'} for face in data['fonts']]}
            one = pathlib.Path(temp, 'one'); two = pathlib.Path(temp, 'two')
            one.mkdir(); two.mkdir()
            code_a, summary_a, err_a = stills(styled('editorial-serif'), one)
            code_b, summary_b, err_b = stills(only_data, two)
            self.assertEqual((code_a, code_b), (0, 0), err_a + err_b)
            self.assertEqual(set(summary_b['fonts'].values()), {'embedded data'})
            self.assertEqual(pathlib.Path(summary_a['stills'][0]).read_bytes(), pathlib.Path(summary_b['stills'][0]).read_bytes())

    def test_a_missing_font_file_is_a_setup_error(self):
        with tempfile.TemporaryDirectory() as temp:
            contract = styled('product-light')
            contract['fonts'] = [{**contract['fonts'][0], 'file': 'inter/Missing.ttf'}]
            code, summary, err = stills(contract, temp)
            self.assertEqual(code, 2)
            self.assertIn('inter/Missing.ttf not found', err)


class ContentScale(unittest.TestCase):
    def test_content_scale_enlarges_every_authored_size(self):
        score = {'width': 1080, 'height': 1920, 'tokens': {}}
        self.assertEqual(render.px(score, 100), 100)
        self.assertEqual(render.px({**score, 'tokens': {'contentScale': 1.25}}, 100), 125)
        self.assertEqual(render.px({'width': 1920, 'height': 1080, 'tokens': {'contentScale': 0.8}}, 96), 77)


if __name__ == '__main__':
    unittest.main(verbosity=1)
