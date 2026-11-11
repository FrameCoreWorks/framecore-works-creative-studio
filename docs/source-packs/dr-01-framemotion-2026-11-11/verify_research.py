"""Original DR-01 verifier: structure, traceability and analytical fixtures only.
No downloaded code, renderer, native application, video or audio is executed.
"""
from pathlib import Path
from fractions import Fraction
from urllib.parse import urlsplit,unquote
import csv,hashlib,json,math,re,sys
P=Path(__file__).resolve().parent
DRAFT='--draft' in sys.argv
checks=[]
def check(name,condition,detail=''):
    checks.append({'check':name,'status':'PASS' if condition else 'FAIL','detail':detail})
def read(name):return (P/name).read_text()
required=['PROMPT.md','SCOPE-CLARIFICATION.md','PLAN.md','README.md','COMPREHENSIVE-REPORT.md','CODE-AND-CONTRACTS.md','PROFESSIONAL-WORKFLOWS.md','QA-BENCHMARKS.md','COVERAGE-MATRIX.md','IMPLEMENTATION_HANDOFF.md','SOURCE-LEDGER.json','SOURCE-LEDGER.csv','LINK-CHECK.json','examples/motion-score.example.json','examples/framemotion-sidecar.example.json','examples/sidecar.schema.json','specialists/craft/CRAFT.md','specialists/craft/GLOSSARY.md','specialists/recipes/RECIPES.md','specialists/recipes/PROCESS-AND-TUTORIALS.md','specialists/backends/STUDIO-AUDIT.md','specialists/backends/BACKENDS.md','specialists/backends/REPOSITORIES.md']
if not DRAFT:required+=['REVIEW.md','review/INDEPENDENT-REVIEW.md','review/findings.json']
check('required_artifacts',all((P/x).is_file() and (P/x).stat().st_size>0 for x in required),str([x for x in required if not(P/x).exists()]))
check('original_prompt_unchanged',hashlib.sha256((P/'PROMPT.md').read_bytes()).hexdigest()=='e3aaf7f2d78bc178a396a2d7ba26bc6a55f9609243a7582990c27eeb9b27dc3d')
terms=[int(x) for x in re.findall(r'^\|\s*(\d+)\s*\|',read('specialists/craft/GLOSSARY.md'),re.M)]
check('100_ordered_glossary_entries',terms==list(range(1,101)))
recipes=read('specialists/recipes/RECIPES.md')
parts=re.split(r'^## (R\d{2})[^\n]*\n',recipes,flags=re.M)
check('18_ordered_recipes',parts[1::2]==['R%02d'%n for n in range(1,19)])
fields=['Problem i cel','Użyj / nie używaj','Assety','Budowa referencyjna','Parametry','Operacje','Błąd → naprawa','Kod','QA','Źród']
missing=[(rid,field) for rid,body in zip(parts[1::2],parts[2::2]) for field in fields if field not in body]
check('all_recipe_fields',not missing,str(missing))
benchmarks=re.findall(r'^## B(\d{2})',read('QA-BENCHMARKS.md'),re.M)
check('5_benchmarks',benchmarks==['01','02','03','04','05'])
benchparts=re.split(r'^## B\d{2}[^\n]*\n',read('QA-BENCHMARKS.md'),flags=re.M)[1:]
check('both_aspect_ratios_each_benchmark',all('16:9' in x and '9:16' in x for x in benchparts))
ledger=json.loads(read('SOURCE-LEDGER.json'));sources=ledger['sources'];ids=[x['id'] for x in sources]
check('source_unique_ids',len(ids)==len(set(ids)))
check('source_counts_honest',ledger['source_records']==len(sources) and ledger['unique_urls']==len({x['url'] for x in sources}) and ledger['unique_canonical_urls']==len({x['canonical_source_url'] for x in sources}))
check('source_goal_40_met',ledger['unique_canonical_urls']>=40,'Count is not itself evidence of quality; independent review required.')
needed=['title','url','author','published_date','accessed','version','locator','inspection','claim','decision','limitation','test','rights','evidence','used_in']
check('source_metadata',all(all(x.get(k) for k in needed) for x in sources))
unused=[]
for x in sources:
    evidence='\n'.join(read(f) for f in x['used_in'] if (P/f).exists())
    # IDs in bracket links or narrative are the audit trail; no claim of content truth.
    if not re.search(r'(?<![A-Z0-9-])'+re.escape(x['id'])+r'(?![0-9])',evidence):unused.append(x['id'])
