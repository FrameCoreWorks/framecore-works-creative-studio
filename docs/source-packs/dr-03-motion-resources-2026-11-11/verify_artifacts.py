#!/usr/bin/env python3
"""Integrity/schema check of DR-03 artifacts. Does not run candidate code or media."""
from pathlib import Path
import csv
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
EXPECTED_PROMPT = "11aa9f40f5f10857d3a0dd41643928743173d610e128addbbde255ed48e438d4"
REQUIRED = ["PLAN.md","BASELINE.md","REPORT.md","CATALOG.json","CATALOG.csv","CARDS.md",
            "DEEP_DIVES.md","RANKINGS.md","SOURCES.json","TEST_PLAN.md","TIME_ADAPTER.md",
            "REJECTIONS.md","IMPLEMENTATION_HANDOFF.md","PROGRESS.md",
            "review/REVIEW.md","review/REVIEW.json","review/RESOLUTION.md"]
def require(condition, message):
    if not condition:
        raise AssertionError(message)
require(hashlib.sha256((ROOT/"PROMPT.md").read_bytes()).hexdigest()==EXPECTED_PROMPT, "Prompt changed")
for name in REQUIRED:
    f=ROOT/name
    require(f.is_file() and f.stat().st_size>20, f"Missing/empty {name}")
catalog=json.loads((ROOT/"CATALOG.json").read_text())
sources=json.loads((ROOT/"SOURCES.json").read_text())
require(isinstance(catalog,list) and catalog,"Catalog must be nonempty array")
require(isinstance(sources,list) and sources,"Sources must be nonempty array")
ids=[c["id"] for c in catalog]
require(len(set(ids))==len(ids),"Duplicate candidate IDs")
sids=[s["id"] for s in sources]
require(len(set(sids))==len(sids),"Duplicate source IDs")
fields=["id","name","url","owner","pin","reviewed","class","novelty","problem",
        "baseline_delta","module","io","runtime","export","cost","rights","maintenance",
        "evidence","target_owner","integration","recommendation","test","source_ids",
        "execution_status","card_path"]
novelties={"NEW","KNOWN_NEW_CAPABILITY","ALREADY_COVERED","DUPLICATE/FORK","BASELINE_UNKNOWN"}
for c in catalog:
    for f in fields:
        require(f in c and c[f] is not None and c[f]!="",f'{c["id"]}: missing {f}')
    require(c["novelty"] in novelties,f'{c["id"]}: novelty enum')
    require(c["execution_status"]=="NOT_RUN",f'{c["id"]}: candidate execution must remain NOT_RUN')
    require(bool(c["source_ids"]) and all(x in sids for x in c["source_ids"]),f'{c["id"]}: broken sources')
    require((ROOT/c["card_path"]).is_file(),f'{c["id"]}: missing detailed card file')
    if c["class"]=="C":
        require("asset_metadata" in c,f'{c["id"]}: asset metadata missing')
for s in sources:
    for f in ["id","url","accessed","kind","read_scope","claims","pin"]:
        require(f in s,f'{s.get("id")}: source missing {f}')
    require(s["url"].startswith("http"),f'{s["id"]}: URL')
with (ROOT/"CATALOG.csv").open(newline="") as f:
    rows=list(csv.DictReader(f))
require([r["id"] for r in rows]==ids,"CSV/JSON candidate mismatch")
for role in ["runtime","knowledge","assets"]:
    for f in ["candidates.json","sources.json","CARDS.md","DEEP_DIVES.md"]:
        require((ROOT/"agents"/role/f).is_file(),f"Missing agent {role}/{f}")
require({c["class"] for c in catalog}=={"A","B","C"},"Three resource classes required")
deep=[c for c in catalog if c.get("deep_dive")]
require(len(deep)>=8,"Fewer than eight deep dives; reconcile requirement explicitly")
require(all(c["id"] in (ROOT/"DEEP_DIVES.md").read_text() for c in deep),"Deep dive index mismatch")
review=json.loads((ROOT/"review/REVIEW.json").read_text())
require(review.get("scope")=="research_artifacts","Review scope must be research only")
require(review.get("fresh_session") is True,"Fresh independent review missing")
require(all(f.get("status")=="resolved" for f in review.get("findings",[]) if f.get("severity") in {"blocking","major"}),"Open material finding in structured review")
require(all(review.get("open_findings",{}).get(k)==0 for k in ["blocking","major"]),"Structured review reports open material findings")
resolution=(ROOT/"review/RESOLUTION.md").read_text()
require("OPEN_MAJOR: 0" in resolution and "OPEN_BLOCKING: 0" in resolution,"Unresolved material review findings")
for f in [ROOT/"REPORT.md",ROOT/"IMPLEMENTATION_HANDOFF.md",ROOT/"TEST_PLAN.md"]:
    require("NOT_RUN" in f.read_text(),f"{f.name}: missing execution boundary")
baseline=json.loads((ROOT/"sources/baseline-inventory.json").read_text())
require(len(baseline)==3 and all(re.fullmatch("[0-9a-f]{40}",r["sha"]) for r in baseline),"Baseline pin invalid")
require(len(json.loads((ROOT/"sources/toolbox-catalog.json").read_text())["entries"])==28,"Toolbox baseline count")
for md in ROOT.rglob("*.md"):
    if "backups" in md.relative_to(ROOT).parts:
        continue
    for target in re.findall(r"\]\(([^)]+)\)",md.read_text()):
        target=target.strip("<>")
        if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:",target) or target.startswith("#"):
            continue
        target=target.split("#")[0]
        if target:
            require((md.parent/target).exists(),f"Broken local link in {md.relative_to(ROOT)}: {target}")
all_files=[f for f in ROOT.rglob("*") if f.is_file()]
require(not any(f.name.startswith("._") for f in all_files),"AppleDouble sidecars")
require(max(f.stat().st_size for f in all_files)<16*1024*1024,"Hipson file hash limit")
require(sum(f.stat().st_size for f in all_files)<128*1024*1024,"Hipson project hash limit")
print(json.dumps({"artifact_integrity":"PASS","prompt_sha256":EXPECTED_PROMPT,
 "candidates":len(catalog),"by_class":{k:sum(c["class"]==k for c in catalog) for k in ["A","B","C"]},
 "deep_dives":len(deep),"source_records":len(sources),"csv_rows":len(rows),
 "review_resolution":"no open major/blocking in lead resolution","product_tests":"NOT_RUN",
 "limits":"Checks structure, local links and declared provenance; does not verify upstream claims or render/audio quality."},ensure_ascii=False,indent=2))

