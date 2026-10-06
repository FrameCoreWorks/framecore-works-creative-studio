import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {validateScore,secondsAtFrame,reviewFrames,cueTimes,renderPaperFrame,renderToneCues} from '../skills/hyperframes-workflow/assets/motion-quality/score.mjs';
import {loadLibrary,searchLibrary,presentEntry,validateLibrary,loadBriefIndex,matchBrief,presentBrief,validateBriefIndex} from '../skills/hyperframes-workflow/assets/motion-prompt-library/library.mjs';
const score=JSON.parse(fs.readFileSync(new URL('../skills/hyperframes-workflow/assets/motion-quality/example-score.json',import.meta.url),'utf8'));
test('rational frame time and half-open end are respected',()=>{
  assert.equal(secondsAtFrame(30,{fps:{num:30000,den:1001},totalFrames:60}),1.001);
  assert.throws(()=>secondsAtFrame(360,score),/outside/);
  assert.throws(()=>secondsAtFrame(-1,score),/outside/);
});
test('score rejects gaps, invalid holds and out-of-range sound tails',()=>{
  for(const mutate of [s=>s.scenes[1].start=121,s=>s.scenes[0].holds=[[1,122]],s=>s.cues[0].durationFrames=400,s=>s.fps.den=0]){
    const s=structuredClone(score);mutate(s);assert.throws(()=>validateScore(s));
  }
});
test('review includes both sides of boundaries, holds and final frame',()=>{
  const f=reviewFrames(score);
  for(const n of [0,74,75,76,119,120,121,239,240,241,269,270,271,359])assert.ok(f.includes(n),String(n));
  assert.equal(f.length,new Set(f).size);assert.ok(f.every(n=>n>=0&&n<360));
});
test('Paper receives milliseconds after playback is stopped, including backward seeks',()=>{
  const calls=[],mount={setSpeed:v=>calls.push(['speed',v]),setFrame:v=>calls.push(['frame',v])};
  renderPaperFrame(mount,60,score);renderPaperFrame(mount,0,score);renderPaperFrame(mount,60,score);
  assert.deepEqual(calls,[['speed',0],['frame',2000],['speed',0],['frame',0],['speed',0],['frame',2000]]);
});
test('Tone schedules seconds and includes release in declared cue duration',async()=>{
  const voices=[],args=[];
  const Tone={Synth:class{constructor(o){this.options=o;voices.push(this);}toDestination(){return this;}triggerAttackRelease(...a){this.note=a;}dispose(){this.disposed=true;}},
    Offline:async(fn,...rest)=>{args.push(...rest);fn();return {mock:true};}};
  assert.deepEqual(await renderToneCues(Tone,score),{mock:true});
  assert.deepEqual(args,[12,2,48000]);
  const cues=cueTimes(score);
  voices.forEach((v,i)=>{assert.equal(v.note[2],cues[i].timeSeconds);assert.equal(v.note[1]+v.options.envelope.release,cues[i].durationSeconds);assert.equal(v.disposed,true);});
});
test('audio rejects aliasing frequencies at selected sample rate',async()=>{
  const s=structuredClone(score);s.cues[0].frequency=10000;
  await assert.rejects(renderToneCues({Offline(){},Synth(){}},s,{sampleRate:8000}),/Nyquist/);
});
test('library validates unique substantive records and exposes provenance',()=>{
  const entries=loadLibrary();assert.deepEqual(validateLibrary(entries),[]);
  const entry=entries.find(e=>e.prompt_origin==='curator_reconstruction');
  assert.match(presentEntry(entry).purpose,/reference data/);assert.match(presentEntry(entry).authority,/does not approve/);
});
test('search respects related opt-in and Polish aliases',()=>{
  const entries=loadLibrary(),results=searchLibrary(entries,'typografia');
  assert.ok(results.length>0);assert.ok(results.some(e=>e.category==='typography'));
  assert.ok(searchLibrary(entries,'społecznościowe').some(e=>e.category==='social'));
  assert.ok(searchLibrary(entries,'',{limit:50}).every(e=>e.prompt_origin==='framecore_original'||e.default_motion_search));
  const related=entries.find(e=>e.category==='interactive'&&e.prompt_text);
  assert.equal(searchLibrary([related],'').length,0);assert.equal(searchLibrary([related],'',{includeRelated:true}).length,1);
});
test('creator-only records cannot silently gain redistributed text or tested status',()=>{
  const e=structuredClone(loadLibrary().find(e=>e.prompt_origin==='creator_prompt_link_only'));
  e.prompt_text='Unauthorized creator text';e.verification='PASS';
  const errors=validateLibrary([e]);assert.ok(errors.some(e=>e.includes('link-only')));assert.ok(errors.some(e=>e.includes('verification')));
});
test('brief index points to existing original records and matches Polish briefs',()=>{
  const entries=loadLibrary(),index=loadBriefIndex();
  assert.deepEqual(validateBriefIndex(index,entries),[]);
  assert.equal(matchBrief(index,'animowane logo do intro')[0].id,'logo-reveal');
  assert.ok(matchBrief(index,'rolka na instagram z wykresem sprzedaży').some(b=>b.id==='data-story'));
  assert.equal(matchBrief(index,'lekcja dla uczniów o ułamkach')[0].id,'education-lesson');
  assert.deepEqual(matchBrief(index,'zupełnie inny temat'),[]);
  const view=presentBrief(index.briefs[0],entries);
  assert.ok(view.records.every(r=>r.title&&r.objective));assert.match(view.authority,/selects no runtime/);
});
test('brief index rejects unknown, imported or excessive records',()=>{
  const entries=loadLibrary(),index=structuredClone(loadBriefIndex());
  index.briefs[0].records=['FC-NOPE-01',entries.find(e=>e.prompt_origin==='curator_reconstruction').id,'FC-BRAND-01','FC-BRAND-02','FC-BRAND-03'];
  const errors=validateBriefIndex(index,entries).join('\n');
  assert.match(errors,/two to four/);assert.match(errors,/unknown record FC-NOPE-01/);assert.match(errors,/FrameCore original/);
});
test('original blueprints have record-specific objectives',()=>{
  const originals=loadLibrary().filter(e=>e.prompt_origin==='framecore_original');
  assert.equal(new Set(originals.map(e=>e.objective)).size,originals.length);
  const rewritten=originals.filter(e=>['brand','editorial','product','social','transitions','typography'].includes(e.category));
  assert.equal(rewritten.length,60);
  assert.ok(rewritten.every(e=>e.prompt_text.includes('The purpose is to '+e.objective[0].toLowerCase()+e.objective.slice(1))));
});
