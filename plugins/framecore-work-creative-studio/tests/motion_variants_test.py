"""Ad templates, brand kits and copy or language variants of a motion contract (motion-variants/variants.py)."""
import importlib.util
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
ASSETS = PLUGIN / 'skills/hyperframes-workflow/assets'
VARIANTS = ASSETS / 'motion-variants/variants.py'
RENDER = ASSETS / 'motion-render/render.py'
TEMPLATES = ASSETS / 'motion-scenes/templates'
KIT = PLUGIN / 'skills/pipeline-core/assets/brand-kit.template.json'
spec = importlib.util.spec_from_file_location('variants', VARIANTS)
variants = importlib.util.module_from_spec(spec)
spec.loader.exec_module(variants)


def run(*args):
    done = subprocess.run([sys.executable, '-B', str(VARIANTS), *map(str, args)], capture_output=True, text=True, timeout=120)
    return done.returncode, done.stdout, done.stderr


class Templates(unittest.TestCase):
    def test_three_vertical_ad_templates_with_feed_formats(self):
        code, out, err = run('templates')
        self.assertEqual(code, 0, err)
        listed = {item['file']: item for item in json.loads(out)}
        self.assertEqual(sorted(listed), ['ad-offer.motion-score.json', 'ad-product.motion-score.json', 'ad-testimonial.motion-score.json'])
        for path in TEMPLATES.glob('*.motion-score.json'):
            score = json.loads(path.read_text(encoding='utf-8'))
            self.assertEqual((score['width'], score['height']), (1080, 1920), path.name)
            self.assertEqual(sorted(f['id'] for f in score['formats']), ['1x1', '4x5'], path.name)
            self.assertEqual(score['copyStatus'], 'template-placeholder')
            self.assertEqual(score['approval']['status'], 'proposed')
            self.assertEqual(score['template']['replace'], sorted(score['copy']), path.name)
            self.assertTrue(score['fonts'] and all((PLUGIN / 'skills/pipeline-core/assets/fonts' / f['file']).is_file() for f in score['fonts']))


class Brand(unittest.TestCase):
    def test_kit_colours_and_bundled_headline_font_reach_the_contract(self):
        score = json.loads((TEMPLATES / 'ad-offer.motion-score.json').read_text(encoding='utf-8'))
        kit = json.loads(KIT.read_text(encoding='utf-8'))
        out, report = variants.apply_brand(score, kit)
        self.assertEqual(out['tokens']['background'], '#F7F3EC')
        self.assertEqual(out['tokens']['foreground'], '#1D1D1B')
        self.assertEqual(out['tokens']['accent'], '#F2C14E')
        self.assertEqual(out['tokens']['fontFamily'], 'Fraunces, Arial, sans-serif')
        self.assertEqual([(f['weight'], f['file']) for f in out['fonts']], [(400, 'fraunces/Fraunces-Regular.ttf'), (600, 'fraunces/Fraunces-SemiBold.ttf'), (900, 'fraunces/Fraunces-Black.ttf')])
        # The template's yellow-on-white accent problem is reported, not hidden.
        self.assertLess(report['contrast']['accent'], 3)
        self.assertTrue(any('accent' in note and 'contrast' in note for note in report['notes']))
        self.assertGreater(report['contrast']['foreground'], 4.5)
        self.assertEqual(score['tokens']['background'], '#101010', 'the input contract is not changed')

    def test_a_changed_look_needs_new_approval(self):
        score = json.loads((TEMPLATES / 'ad-offer.motion-score.json').read_text(encoding='utf-8'))
        score['approval'] = {'status': 'approved', 'revision': 3, 'evidence': 'client email'}
        out, _ = variants.apply_brand(score, json.loads(KIT.read_text(encoding='utf-8')))
        self.assertEqual(out['approval']['status'], 'proposed')
        contracts, _, _ = variants.expand(score, {'variants': [{'id': 'same'}, {'id': 'red', 'tokens': {'accent': '#E63946'}}]}, 'ad')
        approval = {name: contract['approval']['status'] for name, contract in contracts}
        self.assertEqual(approval, {'ad-same.motion.json': 'approved', 'ad-red.motion.json': 'proposed'})

    def test_a_named_condensed_face_replaces_the_plain_weight(self):
        family, faces, chosen = variants.bundled_faces('Archivo Condensed ExtraBold')
        self.assertEqual((family, chosen), ('Archivo', 'Condensed ExtraBold'))
        self.assertEqual([f['weight'] for f in faces], [400, 700, 800])
        self.assertEqual(variants.bundled_faces('Archivo')[1][-1]['weight'], 700)
        self.assertEqual(variants.bundled_faces('Helvetica Neue'), (None, [], None))

    def test_a_font_that_is_not_bundled_is_left_to_the_user(self):
        score = json.loads((TEMPLATES / 'ad-product.motion-score.json').read_text(encoding='utf-8'))
        out, report = variants.apply_brand(score, {'name': 'Lipa', 'fonts': {'headline': {'font': 'Brand Sans Bold'}}})
        self.assertEqual(out['fonts'], score['fonts'])
        self.assertEqual(out['tokens']['fontFamily'], score['tokens']['fontFamily'])
        self.assertTrue(any('Brand Sans Bold is not bundled' in note for note in report['notes']))

    def test_the_cli_never_overwrites(self):
        with tempfile.TemporaryDirectory() as temp:
            target = pathlib.Path(temp, 'b.motion.json')
            self.assertEqual(run('brand', TEMPLATES / 'ad-offer.motion-score.json', '--brand', KIT, '--out', target)[0], 0)
            code, _, err = run('brand', TEMPLATES / 'ad-offer.motion-score.json', '--brand', KIT, '--out', target)
            self.assertEqual(code, 2)
            self.assertIn('already exists', err)


