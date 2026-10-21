"""Durable local jobs; cooperative cancellation owns no unrelated processes."""
import os
import socket
import subprocess
import sys
import time
import uuid
import threading
from pathlib import Path
from fc_core import (FrameCutError, atomic_json, confined, fingerprint, identifier, integer,
                     keys, read_json, require, validate)

_CURRENT = None
_LAST_WRITE = 0.0


def process_token(pid):
    try:
        # Linux starttime distinguishes PID reuse. Other hosts use cooperative heartbeat only.
        text = Path(f'/proc/{pid}/stat').read_text()
        return text[text.rfind(')')+2:].split()[19]
    except (OSError, IndexError):
        return None


def folder(root, project_id, job_id):
    return confined(root, f'.framecut/{identifier(project_id)}/jobs/{identifier(job_id)}')


def active():
    return _CURRENT is not None


def checkpoint(stage=None, frame=None, total=None, force=False, unit='frames'):
    global _LAST_WRITE
    if _CURRENT is None:
        return
    directory, state = _CURRENT
    if (directory/'cancel.json').exists():
        raise FrameCutError('cancelled', 'Job cancelled; no incomplete final is published')
    now = time.monotonic()
    if not force and stage is None and now-_LAST_WRITE < .5:
        return
    if stage is not None:
        state['stage'] = stage
        for key in ('frame', 'total_frames', 'processed', 'total', 'progress_unit'): state.pop(key, None)
    if frame is not None:
        state['processed'] = frame
        state['progress_unit'] = unit
        if unit == 'frames': state['frame'] = frame
    if total is not None:
        state['total'] = total
        if unit == 'frames': state['total_frames'] = total
    state['heartbeat'] = time.time()
    atomic_json(directory/'state.json', state, overwrite=True)
    _LAST_WRITE = now


def status(root, project_id, job_id):
    directory = folder(root, project_id, job_id)
    state = read_json(directory/'state.json')
    if state['status'] in ('queued', 'running') and state.get('host') == socket.gethostname():
        token = state.get('process_token')
        if token is not None and process_token(state['pid']) != token:
            state.update(status='interrupted', finished=time.time(), error={'code': 'interrupted', 'message': 'Worker exited before recording completion'})
            atomic_json(directory/'state.json', state, overwrite=True)
    return state


def cancel(root, project_id, job_id):
    state = status(root, project_id, job_id)
    if state['status'] in ('queued', 'running'):
        directory = folder(root, project_id, job_id)
        if not (directory/'cancel.json').exists():
            atomic_json(directory/'cancel.json', {'requested': time.time()})
        return {**state, 'cancellation_requested': True}
    return state


def validate_request(request):
    keys(request, ('kind', 'deliverable', 'out', 'mode', 'timeout', 'max_disk_mb', 'panels'), ('kind', 'deliverable', 'out'))
    require(request['kind'] in ('render', 'storyboard'), 'Unknown job kind')
    identifier(request['deliverable'])
    require(request.get('mode', 'preview') in ('preview', 'final'), 'Unknown render mode')
    integer(request.get('timeout', 600), 'timeout', 1, 7200)
    integer(request.get('max_disk_mb', 2048), 'disk budget', 64, 102400)
    return request


def start(project_path, request, previous=None):
    path = Path(project_path).absolute()
    require(not path.is_symlink() and path.parent.resolve() == path.parent, 'Project symlink rejected')
    project = read_json(path)
    validate(project, path.parent, True)
    validate_request(request)
    require(not confined(path.parent, request['out']).exists(), 'Job output already exists')
    job_id = 'job-' + uuid.uuid4().hex
    directory = folder(path.parent, project['id'], job_id)
    directory.mkdir(parents=True)
    atomic_json(directory/'project.json', project)
    atomic_json(directory/'request.json', request)
    state = {'schema_version': 1, 'id': job_id, 'project': project['id'], 'project_revision': project['revision'],
             'project_hash': fingerprint(project), 'request': request, 'status': 'queued', 'created': time.time(),
             'stage': 'queued', 'host': socket.gethostname(), 'resumes': previous}
    atomic_json(directory/'state.json', state)
    with (directory/'worker.log').open('ab') as log:
        try:
            process = subprocess.Popen([sys.executable, str(Path(__file__).parent/'framecut.py'), 'job-worker', str(path), '--job', job_id],
                             stdin=subprocess.DEVNULL, stdout=log, stderr=log, start_new_session=(os.name == 'posix'))
            state.update(pid=process.pid, process_token=process_token(process.pid))
            atomic_json(directory/'state.json', state, overwrite=True)
            atomic_json(directory/'launch.json', {'ready': True})
            threading.Thread(target=process.wait, daemon=True).start()
        except OSError as error:
            state.update(status='failed', error={'code': 'worker_start_failed', 'message': str(error)})
            atomic_json(directory/'state.json', state, overwrite=True)
            raise
    return state


def resume(project_path, job_id):
    path = Path(project_path).absolute()
    current = read_json(path)
    state = status(path.parent, current['id'], job_id)
    require(state['status'] in ('failed', 'cancelled', 'interrupted'), 'Only a stopped unfinished job can resume')
    require(state['project_hash'] == fingerprint(current), 'Project changed; create a new job for the new revision', 'stale_revision')
    # Only recover a render lock known to belong to this stopped worker.
    lock = confined(path.parent, f'.framecut/{current["id"]}/render.lock')
    if lock.exists():
        owner = read_json(lock)
        require(owner.get('job') == job_id and state.get('process_token') is not None and
                process_token(state['pid']) != state['process_token'], 'Render lock owner is not proven stopped', 'busy')
        lock.unlink()
    return start(path, state['request'], previous=job_id)


def worker(project_path, job_id):
    global _CURRENT
    path = Path(project_path).absolute()
    current = read_json(path)
    directory = folder(path.parent, current['id'], job_id)
    deadline = time.monotonic()+5
    while not (directory/'launch.json').is_file():
        require(time.monotonic()<deadline, 'Worker launch was not completed', 'worker_start_failed')
        time.sleep(.02)
    from fc_core import project_lock
    with project_lock(directory/'worker'):
        state = read_json(directory/'state.json')
        require(state['status'] == 'queued', 'Worker already started', 'busy')
        project, request = read_json(directory/'project.json'), read_json(directory/'request.json')
        state.update(status='running', pid=os.getpid(), process_token=process_token(os.getpid()), started=time.time())
        _CURRENT = directory, state
        try:
            checkpoint('starting', force=True)
            require(fingerprint(project) == state['project_hash'] == fingerprint(current), 'Queued project changed before execution', 'stale_revision')
            if request['kind'] == 'render':
                from fc_render import render
                result = render(project, path.parent, request['deliverable'], request['out'], request.get('mode', 'preview'), request.get('timeout', 600), request.get('max_disk_mb', 2048))
            else:
                from fc_board import storyboard
                result = storyboard(project, path.parent, request['deliverable'], request['out'], request.get('panels'), request.get('timeout', 600))
            state.update(status='completed', result=result, stage='completed')
        except BaseException as error:
            state.update(status='cancelled' if getattr(error, 'code', None) == 'cancelled' or isinstance(error, KeyboardInterrupt) else 'failed',
                         error={'code': getattr(error, 'code', 'worker_failed'), 'message': str(error)})
        finally:
            state['finished'] = time.time()
            atomic_json(directory/'state.json', state, overwrite=True)
            _CURRENT = None
    return state


def job_identity():
    return _CURRENT[1]['id'] if _CURRENT else None
