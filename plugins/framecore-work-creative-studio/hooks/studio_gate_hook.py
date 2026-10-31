#!/usr/bin/env python3
"""Stop hook for Claude Code and Codex: the turn cannot end while a final file in an export/ folder lacks a current
PASS or user-waived report from skills/delivery-documentation/scripts/studio_gate.py.

It reads the hook event from stdin, looks for folders named `export` up to four levels below the session folder and
checks each deliverable file against its report. It never runs the media checks itself (the model does, with the
gate script) and never changes a file. An export folder counts when it already holds gate reports or a deliverable
changed in the last 12 hours, so old projects with an export folder stay quiet. After two blocks in a row it lets
the turn end with a visible warning instead of looping. Any internal error lets the turn end with a warning.
"""
import json
import os
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/delivery-documentation/scripts'))
import studio_gate  # noqa: E402

MAX_DEPTH = 4
MAX_DIRS = 4000
RECENT_SECONDS = 12 * 3600
MAX_BLOCKS = 2
SKIP_DIRS = {'node_modules', '.git', 'upstream', '__pycache__', 'venv', '.venv', 'dist', 'build', 'Library'}


def export_folders(start):
    seen = 0
    start = Path(start)
    for folder, dirs, _ in os.walk(start):
        depth = len(Path(folder).relative_to(start).parts)
        seen += 1
        if seen > MAX_DIRS:
            return
        if Path(folder).name == 'export':
            dirs[:] = []
            yield Path(folder)
            continue
        dirs[:] = [] if depth >= MAX_DEPTH else [d for d in dirs if not d.startswith('.') and d not in SKIP_DIRS]


def open_files(start, now=None):
    now = now or time.time()
    found = []
    for folder in export_folders(start):
        adopted = (folder / studio_gate.REPORT_DIR).is_dir()
        for path in studio_gate.deliverables(folder):
            if not adopted and now - path.stat().st_mtime > RECENT_SECONDS:
                continue
            state = studio_gate.file_state(path)
            if state not in ('PASS', 'WAIVED'):
                found.append((path, state))
    return found


def counter_file(session):
    base = os.environ.get('PLUGIN_DATA') or os.environ.get('CLAUDE_PLUGIN_DATA') or tempfile.gettempdir()
    safe = ''.join(c for c in str(session) if c.isalnum() or c in '-_')[:80] or 'session'
    return Path(base) / f'studio-gate-blocks-{safe}.txt'


def decide(event, now=None):
    """Returns the JSON object to print, or None to let the turn end silently."""
    found = open_files(event.get('cwd') or os.getcwd(), now)
    counter = counter_file(event.get('session_id'))
    if not found:
        counter.unlink(missing_ok=True)
        return None
    listing = '; '.join(f'{p} ({state})' for p, state in found[:12]) + (f'; and {len(found) - 12} more' if len(found) > 12 else '')
    blocks = int(counter.read_text()) if event.get('stop_hook_active') and counter.is_file() else 0
    if blocks >= MAX_BLOCKS:
        counter.unlink(missing_ok=True)
        return {'systemMessage': f'Studio delivery gate: NOT PASSED after {MAX_BLOCKS} attempts. Do not treat these files as delivered: {listing}'}
    counter.parent.mkdir(parents=True, exist_ok=True)
    counter.write_text(str(blocks + 1))
    script = ROOT / 'skills/delivery-documentation/scripts/studio_gate.py'
    return {'decision': 'block', 'reason': (
        f'Studio delivery gate: these final files have no current PASS report: {listing}. '
        f'Run `python3 "{script}" check <file>` (the brief\'s requirements go in gate.json next to export/), fix every FAIL '
        f'and run it again; a BLOCKED check needs its missing tool. Tell the user plainly what failed. Only if the user '
        f'explicitly accepts a failing file, record it with `python3 "{script}" waive <file> --reason "<their words>"`. '
        f'A file that is not a final deliverable belongs outside export/.')}


def main():
    try:
        raw = sys.stdin.read()
        event = json.loads(raw) if raw.strip() else {}
        output = decide(event)
    except Exception as error:  # a broken hook must never trap the session
        output = {'systemMessage': f'Studio delivery gate could not run ({type(error).__name__}: {error}); check export/ by hand.'}
    if output:
        print(json.dumps(output))
    return 0


if __name__ == '__main__':
    sys.exit(main())
