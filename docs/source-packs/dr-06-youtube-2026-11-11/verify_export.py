"""Read-only DR-06 publication checker; no network, media, or candidate execution."""
from pathlib import Path
from urllib.parse import unquote,urlsplit
import hashlib,json,re,sys
P=Path(__file__).resolve().parent
checks=[]
def check(name,ok,detail=None):checks.append({'check':name,'status':'PASS' if ok else 'FAIL','detail':detail})
def read(n):return json.loads((P/n).read_text(encoding='utf-8'))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=read('EXPORT-MANIFEST.json');rows=m['source_files']
inc=[r for r in rows if r['disposition']=='INCLUDED'];exc=[r for r in rows if r['disposition']=='EXCLUDED']
check('source_inventory_counts',len(rows)==74 and len(inc)==38 and len(exc)==36)
check('unique_source_paths',len({r['source_relative_path'] for r in rows})==74)
check('excluded_backups_explicit',all('.backup' in r['source_relative_path'] or '.bak-' in r['source_relative_path'] or 'backups/' in r['source_relative_path'] for r in exc))
check('all_retained_bytes_unchanged',all(r['original_sha256']==r['export_sha256'] and r['original_bytes']==r['export_bytes'] for r in inc))
bad=[]
for r in inc+m['generated_files']:
    p=P/r['export_relative_path']
    if not p.is_file() or digest(p)!=r['export_sha256']:bad.append(r['export_relative_path'])
check('all_export_hashes',not bad,bad)
expected={r['export_relative_path'] for r in inc+m['generated_files']}|{'EXPORT-MANIFEST.json'}
actual={p.relative_to(P).as_posix() for p in P.rglob('*') if p.is_file()}
check('exact_export_file_closure',actual==expected,{'missing':sorted(expected-actual),'unexpected':sorted(actual-expected)})
check('no_symlinks',not any(p.is_symlink() for p in P.rglob('*')))
pattern=re.compile(r'/(?:Volumes|Users|private|tmp)/|file:/'+r'/|(?:skill|plugin):/'+r'/|\b(?:sk|ghp)-[A-Za-z0-9_]{20,}')
private=[];badjson=[]
for rel in sorted(actual):
    f=P/rel;t=f.read_text(encoding='utf-8')
    if pattern.search(t):private.append(rel)
    if f.suffix=='.json':
        try:json.loads(t)
        except ValueError:badjson.append(rel)
check('private_path_and_credential_pattern_scan',not private,private)
check('all_json_parses',not badjson,badjson)
links=0;broken=[]
for f in P.rglob('*.md'):
    for raw in re.findall(r'\]\(([^)]+)\)',f.read_text(encoding='utf-8')):
        t=raw.strip('<>')
        if urlsplit(t).scheme or t.startswith('#'):continue
        t=unquote(t.split('#',1)[0])
        if not t:continue
        links+=1;dest=(f.parent/t).resolve()
        if not dest.is_file() or P.resolve() not in dest.parents:broken.append({'file':f.relative_to(P).as_posix(),'target':t})
check('relative_markdown_links',not broken,{'checked':links,'broken':broken})
check('original_prompt_digest',digest(P/'PROMPT.md')==(P/'PROMPT.sha256').read_text().strip())
stats=read('EVIDENCE_STATS.json')
check('viewing_scope_preserved',stats['sampled_frame_films']==11 and stats['transcripts_exported']==7 and stats['fully_watched']==0 and stats['audio_listened']==0)
benches=read('benchmarks.json')
check('all_five_benchmarks_NOT_RUN',len(benches)==5 and all(x['status']=='NOT_RUN' and x['actual_result'] is None for x in benches))
repos=read('baseline/repositories.json')
check('baseline_exact_research_pins',[r['head_sha'] for r in repos]==['de4c70fb3f372492b75f50ae831cfd7973de8bf7','adc8094f8e087889e4337c99dd0d267ae1b11a51','889471fcdbc2216ddc465715eff0e82784d5b8ee'])
review=read('review/review.json')
check('historical_review_scope_preserved',review['status']=='pass_with_limitations' and bool(review['limitations']) and review['scope']['full_request_coverage'].startswith('partial:'))
fresh=read('EXPORT-VERIFICATION.json');result=fresh['original_verifier_result']
check('fresh_export_result_labeled',fresh['context']=='Fresh run on publication export; historical verification remains separate' and result['verification']=='PASS' and result['runtime_benchmarks']=='NOT_RUN' and result['full_watches']==0 and result['audio_listens']==0 and not result['errors'])
out={'schema':'dr06-export-checks/1','status':'PASS' if all(c['status']=='PASS' for c in checks) else 'FAIL','scope':'Read-only export hashes/closure/links/evidence labels; no native or audiovisual tests or source revalidation.','checks_passed':sum(c['status']=='PASS' for c in checks),'checks_total':len(checks),'export_file_count':len(actual),'manifest_sha256':digest(P/'EXPORT-MANIFEST.json'),'checks':checks}
print(json.dumps(out,ensure_ascii=False,indent=2));sys.exit(0 if out['status']=='PASS' else 1)
