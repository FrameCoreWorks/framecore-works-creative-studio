#!/usr/bin/env python3
"""Sound for supplied footage: turn the user's video and its cuts into a sound contract that sound.py plans and mixes.

  python footage.py cuts clip.mp4 [--threshold 0.3]
  python footage.py contract clip.mp4 --out clip.sound.json [--cuts auto | --cuts 2.0,4.5 | --cuts cuts.txt]
         [--hit 12.4:impact[:label]] [--reveal 13.0] [--keep-audio] [--duck auto|captions.srt|none]
         [--style meadow] [--title ...] [--goal ...] [--audience ...] [--message ...] [--concept ...]
  python sound.py plan clip.sound.json --out clip-r1.sound.json --table cues.md
  python sound.py mix clip-r1.sound.json --video clip.mp4 --out clip-sound.mp4

The contract has no scene kinds to draw: its scenes are the shots between cuts, and `source` holds the cuts, the
moments the user marked (hits and a reveal) and, with --keep-audio, the video's own sound, which the music ducks
under. Needs Python 3.8+, ffmpeg and ffprobe, and numpy for --duck auto. Times are seconds (12.4) or m:ss.mmm.
"""
import argparse
import json
import os
import re
import subprocess
import sys

SOUNDS = ('whoosh', 'landing', 'click', 'release', 'tick', 'impact', 'boom', 'riser', 'shimmer')


def seconds(value):
    value = str(value).strip()
    match = re.fullmatch(r'(?:(\d+):)?(\d+):(\d+(?:[.,]\d+)?)', value)
    if match:
        h, m, s = match.groups()
        return int(h or 0) * 3600 + int(m) * 60 + float(s.replace(',', '.'))
    return float(value.replace(',', '.'))


def probe(video):
    run = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_type,width,height,r_frame_rate,nb_frames:format=duration', '-of', 'json', video],
                         capture_output=True, text=True, check=True)
    data = json.loads(run.stdout)
    picture = next(s for s in data['streams'] if s.get('codec_type') == 'video')
    num, _, den = picture['r_frame_rate'].partition('/')
    fps = {'num': int(num), 'den': int(den or 1)}
    duration = float(data.get('format', {}).get('duration') or 0)
    frames = int(picture.get('nb_frames') or 0) or round(duration * fps['num'] / fps['den'])
    return {'width': int(picture['width']), 'height': int(picture['height']), 'fps': fps, 'totalFrames': frames,
            'hasAudio': any(s.get('codec_type') == 'audio' for s in data['streams'])}


def detect_cuts(video, threshold=0.3):
    """Times of hard cuts from ffmpeg's scene score (0 to 1; 0.3 suits most edits, lower finds softer changes)."""
    run = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', video, '-vf', f"select='gt(scene,{threshold})',showinfo", '-an', '-f', 'null', '-'],
                         capture_output=True, text=True)
    if run.returncode != 0:
        raise RuntimeError('ffmpeg could not read the video for cut detection')
    return [float(t) for t in re.findall(r'pts_time:([0-9.]+)', run.stderr)]


def read_times(value):
    if os.path.exists(value):
        with open(value, encoding='utf-8') as handle:
            return [seconds(line.split(',')[0]) for line in handle if line.strip() and not line.lstrip().startswith('#')]
    return [seconds(item) for item in value.split(',') if item.strip()]


def active_audio(wav, fps, window=0.05, floor_db=-45.0, below_peak_db=24.0, bridge=0.4, shortest=0.3):
    """Where the video's own sound is present (speech, effects or music): 50 ms RMS above max(-45 dBFS, peak - 24 dB),
    gaps under 0.4 s bridged, bursts under 0.3 s dropped. Returns [{start, end}] in frames."""
    import numpy as np
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', wav, '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    audio = np.frombuffer(raw, '<f4').astype(np.float64)
    hop = int(16000 * window)
    if len(audio) < hop:
        return []
    frames = len(audio) // hop
    rms = np.sqrt(np.mean(audio[:frames * hop].reshape(frames, hop) ** 2, axis=1) + 1e-12)
    db = 20 * np.log10(rms)
    threshold = max(floor_db, float(db.max()) - below_peak_db)
    spans, start = [], None
    for i, loud in enumerate(db > threshold):
        if loud and start is None:
            start = i
        elif not loud and start is not None:
            spans.append([start * window, i * window])
            start = None
    if start is not None:
        spans.append([start * window, frames * window])
    merged = []
    for a, b in spans:
        if merged and a - merged[-1][1] < bridge:
            merged[-1][1] = b
        else:
            merged.append([a, b])
    rate = fps['num'] / fps['den']
    return [{'start': round(a * rate), 'end': round(b * rate)} for a, b in merged if b - a >= shortest]


def duck_from_captions(path, fps):
    here = os.path.dirname(os.path.abspath(__file__))
    import importlib.util
    for candidate in (os.path.join(here, '..', '..', '..', 'caption-studio', 'assets', 'captions', 'captions.py'), os.path.join(here, 'captions.py')):
        if os.path.exists(candidate):
            spec = importlib.util.spec_from_file_location('studio_captions', candidate)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            rate = fps['num'] / fps['den']
            return [{'start': round(c['start_ms'] / 1000 * rate), 'end': round(c['end_ms'] / 1000 * rate)} for c in module.read_cues(path)]
    raise RuntimeError('captions.py (Caption Studio) is needed to read a subtitle file for ducking')


