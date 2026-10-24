#!/usr/bin/env python3
"""voice-narration launcher: local voice-over generation, measurement and a consented, pinned VoxCPM2 install.

    python3 runtime.py status [--json]

Standard library only. `status` never writes. Local engines are for the user's own computer; in a cloud environment
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


COMMANDS = {'status': cmd_status}


def build_parser(env):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('status')
    p.add_argument('--json', action='store_true')
    p.add_argument('--root', type=Path, default=default_root(env))
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
