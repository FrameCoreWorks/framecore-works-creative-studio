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
