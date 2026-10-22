#!/usr/bin/env python3
"""FrameCut: local, revisioned editing CLI. Run --help; commands return structured JSON."""
from __future__ import annotations

import argparse
import copy
import csv
import importlib.util
import json
import os
import shutil
import signal
import sys
import tempfile
import threading
from fractions import Fraction
from pathlib import Path

from fc_core import (FrameCutError, apply_operations, atomic_json, commit_revision, confined, confined_output, file_hash,
                     fingerprint, identifier, ratio, read_json, require, round_boundary, span_seconds, validate)
from fc_media import capabilities, ingest, inspect_media, probe, transcribe, transcript_import
from fc_render import bind_motion, compile_project, motion_request, render, validate_review, verify_delivery


def project_file(argument):
    """Absolute project path with ./ and ../ resolved textually; a symlinked ancestor is still rejected afterwards."""
    return Path(os.path.abspath(argument))


def project_init(path, name, brief=None):
    path = project_file(path)
    require(not path.is_symlink() and path.parent.resolve() == path.parent, "Project path contains a symlink")
    project = {"schema_version": 1, "id": identifier(name), "revision": 1, "brief": brief or {}, "authorization": None,
               "assets": {}, "analyses": {}, "sequences": [], "deliverables": [], "locks": [], "status": "draft", "history": None}
    validate(project)
    atomic_json(path, project)
    return project


def propose(project, asset_id):
    require(asset_id in project["assets"], "Unknown asset")
    analysis = project["analyses"].get(asset_id, {})
    segments = analysis.get("segments", [])
    if not segments:
        return {"status": "needs_editorial_analysis", "asset": asset_id, "candidates": [],
                "next": "Inspect visual/scene evidence and the brief, or import a checked source transcript. No speech is invented."}
    return {"status": "candidates_need_editorial_review", "asset": asset_id, "source_hash": project["assets"][asset_id]["sha256"],
            "candidates": [{"id": "candidate-" + s["id"], "start": s["start"], "end": s["end"], "text": s["text"],
                            "context_before": segments[i-1]["text"] if i else "",
                            "context_after": segments[i+1]["text"] if i+1 < len(segments) else "",
                            "completeness": "unreviewed", "rationale": "Transcript interval only; the host must assess meaning, context, visual support and relevance to the brief."}
                           for i, s in enumerate(segments) if s["start"] is not None],
            "warnings": ["No automatic last-take-wins, filler removal or virality score. Review negations, numbers, qualifiers and joins."]}


def export_edit(project, root, sequence_id, relative, use_otio=False):
    validate(project, root, True)
    seq = next((s for s in project["sequences"] if s["id"] == sequence_id), None)
    require(seq is not None, "Unknown sequence")
    output = confined_output(root, relative)
    require(not output.exists(), "Export directory already exists")
    otio = None
    if use_otio:
        try:
            import opentimelineio as otio
        except ImportError as e:
            raise FrameCutError("missing_capability", "Official OpenTimelineIO Python library is absent; use native/CSV/EDL export or disclose its isolated installation plan") from e
    # Built beside the target and renamed at the end: a failed export leaves no half-written directory to block a retry.
    output.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".framecut-export-", dir=output.parent))
    try:
        result = write_export(project, seq, staging, relative, otio)
        os.rename(staging, output)
    except BaseException:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    return result


def spreadsheet_safe(value):
    """CSV cells that start like a formula are prefixed so a spreadsheet shows them as text."""
    text = str(value)
    return "'" + text if text[:1] in ("=", "+", "-", "@", "\t", "\r") else text


