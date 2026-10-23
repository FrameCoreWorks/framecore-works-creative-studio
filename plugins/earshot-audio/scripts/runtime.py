#!/usr/bin/env python3
"""earshot-audio launcher: a pinned, verified local Earshot runtime and an allowlist of local commands.

    python3 runtime.py status [--json]
    python3 runtime.py install --tier light|full [--yes]
    python3 runtime.py fetch-models [--yes]
    python3 runtime.py run [--threads N] <command> [args...]
    python3 runtime.py python <real-sound script> [args...]
    python3 runtime.py exec [python args...]      the venv interpreter with the plugin's offline cache: {{PY}}

Standard library only. `status` never writes; `install` and `fetch-models` print their plan and write nothing without
--yes. The engine comes from one pinned upstream commit, and every file is checked against upstream.json before
anything is installed. The `llm` (audio upload to Gemini) and `mcp` (server) commands are outside this plugin and are
refused before any process starts. Runs are offline: models must already be in the cache.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

PLUGIN = Path(__file__).resolve().parent.parent
REAL_SOUND = PLUGIN / 'skills' / 'earshot' / 'real-sound' / 'scripts'
PIN = {'repository': 'https://github.com/Leonxlnx/earshot', 'tag': 'v0.4.0',
       'commit': '591fa3e028032e6dce56620a20e932e35667e8d8', 'tree': 'd6f2dbc43f7b38b2147cfd04bbd7aa9055701f1a'}
ALLOWED = frozenset({'doctor', 'measure', 'describe', 'match', 'rank', 'find', 'compare', 'ab', 'realness', 'timeline',
                     'sheet', 'critique', 'profile', 'forge', 'fit', 'sfx', 'kit', 'gallery'})
LIGHT = ['numpy>=1.26', 'scipy>=1.11', 'soundfile>=0.12', 'soxr>=0.3', 'librosa>=0.10', 'pyloudnorm>=0.1',
         'scikit-learn>=1.3', 'pillow>=10', 'matplotlib>=3.8']
FULL = ['torch>=2.6', 'transformers>=4.40', 'safetensors', 'huggingface_hub']
TORCH_INDEX = 'https://download.pytorch.org/whl/cpu'
MODELS = ('laion/larger_clap_general', 'MIT/ast-finetuned-audioset-10-10-0.4593')
OFFLINE = {'EARSHOT_OFFLINE': '1', 'HF_HUB_OFFLINE': '1', 'TRANSFORMERS_OFFLINE': '1'}
SIZES = {'light': 'about 200 MB (engine, NumPy, SciPy, librosa and friends)',
         'full': 'about 1.5 GB (light plus CPU PyTorch and transformers); models are a separate fetch-models step, about 1.1 GB'}


class Refused(Exception):
    pass


def default_root():
    return Path(os.environ.get('EARSHOT_NATIVE_ROOT') or Path.home() / '.framecore-studio' / 'extensions' / 'earshot')


def real_command(argv):
    """The earshot subcommand after any global options (`--threads N` or `--threads=N`)."""
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == '--threads':
            i += 2
        elif arg.startswith('-'):
            i += 1
        else:
            return arg
    return None


def check_command(argv):
    name = real_command(argv)
    if name is None:
        raise Refused('no earshot command given')
    if name not in ALLOWED:
        raise Refused(f'`{name}` is not available in earshot-audio (local commands only: {", ".join(sorted(ALLOWED))})')
    if name == 'doctor' and any(a == '--fetch' or a.startswith('--fetch=') for a in argv):
        raise Refused('model downloads go through `runtime.py fetch-models --yes`, not doctor --fetch')


def real_sound_script(name):
    path = (REAL_SOUND / name).resolve()
    if REAL_SOUND.resolve() not in path.parents or not path.is_file():
        raise Refused(f'{name} is not a real-sound script of this plugin')
    return path


def venv_python(root):
    for candidate in (Path(root) / 'venv' / 'bin' / 'python', Path(root) / 'venv' / 'Scripts' / 'python.exe'):
        if candidate.exists():
            return candidate
    return None


def load_manifest():
    return json.loads((PLUGIN / 'upstream.json').read_text(encoding='utf-8'))


def verify_tree(src, manifest):
    """Paths that differ from the manifest: changed, missing or extra (the .git folder is ignored)."""
    src = Path(src)
    found = {p.relative_to(src).as_posix(): p for p in src.rglob('*') if p.is_file() and '.git' not in p.relative_to(src).parts}
    problems = [path for path, digest in manifest.items()
                if path not in found or hashlib.sha256(found[path].read_bytes()).hexdigest() != digest]
    problems += [path for path in found if path not in manifest]
    return sorted(problems)


def fetch_source(dest):
    """The pinned upstream source in dest: git at the exact commit (tree checked), else the commit's archive."""
    dest = Path(dest)
    if shutil.which('git'):
        repo = dest / 'earshot'
        steps = [['git', 'init', '-q', str(repo)], ['git', '-C', str(repo), 'fetch', '-q', '--depth=1', PIN['repository'], PIN['commit']],
                 ['git', '-C', str(repo), 'checkout', '-q', 'FETCH_HEAD']]
        try:
            for step in steps:
                subprocess.run(step, check=True, capture_output=True, timeout=600)
            tree = subprocess.run(['git', '-C', str(repo), 'rev-parse', 'HEAD^{tree}'], check=True, capture_output=True, text=True).stdout.strip()
            if tree == PIN['tree']:
                return repo
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            pass
        shutil.rmtree(repo, ignore_errors=True)
    archive = dest / 'earshot.zip'
    urllib.request.urlretrieve(f"{PIN['repository']}/archive/{PIN['commit']}.zip", archive)
    with zipfile.ZipFile(archive) as zf:
        zf.extractall(dest / 'unzipped')
    return next((dest / 'unzipped').iterdir())


