#!/usr/bin/env python3
"""Read-only installation inventory. Never install, download models or infer host support."""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
PLUGIN = HERE.parents[3]
HOSTS = ('chatgpt', 'chatgpt_work', 'codex', 'claude_code', 'claude_apps')
UNUSABLE = ('missing', 'broken', 'unknown')


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def execute(argv, timeout=20, env=None):
    """Run only an explicit local command; preserve failure and timeout evidence."""
    try:
        done = subprocess.run([str(a) for a in argv], capture_output=True, text=True,
                              timeout=timeout, env=env)
        return {'exit_code': done.returncode, 'stdout': done.stdout[-16000:],
                'stderr': done.stderr[-2000:], 'command': [str(a) for a in argv]}
    except (OSError, subprocess.SubprocessError) as error:
        return {'exit_code': None, 'stdout': '', 'stderr': str(error),
                'command': [str(a) for a in argv]}


def version(text):
    match = re.search(r'(?<!\d)(\d+\.\d+(?:\.\d+)*(?:-\d+)?)', text or '')
    return match.group(1) if match else None


def unique(paths):
    seen = set()
    for p in paths:
        if not p:
            continue
        path = Path(p).expanduser()
        # Do not resolve Python symlinks: their venv prefix is part of the environment.
        key = os.path.abspath(path)
        if key not in seen:
            seen.add(key)
            yield path


def python_paths(args):
    home = Path.home()
    explicit = [sys.executable, *getattr(args, 'python_env', [])]
    for key in ('FRAMECORE_MANIM_PYTHON', 'FRAMECORE_BLENDER_PYTHON'):
        explicit.append(os.environ.get(key))
    explicit += os.environ.get('FRAMECORE_PYTHON_ENVS', '').split(os.pathsep)
    paths = []
    prefix = Path(os.environ.get('FRAMECORE_MANIM_PREFIX', home / '.framecore-studio/runtimes/manim-0.22.0'))
    paths += [prefix / 'bin/python', prefix / 'Scripts/python.exe']
    roots = [Path(os.environ.get('FRAMECORE_MEDIA_HOME', home / '.cache/framecore-studio/media')),
             Path(args.workspace), Path(args.project), home / '.framecore-studio/environments']
    for root in roots:
        paths += [root / 'bin/python', root / 'Scripts/python.exe']
        for pattern in ('*/bin/python', '*/Scripts/python.exe', '*/.venv/bin/python'):
            paths += sorted(root.glob(pattern))
    # Explicit paths must be probed even if missing; do not silently discard evidence.
    return list(unique([*explicit, *(p for p in paths if p.is_file())]))


PYTHON_PROBE = r'''
import ctypes,ctypes.util,importlib,importlib.metadata as md,json,os,platform,sys
tools=json.loads(sys.argv[1]); out={'python':platform.python_version(),'executable':sys.executable,'prefix':sys.prefix,'modules':{},'libraries':{}}
for t in tools:
    if t['kind']!='python_module' and not t.get('python_alternative'): continue
    module=t.get('module') or t['python_alternative']['module']
    names=t.get('packages') or [t['python_alternative']['package']]
    item={'present':False,'version':None,'distribution':None}
    for name in names:
        try: item.update(present=True,version=md.version(name),distribution=name);break
        except md.PackageNotFoundError: pass
    try:
        m=importlib.import_module(module);item.update(present=True,import_ok=True,path=getattr(m,'__file__',None))
        if not item['version']: item['version']=str(getattr(m,'__version__','')) or None
        if t['id']=='imageio_ffmpeg': item['ffmpeg_path']=m.get_ffmpeg_exe()
        if t['id']=='blender': item['runtime_version']=m.app.version_string
    except Exception as e: item.update(import_ok=False,error=type(e).__name__+': '+str(e))
    out['modules'][t['id']]=item
for name,symbol in [('cairo','cairo_version_string'),('pango-1.0','pango_version_string')]:
    try:
        path=ctypes.util.find_library(name)
        if not path: raise OSError('shared library not found')
        lib=ctypes.CDLL(path);f=getattr(lib,symbol);f.restype=ctypes.c_char_p
        out['libraries'][name]={'present':True,'path':path,'version':f().decode()}
    except Exception as e: out['libraries'][name]={'present':False,'error':str(e)}
print('FRAMECORE_PROBE='+json.dumps(out))
'''


