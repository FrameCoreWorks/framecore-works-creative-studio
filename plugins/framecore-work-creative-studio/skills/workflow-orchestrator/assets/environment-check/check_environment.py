#!/usr/bin/env python3
"""Check which programs and libraries Studio's tools need are present in this environment, and how to install the rest.

  python3 check_environment.py [--online] [--json] [--project DIR] [--browser PATH] [--strict]

Reads tools.json (what to look for, minimum and newest known versions, install commands per platform) and the
capability card (which Studio capability needs what), then reports each tool as ok, behind (older than the newest
version), below_minimum, missing, per_project, not_installed (optional) or unknown, and which capabilities are ready.
--online reads the newest versions from PyPI, npm, nodejs.org, endoflife.date and Chromium's release feed instead of
the dated snapshot in tools.json. Nothing is ever installed or changed. Standard library only, so it runs wherever
Python does (Codex, a local shell, ChatGPT's code execution). Exit code 0, or with --strict 1 when a required tool is
missing or below its minimum.
"""
import argparse
import glob
import importlib.util
import json
import os
import pathlib
import platform
import re
import shutil
import subprocess
import sys
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
PLUGIN_ROOT = HERE.parents[3]
CARD = HERE.parent / 'capability-card.json'
USABLE = ('ok', 'behind')
STUDIO_FINDS_BROWSER = 'Studio\'s frame review finds Chrome on PATH, in CHROME_PATH and in the standard app folders'


def load(path):
    with open(path, encoding='utf-8') as handle:
        return json.load(handle)


def system_name():
    name = platform.system().lower()
    return {'darwin': 'macos', 'windows': 'windows'}.get(name, 'linux' if name == 'linux' else name)


def version_of(text):
    match = re.search(r'(\d+(?:\.\d+)+)', text or '')
    return match.group(1) if match else None


def as_tuple(version):
    return tuple(int(part) for part in re.findall(r'\d+', version or '')[:4])


def older(version, than):
    return bool(version and than) and as_tuple(version) < as_tuple(than)


def run(command, timeout=15):
    try:
        done = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.SubprocessError):
        return None
    return (done.stdout or '') + (done.stderr or '') if done.returncode == 0 else None


def fetch_json(url, timeout=10):
    request = urllib.request.Request(url, headers={'User-Agent': 'framecore-studio-environment-check', 'Accept': 'application/json'})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode('utf-8'))


def latest_online(source):
    """The newest version from the source named in tools.json, or None when it cannot be read."""
    kind, _, name = source.partition(':')
    try:
        if kind == 'pypi':
            return fetch_json(f'https://pypi.org/pypi/{name}/json')['info']['version']
        if kind == 'npm':
            return fetch_json(f'https://registry.npmjs.org/{name}/latest')['version']
        if kind == 'endoflife':
            return fetch_json(f'https://endoflife.date/api/{name}.json')[0]['latest']
        if kind == 'nodejs':
            return next(item['version'].lstrip('v') for item in fetch_json('https://nodejs.org/dist/index.json') if item.get('lts'))
        if kind == 'chromium':
            return fetch_json('https://chromiumdash.appspot.com/fetch_releases?channel=Stable&platform=Linux&num=1')[0]['version']
    except Exception:  # any network or format problem means the newest version is unknown, not an error
        return None
    return None


def python_module_version(tool):
    if importlib.util.find_spec(tool['module']) is None:
        return None, None
    try:
        from importlib import metadata
        return metadata.version(tool['package']), None
    except Exception:
        return 'unknown', None


def check_binary(tool):
    for command in tool['commands']:
        path = shutil.which(command)
        if path:
            output = run([path, *tool.get('version_args', ['--version'])])
            return version_of(output) or 'unknown', path, None
    fallback = tool.get('python_fallback')
    if fallback and importlib.util.find_spec(fallback) is not None:
        try:
            module = __import__(fallback)
            path = module.get_ffmpeg_exe()
            return version_of(run([path, '-version'])) or 'unknown', path, f'bundled by the Python package {fallback}; the renderer uses it, other tools need ffmpeg on PATH'
        except Exception:
            pass
    return None, None, None


