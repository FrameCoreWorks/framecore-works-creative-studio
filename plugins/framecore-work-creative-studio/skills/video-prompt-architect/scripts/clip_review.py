#!/usr/bin/env python3
"""Review generated or supplied clips side by side: first, middle and last decoded frame of each clip on one sheet, with
the measured duration, size, frame rate and audio, checked against the shot plan.

  python3 clip_review.py clips/S01_take2.mp4 clips/S02.mp4 --plan shot-plan.json --aspect 9:16 --fps 30 --out-dir review/

A clip belongs to the shot whose ID its file name contains (S01_take2.mp4 is a take of S01); without a plan, clips are
only measured. Findings: a clip shorter than its shot's edit interval (it cannot fill the shot), a frame size whose ratio
differs from --aspect, a frame rate other than --fps, an unreadable file. Frames are picked by decoded frame number,
as inspect-encode.py does, never by rounded timestamps. Writes contact-sheet.png and review.json; nothing is uploaded and
no quality verdict is made: look at the sheet. Needs ffmpeg with ffprobe and Pillow.
Exit codes: 0 no findings, 1 findings, 2 setup problem or an output folder that exists.
"""
import argparse
import io
import json
import shutil
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

RATIOS = {'16:9': 16 / 9, '9:16': 9 / 16, '1:1': 1.0, '4:5': 4 / 5, '4:3': 4 / 3, '2.39:1': 2.39}
FONTS = Path(__file__).resolve().parents[2] / 'pipeline-core/assets/fonts/inter'


class SetupError(Exception):
    pass


def probe(path, ffprobe):
    done = subprocess.run([ffprobe, '-v', 'error', '-count_frames', '-show_streams', '-show_format', '-of', 'json', str(path)], capture_output=True, text=True)
    if done.returncode != 0:
        return None
    data = json.loads(done.stdout or '{}')
    video = next((s for s in data.get('streams', []) if s.get('codec_type') == 'video'), None)
    if not video:
        return None
    rate = Fraction(video.get('avg_frame_rate') or video.get('r_frame_rate') or '0/1') if (video.get('avg_frame_rate') or '0/0') != '0/0' else Fraction(video.get('r_frame_rate', '0/1'))
    frames = int(video.get('nb_read_frames') or video.get('nb_frames') or 0)
    duration = float(data.get('format', {}).get('duration') or video.get('duration') or 0)
    return {'width': int(video['width']), 'height': int(video['height']), 'fps': round(float(rate), 3) if rate else None, 'frames': frames,
            'seconds': round(duration, 3), 'audio': any(s.get('codec_type') == 'audio' for s in data.get('streams', [])), 'codec': video.get('codec_name')}


