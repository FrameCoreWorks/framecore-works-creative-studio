import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {validateMotionToolkit} from '../scripts/validate-motion-toolkit.mjs';
import '../skills/hyperframes-workflow/assets/motion-toolkit/timeline.test.mjs';
import './motion-quality.test.mjs';
const root = fileURLToPath(new URL('../', import.meta.url));
const canvas = 'skills/hyperframes-workflow/assets/motion-toolkit';
function withCopy(action) {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'studio-motion-'));
  try {
    for (const relative of ['skills/hyperframes-workflow','skills/remotion-video-production/assets']) fs.cpSync(path.join(root,relative),path.join(tmp,relative),{recursive:true});
    action(tmp);
  } finally {fs.rmSync(tmp,{recursive:true,force:true});}
}
test('motion toolkit source inventory and pinned dependency graphs agree', () => assert.deepEqual(validateMotionToolkit(root), []));
test('missing example source fails', () => withCopy(tmp => {
  fs.rmSync(path.join(tmp,canvas,'renderers.mjs'));
  assert.ok(validateMotionToolkit(tmp).some(e => e.detail.includes('Missing:') && e.detail.includes('renderers.mjs')));
}));
test('unpinned dependency and altered graph fail', () => withCopy(tmp => {
  const file=path.join(tmp,canvas,'package.json'),pkg=JSON.parse(fs.readFileSync(file,'utf8'));
  pkg.dependencies['pixi.js']='^8.22.0';fs.writeFileSync(file,JSON.stringify(pkg));
  const errors=validateMotionToolkit(tmp);assert.ok(errors.some(e=>e.detail.includes('exact version')));assert.ok(errors.some(e=>e.detail.includes('lock mismatch')));
}));
test('bundled runtime installation fails', () => withCopy(tmp => {
  fs.mkdirSync(path.join(tmp,canvas,'node_modules'));
  assert.ok(validateMotionToolkit(tmp).some(e=>e.detail.includes('must stay outside')));
}));

