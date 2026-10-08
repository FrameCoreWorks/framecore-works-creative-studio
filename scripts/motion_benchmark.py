#!/usr/bin/env python3
"""Compare motion design results across hosts and models: automatic metrics, a blind review sheet and a summary.

Results are collected as  RESULTS/<run>/<brief-id>/  where <run> names the host, model and reasoning setting (for
example codex-astra6-high or claude-opus55) and the brief folder holds what that run delivered: the MP4, the
.motion.json contract and, optionally, transcript.md and meta.json ({"host", "model", "reasoning", "date"}).

  python3 scripts/motion_benchmark.py blind RESULTS BLIND        # critique every contract, hide the runs behind codes
  python3 scripts/motion_benchmark.py summarize RESULTS BLIND    # after scores.csv is filled in: results per run

`blind` writes BLIND/videos/<code>.mp4, BLIND/scores.csv (one row per video, criteria scored 1 to 5) and
BLIND/key.json, which maps codes to runs; the reviewer does not open the key until `summarize` has run. Automatic
metrics come from the Studio craft critique (critique.py) and from ffprobe (sound present, duration). Nothing is
uploaded or downloaded.
"""
import argparse
import csv
import json
import os
import random
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CRITIQUE = os.path.join(ROOT, 'plugins/framecore-work-creative-studio/skills/hyperframes-workflow/assets/motion-review/critique.py')
BRIEFS = os.path.join(ROOT, 'docs/motion-benchmark/briefs.json')
CRITERIA = ['concept', 'motion', 'typography', 'pacing', 'sound', 'overall']


def find(folder, suffixes):
    names = sorted(n for n in os.listdir(folder) if n.endswith(suffixes))
    return os.path.join(folder, names[0]) if names else None


def probe(path):
    try:
        out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_type:format=duration', '-of', 'json', path],
                             capture_output=True, text=True, check=True).stdout
        data = json.loads(out)
        return {'sound': any(s.get('codec_type') == 'audio' for s in data.get('streams', [])), 'seconds': round(float(data['format']['duration']), 2)}
    except (OSError, subprocess.CalledProcessError, KeyError, ValueError):
        return {'sound': None, 'seconds': None}


def critique(contract, out):
    run = subprocess.run([sys.executable, '-B', CRITIQUE, contract, '--out', out], capture_output=True, text=True)
    try:
        result = json.loads(run.stdout)
        return {'score': result['score'], 'errors': result['errors'], 'warnings': result['warnings'], 'frames': result.get('frames')}
    except (ValueError, KeyError):
        return {'score': None, 'errors': None, 'warnings': None, 'frames': f'failed: {run.stderr.strip()[:200]}'}


