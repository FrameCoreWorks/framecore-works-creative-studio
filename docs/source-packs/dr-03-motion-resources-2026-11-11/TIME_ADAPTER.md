# DR-03 — propozycja adaptera czasu i eksportu
**DERIVED, NOT_RUN.** Kontrakt projektowy do analizy Claude, nie zaimplementowane API FrameMotion. Bazuje na istniejącym Studio stateAtFrame oraz runtime cards; nie zastępuje master clock ani FrameCut timeline. Źródła baseline: B19–B26.

## Jeden zegar, jawny model stanu
Dane wejściowe: asset/code revision, fps jako numerator/denominator, frameCount, render size, seed, lokalne resources/font hashes, parametry look, event log, alpha/color wymagania, frame mapping i prawa. Czas t = frame × denominator / numerator. Export używa frame w [0,N), preview wzywa tę samą operację.

Proponowana minimalna powierzchnia:
- prepare(resources, config): wczytanie tylko jawnie wskazanych zasobów, fontów i WASM; raport gotowości lub typed error.
- capabilities(): pureSeek | replaySeek | bakedOnly | unsupported, alpha support, color pipeline, wymagane dependency pins.
- renderAt(frame): complete state + await draw completion → canvas/RGBA albo klatka; brak ukrytego postępu czasu.
- reset(initialState) / dispose(): wyłącznie własne zasoby. Preview Play tylko wylicza frame z zegara; export nie włącza RAF.
- evidence(): rzeczywisty input/output hash, runtime versions, renderer settings, frame order, unresolved limits.

To propozycja kontraktu, nie kod do wykonania i nie architektoniczna akceptacja.

## Mapowanie z interakcji
| Źródło interakcji | Adaptacja | Gdzie nie wolno udawać seek |
|---|---|---|
| Hover/click toggle | Parametr state albo event {frame,type,value}; UI oddzielone od rysowania | Gdy transition callback mutuje layout poza timeline |
| Scroll progress | Wybrany track progress(frame) w [0,1]; jawny easing i range, fixed viewport | Scrollytelling wymagający zmiennej geometrii bez przygotowania layoutu |
| GSAP | Paused timeline, inicjalizacja raz, seek(t) z kontrolą callbacków; wszystkie efekty funkcją czasu | suppressEvents nie cofnie dowolnych wcześniejszych side effects |
| SVG SMIL / WAAPI | pause + setCurrentTime/currentTime do wybranego t; bounds/rasterize w gotowej przeglądarce | Statyczny SVG rasterizer nie interpretuje timeline SMIL; najpierw materializacja stanu |
| Lottie | Wybrany konkretny renderer i source frames; mapping trim/fps/hold/loop; disable autoplay | JSON valid nie dowodzi mask/gradient/matte/font compatibility |
| dotLottie | Archive inspection, animation ID, local resources/WASM, supported frame API | Nie wysyłać bajtów archiwum do JSON lottie-web; state machines oddzielnie |
| Rive | Linear animation time albo reset+ordered fixed-step state-machine replay | Advance(delta) sam nie jest arbitrary seek; sprawdzić wersję i apply semantics |
| Particles/physics/trails | Analityczny stan, seeded simulation fixed dt z reset/replay lub bake/cache | Sam uniform time/seed nie kontroluje RNG geometrii ani history buffers |
| Audio reactive | Offline feature table: sample index, sr/hop, onset/energy, smoothing, map to frames | Web Audio analyser w czasie rzeczywistym zmienia wynik i zależy od playback |

## Eksport i koszty
Preferować istniejącego hosta kompozycji (Remotion/HyperFrames/Pixi/Three), bez dodatkowego pełnego renderer stacku. Czysty SVG→PNG może być narrow utility; native binary binding i tekst to odrębna zgodność. Blender assets/VDB → baked clip/EXR z wybranej sceny; FFmpeg składa potwierdzone klatki/klipy, nie naprawia niepowtarzalnej logiki.

Wymuszone połączenie DOM + Canvas wymaga rasteryzacji całej kompozycji albo jawnego wspólnego canvas; etykieta obok canvas nie pojawi się w video. Kolor i alpha muszą być uzgodnione na granicach. Zapewnić oczekiwanie na init/font sync/render completion, backpressure, cancel i brak accepted partial output.

Szacunki **DERIVED**: pure module adapter 0.5–2 person-days; shader z RNG/history 2–5; replay state machine 3–7; sim/bake lub native install matrix 3–10. Nie są ofertą ani pomiarem; pierwsza próba może odrzucić kandydata wcześniej. Hardware memory/cost **Unknown** do pomiaru fixture; nie przeliczamy tokenów z czasu.

## Pinning, retry, fallback
Pin full commit + dokładną wersję paczki i lock; osobny hash assetu, fontu i WASM. Nie utożsamiać source SHA z release ZIP. Zakresy dependency i install hooks wymagają odrębnego przeglądu przed uruchomieniem. Utrzymywać wersje peer deps istniejącego projektu.

Po 404/401/licence conflict/unsupported feature: stop danej ścieżki; nie automatyczny inny dostawca. Jedno kontrolowane ponowienie wyłącznie transient read/network error, z zachowaniem wejść; runtime determinism failure nie jest transient. Fallback po decyzji: istniejąca model-authored geometria, prostszy zatwierdzony efekt albo jawny baked clip. Brak alfa nie może uruchomić cichego opaque eksportu.

## Acceptance
Każdy adapter deklaruje wspierany model czasu. Testy T01–T12 w TEST_PLAN.md dobiera się do capabilities. Bez poprawnego importu, praw, powtórnych i odwrotnych odczytów klatek oraz oglądu temporalnego: **NOT_RUN/niezweryfikowany**, nigdy „integration works”.


## Pierwotne podstawy SVG/WAAPI
W3C opisuje w SVG 1.1 pauzę zegara fragmentu i setCurrentTime w sekundach ([SVGSVGElement](https://www.w3.org/TR/SVG11/struct.html#InterfaceSVGSVGElement)). Web Animations Working Draft z 2023-06-05 opisuje zmianę current time jako seek ([§4.4.4](https://www.w3.org/TR/2023/WD-web-animations-1-20230605/#setting-the-current-time-of-an-animation)). To semantyka API; wsparcie wybranej przeglądarki, wykonanie callbacków i rasteryzacja konkretnego assetu pozostają NOT_RUN.
