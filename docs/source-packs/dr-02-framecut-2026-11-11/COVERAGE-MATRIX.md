# DR-02 — macierz wymagań, dowodów i luk

2026-11-11. „Pokryte” oznacza treść badania, nie działającą implementację. **NOT_RUN** nie jest PASS. Dokładne liczby w README/VERIFICATION po scaleniu źródeł.

| Wymóg oryginalnego promptu | Artefakt / miejsce | Dowód i zakres | Luka / dalszy test |
|---|---|---|---|
| 1. Cel, FrameCut standalone + Studio specialist | COMPREHENSIVE-REPORT; CODE-AND-CONTRACTS; IMPLEMENTATION_HANDOFF | DERIVED nad istniejącym ownerem | Repo nowych osobnych pluginów Unknown |
| 1. Publiczny main, commit, README/AGENTS/manifest | specialists/repo/CURRENT-STUDIO | Inspekcja przypiętego main 4611c9c; kod i dokumentacja | Aktualizacja późniejszego main wymaga nowego porównania |
| 1. GitHub vs instalacja | CURRENT-STUDIO; evidence/cache-comparison.json | 14 wybranych plików identycznych | Nie pełny pakiet, aktywacja/host runtime Unknown |
| 2. Źródła oficjalne i praktycy, PL+EN | SOURCE-LEDGER; craft/CRAFT; nle/NLE-WORKFLOWS | Teksty EN, polski wywiad SFP; normy, dokumentacja i kod | Nie całość internetu, część SDK ograniczona dostępem |
| 2. Autor/data/version/locator | SOURCE-LEDGER JSON/CSV | Null/Unknown gdy brak daty; pin code | Link check nie potwierdza treści nieprzeczytanej |
| 2. SOURCED/DERIVED/PRACTITIONER/Unknown | Wszystkie części, ledger inspection | Jawna klasyfikacja | Nie mierzy automatycznie prawdziwości syntezy |
| 3. Około100 pojęć PL/EN | specialists/craft/GLOSSARY | 100 odrębnych haseł G001–G100 | Nie pełny słownik wszystkich NLE |
| 3A. Dramaturgia, sens, rytm, pauza, continuity/J-L | craft/CRAFT, GLOSSARY, RECIPES | Praktycy + oryginalne reguły i kontrprzykłady | Brak własnego screeningu przykładowych filmów |
| 3B. Fabuła/dokument/reklama/produkt/tutorial/multicam/music/showreel/social | craft/CRAFT + RECIPES | Różne cele/selekcja/tempo/audio/kryteria | To profile, nie identyczny template hook/CTA |
| 3C. Ingest, backup/hash, log/proxy/relink/sync | NLE-WORKFLOWS; GLOSSARY; CODE-AND-CONTRACTS | Asset/source clip/timeline instance rozdzielone | Restore/relink native NOT_RUN |
| 3D. Monitory, in/out, 3/4point, insert/overwrite/append/split/trim | GLOSSARY; CODE-AND-CONTRACTS tabela przed/po | Native API odróżnione od RFC | Nowe first-class typy potrzebują implementacji |
| 3D. Ripple/roll/slip/slide/lift/extract/gaps/locks/anchors | CODE-AND-CONTRACTS §4; CONTRACT-FINDINGS | Operacje i wpływ na sąsiadów/lanes | Pełny track model w FrameCut to luka |
| 3D. Nest/compound/multicam/snapping/undo | GLOSSARY; NLE-WORKFLOWS; CODE-AND-CONTRACTS | Model NLE i agentowy plan | Native multicam/nesting unsupported |
| 3E. Rational FPS, PTS/timecode/DF, VFR, mixed rates | CODE-AND-CONTRACTS §3; GLOSSARY; QA-BENCHMARKS | Rachunek exact fractions + source docs | DF parser i VFR rendering native NOT_RUN |
| 3E. Handles/ramp/reverse/freeze/blending/optical flow | GLOSSARY; RECIPES; CODE-AND-CONTRACTS | Native ramp/freeze vs brak reverse/optical flow | Ruch/pitch test NOT_RUN |
| 3F. Dialogue/room tone/SFX/music/EQ/dynamics/noise/ducking/stems | NLE-WORKFLOWS §6; RECIPES; GLOSSARY | Workflow i granice automatyki | Odsłuch i mastering NOT_RUN |
| 3F. LUFS/true peak, pomiar vs słuch | NLE-WORKFLOWS; QA-BENCHMARKS | EBU normy vs runtime/projekt tolerancje | Żaden uniwersalny target internetowy |
| 3G. Color management/transforms/LUT/scopes/ranges/SDR-HDR | NLE-WORKFLOWS §7; GLOSSARY | Technical/creative rozdzielone | Kalibrowany monitoring i HDR native NOT_RUN |
| 3G. Scaling/stabilizacja/reframe/captions/graphics | RECIPES; NLE-WORKFLOWS; CODE-AND-CONTRACTS | Jawne źródła i keyframes | Tracking/stabilizacja zaawansowana hybrydowa |
| 3H. Pełny pipeline + post-lock changes | NLE-WORKFLOWS §2,5 | Etapy, turnovers i change list | Żaden rzeczywisty projekt nie został skonformowany |
| 3H. Resolve Media/Cut/Edit/Fusion/Color/Fairlight/Deliver | NLE-WORKFLOWS §3 | Siedem klasycznych stron + Photo w21 | Version-specific UI i local app Unknown |
| Doprecyzowanie: Premiere/FCP/Avid i pro tools | NLE-WORKFLOWS §4,6–9; REPOSITORIES | Merytoryczne modele pracy, Pro Tools/Nuke/Baselight | Pełne szkolenie każdego pakietu poza zakresem |
| 4. 15–20 receptur z11 polami | specialists/craft/RECIPES | 18 autorskich receptur | Wszystkie wykonania medialne NOT_RUN |
| 4. Selekcja przed timeline, wyjątki/kontrprzykłady | CRAFT; RECIPES; COMPREHENSIVE-REPORT | claim→decision→countercase→QA | Ostateczna ocena konkretnego materiału wymaga jego oglądu |
| 5. Analysis→decision→plan→JSON→validate→compile→preview→QA→export | CODE-AND-CONTRACTS | Rozróżnienie intencji/operacji i istniejącego board workflow | RFC nie jest CLI-komendą |
| 5. FFmpeg/ffprobe/GOP/copy/trim/PTS/concat/xfade/retime/color | CODE-AND-CONTRACTS §5; ROOT-SOURCES F01–F05 | Odczyt oficjalnego HTML, bez local build test | Filtr nie gwarantuje jakości NLE |
| 5. OTIO i inne silniki/API NLE | REPOSITORIES; NLE-WORKFLOWS §8 | Pinned code/doc; role adapterów | Nie uruchomiono downloaded code ani apps |
| 5. JSON trim/split/insert/overwrite/ripple/roll/slip/slide | examples/editorial-intents.json; native-operations.json | 14 intent families,11 native-shaped cases, before/after | Ograniczony własny structural check; runtime NOT_RUN |
| 5. Speed curve/freeze/transform/transition/gain/ducking/subtitles | Te same przykłady; CODE-AND-CONTRACTS | Units, shape, pre/post/konflikty | Nie potwierdzono renderu, glyphów i mixu |
| 5. Immutability/revision/undo/idempotency/conflict/checkpoints/cache | CODE-AND-CONTRACTS §6; CONTRACT-FINDINGS | Istniejące mechanizmy vs proposed receipt/DAG | Idempotency i minimal spans nie są gotowymi funkcjami |
| 6. Cut detection vs content/best take/narrative | CRAFT; CODE-AND-CONTRACTS; model cards repo | Hierarchia obserwacji i decyzji | ASR/diarization mają niepewność, native diarization unsupported |
| 6. Contact sheet vs motion, transcript vs tone | CRAFT; COMPREHENSIVE-REPORT; QA-BENCHMARKS | Krytyczne zakresy oglądu/odsłuchu | Brak medialnego oglądu w tym researchu |
| 6. EDL/XML/FCPXML/AAF/OTIO i bake/loss | QA-BENCHMARKS; CONTRACT-FINDINGS; REPOSITORIES | Plan round-trip i semantyka formatów | Native round-trip NOT_RUN |
| 7. Wersjonowany wspólny kontrakt wszystkich pól | CODE-AND-CONTRACTS §7; examples/motion-handoff-rfc.json | RFC sidecar + mapping do istniejącego v1 | Hash/fonts UNBOUND; nie sfabrykowane wartości |
| 7. FrameCut master, FrameMotion scope/handles/length/revisions | CONTRACT-FINDINGS; CODE-AND-CONTRACTS | Obecny motion-request/bind + proponowane rozszerzenia | Niepodany repo standalone FrameMotion |
| 7. Bez drugiego intake/routerów/owners | CURRENT-STUDIO; HANDOFF | Zachowano Caption/Audio/Asset/Motion owners | Decyzja migracyjna należy do Claude/użytkownika |
| 7. Cały storyboard + krytyczny ruch, plan acceptance, locks | CODE-AND-CONTRACTS; CURRENT-STUDIO | Istniejący workflow board approval odnotowany | Nie zatwierdzano researchu jako filmu |
| 8. Konkretne repo/pliki/API/licencje/odrzucenia | REPOSITORIES + Rxx ledger | Piny/paths i bounded inspection | Licencje model/weights/assets rozdzielić przy użyciu |
| 8. Pięć benchmarków i tolerancje | QA-BENCHMARKS | Fixtures, expected ops/results i QA | NOT_RUN; żadnego fałszywego PASS |
| 8. Frame count/sync/gaps/black/transition/retime/captions/loudness/color/decode | QA-BENCHMARKS | Technical checks vs perceptual rubrics | Runtime dziś nie pokrywa wszystkiego |
| 9. Kompendium/mapa źródeł/receptury/repo/schema/QA/macierze | README + wszystkie części | Komplet artefaktów badania | Nie jest release wtyczki |
| 9. P0/P1/P2 i każde zadanie: owner/I-O/files/deps/fallback/test | IMPLEMENTATION_HANDOFF | 10 szczegółowych zadań z integracyjnymi ograniczeniami | Wdrożenie nieautoryzowane w tym researchu |
| 9. Weryfikacja, niezależny review, Hipson | REVIEW; VERIFICATION; Hipson T-0004 | Kontrola struktury/rachunku/linków i review syntezy | Status końcowy zapisany po świeżej weryfikacji |

## Macierz obecnego produktu

Szczegółowa klasyfikacja „potwierdzone w kodzie / luka / Unknown” znajduje się w `specialists/repo/CURRENT-STUDIO.md` §6. Nie przenosimy statusu „potwierdzone w kodzie” do kolumny „działa w aktywnej sesji”. Bieżący research niczego nie aktywował i nie wdrożył.
