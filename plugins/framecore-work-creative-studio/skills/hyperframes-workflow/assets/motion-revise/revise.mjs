// Revise a delivered motion contract without redesigning it. Dependency-free (Node 20+).
// - diff: list every changed value between two revisions, to show the user what changed.
// - extend: lengthen or shorten one scene and move everything after it (later scenes, holds,
//   captions, cues and the total length) by the same number of frames.
// Exit code: 0 done, 1 differences or problems reported, 2 setup problem.
//
//   node revise.mjs diff before.motion.json after.motion.json
//   node revise.mjs extend contract.motion.json --scene end --frames 30 --out contract-r2.motion.json
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const isObject = value => value !== null && typeof value === 'object';

/** Every changed leaf value as {path, before, after}; arrays compare by index, missing values are undefined. */
export function diffContracts(before, after, at = '') {
  if (!isObject(before) || !isObject(after) || Array.isArray(before) !== Array.isArray(after)) {
    return JSON.stringify(before) === JSON.stringify(after) ? [] : [{path: at || '(root)', before, after}];
  }
  const keys = [...new Set([...Object.keys(before), ...Object.keys(after)])];
  return keys.flatMap(key => diffContracts(before[key], after[key], Array.isArray(before) ? `${at}[${key}]` : at ? `${at}.${key}` : key));
}

/** The differences as a short Markdown list for the reply: path, old value, new value. */
export function diffMarkdown(changes) {
  if (!changes.length) return 'No changes.\n';
  const show = value => (value === undefined ? '(none)' : JSON.stringify(value));
  return changes.map(c => `- \`${c.path}\`: ${show(c.before)} → ${show(c.after)}`).join('\n') + '\n';
}

/**
 * Lengthen (frames > 0) or shorten (frames < 0) one scene. Its end moves and its holds that ended at the old
 * end stretch with it; every later scene moves as a whole, so overlaps such as a sweep hand-over keep their
 * length; captions and cues from the first later scene or the old end onwards move too; totalFrames follows.
 * Returns a new contract; the input is unchanged. Throws when the change would leave a scene, hold or caption empty.
 */
export function extendScene(score, sceneId, frames) {
  if (!Number.isSafeInteger(frames) || frames === 0) throw new Error('frames must be a non-zero integer');
  const next = structuredClone(score);
  const scene = next.scenes.find(item => item.id === sceneId);
  if (!scene) throw new Error(`Unknown scene: ${sceneId}`);
  const oldEnd = scene.end, later = next.scenes.filter(item => item !== scene && item.start > scene.start);
  const pivot = Math.min(oldEnd, ...later.map(item => item.start));
  const move = value => (value >= pivot ? value + frames : value);
  for (const item of next.scenes) {
    if (item === scene) {
      item.end += frames;
      item.holds = (item.holds ?? []).map(([a, b]) => [a, b >= oldEnd ? b + frames : Math.min(b, item.end)]);
    } else if (later.includes(item)) {
      item.start += frames; item.end += frames;
      item.holds = (item.holds ?? []).map(([a, b]) => [a + frames, b + frames]);
    }
    if (item.end <= item.start || (item.holds ?? []).some(([a, b]) => b <= a)) throw new Error(`Scene ${item.id} would become empty`);
  }
  for (const caption of next.captions ?? []) {
    caption.start = move(caption.start); caption.end = move(caption.end);
    if (caption.end <= caption.start) throw new Error(`Caption ${caption.id} would become empty`);
  }
  for (const cue of next.cues ?? []) cue.frame = move(cue.frame);
  next.totalFrames += frames;
  return next;
}

/** Mark a revised contract: next revision number, approval for it with the user's request as evidence. */
/** Descriptive text fields (not `copy`, `id`, `runtime` or `approval`) that name frames or seconds; after a timing change they must be rewritten by hand. */
export function timingMentions(score, at = '') {
  if (typeof score === 'string') return /\bframes?\b|\b\d+(?:\.\d+)?\s*(?:s|sec|seconds?|fps)\b|\d+\s*[–-]\s*\d+/i.test(score) ? [at] : [];
  if (!isObject(score)) return [];
  return Object.entries(score).flatMap(([key, value]) => (at === '' && ['copy', 'id', 'runtime', 'approval'].includes(key) ? [] : timingMentions(value, Array.isArray(score) ? `${at}[${key}]` : at ? `${at}.${key}` : key)));
}

/** The render script's file name for a revision: `video.render.py` or `video-r1.render.py` becomes `video-r2.render.py`. */
export function scriptName(name, revision) {
  const dot = name.indexOf('.');
  const stem = dot < 0 ? name : name.slice(0, dot), rest = dot < 0 ? '' : name.slice(dot);
  return `${stem.replace(/-r\d+$/, '')}-r${revision}${rest}`;
}

export function nextRevision(score, evidence) {
  const revision = (score.revision ?? 0) + 1;
  const next = {...structuredClone(score), revision, approval: evidence ? {status: 'approved', revision, evidence} : {status: 'proposed', revision: null, evidence: null}};
  if (typeof next.runtime?.script === 'string') next.runtime.script = scriptName(next.runtime.script, revision);
  return next;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const [command, ...args] = process.argv.slice(2);
  const option = name => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : undefined; };
  const read = file => JSON.parse(fs.readFileSync(file, 'utf8'));
  try {
    if (command === 'diff' && args.length >= 2) {
      const changes = diffContracts(read(args[0]), read(args[1]));
      process.stdout.write(diffMarkdown(changes));
      process.exitCode = changes.length ? 1 : 0;
    } else if (command === 'extend' && args[0] && option('--scene') && option('--frames') && option('--out')) {
      const out = option('--out');
      if (fs.existsSync(out)) throw new Error(`Output file already exists: ${out}`);
      const before = read(args[0]);
      const after = nextRevision(extendScene(before, option('--scene'), Number(option('--frames'))), option('--evidence'));
      fs.writeFileSync(out, JSON.stringify(after, null, 2) + '\n');
      process.stdout.write(diffMarkdown(diffContracts(before, after)));
      const mentions = timingMentions(after);
      if (mentions.length) process.stdout.write(`\nCheck these text fields that name frames or seconds and rewrite any that the change made wrong:\n${mentions.map(item => `- \`${item}\``).join('\n')}\n`);
    } else {
      throw new Error('Usage: node revise.mjs diff <before.json> <after.json> | extend <contract.json> --scene <id> --frames <n> --out <new.json> [--evidence "<request>"]');
    }
  } catch (error) {
    console.error(error.message);
    process.exitCode = 2;
  }
}