class Expand(unittest.TestCase):
    MATRIX = {
        'formats': ['base', '1x1'],
        'variants': [
            {'id': 'pl', 'language': 'pl'},
            {'id': 'en', 'language': 'en', 'copy': {'hook-1': 'Sale', 'hook-2': 'until Sunday only', 'discount-label': 'off everything',
                                                     'reason-1': 'Free delivery', 'reason-2': '30-day returns', 'reason-3': 'Ships in 24 h', 'cta': 'Shop now'}},
        ],
    }

    def expand(self, temp, matrix):
        path = pathlib.Path(temp, 'matrix.json')
        path.write_text(json.dumps(matrix), encoding='utf-8')
        return run('expand', TEMPLATES / 'ad-offer.motion-score.json', '--matrix', path, '--out-dir', pathlib.Path(temp, 'out'))

    def test_one_contract_per_variant_and_a_render_per_format(self):
        with tempfile.TemporaryDirectory() as temp:
            code, out, err = self.expand(temp, self.MATRIX)
            self.assertEqual(code, 0, err)
            folder = pathlib.Path(temp, 'out')
            self.assertEqual(json.loads(out)['contracts'], ['ad-offer-pl.motion.json', 'ad-offer-en.motion.json'])
            plan = json.loads((folder / 'render-plan.json').read_text(encoding='utf-8'))
            self.assertEqual([(r['variant'], r['format']) for r in plan['renders']], [('pl', 'base'), ('pl', '1x1'), ('en', 'base'), ('en', '1x1')])
            self.assertEqual(plan['renders'][3]['command'], ['python3', 'render.py', 'ad-offer-en.motion.json', 'ad-offer-en-1x1.mp4', '--format', '1x1'])
            self.assertEqual([c['contract'] for c in plan['checks']], ['ad-offer-pl.motion.json', 'ad-offer-en.motion.json'])
            en = json.loads((folder / 'ad-offer-en.motion.json').read_text(encoding='utf-8'))
            pl = json.loads((folder / 'ad-offer-pl.motion.json').read_text(encoding='utf-8'))
            self.assertEqual((en['id'], en['language'], en['copyStatus'], en['copy']['cta']), ('ad-offer-template-en', 'en', 'variant-draft', 'Shop now'))
            self.assertEqual(pl['copy'], json.loads((TEMPLATES / 'ad-offer.motion-score.json').read_text(encoding='utf-8'))['copy'])
            self.assertEqual(en['approval']['status'], 'proposed')
            # The English variant renders in the square format with the bundled fonts and no overflow.
            done = subprocess.run([sys.executable, '-B', str(RENDER), str(folder / 'ad-offer-en.motion.json'), '--format', '1x1', '--stills', '60,449',
                                   '--stills-dir', str(folder / 'stills')], capture_output=True, text=True, timeout=300)
            self.assertEqual(done.returncode, 0, done.stderr)
            summary = json.loads(done.stdout)
            self.assertEqual((summary['width'], summary['height']), (1080, 1080))
            self.assertTrue(summary['fonts']['800'].endswith('Archivo-CondensedExtraBold.ttf'))

    def test_a_variant_cannot_add_text_or_formats(self):
        with tempfile.TemporaryDirectory() as temp:
            code, _, err = self.expand(temp, {'variants': [{'id': 'x', 'copy': {'new-line': 'Extra'}}]})
            self.assertEqual(code, 2)
            self.assertIn("copy IDs not in the contract: ['new-line']", err)
            self.assertFalse(pathlib.Path(temp, 'out').exists())
        with tempfile.TemporaryDirectory() as temp:
            code, _, err = self.expand(temp, {'formats': ['16x9'], 'variants': [{'id': 'a'}]})
            self.assertEqual(code, 2)
            self.assertIn('formats not in the contract', err)
        with tempfile.TemporaryDirectory() as temp:
            code, _, err = self.expand(temp, {'variants': [{'id': 'a'}, {'id': 'a'}]})
            self.assertEqual(code, 2)
            self.assertIn('repeated', err)

    def test_an_existing_output_folder_is_kept(self):
        with tempfile.TemporaryDirectory() as temp:
            pathlib.Path(temp, 'out').mkdir()
            code, _, err = self.expand(temp, self.MATRIX)
            self.assertEqual(code, 2)
            self.assertIn('already exists', err)



class RuntimeMap(unittest.TestCase):
    def test_every_row_matches_the_capability_card(self):
        card = {c['id']: c for c in json.loads((PLUGIN / 'skills/workflow-orchestrator/assets/capability-card.json').read_text(encoding='utf-8'))['capabilities']}
        text = (PLUGIN / 'skills/hyperframes-workflow/references/runtime-map.md').read_text(encoding='utf-8')
        rows = [line.split('|')[1:-1] for line in text.splitlines() if line.startswith('| ') and '`' in line]
        listed = set()
        for cells in rows:
            cap = cells[1].strip().strip('`')
            listed.add(cap)
            self.assertIn(cap, card)
            hosts = [h for h, cell in zip(('none', 'code_execution', 'shell'), cells[2:5]) if cell.strip() == 'yes']
            self.assertEqual(hosts, [h for h in ('none', 'code_execution', 'shell') if h in card[cap]['hosts']], cap)
        motion = {i for i, c in card.items() if c['owner'] in ('hyperframes-workflow', 'remotion-video-production', 'caption-studio')}
        self.assertEqual(listed, motion)


if __name__ == '__main__':
    unittest.main(verbosity=1)
