"""Read-only, stdlib-only checks of this portable research edition.
No network, product-code import, renderer or native editor execution.
"""
from pathlib import Path
from collections import Counter
import csv, hashlib, json, re, subprocess, sys

P=Path(__file__).resolve().parent
manifest=json.loads((P/'EXPORT-MANIFEST.json').read_text())
errors=[]
def check(condition, detail):
    if not condition: errors.append(detail)
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
rows=manifest['source_files']
copied=[x for x in rows if x['disposition']=='EXPORTED']
check(len(rows)==manifest['source_file_count'],'source inventory count')
check(len({x['source_relative_path'] for x in rows})==len(rows),'source inventory unique')
check(len(copied)==manifest['exported_source_file_count'],'exported source count')
check(len(rows)-len(copied)==manifest['excluded_source_file_count'],'exclusion count')
expected={'EXPORT-MANIFEST.json','PORTABLE-VERIFICATION.json'}
for row in copied:
    rel=row['export_relative_path'];f=P/rel;expected.add(rel)
    check(f.is_file(),'missing '+rel)
    if not f.is_file(): continue
    check(digest(f)==row['exported_sha256'],'hash '+rel)
    if not row['adaptations']: check(digest(f)==row['original_sha256'],'unchanged bytes '+rel)
    check(sorted(set(re.findall(r'\b[0-9a-f]{40}\b',f.read_text())))==row['original_40hex_pins'],'preserved pins '+rel)
for row in manifest['generated_files']:
    f=P/row['path'];expected.add(row['path'])
    check(f.is_file(),'missing generated '+row['path'])
    if f.is_file(): check(digest(f)==row['sha256'],'generated hash '+row['path'])
actual={f.relative_to(P).as_posix() for f in P.rglob('*') if f.is_file()}
check(not(actual-expected),'unlisted files '+str(sorted(actual-expected)))
check(not(expected-actual-{'PORTABLE-VERIFICATION.json'}),'missing manifest files')
links=0
for rel in sorted(actual):
    f=P/rel;text=f.read_text()
    # The detector itself contains these strings, not private host identities.
    if rel!='verify_portable.py':
        check(not re.search(r'/Volumes/|/private/|/Users/|file:///|/Library/Application',text),'private absolute path '+rel)
    if f.suffix=='.json':
        try: json.loads(text)
        except Exception as exc: errors.append('invalid JSON '+rel+': '+str(exc))
    if f.suffix!='.md': continue
    for target in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)',text):
        target=target.strip('<>')
        if re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:',target): continue
        target=target.split('#')[0]
        if not target: continue
        links+=1;dest=f.parent/target
        check(dest.is_file(),'broken link '+rel+' -> '+target)
ledger=json.loads((P/'SOURCE-LEDGER.json').read_text())
with (P/'SOURCE-LEDGER.csv').open(newline='') as handle: csv_rows=list(csv.DictReader(handle))
check(len(ledger)==88 and len(csv_rows)==88,'88 source records JSON/CSV')
check(len({s['url'] for s in ledger})==86,'86 distinct recorded addresses')
check(sum(s['url'].startswith('urn:dr02:local-evidence:') for s in ledger)==1,'one labelled local source')
for left,right in zip(ledger,csv_rows):
    for key,value in right.items():
        wanted=left.get(key,'')
        if isinstance(wanted,(list,dict)): wanted=json.dumps(wanted,ensure_ascii=False)
        if wanted is None: wanted=''
        check(str(wanted)==value,'JSON/CSV agreement '+left['id']+' '+key)
availability=json.loads((P/'LINK-CHECK.json').read_text())['results']
counts=Counter(x['status'] for x in availability)
check(counts=={'HTTP_OK':81,'HTTP_ERROR':6,'LOCAL_OR_NON_HTTP':1},'historical availability counts')
check(all(x['http_status']==403 for x in availability if x['status']=='HTTP_ERROR'),'six HTTP403 retained')
check({x['id'] for x in availability if x['status']=='HTTP_ERROR'}=={'C07','C09','C10','C11','N11','N12'},'HTTP403 identities retained')
check(digest(P/'PROMPT.md')=='8b00ad1f655ffefbf27a626d3f00d762042b06fe546c5d60c79400a25a1f2a7d','original prompt hash')
original=next(x for x in copied if x['source_relative_path']=='verify_research.py')
check(not original['adaptations'] and digest(P/'verify_research.py')==original['original_sha256'],'original verifier unchanged')
author_result=None
if not errors:
    proc=subprocess.run([sys.executable,'-B',str(P/'verify_research.py')],cwd=P,text=True,capture_output=True,timeout=60)
    check(proc.returncode==0,'original research verifier exit '+str(proc.returncode))
    try: author_result=json.loads(proc.stdout)
    except Exception: errors.append('author verifier non-JSON output: '+proc.stdout[-2000:])
    if author_result: check(author_result.get('status')=='PASS','author verifier result')
    if proc.stderr: errors.append('author verifier stderr: '+proc.stderr[-1000:])
result={'status':'PASS' if not errors else 'FAIL','scope':'Portable inventory/hash/link/privacy/pin checks plus unmodified original structure/restricted-shape/arithmetic verifier. No native, runtime, render, viewing or listening test.',
    'source_file_inventory':len(rows),'exported_source_files':len(copied),'excluded_source_files':len(rows)-len(copied),
    'generated_files_hashed':len(manifest['generated_files']),'actual_package_files':len(actual),'local_links_checked':links,
    'original_research_verifier':author_result,'historical_gate_replayed':False,'errors':errors}
print(json.dumps(result,ensure_ascii=False,indent=2))
sys.exit(bool(errors))
