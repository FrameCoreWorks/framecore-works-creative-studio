# DR-03 A — moduły wykonawcze

2026-11-11. 12 kart, 5 deep dives. Wszystkie próby produktu **NOT_RUN**. Nowość względem odczytanych źródeł baseline, nie pełnej historii. Nie dodano dependencies, nie pobrano binariów, nie uruchomiono kodu kandydatów. Własne adaptery, zakres i koszty są **DERIVED**. Źródła kodu przypięto; HEAD nie oznacza zalecenia instalacji HEAD. Wersje podane to odczyt manifestu, nie zweryfikowany artefakt npm.

Przekrojowa kompatybilność: geometry helpers mogą zasilać HTML/SVG/Canvas i istniejący Remotion/HyperFrames adapter; Three/Pixi moduły potrzebują właściwego hosta. Żaden wpis nie jest natywnym dodatkiem Blender. Blender/FFmpeg mogą konsumować wynik PNG/video po osobnym kontrakcie; nie udowodniono EXR, WebM-alpha ani zgodności każdego filtra.

## R01 — flubber — morph pojedynczego zamkniętego konturu

**ID:** R01

**Nazwa:** flubber — morph pojedynczego zamkniętego konturu

**Kanoniczny URL:** https://github.com/veltman/flubber

**Owner upstream:** veltman / Noah Veltman

**Pin:** 0cadadf3eb15cd5b2ec7c45c70601ff88b76a6c3

**Data przeglądu:** 2026-11-11

**Klasa:** A

**Nowość:** KNOWN_NEW_CAPABILITY

**Problem:** Morph figur o różnej liczbie punktów bez ręcznego dopasowania węzłów.

**Delta baseline:** Baseline ma MorphSVG; delta to mały, niezależny interpolator pierścieni dla danych SVG/Canvas, bez wymogu GSAP. Nie uzasadnia zastąpienia istniejącego morph engine. Ocena dotyczy odczytanego baseline Studio/Toolbox/Open Assets; FrameMotion baseline Unknown.

