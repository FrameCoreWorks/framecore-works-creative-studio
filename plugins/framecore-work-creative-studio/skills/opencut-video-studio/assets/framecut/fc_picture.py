"""Shared native image transforms for clip encoding and composited storyboard stills."""
import copy
import math
import os
import select
import signal
import subprocess
import tempfile
import time
from fractions import Fraction
from pathlib import Path
from fc_core import FrameCutError, confined, ratio, require, source_clock, span_seconds
from fc_time import parameters, retime_expression
from fc_jobs import checkpoint


def pillow():
    try:
        from PIL import Image
        return Image
    except ImportError as error:
        raise FrameCutError('missing_capability', 'Pillow is required for native transforms and storyboard stills; install it in the selected Python environment') from error


def effective_event(event, delivery):
    result = copy.deepcopy(event)
    framing = delivery.get('framing', {}).get(event['id'], {})
    result.update({k: v for k,v in framing.items() if k != 'keyframes'})
    result['keyframes'] = {**event.get('keyframes', {}), **framing.get('keyframes', {})}
    return result


def geometry(asset):
    p = asset['probe']
    width, height = p['width'], p['height']
    sar = Fraction(p.get('sar', '1:1').replace(':', '/')) if p.get('sar') not in (None, 'N/A', '0:1') else Fraction(1)
    width = max(2, round(width * sar))
    if abs(p.get('rotation', 0)) % 180 == 90:
        width, height = height, width
    scale = min(1, 4096/max(width, height))
    return max(2, round(width*scale)), max(2, round(height*scale))


def decode_command(root, asset, event, fps, frame=None, output=None):
    from fc_render import decimal
    source = confined(root, asset['path'], True)
    args = ['ffmpeg', '-hide_banner', '-nostdin', '-v', 'error', '-threads', '2', '-filter_threads', '1', '-copyts']
    if asset['kind'] == 'image':
        args += ['-loop', '1', '-framerate', str(fps)]
    args += ['-protocol_whitelist', 'file,pipe', '-i', str(source)]
    relative, length = span_seconds(asset, event, fps)
    _, origin = source_clock(asset)
    filters = []
    if asset['kind'] != 'image':
        if event.get('freeze'):
            filters += [f'trim=start={decimal(relative+origin)}', "select='eq(n,0)'", 'loop=loop=-1:size=1:start=0', f'setpts=N/({fps}*TB)']
        else:
            filters += [f'trim=end={decimal(relative+origin+length)}', retime_expression(event, fps, relative+origin)]
    else:
        filters += ['setpts=PTS-STARTPTS']
    width, height = geometry(asset)
    filters += [f'fps=fps={fps}:start_time=0', f'scale={width}:{height}', 'setsar=1',
                f'tpad=stop_mode=clone:stop_duration={decimal(Fraction(2)/fps)}', f'trim=end_frame={event["duration"]}', 'format=rgba']
    if frame is not None:
        filters += [f"select='eq(n,{frame})'"]
    args += ['-map', f'0:{asset["probe"]["video_index"]}', '-an', '-vf', ','.join(filters), '-vsync', '0',
             '-frames:v', str(event['duration'] if frame is None else 1)]
    return args + (['-f', 'rawvideo', '-pix_fmt', 'rgba', 'pipe:1'] if output is None else ['-threads', '1', str(output)])


def transform(image, event, delivery, frame, alpha=False):
    Image = pillow()
    from fc_effects import picture
    event = effective_event(event, delivery)
    v = parameters(event, frame)
    width, height = delivery['width'], delivery['height']
    image = image.convert('RGBA')
    x,y,w,h = event.get('crop', [0,0,1,1])
    # A zoom/pan is local to the authored crop. No hidden subject tracking.
    cw, ch = w/v['zoom'], h/v['zoom']
    x += (w-cw)*v['pan_x']; y += (h-ch)*v['pan_y']
    iw, ih = image.size
    image = image.crop((x*iw, y*ih, (x+cw)*iw, (y+ch)*ih))
    fit = event.get('fit', delivery.get('fit', 'contain'))
    scale = (max if fit == 'cover' else min)(width/image.width, height/image.height)
    # Transform by inverse affine coordinates directly into the output canvas;
    # memory is bounded by output size even at 8x scale or a large rotation.
    scale *= v['scale']
    angle = math.radians(v['rotation'])
    c, s = math.cos(angle)/scale, math.sin(angle)/scale
    center_x, center_y = width*(.5+v['x']), height*(.5+v['y'])
    matrix = (c, s, image.width/2-c*center_x-s*center_y,
              -s, c, image.height/2+s*center_x-c*center_y)
    image = image.transform((width,height), Image.Transform.AFFINE, matrix, Image.Resampling.BICUBIC,
                            fillcolor=(0,0,0,0))
    image = picture(image, event.get('effects', []))
    if v['opacity'] != 1:
        image.putalpha(image.getchannel('A').point([round(n*v['opacity']) for n in range(256)]))
    if not alpha:
        background = Image.new('RGBA', (width,height), (0,0,0,255))
        background.alpha_composite(image)
        image = background
    return image


def kill(process):
    if process.poll() is None:
        try:
            if os.name == 'posix': os.killpg(process.pid, signal.SIGKILL)
            else: process.kill()
        except ProcessLookupError:
            pass
    process.wait()