def python_probe(path, tools):
    env = os.environ.copy()
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env['IMAGEIO_NO_INTERNET'] = '1'
    # Import only: no model constructors, synthesis, rendering or inference.
    result = execute([path, '-B', '-c', PYTHON_PROBE, json.dumps(tools)], timeout=45, env=env)
    for line in reversed(result['stdout'].splitlines()):
        if line.startswith('FRAMECORE_PROBE='):
            try:
                value = json.loads(line.split('=', 1)[1])
                value['requested_path'] = str(path)
                return value
            except ValueError:
                break
    return {'requested_path': str(path), 'error': result['stderr'] or 'interpreter probe did not finish',
            'modules': {}, 'libraries': {}}


def node_roots(args):
    paths = list(getattr(args, 'node_root', []))
    for key in ('FRAMECORE_NODE_MODULES', 'NODE_PATH', 'CODEX_PRIMARY_RUNTIME_NODE_MODULES'):
        paths += os.environ.get(key, '').split(os.pathsep)
    paths += [Path(args.project) / 'node_modules', Path(args.workspace) / 'node_modules']
    paths += sorted(Path(args.workspace).glob('*/node_modules'))
    cache = Path.home() / '.cache/framecore-studio/motion'
    paths += sorted(cache.glob('*/node_modules'))
    if os.environ.get('FRAMECORE_MOTION_HOME'):
        paths.append(Path(os.environ['FRAMECORE_MOTION_HOME']) / 'node_modules')
    npm = shutil.which('npm')
    if npm:
        out = execute([npm, 'root', '-g'], timeout=10)
        if out['exit_code'] == 0:
            paths += out['stdout'].strip().splitlines()[-1:]
    return [p for p in unique(paths) if p.is_dir()]


def installed(version=None, path=None, evidence=None, **more):
    return dict(status='ok', version=version, path=str(path) if path else None,
                evidence=evidence, **more)


def absent(status='missing', note=None, **more):
    result = dict(status=status, version=None, path=None, note=note)
    result.update(more)
    return result


def probe_python(tool, interpreters):
    hits = [(p, p.get('modules', {}).get(tool['id'], {})) for p in interpreters]
    if tool.get('role') in ('manim', 'blender'):
        role = tool['role']
        hits.sort(key=lambda hit: not hit[0].get('modules', {}).get(role, {}).get('import_ok'))
    for p, item in hits:
        if item.get('import_ok'):
            return installed(item.get('version'), item.get('path'), 'distribution metadata and real import',
                             interpreter=p['requested_path'], environment=p['prefix'],
                             runtime_version=item.get('runtime_version'), ffmpeg_path=item.get('ffmpeg_path'))
    broken = [(p, item) for p, item in hits if item.get('present')]
    if broken:
        p, item = broken[0]
        return absent('broken', item.get('error'), interpreter=p['requested_path'])
    if any(p.get('error') for p in interpreters):
        return absent('unknown', 'One or more interpreter probes failed; absence is not confirmed.')
    return absent(note='Not importable in any inspected Python environment.')


def npm_entries(data):
    """Declared runtime entry points, excluding type declarations and subpath-only exports."""
    def strings(value):
        if isinstance(value, str):
            return [value]
        if isinstance(value, list):
            return [entry for child in value for entry in strings(child)]
        if isinstance(value, dict):
            return [entry for key, child in value.items() if key != 'types' for entry in strings(child)]
        return []
    exports = data.get('exports', {})
    if isinstance(exports, dict) and any(key.startswith('.') for key in exports):
        exports = exports.get('.', {})
    entries = [entry for field in ('main', 'module', 'bin') for entry in strings(data.get(field))]
    entries += strings(exports)
    return [p for p in entries if '*' not in p and not p.endswith(('.d.ts', 'package.json'))] or ['index.js']


