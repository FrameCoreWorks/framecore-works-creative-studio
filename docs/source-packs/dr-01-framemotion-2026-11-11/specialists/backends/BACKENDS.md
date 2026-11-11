# BACKENDS — motion profesjonalny → kod

Data badania: 2026-11-11. Część DR-01, opracowanie po polsku. Wszystkie benchmarki i fragmenty kodu poniżej: **NOT_RUN**. To wybór metod i proponowane testy, nie deklaracja zainstalowania ani wdrożenia. SOURCED oznacza dokumentację/kod odczytany; DERIVED — autorską adaptację do FrameMotion. Numery B odnoszą się do [rejestru źródeł](sources.json). Stan Studio i granice istniejących kontraktów opisuje [STUDIO-AUDIT](STUDIO-AUDIT.md).

## 1. Wybór po wymaganym obrazie

**DERIVED:** wybór zaczyna się od najtrudniejszej wymaganej cechy: dokładnego tekstu, zmiennej geometrii, świateł, stanu fizyki albo wiernego compositingu. Liczba bibliotek nie jest miarą jakości. Jeśli istniejąca scena spełnia brief, zachować jej backend. Tabela to rekomendacja warunkowa; nie ranking szybkości.

| Backend | Najlepsze zadanie dla FrameMotion | Co agent ma przygotować | Kluczowy koszt i ograniczenie | Warunek wyboru |
|---|---|---|---|---|
| HTML/CSS/SVG | Exact copy, logo z wektora, UI, diagram, odsłanianie typografii | DOM/SVG o stałym layoucie, fonty lokalne, jawny czas | Layout/shaping i rasteryzacja zależą od przeglądarki; CSS animation na wall clock utrudnia eksport | Geometria i efekt mieszczą się w wybranym browserze |
| GSAP | Złożone sekwencje transformacji, overlap, stagger, krzywe | Jedna zatrzymana timeline; wartości początkowe; etykiety tylko dla autora | Seek domyślnie pomija callbacki; callback-mutacja nie może być jedyną definicją obrazu | Zachowuje obecny renderer, zmienia organizację animacji |
| HyperFrames | HTML/SVG/Canvas → kontrolowany eksport sceny | Seekable composition, readiness, lokalne media i jawny renderer | Chrome/FFmpeg/GPU, wersje i tryb capture mają znaczenie; distributed FPS jest węższy niż lokalny | Potrzebna gotowa warstwa przechwytywania i eksportu, host ją faktycznie ma |
| Remotion / React / TypeScript | Komponenty parametryczne, wiele wariantów danych, obecny projekt React | Pure frame state, props, kompozycja, preload; źródła edytowalne | Browser + render worker memory; licencja warunkowa; hook czasu bywa lokalny | Powtarzalne sceny i możliwość użycia istniejącej ścieżki Remotion |
| Canvas 2D | Proceduralna grafika, własne rysowanie, obrazy/SVG w bitmapie | Pełne czyszczenie i odtworzenie klatki, retained model poza Canvas | Brak automatycznego DOM layout; raster, tekst i alfa wymagają jawnych testów | Zysk z kontroli rysowania przewyższa koszt layout engine |
| PixiJS | Dużo sprite’ów, masek i obiektów 2D, kontrolowane particles | Absolutny stan obiektów, ręczne renderowanie, atlas tekstur | GPU fill-rate, maski/filtry, tekstury; ticker delta nie jest dowolnym seek | Wymagane obciążenie uzasadnia scene graph GPU |
| Three.js / WebGL / shaders | Prawdziwa kamera, geometria, światło, materiały, parallax | Scena 3D, assets, lens/camera, jawne uniform time, pipeline koloru | GPU/driver, pamięć tekstur, antialiasing; shader z feedbackiem ma historię | Brief wymaga geometrii/przestrzeni, a nie tylko pozornego przesunięcia plansz |
| Motion Canvas | Wektorowy explainer z VO, relacje pojęć, sekwencje dydaktyczne | Generatory, signals, time events, deterministyczne zasoby | Seek wstecz może replayować generator; nie zastępuje master NLE | Lokalny specialist clip, którego dramaturgia korzysta z generatorów |
| Blender Python | Model produktu, kamera, cienie, fizyka, passes do compositingu | .blend i skrypt, fonty/tekstury, bake, ustawienia renderu i koloru | CPU/GPU i czas renderu; symulacja wymaga historii/cache; bridge renderowy | Prawdziwe 3D lub symulacja usprawiedliwia etap offline |
| FFmpeg | Konform, mux, składanie gotowych warstw, kodowanie, pomiary | Jawne input clocks, filter graph, kolor/alpha, codec/pix_fmt | To nie edytor sceny AE; inny filtr o podobnej nazwie nie zapewnia tej samej semantyki | Ostatni etap lub prosta operacja na już wyrenderowanym materiale |