check('sources_cited_in_declared_deliverables',not unused,str(unused))
with (P/'SOURCE-LEDGER.csv').open(newline='') as f:csvrows=list(csv.DictReader(f))
check('CSV_JSON_consistent',len(csvrows)==len(sources) and [x['id'] for x in csvrows]==ids)
links=json.loads(read('LINK-CHECK.json'))
check('all_source_URLs_transport_checked',{x['url'] for x in sources}<={x['url'] for x in links['results']})
check('transport_success_count_honest',links['success']==sum(isinstance(x['status'],int) and x['status']<400 for x in links['results']))
local_bad=[]
mds=[f for f in P.rglob('*.md') if 'backups' not in f.parts]
for f in mds:
    for target in re.findall(r'\]\(([^)]+)\)',f.read_text()):
        t=target.strip('<>').split('#')[0]
        if not t or '://' in t or t.startswith('mailto:'):continue
        if not (f.parent/unquote(t)).exists():local_bad.append((str(f.relative_to(P)),t))
check('local_markdown_links_exist',not local_bad,str(local_bad))
score=json.loads(read('examples/motion-score.example.json'));ext=json.loads(read('examples/framemotion-sidecar.example.json'));schema=json.loads(read('examples/sidecar.schema.json'))
check('core_schema_required_keys',set(schema['required'])==set(ext)==set(schema['properties']))
check('example_explicitly_not_approved',score['approval']['status']=='example-not-client-approved' and ext['provenance']['client_approval'] is False and ext['qa']['preflight']=='blocked' and ext['accepted_locks']==[])
check('native_proof_NOT_RUN',all(ext['qa'][k]=='NOT_RUN' for k in ['native_render','realtime_review','listening']))
check('score_hash_binding',hashlib.sha256((P/'examples'/ext['bindings']['score_file']).read_bytes()).hexdigest()==ext['bindings']['score_sha256'])
check('asset_hash_binding',all(hashlib.sha256((P/'examples'/x['file']).read_bytes()).hexdigest()==x['sha256'] for x in ext['dependencies']))
check('missing_font_is_explicit',all(x['availability']=='NOT_PROVIDED' and x['sha256'] is None for x in ext['fonts']))
fps=Fraction(score['fps']['num'],score['fps']['den']);N=score['totalFrames'];a=ext['assignment']
check('global_local_range_parity',a['out_frame']-a['in_frame']==a['local_out']-a['local_in']==N and a['local_in']==0)
check('8_008_seconds_exact',Fraction(N,1)/fps==Fraction(1001,125))
check('exclusive_out_and_adjacency',len(range(a['in_frame'],a['out_frame']))==240 and max(range(a['in_frame'],a['out_frame']))==1139 and not(a['in_frame']<=1140<a['out_frame']))
check('long_sequence_fraction_is_exact',Fraction(108000,1)/fps==Fraction(18018,5))
check('audio_to_visual_impact',all(Fraction(c['sample'],ext['audio']['sample_rate_hz'])*fps==c['local_frame'] and c['animation_start_frame']+c['attack_frames']==c['local_frame'] for c in ext['audio']['cues']))
check('B05_cues',all(Fraction(s,48000)*fps==f for s,f in zip([48048,144144,288288,432432],[30,90,180,270])))
check('shutter_window_25fps180deg',Fraction(180,360)/25==Fraction(1,50) and Fraction(-90,360)/25==Fraction(-1,100))
check('linear_premult_over',tuple(s+d*(1-Fraction(1,2)) for s,d in zip([Fraction(1,2),0,0],[0,0,1]))==(Fraction(1,2),0,Fraction(1,2)))
check('RGBA8_memory_example',1920*1080*4==8294400)
# Constant orientation lateral camera: horizontal image speed is focal_px*vx/depth.
focal=1920/(2*math.tan(math.radians(25)));speeds=[focal*80/(120/float(fps))/z for z in [1000,1200,1400]]
check('B04_lateral_parallax_monotonic',speeds[0]>speeds[1]>speeds[2] and math.isclose(speeds[0]/speeds[2],1.4))
def acyclic(nodes):
    graph={x['id']:x.get('depends_on',[]) for x in nodes};done=set();visiting=set()
    def walk(n):
        if n in visiting:raise ValueError('cycle')
        if n not in graph:raise ValueError('missing node')
        if n in done:return
        visiting.add(n)
        for dep in graph[n]:walk(dep)
        visiting.remove(n);done.add(n)
    try:
        for n in graph:walk(n)
        return True
    except ValueError:return False
