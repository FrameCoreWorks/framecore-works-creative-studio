#!/usr/bin/env python3
"""Combine research indices; writes only beside this file, preserving dated backups."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
from urllib.parse import urlparse
import json, shutil

B=Path(__file__).resolve().parent
stamp=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
def put(name,data):
    p=B/name
    if p.exists():
        previous=p.read_bytes()
        backup=B/"evidence"/"backups"/(name.replace("/","_")+"."+stamp)
        backup.parent.mkdir(parents=True,exist_ok=True)
        backup.write_bytes(previous)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")
registries=["catalog/sources.json","production/sources.json","baseline/sources.json","evidence/policy_sources.json"]
group={}
raw_count=0
for registry in registries:
    rows=json.loads((B/registry).read_text())
    for row in rows:
        raw_count+=1
        u=row["url"]
        if not u.startswith(("http://","https://")):
            u=str(((B/registry).parent/u).resolve().relative_to(B))
        entry=dict(row)
        entry["registry"]=registry
        entry["url"]=u
        group.setdefault(u,[]).append(entry)
sources=[{"url":u,"records":rows} for u,rows in sorted(group.items())]
eps=json.loads((B/"catalog/episodes.json").read_text())
channels=json.loads((B/"catalog/channels.json").read_text())
main=[e for e in eps if e.get("main_sample")]
public=[s for s in sources if s["url"].startswith("https://")]
excluded={"search_result_metadata","watch_page_access_attempt","watch_page_shell"}
opened=[s for s in public if any(r.get("evidence_type") not in excluded for r in s["records"])]
stats={
 "as_of":"2026-11-11",
 "episodes_total":len(eps),
 "channels_total":len(channels),
 "main_episodes":len(main),
 "main_channels":len({e["channel_id"] for e in main}),
 "main_cohorts":dict(Counter(e["cohort"] for e in main)),
 "appendix_episodes":len(eps)-len(main),
 "all_cohorts":dict(Counter(e["cohort"] for e in eps)),
 "main_missing_metadata":{k:sum(e.get(k) in [None,"Unknown"] for e in main) for k in ["duration_seconds","publish_date","views"]},
 "all_missing_metadata":{k:sum(e.get(k) in [None,"Unknown"] for e in eps) for k in ["duration_seconds","publish_date","views"]},
 "all_access_types":dict(Counter(e["access_type"] for e in eps)),
 "recent_12m_all":sum(e.get("recent_12m") is True for e in eps),
 "recent_12m_main":sum(e.get("recent_12m") is True for e in main),
 "source_registry_records":raw_count,
 "unique_public_source_urls":len(public),
 "unique_local_source_urls":len(sources)-len(public),
 "public_urls_with_opened_or_documentary_evidence":len(opened),
 "source_evidence_types":dict(Counter(r.get("evidence_type","Unknown") for s in sources for r in s["records"])),
 "sampled_frame_films":sum("sampled" in e["access_type"] for e in eps),
 "fully_watched":0,
 "audio_listened":0,
 "transcripts_exported":7,
 "deep_dive_cards":12,
 "benchmark_status":"NOT_RUN",
 "limitations":["Search metadata may be stale; dates are not production dates.",
                "Opened/documentary URL counts describe source access, not full film watching.",
                "No full audiovisual analyses or runtime pilot tests."]
}
put("SOURCES.json",sources);put("EVIDENCE_STATS.json",stats)
print(json.dumps({k:stats[k] for k in ["episodes_total","main_episodes","main_channels","unique_public_source_urls","public_urls_with_opened_or_documentary_evidence","sampled_frame_films"]},ensure_ascii=False))