const kinetic = 'skills/remotion-video-production/assets/kinetic-type-starter';
const gsapStarter = 'skills/hyperframes-workflow/assets/gsap-motion-starter';
test('runtime starters share one valid motion score with readable holds', async () => {
  const {validateScore} = await import('../skills/hyperframes-workflow/assets/motion-quality/score.mjs');
  const {checkScore} = await import(path.join(root, kinetic, 'check-score.mjs'));
  const score = JSON.parse(fs.readFileSync(path.join(root, kinetic, 'motion-score.json'), 'utf8'));
  assert.doesNotThrow(() => validateScore(score));
  assert.deepEqual(checkScore(score), {errors: [], warnings: []});
  assert.equal(fs.readFileSync(path.join(root, gsapStarter, 'motion-score.json'), 'utf8'), fs.readFileSync(path.join(root, kinetic, 'motion-score.json'), 'utf8'));
});
test('starter checker rejects gaps, missing copy and short holds', async () => {
  const {checkScore} = await import(path.join(root, kinetic, 'check-score.mjs'));
  const score = JSON.parse(fs.readFileSync(path.join(root, kinetic, 'motion-score.json'), 'utf8'));
  const gap = structuredClone(score); gap.scenes[1].start = gap.scenes[0].end + 5;
  assert.ok(checkScore(gap).errors.some(error => error.includes('not covered')));
  const missing = structuredClone(score); delete missing.copy['step-2'];
  assert.ok(checkScore(missing).errors.some(error => error.includes('step-2')));
  const short = structuredClone(score); short.scenes[0].holds = [[24, 40]];
  assert.ok(checkScore(short).warnings.some(warning => warning.includes('reading heuristic')));
});
test('diverging starter contracts fail the toolkit check', () => withCopy(tmp => {
  const file = path.join(tmp, gsapStarter, 'motion-score.json');
  fs.writeFileSync(file, fs.readFileSync(file, 'utf8').replace('"Ready to render"', '"Ready"'));
  assert.ok(validateMotionToolkit(tmp).some(error => error.detail.includes('motion-score.json differs')));
}));
test('single-file preview stays offline and embeds the shared contract', () => {
  assert.deepEqual(validateMotionToolkit(root).filter(error => error.detail.includes('Single-file')), []);
  withCopy(tmp => {
    const file = path.join(tmp, 'skills/hyperframes-workflow/assets/single-file-preview/motion-preview.html');
    fs.writeFileSync(file, fs.readFileSync(file, 'utf8').replace('<title>', '<script src="https://cdn.example.com/lib.js"></script><title>'));
    assert.ok(validateMotionToolkit(tmp).some(error => error.detail.includes('external resources')));
  });
  withCopy(tmp => {
    const file = path.join(tmp, 'skills/hyperframes-workflow/assets/single-file-preview/motion-preview.html');
    fs.writeFileSync(file, fs.readFileSync(file, 'utf8').replace('"Ready to render"', '"Ready"'));
    assert.ok(validateMotionToolkit(tmp).some(error => error.detail.includes('score differs')));
  });
});
test('starter contract is a complete storyboard and renders for approval', async () => {
  const {checkScore, toMarkdown} = await import(path.join(root, kinetic, 'check-score.mjs'));
  const score = JSON.parse(fs.readFileSync(path.join(root, kinetic, 'motion-score.json'), 'utf8'));
  assert.deepEqual(checkScore(score, {storyboard: true}), {errors: [], warnings: []});
  const markdown = toMarkdown(score);
  assert.match(markdown, /\| title \(line-reveal\): State the idea/);
  assert.match(markdown, /\[205,300\)/);
  assert.match(markdown, /## Acceptance criteria/);
});
test('storyboard check rejects incomplete scenes and unsupported approval', async () => {
  const {checkScore} = await import(path.join(root, kinetic, 'check-score.mjs'));
  const score = JSON.parse(fs.readFileSync(path.join(root, kinetic, 'motion-score.json'), 'utf8'));
  const missing = structuredClone(score); delete missing.scenes[1].focalPoint; missing.acceptance = ['one'];
  const found = checkScore(missing, {storyboard: true}).errors.join('\n');
  assert.match(found, /steps: storyboard field focalPoint/);
  assert.match(found, /three observable acceptance criteria/);
  assert.deepEqual(checkScore(missing).errors, []);
  const approved = structuredClone(score); approved.approval = {status: 'approved', revision: 1, evidence: null};
  assert.ok(checkScore(approved).errors.some(error => error.includes('approval evidence')));
  const stale = structuredClone(score); stale.revision = 2; stale.approval = {status: 'approved', revision: 1, evidence: 'Owner approval in chat'};
  assert.ok(checkScore(stale).errors.some(error => error.includes('current revision')));
});

const scenesDir = 'skills/hyperframes-workflow/assets/motion-scenes';
test('scene engine renders every kind deterministically and never scales a logo', async () => {
  const {buildScene, sceneFrame, sceneKinds} = await import(path.join(root, scenesDir, 'motion-scenes.mjs'));
  const score = JSON.parse(fs.readFileSync(path.join(root, scenesDir, 'examples/all-kinds.motion-score.json'), 'utf8'));
  assert.deepEqual(new Set(score.scenes.map(scene => scene.kind)), new Set(Object.keys(sceneKinds)));
  for (const scene of score.scenes) {
    assert.ok(buildScene(scene, score).children.length > 0, scene.id);
    for (const frame of [scene.start, Math.floor((scene.start + scene.end) / 2), scene.end - 1]) {
      assert.deepEqual(sceneFrame(scene, score, frame), sceneFrame(scene, score, frame));
    }
  }
  const logo = score.scenes.find(scene => scene.kind === 'logo-reveal');
  for (let frame = logo.start; frame < logo.end; frame++) assert.deepEqual(Object.keys(sceneFrame(logo, score, frame).logo.style), ['clipPath']);
  const counter = score.scenes.find(scene => scene.kind === 'counter');
  assert.equal(sceneFrame(counter, score, counter.end - 1).number.text, '775');
  assert.throws(() => buildScene({...logo, kind: 'spin'}, score), /Unknown scene kind/);
});
test('checker kinds match the engine and the all-kinds example is a complete storyboard', async () => {
  const {sceneKinds} = await import(path.join(root, scenesDir, 'motion-scenes.mjs'));
  const {checkScore, knownSceneKinds} = await import(path.join(root, kinetic, 'check-score.mjs'));
  const {validateScore} = await import('../skills/hyperframes-workflow/assets/motion-quality/score.mjs');
  assert.deepEqual(knownSceneKinds, Object.keys(sceneKinds));
  const score = JSON.parse(fs.readFileSync(path.join(root, scenesDir, 'examples/all-kinds.motion-score.json'), 'utf8'));
  assert.doesNotThrow(() => validateScore(score));
  assert.deepEqual(checkScore(score, {storyboard: true}), {errors: [], warnings: []});
  const bad = structuredClone(score);
  bad.scenes[0].params.asset = 'missing'; bad.scenes[1].kind = 'spin'; bad.scenes[3].params.label = 'nope';
  const errors = checkScore(bad).errors.join('\n');
  assert.match(errors, /logo asset missing/); assert.match(errors, /unknown scene kind spin/); assert.match(errors, /missing copy id nope/);
});
test('formats resolve from one contract and keep the 16:9 layout unchanged', async () => {
  const {buildScene, sceneFrame, resolveFormat, nodesByKey: nodesOf} = await import(path.join(root, scenesDir, 'motion-scenes.mjs'));
  const {checkScore} = await import(path.join(root, kinetic, 'check-score.mjs'));
  const score = JSON.parse(fs.readFileSync(path.join(root, kinetic, 'motion-score.json'), 'utf8'));
  assert.equal(resolveFormat(score), score); assert.equal(resolveFormat(score, 'base'), score);
  assert.throws(() => resolveFormat(score, '4x5'), /Unknown format/);
  const tall = resolveFormat(score, '9x16'), steps = scene => scene.find(s => s.id === 'steps');
  assert.deepEqual([tall.width, tall.height, tall.format], [1080, 1920, '9x16']);
  assert.deepEqual(tall.scenes.find(s => s.id === 'title').params, {lines: ['title-1', 'title-2'], sizes: [112, 80]});
  assert.equal(score.scenes.find(s => s.id === 'title').params.sizes, undefined);
  // Base layout: a horizontal row with a scaleX connector; vertical formats stack with a scaleY connector.
  const wide = nodesOf(buildScene(steps(score.scenes), score));
  assert.equal(wide.row.style.flexDirection, undefined); assert.equal(wide.connector.style.height, '6px');
  assert.match(sceneFrame(steps(score.scenes), score, 160).connector.style.transform, /^scaleX/);
  const stacked = nodesOf(buildScene(steps(tall.scenes), tall));
  assert.equal(stacked.row.style.flexDirection, 'column'); assert.equal(stacked['item-0'].style.fontSize, '104px');
  assert.match(sceneFrame(steps(tall.scenes), tall, 160).connector.style.transform, /^scaleY/);
  const forcedRow = {...steps(tall.scenes), params: {...steps(tall.scenes).params, direction: 'row'}};
  assert.equal(nodesOf(buildScene(forcedRow, tall)).row.style.flexDirection, undefined);
  // Safe area is opt-in and becomes column padding.
  assert.equal(buildScene(score.scenes[0], score).style.padding, '0 154px');
  const safe = {...tall, tokens: {...tall.tokens, safeArea: {top: 0.1, bottom: 0.2}}};
  assert.equal(buildScene(safe.scenes[0], safe).style.padding, '192px 86px 384px');
  // Checker rules for formats.
  const bad = structuredClone(score);
  bad.formats.push({id: 'base', width: 10, height: 10}, {id: 'x y', width: 1.5, height: 10, params: {nope: {}}, tokens: {safeArea: {top: 0.7}}});
  const errors = checkScore(bad).errors.join('\n');
  assert.match(errors, /reserved or duplicated: base/); assert.match(errors, /invalid.*x y/);
  assert.match(errors, /format x y: width and height/); assert.match(errors, /unknown scene nope/); assert.match(errors, /format x y: tokens.safeArea/);
});
test('diverging scene engine copies fail the toolkit check', () => {
  withCopy(tmp => {
    const file = path.join(tmp, kinetic, 'src/motion-scenes.mjs');
    fs.writeFileSync(file, fs.readFileSync(file, 'utf8').replace('scale(${0.94 + 0.06 * k})', 'scale(1)'));
    assert.ok(validateMotionToolkit(tmp).some(error => error.detail.includes('Remotion starter scene engine differs')));
  });
  withCopy(tmp => {
    const file = path.join(tmp, 'skills/hyperframes-workflow/assets/single-file-preview/motion-preview.html');
    fs.writeFileSync(file, fs.readFileSync(file, 'utf8').replace('circle(${k * 75}%', 'circle(${k * 50}%'));
    assert.ok(validateMotionToolkit(tmp).some(error => error.detail.includes('Single-file preview scene engine differs')));
  });
});

const reviewTool = 'skills/hyperframes-workflow/assets/motion-review/review-frames.mjs';
const syncTool = 'skills/hyperframes-workflow/assets/motion-sync/sync.mjs';
const exportDir = 'skills/hyperframes-workflow/assets/motion-export';
test('frame review selects contract frames and embeds the score in the preview', async () => {
  const {selectFrames, previewFor, contactSheet, formatsFor} = await import(path.join(root, reviewTool));
  const {reviewFrames} = await import('../skills/hyperframes-workflow/assets/motion-quality/score.mjs');
  const scorePath = path.join(root, kinetic, 'motion-score.json'), score = JSON.parse(fs.readFileSync(scorePath, 'utf8'));
  assert.deepEqual(selectFrames(score), reviewFrames(score));
  const {html, score: embedded} = previewFor(scorePath);
  assert.deepEqual(embedded, score);
  assert.match(html, /window\.reviewFrame = reviewFrame/);
  assert.match(html, /report.id = 'review-report'/);
  const sheet = contactSheet({id: 'x<y', revision: 1, frames: [{frame: 3, image: 'frames/a.png', scenes: ['s'], checked: true, issues: [{severity: 'error', check: 'contrast', scene: 's', element: 'e', detail: '<b>'}]}], summary: {errors: 1, warnings: 0, checkedFrames: 1}});
  assert.deepEqual(formatsFor(score), ['base', '9x16', '1x1']); assert.deepEqual(formatsFor(score, '1x1'), ['1x1']);
  assert.throws(() => formatsFor(score, '4x5'), /Unknown format 4x5/);
  assert.match(html, /resolveFormat\(contract, query.get\('format'\)/);
  assert.match(sheet, /x&lt;y/); assert.match(sheet, /&lt;b&gt;/); assert.match(sheet, /class="error"/);
});
// Opt-in: runs a real headless browser (set MOTION_REVIEW_BROWSER=/path/to/chrome).
test('frame review finds no issues in the starter and errors in a broken contract', {skip: !process.env.MOTION_REVIEW_BROWSER}, async () => {
  const {runReview} = await import(path.join(root, reviewTool));
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'motion-review-test-'));
  try {
    const good = runReview(path.join(root, kinetic, 'motion-score.json'), {out: path.join(tmp, 'good'), browser: process.env.MOTION_REVIEW_BROWSER});
    assert.equal(good.summary.errors, 0); assert.ok(good.summary.checkedFrames > 0);
    assert.deepEqual(good.formats, ['base', '9x16', '1x1']); assert.ok(good.frames.some(frame => frame.format === '9x16' && frame.image.startsWith('frames/9x16/')));
    const {importCaptions, parseSubtitles} = await import(path.join(root, syncTool));
    const captioned = importCaptions(JSON.parse(fs.readFileSync(path.join(root, kinetic, 'motion-score.json'), 'utf8')), parseSubtitles(fs.readFileSync(path.join(root, 'skills/hyperframes-workflow/assets/motion-sync/examples/voice-over.srt'), 'utf8'))).score;
    fs.writeFileSync(path.join(tmp, 'captioned.json'), JSON.stringify(captioned));
    const withCaptions = runReview(path.join(tmp, 'captioned.json'), {out: path.join(tmp, 'captions'), browser: process.env.MOTION_REVIEW_BROWSER, format: '9x16'});
    assert.equal(withCaptions.summary.errors, 0); assert.ok(withCaptions.frames.find(frame => frame.frame === captioned.captions[0].start).checked);
    const broken = JSON.parse(fs.readFileSync(path.join(root, kinetic, 'motion-score.json'), 'utf8'));
    broken.copy['title-1'] = 'Clearmotionwithoutanybreakthatrunsfarbeyondtherightedgeofthisframe';
    fs.writeFileSync(path.join(tmp, 'broken.json'), JSON.stringify(broken));
    const bad = runReview(path.join(tmp, 'broken.json'), {out: path.join(tmp, 'bad'), browser: process.env.MOTION_REVIEW_BROWSER});
    assert.ok(bad.frames.some(frame => frame.issues.some(issue => issue.check === 'outside-frame')));
  } finally { fs.rmSync(tmp, {recursive: true, force: true}); }
});

