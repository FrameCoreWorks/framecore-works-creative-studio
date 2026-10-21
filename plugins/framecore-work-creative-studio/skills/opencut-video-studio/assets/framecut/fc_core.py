"""FrameCut's authoritative project, exact time map and immutable revision store."""
from __future__ import annotations

import copy
import hashlib
import json
import math
import os
import re
import tempfile
from contextlib import contextmanager
from fractions import Fraction
from pathlib import Path

VERSION = "1.1.0"
MAX_INTEGER = 2**53 - 1


class FrameCutError(Exception):
    def __init__(self, code, message):
        self.code = code
        super().__init__(message)


def require(condition, message, code="invalid_input"):
    if not condition:
        raise FrameCutError(code, message)


def integer(v, name, low=0, high=MAX_INTEGER):
    require(type(v) is int and low <= v <= high, f"{name}: expected integer {low}..{high}")
    return v


def number(v, name, low, high):
    require(type(v) in (int, float) and math.isfinite(v) and low <= v <= high,
            f"{name}: expected finite number {low}..{high}")
    return v


def identifier(v):
    require(isinstance(v, str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", v), "Invalid stable ID")
    return v


def keys(obj, allowed, required=()):
    require(isinstance(obj, dict), "Expected object")
    require(not (set(obj) - set(allowed)), f"Unknown fields: {sorted(set(obj) - set(allowed))}")
    require(set(required) <= set(obj), f"Missing fields: {sorted(set(required) - set(obj))}")


def ratio(v):
    keys(v, ("num", "den"), ("num", "den"))
    return Fraction(integer(v["num"], "numerator", 1), integer(v["den"], "denominator", 1))


def round_boundary(v):
    """Nearest integer, ties away from zero; exactly one quantization at a boundary."""
    v = Fraction(v)
    return (2 * v.numerator + v.denominator) // (2 * v.denominator) if v >= 0 else -round_boundary(-v)


def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def fingerprint(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()


def file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def confined(root, relative, must_exist=False):
    require(isinstance(relative, str) and relative and "\x00" not in relative and "\\" not in relative,
            "Expected a portable project-relative path")
    p = Path(relative)
    require(not p.is_absolute() and not any(x in (".", "..", "") for x in relative.split("/")), "Path traversal rejected")
    root = Path(root).resolve()
    resolved = (root / p).resolve()
    require(resolved.is_relative_to(root), "Path escapes project root")
    # Reject symlinks even when they happen to point inside: output aliases are ambiguous.
    cursor = root
    for part in p.parts:
        cursor /= part
        require(not cursor.is_symlink(), "Symlink path rejected")
    if must_exist:
        require(resolved.is_file(), f"Missing project file: {relative}")
    return resolved


def read_json(path):
    require(Path(path).stat().st_size <= 16 * 1024 * 1024, "JSON exceeds 16 MiB", "resource_limit")
    def unique(pairs):
        out = {}
        for k, v in pairs:
            require(k not in out, f"Duplicate JSON key: {k}")
            out[k] = v
        return out
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=unique,
                          parse_constant=lambda x: (_ for _ in ()).throw(FrameCutError("invalid_input", f"Invalid number {x}")))
    except (ValueError, UnicodeError) as e:
        raise FrameCutError("invalid_input", str(e)) from e


def atomic_json(path, obj, overwrite=False):
    path = Path(path)
    require(not path.is_symlink(), "Symlink output rejected")
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = canonical(obj) + b"\n"
    fd, tmp = tempfile.mkstemp(prefix=".framecut-write-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(raw)
            f.flush()
            os.fsync(f.fileno())
        if overwrite:
            os.replace(tmp, path)
        else:
            try:
                os.link(tmp, path)
            except FileExistsError as e:
                raise FrameCutError("invalid_input", f"Output already exists: {path.name}") from e
    finally:
        Path(tmp).unlink(missing_ok=True)


def source_clock(asset):
    p = asset["probe"]
    return Fraction(p["time_base"]), Fraction(p["start_pts"]) * Fraction(p["time_base"])


def span_seconds(asset, event, fps):
    tb, origin = source_clock(asset)
    from fc_time import remainder, source_offset
    return Fraction(event.get("source_in", asset["probe"]["start_pts"])) * tb - origin + remainder(event), source_offset(event, event["duration"], fps)


def event_start(event, seq):
    if "anchor" not in event:
        return event["start"]
    keys(event["anchor"], ("clip", "offset"), ("clip", "offset"))
    matches = [c for c in seq["clips"] if c["id"] == event["anchor"]["clip"]]
    require(len(matches) == 1, f"Orphaned anchor: {event['id']}", "missing_anchor")
    return matches[0]["start"] + integer(event["anchor"]["offset"], "anchor offset", -MAX_INTEGER)


def validate(project, root=None, verify_sources=False):
    keys(project, ("schema_version", "id", "revision", "brief", "authorization", "assets", "analyses", "sequences",
                   "deliverables", "locks", "history", "status"), ("schema_version", "id", "revision", "assets", "analyses", "sequences", "deliverables"))
    require(type(project["schema_version"]) is int and project["schema_version"] == 1, "Unsupported schema version")
    identifier(project["id"])
    integer(project["revision"], "revision", 1)
    require(isinstance(project.get("brief", {}), dict), "Brief must be an object")
    locks = project.get("locks", [])
    require(isinstance(locks, list) and all(isinstance(x, str) for x in locks) and len(set(locks)) == len(locks),
            "Locks must be a list of unique clip IDs")
    for lock in locks:
        identifier(lock)
    require(isinstance(project["assets"], dict) and len(project["assets"]) <= 1000, "Invalid asset collection")
    for aid, a in project["assets"].items():
        identifier(aid)
        keys(a, ("path", "sha256", "kind", "probe", "provenance", "rights", "motion_contract"), ("path", "sha256", "kind", "probe"))
        require(a["kind"] in ("video", "image", "audio"), "Unsupported asset kind")
        require(isinstance(a["sha256"], str) and re.fullmatch(r"[a-f0-9]{64}", a["sha256"]), "Invalid asset hash")
        p = a["probe"]
        require(isinstance(p, dict) and ratio(p["clock"]) == Fraction(p["time_base"]), "Invalid source clock")
        integer(p["start_pts"], "source start PTS", -MAX_INTEGER)
        require(Fraction(str(p["duration"])) > 0, "Invalid source duration")
        if root is not None:
            path = confined(root, a["path"], True)
            if verify_sources:
                require(file_hash(path) == a["sha256"], f"Source changed: {aid}", "stale_source")
    require(isinstance(project["analyses"], dict), "Expected analyses object")
    for aid, analysis in project["analyses"].items():
        require(aid in project["assets"] and analysis.get("source_hash") == project["assets"][aid]["sha256"], "Stale analysis", "stale_source")
        units = analysis.get("words", []) or analysis.get("segments", [])
        previous = -math.inf
        ids = set()
        for word in units:
            identifier(word["id"])
            require(word["id"] not in ids, "Duplicate transcript ID")
            ids.add(word["id"])
            require(isinstance(word.get("text"), str) and len(word["text"]) <= 10000, "Invalid transcript text")
            if word.get("start") is None or word.get("end") is None:
                require(word.get("start") is None and word.get("end") is None, "Partial unknown timing")
                continue
            s = number(word["start"], "transcript start", 0, 864000)
            e = number(word["end"], "transcript end", 0, 864000)
            require(e > s and s >= previous, "Unordered transcript interval")
            require(e <= project["assets"][aid]["probe"]["duration"] + 0.1, "Transcript exceeds source")
            previous = s
    require(isinstance(project["sequences"], list) and len(project["sequences"]) <= 100, "Invalid sequences")
    seq_ids = set()
    for seq in project["sequences"]:
        keys(seq, ("id", "fps", "duration", "clips", "audio", "overlays", "texts", "captions", "background", "editorial"), ("id", "fps", "duration", "clips"))
        identifier(seq["id"])
        require(seq["id"] not in seq_ids, "Duplicate sequence ID")
        seq_ids.add(seq["id"])
        fps = ratio(seq["fps"])
        require(1 <= fps <= 120, "FPS outside 1..120")
        integer(seq["duration"], "sequence duration", 1, int(6 * 3600 * fps))
        require(re.fullmatch(r"#[0-9a-fA-F]{6}", seq.get("background", "#000000")), "Invalid background")
        ids = set()
        previous_end = 0
        previous_length = 0
        previous_transition = 0
        for kind in ("clips", "audio", "overlays", "texts"):
            events = seq.get(kind, [])
            require(isinstance(events, list) and len(events) <= 2000, "Too many events", "resource_limit")
            for event in events:
                keys(event, ("id", "asset", "start", "duration", "source_in", "speed", "gain_db", "mute", "fit", "crop", "transition",
                             "anchor", "rect", "alpha", "text", "size", "color", "animation", "position", "fade", "bus", "duck_db", "note", "keyframes", "keyframe_offset", "speed_curve", "freeze", "source_remainder", "effects"),
                     ("id", "duration"))
                identifier(event["id"])
                require(event["id"] not in ids, "Duplicate event ID")
                ids.add(event["id"])
                require(("start" in event) != ("anchor" in event), "Use start or anchor, exactly once")
                if kind == "clips":
                    require("anchor" not in event, "Base clip cannot anchor to another clip")
                start = integer(event_start(event, seq), "event start")
                length = integer(event["duration"], "event duration", 1)
                require(start + length <= seq["duration"], "Event exceeds sequence duration")
                from fc_time import validate_animation, validate_time
                from fc_effects import validate_effects
                validate_animation(event.get("keyframes", {}))
                integer(event.get("keyframe_offset", 0), "keyframe offset", 0, 2592000)
                if kind == "texts":
                    require(not (set(event) & {"speed_curve", "freeze", "source_remainder"}), "Text has no source time map")
                    require(not event.get("effects"), "Text effects require a motion composition")
                    require(not (set(event.get("keyframes", {})) - {"x", "y", "scale", "rotation", "opacity"}), "Unsupported text keyframe")
                    require(isinstance(event.get("text"), str) and 0 < len(event["text"]) <= 2000, "Invalid text event")
                    require(event.get("animation", "fade") in ("none", "fade", "pop"), "Unknown text animation")
                    number(event.get("size", 0.06), "text size", 0.01, 0.3)
                    require(re.fullmatch(r"#[0-9a-fA-F]{6}", event.get("color", "#FFFFFF")), "Invalid text color")
                    require(event.get("position", "center") in ("center", "top", "bottom"), "Invalid text position")
                    continue
                require(event.get("asset") in project["assets"], "Unknown media asset")
                asset = project["assets"][event["asset"]]
                require(kind == "audio" or asset["kind"] != "audio", "Audio cannot be a visual clip")
                require(kind != "audio" or asset["probe"].get("has_audio"), "Audio event has no audio stream")
                integer(event.get("source_in", asset["probe"]["start_pts"]), "source in PTS", -MAX_INTEGER)
                validate_time(event, fps, Fraction(asset["probe"]["time_base"]))
                validate_effects(event.get("effects", []), "audio" if kind == "audio" else "picture")
                if kind == "audio":
                    require(set(event.get("keyframes", {})) <= {"gain_db"}, "Audio supports gain keyframes only")
                    require(not event.get("freeze"), "Use a gap for silent audio; freeze is a picture operation")
                speed = ratio(event.get("speed", {"num": 1, "den": 1}))
                require(Fraction(1, 4) <= speed <= 4, "Speed outside 1/4..4")
                source_in, source_length = span_seconds(asset, event, fps)
                require(source_in >= 0, "Source interval begins before asset")
                if event.get("freeze"):
                    require(source_in < Fraction(str(asset["probe"]["duration"])), "Freeze point must be inside source")
                if asset["kind"] != "image":
                    require(source_in + source_length <= Fraction(str(asset["probe"]["duration"])) + Fraction(1, 1000), "Insufficient source media", "insufficient_handles")
                require(event.get("fit", "contain") in ("contain", "cover"), "Invalid fit")
                if "crop" in event:
                    require(isinstance(event["crop"], list) and len(event["crop"]) == 4, "Crop is [x,y,width,height]")
                    x, y, w, h = [number(v, "crop", 0, 1) for v in event["crop"]]
                    require(w > 0 and h > 0 and x + w <= 1 and y + h <= 1, "Crop outside source")
                number(event.get("gain_db", 0), "gain dB", -90, 24)
                require(type(event.get("mute", False)) is bool, "Mute must be boolean")
                number(event.get("fade", 0), "audio fade seconds", 0, float(Fraction(length, 2) / fps))
                require(event.get("bus", "dialogue") in ("dialogue", "music", "sfx"), "Unknown audio bus")
                number(event.get("duck_db", 0), "duck dB", -60, 0)
                if kind == "clips":
                    overlap = previous_end - start
                    transition = integer(event.get("transition", 0), "transition frames")
                    require(transition == max(0, overlap) and transition < length and transition + previous_transition < previous_length,
                            "Overlap must equal declared transition and leave clip handles") if transition else require(overlap <= 0, "Undeclared base-track overlap")
                    previous_end = start + length
                    previous_length, previous_transition = length, transition
                if kind == "overlays":
                    require(isinstance(event.get("rect"), list) and len(event["rect"]) == 4, "Overlay needs normalized rect [x,y,w,h]")
                    x, y, w, h = [number(v, "overlay rect", 0, 1) for v in event["rect"]]
                    require(w > 0 and h > 0 and x + w <= 1 and y + h <= 1, "Overlay outside canvas")
                    require(event.get("alpha", "opaque") in ("opaque", "straight"), "Unsupported alpha convention")
                    if event.get("alpha") == "straight":
                        require(asset["probe"].get("has_alpha"), "Transparent overlay has no alpha channel")
        cap = seq.get("captions", {})
        keys(cap, ("enabled", "mode", "size", "bottom", "color", "highlight", "max_words", "corrections", "font", "sources"))
        if "sources" in cap:
            valid_sources = {e["id"] for e in [*seq["clips"], *seq.get("audio", [])]}
            require(isinstance(cap["sources"], list) and all(isinstance(v, str) and v in valid_sources for v in cap["sources"]), "Caption sources must name clip/audio events")
        require(type(cap.get("enabled", False)) is bool, "Caption enabled must be boolean")
        require(cap.get("mode", "sentence") in ("sentence", "kinetic"), "Unknown caption mode")
        number(cap.get("size", 0.055), "caption size", 0.01, 0.16)
        number(cap.get("bottom", 0.18), "caption bottom", 0.05, 0.5)
        integer(cap.get("max_words", 6), "caption word group", 1, 12)
        for field in ("color", "highlight"):
            require(re.fullmatch(r"#[0-9a-fA-F]{6}", cap.get(field, "#FFFFFF")), "Invalid caption color")
        require(re.fullmatch(r"[A-Za-z0-9 _-]{1,80}", cap.get("font", "DejaVu Sans")), "Invalid font family")
        require(isinstance(cap.get("corrections", {}), dict) and all(isinstance(v, str) and len(v) <= 10000 for v in cap.get("corrections", {}).values()), "Invalid caption corrections")
    ids = set()
    clip_ids = {c["id"] for s in project["sequences"] for c in s["clips"]}
    require(set(locks) <= clip_ids, "Lock references missing clip")
    for d in project["deliverables"]:
        keys(d, ("id", "sequence", "width", "height", "fit", "captions", "lufs", "safe_top", "safe_bottom", "framing"), ("id", "sequence", "width", "height"))
        identifier(d["id"])
        require(d["id"] not in ids, "Duplicate deliverable ID")
        ids.add(d["id"])
        require(d["sequence"] in seq_ids, "Deliverable references missing sequence")
        for dim in ("width", "height"):
            require(integer(d[dim], dim, 64, 4096) % 2 == 0, "H.264 dimensions must be even")
        require(d.get("fit", "contain") in ("contain", "cover"), "Invalid deliverable fit")
        require(type(d.get("captions", True)) is bool, "Captions must be boolean")
        if d.get("lufs") is not None:
            number(d["lufs"], "LUFS", -30, -9)
        frames = d.get("framing", {})
        require(isinstance(frames, dict), "Framing must map event IDs")
        sequence = next(s for s in project["sequences"] if s["id"] == d["sequence"])
        visual_ids = {e["id"] for lane in ("clips", "overlays") for e in sequence.get(lane, [])}
        require(set(frames) <= visual_ids, "Framing references missing visual event")
        for frame in frames.values():
            keys(frame, ("crop", "fit", "keyframes"))
            require(frame.get("fit", "contain") in ("contain", "cover"), "Invalid framing fit")
            if "crop" in frame:
                require(isinstance(frame["crop"], list) and len(frame["crop"]) == 4, "Invalid framing crop")
                x,y,w,h = [number(v, "crop", 0, 1) for v in frame["crop"]]
                require(w > 0 and h > 0 and x+w <= 1 and y+h <= 1, "Framing crop outside source")
            from fc_time import validate_animation
            validate_animation(frame.get("keyframes", {}))
            require(set(frame.get("keyframes", {})) <= {"zoom", "pan_x", "pan_y", "x", "y", "scale", "rotation", "opacity"}, "Framing cannot change audio")
        number(d.get("safe_top", 0.08), "safe top", 0, 0.4)
        number(d.get("safe_bottom", 0.15), "safe bottom", 0, 0.4)
    canonical(project)
    return project


@contextmanager
def project_lock(path):
    lock = Path(str(path) + ".lock")
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as e:
        raise FrameCutError("busy", "Project is being edited; inspect an abandoned lock before removing it") from e
    try:
        os.write(fd, str(os.getpid()).encode())
        os.close(fd)
        yield
    finally:
        lock.unlink(missing_ok=True)


def commit_revision(path, project, base_revision, reason):
    path = Path(path).resolve()
    with project_lock(path):
        old = read_json(path)
        require(old["revision"] == base_revision, "Project revision changed; reload before applying edits", "stale_revision")
        require(project["id"] == old["id"], "Cannot replace project identity")
        for lock in old.get("locks", []):
            matches = lambda p: [c for s in p["sequences"] for c in s["clips"] if c["id"] == lock]
            require(matches(project) == matches(old), f"Protected clip changed: {lock}", "locked_content")
        candidate = copy.deepcopy(project)
        candidate["revision"] = base_revision + 1
        candidate["status"] = "draft"
        candidate["history"] = {"parent_revision": base_revision, "parent_hash": fingerprint(old), "reason": str(reason)[:2000]}
        validate(candidate, path.parent, True)
        history = confined(path.parent, f".framecut/{identifier(old['id'])}/history")
        history.mkdir(parents=True, exist_ok=True)
        snapshot = history / f"r{base_revision}.json"
        if snapshot.exists():
            require(fingerprint(read_json(snapshot)) == fingerprint(old), "Revision history conflict", "stale_revision")
        else:
            atomic_json(snapshot, old)
        atomic_json(path, candidate, overwrite=True)
    return candidate


def apply_operations(project, operations):
    require(isinstance(operations, list) and 0 < len(operations) <= 500, "Expected bounded operations list")
    result = copy.deepcopy(project)
    invalidated = set()
    for op in operations:
        keys(op, ("op", "sequence", "id", "value"), ("op", "value"))
        kind = op["op"]
        from fc_edit import EDIT_OPERATIONS, apply_edit
        if kind in EDIT_OPERATIONS:
            apply_edit(result, op)
        elif kind in ("set_brief", "set_authorization", "set_locks", "set_deliverables"):
            result[kind[4:]] = op["value"]
        elif kind == "add_sequence":
            result["sequences"].append(op["value"])
        else:
            seq = next((s for s in result["sequences"] if s["id"] == op.get("sequence")), None)
            require(seq is not None, "Unknown sequence")
            if kind == "set_sequence":
                require(op["value"].get("id") == seq["id"], "Stable sequence ID changed")
                result["sequences"][result["sequences"].index(seq)] = op["value"]
            elif kind in ("set_captions", "set_audio", "set_overlays", "set_texts"):
                seq[kind[4:]] = op["value"]
            elif kind == "replace_clip":
                index = next((i for i, c in enumerate(seq["clips"]) if c["id"] == op.get("id")), None)
                require(index is not None and op["value"].get("id") == op.get("id"), "Unknown/stale clip ID")
                seq["clips"][index] = op["value"]
            else:
                raise FrameCutError("unsupported_operation", f"Unsupported edit operation: {kind}")
        invalidated.update(("projection", "render", "delivery"))
        if kind not in ("set_captions", "set_texts", "set_overlays", "set_brief", "set_authorization", "set_locks"):
            invalidated.update(("picture", "mix", "caption_timing", "interchange"))
    for lock in project.get("locks", []):
        matches = lambda p: [c for s in p["sequences"] for c in s["clips"] if c["id"] == lock]
        require(matches(result) == matches(project), f"Protected clip changed: {lock}", "locked_content")
    validate(result)
    return result, sorted(invalidated)
