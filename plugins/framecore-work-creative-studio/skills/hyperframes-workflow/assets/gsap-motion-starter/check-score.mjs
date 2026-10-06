// Dependency-free check of the shared motion contract (motion-score.json).
// Structural rules match the Motion Graphics Workflow score format; hold lengths
// are compared with the reading heuristic from references/motion-craft.md.
// Storyboard fields are checked whenever present and required with --storyboard.
//
//   node check-score.mjs motion-score.json               timeline and copy check
//   node check-score.mjs motion-score.json --storyboard  also require a complete storyboard
//   node check-score.mjs motion-score.json --markdown    print the storyboard for approval
import fs from 'node:fs';

const approvalStates = ['proposed', 'approved', 'blocked', 'example-not-client-approved'];
const runtimeStates = ['selected', 'proposed', 'unknown'];
const sceneFields = ['purpose', 'focalPoint', 'entry', 'action', 'exit', 'transition', 'audio'];
const text = value => typeof value === 'string' && value.trim().length > 0;

export function checkScore(score, {storyboard = false} = {}) {
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
    if (storyboard) for (const field of sceneFields) if (!text(scene[field])) errors.push(`${scene.id}: storyboard field ${field} is missing`);
    if (scene.acceptance !== undefined && (!Array.isArray(scene.acceptance) || !scene.acceptance.every(text))) errors.push(`${scene.id}: acceptance must be a list of observable criteria`);
  }
  if (!ids.size) errors.push('at least one scene is required');
  if (coverage !== n) errors.push(`scenes cover ${coverage} of ${n} frames`);

  // Storyboard and approval fields.
  const approval = score.approval;
  if (approval !== undefined && typeof approval === 'object' && approval !== null) {
    if (!approvalStates.includes(approval.status)) errors.push(`approval.status must be one of ${approvalStates.join(', ')}`);
    if (approval.status === 'approved' && (!text(approval.evidence) || approval.revision !== score.revision)) errors.push('an approved contract needs approval evidence for its current revision');
  } else if (storyboard) errors.push('approval {status, revision, evidence} is required');
  if (score.runtime !== undefined && !runtimeStates.includes(score.runtime?.status)) errors.push(`runtime.status must be one of ${runtimeStates.join(', ')}`);
  if (score.decisions !== undefined && !['confirmed', 'proposed', 'unknown'].every(key => Array.isArray(score.decisions[key]))) errors.push('decisions needs confirmed, proposed and unknown lists');
  if (score.acceptance !== undefined && (!Array.isArray(score.acceptance) || !score.acceptance.every(text))) errors.push('acceptance must be a list of observable criteria');
  if (storyboard) {
    for (const field of ['goal', 'audience', 'message', 'concept', 'audio']) if (!text(score[field])) errors.push(`storyboard field ${field} is missing`);
    if (!score.runtime) errors.push('runtime {status, value} is required');
    if (!score.decisions) errors.push('decisions {confirmed, proposed, unknown} is required');
    if (!Array.isArray(score.acceptance) || score.acceptance.length < 3) errors.push('at least three observable acceptance criteria are required');
    if (!Array.isArray(score.assets)) errors.push('assets ledger is required (an empty list when no assets are used)');
  }
  return {errors, warnings};
}

const cell = value => String(value ?? '').replace(/\|/g, '\\|').replace(/\n/g, ' ');
const list = values => (values?.length ? values.map(value => `- ${value}`).join('\n') : '- none');

/** Render the contract as a Markdown storyboard for review and approval. */
export function toMarkdown(score) {
  const fps = score.fps.num / score.fps.den;
  const seconds = frame => (frame / fps).toFixed(2);
  const lines = [
    `# Storyboard: ${score.id}, revision ${score.revision}`,
    '',
    `Approval: ${score.approval?.status ?? 'unknown'}${score.approval?.evidence ? ` (${score.approval.evidence})` : ''}. Stage: ${score.stage ?? 'unknown'}. Runtime: ${score.runtime?.status ?? 'unknown'}${score.runtime?.value ? `, ${score.runtime.value}` : ''}.`,
    '',
    `- Goal: ${score.goal ?? ''}`,
    `- Audience: ${score.audience ?? ''}`,
    `- Message: ${score.message ?? ''}`,
    `- Concept: ${score.concept ?? ''}`,
    `- Format: ${score.width} x ${score.height}, ${fps} FPS, ${score.totalFrames} frames (${seconds(score.totalFrames)} s), frames 0..${score.totalFrames - 1}. Viewing: ${score.viewing ?? 'unknown'}. Audio: ${score.audio ?? 'unknown'}.`,
    '',
    '| Scene | Frames [start,end) | Seconds | Copy | Focal point | Entry -> action -> exit | Transition | Readable hold | Audio |',
    '| --- | --- | --- | --- | --- | --- | --- | --- | --- |',
    ...score.scenes.map(scene => `| ${cell(scene.id)}: ${cell(scene.purpose)} | [${scene.start},${scene.end}) | ${seconds(scene.start)}-${seconds(scene.end)} | ${cell((scene.copy ?? []).map(id => `"${score.copy?.[id] ?? id}"`).join(', '))} | ${cell(scene.focalPoint)} | ${cell([scene.entry, scene.action, scene.exit].filter(Boolean).join(' -> '))} | ${cell(scene.transition)} | ${cell((scene.holds ?? []).map(([a, b]) => `[${a},${b})`).join(', '))} | ${cell(scene.audio)} |`),
    '',
    '## Acceptance criteria',
    list([...(score.acceptance ?? []), ...score.scenes.flatMap(scene => (scene.acceptance ?? []).map(item => `${scene.id}: ${item}`))]),
    '',
    '## Decisions',
    `Confirmed:\n${list(score.decisions?.confirmed)}`,
    `Proposed:\n${list(score.decisions?.proposed)}`,
    `Unknown:\n${list(score.decisions?.unknown)}`,
    '',
    `Copy status: ${score.copyStatus ?? 'unknown'}. Assets: ${score.assets?.length ? score.assets.map(asset => asset.id ?? asset).join(', ') : 'none'}.`,
  ];
  return lines.join('\n') + '\n';
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2);
  const file = args.find(arg => !arg.startsWith('--')) ?? 'motion-score.json';
  const score = JSON.parse(fs.readFileSync(file, 'utf8'));
  if (args.includes('--markdown')) process.stdout.write(toMarkdown(score));
  else {
    const {errors, warnings} = checkScore(score, {storyboard: args.includes('--storyboard')});
    for (const warning of warnings) console.warn('WARN ' + warning);
    for (const error of errors) console.error('FAIL ' + error);
    console.log(errors.length ? 'FAIL' : 'PASS');
    process.exitCode = errors.length ? 1 : 0;
  }
}