def _python_ok(python, modules):
    try:
        return subprocess.run([str(python), '-c', f'import {", ".join(modules)}'], capture_output=True, timeout=120).returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


def status(root):
    root = Path(root)
    python = venv_python(root)
    marker = root / 'engine.json'
    try:
        engine = json.loads(marker.read_text()) if marker.is_file() else {}
    except (OSError, ValueError):
        engine = {}
    light = bool(python) and _python_ok(python, ['earshot', 'numpy', 'scipy', 'soundfile', 'librosa', 'pyloudnorm'])
    full = light and _python_ok(python, ['torch', 'transformers'])
    hub = root / 'cache' / 'hf'
    cached = all(any(hub.glob(f"**/models--{model.replace('/', '--')}")) for model in MODELS) if hub.is_dir() else False
    report = {'root': str(root), 'venv': str(python) if python else None, 'engine_commit': engine.get('commit'),
              'pinned_commit': PIN['commit'], 'light_ready': light, 'full_ready': full, 'models_cached': cached,
              'ffmpeg': shutil.which('ffmpeg'), 'ffprobe': shutil.which('ffprobe')}
    report['state'] = 'ready_full' if full and cached else 'ready_light' if light else 'unavailable'
    if python and engine.get('commit') != PIN['commit']:   # an older route's venv, or an unfinished install
        report['state'] = 'unavailable'
        report['note'] = 'the engine here is not the pinned, completed install of this plugin; reinstall with install --yes'
    return report


def plan(tier, root):
    return {'action': f'install --tier {tier}', 'root': str(root), 'writes': [str(Path(root) / 'venv'), str(Path(root) / 'engine.json')],
            'source': f"{PIN['repository']} at {PIN['commit']} ({PIN['tag']}), every file checked against upstream.json",
            'size': SIZES[tier], 'not_installed': ['mcp and llm extras', 'models (fetch-models)'],
            'confirm': 'run again with --yes after the user agrees'}


def install(tier, root):
    root = Path(root)
    with tempfile.TemporaryDirectory(prefix='earshot-src-') as tmp:
        src = fetch_source(tmp)
        problems = verify_tree(src, load_manifest()['files'])
        if problems:
            print('earshot-audio: the downloaded source differs from the pinned upstream; nothing was installed:\n  '
                  + '\n  '.join(problems[:20]), file=sys.stderr)
            return 1
        root.mkdir(parents=True, exist_ok=True)
        subprocess.run([sys.executable, '-m', 'venv', str(root / 'venv')], check=True)
        python = str(venv_python(root))
        # --no-warn-conflicts: the light tier leaves out torch on purpose; pip would call that an ERROR
        pip = [python, '-m', 'pip', 'install', '-q', '--disable-pip-version-check', '--no-warn-conflicts']
        subprocess.run(pip + ['--no-deps', str(src)], check=True)
        subprocess.run(pip + LIGHT, check=True)
        if tier == 'full':
            subprocess.run(pip + ['--index-url', TORCH_INDEX, 'torch>=2.6'], check=True)
            subprocess.run(pip + FULL[1:], check=True)
        disable_remote_modules(engine_package(python))
    (root / 'engine.json').write_text(json.dumps({**PIN, 'tier': tier}, indent=2) + '\n')
    print(json.dumps(status(root), indent=2))
    return 0


REMOTE_MODULES = ('llm.py', 'mcp_server.py')
STUB = ('"""Removed by earshot-audio: this plugin runs Earshot locally only, with no audio upload and no MCP server."""\n'
        'raise ImportError("earshot-audio: the audio-LLM upload and the MCP server are not part of this installation")\n')


def engine_package(python):
    """The installed earshot package folder in the venv, or None."""
    try:
        out = subprocess.run([str(python), '-c', 'import earshot, os; print(os.path.dirname(earshot.__file__))'],
                             capture_output=True, text=True, timeout=120).stdout
        folder = Path(str(out).strip())
        return folder if folder.is_dir() else None
    except (OSError, subprocess.TimeoutExpired, TypeError, ValueError):
        return None


def disable_remote_modules(package):
    """Replace the engine's upload (llm) and server (mcp) modules in the venv with an ImportError stub."""
    if not package:
        raise OSError('the earshot package is not in the venv, so the upload stub could not be applied')
    for name in REMOTE_MODULES:
        (Path(package) / name).write_text(STUB)   # also when absent: an import fails loudly either way


