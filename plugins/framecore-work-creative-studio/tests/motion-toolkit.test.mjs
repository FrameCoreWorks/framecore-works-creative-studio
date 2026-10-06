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
