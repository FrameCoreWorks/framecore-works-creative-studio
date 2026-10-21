"""Small transactional edits and compact, stable-ID timeline inspection."""
import copy
from fc_core import (event_start, fingerprint, identifier, integer, keys, ratio, require)
from fc_time import trim_time

EDIT_OPERATIONS = {'split_clip', 'trim_clip', 'move_clip', 'remove_clip', 'freeze_frame',
                   'set_keyframes', 'set_speed_curve', 'set_effects', 'set_framing'}


def timeline_read(project, sequence_id=None):
    sequences = [s for s in project['sequences'] if sequence_id is None or s['id'] == sequence_id]
    require(sequences or sequence_id is None, 'Unknown sequence')
    return {'project': project['id'], 'revision': project['revision'], 'project_hash': fingerprint(project),
            'sequences': [{'id': s['id'], 'fps': s['fps'], 'duration': s['duration'],
                           'lanes': {lane: [{**{k: copy.deepcopy(e[k]) for k in ('id', 'asset', 'duration', 'source_in', 'speed', 'speed_curve', 'freeze', 'text', 'anchor') if k in e},
                                             'start': event_start(e, s), 'locked': e['id'] in project.get('locks', []),
                                             'animated': bool(e.get('keyframes')), 'effects': e.get('effects', [])}
                                            for e in sorted(s.get(lane, []), key=lambda e: (event_start(e, s), e['id']))]
                                     for lane in ('clips', 'audio', 'overlays', 'texts')}} for s in sequences]}


def change_impact(before, after):
    def events(p):
        return {(s['id'], lane, e['id']): (e, event_start(e, s)) for s in p['sequences']
                for lane in ('clips', 'audio', 'overlays', 'texts') for e in s.get(lane, [])}
    a, b = events(before), events(after)
    changes = []
    for key in sorted(a.keys() | b.keys()):
        if a.get(key) != b.get(key):
            changes.append({'sequence': key[0], 'lane': key[1], 'id': key[2],
                            'change': 'added' if key not in a else 'removed' if key not in b else 'changed',
                            'before_start': a[key][1] if key in a else None, 'after_start': b[key][1] if key in b else None})
    deliveries = sorted({d['id'] for d in before['deliverables']+after['deliverables'] if next((x for x in before['deliverables'] if x['id']==d['id']),None) != next((x for x in after['deliverables'] if x['id']==d['id']),None)})
    return {'events': changes, 'deliverables': deliveries, 'storyboard_review': 'Check affected panels against the accepted board',
            'before_hash': fingerprint(before), 'after_hash': fingerprint(after)}


def shift(seq, boundary, delta, excluded=()):
    """Ripple all absolute lanes. Crossing events need an explicit authored edit first."""
    for lane in ('clips', 'audio', 'overlays', 'texts'):
        for e in seq.get(lane, []):
            if e['id'] in excluded or 'anchor' in e:
                continue
            if e['start'] >= boundary:
                e['start'] += delta
            elif e['start'] < boundary < e['start'] + e['duration']:
                require(False, f"Ripple crosses {lane} event {e['id']}; split or explicitly revise it first", 'edit_conflict')
    seq['duration'] += delta


def copy_framing(project, seq, old_id, new_id):
    for d in project['deliverables']:
        if d['sequence'] == seq['id'] and old_id in d.get('framing', {}):
            d['framing'][new_id] = copy.deepcopy(d['framing'][old_id])


def split(project, seq, clip, offset, right_id):
    identifier(right_id)
    require(0 < offset < clip['duration'], 'Split must be inside the clip')
    require(not clip.get('transition'), 'Split a transition clip only after explicitly revising its transition', 'edit_conflict')
    fps, asset = ratio(seq['fps']), project['assets'][clip['asset']]
    left = trim_time(clip, 0, offset, asset, fps)
    right = trim_time(clip, offset, clip['duration'], asset, fps)
    right.update(id=right_id, start=clip['start'] + offset, transition=0)
    seq['clips'][seq['clips'].index(clip):seq['clips'].index(clip)+1] = [left, right]
    for lane in ('audio', 'overlays', 'texts'):
        for e in seq.get(lane, []):
            if e.get('anchor', {}).get('clip') == clip['id'] and e['anchor']['offset'] >= offset:
                e['anchor'] = {'clip': right_id, 'offset': e['anchor']['offset'] - offset}
    sources = seq.get('captions', {}).get('sources')
    if sources is not None and clip['id'] in sources:
        sources.append(right_id)
    copy_framing(project, seq, clip['id'], right_id)
    return left, right


