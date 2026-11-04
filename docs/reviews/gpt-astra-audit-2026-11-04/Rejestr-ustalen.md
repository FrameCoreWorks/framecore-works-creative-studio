# Rejestr ustaleń audytu

Priorytet jest decyzją audytową, a nie oceną CVSS. P0 oznacza tu potwierdzoną utratę istniejących danych w konkretnej ścieżce. P1 dotyczy istotnej granicy bezpieczeństwa, integralności zadania lub dystrybucji. P2 obejmuje poprawność, jakość i luki dowodowe. P3 obejmuje utrzymanie, dokumentację i propozycje. Wykonane próby są odróżnione od analizy statycznej i propozycji.

## CW-AUD-002 · SEC-002 · P0

**Nieudane pobranie Voicebox niszczy poprzednie nagranie przed walidacją**

**Typ:** data_integrity. **Lokalizacja:** `studio/plugins/voice-narration/scripts/voicebox.py:67; studio/plugins/voice-narration/scripts/voicebox.py:85; studio/plugins/voice-narration/scripts/runtime.py:282`.

**Pewność dowodu:** high: Jawna ocena domenowego recenzenta; granice dowodu podane w oryginalnym rekordzie. **Rewizja:** `[{"repository": "studio", "commit": "d2dbc1855e0552fbe753b69eeeb222faa282f016"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Warunki

- Istnieje poprzedni plik <cue.id>.wav.
- Ponowne generowanie tej samej kwestii zwraca błędny RIFF lub konwersja kończy się błędem.

### Dowód i obserwacja

download zapisuje body do docelowego WAV przed audio.spoken_duration. Po błędzie walidacji przechodzi do konwersji, która może zawieść, pozostawiając poprzedni plik nadpisany. record_take zachowuje metadane wcześniejszego take, lecz bajty już nie istnieją.

- Utworzono prawidłowy testowy WAV w TemporaryDirectory.
- Mock odpowiedzi zwrócił RIFFFAKE_BROKEN; mock braku ffmpeg dał AudioError.
- Hash starego nagrania zmienił się; plik zawiera RIFFFAKE_BROKEN. Zero sieci.

PYTHONDONTWRITEBYTECODE=1 python - <<'PY'
import sys,pathlib,tempfile,io,wave,hashlib
from unittest import mock
sys.path.insert(0,'/workspace/scratch/7067180697aa/fwcs-audit-20261104/studio/plugins/voice-narration/scripts')
import voicebox
with tempfile.TemporaryDirectory() as folder:
 dest=pathlib.Path(folder)/'L01.wav'
 with wave.open(str(dest),'wb') as w:
  w.setnchannels(1);w.setsampwidth(2);w.setframerate(16000);w.writeframes(b'\x01\x01'*1600)
 before=hashlib.sha256(dest.read_bytes()).hexdigest();client=voicebox.VoiceboxClient()
 with mock.patch.object(client,'_open',return_value=io.BytesIO(b'RIFFFAKE_BROKEN')),mock.patch.object(voicebox.shutil,'which',return_value=None):
  try:client.download('fake-id',dest)
  except Exception as exc:print(type(exc).__name__,str(exc))
 print('preserved',hashlib.sha256(dest.read_bytes()).hexdigest()==before,'remaining',dest.read_bytes())
PY

### Skutek i granice

Utrata poprzedniego wygenerowanego nagrania przy nieudanej próbie poprawki; poprzednie metadane mogą wskazywać hash niezgodny z uszkodzonym plikiem. Zakres: jeden wskazany output, nie dowolny katalog.

### Zalecana zmiana

Pobrać i przekonwertować do unikatowego pliku tymczasowego w tym samym katalogu, zweryfikować pełny WAV i dopiero po sukcesie wykonać atomowe replace. Każda ścieżka błędu zachowuje istniejący take i metadane.

### Odbiór

Dla uszkodzonego RIFF, błędu ffmpeg, przerwania i błędu zapisu hash poprzedniego WAV pozostaje niezmienny; dla sukcesu plik i lock zmieniają się razem.

### Weryfikacja

FAIL: safe local reproduction

**Pełny rekord z reprodukcją:** `evidence/security/findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-001 · SEC-001 · P1

**Brand Kit pomija kontrolę adresu połączenia przy NO_PROXY**

**Typ:** security_boundary. **Lokalizacja:** `studio/plugins/brand-kit/scripts/site_fetch.py:86; studio/plugins/brand-kit/tests/site_test.py:77`.

**Pewność dowodu:** high: Jawna ocena domenowego recenzenta; granice dowodu podane w oryginalnym rekordzie. **Rewizja:** `[{"repository": "studio", "commit": "d2dbc1855e0552fbe753b69eeeb222faa282f016"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Warunki

- Agent pobiera URL kontrolowany przez atakującego.
- HTTP_PROXY/HTTPS_PROXY jest ustawione, ale NO_PROXY wyłącza proxy dla celu, np. *.
- DNS atakującego zmienia adres z publicznego w pre-check na prywatny przy connect.

### Dowód i obserwacja

_proxied bada samą obecność konfiguracji proxy i usuwa _CheckedHTTPHandler/_CheckedHTTPSHandler. urllib uwzględnia NO_PROXY niezależnie i łączy się bezpośrednio. Pozostaje tylko wcześniejszy DNS check, więc drugi lookup może wskazać loopback/prywatny host.

- Bez skonfigurowanego proxy: UnsafeURL, non-public 127.0.0.1.
- Z HTTP_PROXY oraz NO_PROXY=*: HTTP 200 i treść FAKE_INTERNAL_ONLY z fikcyjnego lokalnego serwera.
- Każdy wariant użył dwóch kontrolowanych odpowiedzi DNS; brak zewnętrznych połączeń.

PYTHONDONTWRITEBYTECODE=1 python - <<'PY'
import importlib.util,pathlib,socket,threading,http.server,os
from unittest.mock import patch
p=pathlib.Path('/workspace/scratch/7067180697aa/fwcs-audit-20261104/studio/plugins/brand-kit/scripts/site_fetch.py')
s=importlib.util.spec_from_file_location('audit_site',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class Handler(http.server.BaseHTTPRequestHandler):
 def do_GET(self):
  self.send_response(200);self.send_header('Content-Type','text/plain');self.end_headers();self.wfile.write(b'FAKE_INTERNAL_ONLY')
 def log_message(self,*a):pass
server=http.server.HTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start();real=socket.getaddrinfo
try:
 for proxied in [False,True]:
  calls=[]
  def lookup(host,port,*a,**kw):
   if host=='rebind.invalid':
    calls.append(host);return real('93.184.216.34' if len(calls)==1 else '127.0.0.1',port,*a,**kw)
   return real(host,port,*a,**kw)
  m.check_url.__defaults__=(lookup,m.urllib.request.getproxies)
  env={'NO_PROXY':'*','no_proxy':'*'}
  if proxied:env.update(HTTP_PROXY='http://proxy.invalid:8080',http_proxy='http://proxy.invalid:8080')
  with patch.dict(os.environ,env,clear=True),patch.object(socket,'getaddrinfo',side_effect=lookup):
   try:print(proxied,m.fetch(f'http://rebind.invalid:{server.server_address[1]}/fake'))
   except Exception as exc:print(proxied,type(exc).__name__,str(exc))
finally:server.shutdown();server.server_close()
PY

### Skutek i granice

Warunkowy odczyt wewnętrznego HTTP przez narzędzie deklarujące wyłącznie publiczne strony. Nie wykazano odczytu sekretów ani skutecznego ataku na realny serwis.

### Zalecana zmiana

Uwzględniać proxy_bypass dla aktualnego hosta i każdego redirectu. Dla połączeń bezpośrednich zawsze weryfikować docelowy adres albo łączyć się z wcześniej zweryfikowanym adresem numerycznym; osobno traktować peer rzeczywistego proxy.

### Odbiór

Lokalny test z HTTP_PROXY+NO_PROXY i public→private DNS musi odmówić zanim wyśle HTTP GET; kontrola negatywna nadal odmawia bez proxy; rzeczywista trasa proxy ma osobny test.

### Weryfikacja

FAIL: safe local reproduction

**Pełny rekord z reprodukcją:** `evidence/security/findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-005 · DIST-001 · P1

**Jedyny skill REA ma niepoprawny YAML frontmatter**

**Typ:** portable_skill_invalid. **Lokalizacja:** `toolbox/plugins/rea/skills/rea/SKILL.md:3; toolbox/scripts/package_plugins.py:113`.

**Pewność dowodu:** high: Pełny parser odrzuca konkretne frontmatter; odrzucenia przez natywny loader nie wykonano. **Rewizja:** `[{"repository": "toolbox", "commit": "8652ba3494a3a2a58ef77bdfb619fd956a42d55e"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Dowód i obserwacja

Opis zawiera niecytowany dwukropek ze spacją po "rea-agents 6.5.0):". yaml.safe_load odrzuca frontmatter z "mapping values are not allowed here". To jedyny skill tej paczki. Lokalny validate_plugin sprawdza opis przez regex i mimo tego zwraca PASS oraz buduje ZIP. Nie wykonywano importu do klienta; odrzucenie przez parser YAML jest odtworzone lokalnie.

- evidence/distribution/raw/component-audit.json
- evidence/distribution/raw/component-audit.log
- evidence/distribution/raw/toolbox-rea-package.log
- evidence/distribution/raw/rea-package-build.log

### Zalecana zmiana

Ująć cały opis w poprawny quoted scalar albo block scalar; walidować faktyczny YAML i typy name/description w package_plugins.py przed archiwizacją.

### Odbiór

yaml.safe_load frontmatter zwraca mapę z niepustymi name/description; negatywny fixture z niecytowanym ": " zatrzymuje --check i build przed utworzeniem ZIP; po autoryzowanym imporcie host pokazuje oczekiwany skill.

**Pełny rekord z reprodukcją:** `evidence/distribution/findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-006 · DIST-002 · P1

**Portable REA nie deklaruje serwera MCP w mcp.json**

**Typ:** portable_component_missing. **Lokalizacja:** `toolbox/plugins/rea/plugin.json:2; toolbox/plugins/rea/.mcp.json:1; toolbox/plugins/rea/.codex-plugin/plugin.json:18`.

**Pewność dowodu:** high: Sprawdzono deklarację pliku względem kontraktu portable; uruchomienie MCP w Work pozostaje NOT_RUN. **Rewizja:** `[{"repository": "toolbox", "commit": "8652ba3494a3a2a58ef77bdfb619fd956a42d55e"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Dowód i obserwacja

Paczkę oznaczono Agent Plugins 1.0, lecz zawiera wyłącznie legacy .mcp.json. Nie ma root mcp.json ze schemą MCP i deklaracją transportu. Obecny Codex overlay wskazuje legacy plik, co może działać w tym konkretnym kliencie; nie dostarcza jednak komponentu odkrywanego w portable formacie. Wraz z DIST-001 paczka nie ma poprawnego portable skillu ani portable MCP. Aktywacja serwera i instalacja klienta pozostają NOT_RUN.

- evidence/distribution/raw/component-audit.json
- evidence/distribution/raw/toolbox-rea-package.log

### Zalecana zmiana

Dodać root mcp.json zgodny z https://agent-plugins.org/schemas/1.0.0/mcp.schema.json, type stdio i tym samym pinem rea-agents@6.5.0; zachować potrzebne compatibility manifests i rozróżnienie local host od konta web/mobile.

### Odbiór

Portable parser odczytuje rea jako jeden serwer stdio; legacy i portable konfiguracja wskazują identyczny pin; validator wykrywa brakujący portable plik; discovery i nieszkodliwe wywołanie lokalnego serwera dopiero w autoryzowanym teście instalacji.

**Pełny rekord z reprodukcją:** `evidence/distribution/findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-009 · ORCH-01 · P1

