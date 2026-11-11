#!/usr/bin/env python3
"""Independent read-only checks of research data; writes only review result JSON."""
import hashlib, json, re
from pathlib import Path
from fractions import Fraction
from datetime import datetime, timezone
ROOT=Path(__file__).resolve().parent.parent
results=[]
def check(name, ok, detail):
    results.append({'check':name,'pass':bool(ok),'detail':detail})
def read(p): return json.loads((ROOT/p).read_text())
score=read('examples/motion-score.example.json')
side=read('examples/framemotion-sidecar.example.json')
schema=read('examples/sidecar.schema.json')
check('top_level_schema',set(schema['required'])<=set(side)<=set(schema['properties']),'Research core keys only, not full JSON-Schema production validation')
check('score_byte_hash',hashlib.sha256((ROOT/'examples/motion-score.example.json').read_bytes()).hexdigest()==side['bindings']['score_sha256'],'SHA256 against current score bytes')
for dep in side['dependencies']:
    p=ROOT/'examples'/dep['file']
    check('asset_hash:'+dep['asset_id'],p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==dep['sha256'],str(p.relative_to(ROOT)))
fps=Fraction(score['fps']['num'],score['fps']['den']); a=side['assignment']; n=score['totalFrames']
check('assignment',a['out_frame']-a['in_frame']==a['local_out']-a['local_in']==n and a['local_in']==0,'Global and local durations coincide; output [0,N)')
check('duration_rational',Fraction(n)/fps==Fraction(1001,125),str(Fraction(n)/fps)+' s')
for sample,frame in [(48048,30),(144144,90),(288288,180),(432432,270)]:
    check('audio_frame:'+str(frame),Fraction(sample,48000)*fps==frame,str(sample)+' samples @48kHz')
for scene in score['scenes']:
    check('scene_range:'+scene['id'],0<=scene['start']<scene['end']<=n,'Every hold bounded separately')
    for lo,hi in scene.get('holds',[]): check('hold:'+scene['id'],scene['start']<=lo<hi<=scene['end'],str([lo,hi]))
nodes={x['id']:x for x in side['scene_graph']['nodes']}
check('unique_scene_ids',len(nodes)==len(side['scene_graph']['nodes']),'Distinct IDs')
for x in nodes.values():
    check('parent:'+x['id'],x.get('parent') is None or x['parent'] in nodes,'Parent exists')
    if 'mask_ref' in x: check('mask:'+x['id'],x['mask_ref'] in nodes and x['mask_ref']!=x['id'],'Mask exists, not self')
    if 'font_ref' in x: check('font:'+x['id'],x['font_ref'] in {f['id'] for f in side['fonts']},'Font declaration exists; missing bytes intentionally block production')
    if 'copy_ref' in x: check('copy:'+x['id'],x['copy_ref'] in score['copy'],'Copy key exists')
graph={x['id']:x['depends_on'] for x in side['dependency_graph']}; visiting=set(); done=set()
def visit(x):
    if x in visiting or x not in graph: return False
    if x in done: return True
    visiting.add(x)
    ok=all(visit(d) for d in graph[x]); visiting.remove(x);done.add(x)
    return ok
check('dependency_dag',all(visit(x) for x in graph),'Known dependencies, no cycles')
for c in side['channels']:
    check('channel:'+c['node'],c['node'] in nodes and all(0<=k['frame']<=n for k in c['keys']),'Target and boundary key ranges; no render execution')
check('truthful_missing_inputs',side['qa']['preflight']=='blocked' and side['qa']['native_render']=='NOT_RUN' and not side['accepted_locks'],'Missing font/request/adapter is not a production PASS')
gloss=(ROOT/'specialists/craft/GLOSSARY.md').read_text();recipes=(ROOT/'specialists/recipes/RECIPES.md').read_text()
check('100_glossary_terms',len(re.findall(r'^\| \d+ \|',gloss,re.M))==100,'Numbered rows')
sections=re.split(r'^## (R\d{2}) —',recipes,flags=re.M)
check('18_recipes',len(sections[1::2])==18,'R01–R18')
for rid,body in zip(sections[1::2],sections[2::2]):
    labels=['Problem i cel','Użyj / nie używaj','Assety','Budowa referencyjna','Parametry','Operacje','Błąd → naprawa','Kod','QA','Źród']
    check('recipe_fields:'+rid,all(k in body for k in labels),'Ten substantive fields including sources')
ledger=read('SOURCE-LEDGER.json'); sources=ledger['sources']
check('source_record_count',ledger['source_records']==len(sources),str(len(sources)))
check('source_ids_unique',len({s['id'] for s in sources})==len(sources),'No ambiguous IDs')
missing=[]; uncited=[]
for s in sources:
    texts=[]
    for f in s['used_in']:
        p=ROOT/f
        if not p.exists(): missing.append((s['id'],f))
        else: texts.append(p.read_text())
    if not any(re.search(r'(?<![A-Za-z0-9-])'+re.escape(s['id'])+r'(?![A-Za-z0-9-])',t) or s['url'] in t for t in texts): uncited.append(s['id'])
check('used_in_paths_exist',not missing,missing)
check('source_visible_citations',not uncited,uncited)
value_sources={s.get('canonical_source_url',s['url']) for s in sources if s['id'] not in uncited}
check('source_goal_40',len(value_sources)>=40,{'cited_url_groups':len(value_sources),'note':'Citation/URL test does not prove independent sources or exhaustive source accuracy'})
for f in ['README.md','COMPREHENSIVE-REPORT.md','COVERAGE-MATRIX.md','CODE-AND-CONTRACTS.md','QA-BENCHMARKS.md','PROFESSIONAL-WORKFLOWS.md','IMPLEMENTATION_HANDOFF.md','SOURCE-LEDGER.csv','specialists/backends/REPOSITORIES.md']:
    check('package_file:'+f,(ROOT/f).is_file(),'Required integrated artifact')
out={'date':datetime.now(timezone.utc).isoformat(),'scope':'Research structure, references, hashes, arithmetic only; native render, browser fonts, video and audio NOT_RUN','checks':results,'passed':sum(r['pass'] for r in results),'failed':sum(not r['pass'] for r in results)}
Path(__file__).with_name('INDEPENDENT-CHECKS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'passed':out['passed'],'failed':out['failed'],'failures':[r for r in results if not r['pass']]},ensure_ascii=False))
