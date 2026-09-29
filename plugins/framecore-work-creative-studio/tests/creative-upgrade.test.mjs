import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';
import {reviewSequence, reviewTaste} from '../scripts/review-creative-plan.mjs';
import {validateStudio} from '../scripts/validate-studio.mjs';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const json=relative=>JSON.parse(fs.readFileSync(path.join(root,relative),'utf8'));
const sequence=()=>json('skills/storyboard-sequence-architect/assets/shot-plan.example.json');
const taste=()=>json('skills/studio-workstyle-profile/assets/taste-profile.example.json');
function fixture(fn) {
  const temp=fs.mkdtempSync(path.join(os.tmpdir(),'creative-upgrade-'));
  try {fs.cpSync(root,temp,{recursive:true});return fn(temp);}
  finally {fs.rmSync(temp,{recursive:true,force:true});}
}
const codes=directory=>(validateStudio(directory).canonical?.errors??[]).map(e=>e.code);

test('proposed example preserves strict locks and blocks unresolved references',()=>{
  const plan=sequence(), result=reviewSequence(plan);
  assert.equal(result.status,'structurally_valid_plan');
  assert.equal(result.execution_readiness,'blocked');
  assert.equal(result.observed_quality,'uninspected');
  assert.equal(result.blockers.length,5);
  assert.ok(plan.shots.every(s=>s.continuity_requirement==='strict'));
  for(const shot of plan.shots)shot.bound_refs=[...shot.required_refs];
  assert.equal(reviewSequence(plan).execution_readiness,'unverified');
});
test('timeline gaps and falsely measured timing are rejected',()=>{
  const plan=sequence();plan.shots[1].start_s+=0.2;
  assert.match(reviewSequence(plan).errors.join('\n'),/timeline gap/);
  plan.shots[1].start_s=4;plan.shots[0].timing_basis='measured';
  assert.match(reviewSequence(plan).errors.join('\n'),/observed evidence/);
});
test('dissolve overlap is accounted for once and cannot consume a shot',()=>{
  const plan=sequence();plan.shots[1].start_s=3.5;plan.bridges[0].type='dissolve';plan.bridges[0].overlap_s=0.5;
  assert.deepEqual(reviewSequence(plan).errors,[]);
  plan.bridges[0].type='sound_bridge';assert.match(reviewSequence(plan).errors.join('\n'),/picture overlap/);
  plan.bridges[0].type='dissolve';plan.shots[1].start_s=0;plan.bridges[0].overlap_s=4;
  assert.match(reviewSequence(plan).errors.join('\n'),/entire shot/);
});
test('unknown physical state, duplicate bridges and invalid clip duration fail',()=>{
  const plan=sequence();plan.shots[0].exit_state='Unknown';plan.shots[0].generation_duration_s=-1;plan.bridges[1]={...plan.bridges[0]};
  const result=reviewSequence(plan);assert.equal(result.execution_readiness,'blocked');
  assert.match(result.errors.join('\n'),/entry\/exit states/);assert.match(result.errors.join('\n'),/duration.*positive/);assert.match(result.errors.join('\n'),/Duplicate bridge/);
  plan.shots[0].generation_duration_s=3;assert.match(reviewSequence(plan).errors.join('\n'),/exceeds/);
});
test('complex motion asks for human review rather than inventing a render verdict',()=>{
  const plan=sequence();plan.shots[0].camera_moves=2;
  const result=reviewSequence(plan);assert.deepEqual(result.errors,[]);assert.match(result.human_review.join('\n'),/complexity/);assert.equal(result.observed_quality,'uninspected');
});
test('malformed plans fail without throwing',()=>{
  for(const value of [null,[],{}, {target_duration_s:25,shots:[null],bridges:[]}])assert.equal(reviewSequence(value).status,'invalid_plan');
});
test('scoped synthetic taste is valid without persisting it or inventing a reason',()=>{
  const profile=taste();assert.equal(profile.records[1].stated_reason,'Unknown');
  const result=reviewTaste(profile);assert.equal(result.status,'structurally_valid_profile');assert.equal(result.persistence,'not_performed');
  profile.records[0].status='retired';assert.deepEqual(reviewTaste(profile).errors,[]);
});
test('one implicit choice cannot become confirmed reusable taste',()=>{
  const profile=taste();profile.records[2].evidence_count=1;profile.records[2].confidence='confirmed';
  const errors=reviewTaste(profile).errors.join('\n');assert.match(errors,/one implicit/);assert.match(errors,/cannot be labelled confirmed/);
});
test('scope and evidence must survive the taste handoff',()=>{
  const profile=taste();profile.records[0].scope='everyone';profile.records[1].source_decision='Unknown';
  assert.equal(reviewTaste(profile).errors.length,2);
});
test('CLI is read-only and reports malformed JSON separately from invalid plans',()=>{
  const temp=fs.mkdtempSync(path.join(os.tmpdir(),'creative-cli-'));
  try {
    const input=path.join(temp,'plan.json');fs.writeFileSync(input,JSON.stringify(sequence()));const before=fs.readFileSync(input);
    const run=()=>spawnSync(process.execPath,[path.join(root,'scripts/review-creative-plan.mjs'),'sequence',input],{cwd:temp,encoding:'utf8'});
    let result=run();assert.equal(result.status,0,result.stderr);assert.equal(JSON.parse(result.stdout).observed_quality,'uninspected');
    assert.deepEqual(fs.readdirSync(temp),['plan.json']);assert.deepEqual(fs.readFileSync(input),before);
    fs.writeFileSync(input,'{}');assert.equal(run().status,1);
    fs.writeFileSync(input,'{');assert.equal(run().status,2);
  } finally {fs.rmSync(temp,{recursive:true,force:true});}
});
test('exact archive preserves every original source path and file byte',()=>{
  const code=`import hashlib,json,pathlib,tarfile,sys
root=pathlib.Path(sys.argv[1]); m=json.loads((root/'integrations/workflow-kit/source-manifest.json').read_text())
with tarfile.open(root/m['archive']['path'],'r:gz') as a:
 members=a.getmembers(); assert len(members)==len(m['source_files'])==359
 assert {v.name for v in members}=={v['source_path'] for v in m['source_files']}
 for v in m['source_files']:
  member=a.getmember(v['source_path']); assert member.isfile()
  content=a.extractfile(member).read(); assert len(content)==v['bytes']; assert hashlib.sha256(content).hexdigest()==v['sha256'],v['source_path']
`;
  const result=spawnSync('python3',['-c',code,root],{encoding:'utf8'});assert.equal(result.status,0,result.stderr);
});
test('reintroducing source skill frontmatter is detected by recursive discovery',()=>fixture(temp=>{
  const m=JSON.parse(fs.readFileSync(path.join(temp,'integrations/workflow-kit/source-manifest.json'),'utf8'));
  const pointer=path.join(temp,m.discovery_stubs[0].path);
  fs.writeFileSync(pointer,'---\nname: duplicate\ndescription: unwanted source entry\n---\n');
  const result=codes(temp);assert.ok(result.includes('RECURSIVE_DISCOVERY'));assert.ok(result.includes('KIT_DISCOVERY_STUB'));
}));
test('archive corruption is detected independently of the expanded source mirror',()=>fixture(temp=>{
  const m=JSON.parse(fs.readFileSync(path.join(temp,'integrations/workflow-kit/source-manifest.json'),'utf8'));
  fs.appendFileSync(path.join(temp,m.archive.path),'corrupt');assert.ok(codes(temp).includes('KIT_SOURCE_ARCHIVE'));
}));
test('orphaning a registered upgrade resource is caught even when every file still exists',()=>fixture(temp=>{
  const reference='skills/tool-routing-cost/references/execution-adapter-contract.md';
  const registry=JSON.parse(fs.readFileSync(path.join(temp,'scripts/creative-upgrade-contracts.json'),'utf8'));
  for(const owner of registry.owners){
    const f=path.join(temp,'skills',owner,'SKILL.md');
    const text=fs.readFileSync(f,'utf8').replace(/\]\(([^)]+)\)/g,(whole,href)=>
      path.resolve(path.dirname(f),href.split('#')[0])===path.join(temp,reference)?'](SKILL.md)':whole);
    fs.writeFileSync(f,text);
  }
  assert.ok(codes(temp).includes('CREATIVE_REFERENCE_ROUTE'));
}));
