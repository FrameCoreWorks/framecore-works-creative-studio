"""Edit decision list export (opencut-video-studio/scripts/edit_export.py): EDL, OTIO and CSV from one edit."""
import csv
import io
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
TOOL = PLUGIN / 'skills/opencut-video-studio/scripts/edit_export.py'
EDIT = {'title': 'Spot 15s', 'fps': 30, 'start': '01:00:00:00',
        'clips': [{'source': 'A001.mp4', 'in': 1.0, 'out': 3.5, 'name': 'hook', 'note': 'product in hand'},
                  {'source': 'B002 take 3.mov', 'in': '00:00:10:12', 'out': '00:00:13:00'},
                  {'source': 'A001.mp4', 'in': 8, 'out': 12, 'record_in': 6, 'name': 'proof'}]}


def export(edit, folder, *extra):
    path = pathlib.Path(folder, 'spot.json')
    path.write_text(json.dumps(edit), encoding='utf-8')
    done = subprocess.run([sys.executable, '-B', str(TOOL), str(path), '--out-dir', str(pathlib.Path(folder, 'out')), *extra], capture_output=True, text=True, timeout=60)
    return done.returncode, done.stdout, done.stderr


class Export(unittest.TestCase):
    def test_edl_otio_and_csv_describe_the_same_cuts(self):
        with tempfile.TemporaryDirectory() as temp:
            code, out, err = export(EDIT, temp)
            self.assertEqual(code, 0, err)
            self.assertEqual(json.loads(out)['length_seconds'], 10.0)
            folder = pathlib.Path(temp, 'out')
            edl = (folder / 'spot.edl').read_text(encoding='utf-8').splitlines()
            self.assertEqual(edl[:2], ['TITLE: Spot 15s', 'FCM: NON-DROP FRAME'])
            self.assertIn('001  A001     V     C        00:00:01:00 00:00:03:15 01:00:00:00 01:00:02:15', edl)
            self.assertIn('002  B002TAKE V     C        00:00:10:12 00:00:13:00 01:00:02:15 01:00:05:03', edl)
            self.assertIn('003  A001     V     C        00:00:08:00 00:00:12:00 01:00:06:00 01:00:10:00', edl)
            self.assertIn('* FROM CLIP NAME: B002 take 3.mov', edl)
            timeline = json.loads((folder / 'spot.otio').read_text(encoding='utf-8'))
            items = timeline['tracks']['children'][0]['children']
            self.assertEqual([i['OTIO_SCHEMA'] for i in items], ['Clip.2', 'Clip.2', 'Gap.1', 'Clip.2'])
            self.assertEqual(items[2]['source_range']['duration']['value'], 27.0, 'the gap before the proof shot')
            self.assertEqual(items[3]['media_references']['DEFAULT_MEDIA']['target_url'], 'A001.mp4')
            self.assertEqual(timeline['global_start_time']['value'], 108000.0)
            rows = list(csv.DictReader(io.StringIO((folder / 'spot-shots.csv').read_text(encoding='utf-8'))))
            self.assertEqual([r['record in'] for r in rows], ['01:00:00:00', '01:00:02:15', '01:00:06:00'])
            self.assertEqual(rows[0]['note'], 'product in hand')

    def test_fractional_rates_use_their_nominal_timebase(self):
        with tempfile.TemporaryDirectory() as temp:
            code, out, err = export({**EDIT, 'fps': 29.97, 'start': '00:00:00:00'}, temp)
            self.assertEqual(code, 0, err)
            self.assertEqual(json.loads(out)['timebase'], 30)

    def test_bad_edits_are_refused(self):
        cases = [({**EDIT, 'fps': 33.3}, 'unsupported frame rate'), ({**EDIT, 'clips': [{'source': 'a.mp4', 'in': 3, 'out': 2}]}, 'out must come after in'),
                 ({**EDIT, 'clips': [EDIT['clips'][0], {**EDIT['clips'][1], 'record_in': 1}]}, 'overlaps'),
                 ({**EDIT, 'clips': [{'source': 'a.mp4', 'in': '00:00:01:31', 'out': 4}]}, 'not below the timebase')]
        for edit, message in cases:
            with tempfile.TemporaryDirectory() as temp:
                code, _, err = export(edit, temp)
                self.assertEqual(code, 2, message)
                self.assertIn(message, err)

    def test_existing_files_are_kept(self):
        with tempfile.TemporaryDirectory() as temp:
            self.assertEqual(export(EDIT, temp)[0], 0)
            code, _, err = export(EDIT, temp)
            self.assertEqual(code, 2)
            self.assertIn('output exists', err)


if __name__ == '__main__':
    unittest.main(verbosity=1)
