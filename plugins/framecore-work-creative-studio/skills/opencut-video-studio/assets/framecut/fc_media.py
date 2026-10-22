"""Bounded local media inspection and optional, explicitly supplied ASR runtime."""
from __future__ import annotations

import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from fractions import Fraction
from pathlib import Path

from fc_core import (FrameCutError, VERSION, atomic_json, confined, file_hash, fingerprint,
                     identifier, number, require, source_clock)


def run(argv, timeout=300, cwd=None):
    """No shell or remote protocol inputs; kill the whole owned process group on timeout/cancel."""
    require(argv and all(isinstance(x, str) and "\x00" not in x for x in argv), "Invalid process arguments")
    executable = shutil.which(argv[0]) if not Path(argv[0]).is_absolute() else argv[0]
    require(executable is not None and Path(executable).is_file(), f"Missing executable: {Path(argv[0]).name}", "missing_capability")
    with tempfile.TemporaryFile() as stdout, tempfile.TemporaryFile() as stderr:
        proc = subprocess.Popen([str(executable), *argv[1:]], stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr,
                                cwd=cwd, start_new_session=(os.name == "posix"))
        try:
            from fc_jobs import checkpoint
            deadline = time.monotonic() + timeout
            while proc.poll() is None:
                checkpoint()
                if time.monotonic() >= deadline:
                    raise subprocess.TimeoutExpired(argv, timeout)
                if stdout.tell() > 64 * 1024 * 1024 or stderr.tell() > 64 * 1024 * 1024:
                    raise FrameCutError("resource_limit", f"{Path(argv[0]).name} wrote more than 64 MiB of output and was stopped")
                try:
                    proc.wait(timeout=.2)
                except subprocess.TimeoutExpired:
                    pass
        except (subprocess.TimeoutExpired, KeyboardInterrupt, FrameCutError) as stopped:
            if os.name == "posix":
                os.killpg(proc.pid, signal.SIGKILL)
            else:
                proc.kill()
            proc.wait()
            if isinstance(stopped, FrameCutError):
                raise
            if isinstance(stopped, KeyboardInterrupt):
                raise FrameCutError("cancelled", "Child cancelled; no final was published") from None
            raise FrameCutError("resource_limit", f"{Path(argv[0]).name} timed out after {timeout} s; no final was published. "
                                "Raise --timeout for long sources or split the work.") from None
        require(stdout.tell() <= 64 * 1024 * 1024 and stderr.tell() <= 64 * 1024 * 1024,
                "Process evidence exceeds 64 MiB", "resource_limit")
        stdout.seek(0); stderr.seek(0)
        out, err = stdout.read().decode("utf-8", "replace"), stderr.read().decode("utf-8", "replace")
    if proc.returncode:
        raise FrameCutError("render_failed", f"{Path(argv[0]).name} exited {proc.returncode}: {err[-2000:]}")
    return out, err


def ffmpeg(args, timeout=300, cwd=None):
    return run(["ffmpeg", "-hide_banner", "-nostdin", "-v", "warning", "-threads", "2",
                "-filter_threads", "1", "-filter_complex_threads", "1", *args], timeout, cwd)


