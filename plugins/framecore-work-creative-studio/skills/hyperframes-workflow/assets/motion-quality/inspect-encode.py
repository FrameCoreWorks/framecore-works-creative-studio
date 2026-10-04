#!/usr/bin/env python3
"""Inspect an existing local encode. No downloads, rendering services or quality verdicts."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess


def inspect(video, destination):
    video = Path(video).resolve(strict=True)
    if not video.is_file():
        raise ValueError("Input must be an existing local media file")
    ffprobe, ffmpeg = shutil.which("ffprobe"), shutil.which("ffmpeg")
    if not ffprobe or not ffmpeg:
        raise RuntimeError("Existing ffprobe and ffmpeg required; this script installs nothing")
    # Refuse replacement so earlier review evidence remains recoverable.
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=False)
    result = subprocess.run(
        [ffprobe, "-protocol_whitelist", "file,pipe", "-v", "error", "-count_frames", "-show_streams", "-show_format",
         "-of", "json", str(video)], capture_output=True, text=True, check=True)
    probe = json.loads(result.stdout)
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
    # Avoid embedding the machine-specific source pathname from ffprobe.
    evidence["probe"].get("format", {}).pop("filename", None)
    (destination / "evidence.json").write_text(json.dumps(evidence, indent=2) + "\n")
    return {"frames": count, "sample_count": len(frames), "evidence": str(destination / "evidence.json")}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", help="Existing local file, never a remote URL")
    parser.add_argument("destination", help="New review directory; must not already exist")
    args = parser.parse_args()
    try:
        print(json.dumps(inspect(args.video, args.destination), indent=2))
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Inspection failed: {error}\n")
