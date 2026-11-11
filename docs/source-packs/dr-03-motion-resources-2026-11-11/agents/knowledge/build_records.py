"""Generate research records only; this does not execute candidate software."""
from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parent
DATE = '2026-11-11'
S = []
def source(id, url, kind, read_scope, claims, pin='Unknown'):
    S.append(dict(id=id,url=url,accessed=DATE,kind=kind,read_scope=read_scope,claims=claims,pin=pin))

ST='4611c9c4ed44579b8a2c0224c9276d955fccd8d6'
TB='adc8094f8e087889e4337c99dd0d267ae1b11a51'
OA='889471fcdbc2216ddc465715eff0e82784d5b8ee'
LI='6c9fe7c18ed8bab8a44637355171b2129cf5c720'
LW='bede03d25d232826e0c9dca1733d542d8a7754fb'
LD='a84a05f4353cb135a9cc29325a6e75bb735d0c0c'
RV='b61517a5bdcdcce54c4b5f50e86bac7e11fadecc'
RD='047f52be339575f86eb0710a5512e2c600e14313'
PW='3b438229c6a2ccdbe2d3572755935892203d83c3'
FF='b9a9bf7a3a74c2c62bac4c766666d1ca93b2c6ba'
GS='aed9cfd3277740755f6bfc1155c7aa645403b760'
def gh(repo,sha,path): return f'https://github.com/{repo}/blob/{sha}/{path}'
prefix='plugins/framecore-work-creative-studio/skills/'
baseline=[
('KB01','hyperframes-workflow/references/motion-toolkit-runtime-cards.md','Cały plik','Znane: frame-derived Three/Pixi/D3, Mediabunny timestamp/backpressure, Manim clip bridge, Lottie seek i prawa.'),
('KB02','hyperframes-workflow/references/motion-contract-json.md','Cały plik','Istniejący motion-score, racjonalny FPS, fonty, cues, captions, warianty i status zgody.'),
('KB03','remotion-video-production/references/remotion-implementation-notes.md','Cały plik','Deterministyczne klatki, ładowanie, alfa ProRes/WebM i QA już należą do baseline.'),
('KB04','hyperframes-workflow/templates/motion-qa-record.md','Cały plik','Cztery osobne werdykty oraz normal-speed review i seek-order już istnieją.'),
('KB05','hyperframes-workflow/assets/motion-quality/README.md','Cały plik','Inspect-encode, reviewFrames, motion activity, flash screen; nie zastępują odsłuchu/oglądu.'),
('KB06','hyperframes-workflow/assets/motion-sync/README.md','Cały plik','Beat grid, beats.py, lyric timing, band envelope i wcześniejszy AAC offset już istnieją.'),
('KB07','hyperframes-workflow/assets/motion-scenes/motion-scenes.mjs','Pobrany tekst; nagłówek i keepTogether oraz wyszukanie grapheme/Segmenter/font loading','Jednoliterowe wyrazy PL i jednostki łączone NBSP; nie znaleziono Segmenter w tym pliku. Nie jest to audyt całego repo.')]
for id,path,scope,claim in baseline: source(id,gh('FrameCoreWorks/framecore-works-creative-studio',ST,prefix+path),'BASELINE_CODE' if id=='KB07' else 'BASELINE_DOC',scope,claim,ST)
for id,path,claim in [
('KB08','.claude-plugin/marketplace.json','Aktywne m.in. gsap-skills, threejs-skills, manim-skill; katalog nie dowodzi instalacji hosta.'),
('KB09','reviews/gsap-skills.md','GSAP agent skills już zaakceptowane; MIT skills odrębne od licencji GSAP.'),
('KB10','reviews/threejs-skills.md','13 skills r186 już aktywne w katalogu.'),
('KB11','reviews/manim-skill.md','Manim skill już aktywny; dolne granice zależności, opcjonalny Kokoro.'),
('KB12','reviews/earshot-audio.md','Earshot wbudowany w Toolbox, normalna praca offline, osobne setup modeli.'),
('KB13','reviews/ffmpeg-skill.md','Wpis ffmpeg-skill removed 2026-10-31; nie proponować ponownego wpisu jako nowości.')]:
    source(id,gh('FrameCoreWorks/framecore-works-toolbox',TB,path),'BASELINE_DOC','Cały plik lub lines 1–95 dla KB10/KB11',claim,TB)