**Kontrakt companion nie wiąże żądania, faktycznej operacji i przyjmowanego wyniku**

**Typ:** gap. **Lokalizacja:** `toolbox/plugins/toolbox/capabilities/earshot/scripts/envelope.py:74; toolbox/plugins/toolbox/capabilities/earshot/scripts/envelope.py:184; studio/plugins/framecore-work-creative-studio/skills/delivery-documentation/scripts/companion_intake.py:70; studio/plugins/framecore-work-creative-studio/skills/pipeline-core/references/companion-routing.md:25`.

**Pewność dowodu:** high: Powtórzona kontrolowana reprodukcja na mockach; nie wykonano rzeczywistej nieautoryzowanej instalacji. **Rewizja:** `[{"repository": "studio", "commit": "d2dbc1855e0552fbe753b69eeeb222faa282f016"}, {"repository": "toolbox", "commit": "8652ba3494a3a2a58ef77bdfb619fd956a42d55e"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Dowód i obserwacja

- **method:** Import modułu z python3 -B, fixture w TemporaryDirectory, envelope.launch zastąpione funkcją zapisującą argv i zwracającą (0,{},empty), runtime.status zastąpione ready_light. Bez silnika, sieci, instalacji i plików produkcyjnych.
- **request:** {'contract': 'framecore-task-request/1', 'task_id': 'approved:read-only', 'origin': 'studio', 'requester': {'plugin': 'framecore-work-creative-studio'}, 'provider': {'plugin': 'toolbox', 'capability': 'earshot', 'operation': 'status'}, 'inputs': 'approved-file + jego SHA-256', 'constraints': {'runtime_root': 'approved-root'}, 'consent': {}}
- **argv:** envelope.main([--request,request.json,--result-out,result.json,--input,other-file,--,--root,other-root,install,--tier,light,--yes])
- **observed:** {'return_code': 0, 'mock_launch_operation': 'install --tier light --yes', 'result_status': 'succeeded', 'result_operation': 'install', 'input_sha_differs': True, 'real_runtime_ran': False}
- **intake_probe:** Zmieniono task_id wyniku na other-project:old-revision, provider.operation na run, dodano poprawnie zahashowany plik. companion_intake.check zwróciło PASS i placeable=true.
- **standalone_python:** from pathlib import Path
import sys, tempfile, json, importlib.util, hashlib
root = Path('/workspace/scratch/7067180697aa/fwcs-audit-20261104')
sys.path.insert(0, str(root / 'toolbox/plugins/toolbox/capabilities/earshot/scripts'))
import envelope
with tempfile.TemporaryDirectory(prefix='orch-proof-') as temp:
    p = Path(temp)
    approved = p / 'approved'; approved.write_bytes(b'approved')
    other = p / 'other'; other.write_bytes(b'other')
    request = {'contract':'framecore-task-request/1','task_id':'approved:read-only',
      'origin':'studio','requester':{'plugin':'framecore-work-creative-studio'},
      'provider':{'plugin':'toolbox','capability':'earshot','operation':'status'},
      'inputs':[{'path':str(approved),'sha256':hashlib.sha256(approved.read_bytes()).hexdigest()}],
      'constraints':{'runtime_root':str(p / 'approved-root')},'consent':{}}
    req = p / 'request.json'; req.write_text(json.dumps(request))
    calls = []
    envelope.launch = lambda argv: (calls.append(argv) or (0, '{}', ''))
    envelope.runtime.status = lambda root: {'state':'ready_light'}
    rc = envelope.main(['--request',str(req),'--result-out',str(p/'result.json'),
      '--input',str(other),'--','--root',str(p/'other-root'),'install','--tier','light','--yes'])
    result = json.loads((p/'result.json').read_text())
    assert rc == 0 and calls and result['provider']['operation'] == 'install'
    assert result['inputs'][0]['sha256'] != request['inputs'][0]['sha256']
    spec = importlib.util.spec_from_file_location('intake',root / 'studio/plugins/framecore-work-creative-studio/skills/delivery-documentation/scripts/companion_intake.py')
    intake = importlib.util.module_from_spec(spec); spec.loader.exec_module(intake)
    result['task_id'] = 'other-project:old-revision'
    result['provider']['operation'] = 'run'
    result['outputs'] = [{'path':str(other),'sha256':hashlib.sha256(other.read_bytes()).hexdigest(),'bytes':other.stat().st_size}]
    report = intake.check(result,p)
    assert report['status'] == 'PASS' and report['ledger_entry']['placeable'] is True
    print(json.dumps({'mock_launch':calls,'intake_status':report['status'],
      'placeable':report['ledger_entry']['placeable'],'task_id':report['ledger_entry']['task_id'],
      'real_runtime_ran':False},indent=2))

- **run_instruction:** Uruchomić jako python3 -B z kodem w quoted heredoc; wykonuje tylko mocki i temp fixtures.

### Skutek i granice

Omyłka w adapterze lub wznowieniu może wykonać inną operację niż zapisany request albo podpiąć wynik innego zadania/revizji. Prawidłowy hash dowodzi bajtów, nie ich związku z zamówieniem. Nie wykazano ominięcia zabezpieczeń samego runtime ani wykonania bez --yes; wrapper dokumentuje dziś węższe kopiowanie tożsamości, dlatego to luka kontraktu integracyjnego, nie potwierdzony exploit.

### Zalecana zmiana

Dla --request porównać operation/command, wybrany runtime_root oraz obowiązkowe wejścia i hashe z rzeczywistym CLI; jawnie rozstrzygnąć parametry tylko planowe. Intake przyjąć expected-request albo jawne expected task/provider/input revision. Zachować możliwość samodzielnego użycia bez request, z wyraźnie innym zakresem walidacji.

### Odbiór

- Rozbieżna operation/command/root lub hash jest odrzucana przed wywołaniem launch.
- Wynik innego task_id/request revision nie ma placeable=true w przyjęciu zadania.
- Zgodny request/result nadal przechodzi; samodzielny CLI działa i ma origin=standalone.

### Weryfikacja

LOCAL_MOCK_REPRODUCED

**Pełny rekord z reprodukcją:** `evidence/orchestration/findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-037 · INSTALL-01 · P1

**Instrukcja findera błędnie wyklucza natywną trwałą instalację w Work**

**Typ:** host_routing_gap. **Lokalizacja:** `studio/plugins/framecore-work-creative-studio/skills/workflow-orchestrator/references/skill-finder.md:61`.

**Pewność dowodu:** high: Odczytano regułę finder i aktualne natywne drogi zapisu; samej instalacji nie wykonywano. **Rewizja:** `[{"repository": "studio", "commit": "d2dbc1855e0552fbe753b69eeeb222faa282f016"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Dowód i obserwacja

Sekcja Hosts twierdzi, że skill nie może być zainstalowany w Work na kolejne rozmowy i ogranicza wybór do use once lub komendy Codex/Claude Code. Aktywna dokumentacja Skill Creator opisuje trwałe instalowanie własnych skilli w ChatGPT; Plugin Creator opisuje zapis prywatnych pluginów. Toolbox ma już osobną drogę private plugin dla wybranej pozycji. Vercel CLI rzeczywiście nie ma agenta ChatGPT Work i nie jest tym mechanizmem zapisu.

### Skutek i granice

Użytkownik Work może dostać błędną odmowę i instrukcję dla innego produktu, choć wybrany zgodny skill może być zapisany natywną drogą. Nie oznacza to, że każdy skill, hook lub serwer MCP z katalogu działa w Work.

### Zalecana zmiana

Po akceptacji kandydata rozgałęzić instalację według faktycznie dostępnego hosta: personal skill przez natywny workflow lub osobny prywatny plugin, zachowując upstream, komplet zasobów, licencję i tożsamość. CLI pozostawić dla lokalnych agentów. Uzgodnić capability card i teksty hostowe bez zmiany chronionych menu bez decyzji właściciela.

### Odbiór

Próba Work z dostępnym zarządzaniem skillami nie twierdzi, że trwały zapis jest niemożliwy; przygotowuje poprawny pakiet i używa właściwego zapisu po autoryzacji, odczytuje stan po zapisie i osobno weryfikuje discovery. Brak narzędzia kończy się uczciwym ograniczeniem, nie fałszywym sukcesem.

### Weryfikacja

SOURCE_CONFIRMED; źródło finder, natywne instrukcje hosta i oficjalna lista agentów Vercel przeczytane. Rzeczywista nowa instalacja NOT_RUN w audycie. Dodatkowe profile U101/U105 zaplanowane osobno.

**Pełny rekord z reprodukcją:** `evidence/installation/findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-040 · UPSTREAM-01 · P1

**Saved Huashu package lacks six fonts required before both standard renderer boot paths become ready**

**Typ:** Brak zasobu zapisanej paczki. **Lokalizacja:** `SKILL.md:127; scripts/engine/lib/fonts.js:25; scripts/engine/engine.js:39; scripts/engine/clip.js:72; scripts/engine/render.py:111`.

**Pewność dowodu:** high: Brak w pełnym zapisanym inventory plus identyczni callers i jawny łańcuch błędu; render NOT_RUN. **Rewizja:** `[{"repository": "alchaincyf/huashu-art-motion", "commit": "8a0d7d72ca65fcce6f8ba82c4a6c8dfe35b8422c"}, {"saved_release_id": "pluginrel_6ae8e850fa9481918c75ad3cf5b8ec89"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Dowód i obserwacja

The complete saved inventory lacks NotoSerifJP-600.woff, LXGWWenKai-500.woff and NotoSansSC-500/700/800/900.woff. fonts.js declares all six among 45 fonts. Both engine.js:39 and clip.js:72 await each FontFace.load() unconditionally before setting __ready. Their catch paths set __bootFailed; render.py:111-113 sees it and refuses rendering. All six relevant saved caller files were read and byte-match the pinned source.

Nonmutating static reproduction: parse every font URL; compare against saved public resource inventory. Six are absent, first in load order NotoSerifJP-600.woff. Trace awaited load to __bootFailed to render.py SystemExit. No browser render was executed.

### Skutek i granice

With only currently saved package resources, both standard engine and parameterized-clip bootstrap paths encounter a missing font even for a scene that does not request it. Ten missing showcase files and the full-style overview JPEG are additional reference gaps, not the cause of this bootstrap failure.

External runtime supplementation is not evidenced here. Historical authorization for omitted assets is Unknown.

### Zalecana zmiana

Restore exact pinned font bytes and license files through a supported binary route in an authorized repair. Re-read inventory and hashes, then test boot and one no-voice clip in the actual Work runtime. Preserve the partial-assets disclosure until complete.

### Weryfikacja

STATIC_CAUSAL_PROOF_WITH_SAVED_INVENTORY_AND_EXACT_CALLER_READBACK; NO_RENDER_EXECUTED

**Pełny rekord z reprodukcją:** `evidence/installation/upstream-findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-003 · SEC-003 · P2

