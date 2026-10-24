"""Measure reads against their limits and apply a bounded speed-up. Standard library only."""
import array
import hashlib
import subprocess
import sys
import wave
from pathlib import Path

MAX_STRETCH_PERCENT = 5.0


class AudioError(RuntimeError):
    pass


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def spoken_duration(path, threshold_dbfs=-50.0):
    """Seconds up to the last frame above the threshold (16-bit PCM WAV, any channel count)."""
    try:
        with wave.open(str(path), 'rb') as source:
            width, channels, rate = source.getsampwidth(), source.getnchannels(), source.getframerate()
            raw = source.readframes(source.getnframes())
    except (wave.Error, EOFError) as error:
        raise AudioError(f'{path} is not a readable WAV: {error}') from None
    if width != 2:
        raise AudioError(f'{path} is {width * 8}-bit; 16-bit PCM is required')
    samples = array.array('h')
    samples.frombytes(raw[:len(raw) - len(raw) % 2])
    if sys.byteorder == 'big':
        samples.byteswap()
    threshold = 32767 * 10 ** (threshold_dbfs / 20)
    for index in range(len(samples) - 1, -1, -1):
        if abs(samples[index]) > threshold:
            return round((index // channels + 1) / rate, 3)
    return 0.0


def verdict(duration, max_seconds):
    if duration == 0.0:
        return 'silent'
    return 'fits' if duration <= max_seconds else 'over'


def line_wav(out_dir, cue, lock):
    recorded = lock.lines.get(cue.id, {}).get('wav')
    return Path(out_dir) / (recorded or f'{cue.id}.wav')


def measure_all(cues, out_dir, lock=None):
    if lock is None:
        from formats import Lock
        lock = Lock.load(out_dir)
    rows = []
    for cue in cues:
        path = line_wav(out_dir, cue, lock)
        row = {'id': cue.id, 'max_seconds': cue.max_seconds, 'wav': str(path)}
        if not path.exists():
            row.update(duration=None, verdict='missing', over_by=None)
        else:
            try:
                duration = spoken_duration(path)
            except AudioError as error:
                row.update(duration=None, verdict='unreadable', over_by=None, error=str(error))
            else:
                result = verdict(duration, cue.max_seconds)
                over_by = round(duration - cue.max_seconds, 2) if result == 'over' else 0.0
                row.update(duration=duration, verdict=result, over_by=over_by)
        rows.append(row)
    return rows


def stretch(source, percent, ffmpeg, dest):
    """Speed `source` up by `percent` (FFmpeg atempo), writing 16-bit PCM to `dest`."""
    tempo = f'atempo={1 + percent / 100:g}'
    argv = [ffmpeg, '-hide_banner', '-loglevel', 'error', '-y', '-i', str(source),
            '-filter:a', tempo, '-c:a', 'pcm_s16le', str(dest)]
    result = subprocess.run(argv, capture_output=True, text=True)
    if result.returncode != 0:
        raise AudioError(f'FFmpeg failed: {(result.stderr or "").strip().splitlines()[-1:] or "no output"}')
    return Path(dest)