source('KB14',gh('FrameCoreWorks/framecore-open-assets',OA,'README.md'),'BASELINE_DOC','Cały README','Open Assets pozyskuje media z odrębnymi prawami, Studio/Toolbox opcjonalni konsumenci.',OA)
source('KS01','https://unicode.org/reports/tr29/tr29-49.html','PRIMARY_STANDARD','Sekcje 1–3, reguły grafemów i Testing','UAX29 rozróżnia extended i legacy grapheme clusters; preferowane extended; nie rozstrzyga składu wiersza.','Unicode 18.0.0; revision 49; 2026-09-01')
source('KS02','https://www.unicode.org/Public/18.0.0/ucd/auxiliary/GraphemeBreakTest.txt','DOCUMENTED','Test fixture: nagłówek, format i próbki danych; nie uruchomiono','Wersjonowany korpus granic ÷/×; corpus istnieje, wynik autora i zgodność hosta Unknown.','18.0.0; nagłówek 2026-06-12')
source('KS03','https://tc39.es/ecma402/#sec-intl.segmenter','PRIMARY_STANDARD','§19 Intl.Segmenter, FindBoundary, resolvedOptions','Grapheme/word/sentence; granice i dane lokalizacyjne zależą od implementacji.','Living spec odczyt 2026-11-11; bez SHA')
source('KS04','https://www.unicode.org/license.txt','PRIMARY_LICENSE','Cały tekst','Unicode License V3 wymaga zachowania notice przy dystrybucji danych/software.','Unicode License V3; 2026')
source('KS05','https://www.w3.org/TR/2023/WD-css-font-loading-3-20230406/','PRIMARY_STANDARD','FontFace load, FontFaceSet load/check/ready; wersja dokumentu','check może być true przy brakującej rodzinie lub wykluczeniu unicode-range; ready nie dowodzi konkretnego face.','W3C Working Draft 2023-04-06')
source('KS06','https://playwright.dev/docs/api/class-pageassertions','PRIMARY_DOC','toHaveScreenshot, animations, oczekiwanie stabilnych obrazów','Domyślne disabled przewija finite animations do końca i cofa infinite; stabilność dwóch screenshotów nie jest temporal QA.','Living docs; read 2026-11-11')
source('KS07','https://playwright.dev/docs/test-snapshots','PRIMARY_DOC','Visual comparisons, environment, update screenshots, threshold','Baseline screenshot powinien powstać w tym samym środowisku; threshold dotyczy różnic pikseli.','Living docs; read 2026-11-11')
source('KS08',gh('microsoft/playwright',PW,'tests/playwright-test/to-have-screenshot.spec.ts'),'CODE_INSPECTED','Lines 1–155','Kod testu oczekuje timeout żywej infinite animation i wyłączania animacji domyślnie; wynik uruchomienia autora Unknown.',PW)
source('KS09',gh('microsoft/playwright',PW,'package.json'),'CODE_INSPECTED','Lines 1–130','Snapshot repo 1.66.0-next, Node >=20, Apache-2.0, liczne dev/build/test scripts. Nie rekomendacja instalacji HEAD.',PW)
source('KS10','https://librosa.org/doc/0.11.0/generated/librosa.onset.onset_detect.html','PRIMARY_DOC','Całe API onset_detect','Units frames/samples/time; backtrack przesuwa do wcześniejszego minimum energii; sparse i multichannel mają warunki.','0.11.0 documentation')
source('KS11',gh('librosa/librosa',LI,'librosa/onset.py'),'CODE_INSPECTED','Lines 1–220','Kod konwersji units, brak onset zwraca pusty wynik; peak-pick/backtrack rozdzielone.',LI)
source('KS12',gh('librosa/librosa',LI,'tests/test_onset.py'),'CODE_INSPECTED','Lines 1–180; kod testu odczytany, bez uruchomienia','Test fixture: syntetyczny pulse train 120 BPM; testy parametrów hop/FFT/center i kształtu wyniku; wynik autora Unknown, nie dowód dokładności muzycznej.',LI)
source('KS13',gh('librosa/librosa',LI,'pyproject.toml'),'CODE_INSPECTED','Lines 1–180','HEAD wymaga Python >=3.12 i pakietów numba/numpy/scipy/scikit-learn/soundfile/pooch/soxr; nie utożsamiać z 0.11.0.',LI)
source('KS14',gh('librosa/librosa',LI,'LICENSE.md'),'PRIMARY_LICENSE','Cały LICENSE','ISC dla kodu; nie obejmuje dostarczonej muzyki.',LI)
source('KS15',gh('airbnb/lottie',LD,'supported-features.md'),'PRIMARY_DOC','Cała macierz; wybrane rows mask/matte/merge paths/text','Renderer-specific wsparcie; mask feather i web merge paths oznaczone unsupported, luma web Unknown.',LD)
source('KS16',gh('airbnb/lottie-web',LW,'test/index.html'),'CODE_INSPECTED','Cały plik','Harness DOMLoaded, autoplay/loop false, kolejne goToAndStop; białe tło i inclusive totalFrames nie są fixture alfa ani random seek.',LW)
source('KS17',gh('airbnb/lottie-web',LW,'test/index.js'),'CODE_INSPECTED','Lines 1–350; nie uruchomiono','Test recipe Puppeteer+pixelmatch, SVG/Canvas case list, threshold 0.1 i >200 different pixels. Komentarz mówi 50, kod 200. Wynik autora Unknown.',LW)
source('KS18',gh('airbnb/lottie-web',LW,'player/js/animation/AnimationItem.js'),'CODE_INSPECTED','Lines 450–510','goToAndStop(...,true) ustawia raw frame i pauzuje; nie jest dowodem kompatybilności grafiki.',LW)
source('KS19',gh('airbnb/lottie-web',LW,'package.json'),'CODE_INSPECTED','Cały manifest','5.13.0 MIT; test:create/compare i dev Puppeteer/pixelmatch; brak konieczności kopiowania całego harnessu.',LW)
source('KS20',gh('rive-app/rive-docs',RD,'runtimes/web/low-level-api-usage.mdx'),'PRIMARY_DOC','Cały cookbook','Kontrola własnego render loop, matching WASM, advance/apply/artboard/draw, flush WebGL; przykłady rAF wymagają adaptacji.',RD)
source('KS21',gh('rive-app/rive-docs',RD,'feature-support.mdx'),'PRIMARY_DOC','Cały plik; szczególnie web/layerMasks/fallbackFonts','Layer Masks potrzebują WebGL2 oraz GPU Canvas; Canvas/Canvas Lite ich nie wspierają; feature support zmienia się wersjami.',RD)
source('KS22',gh('rive-app/rive-wasm',RV,'js/src/rive_advanced.mjs.d.ts'),'CODE_INSPECTED','Artboard, LinearAnimationInstance, StateMachineInstance; lines 1060–1093 ponownie','Typy rozróżniają advance i advanceAndApply. LinearAnimationInstance ma time; sprzątanie WASM ręczne.',RV)
source('KS23',gh('rive-app/rive-wasm',RV,'wasm/examples/parcel_example/index.js'),'CODE_INSPECTED','Render loop i inicjalizacja','Przykład używa elapsedSeconds; nie dowodzi absolutnego seek ani resetu state machine.',RV)
source('KS24',gh('rive-app/rive-wasm',RV,'js/npm/webgl2_advanced/package.json'),'CODE_INSPECTED','Cały manifest','2.50.0; paczka dostarcza mjs, wasm, fallback wasm, d.ts; brak npm dependencies nie usuwa wymogu WASM/GPU.',RV)
source('KS25',gh('rive-app/rive-wasm',RV,'LICENSE'),'PRIMARY_LICENSE','Cały LICENSE','MIT runtime; .riv/fonty/media wymagają własnych praw.',RV)
source('KS26',gh('FFmpeg/FFmpeg',FF,'libavfilter/vf_colordetect.c'),'CODE_INSPECTED','Cały plik','Filtr raportuje straight, opaque, none lub undetermined; brak wykrytego straight nie potwierdza premultiplied; wyklucza float/hardware/palette formats.',FF)
source('KS27','https://ffmpeg.org/ffmpeg-filters.html','PRIMARY_DOC','Wyniki primary search: colordetect i premultiply; pełne open timeout','Dokumentacja opisuje alpha_mode/color_range oraz premultiply. Ograniczona lektura uzupełniona KS26.','Live documentation; checked 2026-11-11')
source('KS28','https://gsap.com/docs/v3/GSAP/Timeline/seek()/','PRIMARY_DOC','seek(position,suppressEvents)','seek domyślnie suppressEvents true; callback nie jest zapewnionym nośnikiem stanu po seek.','GSAP v3 docs; read 2026-11-11')
source('KS29',gh('greensock/gsap-skills',GS,'skills/gsap-timeline/SKILL.md'),'CODE_INSPECTED','Cały SKILL.md','Timeline, labels, position, playback i paused; skills już baseline.',GS)
source('KS30','https://www.remotion.dev/docs/flickering','PRIMARY_DOC','Cały artykuł tekstowy; nie oglądano filmu','Wiele kart nie współdzieli stanu; concurrency=1 nie zapewnia synchronizacji; frame purity i loading gate.','Living documentation; read 2026-11-11')
source('KS31',gh('FFmpeg/FFmpeg',FF,'libavfilter/vf_colordetectdsp.h'),'CODE_INSPECTED','Cały nagłówek: enum FFAlphaDetect i makra detect_alpha','Brak pozytywnej identyfikacji premultiplied jest jawnie opisany. Test full range porównuje color > alpha + threshold; transparent bez tej przesłanki pozostaje undetermined.',FF)
source('KS32',gh('microsoft/playwright',PW,'packages/playwright/src/matchers/toMatchSnapshot.ts'),'CODE_INSPECTED','Konteksty toHaveScreenshot i expectScreenshot, szczególnie lines 331–445','Matcher domyślnie ustawia animations disabled, przekazuje omitBackground, scale i porównanie; updateSnapshots może przepisać expected, więc to osobna decyzja od weryfikacji.',PW)

