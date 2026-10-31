#!/usr/bin/env python3
"""Studio delivery gate: measured checks a final file must pass before Studio hands it over.

  python3 studio_gate.py check export/reel.mp4                 # run every check, write the report
  python3 studio_gate.py check export/post.png --spec gate.json
  python3 studio_gate.py status export/                         # which files lack a PASS report (exit 1 when any)
  python3 studio_gate.py waive export/teaser.mp4 --reason "user accepts the 6 s still on the end card"

A final file goes to the user only from a folder named `export/`, and only with a PASS (or user WAIVED) report
in `export/.studio-gate/<file name>.json` whose SHA-256 matches the file. Any change to the file voids the report.

The checks reuse Studio's own measuring tools and add the missing ones:
  video  format and timing against the spec, long black stretches, undeclared still time (motion_activity),
         photosensitive flashes (flash_check), audio presence, integrated loudness and true peak
  audio  duration, loudness and true peak, near-silence
  image  size and ratio against the spec (image_probe), a blank or single-colour image
  text   machine-made writing clusters (ai_writing_check), Polish typography (pl_copy_check), length limits
A check that cannot run (a missing ffmpeg, numpy or Pillow) makes the verdict BLOCKED, never PASS, unless the spec
skips it with a reason. The gate measures files; whether the idea works stays with the review and the user.

Exit codes: 0 PASS or WAIVED, 1 FAIL, 2 BLOCKED or an input problem. Needs Python 3.8+ and ffmpeg with ffprobe; no
network, accounts or keys.
"""
import argparse
import datetime
import fnmatch
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

SCHEMA = 'studio-gate/1'
SPEC_SCHEMA = 'studio-gate-spec/1'
REPORT_DIR = '.studio-gate'
SKILLS = Path(__file__).resolve().parents[2]
TOOLS = {
    'motion_activity': SKILLS / 'hyperframes-workflow/assets/motion-quality/motion_activity.py',
    'flash_check': SKILLS / 'hyperframes-workflow/assets/motion-quality/flash_check.py',
    'image_probe': SKILLS / 'output-critic-iteration/scripts/image_probe.py',
    'ai_writing_check': SKILLS / 'copy-voice/scripts/ai_writing_check.py',
    'pl_copy_check': SKILLS / 'copy-voice/scripts/pl_copy_check.py',
}
KINDS = {
    'video': {'.mp4', '.mov', '.webm', '.mkv', '.m4v'},
    'audio': {'.wav', '.mp3', '.m4a', '.aac', '.flac', '.ogg', '.opus'},
    'image': {'.png', '.jpg', '.jpeg', '.webp'},
    'text': {'.txt', '.md', '.srt', '.vtt'},
}
DELIVERABLE = set().union(*KINDS.values()) | {'.gif', '.pdf', '.svg', '.zip', '.html', '.json', '.csv', '.docx', '.pptx'}
SILENT_LUFS = -40.0          # integrated loudness below this is treated as no usable sound
BLACK_RUN_SECONDS = 1.0      # a black stretch at least this long inside the film fails
EDGE_SECONDS = 0.3           # black that touches the first or last moment is a fade, not a fault
DEFAULTS = {'audio': 'any', 'true_peak_max': -1.0, 'lufs_tolerance': 2.0}


def kind_of(path):
    suffix = path.suffix.lower()
    return next((k for k, exts in KINDS.items() if suffix in exts), 'other')


