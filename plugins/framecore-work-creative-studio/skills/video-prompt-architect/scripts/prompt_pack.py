#!/usr/bin/env python3
"""Export a video prompt pack for pasting into a generator, one shot at a time, and check it before any credits are spent.

  python3 prompt_pack.py pack.json --out-dir prompts/              # pack-prompts.md, .csv and .jsonl
  python3 prompt_pack.py pack.json --plan shot-plan.json --out-dir prompts/

pack.json (reference paths are relative to it):
  {"project": "Miód z Beskidów", "model": "the generator the user named", "aspect": "9:16",
   "shots": [{"id": "S01", "prompt": "...", "negative": "...", "duration_s": 4, "references": ["refs/jar.png"],
              "seed": 12, "notes": "..."}]}

Findings: a repeated or missing shot ID, an empty prompt, a duration that is not positive, a reference file that does not
exist, and with --plan a prompt shorter than its shot's edit interval or a planned shot without a prompt. The Markdown
holds each prompt in its own block exactly as written; the CSV and JSONL suit bulk tools. Nothing is sent to a
generator. Exit codes: 0 written without findings, 1 written with findings, 2 bad input or an output that exists.
"""
import argparse
import csv
import io
import json
import sys
from pathlib import Path


class InputError(Exception):
    pass


def main(argv=None):
    parser = argparse.ArgumentParser(description='Export and check a video prompt pack.')
    parser.add_argument('pack')
    parser.add_argument('--plan', help='shot plan JSON with shots {id, start_s, end_s}')
    parser.add_argument('--out-dir', required=True)
    args = parser.parse_args(argv)
    try:
        source = Path(args.pack)
        pack = json.loads(source.read_text(encoding='utf-8'))
        shots = pack.get('shots')
        if not isinstance(shots, list) or not shots:
            raise InputError('the pack needs a list of shots')
        plan = {s.get('id'): s for s in (json.loads(Path(args.plan).read_text(encoding='utf-8')).get('shots') or [])} if args.plan else {}
        findings, seen = [], set()
        for i, shot in enumerate(shots, 1):
            sid = str(shot.get('id') or '').strip()
            if not sid or sid in seen:
                findings.append(f'shot {i}: ID missing or repeated ({sid or "none"})')
            seen.add(sid)
            if not str(shot.get('prompt') or '').strip():
                findings.append(f'{sid or i}: empty prompt')
            duration = shot.get('duration_s')
            if duration is not None and not (isinstance(duration, (int, float)) and not isinstance(duration, bool) and duration > 0):
                findings.append(f'{sid or i}: duration_s must be a positive number of seconds')
            for ref in shot.get('references') or []:
                if '://' not in str(ref) and not (source.parent / str(ref)).is_file():
                    findings.append(f'{sid or i}: reference not found: {ref}')
            planned = plan.get(sid)
            if planned and isinstance(planned.get('start_s'), (int, float)) and isinstance(planned.get('end_s'), (int, float)) and isinstance(duration, (int, float)):
                need = round(planned['end_s'] - planned['start_s'], 3)
                if duration + 1e-9 < need:
                    findings.append(f'{sid}: {duration} s of video for a {need} s shot')
        for sid in plan:
            if sid and sid not in seen:
                findings.append(f'{sid}: planned shot without a prompt')
        stem = source.name.split('.')[0]
        folder = Path(args.out_dir)
        files = {folder / f'{stem}-prompts.md': None, folder / f'{stem}-prompts.csv': None, folder / f'{stem}-prompts.jsonl': None}
        existing = [str(p) for p in files if p.exists()]
        if existing:
            raise InputError(f'output exists: {", ".join(existing)}')
        aspect = pack.get('aspect', '')
        md = [f"# {pack.get('project', stem)}: prompts", '', f"Generator: {pack.get('model', 'not named')}. Aspect: {aspect or 'per shot'}. Shots: {len(shots)}.", '']
        for shot in shots:
            meta = [f"{shot['duration_s']} s" if shot.get('duration_s') else '', shot.get('aspect', aspect), f"seed {shot['seed']}" if shot.get('seed') is not None else '']
            md += [f"## {shot.get('id', '')}", '', ' · '.join(m for m in meta if m), '']
            md += ['```text', str(shot.get('prompt', '')).rstrip(), '```', '']
            if shot.get('negative'):
                md += ['Negative:', '', '```text', str(shot['negative']).rstrip(), '```', '']
            if shot.get('references'):
                md += ['References: ' + ', '.join(str(r) for r in shot['references']), '']
            if shot.get('notes'):
                md += [f"Notes: {shot['notes']}", '']
        if findings:
            md += ['## Findings', ''] + [f'- {f}' for f in findings] + ['']
        table = io.StringIO()
        writer = csv.writer(table)
        writer.writerow(['id', 'duration_s', 'aspect', 'prompt', 'negative', 'references', 'seed'])
        for shot in shots:
            writer.writerow([shot.get('id', ''), shot.get('duration_s', ''), shot.get('aspect', aspect), shot.get('prompt', ''), shot.get('negative', ''),
                             ' | '.join(str(r) for r in shot.get('references') or []), shot.get('seed', '')])
        lines = ''.join(json.dumps({**shot, 'aspect': shot.get('aspect', aspect)}, ensure_ascii=False) + '\n' for shot in shots)
        folder.mkdir(parents=True, exist_ok=True)
        texts = ['\n'.join(md), '﻿' + table.getvalue(), lines]
        for path, text in zip(files, texts):
            path.write_text(text, encoding='utf-8', newline='')
    except (OSError, ValueError, InputError) as error:
        sys.stderr.write(f'{error}\n')
        return 2
    print(json.dumps({'files': [str(p) for p in files], 'shots': len(shots), 'findings': findings}, ensure_ascii=False))
    return 1 if findings else 0


if __name__ == '__main__':
    sys.exit(main())