def stills(path, frames, ffmpeg, height):
    """First, middle and last decoded frame as Pillow images, scaled to `height`."""
    from PIL import Image
    picks = sorted({0, max(0, (frames - 1) // 2), max(0, frames - 1)})
    out = []
    for n in picks:
        done = subprocess.run([ffmpeg, '-v', 'error', '-i', str(path), '-map', '0:v:0', '-vf', f"select='eq(n\\,{n})',scale=-2:{height}", '-fps_mode', 'vfr', '-frames:v', '1',
                               '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True)
        if done.returncode != 0 or not done.stdout:
            raise SetupError(f'{path}: could not read frame {n}')
        out.append(Image.open(io.BytesIO(done.stdout)).convert('RGB'))
    return picks, out


def main(argv=None):
    parser = argparse.ArgumentParser(description='Contact sheet and checks for generated or supplied clips.')
    parser.add_argument('clips', nargs='+')
    parser.add_argument('--plan', help='shot plan JSON (shots with id, start_s, end_s)')
    parser.add_argument('--aspect', choices=sorted(RATIOS), help='expected frame ratio')
    parser.add_argument('--fps', type=float, help='expected frame rate')
    parser.add_argument('--out-dir', required=True)
    args = parser.parse_args(argv)
    try:
        ffmpeg, ffprobe = shutil.which('ffmpeg'), shutil.which('ffprobe')
        if not ffmpeg or not ffprobe:
            raise SetupError('ffmpeg and ffprobe are needed; this tool installs nothing')
        try:
            from PIL import Image, ImageDraw, ImageFont
        except ImportError:
            raise SetupError('Pillow is needed for the contact sheet (pip install pillow)')
        out = Path(args.out_dir)
        if out.exists():
            raise SetupError(f'output folder exists: {out}')
        shots = []
        if args.plan:
            shots = json.loads(Path(args.plan).read_text(encoding='utf-8')).get('shots') or []
        try:
            font, bold = ImageFont.truetype(str(FONTS / 'Inter-Regular.ttf'), 18), ImageFont.truetype(str(FONTS / 'Inter-Bold.ttf'), 20)
        except OSError:
            font = bold = ImageFont.load_default()
        thumb_h, text_w, pad = 240, 520, 14
        rows, report, findings = [], [], []
        for clip in args.clips:
            path = Path(clip)
            info = probe(path, ffprobe) if path.is_file() else None
            shot = next((s for s in shots if s.get('id') and str(s['id']) in path.name), None)
            entry = {'clip': str(path), 'shot': shot.get('id') if shot else None, 'measured': info, 'findings': []}
            if not info:
                entry['findings'].append('unreadable: no video stream')
            else:
                if shot and isinstance(shot.get('start_s'), (int, float)) and isinstance(shot.get('end_s'), (int, float)):
                    need = round(shot['end_s'] - shot['start_s'], 3)
                    entry['planned_seconds'] = need
                    if info['seconds'] + 1e-6 < need:
                        entry['findings'].append(f"shorter than its shot: {info['seconds']} s for {need} s")
                if args.aspect and abs(info['width'] / info['height'] - RATIOS[args.aspect]) > 0.01:
                    entry['findings'].append(f"frame {info['width']} x {info['height']} is not {args.aspect}")
                if args.fps and info['fps'] and abs(info['fps'] - args.fps) > 0.01:
                    entry['findings'].append(f"{info['fps']} fps, not {args.fps:g}")
                if shots and not shot:
                    entry['findings'].append('no shot ID from the plan in its file name')
            report.append(entry)
            findings += [f"{path.name}: {f}" for f in entry['findings']]
            images = stills(path, info['frames'], ffmpeg, thumb_h)[1] if info and info['frames'] else []
            rows.append((entry, images))
        widths = [sum(i.width for i in images) + pad * (len(images) + 1) for _, images in rows]
        sheet = Image.new('RGB', (max(widths + [3 * pad]) + text_w, len(rows) * (thumb_h + 2 * pad) + pad), (36, 36, 36))
        draw = ImageDraw.Draw(sheet)
        for r, (entry, images) in enumerate(rows):
            y, x = pad + r * (thumb_h + 2 * pad), pad
            for image in images:
                sheet.paste(image, (x, y))
                x += image.width + pad
            tx = max(widths + [3 * pad])
            info = entry['measured']
            lines = [(Path(entry['clip']).name, bold), (f"shot {entry['shot'] or '-'}" + (f", planned {entry.get('planned_seconds')} s" if entry.get('planned_seconds') else ''), font)]
            if info:
                lines += [(f"{info['seconds']} s, {info['frames']} frames, {info['fps']} fps", font), (f"{info['width']} x {info['height']}, {info['codec']}, {'with' if info['audio'] else 'no'} audio", font)]
            lines += [(f'! {f}', font) for f in entry['findings']]
            for k, (text, f) in enumerate(lines):
                draw.text((tx, y + k * 26), text, font=f, fill=(255, 120, 100) if text.startswith('!') else (235, 235, 235))
        out.mkdir(parents=True)
        sheet.save(out / 'contact-sheet.png')
        (out / 'review.json').write_text(json.dumps({'clips': report, 'findings': findings, 'scope': 'measured properties and frames only; look at the sheet for picture quality'},
                                                    ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    except (OSError, ValueError, SetupError) as error:
        sys.stderr.write(f'{error}\n')
        return 2
    print(json.dumps({'sheet': str(out / 'contact-sheet.png'), 'clips': len(report), 'findings': findings}, ensure_ascii=False))
    return 1 if findings else 0


if __name__ == '__main__':
    sys.exit(main())
