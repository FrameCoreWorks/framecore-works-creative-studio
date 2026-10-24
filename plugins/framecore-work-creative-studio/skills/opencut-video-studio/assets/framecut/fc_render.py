"""Compile one FrameCut timeline; cache bounded media stages and publish verified bundles."""
from __future__ import annotations

import copy
import json
import os
import re
import shutil
import tempfile
import time
from fractions import Fraction
from pathlib import Path

from fc_core import (FrameCutError, VERSION, atomic_json, confined, confined_output, event_start, file_hash, fingerprint,
                     identifier, integer, ratio, read_json, require, round_boundary, source_clock, span_seconds, validate)
from fc_media import capabilities, ffmpeg, probe, run
from fc_captions import ass_document, caption_font_warnings, project_captions, sidecars


def decimal(value):
    return f"{float(value):.12f}".rstrip("0").rstrip(".") or "0"


def tempo_filters(speed):
    """atempo stages for a constant speed. ffmpeg's atempo moves content about 20 ms early even at 1.0, so none is added at 1x."""
    filters, remaining = [], float(speed)
    while remaining > 2:
        filters.append("atempo=2"); remaining /= 2
    while remaining < .5:
        filters.append("atempo=0.5"); remaining *= 2
    if abs(remaining - 1) > 1e-9:
        filters.append(f"atempo={remaining}")
    return filters


def compile_project(project, root, deliverable_id):
    validate(project, root, True)
    d = next((x for x in project["deliverables"] if x["id"] == deliverable_id), None)
    require(d is not None, "Unknown deliverable")
    seq = next(x for x in project["sequences"] if x["id"] == d["sequence"])
    fps = ratio(seq["fps"])
    warnings = []
    for event in [*seq["clips"], *seq.get("overlays", []), *seq.get("audio", [])]:
        asset = project["assets"][event["asset"]]
        require(asset["probe"].get("color_transfer") not in ("smpte2084", "arib-std-b67"),
                "HDR input needs an explicit tested SDR conform before editing; no silent tone mapping", "unsupported_operation")
        if asset["probe"].get("color_transfer", "unknown") == "unknown" and asset["kind"] != "audio":
            warnings.append({"code": "unlabelled_color", "asset": event["asset"], "handling": "treated as SDR; inspect the output"})
        if "motion_contract" in asset:
            ref = asset["motion_contract"]
            contract_path = confined(root, ref["path"], True)
            require(file_hash(contract_path) == ref["sha256"], "Motion contract changed", "stale_source")
            require(ref.get("fps") == seq["fps"], "Motion composition FPS differs from sequence", "invalid_input")
            if "request" not in ref:
                warnings.append({"code": "unbound_motion", "asset": event["asset"], "message": "Rebind legacy motion with a checked request before final"})
            else:
                request = ref["request"]
                require(request["project_id"] == project["id"] and request["sequence_id"] == seq["id"] and
                        request["event_id"] == event["id"] and request["global_start_frame"] == event_start(event, seq) and
                        request["duration_frames"] == event["duration"] and request["fps"] == seq["fps"] and
                        request["width"] == d["width"] and request["height"] == d["height"] and
                        request["alpha"] == event.get("alpha", "opaque") and
                        event.get("source_in", asset["probe"]["start_pts"]) == asset["probe"]["start_pts"] and
                        ratio(event.get("speed", {"num": 1, "den": 1})) == 1 and not event.get("speed_curve") and not event.get("freeze"),
                        "Motion placement/format changed; request and bind a revised composition", "stale_revision")
    projection = project_captions(project, seq)
    warnings += projection["warnings"]
    warnings += caption_font_warnings(project, seq, projection)
    ass, layout = ass_document(project, seq, d, projection)
    warnings += layout
    if seq.get("captions", {}).get("enabled") and not projection["groups"]:
        warnings.append({"code": "captions_without_timing", "message": "No usable source transcript is bound to this edit"})
    mapping = []
    for c in seq["clips"]:
        a = project["assets"][c["asset"]]
        start, length = span_seconds(a, c, fps)
        mapping.append({"clip": c["id"], "asset": c["asset"], "source_hash": a["sha256"], "source_in_pts": c.get("source_in", a["probe"]["start_pts"]),
                        "time_base": a["probe"]["time_base"], "source_seconds": [str(start), str(start + length)],
                        "timeline_frames": [c["start"], c["start"] + c["duration"]], "speed": c.get("speed", {"num": 1, "den": 1}), "speed_curve": c.get("speed_curve"), "freeze": c.get("freeze", False), "source_remainder": c.get("source_remainder", {"num":0,"den":1})})
    return {"engine": VERSION, "project_id": project["id"], "project_revision": project["revision"], "project_hash": fingerprint(project),
            "sequence": copy.deepcopy(seq), "deliverable": copy.deepcopy(d), "duration_seconds": str(Fraction(seq["duration"]) / fps),
            "audio_samples": round_boundary(Fraction(seq["duration"]) / fps * 48000), "rounding": "nearest, ties away from zero",
            "source_map": mapping, "captions": projection, "warnings": warnings, "ass": ass,
            "composition_authority": "FrameCut FFmpeg; external motion is a bounded local-time media layer"}