**Moduł:** src/interpolate.js, normalize.js, svg.js; interpolate(from,to,{maxSegmentLength,string}). [R01_SRC01](https://github.com/veltman/flubber/blob/0cadadf3eb15cd5b2ec7c45c70601ff88b76a6c3/src/interpolate.js) [R01_SRC02](https://github.com/veltman/flubber/blob/0cadadf3eb15cd5b2ec7c45c70601ff88b76a6c3/src/normalize.js) [R01_SRC03](https://github.com/veltman/flubber/blob/0cadadf3eb15cd5b2ec7c45c70601ff88b76a6c3/src/svg.js)

**Wejścia / wyjścia / parametry / edytowalność / alfa:** IN path string lub ring [[x,y]]; OUT funkcja t→path/ring. T jest absolutnym postępem, edytowalne punkty i kolor przez host. Otwory i kolejne subpath są ignorowane; alfa N/A w geometrii. [R01_README](https://github.com/veltman/flubber/blob/0cadadf3eb15cd5b2ec7c45c70601ff88b76a6c3/README.md) [R01_SRC03](https://github.com/veltman/flubber/blob/0cadadf3eb15cd5b2ec7c45c70601ff88b76a6c3/src/svg.js)

**Runtime / sprzęt / offline:** JS CPU, browser/Node. Pomiar krzywych używa native SVG w browser, a svg-path-properties poza nim, co wymaga testu cross-runtime. Brak potrzeby GPU do geometrii. Dokładny OS/browser/headless, RAM, VRAM i wydajność Unknown; nic nie zostało zainstalowane. [R01_SRC03](https://github.com/veltman/flubber/blob/0cadadf3eb15cd5b2ec7c45c70601ff88b76a6c3/src/svg.js)

**Eksport:** DERIVED: deterministyczny stan → istniejący renderer/capture → sekwencja PNG → istniejący encoder MP4 albo WebM. Nie ma własnego encodera; alfa zależy od render target/capture/kodeka. EXR nieudokumentowane. Zgodność Remotion/HyperFrames/FFmpeg to plan adaptera, nie sprawdzona integracja.

**Koszt / konto / sieć / zależności / instalacja:** Kod bez opłat/konta/klucza; offline po lokalnym przypięciu deps. Manifest 0.4.2: d3-array, d3-polygon, earcut, svg-path-properties ^0.2.1, svgpath, topojson-client. Skrypty test/build, bez install/postinstall/prepare w tym manifeście; build używa starego Rollup/Babel/Uglify. Adaptacja DERIVED 1–2 dni, nie obejmuje napraw upstream. [R01_PACKAGE](https://github.com/veltman/flubber/blob/0cadadf3eb15cd5b2ec7c45c70601ff88b76a6c3/package.json)

**Prawa kodu i mediów:** MIT. Film: licencja silnika nie stanowi licencji wejściowych mediów; własna geometria może być renderowana komercyjnie, a font/asset wymaga osobnej zgody. Redystrybucja kodu: zachować właściwe notice. Assety, fonty, modele i media galerii: Unknown per plik, nie bundlować. Przykłady kodowe objęte repo notice tylko gdy brak osobnej licencji; linkowane dema nie są automatycznie objęte. [R01_LICENSE](https://github.com/veltman/flubber/blob/0cadadf3eb15cd5b2ec7c45c70601ff88b76a6c3/LICENSE)

**Aktualność / błędy / utrzymanie:** HEAD 2019-10-16; 0.4.2. Stary toolchain i import problem #108 (report, nie reproduced); endpoint string wraca w pobliżu 0/1, środek jest aproksymacją, więc trzeba sprawdzić skok i gładkość. [R01_META](https://api.github.com/repos/veltman/flubber/commits?per_page=1) [R01_ISSUE108](https://github.com/veltman/flubber/issues/108) [R01_SRC01](https://github.com/veltman/flubber/blob/0cadadf3eb15cd5b2ec7c45c70601ff88b76a6c3/src/interpolate.js)

**Dowody:** DOCUMENTED + CODE_INSPECTED wskazane pliki; deklaracje autora i issue reports nie są pomiarem. OWN_TEST brak; wykonanie NOT_RUN. Rekomendacja, czas integracji i test są DERIVED.

**Właściciel integracji:** DERIVED: FrameMotion jako właściciel wąskiego adaptera, po ustaleniu jego API; Studio koordynuje i utrzymuje regułę/QA. Toolbox tylko przyszła kwalifikacja adaptera, nie automatyczne dodanie biblioteki.

**Forma:** ADAPTER

**Rekomendacja:** P1: opcjonalny adapter prostych wypełnionych konturów. Odrzucać wielokonturowe litery/logo; użyć obecnej ścieżki MorphSVG lub ręcznej geometrii po jawnym wyborze, nie po cichu.

**Test przydatności:** NOT_RUN / DERIVED: Trójkąt→kropla 2 s/60 klatek, krzywa i ring; odczyt [0,59,1,30,59,0], hash geometrii i obrazu; 16:9/9:16, maxSegmentLength 10/2; donut jako negative fixture musi dać UNSUPPORTED, nie zgubić otworu. Ogląd co klatkę, szczególnie 0→1 i 58→59.

**Status wykonania:** NOT_RUN

**Deep dive:** True

**Karta:** agents/runtime/CARDS.md

**Źródła:** [R01_README](https://github.com/veltman/flubber/blob/0cadadf3eb15cd5b2ec7c45c70601ff88b76a6c3/README.md) [R01_PACKAGE](https://github.com/veltman/flubber/blob/0cadadf3eb15cd5b2ec7c45c70601ff88b76a6c3/package.json) [R01_LICENSE](https://github.com/veltman/flubber/blob/0cadadf3eb15cd5b2ec7c45c70601ff88b76a6c3/LICENSE) [R01_SRC01](https://github.com/veltman/flubber/blob/0cadadf3eb15cd5b2ec7c45c70601ff88b76a6c3/src/interpolate.js) [R01_SRC02](https://github.com/veltman/flubber/blob/0cadadf3eb15cd5b2ec7c45c70601ff88b76a6c3/src/normalize.js) [R01_SRC03](https://github.com/veltman/flubber/blob/0cadadf3eb15cd5b2ec7c45c70601ff88b76a6c3/src/svg.js) [R01_SRC04](https://github.com/veltman/flubber/blob/0cadadf3eb15cd5b2ec7c45c70601ff88b76a6c3/test/interpolate-test.js) [R01_META](https://api.github.com/repos/veltman/flubber/commits?per_page=1) [R01_ISSUES](https://api.github.com/repos/veltman/flubber/issues?state=open&per_page=5) [R01_ISSUE108](https://github.com/veltman/flubber/issues/108)

## R02 — svg-path-properties — pomiar ścieżki poza DOM

**ID:** R02

**Nazwa:** svg-path-properties — pomiar ścieżki poza DOM

**Kanoniczny URL:** https://github.com/rveciana/svg-path-properties

**Owner upstream:** rveciana / Roger Veciana i Rovira

**Pin:** d67531110946126465efcc1f7175a3f06a5ef67d

**Data przeglądu:** 2026-11-11

**Klasa:** A

**Nowość:** KNOWN_NEW_CAPABILITY

**Problem:** Ruch znacznika z prędkością według długości ścieżki i orientacją stycznej w Canvas/Node.

**Delta baseline:** DrawSVG i ruch po path istnieją w GSAP; delta to geometry-only pomiar w Node i dostęp do segmentów. Współzależny z R01, nie liczyć dwóch pełnych nowych możliwości. Ocena dotyczy odczytanego baseline Studio/Toolbox/Open Assets; FrameMotion baseline Unknown.

**Moduł:** src/main.ts: svgPathProperties, getTotalLength/getPointAtLength/getTangentAtLength/getParts. [R02_SRC01](https://github.com/rveciana/svg-path-properties/blob/d67531110946126465efcc1f7175a3f06a5ef67d/src/main.ts)

**Wejścia / wyjścia / parametry / edytowalność / alfa:** IN SVG d; OUT length, x/y, tangent, segment parameters. Host liczy distance=progress*length; brak własnego zegara/mediów; dane edytowalne, alfa N/A. [R02_README](https://github.com/rveciana/svg-path-properties/blob/d67531110946126465efcc1f7175a3f06a5ef67d/README.md) [R02_SRC01](https://github.com/rveciana/svg-path-properties/blob/d67531110946126465efcc1f7175a3f06a5ef67d/src/main.ts)

**Runtime / sprzęt / offline:** JS CPU browser/Node; manifest 2.2.0 wymaga Node >=22. Zero deklarowanych runtime dependencies; żaden install hook w scripts. Bez DOM/GPU dla pomiaru. Dokładny OS/browser/headless, RAM, VRAM i wydajność Unknown; nic nie zostało zainstalowane. [R02_PACKAGE](https://github.com/rveciana/svg-path-properties/blob/d67531110946126465efcc1f7175a3f06a5ef67d/package.json) [R02_README](https://github.com/rveciana/svg-path-properties/blob/d67531110946126465efcc1f7175a3f06a5ef67d/README.md)

**Eksport:** DERIVED: deterministyczny stan → istniejący renderer/capture → sekwencja PNG → istniejący encoder MP4 albo WebM. Nie ma własnego encodera; alfa zależy od render target/capture/kodeka. EXR nieudokumentowane. Zgodność Remotion/HyperFrames/FFmpeg to plan adaptera, nie sprawdzona integracja.

**Koszt / konto / sieć / zależności / instalacja:** Brak konta/klucza/usługi; lokalna biblioteka offline po instalacji. DERIVED 0.5–1 dzień adaptera + wyjaśnienie praw. [R02_PACKAGE](https://github.com/rveciana/svg-path-properties/blob/d67531110946126465efcc1f7175a3f06a5ef67d/package.json)

**Prawa kodu i mediów:** CONFLICT: package.json deklaruje ISC, LICENSE zawiera MIT. Nie rozstrzygamy przez zgadywanie; przed bundlowaniem źródeł/tarballa wyjaśnić upstream i przypiąć konkretne notice. Film z własną ścieżką i redystrybucja samego modułu to osobne użycia; media/fonty/modele/przykłady zewnętrzne Unknown. [R02_PACKAGE](https://github.com/rveciana/svg-path-properties/blob/d67531110946126465efcc1f7175a3f06a5ef67d/package.json) [R02_LICENSE](https://github.com/rveciana/svg-path-properties/blob/d67531110946126465efcc1f7175a3f06a5ef67d/LICENSE)

**Aktualność / błędy / utrzymanie:** HEAD 2026-10-15, 2.2.0. Wersja w R01 to stara ^0.2.1, więc nie podmieniać transitive dependency automatycznie. Przybliżenia krzywych i zerowe segmenty wymagają próby. [R02_META](https://api.github.com/repos/rveciana/svg-path-properties/commits?per_page=1)

**Dowody:** DOCUMENTED + CODE_INSPECTED wskazane pliki; deklaracje autora i issue reports nie są pomiarem. OWN_TEST brak; wykonanie NOT_RUN. Rekomendacja, czas integracji i test są DERIVED.

**Właściciel integracji:** DERIVED: FrameMotion jako właściciel wąskiego adaptera, po ustaleniu jego API; Studio koordynuje i utrzymuje regułę/QA. Toolbox tylko przyszła kwalifikacja adaptera, nie automatyczne dodanie biblioteki.

**Forma:** OPTIONAL_DEPENDENCY

**Rekomendacja:** P1 warunkowo; wartościowy geometry helper, admission wstrzymane przez niespójne oznaczenie praw.

**Test przydatności:** NOT_RUN / DERIVED: Sześcienny Bézier, łuk, cusp i zerowa długość; równe odstępy czasowe→równe odcinki łuku w tolerancji ustalonej na fixture; kierunek bez NaN, rewind; 16:9/9:16; overlay ścieżki i stycznych co klatkę.

**Status wykonania:** NOT_RUN

**Deep dive:** False

**Karta:** agents/runtime/CARDS.md

**Źródła:** [R02_README](https://github.com/rveciana/svg-path-properties/blob/d67531110946126465efcc1f7175a3f06a5ef67d/README.md) [R02_PACKAGE](https://github.com/rveciana/svg-path-properties/blob/d67531110946126465efcc1f7175a3f06a5ef67d/package.json) [R02_LICENSE](https://github.com/rveciana/svg-path-properties/blob/d67531110946126465efcc1f7175a3f06a5ef67d/LICENSE) [R02_SRC01](https://github.com/rveciana/svg-path-properties/blob/d67531110946126465efcc1f7175a3f06a5ef67d/src/main.ts) [R02_META](https://api.github.com/repos/rveciana/svg-path-properties/commits?per_page=1)

## R03 — troika-three-text — gotowość i SDF tekstu w Three.js

**ID:** R03

**Nazwa:** troika-three-text — gotowość i SDF tekstu w Three.js

**Kanoniczny URL:** https://github.com/protectwise/troika

**Owner upstream:** protectwise / Jason Johnston

**Pin:** 9c89d51f828f94a21e33d6f24b38128d78014d5f

**Data przeglądu:** 2026-11-11

**Klasa:** A

**Nowość:** KNOWN_NEW_CAPABILITY

**Problem:** Czytelny tekst w przestrzeni 3D, z układem i rasteryzacją znaków zarządzanymi przed capture.

**Delta baseline:** Baseline zna Three i kinetic text; delta to konkretny text mesh SDF, readiness cache i lokalny font policy, nie cały framework Troika. Ocena dotyczy odczytanego baseline Studio/Toolbox/Open Assets; FrameMotion baseline Unknown.

**Moduł:** packages/troika-three-text/src/Text.js, TextBuilder.js, FontResolver.js; Text.sync, configureTextBuilder, preloadFont. [R03_SRC03](https://github.com/protectwise/troika/blob/9c89d51f828f94a21e33d6f24b38128d78014d5f/packages/troika-three-text/src/Text.js) [R03_SRC04](https://github.com/protectwise/troika/blob/9c89d51f828f94a21e33d6f24b38128d78014d5f/packages/troika-three-text/src/TextBuilder.js) [R03_SRC05](https://github.com/protectwise/troika/blob/9c89d51f828f94a21e33d6f24b38128d78014d5f/packages/troika-three-text/src/FontResolver.js) [R03_SRC02](https://github.com/protectwise/troika/blob/9c89d51f828f94a21e33d6f24b38128d78014d5f/packages/troika-three-text/README.md)

**Wejścia / wyjścia / parametry / edytowalność / alfa:** IN zatwierdzony tekst, font URL, size/maxWidth/anchors/styleRanges/clipRect; OUT mesh i textRenderInfo. Transformacje można wyznaczać z frame; layout asynchroniczny. sync callback jest tylko w gałęzi _needsSync, więc bezwarunkowe Promise(sync) przy każdym frame może wisieć dla unchanged text. SDF nie jest font outline do dalszej edycji. [R03_SRC03](https://github.com/protectwise/troika/blob/9c89d51f828f94a21e33d6f24b38128d78014d5f/packages/troika-three-text/src/Text.js)

**Runtime / sprzęt / offline:** Browser DOM + Three >=0.125.0 peer, WebGL i web worker domyślnie; useWorker=false jest opcją, nie usuwa wymogu browser canvas. Większe sdfGlyphSize zwiększa atlas/pamięć. Headless, OS i GPU trzeba przypiąć; RAM Unknown. [R03_SRC01](https://github.com/protectwise/troika/blob/9c89d51f828f94a21e33d6f24b38128d78014d5f/packages/troika-three-text/package.json) [R03_SRC04](https://github.com/protectwise/troika/blob/9c89d51f828f94a21e33d6f24b38128d78014d5f/packages/troika-three-text/src/TextBuilder.js)

**Eksport:** DERIVED: deterministyczny stan → istniejący renderer/capture → sekwencja PNG → istniejący encoder MP4 albo WebM. Nie ma własnego encodera; alfa zależy od render target/capture/kodeka. EXR nieudokumentowane. Zgodność Remotion/HyperFrames/FFmpeg to plan adaptera, nie sprawdzona integracja.

**Koszt / konto / sieć / zależności / instalacja:** MIT kod bez konta/klucza. Offline NIE jest gwarantowane: FontResolver wysyła XHR i uruchamia unicode fallback. #394 opisuje CDN fallback mimo self-host URL; dokładna transitive polityka nie została wykonana. Subpackage: bidi-js, troika-three-utils, troika-worker-utils, webgl-sdf-generator; brak lifecycle install hook w subpackage. Root postinstall=lerna bootstrap, więc nie instalować całego monorepo. DERIVED 2–4 dni plus font QA. [R03_SRC01](https://github.com/protectwise/troika/blob/9c89d51f828f94a21e33d6f24b38128d78014d5f/packages/troika-three-text/package.json) [R03_PACKAGE](https://github.com/protectwise/troika/blob/9c89d51f828f94a21e33d6f24b38128d78014d5f/package.json) [R03_SRC05](https://github.com/protectwise/troika/blob/9c89d51f828f94a21e33d6f24b38128d78014d5f/packages/troika-three-text/src/FontResolver.js) [R03_ISSUE394](https://github.com/protectwise/troika/issues/394)

**Prawa kodu i mediów:** MIT kod; font pliki i automatyczne fallbacki mają własne prawa Unknown. Film: licencja silnika nie stanowi licencji wejściowych mediów; własna geometria może być renderowana komercyjnie, a font/asset wymaga osobnej zgody. Redystrybucja kodu: zachować właściwe notice. Assety, fonty, modele i media galerii: Unknown per plik, nie bundlować. Przykłady kodowe objęte repo notice tylko gdy brak osobnej licencji; linkowane dema nie są automatycznie objęte. [R03_LICENSE](https://github.com/protectwise/troika/blob/9c89d51f828f94a21e33d6f24b38128d78014d5f/LICENSE)

**Aktualność / błędy / utrzymanie:** HEAD 2026-11-02, subpackage 0.53.1. #398 raportuje font failure pozostawiający pending callbacks, #394 żąda wyłączenia sieci. Kod error path loguje bez zakończenia callback; raporty nie były reproduced. Dokumentacja opisuje dispose i workaround OverrideMaterialManager dla postprocessing. [R03_META](https://api.github.com/repos/protectwise/troika/commits?per_page=1) [R03_ISSUE398](https://github.com/protectwise/troika/issues/398) [R03_ISSUE394](https://github.com/protectwise/troika/issues/394) [R03_SRC05](https://github.com/protectwise/troika/blob/9c89d51f828f94a21e33d6f24b38128d78014d5f/packages/troika-three-text/src/FontResolver.js) [R03_SRC02](https://github.com/protectwise/troika/blob/9c89d51f828f94a21e33d6f24b38128d78014d5f/packages/troika-three-text/README.md)

**Dowody:** DOCUMENTED + CODE_INSPECTED wskazane pliki; deklaracje autora i issue reports nie są pomiarem. OWN_TEST brak; wykonanie NOT_RUN. Rekomendacja, czas integracji i test są DERIVED.

**Właściciel integracji:** DERIVED: FrameMotion jako właściciel wąskiego adaptera, po ustaleniu jego API; Studio koordynuje i utrzymuje regułę/QA. Toolbox tylko przyszła kwalifikacja adaptera, nie automatyczne dodanie biblioteki.

**Forma:** ADAPTER

**Rekomendacja:** P0 research spike: lokalny font manifest, preflight coverage, timeout, cache gotowego layoutu; render tylko po ready. Brak fontu/coverage → jawny FAIL, bez ukrytej zamiany fontu. Nie dopuszczać arbitrary unicode online w eksportach offline.

**Test przydatności:** NOT_RUN / DERIVED: Zażółć gęślą jaźń; NFC/NFD, łączona ligatura i brakujący glyph. Cold/warm load, unchanged text sync, błędny URL i sieć zablokowana. Wersjonowany cache key, bounds i full-frame movie 16:9/9:16, seek [0,47,1,47,0], clipping/alpha/SDF na czarnym i białym tle. Timeout nie może zapisać pustej klatki jako PASS.

**Status wykonania:** NOT_RUN

**Deep dive:** True

**Karta:** agents/runtime/CARDS.md

**Źródła:** [R03_README](https://github.com/protectwise/troika/blob/9c89d51f828f94a21e33d6f24b38128d78014d5f/README.md) [R03_PACKAGE](https://github.com/protectwise/troika/blob/9c89d51f828f94a21e33d6f24b38128d78014d5f/package.json) [R03_LICENSE](https://github.com/protectwise/troika/blob/9c89d51f828f94a21e33d6f24b38128d78014d5f/LICENSE) [R03_SRC01](https://github.com/protectwise/troika/blob/9c89d51f828f94a21e33d6f24b38128d78014d5f/packages/troika-three-text/package.json) [R03_SRC02](https://github.com/protectwise/troika/blob/9c89d51f828f94a21e33d6f24b38128d78014d5f/packages/troika-three-text/README.md) [R03_SRC03](https://github.com/protectwise/troika/blob/9c89d51f828f94a21e33d6f24b38128d78014d5f/packages/troika-three-text/src/Text.js) [R03_SRC04](https://github.com/protectwise/troika/blob/9c89d51f828f94a21e33d6f24b38128d78014d5f/packages/troika-three-text/src/TextBuilder.js) [R03_SRC05](https://github.com/protectwise/troika/blob/9c89d51f828f94a21e33d6f24b38128d78014d5f/packages/troika-three-text/src/FontResolver.js) [R03_META](https://api.github.com/repos/protectwise/troika/commits?per_page=1) [R03_ISSUES](https://api.github.com/repos/protectwise/troika/issues?state=open&per_page=5) [R03_ISSUE398](https://github.com/protectwise/troika/issues/398) [R03_ISSUE394](https://github.com/protectwise/troika/issues/394) [RW_TROIKA](https://protectwise.github.io/troika/troika-three-text/)

## R04 — postprocessing — wąski profil bloom/outline dla Three.js

**ID:** R04

**Nazwa:** postprocessing — wąski profil bloom/outline dla Three.js

**Kanoniczny URL:** https://github.com/pmndrs/postprocessing

**Owner upstream:** pmndrs / Raoul van Rüschen

**Pin:** a1f103559d15cf56cbcbb15d4373711b09418f3f

**Data przeglądu:** 2026-11-11

**Klasa:** A

**Nowość:** KNOWN_NEW_CAPABILITY

**Problem:** Spójne bloom/outline/grade istniejącej sceny Three przy kontrolowanej przestrzeni barw i czasie.

**Delta baseline:** Baseline ma Three, pixel effects i transitions; delta to celowana kompozycja obrazu 3D, nie kolejny renderer ani katalog wszystkich efektów. Ocena dotyczy odczytanego baseline Studio/Toolbox/Open Assets; FrameMotion baseline Unknown.

**Moduł:** src/core/EffectComposer.js + passes/EffectPass.js; do pilota statyczne efekty z istniejącej sceny. GlitchEffect.js jako kontrprzykład arbitrary seek. [R04_SRC01](https://github.com/pmndrs/postprocessing/blob/a1f103559d15cf56cbcbb15d4373711b09418f3f/src/core/EffectComposer.js) [R04_SRC02](https://github.com/pmndrs/postprocessing/blob/a1f103559d15cf56cbcbb15d4373711b09418f3f/src/passes/EffectPass.js) [R04_SRC03](https://github.com/pmndrs/postprocessing/blob/a1f103559d15cf56cbcbb15d4373711b09418f3f/src/effects/GlitchEffect.js)

**Wejścia / wyjścia / parametry / edytowalność / alfa:** IN Three scene/render buffers, efekty/uniformy; OUT GPU obraz. composer.render(deltaTime) to delta, nie czas absolutny; pominięcie argumentu używa timera. EffectPass akumuluje material.time += deltaTime*timeScale, a GlitchEffect losuje Math.random. Alfa i edytowalność zależą od scene/targets. [R04_SRC01](https://github.com/pmndrs/postprocessing/blob/a1f103559d15cf56cbcbb15d4373711b09418f3f/src/core/EffectComposer.js) [R04_SRC02](https://github.com/pmndrs/postprocessing/blob/a1f103559d15cf56cbcbb15d4373711b09418f3f/src/passes/EffectPass.js) [R04_SRC03](https://github.com/pmndrs/postprocessing/blob/a1f103559d15cf56cbcbb15d4373711b09418f3f/src/effects/GlitchEffect.js)

**Runtime / sprzęt / offline:** GPU WebGL/Three peer >=0.168.0 <0.188.0. README zaleca HalfFloatType dla HDR-like pipeline, właściwy outputColorSpace oraz tonemapping na końcu. Node >=24 i pnpm >=12 <13 to devEngines repo, nie dowód wymagań browser runtime. VRAM skaluje się z targetami; pomiar Unknown. Dokładny OS/browser/headless, RAM, VRAM i wydajność Unknown; nic nie zostało zainstalowane. [R04_PACKAGE](https://github.com/pmndrs/postprocessing/blob/a1f103559d15cf56cbcbb15d4373711b09418f3f/package.json) [R04_README](https://github.com/pmndrs/postprocessing/blob/a1f103559d15cf56cbcbb15d4373711b09418f3f/README.md)

**Eksport:** DERIVED: deterministyczny stan → istniejący renderer/capture → sekwencja PNG → istniejący encoder MP4 albo WebM. Nie ma własnego encodera; alfa zależy od render target/capture/kodeka. EXR nieudokumentowane. Zgodność Remotion/HyperFrames/FFmpeg to plan adaptera, nie sprawdzona integracja.

**Koszt / konto / sieć / zależności / instalacja:** Brak opłat/konta/klucza dla library. Demo ma zewnętrzne media, nie pobrano. Scripts build/test/prepublishOnly, brak install/postinstall/prepare w manifest. Peer Three; narzędzia dev obejmują Hugo i shader bundling. DERIVED 2–4 dni dla wybranych efektów; stanowy glitch poza zakresem. [R04_PACKAGE](https://github.com/pmndrs/postprocessing/blob/a1f103559d15cf56cbcbb15d4373711b09418f3f/package.json)

**Prawa kodu i mediów:** Zlib: zachować notice, oznaczyć zmiany i nie przypisywać sobie autorstwa. Film: licencja silnika nie stanowi licencji wejściowych mediów; własna geometria może być renderowana komercyjnie, a font/asset wymaga osobnej zgody. Redystrybucja kodu: zachować właściwe notice. Assety, fonty, modele i media galerii: Unknown per plik, nie bundlować. Przykłady kodowe objęte repo notice tylko gdy brak osobnej licencji; linkowane dema nie są automatycznie objęte. [R04_LICENSE](https://github.com/pmndrs/postprocessing/blob/a1f103559d15cf56cbcbb15d4373711b09418f3f/LICENSE.md)

**Aktualność / błędy / utrzymanie:** HEAD 2026-11-01, 6.39.6. Czytano composer/pass/glitch/noise; nie audytowano wszystkich efektów, shaderów ani transitive deps. Publiczne demo nie dowodzi seek/export. [R04_META](https://api.github.com/repos/pmndrs/postprocessing/commits?per_page=1) [R04_SRC01](https://github.com/pmndrs/postprocessing/blob/a1f103559d15cf56cbcbb15d4373711b09418f3f/src/core/EffectComposer.js) [R04_SRC02](https://github.com/pmndrs/postprocessing/blob/a1f103559d15cf56cbcbb15d4373711b09418f3f/src/passes/EffectPass.js) [R04_SRC03](https://github.com/pmndrs/postprocessing/blob/a1f103559d15cf56cbcbb15d4373711b09418f3f/src/effects/GlitchEffect.js) [R04_SRC04](https://github.com/pmndrs/postprocessing/blob/a1f103559d15cf56cbcbb15d4373711b09418f3f/src/effects/NoiseEffect.js)

**Dowody:** DOCUMENTED + CODE_INSPECTED wskazane pliki; deklaracje autora i issue reports nie są pomiarem. OWN_TEST brak; wykonanie NOT_RUN. Rekomendacja, czas integracji i test są DERIVED.

**Właściciel integracji:** DERIVED: FrameMotion jako właściciel wąskiego adaptera, po ustaleniu jego API; Studio koordynuje i utrzymuje regułę/QA. Toolbox tylko przyszła kwalifikacja adaptera, nie automatyczne dodanie biblioteki.

**Forma:** ADAPTER

**Rekomendacja:** P1: dopuścić wyłącznie whitelistę efektów bez historii po testach; autoritative time adapter per effect. Glitch i akumulujące historię efekty odłożyć do bake/cache.

**Test przydatności:** NOT_RUN / DERIVED: 3 s kontrastowy obiekt i SDF tekst, glow przy krawędzi, półprzezroczystość; frame order permutation, dwukrotny capture tej samej klatki, black/white composite; compare flat gradient w U8/HalfFloat i tone map raz. 16:9/9:16, 4K stress; temporal watch bloom/shimmer, GPU i pamięć logowane.

**Status wykonania:** NOT_RUN

**Deep dive:** True

**Karta:** agents/runtime/CARDS.md

**Źródła:** [R04_README](https://github.com/pmndrs/postprocessing/blob/a1f103559d15cf56cbcbb15d4373711b09418f3f/README.md) [R04_PACKAGE](https://github.com/pmndrs/postprocessing/blob/a1f103559d15cf56cbcbb15d4373711b09418f3f/package.json) [R04_LICENSE](https://github.com/pmndrs/postprocessing/blob/a1f103559d15cf56cbcbb15d4373711b09418f3f/LICENSE.md) [R04_SRC01](https://github.com/pmndrs/postprocessing/blob/a1f103559d15cf56cbcbb15d4373711b09418f3f/src/core/EffectComposer.js) [R04_SRC02](https://github.com/pmndrs/postprocessing/blob/a1f103559d15cf56cbcbb15d4373711b09418f3f/src/passes/EffectPass.js) [R04_SRC03](https://github.com/pmndrs/postprocessing/blob/a1f103559d15cf56cbcbb15d4373711b09418f3f/src/effects/GlitchEffect.js) [R04_SRC04](https://github.com/pmndrs/postprocessing/blob/a1f103559d15cf56cbcbb15d4373711b09418f3f/src/effects/NoiseEffect.js) [R04_META](https://api.github.com/repos/pmndrs/postprocessing/commits?per_page=1) [R04_ISSUES](https://api.github.com/repos/pmndrs/postprocessing/issues?state=open&per_page=5)

## R05 — pixi-filters — kontrolowany CRT i ograniczenia glitch

**ID:** R05

**Nazwa:** pixi-filters — kontrolowany CRT i ograniczenia glitch

**Kanoniczny URL:** https://github.com/pixijs/filters

**Owner upstream:** PixiJS Team

**Pin:** e9d1ca987864f121680bb0d7e9612c05b37748de

**Data przeglądu:** 2026-11-11

**Klasa:** A

**Nowość:** KNOWN_NEW_CAPABILITY

**Problem:** CRT/scanlines i wybrane stylizacje w już używanym Pixi.

**Delta baseline:** Baseline ma Pixi i PixelFX; nowa delta ogranicza się do jawnych time/seed uniformów CRT i wniosku o nieseedowanej geometrii glitch. Ogólny katalog pixel/glitch już pokryty. Ocena dotyczy odczytanego baseline Studio/Toolbox/Open Assets; FrameMotion baseline Unknown.

**Moduł:** src/crt/CRTFilter.ts; src/glitch/GlitchFilter.ts; subpath import pixi-filters/crt. [R05_SRC01](https://github.com/pixijs/filters/blob/e9d1ca987864f121680bb0d7e9612c05b37748de/src/crt/CRTFilter.ts) [R05_SRC02](https://github.com/pixijs/filters/blob/e9d1ca987864f121680bb0d7e9612c05b37748de/src/glitch/GlitchFilter.ts) [R05_PACKAGE](https://github.com/pixijs/filters/blob/e9d1ca987864f121680bb0d7e9612c05b37748de/package.json)

**Wejścia / wyjścia / parametry / edytowalność / alfa:** IN tekstura/Pixi container, parametry CRT time/seed/noise/vignette; OUT filtered texture. apply kopiuje time/seed do uniformów. Glitch seed to uSeed; bands/shuffle/offsets nadal Math.random, więc seed nie kontroluje całego obrazu. Alfa po filtrze do sprawdzenia. [R05_SRC01](https://github.com/pixijs/filters/blob/e9d1ca987864f121680bb0d7e9612c05b37748de/src/crt/CRTFilter.ts) [R05_SRC02](https://github.com/pixijs/filters/blob/e9d1ca987864f121680bb0d7e9612c05b37748de/src/glitch/GlitchFilter.ts)

**Runtime / sprzęt / offline:** Pixi >=8.0.0-0 peer; WebGL GPU, TS/JS. CRT ma ścieżki programów GL/GPU w pliku; rzeczywiste wsparcie wybranego backendu i headless Unknown. Dokładny OS/browser/headless, RAM, VRAM i wydajność Unknown; nic nie zostało zainstalowane. [R05_PACKAGE](https://github.com/pixijs/filters/blob/e9d1ca987864f121680bb0d7e9612c05b37748de/package.json) [R05_SRC01](https://github.com/pixijs/filters/blob/e9d1ca987864f121680bb0d7e9612c05b37748de/src/crt/CRTFilter.ts)

**Eksport:** DERIVED: deterministyczny stan → istniejący renderer/capture → sekwencja PNG → istniejący encoder MP4 albo WebM. Nie ma własnego encodera; alfa zależy od render target/capture/kodeka. EXR nieudokumentowane. Zgodność Remotion/HyperFrames/FFmpeg to plan adaptera, nie sprawdzona integracja.

**Koszt / konto / sieć / zależności / instalacja:** Bez konta/klucza/usługi; offline z lokalnymi teksturami. Manifest 6.1.5: @types/gradient-parser runtime declaration, Pixi peer; brak install hook w scripts; dev screenshots używa Electron. DERIVED 1–2 dni dla CRT. [R05_PACKAGE](https://github.com/pixijs/filters/blob/e9d1ca987864f121680bb0d7e9612c05b37748de/package.json)

**Prawa kodu i mediów:** MIT kod. Film: licencja silnika nie stanowi licencji wejściowych mediów; własna geometria może być renderowana komercyjnie, a font/asset wymaga osobnej zgody. Redystrybucja kodu: zachować właściwe notice. Assety, fonty, modele i media galerii: Unknown per plik, nie bundlować. Przykłady kodowe objęte repo notice tylko gdy brak osobnej licencji; linkowane dema nie są automatycznie objęte. [R05_LICENSE](https://github.com/pixijs/filters/blob/e9d1ca987864f121680bb0d7e9612c05b37748de/LICENSE)

**Aktualność / błędy / utrzymanie:** HEAD 2025-11-29, 6.1.5. Dokładny shader/backend coverage i alpha nie były odpalone. Tylko seed uniform nie stanowi dowodu determinism. [R05_META](https://api.github.com/repos/pixijs/filters/commits?per_page=1) [R05_SRC02](https://github.com/pixijs/filters/blob/e9d1ca987864f121680bb0d7e9612c05b37748de/src/glitch/GlitchFilter.ts)

**Dowody:** DOCUMENTED + CODE_INSPECTED wskazane pliki; deklaracje autora i issue reports nie są pomiarem. OWN_TEST brak; wykonanie NOT_RUN. Rekomendacja, czas integracji i test są DERIVED.

**Właściciel integracji:** DERIVED: FrameMotion jako właściciel wąskiego adaptera, po ustaleniu jego API; Studio koordynuje i utrzymuje regułę/QA. Toolbox tylko przyszła kwalifikacja adaptera, nie automatyczne dodanie biblioteki.

**Forma:** ADAPTER

**Rekomendacja:** P1 CRT-only; glitch odrzucić z pilota bez pełnego seedowania/prebake. Bez dodatkowej biblioteki dla blur/alpha obecnych w Pixi.

**Test przydatności:** NOT_RUN / DERIVED: CRT frame-derived time na siatce i cienkich liniach, 60 klatek loop; powtórzony seed i frame; glitch negative-control ma ujawnić różnice nowych instancji. 16:9/9:16, dwa tła, pełny ogląd scanline aliasing/flicker.

**Status wykonania:** NOT_RUN

**Deep dive:** False

**Karta:** agents/runtime/CARDS.md

**Źródła:** [R05_README](https://github.com/pixijs/filters/blob/e9d1ca987864f121680bb0d7e9612c05b37748de/README.md) [R05_PACKAGE](https://github.com/pixijs/filters/blob/e9d1ca987864f121680bb0d7e9612c05b37748de/package.json) [R05_LICENSE](https://github.com/pixijs/filters/blob/e9d1ca987864f121680bb0d7e9612c05b37748de/LICENSE) [R05_SRC01](https://github.com/pixijs/filters/blob/e9d1ca987864f121680bb0d7e9612c05b37748de/src/crt/CRTFilter.ts) [R05_SRC02](https://github.com/pixijs/filters/blob/e9d1ca987864f121680bb0d7e9612c05b37748de/src/glitch/GlitchFilter.ts) [R05_META](https://api.github.com/repos/pixijs/filters/commits?per_page=1)

## R06 — simplex-noise — pole proceduralne z deterministycznym seedem

**ID:** R06

**Nazwa:** simplex-noise — pole proceduralne z deterministycznym seedem

**Kanoniczny URL:** https://github.com/jwagner/simplex-noise.js

**Owner upstream:** jwagner / Jonas Wagner

**Pin:** 6bfff874f5f0efed6375a9bf27fbd39b3cec6b4e

**Data przeglądu:** 2026-11-11

**Klasa:** A

**Nowość:** NEW

**Problem:** Powtarzalne tła, organiczne trajektorie i sterowanie parametrami bez symulacji zależnej od kolejności klatek.

**Delta baseline:** Baseline ma PixelFX/generative efekty, lecz nie wskazuje geometry-only seeded 2D/3D/4D noise API. Nowa pozycja to ten mały moduł, nie nowa kategoria generative art. Ocena dotyczy odczytanego baseline Studio/Toolbox/Open Assets; FrameMotion baseline Unknown.

**Moduł:** simplex-noise.ts: createNoise2D/3D/4D(random), buildPermutationTable. [R06_SRC01](https://github.com/jwagner/simplex-noise.js/blob/6bfff874f5f0efed6375a9bf27fbd39b3cec6b4e/simplex-noise.ts)

**Wejścia / wyjścia / parametry / edytowalność / alfa:** IN współrzędne i funkcja PRNG przy inicjalizacji; OUT scalar noise, brak obrazu/alpha. Domyślnie Math.random, seed trzeba dostarczyć. Po zbudowaniu permutation table wynik zależy od współrzędnych. Parametry x/y/częstotliwość/amplituda/czas należą do hosta. [R06_README](https://github.com/jwagner/simplex-noise.js/blob/6bfff874f5f0efed6375a9bf27fbd39b3cec6b4e/README.md) [R06_SRC01](https://github.com/jwagner/simplex-noise.js/blob/6bfff874f5f0efed6375a9bf27fbd39b3cec6b4e/simplex-noise.ts)

**Runtime / sprzęt / offline:** CPU JS browser/Node, ESM/CJS; bez declared runtime dependencies. GPU potrzebny tylko dla wybranego host renderera. Stan ograniczony do tablic; exact RAM/throughput Unknown. Dokładny OS/browser/headless, RAM, VRAM i wydajność Unknown; nic nie zostało zainstalowane. [R06_PACKAGE](https://github.com/jwagner/simplex-noise.js/blob/6bfff874f5f0efed6375a9bf27fbd39b3cec6b4e/package.json)

**Eksport:** DERIVED: deterministyczny stan → istniejący renderer/capture → sekwencja PNG → istniejący encoder MP4 albo WebM. Nie ma własnego encodera; alfa zależy od render target/capture/kodeka. EXR nieudokumentowane. Zgodność Remotion/HyperFrames/FFmpeg to plan adaptera, nie sprawdzona integracja.

**Koszt / konto / sieć / zależności / instalacja:** Bez konta/klucza/sieci po przypięciu. Alea jest przykładem PRNG/devDependency, nie runtime dependency; wybrany PRNG wymaga własnego pinu/praw. prepare wywołuje build.sh: mkdir, dwa tsc builds i zapis esm package marker. Brak pobierania usług w odczytanym build.sh. DERIVED 0.5–1 dzień. [R06_PACKAGE](https://github.com/jwagner/simplex-noise.js/blob/6bfff874f5f0efed6375a9bf27fbd39b3cec6b4e/package.json) [R06_SRC02](https://github.com/jwagner/simplex-noise.js/blob/6bfff874f5f0efed6375a9bf27fbd39b3cec6b4e/build.sh) [R06_README](https://github.com/jwagner/simplex-noise.js/blob/6bfff874f5f0efed6375a9bf27fbd39b3cec6b4e/README.md)

**Prawa kodu i mediów:** MIT kod. Film: licencja silnika nie stanowi licencji wejściowych mediów; własna geometria może być renderowana komercyjnie, a font/asset wymaga osobnej zgody. Redystrybucja kodu: zachować właściwe notice. Assety, fonty, modele i media galerii: Unknown per plik, nie bundlować. Przykłady kodowe objęte repo notice tylko gdy brak osobnej licencji; linkowane dema nie są automatycznie objęte. [R06_LICENSE](https://github.com/jwagner/simplex-noise.js/blob/6bfff874f5f0efed6375a9bf27fbd39b3cec6b4e/LICENSE)

**Aktualność / błędy / utrzymanie:** HEAD 2024-07-26, 4.0.3. README ostrzega, że 4.x zmienia output względem 3.x; wspólna instancja PRNG dla kilku create calls zmienia sekwencję w porównaniu z osobnymi. Nie obiecywać starych hashów po upgrade. [R06_META](https://api.github.com/repos/jwagner/simplex-noise.js/commits?per_page=1) [R06_README](https://github.com/jwagner/simplex-noise.js/blob/6bfff874f5f0efed6375a9bf27fbd39b3cec6b4e/README.md)

**Dowody:** DOCUMENTED + CODE_INSPECTED wskazane pliki; deklaracje autora i issue reports nie są pomiarem. OWN_TEST brak; wykonanie NOT_RUN. Rekomendacja, czas integracji i test są DERIVED.

**Właściciel integracji:** DERIVED: FrameMotion jako właściciel wąskiego adaptera, po ustaleniu jego API; Studio koordynuje i utrzymuje regułę/QA. Toolbox tylko przyszła kwalifikacja adaptera, nie automatyczne dodanie biblioteki.

**Forma:** OPTIONAL_DEPENDENCY

**Rekomendacja:** P0: mały helper dla czystego noiseAt(frame,coords,seed), PRNG i parametry w manifest. Loop na okręgu w 4D to własna reguła DERIVED, nie wbudowany exporter.

**Test przydatności:** NOT_RUN / DERIVED: 2 s/60 klatek Najpierw k=((f%N)+N)%N, potem theta=2πk/N i noise4D(x*s,y*s,r*cos(theta),r*sin(theta)); f=N i f=0 mają identyczny k=0. Nie zakładać exact sin(2π)=0; eksport 0..N-1 bez duplikatu. Shuffled seek i drugi proces ten sam seed→identyczne raw field; inny seed różny. 16:9/9:16, temporal ogląd szwu, banding i high-frequency aliasing.

**Status wykonania:** NOT_RUN

**Deep dive:** True

**Karta:** agents/runtime/CARDS.md

**Źródła:** [R06_README](https://github.com/jwagner/simplex-noise.js/blob/6bfff874f5f0efed6375a9bf27fbd39b3cec6b4e/README.md) [R06_PACKAGE](https://github.com/jwagner/simplex-noise.js/blob/6bfff874f5f0efed6375a9bf27fbd39b3cec6b4e/package.json) [R06_LICENSE](https://github.com/jwagner/simplex-noise.js/blob/6bfff874f5f0efed6375a9bf27fbd39b3cec6b4e/LICENSE) [R06_SRC01](https://github.com/jwagner/simplex-noise.js/blob/6bfff874f5f0efed6375a9bf27fbd39b3cec6b4e/simplex-noise.ts) [R06_SRC02](https://github.com/jwagner/simplex-noise.js/blob/6bfff874f5f0efed6375a9bf27fbd39b3cec6b4e/build.sh) [R06_META](https://api.github.com/repos/jwagner/simplex-noise.js/commits?per_page=1) [R06_ISSUES](https://api.github.com/repos/jwagner/simplex-noise.js/issues?state=open&per_page=5)

## R07 — Zdog — referencja pseudo-3D Canvas/SVG

**ID:** R07

**Nazwa:** Zdog — referencja pseudo-3D Canvas/SVG

**Kanoniczny URL:** https://github.com/metafizzy/zdog

**Owner upstream:** metafizzy / David DeSandro

**Pin:** dde8684be686bc6d3cbedb6be49875c0a03a14c0

**Data przeglądu:** 2026-11-11

**Klasa:** A

**Nowość:** ALREADY_COVERED

**Problem:** Prosta płaska ilustracja pseudo-3D z obrotami, bez PBR.

**Delta baseline:** Baseline ma Three/Canvas i explainery, a nie wykazano konkretnej luki uzasadniającej kolejny engine. Przydatna tylko metoda renderowania geometrycznych ilustracji. Ocena dotyczy odczytanego baseline Studio/Toolbox/Open Assets; FrameMotion baseline Unknown.

**Moduł:** js/illustration.js updateRenderGraph i istniejący API Anchor/Shape. [R07_SRC01](https://github.com/metafizzy/zdog/blob/dde8684be686bc6d3cbedb6be49875c0a03a14c0/js/illustration.js)

**Wejścia / wyjścia / parametry / edytowalność / alfa:** IN drzewo figur, translate/rotate/scale; OUT Canvas2D lub SVG. Dema mają dragRotate i rotate +=, więc adapter musiałby ustawiać rotate=f(frame), wyłączyć drag i jawnie renderować. SVG pozostaje edytowalne; alfa wynikowa nie sprawdzona. [R07_README](https://github.com/metafizzy/zdog/blob/dde8684be686bc6d3cbedb6be49875c0a03a14c0/README.md) [R07_SRC01](https://github.com/metafizzy/zdog/blob/dde8684be686bc6d3cbedb6be49875c0a03a14c0/js/illustration.js)

**Runtime / sprzęt / offline:** JS CPU geometry + Canvas2D/SVG browser; headless zależne od browser. W package 1.1.3 brak runtime deps i install hooks. Dokładny OS/browser/headless, RAM, VRAM i wydajność Unknown; nic nie zostało zainstalowane. [R07_PACKAGE](https://github.com/metafizzy/zdog/blob/dde8684be686bc6d3cbedb6be49875c0a03a14c0/package.json)

**Eksport:** DERIVED: deterministyczny stan → istniejący renderer/capture → sekwencja PNG → istniejący encoder MP4 albo WebM. Nie ma własnego encodera; alfa zależy od render target/capture/kodeka. EXR nieudokumentowane. Zgodność Remotion/HyperFrames/FFmpeg to plan adaptera, nie sprawdzona integracja.

**Koszt / konto / sieć / zależności / instalacja:** Brak konta/klucza/usługi dla library; offline local bundle. DERIVED 1–2 dni, lecz brak uzasadnienia kosztu wobec baseline. [R07_PACKAGE](https://github.com/metafizzy/zdog/blob/dde8684be686bc6d3cbedb6be49875c0a03a14c0/package.json)

**Prawa kodu i mediów:** MIT deklarowane przez README i package (osobnego LICENSE w tym odczycie nie ustalono). Media CodePen/galerii, font Zfont i cudze modele osobne Unknown. Nie redystrybuować galerii na podstawie README. Własny film i source bundle rozdzielić. [R07_README](https://github.com/metafizzy/zdog/blob/dde8684be686bc6d3cbedb6be49875c0a03a14c0/README.md) [R07_PACKAGE](https://github.com/metafizzy/zdog/blob/dde8684be686bc6d3cbedb6be49875c0a03a14c0/package.json)

**Aktualność / błędy / utrzymanie:** HEAD 2022-01-22, 1.1.3; README nazywa v1 beta. Brak współczesnego wykonawczego dowodu. [R07_META](https://api.github.com/repos/metafizzy/zdog/commits?per_page=1) [R07_README](https://github.com/metafizzy/zdog/blob/dde8684be686bc6d3cbedb6be49875c0a03a14c0/README.md)

**Dowody:** DOCUMENTED + CODE_INSPECTED wskazane pliki; deklaracje autora i issue reports nie są pomiarem. OWN_TEST brak; wykonanie NOT_RUN. Rekomendacja, czas integracji i test są DERIVED.

**Właściciel integracji:** DERIVED: FrameMotion jako właściciel wąskiego adaptera, po ustaleniu jego API; Studio koordynuje i utrzymuje regułę/QA. Toolbox tylko przyszła kwalifikacja adaptera, nie automatyczne dodanie biblioteki.

**Forma:** KNOWLEDGE_ONLY

**Rekomendacja:** P2: zasada pseudo-3D przez grube linie/koła; nie dodawać pełnego engine ani Toolbox entry.

**Test przydatności:** NOT_RUN / DERIVED: Gdy pojawi się uzasadniony brief: jedna ikona cube+ring obrót z frame, SVG/Canvas porównanie, 16:9/9:16 i bez interakcji. Ogląd przecinających się figur i sortowania głębi.

**Status wykonania:** NOT_RUN

**Deep dive:** False

**Karta:** agents/runtime/CARDS.md

**Źródła:** [R07_README](https://github.com/metafizzy/zdog/blob/dde8684be686bc6d3cbedb6be49875c0a03a14c0/README.md) [R07_PACKAGE](https://github.com/metafizzy/zdog/blob/dde8684be686bc6d3cbedb6be49875c0a03a14c0/package.json) [R07_SRC01](https://github.com/metafizzy/zdog/blob/dde8684be686bc6d3cbedb6be49875c0a03a14c0/js/illustration.js) [R07_META](https://api.github.com/repos/metafizzy/zdog/commits?per_page=1) [RW_ZDOG](https://zzz.dog/api)

## R08 — three.quarks — particles, kandydat dopiero po bake

**ID:** R08

**Nazwa:** three.quarks — particles, kandydat dopiero po bake

**Kanoniczny URL:** https://github.com/Alchemist0823/three.quarks

**Owner upstream:** Alchemist0823 / Forrest Sun

**Pin:** de7c207f791c8b2260c43334a282976221688b1b

**Data przeglądu:** 2026-11-11

**Klasa:** A

**Nowość:** KNOWN_NEW_CAPABILITY

**Problem:** Batched particle/trail VFX w scenach Three.

**Delta baseline:** Baseline zna Three i procedural effects; delta to wyspecjalizowany emitter/behaviour system. Nie wykazano gotowości do losowego seek filmu. Ocena dotyczy odczytanego baseline Studio/Toolbox/Open Assets; FrameMotion baseline Unknown.

**Moduł:** packages/three.quarks/src/ParticleSystem.ts i quarks.core/src/functions/IntervalValue.ts. [R08_SRC02](https://github.com/Alchemist0823/three.quarks/blob/de7c207f791c8b2260c43334a282976221688b1b/packages/three.quarks/src/ParticleSystem.ts) [R08_SRC03](https://github.com/Alchemist0823/three.quarks/blob/de7c207f791c8b2260c43334a282976221688b1b/packages/quarks.core/src/functions/IntervalValue.ts)

**Wejścia / wyjścia / parametry / edytowalność / alfa:** IN emitter, start values, behaviours, tekstura i delta; OUT live particles/batch. update integruje pozycję i wiek, ogranicza delta do 0.1; restart resetuje część stanu, ale IntervalValue używa Math.random. Brak potwierdzonego seed/seek contract. Parametry JSON edytowalne; alpha przez material/texture. [R08_SRC02](https://github.com/Alchemist0823/three.quarks/blob/de7c207f791c8b2260c43334a282976221688b1b/packages/three.quarks/src/ParticleSystem.ts) [R08_SRC03](https://github.com/Alchemist0823/three.quarks/blob/de7c207f791c8b2260c43334a282976221688b1b/packages/quarks.core/src/functions/IntervalValue.ts) [R08_README](https://github.com/Alchemist0823/three.quarks/blob/de7c207f791c8b2260c43334a282976221688b1b/README.md)

**Runtime / sprzęt / offline:** Three >=0.182.0 peer, CPU simulation + GPU render. quarks.core dependency ma wildcard *, wymagany pełny lock. prepare=husky w subpackage; monorepo workspace build jest większy niż runtime. Dokładny OS/browser/headless, RAM, VRAM i wydajność Unknown; nic nie zostało zainstalowane. [R08_SRC01](https://github.com/Alchemist0823/three.quarks/blob/de7c207f791c8b2260c43334a282976221688b1b/packages/three.quarks/package.json) [R08_PACKAGE](https://github.com/Alchemist0823/three.quarks/blob/de7c207f791c8b2260c43334a282976221688b1b/package.json)

**Eksport:** DERIVED: deterministyczny stan → istniejący renderer/capture → sekwencja PNG → istniejący encoder MP4 albo WebM. Nie ma własnego encodera; alfa zależy od render target/capture/kodeka. EXR nieudokumentowane. Zgodność Remotion/HyperFrames/FFmpeg to plan adaptera, nie sprawdzona integracja. Wymaga DERIVED deterministic replay od t=0 lub cache/bake; nie wystarczy render(delta=absoluteTime).

**Koszt / konto / sieć / zależności / instalacja:** Kod MIT bez klucza; ceny/konto/licencja osobnego edytora quarks.art Unknown, edytora nie rekomendujemy jako wymogu. DERIVED >=4–7 dni na seed audit/replay/cache; nie przewidywano instalacji. [R08_README](https://github.com/Alchemist0823/three.quarks/blob/de7c207f791c8b2260c43334a282976221688b1b/README.md) [R08_SRC01](https://github.com/Alchemist0823/three.quarks/blob/de7c207f791c8b2260c43334a282976221688b1b/packages/three.quarks/package.json)

**Prawa kodu i mediów:** MIT kod, nie automatycznie licencja sprite textures, modeli ani eksportowanych presetów edytora. Film: licencja silnika nie stanowi licencji wejściowych mediów; własna geometria może być renderowana komercyjnie, a font/asset wymaga osobnej zgody. Redystrybucja kodu: zachować właściwe notice. Assety, fonty, modele i media galerii: Unknown per plik, nie bundlować. Przykłady kodowe objęte repo notice tylko gdy brak osobnej licencji; linkowane dema nie są automatycznie objęte. [R08_LICENSE](https://github.com/Alchemist0823/three.quarks/blob/de7c207f791c8b2260c43334a282976221688b1b/LICENSE)

**Aktualność / błędy / utrzymanie:** HEAD 2026-05-21, three.quarks 0.17.1. Czytano wycinek generatora i ParticleSystem, nie wszystkie behaviours. Brak gwarancji determinism po samym restart(). [R08_META](https://api.github.com/repos/Alchemist0823/three.quarks/commits?per_page=1) [R08_SRC02](https://github.com/Alchemist0823/three.quarks/blob/de7c207f791c8b2260c43334a282976221688b1b/packages/three.quarks/src/ParticleSystem.ts) [R08_SRC03](https://github.com/Alchemist0823/three.quarks/blob/de7c207f791c8b2260c43334a282976221688b1b/packages/quarks.core/src/functions/IntervalValue.ts)

**Dowody:** DOCUMENTED + CODE_INSPECTED wskazane pliki; deklaracje autora i issue reports nie są pomiarem. OWN_TEST brak; wykonanie NOT_RUN. Rekomendacja, czas integracji i test są DERIVED.

**Właściciel integracji:** DERIVED: FrameMotion jako właściciel wąskiego adaptera, po ustaleniu jego API; Studio koordynuje i utrzymuje regułę/QA. Toolbox tylko przyszła kwalifikacja adaptera, nie automatyczne dodanie biblioteki.

**Forma:** KNOWLEDGE_ONLY

**Rekomendacja:** P2 / HOLD runtime: najpierw dowód kompletnego seedowania i reprodukcji. Przy prostym motion użyć czystej parametrycznej geometrii zamiast symulacji.

**Test przydatności:** NOT_RUN / DERIVED: 100 particles, fixed delta 1/60; dwa niezależne uruchomienia i restart do frame 90; hash positions, particle counts i obrazu; shuffled order przez cache. Stress pamięci i alpha edges, loop nie deklarować dopóki nie zbadano szwu.

**Status wykonania:** NOT_RUN

**Deep dive:** False

**Karta:** agents/runtime/CARDS.md

**Źródła:** [R08_README](https://github.com/Alchemist0823/three.quarks/blob/de7c207f791c8b2260c43334a282976221688b1b/README.md) [R08_PACKAGE](https://github.com/Alchemist0823/three.quarks/blob/de7c207f791c8b2260c43334a282976221688b1b/package.json) [R08_LICENSE](https://github.com/Alchemist0823/three.quarks/blob/de7c207f791c8b2260c43334a282976221688b1b/LICENSE) [R08_SRC01](https://github.com/Alchemist0823/three.quarks/blob/de7c207f791c8b2260c43334a282976221688b1b/packages/three.quarks/package.json) [R08_SRC02](https://github.com/Alchemist0823/three.quarks/blob/de7c207f791c8b2260c43334a282976221688b1b/packages/three.quarks/src/ParticleSystem.ts) [R08_SRC03](https://github.com/Alchemist0823/three.quarks/blob/de7c207f791c8b2260c43334a282976221688b1b/packages/quarks.core/src/functions/IntervalValue.ts) [R08_META](https://api.github.com/repos/Alchemist0823/three.quarks/commits?per_page=1)

## R09 — resvg-js — lokalna rasteryzacja klatek SVG

**ID:** R09

**Nazwa:** resvg-js — lokalna rasteryzacja klatek SVG

**Kanoniczny URL:** https://github.com/thx/resvg-js

**Owner upstream:** thx / projekt resvg-js (historyczne odwołania yisibl)

**Pin:** 9de8ddd9dd62293006d849dd846a3b91ba992f23

**Data przeglądu:** 2026-11-11

**Klasa:** A

**Nowość:** NEW

**Problem:** Render seryjnych, statycznych SVG do PNG bez browser layoutu i bez zależności od systemowych fontów.

**Delta baseline:** Baseline ma SVG/canvas i mediabunny, lecz odczytane karty nie wskazują konkretnego CPU SVG→PNG rasterizera z kontrolą font files. To adapter eksportowy, nie nowy engine animacji. Ocena dotyczy odczytanego baseline Studio/Toolbox/Open Assets; FrameMotion baseline Unknown.

**Moduł:** src/lib.rs/options.rs/fonts.rs, index.d.ts, js-binding.js. Resvg(svg,opts).render().asPng(); imagesToResolve/resolveImage. [R09_SRC01](https://github.com/thx/resvg-js/blob/9de8ddd9dd62293006d849dd846a3b91ba992f23/src/lib.rs) [R09_SRC02](https://github.com/thx/resvg-js/blob/9de8ddd9dd62293006d849dd846a3b91ba992f23/src/options.rs) [R09_SRC03](https://github.com/thx/resvg-js/blob/9de8ddd9dd62293006d849dd846a3b91ba992f23/src/fonts.rs) [R09_SRC05](https://github.com/thx/resvg-js/blob/9de8ddd9dd62293006d849dd846a3b91ba992f23/js-binding.js) [R09_SRC06](https://github.com/thx/resvg-js/blob/9de8ddd9dd62293006d849dd846a3b91ba992f23/index.d.ts)

**Wejścia / wyjścia / parametry / edytowalność / alfa:** IN SVG String/Buffer, fitTo/crop/background, fontFiles i loadSystemFonts; OUT PNG/RGBA, uproszczony SVG i bounds. Pojedynczy dokument statyczny; wrapper nie daje czasu SMIL/CSS. Ruch powstaje przez nowy SVG dla frame. Alfa wymaga decode/kompozycji testowej; raw pixels nie traktować bez sprawdzenia jak straight RGBA. [R09_SRC01](https://github.com/thx/resvg-js/blob/9de8ddd9dd62293006d849dd846a3b91ba992f23/src/lib.rs) [R09_SRC02](https://github.com/thx/resvg-js/blob/9de8ddd9dd62293006d849dd846a3b91ba992f23/src/options.rs) [R09_SRC06](https://github.com/thx/resvg-js/blob/9de8ddd9dd62293006d849dd846a3b91ba992f23/index.d.ts)

**Runtime / sprzęt / offline:** CPU native napi-rs dla Node; manifest Node >=10, to deklaracja, nie współczesny test wszystkich Node. Prebuilt targets obejmują macOS arm64/x64, Linux i Windows; osobny WASM route. js-binding wybiera local/platform package; Linux libc fallback może wywołać ldd. RAM/OS/zgodność hosta Unknown. [R09_PACKAGE](https://github.com/thx/resvg-js/blob/9de8ddd9dd62293006d849dd846a3b91ba992f23/package.json) [R09_SRC05](https://github.com/thx/resvg-js/blob/9de8ddd9dd62293006d849dd846a3b91ba992f23/js-binding.js)

**Eksport:** Bezpośredni PNG (asPng); DERIVED sekwencja PNG z frame-derived SVG → istniejący FFmpeg/encoder MP4 lub WebM. Nie renderuje interaktywnej strony; EXR brak udokumentowanego output. PNG z alphą do przyszłego decode QA. [R09_SRC06](https://github.com/thx/resvg-js/blob/9de8ddd9dd62293006d849dd846a3b91ba992f23/index.d.ts)

**Koszt / konto / sieć / zależności / instalacja:** Kod bez konta/klucza/usługi; lokalne fonty i obrazy umożliwiają offline po przygotowaniu. README no postinstall; package ma build/prepublishOnly, bez install hook. Cargo ma git rev resvg i branch woff2 patch: kontrola lock/release artefact, nie runtime download branch przez gotową binarkę. DERIVED 2–3 dni plus stress native memory. [R09_PACKAGE](https://github.com/thx/resvg-js/blob/9de8ddd9dd62293006d849dd846a3b91ba992f23/package.json) [R09_SRC04](https://github.com/thx/resvg-js/blob/9de8ddd9dd62293006d849dd846a3b91ba992f23/Cargo.toml) [R09_SRC05](https://github.com/thx/resvg-js/blob/9de8ddd9dd62293006d849dd846a3b91ba992f23/js-binding.js) [R09_README](https://github.com/thx/resvg-js/blob/9de8ddd9dd62293006d849dd846a3b91ba992f23/README.md)

**Prawa kodu i mediów:** MPL-2.0 kod: publikacja covered source/binary wymaga spełnienia §3 source availability/notices; większy program może mieć inną licencję. Sam film z własnego SVG nie jest dystrybucją renderer source. Fonty/model/obraz/przykładowy SourceHan font osobne Unknown. Nie kopiować example fonts bez licencji. [R09_LICENSE](https://github.com/thx/resvg-js/blob/9de8ddd9dd62293006d849dd846a3b91ba992f23/LICENSE) [RW_MPL](https://www.mozilla.org/en-US/MPL/2.0/FAQ/)

**Aktualność / błędy / utrzymanie:** HEAD 2026-03-26; manifest 2.7.0-alpha.2, nie stabilna rekomendacja. #421 raportuje memory retention 2.6.2/alpha.2; #423 abort 2.6.2. Odczytany lib.rs ma external memory accounting/catch unwind, lecz nie dowodzi naprawy żadnego issue. NOT_RUN. [R09_META](https://api.github.com/repos/thx/resvg-js/commits?per_page=1) [R09_PACKAGE](https://github.com/thx/resvg-js/blob/9de8ddd9dd62293006d849dd846a3b91ba992f23/package.json) [R09_ISSUE421](https://github.com/thx/resvg-js/issues/421) [R09_ISSUE423](https://github.com/thx/resvg-js/issues/423) [R09_SRC01](https://github.com/thx/resvg-js/blob/9de8ddd9dd62293006d849dd846a3b91ba992f23/src/lib.rs)

**Dowody:** DOCUMENTED + CODE_INSPECTED wskazane pliki; deklaracje autora i issue reports nie są pomiarem. OWN_TEST brak; wykonanie NOT_RUN. Rekomendacja, czas integracji i test są DERIVED.

**Właściciel integracji:** DERIVED: FrameMotion jako właściciel wąskiego adaptera, po ustaleniu jego API; Studio koordynuje i utrzymuje regułę/QA. Toolbox tylko przyszła kwalifikacja adaptera, nie automatyczne dodanie biblioteki.

**Forma:** ADAPTER

**Rekomendacja:** P0 kwalifikacja eksportu, ale HOLD production do font/alpha/memory i crash QA. Pin binary+platform package+hash zgodny ze source; wybór stabilnej wersji osobno. Renderer fallback tylko jawny, z osobnym baseline obrazu.

**Test przydatności:** NOT_RUN / DERIVED: SVG własna geometria + Zażółć gęślą jaźń + gradient/maska/blur; lokalny font z hashem, loadSystemFonts=false, no network. 180 klatek 1080p i 4K stress w izolowanym workerze; peak/RSS trend i brak abort. PNG decode dimensions/alpha; composite white/black; shuffled frame, porównanie browser/resvg jako oddzielne oracle, 16:9/9:16.

**Status wykonania:** NOT_RUN

**Deep dive:** True

**Karta:** agents/runtime/CARDS.md

**Źródła:** [R09_README](https://github.com/thx/resvg-js/blob/9de8ddd9dd62293006d849dd846a3b91ba992f23/README.md) [R09_PACKAGE](https://github.com/thx/resvg-js/blob/9de8ddd9dd62293006d849dd846a3b91ba992f23/package.json) [R09_LICENSE](https://github.com/thx/resvg-js/blob/9de8ddd9dd62293006d849dd846a3b91ba992f23/LICENSE) [R09_SRC01](https://github.com/thx/resvg-js/blob/9de8ddd9dd62293006d849dd846a3b91ba992f23/src/lib.rs) [R09_SRC02](https://github.com/thx/resvg-js/blob/9de8ddd9dd62293006d849dd846a3b91ba992f23/src/options.rs) [R09_SRC03](https://github.com/thx/resvg-js/blob/9de8ddd9dd62293006d849dd846a3b91ba992f23/src/fonts.rs) [R09_SRC04](https://github.com/thx/resvg-js/blob/9de8ddd9dd62293006d849dd846a3b91ba992f23/Cargo.toml) [R09_SRC05](https://github.com/thx/resvg-js/blob/9de8ddd9dd62293006d849dd846a3b91ba992f23/js-binding.js) [R09_SRC06](https://github.com/thx/resvg-js/blob/9de8ddd9dd62293006d849dd846a3b91ba992f23/index.d.ts) [R09_SRC07](https://github.com/thx/resvg-js/blob/9de8ddd9dd62293006d849dd846a3b91ba992f23/example/index.js) [R09_META](https://api.github.com/repos/thx/resvg-js/commits?per_page=1) [R09_ISSUES](https://api.github.com/repos/thx/resvg-js/issues?state=open&per_page=5) [R09_ISSUE421](https://github.com/thx/resvg-js/issues/421) [R09_ISSUE423](https://github.com/thx/resvg-js/issues/423) [RW_MPL](https://www.mozilla.org/en-US/MPL/2.0/FAQ/)

## R10 — pixelmatch — obrazowy comparator do obecnego QA

**ID:** R10

**Nazwa:** pixelmatch — obrazowy comparator do obecnego QA

**Kanoniczny URL:** https://github.com/mapbox/pixelmatch

**Owner upstream:** mapbox / Volodymyr Agafonkin

**Pin:** ab76f526ef951c0ec6284e314a700e161b1800e6

**Data przeglądu:** 2026-11-11

**Klasa:** A

**Nowość:** KNOWN_NEW_CAPABILITY

**Problem:** Lokalizacja różnic pomiędzy tym samym frame po rewind i między preview/export.

**Delta baseline:** Baseline ma motion QA i pixel diff; delta to przypięty comparator v8 z jawną polityką AA/alpha/threshold, nie nowy system oceny jakości. Ocena dotyczy odczytanego baseline Studio/Toolbox/Open Assets; FrameMotion baseline Unknown.

**Moduł:** index.js pixelmatch(img1,img2,output,w,h,options); CLI bin deklarowany, nie odczytany. [R10_SRC01](https://github.com/mapbox/pixelmatch/blob/ab76f526ef951c0ec6284e314a700e161b1800e6/index.js) [R10_PACKAGE](https://github.com/mapbox/pixelmatch/blob/ab76f526ef951c0ec6284e314a700e161b1800e6/package.json)

**Wejścia / wyjścia / parametry / edytowalność / alfa:** IN RGBA arrays o równych rozmiarach; OUT liczba różnic lub max local-window oraz diff. threshold to różnica koloru per pixel, nie procent obrazu. Default includeAA=false; checkerboard=true wpływa na alpha porównanie. Parametr alpha steruje tłem diff, nie eksportem alfy. [R10_README](https://github.com/mapbox/pixelmatch/blob/ab76f526ef951c0ec6284e314a700e161b1800e6/README.md) [R10_SRC01](https://github.com/mapbox/pixelmatch/blob/ab76f526ef951c0ec6284e314a700e161b1800e6/index.js)

**Runtime / sprzęt / offline:** JS CPU browser/Node; core operuje na arrays; package ma pngjs runtime dependency dla ścieżki PNG/CLI mimo README no-dependencies claim o core. Scripts pretest/test bez install hooks. Dokładny OS/browser/headless, RAM, VRAM i wydajność Unknown; nic nie zostało zainstalowane. [R10_PACKAGE](https://github.com/mapbox/pixelmatch/blob/ab76f526ef951c0ec6284e314a700e161b1800e6/package.json) [R10_README](https://github.com/mapbox/pixelmatch/blob/ab76f526ef951c0ec6284e314a700e161b1800e6/README.md)

**Eksport:** Wytwarza diff pixels, PNG po zewnętrznym zapisie; brak filmu. Wpiąć do obecnego QA po decode klatek; MP4/WebM i EXR nie są inputem API bez dekodera. [R10_README](https://github.com/mapbox/pixelmatch/blob/ab76f526ef951c0ec6284e314a700e161b1800e6/README.md)

**Koszt / konto / sieć / zależności / instalacja:** ISC library bez konta/klucza/sieci przy lokalnych arrays. DERIVED 0.5–1 dzień, tylko gdy obecny comparator nie daje tej funkcji. [R10_LICENSE](https://github.com/mapbox/pixelmatch/blob/ab76f526ef951c0ec6284e314a700e161b1800e6/LICENSE)

**Prawa kodu i mediów:** ISC code: zachować notice. Film: licencja silnika nie stanowi licencji wejściowych mediów; własna geometria może być renderowana komercyjnie, a font/asset wymaga osobnej zgody. Redystrybucja kodu: zachować właściwe notice. Assety, fonty, modele i media galerii: Unknown per plik, nie bundlować. Przykłady kodowe objęte repo notice tylko gdy brak osobnej licencji; linkowane dema nie są automatycznie objęte. [R10_LICENSE](https://github.com/mapbox/pixelmatch/blob/ab76f526ef951c0ec6284e314a700e161b1800e6/LICENSE)

**Aktualność / błędy / utrzymanie:** HEAD 2026-10-06; package 8.0.0. Metryka OKLab/HyAB opisana w README, nie zakładać zgodności progów ze starszymi wersjami. Nie mierzy czytelności, rytmu ani poprawności praw do assetu. [R10_META](https://api.github.com/repos/mapbox/pixelmatch/commits?per_page=1) [R10_PACKAGE](https://github.com/mapbox/pixelmatch/blob/ab76f526ef951c0ec6284e314a700e161b1800e6/package.json) [R10_README](https://github.com/mapbox/pixelmatch/blob/ab76f526ef951c0ec6284e314a700e161b1800e6/README.md)

**Dowody:** DOCUMENTED + CODE_INSPECTED wskazane pliki; deklaracje autora i issue reports nie są pomiarem. OWN_TEST brak; wykonanie NOT_RUN. Rekomendacja, czas integracji i test są DERIVED.

**Właściciel integracji:** DERIVED: FrameMotion jako właściciel wąskiego adaptera, po ustaleniu jego API; Studio koordynuje i utrzymuje regułę/QA. Toolbox tylko przyszła kwalifikacja adaptera, nie automatyczne dodanie biblioteki.

**Forma:** SKILL_ADAPTATION

**Rekomendacja:** P0: doprecyzować politykę exact-vs-tolerant w obecnym QA; helper OPTIONAL_DEPENDENCY dopiero jeśli obecny moduł nie ma porównywalnej funkcji.

**Test przydatności:** NOT_RUN / DERIVED: Known-equal frame, single-pixel mutation, AA-only mutation i RGB przy alpha=0; osobno hash raw/decoded i perceptual diff. Kontrolne błędy muszą zostać wykryte. Ogląd pełnej sekwencji i diff overlay, nie tylko zerowy count.

**Status wykonania:** NOT_RUN

**Deep dive:** False

**Karta:** agents/runtime/CARDS.md

**Źródła:** [R10_README](https://github.com/mapbox/pixelmatch/blob/ab76f526ef951c0ec6284e314a700e161b1800e6/README.md) [R10_PACKAGE](https://github.com/mapbox/pixelmatch/blob/ab76f526ef951c0ec6284e314a700e161b1800e6/package.json) [R10_LICENSE](https://github.com/mapbox/pixelmatch/blob/ab76f526ef951c0ec6284e314a700e161b1800e6/LICENSE) [R10_SRC01](https://github.com/mapbox/pixelmatch/blob/ab76f526ef951c0ec6284e314a700e161b1800e6/index.js) [R10_META](https://api.github.com/repos/mapbox/pixelmatch/commits?per_page=1)

## R11 — MeshLine — grube 3D linie i trails

**ID:** R11

**Nazwa:** MeshLine — grube 3D linie i trails

**Kanoniczny URL:** https://github.com/pmndrs/meshline

**Owner upstream:** pmndrs / autor oryginału Jaume Sanchez

**Pin:** 4df8778398e086628076267c67552c079d39be85

**Data przeglądu:** 2026-11-11

**Klasa:** A

**Nowość:** DUPLICATE/FORK

**Problem:** Variable-width/dashed linie billboardowane w Three zamiast platformowego GL_LINE.

**Delta baseline:** README wprost fork spite/THREE.MeshLine; brak wykazanej przewagi nad istniejącą ścieżką Three dla celu FrameCore. Zachować jako comparator, nie samodzielną nowość. Ocena dotyczy odczytanego baseline Studio/Toolbox/Open Assets; FrameMotion baseline Unknown.

**Moduł:** src/MeshLineGeometry.ts setPoints/advance; MeshLineMaterial API w README. [R11_SRC01](https://github.com/pmndrs/meshline/blob/4df8778398e086628076267c67552c079d39be85/src/MeshLineGeometry.ts) [R11_README](https://github.com/pmndrs/meshline/blob/4df8778398e086628076267c67552c079d39be85/README.md)

**Wejścia / wyjścia / parametry / edytowalność / alfa:** IN points i widthCallback, dashOffset/resolution/opacity; OUT triangle-strip mesh. advance usuwa najstarszy punkt i akumuluje historię, dlatego DERIVED trail odtwarzać z deterministycznej listy punktów dla frame. Nie kopiować README widthCallback z Math.random. Alfa zależy od material, depth i blending. [R11_SRC01](https://github.com/pmndrs/meshline/blob/4df8778398e086628076267c67552c079d39be85/src/MeshLineGeometry.ts) [R11_README](https://github.com/pmndrs/meshline/blob/4df8778398e086628076267c67552c079d39be85/README.md)

**Runtime / sprzęt / offline:** Three >=0.137 peer, WebGL GPU. Brak install hooks w scripts build/dev. CPU koszt przebudowy points; headless/VRAM Unknown. Dokładny OS/browser/headless, RAM, VRAM i wydajność Unknown; nic nie zostało zainstalowane. [R11_PACKAGE](https://github.com/pmndrs/meshline/blob/4df8778398e086628076267c67552c079d39be85/package.json)

**Eksport:** DERIVED: deterministyczny stan → istniejący renderer/capture → sekwencja PNG → istniejący encoder MP4 albo WebM. Nie ma własnego encodera; alfa zależy od render target/capture/kodeka. EXR nieudokumentowane. Zgodność Remotion/HyperFrames/FFmpeg to plan adaptera, nie sprawdzona integracja.

**Koszt / konto / sieć / zależności / instalacja:** MIT bez konta/klucza. Offline z własnymi teksturami. DERIVED 1–2 dni, bez uzasadnienia przed porównaniem baseline. [R11_PACKAGE](https://github.com/pmndrs/meshline/blob/4df8778398e086628076267c67552c079d39be85/package.json)

**Prawa kodu i mediów:** MIT fork z notice oryginalnego autora. Film: licencja silnika nie stanowi licencji wejściowych mediów; własna geometria może być renderowana komercyjnie, a font/asset wymaga osobnej zgody. Redystrybucja kodu: zachować właściwe notice. Assety, fonty, modele i media galerii: Unknown per plik, nie bundlować. Przykłady kodowe objęte repo notice tylko gdy brak osobnej licencji; linkowane dema nie są automatycznie objęte. [R11_LICENSE](https://github.com/pmndrs/meshline/blob/4df8778398e086628076267c67552c079d39be85/LICENSE)

**Aktualność / błędy / utrzymanie:** HEAD 2024-06-03, 3.3.1. README deklaruje BufferGeometry input, kod convertPoints wymaga osobnego kompatybilności testu, nie przyjmować całej listy input za sprawdzoną. [R11_META](https://api.github.com/repos/pmndrs/meshline/commits?per_page=1) [R11_README](https://github.com/pmndrs/meshline/blob/4df8778398e086628076267c67552c079d39be85/README.md) [R11_SRC01](https://github.com/pmndrs/meshline/blob/4df8778398e086628076267c67552c079d39be85/src/MeshLineGeometry.ts)

**Dowody:** DOCUMENTED + CODE_INSPECTED wskazane pliki; deklaracje autora i issue reports nie są pomiarem. OWN_TEST brak; wykonanie NOT_RUN. Rekomendacja, czas integracji i test są DERIVED.

**Właściciel integracji:** DERIVED: FrameMotion jako właściciel wąskiego adaptera, po ustaleniu jego API; Studio koordynuje i utrzymuje regułę/QA. Toolbox tylko przyszła kwalifikacja adaptera, nie automatyczne dodanie biblioteki.

**Forma:** KNOWLEDGE_ONLY

**Rekomendacja:** P2: pattern trailAtFrame; nie dodawać forka tylko dla nazwy. Potencjalny mały adapter po dowodzie lepszej jakości niż obecne Three lines.

**Test przydatności:** NOT_RUN / DERIVED: Zmienne width i dash, ostry zakręt, transparent trail na przecięciach; frame order [90,0,89,90], portrait/wide resolution; ogląd aliasingu i depth sorting w całym klipie.

**Status wykonania:** NOT_RUN

**Deep dive:** False

**Karta:** agents/runtime/CARDS.md

**Źródła:** [R11_README](https://github.com/pmndrs/meshline/blob/4df8778398e086628076267c67552c079d39be85/README.md) [R11_PACKAGE](https://github.com/pmndrs/meshline/blob/4df8778398e086628076267c67552c079d39be85/package.json) [R11_LICENSE](https://github.com/pmndrs/meshline/blob/4df8778398e086628076267c67552c079d39be85/LICENSE) [R11_SRC01](https://github.com/pmndrs/meshline/blob/4df8778398e086628076267c67552c079d39be85/src/MeshLineGeometry.ts) [R11_META](https://api.github.com/repos/pmndrs/meshline/commits?per_page=1)

## R12 — opentype.js — kontury glifów do geometry motion

**ID:** R12

**Nazwa:** opentype.js — kontury glifów do geometry motion

**Kanoniczny URL:** https://github.com/opentypejs/opentype.js

**Owner upstream:** opentypejs / Frederik De Bleser i contributors

**Pin:** 5d65b6dcfab5115f90d375f8ba6b7942fdaa0138

**Data przeglądu:** 2026-11-11

**Klasa:** A

**Nowość:** KNOWN_NEW_CAPABILITY

**Problem:** Uzyskanie krzywych i metryk glifu do deformacji, outline reveal i kontrolowanego layoutu.

**Delta baseline:** Baseline ma SplitText i text QA; delta to data-level font outlines, nie kolejny mechanizm rozdzielania DOM liter. Ocena dotyczy odczytanego baseline Studio/Toolbox/Open Assets; FrameMotion baseline Unknown.

**Moduł:** src/font.mjs getPath/getPaths/getAdvanceWidth/stringToGlyphs; parse font bytes. [R12_SRC01](https://github.com/opentypejs/opentype.js/blob/5d65b6dcfab5115f90d375f8ba6b7942fdaa0138/src/font.mjs) [R12_README](https://github.com/opentypejs/opentype.js/blob/5d65b6dcfab5115f90d375f8ba6b7942fdaa0138/README.md)

**Wejścia / wyjścia / parametry / edytowalność / alfa:** IN OTF/TTF/WOFF i tekst; OUT path(s)/metrics/glyphs. Zachowuje kompozytowe litery według docs; ligatury oznaczają, że glyph≠character. Edytowalne krzywe, ale prawa fontu nadal obowiązują. WOFF2 wymaga osobnego dekompresora, nie native parse. Alfa N/A dla geometry. [R12_README](https://github.com/opentypejs/opentype.js/blob/5d65b6dcfab5115f90d375f8ba6b7942fdaa0138/README.md) [R12_SRC01](https://github.com/opentypejs/opentype.js/blob/5d65b6dcfab5115f90d375f8ba6b7942fdaa0138/src/font.mjs)

**Runtime / sprzęt / offline:** Browser/Node CPU; plik package bez version, pin commit jest identyfikatorem. Brak declared runtime dependencies; WOFF2 przykład pobiera osobny WASM/decompress script. Scripts build/test, bez install hook. Dokładny OS/browser/headless, RAM, VRAM i wydajność Unknown; nic nie zostało zainstalowane. [R12_PACKAGE](https://github.com/opentypejs/opentype.js/blob/5d65b6dcfab5115f90d375f8ba6b7942fdaa0138/package.json) [R12_README](https://github.com/opentypejs/opentype.js/blob/5d65b6dcfab5115f90d375f8ba6b7942fdaa0138/README.md)

**Eksport:** DERIVED: deterministyczny stan → istniejący renderer/capture → sekwencja PNG → istniejący encoder MP4 albo WebM. Nie ma własnego encodera; alfa zależy od render target/capture/kodeka. EXR nieudokumentowane. Zgodność Remotion/HyperFrames/FFmpeg to plan adaptera, nie sprawdzona integracja. DERIVED eksport ścieżek do SVG w host adapterze; sama biblioteka nie koduje wideo.

**Koszt / konto / sieć / zależności / instalacja:** Bez konta/klucza dla parsera; fonty mogą kosztować i mieć ograniczenia embeddingu. Preferować lokalne TTF/OTF, nie CDN WOFF2 przykład. DERIVED 1–2 dni + typographic QA. [R12_README](https://github.com/opentypejs/opentype.js/blob/5d65b6dcfab5115f90d375f8ba6b7942fdaa0138/README.md)

**Prawa kodu i mediów:** MIT kod, ale test/fonts/LICENSE podaje OFL-1.1, Apache-2.0 (Roboto) oraz CC BY-SA 4.0 (OpenMoji subset) per plik. Font-source redistribution, outline-derived asset i renderowany film oceniać osobno według konkretnej licencji. Nie importować folderu test/fonts jako MIT assets. Modele/pozostałe media Unknown; przykładowy kod repo pod notice. [R12_LICENSE](https://github.com/opentypejs/opentype.js/blob/5d65b6dcfab5115f90d375f8ba6b7942fdaa0138/LICENSE) [R12_SRC02](https://github.com/opentypejs/opentype.js/blob/5d65b6dcfab5115f90d375f8ba6b7942fdaa0138/test/fonts/LICENSE)

**Aktualność / błędy / utrzymanie:** HEAD 2026-05-19; poprawka checksum nie jest testem wszystkich fontów. Manifest nie zawiera package version. Brak dowodu zgodności layoutu z browser shaping dla każdego skryptu; sprawdzić właściwy język/ligatury. [R12_META](https://api.github.com/repos/opentypejs/opentype.js/commits?per_page=1) [R12_PACKAGE](https://github.com/opentypejs/opentype.js/blob/5d65b6dcfab5115f90d375f8ba6b7942fdaa0138/package.json) [R12_SRC01](https://github.com/opentypejs/opentype.js/blob/5d65b6dcfab5115f90d375f8ba6b7942fdaa0138/src/font.mjs)

**Dowody:** DOCUMENTED + CODE_INSPECTED wskazane pliki; deklaracje autora i issue reports nie są pomiarem. OWN_TEST brak; wykonanie NOT_RUN. Rekomendacja, czas integracji i test są DERIVED.

**Właściciel integracji:** DERIVED: FrameMotion jako właściciel wąskiego adaptera, po ustaleniu jego API; Studio koordynuje i utrzymuje regułę/QA. Toolbox tylko przyszła kwalifikacja adaptera, nie automatyczne dodanie biblioteki.

**Forma:** OPTIONAL_DEPENDENCY

**Rekomendacja:** P1: wąski outline extraction contract przy rzeczywistej potrzebie deformacji glifów. Dla prostego text reveal korzystać z obecnego HTML/font workflow.

**Test przydatności:** NOT_RUN / DERIVED: Polski NFC/NFD, AV kerning, fi ligature, Ł/ą/ź i missing glyph; bounds, number of glyphs vs graphemes, porównanie z zatwierdzonym wzorcem fontu; same layout po shuffled seek, full reveal i clipping w 16:9/9:16.

**Status wykonania:** NOT_RUN

**Deep dive:** False

**Karta:** agents/runtime/CARDS.md

**Źródła:** [R12_README](https://github.com/opentypejs/opentype.js/blob/5d65b6dcfab5115f90d375f8ba6b7942fdaa0138/README.md) [R12_PACKAGE](https://github.com/opentypejs/opentype.js/blob/5d65b6dcfab5115f90d375f8ba6b7942fdaa0138/package.json) [R12_LICENSE](https://github.com/opentypejs/opentype.js/blob/5d65b6dcfab5115f90d375f8ba6b7942fdaa0138/LICENSE) [R12_SRC01](https://github.com/opentypejs/opentype.js/blob/5d65b6dcfab5115f90d375f8ba6b7942fdaa0138/src/font.mjs) [R12_SRC02](https://github.com/opentypejs/opentype.js/blob/5d65b6dcfab5115f90d375f8ba6b7942fdaa0138/test/fonts/LICENSE) [R12_META](https://api.github.com/repos/opentypejs/opentype.js/commits?per_page=1)