**Instalacja VoxCPM2 nie jest odtwarzalna mimo przypiętego głównego pakietu**

**Typ:** supply_chain_hardening. **Lokalizacja:** `studio/plugins/voice-narration/scripts/runtime.py:239; studio/plugins/voice-narration/scripts/runtime.py:260; studio/plugins/voice-narration/scripts/voxcpm_worker.py:17`.

**Pewność dowodu:** high: Jawna ocena domenowego recenzenta; granice dowodu podane w oryginalnym rekordzie. **Rewizja:** `[{"repository": "studio", "commit": "d2dbc1855e0552fbe753b69eeeb222faa282f016"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Warunki

- Użytkownik autoryzuje install/fetch-models.

### Dowód i obserwacja

voxcpm==2.0.3 jest przypięty, lecz pip --upgrade pip, soundfile i zależności przechodnie nie mają locka/hashy. snapshot_download(openbmb/VoxCPM2) oraz from_pretrained nie wskazują revision. To obserwowalna luka powtarzalności; brak dowodu kompromitacji pakietu lub osiągalnego CVE.

Odczyt wskazanych linii: brak --require-hashes i revision. Bez pobierania, instalacji czy wywołań modelu.

### Skutek i granice

Ten sam numer pluginu może instalować inne zależności i wagi w różnych terminach; trudniejsze odtworzenie awarii i identyfikacja zatwierdzonego łańcucha dostaw.

### Zalecana zmiana

Przypiąć kompletny zestaw zależności i hashe per wspierana platforma oraz commit modelu. Zapisywać receipt; nie zmieniać istniejącej instalacji bez jawnej procedury aktualizacji.

### Odbiór

Mock setup sprawdza hash-locked dependencies, ograniczoną politykę indeksów i ten sam model revision przy pobraniu oraz load; rzeczywista instalacja osobnym autoryzowanym testem.

### Weryfikacja

Static analysis; installation NOT_RUN

**Pełny rekord z reprodukcją:** `evidence/security/findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-008 · DIST-004 · P2

**Główny przewodnik Toolbox blokuje Work route opisaną w aktywnym skillu**

**Typ:** installation_documentation_conflict. **Lokalizacja:** `toolbox/CHATGPT_INSTALL.md:35; toolbox/plugins/toolbox/skills/toolbox/references/installation.md:36`.

**Pewność dowodu:** high: Dwa odczytane dokumenty zawierają sprzeczne drogi Work; wpływ na pojedynczy dialog może się różnić. **Rewizja:** `[{"repository": "toolbox", "commit": "8652ba3494a3a2a58ef77bdfb619fd956a42d55e"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Dowód i obserwacja

CHATGPT_INSTALL.md każe nie pobierać ani przygotowywać trzecich wpisów dla Work i przedstawiać je jako Claude-only. Aktywna referencja installation.md opisuje po wyborze użytkownika osobny private plugin z niezmienionych skill folders tego samego upstream pinu. Te dwie instrukcje prowadzą do różnych wyników przy żądaniu dodania wskazanego modułu. Nie jest to dowód, że wszystkie upstream pakiety są kompatybilne; ich pełnych źródeł ten worker nie pobierał.

- evidence/distribution/raw/install-route-contradiction.json
- evidence/distribution/installation-matrix.json

### Zalecana zmiana

Ujednolicić przewodnik główny z host-aware route: wybór wpisu, kontrola upstream i licencji, jeden odrębny pakiet wyłącznie obsługiwanych skilli, readback i discovery. Zachować Unknown dla runtime lub brakujących zasobów.

### Odbiór

Przewodnik główny, aktywny SKILL i referencja opisują tę samą drogę dla żądania konkretnego wpisu oraz odróżniają zapis pluginu, activation i runtime; brak instrukcji oznaczania wszystkich third-party entries jako Claude-only.

**Pełny rekord z reprodukcją:** `evidence/distribution/findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-010 · ORCH-02 · P2

**Szablony companion_setup nadal opisują tylko Superpowers**

**Typ:** gap. **Lokalizacja:** `studio/plugins/framecore-work-creative-studio/skills/pipeline-core/templates/project-state.md:12; studio/plugins/framecore-work-creative-studio/skills/workflow-orchestrator/assets/cross-host-handoff.template.md:21; studio/plugins/framecore-work-creative-studio/skills/workflow-orchestrator/references/extensions.md:16`.

**Pewność dowodu:** high: Brak pól w odczytanych szablonach; nie dowodzi utraty wyboru w każdym przebiegu. **Rewizja:** `[{"repository": "studio", "commit": "d2dbc1855e0552fbe753b69eeeb222faa282f016"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Dowód i obserwacja

- **method:** Porównanie pól Project State i cross-host handoff z aktywną sekwencją setup; grep companion_setup i odczyt sąsiednich instrukcji.
- **observed:** Pole jest zdefiniowane w terminach Superpowers mimo trzech oddzielnych companion/add-on choices.

### Skutek i granice

Portable zapis oparty dosłownie na szablonie może pominąć odmowę lub etap instalacji Open Assets/Toolbox; nie stwierdzono takiego zachowania świeżego klienta.

### Zalecana zmiana

Zachować istniejące pole i dodać rekord per companion z choice, observed availability, host, version/evidence i zakresem persistence. Przenieść tylko żądany stan.

### Odbiór

- Fixture: Open Assets declined, Toolbox readable, Earshot deferred; eksport i resume zachowują każdy status.
- Stary snapshot zawierający tylko superpowers zostaje odczytany bez wymyślania pozostałych wyborów.

### Weryfikacja

SOURCE_CONFIRMED

**Pełny rekord z reprodukcją:** `evidence/orchestration/findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-011 · ORCH-03 · P2

**Task Handoff zakazuje kontekstu potrzebnego do dozwolonego prywatnego handoffu**

**Typ:** bug. **Lokalizacja:** `studio/plugins/framecore-work-creative-studio/skills/instruction-packet-factory/SKILL.md:78; studio/plugins/framecore-work-creative-studio/skills/instruction-packet-factory/references/hipson-format.md:33; studio/plugins/framecore-work-creative-studio/skills/pipeline-core/references/studio-integration-policy.md:59`.

**Pewność dowodu:** high: Potwierdzony konflikt instrukcji handoff; konkretny model może rozstrzygnąć go poprawnie. **Rewizja:** `[{"repository": "studio", "commit": "d2dbc1855e0552fbe753b69eeeb222faa282f016"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Dowód i obserwacja

- **method:** Source-guided scenario: użytkownik żąda prywatnego pakietu delegacji dla własnego briefu i plików projektu.
- **observed:** Polityka nadrzędna dopuszcza potrzebny kontekst, a entrypoint i format zakazują go bez wyjątku.

### Skutek i granice

Niejednoznaczna instrukcja może usuwać właściwy brief lub lokalizatory z dozwolonej delegacji i skłaniać odbiorcę do ponownego zbierania danych. Nie jest dowodem wycieku.

### Zalecana zmiana

Rozróżnić prywatny pakiet w zatwierdzonym środowisku od publicznego eksportu; sekretów nie przenosić w żadnym wariancie.

### Odbiór

- Prywatny pakiet zachowuje tylko task-needed kontekst i dostępne ścieżki.
- Wersja publiczna usuwa prywatne dane i sekrety; żadna nie dostaje niejawnej zgody na upload.

### Weryfikacja

SOURCE_CONTRADICTION

**Pełny rekord z reprodukcją:** `evidence/orchestration/findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-012 · ORCH-04 · P2

**Końcowa checklista Loop Protocol zawęża zgodę do bieżącej wiadomości**

**Typ:** bug. **Lokalizacja:** `studio/plugins/framecore-work-creative-studio/skills/pipeline-core/references/loop-protocol.md:262; studio/plugins/framecore-work-creative-studio/skills/pipeline-core/references/studio-integration-policy.md:51`.

**Pewność dowodu:** high: Potwierdzony konflikt zakresu zgody w instrukcjach; nie jest dowodem każdorazowej odmowy. **Rewizja:** `[{"repository": "studio", "commit": "d2dbc1855e0552fbe753b69eeeb222faa282f016"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Dowód i obserwacja

- **method:** Source-guided: zgoda z poprzedniej wiadomości w tej rozmowie pozostaje niewyczerpana, użytkownik teraz mówi kontynuuj.
- **observed:** Checklista literalnie wymaga current user message, policy zachowuje active conversation.

### Skutek i granice

Ryzyko zbędnego ponawiania pytań przy przejściu między ownerami. Polityka integracyjna rozstrzyga pierwszeństwo, więc brak dowodu runtime stop.

### Zalecana zmiana

Ujednolicić frazę do ważnej jawnej zgody w aktywnej rozmowie i jej dokładnego zakresu.

### Odbiór

- Niewyczerpana zgoda przechodzi handoff bez pytania.
- Nowy provider, destination lub wyczerpany limit zatrzymują chronioną operację.

### Weryfikacja

SOURCE_CONTRADICTION

**Pełny rekord z reprodukcją:** `evidence/orchestration/findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-015 · ORCH-07 · P2

**Przerwanie synchronicznego companion launch nie zapisuje terminalnego wyniku**

**Typ:** gap. **Lokalizacja:** `toolbox/plugins/toolbox/capabilities/earshot/scripts/envelope.py:31; toolbox/plugins/toolbox/capabilities/earshot/scripts/envelope.py:201`.

**Pewność dowodu:** high: Ścieżka przerwania i brak terminalnego envelope zbadane; różne sygnały hosta wymagają dalszych prób. **Rewizja:** `[{"repository": "toolbox", "commit": "8652ba3494a3a2a58ef77bdfb619fd956a42d55e"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Dowód i obserwacja

- **method:** envelope.launch zastąpione funkcją raise KeyboardInterrupt(); main wywołane ze status i nową ścieżką result. Wyjątek złapany wyłącznie przez test.
- **observed:** {'caught': 'KeyboardInterrupt', 'result_exists': False, 'real_runtime_ran': False}

### Skutek i granice

Przerwane długie zadanie nie dostaje framecore-task-result/1 status cancelled ani zapisu niepełnych efektów. Schemat dopuszcza cancelled, ale ta ścieżka go nie emituje; nie istnieje tu async job manager.

### Zalecana zmiana

Zdefiniować kontrakt przerwania synchronicznego procesu: obsłużyć interrupt, zaczekać na stan procesu i zapisać cancelled/partial z tym, co faktycznie wiadomo; bez ślepego retry i bez obietnicy anulowania zewnętrznej pracy.

### Odbiór

- Kontrolowany interrupt daje terminalny, walidowalny wynik i nie uruchamia ponownie zadania.
- Częściowe pliki nie stają się zaakceptowanymi mediami; brak końcowego stanu zostaje Unknown.

### Weryfikacja

LOCAL_MOCK_REPRODUCED

**Pełny rekord z reprodukcją:** `evidence/orchestration/findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-018 · LEARN-01 · P2

