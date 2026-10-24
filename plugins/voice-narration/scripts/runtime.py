#!/usr/bin/env python3
"""voice-narration launcher: local voice-over generation, measurement and a consented, pinned VoxCPM2 install.

    python3 runtime.py status [--json]
    python3 runtime.py install voxcpm [--yes] [--allow-cloud]
    python3 runtime.py fetch-models [--yes] [--allow-cloud]
    python3 runtime.py generate --engine voxcpm|voicebox --cues cues.json --out DIR [--lexicon F] [--only ID ...]
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
import voicebox  # noqa: E402

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
    try:
        lock = formats.Lock.load(args.out)
    except formats.CueError as error:
        print(f'error: {error}', file=sys.stderr)
        return 2
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
    try:
        lock = formats.Lock.load(args.out)
    except formats.CueError as error:
        print(f'error: {error}', file=sys.stderr)
        return 2
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
    lock.set_line(cue.id, wav=dest.name, sha256=audio.sha256(dest), stretch_percent=float(args.percent),
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


WORKER = Path(__file__).resolve().parent / 'voxcpm_worker.py'


def record_take(lock, cue_id, line, dest, ok, error=None):
    """A good take replaces the line; a failed attempt keeps the previous take's description and marks the line."""
    if ok:
        lock.set_line(cue_id, **line, wav=dest.name, sha256=audio.sha256(dest), status='ok', error=None)
    elif cue_id in lock.lines and lock.lines[cue_id].get('wav'):
        lock.set_line(cue_id, status='failed', error=error)
    else:
        lock.set_line(cue_id, **line, status='failed', error=error)


def generate_voicebox(args, cues, lock, texts, lexicon_hash):
    client = voicebox.VoiceboxClient(args.voicebox_url)
    for cue in cues:
        dest = Path(args.out) / f'{cue.id}.wav'
        line = dict(engine='voicebox', model=args.voicebox_engine or 'profile default', engine_version=None,
                    voice_source=f'voicebox profile {args.profile}', consent=None, text_sent=texts[cue.id],
                    stretch_percent=None, lexicon_sha256=lexicon_hash)
        try:
            generation = client.generate(texts[cue.id], args.profile, args.language, args.voicebox_engine)
            state = client.wait(generation)
            if state.get('status') != 'completed':
                raise voicebox.VoiceboxError(state.get('error') or f"generation {state.get('status', 'unknown')}")
            client.download(generation, dest)
        except (voicebox.VoiceboxError, audio.AudioError, OSError) as error:
            record_take(lock, cue.id, line, dest, False, str(error))
            continue
        record_take(lock, cue.id, line, dest, True)


def generate_voxcpm(args, env, cues, lock, texts, lexicon_hash):
    out = Path(args.out)
    jobs = [{'id': c.id, 'text': texts[c.id], 'out': str(out / f'{c.id}.wav'), 'seed': args.seed,
             'reference_wav': str(args.reference_wav) if args.reference_wav else None} for c in cues]
    job_path = out / '.voxcpm-job.json'
    job_path.write_text(json.dumps({'model': VOXCPM_MODEL, 'jobs': jobs}, ensure_ascii=False), encoding='utf-8')
    results = {}
    try:
        result = subprocess.run([str(venv_python(args.root)), '-I', str(WORKER), str(job_path)],
                                env=engine_env(args.root, env, offline=True), capture_output=True, text=True)
        for raw in result.stdout.splitlines():
            try:
                item = json.loads(raw)
                results[item['id']] = item
            except (ValueError, KeyError, TypeError):
                continue
        fallback = one_line(result) if result.returncode else 'no result from the worker'
    except OSError as error:
        fallback = str(error)
    finally:
        job_path.unlink(missing_ok=True)
    version = voxcpm_version(args.root)
    source = f'reference:{args.reference_wav}' if args.reference_wav else 'voxcpm default voice'
    for cue in cues:
        item = results.get(cue.id, {'status': 'failed', 'error': fallback})
        line = dict(engine='voxcpm', model=VOXCPM_MODEL, engine_version=version, voice_source=source,
                    consent=args.consent, text_sent=texts[cue.id], stretch_percent=None, lexicon_sha256=lexicon_hash)
        dest = out / f'{cue.id}.wav'
        ok = item.get('status') == 'ok' and dest.exists()
        record_take(lock, cue.id, line, dest, ok, None if ok else item.get('error') or 'no audio written')


def cmd_generate(args, env):
    if args.reference_wav and not (args.consent or '').strip():
        print('refused: cloning needs --consent with the voice owner\'s recorded permission', file=sys.stderr)
        return 2
    if args.engine == 'voicebox' and not args.profile:
        print('error: --engine voicebox needs --profile (a Voicebox voice profile id)', file=sys.stderr)
        return 2
    try:
        cues = formats.load_cues(args.cues)
        lexicon, lexicon_hash = formats.load_lexicon(args.lexicon)
    except (formats.CueError, OSError, ValueError) as error:
        print(f'error: {error}', file=sys.stderr)
        return 2
    selected = [c for c in cues if not args.only or c.id in args.only]
    unknown = set(args.only or ()) - {c.id for c in cues}
    if unknown:
        print(f'error: no line {", ".join(sorted(unknown))} in {args.cues}', file=sys.stderr)
        return 2
    if args.engine == 'voicebox' and not probe_voicebox(args.voicebox_url):
        print(f'error: voicebox is not running on {args.voicebox_url} (it only runs on the user\'s own computer); '
              'no other engine was tried', file=sys.stderr)
        return 1
    if args.engine == 'voxcpm':
        if not venv_python(args.root).exists():
            print('error: VoxCPM2 is not installed here; run: install voxcpm --yes', file=sys.stderr)
            return 1
        if not weights_cached(args.root):
            print('error: VoxCPM2 weights are not downloaded; run: fetch-models --yes', file=sys.stderr)
            return 1
    texts = {c.id: formats.apply_lexicon(c.text, lexicon) for c in selected}
    try:
        lock = formats.Lock.load(args.out)
    except formats.CueError as error:
        print(f'error: {error}', file=sys.stderr)
        return 2
    Path(args.out).mkdir(parents=True, exist_ok=True)
    if args.engine == 'voicebox':
        generate_voicebox(args, selected, lock, texts, lexicon_hash)
    else:
        generate_voxcpm(args, env, selected, lock, texts, lexicon_hash)
    rows = audio.measure_all(cues, args.out, lock)
    record_measure(lock, rows)
    lock.save()
    print_measure(rows)
    failed = [c.id for c in selected if lock.lines[c.id]['status'] != 'ok']
    for line_id in failed:
        print(f'failed: {line_id}: {lock.lines[line_id]["error"]}', file=sys.stderr)
    return 1 if failed else 0


COMMANDS = {'status': cmd_status, 'install': cmd_install, 'fetch-models': cmd_fetch_models, 'generate': cmd_generate, 'measure': cmd_measure, 'stretch': cmd_stretch}


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
    p = sub.add_parser('generate')
    p.add_argument('--engine', choices=['voxcpm', 'voicebox'], required=True)
    p.add_argument('--cues', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--lexicon', type=Path)
    p.add_argument('--only', nargs='+')
    p.add_argument('--language', default='pl')
    p.add_argument('--profile')
    p.add_argument('--voicebox-engine')
    p.add_argument('--voicebox-url', default=VOICEBOX_URL)
    p.add_argument('--reference-wav', type=Path)
    p.add_argument('--consent')
    p.add_argument('--seed', type=int, default=42)
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
