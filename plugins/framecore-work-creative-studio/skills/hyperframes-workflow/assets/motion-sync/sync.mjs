// Music and voice-over sync for a motion contract. Dependency-free (Node 20+); uses the shared scene engine.
// - Adds a beat grid (score.music: bpm, offset, beats per bar, optional audio file) and reports where each
//   scene, hold and caption starts relative to the beats, with the nearest beat as a proposal.
// - Imports SRT or WebVTT subtitles as captions: exact text goes to the copy ledger, timing to frames.
// It never moves approved scenes: timing changes stay proposals until the contract is revised and approved.
//
//   node sync.mjs motion-score.json --bpm 120 [--offset-ms 0] [--beats-per-bar 4] [--music track.wav]
//                 [--captions voice-over.srt] [--voiceover voice-over.wav] [--out synced.motion-score.json]
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {beatFrames} from '../motion-scenes/motion-scenes.mjs';

const time = /^(?:(\d+):)?(\d{1,2}):(\d{2})[,.](\d{1,3})$/;
const toMs = value => {
  const match = value.trim().match(time);
  if (!match) throw new Error(`Invalid subtitle time: ${value}`);
  const [, h = '0', m, s, ms] = match;
  return ((Number(h) * 60 + Number(m)) * 60 + Number(s)) * 1000 + Number(ms.padEnd(3, '0'));
};

/** Parse SRT or WebVTT text into [{startMs, endMs, text}]. Styling tags are removed; line breaks are kept. */
export function parseSubtitles(text) {
  const cues = [];
  for (const block of text.replace(/^﻿/, '').replace(/\r\n?/g, '\n').split(/\n{2,}/)) {
    const lines = block.split('\n').filter(line => line.trim() !== '');
    const at = lines.findIndex(line => line.includes('-->'));
    if (at < 0) continue; // WEBVTT header, NOTE, STYLE or a stray index
    const [start, rest] = lines[at].split('-->');
    const end = rest.trim().split(/\s+/)[0]; // WebVTT cue settings follow the end time
    const body = lines.slice(at + 1).map(line => line.replace(/<[^>]*>/g, '').replace(/\{\\[^}]*\}/g, '').trim()).filter(Boolean).join('\n');
    if (body) cues.push({startMs: toMs(start), endMs: toMs(end), text: body});
  }
  return cues;
}

const frameAt = (ms, score) => Math.round(ms * score.fps.num / (1000 * score.fps.den));

/** Captions from subtitle cues: exact text into copy as <prefix>-N, timing in master frames. Returns {score, warnings}. */
export function importCaptions(score, cues, {prefix = 'caption', replace = false} = {}) {
  if (score.captions?.length && !replace) throw new Error('The contract already has captions; pass replace to swap them');
  const next = structuredClone(score), warnings = [];
  next.copy = {...next.copy};
  for (const old of score.captions ?? []) delete next.copy[old.copy];
  next.captions = [];
  cues.forEach((cue, i) => {
    const id = `${prefix}-${i + 1}`;
    if (next.copy[id] !== undefined) throw new Error(`Copy ID ${id} is already used; choose another prefix`);
    let start = frameAt(cue.startMs, score), end = frameAt(cue.endMs, score);
    if (start >= score.totalFrames) { warnings.push(`${id} starts at frame ${start}, after the last frame; skipped`); return; }
    if (end > score.totalFrames) { warnings.push(`${id} ends at frame ${end}; cut to ${score.totalFrames}`); end = score.totalFrames; }
    const previous = next.captions[next.captions.length - 1];
    if (previous && start < previous.end) { warnings.push(`${id} overlaps ${previous.id}; it now starts at frame ${previous.end}`); start = previous.end; }
    if (end <= start) { warnings.push(`${id} has no frames left after rounding; skipped`); return; }
    next.copy[id] = cue.text;
    next.captions.push({id, start, end, copy: id});
  });
  return {score: next, warnings};
}