def apply_edit(project, op):
    seq = next((s for s in project['sequences'] if s['id'] == op.get('sequence')), None)
    require(seq is not None, 'Unknown sequence')
    kind, value = op['op'], op['value']
    if kind == 'set_framing':
        keys(value, ('deliverable', 'framing'), ('deliverable', 'framing'))
        d = next((d for d in project['deliverables'] if d['id'] == value['deliverable'] and d['sequence'] == seq['id']), None)
        require(d is not None, 'Unknown deliverable for this sequence')
        d['framing'] = copy.deepcopy(value['framing'])
        return
    matches = [e for lane in ('clips', 'audio', 'overlays', 'texts') for e in seq.get(lane, []) if e['id'] == op.get('id')]
    require(len(matches) == 1, 'Unknown event ID')
    clip = matches[0]
    if kind in ('set_keyframes', 'set_speed_curve', 'set_effects'):
        field = {'set_keyframes': 'keyframes', 'set_speed_curve': 'speed_curve', 'set_effects': 'effects'}[kind]
        clip[field] = copy.deepcopy(value)
        if field == 'keyframes':
            clip['keyframe_offset'] = 0
        if field == 'speed_curve':
            clip.pop('speed', None)
            clip.pop('freeze', None)
        return
    require(clip in seq['clips'], 'This structural edit requires a base picture clip')
    if kind == 'split_clip':
        keys(value, ('frame', 'right_id'), ('frame', 'right_id'))
        split(project, seq, clip, integer(value['frame'], 'split frame')-clip['start'], value['right_id'])
    elif kind == 'trim_clip':
        keys(value, ('in', 'out', 'ripple'), ('in', 'out'))
        begin, end = integer(value['in'], 'trim in'), integer(value['out'], 'trim out', 1, clip['duration'])
        require(begin < end, 'Empty trim interval')
        require(type(value.get('ripple', False)) is bool, 'Ripple must be boolean')
        require(not clip.get('transition'), 'Revise transition before trimming', 'edit_conflict')
        old_end, old_duration = clip['start']+clip['duration'], clip['duration']
        changed = trim_time(clip, begin, end, project['assets'][clip['asset']], ratio(seq['fps']))
        changed['start'] += 0 if value.get('ripple') else begin
        seq['clips'][seq['clips'].index(clip)] = changed
        for lane in ('audio', 'overlays', 'texts'):
            for e in seq.get(lane, []):
                if e.get('anchor', {}).get('clip') == clip['id']:
                    require(begin <= e['anchor']['offset'] and e['anchor']['offset']+e['duration'] <= end,
                            f"Trim removes anchored event {e['id']}; revise it first", 'edit_conflict')
                    e['anchor']['offset'] -= begin
        if value.get('ripple'):
            shift(seq, old_end, changed['duration']-old_duration, (clip['id'],))
    elif kind == 'move_clip':
        keys(value, ('start',), ('start',))
        clip['start'] = integer(value['start'], 'move start')
        seq['clips'].sort(key=lambda e: (e['start'], e['id']))
    elif kind == 'remove_clip':
        keys(value, ('ripple', 'dependents'))
        require(type(value.get('ripple', False)) is bool, 'Ripple must be boolean')
        require(value.get('dependents', 'reject') in ('reject', 'detach', 'remove'), 'Unknown dependent policy')
        for lane in ('audio', 'overlays', 'texts'):
            retained = []
            for e in seq.get(lane, []):
                if e.get('anchor', {}).get('clip') == clip['id']:
                    policy = value.get('dependents', 'reject')
                    require(policy != 'reject', f"Choose detach/remove for anchored event {e['id']}", 'edit_conflict')
                    if policy == 'remove':
                        continue
                    e['start'] = event_start(e, seq)
                    del e['anchor']
                retained.append(e)
            if lane in seq:
                seq[lane] = retained
        require(not clip.get('transition'), 'Revise transition before removal', 'edit_conflict')
        seq['clips'].remove(clip)
        for d in project['deliverables']:
            if d['sequence'] == seq['id']:
                d.get('framing', {}).pop(clip['id'], None)
        if 'sources' in seq.get('captions', {}):
            seq['captions']['sources'] = [x for x in seq['captions']['sources'] if x != clip['id']]
        if value.get('ripple'):
            shift(seq, clip['start']+clip['duration'], -clip['duration'])
    elif kind == 'freeze_frame':
        keys(value, ('frame', 'duration', 'hold_id', 'right_id'), ('frame', 'duration', 'hold_id', 'right_id'))
        duration = integer(value['duration'], 'hold duration', 1)
        frame = integer(value['frame'], 'hold frame')
        left, right = split(project, seq, clip, frame-clip['start'], value['right_id'])
        hold = copy.deepcopy(right)
        hold.update(id=identifier(value['hold_id']), duration=duration, freeze=True, mute=True)
        hold.pop('speed_curve', None)
        hold.pop('speed', None)
        # A freeze holds source pixels; its existing animation is held at the insertion point.
        from fc_time import parameters
        hold['keyframes'] = {k: [{'frame': 0, 'value': v}] for k, v in parameters(right, 0).items()}
        hold['keyframe_offset'] = 0
        shift(seq, frame, duration)
        hold['start'] = frame
        seq['clips'].insert(seq['clips'].index(right), hold)
        copy_framing(project, seq, clip['id'], hold['id'])
        from fc_time import value_at, PARAMETERS
        for delivery in project['deliverables']:
            framing = delivery.get('framing', {}).get(hold['id']) if delivery['sequence']==seq['id'] else None
            if framing is not None:
                framing['keyframes'] = {name: [{'frame': 0, 'value': value_at(points, right.get('keyframe_offset',0), PARAMETERS[name][2])}] for name,points in framing.get('keyframes',{}).items()}