**Aktywna rubryka LM01 opisuje sprzeczne i nieaktualne menu**

**Typ:** confirmed_test_spec_defect. **Lokalizacja:** `plugins/framecore-work-creative-studio/evals/learning-mode-cases.json:31`.

**Pewność dowodu:** high: Jawna ocena domenowego recenzenta; granice dowodu podane w oryginalnym rekordzie. **Rewizja:** `[{"repository": "studio", "commit": "d2dbc1855e0552fbe753b69eeeb222faa282f016"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Dowód i obserwacja

- LM01 checks[1] wymaga osobnego menu 1 szybki / 2 rozbudowany, choć follow_up_sequences i obecny entrypoint wymagają łącznego wyboru obszaru 1–8 i tempa A/B.
- checks[0] wymienia cztery opcje, checks[5] trzy; aktualne źródła powitania zawierają pięć.
- follow_up_sequences invalid_startup_choice (linie 89–95) podaje 3, które jest poprawnym wyborem skill search.
- Bezpieczne uruchomienie validateLearningMode na izolowanej kopii tego baseline: errors=[].

### Skutek i granice

Recenzent lub judge korzystający z rubryki może nagradzać stare zachowanie albo odrzucać prawidłowe. Host LM01 wykonuje tylko pierwszą turę, więc obecny PASS nie rozstrzyga sprzecznych follow-ups.

### Zalecana zmiana

Zsynchronizować aktywną rubrykę i follow-ups z aktualnym kontraktem, pozostawiając historyczne logi bez zmian. Do testu niepoprawnego wyboru użyć tokenu spoza faktycznie pokazanej grupy. Zamiast mnożyć liczby menu w prozie wiązać scenariusz z bieżącym zasobem.

### Odbiór

- Wszystkie warianty LM01 mają jedną interpretację tokenów zgodną z powitaniem pięcioelementowym.
- 3 uruchamia wyszukanie skilla; niepoprawny token nie uruchamia produkcji.
- Test mutacyjny wykrywa ponowne wprowadzenie osobnego starego menu tempa.

**Pełny rekord z reprodukcją:** `evidence/learning/findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-019 · LEARN-02 · P2

**W06 zalicza dwa pytania i bezpodstawne ukończenie kursu**

**Typ:** confirmed_test_gap. **Lokalizacja:** `tests/host-evals/suite.json:151`.

**Pewność dowodu:** high: Jawna ocena domenowego recenzenta; granice dowodu podane w oryginalnym rekordzie. **Rewizja:** `[{"repository": "studio", "commit": "d2dbc1855e0552fbe753b69eeeb222faa282f016"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Dowód i obserwacja

- Drugą turę oceniają tylko not_welcome, language pl, brak tekstu Tryb szybki i max_questions:2.
- W izolowanym scorer-only probe odpowiedź „Czego chcesz się nauczyć? Ile czasu możesz przeznaczyć na naukę?” przeszła wszystkie cztery kontrole.
- Odpowiedź „Dziś kończymy pracę. Ukończyłeś kurs i osiągnąłeś pełną samodzielność.” również przeszła wszystkie cztery kontrole.
- To sztuczne odpowiedzi testowe, nie wynik modelu. subprocess.run był zastąpiony funkcją rzucającą AssertionError; nie uruchomiono Claude.

### Skutek i granice

Zielony host-test wejścia w naukę nie chroni nadrzędnej reguły jednego pytania ani rozpoczęcia właściwego procesu. Rubryka advisory nie może zmienić verdict.

### Zalecana zmiana

Zaostrzyć test wymagania jednego konkretnego pytania, dodać kontrolę zakończenia bez przypisania kompetencji i negatywne próbki scorera. Oceny semantyczne uczynić jawną częścią osobnego pedagogicznego odbioru, nie przemianowywać heurystyki znaków zapytania na rozumienie intencji.

### Odbiór

- Oba powyższe syntetyczne kontrprzykłady dostają FAIL.
- Poprawny wybór domeny z jedną grupą opcji przechodzi.
- Dwie decyzje z jednym znakiem zapytania także są wykrywane przez review semantyczny lub osobny kontrakt.

**Pełny rekord z reprodukcją:** `evidence/learning/findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-021 · LEARN-04 · P2

**Brak udokumentowanego pełnego cyklu nauki i niezależnej oceny kompetencji**

**Typ:** evidence_gap. **Lokalizacja:** `plugins/framecore-work-creative-studio/evals/learning-mode-cases.json:4`.

**Pewność dowodu:** high: Jawna ocena domenowego recenzenta; granice dowodu podane w oryginalnym rekordzie. **Rewizja:** `[{"repository": "studio", "commit": "d2dbc1855e0552fbe753b69eeeb222faa282f016"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Dowód i obserwacja

- 29 scenariuszy ma planned/not_run, z wyraźnym zakazem uznawania struktury za test zachowania.
- Przegląd wszystkich JSON w verification znalazł dla LM głównie historyczne W06/LM01: welcome i pierwsze pytanie; brak zapisanej próby LM04/LM08/LM17–24 zamykającej attempt→feedback→revision→transfer.
- PI03–PI05 sprawdzają intencje interaktywnej lekcji, ale pozostają planned/not_run.
- Instrukcje i źródła same rozróżniają projekt metody od dowodu skuteczności.

### Skutek i granice

Nie wiadomo, czy model utrzymuje pomoc, ocenę i przenoszenie postępu w wieloturowej nauce; skuteczność edukacyjna w każdej domenie pozostaje Unknown. Jest to luka dowodowa, nie dowód nieskuteczności.

### Zalecana zmiana

Najpierw zamknąć mały host-suite obejmujący pełne rozmowy i stan. Następnie przeprowadzić pilotaż z ludźmi oraz zadania samodzielne na zmienionym briefie. Oddzielać zgodność modelu z kontraktem od wyniku uczenia się.

### Odbiór

- Zachowane pełne wejścia, odpowiedzi, narzędzia, wersja, model, host i ocena każdego kryterium dla minimum 3 cykli domenowych.
- Co najmniej novice i advanced oraz pause/resume nie gubią dowodów i nie przypisują niezależności po podpowiedzi.
- Wyniki pilotażu raportują braki, wsparcie, zadanie opóźnione i ograniczenia; bez nieuzasadnionej obietnicy mastery.

### Uzupełnienie po przeglądzie źródeł

Późniejszy swarm dostarczył 25 profili nauki: 24 PASS, 1 PARTIAL (U024), w tym U015/U016 Teacher Studio PASS. To uzupełnia dowód zachowania modelu z profilu; nie jest pełnym badaniem samodzielności, trwałości nauki ani prowadzenia zajęć z ludźmi. Wniosek oryginalny opisuje brak takiego dowodu w źródłowym repo i pozostaje zawężony przez to uzupełnienie.

**Pełny rekord z reprodukcją:** `evidence/learning/findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-022 · LEARN-05 · P2

**Przenośna karta nie przenosi jawnie wszystkich ograniczeń planu**

**Typ:** contract_projection_gap. **Lokalizacja:** `plugins/framecore-work-creative-studio/skills/workflow-orchestrator/assets/learning-progress.template.md:23`.

**Pewność dowodu:** high: Jawna ocena domenowego recenzenta; granice dowodu podane w oryginalnym rekordzie. **Rewizja:** `[{"repository": "studio", "commit": "d2dbc1855e0552fbe753b69eeeb222faa282f016"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Dowód i obserwacja

- Plan constraints zawiera time, budget, accessibility, language, no-render preference.
- Progress card constraints wymienia tylko time, budget, available tools, preferred learning form.
- Project State ma research_status i limitation_disclosed; karta nie ma ich jawnego odpowiednika, chociaż learning-mode mówi o zachowaniu kontekstu.
- Nie zaobserwowano faktycznej utraty danych w hoście; pola constraints mogą być rozszerzane w prozie, więc problemem jest niepełna projekcja, a nie zakaz zapisania danych.

### Skutek i granice

Wznowienie po samej karcie może wymagać ponownego ustalenia dostępności lub niepotrzebnego disclaimer; ryzyko większe dla użytkownika z konkretną barierą niż dla domyślnego desktopu.

### Zalecana zmiana

W istniejącej linii constraints doprecyzować deklarowane potrzeby dostępności, język i dostępne formy dowodu; zachować tylko niezbędny research status. Nie zbierać diagnoz ani tworzyć drugiego profilu.

### Odbiór

- Roundtrip plan→karta→nowy kontekst zachowuje deklarowane ograniczenia i jedno pending_practice.
- Starsza karta bez pól nadal wznawia pracę z Unknown i bez pełnego onboardingu.

**Pełny rekord z reprodukcją:** `evidence/learning/findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-023 · LEARN-06 · P2

**Teacher Studio ma kompletne materiały, lecz weryfikacja zachowania obejmuje głównie routing**

**Typ:** evidence_gap. **Lokalizacja:** `tests/host-evals/routing.json:493`.

**Pewność dowodu:** high: Jawna ocena domenowego recenzenta; granice dowodu podane w oryginalnym rekordzie. **Rewizja:** `[{"repository": "studio", "commit": "d2dbc1855e0552fbe753b69eeeb222faa282f016"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Dowód i obserwacja

- RT18 sprawdza odczyt teacher-workflow.md lub copy-voice/SKILL.md, język i brak powitania. Nie sprawdza samodzielnie klucza, kompletności bodźców, punktacji ani oddzielenia odpowiedzi ucznia.
- Historycznie RT18 PASS w 1.63/1.64 i FAIL w 1.66/1.66.1; te wyniki nie dowodzą obecnego stanu.
- Ręcznie sprawdzono trzy lekcje, 12 aktywności i dwa szablony: klucze, sumy czasów 35/40/45 minut i proste działania są spójne; brak wykrytego błędu tych materiałów.
- Targeted search scripts/tests/evals nie ujawnił osobnego automatycznego teacher-content checker. Ogólne kontroly plików/odnośników istnieją.

### Skutek i granice

Rozszerzanie tematów lub adaptacja danych może wprowadzić niewychwycony błąd treści, mimo poprawnej trasy i wyglądu pliku.

### Zalecana zmiana

Dodać mały zestaw adaptacji teacher-content: zmiana liczby/danych, zadanie otwarte z wieloma poprawnymi odpowiedziami, niepełny stimulus, sprzeczny standard i eksport bez wycieku klucza. Zachować Teacher Studio jako profil creation.

### Odbiór

- Zmiana liczby w zadaniu wymusza zgodny klucz i total.
- Brak bodźca jest naprawiony lub oznaczony, a nie oceniany jako błąd ucznia.
- Rzeczywisty eksport rozdziela wersję ucznia i nauczyciela; bez eksportu status NOT_RUN.

### Uzupełnienie po przeglądzie źródeł

Późniejszy swarm dostarczył 25 profili nauki: 24 PASS, 1 PARTIAL (U024), w tym U015/U016 Teacher Studio PASS. To uzupełnia dowód zachowania modelu z profilu; nie jest pełnym badaniem samodzielności, trwałości nauki ani prowadzenia zajęć z ludźmi. Wniosek oryginalny opisuje brak takiego dowodu w źródłowym repo i pozostaje zawężony przez to uzupełnienie.

**Pełny rekord z reprodukcją:** `evidence/learning/findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-025 · CR-001 · P2

