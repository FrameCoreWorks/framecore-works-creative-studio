"""Read-only DR-03 export validation; no candidate execution or network."""
from pathlib import Path
from urllib.parse import unquote,urlsplit
from collections import Counter
import csv,hashlib,json,re,sys
P=Path(__file__).resolve().parent
checks=[]
def check(name,ok,detail=None):checks.append({"check":name,"status":"PASS" if ok else "FAIL","detail":detail})
def read(n):return json.loads((P/n).read_text(encoding="utf-8"))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=read("EXPORT-MANIFEST.json");rows=m["source_files"]
inc=[r for r in rows if r["disposition"]=="INCLUDED"];exc=[r for r in rows if r["disposition"]=="EXCLUDED"]
check("source_inventory_counts",len(rows)==71 and len(inc)==45 and len(exc)==26)
check("unique_source_paths",len({r["source_relative_path"] for r in rows})==71)
check("excluded_backups_explicit",all(any(s in r["source_relative_path"] for s in (".bak-",".backup-","backups/")) for r in exc))
bad=[]
for r in inc+m["generated_files"]:
    p=P/r["export_relative_path"]
    if not p.is_file() or digest(p)!=r["export_sha256"]:bad.append(r["export_relative_path"])
check("all_export_hashes",not bad,bad)
expected={r["export_relative_path"] for r in inc+m["generated_files"]}|{"EXPORT-MANIFEST.json"}
actual={p.relative_to(P).as_posix() for p in P.rglob("*") if p.is_file()}
check("exact_export_file_closure",actual==expected,{"missing":sorted(expected-actual),"unexpected":sorted(actual-expected)})
check("no_symlinks",not any(p.is_symlink() for p in P.rglob("*")))
pattern=re.compile(r"/(?:Volumes|Users|private|tmp)/|file:/"+r"/|(?:skill|plugin):/"+r"/|\b(?:sk|ghp)-[A-Za-z0-9_]{20,}")
private=[];badjson=[]
for rel in sorted(actual):
    f=P/rel;text=f.read_text(encoding="utf-8")
    if pattern.search(text):private.append(rel)
    if f.suffix==".json":
        try:json.loads(text)
        except ValueError:badjson.append(rel)
check("private_path_and_credential_pattern_scan",not private,private)
check("all_json_parses",not badjson,badjson)
links=0;broken=[]
for f in P.rglob("*.md"):
    for raw in re.findall(r"\]\(([^)]+)\)",f.read_text(encoding="utf-8")):
        t=raw.strip("<>")
        if urlsplit(t).scheme or t.startswith("#"):continue
        t=unquote(t.split("#",1)[0])
        if not t:continue
        links+=1;dest=(f.parent/t).resolve()
        if not dest.is_file() or (P.resolve()!=dest and P.resolve() not in dest.parents):
            broken.append({"file":f.relative_to(P).as_posix(),"target":t})
check("relative_markdown_links",not broken,{"checked":links,"broken":broken})
catalog=read("CATALOG.json");sources=read("SOURCES.json");stats=read("STATISTICS.json")
with (P/"CATALOG.csv").open(encoding="utf-8",newline="") as f:
    reader=csv.DictReader(f);csvrows=list(reader);fields=reader.fieldnames
mismatch=[]
if len(csvrows)!=len(catalog):mismatch.append("count")
for a,b in zip(csvrows,catalog):
    for k in fields:
        want=b.get(k,"N/A")
        if isinstance(want,(list,dict)):
            try:got=json.loads(a[k])
            except ValueError:got=a[k]
        else:got=a[k];want="" if want is None else str(want)
        if want!=got:mismatch.append(a.get("id","?")+":"+k)
check("CSV_JSON_full_exported_fields",not mismatch,mismatch)
check("catalog_statistics",len(catalog)==stats["candidates"]==30 and dict(Counter(c["class"] for c in catalog))==stats["by_class"] and dict(Counter(c["novelty"] for c in catalog))==stats["novelty"])
check("source_statistics",len(sources)==stats["source_records"]==220 and len({s["url"] for s in sources})==stats["unique_source_urls"]==205)
check("deep_dive_statistics",[c["id"] for c in catalog if c.get("deep_dive")]==stats["deep_dives"] and len(stats["deep_dives"])==12)
sids={s["id"] for s in sources}
check("candidate_source_references",all(c["source_ids"] and set(c["source_ids"])<=sids for c in catalog))
check("candidate_card_paths",all((P/c["card_path"]).is_file() for c in catalog))
check("candidate_NOT_RUN_preserved",all(c["execution_status"]=="NOT_RUN" for c in catalog))
review=read("review/REVIEW.json")
check("portable_reviewed_paths",len(review["reviewed_files"])==30 and all(not Path(r).is_absolute() and (P/r).is_file() for r in review["reviewed_files"]))
check("baseline_three_pins",len(read("sources/baseline-inventory.json"))==3 and all(re.fullmatch("[0-9a-f]{40}",r["sha"]) for r in read("sources/baseline-inventory.json")))
fresh=read("EXPORT-VERIFICATION.json")
check("fresh_export_result_labeled",fresh["context"]=="Fresh run on publication export; historical verification remains separate" and fresh["original_verifier_result"]["artifact_integrity"]=="PASS" and fresh["original_verifier_result"]["product_tests"]=="NOT_RUN")
out={"schema":"dr03-export-checks/1","status":"PASS" if all(c["status"]=="PASS" for c in checks) else "FAIL","scope":"Read-only export structure/hash/link/provenance checks; no native, asset or candidate tests and no external source revalidation.","checks_passed":sum(c["status"]=="PASS" for c in checks),"checks_total":len(checks),"export_file_count":len(actual),"manifest_sha256":digest(P/"EXPORT-MANIFEST.json"),"checks":checks}
print(json.dumps(out,ensure_ascii=False,indent=2))
sys.exit(0 if out["status"]=="PASS" else 1)

