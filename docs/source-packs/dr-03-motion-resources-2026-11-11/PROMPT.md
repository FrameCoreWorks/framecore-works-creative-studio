Przeprowadź Deep Research nowych repozytoriów, skilli, bibliotek, narzędzi i gotowych assetów do motion graphics. Celem jest znalezienie konkretnych rozszerzeń dla FrameMotion, FrameCore Works Creative Studio oraz FrameCore Works Toolbox, a także wybranie najbardziej użytecznej wiedzy do adaptacji w ich instrukcjach.

Wykonaj badanie, nie tylko plan. Raport po polsku, nazwy techniczne zachowaj po angielsku. Nie powtarzaj ogólnego podręcznika After Effects: skup się na nowych zasobach i ich rzeczywistym zastosowaniu w produkcji.

1. PUNKT ODNIESIENIA I NOWOŚĆ

Najpierw przeczytaj aktualne README, AGENTS.md, katalogi, manifesty, reviews i istotne pliki:
https://github.com/FrameCoreWorks/framecore-works-creative-studio
https://github.com/FrameCoreWorks/framecore-works-toolbox
https://github.com/FrameCoreWorks/framecore-open-assets

Zapisz sprawdzone commity i datę. FrameMotion jest nową wtyczką do animacji i motion graphics; jej adresu repozytorium nie podano. Nie wymyślaj go ani obecnych funkcji. FrameCut odpowiada za montaż, Studio za koordynację produkcji, Toolbox za katalog rozszerzeń, Open Assets za pozyskiwanie mediów. Zweryfikuj istniejące granice odpowiedzialności, jeśli masz dostęp.

Zbuduj baseline przed szukaniem „nowości”. useAnimations i LottieFiles/generative-icons były już przedmiotem wcześniejszych testów: uwzględnij je w deduplikacji, ale nie zakładaj, że zostały wdrożone. Sprawdź także projekty obecne w aktualnym Toolboxie.

Oznacz każdą pozycję:
NEW, KNOWN_NEW_CAPABILITY, ALREADY_COVERED, DUPLICATE/FORK lub BASELINE_UNKNOWN.
„Nowe dla FrameCore” nie oznacza „niedawno opublikowane”. Gdy baseline jest niedostępny, nowość pozostaje Unknown.

2. CZEGO SZUKAĆ

Szukaj równolegle w trzech klasach:
A. Repozytoria i moduły wykonawcze: biblioteki, renderery, CLI, lokalne MCP, narzędzia konwersji i QA.
B. Wiedza agentowa: SKILL.md, cookbooki, przykłady, przepisy, szablony scen, kontrakty i testy.
C. Gotowe assety produkcyjne: animowane ikony, Lottie/dotLottie, Rive, SVG, sprite sheets, pętle, overlaye z alfą, materiały, tekstury, HDRI, modele 3D, rigi i animacje.

Kategorie:
- kinetic typography, text reveals, layout i animacja liter/słów;
- shape/path animation, stroke drawing, maski i track mattes;
- transitions, particles, trails, procedural backgrounds i generative art;
- shadery, distortion, displacement, lighting i postprocessing;
- glitch, VHS/CRT, scanlines, pixel art, dithering, ASCII i halftone;
- 2.5D/3D, procedural geometry, physics, symulacje i ruch kamery;
- UI/product animation, diagramy, wykresy, infografiki i explainery;
- audio-reactive motion, beat/onset sync i animacja napisów;
- alpha compositing, blur, grain, glow oraz jakość i powtarzalność eksportu.

Zbadaj kompatybilność z Remotion, HyperFrames/GSAP, HTML/SVG/Canvas, PixiJS, Three.js/WebGL, Blender i FFmpeg, ale nie zakładaj obecności tych silników w środowisku wykonawczym.

Nie zawężaj poszukiwań do GitHub. Zbadaj strony autorów, dokumentację, rejestry pakietów i legalne kolekcje assetów. Galerie inspiracji bez praw do wykorzystania oznacz REFERENCE_ONLY.

3. METODA I DOWODY

Szukaj po polsku i angielsku. Używaj dokumentacji autorów, rzeczywistego kodu, przykładów, releases, issues i testów. Listy awesome i posty społecznościowe służą odkrywaniu kandydatów, nie końcowej weryfikacji.

Celuj w 25–40 trafnych kandydatów i dogłębną analizę 8–12 najlepszych. Liczby są orientacyjne: nie dodawaj pozycji słabych ani duplikatów. Pokryj wszystkie kategorie lub jawnie opisz lukę.

Dla istotnych twierdzeń podaj źródło przy twierdzeniu, a kod przypinaj do commitu. Rozróżniaj:
DOCUMENTED, CODE_INSPECTED, AUTHOR_TEST, OWN_TEST, NOT_RUN i Unknown.
Osobno oznacz własne propozycje jako DERIVED. Demo autora nie jest własnym testem.

Dla najlepszych projektów sprawdź pliki implementacji, manifesty, skrypty instalacyjne i zależności, a nie tylko README. Nie uruchamiaj ich w ramach tego badania.

