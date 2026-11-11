# Macierz pokrycia, istniejącego kodu i luk

Data: 2026-11-11. „Potwierdzone” zawsze zawiera zakres dowodu. Ten research nie wykonuje natywnych renderów ani nie potwierdza działania zainstalowanej wtyczki. Części kompendium tworzą jeden pakiet; lokalna luka pojedynczego specjalisty może zostać zamknięta wskazanym dowodem innego specjalisty.

## Oryginalny prompt → dostarczony artefakt

| Wymaganie | Pokrycie / praktyczny wynik | Dowód | Luka lub granica |
|---|---|---|---|
| Metoda, 40+ wartościowych źródeł jako cel | Rejestr JSON/CSV, ID, autor, data/Unknown, locator, decyzja, limitation, test | Rzeczywiste odczyty dokumentacji i kodu; źródła z różnych domen | Liczba URL nie oznacza niezależnych potwierdzeń; aliases/duble identyfikowane |
| Około 100 terminów PL/EN | 100 haseł w specialists/craft/GLOSSARY.md | Źródło/kontekst + autorskie przykłady | Nie jest to normatywny słownik terminologiczny |
| A. Reżyseria ruchu | CRAFT A + PROFESSIONAL-WORKFLOWS | Adobe, IBM, Toon Boom, własna synteza | Brak badania skuteczności reklamy |
| B. Model AE | CRAFT B: comp/precomp/parent/null/anchor/shapes/paths/matte/blend/order/collapse | Dokładne sekcje Adobe | Natywne AE fixtures NOT_RUN; sprzeczność matte ujawniona |
| C. Keyframes/krzywe/expressions | CRAFT C + CODE-AND-CONTRACTS | Adobe/API, własna matematyka | Wykres wartości ≠ speed; parametry różnych programów nie identyczne |
| D. Obraz/compositing | CRAFT D, R08–R18 według indeksu receptur, professional supplement | Adobe, Blender raw manual, Fusion guide, Foundry, SideFX | Roto/keying/tracking i subframe render NOT_RUN |
| E. Tekst/dźwięk | CRAFT E, RECIPES, QA B02/B05, backend fonts/sync | Adobe/Apple/librosa/Studio source | Brak oglądania/odsłuchu; fonty benchmarków nie dostarczone |
| F. Proces profesjonalny | PROCESS-AND-TUTORIALS, handoff/revision/locks | Relacje autorów + oryginalny workflow | Transkrypcja nie jest obejrzanym breakdownem |
| 15–20 receptur | 18 pełnych R01–R18 | Każda ma problem, use/avoid, assety, build, parametry, błędy, repair, code, QA, źródła | Receptury DERIVED, nie zrealizowane natywnie |
| Zadaniowe porównanie backendów | 10 rodzin w BACKENDS | Dokumentacja/API i konkretne source files | Brak instalacji i pomiaru wydajności |
| Technika → kod + fidelity | 22 mapowania w BACKENDS | Wierny/przybliżony/hybrydowy/brak odpowiednika w określonym zakresie | Wierny nie znaczy pixel-identical AE |
| Scene/dependency graph, keyframes, mask/camera/text/cues | CODE-AND-CONTRACTS + examples | Oryginalna propozycja; struktura i analityka własnym skryptem | Proponowany sidecar NOT_IMPLEMENTED; core schema nie pełne API |
| Determinism/seek/bake/font/cache/CPU/GPU/resume | BACKENDS + PROFESSIONAL-WORKFLOWS + P0/P1 backlog | Pinned code, manuale i własna synteza | Cross-platform bitwise parity Unknown |
| Źródła adaptacji, konkretne repo pliki/licencje | REPOSITORIES | Pinned SHA/tag i odczyt wybranych plików | Asset/font/model rights oddzielnie; nie pobierano bibliotek do użycia |
| Kontrakty współpracy | STUDIO-AUDIT + CODE-AND-CONTRACTS | motion-score i FrameCut request/bind actual code | Nie znany adres nowych repo; żadnego zatwierdzenia architektury przez Claude |
| Benchmarki: logo/type/product/2.5D/music | 5 w QA-BENCHMARKS | Syntetyczne dane, jawne kryteria i błędy | Render/realtime/listening NOT_RUN |
| 16:9 oraz 9:16 | Każdy benchmark ma własną adaptację | DERIVED layout proposals | Nie używać jako gotowych placement safe zones |
| Stan obecnej wtyczki | Tabela poniżej + STUDIO-AUDIT | Publiczny main i lokalny odczyt skilla | Instalacja/załadowanie/realne działanie nie utożsamione |
| Backlog P0/P1/P2 + handoff | 12 zadań w IMPLEMENTATION_HANDOFF | Owner/input/output/deps/files/limits/fallback/tests/errors/retry/cost | Nie autoryzuje wdrożenia |
| Niezależna recenzja i weryfikacja | REVIEW.md, review/, verify_research.py, VERIFICATION.json | Recenzja pakietu + własne testy strukturalne/analityczne | Nie recenzja Claude; brak native/media proof |