def probe_npm(tool, roots):
    errors, candidates = [], []
    for root in roots:
        package = root / tool['package'] / 'package.json'
        if not package.is_file():
            continue
        try:
            data = load(package)
            if data.get('name') != tool['package'] or not data.get('version'):
                raise ValueError('invalid package identity/version')
            base = package.parent.resolve()
            entries = [(base / name).resolve() for name in npm_entries(data)]
            if not any(p.is_relative_to(base) and p.is_file() for p in entries):
                raise ValueError('declared runtime entry point is missing')
            bins = data.get('bin', {})
            bins = [bins] if isinstance(bins, str) else list(bins.values())
            if any(not (base / name).resolve().is_relative_to(base) or not (base / name).is_file() for name in bins):
                raise ValueError('declared CLI executable is missing')
            candidates.append(installed(data['version'], package.parent, 'package identity, version and executable/library payload',
                             runtime_test='NOT_RUN; installation check, not a render or browser import'))
        except (OSError, ValueError) as error:
            errors.append(str(error))
    if candidates:
        selected = next((c for c in candidates if c['version'] == tool.get('reported_version')), candidates[0])
        selected['other_installations'] = [{'version': c['version'], 'path': c['path']} for c in candidates if c is not selected]
        return selected
    return absent('broken' if errors else 'missing', '; '.join(errors) or 'No installed npm package in the inspected roots.')


def binary_paths(tool, interpreters):
    paths = [shutil.which(name) for name in tool['commands']]
    if tool['id'] == 'micromamba':
        paths += [os.environ.get('MAMBA_EXE'), Path.home() / '.local/bin/micromamba',
                  Path.home() / 'micromamba/bin/micromamba',
                  Path.home() / '.framecore-studio/toolchains/micromamba/bin/micromamba']
        paths += list((Path.home() / '.cache/framecore-studio').glob('**/micromamba'))
    for p in interpreters:
        if not p.get('prefix'):
            continue
        root = Path(p['prefix'])
        for name in tool['commands']:
            paths += [root / 'bin' / name, root / 'Scripts' / (name + '.exe')]
        if tool['id'] in ('autoeditor', 'deepfilter'):
            folder, name = ('auto-editor', 'auto-editor') if tool['id'] == 'autoeditor' else ('deepfilter', 'deep-filter')
            paths.append(root / 'share' / folder / name)
    return [p for p in unique(paths) if p.is_file()]


def probe_binary(tool, paths):
    failures = []
    for path in paths:
        # Exclude Windows' unrelated filesystem convert.exe from ImageMagick discovery.
        result = execute([path, *tool.get('version_args', ['--version'])])
        text = result['stdout'] + result['stderr']
        if result['exit_code'] == 0 and (tool['id'] != 'imagemagick' or 'ImageMagick' in text):
            return installed(version(text), path, 'local executable version command',
                             version_output=text.strip()[:400])
        failures.append({'path': str(path), 'exit_code': result['exit_code'], 'error': result['stderr']})
    return absent('broken' if failures else 'missing', 'Version command failed.' if failures else 'Executable not found.', attempts=failures)


def probe_model(tool, interpreters):
    paths = [os.environ.get(tool['env'])]
    for p in interpreters:
        if p.get('prefix'):
            root = Path(p['prefix'])
            paths.append(root / 'share' / ('whisper' if tool['id'] == 'whisper_tiny' else 'tessdata') / tool['filename'])
    if tool['id'] == 'whisper_tiny':
        paths += [Path.home() / '.cache/whisper/ggml-tiny.bin', Path.home() / '.local/share/pywhispercpp/models/ggml-tiny.bin']
    else:
        paths += [Path(os.environ.get('TESSDATA_PREFIX', '/usr/share/tesseract-ocr/5/tessdata')) / tool['filename']]
        paths += list(Path('/usr/share/tesseract-ocr').glob('*/tessdata/pol.traineddata'))
    other = []
    for path in unique(paths):
        if not path.is_file():
            continue
        hasher = hashlib.sha256()
        with path.open('rb') as handle:
            for block in iter(lambda: handle.read(1024 * 1024), b''):
                hasher.update(block)
        digest = hasher.hexdigest()
        if digest == tool['sha256']:
            return installed(tool['reported_version'], path, 'model SHA-256 matches pinned public asset', sha256=digest)
        other.append({'path': str(path), 'sha256': digest})
    uncertain = other or any(p.get('error') for p in interpreters)
    return absent('unknown' if uncertain else 'missing', 'Model identity or an environment could not be verified; preserve existing assets.' if uncertain else 'Required model asset is absent.', other_assets=other)


