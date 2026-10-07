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
  const appFilm = JSON.parse(fs.readFileSync(path.join(root, scenesDir, 'examples/app-film.motion-score.json'), 'utf8'));
  assert.deepEqual(new Set([...score.scenes, ...appFilm.scenes].map(scene => scene.kind)), new Set(Object.keys(sceneKinds)));
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

test('sweep exit hands over with a crossing line and leaves other exits unchanged', async () => {
  const {buildScene, sceneFrame} = await import(path.join(root, scenesDir, 'motion-scenes.mjs'));
  const {checkScore} = await import(path.join(root, kinetic, 'check-score.mjs'));
  const {validateScore} = await import('../skills/hyperframes-workflow/assets/motion-quality/score.mjs');
  const score = JSON.parse(fs.readFileSync(path.join(root, scenesDir, 'examples/two-statements.motion-score.json'), 'utf8'));
  assert.doesNotThrow(() => validateScore(score));
  assert.deepEqual(checkScore(score, {storyboard: true}), {errors: [], warnings: []});
  const [intro, outro] = score.scenes;
  const tree = buildScene(intro, score);
  assert.deepEqual([tree.key, tree.children.map(child => child.key)], ['scene', ['container', 'sweep']]);
  assert.equal(buildScene(outro, score).key, 'container');
  // Sweep window: the last exitFrames + 12 = 26 frames, content exit during its first 14.
  assert.deepEqual(sceneFrame(intro, score, 79).sweep.style.opacity, '0');
  assert.deepEqual(sceneFrame(intro, score, 79).container.style, {opacity: '1', transform: 'translateX(0px)'});
  const middle = sceneFrame(intro, score, 94);
  assert.equal(middle.sweep.style.opacity, '1'); assert.equal(middle.container.style.opacity, '0');
  assert.equal(sceneFrame(intro, score, 105).sweep.style.opacity, '1');
  const first = Number(sceneFrame(intro, score, 81).sweep.style.transform.match(/-?\d+/)[0]), last = Number(sceneFrame(intro, score, 105).sweep.style.transform.match(/-?\d+/)[0]);
  assert.ok(first >= 250 && first < 400 && last > 1500 && last <= 1670, `${first} ${last}`);
  const lift = sceneFrame({...intro, params: {...intro.params, exit: true}}, score, 99).container.style.transform;
  assert.match(lift, /^translateY/);
  const bad = structuredClone(score); bad.scenes[0].params.exit = 'spin'; bad.scenes[0].params.sweepFrames = 500; bad.schema_version = '1.0'; bad.audio = {mode: 'silent'};
  const errors = checkScore(bad, {storyboard: true}).errors.join('\n');
  for (const pattern of [/params.exit must be/, /params.sweepFrames/, /schema_version must be the number 1/, /audio must be text/]) assert.match(errors, pattern);
  assert.doesNotMatch(errors, /storyboard field audio is missing/);
});
test('check-preview accepts the template with a new contract and rejects rewrites', async () => {
  const {checkPreview} = await import(path.join(root, 'skills/hyperframes-workflow/assets/single-file-preview/check-preview.mjs'));
  const {previewFor} = await import(path.join(root, reviewTool));
  const {html} = previewFor(path.join(root, scenesDir, 'examples/two-statements.motion-score.json'));
  const good = checkPreview(html);
  assert.deepEqual([good.errors, good.unchanged, good.regions], [[], true, {'scene engine': 'identical', 'video export': 'identical'}]);
  assert.match(checkPreview(html.replace("transform: 'none'", "transform: 'scale(1)'")).errors.join(), /video export is changed/);
  assert.match(checkPreview(html.replace('// BEGIN motion-scenes engine', '// engine')).errors.join(), /scene engine is missing/);
  assert.match(checkPreview(html.replace('>Export video<', '>Save<')).errors.join(), /player outside the contract differs/);
  assert.match(checkPreview(html.replace('"kind": "line-reveal"', '"kindless": true')).errors.join(), /declares no kind/);
  assert.match(checkPreview(html.replace('"schema_version": 1,', '"schema_version": 1')).errors.join(), /not valid JSON/);
  assert.match(checkPreview('<canvas></canvas>').errors.join(), /No embedded motion contract/);
  assert.match(checkPreview(html.replace('</body>', '<script>new MediaRecorder(canvas.captureStream(0))</script></body>')).errors.join(), /records video in real time/);
});

