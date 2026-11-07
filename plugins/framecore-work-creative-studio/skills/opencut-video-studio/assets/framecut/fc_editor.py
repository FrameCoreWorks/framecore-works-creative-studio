"""Editor helpers that plan work for review: a silence cut plan as native operations, and a beat grid for cutting to music.
Neither applies anything; the host reviews the plan and runs `apply --dry-run` before saving a revision."""
import array
import copy
import math
import tempfile
from fractions import Fraction
from pathlib import Path
from fc_core import apply_operations, event_start, integer, ratio, require, span_seconds


def _frame_of(clip, rel_start, seconds, fps):
    speed = ratio(clip.get("speed", {"num": 1, "den": 1}))
    return clip["start"] + (Fraction(str(seconds)) - rel_start) / speed * fps


def plan_silence_cuts(project, sequence_id, silences, asset_id=None, pre_pad=3, post_pad=6, min_cut=6):
    """Turn detected silences (source seconds from the asset's start) into split/remove operations with speech pads.

    post_pad keeps frames after the last sound (its decay); pre_pad keeps frames before the next word (its attack).
    Cuts run from the end of the timeline backwards, so each one leaves the earlier frame numbers intact."""
    seq = next((s for s in project["sequences"] if s["id"] == sequence_id), None)
    require(seq is not None, "Unknown sequence")
    fps = ratio(seq["fps"])
    for value, name in ((pre_pad, "pre pad"), (post_pad, "post pad")):
        integer(value, name, 0, 120)
    integer(min_cut, "minimum cut", 1, 100000)
    require(isinstance(silences, list) and len(silences) <= 5000, "Silences must be a bounded list")
    clips = seq["clips"]
    assets = {c["asset"] for c in clips}
    if asset_id is None:
        require(len(assets) == 1, "Several assets on this sequence: name the asset the silences belong to")
        asset_id = next(iter(assets))
    require(asset_id in project["assets"], "Unknown asset")
    asset = project["assets"][asset_id]
    words = [w for w in project.get("analyses", {}).get(asset_id, {}).get("words", []) if w.get("start") is not None and w.get("end") is not None]
    ids = {e["id"] for lane in ("clips", "audio", "overlays", "texts") for e in seq.get(lane, [])}
    cuts, skipped = [], []
    for index, clip in enumerate(clips):
        if clip["asset"] != asset_id:
            continue
        rel_start, length = span_seconds(asset, clip, fps)
        end_frame = clip["start"] + clip["duration"]
        for silence in silences:
            s, e = Fraction(str(silence["start"])), Fraction(str(silence["end"]))
            if e <= rel_start or s >= rel_start + length:
                continue
            where = {"clip": clip["id"], "silence": [float(s), float(e)]}
            if clip.get("speed_curve") or clip.get("freeze") or clip.get("transition") or (index + 1 < len(clips) and clips[index + 1].get("transition")):
                skipped.append({**where, "reason": "retimed_frozen_or_transition_clip"})
                continue
            start = max(clip["start"], math.ceil(_frame_of(clip, rel_start, max(s, rel_start), fps)) + (post_pad if s > rel_start else 0))
            end = min(end_frame, math.floor(_frame_of(clip, rel_start, min(e, rel_start + length), fps)) - (pre_pad if e < rel_start + length else 0))
            if end - start < min_cut:
                skipped.append({**where, "reason": "shorter_than_min_cut"})
                continue
            speed = ratio(clip.get("speed", {"num": 1, "den": 1}))
            source = (rel_start + Fraction(start - clip["start"]) / fps * speed, rel_start + Fraction(end - clip["start"]) / fps * speed)
            if any(Fraction(str(w["start"])) < source[1] and Fraction(str(w["end"])) > source[0] for w in words):
                skipped.append({**where, "reason": "overlaps_timed_word"})
                continue
            anchored = [x["id"] for lane in ("audio", "overlays", "texts") for x in seq.get(lane, [])
                        if x.get("anchor", {}).get("clip") == clip["id"] and x["anchor"]["offset"] < end - clip["start"]
                        and x["anchor"]["offset"] + x["duration"] > start - clip["start"]]
            absolute = [x["id"] for lane in ("audio", "overlays", "texts") for x in seq.get(lane, [])
                        if "anchor" not in x and x["start"] < end and x["start"] + x["duration"] > start]
            if anchored or absolute:
                skipped.append({**where, "reason": "event_inside_cut", "events": anchored + absolute})
                continue
            cuts.append({"clip": clip["id"], "start": start, "end": end, "frames": end - start,
                         "source_seconds": [float(source[0]), float(source[1])], "silence": [float(s), float(e)]})
    cuts.sort(key=lambda c: c["start"], reverse=True)
    operations, counter = [], 0

    def fresh(base):
        nonlocal counter
        while True:
            counter += 1
            name = f"{base}-{counter}"
            if name not in ids:
                ids.add(name)
                return name
    for cut in cuts:
        clip = next(c for c in clips if c["id"] == cut["clip"])
        clip_end = clip["start"] + clip["duration"]
        if cut["end"] < clip_end:
            operations.append({"op": "split_clip", "sequence": sequence_id, "id": clip["id"], "value": {"frame": cut["end"], "right_id": fresh(clip["id"] + "-keep")}})
        target = clip["id"]
        if cut["start"] > clip["start"]:
            target = fresh(clip["id"] + "-cut")
            operations.append({"op": "split_clip", "sequence": sequence_id, "id": clip["id"], "value": {"frame": cut["start"], "right_id": target}})
        operations.append({"op": "remove_clip", "sequence": sequence_id, "id": target, "value": {"ripple": True, "dependents": "reject"}})
    removed = sum(c["frames"] for c in cuts)
    plan = {"status": "plan_needs_review", "sequence": sequence_id, "asset": asset_id, "cuts": cuts, "skipped": skipped,
            "removed_frames": removed, "removed_seconds": float(Fraction(removed) / fps),
            "pads": {"pre_pad_frames": pre_pad, "post_pad_frames": post_pad, "min_cut_frames": min_cut},
            "operations": operations,
            "review": "Listen to every join: keep breaths that carry rhythm, purposeful pauses and pauses before a punchline. "
                      "Silence is detected by level, not meaning; run apply --dry-run, then a storyboard or preview of the joins."}
    if operations:
        simulated, _ = apply_operations(project, operations)
        after = next(s for s in simulated["sequences"] if s["id"] == sequence_id)
        tail = max(event_start(x, after) + x["duration"] for lane in ("clips", "audio", "overlays", "texts") for x in after.get(lane, []))
        if tail < after["duration"]:
            shortened = copy.deepcopy(after)
            shortened["duration"] = tail
            operations.append({"op": "set_sequence", "sequence": sequence_id, "value": shortened})
        plan["duration_after"] = tail
    return plan


