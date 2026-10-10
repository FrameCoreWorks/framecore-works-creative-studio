#!/usr/bin/env python3
"""Acceptance of a motion deliverable as four separate verdicts, from the evidence that actually exists.

  python acceptance.py video.motion.json --video video.mp4 --critique critique-r2/critique.json
         [--review review-out/review.json] [--text-audit audit-out/text-audit.json]
         [--playback watched|not_watched] [--source-review pass|fail] [--composition-review pass|fail] [--temporal-review pass|fail]
         [--note "who watched what, where"] [--out acceptance.json]

A. technical    the encoded file matches the contract: size, frame rate, frame count, duration, audio presence
B. fidelity     exact copy reaches the picture, unverified claims are not used, every asset has an authority, and
                (by a person) the product and source look right
C. composition  every visible text is complete in readable holds, the layout rules pass in inspected frames, and a
                person judged the key frames at full size and phone scale
D. temporal     pacing evidence plus a person's normal-speed viewing of continuity and the commercial argument

Each verdict is pass, fail or not_verified. Evidence that was not produced leaves its verdict not_verified: a
contract-only critique score (any number) never makes C pass, a valid export never makes C or D pass, and D needs a
recorded normal-speed viewing. Overall: accepted (all four pass), deliverable_with_limits (nothing failed, something
not verified, listed) or blocked (a verdict failed). Exit code 0 accepted, 1 blocked, 3 with limits, 2 setup problem.
Python 3.8+, standard library; ffprobe for --video.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys


def load(path):
    with open(path, encoding='utf-8') as handle:
        return json.load(handle)


def verdict(status, evidence=None, findings=None):
    return {'status': status, 'evidence': evidence or [], 'findings': findings or []}


def technical(score, video):
    if not video:
        return verdict('not_verified', findings=['no encoded file was given'])
    ffprobe = shutil.which('ffprobe')
    if not ffprobe or not os.path.isfile(video):
        return verdict('not_verified', findings=['ffprobe or the video is missing'])
    probe = json.loads(subprocess.run([ffprobe, '-v', 'error', '-count_packets', '-show_entries',
                                       'stream=codec_type,width,height,r_frame_rate,nb_read_packets:format=duration', '-of', 'json', video],
                                      capture_output=True, text=True, check=True).stdout)
    streams = probe.get('streams', [])
    v = next((s for s in streams if s.get('codec_type') == 'video'), None)
    if not v:
        return verdict('fail', findings=['no video stream'])
    num, _, den = v['r_frame_rate'].partition('/')
    fps, want = float(num) / float(den or 1), score['fps']['num'] / score['fps']['den']
    frames = int(v.get('nb_read_packets') or 0)
    has_audio = any(s.get('codec_type') == 'audio' for s in streams)
    expects_audio = bool(score.get('music') or score.get('voiceover') or score.get('sfx'))
    findings = []
    if (v['width'], v['height']) != (score['width'], score['height']):
        findings.append(f"size {v['width']}x{v['height']}, contract {score['width']}x{score['height']}")
    if abs(fps - want) > 0.01:
        findings.append(f'{fps:.3f} fps, contract {want:.3f}')
    if abs(frames - score['totalFrames']) > 1:
        findings.append(f"{frames} frames, contract {score['totalFrames']}")
    if expects_audio and not has_audio:
        findings.append('the contract has sound but the file has no audio stream')
    evidence = [f"{v['width']}x{v['height']}, {fps:.3f} fps, {frames} frames, {float(probe.get('format', {}).get('duration') or 0):.3f} s, audio {'yes' if has_audio else 'no'}"]
    return verdict('fail' if findings else 'pass', evidence, findings)


def norm(text):
    return re.sub(r'\s+', ' ', str(text)).strip()


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
        shown = [norm(t['text']) for s in audit.get('samples', []) for t in s.get('texts', []) if t.get('visible') != 'hidden']
        flat = ' | '.join(shown)
        missing = [k for k, v in copy.items() if norm(v) and norm(v) not in flat and not all(word in flat for word in norm(v).split())]
        if missing:
            findings.append('copy not found in any audited frame: ' + ', '.join(missing))
        else:
            evidence.append(f'all {len(copy)} copy entries found verbatim in audited frames')
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


def temporal(critique, playback, temporal_review, note):
    findings, evidence, gaps = [], [], []
    if critique and critique.get('pacing'):
        evidence.append('pacing sampled four times a second: ' + ', '.join(f'{p["scene"]} still {p["longest_still_s"]} s of {p["allowed_s"]} s' for p in critique['pacing']))
        for f in critique.get('findings', []):
            if f['area'] in TEMPORAL_AREAS and f['severity'] in ('warning', 'error'):
                findings.append(f'critique {f["area"]} {f["where"]}: {f["message"]}')
    else:
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
    # Pacing findings are evidence for the viewer, not a verdict: the person who watched decides, and their findings
    # stay listed. Without that viewing the verdict cannot pass, however clean the samples look.
    status = 'fail' if temporal_review == 'fail' else 'not_verified' if gaps else 'pass'
    return verdict(status, evidence, findings + gaps)


def decide(score, args):
    critique = load(args.critique) if args.critique else None
    review = load(args.review) if args.review else None
    audit = load(args.text_audit) if args.text_audit else None
    verdicts = {
        'A_technical': technical(score, args.video),
        'B_fidelity': fidelity(score, audit, args.source_review),
        'C_composition': composition(critique, review, audit, getattr(args, 'composition_review', None)),
        'D_temporal': temporal(critique, args.playback, args.temporal_review, args.note),
    }
    states = [v['status'] for v in verdicts.values()]
    overall = 'blocked' if 'fail' in states else 'accepted' if all(s == 'pass' for s in states) else 'deliverable_with_limits'
    return {'contract': score.get('id'), 'revision': score.get('revision'), 'video': os.path.basename(args.video) if args.video else None,
            'overall': overall, 'verdicts': verdicts,
            'not_verified': [k for k, v in verdicts.items() if v['status'] == 'not_verified'],
            'rule': 'Each verdict stands alone: a passing export or a contract score never passes composition, fidelity or the viewing.'}


def main(argv=None):
    parser = argparse.ArgumentParser(description='Four separate acceptance verdicts for a motion deliverable.')
    parser.add_argument('contract')
    parser.add_argument('--video')
    parser.add_argument('--critique')
    parser.add_argument('--review')
    parser.add_argument('--text-audit')
    parser.add_argument('--playback', choices=['watched', 'not_watched'], default='not_watched')
    parser.add_argument('--source-review', choices=['pass', 'fail'])
    parser.add_argument('--temporal-review', choices=['pass', 'fail'])
    parser.add_argument('--composition-review', choices=['pass', 'fail'], help="a person's judgement of the key frames at full size and phone scale")
    parser.add_argument('--note', help='who watched what, where (recorded with the viewing)')
    parser.add_argument('--out', help='write the result here (never overwrites)')
    args = parser.parse_args(argv)
    try:
        result = decide(load(args.contract), args)
        if args.out:
            if os.path.exists(args.out):
                raise ValueError(f'Output file already exists: {args.out}')
            with open(args.out, 'w', encoding='utf-8') as handle:
                handle.write(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        sys.stderr.write(f'{error}\n')
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return {'accepted': 0, 'blocked': 1}.get(result['overall'], 3)


if __name__ == '__main__':
    sys.exit(main())