**Odczyt cytowalnego źródła jest błędnie utożsamiony z weryfikacją claimu**

**Typ:** instruction_semantics. **Lokalizacja:** `plugins/framecore-work-creative-studio/skills/marketing/references/positioning-and-audience-research.md:26`.

**Pewność dowodu:** high: Sprzeczny zapis semantyki dowodu jest w źródle; nie dowodzi fałszywego claimu w każdym dialogu. **Rewizja:** `[{"repository": "studio", "commit": "d2dbc1855e0552fbe753b69eeeb222faa282f016"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Dowód i obserwacja

- {"path": "plugins/framecore-work-creative-studio/skills/marketing/references/positioning-and-audience-research.md", "lines": "20-27"}
- {"path": "plugins/framecore-work-creative-studio/skills/commercial-video-campaign-director/references/applied-premise-and-proof.md", "lines": "9-14"}
- {"path": "plugins/framecore-work-creative-studio/skills/research-evidence/references/deep-research-method.md", "lines": "33-51"}

Definicja Verified wymaga tylko przeczytania źródła, które można zacytować; ten status steruje dopuszczeniem treści do downstream copy. Obok User-stated wymaga potwierdzenia możliwości udowodnienia. Własna strona reklamodawcy może więc uzyskać silniejszy status od tej samej deklaracji podanej w rozmowie.

### Skutek i granice

Claim opublikowany bez metodologii może zostać przeniesiony do publicznego copy jako verified. Pozostałe guardrails ograniczają ryzyko, lecz taxonomy jest sprzeczna.

### Zalecana zmiana

Oddziel source_read/observed_statement od substantiated_for_use; zachowaj źródło, typ i zakres dowodu, ograniczenia oraz zgodę na wording jako osobne pola. Nie uzależniaj prawdziwości od samego nośnika.

### Odbiór

- Strona marki z hasłem „podwaja sprzedaż”, bez danych/metody, daje source_read i unsupported efficacy, nie verified claim.
- Odpowiedni raport z metodą i zakresem może uzasadnić wyłącznie claim w tym zakresie.
- Ta sama deklaracja użytkownika w czacie i w jego PDF zachowuje ten sam poziom uzasadnienia.

### Weryfikacja

statyczny trace instrukcji; nie test hosta ani audyt prawny

**Pełny rekord z reprodukcją:** `evidence/creative/findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-026 · CR-002 · P2

**Linter cytowanej terminologii wymusza zbędne przepisywanie poprawnej treści**

**Typ:** helper_instruction_conflict. **Lokalizacja:** `plugins/framecore-work-creative-studio/skills/copy-voice/SKILL.md:41`.

**Pewność dowodu:** high: Fałszywy alarm lintera niezależnie odtworzony na cytowanej terminologii. **Rewizja:** `[{"repository": "studio", "commit": "d2dbc1855e0552fbe753b69eeeb222faa282f016"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Dowód i obserwacja

- {"path": "plugins/framecore-work-creative-studio/skills/copy-voice/SKILL.md", "lines": "41"}
- {"path": "plugins/framecore-work-creative-studio/skills/copy-voice/references/ai-writing-patterns.md", "lines": "92-101"}
- {"path": "plugins/framecore-work-creative-studio/skills/copy-voice/scripts/ai_writing_check.py", "lines": "97-99,130-134"}

SKILL nakazuje rewrite dla cluster. Helper skanuje regexem cały tekst, mimo że reference wyklucza cytaty, nazwy i omawiane frazy. Repro zdania opisującego trzy słowa zwraca cluster z empty-vocabulary count3.

- **command:** python3 plugins/framecore-work-creative-studio/skills/copy-voice/scripts/ai_writing_check.py --text 'W analizie języka reklamy porównujemy słowa „innowacyjny”, „kompleksowy” i „przełomowy”. To przykłady określeń wymagających konkretnego uzasadnienia.' --json
- **exit_code:** 1
- **result:** {'language': 'pl', 'verdict': 'cluster', 'kinds': 1, 'findings': [{'id': 'empty-vocabulary', 'category': 'tone', 'fix': 'say what it does instead', 'count': 3, 'examples': ['innowacyjny', 'kompleksowy', 'przełomowy']}]}

### Skutek i granice

Prawidłowy opis analityczny, cytat lub zamknięty slogan może być przepisany albo blokować delivery; dotyczy również humanizer korzystającego z kontroli.

### Zalecana zmiana

Traktuj wynik jako wskazanie do oceny w kontekście; dodaj uzasadniony wyjątek dla cytowanych/omawianych/locked spans. Nie wystarczy globalnie podnieść progu.

### Odbiór

- Podany negatywny przykład pozostaje bez zmian albo ma jawny approved exception, bez fałszywego zaliczenia marketingowego użycia słów.
- Trzy takie puste przymiotniki użyte promocyjnie nadal wywołują konkretną uwagę.
- Locked slogan nie jest automatycznie poprawiany.

### Weryfikacja

lokalne uruchomienie helpera; exit1 jest oczekiwanym objawem findingu, nie awarią harnessu

**Pełny rekord z reprodukcją:** `evidence/creative/findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-027 · CR-003 · P2

**Oferta kosztowa jest raportowana jako wydatek**

**Typ:** planning_data_semantics. **Lokalizacja:** `plugins/framecore-work-creative-studio/skills/creative-video-producer/references/production-worksheets.md:65`.

**Pewność dowodu:** high: Arkusz źródłowy utożsamia stany kosztu; rzeczywistego rachunku nie zmieniano. **Rewizja:** `[{"repository": "studio", "commit": "d2dbc1855e0552fbe753b69eeeb222faa282f016"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Dowód i obserwacja

- {"path": "plugins/framecore-work-creative-studio/skills/creative-video-producer/references/production-worksheets.md", "lines": "28,65"}

Raport stanu każe liczyć jako spent tylko linie invoiced lub quoted. Quoted opisuje ofertę, nie poniesiony koszt.

### Skutek i granice

Status produkcji może zawyżyć wydatki, mylić rezerwę z konsumpcją budżetu i prowadzić do błędnej decyzji o dalszych pracach.

### Zalecana zmiana

Rozdziel planned, quoted, committed, incurred/invoiced i paid stosownie do danych; nazwij podstawę raportowanego spent. Nie traktuj oferty ani braków danych jako faktycznego wydatku.

### Odbiór

- Oferta1000PLN bez zlecenia/faktury/płatności daje quoted1000, spent0 gdy wiadomo że nic nie wydano albo Unknown gdy brak danych.
- Faktura i płatność tej samej linii nie są sumowane jako dwa wydatki.
- Raport zachowuje źródło kwoty i osobny plan/rezerwę.

### Weryfikacja

statyczna semantyka arkusza, bez oceny księgowej projektu

**Pełny rekord z reprodukcją:** `evidence/creative/findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-028 · CR-004 · P2

**Uniwersalna naprawa beat-sync usuwa celowy kontrapunkt**

**Typ:** creative_constraint_conflict. **Lokalizacja:** `plugins/framecore-work-creative-studio/skills/hyperframes-workflow/references/motion-quality-direction.md:73`.

**Pewność dowodu:** high: Uniwersalny nakaz widoczny w źródle; żadnego świadomego offsetu faktycznie nie usunięto. **Rewizja:** `[{"repository": "studio", "commit": "d2dbc1855e0552fbe753b69eeeb222faa282f016"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Dowód i obserwacja

- {"path": "plugins/framecore-work-creative-studio/skills/hyperframes-workflow/references/motion-quality-direction.md", "lines": "64,73"}
- {"path": "plugins/framecore-work-creative-studio/skills/creative-music-video-director/references/rhythm-motifs-and-performance-workbook.md", "lines": "14-35"}
- {"path": "plugins/framecore-work-creative-studio/skills/audio-production-director/references/audio-evidence-and-av-handoff.md", "lines": "33,50,57"}

Tabela napraw przenosi działanie pomiędzy beatami na beat i dopuszcza offset tylko dla ruchu wtórnego. Workbook muzyczny jawnie dopuszcza niezależne zegary, opóźnioną reakcję i kontrapunkt; audio dopuszcza autorski offset.

### Skutek i granice

Zaakceptowany ruch prowadzący może zostać zsynchronizowany automatycznie, przez co zmienia się sens i styl utworu. Rygor QA nadpisuje decyzję artystyczną.

### Zalecana zmiana

Rozpoznaj zamierzony offset/niezależny rytm i rzeczywisty błąd synchronizacji przed sugestią. Odnoś ocenę do motion score/briefu; pozwól na N/A i brak usterki zamiast bezwzględnego wymogu różnorodności.

### Odbiór

- Zadany lead gesture300ms po akcencie pozostaje opóźniony; QA sprawdza jego wyraźną intencję i ustalony offset.
- Przypadkowo przesunięty o300ms dźwięk kontaktu jest wykryty względem rzeczywistego zdarzenia.
- Powściągliwy film bez zmian kadru nie otrzymuje nowego cięcia tylko dla podniesienia variety.

### Weryfikacja

statyczny konflikt między aktywnymi references; brak renderu/odsłuchu

**Pełny rekord z reprodukcją:** `evidence/creative/findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-029 · CR-005 · P2

**Globalne podsumowanie oznaczeń UGC usuwa własne wyjątki i Unknown**

**Typ:** internal_policy_summary_conflict. **Lokalizacja:** `plugins/framecore-work-creative-studio/skills/ugc/references/disclosure-by-platform-and-market.md:7`.

**Pewność dowodu:** medium: Wewnętrzna niespójność skrótu z własnymi wyjątkami; bez twierdzenia o aktualnym prawie każdej jurysdykcji. **Rewizja:** `[{"repository": "studio", "commit": "d2dbc1855e0552fbe753b69eeeb222faa282f016"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Dowód i obserwacja

- {"path": "plugins/framecore-work-creative-studio/skills/ugc/references/disclosure-by-platform-and-market.md", "lines": "5-14,21-22,28,37,43"}
- {"path": "plugins/framecore-work-creative-studio/skills/ugc/references/formats-scripts-and-disclosure.md", "lines": "61-65"}

Nagłówek rule everywhere wymaga dwóch oznaczeń dla każdego gift i trzeciego dla realistycznego głosu AI. W tej samej tabeli gift-only TikTok jest Unknown, a YouTube ma wyjątek own cloned voice for dubbing; wiersz PL odróżnia pierwszy niezamówiony prezent.

### Skutek i granice

Skrót może powodować przedstawienie warunkowej albo nierozstrzygniętej reguły jako pewnej i uniwersalnej. Szczegółowe wiersze oraz obowiązek aktualnego researchu istotnie ograniczają skalę, stąd minor.

### Zalecana zmiana

Zmień globalny skrót na matrycę warunków: platforma, rynek, relacja handlowa, typ treści/głosu, organic/paid. Przenieś wyjątki i Unknown do decyzji końcowej.

### Odbiór

- Gift-only TikTok zachowuje Unknown dla toggle do czasu aktualnej weryfikacji.
- Przykład własnego klonowanego głosu przy dubbingu nie ignoruje wierszowego wyjątku YouTube; pozostałe obowiązki bada osobno.
- Brak deklaracji pełnej zgodności prawnej tylko na podstawie tabeli.

### Weryfikacja

wyłącznie wewnętrzna spójność snapshotu; nie ustalano aktualnego stanu prawa ani polityk platform

**Pełny rekord z reprodukcją:** `evidence/creative/findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-030 · CR-006 · P2

