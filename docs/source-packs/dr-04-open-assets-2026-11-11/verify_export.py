"""Read-only DR-04 export verifier, stdlib only; no research code execution."""
from pathlib import Path
import ast,csv,hashlib,json,re
from collections import Counter
from urllib.parse import unquote,urlsplit
R=Path(__file__).resolve().parent
def read(n): return json.loads((R/n).read_text())
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def check(c,m):
 if not c: raise AssertionError(m)
def main():
 m=read('EXPORT-MANIFEST.json');rows=m['entries']
 check(len(rows)==m['source_inventory_count']==64,'source inventory count')
 check(len({x['original_path'] for x in rows})==64,'source path uniqueness')
 included=[x for x in rows if x['disposition']=='included']
 excluded=[x for x in rows if x['disposition']=='excluded']
 for x in included:
  check(digest(R/x['export_path'])==x['export_sha256'],'hash '+x['export_path'])
  check(bool(x['adaptations'])==(x['original_sha256']!=x['export_sha256']),'adaptation disclosure '+x['export_path'])
 for x in excluded:
  check(x['export_path'] is None and x['export_sha256'] is None and x['reason'],'exclusion audit')
 for x in m['generated_files']:check(digest(R/x['path'])==x['sha256'],'generated hash '+x['path'])
 expected={x['export_path'] for x in included}|{x['path'] for x in m['generated_files']}|{'EXPORT-MANIFEST.json','EXPORT-VERIFICATION.json'}
 actual={p.relative_to(R).as_posix() for p in R.rglob('*') if p.is_file()}
 check(actual==expected,'unexpected/missing files '+str(actual^expected))
 links=0
 for rel in sorted(actual):
  p=R/rel;t=p.read_text()
  if p.suffix=='.json':json.loads(t)
  if p.suffix=='.py':ast.parse(t,filename=rel) # syntax only
  # Assembly/checker source mentions no host paths. Public content must remain portable.
  check(('/'+'Volumes/') not in t and ('/'+'Users/') not in t and ('file:'+'///') not in t,'private host path '+rel)
  if p.suffix=='.md':
   for target in re.findall(r'\]\(([^)]+)\)',t):
    target=target.strip('<>')
    if urlsplit(target).scheme or target.startswith('#'):continue
    resolved=(p.parent/unquote(target.split('#')[0])).resolve()
    check(resolved.is_relative_to(R),'link escapes pack '+rel)
    check(resolved.exists(),'broken link '+rel+' => '+target);links+=1
 cat,rec,src,summary=[read(n) for n in ['catalog.json','records.json','sources.json','summary.json']]
 check((len(cat),len(rec),len(src))==(26,22,204),'counts')
 check(sum(x['review_depth']=='DEEP' for x in cat)==10,'deep cards')
 check(Counter(x['ranking'] for x in cat)=={'CORE_CANDIDATE':3,'OPTIONAL':13,'MANUAL_REFERENCE_ONLY':6,'REJECTED':4},'ranks')
 check(Counter(x['read_status'] for x in src)=={'READ':196,'BLOCKED':6,'INDEXED_EXCERPT':2},'access labels')
 check(len({x['url'] for x in src})==194,'unique source locators')
 check(len({x['url'] for x in src if x['url'].startswith(('http:','https:'))})==192,'unique public source URLs')
 check(len([x for x in src if x['url'].startswith('urn:dr04:local-evidence:')])==2,'local observations')
 ids={x['id'] for x in cat};rid={x['id'] for x in rec};sid={x['id'] for x in src}
 check((len(ids),len(rid),len(sid))==(26,22,204),'unique IDs')
 for x in cat:
  check(all(k in x for k in ['provider_eligibility','asset_eligibility','host_readiness']),'three gates')
  check(x['host_readiness']=='NOT_RUN','host overclaim')
  check(set(x['source_ids'])<=sid and set(x['records'])<=rid,'catalog refs')
  check((R/x['card_file']).is_file(),'card path')
 for x in rec:
  check(x['provider'] in ids and x['source_id'] in sid,'record refs')
  check(x['host_readiness']==x['download_verification']==x['decode_verification']=='NOT_RUN' and x['sha256'] is None,'record evidence')
 for n,data in [('catalog.csv',cat),('sources.csv',src)]:
  with (R/n).open(newline='') as f:csvrows=list(csv.DictReader(f))
  check(len(csvrows)==len(data),'CSV length')
  for observed,expectedrow in zip(csvrows,data):
   for k,v in observed.items():
    e=expectedrow.get(k,'');e=json.dumps(e,ensure_ascii=False,sort_keys=True) if isinstance(e,(dict,list)) else str(e)
    check(v==e,'CSV mismatch '+n+'/'+k)
 check(summary['provider_product_tests']=='NOT_RUN' and summary['architecture_acceptance']=='NOT_GRANTED_RESEARCH_HANDOFF','summary limits')
 check(summary['commits']==m['research_baseline_commits'],'baseline pins')
 check(digest(R/'PROMPT.md')=='a6f93b1f72b909d0ead07a1ca5f06f83645361942dec830971348ca282451fe1','prompt changed')
 check(len(read('backlog.json'))==10 and all(x['status']=='NOT_RUN' for x in read('backlog.json')),'backlog')
 check(len(set(re.findall(r'\| (T\d{2}) \|',(R/'TEST_PLAN.md').read_text())))==20,'planned tests')
 check(read('review/review.json')['status']=='PASS_WITH_LIMITATIONS','review')
 check(read('MANIFEST_EXAMPLE.json')['status']=='NOT_RUN','example')
 result={'status':'PASS','scope':'EXPORT_DOCUMENT_INTEGRITY_ONLY','source_inventory':64,'retained_source_files':len(included),'excluded_backups':len(excluded),'adapted_source_files':sum(bool(x['adaptations']) for x in included),'providers':26,'deep_cards':10,'metadata_records':22,'source_entries':204,'unique_source_locators':194,'unique_http_urls':192,'nonpublic_local_evidence':2,'relative_links_checked':links,'broken_relative_links':0,'external_links_rechecked':False,'provider_product_tests':'NOT_RUN','native_runtime_tests':'NOT_RUN','preserved_research_helpers_executed':False,'source_preservation':'Verified separately by publisher export receipt; unavailable from portable pack alone'}
 print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()

