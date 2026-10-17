import test from 'node:test';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { existsSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildPage, checkNode, main } from '../skills/hyperframes-workflow/assets/anatomy-engine/studio.mjs';
import { createFrameBridge } from '../skills/hyperframes-workflow/assets/anatomy-engine/frame-bridge.mjs';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const engine = join(root, 'skills/hyperframes-workflow/assets/anatomy-engine');

test('complete pinned Anatomy graphics files retain upstream bytes and licence', () => {
  const manifest = JSON.parse(readFileSync(join(root, 'integrations/anatomy/source-manifest.json')));
  const paths = manifest.files.map(f => f.source_path);
  assert.equal(paths.filter(p => p.startsWith('kit/')).length, 15);
  for (const path of ['kit/gl.mjs', 'kit/turn.mjs', 'kit/turn-audit.mjs', 'kit/react/live.tsx', 'scripts/drive.mjs', 'examples/ripple-tank/model.mjs']) assert.ok(paths.includes(path));
  for (const file of manifest.files) assert.equal(createHash('sha256').update(readFileSync(join(root, file.path))).digest('hex'), file.sha256, file.path);
  assert.match(readFileSync(join(engine, 'LICENSE'), 'utf8'), /2026 Ryan/);
  for (const path of ['SKILL.md', 'scripts/publish.mjs', 'scripts/session.mjs']) assert.equal(existsSync(join(engine, path)), false);
});

test('frame bridge uses half-open frames and deterministic direct/backward/repeated seeks', () => {
  const history = [], target = {};
  const clock = createFrameBridge({ fps: 30, seconds: 2, target, draw: s => history.push({ ...s }) });
  assert.equal(clock.state.frame, 0);
  target.renderFrame(1);
  const middle = clock.state;
  clock.renderIndex(0);
  target.renderFrame(1);
  assert.deepEqual(clock.state, middle);
  assert.equal(clock.renderFrame(2).frame, 59);
  assert.equal(clock.renderIndex(-9).frame, 0);
  assert.throws(() => clock.renderFrame(NaN), /finite/);
  assert.throws(() => clock.renderIndex(0.5), /integer/);
  assert.throws(() => createFrameBridge({ fps: 0, draw() {} }), /Positive/);
  assert.ok(history.length > 4);
});

test('SVG, WebGL and 3D fixtures build actual respective runtimes with one frame bridge', () => {
  for (const mode of ['svg', 'webgl', '3d']) {
    const html = buildPage({ mode, title: '<script>bad</script>' });
    assert.match(html, /class="iso"/);
    assert.match(html, /type="range"/);
    assert.match(html, /target\.renderFrame/);
    assert.match(html, /&lt;script&gt;/);
    assert.doesNotMatch(html, /<script>bad/);
    if (mode === 'svg') assert.match(html, /id="marker"/);
    if (mode === 'webgl') {
      assert.match(html, /glLayer\(/);
      assert.match(html, /webglcontextlost/);
      assert.match(html, /SVG fallback/);
    }
    if (mode === '3d') {
      assert.match(html, /TURN\.mount/);
      assert.match(html, /__isoVerify/);
      assert.match(html, /controller\.set/);
    }
  }
});

test('invalid runtimes/options fail and project/output creation never overwrites', () => {
  assert.throws(() => checkNode('18.20.0'), /20.10/);
  assert.throws(() => checkNode('20.9.0'), /20.10/);
  checkNode('20.10.0'); checkNode('22.20.0');
  assert.throws(() => buildPage({ mode: 'unknown' }), /Mode/);
  assert.throws(() => buildPage({ width: 0 }), /Size/);
  const temp = mkdtempSync(join(tmpdir(), 'studio-anatomy-'));
  try {
    main(['init', join(temp, 'project')]);
    assert.ok(existsSync(join(temp, 'project/kit/turn.mjs')));
    assert.throws(() => main(['init', join(temp, 'project')]), /already exists/);
    assert.throws(() => main(['init', join(engine, 'nested')]), /outside/);
    const out = join(temp, 'page.html');
    main(['build', '--mode', '3d', '--out', out]);
    assert.throws(() => main(['build', '--out', out]), /EEXIST/);
    assert.throws(() => main(['build', '--out', out, '--mystery', '1']), /Invalid/);
  } finally { rmSync(temp, { recursive: true, force: true }); }
});

test('local browser renders all routes, repeats identical frames and exposes a mobile SVG fallback', {
  skip: process.env.STUDIO_ANATOMY_BROWSER_TEST !== '1', timeout: 120000,
}, () => {
  const temp = mkdtempSync(join(tmpdir(), 'studio-anatomy-browser-'));
  const digest = file => createHash('sha256').update(readFileSync(file)).digest('hex');
  const drive = (page, actions, extra = []) => {
    const file = join(temp, 'actions.json');
    writeFileSync(file, JSON.stringify(actions));
    const result = spawnSync(process.execPath, [join(engine, 'scripts/drive.mjs'), page, '--actions', file, ...extra], { encoding: 'utf8', timeout: 30000 });
    assert.equal(result.status, 0, result.stdout + result.stderr);
    assert.match(result.stdout, /console: clean/);
  };
  try {
    for (const mode of ['svg', 'webgl', '3d']) {
      const page = join(temp, mode + '.html');
      writeFileSync(page, buildPage({ mode }));
      const actions = [['until', 'window.__studioAnatomy?.ready']];
      if (mode === 'webgl') actions.push(['eval', 'if(!window.__studioAnatomy.webgl) throw new Error("No WebGL render"); true']);
      for (const [time, name] of [[0, 'start'], [1, 'middle'], [0, 'replay']]) {
        actions.push(['eval', `window.renderFrame(${time}); new Promise(done => requestAnimationFrame(() => requestAnimationFrame(() => done(true))))`], ['shot', join(temp, mode + '-' + name + '.png'), '#stage']);
      }
      actions.push(['key', 'ArrowRight', '#scrub'], ['eval', 'if(window.__studioAnatomy.frame !== 1) throw new Error("Keyboard did not select frame 1"); true']);
      drive(page, actions);
      assert.equal(digest(join(temp, mode + '-start.png')), digest(join(temp, mode + '-replay.png')), mode + ' repeat frame');
      assert.notEqual(digest(join(temp, mode + '-start.png')), digest(join(temp, mode + '-middle.png')));
    }
    drive(join(temp, 'webgl.html'), [
      ['until', 'window.__studioAnatomy?.ready'],
      ['eval', 'if(window.__studioAnatomy.webgl || document.querySelector("#fallback").hidden || document.documentElement.scrollWidth > innerWidth) throw new Error("Fallback or sizing failure"); true'],
    ], ['--no-webgl', '--width', '390', '--height', '844', '--reduced']);
  } finally { rmSync(temp, { recursive: true, force: true }); }
});
