"""Project source speech once onto the edit, then delegate subtitle QA to Caption Studio."""
from __future__ import annotations

import importlib.util
import textwrap
from fractions import Fraction
from pathlib import Path

from fc_time import timeline_offset, parameters
from fc_core import event_start, fingerprint, ratio, require, round_boundary, span_seconds


def project_captions(project, seq):
    fps = ratio(seq["fps"])
    style = seq.get("captions", {})
    result, warnings = [], []
    events = seq["clips"]
    if "sources" in style:
        events = [e for e in [*seq["clips"], *seq.get("audio", [])] if e["id"] in style["sources"]]
    for clip in events:
        if clip.get("freeze"):
            continue
        analysis = project["analyses"].get(clip["asset"], {})
        units = analysis.get("words", []) or analysis.get("segments", [])
        kind = "word" if analysis.get("words") else "segment"
        source_in, length = span_seconds(project["assets"][clip["asset"]], clip, fps)
        epsilon = Fraction(project["assets"][clip["asset"]]["probe"]["time_base"]) / 2
        timeline_start = event_start(clip, seq)
        end = source_in + length
        speed = ratio(clip.get("speed", {"num": 1, "den": 1}))
        for word in units:
            if word["start"] is None:
                warnings.append({"code": "unknown_timing", "word": word["id"], "clip": clip["id"]})
                continue
            a, b = Fraction(str(word["start"])), Fraction(str(word["end"]))
            if b <= source_in + epsilon or a >= end - epsilon:
                continue
            clipped = a < source_in - epsilon or b > end + epsilon
            if clipped:
                warnings.append({"code": "clipped_word" if kind == "word" else "partial_segment", "word": word["id"], "clip": clip["id"], "source": clip["asset"]})
                # A sentence cannot be attributed to a smaller source interval; request an aligned correction.
                if kind == "segment":
                    continue
            start = timeline_start + round_boundary(timeline_offset(clip, max(a, source_in) - source_in, fps))
            finish = timeline_start + round_boundary(timeline_offset(clip, min(b, end) - source_in, fps))
            if finish <= start:
                warnings.append({"code": "subframe_word", "word": word["id"], "clip": clip["id"]})
                continue
            correction_key = f"{clip['asset']}:{word['id']}"
            result.append({"id": f"{clip['id']}:{word['id']}", "source_id": word["id"], "asset": clip["asset"], "clip": clip["id"],
                           "start": start, "end": finish, "source_start": word["start"], "source_end": word["end"],
                           "text": style.get("corrections", {}).get(correction_key, word["text"]), "kind": kind,
                           "verbatim": word["verbatim"] if "verbatim" in word else word["text"], "timing": analysis.get("timing", "unknown")})
    result.sort(key=lambda w: (w["start"], w["end"], w["id"]))
    if style.get("mode") == "kinetic" and any(w["kind"] != "word" for w in result):
        warnings.append({"code": "kinetic_requires_word_timing", "message": "Keep sentence mode or supply checked word timing; no fabricated word alignment."})
    groups, current = [], []
    for w in result:
        split = current and (w["clip"] != current[-1]["clip"] or w["kind"] == "segment" or current[-1]["kind"] == "segment"
                             or len(current) >= style.get("max_words", 6) or w["start"] - current[-1]["end"] > fps / 2
                             or len(" ".join(x["text"] for x in current) + " " + w["text"]) > 70)
        if split:
            groups.append(current); current = []
        current.append(w)
    if current:
        groups.append(current)
    return {"project_revision": project["revision"], "sequence": seq["id"], "fps": seq["fps"], "words": result,
            "groups": groups, "warnings": warnings, "source_mapping_hash": fingerprint(result)}