C=[]
def candidate(id,name,url,owner,pin,novelty,problem,baseline_delta,module,io,runtime,export,cost,rights,maintenance,evidence,target_owner,integration,recommendation,test,source_ids):
    C.append(dict(id=id,name=name,url=url,owner=owner,pin=pin,reviewed=DATE,**{'class':'B'},novelty=novelty,problem=problem,baseline_delta=baseline_delta,module=module,io=io,runtime=runtime,export=export,cost=cost,rights=rights,maintenance=maintenance,evidence=evidence,target_owner=target_owner,integration=integration,recommendation=recommendation,test=test,source_ids=source_ids))

candidate('K01','Unicode UAX29 + GraphemeBreakTest: kontrakt kinetic text','https://unicode.org/reports/tr29/tr29-49.html','Unicode Consortium; ECMAScript Intl TC39','Unicode 18.0.0 UAX29 rev49; corpus 18.0.0; ECMA402 live, runtime Unicode version Unknown','KNOWN_NEW_CAPABILITY',
'Reveal dzielący UTF-16 albo codepoints może oddzielać akcent od litery lub rozbić emoji; polski tekst w NFC i NFD nie może zmieniać liczby kroków reveal.',
'Baseline ma keepTogether dla polskich jednoliterowych wyrazów/jednostek i dokładną copy. Marginalna propozycja: wersjonowane granice extended grapheme, zachowanie bajtów copy, fixture NFD/ZWJ. Brak takiego kontraktu w przeczytanych plikach; brak twierdzenia o całym repo.',
'UAX29 §3 i §7; auxiliary/GraphemeBreakTest.txt; Intl.Segmenter granularity=grapheme.',
'IN: zatwierdzony UTF-8 text, locale pl, strategia segmentacji i jej wersja. OUT: segmenty z oryginalnymi indeksami; brak mediów. Parametryzacja: granularity/locale; exact copy niezmieniona; alfa N/A.',
'Dokumentacja/test data bez runtime. Adapter JS wymaga hostowego Intl.Segmenter i jego ICU; przeglądarka/headless/Node zależne od wersji; CPU, RAM Unknown; offline po przypięciu źródła.',
'Segmenty zasilają obecny HTML/SVG/Canvas/Remotion renderer; same nie eksportują MP4/PNG/EXR/WebM.',
'Odczyt bez konta/klucza/opłat. Brak usługi; pobranie corpus w przyszłym wdrożeniu wymaga zwykłej sieci. Koszt adaptacji DERIVED 0.5–1 dzień.',
'Unicode data: License V3 z notice. Standard cytować; własny przepis nie kopiuje całości. Fonty/emoji glyphs/media: osobne prawa Unknown. Wyrenderowany film i redystrybucja fontu to odrębne decyzje.',
'Wersja Unicode 18 stabilna w odczytanym źródle; przeglądarka może mieć inną wersję Unicode/CLDR. Nie wymuszać upgrade runtime; mismatch raportować.',
'DOCUMENTED test fixture; wynik uruchomienia autora Unknown. NOT_RUN zgodność segmentera i render.',
'Studio hyperframes-workflow + remotion-video-production; FrameMotion proponowany konsument, obecne funkcje Unknown.',
'SKILL_ADAPTATION',
'P0: dopisać w istniejącym właścicielu, bez nowego skilla/dependency. Granice przygotować raz, zachować hash i mapowanie do exact copy.',
'NOT_RUN: Zażółć gęślą jaźń, NFC/NFD, Z+combining dot, a+ogonek, 👩🏽‍💻, 🇵🇱, NBSP; każdy reveal odsłania pełny grafem. Obejrzeć wszystkie klatki reveal 16:9/9:16, porównać final copy i seek [0,47,1,47,0].',
['KB02','KB07','KS01','KS02','KS03','KS04'])