Podstawa SOURCED: stateless timing web [B26](https://www.w3.org/TR/web-animations-1/#stateless); seek GSAP [B24](https://gsap.com/docs/v3/GSAP/Timeline/seek()/); HyperFrames [B18](https://hyperframes.app/docs/2-concepts/4-determinism); lokalny czas Remotion [B30](https://www.remotion.dev/docs/use-current-frame); Pixi ticker [B35](https://github.com/pixijs/pixijs/blob/eb96c76fa27c948c748ff0bb79fc7a29329cd5e9/src/ticker/Ticker.ts); Three mixer [B37](https://github.com/mrdoob/three.js/blob/b5a9e5730f6122498e187da8f7cdedd4358f5aa0/src/animation/AnimationMixer.js); generator flow [B42](https://motioncanvas.io/docs/flow/); Blender CLI [B44](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/advanced/command_line/render.rst); FFmpeg [B45](https://github.com/FFmpeg/FFmpeg/blob/b9a9bf7a3a74c2c62bac4c766666d1ca93b2c6ba/doc/filters.texi). Są to dowody mechanizmu, nie własny benchmark.

## 2. Jedna klatka oznacza jeden stan

**DERIVED:** specyfikacja twórcza mówi, *co i dlaczego* ma się zdarzyć: marka, intencja, exact copy, ważność elementu, moment akcentu, dozwolone zmiany. Adapter mówi, *jak* uzyskać ten stan: matryce, layout, shader, camera, bufor i codec. Planner nie powinien wpisywać fragmentów JavaScript w pola kontraktu używane jako dane.

Istniejący motion-score zachowuje źródło prawdy dla czasu i zgody. Proponowany adapterowy scene graph może mieć węzły group/shape/path/text/image/video/camera/light/matte/effect, ale pozostaje prywatnym modelem wykonania sceny. Nie jest kolejnym master timeline. Każdy węzeł ma stabilne ID, parent, local transform, visibility interval, wskazania assetów i parametry. Osobny dependency graph obejmuje także font shaping → layout → maska → composite → encode; jego krawędzie nie są tym samym co parent-child.

**DERIVED:** walidator grafu odrzuca cykl zależności, odniesienie do nieistniejącej maski, self-matte, nieobsługiwany efekt i niejawny układ współrzędnych. Nazwy przestrzeni, np. local px / composition px / world m / normalized UV, należą do schematu adaptera. Nie zgadywać, czy [0.5,0.5] oznacza pół piksela czy środek kadru. Przeliczenie parent transform uwzględnia anchor przed skalą/obrotem; test markerów narożnych wykrywa odwrócony znak lub kolejność macierzy.

### Czas dokładny na granicach

**SOURCED:** Studio ma rational fps num/den oraz secondsAtFrame; FrameCut używa Fraction i zachowuje sub-PTS remainder przy trim. [B06](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/hyperframes-workflow/assets/motion-quality/score.mjs), [B15](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/opencut-video-studio/assets/framecut/fc_time.py).

**DERIVED:** dla numeru klatki f, t = f × fps_den / fps_num. Wewnątrz sceny f_local = f_master − global_start_frame; zakres pozostaje [in,out). Ostatnia klatka odcinka długości N to N−1; czas jego końca to N × den/num. Nie dodawać wielokrotnie zaokrąglonego dt.

Przykład syntetyczny: 300 klatek przy 30000/1001 to dokładnie 10.01 s. Granicę audio przy 48 000 Hz wyznaczyć jeden raz z rational czasu: round_boundary(300 × 1001 × 48000 / 30000) = 480480 próbek. Marker widocznego uderzenia należy odnosić do klatki kulminacji, nie automatycznie do startu tweenu. Proponowana synchronizacja może wymagać przesunięcia wejścia wcześniej, aby ruch osiągnął cel na cue.

**SOURCED:** HyperFrames current code zachowuje num/den, ale jego distributed-FPS przyjmuje tylko 24/25/30/60; fractional działa lokalnie. Remotion validateFps przyjmuje number, nie obiekt rational. [B19](https://github.com/heygen-com/hyperframes/blob/3ad7611f9fd36c1cef589c59b116ad7043c3b041/packages/core/src/fps.ts), [B20](https://github.com/heygen-com/hyperframes/blob/3ad7611f9fd36c1cef589c59b116ad7043c3b041/packages/core/src/distributedFps.ts), [B32](https://github.com/remotion-dev/remotion/blob/889c61f2da985832fd35efc29eac29ffd72be12e/packages/core/src/validation/validate-fps.ts). Adapter musi więc sprawdzić docelowy encoded rate; samo przyjęcie argumentu nie certyfikuje rational round-trip.

### Seeking, seeded randomness i stan

**DERIVED, pseudokod NOT_RUN:**

    evaluateFrame(spec, f):
        assert integer(f) and 0 <= f < spec.totalFrames
        time = rational(f * spec.fps.den, spec.fps.num)
        state = evaluateOrderedGraph(spec.graph, time, spec.seed)
        render(state)
        await captureReady()
        return pixels

    randomForObject(projectSeed, objectId, property):
        return seededValue(hash(projectSeed, objectId, property))

    particleAt(f, birth, initial, velocity):
        age = max(0, f - birth)
        return initial + velocity * rational(age * fps.den, fps.num)

To jest własna ilustracja, nie kod z repo. Stały seed dla obiektu utrzymuje jego tożsamość. Seed zależny od każdej klatki tworzy biały szum; płynny wiggle potrzebuje interpolowanego noise w czasie. Przy dodaniu jednego particle istniejące particles nie powinny zmienić trajektorii przez przesunięcie indeksów. Używać stabilnych ID, nie kolejności wywołań globalnego PRNG.

**SOURCED:** Remotion random(seed) oblicza wartość z klucza; null przechodzi do Math.random. Pixi ticker nie obsługuje ujemnego delta jako cofania świata. Motion Canvas seek resetuje i przechodzi next(), a GeneratorScene resetuje PRNG z meta.seed. [B31](https://github.com/remotion-dev/remotion/blob/889c61f2da985832fd35efc29eac29ffd72be12e/packages/core/src/random.ts), [B35](https://github.com/pixijs/pixijs/blob/eb96c76fa27c948c748ff0bb79fc7a29329cd5e9/src/ticker/Ticker.ts), [B40](https://github.com/motion-canvas/motion-canvas/blob/7b91435c301d530351dcf5ebb91dd139c002e405/packages/core/src/app/PlaybackManager.ts), [B41](https://github.com/motion-canvas/motion-canvas/blob/7b91435c301d530351dcf5ebb91dd139c002e405/packages/core/src/scenes/GeneratorScene.ts).

**DERIVED:** klasyfikować komponent jako pure / replayable / baked / unsupported-random-access. Dla fizyki ze stanem: reset i replay ze stałym dt albo bake; dla feedback shaderów także bufor historyczny i warm-up. Nie deklarować niezależności klatek tylko dlatego, że kamera przyjmuje czas absolutny. Motion blur z subframe sampling wymaga ewaluacji w podklatkach; shaderowi z historią nie wystarczy wielokrotne wywołanie renderu tej samej klatki.

### Fonty, assety i preview parity

**SOURCED:** CSS FontFaceSet.ready kończy się po layout/loading, ale nie odrzuca na błędnym foncie. [B29](https://www.w3.org/TR/css-font-loading-3/#font-face-set-ready). **DERIVED:** preload każdej zadeklarowanej odmiany, sprawdzenie FontFace.load/status, hash pliku, glyph coverage i kształtowania tekstu „Zażółć gęślą jaźń — Łódź, 90 zł”. Sam rodzinny identyfikator Arial nie zamraża pliku fontu. Zachować ligatury, kerning i grapheme clusters; podział JavaScript string na code units nie jest pewnym podziałem na znaki.

Asset manifest powinien wiązać bytes, relative locator, decode metadata i prawa. Materiały sieciowe pobrać przed produkcyjnym renderem wyłącznie przy odpowiedniej zgodzie; ten research niczego nie uploaduje ani instaluje. Render bez internetu jest proponowanym testem samowystarczalności. Brak pliku powinien dać missing_asset, a nie stock photo albo inny font.

Preview/export parity mierzyć dla tej samej wersji grafu, assetów, fontów, viewportu, DPR i color pipeline. Różnica codec compression nie jest tym samym co błąd layoutu. Porównać obraz przed kodowaniem oraz decoded delivery. Słaby realtime preview może wynikać z czasu pojedynczej klatki i nie oznacza brakujących klatek offline; odwrotnie, ładny preview nie dowodzi poprawnego miksu i eksportu.

## 3. Technika → dane → agent → backend → ograniczenie → test

Wszystkie mapowania są **DERIVED**. „Wierny” oznacza wierną zasadę w zadeklarowanym zakresie, nie zgodność pikselową z AE. „Hybrydowy” zachowuje specjalistyczny/baked etap. Źródła backendu podano na końcu grup.

| Technika zawodowca → zasada | Reprezentacja danych / operacja agenta | Backend i fidelity | Ograniczenie / kontrprzykład | Proponowany test NOT_RUN |
|---|---|---|---|---|
| Parenting/null → wspólny transform | parent ID, anchor, local matrix; zbudować hierarchię | SVG groups, Three Object3D — **wierny** dla transformacji | Parent z nonuniform scale zmienia trajektorię/kształt | Marker anchor i narożniki przed/po reparent |
| Precomp → izolowany zakres i zależności | subgraph, local origin, bounds; kompilować lokalny clip | Remotion/HyperFrames — **wierny** dla czasu, **przybliżenie** collapse transforms | Rasteryzacja po drodze zmienia sampling i blend | Ten sam stan przy 100% i 400% zoom |
| Trim Paths → ujawnienie obrysu | path length, start/end/offset; obliczyć dash | SVG — **przybliżenie** pełnej semantyki AE | Wielokonturowe ścieżki, caps i fill nie są zwykłym dash | Przecięcia, start/koniec konturu, zero-length |
| Repeater → instancje transformowane | count, transform step, opacity per ID | SVG/Pixi/Three — **wierny** dla zadanej geometrii | Kolejność transformacji i stacking wpływają na overlap | 1/2/N kopii oraz zamiana kolejności |
| Spatial path + temporal easing | curve geometry + arc-length map + time curve | Canvas/SVG/GSAP — **wierny**, gdy oba mapowania jawne | Liniowy parametr Béziera nie daje stałej prędkości | Równe odległości w równych interwałach czasu |
| Overshoot/spring → kontrolowane dojście | target, damping model, duration lub analytical spring | Pure frame function — **wierny** dla wybranego modelu | Euler przy zmiennym dt daje inną odpowiedź | Losowa kolejność klatek; zero drift hold |
| Follow-through/overlap | opóźnienia hierarchii lub układ spring | GSAP, Blender — **przybliżenie/hybrydowy** | Niezależny delay nie zastąpi kolizji i bezwładności | Zatrzymanie parenta; child settle bez skoku |
| Alpha matte → pokrycie | matte ID, transform space, invert | SVG/Canvas/Pixi — **wierny** dla zgodnego sampling | Zmiana bounds/scaling matte daje halo | Kompozycja na białym, czarnym i checkerboard |
| Luma matte → luminancja jako coverage | color interpretation i explicit conversion | Shader/offline compositor — **przybliżenie** bez wzorca | sRGB luma vs linear luminance zmienia półtony | Klin tonalny i kolorowe łatki, zapis alpha |
| Adjustment layer → efekt na wyniku grupy | ordered effect node after composite | Render target + shader — **wierny** dla tego porządku | Efekt per-layer przed grupą nie daje tego samego | Dwie przecinające się warstwy blur/glow |
| Blend mode → jawna funkcja łączenia | mode, working space, alpha convention | Canvas/shader — **przybliżenie** do weryfikacji | Ta sama nazwa przy innej przestrzeni nie gwarantuje look | Gradient + półprzezroczysty kolor |
| 2.5D parallax → projekcja warstw | camera + plane depths + overscan | Three albo CSS perspective — **wierny** dla płaszczyzn | Brak boków produktu i prawdziwej geometrii | Silna zmiana kamery ujawnia brakujący obszar |
| 3D product reveal | geometry/material/light/camera/pass IDs | Blender/Three — **hybrydowy** wobec AE | Różne BRDF, tone map, shadows i DOF | Sylwetka, kontakt z podłożem, highlight continuity |
| Kinetic typography | exact copy, graphemes/words/lines, hold intervals | DOM/SVG/Remotion — **wierny** w prostym modelu | Split zmienia ligatury i layout; font fallback | Polskie litery, cudzysłowy, liczba z jednostką |
| Wiggle/procedural noise | seed, frequency Hz, amplitude units, continuous noise | Frame functions/shaders — **przybliżenie** AE expression | Inny noise kernel daje inne przebiegi | Ciągłość oraz identical-ID repeatability |
| Particles | birth/death, seed per ID, forces/bake | Pixi/Three/Blender — **hybrydowy** | Kolizje i feedback nie są random-access z definicji | Reverse/shuffle seek kontra sekwencyjny bake |
| Motion blur → ekspozycja w czasie | shutter interval + sample weights | Subframe renderer/Blender — **przybliżenie/hybrydowy** | Blur przestrzenny nie modeluje ekspozycji; brak subframe geometry | Szybki obiekt obracający się przez krawędź |
| Frame blending / optical flow | source frame map; interpolation algorithm | FFmpeg — **przybliżenie** dla retime | Occlusion, cut, cienki tekst mogą się deformować | Cut bez ghostingu, crossing objects, logo |
| Keying/roto/tracking | matte sequence, tracks, confidence, source provenance | Zewnętrzny etap → clip/alpha — **hybrydowy** | Brak praktycznego uniwersalnego CSS-tweenu równoważnego roto | Włosy, motion blur, zasłonięcie, drift |
| Beat/downbeat/VO accent | reviewed cue times + confidence + intended accent | Istniejący sync/FrameCut — **wierny** dla podanych czasów | Amplituda to nie metrum; alignment ASR wymaga kontroli | Pierwszy, środkowy, ostatni cue + odsłuch całości |
| Data animation | value provenance, interpolation, stable identity | SVG/Canvas/React — **wierny** dla geometrii | Morph może sugerować nieprawdziwą ciągłość kategorii | Liczby i osie zgodne ze źródłem na hold |
| Generatywna scena/nieznany AE plugin | requirement + unsupported feature record | **brak praktycznego odpowiednika** bez specyfikacji | Zgadywanie nazwy filtra nie zachowuje intencji | Zatrzymać i uzgodnić render/bake/zmianę wymogu |

Mechanizmy bazowe: SVG [B28](https://www.w3.org/TR/SVG2/painting.html#StrokeDashing), Canvas alpha [B27](https://html.spec.whatwg.org/multipage/canvas.html#premultiplied-alpha-and-the-2d-rendering-context), Three color [B38](https://threejs.org/manual/pages/color-management.html), Blender bake [B43](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/physics/simulation_nodes.rst), FFmpeg interpolation [B45](https://github.com/FFmpeg/FFmpeg/blob/b9a9bf7a3a74c2c62bac4c766666d1ca93b2c6ba/doc/filters.texi). Macierz nie dowodzi identyczności efektów AE.

## 4. CPU/GPU, cache, pamięć i wznowienie

**DERIVED:** CPU ocenia graf/layout, dekoduje i często koduje; GPU wykonuje wybrane draw/effect passes. Ten podział zależy od backendu i hosta. „GPU enabled” nie jest gwarancją wydajności ani dostępności konkretnego efektu. Najpierw mierzyć najdroższą scenę, potem dobierać worker count. Parallelism mnoży pamięć fontów, dekoderów, tekstur i browser contexts.

Budżet syntetyczny: jedna klatka 1920×1080 RGBA8 to 8 294 400 bajtów ≈ 7.91 MiB; tysiąc takich klatek ≈ 7.72 GiB bez dodatkowych kopii. Nie trzymać filmu w RAM. Ograniczona kolejka frame→encode, backpressure i cache na dysku są bezpieczniejszym projektem. Render target z float i dodatkowymi passes wymaga osobnej kalkulacji.

**SOURCED:** Pixi ostrzega, że culling pomaga GPU-bound, ale może szkodzić CPU-bound; Three wymaga dispose zasobów; HyperFrames ma osobne probe cgroup i tryby pamięci/GPU. [B36](https://pixijs.com/8.x/guides/concepts/performance-tips), [B39](https://threejs.org/manual/pages/cleanup.html), [B21](https://github.com/heygen-com/hyperframes/blob/3ad7611f9fd36c1cef589c59b116ad7043c3b041/packages/engine/src/config.ts), [B22](https://github.com/heygen-com/hyperframes/blob/3ad7611f9fd36c1cef589c59b116ad7043c3b041/packages/engine/src/services/systemMemory.ts). Kod releaseEndedWebglContexts zwalnia konteksty zakończonych klipów [B23](https://github.com/heygen-com/hyperframes/blob/3ad7611f9fd36c1cef589c59b116ad7043c3b041/packages/engine/src/services/webglRelease.ts); nie przenosić tej optymalizacji bez testu powrotu do wcześniejszej sceny.

**DERIVED:** cache key = hash(spec relevant subset, asset bytes, font bytes, renderer build, effect settings, color settings, seed, frame range). Nie wpisywać samych ścieżek jako tożsamości pliku. Wznowienie wymaga poprawnych receipt i testu decode. Zapis chunk do temp → weryfikacja → atomowe opublikowanie → receipt. Przerwana ostatnia paczka nie jest gotowym cache. Zmiana kontraktu unieważnia zależne, a nie wszystkie bloki.

FrameCut już realizuje cache stage receipts [B14](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/opencut-video-studio/assets/framecut/fc_render.py). FrameMotion powinien zwracać własny lokalny receipt; nadrzędny job i retry zostają u właściciela filmu. Błędy invalid input, stale source, unsupported effect i failed QA nie powinny być automatycznie retryowane. Transient capture failure: proponowany jeden retry w tych samych warunkach, potem diagnoza; nie cicha zamiana GPU na inny wygląd ani płatny renderer.

## 5. Wnioski z innych profesjonalnych środowisk

**SOURCED:** Apple Motion potrafi przekształcić część behaviors w keyframes, lecz operacja obejmuje współdziałające behaviors, a część simulation/particle/text nie jest konwertowalna. [B48](https://support.apple.com/en-lamr/guide/motion/motn13743c3a/mac). **DERIVED:** model agenta powinien zachować receptę proceduralną i oddzielną reprezentację baked. Baked curve ułatwia korektę klatki, ale traci wygodne sterowanie prawami ruchu; uproszczenie kluczy musi mieć tolerancję błędu, szczególnie w hold i cue. Nie zakładać, że każdą proceduralną scenę da się zamienić w kilka keyframes.

**SOURCED:** Blender simulation cache powstaje podczas odtwarzania, a disk bake pozwala renderować poza kolejnością [B43]. **DERIVED:** planowanie product reveal z cloth/liquid musi zawierać etap zatwierdzenia ruchu przed ciężkim renderem; zmiana czasu lub geometrii może unieważnić bake. Jest to inny koszt rewizji niż korekta koloru tytułu.

**DERIVED:** z node compositingu warto przejąć jawne zależności i order of operations; z layer compositingu — czytelność hierarchii i local isolation. Ten podaudyt backendów nie obejmował własnych testów Fusion/Cinema 4D. Konkretne źródła i narzędzia tych aplikacji są udokumentowane w równoległych częściach [CRAFT](../craft/CRAFT.md) i [RECIPES](../recipes/RECIPES.md); ich zakres nie jest globalną luką tego researchu.

## 6. Ograniczona kwalifikacja adaptera

**DERIVED, wszystkie testy NOT_RUN:**

1. **Preflight:** wersje, wejścia, czas, rozmiar, alpha/color, font hash, capabilities. Brak wymaganej funkcji kończy wybór explicit unsupported; przybliżenie wymaga jawnej zmiany planu.
2. **State:** render 0, 1, środek, N−1, następnie odwrócona i losowa kolejność, powtórzenie w świeżym procesie. Porównać pre-encode pixels i metadane; określić tolerancję przed testem.
3. **Temporal:** pełen film w realtime; sprawdzić akcent, settling, prędkość, cadence, ghosting, niezamierzone flashe. Stills są dowodem pojedynczej klatki.
4. **Sound:** pełny odsłuch, cue alignment i drift, nie tylko liczba streamów. Oddzielić PCM master od opóźnienia/trimu kodera.
5. **Delivery:** decoded frames, rational FPS, duration, dimensions, color tags, alpha test na dwóch tłach, dependency manifest oraz hash konkretnego pliku.
6. **Repair:** naprawić konkretne odchylenie od zaakceptowanej intencji, zachować locks. Maksymalnie dwa obiegi korekt po pierwszym review, zgodnie z istniejącym limitem Studio; PASS zatrzymuje pracę. Nierozwiązany blocker → named limitation / review candidate, nie kolejne „upiększanie”.

Istniejący punkt zaczepienia stanowi acceptance.py z czterema werdyktami [B09](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/plugins/framecore-work-creative-studio/skills/hyperframes-workflow/assets/motion-review/README.md). Proponowane testy adaptera dostarczają dowodów do tego procesu; nie tworzą kolejnej niezależnej bramki akceptacji.

## 7. Pokrycie i granice

| Temat | Dowód | Pozostaje |
|---|---|---|
| Wszystkie 10 rodzin backendów | Dokumentacja/API/source inspection | Własny benchmark i rzeczywista instalacja Unknown |
| Master/local clock, rational FPS, stale bindings | Obecny kod Studio/FrameCut | Wersjonowany adapter FrameMotion nie istnieje w badanym materiale |
| Seek/random access | Kod Pixi, Motion Canvas, Three, Remotion; dokumentacja web | Pełne render parity tests NOT_RUN |
| CPU/GPU/memory/resume | Kod/procedury wybranych backendów | Pomiary na Macu użytkownika NOT_RUN |
| Alpha/color/fonty | Standardy i dokumentacja właścicieli | Cross-platform pixel equality Unknown |
| Apple Motion/Blender | Odczyt konkretnej instrukcji | Nie oglądano UI, nie wykonano renderu |
| Fusion/Cinema 4D | W tej części ogólna adaptacja grafu; konkretne źródła w [CRAFT](../craft/CRAFT.md) i [RECIPES](../recipes/RECIPES.md) | Własny test backendu NOT_RUN; zakres źródeł opisują części specjalistyczne |