def motion_request(project, seq, event, delivery):
    """Projection for Motion Graphics, not a second editable global timeline."""
    identifier(event["id"])
    start = integer(event_start(event, seq), "motion start")
    duration = integer(event["duration"], "motion duration", 1)
    require(start + duration <= seq["duration"], "Motion request exceeds sequence")
    require(event.get("alpha", "opaque") in ("opaque", "straight"), "Unsupported alpha convention")
    return {"schema_version": 1, "owner": "hyperframes-workflow", "project_id": project["id"], "project_revision": project["revision"],
            "sequence_id": seq["id"], "event_id": event["id"], "global_start_frame": event_start(event, seq),
            "local_start_frame": 0, "duration_frames": event["duration"], "fps": seq["fps"],
            "width": delivery["width"], "height": delivery["height"], "alpha": event.get("alpha", "opaque"),
            "color": "SDR bt709", "deliver": "Rendered local composition plus motion-score JSON and SHA-256; ingest both, then attach at the existing event.",
            "project_hash": fingerprint(project), "sequence_hash": fingerprint(seq), "deliverable_id": delivery["id"],
            "deliverable_hash": fingerprint(delivery), "brief_hash": fingerprint(project.get("brief", {})),
            "brief": event.get("note", project.get("brief", {}))}


def bind_motion(project, root, asset_id, contract_relative, fps, request):
    """Validate a returned composition against its immutable originating request before mutation."""
    require(request.get("project_id") == project["id"], "Motion request belongs to another project", "stale_revision")
    revision = integer(request["project_revision"], "request revision", 1)
    require(revision <= project["revision"], "Motion request is from a future revision", "stale_revision")
    baseline = project if revision == project["revision"] else read_json(confined(root, f".framecut/{project['id']}/history/r{revision}.json", True))
    require(request["project_hash"] == fingerprint(baseline), "Motion request baseline differs", "stale_revision")
    seq = next(s for s in project["sequences"] if s["id"] == request["sequence_id"])
    d = next(d for d in project["deliverables"] if d["id"] == request["deliverable_id"])
    baseline_seq = next(s for s in baseline["sequences"] if s["id"] == seq["id"])
    baseline_d = next(d for d in baseline["deliverables"] if d["id"] == request["deliverable_id"])
    require(request["sequence_hash"] == fingerprint(baseline_seq) == fingerprint(seq) and
            request["deliverable_hash"] == fingerprint(baseline_d) == fingerprint(d) and
            request["brief_hash"] == fingerprint(baseline.get("brief", {})) == fingerprint(project.get("brief", {})),
            "Motion context changed; issue a fresh request", "stale_revision")
    require(request.get("local_start_frame") == 0 and request["fps"] == seq["fps"] and
            (request["width"], request["height"]) == (d["width"], d["height"]), "Invalid motion request geometry")
    start = integer(request["global_start_frame"], "motion start")
    frames = integer(request["duration_frames"], "motion duration", 1)
    require(start + frames <= seq["duration"], "Motion request exceeds sequence")
    require(request["alpha"] in ("opaque", "straight"), "Unsupported alpha convention")
    asset = project["assets"][asset_id]
    media = confined(root, asset["path"], True)
    require(file_hash(media) == asset["sha256"], "Motion media changed", "stale_source")
    p = probe(media)
    require(p["kind"] == "video" and Fraction(p["fps"]) == fps == ratio(request["fps"]) and
            (p["width"], p["height"]) == (request["width"], request["height"]), "Motion media FPS/dimensions differ from request", "qa_failed")
    require(request["alpha"] != "straight" or p.get("has_alpha"), "Motion media has no requested alpha", "qa_failed")
    counted, _ = run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames", "-of", "json", str(media)], 300)
    require(int(json.loads(counted)["streams"][0]["nb_read_frames"]) == frames and
            abs(Fraction(str(p["duration"])) * fps - frames) < Fraction(1, 2), "Motion media duration differs from request", "qa_failed")
    contract = confined(root, contract_relative, True)
    require(isinstance(read_json(contract), dict), "Motion authoring contract must be a JSON object")
    return {"path": contract_relative, "sha256": file_hash(contract), "fps": request["fps"], "request": copy.deepcopy(request)}