candidate('K02','CSS Font Loading: negatywne przypadki gotowości fontów','https://www.w3.org/TR/2023/WD-css-font-loading-3-20230406/','W3C CSS Working Group','Working Draft 2023-04-06','KNOWN_NEW_CAPABILITY',
'fonts.ready/check może dać pozorny PASS, gdy użyto fallbacku lub błędnej nazwy rodziny; pomiar przed właściwym face daje inny układ i clipping.',
'KB01 już wymaga actual face readiness. Nowa użyteczność: źródłowo udokumentowane negatywne testy missing-family i unicode-range, odrębna kontrola face/coverage/layout, nie kolejna ogólna zasada await fonts.',
'FontFace.load; FontFaceSet.load/check/ready; testy negatywne opisane w tej karcie i dodatku do K01 w DEEP_DIVES.md.',
'IN: lokalny font file+hash+face descriptors i pełna copy; OUT: loaded face list, błędy, szerokości/bounds i obraz kontrolny; parametry weight/style/stretch; alfa N/A.',
'Browser Font Loading API; dokładny browser/OS/DPR/fonts pin; CPU; headless możliwy zależnie od hosta. RAM Unknown. Lokalny face pozwala offline; font URL może uruchomić sieć.',
'Bramka przed pomiarami i istniejącym MP4/PNG/WebM exportem; nie renderer. EXR N/A.',
'Dokumentacja bez opłat/konta. Własny font może mieć koszt; Unknown. Szacunek DERIVED 0.5–1 dzień.',
'W3C permissive document license wskazana w spec; font licencjonowany osobno. Prawo użycia tekstu w filmie nie daje prawa bundlowania fontu; Unknown per font.',
'Spec Working Draft, nie Recommendation. API opisane stabilnie, faktyczne face/coverage nadal do próby na wybranym browserze.',
'DOCUMENTED; NOT_RUN font loading/render. Brak twierdzenia o glyph coverage na podstawie samego check().',
'Studio obecny kontrakt fonts i QA; Caption Studio dla tekstu; FrameMotion proponowany konsument.',
'SKILL_ADAPTATION',
'P0: dwa negative fixtures i wymóg hashów fontów; bez nowej biblioteki. Brak pokrycia → jawny FAIL/Unknown, bez cichego system fallback.',
'NOT_RUN: prawidłowy face vs literówka family vs subset bez ąęł; require resolved exact face, glyph review, identyczne bounds po cold/warm load. Ogląd reveal i readable hold w obu proporcjach.',
['KB01','KB02','KB03','KS05'])

