# DR-03 B — pełne karty wiedzy agentowej
Data: 2026-11-11. Wszystkie próby wykonawcze: **NOT_RUN**. DERIVED oznacza własny projekt adaptacji, nie istniejącą integrację. Repo FrameMotion i jego aktualne API: **Unknown**. 9 kandydatów; K09 celowo ALREADY_COVERED. Class B nie jest biblioteką assetów; resolution/duration/FPS/loop/layers/asset-origin są N/A dla dokumentacji, a dla planowanych fixtures opisane w testach. Źródła: GitHub connector oraz dokumentacja primary; nie wykonano pobranego kodu.

## K01 — Unicode UAX29 + GraphemeBreakTest: kontrakt kinetic text
Kanoniczny URL: [Unicode UAX29 + GraphemeBreakTest: kontrakt kinetic text](https://unicode.org/reports/tr29/tr29-49.html)

- **Owner:** Unicode Consortium; ECMAScript Intl TC39
- **Pin / tag:** Unicode 18.0.0 UAX29 rev49; corpus 18.0.0; ECMA402 live, runtime Unicode version Unknown
- **Data przeglądu:** 2026-11-11
- **Klasa:** B
- **Nowość:** KNOWN_NEW_CAPABILITY
- **Problem:** Reveal dzielący UTF-16 albo codepoints może oddzielać akcent od litery lub rozbić emoji; polski tekst w NFC i NFD nie może zmieniać liczby kroków reveal.
- **Delta wobec baseline:** Baseline ma keepTogether dla polskich jednoliterowych wyrazów/jednostek i dokładną copy. Marginalna propozycja: wersjonowane granice extended grapheme, zachowanie bajtów copy, fixture NFD/ZWJ. Brak takiego kontraktu w przeczytanych plikach; brak twierdzenia o całym repo.
- **Dokładny moduł:** UAX29 §3 i §7; auxiliary/GraphemeBreakTest.txt; Intl.Segmenter granularity=grapheme.
- **Wejścia / wyjścia / edytowalność / alfa:** IN: zatwierdzony UTF-8 text, locale pl, strategia segmentacji i jej wersja. OUT: segmenty z oryginalnymi indeksami; brak mediów. Parametryzacja: granularity/locale; exact copy niezmieniona; alfa N/A.
- **Runtime / host / zasoby:** Dokumentacja/test data bez runtime. Adapter JS wymaga hostowego Intl.Segmenter i jego ICU; przeglądarka/headless/Node zależne od wersji; CPU, RAM Unknown; offline po przypięciu źródła.
- **Eksport:** Segmenty zasilają obecny HTML/SVG/Canvas/Remotion renderer; same nie eksportują MP4/PNG/EXR/WebM.
- **Koszt / konto / sieć:** Odczyt bez konta/klucza/opłat. Brak usługi; pobranie corpus w przyszłym wdrożeniu wymaga zwykłej sieci. Koszt adaptacji DERIVED 0.5–1 dzień.
- **Prawa:** Unicode data: License V3 z notice. Standard cytować; własny przepis nie kopiuje całości. Fonty/emoji glyphs/media: osobne prawa Unknown. Wyrenderowany film i redystrybucja fontu to odrębne decyzje.
- **Utrzymanie / ograniczenia:** Wersja Unicode 18 stabilna w odczytanym źródle; przeglądarka może mieć inną wersję Unicode/CLDR. Nie wymuszać upgrade runtime; mismatch raportować.
- **Poziom dowodu:** DOCUMENTED test fixture; wynik uruchomienia autora Unknown. NOT_RUN zgodność segmentera i render.
- **Właściciel docelowy:** Studio hyperframes-workflow + remotion-video-production; FrameMotion proponowany konsument, obecne funkcje Unknown.
- **Forma:** SKILL_ADAPTATION
- **Rekomendacja:** P0: dopisać w istniejącym właścicielu, bez nowego skilla/dependency. Granice przygotować raz, zachować hash i mapowanie do exact copy.
- **Test akceptacyjny:** NOT_RUN: Zażółć gęślą jaźń, NFC/NFD, Z+combining dot, a+ogonek, 👩🏽‍💻, 🇵🇱, NBSP; każdy reveal odsłania pełny grafem. Obejrzeć wszystkie klatki reveal 16:9/9:16, porównać final copy i seek [0,47,1,47,0].
- **Deep dive w DEEP_DIVES.md:** True

Źródła: [KB02](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/hyperframes-workflow/references/motion-contract-json.md), [KB07](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/hyperframes-workflow/assets/motion-scenes/motion-scenes.mjs), [KS01](https://unicode.org/reports/tr29/tr29-49.html), [KS02](https://www.unicode.org/Public/18.0.0/ucd/auxiliary/GraphemeBreakTest.txt), [KS03](https://tc39.es/ecma402/#sec-intl.segmenter), [KS04](https://www.unicode.org/license.txt).

## K02 — CSS Font Loading: negatywne przypadki gotowości fontów
Kanoniczny URL: [CSS Font Loading: negatywne przypadki gotowości fontów](https://www.w3.org/TR/2023/WD-css-font-loading-3-20230406/)

- **Owner:** W3C CSS Working Group
- **Pin / tag:** Working Draft 2023-04-06
- **Data przeglądu:** 2026-11-11
- **Klasa:** B
- **Nowość:** KNOWN_NEW_CAPABILITY
- **Problem:** fonts.ready/check może dać pozorny PASS, gdy użyto fallbacku lub błędnej nazwy rodziny; pomiar przed właściwym face daje inny układ i clipping.
- **Delta wobec baseline:** KB01 już wymaga actual face readiness. Nowa użyteczność: źródłowo udokumentowane negatywne testy missing-family i unicode-range, odrębna kontrola face/coverage/layout, nie kolejna ogólna zasada await fonts.
- **Dokładny moduł:** FontFace.load; FontFaceSet.load/check/ready; testy negatywne opisane w tej karcie i dodatku do K01 w DEEP_DIVES.md.
- **Wejścia / wyjścia / edytowalność / alfa:** IN: lokalny font file+hash+face descriptors i pełna copy; OUT: loaded face list, błędy, szerokości/bounds i obraz kontrolny; parametry weight/style/stretch; alfa N/A.
- **Runtime / host / zasoby:** Browser Font Loading API; dokładny browser/OS/DPR/fonts pin; CPU; headless możliwy zależnie od hosta. RAM Unknown. Lokalny face pozwala offline; font URL może uruchomić sieć.
- **Eksport:** Bramka przed pomiarami i istniejącym MP4/PNG/WebM exportem; nie renderer. EXR N/A.
- **Koszt / konto / sieć:** Dokumentacja bez opłat/konta. Własny font może mieć koszt; Unknown. Szacunek DERIVED 0.5–1 dzień.
- **Prawa:** W3C permissive document license wskazana w spec; font licencjonowany osobno. Prawo użycia tekstu w filmie nie daje prawa bundlowania fontu; Unknown per font.
- **Utrzymanie / ograniczenia:** Spec Working Draft, nie Recommendation. API opisane stabilnie, faktyczne face/coverage nadal do próby na wybranym browserze.
- **Poziom dowodu:** DOCUMENTED; NOT_RUN font loading/render. Brak twierdzenia o glyph coverage na podstawie samego check().
- **Właściciel docelowy:** Studio obecny kontrakt fonts i QA; Caption Studio dla tekstu; FrameMotion proponowany konsument.
- **Forma:** SKILL_ADAPTATION
- **Rekomendacja:** P0: dwa negative fixtures i wymóg hashów fontów; bez nowej biblioteki. Brak pokrycia → jawny FAIL/Unknown, bez cichego system fallback.
- **Test akceptacyjny:** NOT_RUN: prawidłowy face vs literówka family vs subset bez ąęł; require resolved exact face, glyph review, identyczne bounds po cold/warm load. Ogląd reveal i readable hold w obu proporcjach.
- **Deep dive w DEEP_DIVES.md:** False

Źródła: [KB01](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/hyperframes-workflow/references/motion-toolkit-runtime-cards.md), [KB02](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/hyperframes-workflow/references/motion-contract-json.md), [KB03](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/remotion-video-production/references/remotion-implementation-notes.md), [KS05](https://www.w3.org/TR/2023/WD-css-font-loading-3-20230406/).

## K03 — Playwright screenshot assertions jako kontrolowany oracle motion
Kanoniczny URL: [Playwright screenshot assertions jako kontrolowany oracle motion](https://playwright.dev/docs/api/class-pageassertions)

- **Owner:** Microsoft Playwright
- **Pin / tag:** 3b438229c6a2ccdbe2d3572755935892203d83c3; package 1.66.0-next odczytany, nie rekomendowany install
- **Data przeglądu:** 2026-11-11
- **Klasa:** B
- **Nowość:** KNOWN_NEW_CAPABILITY
- **Problem:** Domyślny screenshot test może usunąć animację, którą ma badać, a statyczny PASS może ukryć migotanie i zależność od kolejności klatek.
- **Delta wobec baseline:** Baseline ma seek-order i full watch. Nowy punkt: jawna opcja animations=allow po zatrzymaniu własnego zegara oraz negative fixture wykrywający ucieczkę wall-clock; upstream test pokazuje tę pułapkę.
- **Dokładny moduł:** docs PageAssertions.toHaveScreenshot; tests/playwright-test/to-have-screenshot.spec.ts lines 1–150; wzór testu DERIVED w DEEP_DIVES.md, K03.
- **Wejścia / wyjścia / edytowalność / alfa:** IN: gotowa scena z prepare/setFrame/settled i frame list; OUT: PNG expected/actual/diff + frame/env manifest. Edytowalne testy; nie daje edytowalnej animacji. Alfa screenshot wymaga osobnej konfiguracji i decode QA.
- **Runtime / host / zasoby:** Odczytany HEAD Node>=20, browser install osobny. Headless/OS/GPU/DPR pin; pamięć Unknown. Offline dla lokalnej sceny i zasobów; browser/runtime nie zakładane zainstalowane.
- **Eksport:** PNG/WebP snapshots; finalny MP4/WebM z istniejącej ścieżki, następnie decode i temporal watch. Screenshoty nie dowodzą encodera ani EXR.
- **Koszt / konto / sieć:** Bez konta/klucza dla local runner; setup może pobierać browser. Korzystać z istniejącej instalacji. Koszt adaptacji DERIVED 1–2 dni.
- **Prawa:** Repo/test code Apache-2.0 wg manifestu i nagłówka testu. Prawa przedstawionej sceny, fontów i assetów osobne Unknown.
- **Utrzymanie / ograniczenia:** Odczyt HEAD 2026-11-11, development 1.66.0-next. Przy wdrożeniu wybór istniejącej stabilnej wersji i lock, nie update do HEAD; baseline środowiskowy konieczny.
- **Poziom dowodu:** DOCUMENTED; CODE_INSPECTED scenariusze testów; wynik uruchomienia autora Unknown; wszystkie nasze testy NOT_RUN.
- **Właściciel docelowy:** Studio istniejący motion QA; adapter testowy dla FrameMotion po ustaleniu API; Toolbox bez nowego wpisu.
- **Forma:** SKILL_ADAPTATION
- **Rekomendacja:** P0: rozszerzyć obecny QA o negative-control i jawny capture mode, zachowując cztery oddzielne werdykty. Nie kopiować całego Playwright repo.
- **Test akceptacyjny:** NOT_RUN: 2 s scena z frame-derived pozycją + celowo błędny CSS loop; prawidłowa scena identyczna przy shuffled seek, błędna wykryta. Przejście co klatkę + normal speed finalnego encode; expected snapshots zatwierdzone wizualnie.
- **Deep dive w DEEP_DIVES.md:** True

Źródła: [KB04](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/hyperframes-workflow/templates/motion-qa-record.md), [KB05](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/hyperframes-workflow/assets/motion-quality/README.md), [KS06](https://playwright.dev/docs/api/class-pageassertions), [KS07](https://playwright.dev/docs/test-snapshots), [KS08](https://github.com/microsoft/playwright/blob/3b438229c6a2ccdbe2d3572755935892203d83c3/tests/playwright-test/to-have-screenshot.spec.ts), [KS09](https://github.com/microsoft/playwright/blob/3b438229c6a2ccdbe2d3572755935892203d83c3/package.json), [KS32](https://github.com/microsoft/playwright/blob/3b438229c6a2ccdbe2d3572755935892203d83c3/packages/playwright/src/matchers/toMatchSnapshot.ts).

## K04 — librosa onset: czas ataku vs backtracked slice point
Kanoniczny URL: [librosa onset: czas ataku vs backtracked slice point](https://librosa.org/doc/0.11.0/generated/librosa.onset.onset_detect.html)

- **Owner:** librosa development team
- **Pin / tag:** API docs 0.11.0; inspected HEAD 6c9fe7c18ed8bab8a44637355171b2129cf5c720 (nie tożsamy runtime)
- **Data przeglądu:** 2026-11-11
- **Klasa:** B
- **Nowość:** KNOWN_NEW_CAPABILITY
- **Problem:** Pomieszanie audio analysis frames z video frames lub użycie backtrack do wizualnego hitu powoduje błędny sync. Onset nie jest automatycznie beat/downbeat.
- **Delta wobec baseline:** KB06 ma beats.py i per-frame band hits; Toolbox ma Earshot. Dodatek to precyzyjna rozdzielność onsetSample/sliceSample i walidacja jednostek. Nie wymieniać istniejącej analizy ani nie dodawać pełnego silnika bez testu przewagi.
- **Dokładny moduł:** librosa/onset.py onset_detect/onset_backtrack; tests/test_onset.py pulse train; 0.11.0 API recipe.
- **Wejścia / wyjścia / edytowalność / alfa:** IN: lokalny PCM, sr, hop_length, channel policy, trim origin, peak params. OUT: sample/time onset indices i osobne slice points; później JSON cue frames. Edytowalne dane; alfa N/A.
- **Runtime / host / zasoby:** Inspected HEAD Python>=3.12 z numba/numpy/scipy/scikit-learn/soundfile/pooch/soxr; 0.11.0 requirements tu Unknown. CPU, RAM zależne od długości, Unknown. Offline dla lokalnego PCM; przykładowe downloadery niepotrzebne.
- **Eksport:** Nie renderuje; cue JSON do motion-score, istniejący exporter i mux. Encoded audio trzeba zdekodować, zmierzyć offset i odsłuchać.
- **Koszt / konto / sieć:** Brak konta/API dla lokalnej analizy; CPU i zależności. Przykładowe load/ex mogą pobierać media: nie używać w offline fixtures. DERIVED 1–2 dni jeśli librosa już dostępna, inaczej osobna decyzja.
- **Prawa:** Kod ISC. Audio/dataset/example recordings mają własne prawa Unknown; fixture własny syntetyczny bez materiału muzycznego. Nie bundlować przykładów muzycznych.
- **Utrzymanie / ograniczenia:** HEAD od 2026-11-10; rozjazd docs0.11 i HEAD jawny. Pin wersji konieczny, obecna wersja Earshot/librosa na hoście Unknown.
- **Poziom dowodu:** DOCUMENTED; CODE_INSPECTED syntetyczny test fixture; wynik uruchomienia autora Unknown; NOT_RUN sync/audio/decode.
- **Właściciel docelowy:** Studio audio-production-director/motion-sync; Toolbox Earshot tylko jeśli istniejąca capability wymaga rozszerzenia; FrameCut mux/edycja.
- **Forma:** KNOWLEDGE_ONLY
- **Rekomendacja:** P1: najpierw dopisać unit contract i fixture. OPTIONAL_DEPENDENCY dopiero gdy porównanie z istniejącymi beats/envelope/Earshot wykaże potrzebę.
- **Test akceptacyjny:** NOT_RUN: pulse train 48 kHz o onsetach 0.25/0.75/1.25 s + 7 ms przesunięcie, hop 128/512, cisza i ramp; round(sample/sr * fpsNum/fpsDen) raz. Tolerancja mierzona, nie zakładana; listen + waveform/marker i first/last event po encode.
- **Deep dive w DEEP_DIVES.md:** False

Źródła: [KB06](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/hyperframes-workflow/assets/motion-sync/README.md), [KB12](https://github.com/FrameCoreWorks/framecore-works-toolbox/blob/adc8094f8e087889e4337c99dd0d267ae1b11a51/reviews/earshot-audio.md), [KS10](https://librosa.org/doc/0.11.0/generated/librosa.onset.onset_detect.html), [KS11](https://github.com/librosa/librosa/blob/6c9fe7c18ed8bab8a44637355171b2129cf5c720/librosa/onset.py), [KS12](https://github.com/librosa/librosa/blob/6c9fe7c18ed8bab8a44637355171b2129cf5c720/tests/test_onset.py), [KS13](https://github.com/librosa/librosa/blob/6c9fe7c18ed8bab8a44637355171b2129cf5c720/pyproject.toml), [KS14](https://github.com/librosa/librosa/blob/6c9fe7c18ed8bab8a44637355171b2129cf5c720/LICENSE.md).

## K05 — Lottie feature matrix + upstream frame-diff recipe
Kanoniczny URL: [Lottie feature matrix + upstream frame-diff recipe](https://github.com/airbnb/lottie/blob/a84a05f4353cb135a9cc29325a6e75bb735d0c0c/supported-features.md)

- **Owner:** Airbnb Lottie maintainers
- **Pin / tag:** matrix a84a05f4353cb135a9cc29325a6e75bb735d0c0c; lottie-web bede03d25d232826e0c9dca1733d542d8a7754fb (5.13.0)
- **Data przeglądu:** 2026-11-11
- **Klasa:** B
- **Nowość:** KNOWN_NEW_CAPABILITY
- **Problem:** Poprawny JSON i działający seek nie gwarantują mask/matte/text/blur w wybranym SVG/Canvas rendererze ani prawidłowej alfy.
- **Delta wobec baseline:** KB01 już zawiera Lottie seek/subframe/rights. Nowy margines: konkretny feature inventory + minimalny dwurendererowy fixture i krytyka upstream white-background sequential harness; żadna nowa obsługa useAnimations/Generative Icons.
- **Dokładny moduł:** supported-features.md; lottie-web/test/index.html + test/index.js; AnimationItem.goToAndStop.
- **Wejścia / wyjścia / edytowalność / alfa:** IN: uprawniony JSON, fr/ip/op, renderer pin i resource hashes; OUT: feature flags oraz PNG frame diffs i verdict per renderer. JSON edytowalny; layout/glyph asset zależne od źródła; alfa wymaga testu.
- **Runtime / host / zasoby:** lottie-web browser SVG/Canvas, JS; harness Node+Puppeteer+pixelmatch+pngjs+express. CPU/GPU zależne od browsera; RAM Unknown. Local assets offline; external URLs należy wykryć, nie fetch automatycznie.
- **Eksport:** DOM/SVG/Canvas capture do PNG, następnie istniejący Remotion/HyperFrames eksport; .lottie archive ma odrębny player. Brak bezpośredniej gwarancji MP4/WebM/EXR.
- **Koszt / konto / sieć:** Kod bez konta/klucza; zależności testowe i browser osobno. Niewielki wzorzec zamiast kopiowania całego harnessu. DERIVED 1–2 dni.
- **Prawa:** lottie-web MIT wg manifestu; test animations/gallery prawa odrębne Unknown, użyć własnych fixtures. Film reuse wymaga praw źródłowego assetu; redystrybucja JSON nie wynika z MIT playera.
- **Utrzymanie / ograniczenia:** Odczytany HEAD lottie-web ostatni commit 2024-11-19, matrix 2026-03-25. Matrix nie przypina każdej funkcji do wersji playera. Test harness ma komentarz 50 vs kod >200 px oraz białe tło; nie kopiować bez oceny.
- **Poziom dowodu:** DOCUMENTED; CODE_INSPECTED test recipe; wynik uruchomienia autora Unknown. NOT_RUN wszystkie nowe renderery/asset compatibility.
- **Właściciel docelowy:** Studio hyperframes-workflow i remotion-video-production; FrameMotion proponowany importer; Open Assets provenance.
- **Forma:** SKILL_ADAPTATION
- **Rekomendacja:** P1: import gate renderer/version/features/resources + per-asset visual QA. Unsupported → jawna odmowa lub zaakceptowany bake do klatek, bez cichej utraty feature.
- **Test akceptacyjny:** NOT_RUN: własny JSON trim path/alpha matte/tekst PL + osobny known-unsupported mask feather. Frames 0,N-1 i granice, shuffled seek, PNG alpha na białym/czarnym/magenta. Obejrzeć cały 2 s loop; JSON schema PASS nie daje visual PASS.
- **Deep dive w DEEP_DIVES.md:** False

Źródła: [KB01](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/hyperframes-workflow/references/motion-toolkit-runtime-cards.md), [KB04](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/hyperframes-workflow/templates/motion-qa-record.md), [KS15](https://github.com/airbnb/lottie/blob/a84a05f4353cb135a9cc29325a6e75bb735d0c0c/supported-features.md), [KS16](https://github.com/airbnb/lottie-web/blob/bede03d25d232826e0c9dca1733d542d8a7754fb/test/index.html), [KS17](https://github.com/airbnb/lottie-web/blob/bede03d25d232826e0c9dca1733d542d8a7754fb/test/index.js), [KS18](https://github.com/airbnb/lottie-web/blob/bede03d25d232826e0c9dca1733d542d8a7754fb/player/js/animation/AnimationItem.js), [KS19](https://github.com/airbnb/lottie-web/blob/bede03d25d232826e0c9dca1733d542d8a7754fb/package.json).

## K06 — Rive low-level cookbook: replay sterowany klatką i renderer gate
Kanoniczny URL: [Rive low-level cookbook: replay sterowany klatką i renderer gate](https://github.com/rive-app/rive-docs/blob/047f52be339575f86eb0710a5512e2c600e14313/runtimes/web/low-level-api-usage.mdx)

- **Owner:** Rive
- **Pin / tag:** docs 047f52be339575f86eb0710a5512e2c600e14313; runtime b61517a5bdcdcce54c4b5f50e86bac7e11fadecc; webgl2-advanced manifest 2.50.0
- **Data przeglądu:** 2026-11-11
- **Klasa:** B
- **Nowość:** NEW
- **Problem:** Interaktywny .riv ze state machine nie ma wykazanego absolutnego seek i może zależeć od wcześniejszych inputów; renderer może nie mieć wymaganej funkcji.
- **Delta wobec baseline:** W przeczytanym baseline Lottie/Canvas/Three występują, Rive replay cookbook nie występuje. NEW dotyczy proponowanego kontraktu i wiedzy, nie deklaracji gotowego supportu FrameMotion. Ogólna zasada fixed clock już istnieje.
- **Dokładny moduł:** runtimes/web/low-level-api-usage.mdx; feature-support.mdx; js/src/rive_advanced.mjs.d.ts; wasm/examples/parcel_example/index.js.
- **Wejścia / wyjścia / edytowalność / alfa:** IN: lokalny .riv + assets+fonts, artboard, animation/stateMachine, fixed input event trace, dimensions, FPS. OUT: Canvas frame i export manifest. Parametry przez inputs/data binding zależnie od pin; .riv runtime file nie zastępuje źródła projektu edytora; alfa Unknown przed testem.
- **Runtime / host / zasoby:** JS/WASM i Canvas2D lub WebGL2; Layer Masks potrzebują WebGL2+GPU Canvas. RAM/OS support/real host GPU Unknown. Offline możliwy z lokalnym matching WASM i wszystkimi resources; embedded scripting/out-of-band assets wymagają osobnej inspekcji.
- **Eksport:** DERIVED: capture kontrolowanych Canvas frames → PNG lub istniejący encoder. MP4/WebM poprzez osobny exporter; alpha i encoded fidelity NOT_RUN. EXR brak udokumentowanej drogi tutaj.
- **Koszt / konto / sieć:** Runtime MIT bez API key w lokalnej ścieżce; edytor, źródłowe assety i ich export entitlement Unknown, nie potrzebne do odczytania posiadanego .riv. DERIVED adapter 3–5 dni + przypadki assetów.
- **Prawa:** Runtime MIT; .riv, fonty, obrazy i audio mają osobne prawa Unknown. Film i redystrybucja .riv rozdzielone. Nie importować demo assetów bez praw.
- **Utrzymanie / ograniczenia:** Runtime commit 2026-11-11, docs 2026-11-10. Zaobserwowany drift: docs advance opisuje apply, typy rozdzielają advance/advanceAndApply; cookbook zawiera LinearAnimationInstnace. Nie kopiować bez dopasowania do pina.
- **Poziom dowodu:** DOCUMENTED; CODE_INSPECTED; NOT_RUN import, state replay, negative time, exports. Arbitrary seek/state serialization Unknown.
- **Właściciel docelowy:** FrameMotion proponowany adapter po poznaniu jego API/repo; Studio routing/QA; Toolbox entry dopiero osobny review i zgoda.
- **Forma:** ADAPTER
- **Rekomendacja:** P2 warunkowo: linear animation prototype najpierw. State machine: DERIVED reset do świeżej instancji + replay od 0 stałym krokiem i log inputów; jeżeli niedeterministyczne, bake klip albo reject. Nie obiecywać seed API.
- **Test akceptacyjny:** NOT_RUN: 60-frame .riv linear i osobna machine z triggerem w f12; sek.wynik vs fresh f47 i [47,0,47]. Fixed dt=1/fps, nie pojedynczy advance(47/fps). Sprawdzić memory cleanup, fonts PL, mask unsupported w Canvas2D, alpha i loop na export.
- **Deep dive w DEEP_DIVES.md:** True

Źródła: [KB01](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/hyperframes-workflow/references/motion-toolkit-runtime-cards.md), [KS20](https://github.com/rive-app/rive-docs/blob/047f52be339575f86eb0710a5512e2c600e14313/runtimes/web/low-level-api-usage.mdx), [KS21](https://github.com/rive-app/rive-docs/blob/047f52be339575f86eb0710a5512e2c600e14313/feature-support.mdx), [KS22](https://github.com/rive-app/rive-wasm/blob/b61517a5bdcdcce54c4b5f50e86bac7e11fadecc/js/src/rive_advanced.mjs.d.ts), [KS23](https://github.com/rive-app/rive-wasm/blob/b61517a5bdcdcce54c4b5f50e86bac7e11fadecc/wasm/examples/parcel_example/index.js), [KS24](https://github.com/rive-app/rive-wasm/blob/b61517a5bdcdcce54c4b5f50e86bac7e11fadecc/js/npm/webgl2_advanced/package.json), [KS25](https://github.com/rive-app/rive-wasm/blob/b61517a5bdcdcce54c4b5f50e86bac7e11fadecc/LICENSE).

## K07 — FFmpeg colordetect: semantyka straight/premultiplied i kolor
Kanoniczny URL: [FFmpeg colordetect: semantyka straight/premultiplied i kolor](https://github.com/FFmpeg/FFmpeg/blob/b9a9bf7a3a74c2c62bac4c766666d1ca93b2c6ba/libavfilter/vf_colordetect.c)

- **Owner:** FFmpeg contributors; Niklas Haas (file)
- **Pin / tag:** FFmpeg source b9a9bf7a3a74c2c62bac4c766666d1ca93b2c6ba; local filter availability Unknown
- **Data przeglądu:** 2026-11-11
- **Klasa:** B
- **Nowość:** KNOWN_NEW_CAPABILITY
- **Problem:** has_alpha lub alpha-capable pix_fmt nie dowodzi aktywnej przezroczystości, poprawnego premultiplication ani kolorów krawędzi po compositingu.
- **Delta wobec baseline:** KB03/KB04 już sprawdzają alpha i encoded metadata. Margines: klasyfikacja undetermined zamiast fałszywego premultiplied, fixture straight/premultiplied na wielu tłach i kontrola range. Nie przywraca removed ffmpeg-skill.
- **Dokładny moduł:** libavfilter/vf_colordetect.c; docs colordetect/alphaextract/premultiply jako dalszy punkt wdrożenia; procedura w DEEP_DIVES.md, K07, jest propozycją DERIVED.
- **Wejścia / wyjścia / edytowalność / alfa:** IN: lokalny decoded video/frame z alpha + deklaracja color range/matrix/transfer/primaries/alpha mode. OUT: obserwacje none/opaque/straight/undetermined i osobne kompozyty; brak edycji źródłowego motion.
- **Runtime / host / zasoby:** Lokalny FFmpeg z colordetect filtrem; minimum release Unknown, sprawdzić filter list przy przyszłym wdrożeniu. Kod wymaga planar non-float/non-hardware formats, max16-bit; CPU; RAM Unknown. Offline.
- **Eksport:** Kontrola po MP4/WebM/ProRes/PNG decode; alpha-capable format potrzebny do transparent overlay. Film MP4 typowo przekazywać z uzgodnionym tłem; nie zakładać alpha w H264. EXR float wymaga innej ścieżki niż odczytany filtr.
- **Koszt / konto / sieć:** Bez konta/klucza/usługi. Wykorzystać istniejący FFmpeg, nie instalować ani aktualizować dla badania. DERIVED 0.5–1 dzień fixture+notes.
- **Prawa:** Odczytany filtr LGPL-2.1-or-later; licencja całego binarium zależy od build options Unknown. Materiały/codec delivery prawa osobne. Adaptować wiedzę, bez bundlowania binariów.
- **Utrzymanie / ograniczenia:** Plik bieżącego HEAD 2026-11-11; nie potwierdza obecności w lokalnym buildzie. Heurystyka: transparent może pozostać undetermined; brak dowodu, że dane są premultiplied.
- **Poziom dowodu:** CODE_INSPECTED; DOCUMENTED ograniczony odczyt docs; NOT_RUN filtr/decode/kompozyt.
- **Właściciel docelowy:** Studio motion QA i FrameCut przy finalnym compositingu; Toolbox bez nowego wpisu.
- **Forma:** KNOWLEDGE_ONLY
- **Rekomendacja:** P1: rozszerzyć alfa evidence o decoded alpha extrema i 3 backgrounds. Filtr tylko opcjonalne świadectwo, nie źródło automatycznej konwersji.
- **Test akceptacyjny:** NOT_RUN: prosty półprzezroczysty czerwony glow, straight i premultiplied PNG, opaque-control. Composite na czarnym/białym/magenta; ocena halo całej pętli. Decode export, zachowanie alpha i zakresu; undetermined ≠ PASS.
- **Deep dive w DEEP_DIVES.md:** True

Źródła: [KB03](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/remotion-video-production/references/remotion-implementation-notes.md), [KB04](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/hyperframes-workflow/templates/motion-qa-record.md), [KB13](https://github.com/FrameCoreWorks/framecore-works-toolbox/blob/adc8094f8e087889e4337c99dd0d267ae1b11a51/reviews/ffmpeg-skill.md), [KS26](https://github.com/FFmpeg/FFmpeg/blob/b9a9bf7a3a74c2c62bac4c766666d1ca93b2c6ba/libavfilter/vf_colordetect.c), [KS27](https://ffmpeg.org/ffmpeg-filters.html), [KS31](https://github.com/FFmpeg/FFmpeg/blob/b9a9bf7a3a74c2c62bac4c766666d1ca93b2c6ba/libavfilter/vf_colordetectdsp.h).

## K08 — GSAP seek callback contract — uzupełnienie istniejącego skilla
Kanoniczny URL: [GSAP seek callback contract — uzupełnienie istniejącego skilla](https://gsap.com/docs/v3/GSAP/Timeline/seek()/)

- **Owner:** GreenSock/Webflow
- **Pin / tag:** gsap-skills aed9cfd3277740755f6bfc1155c7aa645403b760; GSAP runtime pin Unknown
- **Data przeglądu:** 2026-11-11
- **Klasa:** B
- **Nowość:** KNOWN_NEW_CAPABILITY
- **Problem:** Stan zbudowany tylko w onStart/onComplete/tl.call może różnić się po seek, ponieważ seek domyślnie tłumi callbacks.
- **Delta wobec baseline:** Sam gsap-skills i timeline są ALREADY_COVERED. Wąska nowość to negative fixture callback-only state oraz zakaz polegania na callbackach przy odtwarzaniu klatki; ogólny seek/clock już KB01/KB04.
- **Dokładny moduł:** Official Timeline.seek() docs; gsap-timeline/SKILL.md (już katalog).
- **Wejścia / wyjścia / edytowalność / alfa:** IN: paused timeline, master seconds, stan sceny; OUT: właściwości DOM/Canvas. DERIVED: pełny stan wizualny od czasu, callbacks dla niekrytycznych zdarzeń; parametry duration/ease/labels.
- **Runtime / host / zasoby:** Istniejący GSAP/browser, HTML/SVG/Canvas zależnie od sceny. CPU/GPU/RAM Unknown. Local package offline; CDN byłby siecią. Brak konieczności instalowania nowego skilla.
- **Eksport:** Istniejący HyperFrames capture/export; GSAP samo nie koduje MP4/PNG/WebM/EXR. Alfa zależna od capture.
- **Koszt / konto / sieć:** Dokumentacja i skills bez konta/key; runtime licencja odrębna. Szacunek DERIVED 0.25–0.5 dnia.
- **Prawa:** Skills MIT w przeczytanym pliku. Runtime GSAP ma odrębne warunki opisane w KB09; aktualna prawna kwalifikacja konkretnej integracji Unknown. Nie redystrybuować źródłowych assetów na tej podstawie.
- **Utrzymanie / ograniczenia:** Skills HEAD aed9cfd 2026-04-21 pokrywa katalog; docs read 2026-11-11. Brak nowego repo do wpisania.
- **Poziom dowodu:** DOCUMENTED; CODE_INSPECTED skill, nie runtime; NOT_RUN timeline/render.
- **Właściciel docelowy:** Studio hyperframes-workflow; istniejący Toolbox gsap-skills.
- **Forma:** KNOWLEDGE_ONLY
- **Rekomendacja:** P1: krótki addendum do istniejącego ownera i 1 test. REJECT jako nowy Toolbox entry lub nowy skill.
- **Test akceptacyjny:** NOT_RUN: tl.call zmienia tekst w 0.5 s; porównanie sequential vs seek(1,true) po świeżym init. Naprawiony pure visual state daje tę samą klatkę po 1→0→1 s. Nie rozwiązywać przez bezwarunkowe replay skutków ubocznych.
- **Deep dive w DEEP_DIVES.md:** False

Źródła: [KB01](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/hyperframes-workflow/references/motion-toolkit-runtime-cards.md), [KB04](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/hyperframes-workflow/templates/motion-qa-record.md), [KB08](https://github.com/FrameCoreWorks/framecore-works-toolbox/blob/adc8094f8e087889e4337c99dd0d267ae1b11a51/.claude-plugin/marketplace.json), [KB09](https://github.com/FrameCoreWorks/framecore-works-toolbox/blob/adc8094f8e087889e4337c99dd0d267ae1b11a51/reviews/gsap-skills.md), [KS28](https://gsap.com/docs/v3/GSAP/Timeline/seek()/), [KS29](https://github.com/greensock/gsap-skills/blob/aed9cfd3277740755f6bfc1155c7aa645403b760/skills/gsap-timeline/SKILL.md).

## K09 — Remotion flickering cookbook — kontrola negatywna nowości
Kanoniczny URL: [Remotion flickering cookbook — kontrola negatywna nowości](https://www.remotion.dev/docs/flickering)

- **Owner:** Remotion
- **Pin / tag:** Live docs 2026-11-11; runtime pin Unknown
- **Data przeglądu:** 2026-11-11
- **Klasa:** B
- **Nowość:** ALREADY_COVERED
- **Problem:** Zależność od poprzedniej klatki lub wall-clock powoduje różnice między preview a równoległym renderem.
- **Delta wobec baseline:** useCurrentFrame, seeded data, loading gate i seek-order są już KB01/KB03/KB04. Nie nowy zasób do wdrożenia; przydatne oficjalne uzasadnienie, że concurrency=1 nie zapewnia synchronizacji.
- **Dokładny moduł:** Official docs Flickering: multithreading i asset loading.
- **Wejścia / wyjścia / edytowalność / alfa:** IN frame/props/assets → image; istniejące komponenty/render API, bez nowego formatu.
- **Runtime / host / zasoby:** Obecny Remotion/React/Chromium; dokładne OS, CPU/GPU, RAM i wersje Unknown w tym researchu. Brak nowej instalacji; lokalne assets pozwalają offline.
- **Eksport:** Istniejący native Remotion export. Format/alpha w KB03 i docelowym kontrakcie; nie badano wykonawczo.
- **Koszt / konto / sieć:** Czytanie docs bez konta. Runtime komercyjne warunki/cena dla użytkownika Unknown; korzystać z istniejącej autoryzowanej ścieżki.
- **Prawa:** Licencja Remotion nie została tu ponownie oceniona; Unknown dla redystrybucji. Assety/fonty/filmy osobne prawa. Nie kopiujemy repo ani docs.
- **Utrzymanie / ograniczenia:** Dokumentacja odczytana 2026-11-11; nie wykonano wersyjnego diff repo. Ryzyko concurrency opisane przez autora.
- **Poziom dowodu:** DOCUMENTED; NOT_RUN produkt/render; brak OWN_TEST.
- **Właściciel docelowy:** Studio remotion-video-production.
- **Forma:** KNOWLEDGE_ONLY
- **Rekomendacja:** Nie tworzyć nowego skilla ani wpisu. Użyć jako linku źródłowego w QA K03; ranking nowości poza top.
- **Test akceptacyjny:** NOT_RUN: identyczne selected frames w świeżych browser contexts i shuffled order. concurrency=1 nie uznawać za dowód naprawy; full normal-speed watch finalnego pliku.
- **Deep dive w DEEP_DIVES.md:** False

Źródła: [KB01](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/hyperframes-workflow/references/motion-toolkit-runtime-cards.md), [KB03](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/remotion-video-production/references/remotion-implementation-notes.md), [KB04](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/hyperframes-workflow/templates/motion-qa-record.md), [KS30](https://www.remotion.dev/docs/flickering).