def build_contract(video, args):
    info = probe(video)
    fps, total = info['fps'], info['totalFrames']
    rate = fps['num'] / fps['den']
    to_frame = lambda t: max(0, min(total - 1, round(t * rate)))  # noqa: E731
    if args.cuts == 'auto':
        cut_times, cuts_from = detect_cuts(video, args.threshold), f'detected by ffmpeg scene score above {args.threshold}'
    elif args.cuts in (None, 'none'):
        cut_times, cuts_from = [], 'none'
    else:
        cut_times, cuts_from = read_times(args.cuts), 'supplied by the user'
    cuts = sorted({to_frame(t) for t in cut_times if 0 < to_frame(t) < total})
    bounds = [0] + cuts + [total]
    scenes = [{'id': f'shot-{i + 1}', 'kind': 'footage', 'start': a, 'end': b} for i, (a, b) in enumerate(zip(bounds, bounds[1:])) if b > a]
    hits = []
    for item in args.hit or []:
        parts = item.split(':')
        # m:ss.mmm times contain colons, so the sound is the first known sound name after the time.
        at = next(i for i, part in enumerate(parts) if part in SOUNDS) if any(p in SOUNDS for p in parts) else None
        if at is None:
            raise ValueError(f'--hit {item}: use TIME:SOUND[:label] with SOUND one of {", ".join(SOUNDS)}')
        hits.append({'frame': to_frame(seconds(':'.join(parts[:at]))), 'sound': parts[at], 'label': ':'.join(parts[at + 1:]) or f'{parts[at]} marked by the user'})
    shot = (total / rate) / max(1, len(scenes))
    source = {'kind': 'footage', 'video': os.path.basename(video), 'cuts': cuts, 'cutsFrom': cuts_from, 'hits': hits,
              'reveal': to_frame(seconds(args.reveal)) if args.reveal else None, 'averageShotSeconds': round(shot, 2)}
    contract = {'id': os.path.splitext(os.path.basename(video))[0], 'fps': fps, 'width': info['width'], 'height': info['height'], 'totalFrames': total,
                'motion': {'tempo': 'fast' if shot < 1.2 else 'medium' if shot < 2.5 else 'slow'}, 'scenes': scenes, 'source': source,
                'copy': {}, 'revision': 0, 'approval': {'status': 'proposed', 'revision': None, 'evidence': None}}
    for key in ('title', 'goal', 'audience', 'message', 'concept', 'style'):
        if getattr(args, key, None):
            contract[key] = getattr(args, key)
    folder = os.path.dirname(os.path.abspath(args.out))
    if args.keep_audio:
        if not info['hasAudio']:
            raise ValueError('--keep-audio: the video has no audio track')
        name = contract['id'] + '.original.wav'
        path = os.path.join(folder, name)
        if os.path.exists(path):
            raise ValueError(f'Output file already exists: {path}')
        subprocess.run(['ffmpeg', '-v', 'error', '-i', video, '-vn', '-ac', '2', '-ar', '48000', '-c:a', 'pcm_s24le', path], check=True)
        source['originalAudio'] = {'src': name, 'volume': 1.0}
        if args.duck == 'auto':
            source['duck'], source['duckFrom'] = active_audio(path, fps), 'the video\'s own sound above its level threshold'
        elif args.duck not in (None, 'none'):
            source['duck'], source['duckFrom'] = duck_from_captions(args.duck, fps), f'subtitle cues in {os.path.basename(args.duck)}'
    return contract


def main(argv=None):
    parser = argparse.ArgumentParser(description='Sound contracts for supplied footage.')
    sub = parser.add_subparsers(dest='command', required=True)
    c = sub.add_parser('cuts')
    c.add_argument('video')
    c.add_argument('--threshold', type=float, default=0.3)
    k = sub.add_parser('contract')
    k.add_argument('video')
    k.add_argument('--out', required=True)
    k.add_argument('--cuts', default='auto', help='auto, none, a comma-separated list of times or a file with one time per line')
    k.add_argument('--threshold', type=float, default=0.3)
    k.add_argument('--hit', action='append', help='TIME:SOUND[:label], for example 12.4:impact:logo lands; SOUND is ' + ', '.join(SOUNDS))
    k.add_argument('--reveal', help='the time the closing reveal settles (logo, product, end card)')
    k.add_argument('--keep-audio', action='store_true', help="keep the video's own sound in the mix")
    k.add_argument('--duck', default='auto', help='with --keep-audio: auto, none, or an SRT or WebVTT file whose cues mark speech')
    for key in ('title', 'goal', 'audience', 'message', 'concept', 'style'):
        k.add_argument('--' + key)
    args = parser.parse_args(argv)
    try:
        if args.command == 'cuts':
            info = probe(args.video)
            rate = info['fps']['num'] / info['fps']['den']
            times = detect_cuts(args.video, args.threshold)
            print(json.dumps({'cuts': [{'time': round(t, 3), 'frame': round(t * rate)} for t in times], 'threshold': args.threshold, 'totalFrames': info['totalFrames']}))
            return 0
        if os.path.exists(args.out):
            raise ValueError(f'Output file already exists: {args.out}')
        contract = build_contract(args.video, args)
        with open(args.out, 'w', encoding='utf-8') as handle:
            handle.write(json.dumps(contract, indent=2, ensure_ascii=False) + '\n')
        source = contract['source']
        print(json.dumps({'out': args.out, 'shots': len(contract['scenes']), 'cuts': len(source['cuts']), 'cutsFrom': source['cutsFrom'], 'hits': len(source['hits']),
                          'reveal': source['reveal'], 'originalAudio': bool(source.get('originalAudio')), 'duck': len(source.get('duck') or []), 'tempo': contract['motion']['tempo']}, ensure_ascii=False))
        return 0
    except (OSError, ValueError, RuntimeError, KeyError, StopIteration, subprocess.CalledProcessError) as error:
        sys.stderr.write(f'{error}\n')
        return 2


if __name__ == '__main__':
    sys.exit(main())