candidate('K03','Playwright screenshot assertions jako kontrolowany oracle motion','https://playwright.dev/docs/api/class-pageassertions','Microsoft Playwright',PW+'; package 1.66.0-next odczytany, nie rekomendowany install','KNOWN_NEW_CAPABILITY',
'Domyślny screenshot test może usunąć animację, którą ma badać, a statyczny PASS może ukryć migotanie i zależność od kolejności klatek.',
'Baseline ma seek-order i full watch. Nowy punkt: jawna opcja animations=allow po zatrzymaniu własnego zegara oraz negative fixture wykrywający ucieczkę wall-clock; upstream test pokazuje tę pułapkę.',
'docs PageAssertions.toHaveScreenshot; tests/playwright-test/to-have-screenshot.spec.ts lines 1–150; wzór testu DERIVED w DEEP_DIVES.md, K03.',
'IN: gotowa scena z prepare/setFrame/settled i frame list; OUT: PNG expected/actual/diff + frame/env manifest. Edytowalne testy; nie daje edytowalnej animacji. Alfa screenshot wymaga osobnej konfiguracji i decode QA.',
'Odczytany HEAD Node>=20, browser install osobny. Headless/OS/GPU/DPR pin; pamięć Unknown. Offline dla lokalnej sceny i zasobów; browser/runtime nie zakładane zainstalowane.',
'PNG/WebP snapshots; finalny MP4/WebM z istniejącej ścieżki, następnie decode i temporal watch. Screenshoty nie dowodzą encodera ani EXR.',
'Bez konta/klucza dla local runner; setup może pobierać browser. Korzystać z istniejącej instalacji. Koszt adaptacji DERIVED 1–2 dni.',
'Repo/test code Apache-2.0 wg manifestu i nagłówka testu. Prawa przedstawionej sceny, fontów i assetów osobne Unknown.',
'Odczyt HEAD 2026-11-11, development 1.66.0-next. Przy wdrożeniu wybór istniejącej stabilnej wersji i lock, nie update do HEAD; baseline środowiskowy konieczny.',
'DOCUMENTED; CODE_INSPECTED scenariusze testów; wynik uruchomienia autora Unknown; wszystkie nasze testy NOT_RUN.',
'Studio istniejący motion QA; adapter testowy dla FrameMotion po ustaleniu API; Toolbox bez nowego wpisu.',
'SKILL_ADAPTATION',
'P0: rozszerzyć obecny QA o negative-control i jawny capture mode, zachowując cztery oddzielne werdykty. Nie kopiować całego Playwright repo.',
'NOT_RUN: 2 s scena z frame-derived pozycją + celowo błędny CSS loop; prawidłowa scena identyczna przy shuffled seek, błędna wykryta. Przejście co klatkę + normal speed finalnego encode; expected snapshots zatwierdzone wizualnie.',
['KB04','KB05','KS06','KS07','KS08','KS09','KS32'])

candidate('K04','librosa onset: czas ataku vs backtracked slice point','https://librosa.org/doc/0.11.0/generated/librosa.onset.onset_detect.html','librosa development team','API docs 0.11.0; inspected HEAD '+LI+' (nie tożsamy runtime)','KNOWN_NEW_CAPABILITY',
'Pomieszanie audio analysis frames z video frames lub użycie backtrack do wizualnego hitu powoduje błędny sync. Onset nie jest automatycznie beat/downbeat.',
'KB06 ma beats.py i per-frame band hits; Toolbox ma Earshot. Dodatek to precyzyjna rozdzielność onsetSample/sliceSample i walidacja jednostek. Nie wymieniać istniejącej analizy ani nie dodawać pełnego silnika bez testu przewagi.',
'librosa/onset.py onset_detect/onset_backtrack; tests/test_onset.py pulse train; 0.11.0 API recipe.',
'IN: lokalny PCM, sr, hop_length, channel policy, trim origin, peak params. OUT: sample/time onset indices i osobne slice points; później JSON cue frames. Edytowalne dane; alfa N/A.',
'Inspected HEAD Python>=3.12 z numba/numpy/scipy/scikit-learn/soundfile/pooch/soxr; 0.11.0 requirements tu Unknown. CPU, RAM zależne od długości, Unknown. Offline dla lokalnego PCM; przykładowe downloadery niepotrzebne.',
'Nie renderuje; cue JSON do motion-score, istniejący exporter i mux. Encoded audio trzeba zdekodować, zmierzyć offset i odsłuchać.',
'Brak konta/API dla lokalnej analizy; CPU i zależności. Przykładowe load/ex mogą pobierać media: nie używać w offline fixtures. DERIVED 1–2 dni jeśli librosa już dostępna, inaczej osobna decyzja.',
'Kod ISC. Audio/dataset/example recordings mają własne prawa Unknown; fixture własny syntetyczny bez materiału muzycznego. Nie bundlować przykładów muzycznych.',
'HEAD od 2026-11-10; rozjazd docs0.11 i HEAD jawny. Pin wersji konieczny, obecna wersja Earshot/librosa na hoście Unknown.',
'DOCUMENTED; CODE_INSPECTED syntetyczny test fixture; wynik uruchomienia autora Unknown; NOT_RUN sync/audio/decode.',
'Studio audio-production-director/motion-sync; Toolbox Earshot tylko jeśli istniejąca capability wymaga rozszerzenia; FrameCut mux/edycja.',
'KNOWLEDGE_ONLY',
'P1: najpierw dopisać unit contract i fixture. OPTIONAL_DEPENDENCY dopiero gdy porównanie z istniejącymi beats/envelope/Earshot wykaże potrzebę.',
'NOT_RUN: pulse train 48 kHz o onsetach 0.25/0.75/1.25 s + 7 ms przesunięcie, hop 128/512, cisza i ramp; round(sample/sr * fpsNum/fpsDen) raz. Tolerancja mierzona, nie zakładana; listen + waveform/marker i first/last event po encode.',
['KB06','KB12','KS10','KS11','KS12','KS13','KS14'])