check('dependency_graph_DAG',acyclic(ext['dependency_graph']))
check('negative_cycle_rejected',not acyclic([{'id':'a','depends_on':['b']},{'id':'b','depends_on':['a']}]))
nodeids={x['id'] for x in ext['scene_graph']['nodes']};node={x['id']:x for x in ext['scene_graph']['nodes']}
check('scene_refs',all(x.get('parent') is None or x['parent'] in nodeids for x in node.values()) and all(x.get('mask_ref','mask1') in nodeids for x in node.values()))
check('composition_mask_semantics',node['mask1']['renderable'] is False and node['mask1']['space']==node['mark1']['mask_space']=='composition-px')
channel=ext['channels'][0]
check('channel_extrapolation_explicit',channel['extrapolation']=={'before_first':'hold-first','after_last':'hold-last'})
def fixture_value(f):
    keys=channel['keys']
    if f<=keys[0]['frame']:return keys[0]['value']
    if f>=keys[-1]['frame']:return keys[-1]['value']
    # Analytical test only; exact temporal Bezier sampled using inverse x.
    u=(f-keys[0]['frame'])/(keys[-1]['frame']-keys[0]['frame']);x1,y1,x2,y2=keys[0]['ease_to_next']
    def bez(t,a,b):return 3*(1-t)**2*t*a+3*(1-t)*t*t*b+t**3
    lo,hi=0.,1.
    for _ in range(60):
        mid=(lo+hi)/2
        if bez(mid,x1,x2)<u:lo=mid
        else:hi=mid
    q=bez((lo+hi)/2,y1,y2)
    return [a+(b-a)*q for a,b in zip(keys[0]['value'],keys[1]['value'])]
check('frame0_18_30_239_defined',fixture_value(0)==fixture_value(18)==[-200,440] and fixture_value(30)==fixture_value(239)==[960,440])
check('seek_order_invariance_analytical',[fixture_value(f) for f in [0,30,18,239]]==[[-200,440],[960,440],[-200,440],[960,440]])
check('text_visibility_boundary',node['type1']['visibility']=={'in_frame':45,'out_frame':240})
allfiles=[f for f in P.rglob('*') if f.is_file()]
check('Hipson_file_size_limits',all(f.stat().st_size<=16*1024*1024 for f in allfiles) and sum(f.stat().st_size for f in allfiles)<128*1024*1024)
if not DRAFT:
    review=json.loads(read('review/findings.json'))
    resolutions=json.loads(read('review-resolutions.json'))
    unresolved=[x['id'] for x in review['findings'] if x['severity'] in ['blocking','major'] and resolutions.get(x['id'],{}).get('status')!='resolved']
    check('review_findings_resolved',not unresolved,str(unresolved))
    check('independent_review_verdict',review['verdict']=='PASS_WITH_LIMITATIONS')
report={'status':'PASS' if all(x['status']=='PASS' for x in checks) else 'FAIL','scope':'Structure, reference traceability and original analytical fixtures; not renderer execution, visual/audio proof or exhaustive source truth verification.','draft':DRAFT,'checks_passed':sum(x['status']=='PASS' for x in checks),'checks_total':len(checks),'source_records':len(sources),'canonical_source_units':ledger['unique_canonical_urls'],'glossary_entries':len(terms),'recipes':len(parts[1::2]),'benchmarks':len(benchmarks),'checks':checks}
print(json.dumps(report,ensure_ascii=False,indent=2))
sys.exit(0 if report['status']=='PASS' else 1)
