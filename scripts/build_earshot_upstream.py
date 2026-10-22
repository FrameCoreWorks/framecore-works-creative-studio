#!/usr/bin/env python3
"""Copy upstream Earshot's real-sound files into plugins/earshot-audio and write its upstream.json.

    python3 scripts/build_earshot_upstream.py <checkout of Leonxlnx/earshot at the pinned commit>

The checkout must be exactly the pinned commit and tree (runtime.py PIN). Every tracked file is hashed into
upstream.json, which runtime.py uses to verify the source before installing. Copied files are byte-identical; run
it again after a pin change, never edit the copies.
"""
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugins' / 'earshot-audio'
spec = importlib.util.spec_from_file_location('earshot_runtime', PLUGIN / 'scripts' / 'runtime.py')
runtime = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runtime)
# upstream folder -> plugin folder; the layout below real-sound/ stays upstream's so its <skill>/scripts paths hold
COPY = {'skills/real-sound/scripts': 'skills/earshot/real-sound/scripts',
        'skills/real-sound/references': 'skills/earshot/real-sound/references',
        'skills/real-sound/templates': 'skills/earshot/real-sound/templates'}
SINGLE = {'LICENSE': 'LICENSE'}


def git(checkout, *args):
    return subprocess.run(['git', '-C', str(checkout), *args], check=True, capture_output=True, text=True).stdout.strip()


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        raise SystemExit(__doc__)
    checkout = Path(argv[0]).resolve()
    head, tree = git(checkout, 'rev-parse', 'HEAD'), git(checkout, 'rev-parse', 'HEAD^{tree}')
    if (head, tree) != (runtime.PIN['commit'], runtime.PIN['tree']):
        raise SystemExit(f'checkout is {head} / {tree}, not the pin {runtime.PIN["commit"]} / {runtime.PIN["tree"]}')
    files = {path: hashlib.sha256((checkout / path).read_bytes()).hexdigest() for path in git(checkout, 'ls-files').splitlines()}
    copied = {}
    for source, target in COPY.items():
        shutil.rmtree(PLUGIN / target, ignore_errors=True)
        for path in sorted(p for p in files if p.startswith(source + '/')):
            out = PLUGIN / target / path[len(source) + 1:]
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(checkout / path, out)
            copied[out.relative_to(PLUGIN).as_posix()] = path
    for source, target in SINGLE.items():
        shutil.copyfile(checkout / source, PLUGIN / target)
        copied[target] = source
    manifest = {'repository': runtime.PIN['repository'], 'tag': runtime.PIN['tag'], 'commit': head, 'tree': tree,
                'license': 'MIT, Copyright (c) 2026 Leon Lin', 'files': files, 'copied': dict(sorted(copied.items()))}
    (PLUGIN / 'upstream.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print(f'{len(files)} upstream files hashed, {len(copied)} copied into {PLUGIN.relative_to(ROOT)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