def _decode(path, rate, max_seconds, timeout):
    from fc_media import ffmpeg
    with tempfile.TemporaryDirectory(prefix=".framecut-beats-") as tmp:
        pcm = Path(tmp) / "mono.pcm"
        ffmpeg(["-i", str(path), "-t", str(max_seconds), "-vn", "-ac", "1", "-ar", str(rate), "-f", "s16le", str(pcm)], timeout)
        samples = array.array("h")
        samples.frombytes(pcm.read_bytes())
    return samples


def beat_grid(path, fps=None, max_seconds=900, min_bpm=60, max_bpm=200, timeout=300):
    """Tempo and beat times of a music file from its energy onsets (a steady grid snapped to nearby onsets).

    Suits music with a clear pulse; rubato, live drift and beatless pads give low confidence. Bars and downbeats
    are not detected: the host counts them from the first strong beat and checks by ear."""
    rate, hop = 11025, 128
    samples = _decode(path, rate, max_seconds, timeout)
    require(len(samples) > rate * 2, "Need at least two seconds of audio for a beat grid")
    count = len(samples) // hop
    energy = [math.log10(1e-3 + sum(v * v for v in samples[k * hop:(k + 1) * hop]) / hop) for k in range(count)]
    onset = [0.0] + [max(0.0, energy[k] - energy[k - 1]) for k in range(1, count)]
    mean = sum(onset) / len(onset)
    centred = [v - mean for v in onset]
    per_second = rate / hop
    best = None
    scores = {}
    for lag in range(int(per_second * 60 / max_bpm), int(per_second * 60 / min_bpm) + 2):
        value = sum(centred[k] * centred[k + lag] for k in range(count - lag)) / (count - lag)
        bpm = 60 * per_second / lag
        weight = math.exp(-0.5 * (math.log2(bpm / 120) / 0.9) ** 2)
        scores[lag] = value
        if best is None or value * weight > best[1]:
            best = (lag, value * weight)
    lag = best[0]
    left, mid, right = scores.get(lag - 1, scores[lag]), scores[lag], scores.get(lag + 1, scores[lag])
    denominator = left - 2 * mid + right
    period = lag + (0.5 * (left - right) / denominator if denominator < 0 else 0)
    period = min(per_second * 60 / min_bpm, max(per_second * 60 / max_bpm, period))
    phase_scores = []
    for phase in range(int(period) + 1):
        total, k = 0.0, 0
        while phase + k * period < count:
            n = min(count - 1, int(round(phase + k * period)))
            total += max(onset[max(0, n - 1):n + 2])
            k += 1
        phase_scores.append(total)
    phase = max(range(len(phase_scores)), key=phase_scores.__getitem__)
    beats, strength = [], []
    k = 0
    while phase + k * period < count:
        n = min(count - 1, int(round(phase + k * period)))
        window = range(max(0, n - 3), min(count, n + 4))
        peak = max(window, key=onset.__getitem__)
        n = peak if onset[peak] > mean * 2 else n
        beats.append(round((n + 0.5) * hop / rate, 4))
        strength.append(round(onset[n], 4))
        k += 1
    variance = sum(v * v for v in centred) / count
    # Periodicity of the onsets at the chosen lag relative to their total variance: near 1 for a steady pulse.
    confidence = max(0.0, min(1.0, scores[lag] / variance)) if variance > 0 else 0.0
    result = {"status": "beat_grid", "bpm": round(60 * per_second / period, 2), "confidence": round(confidence, 3),
              "beats": beats, "strength": strength, "analyzed_seconds": round(len(samples) / rate, 3),
              "method": "energy onsets, autocorrelation tempo, steady grid snapped to onsets within 3 hops (35 ms)",
              "limitations": ["Downbeats and bars are not detected; count them from a strong beat and check by ear.",
                              "Tempo changes, rubato and beatless music give an unreliable grid.",
                              "Half or double tempo is possible; check against the music before cutting."]}
    typical = sorted(strength)[len(strength) // 2] if strength else 0
    if typical < 0.15:
        # The grid lands on rises of under about 1.5 dB: a periodic level ripple, not audible beats.
        confidence = min(confidence, 0.2)
        result["confidence"] = round(confidence, 3)
    if confidence < 0.3:
        result["warnings"] = ["low_confidence: no steady pulse found; cut to the music by ear or supply the tempo."]
    if fps is not None:
        rate_fps = Fraction(str(fps)) if not isinstance(fps, Fraction) else fps
        result["fps"] = str(rate_fps)
        result["beat_frames"] = [int(round(Fraction(str(b)) * rate_fps)) for b in beats]
    return result
