import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {fileURLToPath} from 'node:url';
import {spawnSync as spawnFontProbe} from 'node:child_process';
import {validateScore,secondsAtFrame,reviewFrames,cueTimes,renderPaperFrame,renderToneCues} from '../skills/hyperframes-workflow/assets/motion-quality/score.mjs';
import {loadLibrary,searchLibrary,presentEntry,validateLibrary,loadBriefIndex,matchBrief,presentBrief,validateBriefIndex,loadSnippets,validateSnippets,snippetContract,galleryShortlist} from '../skills/hyperframes-workflow/assets/motion-prompt-library/library.mjs';
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
const OPUS_COMMIT='92aee2f586ac0715cb3cbcb6384834f98a33383d';
test('the Opus gallery is complete, link-only and pinned, with a Studio note per record',()=>{
  const entries=loadLibrary(),gallery=entries.filter(e=>e.file==='specimen-opus-gallery.json'),briefs=new Set(loadBriefIndex().briefs.map(b=>b.id));
  assert.equal(gallery.length,703);
  for (const e of gallery) {
    assert.equal(e.prompt_origin,'creator_prompt_link_only',e.id);assert.equal(e.prompt_text,null,e.id);
    assert.ok(e.prompt_source_url.startsWith('https://github.com/yihui-dev/awesome-opus5-5-videos/blob/'+OPUS_COMMIT+'/prompts/'),e.id);
    assert.ok(typeof e.mechanism==='string'&&e.mechanism.length>=30,e.id);
    assert.ok(e.brief_types.every(b=>briefs.has(b)),e.id);
  }
  assert.equal(gallery.filter(e=>e.category==='interactive').every(e=>!e.default_motion_search),true);
  assert.ok(gallery.filter(e=>e.caution).length>=3);
});
test('gallery records reach briefs as technique, at most three, never as originals',()=>{
  const entries=loadLibrary(),index=loadBriefIndex();
  const view=presentBrief(index.briefs.find(b=>b.id==='tech-explainer'),entries);
  assert.ok(view.gallery.length>0&&view.gallery.length<=3);
  assert.ok(view.gallery.every(g=>g.id.startsWith('OPUS-')&&g.mechanism&&g.source&&g.prompt_source));
  assert.match(view.authority,/selects no runtime/);
  const shown=presentEntry(entries.find(e=>e.id===view.gallery[0].id));
  assert.ok(shown.mechanism&&shown.prompt_source);assert.equal(shown.prompt,null);
  assert.ok(searchLibrary(entries,'cocktail recipe',{limit:5}).some(e=>e.id.startsWith('OPUS-')));
});
test('tampered gallery records fail validation',()=>{
  const entries=loadLibrary(),e=structuredClone(entries.find(x=>x.file==='specimen-opus-gallery.json'));
  e.mechanism='';e.prompt_source_url='https://github.com/yihui-dev/awesome-opus5-5-videos/blob/main/prompts/x.md';e.brief_types=['no-such-brief'];
  const errors=[...validateLibrary([e]),...validateBriefIndex(loadBriefIndex(),[...entries,{...e,id:'OPUS-copy'}])].join('\n');
  assert.match(errors,/mechanism/);assert.match(errors,/pinned/);assert.match(errors,/unknown brief type no-such-brief/);
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
test('brief tags name scene kinds that the linked contract shows',()=>{
  const entries=loadLibrary(),index=structuredClone(loadBriefIndex());
  assert.equal(presentBrief(index.briefs.find(b=>b.id==='quote-testimonial'),entries).contract,'motion-scenes/templates/ad-testimonial.motion-score.json');
  assert.ok(index.briefs.filter(b=>b.contract).length>=12);
  index.briefs[0].scene_kinds=['bar-chart'];index.briefs[1].scene_kinds=['quote'];index.briefs[1].contract=null;index.briefs[2].contract='../secret.json';
  const errors=validateBriefIndex(index,entries).join('\n');
  assert.match(errors,/has no bar-chart scene/);assert.match(errors,/need a contract/);assert.match(errors,/contract must be null/);
});
const arialLike=(()=>{const {spawnSync}={spawnSync:spawnFontProbe};const dir=fileURLToPath(new URL('../skills/hyperframes-workflow/assets/motion-render/',import.meta.url));const out=spawnSync('python3',['-B','-c',"import sys;sys.path.insert(0,sys.argv[1]);import render as r;f=r.font_files();print(any(r.find_font(n,False,f) for n in ('Arial','LiberationSans','Arimo','Helvetica')))",dir],{encoding:'utf8'});return out.stdout?.trim()==='True';})();
const ARIAL_SKIP=!arialLike&&'no Arial or metric-compatible font (Liberation Sans, Arimo): these examples are laid out for Arial';
test('twenty runnable snippets build complete storyboards that the renderer draws without cropping',{skip:ARIAL_SKIP},async()=>{
  const os=await import('node:os'),path=await import('node:path'),{spawnSync}=await import('node:child_process');
  const {checkScore}=await import('../skills/remotion-video-production/assets/kinetic-type-starter/check-score.mjs');
  const entries=loadLibrary(),file=loadSnippets();
  assert.equal(file.snippets.length,20);
  assert.deepEqual(validateSnippets(file,entries),[]);
  const view=presentBrief(loadBriefIndex().briefs.find(b=>b.id==='social-vertical'),entries,file.snippets);
  assert.equal(view.records.find(r=>r.id==='FC-SOCIAL-02').snippet,'node library.mjs snippet FC-SOCIAL-02');
  const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'snippets-'));
  try {
    const jobs=file.snippets.map(s=>{
      const contract=snippetContract(s,entries);
      assert.deepEqual(checkScore(contract,{storyboard:true}),{errors:[],warnings:[]},s.record);
      const out=path.join(tmp,s.record+'.motion.json');fs.writeFileSync(out,JSON.stringify(contract));
      return [out,contract.scenes.map(sc=>Math.floor((sc.holds[0][0]+sc.holds[0][1])/2)).join(',')];
    });
    if (spawnSync('python3',['-c','import PIL'],{encoding:'utf8'}).status!==0) return;
    const render=fileURLToPath(new URL('../skills/hyperframes-workflow/assets/motion-render/render.py',import.meta.url));
    for (const [out,frames] of jobs) {
      const done=spawnSync('python3',['-B',render,out,'--stills',frames,'--stills-dir',out+'-stills'],{encoding:'utf8'});
      assert.equal(done.status,0,path.basename(out)+': '+done.stderr);
    }
  } finally {fs.rmSync(tmp,{recursive:true,force:true});}
  const bad=structuredClone(file);bad.snippets[0].record='FC-NOPE-01';bad.snippets[1].style='neon';bad.snippets[2].assets_from={x:'../secret.json'};
  const errors=validateSnippets(bad,entries).join('\n');
  assert.match(errors,/existing FrameCore original/);assert.match(errors,/unknown style neon/);assert.match(errors,/must come from examples/);
});
test('original blueprints have record-specific objectives',()=>{
  const originals=loadLibrary().filter(e=>e.prompt_origin==='framecore_original');
  assert.equal(new Set(originals.map(e=>e.objective)).size,originals.length);
  const rewritten=originals.filter(e=>['brand','editorial','product','social','transitions','typography'].includes(e.category));
  assert.equal(rewritten.length,60);
  assert.ok(rewritten.every(e=>e.prompt_text.includes('The purpose is to '+e.objective[0].toLowerCase()+e.objective.slice(1))));
});

test('the gallery shortlist is a small file that matches the gallery and lists records per brief type', () => {
  const entries=loadLibrary(), index=loadBriefIndex();
  const file=new URL('../skills/hyperframes-workflow/assets/motion-prompt-library/opus-gallery-shortlist.md', import.meta.url);
  assert.ok(fs.existsSync(file), 'opus-gallery-shortlist.md is missing');
  const text=fs.readFileSync(file,'utf8');
  assert.equal(text, galleryShortlist(index,entries), 'shortlist is stale: run node library.mjs shortlist --write');
  assert.ok(Buffer.byteLength(text) < 60000, 'shortlist must stay small enough to read in one step');
  assert.match(text, /## tech-explainer/);
  assert.match(text, /OPUS-[a-z0-9-]+/);
  assert.doesNotMatch(text, /prompt_text/);
});