class Cache:
    def __init__(self, root, project_id, environment, timeout):
        self.root = confined(root, f".framecut/{project_id}/cache")
        self.root.mkdir(parents=True, exist_ok=True)
        self.environment = environment
        self.timeout = timeout
        self.hits, self.built = [], []
        self.watched = {}

    def watch(self, root, project):
        """Remember each source's size and mtime so a file swapped mid-render cannot be stored as that source's stage."""
        for asset in project["assets"].values():
            path = confined(root, asset["path"], True)
            info = path.stat()
            self.watched[path] = (info.st_size, info.st_mtime_ns)

    def unchanged(self):
        for path, seen in self.watched.items():
            info = path.stat()
            require((info.st_size, info.st_mtime_ns) == seen, f"Source changed during the render: {path.name}", "stale_source")

    def stage(self, label, settings, suffix, build):
        from fc_jobs import checkpoint
        checkpoint("cache:"+label)
        key = fingerprint({"engine": VERSION, "stage": label, "settings": settings, "environment": self.environment})
        path = self.root / (key + suffix)
        receipt = self.root / (key + ".json")
        if path.is_file() and receipt.is_file() and not path.is_symlink() and not receipt.is_symlink():
            meta = read_json(receipt)
            if meta.get("sha256") == file_hash(path):
                self.hits.append(label)
                return path
        require(not path.is_symlink() and not receipt.is_symlink(), "Cache symlink rejected")
        # A crashed stage has no valid receipt. Its owned temporary directory can be discarded.
        with tempfile.TemporaryDirectory(prefix="stage-", dir=self.root) as tmp:
            output = Path(tmp) / ("media" + suffix)
            build(output)
            self.unchanged()
            require(output.is_file() and output.stat().st_size > 0, "Stage produced no media", "render_failed")
            info = probe(output)
            meta = {"sha256": file_hash(output), "bytes": output.stat().st_size, "probe": info, "stage": label, "key": key}
            os.replace(output, path)
            atomic_json(receipt, meta, overwrite=True)
        self.built.append(label)
        return path


def video_clip(root, asset, event, d, fps, cache, alpha=False):
    w, h = d["width"], d["height"]
    settings = {"source": asset["sha256"], "probe": asset["probe"], "event": {k: v for k, v in event.items() if k not in ("start", "anchor", "note", "gain_db", "mute", "transition", "bus")},
                "width": w, "height": h, "fps": str(fps), "fit": event.get("fit", d.get("fit", "contain")), "alpha": alpha}
    from fc_picture import encode_clip
    settings["framing"] = d.get("framing", {}).get(event["id"], {})
    return cache.stage("visual", settings, ".mov" if alpha else ".mp4",
                       lambda out: encode_clip(root, asset, event, d, fps, out, cache.timeout, alpha))


