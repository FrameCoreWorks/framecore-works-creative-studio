"""Original exact source maps and shared animation evaluation for FrameCut."""
from fractions import Fraction
from fc_core import integer, keys, number, ratio, require, round_boundary

PARAMETERS = {'x': (-2, 2, 0), 'y': (-2, 2, 0), 'scale': (.05, 8, 1),
              'rotation': (-3600, 3600, 0), 'opacity': (0, 1, 1),
              'gain_db': (-90, 24, 0), 'zoom': (1, 8, 1),
              'pan_x': (0, 1, .5), 'pan_y': (0, 1, .5)}


def fraction_data(value):
    value = Fraction(value)
    return {'num': value.numerator, 'den': value.denominator}


def remainder(event):
    data = event.get('source_remainder', {'num': 0, 'den': 1})
    keys(data, ('num', 'den'), ('num', 'den'))
    return Fraction(integer(data['num'], 'source remainder numerator'), integer(data['den'], 'source remainder denominator', 1))


def validate_animation(tracks):
    require(isinstance(tracks, dict) and set(tracks) <= set(PARAMETERS), 'Unknown keyframe parameter')
    for name, points in tracks.items():
        require(isinstance(points, list) and 1 <= len(points) <= 128, 'Keyframe track needs 1..128 points')
        last = -1
        for point in points:
            keys(point, ('frame', 'value', 'easing'), ('frame', 'value'))
            frame = integer(point['frame'], 'keyframe', 0, 2592000)
            require(frame > last, 'Keyframes must be strictly ordered')
            last = frame
            number(point['value'], name, *PARAMETERS[name][:2])
            require(point.get('easing', 'linear') in ('linear', 'smooth', 'hold'), 'Unknown easing')


def value_at(points, frame, default):
    if not points:
        return default
    if frame <= points[0]['frame']:
        return points[0]['value']
    for a, b in zip(points, points[1:]):
        if frame < b['frame']:
            u = float((frame - a['frame']) / (b['frame'] - a['frame']))
            mode = a.get('easing', 'linear')
            u = 0 if mode == 'hold' else u*u*(3-2*u) if mode == 'smooth' else u
            return a['value'] + (b['value'] - a['value']) * u
    return points[-1]['value']


def parameters(event, frame):
    frame += event.get('keyframe_offset', 0)
    return {name: value_at(event.get('keyframes', {}).get(name), frame, bounds[2]) for name, bounds in PARAMETERS.items()}


def validate_time(event, fps, source_tb):
    require(remainder(event) < source_tb, 'Source remainder must be less than one source PTS tick')
    require(type(event.get('freeze', False)) is bool, 'Freeze must be boolean')
    if event.get('freeze'):
        require(not event.get('speed_curve'), 'Freeze and speed curve are mutually exclusive')
    if 'speed_curve' in event:
        points = event['speed_curve']
        require(isinstance(points, list) and 2 <= len(points) <= 64, 'Speed curve needs 2..64 points')
        require(points[0]['frame'] == 0 and points[-1]['frame'] == event['duration'], 'Speed curve must cover the whole clip')
        require(ratio(event.get('speed', {'num': 1, 'den': 1})) == 1, 'Use speed or speed_curve, not both')
        previous = -1
        for point in points:
            keys(point, ('frame', 'speed'), ('frame', 'speed'))
            frame = integer(point['frame'], 'speed key frame', 0, event['duration'])
            require(frame > previous, 'Speed keys must be strictly ordered')
            previous = frame
            require(Fraction(1, 4) <= ratio(point['speed']) <= 4, 'Speed outside 1/4..4')


def speed_points(event):
    return event.get('speed_curve') or [{'frame': 0, 'speed': event.get('speed', {'num': 1, 'den': 1})},
                                        {'frame': event['duration'], 'speed': event.get('speed', {'num': 1, 'den': 1})}]


def source_offset(event, frame, fps):
    """Source seconds consumed by a timeline position, before quantization."""
    if event.get('freeze'):
        return Fraction(0)
    frame = min(Fraction(event['duration']), max(Fraction(0), Fraction(frame)))
    total = Fraction(0)
    points = speed_points(event)
    for a, b in zip(points, points[1:]):
        width = b['frame'] - a['frame']
        u = min(Fraction(width), max(Fraction(0), frame - a['frame']))
        va, vb = ratio(a['speed']), ratio(b['speed'])
        total += (va*u + (vb-va)*u*u/(2*width)) / fps
        if frame <= b['frame']:
            break
    return total


def timeline_offset(event, seconds, fps):
    """Inverse monotone map; bisection error is at most duration / 2**64 frames."""
    if not event.get('speed_curve'):
        return Fraction(seconds) / ratio(event.get('speed', {'num': 1, 'den': 1})) * fps
    low, high = Fraction(0), Fraction(event['duration'])
    for _ in range(64):
        middle = (low + high) / 2
        if source_offset(event, middle, fps) < seconds:
            low = middle
        else:
            high = middle
    return (low + high) / 2


def trim_time(event, begin, end, asset, fps):
    """Keep the source interval and the original animation clock across split/trim."""
    import copy
    result = copy.deepcopy(event)
    tick = Fraction(asset['probe']['time_base'])
    source = Fraction(event.get('source_in', asset['probe']['start_pts'])) * tick + remainder(event) + source_offset(event, begin, fps)
    pts = source // tick
    result['source_in'] = pts
    result['source_remainder'] = fraction_data(source - pts*tick)
    result['duration'] = end - begin
    result['keyframe_offset'] = event.get('keyframe_offset', 0) + begin
    if event.get('speed_curve'):
        points = event['speed_curve']
        def at(n):
            for a, b in zip(points, points[1:]):
                if n <= b['frame']:
                    return ratio(a['speed']) + (ratio(b['speed'])-ratio(a['speed'])) * Fraction(n-a['frame'], b['frame']-a['frame'])
            return ratio(points[-1]['speed'])
        result['speed_curve'] = [{'frame': n-begin, 'speed': fraction_data(at(n))}
                                for n in [begin, *[p['frame'] for p in points if begin < p['frame'] < end], end]]
    return result


def retime_expression(event, fps, source_start=0):
    """FFmpeg setpts inverse of the same piecewise-linear speed integral."""
    def dec(x):
        return format(float(x), '.16g')
    points = speed_points(event)
    expression = dec(Fraction(event['duration'])/fps)
    for a, b in reversed(list(zip(points, points[1:]))):
        start = source_offset(event, a['frame'], fps)
        stop = source_offset(event, b['frame'], fps)
        va, vb = ratio(a['speed']), ratio(b['speed'])
        acceleration = (vb-va) / (Fraction(b['frame']-a['frame'])/fps)
        elapsed = f'(T-STARTT-{dec(start)})'
        local = f'{elapsed}/{dec(va)}' if acceleration == 0 else f'2*{elapsed}/({dec(va)}+sqrt(max(0,{dec(va*va)}+{dec(2*acceleration)}*{elapsed})))'
        value = f'({dec(Fraction(a["frame"])/fps)}+{local})'
        expression = f'if(lt(T-STARTT,{dec(stop)}),{value},{expression})'
    expression = expression.replace('T-STARTT', f'(T-{dec(source_start)})')
    expression = f'if(lt(T,{dec(source_start)}),(T-{dec(source_start)})/{dec(ratio(points[0]["speed"]))},{expression})'
    return f"setpts='{expression}/TB'"
