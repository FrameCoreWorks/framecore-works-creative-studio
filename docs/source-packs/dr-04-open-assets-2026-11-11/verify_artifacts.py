"""Validate DR-04 document integrity. Does not contact or execute providers."""
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROMPT_SHA = 'a6f93b1f72b909d0ead07a1ca5f06f83645361942dec830971348ca282451fe1'
REQUIRED = ['PROMPT.md','PLAN.md','REPORT.md','RANKINGS.md','RIGHTS_AND_EVIDENCE.md',
            'ADAPTER_DESIGNS.md','BACKLOG.md','backlog.json','TEST_PLAN.md',
            'IMPLEMENTATION_HANDOFF.md','GAPS.md','RUN_LOG.md','VERIFICATION.md',
            'catalog.json','catalog.csv','records.json','sources.json','sources.csv',
            'summary.json','MANIFEST_EXAMPLE.json','baseline/BASELINE.md','baseline/baseline.json',
            'baseline/sources.json','audio_video/CARDS.md','audio_video/catalog.json',
            'audio_video/records.json','audio_video/sources.json','visual_data/CARDS.md',
            'visual_data/catalog.json','visual_data/records.json','visual_data/sources.json',
            'review/REVIEW.md','review/review.json','assemble_artifacts.py','verify_artifacts.py']