def blind(results, out, seed=None):
    if os.path.exists(out):
        raise ValueError(f'Output folder already exists: {out}')
    briefs = {b['id']: b for b in json.load(open(BRIEFS, encoding='utf-8'))['briefs']}
    entries = []
    for run in sorted(os.listdir(results)):
        run_dir = os.path.join(results, run)
        if not os.path.isdir(run_dir):
            continue
        for brief in sorted(os.listdir(run_dir)):
            folder = os.path.join(run_dir, brief)
            if os.path.isdir(folder):
                entries.append((run, brief, folder))
    if not entries:
        raise ValueError(f'No results found in {results} (expected RESULTS/<run>/<brief-id>/)')
    os.makedirs(os.path.join(out, 'videos'))
    os.makedirs(os.path.join(out, 'critique'))
    rng = random.Random(seed)
    codes = rng.sample(range(100, 1000), len(entries))
    key, rows = {}, []
    for (run, brief, folder), number in zip(entries, codes):
        code = f'V{number}'
        video, contract = find(folder, ('.mp4', '.webm', '.mov')), find(folder, ('.motion.json', '.json'))
        meta = {}
        if os.path.exists(os.path.join(folder, 'meta.json')):
            meta = json.load(open(os.path.join(folder, 'meta.json'), encoding='utf-8'))
        auto = {'delivered_video': bool(video), 'delivered_contract': bool(contract)}
        if video:
            shutil.copyfile(video, os.path.join(out, 'videos', code + os.path.splitext(video)[1]))
            auto.update(probe(video))
        if contract and os.path.basename(contract) != 'meta.json':
            auto['critique'] = critique(contract, os.path.join(out, 'critique', code))
        key[code] = {'run': run, 'brief': brief, 'known_brief': brief in briefs, 'meta': meta, 'auto': auto}
        rows.append({'code': code, 'brief': brief, **{c: '' for c in CRITERIA}, 'notes': ''})
    rows.sort(key=lambda row: (row['brief'], row['code']))
    with open(os.path.join(out, 'scores.csv'), 'w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=['code', 'brief', *CRITERIA, 'notes'])
        writer.writeheader()
        writer.writerows(rows)
    with open(os.path.join(out, 'key.json'), 'w', encoding='utf-8') as handle:
        handle.write(json.dumps(key, indent=2, ensure_ascii=False) + '\n')
    return {'videos': len(rows), 'scores': os.path.join(out, 'scores.csv')}


def mean(values):
    values = [v for v in values if isinstance(v, (int, float))]
    return round(sum(values) / len(values), 2) if values else None


def summarize(out):
    key = json.load(open(os.path.join(out, 'key.json'), encoding='utf-8'))
    with open(os.path.join(out, 'scores.csv'), encoding='utf-8') as handle:
        scores = {row['code']: row for row in csv.DictReader(handle)}
    runs = {}
    for code, entry in key.items():
        row = scores.get(code, {})
        run = runs.setdefault(entry['run'], {'videos': 0, 'delivered': 0, 'with_sound': 0, 'critique': [], 'errors': [], **{c: [] for c in CRITERIA}})
        run['videos'] += 1
        auto = entry['auto']
        run['delivered'] += bool(auto.get('delivered_video'))
        run['with_sound'] += bool(auto.get('sound'))
        crit = auto.get('critique') or {}
        run['critique'].append(crit.get('score'))
        run['errors'].append(crit.get('errors'))
        for c in CRITERIA:
            try:
                run[c].append(float(row.get(c, '')))
            except ValueError:
                pass
    table = {name: {'videos': r['videos'], 'delivered': r['delivered'], 'with_sound': r['with_sound'], 'critique_score': mean(r['critique']),
                    'critique_errors': mean(r['errors']), **{c: mean(r[c]) for c in CRITERIA}} for name, r in sorted(runs.items())}
    lines = ['| Run | Videos | Delivered | With sound | Critique | Errors | ' + ' | '.join(c.capitalize() for c in CRITERIA) + ' |',
             '| --- | ---: | ---: | ---: | ---: | ---: | ' + ' | '.join('---:' for _ in CRITERIA) + ' |']
    for name, t in table.items():
        cells = [t['videos'], t['delivered'], t['with_sound'], t['critique_score'], t['critique_errors'], *[t[c] for c in CRITERIA]]
        lines.append(f'| {name} | ' + ' | '.join('–' if v is None else str(v) for v in cells) + ' |')
    report = '\n'.join(lines) + '\n'
    with open(os.path.join(out, 'summary.md'), 'w', encoding='utf-8') as handle:
        handle.write(report)
    with open(os.path.join(out, 'summary.json'), 'w', encoding='utf-8') as handle:
        handle.write(json.dumps(table, indent=2, ensure_ascii=False) + '\n')
    return table, report


def main(argv=None):
    parser = argparse.ArgumentParser(description='Blind comparison of motion design runs.')
    sub = parser.add_subparsers(dest='command', required=True)
    b = sub.add_parser('blind')
    b.add_argument('results')
    b.add_argument('out')
    b.add_argument('--seed', type=int, help='fix the code assignment (for tests only)')
    s = sub.add_parser('summarize')
    s.add_argument('results')
    s.add_argument('out')
    args = parser.parse_args(argv)
    try:
        if args.command == 'blind':
            print(json.dumps(blind(args.results, args.out, args.seed)))
        else:
            _, report = summarize(args.out)
            print(report)
        return 0
    except (OSError, ValueError, KeyError) as error:
        sys.stderr.write(f'{error}\n')
        return 2


if __name__ == '__main__':
    sys.exit(main())
