#!/usr/bin/env python3
"""voice-narration launcher: local voice-over generation, measurement and a consented, pinned VoxCPM2 install.

    python3 runtime.py status [--json]
    python3 runtime.py install voxcpm [--yes] [--allow-cloud]
    python3 runtime.py fetch-models [--yes] [--allow-cloud]
    python3 runtime.py measure --cues cues.json --out DIR [--json]
    python3 runtime.py stretch LINE_ID --percent N --cues cues.json --out DIR [--yes]

Standard library only. `status` never writes; `install` and `fetch-models` print their plan and write nothing
without --yes, and in a cloud environment --yes also needs --allow-cloud. Local engines are for the user's own computer; in a cloud environment
the launcher says so. Any command not listed in COMMANDS is refused before a process starts.
"""
import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audio  # noqa: E402
import formats  # noqa: E402

PLUGIN = Path(__file__).resolve().parent.parent
VOICEBOX_URL = 'http://127.0.0.1:17493'
VOXCPM_PIN = 'voxcpm==2.0.3'
VOXCPM_MODEL = 'openbmb/VoxCPM2'


def detect_environment(env):
    """'cloud' when a known sandbox marker is set, otherwise 'local'."""
    if env.get('CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE') or env.get('CLAUDE_CODE_REMOTE', '').lower() == 'true':
        return 'cloud'
    if env.get('CODEX_SANDBOX') or env.get('CODEX_CLOUD'):
        return 'cloud'
    return 'local'


def default_root(env):
    if env.get('VOICE_NARRATION_ROOT'):
        return Path(env['VOICE_NARRATION_ROOT'])
    return Path.home() / '.framecore-studio' / 'extensions' / 'voxcpm'


def venv_python(root):
    if os.name == 'nt':
        return root / 'venv' / 'Scripts' / 'python.exe'
    return root / 'venv' / 'bin' / 'python'


def hf_cache(root):
    return root / 'hf-cache'


def weights_cached(root):
    snapshots = hf_cache(root) / 'hub' / ('models--' + VOXCPM_MODEL.replace('/', '--')) / 'snapshots'
    return snapshots.is_dir() and any(snapshots.iterdir())


def probe_voicebox(base_url=VOICEBOX_URL):
    try:
        with urllib.request.urlopen(base_url + '/health', timeout=2) as response:
            return response.status == 200
    except (OSError, ValueError):
        return False