def transfer(fd, data_or_size, deadline, writing=False):
    """Bounded pipe I/O with cancellation and timeout on POSIX render workers."""
    remaining = len(data_or_size) if writing else data_or_size
    data, offset = bytearray(), 0
    while remaining:
        checkpoint()
        require(time.monotonic() < deadline, 'Native picture stage timed out', 'resource_limit')
        ready = select.select([] if writing else [fd], [fd] if writing else [], [], .2)
        if not ready[1 if writing else 0]:
            continue
        try:
            if writing:
                count = os.write(fd, memoryview(data_or_size)[offset:offset+min(65536,remaining)])
            else:
                block = os.read(fd, min(1048576, remaining))
                if not block:
                    break
                data.extend(block); count = len(block)
        except BlockingIOError:
            continue
        remaining -= count; offset += count
    return offset if writing else bytes(data)


def encode_clip(root, asset, event, delivery, fps, output, timeout, alpha=False):
    Image = pillow()
    from fc_media import run
    if os.name != 'posix':
        # File-backed fallback avoids unsupported select() on Windows pipes.
        return encode_files(root, asset, event, delivery, fps, output, timeout, alpha)
    width,height = geometry(asset)
    deadline = time.monotonic()+timeout
    encoder_args = ['ffmpeg','-hide_banner','-nostdin','-v','error','-threads','2','-filter_threads','1',
                    '-f','rawvideo','-pix_fmt','rgba','-s',f'{delivery["width"]}x{delivery["height"]}', '-r',str(fps),'-i','pipe:0','-an']
    encoder_args += ['-c:v','qtrle','-pix_fmt','argb'] if alpha else ['-vf','scale=out_color_matrix=bt709:out_range=tv','-c:v','libx264','-preset','veryfast','-crf','16','-pix_fmt','yuv444p','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709']
    processes = []
    with tempfile.TemporaryFile() as decoder_log, tempfile.TemporaryFile() as encoder_log:
        try:
            decoder = subprocess.Popen(decode_command(root,asset,event,fps), stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=decoder_log, start_new_session=True)
            processes.append(decoder)
            encoder = subprocess.Popen([*encoder_args,str(output)], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=encoder_log, start_new_session=True)
            processes.append(encoder)
            os.set_blocking(decoder.stdout.fileno(), False)
            os.set_blocking(encoder.stdin.fileno(), False)
            checkpoint('picture:'+event['id'], frame=0, total=event['duration'])
            for frame in range(event['duration']):
                raw = transfer(decoder.stdout.fileno(), width*height*4, deadline)
                require(len(raw) == width*height*4, 'Source decoder returned an incomplete frame', 'render_failed')
                image = transform(Image.frombytes('RGBA',(width,height),raw), event, delivery, frame, alpha)
                transfer(encoder.stdin.fileno(), image.tobytes(), deadline, True)
                checkpoint(frame=frame+1, total=event['duration'])
            encoder.stdin.close()
            decoder.stdout.close()
            for process in processes:
                process.wait(timeout=max(.1,deadline-time.monotonic()))
            if decoder.returncode or encoder.returncode:
                decoder_log.seek(0); encoder_log.seek(0)
                raise FrameCutError('render_failed', (decoder_log.read()+encoder_log.read()).decode('utf-8','replace')[-2000:])
        except (OSError, subprocess.TimeoutExpired) as error:
            raise FrameCutError('render_failed', str(error)) from error
        finally:
            for process in processes:
                kill(process)


def encode_files(root, asset, event, delivery, fps, output, timeout, alpha):
    from fc_media import run, ffmpeg
    Image = pillow()
    with tempfile.TemporaryDirectory(prefix='frames-', dir=Path(output).parent) as tmp:
        directory = Path(tmp)
        require(event['duration']*(delivery['width']*delivery['height']+math.prod(geometry(asset)))*4 < 512*1024**2,
                'File-backed transform exceeds 512 MiB; split the requested interval', 'resource_limit')
        run(decode_command(root, asset, event, fps, output=directory/'source-%08d.png'), timeout)
        for frame in range(event['duration']):
            checkpoint('picture:'+event['id'], frame=frame, total=event['duration'])
            with Image.open(directory/f'source-{frame+1:08d}.png') as image:
                transformed = transform(image, event, delivery, frame, alpha)
            transformed.save(directory/f'render-{frame+1:08d}.png')
        encoding = ['-c:v','qtrle','-pix_fmt','argb'] if alpha else ['-vf','scale=out_color_matrix=bt709:out_range=tv','-c:v','libx264','-crf','16','-pix_fmt','yuv444p','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709']
        ffmpeg(['-framerate',str(fps),'-i',str(directory/'render-%08d.png'),'-frames:v',str(event['duration']),*encoding,str(output)], timeout)


def clip_frame(root, asset, event, delivery, fps, frame, timeout, alpha=False):
    from fc_media import run
    Image = pillow()
    with tempfile.TemporaryDirectory(prefix='.framecut-still-', dir=root) as tmp:
        output = Path(tmp)/'source.png'
        run(decode_command(root,asset,event,fps,frame,output), timeout)
        require(output.is_file(), 'Requested frame could not be decoded', 'render_failed')
        with Image.open(output) as image:
            return transform(image, event, delivery, frame, alpha)