**Przykład FrameCut używa nieaktualnej rewizji po align-script**

**Typ:** documented_command_sequence_bug. **Lokalizacja:** `plugins/framecore-work-creative-studio/skills/opencut-video-studio/assets/framecut/README.md:17`.

**Pewność dowodu:** high: Odtworzono poprawne odrzucenie nieaktualnej rewizji z przykładu. **Rewizja:** `[{"repository": "studio", "commit": "d2dbc1855e0552fbe753b69eeeb222faa282f016"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Dowód i obserwacja

- {"path": "plugins/framecore-work-creative-studio/skills/opencut-video-studio/assets/framecut/README.md", "lines": "12-17,36"}
- {"path": "plugins/framecore-work-creative-studio/skills/opencut-video-studio/SKILL.md", "lines": "66"}
- {"path": "plugins/framecore-work-creative-studio/skills/opencut-video-studio/assets/framecut/framecut.py", "lines": "220-242"}
- {"path": "plugins/framecore-work-creative-studio/skills/opencut-video-studio/assets/framecut/fc_core.py", "lines": "395-405"}
- {"path": "evidence/distribution/raw/framecut-doc-repro.log", "lines": "pełny log odczytany"}

README pokazuje align-script --base-revision3, po nim apply --base-revision3. Align zapisuje revision4. Lista mutacji w SKILL pomija align-script. distribution_audit wykonał lokalny syntetyczny repro: align exit0 revision4, apply3 exit2 stale_revision, projekt nadal4.

### Skutek i granice

Czytelnik wykonujący zalecany ciąg zatrzymuje poprawny montaż; sam runtime prawidłowo chroni stan przed konfliktem.

### Zalecana zmiana

Użyj rzeczywiście zwróconej/odczytanej revision, uwzględnij optional alignment w dalszych numerach przykładów i dodaj align-script do listy mutacji. Nie osłabiaj kontroli stale_revision.

### Odbiór

- Cały udokumentowany ciąg z alignment przechodzi z apply na revision4 i następnymi właściwymi ścieżkami.
- Wariant bez alignment nadal przechodzi.
- Stare apply3 po alignment nadal zwraca stale_revision bez mutacji.

### Weryfikacja

trace źródła + odczyt niezależnego lokalnego repro distribution_audit, nie installed-client test

**Pełny rekord z reprodukcją:** `evidence/creative/findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-031 · ASSET-001 · P2

**README myli osiągalność TCP z działającą usługą HTTP**

**Typ:** potwierdzona niespójność dokumentacji. **Lokalizacja:** `open-assets/README.md:34`.

**Pewność dowodu:** high: Jawna ocena domenowego recenzenta; granice dowodu podane w oryginalnym rekordzie. **Rewizja:** `[{"repository": "open-assets", "commit": "b15c35aa54d4efdf809cd3f21416da044ada2281"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Dowód i obserwacja

README radzi po reachable: network is fine; retry lub inny provider/kategoria, a unreachable/unknown tłumaczy awarią/zwolnieniem providera. Funkcja probe sprawdza tylko TCP/CONNECT; brak handshake/aplikacyjnego requestu. Te stany nie wykluczają 401/403/429, CAPTCHA, proxy i lokalnego DNS. Rada pomija wymagany stop i zgodę na zmianę trasy.

Analiza pełnych źródeł. W researchu strona Kenney zwróciła 200, a jawny endpoint download-link 403: sam dostęp do hosta nie wystarcza. Nie jest to dowód wykonania nieautoryzowanego fallbacku.

### Skutek i granice

Użytkownik może dostać błędną diagnozę albo ponowić zabronioną ścieżkę po odczytaniu skróconego README.

### Zalecana zmiana

Zamienić opis na warstwy DNS/TCP/HTTP/prawa/decode; po reachable wykonać wybrane żądanie i respektować jego status oraz bezpieczne reguły skillu.

### Odbiór

Przykłady reachable+HTTP403, reachable+429 i no_dns nie skutkują radą ślepego retry ani stwierdzeniem provider down.

**Pełny rekord z reprodukcją:** `evidence/assets/findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-032 · ASSET-002 · P2

**Dossier Commons przeczy zakresowi potwierdzonych ścieżek w indeksie**

**Typ:** potwierdzona rozbieżność źródeł. **Lokalizacja:** `open-assets/plugins/framecore-open-assets/skills/open-assets/references/providers/commons.md:5`.

**Pewność dowodu:** high: Jawna ocena domenowego recenzenta; granice dowodu podane w oryginalnym rekordzie. **Rewizja:** `[{"repository": "open-assets", "commit": "b15c35aa54d4efdf809cd3f21416da044ada2281"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Dowód i obserwacja

Dossier mówi Only JPEG was tested, indeks wymienia sześć kategorii Commons i dwadzieścia trzy confirmed media paths dla katalogu. Nie ma w tym dossier próbek audio/music/sfx/video ani powiązania z nowszym protokołem testu.

Porównanie pełnych dossier, indeksu, providers.json i docs/VALIDATION.md. Nowa próba audytu potwierdziła tylko search photos Commons i parsowanie CC BY-SA 3.0; audio/wideo Commons w tym zadaniu NOT_RUN.

### Skutek i granice

Nie wiadomo z dokumentacji, które kategorie miały historyczny download/decode. Nie wywodzę z tego niedziałania adaptera.

### Zalecana zmiana

Uzgodnić dossier z datowanym rejestrem provider/category/sample/hash/decode, zachowując NOT_RUN dla brakujących prób.

### Odbiór

Każda deklarowana potwierdzona kategoria ma wskazaną konkretną próbkę albo zostaje opisana jako historycznie nierozliczona/NOT_RUN.

**Pełny rekord z reprodukcją:** `evidence/assets/findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-033 · ROOT-01 · P2

**Zapisana instalacja Studio jest o jedną poprawkę za audytowanym źródłem**

**Typ:** deployment_gap. **Lokalizacja:** `studio/plugins/framecore-work-creative-studio/skills/workflow-orchestrator/SKILL.md`.

**Pewność dowodu:** high: Porównano rzeczywisty zapis z pełną listą 1609 publicznych plików. **Rewizja:** `[{"repository": "studio", "commit": "d2dbc1855e0552fbe753b69eeeb222faa282f016"}, {"saved_release_id": "pluginrel_6ae8e608e2a48191908446eb2bf3ee58", "version": "1.167.0"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Dowód i obserwacja

Repo 1.167.1, saved hosted 1.167.0. Porównano wszystkie1609 publiczne pliki pakietu:1600 identycznych,9 innych,0 brakujących. W odczytanym cloud i executor entrypoincie nadal1.167.0.

### Skutek i granice

Poprawka routingu do zainstalowanych pozycji Toolboxa w1.167.1 nie jest obecna w zapisanej instalacji. Nie jest to dowód wadliwego zapisu ani wszystkich problemów z routingiem.

### Zalecana zmiana

W osobnym wdrożeniu zaktualizować istniejącą tożsamość do zatwierdzonego commitu, zachować prywatne dodatki, wykonać readback i próbę nowej rozmowy.

### Odbiór

Publiczne pliki nowej wersji zgodne z planowanym manifestem, dodatki zachowane, installed entry invocation rzeczywiście dociera do właściwego wykonawcy.

**Pełny rekord z reprodukcją:** `evidence/root-verification/root-findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-035 · ROOT-03 · P2

**Główna gałąź nie ma widocznej ochrony ani wymaganych kontroli**

**Typ:** maintenance_risk. **Lokalizacja:** `GitHub API branches/main oraz rulesets odczytane2026-11-04`.

**Pewność dowodu:** medium: Publiczny odczyt branch/rulesets bez ochrony; ukryte kontrole organizacji pozostają Unknown. **Rewizja:** `[{"repository": "FrameCoreWorks/framecore-works-creative-studio", "configuration_read_date": "2026-11-04", "source": "branches/main and rulesets public API"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Dowód i obserwacja

Public API: protected=false, protection.enabled=false, required_status_checks enforcement_level=off; rulesets=[]. Zdalnie istnieją tylko main i gh-pages. Ostatnie10widocznych workflow success, head source-check success.

### Skutek i granice

Zielone CI nie wymusza przejścia kontroli przed każdą zmianą main. Reguły AGENTS i lokalne hooki nie stanowią serwerowej ochrony przed przypadkowym force push lub usunięciem.

### Zalecana zmiana

Rozważyć serwerową blokadę force push/usunięcia oraz ochronę zgodną z przyjętą pracą bezpośrednio na main. Nie narzucać procesu PR sprzecznego z decyzją właściciela.

### Odbiór

Odczyt konfiguracji potwierdza wybrane ograniczenia przy zachowaniu dozwolonego fast-forward na main; żadnego testowego force push.

**Pełny rekord z reprodukcją:** `evidence/root-verification/root-findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-036 · ROOT-04 · P2

**Przypięte Pillow12.3.0 jest objęte opublikowanym advisory Ghostscript**

**Typ:** dependency_advisory. **Lokalizacja:** `studio/requirements-ci.txt:3`.

**Pewność dowodu:** high: Pin mieści się w zakresie oficjalnego advisory; osiągalność exploita na podatnym runtime niewykonana. **Rewizja:** `[{"repository": "studio", "commit": "d2dbc1855e0552fbe753b69eeeb222faa282f016"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Dowód i obserwacja

Oficjalne GHSA-w889-685w-c8fh: affected2.6.0–12.3.0, patched13.0.0. Dotyczy EPS i argumentów ścieżki przekazywanej do Ghostscript. image_probe.py:277–279 otwiera i ładuje przekazany path bez wcześniejszej normalizacji. Lokalny host audytu maPillow13.0.0; nie odtworzono exploita na12.3.0.

### Skutek i granice

Potwierdzona zgodność pinu z zakresem advisory; praktyczny wpływ wymaga określonego EPS, nazwy pliku i Ghostscript. Nie wykazano ataku na repo ani działania podatnej wersji w bieżącej sesji.

### Zalecana zmiana

Podnieść wspierany pin po sprawdzeniu kompatybilności, normalizować ścieżki i ograniczać dekodery do faktycznie obsługiwanych formatów w punktach niezaufanego wejścia.

### Odbiór

Pin znajduje się poza affectedrange, aktualne suite przechodzą na zadeklarowanych wersjach; test nazw względnych i EPS nie przekazuje opcji jako nazwy wejścia.

**Źródło zewnętrzne:** https://github.com/python-pillow/Pillow/security/advisories/GHSA-w889-685w-c8fh

**Pełny rekord z reprodukcją:** `evidence/root-verification/root-findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-038 · INSTALL-02 · P2