const playerFile = 'skills/hyperframes-workflow/assets/single-file-preview/motion-preview.html';
const fragmentFor = score => '#contract=' + Buffer.from(JSON.stringify(score)).toString('base64url');
test('player links carry the contract in the fragment and round-trip exactly', async () => {
  const {playerLink, contractFromLink, playerUrl} = await import(path.join(root, 'skills/hyperframes-workflow/assets/single-file-preview/player-link.mjs'));
  const score = JSON.parse(fs.readFileSync(path.join(root, scenesDir, 'examples/two-statements.motion-score.json'), 'utf8'));
  const link = playerLink(score);
  assert.equal(playerUrl, 'https://framecoreworks.github.io/framecore-works-creative-studio/');
  assert.ok(link.startsWith(playerUrl + '#contract='));
  assert.match(link.slice((playerUrl + '#contract=').length), /^[A-Za-z0-9_-]+$/);
  assert.equal(link, playerUrl + fragmentFor(score));
  assert.deepEqual(contractFromLink(link), score);
  assert.equal(contractFromLink(link).copy['intro-2'], 'pomysł');
  assert.ok(playerLink(score, 'file:///tmp/player.html').startsWith('file:///tmp/player.html#contract='));
  assert.throws(() => contractFromLink(playerUrl), /no #contract=/);
});
test('the motion player can open a contract and keeps shortcuts out of text fields', () => {
  const html = fs.readFileSync(path.join(root, playerFile), 'utf8');
  for (const id of ['open', 'open-panel', 'open-text', 'open-file', 'open-load', 'open-example', 'open-errors']) assert.match(html, new RegExp(`id="${id}"`));
  assert.match(html, /location\.hash = `contract=\$\{encodeContract/);
  assert.match(html, /if \(!panel\.hidden \|\| \/\^\(INPUT\|TEXTAREA\|SELECT\)\$\/\.test\(event\.target\.tagName\)\) return;/);
});
// Opt-in: a contract in the address fragment replaces the embedded one; a broken one falls back to it.
test('the motion player draws a contract from the address fragment', {skip: !process.env.MOTION_REVIEW_BROWSER}, async () => {
  const {spawnSync} = await import('node:child_process');
  const {pathToFileURL} = await import('node:url');
  const score = JSON.parse(fs.readFileSync(path.join(root, scenesDir, 'examples/two-statements.motion-score.json'), 'utf8'));
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'motion-player-test-'));
  const report = fragment => {
    const args = ['--headless=new', '--disable-gpu', `--user-data-dir=${profile}`, '--window-size=1920,1080', '--virtual-time-budget=3000', '--dump-dom', `${pathToFileURL(path.join(root, playerFile)).href}?frame=60&review=1${fragment}`];
    if (process.platform === 'linux' && process.getuid?.() === 0) args.unshift('--no-sandbox');
    const out = spawnSync(process.env.MOTION_REVIEW_BROWSER, args, {encoding: 'utf8', timeout: 60000}).stdout;
    return JSON.parse(out.match(/id="review-report">([\s\S]*?)<\/script>/)[1]);
  };
  try {
    const opened = report(fragmentFor(score));
    assert.equal(opened.id, 'two-statements'); assert.equal(opened.checked, true); assert.deepEqual(opened.issues, []);
    assert.equal(report(fragmentFor({...score, scenes: [{...score.scenes[0], kind: 'spin'}]})).id, 'kinetic-type-starter');
    assert.equal(report('#contract=not-base64!').id, 'kinetic-type-starter');
  } finally { fs.rmSync(profile, {recursive: true, force: true}); }
});

test('contract revisions diff values and extend a scene while moving everything after it', async () => {
  const {diffContracts, diffMarkdown, extendScene, nextRevision, timingMentions} = await import(path.join(root, 'skills/hyperframes-workflow/assets/motion-revise/revise.mjs'));
  const {checkScore} = await import(path.join(root, 'skills/hyperframes-workflow/assets/gsap-motion-starter/check-score.mjs'));
  const score = JSON.parse(fs.readFileSync(path.join(root, 'skills/hyperframes-workflow/assets/motion-scenes/examples/two-statements.motion-score.json'), 'utf8'));
  const [first, second] = score.scenes;
  assert.ok(second.start < first.end, 'example scenes overlap');
  const longer = extendScene(score, first.id, 15);
  assert.equal(longer.totalFrames, score.totalFrames + 15);
  assert.equal(longer.scenes[0].end, first.end + 15);
  assert.equal(longer.scenes[1].start, second.start + 15);
  assert.equal(longer.scenes[0].end - longer.scenes[1].start, first.end - second.start, 'overlap preserved');
  assert.deepEqual(checkScore(longer).errors, []);
  assert.deepEqual(checkScore(extendScene(score, first.id, -10)).errors, []);
  const last = score.scenes.at(-1);
  const outro = extendScene(score, last.id, 30);
  assert.equal(outro.scenes.at(-1).end, outro.totalFrames);
  assert.deepEqual(checkScore(outro).errors, []);
  assert.deepEqual(score, JSON.parse(fs.readFileSync(path.join(root, 'skills/hyperframes-workflow/assets/motion-scenes/examples/two-statements.motion-score.json'), 'utf8')), 'input untouched');
  assert.throws(() => extendScene(score, 'missing', 10), /Unknown scene/);
  assert.throws(() => extendScene(score, first.id, 0), /non-zero integer/);
  assert.throws(() => extendScene(score, first.id, 1.5), /non-zero integer/);
  assert.throws(() => extendScene(score, first.id, -(first.end - first.start)), /empty/);
  const changes = diffContracts(score, outro);
  assert.ok(changes.some(change => change.path === 'totalFrames' && change.after === score.totalFrames + 30));
  assert.match(diffMarkdown(changes), /`totalFrames`: \d+ → \d+/);
  assert.equal(diffMarkdown(diffContracts(score, score)), 'No changes.\n');
  const approved = nextRevision(score, 'User: longer ending');
  assert.deepEqual([approved.revision, approved.approval.status, approved.approval.revision], [score.revision + 1, 'approved', score.revision + 1]);
  assert.equal(nextRevision(score).approval.status, 'proposed');
  const mentions = timingMentions({id: 'clip-6s', copy: {a: '30 frames'}, acceptance: ['Stable from frame 93'], scenes: [{entry: 'Rise over frames 0–15', purpose: 'Greet'}]});
  assert.deepEqual(mentions, ['acceptance[0]', 'scenes[0].entry']);
});

test('a delivered render script is named in the contract and follows each revision', async () => {
  const {nextRevision, scriptName} = await import(path.join(root, 'skills/hyperframes-workflow/assets/motion-revise/revise.mjs'));
  const {checkScore} = await import(path.join(root, 'skills/hyperframes-workflow/assets/gsap-motion-starter/check-score.mjs'));
  const score = JSON.parse(fs.readFileSync(path.join(root, 'skills/hyperframes-workflow/assets/motion-scenes/examples/two-statements.motion-score.json'), 'utf8'));
  const withScript = name => ({...score, runtime: {status: 'selected', value: 'Python frame renderer', script: name}});
  assert.deepEqual(checkScore(withScript('two-statements.render.py')).errors, []);
  for (const bad of ['../render.py', 'https://example.com/render.py', 'scripts/render.py', 'render', '']) assert.ok(checkScore(withScript(bad)).errors.some(error => error.includes('runtime.script')), bad);
  assert.equal(scriptName('video.render.py', 2), 'video-r2.render.py');
  assert.equal(scriptName('video-r2.render.py', 3), 'video-r3.render.py');
  assert.equal(nextRevision(withScript('video-r1.render.py'), 'User: change').runtime.script, `video-r${score.revision + 1}.render.py`);
  assert.equal(nextRevision(score).runtime?.script, score.runtime?.script);
});

// The Python renderer is a port of the scene engine; these checks run when python3 with Pillow is installed.
const renderDir = 'skills/hyperframes-workflow/assets/motion-render';
import {spawnSync as spawnPython} from 'node:child_process';
const python = spawnPython('python3', ['-c', 'import PIL'], {encoding: 'utf8'}).status === 0;
test('Python renderer matches the engine kinds and easings and renders deterministic stills', {skip: !python && 'python3 with Pillow not installed'}, async () => {
  const spawnSync = spawnPython;
  const {easings, sceneKinds} = await import(path.join(root, 'skills/hyperframes-workflow/assets/motion-scenes/motion-scenes.mjs'));
  const script = path.join(root, renderDir, 'render.py');
  const probe = spawnSync('python3', ['-B', '-c', `import importlib.util, json, sys
spec = importlib.util.spec_from_file_location('render', sys.argv[1]); r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)
print(json.dumps({'kinds': list(r.KINDS), 'easings': {k: [f(x / 20) for x in range(21)] for k, f in r.EASINGS.items()}, 'numbers': [r.number_text({'decimals': 1, 'suffix': '%'}, 12345.25), r.number_text({'locale': 'pl-PL'}, 1234), r.number_text({'locale': 'pl-PL'}, 12345)]}))`, script], {encoding: 'utf8'});
  assert.equal(probe.status, 0, probe.stderr);
  const result = JSON.parse(probe.stdout);
  assert.deepEqual(result.kinds.sort(), Object.keys(sceneKinds).sort());
  for (const [name, values] of Object.entries(result.easings)) values.forEach((value, i) => assert.ok(Math.abs(value - easings[name](i / 20)) < 1e-9, `${name} at ${i / 20}`));
  assert.deepEqual(result.numbers, [
    new Intl.NumberFormat('en-US', {minimumFractionDigits: 1, maximumFractionDigits: 1}).format(12345.25) + '%',
    new Intl.NumberFormat('pl-PL').format(1234), new Intl.NumberFormat('pl-PL').format(12345)]);
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'motion-render-'));
  try {
    const contract = path.join(root, 'skills/hyperframes-workflow/assets/motion-scenes/examples/two-statements.motion-score.json');
    const run = dir => spawnSync('python3', [script, contract, '--stills', '0,30,93,179', '--stills-dir', path.join(tmp, dir)], {encoding: 'utf8'});
    const first = run('a'), second = run('b');
    assert.equal(first.status, 0, first.stderr);
    const summary = JSON.parse(first.stdout);
    assert.deepEqual([summary.width, summary.height, summary.frames, summary.stills.length], [1920, 1080, 180, 4]);
    for (const name of fs.readdirSync(path.join(tmp, 'a'))) assert.ok(fs.readFileSync(path.join(tmp, 'a', name)).equals(fs.readFileSync(path.join(tmp, 'b', name))), name);
    fs.writeFileSync(path.join(tmp, 'taken.mp4'), '');
    assert.equal(spawnSync('python3', [script, contract, path.join(tmp, 'taken.mp4')], {encoding: 'utf8'}).status, 2);
    const broken = path.join(tmp, 'broken.json');
    fs.writeFileSync(broken, JSON.stringify({...JSON.parse(fs.readFileSync(contract, 'utf8')), scenes: [{id: 'x', start: 0, end: 10}]}));
    assert.match(spawnSync('python3', [script, broken, '--stills', '0'], {encoding: 'utf8'}).stderr, /no supported kind/);
  } finally { fs.rmSync(tmp, {recursive: true, force: true}); }
});

test('motion styles apply to a contract, keep text contrast and use known easings', async () => {
  const {easings} = await import(path.join(root, 'skills/hyperframes-workflow/assets/motion-scenes/motion-scenes.mjs'));
  const {checkScore} = await import(path.join(root, 'skills/hyperframes-workflow/assets/gsap-motion-starter/check-score.mjs'));
  const {styles, choosing} = JSON.parse(fs.readFileSync(path.join(root, 'skills/hyperframes-workflow/assets/motion-styles/styles.json'), 'utf8'));
  const base = JSON.parse(fs.readFileSync(path.join(root, 'skills/hyperframes-workflow/assets/motion-scenes/examples/two-statements.motion-score.json'), 'utf8'));
  const ids = styles.map(style => style.id);
  assert.equal(new Set(ids).size, ids.length);
  for (const entry of choosing) for (const id of entry.styles) assert.ok(ids.includes(id), id);
  const luminance = hex => { const c = [1, 3, 5].map(i => parseInt(hex.slice(i, i + 2), 16) / 255).map(v => (v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4)); return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]; };
  const contrast = (a, b) => { const [hi, lo] = [luminance(a), luminance(b)].sort((x, y) => y - x); return (hi + 0.05) / (lo + 0.05); };
  for (const style of styles.filter(item => item.tokens)) {
    const t = style.tokens;
    assert.ok(contrast(t.foreground, t.background) >= 4.5, `${style.id} foreground`);
    assert.ok(contrast(t.muted, t.background) >= 3, `${style.id} muted`);
    for (const key of ['entryEasing', 'exitEasing', 'resolveEasing']) assert.ok(easings[style.motion[key]], `${style.id} ${key}`);
    const contract = {...base, style: style.id, tokens: {...base.tokens, ...t}, motion: {...style.motion}};
    assert.deepEqual(checkScore(contract).errors, [], style.id);
  }
});

test('retained kaventro/motion-designer scripts match the recorded hashes', async () => {
  const {createHash} = await import('node:crypto');
  const dir = path.join(root, 'integrations/kaventro-motion-designer');
  const manifest = JSON.parse(fs.readFileSync(path.join(dir, 'source-manifest.json'), 'utf8'));
  assert.equal(manifest.license, 'MIT');
  for (const item of manifest.retained_files) {
    const file = path.resolve(dir, item.destination_path);
    assert.equal(createHash('sha256').update(fs.readFileSync(file)).digest('hex'), item.sha256, item.destination_path);
  }
});

const ffmpegSpectral = spawnPython('ffmpeg', ['-hide_banner', '-filters'], {encoding: 'utf8'}).stdout?.includes('aspectralstats');
test('beats.py finds tempo, bar 1 and the drop of a click track and music_edit.py cuts whole bars', {skip: !ffmpegSpectral && 'ffmpeg with aspectralstats not installed'}, () => {
  const sync = path.join(root, 'skills/hyperframes-workflow/assets/motion-sync');
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'motion-beats-'));
  try {
    const track = path.join(tmp, 'track.wav');
    const expr = "(0.6*between(mod(t-0.25,2),0,0.04)*sin(2*PI*1000*t)+0.35*between(mod(t-0.25,0.5),0,0.03)*sin(2*PI*600*t))*(1+1.5*gte(t,16.25))";
    assert.equal(spawnPython('ffmpeg', ['-v', 'error', '-y', '-f', 'lavfi', '-i', `aevalsrc='${expr}':s=44100:d=32`, track]).status, 0);
    const beats = spawnPython('python3', [path.join(sync, 'beats.py'), track, '--json', path.join(tmp, 'grid.json')], {encoding: 'utf8'});
    assert.equal(beats.status, 0, beats.stderr);
    const grid = JSON.parse(fs.readFileSync(path.join(tmp, 'grid.json'), 'utf8'));
    assert.ok(Math.abs(grid.bpm - 120) < 0.05 && Math.abs(grid.bar1 - 0.25) < 0.01, `${grid.bpm} ${grid.bar1}`);
    assert.equal(grid.bars.find(bar => bar.mark === 'drop')?.bar, 9);
    const cut = spawnPython('python3', [path.join(sync, 'music_edit.py'), track, path.join(tmp, 'grid.json'), '--from-bar', '2', '--bars', '4', '--fps', '30', '--out', path.join(tmp, 'cut')], {encoding: 'utf8'});
    assert.equal(cut.status, 0, cut.stderr);
    assert.match(cut.stdout, /240 frames/);
  } finally { fs.rmSync(tmp, {recursive: true, force: true}); }
});

test('Python renderer motion blur keeps holds sharp and phone-size stills scale down', {skip: !python && 'python3 with Pillow not installed'}, () => {
  const script = path.join(root, renderDir, 'render.py');
  const contract = path.join(root, 'skills/hyperframes-workflow/assets/motion-scenes/examples/two-statements.motion-score.json');
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'motion-blur-'));
  try {
    for (const [dir, extra] of [['sharp', []], ['blur', ['--blur', '4']], ['phone', ['--stills-width', '360']]]) {
      const run = spawnPython('python3', [script, contract, '--stills', '30,80', '--stills-dir', path.join(tmp, dir), ...extra], {encoding: 'utf8'});
      assert.equal(run.status, 0, run.stderr);
    }
    const read = (dir, frame) => fs.readFileSync(path.join(tmp, dir, `frame-000${frame}.png`));
    assert.ok(read('sharp', 30).equals(read('blur', 30)), 'a hold is identical with blur');
    assert.ok(!read('sharp', 80).equals(read('blur', 80)), 'the sweep is blurred');
    assert.equal(read('phone', 30).readUInt32BE(16), 360);
  } finally { fs.rmSync(tmp, {recursive: true, force: true}); }
});

test('device scenes place screenshots in a phone or browser window, push screens and focus the camera', async () => {
  const {buildScene, deviceFrame, deviceLayout, nodesByKey, resolveFormat, sceneFrame} = await import(path.join(root, scenesDir, 'motion-scenes.mjs'));
  const {checkScore} = await import(path.join(root, kinetic, 'check-score.mjs'));
  const score = JSON.parse(fs.readFileSync(path.join(root, scenesDir, 'examples/app-film.motion-score.json'), 'utf8'));
  assert.deepEqual(checkScore(score, {storyboard: true}).errors, []);
  for (const format of ['base', '9x16']) {
    const view = resolveFormat(score, format);
    for (const scene of view.scenes.filter(item => item.kind === 'device')) {
      const d = deviceLayout(scene, view);
      assert.ok(d.dx >= 0 && d.dy >= 0 && d.dx + d.dw <= view.width && d.dy + d.dh <= view.height, `${format} ${scene.id} inside the frame`);
      const c = d.caption;
      const apart = c.x + c.w <= d.dx || d.dx + d.dw <= c.x || c.y + c.h <= d.dy;
      assert.ok(apart, `${format} ${scene.id}: caption beside or above the device`);
      for (const value of Object.values(d).filter(Number.isFinite)) assert.ok(Number.isInteger(value), `${scene.id} whole pixels`);
    }
  }
  const phone = score.scenes.find(scene => scene.id === 'phone');
  const nodes = nodesByKey(buildScene(phone, score));
  assert.ok(nodes.island && nodes['screen-0'].src.startsWith('data:image/png') && nodes['screen-1']);
  const at = phone.start + phone.params.screens[1].at;
  assert.deepEqual(deviceFrame(phone, score, at - 1).screens.map(state => state.opacity), [1, 0]);
  const mid = deviceFrame(phone, score, at + 6).screens;
  assert.ok(mid[0].x < 0 && mid[1].x > 0 && mid[1].x < deviceLayout(phone, score).sw, 'push in progress');
  assert.deepEqual(deviceFrame(phone, score, at + 12).screens.map(state => [state.opacity, state.x]), [[0, 0], [1, 0]]);
  const focus = phone.params.focus[0], held = deviceFrame(phone, score, phone.start + focus.at + focus.frames);
  assert.ok(Math.abs(held.focus.s - focus.scale) < 1e-9);
  const d = held.layout, point = [d.bezel + focus.x * d.sw, d.bezel + d.bar + focus.y * d.sh];
  assert.ok(Math.abs(held.tx + held.focus.s * point[0] - point[0]) < 1e-6 && Math.abs(held.ty + held.focus.s * point[1] - point[1]) < 1e-6, 'focus keeps its point in place');
  assert.match(sceneFrame(phone, score, at + 6).device.style.transform, /^translate\(/);
  const window = score.scenes.find(scene => scene.id === 'desktop');
  assert.equal(Object.keys(nodesByKey(buildScene(window, score))).filter(key => key.startsWith('dot-')).length, 3);
  const bad = structuredClone(score);
  bad.scenes[0].params.frame = 'tablet'; bad.scenes[0].params.screens[1].at = 0; bad.assets[0].width = undefined;
  const errors = checkScore(bad).errors.join('\n');
  assert.match(errors, /frame must be phone, window or browser/); assert.match(errors, /screen 2 needs an integer at/); assert.match(errors, /screen 1 needs an assets entry with src, width and height/);
});

test('Python renderer draws device scenes deterministically', {skip: !python && 'python3 with Pillow not installed'}, () => {
  const script = path.join(root, renderDir, 'render.py');
  const contract = path.join(root, scenesDir, 'examples/app-film.motion-score.json');
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'motion-device-'));
  try {
    for (const dir of ['a', 'b']) {
      const run = spawnPython('python3', ['-B', script, contract, '--format', '9x16', '--stills', '60,118,170,250', '--stills-dir', path.join(tmp, dir)], {encoding: 'utf8'});
      assert.equal(run.status, 0, run.stderr);
    }
    for (const name of fs.readdirSync(path.join(tmp, 'a'))) assert.ok(fs.readFileSync(path.join(tmp, 'a', name)).equals(fs.readFileSync(path.join(tmp, 'b', name))), name);
    assert.equal(fs.readFileSync(path.join(tmp, 'a', 'frame-00060.png')).readUInt32BE(20), 1920);
  } finally { fs.rmSync(tmp, {recursive: true, force: true}); }
});

test('device taps press before the screen change, the browser frame shows its address, scene backgrounds wipe in', async () => {
  const {backgroundWipe, buildScene, deviceFrame, deviceLayout, nodesByKey, sceneFrame} = await import(path.join(root, scenesDir, 'motion-scenes.mjs'));
  const {checkScore} = await import(path.join(root, kinetic, 'check-score.mjs'));
  const film = JSON.parse(fs.readFileSync(path.join(root, scenesDir, 'examples/app-film.motion-score.json'), 'utf8'));
  const phone = film.scenes.find(scene => scene.id === 'phone'), tap = phone.params.taps[0], at = phone.start + tap.at;
  assert.ok(phone.params.screens[1].at - tap.at >= 3 && phone.params.screens[1].at - tap.at <= 5, 'the tap causes the screen change');
  const state = frame => deviceFrame(phone, film, frame).taps[0];
  assert.equal(state(at - 5).opacity, 0);
  assert.equal(state(at).opacity, 1);
  assert.ok(state(at + 2).scale < 1, 'the marker presses');
  assert.ok(state(at + 4).ripple > 0 && state(at + 4).rippleScale > 1, 'a ring spreads');
  assert.equal(state(at + 14).opacity, 0);
  const nodes = nodesByKey(buildScene(phone, film));
  assert.ok(nodes['tap-0'] && nodes['ripple-0'] && nodes.screen.children.indexOf(nodes['tap-0']) > nodes.screen.children.indexOf(nodes['screen-1']), 'taps draw above the screens');
  assert.equal(sceneFrame(phone, film, at + 2)['tap-0'].style.opacity, '1');
  const web = film.scenes.find(scene => scene.id === 'desktop'), layout = deviceLayout(web, film);
  assert.equal(web.params.frame, 'browser');
  assert.ok(layout.address && layout.address.x + layout.address.w <= layout.dw && layout.address.y + layout.address.h <= layout.bar);
  assert.equal(nodesByKey(buildScene(web, film)).url.text, film.copy.url);
  const blocks = JSON.parse(fs.readFileSync(path.join(root, scenesDir, 'examples/color-block.motion-score.json'), 'utf8'));
  assert.deepEqual(checkScore(blocks, {storyboard: true}).errors, []);
  const [one, two] = blocks.scenes;
  assert.equal(two.start, one.end - (two.params.backgroundFrames ?? 12), 'the next colour wipes in while the previous scene still covers the frame');
  assert.equal(buildScene(one, blocks).style.background, one.params.background);
  assert.equal(backgroundWipe(one, blocks, one.start), null);
  assert.deepEqual(backgroundWipe(two, blocks, two.start), [0, blocks.width, 0, 0]);
  assert.deepEqual(backgroundWipe(two, blocks, two.start + 12), [0, 0, 0, 0]);
  assert.equal(sceneFrame(two, blocks, two.start + 12).scene.style.clipPath, 'inset(0px 0px 0px 0px)');
  const plain = JSON.parse(fs.readFileSync(path.join(root, scenesDir, 'examples/two-statements.motion-score.json'), 'utf8'));
  assert.deepEqual(buildScene(plain.scenes[0], plain).style, {position: 'absolute', inset: '0'}, 'scenes without a background keep their tree');
  const bad = structuredClone(film);
  bad.scenes[0].params.taps = [{at: 2, x: 1.5}]; bad.scenes[0].params.frame = 'tablet'; bad.scenes[2].params.backgroundWipe = 'spiral';
  const errors = checkScore(bad).errors.join('\n');
  assert.match(errors, /tap 1 needs an integer at/); assert.match(errors, /frame must be phone, window or browser/); assert.match(errors, /backgroundWipe must be/);
});

test('Python renderer draws taps, the browser frame and wiping backgrounds deterministically', {skip: !python && 'python3 with Pillow not installed'}, () => {
  const script = path.join(root, renderDir, 'render.py');
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'motion-wipe-'));
  try {
    for (const [name, frames] of [['color-block', '0,100,114,120,230'], ['app-film', '106,108,110,228']]) {
      for (const dir of ['a', 'b']) {
        const run = spawnPython('python3', ['-B', script, path.join(root, scenesDir, `examples/${name}.motion-score.json`), '--stills', frames, '--stills-dir', path.join(tmp, name, dir)], {encoding: 'utf8'});
        assert.equal(run.status, 0, run.stderr);
      }
      for (const file of fs.readdirSync(path.join(tmp, name, 'a'))) assert.ok(fs.readFileSync(path.join(tmp, name, 'a', file)).equals(fs.readFileSync(path.join(tmp, name, 'b', file))), `${name} ${file}`);
    }
  } finally { fs.rmSync(tmp, {recursive: true, force: true}); }
});

// Motion sound design: synthesized designs, cue planning from the picture's timing, and a measured, mastered mix.
const soundDir = 'skills/hyperframes-workflow/assets/motion-sound';
const ffmpegLoudnorm = spawnPython('ffmpeg', ['-hide_banner', '-filters'], {encoding: 'utf8'}).stdout?.includes('loudnorm');
const numpy = spawnPython('python3', ['-c', 'import numpy'], {encoding: 'utf8'}).status === 0;
test('sound designs render deterministically, finite and aligned, and match the checker list', {skip: !numpy && 'numpy not installed'}, async () => {
  const source = fs.readFileSync(path.join(root, kinetic, 'check-score.mjs'), 'utf8');
  const listed = JSON.parse(source.match(/const soundDesigns = (\[[^\]]*\]);/)[1].replaceAll("'", '"'));
  const probe = spawnPython('python3', ['-B', '-c', `import sys, json, numpy as np
sys.path.insert(0, sys.argv[1]); import synth
out = {'designs': list(synth.DESIGNS)}
for name in synth.DESIGNS:
    a, offset = synth.render_design(name, {}, 7, 'A minor'); b, _ = synth.render_design(name, {}, 7, 'A minor')
    out[name] = {'same': bool(np.array_equal(a, b)), 'finite': bool(np.isfinite(a).all()), 'stereo': a.shape[1] == 2, 'offset': offset, 'seconds': len(a) / synth.RATE}
w, offset = synth.whoosh(0.8, 0.5, 0.8, 1, 1.0, 3)
env = np.convolve(np.mean(w, axis=1) ** 2, np.ones(480) / 480, mode='same')
out['whoosh_peak_error_ms'] = abs(int(np.argmax(env)) / synth.RATE - offset) * 1000
c, _ = synth.render_design('click', {}, 4)
x = np.zeros((synth.RATE, 2)); x[1000:1000 + len(c)] = c * 6
out['limited_true_peak_db'] = synth.true_peak_db(synth.limit(x, -1.0))
bed = synth.compose_bed(6.0, 120, 'D major', [1, 3, 1], reveal_bar=2)
out['bed_edges_db'] = [20 * np.log10(np.abs(bed[:2]).max() + 1e-12), 20 * np.log10(np.abs(bed[-2:]).max() + 1e-12)]
print(json.dumps(out))`, path.join(root, soundDir)], {encoding: 'utf8'});
  assert.equal(probe.status, 0, probe.stderr);
  const result = JSON.parse(probe.stdout);
  assert.deepEqual(result.designs, listed);
  for (const name of result.designs) assert.ok(result[name].same && result[name].finite && result[name].stereo && result[name].seconds > 0, name);
  assert.equal(result.riser.offset, result.riser.seconds, 'a riser aligns on its end');
  assert.ok(result.limited_true_peak_db <= -0.95, `the limiter holds true peak within 0.05 dB, between samples too: ${result.limited_true_peak_db}`);
  assert.ok(result.bed_edges_db[0] < -40 && result.bed_edges_db[1] < -40, `the bed fades in and out: ${result.bed_edges_db}`);
  assert.ok(result.whoosh_peak_error_ms < 1, 'a whoosh aligns on its measured peak');
});

test('sound cues follow the picture: taps, pushes, wipes, landings, a composed bed and checked contracts', {skip: !(python && numpy) && 'python3 with Pillow and numpy not installed'}, async () => {
  const {checkScore} = await import(path.join(root, kinetic, 'check-score.mjs'));
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'motion-sound-'));
  try {
    const plan = (name, density, out, extra = []) => spawnPython('python3', ['-B', path.join(root, soundDir, 'sound.py'), 'plan', path.join(root, scenesDir, `examples/${name}.motion-score.json`), '--out', out, '--density', density, ...extra], {encoding: 'utf8'});
    for (const dir of ['a', 'b']) assert.equal(plan('app-film', 'standard', path.join(tmp, `${dir}.json`)).status, 0);
    assert.ok(fs.readFileSync(path.join(tmp, 'a.json')).equals(fs.readFileSync(path.join(tmp, 'b.json'))), 'planning is deterministic');
    const film = JSON.parse(fs.readFileSync(path.join(tmp, 'a.json'), 'utf8'));
    const source = JSON.parse(fs.readFileSync(path.join(root, scenesDir, 'examples/app-film.motion-score.json'), 'utf8'));
    assert.equal(film.revision, source.revision + 1);
    assert.equal(film.approval.status, 'proposed');
    assert.equal(film.soundDesign.engine, 'studio-synth-1');
    const bar = 4 * 60 / film.soundDesign.music.bpm, seconds = source.totalFrames / 30;
    assert.equal(film.soundDesign.music.energies.length, Math.ceil(seconds / bar));
    const {revealBar, revealFrame, bpm} = film.soundDesign.music, target = 100;
    assert.ok(Math.abs(revealBar * bar - revealFrame / 30) < 0.001, 'the final reveal lands on a downbeat of the composed music');
    assert.ok(Math.abs(bpm / target - 1) <= 0.08, 'the fitted tempo stays near the style tempo');
    assert.ok(film.sfx.some(cue => cue.frame === revealFrame && cue.event.includes('settles')), 'the final hit and the downbeat share the frame');
    assert.deepEqual(checkScore(film).errors, []);
    const phone = source.scenes.find(scene => scene.id === 'phone'), tap = phone.start + phone.params.taps[0].at;
    assert.ok(film.sfx.some(cue => cue.sound === 'click' && cue.frame === tap), 'the click is on the tap frame');
    assert.ok(film.sfx.some(cue => cue.sound === 'release' && cue.frame === tap + 4));
    const push = film.sfx.find(cue => cue.event.includes('pushes in'));
    assert.equal(push.frame, phone.start + phone.params.screens[1].at + 6, 'the push whoosh peaks halfway through the push');
    assert.equal(push.params.direction, -1, 'it travels with the incoming screen');
    for (const cue of film.sfx.filter(item => item.sound === 'whoosh')) assert.ok(cue.gain <= -10, `whooshes stay below hits: ${cue.event}`);
    film.sfx.forEach((cue, i) => i && assert.ok(cue.frame >= film.sfx[i - 1].frame, 'frame order'));
    assert.equal(plan('color-block', 'minimal', path.join(tmp, 'blocks.json'), ['--no-music']).status, 0);
    const blocks = JSON.parse(fs.readFileSync(path.join(tmp, 'blocks.json'), 'utf8'));
    assert.equal(blocks.soundDesign.music, undefined);
    const wipe = blocks.sfx.find(cue => cue.event.includes('wipes in'));
    assert.ok(wipe && wipe.params.direction === 1, 'a wipe from the left travels left to right');
    assert.ok(!blocks.sfx.some(cue => cue.sound === 'knock'), 'minimal density leaves out landings');
    assert.notEqual(plan('app-film', 'standard', path.join(tmp, 'a.json')).status, 0, 'never overwrites');
    const bad = {...film, sfx: [{frame: film.totalFrames, sound: 'beep'}, {frame: 1, sound: 'click', gain: 12, pan: 2, params: []}]};
    const errors = checkScore(bad).errors.join('\n');
    assert.match(errors, /frame must be an integer inside the timeline/); assert.match(errors, /sound must be one of/); assert.match(errors, /gain must be/); assert.match(errors, /pan must be/); assert.match(errors, /params must be an object/); assert.match(errors, /frame order/);
  } finally { fs.rmSync(tmp, {recursive: true, force: true}); }
});

test('a mastered sound mix puts every hit on its frame', {skip: !(python && numpy && ffmpegLoudnorm) && 'python3 with Pillow and numpy, or ffmpeg with loudnorm, not installed'}, () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'motion-mix-'));
  try {
    const sound = path.join(root, soundDir, 'sound.py'), planned = path.join(tmp, 'film.json'), wav = path.join(tmp, 'mix.wav'), stems = path.join(tmp, 'stems');
    assert.equal(spawnPython('python3', ['-B', sound, 'plan', path.join(root, scenesDir, 'examples/app-film.motion-score.json'), '--out', planned], {encoding: 'utf8'}).status, 0);
    const mixed = spawnPython('python3', ['-B', sound, 'mix', planned, '--wav', wav, '--stems', stems], {encoding: 'utf8'});
    assert.equal(mixed.status, 0, mixed.stderr + mixed.stdout);
    const summary = JSON.parse(mixed.stdout);
    assert.ok(summary.timing.all_ok && summary.timing.max_offset_ms <= 2, mixed.stdout);
    assert.ok(Math.abs(summary.loudness.lufs + 14) <= 2 && summary.loudness.true_peak_db <= -0.95, mixed.stdout);
    assert.ok(fs.existsSync(path.join(stems, 'music.wav')), 'the music stem is written next to the effects stem');
    const checked = spawnPython('python3', ['-B', sound, 'check', path.join(stems, 'effects.wav'), planned], {encoding: 'utf8'});
    assert.equal(checked.status, 0, checked.stdout);
  } finally { fs.rmSync(tmp, {recursive: true, force: true}); }
});
