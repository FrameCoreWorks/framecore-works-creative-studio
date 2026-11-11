# DR-02 — Stan obecnego Studio i FrameCut

Data badania: 2026-11-11. Metoda: odczyt publicznego GitHub przez konektor GitHub, inspekcja konkretnych plików, odczyt zainstalowanego cache i porównanie wybranego podzbioru bajtów. Nie uruchamiano pobranego kodu, testów repozytorium, rendererów ani NLE. Poniższe **SOURCED** oznacza potwierdzenie w źródle/kodzie, nie sukces wykonania. **DERIVED** oznacza wniosek z inspekcji. Wszystkie próby medialne i round-trip: **NOT_RUN**.

## 1. Trzy wersje i dwie powierzchnie

- Publiczny `main`: [`4611c9c4ed44579b8a2c0224c9276d955fccd8d6`](https://github.com/FrameCoreWorks/framecore-works-creative-studio/commit/4611c9c4ed44579b8a2c0224c9276d955fccd8d6), data commitu **2026-11-11 07:20:22 UTC**. Pobrano wskazany commit, a nie przypisywano lokalnego checkoutu do GitHuba.
- Pakiet Creative Studio: **1.174.1**, techniczny identyfikator `framecore-work-creative-studio`. [R01][R30]
- Wewnętrzny runtime FrameCut: **1.1.0** (`fc_core.VERSION`); projekt: **schema_version 1**. To nie są alternatywne nazwy tej samej wersji. [R03][R04]
- Zainstalowany cache (tylko odczyt): `[private installed Creative Studio cache 1.174.1]`.
- Porównano 14 wybranych plików pakietu z treścią przypiętego commitu: **14/14 identycznych bajtowo**. Wykaz i SHA-256: `evidence/cache-comparison.json`. Porównanie nie obejmuje całego pakietu, hosted ChatGPT release ani rejestracji skilli w aktywnym hoście.
- Adresów nowych, osobnych repozytoriów FrameCut/FrameMotion nie podano. Ich stan implementacji pozostaje **Unknown**. Nie wyprowadzano adresów z nazw.

**Konsekwencja:** FrameCut nie jest greenfield. Istnieje jako publicznie udokumentowany i zaimplementowany właściciel `opencut-video-studio` wewnątrz Studio. Rozdzielenie go na wtyczkę wymaga zachowania lub jawnej migracji obecnych kontraktów, nie zaprojektowania drugiego projektu/timeline obok nich. [R01][R03][R09]

## 2. Potwierdzone pliki i przypięte lokalizacje

Wszystkie odnośniki poniżej są przypięte do tego samego SHA. Pełne ścieżki w repo są podane w linkach; skrót `P/` oznacza `plugins/framecore-work-creative-studio/`.

| Obszar | Dokładny punkt inspekcji | Ustalenie |
|---|---|---|
| Publiczny produkt | [README L36–92](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/README.md#L36-L92) | FrameCut editing i wersja produktu; README nie dowodzi wykonania. [R01] |
| Reguły zmian | [AGENTS L1–18](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/AGENTS.md#L1-L18) | Pakiet współdzielony, maintenance mode, rozdzielenie poziomów dowodu. [R02] |
| Manifest | [plugin.json L1–12](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/.claude-plugin/plugin.json#L1-L12) | Wersja 1.174.1, autor, Apache-2.0. [R30] |
| Kształt projektu | [schema.json L1–31](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/opencut-video-studio/assets/framecut/schema.json#L1-L31) | Project v1, wymagane obiekty, brak dowolnych pól na poziomie projektu. [R03] |
| Semantyka | [fc_core.py L200–385](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/opencut-video-studio/assets/framecut/fc_core.py#L200-L385) | Walidacja clock/hash/zakresów/lane/anchor/overlap; właściwy autorytet semantyczny. [R04] |
| Rewizje i operacje | [fc_core.py L390–469](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/opencut-video-studio/assets/framecut/fc_core.py#L390-L469) | Lock pliku, stale revision, history, atomic candidate, closed operation envelope. [R04] |
| Edycja natywna | [fc_edit.py L38–75](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/opencut-video-studio/assets/framecut/fc_edit.py#L38-L75), [L77–172](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/opencut-video-studio/assets/framecut/fc_edit.py#L77-L172) | Ripple/split/dependents oraz dispatch operacji; brak pełnego zestawu NLE. [R05] |
| Czas i animation | [fc_time.py L50–138](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/opencut-video-studio/assets/framecut/fc_time.py#L50-L138) | Exact source integral, inverse, source remainder i zachowanie okna animation po trim/split. [R06] |
| Motion request/return | [fc_render.py L87–137](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/opencut-video-studio/assets/framecut/fc_render.py#L87-L137) | Lokalny clock od 0 i walidowane przywiązanie do parent context. [R07] |
| Technical QA / review | [fc_render.py L404–426](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/opencut-video-studio/assets/framecut/fc_render.py#L404-L426), [L576–621](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/opencut-video-studio/assets/framecut/fc_render.py#L576-L621) | Decode/frame count oraz odrębna gotowość po udokumentowanym oglądzie/odsłuchu. [R07] |
| Interchange | [framecut.py L88–138](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/opencut-video-studio/assets/framecut/framecut.py#L88-L138) | Native/CSV/relink oraz ograniczony picture EDL/OTIO; jawny loss report. [R08] |
| Owners | [studio-integration-policy L67–69](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/pipeline-core/references/studio-integration-policy.md#L67-L69) | Jeden master i powroty specjalistów do FrameCut. [R09] |
| Caption handoff | [caption-studio L124–128](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/caption-studio/SKILL.md#L124-L128) | Zachowanie source word IDs, osobne korekty i tłumaczenie; jedno przemapowanie czasu. [R10] |
| Audio handoff | [audio-production-director L65–67](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/audio-production-director/SKILL.md#L65-L67) | Sound direction wraca do FrameCut; audio nie zmienia samodzielnie picture duration. [R11] |
| Companions | [companion-routing L25–63](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/pipeline-core/references/companion-routing.md#L25-L63) | Request/result, hash intake i stan not_reviewed; Toolbox/Open Assets mają własne role. [R12] |
| Testy autora | [framecut_development_test.py L37–114](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/tests/framecut_development_test.py#L37-L114), [L153–303](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/tests/framecut_development_test.py#L153-L303) | Scenariusze exact split/ripple/freeze/ramp/job; przeczytane, nie uruchomione. [R13] |

## 3. Co naprawdę ma już kontrakt

**SOURCED.** Projekt przechowuje `id`, `revision`, `brief`, `authorization`, `assets`, `analyses`, `sequences`, `deliverables`, opcjonalnie `locks`, `status`, `history`. Asset jest osobnym bytem z relatywną ścieżką, SHA-256, typem, wynikiem probe oraz dopuszczonym provenance/rights/motion binding. Zdarzenie na timeline ma własne ID i odnosi się do assetu; nie jest plikiem źródłowym. [R03][R04]

Sequence ma rational `fps:{num,den}`, długość w klatkach i listy `clips`, `audio`, `overlays`, `texts`. Czas `start`, `duration`, overlap `transition` oraz `anchor.offset` to integer frames sekwencji. `source_in` jest liczbą ticków PTS konkretnego assetu; `source_remainder` przechowuje ułamek sekundy poniżej jednego ticka. Należy używać oryginalnego `time_base/start_pts`, nie mnożyć sekund przez nominalny source FPS. Zakresy są półotwarte. [R04][R06]

`apply --ops ... --base-revision N --reason ...` przyjmuje atomową tablicę do 500 operacji. Kopiuje projekt, wykonuje zmiany, sprawdza locks i cały wynik; dopiero zapis pod lockiem sprawdza aktualną rewizję, hashe źródeł i tworzy nową rewizję. Undo przywraca wcześniejszą treść jako nową rewizję z zachowaniem obecnych zabezpieczeń. Sam status stale_revision nie jest idempotentnym potwierdzeniem ponownie wysłanej operacji. [R04][R05]

Obsługiwane proste mutation ops: `add_sequence`, `set_sequence`, `replace_clip`, `set_captions`, `set_audio`, `set_overlays`, `set_texts`, `set_brief`, `set_authorization`, `set_locks`, `set_deliverables`. Natywne edycje: `split_clip`, `trim_clip`, `move_clip`, `remove_clip`, `freeze_frame`, `set_keyframes`, `set_speed_curve`, `set_effects`, `set_framing`. Operation envelope dopuszcza tylko `op, sequence, id, value`. Projektowane nowe pola/operacje muszą być RFC lub rozszerzeniem walidatora; obecny runtime odrzuci je. [R04][R05]

Keyframes używają `frame,value,easing` i tracków `x,y,scale,rotation,opacity,gain_db,zoom,pan_x,pan_y` z ograniczeniami dla danego rodzaju eventu. Easing to linear/smooth/hold, przypisany do odcinka wychodzącego. Native speed curve ma 2–64 punkty, pokrywa 0..duration, dodatnie rational speed 1/4..4; reverse nie jest obsługiwany. Freeze jest osobną operacją. Variable-speed audio zmienia tempo **i pitch**; bogaty time-stretch/optical flow nie wynika z samej obecności krzywej. [R03][R05][R06]

## 4. Właściciele — zachować zamiast dublować

| Odpowiedzialność | Obecny właściciel | Implikacja dla nowych wtyczek |
|---|---|---|
| Brief, kierunek, Project State i route | Studio | Przekazywać istniejący working agreement; bez drugiego intake. |
| Master edit, source→sequence map, revisions, integration, render/delivery | FrameCut (`opencut-video-studio`) | Zachować jednego właściciela nadrzędnego clock. |
| Caption grouping/readability/style/QA | Caption Studio | FrameCut odpowiada za projekcję czasu; craft pozostaje u specjalisty. |
| Local motion i implementacja proceduralnego sound | Motion Graphics (`hyperframes-workflow`) | Proponowany FrameMotion przejmuje scoped composition, nie global edit. |
| Sound direction, music/voice/rights/review | Audio Production | Odsyła timed cues/derived assets z measured delay. |
| Źródła stock/otwarte media | FrameCore Open Assets | Zachować per-asset rights/provenance. |
| Earshot execution/analysis | FrameCore Works Toolbox | Nie dodawać drugiej usługi Earshot do FrameCut. |
| Inventory, dependencies, packaging | Asset Manifest i Delivery | Inventory nie oznacza creative approval; packaging dopiero po QA. |

Źródła: [R09][R10][R11][R12]; dla inventory dodatkowo przeczytano `skills/asset-manifest/SKILL.md`, L111–113. Nie zmieniono żadnego z tych właścicieli.

## 5. Workflow approval i sprawdzanie delivery

Obecny `opencut-video-studio/SKILL.md` wymaga pełnego storyboardu/contact sheets obejmującego całość oraz akceptacji bieżącej wersji przed pierwszym finalem. To gate host workflow: `framecut_context` w Project State/brief przechowuje stage, board revision, coverage, feedback i faktyczną approval evidence. CLI `authorization` nie dowodzi akceptacji niewidzianego boardu. Akceptacja nie wymaga potwierdzania każdego cięcia; zwykły ingest lub render nie unieważnia niezmienionego projektu. Po akceptacji żądane przez użytkownika poprawki idą do montażu; niezamówiona zmiana zaakceptowanej decyzji wymaga osobnej akceptacji. Ta reguła została odczytana jako istniejący kontrakt, nie uruchamiana dla niniejszego researchu.

Technical verifier sprawdza wymiary, rational rate, decoded frame count równy sequence duration, pełny decode bez błędów, audio track i różnicę długości. Jeżeli podano deliverable `lufs` i istnieje skończony wynik pomiaru, akceptuje tolerancję ±1,5 LU oraz true peak ≤−0,5 dBTP. To **tolerancje obecnego projektu**, nie normy wszystkich dostaw. Zgodność długości tracków nie dowodzi lokalnego lip-sync, detekcji czarnych klatek ani zachowania sensu. [R07]

`delivery_readiness`: preview→PREVIEW_ONLY; fatal warning→BLOCKED; brak/niepełny review→REVIEW_REQUIRED; pełny, passing review z `picture_watched` i `audio_heard` (lub intentional silence)→READY. Te flagi są deklaracjami recenzenta powiązanymi z hashem wideo. Techniczny PASS nie potwierdza odsłuchu ani akceptacji użytkownika. [R07]

## 6. Macierz potwierdzone / luka / Unknown

| Obszar | Stan źródłowy | Co pozostaje do sprawdzenia / doprojektowania |
|---|---|---|
| Immutable assets, revisions, stale source/revision, snapshot history | Potwierdzone w kodzie | Skuteczność i awarie procesu w tym hoście: NOT_RUN. |
| Atomic split/trim/ripple/remove/freeze | Potwierdzone w kodzie + testy autora | Wszystkie fixture i actual decode: NOT_RUN. |
| Insert/overwrite/roll/slip/slide jako własne typy | Luka w inspected operation set | Jawne semantyki, track impact i kompilacja do transakcji. |
| Multicam, track targeting/locking, nest/compound jako NLE | Nieobsługiwane / brak natywnych typów | Propozycja rozszerzenia, nie opis aktualnej funkcji. |
| Timed captions, word protection, sentence/kinetic, translations boundary | Potwierdzone | ASR quality, readability real media i tłumaczenia potrzebują review. |
| Audio split events/J-L, gain/ducking, requested LUFS | Potwierdzone | Wielokanałowe stemsy, miks i lip-sync pozostają osobnym acceptance. |
| Speed ramp/freeze | Potwierdzone w ograniczonej semantyce | Pitch-preserving ramp, reverse, optical flow: luka. |
| Motion request + return binding | Potwierdzone | Handles/font manifests/seed/color enforcement i nowy FrameMotion ID: RFC. |
| SDR finishing | Potwierdzone; HDR jawnie odrzucany | Pełne color-management/HDR mastering: luka. |
| EDL/OTIO | Ograniczone picture cuts + loss report | Pełna semantyka, trailing gap, mixed rates i NLE round-trip: NOT_RUN. |
| Black-frame/gap intent + local A/V sync | Nie pokryte samym verify_video | Plan testu z expected gaps i kontrolnymi transientami. |
| Cache i durable jobs | Kod i testy autora istnieją | Długi projekt, kill/recovery, budżet dysku i wydajność: NOT_RUN. |
| Osobne nowe pluginy FrameCut/FrameMotion | Unknown | Nie podano repo; brak podstaw do claims o ich aktualnym kodzie. |

## 7. Zakres inspekcji i ograniczenia

Rzeczywiście odczytano README, AGENTS, manifest, projekt schema, core/edit/time/editor/render/audio/captions/CLI, ownership policy, companion routing, caption/audio/asset skills, legacy export i trzy pliki testów. Pełny statyczny security audit ani pełna analiza wszystkich modułów nie były celem. Nie przeszukano prywatnego hosted overlay. Nie wyciągano wniosków o runtime z samej obecności cache.

**DERIVED – szczególne testy do backlogu:** eksport kończy OTIO track na końcu ostatniego base clip (`previous`) i porównuje odczytaną długość do tej wartości, a nie do `seq.duration`; trailing gap może zniknąć. Obserwacja kodu nie jest reprodukcją błędu. Drugi test powinien wykazać, że porównywanie tylko duration nie wykrywa zamiany source ranges. [R08]

Publiczna dokumentacja i kod oryginalny są Apache-2.0; snapshoty upstream zachowują własne licencje. Badanie nie stanowi zgody na kopiowanie całych bibliotek ani instalację zależności. [R01][R02][R30]

Powiązane materiały: `CONTRACT-FINDINGS.md`, `REPOSITORIES.md`, `sources.json`. W oryginalnym badaniu kopie w `evidence/` służyły wyłącznie inspekcji. W tym eksporcie zastępuje je [spis przypiętych źródeł](../../SOURCE-SNAPSHOT-REFERENCES.json); zachowano zanonimizowany historyczny wynik porównania cache.