candidate('K05','Lottie feature matrix + upstream frame-diff recipe','https://github.com/airbnb/lottie/blob/'+LD+'/supported-features.md','Airbnb Lottie maintainers','matrix '+LD+'; lottie-web '+LW+' (5.13.0)','KNOWN_NEW_CAPABILITY',
'Poprawny JSON i działający seek nie gwarantują mask/matte/text/blur w wybranym SVG/Canvas rendererze ani prawidłowej alfy.',
'KB01 już zawiera Lottie seek/subframe/rights. Nowy margines: konkretny feature inventory + minimalny dwurendererowy fixture i krytyka upstream white-background sequential harness; żadna nowa obsługa useAnimations/Generative Icons.',
'supported-features.md; lottie-web/test/index.html + test/index.js; AnimationItem.goToAndStop.',
'IN: uprawniony JSON, fr/ip/op, renderer pin i resource hashes; OUT: feature flags oraz PNG frame diffs i verdict per renderer. JSON edytowalny; layout/glyph asset zależne od źródła; alfa wymaga testu.',
'lottie-web browser SVG/Canvas, JS; harness Node+Puppeteer+pixelmatch+pngjs+express. CPU/GPU zależne od browsera; RAM Unknown. Local assets offline; external URLs należy wykryć, nie fetch automatycznie.',
'DOM/SVG/Canvas capture do PNG, następnie istniejący Remotion/HyperFrames eksport; .lottie archive ma odrębny player. Brak bezpośredniej gwarancji MP4/WebM/EXR.',
'Kod bez konta/klucza; zależności testowe i browser osobno. Niewielki wzorzec zamiast kopiowania całego harnessu. DERIVED 1–2 dni.',
'lottie-web MIT wg manifestu; test animations/gallery prawa odrębne Unknown, użyć własnych fixtures. Film reuse wymaga praw źródłowego assetu; redystrybucja JSON nie wynika z MIT playera.',
'Odczytany HEAD lottie-web ostatni commit 2024-11-19, matrix 2026-03-25. Matrix nie przypina każdej funkcji do wersji playera. Test harness ma komentarz 50 vs kod >200 px oraz białe tło; nie kopiować bez oceny.',
'DOCUMENTED; CODE_INSPECTED test recipe; wynik uruchomienia autora Unknown. NOT_RUN wszystkie nowe renderery/asset compatibility.',
'Studio hyperframes-workflow i remotion-video-production; FrameMotion proponowany importer; Open Assets provenance.',
'SKILL_ADAPTATION',
'P1: import gate renderer/version/features/resources + per-asset visual QA. Unsupported → jawna odmowa lub zaakceptowany bake do klatek, bez cichej utraty feature.',
'NOT_RUN: własny JSON trim path/alpha matte/tekst PL + osobny known-unsupported mask feather. Frames 0,N-1 i granice, shuffled seek, PNG alpha na białym/czarnym/magenta. Obejrzeć cały 2 s loop; JSON schema PASS nie daje visual PASS.',
['KB01','KB04','KS15','KS16','KS17','KS18','KS19'])

candidate('K06','Rive low-level cookbook: replay sterowany klatką i renderer gate','https://github.com/rive-app/rive-docs/blob/'+RD+'/runtimes/web/low-level-api-usage.mdx','Rive','docs '+RD+'; runtime '+RV+'; webgl2-advanced manifest 2.50.0','NEW',
'Interaktywny .riv ze state machine nie ma wykazanego absolutnego seek i może zależeć od wcześniejszych inputów; renderer może nie mieć wymaganej funkcji.',
'W przeczytanym baseline Lottie/Canvas/Three występują, Rive replay cookbook nie występuje. NEW dotyczy proponowanego kontraktu i wiedzy, nie deklaracji gotowego supportu FrameMotion. Ogólna zasada fixed clock już istnieje.',
'runtimes/web/low-level-api-usage.mdx; feature-support.mdx; js/src/rive_advanced.mjs.d.ts; wasm/examples/parcel_example/index.js.',
'IN: lokalny .riv + assets+fonts, artboard, animation/stateMachine, fixed input event trace, dimensions, FPS. OUT: Canvas frame i export manifest. Parametry przez inputs/data binding zależnie od pin; .riv runtime file nie zastępuje źródła projektu edytora; alfa Unknown przed testem.',
'JS/WASM i Canvas2D lub WebGL2; Layer Masks potrzebują WebGL2+GPU Canvas. RAM/OS support/real host GPU Unknown. Offline możliwy z lokalnym matching WASM i wszystkimi resources; embedded scripting/out-of-band assets wymagają osobnej inspekcji.',
'DERIVED: capture kontrolowanych Canvas frames → PNG lub istniejący encoder. MP4/WebM poprzez osobny exporter; alpha i encoded fidelity NOT_RUN. EXR brak udokumentowanej drogi tutaj.',
'Runtime MIT bez API key w lokalnej ścieżce; edytor, źródłowe assety i ich export entitlement Unknown, nie potrzebne do odczytania posiadanego .riv. DERIVED adapter 3–5 dni + przypadki assetów.',
'Runtime MIT; .riv, fonty, obrazy i audio mają osobne prawa Unknown. Film i redystrybucja .riv rozdzielone. Nie importować demo assetów bez praw.',
'Runtime commit 2026-11-11, docs 2026-11-10. Zaobserwowany drift: docs advance opisuje apply, typy rozdzielają advance/advanceAndApply; cookbook zawiera LinearAnimationInstnace. Nie kopiować bez dopasowania do pina.',
'DOCUMENTED; CODE_INSPECTED; NOT_RUN import, state replay, negative time, exports. Arbitrary seek/state serialization Unknown.',
'FrameMotion proponowany adapter po poznaniu jego API/repo; Studio routing/QA; Toolbox entry dopiero osobny review i zgoda.',
'ADAPTER',
'P2 warunkowo: linear animation prototype najpierw. State machine: DERIVED reset do świeżej instancji + replay od 0 stałym krokiem i log inputów; jeżeli niedeterministyczne, bake klip albo reject. Nie obiecywać seed API.',
'NOT_RUN: 60-frame .riv linear i osobna machine z triggerem w f12; sek.wynik vs fresh f47 i [47,0,47]. Fixed dt=1/fps, nie pojedynczy advance(47/fps). Sprawdzić memory cleanup, fonts PL, mask unsupported w Canvas2D, alpha i loop na export.',
['KB01','KS20','KS21','KS22','KS23','KS24','KS25'])

