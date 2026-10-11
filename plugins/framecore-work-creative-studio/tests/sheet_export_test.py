"""Shot list and AV script export (storyboard-sequence-architect/scripts/sheet_export.py): XLSX, CSV and PDF."""
import csv
import importlib.util
import io
import json
import pathlib
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile

PILLOW = importlib.util.find_spec('PIL') is not None

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
TOOL = PLUGIN / 'skills/storyboard-sequence-architect/scripts/sheet_export.py'
PLAN = PLUGIN / 'skills/storyboard-sequence-architect/assets/shot-plan.example.json'
AV = {'title': 'Miód z Beskidów, AV script v2', 'rows': [
    {'time': '0:00–0:02', 'video': 'Słoik w dłoni pszczelarza.', 'super': 'Miód z Beskidów', 'audio': 'Lektor: Prosto z pasieki.', 'music': 'Gitara'},
    {'time': '0:02–0:08', 'video': 'Zbliżenie na plaster.\nDrugi plan: pasieka o świcie.', 'super': '−20% do niedzieli', 'audio': 'Lektor: Zbieramy ręcznie.', 'music': 'Narasta'}]}


def export(path, folder, *extra):
    done = subprocess.run([sys.executable, '-B', str(TOOL), str(path), '--out-dir', str(folder), *extra], capture_output=True, text=True, timeout=120)
    return done.returncode, done.stdout, done.stderr


class Export(unittest.TestCase):
    def test_an_av_script_keeps_its_exact_polish_text_in_every_format(self):
        with tempfile.TemporaryDirectory() as temp:
            source = pathlib.Path(temp, 'av.json')
            source.write_text(json.dumps(AV, ensure_ascii=False), encoding='utf-8')
            code, out, err = export(source, pathlib.Path(temp, 'out'), '--formats', 'xlsx,csv,pdf' if PILLOW else 'xlsx,csv')
            self.assertEqual(code, 0, err)
            if PILLOW:
                self.assertEqual(json.loads(out)['pdf_pages'], 1)
            folder = pathlib.Path(temp, 'out')
            with zipfile.ZipFile(folder / 'av.xlsx') as archive:
                self.assertEqual(sorted(archive.namelist()), sorted(['[Content_Types].xml', '_rels/.rels', 'xl/workbook.xml', 'xl/_rels/workbook.xml.rels', 'xl/worksheets/sheet1.xml', 'xl/styles.xml']))
                sheet = archive.read('xl/worksheets/sheet1.xml').decode('utf-8')
            self.assertIn('−20% do niedzieli', sheet)
            self.assertIn('Zbliżenie na plaster.\nDrugi plan: pasieka o świcie.', sheet)
            self.assertIn('state="frozen"', sheet)
            rows = list(csv.reader(io.StringIO((folder / 'av.csv').read_text(encoding='utf-8-sig'))))
            self.assertEqual(rows[0][:3], ['Time', 'Video', 'Super (on screen)'])
            self.assertEqual(rows[2][2], '−20% do niedzieli')
            if PILLOW:
                pdf = (folder / 'av.pdf').read_bytes()
                self.assertTrue(pdf.startswith(b'%PDF'))
                self.assertEqual(len(re.findall(rb'/Type\s*/Page\b', pdf)), 1)
            if importlib.util.find_spec('openpyxl'):
                import openpyxl
                ws = openpyxl.load_workbook(folder / 'av.xlsx').active
                self.assertEqual((ws.title, ws['C3'].value, ws.freeze_panes), ('AV script', '−20% do niedzieli', 'A2'))

    def test_a_shot_plan_becomes_a_shot_list(self):
        with tempfile.TemporaryDirectory() as temp:
            code, out, err = export(PLAN, pathlib.Path(temp, 'out'), '--formats', 'csv')
            self.assertEqual(code, 0, err)
            rows = list(csv.reader(io.StringIO(pathlib.Path(temp, 'out', 'shot-plan.csv').read_text(encoding='utf-8-sig'))))
            self.assertEqual(rows[0], ['Shot', 'In', 'Out', 'Seconds', 'Action', 'Camera', 'Audio', 'Notes', 'References'])
            self.assertEqual(rows[1][:4], ['S01', '0:00', '0:04', '4'])
            self.assertEqual(len(rows), 1 + len(json.loads(PLAN.read_text(encoding='utf-8'))['shots']))

    @unittest.skipUnless(PILLOW, 'Pillow is not installed')
    def test_long_tables_continue_on_new_pages_with_the_header(self):
        rows = [{'time': f'0:{i:02d}', 'video': 'Ujęcie ' + 'bardzo długie ' * 12, 'super': '', 'audio': 'Lektor: ' + 'słowo ' * 20, 'music': ''} for i in range(40)]
        with tempfile.TemporaryDirectory() as temp:
            source = pathlib.Path(temp, 'long.json')
            source.write_text(json.dumps({'title': 'Długi scenariusz', 'rows': rows}, ensure_ascii=False), encoding='utf-8')
            code, out, err = export(source, pathlib.Path(temp, 'out'), '--formats', 'pdf')
            self.assertEqual(code, 0, err)
            self.assertGreater(json.loads(out)['pdf_pages'], 2)

    def test_bad_input_and_existing_files(self):
        with tempfile.TemporaryDirectory() as temp:
            source = pathlib.Path(temp, 'bad.json')
            source.write_text(json.dumps({'columns': ['A', 'B'], 'rows': [['only one']]}), encoding='utf-8')
            self.assertEqual(export(source, pathlib.Path(temp, 'out'))[0], 2)
            self.assertEqual(export(PLAN, pathlib.Path(temp, 'plan'), '--formats', 'csv')[0], 0)
            code, _, err = export(PLAN, pathlib.Path(temp, 'plan'), '--formats', 'csv')
            self.assertEqual(code, 2)
            self.assertIn('output exists', err)


if __name__ == '__main__':
    unittest.main(verbosity=1)
