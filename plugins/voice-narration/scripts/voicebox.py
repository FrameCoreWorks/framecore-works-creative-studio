"""Client for Voicebox's local REST API (reviewed at jamiepine/voicebox 2bcb98d, v0.5.0). Standard library only.

POST /generate starts a generation and returns its id; GET /generate/{id}/status streams its state as server-sent
events until it is completed or failed; GET /audio/{id} serves the audio.
"""
import json
import shutil
import subprocess
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

import audio

DEFAULT_URL = 'http://127.0.0.1:17493'


class VoiceboxError(RuntimeError):
    pass


class VoiceboxClient:
    def __init__(self, base_url=DEFAULT_URL, timeout=600):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout

    def _open(self, path, payload=None):
        data = None if payload is None else json.dumps(payload).encode('utf-8')
        request = urllib.request.Request(self.base_url + path, data=data,
                                         headers={'Content-Type': 'application/json',
                                                  'X-Voicebox-Client-Id': 'voice-narration'})
        try:
            return urllib.request.urlopen(request, timeout=self.timeout)
        except urllib.error.HTTPError as error:
            detail = error.read().decode('utf-8', 'replace')[:200]
            raise VoiceboxError(f'voicebox {path} answered {error.code}: {detail}') from None
        except (OSError, ValueError) as error:
            raise VoiceboxError(f'voicebox {path} unreachable: {error}') from None

    def generate(self, text, profile_id, language, engine=None):
        payload = {'text': text, 'profile_id': profile_id, 'language': language}
        if engine:
            payload['engine'] = engine
        try:
            with self._open('/generate', payload) as response:
                return str(json.loads(response.read())['id'])
        except (OSError, ValueError, KeyError, TypeError) as error:
            raise VoiceboxError(f'voicebox /generate gave an unexpected answer: {error}') from None

    def wait(self, generation_id):
        state = {}
        try:
            with self._open(f'/generate/{generation_id}/status') as response:
                for raw in response:
                    line = raw.decode('utf-8', 'replace').strip()
                    if line.startswith('data:'):
                        state = json.loads(line[5:])
                        if not isinstance(state, dict):
                            raise ValueError('status is not an object')
                        if state.get('status') in ('completed', 'failed', 'not_found'):
                            break
        except (OSError, ValueError) as error:
            raise VoiceboxError(f'voicebox status stream broke: {error}') from None
        return state

    def download(self, generation_id, dest):
        dest = Path(dest)
        try:
            with self._open(f'/audio/{generation_id}') as response:
                body = response.read()
        except OSError as error:
            raise VoiceboxError(f'voicebox audio download broke: {error}') from None
        dest.parent.mkdir(parents=True, exist_ok=True)
        if body[:4] == b'RIFF':
            dest.write_bytes(body)
            try:
                audio.spoken_duration(dest)
                return dest
            except audio.AudioError:
                pass
        return to_pcm_wav(body, dest)


def to_pcm_wav(body, dest):
    ffmpeg = shutil.which('ffmpeg')
    if not ffmpeg:
        raise audio.AudioError('voicebox returned non-WAV audio and FFmpeg is missing')
    with tempfile.NamedTemporaryFile(suffix='.audio', delete=False) as tmp:
        tmp.write(body)
    try:
        result = subprocess.run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-y', '-i', tmp.name,
                                 '-c:a', 'pcm_s16le', str(dest)], capture_output=True, text=True,
                                encoding='utf-8', errors='replace')
    finally:
        Path(tmp.name).unlink(missing_ok=True)
    if result.returncode != 0:
        raise audio.AudioError('FFmpeg could not convert the voicebox audio')
    return Path(dest)