candidate('K07','FFmpeg colordetect: semantyka straight/premultiplied i kolor','https://github.com/FFmpeg/FFmpeg/blob/'+FF+'/libavfilter/vf_colordetect.c','FFmpeg contributors; Niklas Haas (file)','FFmpeg source '+FF+'; local filter availability Unknown','KNOWN_NEW_CAPABILITY',
'has_alpha lub alpha-capable pix_fmt nie dowodzi aktywnej przezroczystości, poprawnego premultiplication ani kolorów krawędzi po compositingu.',
'KB03/KB04 już sprawdzają alpha i encoded metadata. Margines: klasyfikacja undetermined zamiast fałszywego premultiplied, fixture straight/premultiplied na wielu tłach i kontrola range. Nie przywraca removed ffmpeg-skill.',
'libavfilter/vf_colordetect.c; docs colordetect/alphaextract/premultiply jako dalszy punkt wdrożenia; procedura w DEEP_DIVES.md, K07, jest propozycją DERIVED.',
'IN: lokalny decoded video/frame z alpha + deklaracja color range/matrix/transfer/primaries/alpha mode. OUT: obserwacje none/opaque/straight/undetermined i osobne kompozyty; brak edycji źródłowego motion.',
'Lokalny FFmpeg z colordetect filtrem; minimum release Unknown, sprawdzić filter list przy przyszłym wdrożeniu. Kod wymaga planar non-float/non-hardware formats, max16-bit; CPU; RAM Unknown. Offline.',
'Kontrola po MP4/WebM/ProRes/PNG decode; alpha-capable format potrzebny do transparent overlay. Film MP4 typowo przekazywać z uzgodnionym tłem; nie zakładać alpha w H264. EXR float wymaga innej ścieżki niż odczytany filtr.',
'Bez konta/klucza/usługi. Wykorzystać istniejący FFmpeg, nie instalować ani aktualizować dla badania. DERIVED 0.5–1 dzień fixture+notes.',
'Odczytany filtr LGPL-2.1-or-later; licencja całego binarium zależy od build options Unknown. Materiały/codec delivery prawa osobne. Adaptować wiedzę, bez bundlowania binariów.',
'Plik bieżącego HEAD 2026-11-11; nie potwierdza obecności w lokalnym buildzie. Heurystyka: transparent może pozostać undetermined; brak dowodu, że dane są premultiplied.',
'CODE_INSPECTED; DOCUMENTED ograniczony odczyt docs; NOT_RUN filtr/decode/kompozyt.',
'Studio motion QA i FrameCut przy finalnym compositingu; Toolbox bez nowego wpisu.',
'KNOWLEDGE_ONLY',
'P1: rozszerzyć alfa evidence o decoded alpha extrema i 3 backgrounds. Filtr tylko opcjonalne świadectwo, nie źródło automatycznej konwersji.',
'NOT_RUN: prosty półprzezroczysty czerwony glow, straight i premultiplied PNG, opaque-control. Composite na czarnym/białym/magenta; ocena halo całej pętli. Decode export, zachowanie alpha i zakresu; undetermined ≠ PASS.',
['KB03','KB04','KB13','KS26','KS27','KS31'])

candidate('K08','GSAP seek callback contract — uzupełnienie istniejącego skilla','https://gsap.com/docs/v3/GSAP/Timeline/seek()/','GreenSock/Webflow','gsap-skills '+GS+'; GSAP runtime pin Unknown','KNOWN_NEW_CAPABILITY',
'Stan zbudowany tylko w onStart/onComplete/tl.call może różnić się po seek, ponieważ seek domyślnie tłumi callbacks.',
'Sam gsap-skills i timeline są ALREADY_COVERED. Wąska nowość to negative fixture callback-only state oraz zakaz polegania na callbackach przy odtwarzaniu klatki; ogólny seek/clock już KB01/KB04.',
'Official Timeline.seek() docs; gsap-timeline/SKILL.md (już katalog).',
'IN: paused timeline, master seconds, stan sceny; OUT: właściwości DOM/Canvas. DERIVED: pełny stan wizualny od czasu, callbacks dla niekrytycznych zdarzeń; parametry duration/ease/labels.',
'Istniejący GSAP/browser, HTML/SVG/Canvas zależnie od sceny. CPU/GPU/RAM Unknown. Local package offline; CDN byłby siecią. Brak konieczności instalowania nowego skilla.',
'Istniejący HyperFrames capture/export; GSAP samo nie koduje MP4/PNG/WebM/EXR. Alfa zależna od capture.',
'Dokumentacja i skills bez konta/key; runtime licencja odrębna. Szacunek DERIVED 0.25–0.5 dnia.',
'Skills MIT w przeczytanym pliku. Runtime GSAP ma odrębne warunki opisane w KB09; aktualna prawna kwalifikacja konkretnej integracji Unknown. Nie redystrybuować źródłowych assetów na tej podstawie.',
'Skills HEAD aed9cfd 2026-04-21 pokrywa katalog; docs read 2026-11-11. Brak nowego repo do wpisania.',
'DOCUMENTED; CODE_INSPECTED skill, nie runtime; NOT_RUN timeline/render.',
'Studio hyperframes-workflow; istniejący Toolbox gsap-skills.',
'KNOWLEDGE_ONLY',
'P1: krótki addendum do istniejącego ownera i 1 test. REJECT jako nowy Toolbox entry lub nowy skill.',
'NOT_RUN: tl.call zmienia tekst w 0.5 s; porównanie sequential vs seek(1,true) po świeżym init. Naprawiony pure visual state daje tę samą klatkę po 1→0→1 s. Nie rozwiązywać przez bezwarunkowe replay skutków ubocznych.',
['KB01','KB04','KB08','KB09','KS28','KS29'])

