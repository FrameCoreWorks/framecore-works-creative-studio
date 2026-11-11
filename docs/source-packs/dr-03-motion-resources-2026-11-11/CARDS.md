# DR-03 — kompletne karty kandydatów

Data: 2026-11-11. Wykonanie kandydatów: NOT_RUN. Źródła przy twierdzeniach; zbiorczy rejestr SOURCES.json. Klasy/nowość w CATALOG.json; rankingi i priorytety leada w RANKINGS.md i IMPLEMENTATION_HANDOFF.md.

---

## Klasa A: runtime

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


---

## Klasa B: knowledge

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


---

## Klasa C: assets

# DR-03 C — kompletne karty assetów

Data: 2026-11-11. Dziewięć kart: sześć NEW, dwa ALREADY_COVERED i jeden BASELINE_UNKNOWN / REFERENCE_ONLY. Nowość oceniona względem odczytanego BASELINE.md; nie jest deklaracją funkcji FrameMotion. useAnimations i Generative Icons są znane i nie zostały ponownie skatalogowane.

Research wykonano przez GitHub connector i publiczne strony autorów. Nie pobrano binariów, archiwów, .riv, VDB ani skompilowanych ikon. Nie uruchomiono kandydatów, instalacji, zakupów, uploadów lub rendererów. **Wszystkie próby wykonawcze: NOT_RUN.** Metadane i deklaracje autora nie dowodzą wyglądu, alfy ani jakości pętli. Dane opisane jako DERIVED są propozycją integracji lub testu.

Prawa rozdzielono dla kodu, assetów, fontów, modeli i przykładów oraz dla filmu i źródłowej redystrybucji. Brak pliku nie został zastąpiony domysłem. Open Assets jest właścicielem pozyskiwania, ale wskazanie nowej strony nie oznacza kwalifikowanego providera lub działającej ścieżki pobrania.

## A01 — Meteocons — weather SVG/Lottie

