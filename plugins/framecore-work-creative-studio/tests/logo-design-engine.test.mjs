import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const engine = path.join(root, 'skills/static-graphic-design-creator/assets/logo-design-engine');
const adapter = path.join(engine, 'studio_logo.py');
const python = process.env.PYTHON || 'python3';
const env = {...process.env, PYTHONDONTWRITEBYTECODE: '1'};
const hash = p => createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const run = args => spawnSync(python, [adapter, ...args], {encoding: 'utf8', timeout: 120000, env});
const ok = args => {const r = run(args); assert.equal(r.status, 0, r.stderr + r.stdout); return JSON.parse(r.stdout);};
const svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><title>Fixture</title><path d="M32 32H224V224H32ZM88 88V168H168V88Z" fill="#167066" fill-rule="evenodd"/></svg>';
function fixture(t) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'studio-logo-'));
  t.after(() => fs.rmSync(dir, {recursive: true, force: true}));
  fs.writeFileSync(path.join(dir, 'mark.svg'), svg);
  fs.writeFileSync(path.join(dir, 'spec.json'), JSON.stringify({brand: 'QA fixture', brief: 'Tool fixture, not a proposed identity', criteria: 'Preserve the hollow square at the requested size', greyscale: false, concepts: [{name: 'Fixture', symbol: 'mark.svg', idea: 'Test geometry'}]}));
  return dir;
}

test('all pinned reusable source files remain byte-identical, with both rights notices', () => {
  const manifest = JSON.parse(fs.readFileSync(path.join(root, 'integrations/logo-design-skill/source-manifest.json')));
  assert.equal(manifest.commit, '0ecf52e9a4b3ac92b714f7cc6e3148ab8c774134');
  assert.ok(manifest.bundled_files.length >= 100);
  for (const file of manifest.bundled_files) assert.equal(hash(path.join(root, file.path)), file.sha256, file.path);
  assert.equal(fs.readdirSync(path.join(engine, 'scripts')).filter(f => f.endsWith('.py')).length, 9);
  assert.equal(fs.readdirSync(path.join(engine, 'references')).length, 14);
  assert.equal(fs.readdirSync(path.join(engine, 'templates')).length, 2);
  assert.ok(fs.existsSync(path.join(engine, 'LICENSE')));
  assert.ok(fs.existsSync(path.join(engine, 'TRADEMARKS.md')));
  assert.ok(!fs.existsSync(path.join(engine, 'SKILL.md')));
  assert.ok(!fs.existsSync(path.join(engine, 'assets/library/svg')));
});

test('capability probe does not claim render execution or host registration', () => {
  const r = ok(['probe']);
  assert.equal(r.source_tools, 9);
  assert.equal(r.catalog_records, 1432);
  assert.equal(r.bundled_reference_svg_count, 0);
  assert.equal(r.render_execution, 'not_run');
  assert.equal(r.automatic_dependency_installation, false);
});

test('catalog search returns pinned external references without pretending their SVGs are bundled', () => {
  const r = ok(['search', '--type', 'letterform', '--limit', '2']);
  assert.equal(r.records.length, 2);
  assert.equal(r.corpus_attached, false);
  for (const item of r.records) {
    assert.equal(item.local_svg, null);
    assert.match(item.source_url, /0ecf52e9.*\/svg\/.*\.svg$/);
    assert.match(item.rights, /Separate trademark rights/);
  }
});

test('new project creates a blank brief and refuses to overwrite an existing directory', t => {
  const dir = fixture(t), out = path.join(dir, 'new');
  const r = ok(['init', out]);
  assert.equal(r.artwork, 'not_created');
  assert.equal(JSON.parse(fs.readFileSync(path.join(out, 'presentation-spec.json'))).brand, '');
  assert.notEqual(run(['init', out]).status, 0);
});

test('full SVG/HTML build emits sheets, presentation, audits, variants and content-bound manifest', t => {
  const dir = fixture(t), out = path.join(dir, 'review');
  const original = hash(path.join(dir, 'mark.svg'));
  const r = ok(['build', path.join(dir, 'spec.json'), '--out', out]);
  assert.equal(r.status, 'built');
  const report = JSON.parse(fs.readFileSync(path.join(out, 'delivery.json')));
  assert.equal(report.visual_approval, 'not_run');
  assert.equal(report.audit_is_certification, false);
  assert.equal(report.inputs[0].sha256, original);
  assert.equal(hash(path.join(dir, 'mark.svg')), original);
  assert.ok(!fs.existsSync(path.join(out, 'concepts.png')), 'raster off must not launch a renderer');
  for (const name of ['concepts.svg', 'preview.html', 'presentation.html', 'audit.json', 'variants-01/logo-01-black.svg', 'variants-01/logo-01-app-icon.svg']) assert.ok(fs.existsSync(path.join(out, name)), name);
  for (const file of report.files) assert.equal(hash(path.join(out, file.path)), file.sha256, file.path);
  assert.notEqual(run(['build', path.join(dir, 'spec.json'), '--out', out]).status, 0);
});

