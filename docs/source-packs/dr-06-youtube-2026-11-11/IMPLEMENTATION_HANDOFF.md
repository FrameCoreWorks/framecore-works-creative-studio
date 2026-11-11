# DR-06 — przekazanie do analizy architekta

**Status: research i propozycje DERIVED.** Claude pozostaje architektem. Ten pakiet nie oznacza jego recenzji, akceptacji, wdrożenia FrameMotion/FrameCut ani wykonania benchmarków. Nie uruchamiano Claude CLI (znany wcześniejszy OAuth 401); brak fallbacku na inny model. Nie wysyłano wiadomości do innych czatów. Katalog wyników jest materiałem do odczytu przez wątek nadrzędny.

## Najważniejsze ustalenie

Docelowy pipeline powinien umieć odtworzyć edytowalną scenę z kodu, przypiętych assetów i czasu. Biblioteka postaci oraz ujęć musi obsługiwać oryginalną historię. Najmocniejsze znalezione publiczne kody dotyczą warstwy animacji explainerów i symulacji. Najbliższą serią fabularną jest Milo, lecz pełny code-based workflow jest deklaracją autora, bez opublikowanego repo. Klasyczne filmy zachowano jako materiał do analizy dramaturgii, póz, przestrzeni i ciągłości.

## Zweryfikowana baza i granice

Trzy publiczne repozytoria, SHA i data odczytu są w [baseline/BASELINE.md](baseline/BASELINE.md) i [repositories.json](baseline/repositories.json). Obecny punkt odniesienia FrameCut znajduje się w skillu opencut-video-studio w Creative Studio; nowych repozytoriów oddzielnych produktów nie podano. Nie tworzyć adresów ani twierdzeń o ich API.

W bazie istnieją: kontrakty task request/result v1, zamknięty top-level framecut.project/v1, wymierny FPS, rewizje i typed edit operations, Asset Manifest, przekazanie Earshot oraz sidecary Open Assets. Propozycja odcinka ma być **sidecarem**, a nie dopisaniem dowolnych kluczy do zamkniętego obiektu projektu. [Dokładny projekt danych i fixture](baseline/CONTRACTS.md).

## Proponowany przepływ

Creative Studio utrzymuje brief, biblię, scenariusz, karty tez, storyboard i decyzje. FrameMotion w proponowanej roli otrzymuje specyfikacje ujęć i zwraca lokalne rendery z receipt. FrameCut jako jedyny właściciel master timeline przyjmuje wersjonowane operacje i składa obraz, dialog, muzykę, SFX oraz napisy. Open Assets/Toolbox dostarcza zasoby i analizy z prawami, hashem i parametrami.

Lokalny czas ujęcia należy do renderera; jego pozycja w odcinku do mastera. Agent nie przesuwa całego filmu przez zmianę lokalnej kompozycji. Wszelkie zmiany zależne od pozycji niosą base_revision/hash. Stale base jest odrzucana. Czas zapisuje się całkowitymi klatkami i fps num/den; audio przez granice próbek, z jednym jawnym sposobem zaokrąglenia.

Właściciel assetu kontroluje tożsamość, rig, garderobę i licencję. Scenarzysta dokładny tekst oraz wersję kwestii. Sound zatwierdzony take i głos. Montażysta master. QA odczytuje finalny plik, nie jedynie receipt renderera. Rola nie wymaga osobnego agenta.

## Backlog do decyzji architekta