def caption_owner():
    path = Path(__file__).resolve().parents[3] / "caption-studio/assets/captions/captions.py"
    spec = importlib.util.spec_from_file_location("framecut_caption_owner", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def subtitle_cues(projection):
    fps = ratio(projection["fps"])
    return [{"start_ms": round_boundary(Fraction(g[0]["start"]) / fps * 1000),
             "end_ms": round_boundary(Fraction(g[-1]["end"]) / fps * 1000),
             "text": " ".join(w["text"] for w in g)} for g in projection["groups"]]


def sidecars(projection, language="en"):
    owner = caption_owner()
    cues = subtitle_cues(projection)
    for cue in cues:
        cue["text"] = owner.break_lines(cue["text"], language)
    return {"srt": owner.write(cues, "srt"), "vtt": owner.write(cues, "vtt"),
            "qa": owner.check(cues, language=language, fps=float(ratio(projection["fps"]))) if cues else {"status": "no_captions", "cues": 0}}


def ass_color(c):
    return "&H00" + c[5:7] + c[3:5] + c[1:3]


def ass_time(frame, fps):
    cs = round_boundary(Fraction(frame) / fps * 100)
    return f"{cs // 360000}:{cs // 6000 % 60:02}:{cs // 100 % 60:02}.{cs % 100:02}"


def ass_text(text):
    # Never interpret authored text as ASS tags or escapes.
    return text.replace("\\", "＼").replace("{", "｛").replace("}", "｝").replace("\r", "").replace("\n", "\\N")


def ass_document(project, seq, delivery, projection):
    w, h = delivery["width"], delivery["height"]
    fps, cap = ratio(seq["fps"]), seq.get("captions", {})
    size = round(h * cap.get("size", .055))
    font = cap.get("font", "DejaVu Sans")
    bottom = max(cap.get("bottom", .18), delivery.get("safe_bottom", .15))
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {w}
PlayResY: {h}
WrapStyle: 0
ScaledBorderAndShadow: yes
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,{font},{size},{ass_color(cap.get('color','#FFFFFF'))},{ass_color(cap.get('highlight','#FFCF33'))},&H00101010,&H80000000,-1,0,0,0,100,100,0,0,1,{max(1,round(size*.07))},0,2,{round(w*.08)},{round(w*.08)},{round(h*bottom)},1
Style: Text,{font},{size},&H00FFFFFF,&H00FFFFFF,&H00101010,&H80000000,-1,0,0,0,100,100,0,0,1,2,0,5,{round(w*.08)},{round(w*.08)},0,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines, layout = [], []
    def emit(start, end, style, content, layer=0):
        if end > start:
            lines.append(f"Dialogue: {layer},{ass_time(start,fps)},{ass_time(end,fps)},{style},,0,0,0,,{content}")
    if cap.get("enabled", False) and delivery.get("captions", True):
        for group in projection["groups"]:
            text = " ".join(x["text"] for x in group)
            # Conservative width estimate is a warning; actual frame review remains required.
            chars = max(8, int(w * .84 / max(1, size * .59)))
            wrapped = textwrap.wrap(text, width=chars, break_long_words=False, break_on_hyphens=False)
            if len(wrapped) > 2 or any(len(line) > chars for line in wrapped):
                layout.append({"code": "caption_layout_overflow", "start": group[0]["start"], "text": text})
            if cap.get("mode", "sentence") == "kinetic" and all(x["kind"] == "word" for x in group):
                # Render whole phrase continuously; only the word with measured timing changes color.
                boundaries = sorted({group[0]["start"], group[-1]["end"], *(v for x in group for v in (x["start"], x["end"]))})
                for a, b in zip(boundaries, boundaries[1:]):
                    words = []
                    for x in group:
                        color = cap.get("highlight", "#FFCF33") if x["start"] <= a < x["end"] else cap.get("color", "#FFFFFF")
                        words.append("{\\c" + ass_color(color) + "&}" + ass_text(x["text"]))
                    emit(a, b, "Caption", " ".join(words))
            else:
                emit(group[0]["start"], group[-1]["end"], "Caption", "\\N".join(ass_text(x) for x in wrapped))
    for event in seq.get("texts", []):
        start = event_start(event, seq)
        position = event.get("position", "center")
        y = h * ({"top": max(.15, delivery.get("safe_top", .08) + .06), "center": .5,
                  "bottom": 1 - delivery.get("safe_bottom", .15) - .08}[position])
        px = round(h * event.get("size", .06))
        animation = {"none": "", "fade": "\\fad(120,120)", "pop": "\\fscx88\\fscy88\\t(0,140,\\fscx100\\fscy100)"}[event.get("animation", "fade")]
        tag = "{" + f"\\an5\\pos({w//2},{round(y)})\\fs{px}\\c{ass_color(event.get('color','#FFFFFF'))}&" + animation + "}"
        if event.get("keyframes"):
            for frame in range(event["duration"]):
                v = parameters(event, frame)
                animated = "{" + f"\\an5\\pos({round(w*(.5+v['x']))},{round(y+h*v['y'])})\\fs{px}\\fscx{100*v['scale']:.3f}\\fscy{100*v['scale']:.3f}\\frz{-v['rotation']:.3f}\\alpha&H{round(255*(1-v['opacity'])):02X}&\\c{ass_color(event.get('color','#FFFFFF'))}&" + "}"
                emit(start+frame, start+frame+1, "Text", animated+ass_text(event["text"]), 1)
        else:
            emit(start, start + event["duration"], "Text", tag + ass_text(event["text"]), 1)
        if position == "bottom" and cap.get("enabled"):
            layout.append({"code": "caption_text_collision", "event": event["id"], "start": start})
    return header + "\n".join(lines) + "\n", layout