def base_picture(root, project, seq, d, cache):
    fps = ratio(seq["fps"])
    items, end = [], 0
    def blank(length):
        return cache.stage("gap", {"length": length, "fps": str(fps), "d": [d['width'], d['height']], "color": seq.get("background", "#000000")}, ".mp4",
                           lambda out: ffmpeg(["-f", "lavfi", "-i", f"color=c={seq.get('background','#000000')}:s={d['width']}x{d['height']}:r={fps}",
                                               "-frames:v", str(length), "-an", "-vf", "scale=in_color_matrix=bt601:out_color_matrix=bt709:out_range=tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv444p", str(out)], cache.timeout))
    for clip in seq["clips"]:
        if clip["start"] > end:
            items.append((blank(clip["start"]-end), end, clip["start"]-end, 0))
        items.append((video_clip(root, project["assets"][clip["asset"]], clip, d, fps, cache), clip["start"], clip["duration"], clip.get("transition", 0)))
        end = clip["start"] + clip["duration"]
    if end < seq["duration"]:
        items.append((blank(seq["duration"] - end), end, seq["duration"] - end, 0))
    if len(items) == 1:
        return items[0][0]
    settings = {"items": [(file_hash(p), start, length, overlap) for p, start, length, overlap in items], "fps": str(fps), "cfr_crossfade": 1}
    def build(out):
        args, graph = [], []
        for i, (p, _, _, _) in enumerate(items):
            args += ["-i", str(p)]
            graph.append(f"[{i}:v]settb=AVTB,setpts=PTS-STARTPTS[v{i}]")
        last = "v0"
        for i, (_, start, _, overlap) in enumerate(items[1:], 1):
            label = f"join{i}"
            if overlap:
                # setpts/concat may clear frame-rate metadata in FFmpeg 7. Normalize
                # both already-timed streams, including a preceding cut, for xfade.
                graph.append(f"[{last}]fps={fps},settb=AVTB[fadeleft{i}]")
                graph.append(f"[v{i}]fps={fps},settb=AVTB[faderight{i}]")
                graph.append(f"[fadeleft{i}][faderight{i}]xfade=transition=fade:duration={decimal(Fraction(overlap)/fps)}:offset={decimal(Fraction(start)/fps)}[{label}]")
            else:
                graph.append(f"[{last}][v{i}]concat=n=2:v=1:a=0[{label}]")
            last = label
        ffmpeg([*args, "-filter_complex", ";".join(graph), "-map", f"[{last}]", "-an", "-r", str(fps), "-frames:v", str(seq["duration"]),
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv444p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", str(out)], cache.timeout)
    return cache.stage("assembly", settings, ".mp4", build)


def audio_events(project, seq):
    events = []
    for i, c in enumerate(seq["clips"]):
        if not c.get("mute") and not c.get("freeze") and project["assets"][c["asset"]]["probe"].get("has_audio"):
            event = copy.deepcopy(c)
            event["_fade_in_frames"] = c.get("transition", 0)
            event["_fade_out_frames"] = seq["clips"][i+1].get("transition", 0) if i+1 < len(seq["clips"]) else 0
            events.append(event)
    events.extend(copy.deepcopy(seq.get("audio", [])))
    return [e for e in events if not e.get("mute")]


DEFAULT_DUCK_DB = -6
DUCK_ATTACK, DUCK_RELEASE, DUCK_HOLD = 0.15, 0.4, 0.5


def speech_intervals(project, seq):
    """Where each clip's own timed transcript has speech, as (start, end) seconds on the timeline with ramp room around each phrase.

    Phrases closer than DUCK_HOLD merge so music does not pump between words. A clip with a transcript but no words in range maps
    to an empty list (no speech). A clip without a timed transcript is absent: the caller falls back to the clip's whole extent."""
    from fc_captions import project_captions
    fps = float(ratio(seq["fps"]))
    spans = {}
    for word in project_captions(project, {**seq, "captions": {}})["words"]:
        spans.setdefault(word["clip"], []).append((word["start"] / fps, word["end"] / fps))
    result = {}
    for clip in seq["clips"]:
        analysis = project["analyses"].get(clip["asset"])
        if not (analysis and (analysis.get("words") or analysis.get("segments"))):
            continue
        merged = []
        for start, end in sorted(spans.get(clip["id"], [])):
            start, end = start - DUCK_ATTACK, end + DUCK_RELEASE
            if merged and start - merged[-1][1] <= DUCK_HOLD:
                merged[-1][1] = max(merged[-1][1], end)
            else:
                merged.append([start, end])
        result[clip["id"]] = [(max(0.0, a), b) for a, b in merged]
    return result


def duck_gain(intervals, amplitude, offset):
    """ffmpeg volume expression: smooth ramps down to `amplitude` inside each interval, 1 elsewhere. Intervals must not overlap."""
    terms = []
    for a, b in intervals:
        a, b = a - offset, b - offset
        terms.append(f"clip(min((t-({decimal(a)}))/{DUCK_ATTACK},(({decimal(b)})-t)/{DUCK_RELEASE}),0,1)")
    return f"volume='1-(1-{amplitude})*({'+'.join(terms)})':eval=frame"


def soundtrack(root, project, seq, d, cache):
    fps = ratio(seq["fps"])
    samples = round_boundary(Fraction(seq["duration"]) / fps * 48000)
    events = audio_events(project, seq)
    settings = {"events": [{**e, "resolved_start": event_start(e, seq)} for e in events],
                "assets": {e["asset"]: {"sha256": project["assets"][e["asset"]]["sha256"], "probe": project["assets"][e["asset"]]["probe"]} for e in events},
                "fps": str(fps), "samples": samples, "lufs": d.get("lufs"), "duck_default": DEFAULT_DUCK_DB,
                "speech": speech_intervals(project, seq)}
    def build(out):
        args = ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
        graph, outputs = [f"[0:a]atrim=end_sample={samples},asetpts=PTS-STARTPTS[silence]"], ["[silence]"]
        speech = settings["speech"]
        dialogue = []
        for e in events:
            if e.get("bus", "dialogue") != "dialogue":
                continue
            if e["id"] in speech:
                dialogue += speech[e["id"]]
            else:
                dialogue.append((float(Fraction(event_start(e, seq)) / fps), float(Fraction(event_start(e, seq) + e["duration"]) / fps)))
        dialogue.sort()
        gap = 0.0
        while True:
            merged = []
            for a, b in dialogue:
                if merged and a <= merged[-1][1] + gap:
                    merged[-1][1] = max(merged[-1][1], b)
                else:
                    merged.append([a, b])
            if len(merged) <= 400:  # keeps the filter expression bounded for very long talks
                break
            gap = max(1.0, gap * 2)
        dialogue = [tuple(x) for x in merged]
        for i, e in enumerate(events, 1):
            asset = project["assets"][e["asset"]]
            if e.get("speed_curve"):
                from fc_audio import varispeed
                path = varispeed(root, asset, e, fps, cache)
                asset = {"path": str(path.relative_to(Path(root))), "probe": probe(path)}
                e = copy.deepcopy(e)
                e.pop("speed_curve", None); e.pop("source_remainder", None)
                e["source_in"] = asset["probe"]["start_pts"]
            args += ["-copyts", "-protocol_whitelist", "file,pipe", "-i", str(confined(root, asset["path"], True))]
            relative, length = span_seconds(asset, e, fps)
            _, origin = source_clock(asset)
            start_seconds = origin + relative
            speed = ratio(e.get("speed", {"num": 1, "den": 1}))
            duration = Fraction(e["duration"]) / fps
            n = round_boundary(duration * 48000)
            start_samples = round_boundary(Fraction(event_start(e, seq)) / fps * 48000)
            filters = [f"atrim=start={decimal(start_seconds)}:duration={decimal(length)}", "asetpts=PTS-STARTPTS"]
            filters += [*tempo_filters(speed), "aresample=48000", "aformat=channel_layouts=stereo"]
            audio_stream = next(s for s in asset["probe"]["streams"] if s["index"] == asset["probe"]["audio_index"])
            offset = max(Fraction(0), Fraction(audio_stream.get("start_time", "0")) - start_seconds) / speed
            if offset:
                filters.append(f"adelay={round_boundary(offset*48000)}S:all=1")
            filters += [f"apad=whole_len={n}", f"atrim=end_sample={n}", f"volume={e.get('gain_db',0)}dB"]
            from fc_audio import gain_expression
            from fc_effects import audio_filters
            gain = gain_expression(e, fps)
            if gain:
                filters.append(gain)
            # Picture effects stay on picture; independent audio owns audio effects.
            if e in seq.get("audio", []) or e.get("id") in {a["id"] for a in seq.get("audio", [])}:
                filters.extend(audio_filters(e.get("effects", [])))
            for direction, frames in (("in", e.get("_fade_in_frames", 0)), ("out", e.get("_fade_out_frames", 0))):
                fade = max(float(Fraction(frames) / fps), e.get("fade", 0))
                if fade:
                    filters.append(f"afade=t={direction}:st={0 if direction=='in' else decimal(duration-Fraction(str(fade)))}:d={fade}")
            duck = e.get("duck_db", DEFAULT_DUCK_DB)
            if e.get("bus") == "music" and duck < 0 and dialogue:
                # Smooth ramps follow the speech, not the whole clip; duck_db 0 keeps the music level.
                filters.append(duck_gain(dialogue, round(10 ** (duck / 20), 4), float(Fraction(event_start(e, seq)) / fps)))
            filters.append(f"adelay={start_samples}S:all=1")
            graph.append(f"[{i}:{asset['probe']['audio_index']}]" + ",".join(filters) + f"[a{i}]")
            outputs.append(f"[a{i}]")
        graph.append("".join(outputs) + f"amix=inputs={len(outputs)}:normalize=0:dropout_transition=0,atrim=end_sample={samples},alimiter=limit=0.95:level=0:latency=1[mix]")
        filters = ";".join(graph)
        intermediate = out.with_name("unmastered.wav")
        ffmpeg([*args, "-filter_complex", filters, "-map", "[mix]", "-c:a", "pcm_s24le", str(intermediate)], cache.timeout)
        target = d.get("lufs")
        if target is None:
            os.replace(intermediate, out)
        else:
            _, log = run(["ffmpeg", "-hide_banner", "-nostdin", "-i", str(intermediate), "-af", f"loudnorm=I={target}:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], cache.timeout)
            matches = re.findall(r"\{\s*\"input_i\".*?\}", log, re.S)
            require(matches, "Loudness measurement unavailable", "qa_failed")
            measured = json.loads(matches[-1])
            if measured["input_i"] == "-inf":
                os.replace(intermediate, out)  # Silence is reported as silence, never a measured target match.
            else:
                params = f"loudnorm=I={target}:TP=-1.5:LRA=11:linear=true:measured_I={measured['input_i']}:measured_TP={measured['input_tp']}:measured_LRA={measured['input_lra']}:measured_thresh={measured['input_thresh']}:offset={measured['target_offset']}"
                ffmpeg(["-i", str(intermediate), "-af", params + f",aresample=48000,apad=whole_len={samples},atrim=end_sample={samples}", "-c:a", "pcm_s24le", str(out)], cache.timeout)
    return cache.stage("mix", settings, ".wav", build)


def verify_video(path, seq, d, timeout=300):
    p = probe(path)
    fps = ratio(seq["fps"])
    require(p.get("width") == d["width"] and p.get("height") == d["height"], "Output dimensions differ", "qa_failed")
    require(Fraction(p["fps"]) == fps, "Output frame rate differs", "qa_failed")
    out, _ = run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames", "-of", "json", str(path)], timeout)
    frames = int(json.loads(out)["streams"][0]["nb_read_frames"])
    require(frames == seq["duration"], f"Expected {seq['duration']} frames, decoded {frames}", "qa_failed")
    _, errors = run(["ffmpeg", "-nostdin", "-v", "error", "-xerror", "-i", str(path), "-f", "null", "-"], timeout)
    require(not errors.strip(), "Output decode errors", "qa_failed")
    require(p["has_audio"], "Expected mixed audio track missing", "qa_failed")
    audio = next(s for s in p["streams"] if s["codec_type"] == "audio")
    expected = float(Fraction(seq["duration"]) / fps)
    require(abs(float(audio.get("duration", expected))-expected) <= max(1024/48000, 1/float(fps)) + .002,
            "Audio duration differs from picture", "qa_failed")
    _, loud = run(["ffmpeg", "-hide_banner", "-nostdin", "-i", str(path), "-vn", "-af", "loudnorm=print_format=json", "-f", "null", "-"], timeout)
    measurements = re.findall(r"\{\s*\"input_i\".*?\}", loud, re.S)
    measurement = json.loads(measurements[-1]) if measurements else None
    if d.get("lufs") is not None and measurement and measurement["input_i"] != "-inf":
        require(abs(float(measurement["input_i"])-d["lufs"]) <= 1.5, "Delivered loudness outside target tolerance", "qa_failed")
        require(float(measurement["input_tp"]) <= -.5, "Delivered audio exceeds true peak ceiling", "qa_failed")
    return {"status": "PASS", "decoded_frames": frames, "probe": p, "loudness": measurement,
            "review": "Technical verification only; actual picture, joins, speech meaning and sound need scoped review."}


def take_lock(lock, root, project):
    """Create the per-project render lock. A lock whose recorded owner process is provably gone is reclaimed; any other is reported with its facts."""
    from fc_jobs import job_identity, process_token
    for attempt in (0, 1):
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError:
            try:
                owner = json.loads(lock.read_text())
            except (OSError, ValueError):
                owner = {}
            pid, token = owner.get("pid"), owner.get("process_token")
            gone = type(pid) is int and token is not None and process_token(pid) != token
            if gone and attempt == 0:
                lock.unlink(missing_ok=True)
                continue
            age = round(time.time() - lock.stat().st_mtime) if lock.exists() else 0
            state = "its owner process is gone" if gone else "its owner is still running" if token is not None else "its owner cannot be checked on this system"
            raise FrameCutError("busy", f"A render holds {lock.relative_to(Path(root).resolve()).as_posix()} (pid {pid}, {age} s old; {state}). "
                                "Remove the file only after confirming no render of this project is running.") from None
        os.write(fd, json.dumps({"pid": os.getpid(), "process_token": process_token(os.getpid()), "project_hash": fingerprint(project),
                                 "job": job_identity()}).encode())
        os.close(fd)
        return


FATAL_WARNINGS = {"clipped_word", "partial_segment", "subframe_word", "kinetic_requires_word_timing", "captions_without_timing",
                  "caption_layout_overflow", "caption_text_collision", "unbound_motion", "font_missing_glyphs"}


def final_blockers(warnings, seq):
    """Warnings that stop a final. A spoken word with no time is dropped from captions, so it blocks whenever captions are on."""
    captions_on = bool(seq.get("captions", {}).get("enabled"))
    return [w for w in warnings if w["code"] in FATAL_WARNINGS or (captions_on and w["code"] == "unknown_timing")]


def blocker_detail(blockers):
    """Codes with a few concrete locations, so the agent can name the cue or word to repair."""
    parts = []
    for code in sorted({w["code"] for w in blockers}):
        examples = [w for w in blockers if w["code"] == code][:3]
        where = "; ".join(str(w.get("text") or w.get("word") or w.get("event") or w.get("clip") or "")[:60] + (f" @frame {w['start']}" if "start" in w else "")
                          for w in examples).strip("; ")
        parts.append(code + (f" ({where})" if where else ""))
    return ", ".join(parts)


def render(project, root, deliverable_id, out_relative, mode="preview", timeout=600, max_disk_mb=2048):
    plan = compile_project(project, root, deliverable_id)
    seq, d = plan["sequence"], plan["deliverable"]
    blockers = final_blockers(plan["warnings"], seq)
    if mode == "final":
        require(project.get("authorization"), "Record the user's existing instruction covering this final", "authorization_missing")
        require(not blockers, f"Resolve caption/meaning/layout warnings before final ({d['id']}): " + blocker_detail(blockers), "qa_failed")
    output = confined_output(root, out_relative)
    require(not output.exists(), "Output directory already exists; use a new revision path")
    require(output != Path(root).resolve(), "Cannot overwrite project root")
    require(max_disk_mb >= 64 and shutil.disk_usage(Path(root)).free >= max_disk_mb * 1024**2, "Insufficient free disk for requested budget", "resource_limit")
    env = capabilities()
    from fc_effects import catalogue_info
    env["effect_catalogue_hash"] = catalogue_info()["catalogue_hash"]
    env["adapter_hash"] = fingerprint({p.name: file_hash(p) for p in Path(__file__).parent.glob('*.py')})
    if shutil.which("fc-match"):
        font_file = run(["fc-match", "-f", "%{file}", seq.get("captions", {}).get("font", "DejaVu Sans")], 10)[0].strip()
        if Path(font_file).is_file():
            env["font"] = {"requested": seq.get("captions", {}).get("font", "DejaVu Sans"), "sha256": file_hash(font_file)}
    require(env.get("h264_aac"), "FFmpeg with libx264/AAC required", "missing_capability")
    for name in ("ass", "overlay", "xfade", "loudnorm", "amix", "atempo"):
        require(env.get("filters", {}).get(name), f"FFmpeg filter unavailable: {name}", "missing_capability")
    cache = Cache(root, project["id"], env, timeout)
    # Hold a render lock per project; revisions may continue, but publishing is bound to this immutable hash.
    lock = cache.root.parent / "render.lock"
    take_lock(lock, root, project)
    cache.watch(root, project)
    started = time.monotonic()
    try:
        picture = base_picture(root, project, seq, d, cache)
        audio = soundtrack(root, project, seq, d, cache)
        layers = []
        for e in seq.get("overlays", []):
            layer_d = dict(d)
            layer_d["width"] = max(2, round(d["width"] * e["rect"][2] / 2) * 2)
            layer_d["height"] = max(2, round(d["height"] * e["rect"][3] / 2) * 2)
            layers.append((e, video_clip(root, project["assets"][e["asset"]], e, layer_d, ratio(seq["fps"]), cache, e.get("alpha") == "straight")))
        require(sum(p.stat().st_size for p in cache.root.rglob('*') if p.is_file()) <= max_disk_mb * 1024**2,
                "Cache exceeds render disk budget; retain accepted artifacts and explicitly clear unused cache", "resource_limit")
        output.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix=".framecut-render-", dir=output.parent) as tmp:
            work = Path(tmp)
            (work / "captions.ass").write_text(plan["ass"], encoding="utf-8")
            args = ["-i", str(picture), "-i", str(audio)]
            graph = ["[0:v]setpts=PTS-STARTPTS,format=rgba[v0]"]
            last = "v0"
            fps = ratio(seq["fps"])
            for i, (event, layer) in enumerate(layers, 2):
                args += ["-i", str(layer)]
                start, duration = Fraction(event_start(event, seq)) / fps, Fraction(event["duration"]) / fps
                graph.append(f"[{i}:v]setpts=PTS-STARTPTS+{decimal(start)}/TB[o{i}]")
                x, y = round(d["width"]*event["rect"][0]), round(d["height"]*event["rect"][1])
                graph.append(f"[{last}][o{i}]overlay=x={x}:y={y}:format=rgb:eof_action=pass:repeatlast=0:enable='gte(t,{decimal(start)})*lt(t,{decimal(start+duration)})'[v{i}]")
                last = f"v{i}"
            graph.append(f"[{last}]ass=filename=captions.ass,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p[final]")
            ffmpeg([*args, "-filter_complex", ";".join(graph), "-map", "[final]", "-map", "1:a:0", "-frames:v", str(seq["duration"]),
                    "-r", str(fps), "-c:v", "libx264", "-preset", "veryfast" if mode == "preview" else "medium", "-crf", "20" if mode == "preview" else "18",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "video.mp4"], timeout, work)
            from fc_jobs import checkpoint
            checkpoint("verification")
            checks = verify_video(work / "video.mp4", seq, d, timeout)
            subtitles = sidecars(plan["captions"], project.get("brief", {}).get("language", "en"))
            for ext in ("srt", "vtt"):
                (work / f"captions.{ext}").write_text(subtitles[ext], encoding="utf-8")
            atomic_json(work / "caption-qa.json", subtitles["qa"])
            atomic_json(work / "source-map.json", plan["source_map"])
            atomic_json(work / "project.json", project)
            atomic_json(work / "projection.json", {k: v for k, v in plan.items() if k != "ass"})
            # Visual review samples include both sides of each editorial boundary and text/motion entries.
            moments = {0, seq["duration"]-1}
            for event in [*seq["clips"], *seq.get("overlays", []), *seq.get("texts", [])]:
                t = event_start(event, seq)
                moments.update((max(0, t-1), t, min(seq["duration"]-1, t+event["duration"]//2)))
            (work / "review").mkdir()
            for n in sorted(moments)[:100]:
                ffmpeg(["-i", "video.mp4", "-vf", f"select=eq(n\\,{n}),scale=640:-2", "-frames:v", "1", f"review/frame-{n:08d}.jpg"], timeout, work)
            receipt = {"schema_version": 1, "engine": VERSION, "status": "render_complete", "mode": mode,
                       "project_id": project["id"], "project_revision": project["revision"], "project_hash": fingerprint(project),
                       "deliverable": d, "sequence": seq["id"], "technical": checks, "warnings": plan["warnings"],
                       "visual_audio_review": {"status": "NOT_RUN", "note": "Inspect actual media and record scope; encoder success is not acceptance."},
                       "cache_hits": cache.hits, "cache_built": cache.built, "elapsed_seconds": round(time.monotonic()-started, 3),
                       "environment": env, "files": {p.relative_to(work).as_posix(): file_hash(p) for p in work.rglob('*') if p.is_file()}}
            atomic_json(work / "receipt.json", receipt)
            require(not output.exists(), "Output created concurrently")
            from fc_jobs import checkpoint
            checkpoint("publishing")
            validate(project, root, True)
            os.rename(work, output)
        return {"status": "render_complete", "output": out_relative, "receipt": f"{out_relative}/receipt.json", "cache_hits": cache.hits,
                "cache_built": cache.built, "review_status": "NOT_RUN", "warnings": plan["warnings"]}
    finally:
        lock.unlink(missing_ok=True)


def validate_review(evidence):
    require(isinstance(evidence, dict), "Review must be an object")
    require(all(isinstance(evidence.get(k), str) and evidence[k].strip() for k in ("reviewer", "scope", "observations")),
            "Review needs reviewer, actual scope and observations")
    require(evidence.get("outcome") in ("pass", "needs_revision", "blocked"), "Invalid review outcome")
    require(type(evidence.get("audio_heard")) is bool and type(evidence.get("picture_watched")) is bool,
            "Declare what was actually heard/watched")
    require(evidence.get("coverage", "sampled") in ("sampled", "full"), "Review coverage must be sampled or full")
    if evidence.get("audio_intentionally_silent") is not None:
        require(type(evidence["audio_intentionally_silent"]) is bool, "Silent-delivery declaration must be boolean")
    return evidence


def delivery_readiness(review, receipt=None):
    if receipt is not None:
        if receipt.get("mode") != "final":
            return {"status": "PREVIEW_ONLY", "reason": "A preview bundle skips the final gates; render with --mode final to deliver"}
        blocked = sorted({w["code"] for w in receipt.get("warnings", []) if w.get("code") in FATAL_WARNINGS})
        if blocked:
            return {"status": "BLOCKED", "reason": "Receipt carries blocking warnings: " + ", ".join(blocked)}
    if review.get("status") == "NOT_RUN":
        return {"status": "REVIEW_REQUIRED", "reason": "Actual picture/audio review has not been recorded"}
    validate_review(review)
    if review["outcome"] != "pass":
        return {"status": "BLOCKED", "reason": review["outcome"]}
    complete = review.get("coverage") == "full" and review["picture_watched"] and (review["audio_heard"] or review.get("audio_intentionally_silent") is True)
    return {"status": "READY" if complete else "REVIEW_REQUIRED", "reason": "Recorded full review passed" if complete else "Passing sampled/incomplete review does not cover the full film"}


def verify_delivery(project, root, relative):
    folder = confined(root, relative)
    receipt = read_json(folder / "receipt.json")
    require(receipt["project_hash"] == fingerprint(project), "Delivery belongs to a different project revision", "stale_revision")
    for relative_path, expected in receipt["files"].items():
        path = confined(folder, relative_path, True)
        require(file_hash(path) == expected, f"Delivery content changed: {relative_path}", "qa_failed")
    seq = next(s for s in project["sequences"] if s["id"] == receipt["sequence"])
    checks = verify_video(folder / "video.mp4", seq, receipt["deliverable"])
    review = receipt["visual_audio_review"]
    if (folder / "review-evidence.json").exists():
        evidence = read_json(confined(folder, "review-evidence.json", True))
        require(evidence.get("project_hash") == fingerprint(project) and evidence.get("video_hash") == file_hash(folder / "video.mp4"), "Review belongs to stale media", "stale_revision")
        review = evidence["evidence"]
    return {"status": "PASS", "project_revision": project["revision"], "technical": checks,
            "visual_audio_review": review, "delivery_readiness": delivery_readiness(review, receipt),
            "acceptance": "Readiness reflects recorded review, not independent proof or user acceptance"}
