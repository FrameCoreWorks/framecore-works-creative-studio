#!/usr/bin/env python3
"""Write analysis; no candidate imports or runtime tests."""
import json,datetime,shutil
from pathlib import Path
P=Path(__file__).resolve().parent
S={s['id']:s for s in json.loads((P/'sources.json').read_text())}
def r(*ids):return ' '.join(f'[{i}]({S[i]["url"]})' for i in ids)
text='''# DR-03 A — pięć analiz do adaptacji

Data 2026-11-11. Skille: Creative Studio research-evidence; Superpowers verification-before-completion. To read-only research; **NOT_RUN** oznacza wszystkie próby importu, font loading, seek, renderu, encodera, alfy i memory stress. **CODE_INSPECTED** oznacza tylko odczyt określonych funkcji. R01 test fixture: **CODE_INSPECTED** oznacza odczyt kodu testowego autora; wynik wykonania autora **Unknown**, własne wykonanie **NOT_RUN**. Nie przyznano etykiety AUTHOR_TEST na podstawie samego kodu. Issue to **DOCUMENTED / issue report**, nawet jeśli zawiera repro. Własne kontrakty, pseudokod, progi i szacunki są **DERIVED**.

Nowość oceniono względem BASELINE.md: master frame clock, GSAP, Three/Pixi, temporal QA i mediabunny już istnieją. Wartość poniżej to wąskie moduły i nowe warunki użycia. FrameMotion ma nieznany URL/API; wszystkie przypisania mu implementacji są propozycją. Żaden moduł nie uzyskał jeszcze admission do Toolbox.

Wspólny kontrakt **DERIVED**: `prepare(inputManifest)` → `setFrame(frame,fps)` → `settled(frame)` → istniejący capture → decode/QA. Manifest obejmuje pin pakietu i host runtime, lock, rozmiar, DPR, FPS, seed, font/asset hashes i color policy. `setFrame` ustawia stan; nie przesuwa niezależnego tickera. Brak gotowości kończy frame błędem, nie pustym obrazem. W żadnym pilocie nie jest dozwolone globalne podmienianie `Math.random`, cicha zamiana fontu ani automatyczne doinstalowanie silnika. To projekt reguły, nie gotowa implementacja.

'''
text+='''## R01 — flubber: bezpieczny morph prostego konturu

**Źródło → zasada.** `interpolate` normalizuje i dopasowuje pierścienie, zwraca funkcję postępu. SVG curved paths przechodzą przez pomiar i próbkowanie, w browser przez native SVG, poza browser przez starsze svg-path-properties. W ścieżce aproksymacji zostaje pierwszy subpath. API jest heurystyczne, nie gwarantuje zachowania topologii otworów. **CODE_INSPECTED**: interpolate.js, normalize.js, svg.js; README opisuje ograniczenie holes/multiple shapes. '''+r('R01_README','R01_SRC01','R01_SRC02','R01_SRC03')+'''

**Warunek użycia.** Jeden prosty, zamknięty kontur o kontrolowanym zakresie współrzędnych, bez logo z counterami/otworami. `maxSegmentLength` jest tolerancją geometryczną w lokalnych jednostkach, nie automatycznym poziomem jakości końcowego 4K. Baseline MorphSVG pozostaje właściwy tam, gdzie został już zaakceptowany. Przewaga R01 to mały geometry-only interpolator do danych i Canvas, a nie ogólny morph. **DERIVED**: przed wywołaniem policzyć subpath i odrzucić ambiguous topology; samo `normalizeRing` nie jest pełnym walidatorem semantyki logo.

**Dane.** `{fromPath,toPath,coordinateSpace,maxSegmentLength,frameCount,easingId,fillRule,outputSize,pin}` oraz hash wejściowej geometrii. Użytkownik dostarcza dozwolone kształty; fonty, brand logos i materiały demo nie są częścią MIT prawa do biblioteki. Kopia kodu we wtyczce wymaga notice; film z własnej geometrii nie jest tą samą czynnością co redystrybucja source. '''+r('R01_LICENSE')+'''

**Operacja agenta.** **DERIVED**: podczas prepare utworzyć interpolator raz, policzyć znormalizowane bounds i ostrzec o nieobsługiwanych konturach. W frame f obliczyć `p=clamp(f/(N-1),0,1)`, zastosować zadane easing i wywołać interpolator(p). Nie inicjować D3 transition/requestAnimationFrame. Cache key musi zawierać typ pomiaru browser/Node; nie mieszać obu oracle w tym samym renderze. Przy reflow 16:9→9:16 stosować jawny transform geometrii i ponowny QA. To proponowana operacja, nie sprawdzony adapter.

**Przykład.** Własna kropla zmienia się w sześciokąt w 60 klatkach; obok metryka, której ruch bazuje na tym samym master frame. Nie testować donut jako zwykły PASS: oczekiwany jest jawny UNSUPPORTED przed interpolacją. Dla wordmarku z „B”/„ą” nie używać flubber pojedynczego konturu.

**Granice i dependencies.** W pinie 0.4.2 są stare zależności, m.in. svg-path-properties ^0.2.1 oraz toolchain Rollup/Babel/Uglify; nie podmieniać jej R02 2.2.0, bo to inne API/engine wymagania. Manifest nie ma install/postinstall/prepare, ale build/test uruchamiają kod. Issue #108 zgłasza named import error; nie odtworzono. `interpolate` blisko końców oddaje oryginalny path, co w połączeniu z aproksymacją środkowych klatek wymaga edge QA. '''+r('R01_PACKAGE','R01_ISSUE108','R01_SRC01')+'''

**Pinning / failure / retry / fallback.** **DERIVED**: source commit plus verified package integrity i lock graph; limit liczby punktów oraz czasu prepare dobrać z pomiaru. Parse/topology error bez retry; błąd importu zatrzymuje pilot. Przyszły jawny fallback do baseline MorphSVG wymaga osobnego wzorca obrazu, nie zmieniać w połowie eksportu. Szacunek 1–2 dni adaptera, bez modernizacji upstream.

**QA — NOT_RUN.** Fixture 60 klatek, curved path i polygon; ord `[0,59,1,30,59,0]`, druga instancja, native vs Node porównane jako różne środowiska. Oczekiwane: hash punktów dla tego samego frame zgodny w danym runtime; brak NaN i niezamierzonych bounds, donut odrzucony; całe klatki obejrzane z naciskiem na przejście oryginalny path↔aproksymacja. Selekcja maxSegmentLength 10/2 porównana przy 1080p/4K; brak wymyślonej tolerancji PASS przed wzorcem. Test autora zawiera punkty t=0/0.5/1, ale nie uruchomiono go. '''+r('R01_SRC04')+'''

**Wniosek do właściciela.** P1 ADAPTER pod FrameMotion po ustaleniu API; Studio dopisuje regułę „single closed contour only” do istniejącego workflow, nie tworzy nowego skilla.

'''
text+='''## R03 — Troika: tekst gotowy przed rozpoczęciem renderu

**Źródło → zasada.** Text.js wywołuje async typesetting wyłącznie, gdy `_needsSync`; callback jest wewnątrz tej gałęzi. TextBuilder przygotowuje atlas i dane glifów w workerze/na main thread, a FontResolver używa XHR i fallback resolvera. **CODE_INSPECTED** dowodzi asynchroniczności i braku callback przy unchanged props; nie potwierdza jakości polskich znaków. '''+r('R03_SRC03','R03_SRC04','R03_SRC05')+'''

**Warunek użycia.** SDF mesh w już istniejącej scenie Three, gdy potrzebne są perspektywa, lighting lub curving. Zwykłe napisy i 2D reveals pozostają w baseline. Potrzebny jest jawny local font i pełny glyph coverage dla zatwierdzonej copy. Nie obiecywać offline przy dowolnym tekście użytkownika: #394 opisuje fallback na CDN również po błędzie self-hosted data URL; dotyczy to zgłoszonych wersji, nie własnego testu. '''+r('R03_SRC02','R03_ISSUE394')+'''

**Dane.** **DERIVED** manifest: exact copy bez normalizacji, grapheme map z istniejącego kontraktu, font path/hash/licence/coverage, size/maxWidth/anchors/lineHeight/clipRect, SDF size, Three/Troika/browser pins, local resource origin oraz cache key obejmujący wszystkie layout props. Glyphy i grafemy nie muszą mieć relacji 1:1 przez ligatury. Różne ratio mogą wymagać innego maxWidth, więc są oddzielnymi layout cache entries.

**Operacja agenta.** **DERIVED**: walidacja praw/coverage → preload pełnych sekwencji copy → utworzenie Text i ustawienie layout props → jedna oczekiwana operacja sync dla zmienionej konfiguracji → walidacja textRenderInfo/bounds → zapis stanu ready. Frame zmienia tylko transform/material parametry, gdy układ pozostaje taki sam. Nie budować w każdym frame `await new Promise(resolve=>text.sync(resolve))`, bo unchanged text może nie wywołać callback. Wrapper śledzi własną rewizję i pending promise; nie opiera kontraktu na prywatnym `_needsSync`. Nowa rewizja musi zakończyć się przed capture. Dispose po scenie jest częścią lifecycle. '''+r('R03_SRC03','R03_SRC02')+'''

**Przykład.** „Zażółć gęślą jaźń” na delikatnie zakrzywionym panelu produktu; kamera i panel sterowane z frame. Przed frame 0 atlas i layout już ready; tekst nie „wpada” klatkę później. Druga scena z tym samym layout korzysta z cache, ale żadna różnica font hash/maxWidth nie może reuse starego wyniku.

**Granice, timeout i fallback.** FontResolver error path loguje błąd bez callback, a #398 opisuje wiszące teksty; **DOCUMENTED report**, nie reproduced. **DERIVED**: lokalny preload/preflight, deadline, kontrola braku zewnętrznych requestów i zakończenie joba błędem FONT_NOT_READY, ewentualnie jedna ponowna inicjalizacja workera po potwierdzonym chwilowym błędzie. Brak niejawnego fallbacku do system font; zatwierdzony alternatywny font wymaga nowego layout i QA. Polskie glyphs, ligatury i compositing SDF są Unknown do próby. '''+r('R03_ISSUE398','R03_SRC05')+'''

**Manifest / koszt / prawa.** Subpackage 0.53.1 zależy od bidi-js, troika-three-utils, troika-worker-utils i webgl-sdf-generator, peer Three >=0.125.0; root ma postinstall lerna bootstrap, sam subpackage nie ma install hook. Nie wdrażać całego Troika framework. Kod MIT i wszystkie fonty mają rozdzielne prawa. Bundling fallback fontów nie wynika z MIT wrappera. Szacunek 2–4 dni, koszt atlasu/workerów wymaga pomiaru. '''+r('R03_SRC01','R03_PACKAGE','R03_LICENSE')+'''

**Połączenie z postprocessing.** Dokumentacja autora wymaga special material override workaround przy tej bibliotece; propozycja integracji musi objąć tę kombinację w osobnej fixture. To wskazówka autora, nie dowód, że domyślny composer zachowa maskę tekstu. '''+r('RW_TROIKA')+'''

**QA — NOT_RUN.** Cold/warm font i shader load; exact font; NFC/NFD, Ł, ą, ź, fi i brakujący znak. Negative fixtures: URL 404, font bez ogonka, odcięta sieć, repeated sync przy unchanged text. Oczekiwanie: bounded error albo jawne ready, nigdy niewidoczny tekst jako PASS. Capture `[0,47,1,47,0]` po settled, bounds i obraz zgodne w tym samym env, 16:9/9:16 bez clipping. Obejrzeć cały reveal i hold normal speed/klatka po klatce, na białym/czarnym tle; monitorować czas ready, atlas/RSS i dispose. Pin artefaktu npm + wszystkich transitive/Three/browser/fontów przed wykonaniem.

**Wniosek do właściciela.** P0 kwalifikacyjny ADAPTER, nie produkcyjna rekomendacja bez testu offline/font-failure. Studio rozszerza obecny font readiness contract; FrameMotion dostaje niewielki renderer text mesh po uzgodnieniu API.

'''
text+='''## R04 — postprocessing: whitelist efektów oraz jawny czas i kolor

**Źródło → zasada.** Composer bez argumentu render używa timera. Z argumentem przekazuje delta dalej; EffectPass uruchamia effect.update i zwiększa material.time o delta*timeScale. GlitchEffect ma stan czasu i Math.random. **CODE_INSPECTED**: podanie t sekund do render(t) nie jest absolute seek, a powtórzona ta sama klatka może zmienić stan. Nie wynika z tego niemożność adaptacji każdego efektu. '''+r('R04_SRC01','R04_SRC02','R04_SRC03')+'''

**Warunek użycia.** Istniejąca scena Three i konkretny brak wyglądu: bloom, outline lub grade. Pilot ograniczony do efektów, których update/shadery/state zostały indywidualnie sprawdzone; w tym badaniu nie zatwierdzono całej biblioteki. Generic glitch/pixel catalog dubluje PixelFX, a transitions dublują gl-transitions w baseline.

**Dane.** **DERIVED** effect manifest: exact effect names/pins, uniform schedule z frame, historia wymagane/nie, color input/output, tone map position, frameBufferType, HDR range, resolution/DPR, clear alpha, camera/depth setup, asset/font hashes. Nie wystarczy tablica efektów bez kontraktu kolejności i blendingu. Wymiary 16:9 i 9:16 mają niezależne targety i wymagają resize check.

**Operacja agenta.** **DERIVED** dla stateless whitelist: scena stateAtFrame(f) → ustawienie wszystkich uniformów absolutnie → jawne zero delta, przy czym samo zero delta nie resetuje już zakumulowanego czasu; adapter musi jawnie kontrolować material.time i sprawdzić dostępne API na pinie. Każdy stanowy efekt musi mieć udowodniony reset/replay lub bake/cache; nie dopisywać „seek supported” na podstawie dostępu do jednego time uniform. Nie patchować losowości globalnie. Jeśli nie ma wiarygodnego API czasu, usunąć efekt z whitelisty. Równoległy render klatek ma używać izolowanego przygotowanego stanu.

**Przykład.** Product shot istniejącego modelu z delikatnym bloom na emissive panel i stabilnym outline. Pozycja kamery bierze się z master frame. GlitchEffect nie znajduje się w tym pilocie. Konfiguracja tonalna musi dać zgodne gradienty przy preview i export, z unikalnym miejscem tone mapping.

**Kolor i alfa.** README opisuje domyślne U8 sRGB render targets, ryzyko banding i preferencję HalfFloatType dla HDR-like desktop; tonemapping ma być na końcu. To **DOCUMENTED**, nie wynik pomiaru obecnego hosta. HalfFloat nie oznacza automatycznie EXR export. RGB z przezroczystą krawędzią musi przejść compositing test; nie obiecywać alpha na podstawie obecności transparent material. '''+r('R04_README')+'''

**Manifest / pin / failure.** 6.39.6 wymaga peer Three >=0.168 <0.188; devEngines Node>=24 i pnpm12 dotyczą development repo. Brak install hook w odczytanym package; test script uruchamia lint/build/doc i nie był wykonywany. Lock i binary/browser/GPU fingerprint są warunkiem przyszłego porównania. **DERIVED**: limit wielkości render targets ustalić po pomiarze VRAM, release/dispose między shotami; context loss → jedno jawne odtworzenie całego shotu z manifestu, kolejne → FAIL. Nie redukować jakości po cichu. Zlib notice i oznaczenie zmian dotyczą source redistribution; modele/LUT/HDRI/przykłady assets pozostają oddzielnie licencjonowane. Szacunek 2–4 dni dla 1–2 efektów. '''+r('R04_PACKAGE','R04_LICENSE')+'''

**QA — NOT_RUN.** 3 s ruchu z siatką, ciemnym gradientem, HDR emissive i półprzezroczystą krawędzią. Same frame dwukrotnie; shuffled seek; dwa procesy na identycznym GPU/browser. Expected obraz zaakceptowany dopiero po obejrzeniu; 0-diff nie zastępuje poprawnego koloru. Ogląd pełnego encode i lokalnych klatek glow, clipping, flicker, shimmer, czytelność tekstu; black/white alpha composites. Negative fixture render(absoluteT) ma zostać rozpoznana jako błędna implementacja. Z osobnym R03 sprawdzić text mask i documented material workaround. 1080p→4K oraz oba ratio; pamięć/czas frames logowane, progi wydajności ustalane po pomiarze.

**Wniosek do właściciela.** P1 ADAPTER z whitelistą; nie Toolbox entry całego repo i nie nowy skill. Stanowy glitch pozostaje P2 do badań bake/cache.

'''
text+='''## R06 — simplex-noise: losowość utworzona raz, czas jako współrzędna

**Źródło → zasada.** createNoise2D/3D/4D przyjmuje RandomFn; domyślnie to Math.random. Permutation table jest tworzona podczas inicjalizacji. Funkcje próbkują pole z podanych współrzędnych. **CODE_INSPECTED** i README uzasadniają zasadę: przypiąć seed/PRNG przy prepare, a frame mapować na współrzędne bez kumulacji. Biblioteka sama nie zna klatek ani filmu. '''+r('R06_SRC01','R06_README')+'''

**Warunek użycia.** Proceduralne pole, displacement geometrii, organiczny drift lub proceduralne tło, gdy nie jest potrzebna fizyczna symulacja. Nie zastępuje particle dynamics ani modelu audio. Earshot może dostarczyć istniejące onset/beat dane; mapowanie ich na amplitudę jest osobnym kontraktem, nie funkcją tej biblioteki.

**Dane.** **DERIVED** `{noiseVersion,prngName,prngVersion,seed,dimensions,scale,amplitude,loopFrames,radius,coordinateOrigin,outputSize,frameRate}`. Niezależne noise channels mają odrębne, stabilnie nazwane seed streams; ich kolejność tworzenia nie powinna zmieniać efektu. README zastrzega różnicę między współdzieloną instancją PRNG a fresh PRNG oraz zmianę output między 3.x/4.x. Pin output format i seed alone nie wystarczą do identyczności po upgrade. '''+r('R06_README')+'''

**Operacja agenta.** **DERIVED**: createNoise4D raz z zatwierdzonym PRNG. Dla każdego piksela/próbki i całkowitego frame f najpierw normalizuj `k=((f%N)+N)%N`, potem licz `theta=2π*k/N` oraz pole `noise4D(x*s,y*s,r*cos(theta),r*sin(theta))`. To własna konstrukcja loop w przestrzeni 4D, nie gotowa funkcja biblioteki. Matematyczne domknięcie f=N do f=0 testować z tolerancją liczbową; nie zakładać bitowej równości cos/sin przy 2π. Ta normalizacja następuje przed kątem: f=N oraz f=0 dają dokładnie k=0; dla ujemnych klatek podwójne modulo daje właściwy zakres. Bez normalizacji równość jest matematyczna, a nie bitowa. Eksportuje się 0..N-1, nie dokłada duplikatu końca. Szczegóły pixel raster i gradientu należą do istniejącego renderer.

**Przykład.** Subtelne tło do typograficznej planszy: 2 s pętli, amplituda pól ograniczona, tekst pozostaje stabilny i czytelny. Dodatkowy channel kontroluje kierunek dekoracyjnych linii. Preview i export korzystają z tej samej mapy współrzędnych i PRNG; format portrait nie rozciąga przypadkiem frequency przez ukrytą zmianę unit scale.

**Granice.** Ciągłe pole nie gwarantuje braku temporal aliasing po próbkowaniu. Zbyt duża częstotliwość przestrzenna/czasowa może migotać; banding zależy od koloru/raster/output. Przepis loop nie oznacza, że speed derivative dla dowolnej późniejszej funkcji będzie bez szwu. CPU raster milionów próbek trzeba zmierzyć; benchmark autora nie jest wynikiem tego hosta. Alfa nie istnieje w scalar noise — compositing musi być świadomie zdefiniowany w rendererze.

**Manifest / prawa / failure.** Pakiet 4.0.3 ma zero runtime dependencies; Alea w README jest przykładem, trzeba osobno zatwierdzić pin/licencję PRNG. prepare uruchamia build.sh z dwoma tsc i zapisaniem package marker; nie wykonywano tego. MIT code, fonty/model/assets nie są dołączone do proponowanego helpera. Source bundle zachowuje notice. **DERIVED**: nonfinite input/seed mismatch → fail fast bez retry; cache invalidation obejmuje wersje i parametry; jawny statyczny background fallback tylko po zaakceptowaniu zmiany briefu. Szacunek 0.5–1 dzień. '''+r('R06_PACKAGE','R06_SRC02','R06_LICENSE')+'''

**QA — NOT_RUN.** 60 klatek, kilka stałych punktów oraz whole-field raster; porządek [0,59,1,30,59,0]; dwa procesy/ten sam seed wymagają tej samej tablicy w identycznym runtime. Zmiana seedu ma zmienić przynajmniej kontrolną próbkę (nie testować „ładności”). Boundary f=60 modulo60 =0. Obejrzeć pełną pętlę trzy razy, a szew również klatka po klatce; test high frequency jako negative-control temporal aliasing. 16:9/9:16 z deklaracją jednostek; alpha background osobny. Hash geometrii/scalar oraz pixel diff zapisywane osobno, by odróżnić noise drift od zmian GPU.

**Wniosek do właściciela.** P0 OPTIONAL_DEPENDENCY: mały helper danych; istniejący Studio workflow przyjmuje seeded frame contract. Nie nowy generative engine.

'''
text+='''## R09 — resvg-js: każda klatka jako samowystarczalny dokument SVG

**Źródło → zasada.** `Resvg(svg,options).render().asPng()` rasteruje dokument; opcje obejmują local fontFiles/loadSystemFonts, skalowanie/crop/background. API nie ma zegara animacji. imagesToResolve/resolveImage oddziela referencje obrazów od przekazania ich danych. **CODE_INSPECTED** lib.rs/options.rs/fonts.rs i typy API. **DERIVED**: motion generuje serializowany statyczny SVG dla każdego frame, renderer wykonuje tylko ten snapshot. '''+r('R09_SRC01','R09_SRC02','R09_SRC03','R09_SRC06')+'''

**Warunek użycia.** Samowystarczalna scena SVG, bez wymogu browser DOM/layout, JS interakcji lub odtwarzania CSS/SMIL. Nie każda browser SVG feature jest dowiedziona jako zgodna z resvg. Jeśli efekt zależy od konkretnego filtra, maski lub tekstu, feature fixture jest bramką przed wyborem tego backendu. To nowa opcjonalna ścieżka rasteryzacji, nie migracja całego motion toolkitu.

**Dane.** **DERIVED** `{svgAtFrame,viewBox,width,height,fps,fontManifest,imageManifest,background,fitTo,crop,sourcePin,npmIntegrity,nativePlatform,rendererVersion}`. Fonty o jawnej licencji i hash; `loadSystemFonts=false` zapobiega niekontrolowanemu wyborowi fontu systemowego, lecz samo ustawienie nie dowodzi glyph coverage. Obrazy jako zatwierdzone lokalne bytes. Nie pozwalać, aby generator SVG dowolnie pobierał href z sieci.

**Operacja agenta.** **DERIVED**: build/validate SVG snapshot → jawne zasilenie obrazów i fontów → Resvg render → PNG decode dimensions/alpha → atomowy zapis klatki o numerze/PTS → manifest sequence. Równoległość ograniczana liczbą workerów i zmierzonym memory budget. Żaden real-time clock. Wynik PNG z alfa jest masterem; MP4 zwykle wymaga wskazanego tła, a WebM-alpha wymaga osobnej konfiguracji i decode dowodu. EXR nie jest udokumentowanym output wrappera.

**Przykład.** Infografika z własnym wykresem, polskim nagłówkiem, gradientem i maską; SVG data pochodzi z master frame, 180 klatek. To samo wejście ma odpowiadać tej samej klatce także przy out-of-order request. Portrait ma oddzielny layout/viewBox, nie przypadkowy crop.

**Instalacja i supply chain.** Manifest w tym commicie to 2.7.0-alpha.2, nie rekomendacja newest stable. README deklaruje prebuilt .node i no postinstall. Odczytany loader require wybiera platformowy package/lokalny binary, zawiera override NAPI_RS_NATIVE_LIBRARY_PATH i Linux libc fallback z `ldd --version`. Cargo.toml ma patched resvg git rev i woff2 branch; jest to ryzyko powtarzalności source build. Nie dowodzi pobierania brancha przez runtime prebuilt. Lock Cargo, wydane tarballe i zawartość binariów nie zostały audytowane. **DERIVED** przed pilotem: wybrać konkretny release, sprawdzić integrity i źródło platform artefact, nie instalować z branch HEAD. '''+r('R09_PACKAGE','R09_README','R09_SRC05','R09_SRC04')+'''

**Memory, crash, retry.** #421 raportuje wzrost RSS w pętli render na Windows/Node dla 2.6.2/alpha.2; #423 raportuje native abort. W odczytanym kodzie jest external memory accounting i catch unwind, co nie wystarcza do deklaracji naprawy. **DERIVED**: izolowany worker procesu, timeout i limit RSS z przyszłego pomiaru; retry jeden raz w świeżym workerze tylko dla transient job failure, nie przy powtarzalnym crash SVG. Po powtórce zatrzymać shot; nie stosować bez końca restartów ani przełączać browser backend bez nowego QA. '''+r('R09_ISSUE421','R09_ISSUE423','R09_SRC01')+'''

**Prawa.** MPL-2.0 §3 dotyczy dystrybucji covered source/executable; source dostępność i notices muszą towarzyszyć odpowiedniej dystrybucji. Film z własnego SVG nie jest redystrybucją renderer source; prawo do użytego fontu/obrazka nadal rozpatruje się oddzielnie. Repo example font nie został zakwalifikowany jako gotowy asset. Binarny bundling we wtyczce wymaga więcej niż samego linku do repo. '''+r('R09_LICENSE','RW_MPL')+'''

**QA — NOT_RUN.** Funkcjonalna fixture: polski tekst, local exact font, blur/mask/gradient, 50% opacity krawędź i obraz. Negative: missing font, unresolved image, oversized/invalid SVG. Oczekiwane: bounded explicit error/asset policy; nie przyjmować substytucji fontu jako PASS. Decode PNG: rozmiar, nonzero alpha range tam, gdzie fixture tego wymaga, black/white composite bez halo. `pixels` raw alpha representation sprawdzić na premultiplication fixture; nie zakładać identyczności z decoded PNG. Porównać 180 klatek i dłuższy stress 4K; RSS trend, timeout, exit status. Sekwencja shuffle i drugi proces; osobny browser-resvg perceptual diff, ponieważ zgodność rendererów nie jest domyślną gwarancją. Ogląd całego filmu w 16:9/9:16 oraz krawędzi tekstu/maski w wybranych frame.

**Wniosek do właściciela.** P0 kwalifikacja ADAPTER z produkcyjnym HOLD do wykonania testów; 2–3 dni plus nierozstrzygnięta naprawa native issue. FrameMotion może konsumować PNG; Studio zarządza manifestem i QA; Toolbox dopiero po dowodzie przewagi i kwalifikacji adaptera.

'''
text+='''## Kolejność eksperymentów i brakujące dowody

1. R06 i R01: małe fixtures geometry/seed/topology. Wspólny clock i random-order contract już są w baseline — dopisać tylko nowe przyczyny fail.
2. R03: font/unchanged-sync/offline negative controls, zanim będzie renderowany film 3D text.
3. R09: feature/alpha/native-memory gate; nie importować alpha HEAD do produkcji automatycznie.
4. R04: jeden stateless efekt po indywidualnej inspekcji jego shader/update, dopiero potem kompozycja z Troika.

Brak własnych wyników importu, licencji wydanych tarballi, renderer fingerprint, alpha decode, determinism benchmark i timings. Wszystkie pozostają **NOT_RUN / Unknown**. Ogólne sprawdzenie JSON/Markdown nie zmienia tego stanu.
'''
if (P/'DEEP_DIVES.md').exists():shutil.copy2(P/'DEEP_DIVES.md',P/('DEEP_DIVES.md.backup-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S')))
(P/'DEEP_DIVES.md').write_text(text)
print({'deep_dives':5,'bytes':len(text.encode()),'product_tests':'NOT_RUN'})
