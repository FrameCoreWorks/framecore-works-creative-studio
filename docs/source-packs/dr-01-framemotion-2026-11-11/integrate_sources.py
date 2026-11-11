"""Normalize source records without turning transport checks into reading evidence."""
import csv,json,shutil
from pathlib import Path
from urllib.parse import urlsplit,urlunsplit
from datetime import datetime,timezone
P=Path(__file__).resolve().parent
rows=[]
for rel in ['HOST-SOURCES.json','specialists/craft/sources.json','specialists/recipes/sources.json','specialists/backends/sources.json']:
    data=json.loads((P/rel).read_text()); data=data if isinstance(data,list) else data['sources']
    for source in data:
        item=dict(source);item['origin_ledger']=rel;item['raw_used_in']=item['used_in']
        item['label']='PRACTITIONER' if item['id'] in ['R-S14','R-S15','R-S16','R-S17'] else 'SOURCED'
        if 'recipes' in rel:
            item['used_in']=['specialists/recipes/RECIPES.md','specialists/recipes/PROCESS-AND-TUTORIALS.md']
        else:
            item['used_in']=sorted({str(Path(rel).parent/f.split(':')[0]) for f in item['used_in']})
        item['published_date']=item.get('published_date') or 'Unknown'
        u=urlsplit(item['url']);path=u.path.rstrip('/')
        if u.netloc=='www.w3.org' and path in ['/TR/css-font-loading','/TR/css-font-loading-3']:path='/TR/css-font-loading'
        item['canonical_source_url']=urlunsplit((u.scheme,u.netloc,path,u.query,''))
        rows.append(item)
# Group known Adobe legacy and desktop aliases by identical document basename.
adobe={}
for item in rows:
    u=urlsplit(item['url'])
    if u.netloc=='helpx.adobe.com':
        key=u.path.split('/')[-1]
        adobe.setdefault(key,item['canonical_source_url'])
        item['canonical_source_url']=adobe[key]
assert len({x['id'] for x in rows})==len(rows)
units={}
for item in rows:units.setdefault(item['canonical_source_url'],[]).append(item['id'])
ledger={'research_id':'DR-01','date':'2026-11-11','method':'Actually opened primary/author documents and source files. Source units group duplicate URLs, fragments, known W3C and Adobe legacy aliases; units are not independent confirmations. Source metadata retained. HEAD check only tests transport.','source_records':len(rows),'unique_urls':len({x['url'] for x in rows}),'unique_canonical_urls':len(units),'duplicate_groups':{k:v for k,v in units.items() if len(v)>1},'sources':rows}
stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
for name in ['SOURCE-LEDGER.json','SOURCE-LEDGER.csv']:
    path=P/name
    if path.exists():shutil.copy2(path,path.with_name(name+'.bak-'+stamp))
(P/'SOURCE-LEDGER.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
fields=['id','title','url','canonical_source_url','author','published_date','accessed','version','locator','inspection','label','claim','decision','limitation','test','rights','evidence','used_in','origin_ledger']
with (P/'SOURCE-LEDGER.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
    for x in rows:w.writerow({k:json.dumps(x.get(k),ensure_ascii=False) if isinstance(x.get(k),(dict,list)) else x.get(k,'Unknown') for k in fields})
print(json.dumps({k:v for k,v in ledger.items() if k!='sources'},ensure_ascii=False))