def browser_candidates(explicit):
    """(path, found_where) pairs: the places Studio's frame review looks first, then other usual installs."""
    names = ['google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser', 'chrome']
    studio = [explicit, os.environ.get('CHROME_PATH')]
    studio += [shutil.which(name) for name in names]
    studio += ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/Applications/Chromium.app/Contents/MacOS/Chromium',
               'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe']
    other = [os.environ.get('MOTION_REVIEW_BROWSER'), 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe']
    local = os.environ.get('LOCALAPPDATA')
    if local:
        other.append(os.path.join(local, 'Google', 'Chrome', 'Application', 'chrome.exe'))
    roots = [os.environ.get('PLAYWRIGHT_BROWSERS_PATH'), os.path.expanduser('~/.cache/ms-playwright'),
             os.path.expanduser('~/Library/Caches/ms-playwright'), os.path.join(local, 'ms-playwright') if local else None]
    for root in filter(None, roots):
        for pattern in ('chromium-*/chrome-linux*/chrome', 'chromium-*/chrome-win*/chrome.exe',
                        'chromium-*/chrome-mac*/Chromium.app/Contents/MacOS/Chromium', 'chrome/*/chrome-*/chrome'):
            other += sorted(glob.glob(os.path.join(root, pattern)), reverse=True)
    seen = set()
    for where, paths in (('studio', studio), ('other', other)):
        for path in paths:
            if path and path not in seen and os.path.isfile(path):
                seen.add(path)
                yield path, where


def check_browser(tool, explicit):
    for path, where in browser_candidates(explicit):
        version = version_of(run([path, '--version'], timeout=20)) or 'unknown'
        note = None if where == 'studio' else f'found outside the usual places; pass --browser "{path}" or set CHROME_PATH to it ({STUDIO_FINDS_BROWSER})'
        return version, path, note
    return None, None, None


def check_node_package(tool, project):
    pinned = None
    pin_file = PLUGIN_ROOT / tool['pinned_by']
    if pin_file.is_file():
        manifest = load(pin_file)
        pinned = {**manifest.get('devDependencies', {}), **manifest.get('dependencies', {})}.get(tool['package'])
    installed = pathlib.Path(project, 'node_modules', tool['package'], 'package.json')
    if installed.is_file():
        return load(installed).get('version', 'unknown'), str(installed.parent), pinned
    return None, None, pinned


def skill_dirs(project):
    home = pathlib.Path.home()
    codex = pathlib.Path(os.environ.get('CODEX_HOME', home / '.codex'))
    config = pathlib.Path(os.environ.get('XDG_CONFIG_HOME', home / '.config'))
    return [home / '.agents' / 'skills', codex / 'skills', home / '.claude' / 'skills', config / 'agents' / 'skills',
            pathlib.Path(project) / '.agents' / 'skills', pathlib.Path(project) / '.claude' / 'skills',
            pathlib.Path(project) / '.codex' / 'skills']


def check_hyperframes(tool, project):
    found = []
    for folder in skill_dirs(project):
        if folder.is_dir():
            found += sorted(str(p.parent) for p in folder.glob('hyperframes*/SKILL.md'))
    for plugins in (pathlib.Path.home() / '.claude' / 'plugins', pathlib.Path(os.environ.get('CODEX_HOME', pathlib.Path.home() / '.codex')) / 'plugins'):
        if plugins.is_dir():
            found += sorted(str(p) for p in plugins.glob('**/hyperframes*') if p.is_dir() and len(p.relative_to(plugins).parts) <= 3)
    version, path = None, shutil.which('hyperframes')
    if path:
        version = version_of(run([path, '--version'], timeout=30))
    elif shutil.which('npx'):
        output = run([shutil.which('npx'), '--no-install', 'hyperframes', '--version'], timeout=60)
        version, path = version_of(output), ('npx cache' if output else None)
    return version, path, found


def check_tool(tool, args, latest):
    result = {'id': tool['id'], 'label': tool['label'], 'optional': bool(tool.get('optional')), 'minimum': tool.get('minimum'),
              'latest': latest, 'version': None, 'path': None, 'note': None}
    kind = tool['kind']
    if kind == 'python':
        result['version'], result['path'] = platform.python_version(), sys.executable
    elif kind == 'python_module':
        result['version'], result['note'] = python_module_version(tool)
    elif kind == 'binary':
        result['version'], result['path'], result['note'] = check_binary(tool)
    elif kind == 'browser':
        result['version'], result['path'], result['note'] = check_browser(tool, args.browser)
    elif kind == 'node_package':
        result['version'], result['path'], pinned = check_node_package(tool, args.project)
        result['pinned'] = pinned
        if not result['version']:
            result['status'] = 'per_project'
            result['note'] = f'installed per project with npm install; Studio\'s starter pins {pinned}' if pinned else 'installed per project with npm install'
            return result
    elif kind == 'hyperframes':
        result['version'], result['path'], skills = check_hyperframes(tool, args.project)
        result['skills'] = skills
        if not result['version'] and not skills:
            result['status'] = 'not_installed'
            return result
        if not result['version']:
            result['status'], result['note'] = 'ok', 'skills found; the CLI runs through npx when a task needs it'
            return result
    if not result['version']:
        result['status'] = 'not_installed' if result['optional'] else 'missing'
    elif result['version'] != 'unknown' and older(result['version'], tool.get('minimum')):
        result['status'] = 'below_minimum'
    elif result['version'] != 'unknown' and older(result['version'], latest):
        result['status'] = 'behind'
    else:
        result['status'] = 'ok'
    return result


def requirement_state(tools, results, network):
    """True, False or None (cannot be checked here) for every requirement value of the capability card."""
    state = {'python': True, 'none': True, 'network': network, 'host_tool': None, 'user_browser': None}
    for tool in tools:
        need = tool.get('requirement')
        if not need or tool.get('optional'):
            continue
        usable = results[tool['id']]['status'] in USABLE
        state[need] = usable if state.get(need) is None else state[need] and usable
    return state


def capability_state(card, tools, results, state):
    extra = {tool['capability']: tool['id'] for tool in tools if tool.get('capability')}
    out = []
    for item in card['capabilities']:
        if item['executed_by'] == 'host' or not item.get('hosts'):
            continue
        missing = [need for need in item.get('requires', []) if state.get(need) is False]
        unknown = [need for need in item.get('requires', []) if state.get(need) is None]
        without = [need for need in item.get('optional', []) if state.get(need) is False]
        note = None
        if item['id'] in extra:
            linked = results[extra[item['id']]]
            if linked['status'] == 'not_installed':
                missing.append(extra[item['id']])
            elif linked['status'] == 'per_project':
                note = linked['note']
        if item['id'] == 'hyperframes_engine' and older(results['node']['version'], '22'):
            missing.append('node>=22')
        if 'browser' in item.get('requires', []) and results['browser']['status'] in USABLE and results['browser']['note']:
            note = ', '.join(filter(None, [note, 'give the tool --browser or CHROME_PATH']))
        status = 'missing' if missing else 'unknown' if unknown else 'ready'
        out.append({'id': item['id'], 'owner': item['owner'], 'status': status, 'missing': missing, 'not_checked': unknown,
                    'reduced_without': without, 'when_missing': item['when_missing'] if missing else None, 'note': note})
    return out


def install_steps(tools, results, system):
    steps = []
    for tool in tools:
        result = results[tool['id']]
        if result['status'] not in ('missing', 'below_minimum', 'behind', 'not_installed'):
            continue
        hints = tool['install']
        command = hints.get(system) or hints.get('any')
        if result['status'] == 'behind' and tool['kind'] == 'python_module':
            command = f'python3 -m pip install --user --upgrade {tool["package"]}'
        action = 'update' if result['status'] in ('behind', 'below_minimum') else 'install'
        steps.append({'id': tool['id'], 'action': action, 'optional': result['optional'], 'below': result['status'] == 'below_minimum', 'command': command,
                      'more': hints.get('any') if command != hints.get('any') else None})
    return steps


def report(args):
    spec, card = load(HERE / 'tools.json'), load(CARD)
    system = system_name()
    latest, network = {}, None
    for tool in spec['tools']:
        latest[tool['id']] = tool.get('known_latest')
        if args.online and tool.get('latest_source'):
            value = latest_online(tool['latest_source'])
            if value:
                latest[tool['id']], network = value, True
            elif network is None:
                network = False
    results = {tool['id']: check_tool(tool, args, latest[tool['id']]) for tool in spec['tools']}
    state = requirement_state(spec['tools'], results, network)
    return {
        'checked': spec['checked'],
        'latest_from': 'online' if network else f'snapshot of {spec["checked"]}' + (' (online lookup failed)' if args.online else ''),
        'system': system, 'platform': platform.platform(), 'python': sys.executable, 'project': os.path.abspath(args.project),
        'tools': list(results.values()),
        'requirements': state,
        'capabilities': capability_state(card, spec['tools'], results, state),
        'install': install_steps(spec['tools'], results, system),
        'installs_nothing': True,
    }


def text(data):
    lines = [f'Studio environment check ({data["system"]}, newest versions: {data["latest_from"]})', '']
    for tool in data['tools']:
        version = tool['version'] or '-'
        extra = f' (newest {tool["latest"]})' if tool['status'] == 'behind' else f' (needs {tool["minimum"]})' if tool['status'] == 'below_minimum' else ''
        lines.append(f'  {tool["status"]:<14} {tool["label"]}: {version}{extra}' + (f' [{tool["path"]}]' if tool['path'] else ''))
        if tool.get('note'):
            lines.append(f'  {"":<14} {tool["note"]}')
    lines += ['', 'Capabilities:']
    for item in data['capabilities']:
        detail = ', '.join(filter(None, [
            'missing ' + ', '.join(item['missing']) if item['missing'] else '',
            'not checked here: ' + ', '.join(item['not_checked']) if item['not_checked'] else '',
            'reduced without ' + ', '.join(item['reduced_without']) if item['reduced_without'] else '',
            item['note'] or '']))
        lines.append(f'  {item["status"]:<8} {item["id"]}' + (f' ({detail})' if detail else ''))
    groups = [('Needed (nothing was installed; ask Studio to run a step, or run it yourself):', lambda s: not s['optional'] and s['action'] == 'install' or s['below']),
              ('Optional:', lambda s: s['optional'] and s['action'] == 'install'),
              ('Newer versions available (the current ones work):', lambda s: s['action'] == 'update' and not s['below'])]
    for title, belongs in groups:
        steps = [step for step in data['install'] if belongs(step)]
        if steps:
            lines += ['', title]
        for step in steps:
            lines.append(f'  {step["id"]}: {step["command"]}')
            if step['more']:
                lines.append(f'      also: {step["more"]}')
    if not data['install']:
        lines += ['', 'Nothing to install or update.']
    return '\n'.join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description='Check the programs and libraries Studio uses; installs nothing.')
    parser.add_argument('--online', action='store_true', help='read the newest versions from their registries')
    parser.add_argument('--json', action='store_true', help='print the report as JSON')
    parser.add_argument('--project', default='.', help='project folder for per-project packages and skills (default: current folder)')
    parser.add_argument('--browser', help='path to Chrome or Chromium to check')
    parser.add_argument('--strict', action='store_true', help='exit 1 when a required tool is missing or below its minimum')
    args = parser.parse_args(argv)
    data = report(args)
    print(json.dumps(data, indent=2, ensure_ascii=False) if args.json else text(data))
    failed = [tool for tool in data['tools'] if not tool['optional'] and tool['status'] in ('missing', 'below_minimum')]
    return 1 if args.strict and failed else 0


if __name__ == '__main__':
    sys.exit(main())
