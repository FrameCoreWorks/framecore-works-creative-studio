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
// Declarative scene kinds; keep in sync with sceneKinds in motion-scenes.mjs.
const sceneKinds = {
  'line-reveal': {required: ['lines'], copyParams: ['lines']},
  'item-stagger': {required: ['items'], copyParams: ['items']},
  'end-card': {required: ['text'], copyParams: ['text']},
  'counter': {required: ['to'], copyParams: ['label']},
  'quote': {required: ['quote'], copyParams: ['quote', 'attribution']},
  'logo-reveal': {required: ['asset'], copyParams: []},
};
export const knownSceneKinds = Object.keys(sceneKinds);
const text = value => typeof value === 'string' && value.trim().length > 0;

export function checkScore(score, {storyboard = false} = {}) {
  const errors = [], warnings = [];
  const {num, den} = score.fps ?? {};
  if (!Number.isSafeInteger(num) || !Number.isSafeInteger(den) || num <= 0 || den <= 0) errors.push('fps needs positive integer num/den');
  const n = score.totalFrames, fps = num / den;
  if (!Number.isSafeInteger(n) || n < 1) errors.push('totalFrames must be a positive integer');
  if (!Number.isSafeInteger(score.width) || !Number.isSafeInteger(score.height)) errors.push('width and height must be integers');
  checkFormats(score, errors);
  checkSound(score, errors, warnings);
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
    if (scene.kind !== undefined) {
      const kind = sceneKinds[scene.kind], params = scene.params ?? {};
      if (!kind) errors.push(`${scene.id}: unknown scene kind ${scene.kind}; use one of ${knownSceneKinds.join(', ')}`);
      else {
        for (const key of kind.required) if (params[key] === undefined) errors.push(`${scene.id}: ${scene.kind} needs params.${key}`);
        for (const key of kind.copyParams) for (const id of [].concat(params[key] ?? [])) if (typeof score.copy?.[id] !== 'string') errors.push(`${scene.id}: params.${key} references missing copy id ${id}`);
        if (scene.kind === 'logo-reveal' && !text((score.assets ?? []).find(asset => asset.id === params.asset)?.src)) errors.push(`${scene.id}: logo asset ${params.asset} needs an assets entry with src`);
        if (scene.kind === 'counter' && ![params.to, params.from ?? 0].every(Number.isFinite)) errors.push(`${scene.id}: counter from/to must be numbers`);
      }
    }
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

const safeAreaOk = area => area === undefined || (typeof area === 'object' && area !== null && ['top', 'bottom'].every(side => area[side] === undefined || (Number.isFinite(area[side]) && area[side] >= 0 && area[side] < 0.5)));

// Output formats: score.formats lists variants of the base size; 'base' names the score's own size.
function checkFormats(score, errors) {
  if (!safeAreaOk(score.tokens?.safeArea)) errors.push('tokens.safeArea top/bottom must be fractions of the height from 0 to below 0.5');
  if (score.formats === undefined) return;
  if (!Array.isArray(score.formats)) { errors.push('formats must be a list'); return; }
  const ids = new Set(['base']), scenes = new Set((score.scenes ?? []).map(scene => scene.id));
  for (const format of score.formats) {
    const id = format?.id;
    if (typeof id !== 'string' || !/^[A-Za-z0-9-]+$/.test(id) || ids.has(id)) errors.push(`format id missing, invalid, reserved or duplicated: ${id}; use letters, digits and hyphens`);
    ids.add(id);
    if (!Number.isSafeInteger(format?.width) || !Number.isSafeInteger(format?.height) || format.width < 1 || format.height < 1) errors.push(`format ${id}: width and height must be positive integers`);
    if (!safeAreaOk(format?.tokens?.safeArea)) errors.push(`format ${id}: tokens.safeArea top/bottom must be fractions of the height from 0 to below 0.5`);
    for (const sceneId of Object.keys(format?.params ?? {})) if (!scenes.has(sceneId)) errors.push(`format ${id}: params for unknown scene ${sceneId}`);
  }
}

// Music beat grid, voice-over file and captions (exact text in copy, timing in master frames).
function checkSound(score, errors, warnings) {
  const music = score.music, n = score.totalFrames, fps = score.fps?.num / score.fps?.den;
  if (music !== undefined) {
    if (typeof music !== 'object' || music === null) errors.push('music must be an object');
    else {
      if (music.bpm !== undefined && !(Number.isFinite(music.bpm) && music.bpm > 0 && music.bpm <= 400)) errors.push('music.bpm must be a number above 0 and at most 400');
      if (music.offsetMs !== undefined && !(Number.isFinite(music.offsetMs) && music.offsetMs >= 0)) errors.push('music.offsetMs must be 0 or more');
      if (music.beatsPerBar !== undefined && !(Number.isSafeInteger(music.beatsPerBar) && music.beatsPerBar >= 1)) errors.push('music.beatsPerBar must be a positive integer');
    }
  }
  for (const [name, track] of [['music', music], ['voiceover', score.voiceover]]) {
    if (track?.src !== undefined && !text(track.src)) errors.push(`${name}.src must be a file name`);
    if (track?.volume !== undefined && !(Number.isFinite(track.volume) && track.volume >= 0 && track.volume <= 1)) errors.push(`${name}.volume must be from 0 to 1`);
  }
  if (score.captions === undefined) return;
  if (!Array.isArray(score.captions)) { errors.push('captions must be a list'); return; }
  const ids = new Set();
  let previousEnd = 0;
  for (const caption of score.captions) {
    const id = caption?.id;
    if (!text(id) || ids.has(id)) errors.push(`caption id missing or duplicated: ${id}`);
    ids.add(id);
    if (!(Number.isSafeInteger(caption?.start) && Number.isSafeInteger(caption?.end) && caption.start >= 0 && caption.end <= n && caption.end > caption.start)) { errors.push(`caption ${id}: invalid [start,end)`); continue; }
    if (caption.start < previousEnd) errors.push(`caption ${id}: starts before the previous caption ends; captions must be in order without overlap`);
    previousEnd = caption.end;
    if (typeof score.copy?.[caption.copy] !== 'string') { errors.push(`caption ${id}: copy id ${caption.copy} is missing`); continue; }
    const characters = score.copy[caption.copy].length;
    if (Number.isFinite(fps)) {
      const needed = Math.ceil(Math.max(1, characters / 13 + 0.5) * fps);
      if (caption.end - caption.start < needed) warnings.push(`caption ${id}: ${caption.end - caption.start} frames is below the reading heuristic of ${needed} frames for ${characters} characters`);
    }
  }
}

const beatOf = (score, frame) => {
  const music = score.music, fps = score.fps.num / score.fps.den;
  if (!(music?.bpm > 0)) return '';
  const beat = Math.max(0, Math.round((frame / fps - (music.offsetMs ?? 0) / 1000) * music.bpm / 60)), perBar = music.beatsPerBar ?? 4;
  const offset = frame - Math.round(((music.offsetMs ?? 0) / 1000 + beat * 60 / music.bpm) * fps);
  return `${Math.floor(beat / perBar) + 1}.${(beat % perBar) + 1}${offset ? ` (${offset > 0 ? '+' : ''}${offset} f)` : ''}`;
};

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
    ...(score.music?.bpm ? [`- Music: ${score.music.bpm} BPM, ${score.music.beatsPerBar ?? 4} beats per bar, first beat at ${score.music.offsetMs ?? 0} ms${score.music.src ? `, file ${score.music.src}` : ''}. Scene starts below show bar.beat and the offset from the nearest beat.`] : []),
    ...(score.voiceover?.src ? [`- Voice-over: file ${score.voiceover.src}.`] : []),
    ...(score.formats?.length ? [`- Other formats: ${score.formats.map(format => `${format.id} ${format.width} x ${format.height}${format.viewing ? ` (${format.viewing})` : ''}`).join('; ')}.`] : []),
    '',
    '| Scene | Frames [start,end) | Seconds | Copy | Focal point | Entry -> action -> exit | Transition | Readable hold | Audio |',
    '| --- | --- | --- | --- | --- | --- | --- | --- | --- |',
    ...score.scenes.map(scene => `| ${cell(scene.id)}${scene.kind ? ` (${cell(scene.kind)})` : ''}: ${cell(scene.purpose)} | [${scene.start},${scene.end})${score.music?.bpm ? `, beat ${beatOf(score, scene.start)}` : ''} | ${seconds(scene.start)}-${seconds(scene.end)} | ${cell((scene.copy ?? []).map(id => `"${score.copy?.[id] ?? id}"`).join(', '))} | ${cell(scene.focalPoint)} | ${cell([scene.entry, scene.action, scene.exit].filter(Boolean).join(' -> '))} | ${cell(scene.transition)} | ${cell((scene.holds ?? []).map(([a, b]) => `[${a},${b})`).join(', '))} | ${cell(scene.audio)} |`),
    ...(score.captions?.length ? ['', '## Captions', '', '| Caption | Frames [start,end) | Seconds | Text |', '| --- | --- | --- | --- |',
      ...score.captions.map(caption => `| ${cell(caption.id)} | [${caption.start},${caption.end}) | ${seconds(caption.start)}-${seconds(caption.end)} | ${cell(score.copy?.[caption.copy] ?? caption.copy)} |`)] : []),
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
