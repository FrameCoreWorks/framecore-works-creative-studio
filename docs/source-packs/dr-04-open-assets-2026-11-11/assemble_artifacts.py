"""Local document assembly only. No network, imports of candidate code or media IO."""
import csv
import hashlib
import io
import json
import shutil
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STAMP = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')


def read(name):
    return json.loads((ROOT / name).read_text())


def save(name, content):
    path = ROOT / name
    if path.exists():
        backup = ROOT / 'backups' / STAMP / name
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


def dump(name, value):
    save(name, json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def csv_text(rows, fields):
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=fields)
    writer.writeheader()
    for row in rows:
        writer.writerow({key: json.dumps(row.get(key), ensure_ascii=False, sort_keys=True)
                         if isinstance(row.get(key), (list, dict)) else row.get(key, '')
                         for key in fields})
    return stream.getvalue()


def main():
    providers, records, sources = [], [], []
    rank_alias = {'MANUAL': 'MANUAL_REFERENCE_ONLY', 'REFERENCE_ONLY': 'MANUAL_REFERENCE_ONLY',
                  'OUT_OF_CORE': 'OPTIONAL'}
    deep_audio = {'internet_archive_curated', 'nasa_audio', 'nps_sound_video',
                  'wyzowl_sfx_kit', 'clr_music'}
    priority = {'nasa_audio': 'P0', 'iconify': 'P1', 'fontsource': 'P1',
                'internet_archive_curated': 'P0_RESEARCH_ONLY', 'phylopic-svg': 'P1',
                'wyzowl_sfx_kit': 'P1', 'google-fonts-repo': 'P1'}
    for part in ('audio_video', 'visual_data'):
        for row in read(part + '/catalog.json'):
            item = dict(row)
            original_rank = row.get('ranking', row.get('rank'))
            classification = row['provider_eligibility'] if isinstance(original_rank, int) else original_rank
            item['ranking'] = rank_alias.get(classification, classification)
            item['specialist_rank'] = original_rank
            item['provider_eligibility'] = {'decision': row['provider_eligibility'],
                                           'access_basis': row['auth'],
                                           'automation_basis': row['automation']}
            item['review_depth'] = row.get('review_depth', 'DEEP' if row['id'] in deep_audio else 'SURVEY')
            item['implementation_priority'] = priority.get(row['id'], row.get('priority', 'P2'))
            item['card_file'] = part + '/CARDS.md'
            item['provenance_file'] = part + '/catalog.json'
            item['assessment_status'] = 'DERIVED_RESEARCH_ONLY'
            item['host_readiness'] = 'NOT_RUN'
            providers.append(item)
        for row in read(part + '/records.json'):
            row = dict(row)
            row['record_read'] = True
            row['host_readiness'] = 'NOT_RUN'
            row['download_verification'] = 'NOT_RUN'
            row['decode_verification'] = 'NOT_RUN'
            row.setdefault('sha256', None)
            row['provenance_file'] = part + '/records.json'
            records.append(row)
    for part in ('baseline/sources.json', 'audio_video/sources.json',
                 'visual_data/sources.json', 'evidence/root_sources.json'):
        for row in read(part):
            row = dict(row)
            row.setdefault('read_status', 'UNCONFIRMED_CONTENT' if row.get('evidence') == 'Unknown' else 'READ')
            row['provenance_file'] = part
            sources.append(row)
    source_ids = [s['id'] for s in sources]
    assert len(set(source_ids)) == len(source_ids), 'duplicate source IDs'
    record_ids = {r['id'] for r in records}
    assert len(record_ids) == len(records), 'duplicate record IDs'
    for row in providers:
        assert set(row['source_ids']) <= set(source_ids), row['id']
        assert set(row['records']) <= record_ids, row['id']
    dump('catalog.json', providers)
    fields = ['id','name','owner','url','ranking','novelty','novelty_evidence','review_depth',
              'categories','provider_eligibility','asset_eligibility','host_readiness','access_mode',
              'auth','license','automation','search','details','download','formats','variants',
              'network','risks','adapter','implementation_priority','evidence','source_ids','records','card_file']
    save('catalog.csv', csv_text(providers, fields))
    dump('records.json', records)
    dump('sources.json', sources)
    save('sources.csv', csv_text(sources, ['id','url','accessed_at','evidence','read_status','claim','provenance_file']))
    baseline = read('baseline/baseline.json')
    summary = {'as_of': '2026-11-11', 'hipson_task': 'T-0007', 'research': 'DR-04',
               'provider_count': len(providers), 'deep_card_count': sum(x['review_depth']=='DEEP' for x in providers),
               'rank_counts': dict(Counter(x['ranking'] for x in providers)),
               'novelty_counts': dict(Counter(x['novelty'] for x in providers)),
               'record_count': len(records), 'source_entry_count': len(sources),
               'unique_source_urls': len({s['url'] for s in sources}),
               'source_read_status_counts': dict(Counter(s['read_status'] for s in sources)),
               'commits': baseline['commits'], 'provider_product_tests': 'NOT_RUN',
               'architecture_acceptance': 'NOT_GRANTED_RESEARCH_HANDOFF',
               'prompt_sha256': hashlib.sha256((ROOT/'PROMPT.md').read_bytes()).hexdigest()}
    dump('summary.json', summary)
    table = '# Rankingi i pokrycie kandydatów\n\nData 2026-11-11. Wszystkie decyzje DERIVED; każdy host NOT_RUN. Pełne osie, warunki i źródła są w catalog.json/CSV i kartach. CORE_CANDIDATE jest warunkowy, nie oznacza gotowej integracji. OUT_OF_CORE z kart specjalistów jest w zbiorczym katalogu pod OPTIONAL z zachowaniem przyczyny. P0_RESEARCH_ONLY oznacza rozstrzygnięcie przed implementacją.\n\n'
    for rank in ('CORE_CANDIDATE','OPTIONAL','MANUAL_REFERENCE_ONLY','REJECTED'):
        rows = [r for r in providers if r['ranking']==rank]
        table += '## '+rank+' ('+str(len(rows))+')\n\n| Kandydat | Nowość | Media / dostęp | Prawa i ograniczenie |\n|---|---|---|---|\n'
        for r in rows:
            detail = r['asset_eligibility'].replace('|','/')
            table += '| '+r['name']+' | '+r['novelty']+' | '+', '.join(r['categories'])+' / '+r['access_mode']+' | '+detail+' |\n'
        table += '\n'
    table += '## Podwójne liczenie\n\nOpenMoji static ma status DUPLICATE_MIRROR wobec odpowiedniej kolekcji Iconify; nie jest dodatkową nową biblioteką. Fontsource i Google Fonts to różne drogi dystrybucji tych samych rodzin: porównać rodzinę, wersję i wariant przed liczeniem przyrostu. Internet Archive może zawierać LibriVox/NASA, a Openverse indeksuje Commons i muzea; deduplikacja jest per asset, nie po nazwie serwisu. Statusy ALREADY_COVERED i BASELINE_UNKNOWN są dostępne, lecz żadna pozycja tego finalnego katalogu ich nie otrzymała.\n'
    save('RANKINGS.md', table)
    print(json.dumps({k:v for k,v in summary.items() if k != 'commits'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
