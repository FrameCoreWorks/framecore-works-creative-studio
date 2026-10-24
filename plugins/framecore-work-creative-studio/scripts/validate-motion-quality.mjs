import fs from 'node:fs';
import path from 'node:path';
// Read data only. Never import or execute a bundled prompt or example renderer.
export function validateMotionQuality(root) {
  const errors=[],dir=path.join(root,'skills/hyperframes-workflow/assets/motion-prompt-library');
  const fail=detail=>errors.push({code:'MOTION_LIBRARY',detail});
  try {
    const files=fs.readdirSync(dir).filter(f=>/^(original|specimen)-[a-z-]+\.json$/.test(f));
    const ids=new Set(),prompts=new Set(),originals=new Map(),objectives=new Set();
    for(const file of files){
      const data=JSON.parse(fs.readFileSync(path.join(dir,file),'utf8'));
      if(data.schema_version!==1||!Array.isArray(data.entries)||!data.entries.length){fail(file+': invalid schema');continue;}
      for(const e of data.entries){
        if(!e.id||ids.has(e.id))fail(file+': duplicate/missing ID');ids.add(e.id);
        // A mixed shard (the Opus gallery) names each record's category from a fixed set.
        const categoryOk=data.category==='mixed'?['motion','explainers','3d','interactive'].includes(e.category):e.category===data.category;
        if(!categoryOk||!e.title||!e.rights||!e.verification)fail(e.id+': incomplete provenance');
        if(String(e.id).startsWith('OPUS-')&&(typeof e.mechanism!=='string'||e.mechanism.length<30||!String(e.prompt_source_url).includes('/blob/'+e.upstream_commit+'/')))fail(e.id+': gallery record needs a mechanism note and a pinned prompt URL');
        if(file.startsWith('original-')){
          if(e.prompt_origin!=='framecore_original'||e.verification!=='not_run')fail(e.id+': original evidence boundary');
          for(const k of ['beats','acceptance','inputs','tags','avoid'])if(!Array.isArray(e[k])||!e[k].length)fail(e.id+': missing '+k);
          originals.set(e.id,e);if(!e.objective||objectives.has(e.objective))fail(e.id+': objective must be record-specific');objectives.add(e.objective);
        }else{
          if(!['curator_reconstruction','creator_prompt_link_only'].includes(e.prompt_origin))fail(e.id+': invalid source kind');
          if(!/^[a-f0-9]{40}$/.test(e.upstream_commit||''))fail(e.id+': missing source pin');
          if(e.verification!=='curator_reported_video_exists; not reproduced by Studio')fail(e.id+': unsupported verification claim');
          for(const k of ['source_url','prompt_source_url']){try{if(new URL(e[k]).protocol!=='https:')fail(e.id+': non-HTTPS source');}catch{fail(e.id+': invalid URL');}}
        }
        if(e.prompt_origin==='creator_prompt_link_only'){if(e.prompt_text!==null)fail(e.id+': creator prompt redistribution');}
        else{
          if(typeof e.prompt_text!=='string'||e.prompt_text.length<80)fail(e.id+': empty prompt');
          const key=String(e.prompt_text).toLowerCase().replace(/\s+/g,' ').trim();
          if(prompts.has(key))fail(e.id+': duplicate prompt');prompts.add(key);
        }
      }
    }
    for(const category of ['brand','typography','product','data','explainers','editorial','education','audio','procedural','transitions','spatial','social'])if(!files.includes('original-'+category+'.json'))fail('Missing original family: '+category);
    for(const category of ['motion','launch','explainers','films','interactive'])if(!files.includes('specimen-'+category+'.json'))fail('Missing source family: '+category);
    // Brief index: curated brief types must point to existing FrameCore originals.
    const index=JSON.parse(fs.readFileSync(path.join(dir,'brief-index.json'),'utf8')),briefIds=new Set();
    if(index.schema_version!==1||!Array.isArray(index.briefs)||index.briefs.length<10)fail('brief-index.json: invalid schema');
    for(const b of index.briefs||[]){
      if(!/^[a-z0-9-]+$/.test(b.id||'')||briefIds.has(b.id))fail('brief '+b.id+': missing or duplicate id');briefIds.add(b.id);
      if(!Array.isArray(b.aliases)||b.aliases.length<3||!b.label||!b.use||!b.avoid||!['kinetic-type-starter','gsap-motion-starter'].includes(b.starter))fail('brief '+b.id+': incomplete');
      if(!Array.isArray(b.records)||b.records.length<2||b.records.length>4||new Set(b.records).size!==b.records.length)fail('brief '+b.id+': needs two to four distinct records');
      for(const id of b.records||[])if(!originals.has(id))fail('brief '+b.id+': '+id+' is not a FrameCore original');
    }
  }catch(error){fail(error.message);}
  return errors;
}
