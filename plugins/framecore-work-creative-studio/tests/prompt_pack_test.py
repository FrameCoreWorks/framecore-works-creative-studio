"""Video prompt pack export (video-prompt-architect/scripts/prompt_pack.py): exact prompts, checks against the plan."""
import csv
import io
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

PLUGIN = pathlib.Path(__file__).resolve().parent.parent
TOOL = PLUGIN / 'skills/video-prompt-architect/scripts/prompt_pack.py'
PROMPT = 'Słoik miodu na drewnianym stole, światło od okna; kamera powoli najeżdża.\nBez napisów.'


def run(folder, pack, *extra):
    path = pathlib.Path(folder, 'pack.json')
    path.write_text(json.dumps(pack, ensure_ascii=False), encoding='utf-8')
    done = subprocess.run([sys.executable, '-B', str(TOOL), str(path), '--out-dir', str(pathlib.Path(folder, 'out')), *map(str, extra)], capture_output=True, text=True, timeout=60)
    return done.returncode, done.stdout, done.stderr


class Pack(unittest.TestCase):
    def test_prompts_are_kept_exactly_and_checked(self):
        with tempfile.TemporaryDirectory() as temp:
            pathlib.Path(temp, 'refs').mkdir()
            pathlib.Path(temp, 'refs', 'jar.png').write_bytes(b'png')
            plan = pathlib.Path(temp, 'plan.json')
            plan.write_text(json.dumps({'shots': [{'id': 'S01', 'start_s': 0, 'end_s': 4}, {'id': 'S02', 'start_s': 4, 'end_s': 9}, {'id': 'S03', 'start_s': 9, 'end_s': 12}]}), encoding='utf-8')
            pack = {'project': 'Miód', 'model': 'the user\'s generator', 'aspect': '9:16', 'shots': [
                {'id': 'S01', 'prompt': PROMPT, 'duration_s': 4, 'references': ['refs/jar.png'], 'seed': 7},
                {'id': 'S02', 'prompt': 'Łyżka w miodzie.', 'negative': 'tekst, logo', 'duration_s': 4, 'references': ['refs/missing.png']}]}
            code, out, err = run(temp, pack, '--plan', plan)
            self.assertEqual(code, 1, err)
            self.assertEqual(json.loads(out)['findings'], ['S02: reference not found: refs/missing.png', 'S02: 4 s of video for a 5 s shot', 'S03: planned shot without a prompt'])
            md = pathlib.Path(temp, 'out', 'pack-prompts.md').read_text(encoding='utf-8')
            self.assertIn('```text\n' + PROMPT + '\n```', md)
            self.assertIn('4 s · 9:16 · seed 7', md)
            rows = list(csv.reader(io.StringIO(pathlib.Path(temp, 'out', 'pack-prompts.csv').read_text(encoding='utf-8-sig'))))
            self.assertEqual(rows[1][3], PROMPT)
            jsonl = [json.loads(line) for line in pathlib.Path(temp, 'out', 'pack-prompts.jsonl').read_text(encoding='utf-8').splitlines()]
            self.assertEqual((jsonl[1]['negative'], jsonl[1]['aspect']), ('tekst, logo', '9:16'))

    def test_a_clean_pack_exits_zero_and_bad_packs_are_refused(self):
        with tempfile.TemporaryDirectory() as temp:
            self.assertEqual(run(temp, {'shots': [{'id': 'S01', 'prompt': 'x', 'duration_s': 3}]})[0], 0)
            self.assertEqual(run(temp, {'shots': [{'id': 'S01', 'prompt': 'x'}]})[0], 2, 'outputs exist')
        with tempfile.TemporaryDirectory() as temp:
            code, out, _ = run(temp, {'shots': [{'id': 'S01', 'prompt': ''}, {'id': 'S01', 'prompt': 'y', 'duration_s': 0}]})
            self.assertEqual(code, 1)
            self.assertEqual(json.loads(out)['findings'], ['S01: empty prompt', 'shot 2: ID missing or repeated (S01)', 'S01: duration_s must be a positive number of seconds'])
            self.assertEqual(run(temp, {'shots': []})[0], 2)


if __name__ == '__main__':
    unittest.main(verbosity=1)