def write_export(project, seq, output, relative, otio):
    fps = ratio(seq["fps"])
    losses = []
    if seq.get("audio"):
        losses.append("Independent audio events and gain/ducking remain in the FrameCut project; basic editorial export covers picture cuts only.")
    if seq.get("overlays") or seq.get("texts") or seq.get("captions", {}).get("enabled"):
        losses.append("Motion, titles and caption styling are retained in the FrameCut project/authoring contracts; editor interchange does not recreate them.")
    if any(c.get("keyframes") or c.get("effects") for c in seq["clips"]) or any(d.get("framing") for d in project["deliverables"] if d['sequence']==seq['id']):
        losses.append("Keyframes, effects and deliverable framing remain in the native project; picture interchange does not recreate them.")
    events = []
    complex_edit = False
    for c in seq["clips"]:
        a = project["assets"][c["asset"]]
        start, length = span_seconds(a, c, fps)
        complex_edit |= bool(c.get("transition") or c.get("speed_curve") or c.get("freeze") or ratio(c.get("speed", {"num": 1, "den": 1})) != 1)
        events.append({"source": a["path"], "in": float(start), "out": float(start+length), "record_in": float(Fraction(c["start"])/fps),
                       "name": c["id"], "note": c.get("note", ""), "source_hash": a["sha256"], "record_frames": [c["start"], c["start"]+c["duration"]]})
    if complex_edit:
        losses.append("Transitions or speed changes require the native FrameCut project; basic EDL/OTIO is withheld rather than flattened misleadingly.")
    atomic_json(output / "framecut-project.json", project)
    atomic_json(output / "relink.json", {"base": "original project root", "assets": {k: {"path": a["path"], "sha256": a["sha256"]} for k, a in project["assets"].items()},
                                          "note": "Media is not copied; relink to the original project root. This snapshot is not a standalone media bundle."})
    with (output / "shots.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=("source", "in", "out", "record_in", "name", "note", "source_hash", "record_frames"))
        writer.writeheader(); writer.writerows({k: (spreadsheet_safe(v) if k in ("source", "name", "note") else v) for k, v in e.items()} for e in events)
    if not complex_edit and events:
        legacy_path = Path(__file__).resolve().parents[2] / "scripts/edit_export.py"
        spec = importlib.util.spec_from_file_location("framecut_legacy_export", legacy_path)
        legacy = importlib.util.module_from_spec(spec); spec.loader.exec_module(legacy)
        try:
            timeline = legacy.build({"title": seq["id"], "fps": float(fps), "clips": events})
        except legacy.InputError as error:
            raise FrameCutError("unsupported_operation", f"EDL export is unavailable for this sequence: {error}. Use the native project and CSV files") from None
        (output / "picture.edl").write_text(legacy.edl(timeline), encoding="utf-8")
        losses.append("CMX EDL is picture-only non-drop-frame at a nominal timebase; source PTS/VFR precision remains in source-map/native project. Named editor import is unverified.")
        if otio:
            track = otio.schema.Track(name="V1", kind=otio.schema.TrackKind.Video)
            previous = 0
            for c, e in zip(seq["clips"], events):
                if c["start"] > previous:
                    track.append(otio.schema.Gap(source_range=otio.opentime.TimeRange(otio.opentime.RationalTime(0, float(fps)), otio.opentime.RationalTime(c["start"]-previous, float(fps)))))
                clip = otio.schema.Clip(name=c["id"], media_reference=otio.schema.ExternalReference(target_url=e["source"]),
                                        source_range=otio.opentime.TimeRange(otio.opentime.RationalTime(e["in"]*float(fps), float(fps)), otio.opentime.RationalTime(c["duration"], float(fps))))
                clip.metadata["framecut"] = {"asset_hash": e["source_hash"], "project_revision": project["revision"], "source_in_pts": c.get("source_in", project["assets"][c["asset"]]["probe"]["start_pts"])}
                track.append(clip); previous = c["start"]+c["duration"]
            timeline = otio.schema.Timeline(name=seq["id"]); timeline.tracks.append(track)
            otio.adapters.write_to_file(timeline, str(output / "picture.otio"))
            reread = otio.adapters.read_from_file(str(output / "picture.otio"))
            require(round_boundary(Fraction(str(reread.duration().to_seconds())) * fps) == previous, "OTIO round-trip duration differs", "qa_failed")
    atomic_json(output / "loss-report.json", {"losses": losses, "editor_import": "NOT_RUN", "official_otio": bool(otio), "project_revision": project["revision"]})
    return {"status": "exported", "output": relative, "losses": losses, "editor_import": "NOT_RUN"}


def main(argv=None):
    # SIGTERM cancels like Ctrl-C, so the running child is stopped and the render lock is cleaned up.
    if threading.current_thread() is threading.main_thread():
        signal.signal(signal.SIGTERM, lambda *_: (_ for _ in ()).throw(KeyboardInterrupt()))
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("capabilities", help="Offline capability probe; never installs")
    q = sub.add_parser("effects", help="List versioned effects or run their fixtures")
    q.add_argument("--check", action="store_true")
    q = sub.add_parser("init", help="Create a project; its parent is the explicit allowed media/output root")
    q.add_argument("project"); q.add_argument("--id", required=True); q.add_argument("--brief")
    for name in ("ingest", "validate", "analyze", "import-transcript", "align-script", "transcribe", "propose", "apply", "undo", "compile", "render", "verify", "export", "motion-request", "attach-motion", "review", "timeline-read", "preview-frame", "storyboard", "job-start", "job-status", "job-cancel", "job-resume", "job-worker"):
        q = sub.add_parser(name); q.add_argument("project")
        if name in ("ingest", "analyze", "import-transcript", "align-script", "transcribe", "propose", "attach-motion"):
            q.add_argument("--asset", required=True)
        if name == "ingest":
            q.add_argument("--media", required=True, help="Path relative to the project root")
            q.add_argument("--rights", default="unknown"); q.add_argument("--provenance", default="user-supplied")
        if name in ("ingest", "import-transcript", "align-script", "transcribe", "attach-motion", "apply", "undo"):
            q.add_argument("--base-revision", type=int, required=True)
        if name in ("analyze", "compile", "render", "export", "motion-request", "preview-frame", "storyboard"):
            q.add_argument("--out", required=True, help="New project-relative output path")
        if name == "analyze":
            q.add_argument("--max-seconds", type=int, default=1800); q.add_argument("--thumbnails", type=int, default=8)
        if name == "import-transcript": q.add_argument("--transcript", required=True)
        if name == "align-script":
            q.add_argument("--script", required=True, help="Text file with the known script (UTF-8)")
            q.add_argument("--min-match", type=float, default=0.6, help="Refuse when less than this share of the script matches the speech")
        if name == "transcribe":
            q.add_argument("--python", required=True); q.add_argument("--model", required=True); q.add_argument("--language", default="auto")
            q.add_argument("--word-times", action="store_true", help="Request approximate ASR token word times; review them before kinetic delivery")
        if name == "apply":
            q.add_argument("--ops", required=True); q.add_argument("--reason", required=True)
            q.add_argument("--dry-run", action="store_true", help="Validate the transaction and report impact without saving")
        if name == "undo": q.add_argument("--revision", type=int, required=True)
        if name in ("compile", "render", "motion-request", "preview-frame", "storyboard"): q.add_argument("--deliverable", required=True)
        if name == "render":
            q.add_argument("--mode", choices=("preview", "final"), default="preview")
            q.add_argument("--timeout", type=int, default=600); q.add_argument("--max-disk-mb", type=int, default=2048)
        if name in ("verify", "review"): q.add_argument("--bundle", required=True)
        if name == "export": q.add_argument("--sequence", required=True); q.add_argument("--otio", action="store_true")
        if name == "motion-request": q.add_argument("--event", required=True, help="JSON event with local duration and global start/anchor")
        if name == "attach-motion":
            q.add_argument("--contract", required=True); q.add_argument("--fps", required=True, help="Rational num/den")
            q.add_argument("--request", required=True, help="Original motion-request JSON")
        if name == "timeline-read": q.add_argument("--sequence")
        if name == "preview-frame": q.add_argument("--frame", type=int, required=True)
        if name == "storyboard": q.add_argument("--panels", help="Optional authored moments JSON; structural coverage is always retained")
        if name == "job-start": q.add_argument("--request", required=True)
        if name in ("job-status", "job-cancel", "job-resume", "job-worker"): q.add_argument("--job", required=True)
        if name == "review": q.add_argument("--evidence", required=True, help="Authored review JSON, with reviewer, scope, observations and outcome")
    args = p.parse_args(argv)
    try:
        if args.command == "capabilities":
            result = capabilities()
        elif args.command == "effects":
            from fc_effects import catalogue_info, check_fixtures
            result = check_fixtures() if args.check else catalogue_info()
        elif args.command == "init":
            result = project_init(args.project, args.id, read_json(args.brief) if args.brief else {})
        else:
            path = project_file(args.project)
            require(not path.is_symlink() and path.parent.resolve() == path.parent, "Project path contains a symlink")
            root, project = path.parent, read_json(path)
            cmd = args.command
            validate(project, root if not cmd.startswith("job-") else None, not cmd.startswith("job-"))
            if cmd == "validate": result = {"status": "PASS", "revision": project["revision"], "project_hash": fingerprint(project)}
            elif cmd == "ingest":
                require(args.asset not in project["assets"], "Asset ID already exists; preserve immutable source identities")
                project["assets"][args.asset] = ingest(root, args.media, args.asset, args.rights, args.provenance)
                result = commit_revision(path, project, args.base_revision, "ingest source")
            elif cmd == "analyze":
                require(1 <= args.max_seconds <= 21600 and 1 <= args.thumbnails <= 64, "Analysis bounds invalid")
                result = inspect_media(root, project["assets"][args.asset], confined_output(root, args.out), args.max_seconds, args.thumbnails)
            elif cmd in ("import-transcript", "transcribe"):
                asset = project["assets"][args.asset]
                analysis = (transcript_import(asset, read_json(args.transcript)) if cmd == "import-transcript" else transcribe(root, asset, args.python, args.model, args.language, word_times=args.word_times))
                project["analyses"][args.asset] = analysis
                result = commit_revision(path, project, args.base_revision, cmd)
            elif cmd == "align-script":
                from fc_align import align_script
                analysis = project["analyses"].get(args.asset)
                require(analysis and any(w.get("start") is not None for w in analysis.get("words", [])),
                        "align-script needs word timing: import a transcript with word times or transcribe with --word-times first")
                require(0 < args.min_match <= 1, "--min-match must be between 0 and 1")
                script_path = Path(args.script)
                require(script_path.is_file() and script_path.stat().st_size <= 1024 * 1024, "The script must be a UTF-8 text file of at most 1 MiB")
                aligned = align_script(analysis["words"], script_path.read_text(encoding="utf-8"), args.min_match)
                updated = {k: v for k, v in analysis.items() if k != "fingerprint"}
                updated.update(words=aligned["words"], segments=[], timing="aligned", alignment=aligned["report"],
                               limitations=[*analysis.get("limitations", []), "Spelling comes from the supplied script and timing from the heard words; interpolated words are estimates."])
                updated["fingerprint"] = fingerprint(updated)
                project["analyses"][args.asset] = updated
                saved = commit_revision(path, project, args.base_revision, "align script to speech")
                result = {**aligned["report"], "revision": saved["revision"]}
            elif cmd == "propose": result = propose(project, args.asset)
            elif cmd == "apply":
                require(project["revision"] == args.base_revision, "Project revision changed", "stale_revision")
                candidate, invalidated = apply_operations(project, read_json(args.ops))
                from fc_edit import change_impact
                impact = change_impact(project, candidate)
                saved = candidate if args.dry_run else commit_revision(path, candidate, args.base_revision, args.reason)
                result = {"status": "dry_run" if args.dry_run else "revised", "revision": saved["revision"], "invalidated": invalidated, "analysis_preserved": True, "impact": impact}
            elif cmd == "undo":
                previous = read_json(confined(root, f".framecut/{project['id']}/history/r{args.revision}.json", True))
                previous["locks"] = copy.deepcopy(project.get("locks", []))
                result = commit_revision(path, previous, args.base_revision, f"restore content of revision {args.revision}; current locks still apply")
            elif cmd == "compile":
                plan = compile_project(project, root, args.deliverable)
                atomic_json(confined_output(root, args.out), plan)
                result = {"status": "compiled", "path": args.out, "warnings": plan["warnings"]}
            elif cmd == "render":
                require(1 <= args.timeout <= 7200 and 64 <= args.max_disk_mb <= 102400, "Render resource limits invalid")
                result = render(project, root, args.deliverable, args.out, args.mode, args.timeout, args.max_disk_mb)
            elif cmd == "timeline-read":
                from fc_edit import timeline_read
                result = timeline_read(project, args.sequence)
            elif cmd == "preview-frame":
                from fc_board import preview_frame
                result = preview_frame(project, root, args.deliverable, args.frame, args.out)
            elif cmd == "storyboard":
                from fc_board import storyboard
                result = storyboard(project, root, args.deliverable, args.out, read_json(args.panels) if args.panels else None)
            elif cmd.startswith("job-"):
                from fc_jobs import start, status, cancel, resume, worker
                if cmd == "job-start": result = start(path, read_json(args.request))
                elif cmd == "job-status": result = status(root, project["id"], args.job)
                elif cmd == "job-cancel": result = cancel(root, project["id"], args.job)
                elif cmd == "job-resume": result = resume(path, args.job)
                else: result = worker(path, args.job)
            elif cmd == "verify": result = verify_delivery(project, root, args.bundle)
            elif cmd == "export": result = export_edit(project, root, args.sequence, args.out, args.otio)
            elif cmd == "motion-request":
                d = next(x for x in project["deliverables"] if x["id"] == args.deliverable)
                seq = next(x for x in project["sequences"] if x["id"] == d["sequence"])
                result = motion_request(project, seq, read_json(args.event), d)
                atomic_json(confined_output(root, args.out), result)
            elif cmd == "attach-motion":
                project["assets"][args.asset]["motion_contract"] = bind_motion(project, root, args.asset, args.contract, Fraction(args.fps), read_json(args.request))
                result = commit_revision(path, project, args.base_revision, "bind local motion contract")
            elif cmd == "review":
                verified = verify_delivery(project, root, args.bundle)
                evidence = validate_review(read_json(args.evidence))
                result = {"project_hash": fingerprint(project), "project_revision": project["revision"], "technical": verified["status"], "evidence": evidence,
                          "video_hash": file_hash(confined(root, args.bundle + "/video.mp4", True))}
                latest = confined(root, args.bundle + "/review-evidence.json")
                if latest.exists():
                    previous = read_json(latest)
                    archived = confined(root, args.bundle + "/review/history/" + fingerprint(previous) + ".json")
                    if not archived.exists(): atomic_json(archived, previous)
                atomic_json(latest, result, overwrite=True)
            else: raise FrameCutError("unsupported_operation", cmd)
        print(json.dumps(result, ensure_ascii=False, allow_nan=False))
        return 0
    except KeyboardInterrupt:
        print(json.dumps({"status": "error", "error": {"code": "cancelled", "message": "Interrupted; no final was published. A render lock left by a killed process is reclaimed by the next render."}}), file=sys.stderr)
        return 130
    except (FrameCutError, OSError, ValueError, KeyError, TypeError, StopIteration, ZeroDivisionError, AttributeError, RecursionError, IndexError) as error:
        # Internal failures keep the typed shape; the exception name says where to look when the message is empty.
        known = isinstance(error, FrameCutError)
        message = str(error) or type(error).__name__
        print(json.dumps({"status": "error", "error": {"code": getattr(error, "code", "invalid_input" if known or isinstance(error, (OSError, ValueError, KeyError, TypeError)) else "internal_error"),
                                                       "message": message if known else f"{type(error).__name__}: {message}"}}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