def browser_paths(tool, args, npm_results):
    if tool['id'] == 'browser_animate':
        paths = [os.environ.get('FRAMECORE_ANIMATE_BROWSER')]
        node, pw = shutil.which('node'), npm_results.get('playwright', {})
        if node and pw.get('path'):
            out = execute([node, '-e', 'console.log(require(process.argv[1]).chromium.executablePath())', pw['path']], timeout=10)
            if out['exit_code'] == 0:
                paths += out['stdout'].strip().splitlines()[-1:]
        roots = [Path(os.environ.get('PLAYWRIGHT_BROWSERS_PATH', Path.home() / '.cache/ms-playwright'))]
    else:
        paths = [args.browser, os.environ.get('CHROME_PATH'), os.environ.get('HYPERFRAMES_BROWSER_PATH')]
        paths += [shutil.which(n) for n in ('chromium', 'chromium-browser', 'google-chrome', 'chrome-headless-shell')]
        roots = [Path.home() / '.cache/hyperframes/chrome', Path.home() / '.cache/puppeteer', Path.home() / '.cache/ms-playwright']
        paths += ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', r'C:\Program Files\Google\Chrome\Application\chrome.exe']
    for root in roots:
        for pattern in ('**/chrome-headless-shell', '**/headless_shell', '**/chrome', '**/chrome.exe'):
            paths += sorted(root.glob(pattern))[:20]
    return [p for p in unique(paths) if p.is_file()]


def probe_animate(args):
    root = Path(os.environ.get('FRAMECORE_ANIMATE_ROOT', Path(args.workspace) / 'animate-engine')).expanduser()
    if not root.is_dir():
        return absent(note='Installed Animate engine source directory not found.')
    try:
        source = load(PLUGIN / 'integrations/animate/source-manifest.json')
        for entry in source['bundled_files']:
            p = root / entry['path']
            blob = p.read_bytes()
            if hashlib.sha1(b'blob ' + str(len(blob)).encode() + b'\0' + blob).hexdigest() != entry['git_blob_sha']:
                return absent('unknown', 'Engine source differs from the pinned source; preserve edits.', path=str(root))
        return installed(source['source_version'], root, 'installed engine files match pinned upstream source', runtime_test='NOT_RUN; driver and browser checked separately')
    except (OSError, ValueError, KeyError) as error:
        return absent('broken', str(error))


def probe(tool, args, interpreters, roots, npm_results):
    kind = tool['kind']
    if kind == 'python_module':
        return probe_python(tool, interpreters)
    if kind == 'npm':
        return npm_results[tool['id']]
    if kind == 'python':
        role = tool['role']
        module = {'manim': 'manim', 'blender': 'blender'}.get(role)
        candidates = [p for p in interpreters if p.get('python') and (role == 'active' or p.get('modules', {}).get(module, {}).get('import_ok'))]
        if candidates:
            p = candidates[0]
            return installed(p['python'], p['requested_path'], 'interpreter executed; role tied to the imported engine' if module else 'active interpreter executed')
        return absent('unknown' if any(p.get('error') for p in interpreters) else 'missing', 'No verified interpreter for this role.')
    if kind == 'binary':
        result = probe_binary(tool, binary_paths(tool, interpreters))
        if result['status'] != 'ok' and tool.get('python_alternative'):
            alternate = probe_python(tool, interpreters)
            if alternate['status'] == 'ok':
                return alternate
        return result
    if kind == 'library':
        for p in interpreters:
            item = p.get('libraries', {}).get(tool['library'], {})
            if item.get('present'):
                return installed(item.get('version'), item.get('path'), 'shared library loaded and version function called', interpreter=p['requested_path'])
        return absent('unknown' if any(p.get('error') for p in interpreters) else 'missing',
                      'Shared library did not load in an inspected environment.')
    if kind == 'model':
        return probe_model(tool, interpreters)
    if kind == 'ffmpeg_fallback':
        paths = [p.get('modules', {}).get('imageio_ffmpeg', {}).get('ffmpeg_path') for p in interpreters]
        paths = [p for p in paths if p]
        if paths:
            return probe_binary({'id': tool['id'], 'version_args': ['-version']}, paths)
        return absent('unknown' if any(p.get('error') for p in interpreters) else 'missing',
                      'imageio-ffmpeg did not expose a verified bundled executable.')
    if kind == 'browser':
        return probe_binary(tool, browser_paths(tool, args, npm_results))
    if kind == 'animate':
        return probe_animate(args)
    return absent('unknown', 'No implemented probe for this kind.')


