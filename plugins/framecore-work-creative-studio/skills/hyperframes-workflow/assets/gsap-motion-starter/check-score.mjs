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
  'device': {required: ['screens'], copyParams: ['caption', 'url']},
};
export const knownSceneKinds = Object.keys(sceneKinds);
// Sound designs of motion-sound/synth.py; keep in sync with DESIGNS there.
const soundDesigns = ['whoosh', 'impact', 'boom', 'riser', 'click', 'release', 'tick', 'knock', 'landing', 'tap', 'pop', 'swish', 'shimmer'];
const text = value => typeof value === 'string' && value.trim().length > 0;

export function checkScore(score, {storyboard = false} = {}) {
  const errors = [], warnings = [];
  if (score.schema_version !== undefined && score.schema_version !== 1) errors.push(`schema_version must be the number 1, not ${JSON.stringify(score.schema_version)}`);
  if (score.audio !== undefined && typeof score.audio !== 'string') errors.push('audio must be text: the audio plan or "intentional silence"; audio files go in music and voiceover');
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
        if (params.background !== undefined && !text(params.background)) errors.push(`${scene.id}: background must be a colour`);
        if (params.backgroundWipe !== undefined && !['none', 'left', 'right', 'up', 'down'].includes(params.backgroundWipe)) errors.push(`${scene.id}: backgroundWipe must be none, left, right, up or down`);
        if (scene.kind === 'device') {
          const shots = Array.isArray(params.screens) ? params.screens : [];
          if (!shots.length) errors.push(`${scene.id}: device needs at least one screen`);
          if (params.frame !== undefined && !['phone', 'window', 'browser'].includes(params.frame)) errors.push(`${scene.id}: device frame must be phone, window or browser`);
          (Array.isArray(params.taps) ? params.taps : params.taps === undefined ? [] : [null]).forEach((tap, i) => {
            const inside = value => value === undefined || (Number.isFinite(value) && value >= 0 && value <= 1);
            if (!(Number.isInteger(tap?.at) && tap.at >= 4 && scene.start + tap.at < scene.end && inside(tap.x) && inside(tap.y))) errors.push(`${scene.id}: tap ${i + 1} needs an integer at (at least 4, inside the scene) and x, y between 0 and 1`);
          });
          if (params.transition !== undefined && !['push', 'fade', 'cut'].includes(params.transition)) errors.push(`${scene.id}: device transition must be push, fade or cut`);
          shots.forEach((shot, i) => {
            const asset = (score.assets ?? []).find(item => item.id === shot?.asset);
            if (!text(asset?.src) || !(asset.width > 0) || !(asset.height > 0)) errors.push(`${scene.id}: screen ${i + 1} needs an assets entry with src, width and height`);
            if (i > 0 && !(Number.isInteger(shot.at) && shot.at > (shots[i - 1].at ?? 0) && scene.start + shot.at < scene.end)) errors.push(`${scene.id}: screen ${i + 1} needs an integer at after the previous screen and inside the scene`);
          });
        }
        if (scene.kind === 'logo-reveal' && !text((score.assets ?? []).find(asset => asset.id === params.asset)?.src)) errors.push(`${scene.id}: logo asset ${params.asset} needs an assets entry with src`);
        if (scene.kind === 'counter' && ![params.to, params.from ?? 0].every(Number.isFinite)) errors.push(`${scene.id}: counter from/to must be numbers`);
        if (params.exit !== undefined && ![true, false, 'lift', 'sweep'].includes(params.exit)) errors.push(`${scene.id}: params.exit must be true, false, 'lift' or 'sweep'`);
        if (params.sweepFrames !== undefined && !(Number.isSafeInteger(params.sweepFrames) && params.sweepFrames >= 1 && params.sweepFrames <= scene.end - scene.start)) errors.push(`${scene.id}: params.sweepFrames must be a positive integer within the scene`);
      }
    }
  }
  if (!ids.size) errors.push('at least one scene is required');
  if (coverage !== n) errors.push(`scenes cover ${coverage} of ${n} frames`);

  // Storyboard and approval fields.
  const approval = score.approval;
  if (approval !== undefined && typeof approval === 'object' && approval !== null) {
    if (!approvalStates.includes(approval.status)) errors.push(`approval.status must be one of ${approvalStates.join(', ')}; a direct request to build a complete brief is "approved" with evidence quoting it`);
    if (approval.status === 'approved' && (!text(approval.evidence) || approval.revision !== score.revision)) errors.push('an approved contract needs approval evidence for its current revision');
  } else if (storyboard) errors.push('approval {status, revision, evidence} is required');
  if (score.runtime !== undefined && !runtimeStates.includes(score.runtime?.status)) errors.push(`runtime.status must be one of ${runtimeStates.join(', ')}`);
  if (score.sfx !== undefined) {
    if (!Array.isArray(score.sfx)) errors.push('sfx must be a list of {frame, sound, gain, pan} cues');
    else score.sfx.forEach((cue, i) => {
      if (!(Number.isInteger(cue?.frame) && cue.frame >= 0 && cue.frame < score.totalFrames)) errors.push(`sfx ${i + 1}: frame must be an integer inside the timeline`);
      if (!soundDesigns.includes(cue?.sound)) errors.push(`sfx ${i + 1}: sound must be one of ${soundDesigns.join(', ')}`);
      if (cue?.params !== undefined && (typeof cue.params !== 'object' || cue.params === null || Array.isArray(cue.params))) errors.push(`sfx ${i + 1}: params must be an object`);
      if (cue?.gain !== undefined && !(Number.isFinite(cue.gain) && cue.gain <= 6)) errors.push(`sfx ${i + 1}: gain must be a number of dB, at most 6`);
      if (cue?.pan !== undefined && !(Number.isFinite(cue.pan) && cue.pan >= -1 && cue.pan <= 1)) errors.push(`sfx ${i + 1}: pan must be between -1 and 1`);
      if (i > 0 && Number.isInteger(cue?.frame) && cue.frame < score.sfx[i - 1]?.frame) errors.push(`sfx ${i + 1}: cues must be in frame order`);
    });
  }
  if (score.runtime?.script !== undefined && !(text(score.runtime.script) && /^[^/\\:]+\.[A-Za-z0-9]+$/.test(score.runtime.script))) errors.push('runtime.script must be the plain file name of the delivered render script, such as video-r2.render.py');
  if (score.decisions !== undefined && !['confirmed', 'proposed', 'unknown'].every(key => Array.isArray(score.decisions[key]))) errors.push('decisions needs confirmed, proposed and unknown lists');
  if (score.acceptance !== undefined && (!Array.isArray(score.acceptance) || !score.acceptance.every(text))) errors.push('acceptance must be a list of observable criteria');
  if (storyboard) {
    for (const field of ['goal', 'audience', 'message', 'concept', 'audio']) if (!text(score[field]) && !(field === 'audio' && score.audio !== undefined)) errors.push(`storyboard field ${field} is missing`);
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