## Stan implementacji — trzy osobne kategorie

| Obszar | Potwierdzone w **publicznym Studio** | Luka względem propozycji | Unknown w działającej instalacji |
|---|---|---|---|
| Motion score | Dokumentacja i score.mjs, rational fps i ranges | Uniwersalne capability/fidelity metadata | Czy runtime klienta czyta dokładnie ten commit |
| Declarative scenes | motion-scenes.mjs odczytany | Pełny graph compositingu AE/3D jako wspólne IR | Pokrycie silników uruchomionych lokalnie |
| FrameCut global timeline | fc_core/fc_time i owner skill | Nowy publiczny produkt FrameMotion wymaga kompatybilnego adaptera | Stan oddzielnego repo FrameCut |
| Motion request/bind | Revision/context hashes, frame count/FPS/size i obecność kanału alpha | Jawny future sidecar z required capabilities | End-to-end attach/render u użytkownika |
| Audio/sync | Udokumentowane grid/VO/lyrics/envelope oraz sound engine | Ujednolicony sample-time/provenance projection przy zachowaniu ownera | Jakość faktycznych miksów/analysis |
| QA | Motion review, FrameCut verify i delivery-readiness | Adapters benchmark fixtures i measured parity | Faktyczne oglądanie/odsłuch w aktywnym hoście |
| Fonts/assets | Fonty w score, assets/provenance/rights | Hash manifest i glyph preflight całego zestawu | Konkretne licencje przyszłego klienta |
| Color/alpha | Deklaracja requestu SDR bt709, opaque/straight; bind sprawdza has_alpha, nie association/kolor | Szersza wymiana linear/HDR/premult wymaga jawnej kwalifikacji | Wierność kolorystyczna ekranu/exportu |
| Version | Publiczny manifest 1.174.1; commit zapisany | Brak potrzeby zmiany wersji w tym researchu | Cały installed bundle vs main; local skill read tylko 1.174.1 |

## Profesjonalne narzędzia — zakres rzeczywistego porównania

| Narzędzie | Zbadana metoda | Wkład do FrameMotion | Pozostała luka |
|---|---|---|---|
| After Effects | Warstwy/precomp, krzywe, typografia, color/alpha, matte, tracking/roto/blur | Główna mapa warsztatu i pułapek | Natywne testy NOT_RUN |
| Fusion / Resolve Fusion | Oficjalny Visual Effects Guide 20 oraz produktowy node model | Jawny DAG, mask/tracking/composite, kontrola kolejności | Nie pełen manual wszystkich nodes; UI/render NOT_RUN |
| Apple Motion | Keyframes/behaviors, Sequence Text/Audio, konwersje | Parametryzacja i oddzielenie procedury od momentów | Wersja aplikacji nie zawsze podana w live docs |
| Cinema 4D | Fields/Effectors/Delay/cache | Stabilne instancje, wpływ przestrzenny, bake | Redshift/full production pipeline poza zakresem |
| Blender | Camera/DOF, motion/vector blur, simulation bake, CLI render | Prawdziwa scena 3D, hybrydowe passes i kontrolowany cache | Brak uruchomienia Blendera i renderów |
| Nuke | Premult/Unpremult dla Merge | Alpha-domain i edge fixture | Nie pełny kurs Nuke/keyingu |
| Houdini | SOP/DOP cache | Rozdzielenie obrazu/geometrii/stanu solvera | Nie kwalifikacja solverów ani nowe zależności |

## Jawne luki źródłowe i ograniczenia

Nie deklarujemy obejrzenia tutoriali wideo, przesłuchania muzyki, przejrzenia wszystkich poradników ani rozstrzygnięcia smaku przez metrykę. Dla School of Motion wykorzystano dostępne teksty/transkrypcje autorów; pozostałe nazwane kierunki (Video Copilot, Ben Marriott, Jake Bartlett, ECAbrams) mają stan zgodny z mapą poradników, nie automatycznie VERIFIED.

Część stron producentów blokowała odczyt; dla Blendera odczytano oficjalne raw RST, dla Fusion wybrany oficjalny przewodnik tekstowy. Nie oznacza to obejrzenia ilustracji i wideo. Duży manual Fusion nie został w całości zweryfikowany. Link-check jest osobną kontrolą transportu; HTTP200 nie potwierdza treści, a HTTP403 przy późniejszym sprawdzeniu nie usuwa wcześniej udokumentowanego odczytu.

Nie mierzyliśmy czasu renderu ani wydajności żadnego backendu. Parametry benchmarków to propozycje dla danych syntetycznych. Licencje i wersje są datowanym odczytem: przed wdrożeniem sprawdzić je ponownie dla konkretnego produktu i modelu dystrybucji. Brak źródła lub testu pozostaje Unknown/NOT_RUN, a nie ukrytym domyślnym PASS.