def installation_plan(results, catalog):
    steps = []
    for tool, result in zip(catalog, results):
        if result['status'] == 'ok':
            continue
        action = 'install' if result['status'] == 'missing' else 'repair' if result['status'] == 'broken' else 'verify'
        steps.append({'id': tool['id'], 'label': tool['label'], 'action': action,
                      'reported_version': tool['reported_version'], 'reason': result.get('note'),
                      'recipe': tool['install'], 'state': 'planned; not executed'})
    return steps


def report(args, host=None, detected_by=None):
    catalog = load(HERE / 'runtime-tools.json')
    tools = catalog['tools']
    paths = python_paths(args)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        interpreters = list(pool.map(lambda p: python_probe(p, tools), paths))
    roots = node_roots(args)
    npm_results = {t['id']: probe_npm(t, roots) for t in tools if t['kind'] == 'npm'}
    results = []
    for tool in tools:
        try:
            result = probe(tool, args, interpreters, roots, npm_results)
        except (OSError, ValueError, KeyError, TypeError) as error:
            result = absent('unknown', 'Probe error: ' + str(error))
        result.update(id=tool['id'], label=tool['label'], reported_version=tool['reported_version'])
        result['version_comparison'] = ('not_specified' if not tool['reported_version'] else
            'unknown' if not result.get('version') else 'matches_reported' if result['version'] == tool['reported_version'] else 'different; no automatic replacement')
        results.append(result)
    # A package version mismatch is informational; inconsistent Remotion peers need review.
    remotion = [r for r in results if r['id'] in ('remotion', 'remotion_cli', 'remotion_renderer', 'remotion_three') and r['status'] == 'ok']
    compatibility = []
    if len({r['version'] for r in remotion}) > 1:
        compatibility.append({'id': 'remotion_family', 'status': 'unknown', 'reason': 'Remotion packages have different versions; check each project lockfile, do not silently upgrade.'})
    failing = [{'id': r['id'], 'status': r['status']} for r in results if r['status'] in UNUSABLE] + compatibility
    verdict = 'unknown_host' if not host else ('limited' if host in ('chatgpt', 'chatgpt_work', 'claude_apps') else 'fail') if failing else 'pass'
    return {'schema_version': 1, 'inventory': 'installation_and_update', 'mode': 'update' if args.update else 'final',
            'host': host, 'host_detected_by': detected_by, 'reference_basis': catalog['reference_basis'],
            'reported_at': catalog['reported_at'], 'tools': results, 'compatibility': compatibility,
            'final': {'verdict': verdict, 'failing': failing},
            'installation_plan': installation_plan(results, tools),
            'inspected_python_environments': [{'path': p['requested_path'], 'version': p.get('python'), 'error': p.get('error')} for p in interpreters],
            'inspected_node_roots': [str(p) for p in roots], 'installs_nothing': True,
            'network_used': False, 'model_inference': 'NOT_RUN', 'render_tests': 'NOT_RUN'}


def text(data):
    lines = [f"Studio tool inventory: {data['host'] or 'Unknown'}; {data['mode']}",
             'Reference versions are owner-reported working versions, not required downgrades or newest releases.', '']
    for r in data['tools']:
        lines.append(f"{r['status']}: {r['label']} | detected {r.get('version') or 'Unknown'} | reported {r['reported_version'] or 'not specified'}")
        lines.append('  ' + (r.get('evidence') or r.get('note') or 'Unknown'))
        if r.get('path'):
            lines.append('  ' + r['path'])
    lines += ['', 'Planned installation or verification; nothing has been installed:']
    for step in data['installation_plan']:
        lines.append(f"- {step['action']}: {step['label']} ({step['reported_version'] or 'version not specified'}), environment: {step['recipe']['destination_role']}")
    if not data['installation_plan']:
        lines.append('None.')
    for item in data['compatibility']:
        lines.append('Compatibility review: ' + item['reason'])
    lines.append('FINAL: ' + data['final']['verdict'].upper())
    return '\n'.join(lines)
