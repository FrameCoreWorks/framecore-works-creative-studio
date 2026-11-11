"""Read-only public transport checks; DOES NOT establish source content or truth."""
import concurrent.futures, json, urllib.request, urllib.error
from pathlib import Path
from datetime import datetime, timezone
P=Path(__file__).resolve().parent
rows=json.loads((P/'SOURCE-LEDGER.json').read_text())['sources']
urls=sorted({x['url'] for x in rows})
def check(url):
    req=urllib.request.Request(url, method='HEAD', headers={'User-Agent':'Mozilla/5.0 (DR01 public research link check)'})
    try:
        with urllib.request.urlopen(req, timeout=12) as r:
            return {'url':url,'status':r.status,'final_url':r.url,'method':'HEAD','content_verified':False}
    except urllib.error.HTTPError as e:
        return {'url':url,'status':e.code,'final_url':e.url,'method':'HEAD','content_verified':False}
    except Exception as e:
        return {'url':url,'status':'ERROR','error':str(e)[:200],'method':'HEAD','content_verified':False}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    results=list(pool.map(check,urls))
out={'checked_at_utc':datetime.now(timezone.utc).isoformat(),'scope':'HTTP transport only; source reading evidence lives in source ledger. HEAD errors do not invalidate separately observed reads. No GET large media downloads.','urls':len(urls),'success':sum(isinstance(x['status'],int) and x['status']<400 for x in results),'results':results}
f=P/'LINK-CHECK.json'
if f.exists():
    import shutil
    shutil.copy2(f, f.with_name(f.name+'.bak-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')))
f.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='results'},ensure_ascii=False))
print(json.dumps([x for x in results if not(isinstance(x['status'],int) and x['status']<400)],ensure_ascii=False))
