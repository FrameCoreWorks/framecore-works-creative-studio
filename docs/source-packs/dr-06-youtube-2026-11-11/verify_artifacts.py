#!/usr/bin/env python3
"""Read-only verification of DR-06 research artifacts; no render or network access."""
from pathlib import Path
import csv, hashlib, json, re, sys
from datetime import date
from urllib.parse import urlparse, unquote

BASE = Path(__file__).resolve().parent
draft = "--draft" in sys.argv
errors = []
def require(ok, msg):
    if not ok: errors.append(msg)
def readj(name):
    try: return json.loads((BASE/name).read_text())
    except Exception as e:
        errors.append(f"{name}: {e}")
        return []
required = [
    "PROMPT.md","PROMPT.sha256","PLAN.md","REPORT.md","SWARM.md",
    "SOURCES.json","EVIDENCE_STATS.json","SERIES_BIBLE_AND_WORKSHOP.md",
    "ORIGINAL_FORMATS.md","ECONOMICS.md","BENCHMARKS_AND_QA.md","benchmarks.json",
    "POLICY_AND_DELIVERY.md","IMPLEMENTATION_HANDOFF.md",
    "catalog/episodes.json","catalog/episodes.csv","catalog/channels.json",
    "catalog/channels.csv","catalog/DEEP_DIVES.md","catalog/COVERAGE.md",
    "catalog/sources.json","production/METHODS.md","production/PRODUCTION_CASES.md",
    "production/sources.json","baseline/BASELINE.md","baseline/repositories.json",
    "baseline/CONTRACTS.md","baseline/OPERATION_MAP.md","baseline/sources.json",
    "evidence/VIEWING_LOG.md","evidence/policy_sources.json",
]
for name in required: require((BASE/name).is_file(), "Missing "+name)
prompt=(BASE/"PROMPT.md").read_bytes()
require(hashlib.sha256(prompt).hexdigest()==(BASE/"PROMPT.sha256").read_text().strip(),
        "Original PROMPT hash changed")
eps=readj("catalog/episodes.json"); channels=readj("catalog/channels.json")
require(len({e["episode_id"] for e in eps})==len(eps),"Duplicate episode IDs")
require(len({e["channel_id"] for e in channels})==len(channels),"Duplicate channel IDs")
channel_ids={c["channel_id"] for c in channels}
fields=["url","title","publish_date","duration_seconds","language","views","views_read_date",
        "audience","audience_evidence","narration","visual_style","series_role",
        "access_type","scope","source_ids","main_sample","inclusion_class"]
cat_sources=readj("catalog/sources.json")
cat_ids={s["source_id"] for s in cat_sources}
for e in eps:
    prefix=e["episode_id"]+": "
    require(all(k in e for k in fields),prefix+"missing required metadata key")
    require(e["channel_id"] in channel_ids,prefix+"unknown channel")
    require(e["url"]=="https://www.youtube.com/watch?v="+e["episode_id"],prefix+"URL/id mismatch")
    require(re.fullmatch(r"[A-Za-z0-9_-]{11}",e["episode_id"]) is not None,prefix+"invalid ID")
    require(set(e["source_ids"])<=cat_ids,prefix+"unknown source ID")
    if e.get("views") is not None:
        require(isinstance(e["views"],int) and e["views"]>=0,prefix+"invalid views")
        require(bool(e.get("views_read_date")) and bool(e.get("views_provenance")),prefix+"views missing provenance/date")
    for key in ["publish_date","views_read_date"]:
        if e.get(key) not in [None,"Unknown"]:
            try: require(date.fromisoformat(e[key])<=date(2026,11,11),prefix+"future "+key)
            except ValueError: require(False,prefix+"invalid date "+key)
    if e.get("duration_seconds") is not None:
        require(isinstance(e["duration_seconds"],int) and e["duration_seconds"]>0,prefix+"invalid duration")
    require(not e.get("timestamps") or "sampled" in e["access_type"],prefix+"timestamps without sampled access")
    require("full_watch" not in e["access_type"],prefix+"unsupported full-watch claim")
main=[e for e in eps if e.get("main_sample")]
require(30<=len(main)<=50,"Main sample outside 30–50 films")
require(15<=len({e["channel_id"] for e in main})<=25,"Main sample outside 15–25 channels")
for name,records,key in [("episodes",eps,"episode_id"),("channels",channels,"channel_id")]:
    with (BASE/f"catalog/{name}.csv").open(newline="") as f: rows=list(csv.DictReader(f))
    require([r[key] for r in rows]==[r[key] for r in records],name+" CSV/JSON IDs/order mismatch")
    for row, rec in zip(rows,records):
        for col, value in row.items():
            expected=rec.get(col)
            if isinstance(expected,(list,dict)):
                try: require(json.loads(value)==expected,f"{name} CSV field mismatch {rec[key]}/{col}")
                except Exception: require(False,f"{name} invalid CSV JSON field {rec[key]}/{col}")
            elif expected is None: require(value in ["","Unknown","null"],f"{name} CSV null mismatch {rec[key]}/{col}")
            elif isinstance(expected,bool): require(value.lower()==str(expected).lower(),f"{name} CSV bool mismatch {rec[key]}/{col}")
            else: require(value==str(expected),f"{name} CSV field mismatch {rec[key]}/{col}")
