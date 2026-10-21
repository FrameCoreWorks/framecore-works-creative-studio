"""Bounded stereo varispeed using FrameCut's shared source-time map."""
import array
import math
import sys
import wave
from fractions import Fraction
from fc_core import ratio, require, round_boundary, source_clock, span_seconds
from fc_jobs import checkpoint
from fc_time import source_offset, speed_points


def gain_expression(event, fps):
    points = event.get('keyframes', {}).get('gain_db', [])
    if not points:
        return None
    t = f'(t*{float(fps):.16g}+{event.get("keyframe_offset",0)})'
    expr = str(points[-1]['value'])
    for a,b in reversed(list(zip(points,points[1:]))):
        u = f'(({t}-{a["frame"]})/{b["frame"]-a["frame"]})'
        easing = a.get('easing','linear')
        shaped = '0' if easing == 'hold' else f'({u}*{u}*(3-2*{u}))' if easing == 'smooth' else u
        value = f'({a["value"]}+({b["value"]-a["value"]})*{shaped})'
        expr = f'if(lt({t},{b["frame"]}),{value},{expr})'
    expr = f'if(lte({t},{points[0]["frame"]}),{points[0]["value"]},{expr})'
    return f"volume='pow(10,({expr})/20)':eval=frame"


def varispeed(root, asset, event, fps, cache):
    from fc_core import confined
    from fc_media import ffmpeg
    from fc_render import decimal
    settings = {'source': asset['sha256'], 'probe': asset['probe'], 'event': {k:event[k] for k in ('source_in','source_remainder','duration','speed_curve') if k in event}, 'fps':str(fps), 'audio_policy':'continuous-varispeed-pitch-follows-speed'}
    def build(out):
        relative, length = span_seconds(asset,event,fps)
        _,origin = source_clock(asset)
        start = relative+origin
        audio_stream = next(s for s in asset['probe']['streams'] if s['index']==asset['probe']['audio_index'])
        delay = max(Fraction(0),Fraction(audio_stream.get('start_time','0'))-start)
        samples = round_boundary(Fraction(event['duration'])/fps*48000)
        source = out.with_name('source.pcm')
        n_source = math.ceil(length*48000)+2
        filters = [f'atrim=start={decimal(start)}:duration={decimal(length)}','asetpts=PTS-STARTPTS','aresample=48000','aformat=channel_layouts=stereo']
        if delay:
            filters.append(f'adelay={round_boundary(delay*48000)}S:all=1')
        filters += [f'apad=whole_len={n_source}',f'atrim=end_sample={n_source}']
        ffmpeg(['-copyts','-protocol_whitelist','file,pipe','-i',str(confined(root,asset['path'],True)),
                '-map',f'0:{asset["probe"]["audio_index"]}','-af',','.join(filters),'-c:a','pcm_s32le','-f','s32le',str(source)],cache.timeout)
        points = speed_points(event)
        spans = [(a['frame'],b['frame'],float(source_offset(event,a['frame'],fps)*48000),float(ratio(a['speed'])),float(ratio(b['speed'])-ratio(a['speed']))/(2*(b['frame']-a['frame']))) for a,b in zip(points,points[1:])]
        factor = float(fps)/48000
        with source.open('rb') as reader, wave.open(str(out),'wb') as writer:
            source_frames = source.stat().st_size // 8
            writer.setnchannels(2); writer.setsampwidth(4); writer.setframerate(48000)
            span_index = 0
            for offset in range(0,samples,4096):
                checkpoint('varispeed:'+event['id'], frame=offset, total=samples, unit='samples')
                indexes = []
                for index in range(offset,min(offset+4096,samples)):
                    frame = index*factor
                    while span_index+1<len(spans) and frame>=spans[span_index][1]: span_index+=1
                    a,b,base,speed,quadratic = spans[span_index]
                    u = frame-a
                    indexes.append(base+(speed*u+quadratic*u*u)/factor)
                first = max(0,math.floor(indexes[0]))
                last = min(source_frames,math.floor(indexes[-1])+2)
                reader.seek(min(first,source_frames)*8)
                raw = array.array('i',reader.read(max(0,last-first)*8))
                if sys.byteorder!='little': raw.byteswap()
                values = array.array('i')
                for index in indexes:
                    pos = math.floor(index)-first
                    blend = index-math.floor(index)
                    for channel in range(2):
                        i = 2*pos+channel
                        a = raw[i] if 0<=i<len(raw) else 0
                        b = raw[i+2] if 0<=i+2<len(raw) else a
                        values.append(max(-2147483648,min(2147483647,round(a+(b-a)*blend))))
                if sys.byteorder!='little': values.byteswap()
                writer.writeframes(values.tobytes())
    return cache.stage('varispeed',settings,'.wav',build)