candidate('K09','Remotion flickering cookbook — kontrola negatywna nowości','https://www.remotion.dev/docs/flickering','Remotion','Live docs 2026-11-11; runtime pin Unknown','ALREADY_COVERED',
'Zależność od poprzedniej klatki lub wall-clock powoduje różnice między preview a równoległym renderem.',
'useCurrentFrame, seeded data, loading gate i seek-order są już KB01/KB03/KB04. Nie nowy zasób do wdrożenia; przydatne oficjalne uzasadnienie, że concurrency=1 nie zapewnia synchronizacji.',
'Official docs Flickering: multithreading i asset loading.',
'IN frame/props/assets → image; istniejące komponenty/render API, bez nowego formatu.',
'Obecny Remotion/React/Chromium; dokładne OS, CPU/GPU, RAM i wersje Unknown w tym researchu. Brak nowej instalacji; lokalne assets pozwalają offline.',
'Istniejący native Remotion export. Format/alpha w KB03 i docelowym kontrakcie; nie badano wykonawczo.',
'Czytanie docs bez konta. Runtime komercyjne warunki/cena dla użytkownika Unknown; korzystać z istniejącej autoryzowanej ścieżki.',
'Licencja Remotion nie została tu ponownie oceniona; Unknown dla redystrybucji. Assety/fonty/filmy osobne prawa. Nie kopiujemy repo ani docs.',
'Dokumentacja odczytana 2026-11-11; nie wykonano wersyjnego diff repo. Ryzyko concurrency opisane przez autora.',
'DOCUMENTED; NOT_RUN produkt/render; brak OWN_TEST.',
'Studio remotion-video-production.',
'KNOWLEDGE_ONLY',
'Nie tworzyć nowego skilla ani wpisu. Użyć jako linku źródłowego w QA K03; ranking nowości poza top.',
'NOT_RUN: identyczne selected frames w świeżych browser contexts i shuffled order. concurrency=1 nie uznawać za dowód naprawy; full normal-speed watch finalnego pliku.',
['KB01','KB03','KB04','KS30'])

# Source checks performed during recovery; these are reads, not execution results.
for s in S:
    if s['id'] in {'KS01','KS02','KS03','KS05','KS06','KS08','KS09','KS20','KS21','KS22','KS24','KS26','KS31','KS32'}:
        s['rechecked'] = DATE
        s['recheck_scope'] = 'Primary source read via GitHub connector for GitHub URLs, web for standards/docs; no execution.'
for c in C:
    c['deep_dive'] = c['id'] in {'K01','K03','K06','K07'}
    c['deep_dive_file'] = 'DEEP_DIVES.md' if c['deep_dive'] else None

def write(name,content):
    path=ROOT/name
    if path.exists():
        stamp=datetime.now().strftime('%Y-%m-%d-%H%M%S-%f')
        path.with_name(path.name+'.bak-'+stamp).write_bytes(path.read_bytes())
    path.write_text(content,encoding='utf-8')
write('sources.json',json.dumps(S,ensure_ascii=False,indent=2)+'\n')
write('candidates.json',json.dumps(C,ensure_ascii=False,indent=2)+'\n')

labels={'owner':'Owner','pin':'Pin / tag','reviewed':'Data przeglądu','class':'Klasa','novelty':'Nowość','problem':'Problem','baseline_delta':'Delta wobec baseline','module':'Dokładny moduł','io':'Wejścia / wyjścia / edytowalność / alfa','runtime':'Runtime / host / zasoby','export':'Eksport','cost':'Koszt / konto / sieć','rights':'Prawa','maintenance':'Utrzymanie / ograniczenia','evidence':'Poziom dowodu','target_owner':'Właściciel docelowy','integration':'Forma','recommendation':'Rekomendacja','test':'Test akceptacyjny','deep_dive':'Deep dive w DEEP_DIVES.md'}
source_map={s['id']:s for s in S}
out=['# DR-03 B — pełne karty wiedzy agentowej',f'Data: {DATE}. Wszystkie próby wykonawcze: **NOT_RUN**. DERIVED oznacza własny projekt adaptacji, nie istniejącą integrację. Repo FrameMotion i jego aktualne API: **Unknown**. 9 kandydatów; K09 celowo ALREADY_COVERED. Class B nie jest biblioteką assetów; resolution/duration/FPS/loop/layers/asset-origin są N/A dla dokumentacji, a dla planowanych fixtures opisane w testach. Źródła: GitHub connector oraz dokumentacja primary; nie wykonano pobranego kodu.','']
for c in C:
    out.extend([f"## {c['id']} — {c['name']}",f"Kanoniczny URL: [{c['name']}]({c['url']})",''])
    for key,label in labels.items(): out.append(f"- **{label}:** {c[key]}")
    out.append('\nŹródła: '+', '.join(f"[{sid}]({source_map[sid]['url']})" for sid in c['source_ids'])+'.\n')
write('CARDS.md','\n'.join(out)+'\n')
print(json.dumps({'candidates':len(C),'sources':len(S),'files':['candidates.json','sources.json','CARDS.md']},ensure_ascii=False))