test('separate avatar geometry drives favicon and app-icon while the master stays unchanged', t => {
  const dir = fixture(t), out = path.join(dir, 'avatar-review');
  fs.writeFileSync(path.join(dir, 'avatar.svg'), '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><circle cx="128" cy="128" r="80" fill="#167066"/></svg>');
  const spec = JSON.parse(fs.readFileSync(path.join(dir, 'spec.json')));
  spec.concepts[0].avatar = 'avatar.svg';
  fs.writeFileSync(path.join(dir, 'spec.json'), JSON.stringify(spec));
  ok(['build', path.join(dir, 'spec.json'), '--out', out]);
  for (const variant of ['favicon', 'app-icon']) {
    const text = fs.readFileSync(path.join(out, 'variants-01/logo-01-' + variant + '.svg'), 'utf8');
    assert.match(text, /<circle\b/);
    assert.doesNotMatch(text, /M32 32H224/);
  }
  assert.match(fs.readFileSync(path.join(out, 'variants-01/logo-01-black.svg'), 'utf8'), /M32 32H224/);
});

test('build rejects active SVG and package-local output before creating deliverables', t => {
  const dir = fixture(t);
  fs.writeFileSync(path.join(dir, 'mark.svg'), svg.replace('</svg>', '<script>alert(1)</script></svg>'));
  assert.notEqual(run(['build', path.join(dir, 'spec.json'), '--out', path.join(dir, 'bad')]).status, 0);
  assert.ok(!fs.existsSync(path.join(dir, 'bad')));
  assert.notEqual(run(['init', path.join(engine, 'forbidden-output')]).status, 0);
});

test('corpus verification rejects incomplete or modified original references', t => {
  const dir = fixture(t);
  const r = run(['verify-corpus', dir]);
  assert.notEqual(r.status, 0);
  assert.match(r.stderr, /differs from the reviewed pin/);
});

test('greyscale contact sheet uses a filter-capable browser instead of silent Cairo colour output', t => {
  const dir = fixture(t);
  const code = `import importlib.util,json,sys
from pathlib import Path
s=importlib.util.spec_from_file_location('adapter',sys.argv[1]); a=importlib.util.module_from_spec(s);s.loader.exec_module(a)
calls=[]
a.render_png.find_chrome=lambda:'mock-browser'
a.render_png.render=lambda *args,**kw: calls.append(kw.get('backend')) or 'mock'
a.tool('concept_sheet',[sys.argv[2],'--greyscale','-o',sys.argv[3]])
print(json.dumps(calls))`;
  const r = spawnSync(python, ['-c', code, adapter, path.join(dir, 'mark.svg'), path.join(dir, 'sheet.svg')], {encoding: 'utf8', env});
  assert.equal(r.status, 0, r.stderr);
  assert.deepEqual(JSON.parse(r.stdout), ['chrome']);
});

test('renderer failure records incomplete output and cannot satisfy a required raster build', t => {
  const dir = fixture(t), out = path.join(dir, 'missing-raster');
  const code = `import importlib.util,sys
s=importlib.util.spec_from_file_location('adapter',sys.argv[1]); a=importlib.util.module_from_spec(s);s.loader.exec_module(a)
a.render_png.available_backends=lambda:['mock']
a.render_png.render=lambda *args,**kw: None
try: a.build(sys.argv[2],sys.argv[3],'required')
except ValueError as e: print(e);sys.exit(1)`;
  const r = spawnSync(python, ['-c', code, adapter, path.join(dir, 'spec.json'), out], {encoding: 'utf8', env});
  assert.equal(r.status, 1, r.stderr);
  assert.match(r.stdout, /raster outputs are incomplete/);
  const report = JSON.parse(fs.readFileSync(path.join(out, 'delivery.json')));
  assert.equal(report.status, 'incomplete');
  assert.ok(report.raster[0].missing.includes('logo-01-black-512.png'));
  assert.ok(!fs.existsSync(path.join(out, 'variants-01/favicon.ico')));
});

test('raster build verifies PNG and favicon files instead of treating upstream exit zero as completion', {skip: process.env.STUDIO_LOGO_RENDER_TEST !== '1'}, t => {
  const dir = fixture(t), out = path.join(dir, 'raster');
  const r = ok(['build', path.join(dir, 'spec.json'), '--out', out, '--raster', 'required']);
  assert.equal(r.status, 'built');
  for (const file of ['concepts.png', 'variants-01/favicon-16.png', 'variants-01/favicon-32.png', 'variants-01/favicon-48.png', 'variants-01/icon-512.png']) {
    const data = fs.readFileSync(path.join(out, file));
    assert.equal(data.subarray(0, 8).toString('hex'), '89504e470d0a1a0a');
    if (file.includes('16.png')) assert.equal(data.readUInt32BE(16), 16);
  }
  assert.equal(fs.readFileSync(path.join(out, 'variants-01/favicon.ico')).readUInt16LE(2), 1);
  const report = JSON.parse(fs.readFileSync(path.join(out, 'delivery.json')));
  assert.ok(report.raster.every(item => item.status === 'complete'));
});
