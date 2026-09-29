import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';
import {validateStudio} from '../scripts/validate-studio.mjs';

const source = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
function fixture(action) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'studio-kit-test-'));
  try { fs.cpSync(source, root, {recursive:true}); return action(root); }
  finally { fs.rmSync(root, {recursive:true, force:true}); }
}
const edit = (root, file, fn) => { const p=path.join(root,file);fs.writeFileSync(p,fn(fs.readFileSync(p,'utf8'))); };
const editJson = (root,file,fn) => edit(root,file,text => {const value=JSON.parse(text);fn(value);return JSON.stringify(value);});
const codes = root => (validateStudio(root).canonical?.errors ?? []).map(item => item.code);

test('workflow-kit candidate passes canonical validation', () => assert.equal(validateStudio(source).status,'PASS'));
test('corrupted or extra snapshot files fail byte inventory', () => {
  fixture(root => {edit(root,'integrations/workflow-kit/upstream/README.md',t=>t+'\ncorrupted\n');assert.ok(codes(root).includes('KIT_SOURCE_HASH'));});
  fixture(root => {fs.writeFileSync(path.join(root,'integrations/workflow-kit/upstream/extra.txt'),'x');assert.ok(codes(root).includes('KIT_SOURCE_INVENTORY'));});
});
test('source skill omissions and active resource omissions are rejected', () => {
  fixture(root => {editJson(root,'integrations/workflow-kit/source-manifest.json',m=>m.skill_map.pop());assert.ok(codes(root).includes('KIT_SKILL_MAP'));});
  fixture(root => {editJson(root,'integrations/workflow-kit/source-manifest.json',m=>m.active_resources.pop());assert.ok(codes(root).includes('KIT_RESOURCE_COVERAGE'));});
});
test('active method must be reachable from the real skill root', () => fixture(root => {
  edit(root,'skills/image-prompt-architect/SKILL.md',t=>t.replace('(kit/method.md)','(references/static-prompt-compiler.md)'));
  assert.ok(codes(root).includes('KIT_METHOD_ROUTE'));
}));
test('a stale role map cannot hide behind valid skill names', () => fixture(root => {
  editJson(root,'scripts/workflow-kit-routes.json',m=>m.roles['static-direction'].shift());
  assert.ok(codes(root).includes('KIT_ROLE_MAP'));
}));
test('a missing handoff field or gate owner fails contract parity', () => {
  fixture(root => {editJson(root,'scripts/workflow-kit-routes.json',m=>m.handoffs[0].required_fields='goal');assert.ok(codes(root).includes('KIT_HANDOFF_MAP'));});
  fixture(root => {editJson(root,'scripts/workflow-kit-routes.json',m=>m.gates[0].owners=['missing-role']);assert.ok(codes(root).includes('KIT_GATE_OWNER'));});
});
test('all mapped roles are reachable through the formal handoff graph', () => fixture(root => {
  editJson(root,'scripts/workflow-kit-routes.json',m=>{m.handoffs=m.handoffs.filter(h=>h.to!=='music-video-direction');});
  assert.ok(codes(root).includes('KIT_ROLE_REACHABILITY'));
}));
test('a required research route cannot disappear from a planned case', () => fixture(root => {
  editJson(root,'evals/workflow-kit-cases.json',m=>{const c=m.cases.find(c=>c.id==='WK01');c.expected_owners=c.expected_owners.filter(owner=>owner!=='research-evidence');});
  assert.ok(codes(root).includes('KIT_RESEARCH_OWNER'));
}));
test('supplied images route by reference, edit-base, and review operation', () => fixture(root => {
  edit(root,'skills/workflow-orchestrator/references/capabilities-and-handoffs.md',t=>t.replace('Approved base image supplied for an edit','Actual still/raster image'));
  assert.ok(codes(root).includes('KIT_IMAGE_OPERATION_ROUTE'));
}));
test('research preflight has a reachable request, return handoff, and shared blueprint gate', () => fixture(root => {
  editJson(root,'scripts/workflow-kit-routes.json',m=>{m.handoffs=m.handoffs.filter(h=>!(h.from==='research-evidence'&&h.to==='workflow-orchestrator'));});
  assert.ok(codes(root).includes('KIT_RESEARCH_ROUTE'));
}));

test('video QA cannot be redirected to still-only review', () => fixture(root => {
  editJson(root,'scripts/workflow-kit-routes.json',m=>m.qa_by_modality.video='output-critic-iteration');
  assert.ok(codes(root).includes('KIT_MEDIA_QA'));
}));
test('silent continuity downgrade is a regression even with the authority page present', () => fixture(root => {
  edit(root,'skills/storyboard-sequence-architect/kit/method.md',t=>t+'\nName the carrier or mark continuity approximate.\n');
  assert.ok(codes(root).includes('KIT_STALE_POLICY'));
}));
test('integration specifications cannot disappear or claim model execution', () => {
  fixture(root => {editJson(root,'evals/workflow-kit-cases.json',m=>m.cases.pop());assert.ok(codes(root).includes('INTEGRATION_COVERAGE'));});
  fixture(root => {editJson(root,'evals/workflow-kit-cases.json',m=>m.cases[0].execution_status='passed');assert.ok(codes(root).includes('INTEGRATION_EVIDENCE'));});
});

test('relocated helpers support stdin import and share the authoritative static catalog', () => {
  const code = `
    import assert from 'node:assert/strict';
    import fs from 'node:fs';
    import {preflight} from './skills/image-prompt-architect/kit/scripts/static-design-preflight.mjs';
    import {loadCatalog,resolveCode} from './skills/commercial-visual-campaign-director/kit/scripts/poster-codes.mjs';
    assert.equal(preflight({request_kind:'concepts'}).status,'not_applicable');
    assert.equal(preflight({request_kind:'prompt',task_mode:'edit',references:[]}).status,'blocked');
    const catalog=loadCatalog();assert.equal(resolveCode('EP001',catalog).id,'EP001');
    assert.deepEqual(catalog,JSON.parse(fs.readFileSync('./skills/static-graphic-design-creator/upstream/references/event-poster-design-codes.json','utf8')));
  `;
  const result = spawnSync(process.execPath,['--input-type=module','-'],{input:code,cwd:source,encoding:'utf8',timeout:10000});
  assert.equal(result.status,0,result.stderr);
});
