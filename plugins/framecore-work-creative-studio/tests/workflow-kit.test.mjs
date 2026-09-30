import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';
import {validateStudio} from '../scripts/validate-studio.mjs';
import {preflight} from '../skills/image-prompt-architect/kit/scripts/static-design-preflight.mjs';

const source = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
function fixture(action) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'studio-kit-test-'));
  try { fs.cpSync(source, root, {recursive:true}); return action(root); }
  finally { fs.rmSync(root, {recursive:true, force:true}); }
}
const edit = (root, file, fn) => { const p=path.join(root,file);fs.writeFileSync(p,fn(fs.readFileSync(p,'utf8'))); };
const editJson = (root,file,fn) => edit(root,file,text => {const value=JSON.parse(text);fn(value);return JSON.stringify(value);});
const codes = root => (validateStudio(root).canonical?.errors ?? []).map(item => item.code);

test('exact copy cannot match inside a longer word or price', () => {
  const example = JSON.parse(fs.readFileSync(path.join(source, 'skills/image-prompt-architect/kit/templates/static-design-notes.json'), 'utf8'));
  for (const [approved, supplied, expected] of [
    ['10 zł', '10 zł', true], ['10 zł', '110 zł', false], ['10 zł', '10 złotych', false],
    ['10 zł', '110,10 zł', false], ['10 zł', '110.10 zł', false],
    ['10', '10,90', false], ['10', '10.90', false], ['10,90 zł', '10,90 zł', true],
    ['CISZA', 'NIECISZA', false], ['CISZA', 'CISZA', true], ['CISZA', 'cisza', false],
    ['ŻÓŁĆ', 'ŻÓŁĆ', true], ['ŻÓŁĆ', 'ŻÓŁĆx', false], ['A', 'A\u0301', false],
    ['CENA', 'CENA_2', false], ['10 zł', '10  zł', false],
    ['C++ (50%)', 'C++ (50%)', true], ['C++ (50%)', 'C+ (50%)', false]
  ]) {
    const notes = structuredClone(example);
    notes.copy.items[0].text = approved;
    notes.prompt = `Create a poster. Visible text: "${supplied}".`;
    assert.equal(preflight(notes).status, expected ? 'ready_for_prompt_review' : 'blocked', supplied);
  }
  example.copy.items[0].text = '10 zł';
  for (const prompt of ['10 zł', 'Headline: 10 zł.', 'Reject "110 zł"; use "10 zł".']) {
    example.prompt = prompt;
    assert.equal(preflight(example).status, 'ready_for_prompt_review', prompt);
  }
});

test('blueprint QA gates and mapped audio owner cannot disappear', () => {
  const relative = 'skills/pipeline-core/references/workflow-blueprints.md';
  for (const heading of ['Static Campaign Or E-Commerce Graphic', 'Video Campaign Or Storyboard', 'Artist-led Music Video', 'Standalone Audio Planning Or Review']) fixture(root => {
    edit(root, relative, text => {
      const start = text.indexOf('## ' + heading), end = text.indexOf('\n## ', start + 3);
      const block = text.slice(start, end);
      const changed = block.replace(/^- `post_execution_fit`.*\n/m, '');
      assert.notEqual(changed, block);
      return text.slice(0, start) + changed + text.slice(end);
    });
    assert.ok(codes(root).includes('KIT_BLUEPRINT_GATE'), heading);
  });
  fixture(root => {
    edit(root, relative, text => text.replace('6. `audio-production`', '6. `audio-production-missing`'));
    assert.ok(codes(root).includes('KIT_BLUEPRINT_ROLE'));
  });
  for (const label of ['Route:', 'Required gates:']) fixture(root => {
    edit(root, relative, text => {
      const start = text.indexOf('## Standalone Audio Planning Or Review');
      const block = text.slice(start);
      return text.slice(0, start) + block.replace(label, 'Removed:').replace(/^- `post_execution_fit`.*\n/m, '');
    });
    assert.ok(codes(root).includes('KIT_BLUEPRINT_STRUCTURE'), label);
  });
});

test('matching graph and prose cannot remove outgoing music handoffs', () => fixture(root => {
  editJson(root, 'scripts/workflow-kit-routes.json', data => {
    const outgoing = data.handoffs.filter(row => row.from === 'music-video-direction');
    assert.equal(outgoing.length, 3);
    for (const row of outgoing) row.from = 'workflow-orchestrator';
  });
  edit(root, 'skills/pipeline-core/references/handoff-matrix.md', text => text.replace(/^\| music-video-direction \|/gm, '| workflow-orchestrator |'));
  const errors = codes(root);
  assert.ok(errors.includes('KIT_MUSIC_HANDOFF'));
  assert.ok(!errors.includes('KIT_HANDOFF_MAP'));
}));

test('each required image operation contract must occur exactly once', () => {
  for (const need of ['Image supplied as a reference for a new asset', 'Approved base image supplied for an edit', 'Existing image explicitly supplied for review']) {
    for (const duplicate of [false, true]) fixture(root => {
      editJson(root, 'scripts/studio-contracts.json', data => {
        const contract = data.operation_routes.find(route => route.need === need);
        assert.ok(contract);
        if (duplicate) data.operation_routes.push(contract);
        else data.operation_routes = data.operation_routes.filter(route => route.need !== need);
      });
      assert.ok(codes(root).includes('OPERATION_ROUTE_CONTRACT'), need);
    });
  }
});

test('workflow-kit candidate passes canonical validation', () => assert.equal(validateStudio(source).status,'PASS'));
test('CQoT cannot use a conflicting quality-gate expansion', () => fixture(root => {
  edit(root, 'skills/pipeline-core/references/inference-reasoning-methods.md', text => text.replace('Critical-Questions-of-Thought', 'Concise Quality Of Thought'));
  assert.ok(codes(root).includes('REASONING_METHOD_POLICY'));
}));
test('method handoffs cannot lose the shared review budget or evidence boundary', () => {
  fixture(root => {
    edit(root, 'skills/pipeline-core/references/inference-reasoning-methods.md', text => text.replace('No method\nor handoff resets this budget', 'Each handoff starts a fresh repair budget'));
    assert.ok(codes(root).includes('REASONING_METHOD_POLICY'));
  });
  fixture(root => {
    edit(root, 'skills/pipeline-core/references/inference-reasoning-methods.md', text => text.replace('leave missing evidence Unknown', 'accept the model answer as verification'));
    assert.ok(codes(root).includes('REASONING_METHOD_POLICY'));
  });
});
test('direct reviewer and research owners must retain the conditional method route', () => {
  for (const owner of ['output-critic-iteration', 'research-evidence']) fixture(root => {
    edit(root, 'skills/' + owner + '/SKILL.md', text => text.replace('inference-reasoning-methods.md#one-review-conditional-methods', 'inference-reasoning-methods.md'));
    assert.ok(codes(root).includes('REASONING_METHOD_ROUTE'));
  });
});
test('static-only blueprints cannot restore separate copy or prompt intake', () => fixture(root => {
  edit(root, 'skills/pipeline-core/references/workflow-blueprints.md', text => text.replace('6. `static-direction`', '6. `static-direction`\n7. `copy-voice` when visible text matters'));
  assert.ok(codes(root).includes('KIT_STATIC_OWNER'));
}));
test('a passing Copy Pack cannot acquire a compulsory rewrite cycle', () => fixture(root => {
  edit(root, 'skills/pipeline-core/references/loop-protocol.md', text => text.replace('At least one bounded review is required', 'At least one review-and-revision cycle is required'));
  assert.ok(codes(root).includes('KIT_COPY_REVIEW_POLICY'));
}));
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