def probe(path):
    path = Path(path).resolve()
    require(path.is_file() and path.stat().st_size <= 50 * 1024**3, "Missing file or source exceeds 50 GiB", "resource_limit")
    raw = json.loads(run(["ffprobe", "-v", "error", "-protocol_whitelist", "file,pipe", "-show_streams", "-show_format", "-of", "json", str(path)], 60)[0])
    streams = raw.get("streams", [])
    visual = next((s for s in streams if s.get("codec_type") == "video" and not s.get("disposition", {}).get("attached_pic")), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    require(visual or audio, "No playable video or audio stream")
    main = visual or audio
    tb = Fraction(main.get("time_base", "1/1000"))
    duration = float(main.get("duration") or raw.get("format", {}).get("duration") or 0)
    image = bool(visual and path.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff"))
    if image:
        duration = 86400
    require(duration > 0 and duration <= 864000, "Missing duration or source exceeds ten days", "resource_limit")
    start_pts = int(main.get("start_pts", round(float(main.get("start_time", 0)) / float(tb))))
    result = {"kind": "image" if image else "video" if visual else "audio", "duration": duration,
              "time_base": str(tb), "clock": {"num": tb.numerator, "den": tb.denominator}, "start_pts": start_pts,
              "has_audio": bool(audio), "audio_index": audio["index"] if audio else None,
              "video_index": visual["index"] if visual else None, "streams": streams,
              "format_start": raw.get("format", {}).get("start_time", "0"),
              "timestamp_policy": "decode relative to selected stream start; preserve source PTS, never use nominal source frame index"}
    if visual:
        require(0 < visual.get("width", 0) <= 16384 and 0 < visual.get("height", 0) <= 16384,
                "Source picture has no decodable size or exceeds 16K", "resource_limit")
        pix = visual.get("pix_fmt", "")
        result.update(width=visual["width"], height=visual["height"], fps=visual.get("avg_frame_rate", "0/0"),
                      nominal_fps=visual.get("r_frame_rate", "0/0"), sar=visual.get("sample_aspect_ratio", "1:1"),
                      rotation=next((s.get("rotation", 0) for s in visual.get("side_data_list", []) if "rotation" in s), int(visual.get("tags", {}).get("rotate", 0))),
                      has_alpha=("a" in pix and pix not in ("gray", "gray16le", "gray16be")) or pix in ("rgba", "bgra", "argb", "abgr", "pal8"),
                      color_transfer=visual.get("color_transfer", "unknown"), color_space=visual.get("color_space", "unknown"),
                      color_primaries=visual.get("color_primaries", "unknown"), pix_fmt=pix)
    return result


def ingest(root, relative, asset_id, rights="unknown", provenance="user-supplied"):
    identifier(asset_id)
    path = confined(root, relative, True)
    before = path.stat()
    p = probe(path)
    digest = file_hash(path)
    after = path.stat()
    # The stored probe and hash must describe the same bytes.
    require((before.st_size, before.st_mtime_ns) == (after.st_size, after.st_mtime_ns), f"Source changed while it was ingested: {relative}", "stale_source")
    return {"path": relative, "sha256": digest, "kind": p["kind"], "probe": p,
            "rights": rights, "provenance": provenance}


def capabilities():
    result = {"engine": "FrameCut", "version": VERSION, "installs_performed": False, "tools": {}}
    for name in ("ffmpeg", "ffprobe"):
        try:
            out, _ = run([name, "-version"], 10)
            result["tools"][name] = {"status": "installed", "version": out.splitlines()[0]}
        except FrameCutError as e:
            result["tools"][name] = {"status": e.code}
    if result["tools"]["ffmpeg"]["status"] == "installed":
        filters = run(["ffmpeg", "-hide_banner", "-filters"], 10)[0]
        encoders = run(["ffmpeg", "-hide_banner", "-encoders"], 10)[0]
        result["filters"] = {k: bool(re.search(r"\s" + k + r"\s", filters)) for k in
                             ("ass", "overlay", "xfade", "loudnorm", "silencedetect", "select", "amix", "atempo")}
        result["h264_aac"] = all(re.search(r"\s" + k + r"\s", encoders) for k in ("libx264", "aac"))
        result["h264_aac"] = bool(result["h264_aac"])
    try:
        import PIL
        result["pillow"] = {"status": "installed", "version": PIL.__version__}
    except ImportError:
        result["pillow"] = {"status": "missing", "plan": "Install Pillow in the selected local Python environment before native transforms/storyboards."}
    result["features"] = ["timeline-read", "transactional-edits", "preview-frame", "storyboard", "durable-jobs", "keyframes", "variant-framing", "freeze-frame", "speed-curve", "effect-catalogue"]
    result["installation_policy"] = "Use the existing complete inventory and disclose its missing-tool plan; this probe installs nothing."
    return result


def inspect_media(root, asset, out_dir, max_seconds=1800, thumbnails=8):
    """Scene/silence evidence plus timestamped thumbnails; never a semantic/whole-film judgment."""
    source = confined(root, asset["path"], True)
    require(file_hash(source) == asset["sha256"], "Source changed", "stale_source")
    final = Path(out_dir)
    require(not final.exists(), f"Analysis directory already exists: {final.name}")
    final.parent.mkdir(parents=True, exist_ok=True)
    # Built beside the target and renamed at the end, so a failure leaves nothing that blocks a retry.
    folder = Path(tempfile.mkdtemp(prefix=".framecut-analysis-", dir=final.parent))
    try:
        result = _inspect(source, asset, folder, max_seconds, thumbnails)
        os.rename(folder, final)
    except BaseException:
        shutil.rmtree(folder, ignore_errors=True)
        raise
    return result


def _inspect(source, asset, folder, max_seconds, thumbnails):
    length = min(asset["probe"]["duration"], max_seconds)
    result = {"source_hash": asset["sha256"], "engine": f"FrameCut {VERSION} / FFmpeg", "analyzed_seconds": length,
              "partial": length < asset["probe"]["duration"], "scenes": [], "silences": [], "thumbnails": [],
              "limitations": ["Scene/silence detections are candidate signals, not semantic edit decisions.", "Thumbnails prove sampled frames only."]}
    if asset["kind"] == "image":
        length = 1
    if asset["kind"] != "audio":
        _, log = run(["ffmpeg", "-hide_banner", "-nostdin", "-v", "info", "-threads", "2", "-i", str(source),
                      "-t", str(length), "-an", "-vf", "setpts=PTS-STARTPTS,select='gt(scene,0.3)',showinfo", "-f", "null", "-"], max(60, int(length * 3)))
        result["scenes"] = [float(x) for x in re.findall(r"pts_time:([\d.]+)", log)]
        for i in range(1 if asset["kind"] == "image" else thumbnails):
            # The last picture of a short clip can end before the nominal grid point, so stay inside the clip.
            t = 0 if asset["kind"] == "image" else min(max(0, (i + 0.5) * length / thumbnails), max(0, length - 0.15))
            name = f"frame-{i:03d}.jpg"
            ffmpeg(["-ss", str(t), "-i", str(source), "-frames:v", "1", "-vf", "scale=640:-2", str(folder / name)], 45)
            result["thumbnails"].append({"file": name, "source_seconds": t, "sha256": file_hash(folder / name)})
        # Actual decoded PTS, bounded to the analyzed interval, not frame / nominal FPS.
        pts_raw = json.loads(run(["ffprobe", "-v", "error", "-read_intervals", f"%+{length}", "-select_streams", "v:0",
                                 "-show_frames", "-show_entries", "frame=best_effort_timestamp,best_effort_timestamp_time", "-of", "json", str(source)], max(60, int(length * 2)))[0])
        atomic_json(folder / "source-pts.json", pts_raw)
        result["decoded_pts_file"] = "source-pts.json"
    if asset["probe"].get("has_audio"):
        _, log = run(["ffmpeg", "-hide_banner", "-nostdin", "-v", "info", "-threads", "2", "-i", str(source), "-t", str(length),
                      "-map", f"0:{asset['probe']['audio_index']}", "-af", "asetpts=PTS-STARTPTS,silencedetect=noise=-35dB:d=0.35", "-f", "null", "-"], max(60, int(length * 2)))
        silence_start = None
        for field, value in re.findall(r"silence_(start|end):\s*([\d.]+)", log):
            if field == "start":
                silence_start = float(value)
            elif silence_start is not None:
                result["silences"].append({"start": silence_start, "end": float(value)})
                silence_start = None
        if silence_start is not None:
            result["silences"].append({"start": silence_start, "end": length})
    atomic_json(folder / "analysis.json", result)
    return result


def transcript_import(asset, data):
    require(isinstance(data, dict), "Transcript must be an object")
    require(data.get("source_hash", asset["sha256"]) == asset["sha256"], "Transcript source mismatch", "stale_source")
    timing = data.get("timing", "segment")
    require(timing in ("manual", "aligned", "asr_word", "segment", "unknown"), "Unknown timing method")
    result = {"source_hash": asset["sha256"], "engine": data.get("engine", "user import"), "timing": timing,
              "language": data.get("language", "unknown"), "model_hash": data.get("model_hash"),
              "words": [], "segments": [], "limitations": data.get("limitations", [])}
    for field in ("words", "segments"):
        for i, item in enumerate(data.get(field, [])):
            require(isinstance(item, dict) and isinstance(item.get("text", item.get("word")), str), "Invalid transcript item")
            result[field].append({"id": item.get("id", f"{field[0]}{i:06d}"), "text": item.get("text", item.get("word")),
                                  "start": item.get("start"), "end": item.get("end"), "speaker": item.get("speaker"),
                                  "confidence": item.get("confidence"), "verbatim": item.get("text", item.get("word"))})
    require(not result["words"] or timing in ("manual", "aligned", "asr_word"), "Word times require an explicit timing method")
    result["warnings"] = transcript_warnings(result)
    result["fingerprint"] = fingerprint(result)
    return result


GARBAGE = set("\ufffd♪♫♬♩♭♮♯")


def transcript_warnings(result):
    """Signs of a recognition failure, reported as checks to read, never as verdicts."""
    warnings = []
    tokens = [token for item in (result["words"] or result["segments"]) for token in (item["text"] or "").split()]
    if tokens and sum(1 for token in tokens if GARBAGE & set(token)) > 0.2 * len(tokens):
        warnings.append("More than 20 % of the transcript is music notes or unreadable characters: "
                        "the recogniser may have heard music or noise; listen before using it")
    timed = [w for w in result["words"] if isinstance(w["start"], (int, float)) and isinstance(w["end"], (int, float))]
    micro = sum(1 for w in timed if w["end"] - w["start"] < 0.05)
    if micro >= 5 and micro > 0.2 * len(timed):
        warnings.append(f"{micro} of {len(timed)} words last under 0.05 s: word timing is unreliable; check boundaries before kinetic captions")
    lines = [re.sub(r"[\W_]+", "", (s["text"] or "").casefold()) for s in result["segments"]]
    if any(lines[i] and lines[i] == lines[i + 1] == lines[i + 2] for i in range(len(lines) - 2)):
        warnings.append("Three identical segments in a row: a common recognition loop on silence or music; check that stretch")
    return warnings


def model_language_check(model, language):
    """An English-only model (*.en) cannot transcribe another language; refuse before any decoding."""
    if not re.search(r"\.en([.\-_]|$)", Path(model).name):   # also quantized names such as ggml-base.en-q5_1.bin
        return None
    require(language in ("en", "auto"), f"The model {Path(model).name} is English-only and cannot transcribe '{language}'; "
            "choose a multilingual model", "model_language_mismatch")
    return (f"The model {Path(model).name} is English-only and the language is auto: "
            "speech in another language will come out as English guesses") if language == "auto" else None


def transcribe(root, asset, python, model, language="auto", timeout=600, word_times=False):
    require(asset["probe"].get("has_audio"), "Source has no speech/audio stream")
    require(re.fullmatch(r"[a-z]{2,3}|auto", language), "Invalid language code")
    model = Path(model).resolve()
    require(model.is_file(), "ASR model unavailable; no model is downloaded automatically", "model_unavailable")
    language_warning = model_language_check(model, language)
    source = confined(root, asset["path"], True)
    require(file_hash(source) == asset["sha256"], "Source changed", "stale_source")
    with tempfile.TemporaryDirectory(prefix="framecut-asr-") as tmp:
        wav = Path(tmp) / "audio.wav"
        ffmpeg(["-i", str(source), "-map", f"0:{asset['probe']['audio_index']}", "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(wav)], timeout)
        # Fixed worker, not a user-authored Python expression. Explicit runtime can be an isolated environment.
        out, _ = run([str(Path(python).absolute()), str(Path(__file__).resolve()), "asr-worker", str(wav), str(model), language, "words" if word_times else "segments"], timeout)
        data = json.loads(out.strip().splitlines()[-1])
    data.update(model_hash=file_hash(model), source_hash=asset["sha256"])
    result = transcript_import(asset, data)
    if language_warning:
        result["warnings"].append(language_warning)
        result["fingerprint"] = fingerprint({k: v for k, v in result.items() if k != "fingerprint"})
    return result


if __name__ == "__main__":
    if len(sys.argv) != 6 or sys.argv[1] != "asr-worker":
        raise SystemExit("Use framecut.py; this module only exposes a fixed ASR worker.")
    try:
        from pywhispercpp.model import Model
        model = Model(sys.argv[3], context_params={"use_gpu": False}, language=sys.argv[4], n_threads=2,
                      print_progress=False, print_realtime=False, print_timestamps=False)
        segments = model.transcribe(sys.argv[2])
        words = []
        if sys.argv[5] == "words":
            word_segments = model.transcribe(sys.argv[2], token_timestamps=True, max_len=1, split_on_word=True)
            words = [{"start": s.t0 / 100, "end": s.t1 / 100, "text": s.text.strip()}
                     for s in word_segments if s.text.strip() and s.t1 > s.t0]
        print(json.dumps({"engine": "pywhispercpp", "timing": "asr_word" if words else "segment", "language": sys.argv[4], "words": words,
                          "segments": [{"start": s.t0 / 100, "end": s.t1 / 100, "text": s.text.strip()} for s in segments],
                          "limitations": ["Draft ASR: review words/names/meaning. Token word timestamps are estimates, not forced alignment or diarization; inspect boundaries before kinetic delivery."]}, ensure_ascii=False))
    except ImportError:
        raise SystemExit("PyWhisperCpp is absent in the selected Python runtime; use the existing runtime inventory.")
