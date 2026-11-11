"""Own research ledger aggregation and bounded URL availability check. No providers/code execution."""
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from urllib.parse import urlparse
import json,csv,io,shutil,sys
P=Path(__file__).resolve().parent

def save(name,data):
 f=P/name
 if f.exists():
  b=P/'backups'/datetime.now().strftime('%Y%m%dT%H%M%S%f')/name;b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,b)
 f.write_text(data)

sources=[]
for name in ['ROOT-SOURCES.json','specialists/craft/sources.json','specialists/nle/sources.json','specialists/repo/sources.json']:
 data=json.loads((P/name).read_text());sources.extend(data['sources'] if isinstance(data,dict) else data)
for s in sources:
 s['used_in']={'F':'CODE-AND-CONTRACTS.md','C':'specialists/craft/','N':'specialists/nle/','R':'specialists/repo/'}[s['id'][0]]
save('SOURCE-LEDGER.json',json.dumps(sources,ensure_ascii=False,indent=2)+'\n')
cols=['id','title','url','author','published_date','accessed','version','locator','inspection','evidence_class','claims','decision','counterexample','test','rights','limitations','used_in']
out=io.StringIO();w=csv.DictWriter(out,fieldnames=cols,extrasaction='ignore');w.writeheader()
for s in sources:w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in s.items() if k in cols})
save('SOURCE-LEDGER.csv',out.getvalue())
print('Source records:',len(sources),'unique URLs:',len({s['url'] for s in sources}),flush=True)
if '--links' in sys.argv:
 def link(s):
  url=s['url'];r={'id':s['id'],'url':url,'checked':'2026-11-11','method':'bounded HTTPS GET headers + first256 bytes; no execution'}
  if not url.startswith(('https://','http://')):
   r.update(status='LOCAL_OR_NON_HTTP',note='Local document evidence is recorded by specialist; no web request');return r
  try:
   req=Request(url,headers={'User-Agent':'DR02-research-source-check/1.0','Range':'bytes=0-255'})
   with urlopen(req,timeout=15) as res:
    r.update(status='HTTP_OK',http_status=res.status,final_url=res.url,content_type=res.headers.get('Content-Type'));res.read(256)
  except HTTPError as e:r.update(status='HTTP_ERROR',http_status=e.code,detail=str(e))
  except Exception as e:r.update(status='UNAVAILABLE_NOW',detail=str(e))
  return r
 with ThreadPoolExecutor(max_workers=4) as ex:results=list(ex.map(link,sources))
 save('LINK-CHECK.json',json.dumps({'scope':'availability only; source reading is in ledger. HTTP error is not proof a source never existed. No paid/logged-in access.','results':results},ensure_ascii=False,indent=2)+'\n')
 from collections import Counter
 print(dict(Counter(r['status'] for r in results)),flush=True)
