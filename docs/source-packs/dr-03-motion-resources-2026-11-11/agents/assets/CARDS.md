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