| Priorytet / ID | Praca i uzasadnienie | Dowód ukończenia |
|---|---|---|
| P0-01 | Wybrać jeden lokalny renderer 2D i jeden profil outputu dla krótkiej sceny; kandydaci SVG/Remotion/HyperFrames po sprawdzeniu hosta i licencji. Nie wdrażać sześciu adapterów naraz. | B01/B04 wykonane na rzeczywistych plikach; render i import do obecnej bazy potwierdzone. |
| P0-02 | Dodać wersjonowany sidecar odcinka i walidator zależności bez zmiany istniejących kontraktów task/project. | Round-trip starego projektu i nowego sidecara, błędne id/rev/FPS/rights odrzucane, dowód zgodności historycznej. NOT_RUN. |
| P0-03 | Jedyny master, lokalne kompozycje, render handles, source/timeline ranges i audio rounding. | B04 na 24/1 oraz 24000/1001; brak narastającego driftu i cichego ripple; stale revision rejected. |
| P0-04 | Biblia 2 postaci, nazwy kontrolek, 3 widoki i continuity_in/out. | B01/B02 z przekazaniem rekwizytu; zero niewyjaśnionych zmian. |
| P0-05 | Per-line exact text/voice/take + fonetyczny słownik PL, napisy z finalnej wersji. | Odsłuch i inspekcja ust, błędna fleksja/nazwa naprawiona w osobnej rewizji. |
| P0-06 | Dirty DAG, cache keys, bounded retry i wznowienie po job_id/hash; jawny budżet. | B04 dowodzi re-use niezależnego ujęcia, odrzuca cudzą rewizję i nie uruchamia cichego provider fallbacku. |
| P0-07 | Delivery gate: pełny seans/odsłuch, media probe/decode, prawa, audience/disclosure. | B05 oraz pakiet wydania, bez otwartych blockerów; osobna decyzja właściciela o publikacji. |
| P1-01 | Adapter Manim/symulacji do explainera z dowodami tez i jednostek. | B03, spójność danych/VO/grafiki, wersja kodu i seed. |
| P1-02 | Biblioteka póz/gestów/cykli i testy regresji riga na klatkach ryzyka. | Nowy odcinek używa biblioteki z odrębną historią, poprawka riga pokazuje listę wpływu. |
| P1-03 | Telemetria pracy/renderu/retry oraz raport kosztu pilota i epizodu 2. | Faktycznie zmierzone godziny, koszt i cache; aktualizacja ECONOMICS. |
| P1-04 | Lokalizacja językowa i ponowny conform przy zmianie długości dialogu. | Wersja PL zachowuje nazwy, meaning i synchronizację; odrębny master rev. |
| P2-01 | Stylizowany 3D adapter Blender Python i kolejka zasobów CPU/GPU. | B02/B05, pamięć i czas zmierzone; brak założenia, że krótki demo render skaluje się na serial. |
| P2-02 | Ograniczony generatywny insert z kontrolowanym bohaterem i dźwiękiem w osobnych warstwach. | Test 2 sąsiednich cięć, jawne odrzuty/koszt/zgody; możliwość powrotu do lokalnego ujęcia. |
| P2-03 | Większa biblioteka serii i sezonowy audit różnorodności historii. | Co najmniej 3 odmienne łuki odcinków oraz czytelna pamięć stanu świata. |

## Co architekt ma rozstrzygnąć

1. Który format pilota spośród [trzech propozycji](ORIGINAL_FORMATS.md) najlepiej weryfikuje główne ryzyko produktu.
2. Gdzie przechować sidecar i kto publikuje master revision; czy obecny cache rozróżnia render lokalny od montażowego placementu.
3. Który adapter ma już działający readiness hosta i jaki minimalny fixture potwierdzi import/render.
4. Jakie progi ręcznej akceptacji obrazu, polskiej mowy i czasu pracy obowiązują dla pilota.

## Otwarte luki i sugerowany następny zakres

Pełne oglądanie/odsłuch referencji, tempo cięć, miks oraz lipsync pozostają nieweryfikowane. Katalog zawiera Unknown długości/dat/metryk; szczegółowe liczby w [COVERAGE](catalog/COVERAGE.md). Nie ma empirycznego czasu produkcji ani odsetka odrzuceń. Nie wykazano kompletnego otwartego code-based serialu dialogowego z cache i zmianą kwestii; to właśnie ryzyko do zbadania.

Po decyzji architekta osobne zadanie może wykonać B01–B04 lokalnie w dozwolonym projekcie i dopiero potem pełny pilot. Ten handoff sam nie autoryzuje płatnych usług, uploadu, instalacji, zmiany repozytorium ani publikacji.

## Lekcja do ewentualnego wspólnego dziennika

Propozycja do zatwierdzenia, bez zapisu do Shared: oddzielać **co tworzy kod** od **siły dowodu**. Publiczny silnik animacji, repo symulacji, opis autora i finalny master dają różne zakresy potwierdzenia. Dowód: Milo (deklaracja), 3Blue1Brown/Reducible (sceny kodowe), Primer (repo + opis odcinka), devlogi (kod elementu filmu). Model/request/observed oraz rzeczywiste przypisania są w [SWARM.md](SWARM.md).