def read(name):
    return json.loads((ROOT / name).read_text())


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    for name in REQUIRED:
        p = ROOT / name
        check(p.is_file() and p.stat().st_size > 0, 'missing/empty ' + name)
    check(hashlib.sha256((ROOT/'PROMPT.md').read_bytes()).hexdigest() == PROMPT_SHA, 'original prompt changed')
    files = [p for p in ROOT.rglob('*') if p.is_file()]
    check(max(p.stat().st_size for p in files) < 16 * 1024 * 1024, 'Hipson file size limit')
    check(sum(p.stat().st_size for p in files) < 128 * 1024 * 1024, 'Hipson tree size limit')
    check(not any(p.suffix.lower() in {'.png','.jpg','.jpeg','.mp3','.mp4','.wav','.ogg','.flac','.zip','.ttf','.woff','.woff2','.blend','.exr','.hdr'} for p in files), 'unexpected media/binary sample')

    cat, rec, src, summary = (read(x) for x in ['catalog.json','records.json','sources.json','summary.json'])
    ids = {x['id'] for x in cat}; rid = {x['id'] for x in rec}; sid = {x['id'] for x in src}
    check(len(ids)==len(cat) and len(rid)==len(rec) and len(sid)==len(src), 'duplicate IDs')
    ranks = {'CORE_CANDIDATE','OPTIONAL','MANUAL_REFERENCE_ONLY','REJECTED'}
    novelties = {'NEW_PROVIDER','EXISTING_NEW_CATEGORY','ALREADY_COVERED','DUPLICATE_MIRROR','BASELINE_UNKNOWN'}
    fields = {'id','name','owner','url','ranking','novelty','novelty_evidence','categories','provider_eligibility',
              'asset_eligibility','host_readiness','access_mode','auth','license','automation','search','details',
              'download','formats','variants','network','risks','adapter','source_ids','records','review_depth','card_file'}
    for row in cat:
        check(fields <= set(row), 'provider fields '+row['id'])
        check(row['ranking'] in ranks and row['novelty'] in novelties, 'invalid classification '+row['id'])
        check(row['host_readiness']=='NOT_RUN', 'provider readiness overclaim '+row['id'])
        check(row['review_depth'] in {'DEEP','SURVEY'}, 'review depth '+row['id'])
        check(row['source_ids'] and set(row['source_ids'])<=sid, 'provider source refs '+row['id'])
        check(set(row['records'])<=rid, 'provider record refs '+row['id'])
        check('OWN_TEST' not in str(row['evidence']), 'metadata is not product test '+row['id'])
        check((ROOT/row['card_file']).is_file(), 'missing card '+row['id'])
    for row in rec:
        check(row['provider'] in ids and row['source_id'] in sid, 'record reference '+row['id'])
        check(row['host_readiness']==row['download_verification']==row['decode_verification']=='NOT_RUN', 'record test overclaim '+row['id'])
        check(row.get('sha256') is None, 'invented sample SHA '+row['id'])
        check(row.get('evidence')!='OWN_TEST', 'record metadata OWN_TEST '+row['id'])
    for row in src:
        check(all(row.get(k) for k in ['id','url','accessed_at','evidence','claim','read_status']), 'source fields '+row['id'])
        check(row['read_status'] in {'READ','BLOCKED','INDEXED_EXCERPT','UNCONFIRMED_CONTENT'}, 'source read status '+row['id'])

    for csvname, data in [('catalog.csv',cat),('sources.csv',src)]:
        with (ROOT/csvname).open(newline='') as f:
            rows = list(csv.DictReader(f))
        check(len(rows)==len(data), 'CSV count '+csvname)
        check([x['id'] for x in rows]==[x['id'] for x in data], 'CSV order '+csvname)
        for expected, observed in zip(data,rows):
            for key,value in observed.items():
                e = expected.get(key,'')
                e = json.dumps(e,ensure_ascii=False,sort_keys=True) if isinstance(e,(dict,list)) else str(e)
                check(value==e, 'CSV/JSON mismatch '+csvname+'/'+expected['id']+'/'+key)

    check(summary['provider_count']==len(cat) and summary['record_count']==len(rec), 'summary counts')
    check(summary['source_entry_count']==len(src) and summary['unique_source_urls']==len({x['url'] for x in src}), 'summary source counts')
    check(summary['deep_card_count']==sum(x['review_depth']=='DEEP' for x in cat), 'summary deep count')
    check(summary['rank_counts']==dict(Counter(x['ranking'] for x in cat)), 'rank counts')
    check(summary['novelty_counts']==dict(Counter(x['novelty'] for x in cat)), 'novelty counts')
    check(summary['source_read_status_counts']==dict(Counter(x['read_status'] for x in src)), 'read-status counts')
    check(summary['prompt_sha256']==PROMPT_SHA and summary['provider_product_tests']=='NOT_RUN', 'summary verification scope')
    baseline = read('baseline/baseline.json')
    check(baseline['provider_count']==15 and baseline['provider_category_pair_count']==24, 'baseline count')
    for row in baseline['commits'].values():
        check(bool(re.fullmatch(r'[0-9a-f]{40}',row['commit'])), 'missing pinned commit')
    check(baseline['own_runtime_search_download_decode']=='NOT_RUN', 'baseline execution overclaim')

    tasks = read('backlog.json')
    check({x['priority'] for x in tasks}=={'P0','P1','P2'}, 'backlog priorities')
    tids = {x['id'] for x in tasks}
    test_text = (ROOT/'TEST_PLAN.md').read_text()
    for row in tasks:
        check(all(k in row for k in ['goal','inputs','outputs','owner','dependencies','errors','limits','cost','acceptance','tests','status']), 'task fields '+row['id'])
        check(row['status']=='NOT_RUN' and set(row['dependencies'])<=tids, 'task status/deps '+row['id'])
        check(all(t in test_text for t in row['tests']), 'test reference '+row['id'])
    check(len(set(re.findall(r'\| (T\d{2}) \|',test_text)))==20, 'test plan coverage')
    example=read('MANIFEST_EXAMPLE.json')
    check(example['status']=='NOT_RUN' and example['current_sidecar_field_names']['sha256'] is None, 'example is fake proof')

    review=read('review/review.json')
    check(review['scope']=='DOCUMENT_REVIEW_ONLY', 'review scope')
    check(review['status'] in {'PASS','PASS_WITH_LIMITATIONS'}, 'review changes required')
    open_major=[x for x in review.get('findings',[]) if x.get('severity') in {'blocking','major'} and x.get('status','open') not in {'resolved','fixed'}]
    check(not open_major, 'unresolved major review findings')
    for name in [n for n in REQUIRED if n.endswith('.md')]:
        for target in re.findall(r'\]\(([^)]+)\)', (ROOT/name).read_text()):
            target=target.strip('<>')
            if target.startswith(('https://','http://','mailto:','#','codex://')):
                continue
            path=(ROOT/name).parent/target
            if not path.exists():
                path=(ROOT/name).parent/target.split('#')[0]
            check(path.exists(), 'broken local link '+name+' → '+target)
    print(json.dumps({'status':'PASS','scope':'DOCUMENT_INTEGRITY_ONLY','providers':len(cat),
                      'deep_cards':summary['deep_card_count'],'records':len(rec),'source_entries':len(src),
                      'ranks':summary['rank_counts'],'original_prompt':'UNCHANGED','product_tests':'NOT_RUN',
                      'review_status':review['status'],'total_bytes_including_backups':sum(p.stat().st_size for p in files)},
                     ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