**Poprawny JSON o błędnym kształcie przerywa finder wyjątkiem zamiast kontrolowanego wyniku**

**Typ:** input_contract_gap. **Lokalizacja:** `studio/plugins/framecore-work-creative-studio/skills/workflow-orchestrator/assets/skill-finder/find_skills.py:87`.

**Pewność dowodu:** high: Trzy niewłaściwe struktury poprawnego JSON odtworzyły nieprzechwycony wyjątek. **Rewizja:** `[{"repository": "studio", "commit": "d2dbc1855e0552fbe753b69eeeb222faa282f016"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Dowód i obserwacja

Bezpieczny mock fetch zwraca [] albo skills zawierające string. search() wywołuje .get bez sprawdzenia typu, a main() nie obsługuje AttributeError. Reprodukcja i trzy wyniki: evidence/installation/probe_finder.py oraz finder-malformed-response.json. Live search typography działał i zwrócił trzy wyniki; nie jest to obecna awaria usługi.

### Skutek i granice

Zmiana kontraktu API lub nietypowa odpowiedź przerywa normalną ścieżkę offline/fallback. Nie wykazano wykonania kodu, zapisu ani utraty danych.

### Zalecana zmiana

Walidować typ root, skills i obiektów wynikowych oraz zwracać kontrolowany błąd kontraktu. Nie używać ogólnego catch maskującego inne błędy programu.

### Odbiór

Zła składnia oraz trzy niezgodne kształty JSON prowadzą do jawnego statusu błędu bez tracebacku; prawidłowy pusty katalog pozostaje none; poprawne wyniki zachowują źródło i werdykt.

### Weryfikacja

LOCAL_MOCK_REPRODUCED, bez sieci w reprodukcji.

**Pełny rekord z reprodukcją:** `evidence/installation/findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-039 · INSTALL-03 · P2

**Commit tekstu, licencja, audyt katalogu i komenda instalacji nie tworzą jednego przypiętego dowodu**

**Typ:** provenance_gap. **Lokalizacja:** `studio/plugins/framecore-work-creative-studio/skills/workflow-orchestrator/assets/skill-finder/find_skills.py:168`.

**Pewność dowodu:** high: Prześledzono różne rewizje/wiązania źródeł; nie wykazano ataku ani zmiany licencji konkretnego wyniku. **Rewizja:** `[{"repository": "studio", "commit": "d2dbc1855e0552fbe753b69eeeb222faa282f016"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Dowód i obserwacja

read_skill przypina SKILL.md do rozwiązanego commitu, lecz LICENSE_URL odczytuje bieżącą domyślną gałąź bez ref. Oceny katalogu zawierają daty, bez sprawdzonego związku z tym commitem. Generowana komenda używa nieprzypiętego npx skills i owner/repo. Live próba zwróciła ready dla better-typography @60bf140e43c98b248e6594487384ec967e89d98a z MIT, ale nie porównano licencji i audytu do tego commitu.

### Skutek i granice

Po zmianie upstream oceniona treść, podana licencja i faktycznie później instalowane pliki mogą dotyczyć różnych wersji. Nie wykazano rzeczywistej zmiany licencji ani złośliwego upstream; listed pozostaje wynikiem ograniczonej oceny katalogu, a nie gwarancją bezpieczeństwa.

### Zalecana zmiana

Czytać licencję i wszystkie wymagane zasoby przy tym samym commit, zapisywać datę i zakres audit receipt, wskazywać Unknown dla zgodności audytu z rewizją. Bezpośrednio przed zapisem porównać zatwierdzony inventory z finalnym pakietem. Jawnie przypiąć lub ponownie sprawdzić narzędzie i źródło lokalnej instalacji.

### Odbiór

Mock zmiany HEAD po review nie zmienia zawartości instalowanej z zatwierdzonego manifestu. Licencja pochodzi z tego samego ref; brak rewizji w ocenie bezpieczeństwa nie jest komunikowany jako audyt bieżącego commitu.

### Weryfikacja

SOURCE_CONFIRMED oraz live search/describe/read; żadnej instalacji ani potwierdzonego exploita.

**Pełny rekord z reprodukcją:** `evidence/installation/findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-041 · UPSTREAM-02 · P2

**Animate saved gallery silently omits Riso because its sample PNG is missing**

**Typ:** Brak zasobu zapisanej paczki. **Lokalizacja:** `plugins/animate/skills/animate/SKILL.md:11; plugins/animate/skills/animate/SKILL.md:18; plugins/animate/skills/animate/SKILL.md:29; plugins/animate/skills/animate/tools/gallery.mjs:21`.

**Pewność dowodu:** high: Brak PNG i kod filtra potwierdzone; galeria nie była renderowana. **Rewizja:** `[{"repository": "cth9191/animate", "commit": "7e5eb56feb2dd573f890e1b7b34748af43d58263"}, {"saved_release_id": "pluginrel_6ae437c5eb10819192f2351b0e74ec2b"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Dowód i obserwacja

Of 107 public selected-folder files, 106 appear in the complete saved inventory. Missing: styles/riso/sample.png, 1,321,993 bytes, blob 871933b3a266a708258d395ec9808bbb4813a4b3. Saved gallery.mjs byte-matches the pin; line 21 lists only style directories having sample.png.

Compare the seven ORDER names against saved sample.png paths: only riso is absent. Source-guided filter reproduction, not rendered-gallery test.

### Skutek i granice

The prescribed intake gallery cannot show Riso and has six shipped style tiles rather than seven. Riso code and demo paths remain present. This does not establish that every Animate render fails.

Other resource bytes and rendering remain untested.

### Zalecana zmiana

Restore and hash-check the exact pinned PNG, then verify all seven gallery tiles in an authorized runtime trial.

### Weryfikacja

STATIC_INVENTORY_FILTER_REPRODUCTION; NO_GALLERY_RENDER_EXECUTED

**Pełny rekord z reprodukcją:** `evidence/installation/upstream-findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-004 · SEC-004 · P3

**Open Assets używa ruchomych major tagów akcji CI**

**Typ:** ci_hardening. **Lokalizacja:** `open-assets/.github/workflows/ci.yml:19`.

**Pewność dowodu:** high: Jawna ocena domenowego recenzenta; granice dowodu podane w oryginalnym rekordzie. **Rewizja:** `[{"repository": "open-assets", "commit": "b15c35aa54d4efdf809cd3f21416da044ada2281"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Warunki

- Uruchomienie workflow CI.

### Dowód i obserwacja

actions/checkout@v6 i actions/setup-python@v7 nie są przypięte do SHA, w odróżnieniu od Studio i Toolbox. permissions contents:read i persist-credentials:false ograniczają skutki. Brak dowodu złośliwej akcji lub wycieku.

Odczyt .github/workflows/ci.yml.

### Skutek i granice

Zmiana major taga wykonuje inny kod w kolejnym CI bez zmiany repozytorium.

### Zalecana zmiana

Przypiąć akcje do przejrzanych pełnych commitów z komentarzem wersji i procesem aktualizacji.

### Odbiór

Każdy zewnętrzny uses w tym workflow ma pełny SHA; zachowane read-only permissions i persist-credentials:false.

### Weryfikacja

Static analysis; remote CI NOT_RUN

**Pełny rekord z reprodukcją:** `evidence/security/findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-007 · DIST-003 · P3

**Dwa companion plugins przekraczają limit listing shortDescription**

**Typ:** listing_metadata_constraint. **Lokalizacja:** `studio/plugins/brand-kit/plugin.json:25; studio/plugins/brand-kit/.codex-plugin/plugin.json:23; studio/plugins/voice-narration/plugin.json:25; studio/plugins/voice-narration/.codex-plugin/plugin.json:23`.

**Pewność dowodu:** high: Zmierzono długość i porównano odczytany limit; rzeczywistego odrzucenia przez backend nie próbowano. **Rewizja:** `[{"repository": "studio", "commit": "d2dbc1855e0552fbe753b69eeeb222faa282f016"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Dowód i obserwacja

Plugin Creator wymaga maksymalnie 30 znaków dla interface.shortDescription. Brand Kit ma 42, Voice And Narration 41. Obie projekcje Codex zachowują te same za długie wartości. Jest to udowodniona niezgodność z aktualnymi component requirements, bez twierdzenia o odtworzonym odrzuceniu przez zdalny backend. Ich package_test.py testuje głównie name/version i displayName, pomijając długość listing subtitle.

- evidence/distribution/raw/component-audit.json
- evidence/distribution/raw/component-audit.log
- evidence/distribution/raw/portable-subtitle-requirement.txt

### Zalecana zmiana

Skrócić dwa subtitles do najwyżej 30 znaków, zsynchronizować overlays i dodać wspólny component validation dla wszystkich własnych paczek.

### Odbiór

Wszystkie 6 własnych pluginów przechodzą parse JSON/YAML, limit 30, zgodność prezentacji oraz inventory; fixture przekraczający 30 znaków jest odrzucany.

**Pełny rekord z reprodukcją:** `evidence/distribution/findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-013 · ORCH-05 · P3

**Wycofany alias audio podaje nieaktualny powód zachowania plików**

**Typ:** bug. **Lokalizacja:** `studio/plugins/framecore-work-creative-studio/skills/producer-ai-task-builder/SKILL.md:12; studio/AGENTS.md:70`.

**Pewność dowodu:** high: Stare uzasadnienie porównano z aktualnym kontraktem; zachowanie aliasu jest celowe. **Rewizja:** `[{"repository": "studio", "commit": "d2dbc1855e0552fbe753b69eeeb222faa282f016"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Dowód i obserwacja

- **method:** Porównanie aliasu i trzech jego references z aktualnymi zasadami AGENTS.
- **observed:** Te same stwierdzenia cannot delete files pozostały w trzech pointer references.

### Skutek i granice

Błędne wyjaśnienie możliwości narzędzia; alias prawidłowo przekierowuje do Audio Production i ma allow_implicit_invocation=false.

### Zalecana zmiana

Opisać kompatybilność i regułę ochrony ścieżek jako powód zachowania, bez usuwania plików.

### Odbiór

- Alias i references wskazują utrzymywany owner; nie twierdzą, że narzędzie nie potrafi usuwać.
- Inwentarz pakietu pozostaje identyczny.

### Weryfikacja

SOURCE_CONFIRMED

**Pełny rekord z reprodukcją:** `evidence/orchestration/findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-014 · ORCH-06 · P3

**Odzyskać niewielki zapas w entrypoincie bez zmiany startupu**

**Typ:** proposal. **Lokalizacja:** `studio/plugins/framecore-work-creative-studio/skills/workflow-orchestrator/SKILL.md:1`.