def voxcpm_version(root):
    python = venv_python(root)
    if not python.exists():
        return 'unavailable'
    probe = 'import importlib.metadata as m; print(m.version("voxcpm"))'
    try:
        result = subprocess.run([str(python), '-I', '-c', probe], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        return 'unavailable'
    return result.stdout.strip() if result.returncode == 0 and result.stdout.strip() else 'unavailable'


def gpu():
    smi = shutil.which('nvidia-smi')
    if not smi:
        return 'unknown'
    try:
        result = subprocess.run([smi, '--query-gpu=name,memory.total', '--format=csv,noheader'],
                                capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired):
        return 'unknown'
    if result.returncode != 0:
        return 'unknown'
    return result.stdout.strip() or 'unknown'


def status(root, env):
    return {
        'environment': detect_environment(env),
        'python': platform.python_version(),
        'venv': str(root / 'venv'),
        'voxcpm_version': voxcpm_version(root),
        'weights_cached': weights_cached(root),
        'voicebox': 'ready' if probe_voicebox() else 'unavailable',
        'ffmpeg': shutil.which('ffmpeg') is not None,
        'ffprobe': shutil.which('ffprobe') is not None,
        'gpu': gpu(),
    }


def cmd_status(args, env):
    data = status(args.root, env)
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        for key, value in data.items():
            print(f'{key}: {value}')
        if data['environment'] == 'cloud':
            print('note: this is a cloud environment; local engines belong on the user\'s own computer')
    return 0


def print_measure(rows):
    for row in rows:
        duration = '-' if row['duration'] is None else f"{row['duration']:.2f}s"
        extra = f" (+{row['over_by']:.2f}s)" if row['verdict'] == 'over' else ''
        print(f"{row['id']}: {duration} / {row['max_seconds']:.2f}s {row['verdict']}{extra}")


def record_measure(lock, rows):
    for row in rows:
        if row['verdict'] in ('fits', 'over', 'silent'):
            lock.set_line(row['id'], duration=row['duration'], max_seconds=row['max_seconds'], verdict=row['verdict'])


def cmd_measure(args, env):
    try:
        cues = formats.load_cues(args.cues)
    except formats.CueError as error:
        print(f'error: {error}', file=sys.stderr)
        return 2
    lock = formats.Lock.load(args.out)
    rows = audio.measure_all(cues, args.out, lock)
    record_measure(lock, rows)
    if any(row['verdict'] in ('fits', 'over', 'silent') for row in rows):
        lock.save()
    if args.json:
        print(json.dumps(rows, indent=2))
    else:
        print_measure(rows)
    return 1 if any(row['verdict'] in ('missing', 'unreadable') for row in rows) else 0


def cmd_stretch(args, env):
    if not 0 < args.percent <= audio.MAX_STRETCH_PERCENT:
        print(f'refused: --percent must be above 0 and at most {audio.MAX_STRETCH_PERCENT:g}', file=sys.stderr)
        return 2
    try:
        cue = {c.id: c for c in formats.load_cues(args.cues)}[args.line_id]
    except formats.CueError as error:
        print(f'error: {error}', file=sys.stderr)
        return 2
    except KeyError:
        print(f'error: no line {args.line_id} in {args.cues}', file=sys.stderr)
        return 2
    source = Path(args.out) / f'{cue.id}.wav'
    dest = Path(args.out) / f'{cue.id}.stretched.wav'
    if not args.yes:
        print(f'plan: speed {source} up by {args.percent:g}% with FFmpeg into {dest}; nothing written. Rerun with --yes.')
        return 0
    ffmpeg = shutil.which('ffmpeg')
    if not ffmpeg:
        print('error: FFmpeg is not on PATH; shorten the text or regenerate the line instead', file=sys.stderr)
        return 1
    if not source.exists():
        print(f'error: {source} does not exist', file=sys.stderr)
        return 1
    try:
        audio.stretch(source, args.percent, ffmpeg, dest)
        duration = audio.spoken_duration(dest)
    except audio.AudioError as error:
        print(f'error: {error}', file=sys.stderr)
        return 1
    lock = formats.Lock.load(args.out)
    lock.set_line(cue.id, wav=str(dest), sha256=audio.sha256(dest), stretch_percent=float(args.percent),
                  duration=duration, max_seconds=cue.max_seconds, verdict=audio.verdict(duration, cue.max_seconds))
    lock.save()
    print_measure([{'id': cue.id, 'duration': duration, 'max_seconds': cue.max_seconds,
                    'verdict': audio.verdict(duration, cue.max_seconds),
                    'over_by': round(duration - cue.max_seconds, 2)}])
    return 0


CLOUD_WARNING = ('warning: this is a cloud environment; the files land on a temporary disk and are lost with the '
                 'session. Local engines belong on the user\'s own computer.')


def engine_env(root, env, offline):
    result = dict(env)
    result['HF_HOME'] = str(hf_cache(root))
    if offline:
        result['HF_HUB_OFFLINE'] = '1'
    return result


def consent_gate(args, env, plan_lines):
    """Print the plan and return an exit code when nothing should be written, else None."""
    cloud = detect_environment(env) == 'cloud'
    if not args.yes:
        if cloud:
            print(CLOUD_WARNING)
        print('\n'.join(plan_lines))
        print('Nothing was written. Rerun with --yes to proceed.')
        return 0
    if cloud and not args.allow_cloud:
        print('refused: cloud environment; files would be lost with the session. '
              'Use ElevenLabs or the script handoff, or add --allow-cloud if the user insists.', file=sys.stderr)
        return 2
    return None


def one_line(error):
    detail = (getattr(error, 'stderr', None) or '').strip().splitlines()
    return detail[-1] if detail else str(error)


def cmd_install(args, env):
    root = args.root
    code = consent_gate(args, env, [
        f'plan: create a Python environment in {root / "venv"}',
        f'plan: pip install {VOXCPM_PIN} soundfile (about 3 GB of Python packages including PyTorch)',
        'plan: model weights are fetched separately with fetch-models'])
    if code is not None:
        return code
    try:
        root.mkdir(parents=True, exist_ok=True)
        subprocess.run([sys.executable, '-m', 'venv', str(root / 'venv')], check=True, capture_output=True, text=True)
        pip = [str(venv_python(root)), '-m', 'pip', 'install', '-q', '--disable-pip-version-check']
        subprocess.run(pip + ['--upgrade', 'pip'], check=True, capture_output=True, text=True)
        subprocess.run(pip + [VOXCPM_PIN, 'soundfile'], check=True, capture_output=True, text=True)
    except (OSError, subprocess.CalledProcessError) as error:
        print(f'error: installation failed: {one_line(error)}', file=sys.stderr)
        return 1
    print(f'installed: voxcpm {voxcpm_version(root)} in {root / "venv"}; next: fetch-models --yes')
    return 0


def cmd_fetch_models(args, env):
    root = args.root
    code = consent_gate(args, env, [
        f'plan: download the {VOXCPM_MODEL} weights (about 5 GB) from huggingface.co into {hf_cache(root)}'])
    if code is not None:
        return code
    python = venv_python(root)
    if not python.exists():
        print('error: VoxCPM2 is not installed here; run: install voxcpm --yes', file=sys.stderr)
        return 1
    script = f"from huggingface_hub import snapshot_download; snapshot_download('{VOXCPM_MODEL}')"
    try:
        subprocess.run([str(python), '-I', '-c', script], check=True, env=engine_env(root, env, offline=False),
                       capture_output=True, text=True)
    except (OSError, subprocess.CalledProcessError) as error:
        print(f'error: download failed: {one_line(error)}', file=sys.stderr)
        return 1
    print(f'fetched: {VOXCPM_MODEL} into {hf_cache(root)}')
    return 0


COMMANDS = {'status': cmd_status, 'install': cmd_install, 'fetch-models': cmd_fetch_models, 'measure': cmd_measure, 'stretch': cmd_stretch}


def build_parser(env):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('status')
    p.add_argument('--json', action='store_true')
    p.add_argument('--root', type=Path, default=default_root(env))
    p = sub.add_parser('install')
    p.add_argument('engine', choices=['voxcpm'])
    p.add_argument('--yes', action='store_true')
    p.add_argument('--allow-cloud', action='store_true')
    p.add_argument('--root', type=Path, default=default_root(env))
    p = sub.add_parser('fetch-models')
    p.add_argument('--yes', action='store_true')
    p.add_argument('--allow-cloud', action='store_true')
    p.add_argument('--root', type=Path, default=default_root(env))
    p = sub.add_parser('measure')
    p.add_argument('--cues', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--json', action='store_true')
    p = sub.add_parser('stretch')
    p.add_argument('line_id')
    p.add_argument('--percent', type=float, required=True)
    p.add_argument('--cues', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--yes', action='store_true')
    return parser


def main(argv=None, env=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    env = dict(os.environ if env is None else env)
    if argv and not argv[0].startswith('-') and argv[0] not in COMMANDS:
        print(f'refused: {argv[0]} is not a voice-narration command', file=sys.stderr)
        return 2
    args = build_parser(env).parse_args(argv)
    return COMMANDS[args.command](args, env)


if __name__ == '__main__':
    sys.exit(main())