4. KARTA KAŻDEGO KANDYDATA

Podaj:
- nazwa, kanoniczny URL, owner, commit/tag, data przeglądu;
- klasa zasobu, status nowości, konkretny problem i przewaga nad baseline;
- konkretny plik/moduł/asset do użycia;
- wejścia/wyjścia, API/CLI, formaty, edytowalność, alfa i parametryzacja;
- wymagania runtime, system, CPU/GPU, pamięć, browser/headless/offline;
- droga do MP4, sekwencji PNG/EXR, WebM lub innego użytecznego eksportu;
- koszt, konto, klucz, sieć i ukryte zależności usługowe;
- licencja kodu, osobno assetów, fontów, modeli i przykładów;
- aktualność, istotne błędy, utrzymanie, ograniczenia i poziom dowodu;
- docelowy właściciel oraz zakres możliwej integracji;
- rekomendacja i test, który potwierdzi przydatność.

Dla assetów dopisz rozdzielczość, długość, FPS, loop/seam, kanał alfa, warstwy, powiązane pliki i pochodzenie. Parametry nieustalone oznacz Unknown.

Rozdziel prawo do użycia w wyrenderowanym filmie od prawa do redystrybucji źródłowego assetu we wtyczce. Licencja repozytorium nie musi obejmować jego galerii.

5. PRZYDATNOŚĆ DO PRODUKCJI AGENTOWEJ

Oceń:
- sterowanie po numerze klatki/czasie absolutnym;
- seek, rewind, seeded randomness i bake/cache symulacji;
- brak zależności od czasu rzeczywistego, scrolla, kliknięć lub sesji użytkownika;
- font loading, polskie znaki, stabilność layoutu;
- powtarzalność preview/export, rozdzielczość, FPS i proporcje;
- możliwość rozdzielenia logiki efektu od interfejsu strony;
- błędy importu, clipping, flicker, aliasing, kolor i premultiplied alpha;
- koszty renderowania oraz skalę wymaganych przeróbek.

Nie traktuj interaktywnego dema jako gotowego narzędzia wideo. Dla adaptera opisz, jak zamienić interakcję na kontrolowany czas i eksport. Jeśli nie ma wiarygodnej drogi, oznacz ograniczenie.

Dla Lottie/Rive/animowanego SVG sprawdź zgodność użytych funkcji z konkretnym rendererem i eksportem. Sama poprawność JSON nie potwierdza zgodności wizualnej.

6. ADAPTACJA WIEDZY I TESTY

Dla każdego z najlepszych kandydatów przygotuj kartę:
źródło → użyteczna zasada → warunek użycia → dane → operacja agenta → przykład zastosowania → ograniczenia → QA.

Wybierz właściwą formę:
KNOWLEDGE_ONLY, SKILL_ADAPTATION, OPTIONAL_DEPENDENCY, ADAPTER, TOOLBOX_ENTRY, ON_DEMAND_ASSET lub REJECT.
Nie importuj całych repozytoriów, jeśli wystarczy jedna metoda. Nie twórz skilla, jeśli wiedza pasuje do istniejącego właściciela.

Zaproponuj małe testy: import i decode, odczyt klatek w różnej kolejności, powtarzalny render krótkiej pętli, eksport z alfą, polski tekst oraz adaptacja 16:9/9:16. Dla każdego określ fixture, wynik, błędy i sposób oglądu temporalnego. Testy niewykonane oznacz NOT_RUN.

Dla zależności opisz pinning, błędy, retry, limity, fallback i koszt integracji jako szacunek. Nie deklaruj działającej integracji na podstawie samej inspekcji.

7. WYNIK

Dostarcz:
- mapę obecnych możliwości i luk;
- katalog kandydatów z deduplikacją;
- osobne rankingi nowych możliwości, gotowych assetów i wiedzy do adaptacji;
- szczegółową analizę najlepszych pozycji;
- tabelę odrzuceń i zasobów REFERENCE_ONLY;
- plan testów, backlog P0/P1/P2 i IMPLEMENTATION_HANDOFF;
- rejestr źródeł oraz kompletne karty do przyszłego wykorzystania przez agentów.

Ranking uzasadnij nową użytecznością, jakością, kontrolą renderu, prawami i kosztem integracji. Gwiazdki GitHub nie są miarą jakości produkcyjnej. Nie rekomenduj kolejnego pełnego silnika bez wskazania realnej luki.

Jeśli można tworzyć pliki, zapisz raport Markdown i katalog CSV/JSON. Zachowaj datę, commity, statusy dowodów i brakujące dane.

To research bez instalacji, uruchamiania pobranego kodu, masowych pobrań, zmian w repozytoriach, płatnych usług, uploadu prywatnych danych, pushu, deployu i publikacji. Czytaj publiczne źródła, bez obchodzenia ograniczeń dostępu. Testy wykonawcze pozostaw jako osobny plan.

Zacznij badanie teraz. Nie pytaj o konkretną reklamę: szukamy rozszerzeń wielokrotnego użytku, które zwiększą możliwości produkcyjne FrameCore.