def engine_env(root, offline=True):
    env = {k: v for k, v in os.environ.items() if k not in ('GEMINI_API_KEY', 'GOOGLE_API_KEY')}
    env['EARSHOT_HOME'] = str(Path(root) / 'cache')   # the cache fetch-models fills; keys dropped, nothing to upload with
    if offline:
        env.update(OFFLINE)
    return env


def split_passthrough(argv):
    """(root, command, rest) for `run` and `python`, whose arguments go to earshot untouched; else None."""
    root, i = None, 0
    if argv[:1] == ['--root'] and len(argv) > 1:
        root, i = Path(argv[1]), 2
    elif argv[:1] and argv[0].startswith('--root='):
        root, i = Path(argv[0].split('=', 1)[1]), 1
    if i < len(argv) and argv[i] in ('run', 'python', 'exec'):
        return root, argv[i], argv[i + 1:]
    return None


def check_exec(args):
    """`-m earshot <command>` goes through the allowlist; any other earshot module run directly is refused."""
    if '-m' in args:
        module = args[args.index('-m') + 1] if args.index('-m') + 1 < len(args) else ''
        if module == 'earshot':
            check_command(args[args.index('-m') + 2:])
        elif module.startswith('earshot.'):
            raise Refused(f'`-m {module}` is not available in earshot-audio; use `-m earshot <command>`')


def passthrough(root, command, rest):
    if command == 'exec':
        try:
            check_exec(rest)
        except Refused as error:
            print(f'earshot-audio: {error}', file=sys.stderr)
            return 2
        python = venv_python(root)
        if not python:
            print('earshot-audio: the engine is not installed here; see `runtime.py install --tier light`', file=sys.stderr)
            return 1
        return subprocess.run([str(python), *rest], env=engine_env(root)).returncode
    if command == 'run':
        try:
            check_command(rest)
        except Refused as error:
            print(f'earshot-audio: {error}', file=sys.stderr)
            return 2
        python = venv_python(root)
        if not python:
            print('earshot-audio: the engine is not installed here; see `runtime.py install --tier light`', file=sys.stderr)
            return 1
        return subprocess.run([str(python), '-m', 'earshot', *rest], env=engine_env(root)).returncode
    if not rest:
        print('earshot-audio: name a real-sound script', file=sys.stderr)
        return 2
    try:
        script = real_sound_script(rest[0])
    except Refused as error:
        print(f'earshot-audio: {error}', file=sys.stderr)
        return 2
    python = venv_python(root)
    if not python:
        print('earshot-audio: the engine is not installed here; see `runtime.py install --tier light`', file=sys.stderr)
        return 1
    return subprocess.run([str(python), '-I', str(script), *rest[1:]], env=engine_env(root)).returncode


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    split = split_passthrough(argv)
    if split:
        root, command, rest = split
        return passthrough(root or default_root(), command, rest)
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--root', type=Path, default=None, help='runtime folder (default ~/.framecore-studio/extensions/earshot)')
    sub = parser.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('status')
    p.add_argument('--json', action='store_true')
    p.add_argument('--root', type=Path, default=argparse.SUPPRESS)
    p = sub.add_parser('install')
    p.add_argument('--tier', choices=('light', 'full'), required=True)
    p.add_argument('--yes', action='store_true')
    p.add_argument('--root', type=Path, default=argparse.SUPPRESS)
    p = sub.add_parser('fetch-models')
    p.add_argument('--yes', action='store_true')
    p.add_argument('--root', type=Path, default=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    root = Path(args.root) if args.root else default_root()

    if args.cmd == 'status':
        report = status(root)
        print(json.dumps(report, indent=2) if args.json else
              f"{report['state']}: light {report['light_ready']}, full {report['full_ready']}, models cached {report['models_cached']}, "
              f"engine {report['engine_commit'] or 'not installed'} (pinned {PIN['commit'][:7]})")
        return 0
    if args.cmd == 'install':
        if not args.yes:
            print(json.dumps(plan(args.tier, root), indent=2))
            return 0
        try:
            return install(args.tier, root)
        except (subprocess.CalledProcessError, OSError) as error:
            what = ' '.join(map(str, error.cmd[-2:])) if isinstance(error, subprocess.CalledProcessError) else str(error)
            print(f'earshot-audio: install stopped at `{what}` (network, proxy or disk); nothing beyond it was installed; '
                  f'see `runtime.py status`', file=sys.stderr)
            return 1
    if args.cmd == 'fetch-models':
        python = venv_python(root)
        if not args.yes:
            print(json.dumps({'action': 'fetch-models', 'downloads': list(MODELS), 'size': 'about 1.1 GB, pinned revisions',
                              'into': str(root / 'cache'), 'confirm': 'run again with --yes after the user agrees'}, indent=2))
            return 0
        if not python or not status(root).get('full_ready'):
            print('earshot-audio: models need the full tier: `runtime.py install --tier full --yes` first', file=sys.stderr)
            return 1
        return subprocess.run([str(python), '-m', 'earshot', 'doctor', '--fetch'], env=engine_env(root, offline=False)).returncode
    return 2


if __name__ == '__main__':
    sys.exit(main())
