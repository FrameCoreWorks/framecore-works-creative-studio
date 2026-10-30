#!/usr/bin/env python3
"""Acceptance of a motion deliverable as four separate verdicts, from the evidence that actually exists.

  python acceptance.py video.motion.json --video video.mp4 --critique critique-r2/critique.json
         [--review review-out/review.json] [--text-audit audit-out/text-audit.json]
         [--playback watched|not_watched] [--source-review pass|fail] [--composition-review pass|fail] [--temporal-review pass|fail]
         [--listening heard|not_heard] [--sound-review pass|fail] [--motion-activity activity.json]
         [--copy locked-copy.txt] [--note "who watched what, where"] [--out acceptance.json]
         [--pack delivery-dir --include video.render.py ...]

A composition outside the contract route (HyperFrames, GSAP, hand-written HTML) has no copy in its contract: give the
composition with --composition (its text audit must be bound to those bytes), the locked copy with --copy (one entry
per line) and motion_activity.py --json on the encoded file with --motion-activity (bound to that file's SHA-256).

A. technical    the encoded file matches the contract: size, frame rate, frame count, duration, audio presence
B. fidelity     exact copy reaches the picture, unverified claims are not used, every asset has an authority, and
                (by a person) the product and source look right
C. composition  every visible text is complete in readable holds, the layout rules pass in inspected frames, and a
                person judged the key frames at full size and phone scale
D. temporal     pacing evidence plus a person's normal-speed viewing of continuity and the commercial argument, and,
                when the contract or the file has sound, a recorded listening of mix, sync and levels

Each verdict is pass, fail or not_verified. Evidence that was not produced leaves its verdict not_verified: a
contract-only critique score (any number) never makes C pass, a valid export never makes C or D pass, and D needs a
recorded normal-speed viewing (and a recorded listening when there is sound: an audio stream is not a listening). Overall: accepted (all four pass), deliverable_with_limits (nothing failed, something
not verified, listed) or blocked (a verdict failed). Exit code 0 accepted, 1 blocked, 3 with limits, 2 setup problem.
Python 3.8+, standard library; ffprobe for --video.

--pack writes a delivery folder only when the result is not blocked: the exact video and contract that were judged,
the evidence under evidence/, --include files (render script, composition sources) under source/, acceptance.json,
manifest.json (bytes and SHA-256 of every file) and HANDOFF.md (status, verdicts, what was not verified, how to
revise). A blocked film is never packaged. Idea adapted from social-motion-agent (MIT); no code or media copied.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata


def load(path):
    with open(path, encoding='utf-8') as handle:
        return json.load(handle)


def file_hash(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def bound_report(path, score, contract_hash, video_hash, format_id='base'):
    """Only use evidence for these exact source bytes and, for video critiques, this encoded file."""
    if not path:
        return None, None
    report = load(path)
    binding = report.get('evidence_binding') or {}
    contract = binding.get('contract') or {}
    if not contract_hash or not contract.get('sha256') or not binding.get('kind'):
        return None, ('not_verified', 'report has no verifiable contract binding; rerun it for the current contract')
    expected = {'id': score.get('id'), 'revision': score.get('revision'), 'sha256': contract_hash}
    if contract != expected:
        return None, ('fail', 'report contract identity, revision or SHA-256 mismatch; rerun it')
    if binding['kind'] == 'encoded_video':
        if not video_hash:
            return None, ('not_verified', 'report inspected a video but no current video is available for comparison')
        if binding.get('video_sha256') != video_hash:
            return None, ('fail', 'report video SHA-256 mismatch; rerun it on the current encoded file')
    elif binding['kind'] not in ('preview', 'contract_only'):
        return None, ('not_verified', 'report evidence kind is unknown; rerun it')
    return report_for_format(report, format_id)


def report_for_format(report, format_id):
    """A format ID identifies layout overrides even when two outputs have the same dimensions."""
    binding = report.get('evidence_binding') or {}
    if binding.get('kind') == 'contract_only':
        return report, None
    frames = report.get('frames')
    declared = binding.get('format')
    if isinstance(frames, list):
        selected = [f for f in frames if f.get('format', declared or 'base') == format_id]
        if not selected:
            return None, ('not_verified', f'no reviewed frames for format {format_id}; rerun the frame review')
        issues = [i for f in selected for i in f.get('issues', [])]
        return dict(report, frames=selected, formats=[format_id], summary={
            **report.get('summary', {}), 'checkedFrames': sum(bool(f.get('checked')) for f in selected),
            'errors': sum(i.get('severity') == 'error' for i in issues),
            'warnings': sum(i.get('severity') == 'warning' for i in issues),
            'textAudited': sum(bool(f.get('textAudit')) for f in selected)}), None
    if declared == 'all':
        # Aggregate critique findings do not all carry machine-readable format IDs. Keep them conservatively
        # for the legacy base route; a variant needs a selected-format rerun rather than discarding findings.
        if format_id != 'base':
            return None, ('not_verified', f'aggregate critique cannot certify format {format_id}; rerun with --format')
    elif declared is None:
        if format_id != 'base':
            return None, ('not_verified', f'report has no format identity for {format_id}; rerun with --format')
    elif declared != format_id:
        return None, ('fail', f'report format {declared} does not match selected format {format_id}')
    return report, None


def bound_composition(path, composition_hash, format_id='base'):
    """A text audit of a composition outside the contract route counts only for these exact composition bytes."""
    report = load(path)
    binding = report.get('evidence_binding') or {}
    if binding.get('kind') != 'composition' or not (binding.get('composition') or {}).get('sha256'):
        return None, ('not_verified', 'text audit has no composition binding; rerun text-audit.mjs on the composition')
    if binding['composition']['sha256'] != composition_hash:
        return None, ('fail', 'text audit composition SHA-256 mismatch; rerun it on the current composition')
    return report_for_format(report, format_id)


def bound_activity(path, video_hash):
    """Motion activity counts as pacing evidence only for the encoded file it measured."""
    if not path:
        return None, None
    report = load(path)
    if not video_hash or report.get('video_sha256') != video_hash:
        return None, ('not_verified', 'motion activity is not bound to the given encoded file; rerun motion_activity.py --json on it')
    return report, None


def verdict(status, evidence=None, findings=None):
    return {'status': status, 'evidence': evidence or [], 'findings': findings or []}


def technical(score, video):
    if not video:
        return verdict('not_verified', findings=['no encoded file was given'])
    ffprobe = shutil.which('ffprobe')
    if not ffprobe or not os.path.isfile(video):
        return verdict('not_verified', findings=['ffprobe or the video is missing'])
    probe = json.loads(subprocess.run([ffprobe, '-v', 'error', '-count_packets', '-show_entries',
                                       'stream=codec_type,width,height,r_frame_rate,nb_read_packets,duration:format=duration', '-of', 'json', video],
                                      capture_output=True, text=True, check=True).stdout)
    streams = probe.get('streams', [])
    v = next((s for s in streams if s.get('codec_type') == 'video'), None)
    if not v:
        return verdict('fail', findings=['no video stream'])
    num, _, den = v['r_frame_rate'].partition('/')
    fps, want = float(num) / float(den or 1), score['fps']['num'] / score['fps']['den']
    frames = int(v.get('nb_read_packets') or 0)
    has_audio = any(s.get('codec_type') == 'audio' for s in streams)
    expects_audio = expects_sound(score)
    findings = []
    if (v['width'], v['height']) != (score['width'], score['height']):
        findings.append(f"size {v['width']}x{v['height']}, contract {score['width']}x{score['height']}")
    if abs(fps - want) > 0.01:
        findings.append(f'{fps:.3f} fps, contract {want:.3f}')
    if abs(frames - score['totalFrames']) > 1:
        findings.append(f"{frames} frames, contract {score['totalFrames']}")
    # Playback length: the picture and the whole file must run the contract's time (a frame of tolerance; a short
    # audio tail of encoder padding is allowed, a long one is a different video).
    expected = score['totalFrames'] * score['fps']['den'] / score['fps']['num']
    frame = score['fps']['den'] / score['fps']['num']
    video_seconds = float(v.get('duration') or 0)
    file_seconds = float(probe.get('format', {}).get('duration') or 0)
    if video_seconds and abs(video_seconds - expected) > 1.5 * frame:
        findings.append(f'picture runs {video_seconds:.3f} s, contract {expected:.3f} s')
    if file_seconds and file_seconds - expected > max(2 * frame, 0.1):
        findings.append(f'the file plays {file_seconds:.3f} s, contract {expected:.3f} s (a tail without the planned picture)')
    if expects_audio and not has_audio:
        findings.append('the contract has sound but the file has no audio stream')
    evidence = [f"{v['width']}x{v['height']}, {fps:.3f} fps, {frames} frames, {float(probe.get('format', {}).get('duration') or 0):.3f} s, audio {'yes' if has_audio else 'no'}"]
    result = verdict('fail' if findings else 'pass', evidence, findings)
    result['audio'] = has_audio
    return result


def expects_sound(score):
    """Sound is in scope when the contract carries audio files, timed cues or an audio plan other than silence."""
    plan = str(score.get('audio') or '').strip()
    return bool(score.get('music') or score.get('voiceover') or score.get('sfx') or score.get('cues')
                or (plan and not re.match(r'(intentional\s+)?silen', plan, re.I)))


def norm(text):
    return re.sub(r'\s+', ' ', str(text)).strip()


def tokens(text):
    """Preserve locked copy, allowing line wraps and equivalent Unicode composition only."""
    return unicodedata.normalize('NFC', str(text)).split()


def shown_in_order(want, sample_tokens):
    n = len(want)
    return any(sample_tokens[i:i + n] == want for i in range(len(sample_tokens) - n + 1))


def fidelity(score, audit, source_review):
    findings, evidence, unknown = [], [], []
    copy = {k: v for k, v in (score.get('copy') or {}).items() if isinstance(v, str)}
    claims = ((score.get('strategy') or {}).get('claims') or [])
    for claim in claims:
        text = norm(claim.get('text', ''))
        if claim.get('status') != 'verified' and text and any(text.lower() in norm(v).lower() for v in copy.values()):
            findings.append(f'claim "{text}" is {claim.get("status", "unverified")} but appears in the copy')
    for asset in score.get('assets') or []:
        if not asset.get('authority'):
            unknown.append(f'asset {asset.get("id")} has no recorded authority')
    if audit:
        # Each copy entry must appear whole, its words in order, inside one audited frame; words gathered from
        # different frames, a changed number or a changed word order do not count.
        frames = [tokens(' '.join(t['text'] for t in s.get('texts', []) if t.get('visible') != 'hidden')) for s in audit.get('samples', [])]
        missing = [k for k, v in copy.items() if tokens(v) and not any(shown_in_order(tokens(v), f) for f in frames)]
        if missing:
            findings.append('copy not found whole and in order in any audited frame: ' + ', '.join(missing))
        else:
            evidence.append(f'all {len(copy)} copy entries found word for word, in order, within one audited frame each')
    else:
        unknown.append('no text audit: exact copy in the picture not checked')
    if source_review == 'fail':
        findings.append('a person found the product or source misrepresented')
    elif source_review == 'pass':
        evidence.append('a person compared product and source with the frames')
    else:
        unknown.append('nobody compared product and source with the frames')
    status = 'fail' if findings else 'not_verified' if unknown else 'pass'
    return verdict(status, evidence, findings + unknown)


TEMPORAL_AREAS = ('pace', 'transitions', 'hook', 'ending')


def composition(critique, review, audit, composition_review=None):
    findings, evidence, gaps = [], [], []
    if critique:
        status = critique.get('status')
        if status in ('contract_only', 'incomplete'):
            gaps.append(f'critique is {status} (score {critique.get("score")} covers {critique.get("score_scope", "the contract only")}); no picture certified by it')
        else:
            # Every critique error outside the timeline areas (layout, composition, contrast, integration, readability,
            # text amount and any other picture finding) blocks composition; timeline errors block the viewing verdict.
            visual = [f for f in critique.get('findings', []) if f['area'] not in TEMPORAL_AREAS]
            findings += [f'critique {f["severity"]} {f["area"]} {f["where"]}: {f["message"]}' for f in visual if f['severity'] == 'error']
            evidence.append(f'critique inspected frames ({critique.get("frames")}), score {critique.get("score")}')
    if review:
        errors = [i for f in review.get('frames', []) for i in f.get('issues', []) if i.get('severity') == 'error']
        findings += [f'review frame: {i["check"]} {i.get("scene")}/{i.get("element")}: {i.get("detail")}' for i in errors]
        evidence.append(f'frame review: {len(review.get("frames", []))} frames, {review.get("summary", {}).get("checkedFrames")} in holds')
    if audit:
        errors = [i for s in audit.get('samples', []) for i in s.get('issues', []) if i.get('severity') == 'error']
        findings += [f'text audit {i["check"]} "{i.get("text")}": {i.get("detail")}' for i in errors]
        exceptions = sum(len(s.get('exceptions', [])) for s in audit.get('samples', []))
        evidence.append(f'text audit: {audit.get("summary", {}).get("textsChecked")} visible texts in {len(audit.get("samples", []))} samples, {exceptions} declared exceptions')
        if audit.get('verdict') == 'not_verified':
            gaps.append('text audit could not seek the timeline: ' + str(audit.get('reason')))
    if not review and not audit:
        gaps.append('no frame review or text audit: visible text completeness not checked')
    if not critique or critique.get('status') in ('contract_only', 'incomplete'):
        if not review:
            gaps.append('no inspected frames for layout and composition')
    # Checks find measurable defects; whether the frame is well composed is a person's judgement of the key frames.
    if composition_review == 'fail':
        findings.append('a person judged the key frames weak (hierarchy, scale, use of the format or photo integration)')
    elif composition_review == 'pass':
        evidence.append('a person judged the opening, densest and ending frames at full size and phone scale')
    else:
        gaps.append('nobody judged the key frames at full size and phone scale')
    # Warnings are listed for the person who judges the frames; they do not fail the verdict on their own.
    judge = []
    if critique and critique.get('status') in ('checked', 'issues'):
        judge += [f'judge: critique {f["area"]} {f["where"]}: {f["message"]}' for f in critique.get('findings', []) if f['area'] in ('layout', 'composition', 'contrast', 'integration') and f['severity'] == 'warning']
    if review:
        judge += [f'judge: review {i["check"]} {i.get("scene")}/{i.get("element")}: {i.get("detail")}' for f in review.get('frames', []) for i in f.get('issues', []) if i.get('severity') == 'warning']
    status = 'fail' if findings else 'not_verified' if gaps else 'pass'
    return verdict(status, evidence, findings + gaps + judge)


def temporal(critique, playback, temporal_review, note, sound=False, listening='not_heard', sound_review=None, activity=None):
    findings, evidence, gaps = [], [], []
    if activity:
        # motion_activity.py measured the encoded file: still share and the longest undeclared still
        evidence.append(f'motion activity on the encoded file: {activity.get("verdict")}, still {round(100 * activity.get("still_share", 0))} %, '
                        f'longest still {activity.get("longest_still_seconds")} s')
        findings.extend(f'motion activity: {problem}' for problem in activity.get('problems') or [])
    if critique and critique.get('pacing'):
        evidence.append('pacing sampled four times a second: ' + ', '.join(f'{p["scene"]} still {p["longest_still_s"]} s of {p["allowed_s"]} s' for p in critique['pacing']))
        for f in critique.get('findings', []):
            if f['area'] in TEMPORAL_AREAS and f['severity'] in ('warning', 'error'):
                findings.append(f'critique {f["area"]} {f["where"]}: {f["message"]}')
    elif not activity:
        gaps.append('no pacing samples from frames')
    if playback != 'watched':
        gaps.append('nobody watched the encoded file at normal speed')
    else:
        evidence.append('watched at normal speed' + (f': {note}' if note else ''))
    if temporal_review == 'fail':
        findings.append('the viewing found continuity or the commercial argument unclear')
    elif temporal_review == 'pass' and playback == 'watched':
        evidence.append('continuity, hook-to-payoff and CTA judged clear in that viewing')
    else:
        gaps.append('continuity and commercial coherence not judged in a normal-speed viewing')
    if sound:
        if listening != 'heard':
            gaps.append('nobody listened to the sound at normal speed (mix, sync with the picture, levels)')
        elif sound_review == 'fail':
            findings.append('the listening found the sound out of sync, unbalanced or clipped')
        elif sound_review == 'pass':
            evidence.append('sound heard at normal speed: sync, balance and levels judged right')
        else:
            gaps.append('the sound was heard but not judged')
    else:
        evidence.append('no sound in scope: silent contract and no audio stream')
    # Pacing findings are evidence for the viewer, not a verdict: the person who watched decides, and their findings
    # stay listed. Without that viewing the verdict cannot pass, however clean the samples look.
    status = 'fail' if temporal_review == 'fail' or (sound and listening == 'heard' and sound_review == 'fail') else 'not_verified' if gaps else 'pass'
    return verdict(status, evidence, findings + gaps)


def decide(score, args):
    format_id = getattr(args, 'format', 'base')
    selected = score if format_id == 'base' else next((f for f in score.get('formats', []) if f.get('id') == format_id), None)
    if selected is None:
        raise ValueError(f'Unknown format: {format_id}')
    contract_path = getattr(args, 'contract', None)
    contract_hash = file_hash(contract_path) if contract_path else None
    video_hash = file_hash(args.video) if args.video and os.path.isfile(args.video) else None
    critique, critique_gap = bound_report(args.critique, score, contract_hash, video_hash, format_id)
    review, review_gap = bound_report(args.review, score, contract_hash, video_hash, format_id)
    audit, audit_gap = bound_report(args.text_audit, score, contract_hash, video_hash, format_id)
    composition_hash = file_hash(args.composition) if getattr(args, 'composition', None) else None
    if composition_hash and args.text_audit:
        audit, audit_gap = bound_composition(args.text_audit, composition_hash, format_id)
    activity, activity_gap = bound_activity(getattr(args, 'motion_activity', None), video_hash)
    if getattr(args, 'copy', None):
        with open(args.copy, encoding='utf-8') as handle:
            lines = [line.strip() for line in handle if line.strip()]
        score = dict(score, copy={**(score.get('copy') or {}), **{f'locked-{i + 1}': line for i, line in enumerate(lines)}})
    technical_verdict = technical(dict(score, width=selected['width'], height=selected['height']), args.video)
    sound = expects_sound(score) or bool(technical_verdict.pop('audio', False))
    verdicts = {
        'A_technical': technical_verdict,
        'B_fidelity': fidelity(score, audit, args.source_review),
        'C_composition': composition(critique, review, audit, getattr(args, 'composition_review', None)),
        'D_temporal': temporal(critique, args.playback, args.temporal_review, args.note, sound,
                               getattr(args, 'listening', 'not_heard'), getattr(args, 'sound_review', None), activity),
    }
    for label, gap, affected in (
            ('critique', critique_gap, ('C_composition', 'D_temporal')),
            ('review', review_gap, ('C_composition',)),
            ('text audit', audit_gap, ('B_fidelity', 'C_composition')),
            ('motion activity', activity_gap, ('D_temporal',))):
        if gap:
            status, reason = gap
            for key in affected:
                result = verdicts[key]
                if result['status'] != 'fail':
                    result['status'] = status
                result['findings'].append(f'{label}: {reason}')
    states = [v['status'] for v in verdicts.values()]
    overall = 'blocked' if 'fail' in states else 'accepted' if all(s == 'pass' for s in states) else 'deliverable_with_limits'
    return {'contract': score.get('id'), 'revision': score.get('revision'), 'format': format_id, 'video': os.path.basename(args.video) if args.video else None,
            'evidence_binding': {'contract_sha256': contract_hash, 'video_sha256': video_hash},
            'overall': overall, 'verdicts': verdicts,
            'not_verified': [k for k, v in verdicts.items() if v['status'] == 'not_verified'],
            'rule': 'Each verdict stands alone: a passing export or a contract score never passes composition, fidelity or the viewing.'}


def pack(result, args, directory):
    """Copy the judged files into a new delivery folder with a manifest and a handoff note."""
    import shutil as copier
    planned = [(os.path.basename(args.video), args.video), (os.path.basename(args.contract), args.contract)]
    for role, path in (('critique', args.critique), ('review', args.review), ('text-audit', args.text_audit),
                       ('motion-activity', args.motion_activity), ('locked-copy', args.copy)):
        if path:
            planned.append((f'evidence/{role}{os.path.splitext(path)[1] or ".txt"}', path))
    base = os.path.dirname(os.path.abspath(args.contract))
    for path in ([args.composition] if args.composition else []) + list(args.include or []):
        # Keep folders such as fonts/ the contract and composition name relative to it, so the package rerenders.
        relative = os.path.relpath(os.path.abspath(path), base)
        planned.append(('source/' + (os.path.basename(path) if relative.startswith('..') else relative.replace(os.sep, '/')), path))
    names = [name for name, _ in planned]
    if len(set(names)) != len(names):
        raise ValueError('two packaged files would share a name: ' + ', '.join(sorted({n for n in names if names.count(n) > 1})))
    if file_hash(args.video) != result['evidence_binding']['video_sha256'] or file_hash(args.contract) != result['evidence_binding']['contract_sha256']:
        raise ValueError('the video or contract changed while it was judged; run acceptance again')
    os.makedirs(directory)
    for name, path in planned:
        os.makedirs(os.path.dirname(os.path.join(directory, name)) or directory, exist_ok=True)
        copier.copyfile(path, os.path.join(directory, name))
    with open(os.path.join(directory, 'acceptance.json'), 'w', encoding='utf-8') as handle:
        handle.write(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    names.append('acceptance.json')
    rows = [f"| {key} | {value['status']} |" for key, value in result['verdicts'].items()]
    limits = [f'- {key}: {finding}' for key in result['not_verified'] for finding in result['verdicts'][key]['findings']]
    handoff = [f"# Handoff: {result['contract']} revision {result['revision']} ({result['format']})", '',
               f"Status: **{result['overall']}**", '',
               f"Delivered file: `{names[0]}`, SHA-256 `{result['evidence_binding']['video_sha256']}`. The evidence in this "
               'folder covers only these bytes; any change to the video or the contract needs a new acceptance run and a new folder.', '',
               '| Verdict | Status |', '| --- | --- |', *rows, '',
               '## Not verified', '', *(limits or ['- nothing: all four verdicts passed']), '',
               '## Files', '', *[f'- `{name}`' for name in names + ['manifest.json', 'HANDOFF.md']], '',
               '## How to revise', '',
               'Start from the contract and the render script or composition in `source/`, change only what was asked, '
               're-render with the same script, review again and run acceptance with `--pack` into a new folder.']
    if args.note:
        handoff[4:4] = [f'Viewing note: {args.note}', '']
    with open(os.path.join(directory, 'HANDOFF.md'), 'w', encoding='utf-8') as handle:
        handle.write('\n'.join(handoff) + '\n')
    names.append('HANDOFF.md')
    manifest = {'contract': result['contract'], 'revision': result['revision'], 'overall': result['overall'],
                'files': [{'path': name, 'bytes': os.path.getsize(os.path.join(directory, name)),
                           'sha256': file_hash(os.path.join(directory, name))} for name in names]}
    with open(os.path.join(directory, 'manifest.json'), 'w', encoding='utf-8') as handle:
        handle.write(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')


def main(argv=None):
    parser = argparse.ArgumentParser(description='Four separate acceptance verdicts for a motion deliverable.')
    parser.add_argument('contract')
    parser.add_argument('--video')
    parser.add_argument('--format', default='base', help='base or a declared format ID')
    parser.add_argument('--critique')
    parser.add_argument('--review')
    parser.add_argument('--text-audit')
    parser.add_argument('--playback', choices=['watched', 'not_watched'], default='not_watched')
    parser.add_argument('--source-review', choices=['pass', 'fail'])
    parser.add_argument('--temporal-review', choices=['pass', 'fail'])
    parser.add_argument('--composition-review', choices=['pass', 'fail'], help="a person's judgement of the key frames at full size and phone scale")
    parser.add_argument('--listening', choices=['heard', 'not_heard'], default='not_heard', help='someone listened to the sound at normal speed')
    parser.add_argument('--sound-review', choices=['pass', 'fail'], help="that listener's judgement of sync, balance and levels")
    parser.add_argument('--note', help='who watched what, where (recorded with the viewing)')
    parser.add_argument('--motion-activity', help='the JSON from motion_activity.py --json on the encoded file')
    parser.add_argument('--copy', help='locked copy, one entry per line, for a composition whose contract holds none')
    parser.add_argument('--composition', help='the HTML composition a text audit was run on (HyperFrames, GSAP, hand-written)')
    parser.add_argument('--out', help='write the result here (never overwrites)')
    parser.add_argument('--pack', help='write a delivery folder (new) with the judged files, evidence, manifest and HANDOFF.md; never for a blocked film')
    parser.add_argument('--include', action='append', help='a source file to deliver under source/ with --pack (render script, composition assets); repeatable')
    args = parser.parse_args(argv)
    try:
        if args.pack and os.path.exists(args.pack):
            raise ValueError(f'Delivery folder already exists: {args.pack}')
        if args.pack and not (args.video and os.path.isfile(args.video)):
            raise ValueError('--pack needs the encoded file given with --video')
        for path in args.include or []:
            if not os.path.isfile(path):
                raise ValueError(f'Included file not found: {path}')
        result = decide(load(args.contract), args)
        if args.out:
            if os.path.exists(args.out):
                raise ValueError(f'Output file already exists: {args.out}')
            with open(args.out, 'w', encoding='utf-8') as handle:
                handle.write(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
        if args.pack and result['overall'] == 'blocked':
            sys.stderr.write('Not packaged: a verdict failed. Fix it, re-render and run acceptance again.\n')
        elif args.pack:
            pack(result, args, args.pack)
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        sys.stderr.write(f'{error}\n')
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return {'accepted': 0, 'blocked': 1}.get(result['overall'], 3)


if __name__ == '__main__':
    sys.exit(main())