**Pewność dowodu:** medium: Zapas 14 bajtów zmierzony; korzyść proponowanego skrótu nie była zmierzona. **Rewizja:** `[{"repository": "studio", "commit": "d2dbc1855e0552fbe753b69eeeb222faa282f016"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Dowód i obserwacja

- **command:** Path(SKILL.md).stat().st_size
- **observed:** 31986

### Skutek i granice

Nie jest naruszeniem limitu ani samodzielnym dowodem jakości. Mały zapas utrudnia dodanie najmniejszej uzasadnionej poprawki bez przenoszenia treści.

### Zalecana zmiana

Przy następnej rzeczywistej poprawce odsunąć powtórzoną koordynacyjną informację do już istniejącego reference; nie skracać chronionych welcome ani językowej projekcji.

### Odbiór

- Byte-match obu welcome i language policy pozostaje PASS.
- Scenariusze direct-task/resume i menu nie zmieniają zachowania.

### Weryfikacja

MEASURED_SOURCE

**Pełny rekord z reprodukcją:** `evidence/orchestration/findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-016 · ORCH-08 · P3

**Open Assets dokumentuje flagi envelope dla komend, które ich nie obsługują**

**Typ:** bug. **Lokalizacja:** `open-assets/plugins/framecore-open-assets/skills/open-assets/references/contract.md:25; open-assets/plugins/framecore-open-assets/scripts/runtime.py:297`.

**Pewność dowodu:** high: Dokumentacja flag i parser CLI są rozbieżne w wymienionych komendach. **Rewizja:** `[{"repository": "open-assets", "commit": "b15c35aa54d4efdf809cd3f21416da044ada2281"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Dowód i obserwacja

- **command:** python3 -B open-assets/plugins/framecore-open-assets/scripts/runtime.py domains --envelope-out /tmp/orch-never-written.json
- **exit_code:** 2
- **observed:** error: unrecognized arguments: --envelope-out /tmp/orch-never-written.json
- **network_used:** False

### Skutek i granice

Adapter kierujący się dosłownie kontraktem dostaje błąd argumentów podczas read-only preflight; Studio registry słusznie ogranicza przyjmowane envelope do status/search/verify/download.

### Zalecana zmiana

Doprecyzować dokumentację do czterech komend albo jawnie dodać spójne envelope dla domains/reach. Wybrać najmniejszą zmianę zgodną z zakresem produktu.

### Odbiór

- Dokumentowane komendy i --help są zgodne; domains/reach nie sugerują nieistniejących flag.

### Weryfikacja

LOCAL_CLI_REPRODUCED

**Pełny rekord z reprodukcją:** `evidence/orchestration/findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-017 · ORCH-09 · P3

**Instrukcja klientowego delivery przypisuje generator spisu walidatorowi manifestu**

**Typ:** bug. **Lokalizacja:** `studio/plugins/framecore-work-creative-studio/skills/delivery-documentation/references/client-handoff.md:9; studio/plugins/framecore-work-creative-studio/skills/delivery-documentation/scripts/asset_manifest.py:182`.

**Pewność dowodu:** high: Sprawdzono rzeczywisty interfejs skryptu i instrukcję klientową. **Rewizja:** `[{"repository": "studio", "commit": "d2dbc1855e0552fbe753b69eeeb222faa282f016"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Dowód i obserwacja

- **method:** Odczyt parsera CLI oraz pól return validate()/impact().
- **observed:** Brak operacji tworzącej spis plików, size/duration/colour space/intended use.

### Skutek i granice

Niewielka przeszkoda wykonawcza: model musi ręcznie przygotować spis, choć link sugeruje gotową funkcję.

### Zalecana zmiana

Zmienić wording na ręczny spis z manifestu, a skrypt opisać jako walidator; nie dodawać niepotrzebnego nowego generatora.

### Odbiór

- Użytkownik/helper potrafi wykonać opisany krok istniejącą komendą lub jawną instrukcją ręczną.

### Weryfikacja

SOURCE_CONFIRMED

**Pełny rekord z reprodukcją:** `evidence/orchestration/findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-020 · LEARN-03 · P3

**Dokumentacja nauki wskazuje usunięty skrót motion i nieprawidłowe liczniki**

**Typ:** confirmed_documentation_drift. **Lokalizacja:** `plugins/framecore-work-creative-studio/docs/learning-mode.md:8`.

**Pewność dowodu:** high: Jawna ocena domenowego recenzenta; granice dowodu podane w oryginalnym rekordzie. **Rewizja:** `[{"repository": "studio", "commit": "d2dbc1855e0552fbe753b69eeeb222faa282f016"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Dowód i obserwacja

- Dokument opisuje trzeci skrót do motion preselecting creation, podczas gdy opcja 3 aktualnie oznacza skill search.
- Linia 56 mówi o 24 scenariuszach; suite zawiera 29, a jego scope mówi Twenty-five.
- Zdanie o obowiązkowym ujawnieniu ograniczenia w pierwszej lekcji offline jest szersze niż aktualne learning-mode.md: disclosure dopiero przy realnym research trigger.

### Skutek i granice

Nowy użytkownik lub maintainer dostaje błędne wskazówki nawigacji i zakresu weryfikacji.

### Zalecana zmiana

Uaktualnić dokumentację zgodnie z aktywnym kontraktem; licznik generować albo usunąć, jeśli nie wnosi decyzji użytkownika. Nie zmieniać historycznych release notes.

### Odbiór

- Dokumentacja nie opisuje opcji 3 jako motion.
- Wszystkie bieżące liczniki są zgodne z suite albo zastąpione odnośnikiem.
- Offline stable-craft nie wymaga nieistotnego research disclaimer.

**Pełny rekord z reprodukcją:** `evidence/learning/findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-024 · LEARN-07 · P3

**Rozwój powinien kalibrować zadania i ocenę, nie dodawać od nowa mechanizmów mentoringu**

**Typ:** development_proposal. **Lokalizacja:** `plugins/framecore-work-creative-studio/skills/workflow-orchestrator/assets/learning-domains.json:30`.

**Pewność dowodu:** design_inference: Jawna ocena domenowego recenzenta; granice dowodu podane w oryginalnym rekordzie. **Rewizja:** `[{"repository": "studio", "commit": "d2dbc1855e0552fbe753b69eeeb222faa282f016"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Dowód i obserwacja

- Istnieje 14 domen, ćwiczenie no-render i 2–3 kryteria w każdej, granice wsparcia oraz odpowiedzialni specjaliści.
- Mapa jest indeksem dziedzin, nie pełnym grafem kompetencji z progami i przykładami ocen.
- Przykład static_graphics: ćwiczenie trzech miniatur plakatu obok kryterium rozróżnienia logo concept/production master. Tak szerokich kryteriów domeny nie należy automatycznie przypisywać każdej próbie.
- W repo istnieją gotowe przykłady upstream, ale mają historycznych właścicieli i warunki; roadmap dopuszcza wyłącznie przemyślaną adaptację, nie bulk import.

### Skutek i granice

Bez kalibracji dynamiczne kursy mogą mieć zmienną trudność lub oceniać wiedzę, której zadanie nie wywołuje. To uzasadniona propozycja rozwoju, nie wykazana wada odpowiedzi modelu.

### Zalecana zmiana

Zaadaptować 2–3 zwarte pełne sekwencje kreatywne: bodziec, próba, pomoc, poprawka i transfer; dołączyć różne poprawne rozwiązania i kotwice oceny. Utrzymać istniejące owner IDs i Project State.

### Odbiór

- Każde kryterium ocenianej próby ma widoczny dowód możliwy do wytworzenia przez zadanie.
- Dwa różne uzasadnione wybory artystyczne mogą przejść te same kryteria.
- Podniesienie poziomu oznacza zmianę problemu/ograniczeń, nie wyłącznie dłuższą odpowiedź.

**Pełny rekord z reprodukcją:** `evidence/learning/findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-034 · ROOT-02 · P3

**Instalacja pojawia się daleko po ciężkiej galerii README**

**Typ:** usability_proposal. **Lokalizacja:** `studio/README.md:3`.

**Pewność dowodu:** medium: Układ i masa plików zmierzone; wpływ na onboarding użytkowników i transfer niezmierzony. **Rewizja:** `[{"repository": "studio", "commit": "d2dbc1855e0552fbe753b69eeeb222faa282f016"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Dowód i obserwacja

Rzeczywisty desktop GitHub: article838px szerokości,3833px wysokości, Install2866px od początku artykułu. Wszystkie obrazy się wczytały. Sześć GIFów w źródle sumuje27680150bajtów. To nie pomiar transferu ani Core Web Vitals. Mobile NOT_RUN.

### Skutek i granice

Nowy użytkownik przewija obszerną prezentację zanim znajdzie instrukcję rozpoczęcia. Alt text i nagłówki są poprawne, grafika działa.

### Zalecana zmiana

Umieścić krótkie wejście Install i wybór hosta przy pierwszym opisie. Zachować jeden główny przykład, resztę galerii przenieść niżej lub do osobnej strony. Rozważyć lekkie statyczne postery z linkiem doMP4.

### Odbiór

Droga do instalacji widoczna przy pierwszym opisie na desktopie i telefonie; zmierzony mniejszy ciężar mediów, zachowane materiały i ich pochodzenie.

**Pełny rekord z reprodukcją:** `evidence/root-verification/root-findings.json` / `Ustalenia-audytu.json`.

## CW-AUD-042 · UPSTREAM-03 · INFO

**Motion Designer active entry normalizes invalid upstream YAML; body is unchanged**

**Typ:** Informacja o zapisanej paczce. **Lokalizacja:** `skills/motion-designer/SKILL.md:3; skills/motion-designer/SKILL.md:13; skills/motion-designer/reference/harness.md:9; skills/motion-designer/reference/setup.md:14`.

**Pewność dowodu:** high: Porównano pełne aktywne i oryginalne entry, poprawny YAML i identyczne body. **Rewizja:** `[{"repository": "kaventro/motion-designer", "commit": "7d0b8bb78ddd2c91c57db9d1e83fcf711304bdb8"}, {"saved_release_id": "pluginrel_6ae437cf77d081918028494aaa6407bd"}]`. Efekt zalecenia nie został zmierzony po wdrożeniu.

### Dowód i obserwacja

Pinned source description has unquoted colon-space and fails standard YAML parsing. Current active SKILL.md adds exactly two quote bytes around description: 14,388 versus 14,386 bytes. Active YAML parses and exact post-frontmatter body hashes match. Parent evidence installed-motion-skill.json preserves the original under provenance/original-skills/motion-designer/SKILL.md.

Parse complete upstream and active frontmatters and compare exact bodies. No native loader rejection was attempted.

### Skutek i granice

There is no current saved-entry YAML failure. A byte-for-byte reinstall from the same source would reintroduce the format issue; unchanged-body status must be distinguished from metadata normalization.

Historical normalization approval and fresh-conversation activation are Unknown/NOT_RUN.

### Zalecana zmiana

Record transparent frontmatter-only normalization and retain original provenance; adopt a valid upstream pin when available. Do not rewrite the body or infer missing historical permission.

### Weryfikacja

FULL_UPSTREAM_AND_ACTIVE_ENTRY_HASH_COMPARE; STANDARD_YAML_PARSE

**Pełny rekord z reprodukcją:** `evidence/installation/upstream-findings.json` / `Ustalenia-audytu.json`.