repos=readj("baseline/repositories.json")
require(len(repos)==3,"Need exactly 3 baseline repositories")
for r in repos:
    require(bool(re.fullmatch("[0-9a-f]{40}",r["head_sha"])),"Invalid pinned SHA")
    require(r["head_sha"] in r["pinned_commit_url"],"Commit URL mismatch")
require(len({r["task_contract_sha256"] for r in repos})==1,"Baseline shared contract hash mismatch")
benches=readj("benchmarks.json")
require({x["id"] for x in benches}=={"B01","B02","B03","B04","B05"},"Benchmark IDs mismatch")
require(all(x["status"]=="NOT_RUN" and x["actual_result"] is None for x in benches),"Unexecuted benchmark marked run")
sources=readj("SOURCES.json")
urls=[s["url"] for s in sources]
require(len(urls)==len(set(urls)),"Combined source index has duplicate URL")
public=[u for u in urls if u.startswith("https://")]
require(len(public)>=40,"Fewer than 40 unique public source URLs")
for u in public: require(bool(urlparse(u).netloc),"Invalid public source URL")
stats=readj("EVIDENCE_STATS.json")
if isinstance(stats,dict):
    require(stats["episodes_total"]==len(eps),"Stats episode drift")
    require(stats["main_episodes"]==len(main),"Stats main sample drift")
    require(stats["unique_public_source_urls"]==len(public),"Stats source count drift")
    require(stats["fully_watched"]==0 and stats["audio_listened"]==0,"Unsupported viewing stats")
    require(stats["sampled_frame_films"]==sum("sampled" in e["access_type"] for e in eps)==11,"Sampled-frame scope mismatch")
    require(stats["transcripts_exported"]==sum("transcript" in e["access_type"] for e in eps)==7,"Transcript scope mismatch")
    require(stats["main_channels"]==len({e["channel_id"] for e in main}),"Stats main-channel mismatch")
    for key in ["duration_seconds","publish_date","views"]:
        require(stats["main_missing_metadata"][key]==sum(e.get(key) in [None,"Unknown"] for e in main),"Metadata gap stats mismatch: "+key)
    indexed={r["source_id"] for source in sources for r in source["records"]}
    require(cat_ids<=indexed,"Catalog sources missing from combined index")
deep=(BASE/"catalog/DEEP_DIVES.md")
if deep.exists():
    require(8<=len(re.findall(r"^### [0-9]+[.]",deep.read_text(),re.M))<=12,"Deep dive card count")
# Check actual local links in final Markdown (backups intentionally excluded).
for path in BASE.rglob("*.md"):
    if any("backup" in part.lower() for part in path.relative_to(BASE).parts) or path.name=="PROMPT.md": continue
    txt=path.read_text()
    for target in re.findall(r"\]\(([^)]+)\)",txt):
        target=target.strip("<>")
        if target.startswith(("https://","http://","#","mailto:","codex:")): continue
        target=unquote(target.split("#",1)[0])
        if not target: continue
        require((path.parent/target).exists(),f"Broken local link {path.relative_to(BASE)}: {target}")
if not draft:
    review=readj("review/review.json")
    require(isinstance(review,dict) and review.get("status") in ["pass","pass_with_limitations"],"Final independent review not passed")
    if isinstance(review,dict):
        require(not any(x.get("severity") in ["blocking","major"] and x.get("status") not in ["resolved","closed","accepted_limitation"] for x in review.get("findings",[])),
                "Unresolved material review finding")
report={
    "verification":"FAIL" if errors else ("DRAFT_PASS" if draft else "PASS"),
    "episodes":len(eps),"main_episodes":len(main),
    "main_channels":len({e["channel_id"] for e in main}),
    "main_missing_metadata":{k:sum(e.get(k) in [None,"Unknown"] for e in main) for k in ["duration_seconds","publish_date","views"]},
    "unique_public_source_urls":len(public),
    "runtime_benchmarks":"NOT_RUN","full_watches":0,"audio_listens":0,"errors":errors
}
print(json.dumps(report,ensure_ascii=False,indent=2))
sys.exit(1 if errors else 0)