def sha256(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as handle:
        for block in iter(lambda: handle.read(1 << 20), b''):
            digest.update(block)
    return digest.hexdigest()


def report_path(path):
    return path.parent / REPORT_DIR / (path.name + '.json')


# ---- spec -------------------------------------------------------------------------------------------------------

def find_spec(path, explicit=None):
    if explicit:
        return Path(explicit)
    for folder in [path.parent, *list(path.parents)[1:3]]:
        candidate = folder / 'gate.json'
        if candidate.is_file():
            return candidate
    return None


def load_spec(path, spec_path):
    """Merged requirements for this file: defaults, then the spec's defaults, then every matching `files` pattern."""
    merged = dict(DEFAULTS)
    if spec_path is None:
        return merged, None
    data = json.loads(Path(spec_path).read_text(encoding='utf-8'))
    if data.get('schema') != SPEC_SCHEMA:
        raise ValueError(f'{spec_path}: schema must be {SPEC_SCHEMA}')
    merged.update(data.get('defaults') or {})
    for pattern, rules in (data.get('files') or {}).items():
        if fnmatch.fnmatch(path.name, pattern):
            merged.update(rules)
    return merged, str(spec_path)


# ---- helpers ----------------------------------------------------------------------------------------------------

def result(check_id, status, detail):
    return {'id': check_id, 'result': status, 'detail': detail}


def not_run(check_id, why):
    return result(check_id, 'NOT_RUN', why)


def run_tool(name, args, timeout=900):
    """Run a bundled Studio checker with --json; returns (exit code, parsed JSON or None, stderr)."""
    script = TOOLS[name]
    if not script.is_file():
        return None, None, f'{script.name} is missing from the package'
    proc = subprocess.run([sys.executable, str(script), *args, '--json'], capture_output=True, text=True, timeout=timeout)
    try:
        data = json.loads(proc.stdout) if proc.stdout.strip() else None
    except json.JSONDecodeError:
        data = None
    return proc.returncode, data, proc.stderr.strip()


def ffprobe(path):
    tool = shutil.which('ffprobe')
    if not tool:
        raise RuntimeError('ffprobe not found')
    proc = subprocess.run([tool, '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)],
                          capture_output=True, text=True, check=True, timeout=120)
    return json.loads(proc.stdout)


def ffmpeg_filter(path, args, timeout=900):
    tool = shutil.which('ffmpeg')
    if not tool:
        raise RuntimeError('ffmpeg not found')
    proc = subprocess.run([tool, '-hide_banner', '-nostats', '-i', str(path), *args, '-f', 'null', '-'],
                          capture_output=True, text=True, timeout=timeout)
    if proc.returncode:
        raise RuntimeError((proc.stderr.strip().splitlines() or ['ffmpeg failed'])[-1])
    return proc.stderr


def rate(text):
    try:
        num, den = str(text).split('/')
        return float(num) / float(den) if float(den) else 0.0
    except (ValueError, ZeroDivisionError):
        return 0.0


def ratio_of(text):
    w, h = (float(x) for x in str(text).split(':'))
    return w / h


# ---- checks -----------------------------------------------------------------------------------------------------

def check_format(info, spec, kind):
    out = []
    streams = info.get('streams', [])
    video = next((s for s in streams if s.get('codec_type') == 'video'), None)
    audio = [s for s in streams if s.get('codec_type') == 'audio']
    duration = float(info.get('format', {}).get('duration') or 0)
    if kind == 'video':
        if not video:
            return [result('format', 'FAIL', 'no video stream')], duration, bool(audio)
        w, h, fps = int(video.get('width') or 0), int(video.get('height') or 0), rate(video.get('avg_frame_rate'))
        problems = []
        if spec.get('width') and w != spec['width']:
            problems.append(f'width {w}, spec {spec["width"]}')
        if spec.get('height') and h != spec['height']:
            problems.append(f'height {h}, spec {spec["height"]}')
        if spec.get('aspect') and h and abs(w / h - ratio_of(spec['aspect'])) > 0.01:
            problems.append(f'ratio {w}:{h}, spec {spec["aspect"]}')
        if spec.get('fps') and abs(fps - float(spec['fps'])) > 0.01:
            problems.append(f'{fps:.3f} fps, spec {spec["fps"]}')
        detail = f'{w}x{h}, {fps:.3f} fps, {duration:.2f} s, audio streams {len(audio)}'
    else:
        problems, detail = [], f'{duration:.2f} s'
    if duration <= 0:
        problems.append('no measurable duration')
    if spec.get('duration_min') is not None and duration < float(spec['duration_min']) - 0.05:
        problems.append(f'{duration:.2f} s is shorter than {spec["duration_min"]} s')
    if spec.get('duration_max') is not None and duration > float(spec['duration_max']) + 0.05:
        problems.append(f'{duration:.2f} s is longer than {spec["duration_max"]} s')
    if kind == 'video':
        if spec.get('audio') == 'required' and not audio:
            problems.append('the spec requires sound and the file has no audio stream')
        if spec.get('audio') == 'silent' and audio:
            problems.append('the spec requires no sound and the file has an audio stream')
    out.append(result('format', 'FAIL' if problems else 'PASS', '; '.join(problems) or detail))
    return out, duration, bool(audio)


def check_black(path, duration):
    try:
        log = ffmpeg_filter(path, ['-vf', 'blackdetect=d=0.25:pix_th=0.10', '-an'])
    except RuntimeError as error:
        return not_run('black', str(error))
    runs = [(float(a), float(b)) for a, b in re.findall(r'black_start:([\d.]+) black_end:([\d.]+)', log)]
    total = sum(b - a for a, b in runs)
    inner = [(a, b) for a, b in runs if b - a >= BLACK_RUN_SECONDS and a > EDGE_SECONDS and b < duration - EDGE_SECONDS]
    if duration and total >= 0.5 * duration:
        return result('black', 'FAIL', f'{total:.1f} s of {duration:.1f} s is black')
    if inner:
        return result('black', 'FAIL', 'black stretch inside the film: ' + ', '.join(f'{a:.2f}-{b:.2f} s' for a, b in inner))
    return result('black', 'PASS', f'{len(runs)} black runs, none inside the film of {BLACK_RUN_SECONDS} s or more')


def check_tool_verdict(check_id, name, args):
    try:
        code, data, err = run_tool(name, args)
    except (OSError, subprocess.TimeoutExpired) as error:
        return not_run(check_id, str(error))
    if code is None or code >= 2 or data is None:
        return not_run(check_id, err or f'{name} could not run (exit {code})')
    if code == 0:
        return result(check_id, 'PASS', f'{name}: PASS')
    return result(check_id, 'FAIL', f'{name}: ' + '; '.join(data.get('problems') or ['REVISE']))


def check_loudness(path, spec, required):
    try:
        log = ffmpeg_filter(path, ['-map', '0:a:0', '-af', 'ebur128=peak=true', '-vn'])
    except RuntimeError as error:
        return [not_run('loudness', str(error))]
    integrated = re.findall(r'I:\s+(-?[\d.]+|-inf) LUFS', log)
    peaks = re.findall(r'Peak:\s+(-?[\d.]+|-inf) dBFS', log)
    if not integrated:
        return [not_run('loudness', 'ebur128 printed no summary')]
    lufs = float('-inf') if integrated[-1] == '-inf' else float(integrated[-1])
    peak = float('-inf') if not peaks or peaks[-1] == '-inf' else float(peaks[-1])
    problems = []
    if lufs < SILENT_LUFS and required:
        problems.append(f'sound is practically silent ({lufs} LUFS)')
    if spec.get('lufs') is not None and abs(lufs - float(spec['lufs'])) > float(spec['lufs_tolerance']):
        problems.append(f'{lufs} LUFS, spec {spec["lufs"]} ± {spec["lufs_tolerance"]}')
    if spec.get('true_peak_max') is not None and peak > float(spec['true_peak_max']):
        problems.append(f'true peak {peak} dBTP above {spec["true_peak_max"]} dBTP')
    return [result('loudness', 'FAIL' if problems else 'PASS', '; '.join(problems) or f'{lufs} LUFS, true peak {peak} dBTP')]


def check_blank_image(path):
    try:
        from PIL import Image, ImageStat
    except ImportError:
        return not_run('blank', 'Pillow is not installed')
    with Image.open(path) as image:
        grey = image.convert('L')
        spread = ImageStat.Stat(grey).stddev[0]
        alpha_empty = 'A' in image.getbands() and image.getchannel('A').getextrema()[1] == 0
    if alpha_empty:
        return result('blank', 'FAIL', 'the image is fully transparent')
    if spread < 1.0:
        return result('blank', 'FAIL', f'the image is a single flat colour (spread {spread:.2f})')
    return result('blank', 'PASS', f'tonal spread {spread:.1f}')


def check_image(path, spec):
    out = [check_blank_image(path)]
    args = [str(path)]
    if spec.get('preset'):
        args += ['--preset', spec['preset']]
    elif spec.get('width') and spec.get('height'):
        args += ['--size', f'{spec["width"]}x{spec["height"]}']
    try:
        code, data, err = run_tool('image_probe', args)
    except (OSError, subprocess.TimeoutExpired) as error:
        return out + [not_run('image', str(error))]
    if code is None or code >= 2 or data is None:
        return out + [not_run('image', err or 'image_probe could not run')]
    problems = list(data.get('problems') or [])
    if spec.get('aspect') and data.get('size') and data['size'][1]:
        w, h = data['size']
        if abs(w / h - ratio_of(spec['aspect'])) > 0.01:
            problems.append(f'ratio {w}:{h}, spec {spec["aspect"]}')
    if spec.get('alpha') and data.get('transparency') != 'used':
        problems.append('the spec requires transparency and the image has none')
    out.append(result('image', 'FAIL' if problems else 'PASS', '; '.join(problems) or f'{data.get("size")} {data.get("mode")}'))
    return out


def check_text(path, spec):
    text = path.read_text(encoding='utf-8')
    if not text.strip():
        return [result('text', 'FAIL', 'the file has no text')]
    out = []
    try:
        code, data, err = run_tool('ai_writing_check', [str(path)])
    except (OSError, subprocess.TimeoutExpired) as error:
        code, data, err = None, None, str(error)
    language = (data or {}).get('language') or spec.get('language')
    if code is None or code >= 2 or data is None:
        out.append(not_run('ai_writing', err or 'ai_writing_check could not run'))
    else:
        out.append(result('ai_writing', 'FAIL' if code == 1 else 'PASS',
                          f'ai_writing_check: {data.get("verdict")} ({data.get("kinds")} pattern kinds)'))
    if (spec.get('language') or language) == 'pl':
        args = [str(path)] + (['--channel', spec['channel']] if spec.get('channel') else [])
        try:
            code, data, err = run_tool('pl_copy_check', args)
        except (OSError, subprocess.TimeoutExpired) as error:
            code, data, err = None, None, str(error)
        if code is None or code >= 3 or data is None:
            out.append(not_run('pl_copy', err or 'pl_copy_check could not run'))
        else:
            fixes = [f['code'] for f in data.get('findings', []) if f.get('kind') == 'fix']
            checks = [f['code'] for f in data.get('findings', []) if f.get('kind') != 'fix']
            over = (data.get('channel') or {}).get('status') == 'over_hard_limit'
            problems = ([f'safe typography fixes not applied: {", ".join(sorted(set(fixes)))} (run pl_copy_check.py --fix)'] if fixes else [])
            problems += ([f'over the {spec["channel"]} hard limit'] if over else [])
            detail = '; '.join(problems) or ('to review: ' + ', '.join(sorted(set(checks))) if checks else 'no findings')
            out.append(result('pl_copy', 'FAIL' if problems else ('WARN' if checks else 'PASS'), detail))
    if spec.get('max_chars'):
        n = len(text.strip())
        out.append(result('length', 'FAIL' if n > int(spec['max_chars']) else 'PASS', f'{n} characters, limit {spec["max_chars"]}'))
    return out


def run_checks(path, spec):
    kind = kind_of(path)
    if path.stat().st_size == 0:
        return kind, [result('file', 'FAIL', 'the file is empty')]
    checks = [result('file', 'PASS', f'{path.stat().st_size} bytes')]
    if kind in ('video', 'audio'):
        try:
            info = ffprobe(path)
        except (RuntimeError, subprocess.CalledProcessError, json.JSONDecodeError) as error:
            return kind, checks + [result('format', 'FAIL' if isinstance(error, subprocess.CalledProcessError) else 'NOT_RUN',
                                          f'cannot read the file: {error}')]
        found, duration, has_audio = check_format(info, spec, kind)
        checks += found
        if kind == 'video' and duration > 0:
            checks.append(check_black(path, duration))
            holds = [h for item in spec.get('holds', []) for h in ('--hold', item)]
            limits = []
            if spec.get('max_still_share') is not None:
                limits += ['--max-share', str(spec['max_still_share'])]
            if spec.get('max_still_seconds') is not None:
                limits += ['--max-still', str(spec['max_still_seconds'])]
            checks.append(check_tool_verdict('still', 'motion_activity', [str(path), *holds, *limits]))
            checks.append(check_tool_verdict('flash', 'flash_check', [str(path)]))
        if has_audio or kind == 'audio':
            checks += check_loudness(path, spec, required=spec.get('audio') != 'silent')
    elif kind == 'image':
        checks += check_image(path, spec)
    elif kind == 'text':
        checks += check_text(path, spec)
    else:
        checks.append(result('content', 'PASS', f'no measured checks for {path.suffix or "this type"}; review the file itself'))
    skips = spec.get('skip') or {}
    for item in checks:
        if item['id'] in skips and item['result'] in ('FAIL', 'NOT_RUN'):
            item['detail'] += f' (skipped by the spec: {skips[item["id"]]})'
            item['result'] = 'SKIPPED'
    return kind, checks


def verdict_of(checks):
    results = {c['result'] for c in checks}
    return 'FAIL' if 'FAIL' in results else 'BLOCKED' if 'NOT_RUN' in results else 'PASS'


def write_report(path, report):
    target = report_path(path)
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    return target


def base_report(path):
    stat = path.stat()
    return {'schema': SCHEMA, 'file': path.name, 'sha256': sha256(path), 'size': stat.st_size, 'mtime_ns': stat.st_mtime_ns,
            'checked_at': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')}


def gate(path, spec_arg=None):
    path = Path(path).resolve(strict=True)
    if not path.is_file():
        raise ValueError(f'{path} is not a file')
    spec, spec_source = load_spec(path, find_spec(path, spec_arg))
    kind, checks = run_checks(path, spec)
    report = base_report(path)
    report.update({'kind': kind, 'spec': spec_source, 'verdict': verdict_of(checks), 'checks': checks})
    report['report'] = str(write_report(path, report))
    return report


def waive(path, reason):
    path = Path(path).resolve(strict=True)
    if not reason or len(reason.strip()) < 8:
        raise ValueError('a waiver needs the user\'s reason in their words')
    previous = report_path(path)
    prior = json.loads(previous.read_text(encoding='utf-8')) if previous.is_file() else None
    report = base_report(path)
    report.update({'verdict': 'WAIVED', 'waiver_reason': reason.strip(),
                   'waived_checks': [c for c in (prior or {}).get('checks', []) if c['result'] in ('FAIL', 'NOT_RUN')]
                   if prior and prior.get('sha256') == report['sha256'] else 'no current report for this file'})
    report['report'] = str(write_report(path, report))
    return report


# ---- status (also used by the hook) -----------------------------------------------------------------------------

def deliverables(folder):
    for item in sorted(Path(folder).rglob('*')):
        rel = item.relative_to(folder)
        if item.is_file() and item.suffix.lower() in DELIVERABLE and not any(p.startswith('.') for p in rel.parts):
            yield item


def file_state(path):
    """PASS or WAIVED when a current report covers the file; otherwise the reason it is not cleared."""
    target = report_path(path)
    if not target.is_file():
        return 'UNCHECKED'
    try:
        report = json.loads(target.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError):
        return 'UNCHECKED'
    stat = path.stat()
    same = report.get('size') == stat.st_size and report.get('mtime_ns') == stat.st_mtime_ns
    if not same and report.get('sha256') != sha256(path):
        return 'CHANGED'
    return report.get('verdict', 'UNCHECKED')


def status(folder):
    rows = [{'file': str(p), 'state': file_state(p)} for p in deliverables(folder)]
    return {'folder': str(folder), 'files': rows, 'open': [r for r in rows if r['state'] not in ('PASS', 'WAIVED')]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest='command', required=True)
    c = sub.add_parser('check', help='run the checks on one or more final files and write their reports')
    c.add_argument('files', nargs='+')
    c.add_argument('--spec', help='gate.json with the brief\'s requirements (default: nearest gate.json)')
    c.add_argument('--json', action='store_true')
    s = sub.add_parser('status', help='list the files in an export folder that lack a current PASS or WAIVED report')
    s.add_argument('folder')
    s.add_argument('--json', action='store_true')
    w = sub.add_parser('waive', help='record that the user accepts a file that did not pass, with their reason')
    w.add_argument('file')
    w.add_argument('--reason', required=True)
    w.add_argument('--json', action='store_true')
    args = parser.parse_args(argv)
    try:
        if args.command == 'status':
            report = status(Path(args.folder))
            print(json.dumps(report, indent=2) if args.json else
                  '\n'.join(f"{r['state']:9} {r['file']}" for r in report['files']) or 'no deliverable files')
            return 1 if report['open'] else 0
        if args.command == 'waive':
            report = waive(args.file, args.reason)
            print(json.dumps(report, indent=2, ensure_ascii=False) if args.json else f"WAIVED {report['file']}: {report['waiver_reason']}")
            return 0
        reports = [gate(f, args.spec) for f in args.files]
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f'studio_gate: {error}', file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(reports if len(reports) > 1 else reports[0], indent=2, ensure_ascii=False))
    else:
        for r in reports:
            print(f"{r['verdict']} {r['file']}")
            for item in r['checks']:
                if item['result'] != 'PASS':
                    print(f"  {item['result']:8} {item['id']}: {item['detail']}")
    worst = {r['verdict'] for r in reports}
    return 1 if 'FAIL' in worst else 2 if 'BLOCKED' in worst else 0


if __name__ == '__main__':
    sys.exit(main())
