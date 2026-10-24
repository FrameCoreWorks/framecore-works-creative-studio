"""VoxCPM2 worker: runs only with the plugin's venv interpreter, never with the system Python.

    <venv python> -I voxcpm_worker.py job.json

job.json: {"model": "openbmb/VoxCPM2", "jobs": [{"id", "text", "out", "seed", "reference_wav"?}]}. The model loads
once; each job writes a 16-bit PCM WAV and prints one JSON line {"id", "status", "error"?}. A failed job does not
stop the others. The launcher sets HF_HOME and HF_HUB_OFFLINE, so the weights must already be cached.
"""
import json
import sys


def main(job_path):
    with open(job_path, encoding='utf-8') as handle:
        job = json.load(handle)
    try:
        import soundfile
        from voxcpm import VoxCPM
        model = VoxCPM.from_pretrained(job['model'], load_denoiser=False)
    except Exception as error:  # noqa: BLE001 - report any load failure as one line per job
        for item in job['jobs']:
            print(json.dumps({'id': item['id'], 'status': 'failed', 'error': f'model load failed: {error}'}), flush=True)
        return 1
    failed = 0
    for item in job['jobs']:
        try:
            options = {'text': item['text'], 'cfg_value': 2.0, 'inference_timesteps': 10, 'seed': item.get('seed', 42)}
            if item.get('reference_wav'):
                options['reference_wav_path'] = item['reference_wav']
            wav = model.generate(**options)
            soundfile.write(item['out'], wav, model.tts_model.sample_rate, subtype='PCM_16')
            print(json.dumps({'id': item['id'], 'status': 'ok'}), flush=True)
        except Exception as error:  # noqa: BLE001
            failed += 1
            print(json.dumps({'id': item['id'], 'status': 'failed', 'error': str(error)}), flush=True)
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
