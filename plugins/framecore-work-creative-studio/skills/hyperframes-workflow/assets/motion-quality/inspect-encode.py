#!/usr/bin/env python3
"""Inspect an existing local encode. No downloads, rendering services or quality verdicts."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess

SILENCE_DB = -80.0   # a peak at or below this is inaudible


def peak_db(ffmpeg, video):
    """Peak level of the first audio stream from ffmpeg volumedetect, in dB; None when it reports none."""
    result = subprocess.run([ffmpeg, "-protocol_whitelist", "file,pipe", "-hide_banner", "-nostats", "-i", str(video),
                             "-map", "0:a:0", "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True, check=True)
    match = re.search(r"max_volume:\s*(-?inf|-?[\d.]+) dB", result.stderr)
    if not match:
        return None
    return float("-inf") if "inf" in match.group(1) else float(match.group(1))


def inspect(video, destination, audio=None, cover_time=None):
    video = Path(video).resolve(strict=True)
    if not video.is_file():
        raise ValueError("Input must be an existing local media file")
    ffprobe, ffmpeg = shutil.which("ffprobe"), shutil.which("ffmpeg")
    if not ffprobe or not ffmpeg:
        raise RuntimeError("Existing ffprobe and ffmpeg required; this script installs nothing")
    if audio not in (None, "required", "silent"):
        raise ValueError("audio must be required or silent")
    result = subprocess.run(
        [ffprobe, "-protocol_whitelist", "file,pipe", "-v", "error", "-count_frames", "-show_streams", "-show_format",
         "-of", "json", str(video)], capture_output=True, text=True, check=True)
    probe = json.loads(result.stdout)
    if cover_time is not None:
        duration = float(probe.get("format", {}).get("duration") or 0)
        if not 0 <= cover_time < duration:
            raise ValueError(f"Cover time {cover_time} s is outside the film (0 to {duration} s)")
    # Refuse replacement so earlier review evidence remains recoverable.
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=False)
    streams = [s for s in probe.get("streams", []) if s.get("codec_type") == "video"]
    if not streams:
        raise ValueError("No video stream")
    stream = streams[0]
    count = int(stream.get("nb_read_frames") or stream.get("nb_frames") or 0)
    if count < 1:
        raise ValueError("Decoded frame count unavailable")
    frames = sorted({round(i * (count - 1) / 29) for i in range(30)})
    expression = "+".join(f"eq(n\\,{frame})" for frame in frames)
    # Use decoded frame numbers, not rounded timestamp seeking.
    filters = f"select='{expression}',scale=400:-2,tile=5x6:padding=3:margin=3"
    sheet = destination / "contact-sheet.jpg"
    subprocess.run([ffmpeg, "-protocol_whitelist", "file,pipe", "-hide_banner", "-loglevel", "error", "-i", str(video),
                    "-map", "0:v:0", "-vf", filters, "-fps_mode", "vfr", "-frames:v", "1", str(sheet)],
                   check=True, capture_output=True, text=True)
    with video.open("rb") as source:
        hasher = hashlib.sha256()
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            hasher.update(chunk)
        digest = hasher.hexdigest()
    evidence = {
        "schema_version": 1, "input_filename": video.name, "sha256": digest,
        "probe": probe, "sampled_frame_indices": frames,
        "contact_sheet": sheet.name, "technical_inspection": "metadata_extracted",
        "visual_review": "not_run", "full_temporal_review": "not_run",
        "audio_listening": "not_run",
        "limitation": "Sampling and metadata do not certify typography, pacing, audio or quality."
    }
    failed = []
    if audio:
        streams = sum(1 for s in probe.get("streams", []) if s.get("codec_type") == "audio")
        peak = peak_db(ffmpeg, video) if streams else None
        audible = peak is not None and peak > SILENCE_DB
        passed = audible if audio == "required" else not audible
        evidence["audio_check"] = {"expected": audio, "streams": streams,
                                   "max_volume_db": None if peak is None or peak == float("-inf") else peak,
                                   "result": "PASS" if passed else "FAIL"}
        if not passed:
            failed.append("audio")
    if cover_time is not None:
        subprocess.run([ffmpeg, "-protocol_whitelist", "file,pipe", "-hide_banner", "-loglevel", "error", "-i", str(video),
                        "-ss", str(cover_time), "-map", "0:v:0", "-frames:v", "1", str(destination / "cover.png")],
                       check=True, capture_output=True, text=True)
        evidence["cover"] = {"time": cover_time, "file": "cover.png"}
    # Avoid embedding the machine-specific source pathname from ffprobe.
    evidence["probe"].get("format", {}).pop("filename", None)
    (destination / "evidence.json").write_text(json.dumps(evidence, indent=2) + "\n")
    return {"frames": count, "sample_count": len(frames), "evidence": str(destination / "evidence.json"), "failed_checks": failed}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", help="Existing local file, never a remote URL")
    parser.add_argument("destination", help="New review directory; must not already exist")
    parser.add_argument("--audio", choices=("required", "silent"), help="required: an audible audio stream; silent: none audible")
    parser.add_argument("--cover-time", type=float, help="extract the frame at this time in seconds as cover.png")
    args = parser.parse_args()
    try:
        report = inspect(args.video, args.destination, args.audio, args.cover_time)
        print(json.dumps(report, indent=2))
        if report["failed_checks"]:
            parser.exit(1, f"Failed checks: {', '.join(report['failed_checks'])}\n")
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Inspection failed: {error}\n")
