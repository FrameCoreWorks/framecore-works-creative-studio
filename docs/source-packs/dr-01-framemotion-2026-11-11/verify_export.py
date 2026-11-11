"""Read-only DR-01 export validation. No network, applications or downloaded code."""
from pathlib import Path
from fractions import Fraction
from urllib.parse import unquote, urlsplit
import csv, hashlib, json, re, sys
P=Path(__file__).resolve().parent
checks=[]
def check(name,ok,detail=None):
    checks.append({"check":name,"status":"PASS" if ok else "FAIL","detail":detail})
def read(name):return json.loads((P/name).read_text(encoding="utf-8"))
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
m=read("EXPORT-MANIFEST.json")
rows=m["source_files"]
included=[x for x in rows if x["disposition"]=="INCLUDED"]
excluded=[x for x in rows if x["disposition"]=="EXCLUDED"]
check("source_inventory_counts",len(rows)==74 and len(included)==47 and len(excluded)==27)
check("unique_source_paths",len({x["source_relative_path"] for x in rows})==len(rows))
check("excluded_backups_explicit",all(".bak-" in x["source_relative_path"] or "/backups/" in x["source_relative_path"] for x in excluded))
bad=[]
for row in included:
    f=P/row["export_relative_path"]
    if not f.is_file() or digest(f)!=row["export_sha256"]:bad.append(row["export_relative_path"])
check("retained_file_hashes",not bad,bad)
bad=[]
for row in m["generated_files"]:
    f=P/row["export_relative_path"]
    if not f.is_file() or digest(f)!=row["export_sha256"]:bad.append(row["export_relative_path"])
check("generated_file_hashes",not bad,bad)
expected={x["export_relative_path"] for x in included+m["generated_files"]}|{"EXPORT-MANIFEST.json"}
actual={x.relative_to(P).as_posix() for x in P.rglob("*") if x.is_file()}
check("exact_export_file_closure",expected==actual,{"missing":sorted(expected-actual),"unexpected":sorted(actual-expected)})
check("no_symlinks",not any(x.is_symlink() for x in P.rglob("*")))
pattern=re.compile(r"/(?:Volumes|Users|private|tmp)/|file:/"+r"/|(?:skill|plugin):/"+r"/|\b(?:sk|ghp)-[A-Za-z0-9_]{20,}")
private=[]
json_bad=[]
for rel in sorted(actual):
    f=P/rel
    text=f.read_text(encoding="utf-8")
    if pattern.search(text):private.append(rel)
    if f.suffix==".json":
        try:json.loads(text)
        except ValueError:json_bad.append(rel)
check("private_path_and_credential_pattern_scan",not private,private)
check("all_json_parses",not json_bad,json_bad)
bad_links=[];link_count=0
for f in P.rglob("*.md"):
    for raw in re.findall(r"\]\(([^)]+)\)",f.read_text(encoding="utf-8")):
        target=raw.strip("<>")
        if urlsplit(target).scheme or target.startswith("#"):continue
        target=unquote(target.split("#",1)[0])
        if not target:continue
        link_count+=1
        dest=(f.parent/target).resolve()
        if not dest.is_file() or (P.resolve()!=dest and P.resolve() not in dest.parents):
            bad_links.append({"file":f.relative_to(P).as_posix(),"target":target})
check("relative_markdown_links",not bad_links,{"checked":link_count,"broken":bad_links})
ledger=read("SOURCE-LEDGER.json");sources=ledger["sources"]
with (P/"SOURCE-LEDGER.csv").open(encoding="utf-8",newline="") as f:
    reader=csv.DictReader(f);csvrows=list(reader);fields=reader.fieldnames
mismatch=[]
if len(csvrows)!=len(sources):mismatch.append("count")
for a,b in zip(csvrows,sources):
    for key in fields:
        expected=b.get(key,"Unknown")
        if isinstance(expected,(list,dict)):
            try:got=json.loads(a[key])
            except ValueError:got=a[key]
        else:
            got=a[key];expected="" if expected is None else str(expected)
        if got!=expected:mismatch.append(a.get("id","?")+":"+key)
check("CSV_JSON_full_exported_fields",not mismatch,mismatch)
score=read("examples/motion-score.example.json");side=read("examples/framemotion-sidecar.example.json")
check("score_hash_binding",digest(P/"examples"/side["bindings"]["score_file"])==side["bindings"]["score_sha256"])
check("asset_hash_bindings",all(digest(P/"examples"/x["file"])==x["sha256"] for x in side["dependencies"]))
fps=Fraction(score["fps"]["num"],score["fps"]["den"])
check("rational_duration",Fraction(score["totalFrames"],1)/fps==Fraction(1001,125))
check("audio_cue_frame_arithmetic",all(Fraction(x["sample"],side["audio"]["sample_rate_hz"])*fps==x["local_frame"] for x in side["audio"]["cues"]))
check("unapproved_and_native_NOT_RUN_preserved",side["provenance"]["client_approval"] is False and side["qa"]["preflight"]=="blocked" and all(side["qa"][k]=="NOT_RUN" for k in ("native_render","realtime_review","listening")))
historical=read("VERIFICATION.json");fresh=read("EXPORT-VERIFICATION.json")
check("historical_and_export_results_separate",historical["checks_total"]==43 and fresh["context"]=="Fresh run on publication export; not the historical source run" and fresh["original_verifier_result"]["checks_total"]==43 and fresh["original_verifier_result"]["checks_passed"]==43)
out={"schema":"dr01-export-checks/1","status":"PASS" if all(x["status"]=="PASS" for x in checks) else "FAIL","scope":"Read-only document/hash/link/analytic export checks; no native renderer, video, audio, browser fonts or external URL checks.","checks_passed":sum(x["status"]=="PASS" for x in checks),"checks_total":len(checks),"export_file_count":len(actual),"manifest_sha256":digest(P/"EXPORT-MANIFEST.json"),"checks":checks}
print(json.dumps(out,ensure_ascii=False,indent=2))
sys.exit(0 if out["status"]=="PASS" else 1)