[Strona kanoniczna](https://github.com/basmilius/meteocons) · Autor: Bas Milius / basmilius · Klasa C · **NEW** · Przegląd: 2026-11-11.

Dowody: DOCUMENTED; CODE_INSPECTED (wybrane pliki i fragmenty); NOT_RUN; DERIVED (integracja/test).

Źródła materialnych twierdzeń: [AS01](https://api.github.com/repos/basmilius/meteocons/commits?per_page=1), [AS02](https://github.com/basmilius/meteocons), [AS03](https://github.com/basmilius/meteocons/blob/70dfb1d6e30dc9e791cfb0e4c5b5e5e60e972aa0/.gitignore), [AS04](https://github.com/basmilius/meteocons/blob/70dfb1d6e30dc9e791cfb0e4c5b5e5e60e972aa0/packages/lottie/package.json), [AS05](https://github.com/basmilius/meteocons/blob/70dfb1d6e30dc9e791cfb0e4c5b5e5e60e972aa0/packages/exporter/package.json), [AS06](https://github.com/basmilius/meteocons/blob/70dfb1d6e30dc9e791cfb0e4c5b5e5e60e972aa0/animations/configs/sun.json), [AS07](https://github.com/basmilius/meteocons/blob/70dfb1d6e30dc9e791cfb0e4c5b5e5e60e972aa0/animations/partials/sun.json), [AS08](https://github.com/basmilius/meteocons/blob/70dfb1d6e30dc9e791cfb0e4c5b5e5e60e972aa0/packages/lottie/LICENSE), [AS09](https://github.com/basmilius/meteocons/blob/70dfb1d6e30dc9e791cfb0e4c5b5e5e60e972aa0/packages/exporter/src/lottie/animation-helpers.ts), [AS10](https://github.com/basmilius/meteocons/blob/70dfb1d6e30dc9e791cfb0e4c5b5e5e60e972aa0/packages/exporter/src/lottie/generator.ts), [AS11](https://github.com/basmilius/meteocons/blob/70dfb1d6e30dc9e791cfb0e4c5b5e5e60e972aa0/packages/exporter/src/svg/processor.ts), [AS12](https://github.com/basmilius/meteocons/blob/70dfb1d6e30dc9e791cfb0e4c5b5e5e60e972aa0/package.json), [AS13](https://api.github.com/repos/basmilius/meteocons/releases?per_page=2), [AS14](https://meteocons.com/docs/cdn/), [AS15](https://github.com/basmilius/meteocons/issues/54).

**Pin / wersja.** Source 70dfb1d6e30dc9e791cfb0e4c5b5e5e60e972aa0; release 3.0.0-next.9; site 3.0.0-next.10; source package 0.0.0; selected compiled asset hash Unknown

**Problem produkcyjny.** Spójne animowane symbole pogody i energii dla infografik bez rysowania każdego stanu.

**Różnica względem baseline.** Nowa konkretna rodzina assetów; Lottie engine i master-time już istnieją w baseline. Nie zastępuje useAnimations ani Generative Icons.

**Konkretny moduł / asset.** Docelowy fixture: clear-day, rain i wind-beaufort-1 w SVG/Lottie. Odczytane animations/configs/sun.json, partials/sun.json, exporter generator/helpers/processor i manifesty; skompilowane pliki pozostają niepobrane.

**Wejścia, wyjścia i edycja.** SVG/SMIL i JSON Lottie; style fill/flat/line/monochrome. Kolory/geometria edytowalne po kontroli praw. Plik JSON vs .lottie container to różne formaty; kontener nie sprawdzony.

**Runtime i zasoby.** DERIVED: przeglądarka/headless z przypiętym lottie-web 5.13.0 z baseline albo kontrolowanym inline SVG; CPU/GPU/RAM Unknown. Odtwarzanie offline możliwe dopiero po lokalnym zapisaniu zatwierdzonego pliku. Budowa źródła wymaga Bun/Figma token/network; nie jest potrzebna do użycia gotowego assetu.

**Droga eksportu.** DERIVED: asset frame → istniejący adapter Lottie/SVG → PNG RGBA → MP4 na tle; WebM alpha tylko po kontroli kodeka. Remotion/HyperFrames przez istniejący master-time; brak dowodu kompatybilności per asset.

**Koszt, konto i sieć.** Ikony MIT bez opłaty; sieć do pozyskania. Konta/klucza nie potrzeba w opisie CDN; autoring/exporter Figma wymaga tokena. Zero usług uruchomionych.

**Utrzymanie i ograniczenia.** HEAD z 2026-04-12; wersje rozjechane. Generated outputs są gitignored. CDN prerelease może zniknąć 3 miesiące po następnym pełnym release. Issue 54 opisuje przyspieszenie dash tuż przed loop; raport nieodtworzony i wewnętrznie niejednoznaczny co do wind-beaufort-12.

**Właściciel docelowy.** Open Assets: pin/proweniencja; Studio hyperframes-workflow: renderer QA; FrameMotion tylko proponowany przyszły adapter, API Unknown.

**Forma integracji.** ON_DEMAND_ASSET

**Rekomendacja.** P1 warunkowo: pojedyncze zatwierdzone ikony z zapisanym hashem; nie klon całego generatora i nie latest CDN. Wind-beaufort jako negatywny fixture do temporal QA.

### Prawa

| Zakres | Ustalenie |
|---|---|
| Kod | MIT repo/exporter; zależności mają odrębne licencje, nieaudytowane |
| Assety | MIT w packages/lottie/LICENSE |
| Fonty | Unknown; no font files inspected |
| Modele / rig | N/A |
| Przykłady / preview | Nie przenosić automatycznie praw do screenshotów, Figma workspace lub zależności |
| Wyrenderowany film | Dopuszczone użycie komercyjne wg MIT, z zachowaniem notices w dystrybucji produktu |
| Redystrybucja źródeł | MIT ze wskazanym copyright i treścią licencji; tylko objęte pliki |

### Metadane assetu

| Pole | Ustalenie |
|---|---|
| Rozdzielczość | Unknown dla gotowego pliku; wektorowy format |
| Długość | Kod generatora: 360 frames / 60 fps = 6 s; partial sun: 6 s; NIE odczyt konkretnego op/fr pobranego assetu |
| FPS | 60 w odczytanym generatorze; konkretny plik Unknown |
| Pętla / seam | SVG repeatCount indefinite; sun pełny obrót. Jakość seam Unknown, issue 54 opisuje wadę innych ikon |
| Alfa | Unknown; żaden eksport RGBA nieodczytany |
| Warstwy | Sun partial: Rays; pełny zestaw warstw konkretnego assetu Unknown |
| Powiązane pliki | configs, partials, generated SVG i Lottie; zależności Figma dla odtworzenia źródła |
| Pochodzenie | Bas Milius; źródła animacji w repo; gotowe ikony publikowane przez autora |

### Plan próby — NOT_RUN

**Fixture:** clear-day/rain/wind-beaufort-1; po zgodzie pobrania pin/version/hash; 0,359,17,120,0 w 60 fps; 16:9 / 9:16; label „Zażółć gęślą jaźń” obok ikony.

**Oczekiwany wynik:** Ten sam frame z obu kolejności, brak samoczynnego tickera, pokrycie renderer SVG/Canvas oznaczone osobno; zachowana alfa i granice.

**Objawy błędu:** Nagłe przyspieszenie przy końcu, offset maski, różnice SVG/Lottie, białe tło, clipping.

**Ogląd temporalny:** Pełna 6 s pętla dwa razy w tempie docelowym i 0.25×; contact sheet początku/końca nie zastępuje odtworzenia.

## A02 — Kenney Particle Pack

[Strona kanoniczna](https://kenney.nl/assets/particle-pack) · Autor: Kenney · Klasa C · **NEW** · Przegląd: 2026-11-11.

Dowody: DOCUMENTED; NOT_RUN; DERIVED.

Źródła materialnych twierdzeń: [AS16](https://kenney.nl/assets/particle-pack), [AS17](https://kenney.nl/support), [AS34](https://creativecommons.org/publicdomain/zero/1.0/).

**Pin / wersja.** 1.0 (2018); paczka/hash Unknown

**Problem produkcyjny.** Małe tekstury wejściowe do cząstek i shaderów bez dodatkowego pełnego silnika.

**Różnica względem baseline.** Uzupełnia procedural PixelFX o konkretną rodzinę źródłowych masek. Nie jest nową symulacją ani gotową animowaną pętlą.

**Konkretny moduł / asset.** Particle Pack — 80 plików według autora. Konkretny basename i format pliku Unknown, archiwum nieotwarte.

**Wejścia, wyjścia i edycja.** Raster 512×512; format/bit depth/alpha Unknown do import/decode. Parametry ruchu nadaje konsument.

**Runtime i zasoby.** DERIVED: HTML Canvas/PixiJS/Three.js lub Blender jako tekstura; bez własnego runtime. Zużycie RAM zależne od atlasu/liczby cząstek; dokładne Unknown. Offline po pobraniu.

**Droga eksportu.** DERIVED: deterministyczny emitter frame/seed → PNG RGBA lub istniejący eksport wideo; FFmpeg składa zatwierdzone klatki. Sam pack nie eksportuje filmu.

**Koszt, konto i sieć.** Bezpłatny pack; dobrowolna donacja, płatne All-in-1 nie jest konieczne. Nie podano potrzeby klucza. Download niepróbowany.

**Utrzymanie i ograniczenia.** Wersja 1.0 z 2018; brak dowodu błędów lub dalszego maintenance tego packa. Stary asset nie oznacza przestarzałego runtime, bo runtime brak.

**Właściciel docelowy.** Open Assets dla praw/pobrania; Studio/FrameMotion dla parametrów emittera.

**Forma integracji.** ON_DEMAND_ASSET

**Rekomendacja.** P1 mały pilot 2–3 tekstur. Nie zakładać istniejącego kwalifikowanego providera Kenney w Open Assets.

### Prawa

| Zakres | Ustalenie |
|---|---|
| Kod | Not included / Unknown if added separately |
| Assety | CC0 |
| Fonty | Unknown; no font files inspected |
| Modele / rig | N/A |
| Przykłady / preview | Logo Kenney wyłączone; nie używać jako endorsement |
| Wyrenderowany film | Użycie komercyjne objętych plików |
| Redystrybucja źródeł | CC0 pozwala redistribuować objęte assety |

### Metadane assetu

| Pole | Ustalenie |
|---|---|
| Rozdzielczość | 512×512 wg strony |
| Długość | N/A dla statycznej tekstury; animacja Unknown |
| FPS | N/A |
| Pętla / seam | Unknown; asset nie jest potwierdzonym flipbookiem |
| Alfa | Unknown |
| Warstwy | Unknown |
| Powiązane pliki | 80 plików; zawartość i formaty archiwum Unknown |
| Pochodzenie | Kenney, autorska strona packa |

### Plan próby — NOT_RUN

**Fixture:** Po osobnym pobraniu jedna soft-particle i jedna ostra maska; seed 42, 300 frames; 50/200 cząstek.

**Oczekiwany wynik:** Decode/rozmiar zgodny; powtarzalne pozycje; poza kształtem przezroczystość potwierdzona; koszt zmierzony.

**Objawy błędu:** Halo na ciemnym tle, prostokąt zamiast alfy, aliasing przy skali, stan zależny od kolejności.

**Ogląd temporalny:** 10 s odtworzenie na jasnym/ciemnym tle; 0,299,30,0; 16:9 / 9:16.

## A03 — Quaternius Universal Animation Library 2

[Strona kanoniczna](https://quaternius.itch.io/universal-animation-library-2) · Autor: Quaternius; współautor animacji Gonzalo Furnier · Klasa C · **NEW** · Przegląd: 2026-11-11.

Dowody: DOCUMENTED; AUTHOR_TEST (tylko deklaracja autora dot. Godot/Unity/Unreal, logi nieodczytane); NOT_RUN; DERIVED.

Źródła materialnych twierdzeń: [AS18](https://quaternius.itch.io/universal-animation-library-2), [AS19](https://quaternius.com/packs/universalanimationlibrary2.html), [AS34](https://creativecommons.org/publicdomain/zero/1.0/).

**Pin / wersja.** Changelog v2.2 (2026-09-28); strona updated 2026-11-08; Standard archive hash Unknown

**Problem produkcyjny.** Gotowe ruchy humanoida, w tym root motion, zamiast ręcznego blokowania każdej akcji postaci.

**Różnica względem baseline.** Nowa biblioteka danych ruchu, nie kolejny pełny silnik 3D. Baseline ma ogólne Blender/Three/character workflows, ale nie tę paczkę.

**Konkretny moduł / asset.** Standard.zip 17 MB jako pierwszy kandydat; Source.zip 50 MB z .blend osobno płatny. Konkretne clip names/inventory Standard Unknown.

**Wejścia, wyjścia i edycja.** Autor wymienia FBX/GLB oraz .blend w Source; root-motion i bez root-motion. Retarget wymaga zgodności kości/osi i skali. Nie przenosić liczby 130+ całej biblioteki na darmowy wariant.

**Runtime i zasoby.** DERIVED: Blender z importerem glTF/FBX lub Three.js GLTFLoader/AnimationMixer po kwalifikacji; dokładny Blender/Three.js pin Unknown. CPU/GPU/RAM zależą od modelu/sceny; render offline po legalnym pozyskaniu.

**Droga eksportu.** DERIVED: ustalony czas klipu → bake transformów → PNG/EXR z Blendera → MP4/WebM; GLB po reeksporcie tylko z testem zachowania kości i interpolacji.

**Koszt, konto i sieć.** Standard name-your-price; Source $14.99 lub więcej. Zakup/konto/płatności niepróbowane. .blend nie jest darmowym zasobem tylko dlatego, że pack ma CC0.

**Utrzymanie i ograniczenia.** v2.0 dodał root motion i poprawki kroków/skali; v2.1 nazwy Godot; v2.2 poprawił końce Sword_Light i nazewnictwo recovery. Autorskie deklaracje testów silników nie potwierdzają Blender/Three.

**Właściciel docelowy.** Open Assets: edycja/prawa/pin; Studio character/Blender owner: retarget i bake; FrameMotion: ewentualny clip-time contract.

**Forma integracji.** ON_DEMAND_ASSET

**Rekomendacja.** P1 dla motion z postacią; najpierw darmowy Standard i inventory. Płatna .blend edycja nie mieści się w tym researchu.

### Prawa

| Zakres | Ustalenie |
|---|---|
| Kod | Kod shaderów/engine projects nieinspekcjonowany; nie zakładać CC0 z licencji ruchów |
| Assety | CC0 wg stron autora; zakres plików konkretnego pobrania do odczytu |
| Fonty | Unknown; no font files inspected |
| Modele / rig | Humanoid rig/model deklarowany CC0; inventory i ewentualne dodatkowe elementy Unknown |
| Przykłady / preview | Preview film/obrazy i ewentualne rekwizyty sprawdzać osobno |
| Wyrenderowany film | Tak dla objętych CC0 animacji/modeli |
| Redystrybucja źródeł | Tak dla objętych CC0 plików, po potwierdzeniu licencji wewnątrz wariantu |

### Metadane assetu

| Pole | Ustalenie |
|---|---|
| Rozdzielczość | N/A dla danych kości; render rozdzielczość do ustalenia |
| Długość | Unknown |
| FPS | Unknown |
| Pętla / seam | Unknown per clip; nie wszystkie akcje zapętlone |
| Alfa | N/A źródło 3D; alfa zależy od renderu |
| Warstwy | Rig/animacje; liczba kości, ścieżek, tracks Unknown |
| Powiązane pliki | Wariant root motion/in-place; FBX/GLB; Source.blend płatny |
| Pochodzenie | Quaternius; wymieniony współtwórca Gonzalo Furnier; strona deklaruje no generative AI |

### Plan próby — NOT_RUN

**Fixture:** Jedna locomotion root-motion + in-place, jeśli są w Standard; neutralny humanoid; 10 s; osobno hit→recovery jeśli oba dostępne.

**Oczekiwany wynik:** Jednostki/kości prawidłowe; ruch root stosowany raz; pose w t=0,t=1,t=0 identyczne; join bez pop.

**Objawy błędu:** Podwójny root translation, foot sliding, 100× scale, niedopasowane recovery, missing clip.

**Ogląd temporalny:** Przód/bok stóp i trajektorii przez pełny klip oraz 2 cykle; 16:9 / 9:16; etykieta PL z niezależnym fontem.

## A04 — JangaFX Tornado Looping — VDB

[Strona kanoniczna](https://jangafx.com/software/embergen/download/free-vdb-animations) · Autor: JangaFX · Klasa C · **NEW** · Przegląd: 2026-11-11.

Dowody: DOCUMENTED; NOT_RUN; DERIVED.

Źródła materialnych twierdzeń: [AS20](https://jangafx.com/software/embergen/download/free-vdb-animations), [AS34](https://creativecommons.org/publicdomain/zero/1.0/).

**Pin / wersja.** Tornado Looping, snapshot 2026-11-11; brak tagu i hasha

**Problem produkcyjny.** Wolumetryczny efekt z własnym oświetleniem/kamerą bez symulowania tornado od zera.

**Różnica względem baseline.** Prebaked dane VDB to inna możliwość niż 2D sprite/overlay; brak tego konkretnego cache w baseline.

**Konkretny moduł / asset.** Tornado Looping VDB sequence 200 frames; EmberGen preset wg autora. Nazwy plików i gridów Unknown.

**Wejścia, wyjścia i edycja.** VDB volume sequence; preset EmberGen. Nie jest 2D footage ani renderowana alfa.

**Runtime i zasoby.** Autor wskazuje Blender/Houdini/Octane/Arnold jako konsumentów VDB. DERIVED: import tylko w zakwalifikowanym lokalnym DCC; koszt pamięci/CPU/GPU Unknown, 1.7 GB download nie określa RAM. Bez EmberGen do użycia samego cache; preset wymaga osobnej aplikacji.

**Droga eksportu.** DERIVED: frame-index volume → DCC render EXR/PNG RGBA → FFmpeg MP4/WebM; bez natywnego bezpośredniego VDB support w Remotion/HTML/Pixi.

**Koszt, konto i sieć.** VDB bezpłatny CC0; link MediaFire nieotwarty; koszty DCC/renderu zależne od wyboru. EmberGen authoring osobna licencja, nieuruchomiony.

**Utrzymanie i ograniczenia.** Paczka bez wersji/changelogu; author claims looping. Nie ustalono gridów, bounds, origin, FPS ani seam.

**Właściciel docelowy.** Open Assets: rejestr praw i duży transfer; Studio Blender: shader/camera/render. Nie dodawać VDB runtime do przeglądarki dla jednego assetu.

**Forma integracji.** ON_DEMAND_ASSET

**Rekomendacja.** P2 on-demand dla konkretnej sceny; koszt 1.7 GB i renderu nie uzasadnia bundlowania.

### Prawa

| Zakres | Ustalenie |
|---|---|
| Kod | EmberGen binary nieobjęty CC0 assetu |
| Assety | CC0 dla free VDB simulations |
| Fonty | Unknown; no font files inspected |
| Modele / rig | Wolumen CC0, nie mesh; preset rights Unknown oddzielnie |
| Przykłady / preview | Film demonstracyjny niepozyskany |
| Wyrenderowany film | Tak dla objętej symulacji |
| Redystrybucja źródeł | Tak dla VDB objętego CC0; zakres included preset do odczytu |

### Metadane assetu

| Pole | Ustalenie |
|---|---|
| Rozdzielczość | Unknown voxel/grid dimensions |
| Długość | 200 frames; sekundy Unknown bez fps |
| FPS | Unknown |
| Pętla / seam | Looping wg nazwy autora; wizualna ciągłość NOT_RUN |
| Alfa | N/A w VDB; transmitancja/alpha powstaje w renderze |
| Warstwy | Grid names/channels Unknown |
| Powiązane pliki | EmberGen preset declared; archive 1.7 GB |
| Pochodzenie | JangaFX; symulacja z EmberGen wg autora |

### Plan próby — NOT_RUN

**Fixture:** Po oddzielnej zgodzie transferu inspect 200 VDB; render klatek 0, 199, 50, 0; jeden shader i kamera; 2 pętle.

**Oczekiwany wynik:** Każdy indeks odczytany; powtarzalny render; grid/bounds stabilne; jawnie wybrany fps.

**Objawy błędu:** Missing grid, czarne volume, skoki bounds, seam, flicker denoise, RAM peak.

**Ogląd temporalny:** Pełne 400 frames na neutralnym tle i alpha checker; nie oceniać loop z samej pierwszej/ostatniej klatki.

## A05 — Rive Vehicle Loader

[Strona kanoniczna](https://rive.app/community/files/4154-8679-vehicle-loader/) · Autor: pedroalpera · Klasa C · **NEW** · Przegląd: 2026-11-11.

Dowody: DOCUMENTED; NOT_RUN; DERIVED.

Źródła materialnych twierdzeń: [AS21](https://rive.app/community/files/4154-8679-vehicle-loader/), [AS22](https://creativecommons.org/licenses/by/4.0/), [AS23](https://rive.app/docs/runtimes/web/low-level-api-usage).

**Pin / wersja.** Marketplace item 4154-8679 ; 2023-01-20; .riv hash/revision Unknown

**Problem produkcyjny.** Przykład wejścia, trwania i wyjścia loadera produktu z jednym projektem Rive.

**Różnica względem baseline.** Konkretna licencjonowana scena/state machine; nie dowodzi nowej deterministycznej integracji Rive w FrameMotion.

**Konkretny moduł / asset.** Vehicle Loader .riv — download/remix widoczne; plik niepobrany. Dokładne timeline/input names Unknown.

**Wejścia, wyjścia i edycja.** .riv do runtime; scene/state machine wg opisu. Edycja przez Rive; ewentualne zewnętrzne obrazy/fonty Unknown.

**Runtime i zasoby.** Rive Canvas/WebGL advanced + zgodna wersja WASM do własnej pętli. Frame-index seek niepotwierdzony dla pliku; reset+replay stałym dt jest proponowanym adapterem. Headless/offline/CPU/GPU/RAM do próby; self-host WASM opisana możliwość.

**Droga eksportu.** DERIVED: scripted inputs → advanced runtime canvas → sekwencja PNG → MP4; alfa i zgodność Canvas/WebGL wymagają testu. Nie traktować klikanej maszyny stanów jako gotowego renderu.

**Koszt, konto i sieć.** Strona oferuje download/remix, bez ceny na odczytanej stronie; wymóg konta do faktycznego pobrania/edycji Unknown. Runtime/editor koszty oddzielne; żadnego konta nie utworzono.

**Utrzymanie i ograniczenia.** Data 2023-01-20; brak file revision. Low-level API advance/apply nie zapewnia bezstanowego seek; mieszanie i eventy wymagają reset/replay.

**Właściciel docelowy.** Open Assets: licencja itemu; Studio motion: pilot Rive; FrameMotion adapter tylko hipoteza.

**Forma integracji.** ON_DEMAND_ASSET

**Rekomendacja.** P2 fixture interakcji→timeline. Wstrzymać użycie do filmu do kontroli feature support, seek i fonts.

### Prawa

| Zakres | Ustalenie |
|---|---|
| Kod | Rive runtime ma osobną licencję; nieaudytowana w tej karcie |
| Assety | Konkretny item CC BY 4.0 |
| Fonty | Unknown; sprawdzić embedded/out-of-band fonty |
| Modele / rig | N/A |
| Przykłady / preview | CC BY tego itemu nie dotyczy innych galerii Rive |
| Wyrenderowany film | Tak z wymaganym credit, linkiem do licencji i informacją o zmianach |
| Redystrybucja źródeł | Tak na warunkach CC BY 4.0; zachować attribution i nie dodawać sprzecznych ograniczeń |

### Metadane assetu

| Pole | Ustalenie |
|---|---|
| Rozdzielczość | Unknown |
| Długość | Unknown |
| FPS | Unknown |
| Pętla / seam | Idle loader wg opisu; seam Unknown |
| Alfa | Unknown |
| Warstwy | State Machine + timelines wg opisu; konkretne warstwy Unknown |
| Powiązane pliki | Rive editor/remix; zewnętrzne fonty/obrazy Unknown |
| Pochodzenie | pedroalpera, item-specific community upload |

### Plan próby — NOT_RUN

**Fixture:** Vehicle Loader z listą wejść/artboard po inspect; loading-end w klatce 90; powtarzane 0, 120, 30, 0 przez reset/replay.

**Oczekiwany wynik:** Ten sam obraz przy tym samym scenariuszu; wejście/wyjście w zadanej klatce; runtime + WASM przypięte razem.

**Objawy błędu:** Zależność od rAF, różny start, wycieki WASM, błędny stan po rewind, missing asset.

**Ogląd temporalny:** Cała sekwencja start→idle→end w docelowym fps; Canvas/WebGL osobno; alpha checker; 16:9 / 9:16.

## A06 — DAEDAL Bokeh & Particles Pack

[Strona kanoniczna](https://daedal.art/resources/bokeh-and-particles-pack/) · Autor: DAEDAL / luciansofronie · Klasa C · **NEW** · Przegląd: 2026-11-11.

Dowody: DOCUMENTED; NOT_RUN; DERIVED.

Źródła materialnych twierdzeń: [AS24](https://daedal.art/resources/bokeh-and-particles-pack/), [AS25](https://daedal.art/terms/), [AS26](https://api.github.com/repos/luciansofronie/daedal-downloads/releases/tags/packs-v1), [AS34](https://creativecommons.org/publicdomain/zero/1.0/).

**Pin / wersja.** packs-v1; asset 681890709; SHA256 dcec36fe3211ac8cc0e0326e93b078242f8bc9e9fe3ee2aaa0256cb80f6dde54 (metadata upstream, NIE własny hash); 35 525 100 bytes

**Problem produkcyjny.** Gotowe pętle atmosfery/bokeh jako plik wejściowy do montażu lub kompozycji motion.

**Różnica względem baseline.** Konkretny overlay pack z jawnym frame rate i licencją; uzupełnia engine/PixelFX, nie nowy system montażu.

**Konkretny moduł / asset.** DAEDAL_Bokeh_and_Particles_Pack.zip release packs-v1; wybrany przyszły fixture Floating Dust/Warm; inventory ZIP nieodczytane.

**Wejścia, wyjścia i edycja.** MP4 na czarnym tle; 4K 24 fps. Screen/Add to compositing mode, NIE wbudowany kanał alfa. Deklarowane 12 plików nie oznacza 12 klipów; README/LICENSE mogą wejść do tej liczby.

**Runtime i zasoby.** DERIVED: decoder MP4 + compositor obsługujący Screen/Add; FFmpeg albo istniejący FrameCut/HyperFrames/Remotion pipeline po próbie. Brak własnego executable/installera; offline po pobraniu. Codec/pixel format/RAM Unknown.

**Droga eksportu.** DERIVED: decode wg PTS → Screen/Add nad sceną → MP4; pochodna alfa wymaga osobnej matematyki/akceptacji, nie deklarować jej z czarnego tła. WebM alpha/sekwencja PNG tylko po kontrolowanej konwersji.

**Koszt, konto i sieć.** Free, brak konta/email wg strony; GitHub Release. 35.5 MB archiwum przekracza domyślny cap 32 MiB Open Assets: nie kwalifikuje się automatycznie do bieżącego downloadera bez osobnej decyzji/obsługi limitu.

**Utrzymanie i ograniczenia.** Release 2026-10-27, immutable=false; hash metadata pozwala przyszły comparison, nie potwierdza bieżącej zawartości. Brak własnego decode i visual review.

**Właściciel docelowy.** Open Assets dla source record; FrameCut montaż overlay; Studio/FrameMotion tylko kontrola czasu i kompozycji.

**Forma integracji.** ON_DEMAND_ASSET

**Rekomendacja.** P1 pierwszy pilot po uwzględnieniu limitu transferu; mniejszy koszt integracji niż nowy generator. Ocena jakości i seam otwarta.

### Prawa

| Zakres | Ustalenie |
|---|---|
| Kod | Nie pozyskujemy DAEDAL app/panel; ich terms nie są licencją tego packa |
| Assety | CC0 film assets, author says procedural/no third-party footage in downloads |
| Fonty | Unknown; no font files inspected |
| Modele / rig | N/A |
| Przykłady / preview | Preview Luca Bravo/Unsplash wyłączone z CC0 i pobrania; nie bundlować zdjęcia |
| Wyrenderowany film | Dozwolone komercyjne użycie objętych assetów |
| Redystrybucja źródeł | CC0 dozwala źródłową redystrybucję objętych assetów; pozostawić proweniencję |

### Metadane assetu

| Pole | Ustalenie |
|---|---|
| Rozdzielczość | 3840×2160 wg autora |
| Długość | Bokeh 12 s / particles 10 s wg strony |
| FPS | 24 wg strony |
| Pętla / seam | Seamless wg autora; NOT_RUN |
| Alfa | On pure black; wbudowana alfa NIE zadeklarowana, nie traktować jako alpha |
| Warstwy | Flattened MP4; bez udokumentowanych warstw edycyjnych |
| Powiązane pliki | 12 files wg strony; README/LICENSE deklarowane; ZIP 35 525 100 bytes; preview photo osobno |
| Pochodzenie | Proceduralnie wygenerowane dla DAEDAL wg terms; preview Luca Bravo / Unsplash osobno |

### Plan próby — NOT_RUN

**Fixture:** Jedna 10 s i jedna 12 s pętla; plik/hash/codec/PTS; 3 cykle 24 fps; ciemne i jasne tło; 16:9 / 9:16.

**Oczekiwany wynik:** 240/288 frames tylko jeśli realne metadata to potwierdzą; ciągłość PTS; identyczny frame w różnej kolejności; poprawny Screen.

**Objawy błędu:** Banding, raised blacks, macroblocks, brightness seam, niewłaściwa gamma blend, obcięte ważne detale po crop.

**Ogląd temporalny:** Pełny loop × 3 w docelowym tempie i 0.25×; histogram ostatnich/pierwszych 12 frames; waveform/alpha dla wynikowego formatu.

## A07 — Poly Haven Studio Small 09 HDRI

[Strona kanoniczna](https://polyhaven.com/a/studio_small_09) · Autor: Sergej Majboroda / Poly Haven · Klasa C · **ALREADY_COVERED** · Przegląd: 2026-11-11.

Dowody: DOCUMENTED; NOT_RUN; DERIVED.

Źródła materialnych twierdzeń: [AS27](https://polyhaven.com/a/studio_small_09), [AS28](https://polyhaven.com/license), [AS34](https://creativecommons.org/publicdomain/zero/1.0/).

**Pin / wersja.** studio_small_09; snapshot 2026-11-11; file hash Unknown

**Problem produkcyjny.** Powtarzalne studyjne oświetlenie dla animacji produktu 3D.

**Różnica względem baseline.** Provider HDRI już istnieje w Open Assets; to fixture porównawczy, nie nowa integracja.

**Konkretny moduł / asset.** studio_small_09, docelowo 4K EXR 18.54 MB według strony; plik niepobrany.

**Wejścia, wyjścia i edycja.** HDR/EXR environment, warianty 1K–16K; tonemapped JPG i color chart to osobne pliki. Nie mylić JPG z HDR.

**Runtime i zasoby.** DERIVED: Blender lub Three.js environment map po doborze loadera; offline po zapisaniu pliku; pamięć CPU/GPU zależy od dekodu, Unknown.

**Droga eksportu.** DERIVED: oświetlenie sceny → PNG/EXR → MP4; statyczny HDRI sam nie daje klipu.

**Koszt, konto i sieć.** Bezpłatny asset; konto i klucz nie są wskazane na stronie. Warunki usług/API osobno. Pobrania nie próbowano.

**Utrzymanie i ograniczenia.** Stały asset ID, brak wersji i hasha. Assets provided by Poly Haven.

**Właściciel docelowy.** Istniejący Open Assets → Studio Blender/3D.

**Forma integracji.** ON_DEMAND_ASSET

**Rekomendacja.** Bez nowego wpisu Toolbox. P1 tylko jako fixture oświetlenia istniejącej drogi.

### Prawa

| Zakres | Ustalenie |
|---|---|
| Kod | Not included / Unknown if added separately |
| Assety | CC0 HDRI |
| Fonty | Unknown; no font files inspected |
| Modele / rig | N/A |
| Przykłady / preview | Poly Haven wyklucza example/user renders i zawartość witryny z ogólnego CC0 assetów |
| Wyrenderowany film | Tak |
| Redystrybucja źródeł | Tak, CC0 |

### Metadane assetu

| Pole | Ustalenie |
|---|---|
| Rozdzielczość | Warianty 1K–16K; dokładne w×h Unknown |
| Długość | N/A — statyczny |
| FPS | N/A |
| Pętla / seam | Unknown; sprawdzić seam środowiska |
| Alfa | N/A jako oświetlenie; transparent film osobno |
| Warstwy | N/A |
| Powiązane pliki | HDR/EXR, 8K tonemapped JPG, color chart |
| Pochodzenie | Sergej Majboroda / Poly Haven |

### Plan próby — NOT_RUN

**Fixture:** 4K EXR; chromowana i matowa kula; 3-sekundowy orbit kamery.

**Oczekiwany wynik:** Liniowy HDR, stała ekspozycja i obrót środowiska; powtarzalny render.

**Objawy błędu:** Clipping, błędna przestrzeń barw, seam środowiska.

**Ogląd temporalny:** Pełny orbit, diffuse/specular osobno; 16:9 i 9:16.

## A08 — ambientCG Metal046B

[Strona kanoniczna](https://ambientcg.com/view?id=Metal046B) · Autor: ambientCG · Klasa C · **ALREADY_COVERED** · Przegląd: 2026-11-11.

Dowody: DOCUMENTED; NOT_RUN; DERIVED.

Źródła materialnych twierdzeń: [AS29](https://ambientcg.com/view?id=Metal046B), [AS30](https://docs.ambientcg.com/license/), [AS34](https://creativecommons.org/publicdomain/zero/1.0/).

**Pin / wersja.** Metal046B; wydany 2022-11-28; hash archiwum Unknown

**Problem produkcyjny.** PBR powierzchnia metalu do typografii 3D i animacji produktu.

**Różnica względem baseline.** Materiały ambientCG należą już do Open Assets; to konkretny fixture, nie nowy provider.

**Konkretny moduł / asset.** Metal046B PBR Maps; docelowo 2K PNG 56 MB; 1K PNG 15 MB jako mniejszy pilot. Lista map Unknown.

**Wejścia, wyjścia i edycja.** Mapy JPG/PNG w wariantach 1K–8K, opisane jako USDZ-compatible. Nazwy i konwencja normal map nieodczytane.

**Runtime i zasoby.** DERIVED: Blender lub Three.js PBR material; offline po pobraniu; RAM/GPU Unknown. Ustalić non-color dla danych, zamiast przypisać sRGB wszystkim mapom.

**Droga eksportu.** DERIVED: tekstura → materiał sceny → PNG/EXR → MP4. Sam asset nie animuje.

**Koszt, konto i sieć.** CC0, bezpłatny; bez pobrania w tym researchu. Wariant 56 MB przekracza domyślne 32 MiB; pilot 15 MB może wejść w limit po weryfikacji metadanych.

**Utrzymanie i ograniczenia.** Release 2022-11-28; procedural według strony; brak własnego importu lub testu seam.

**Właściciel docelowy.** Istniejący Open Assets → Studio 3D.

**Forma integracji.** ON_DEMAND_ASSET

**Rekomendacja.** P1 jako kontrola PBR, bez nowego wpisu. Sprawdzić listę map przed renderem.

### Prawa

| Zakres | Ustalenie |
|---|---|
| Kod | Not included / Unknown if added separately |
| Assety | CC0 asset files i material preview renders wg ambientCG terms |
| Fonty | Unknown; no font files inspected |
| Modele / rig | N/A |
| Przykłady / preview | ambientCG jawnie obejmuje material preview renders CC0; nie uogólniać tego na Poly Haven |
| Wyrenderowany film | Tak |
| Redystrybucja źródeł | Tak |

### Metadane assetu

| Pole | Ustalenie |
|---|---|
| Rozdzielczość | Warianty 1K–8K; dokładne w×h Unknown |
| Długość | N/A — statyczny |
| FPS | N/A |
| Pętla / seam | Link tiling preview istnieje; seam Unknown bez oglądu |
| Alfa | Unknown |
| Warstwy | PBR map set; dokładne kanały Unknown |
| Powiązane pliki | ZIP JPG/PNG 1K–8K; 1K PNG 15 MB, 2K PNG 56 MB |
| Pochodzenie | ambientCG; procedural według strony |

### Plan próby — NOT_RUN

**Fixture:** Pack 1K PNG; litery „Łódź” z oddzielnym własnym fontem; światło pod małym kątem i UV repeat 2×2.

**Oczekiwany wynik:** Mapy zgodne rozdzielczością; orientacja normal ustalona; brak widocznej krawędzi UV.

**Objawy błędu:** Odwrócone normale, roughness w sRGB, nieciągły pattern, mora.

**Ogląd temporalny:** Orbit i ruch światła przez 4 sekundy; 16:9 i 9:16; ogląd w skali 100%.

## A09 — ActionVFX Free Dust Waves — reference only

[Strona kanoniczna](https://www.actionvfx.com/collections/free-dust-wave-stock-footage) · Autor: ActionVFX · Klasa C · **BASELINE_UNKNOWN** · Przegląd: 2026-11-11.

Dowody: NOT_RUN; Unknown (prawa i pliki); DOCUMENTED (tylko dostęp 403).

Źródła materialnych twierdzeń: [AS31](https://www.actionvfx.com/collections/free-dust-wave-stock-footage), [AS32](https://www.actionvfx.com/terms), [AS33](https://www.actionvfx.com/blog/explosions-vol-2-aerial-explosions-and-dust-wave-vol-2-now-available).

**Pin / wersja.** Unknown; bieżąca kolekcja HTTP 403

**Problem produkcyjny.** Lead do praktycznych dust-wave overlays; bez potwierdzonych praw nie stanowi assetu produkcyjnego.

**Różnica względem baseline.** Nie oceniono nowej możliwości, gdy niedostępne są bieżąca kolekcja i warunki. Nie wliczać do rankingu zaakceptowanych assetów.

**Konkretny moduł / asset.** Free Dust Waves collection — brak dostępu do strony/plików; konkretny asset Unknown.

**Wejścia, wyjścia i edycja.** Unknown; specyfikacje płatnego Vol. 2 nie dotyczą bezpłatnego packa.

**Runtime i zasoby.** Unknown; hipotetyczny decoder/compositor nie dowodzi faktycznego formatu.

**Droga eksportu.** Unknown; nie deklarować alpha, MP4, EXR lub kodeka bez źródła.

**Koszt, konto i sieć.** Unknown; nazwa Free nie ustala bieżących wymagań konta, subskrypcji ani praw.

**Utrzymanie i ograniczenia.** Kolekcja 403, terms inaccessible, artykuł autora 403. Search snapshot służy wyłącznie odkrywaniu, nie ustaleniu praw.

**Właściciel docelowy.** Open Assets: weryfikacja przy dostępnych warunkach; Studio: reference only.

**Forma integracji.** REJECT

**Rekomendacja.** REFERENCE_ONLY. Nie pobierać ani redystrybuować we wtyczce. Zgłosić lukę gotowego overlaya z alfą.

### Prawa

| Zakres | Ustalenie |
|---|---|
| Kod | Unknown |
| Assety | Unknown — bieżące warunki nieodczytane |
| Fonty | Unknown |
| Modele / rig | Unknown |
| Przykłady / preview | REFERENCE_ONLY, bez pobrań lub użycia |
| Wyrenderowany film | Unverified; wstrzymane |
| Redystrybucja źródeł | Unverified; wstrzymane |

### Metadane assetu

| Pole | Ustalenie |
|---|---|
| Rozdzielczość | Unknown |
| Długość | Unknown |
| FPS | Unknown |
| Pętla / seam | Unknown |
| Alfa | Unknown |
| Warstwy | Unknown |
| Powiązane pliki | Unknown |
| Pochodzenie | ActionVFX — lead; konkretne pliki i prawa Unknown |

### Plan próby — NOT_RUN

**Fixture:** Najpierw aktualna licencja, konkretny item, format i droga pobrania; później import i kontrola alfy.

**Oczekiwany wynik:** Do ustalenia po uzyskaniu danych; teraz brak dowodów.

**Objawy błędu:** Założenie free=CC0 albo paid Vol.2 specs=free pack.

**Ogląd temporalny:** NOT_RUN; brak materiału do oglądu.

## Ranking assetów do osobnego pilota

| Kolejność | Pozycja | Dlaczego / warunek |
|---|---|
| 1 | A06 DAEDAL | Jasne parametry klipu i CC0; trzeba rozwiązać limit transferu i potwierdzić seam/kolor. Black overlay nie ma potwierdzonej alfy. |
| 2 | A02 Kenney | Małe statyczne wejścia i prosty kontrakt czasu po stronie emittera; format i alfa do decode. |
| 3 | A01 Meteocons | Spójny zestaw wektorowy i inspected źródła; drift wersji oraz issue pętli obniżają gotowość. |
| 4 | A03 Quaternius | Duża oszczędność pracy nad ruchem humanoida; retarget i warianty darmowe/płatne wymagają inventory. |
| 5 | A04 JangaFX | Nowy rodzaj gotowych danych wolumetrycznych; duży transfer i koszt renderowania. |
| 6 | A05 Rive Vehicle Loader | Dobry trudny fixture interakcji → czas; runtime, plik i arbitrary seek niepotwierdzone. |

A07/A08 pozostają fixture istniejących providerów. A09 nie jest rekomendowanym assetem. Ranking jest DERIVED z kosztu integracji, nowych zastosowań, praw i kontroli czasu; nie jest rankingiem jakości wizualnej.

## Luki

Nie potwierdzono gotowego overlaya wideo z natywnym kanałem alfa. Nie uzyskano inventory plików binarnych, parametrów klipów Rive/Quaternius ani wymiarów VDB. Są to jawne warunki przyszłych prób, nie powód do dopisywania słabszych pozycji.