/** Where scene starts, holds and captions fall on the beat grid, with the nearest beat as a proposal. */
export function beatReport(score) {
  const beats = beatFrames(score);
  if (!beats.length) return {framesPerBeat: null, rows: []};
  const framesPerBeat = score.fps.num / score.fps.den * 60 / score.music.bpm;
  const nearest = frame => beats.reduce((best, beat) => (Math.abs(beat.frame - frame) < Math.abs(best.frame - frame) ? beat : best));
  const row = (item, frame) => {
    const beat = nearest(frame);
    return {item, frame, beat: `${beat.bar}.${beat.beatInBar}`, beatFrame: beat.frame, offset: frame - beat.frame, downbeat: beat.beatInBar === 1};
  };
  const rows = [];
  for (const scene of score.scenes) {
    rows.push(row(`${scene.id} start`, scene.start));
    for (const [start] of scene.holds ?? []) rows.push(row(`${scene.id} hold`, start));
  }
  for (const caption of score.captions ?? []) rows.push(row(`${caption.id}`, caption.start));
  return {framesPerBeat, rows};
}

export function reportMarkdown(score) {
  const {framesPerBeat, rows} = beatReport(score);
  if (!framesPerBeat) return 'No beat grid: set music.bpm.\n';
  const lines = [
    `Beat grid: ${score.music.bpm} BPM, ${score.music.beatsPerBar ?? 4} beats per bar, first beat at ${score.music.offsetMs ?? 0} ms; ${Number(framesPerBeat.toFixed(4))} frames per beat.`,
    '',
    '| Event | Frame | Nearest beat (bar.beat) | Beat frame | Offset (frames) |',
    '| --- | --- | --- | --- | --- |',
    ...rows.map(r => `| ${r.item} | ${r.frame} | ${r.beat}${r.downbeat ? ' (downbeat)' : ''} | ${r.beatFrame} | ${r.offset > 0 ? '+' : ''}${r.offset} |`),
    '',
    'Offsets are proposals, not changes: moving a scene or hold changes approved timing and needs a new revision and approval.',
  ];
  return lines.join('\n') + '\n';
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const args = process.argv.slice(2), valued = ['--bpm', '--offset-ms', '--beats-per-bar', '--music', '--captions', '--voiceover', '--out', '--prefix'];
  const option = name => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : undefined; };
  const input = args.find((arg, i) => !arg.startsWith('--') && !valued.includes(args[i - 1]));
  try {
    if (!input) throw new Error('Usage: node sync.mjs motion-score.json [--bpm 120 --offset-ms 0 --beats-per-bar 4 --music track.wav] [--captions vo.srt --voiceover vo.wav] [--out new.json]');
    let score = JSON.parse(fs.readFileSync(input, 'utf8')), changed = false;
    if (option('--bpm')) {
      const bpm = Number(option('--bpm')), offsetMs = Number(option('--offset-ms') ?? 0), beatsPerBar = Number(option('--beats-per-bar') ?? 4);
      if (!(bpm > 0) || !(offsetMs >= 0) || !Number.isInteger(beatsPerBar) || beatsPerBar < 1) throw new Error('--bpm must be positive, --offset-ms at least 0 and --beats-per-bar a positive integer');
      score.music = {...score.music, bpm, offsetMs, beatsPerBar, ...(option('--music') ? {src: option('--music')} : {})};
      changed = true;
    } else if (option('--music')) { score.music = {...score.music, src: option('--music')}; changed = true; }
    if (option('--voiceover')) { score.voiceover = {...score.voiceover, src: option('--voiceover')}; changed = true; }
    if (option('--captions')) {
      const result = importCaptions(score, parseSubtitles(fs.readFileSync(option('--captions'), 'utf8')), {prefix: option('--prefix') ?? 'caption', replace: args.includes('--replace')});
      for (const warning of result.warnings) console.warn('WARN ' + warning);
      score = result.score; changed = true;
      console.log(`${score.captions.length} captions imported.`);
    }
    process.stdout.write(reportMarkdown(score));
    if (changed) {
      const out = option('--out');
      if (!out) console.log('Dry run: nothing written. Pass --out <new file> to save the synced contract.');
      else {
        if (fs.existsSync(out)) throw new Error(`Output file already exists: ${out}`);
        score.revision = (score.revision ?? 0) + 1;
        fs.writeFileSync(out, JSON.stringify(score, null, 2) + '\n');
        console.log(`Wrote ${out} as revision ${score.revision}; earlier approval does not cover it.`);
      }
    }
  } catch (error) {
    console.error(error.message);
    process.exitCode = 2;
  }
}