test('subtitles parse from SRT and WebVTT into exact caption copy and frames', async () => {
  const {parseSubtitles, importCaptions} = await import(path.join(root, syncTool));
  const vtt = '\uFEFFWEBVTT\r\n\r\nNOTE draft\r\n\r\nintro\r\n00:01.500 --> 00:03.000 line:90%\r\n<v Host>Zażółć <i>gęślą</i>\r\njaźń\r\n\r\n00:00:02.000 --> 00:00:05.250\r\n{\\an8}Second';
  assert.deepEqual(parseSubtitles(vtt), [{startMs: 1500, endMs: 3000, text: 'Zażółć gęślą\njaźń'}, {startMs: 2000, endMs: 5250, text: 'Second'}]);
  const srt = fs.readFileSync(path.join(root, 'skills/hyperframes-workflow/assets/motion-sync/examples/voice-over.srt'), 'utf8');
  assert.equal(parseSubtitles(srt).length, 3);
  assert.throws(() => parseSubtitles('1\n00:00:01 --> 00:00:02\nx'), /Invalid subtitle time/);
  const score = JSON.parse(fs.readFileSync(path.join(root, kinetic, 'motion-score.json'), 'utf8'));
  const {score: synced, warnings} = importCaptions(score, [...parseSubtitles(vtt), {startMs: 9800, endMs: 12000, text: 'Tail'}, {startMs: 11000, endMs: 11500, text: 'Late'}]);
  assert.deepEqual(synced.captions.map(c => [c.id, c.start, c.end]), [['caption-1', 45, 90], ['caption-2', 90, 158], ['caption-3', 294, 300]]);
  assert.equal(synced.copy['caption-1'], 'Zażółć gęślą\njaźń');
  assert.equal(score.captions, undefined);
  assert.ok(warnings.some(w => /overlaps caption-1/.test(w)) && warnings.some(w => /cut to 300/.test(w)) && warnings.some(w => /after the last frame/.test(w)));
  assert.throws(() => importCaptions(synced, []), /already has captions/);
  const replaced = importCaptions(synced, [{startMs: 0, endMs: 2000, text: 'Only'}], {replace: true}).score;
  assert.deepEqual(Object.keys(replaced.copy).filter(id => id.startsWith('caption-')), ['caption-1']);
  assert.throws(() => importCaptions(score, [{startMs: 0, endMs: 2000, text: 'x'}], {prefix: 'title'}), /title-1 is already used/);
});
test('beat grid, caption layer and checks follow the contract', async () => {
  const {beatFrames, buildCaptions, captionsFrame} = await import(path.join(root, scenesDir, 'motion-scenes.mjs'));
  const {beatReport, importCaptions, parseSubtitles} = await import(path.join(root, syncTool));
  const {checkScore, toMarkdown} = await import(path.join(root, kinetic, 'check-score.mjs'));
  const {selectFrames} = await import(path.join(root, reviewTool));
  const {reviewFrames} = await import('../skills/hyperframes-workflow/assets/motion-quality/score.mjs');
  const base = JSON.parse(fs.readFileSync(path.join(root, kinetic, 'motion-score.json'), 'utf8'));
  assert.deepEqual(beatFrames(base), []); assert.equal(buildCaptions(base), null);
  assert.deepEqual(beatFrames({...base, totalFrames: 90, music: {bpm: 128, offsetMs: 250}}).map(b => b.frame), [8, 22, 36, 50, 64, 78]);
  assert.deepEqual(beatFrames({...base, fps: {num: 30000, den: 1001}, totalFrames: 60, music: {bpm: 120, beatsPerBar: 3}}).map(b => [b.frame, b.bar, b.beatInBar]), [[0, 1, 1], [15, 1, 2], [30, 1, 3], [45, 2, 1]]);
  const srt = fs.readFileSync(path.join(root, 'skills/hyperframes-workflow/assets/motion-sync/examples/voice-over.srt'), 'utf8');
  const score = {...importCaptions(base, parseSubtitles(srt)).score, music: {bpm: 120, offsetMs: 0, beatsPerBar: 4}};
  assert.deepEqual(checkScore(score, {storyboard: true}), {errors: [], warnings: []});
  const steps = beatReport(score).rows.find(row => row.item === 'steps start');
  assert.deepEqual([steps.beat, steps.beatFrame, steps.offset, steps.downbeat], ['3.1', 120, -3, true]);
  const markdown = toMarkdown(score);
  assert.match(markdown, /\[117,215\), beat 3\.1 \(-3 f\)/); assert.match(markdown, /## Captions/); assert.match(markdown, /\| caption-2 \| \[126,210\)/);
  assert.deepEqual(captionsFrame(score, 125), {captions: {style: {visibility: 'hidden'}}, caption: {text: ''}});
  assert.equal(captionsFrame(score, 126).caption.text, 'Plan it, build it, review it.');
  assert.equal(buildCaptions(score).style.bottom, '86px');
  assert.equal(buildCaptions({...score, tokens: {...score.tokens, safeArea: {bottom: 0.2}}}).style.bottom, '216px');
  assert.deepEqual(selectFrames(score), reviewFrames(score));
  for (const caption of score.captions) assert.ok([caption.start, caption.end - 1].every(f => selectFrames(score).includes(f)));
  const bad = structuredClone(score);
  bad.music = {bpm: 0, beatsPerBar: 2.5, volume: 2}; bad.captions[1].start = 100; bad.captions[2].copy = 'nope'; bad.captions.push({id: 'caption-1', start: 298, end: 299, copy: 'caption-1'});
  const errors = checkScore(bad).errors.join('\n');
  for (const pattern of [/music.bpm/, /music.beatsPerBar/, /music.volume/, /caption caption-2: starts before/, /caption caption-3: copy id nope/, /caption id missing or duplicated: caption-1/]) assert.match(errors, pattern);
  const fast = structuredClone(score); fast.captions[0].end = 40;
  assert.ok(checkScore(fast).warnings.some(w => /caption caption-1: 22 frames is below the reading heuristic/.test(w)));
});

// Minimal readers for the muxer tests.
const ebml = (bytes, start = 0, end = bytes.length, out = []) => {
  for (let i = start; i < end;) {
    let idLength = 1; while (!(bytes[i] & (0x80 >> (idLength - 1)))) idLength++;
    const id = [...bytes.subarray(i, i + idLength)].map(b => b.toString(16).padStart(2, '0')).join('').toUpperCase();
    let sizeLength = 1; while (!(bytes[i + idLength] & (0x80 >> (sizeLength - 1)))) sizeLength++;
    let size = bytes[i + idLength] & (0xFF >> sizeLength);
    for (let k = 1; k < sizeLength; k++) size = size * 256 + bytes[i + idLength + k];
    const body = i + idLength + sizeLength;
    out.push({id, body, size});
    if (['18538067', '1654AE6B', 'AE', '1F43B675', '1549A966'].includes(id)) ebml(bytes, body, body + size, out);
    i = body + size;
  }
  return out;
};
const boxes = (bytes, start = 0, end = bytes.length, out = []) => {
  const view = new DataView(bytes.buffer, bytes.byteOffset);
  for (let i = start; i < end;) {
    const size = view.getUint32(i), type = String.fromCharCode(...bytes.subarray(i + 4, i + 8));
    out.push({type, start: i, size, body: i + 8});
    if (['moov', 'trak', 'mdia', 'minf', 'stbl'].includes(type)) boxes(bytes, i + 8, i + size, out);
    i += size;
  }
  return out;
};
const fakeChunks = (count, keyEvery = 60) => Array.from({length: count}, (_, i) => ({timestamp: Math.round(i * 1e6 * 1001 / 30000), key: i % keyEvery === 0, data: new Uint8Array([0, 0, 0, 2, i % 256, 7])}));
test('WebM muxer writes one block per frame and a cluster per keyframe', async () => {
  const {muxWebM} = await import(path.join(root, exportDir, 'video-export.mjs'));
  const bytes = muxWebM({width: 1080, height: 1920, fps: {num: 30000, den: 1001}, codec: 'vp09.00.40.08', chunks: fakeChunks(150)});
  const elements = ebml(bytes);
  assert.equal(elements[0].id, '1A45DFA3');
  const text = id => Buffer.from(bytes.subarray(elements.find(e => e.id === id).body, elements.find(e => e.id === id).body + elements.find(e => e.id === id).size)).toString();
  assert.equal(text('86'), 'V_VP9');
  assert.equal(elements.filter(e => e.id === 'A3').length, 150);
  assert.equal(elements.filter(e => e.id === '1F43B675').length, 3);
  const blocks = elements.filter(e => e.id === 'A3');
  assert.deepEqual([bytes[blocks[0].body + 3], bytes[blocks[1].body + 3], bytes[blocks[60].body + 3]], [0x80, 0, 0x80]);
});
test('MP4 muxer writes H.264 sample tables that point into mdat', async () => {
  const {muxMP4, videoCandidates, chooseVideoEncoding} = await import(path.join(root, exportDir, 'video-export.mjs'));
  assert.equal(videoCandidates[0].container, 'mp4'); assert.equal(await chooseVideoEncoding(1920, 1080, {num: 30, den: 1}), null);
  const chunks = fakeChunks(90, 30), description = new Uint8Array([1, 100, 0, 40, 255, 225, 0, 0, 1, 0, 0]);
  const bytes = muxMP4({width: 1920, height: 1080, fps: {num: 30000, den: 1001}, codec: 'avc1.640028', description, chunks});
  const list = boxes(bytes), view = new DataView(bytes.buffer, bytes.byteOffset), find = type => list.find(b => b.type === type);
  assert.deepEqual(list.filter(b => b.start === 0 || ['moov', 'mdat'].includes(b.type)).map(b => b.type), ['ftyp', 'moov', 'mdat']);
  assert.equal(view.getUint32(find('stco').body + 8), find('mdat').body);
  assert.deepEqual([view.getUint32(find('stts').body + 8), view.getUint32(find('stts').body + 12)], [90, 1001]);
  assert.equal(view.getUint32(find('stsz').body + 8), 90);
  assert.equal(view.getUint32(find('stss').body + 4), 3);
  assert.equal(find('ctts'), undefined);
  assert.deepEqual([...bytes.subarray(find('mdat').body, find('mdat').body + 6)], [0, 0, 0, 2, 0, 7]);
  const reordered = chunks.map((chunk, i) => ({...chunk, timestamp: chunks[i % 2 ? i - 1 : Math.min(i + 1, 89)].timestamp}));
  assert.ok(boxes(muxMP4({width: 1920, height: 1080, fps: {num: 30000, den: 1001}, codec: 'avc1.640028', description, chunks: reordered})).some(b => b.type === 'ctts'));
  assert.throws(() => muxMP4({width: 2, height: 2, fps: {num: 30, den: 1}, codec: 'vp8', description, chunks}), /H.264 only/);
  assert.throws(() => muxMP4({width: 2, height: 2, fps: {num: 30, den: 1}, codec: 'avc1.640028', chunks}), /avcC/);
});
test('diverging video export copy fails the toolkit check', () => withCopy(tmp => {
  const file = path.join(tmp, 'skills/hyperframes-workflow/assets/single-file-preview/motion-preview.html');
  fs.writeFileSync(file, fs.readFileSync(file, 'utf8').replace("keyFrame: frame % keyEvery === 0", "keyFrame: true"));
  assert.ok(validateMotionToolkit(tmp).some(error => error.detail.includes('video export differs')));
}));
// Opt-in: exports a real file through a headless browser (set MOTION_REVIEW_BROWSER=/path/to/chrome).
test('browser export writes a playable file for a chosen format', {skip: !process.env.MOTION_REVIEW_BROWSER}, async () => {
  const {exportFile} = await import(path.join(root, exportDir, 'export-video.mjs'));
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'motion-export-test-'));
  try {
    const result = await exportFile(path.join(root, kinetic, 'motion-score.json'), {out: path.join(tmp, 'film'), format: '1x1', browser: process.env.MOTION_REVIEW_BROWSER});
    assert.equal(result.frames, 300);
    const head = fs.readFileSync(result.file).subarray(0, 8);
    assert.ok(result.container === 'webm' ? head.readUInt32BE(0) === 0x1A45DFA3 : head.toString('latin1', 4, 8) === 'ftyp');
    await assert.rejects(exportFile(path.join(root, kinetic, 'motion-score.json'), {out: result.file, browser: process.env.MOTION_REVIEW_BROWSER}), /already exists/);
  } finally { fs.rmSync(tmp, {recursive: true, force: true}); }
});
