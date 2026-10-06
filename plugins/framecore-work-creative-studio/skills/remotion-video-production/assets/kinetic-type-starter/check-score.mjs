// Dependency-free check of the shared motion score before preview or render.
// Structural rules match the Motion Graphics Workflow score format; hold lengths
// are compared with the reading heuristic from references/motion-craft.md.
import fs from 'node:fs';

export function checkScore(score) {
  const errors = [], warnings = [];
  const {num, den} = score.fps ?? {};
  if (!Number.isSafeInteger(num) || !Number.isSafeInteger(den) || num <= 0 || den <= 0) errors.push('fps needs positive integer num/den');
  const n = score.totalFrames, fps = num / den;
  if (!Number.isSafeInteger(n) || n < 1) errors.push('totalFrames must be a positive integer');
  if (!Number.isSafeInteger(score.width) || !Number.isSafeInteger(score.height)) errors.push('width and height must be integers');
  let coverage = 0;
  const ids = new Set();
  for (const scene of score.scenes ?? []) {
    if (!scene.id || ids.has(scene.id)) errors.push(`scene id missing or duplicated: ${scene.id}`);
    ids.add(scene.id);
    if (!(Number.isSafeInteger(scene.start) && Number.isSafeInteger(scene.end) && scene.start >= 0 && scene.end <= n && scene.end > scene.start)) errors.push(`${scene.id}: invalid [start,end)`);
    if (scene.start > coverage) errors.push(`${scene.id}: frames ${coverage}..${scene.start - 1} are not covered`);
    coverage = Math.max(coverage, scene.end);
    const characters = (scene.copy ?? []).map(id => {
      if (typeof score.copy?.[id] !== 'string') errors.push(`${scene.id}: copy id ${id} is missing`);
      return score.copy?.[id] ?? '';
    }).join(' ').length;
    const holds = scene.holds ?? [];
    for (const [start, end] of holds) if (!(start >= scene.start && end <= scene.end && end > start)) errors.push(`${scene.id}: hold [${start},${end}) outside the scene`);
    if (characters && Number.isFinite(fps)) {
      const needed = Math.ceil(Math.max(1, characters / 13 + 0.5) * fps);
      const longest = Math.max(0, ...holds.map(([start, end]) => end - start));
      if (longest < needed) warnings.push(`${scene.id}: longest hold ${longest} frames is below the reading heuristic of ${needed} frames for ${characters} characters`);
    }
  }
  if (!ids.size) errors.push('at least one scene is required');
  if (coverage !== n) errors.push(`scenes cover ${coverage} of ${n} frames`);
  return {errors, warnings};
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const file = process.argv[2] ?? 'motion-score.json';
  const {errors, warnings} = checkScore(JSON.parse(fs.readFileSync(file, 'utf8')));
  for (const warning of warnings) console.warn('WARN ' + warning);
  for (const error of errors) console.error('FAIL ' + error);
  console.log(errors.length ? 'FAIL' : 'PASS');
  process.exitCode = errors.length ? 1 : 0;
}
