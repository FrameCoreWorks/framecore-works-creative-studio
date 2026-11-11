# DR-01 — profesjonalny motion design, animacja i compositing dla FrameMotion

Badanie: **2026-11-11**, język polski z terminami EN. Zakres: PROMPT.md + SCOPE-CLARIFICATION.md. To główna synteza **wieloczęściowego kompendium**; szczegóły warsztatu, słownik, receptury, repozytoria i kontrakty są rozdzielone w plikach wskazanych poniżej, żeby nie mieszać instrukcji twórczych z API. Nie wdrożono kodu wtyczek, niczego nie instalowano i nie wykonano filmów testowych.

## Najważniejszy wniosek

FrameMotion powinien przenosić **sposób podejmowania i sprawdzania decyzji profesjonalisty**, a nie listę efektów After Effects. Fachowiec zaczyna od znaczenia, buduje kompozycję, wybiera moment akcentu, ustawia stabilne stany, dopiero potem kształtuje drogę i prędkość. Następnie kontroluje kolejność operacji obrazu, tekst, dźwięk i wynik w czasie. Agent potrzebuje tych samych kroków oraz zapisanych granic: co wolno zmienić, kto ma timeline i jak rozpoznać konkretny defekt.

**DERIVED:** dobrym rdzeniem nie jest „uniwersalny tween” ani „AE w JSON”, lecz trzy warstwy: istniejący score z intencją i akceptacją → jawna reprezentacja sceny/zależności → adapter o sprawdzonych możliwościach. Parametry bez intencji produkują przypadkową animację; intencja bez formalnych jednostek nie daje powtarzalnego renderu.

**SOURCED, inspekcja kodu:** Studio ma już motion-score oraz FrameCut motion-request/binding z rewizjami i kontrolą materiału. Ten stan ma pierwszeństwo. Publiczny main z badania: `4611c9c4ed44579b8a2c0224c9276d955fccd8d6`; nie jest to identyfikator zainstalowanej instancji. Dowody, ścieżki i ograniczenia: [audyt Studio](specialists/backends/STUDIO-AUDIT.md).

## Jak korzystać z kompendium

| Potrzeba | Część, którą należy przeczytać |
|---|---|
| Warsztat A–E: ruch, AE, krzywe, compositing, typografia | [CRAFT.md](specialists/craft/CRAFT.md) |
| 100 terminów PL/EN z przykładem i skutkiem | [GLOSSARY.md](specialists/craft/GLOSSARY.md) |
| 18 pełnych receptur | [RECIPES.md](specialists/recipes/RECIPES.md) |
| Proces, poprawki, tutoriale i praktycy | [PROCESS-AND-TUTORIALS.md](specialists/recipes/PROCESS-AND-TUTORIALS.md) |
| AE/Fusion/Motion/C4D/Blender plus Nuke/Houdini | [PROFESSIONAL-WORKFLOWS.md](PROFESSIONAL-WORKFLOWS.md) i sekcje porównawcze warsztatu/receptur |
| Dobór backendu i technika → dane → kod → test | [BACKENDS.md](specialists/backends/BACKENDS.md) |
| Konkretne pliki repo, licencje i odrzucenia | [REPOSITORIES.md](specialists/backends/REPOSITORIES.md) |
| Wersjonowany kontrakt, grafy i przykłady | [CODE-AND-CONTRACTS.md](CODE-AND-CONTRACTS.md), [examples](examples/README.md) |
| QA, pięć benchmarków i formaty | [QA-BENCHMARKS.md](QA-BENCHMARKS.md) |
| Obecna wtyczka / luka / Unknown | [COVERAGE-MATRIX.md](COVERAGE-MATRIX.md) |
| Wdrożenie po osobnym zleceniu | [IMPLEMENTATION_HANDOFF.md](IMPLEMENTATION_HANDOFF.md) |

## Zasady warsztatu przełożone na działania agenta

### 1. Zdefiniuj rezultat, który da się odrzucić

„Dynamiczna animacja premium” nie określa ruchu. „Połączenie trzech części tworzy znak, który przez cały hold zachowuje oryginalne proporcje i dokładny tekst” już tak. Własny brief sceny zawiera cel poznawczy/emocjonalny, pierwszą dominantę, stan końcowy, moment impactu, reading hold i locks. **Kontrprzykład:** narracja o awarii może świadomie łamać rytm i siatkę; zasada jednego akcentu nie zabrania takiej intencji. **Test:** jednokrotne odtworzenie odpowiada na pytanie, co widz zauważył i co zrozumiał. Bez testu widza to hipoteza, nie gwarancja skuteczności reklamy.

### 2. Zbuduj statyczną kompozycję i stany znaczące

Siatka, negatywna przestrzeń, kolor, kerning i hierarchia działają również w czasie. Najpierw ustal styleframe wejścia/impactu/hold/wyjścia. Dla długiego polskiego słowa ujawnianego maską uwzględnij ogonki i ascenders. **Kontrprzykład:** skupienie wyłącznie na klatce „hero” może ukryć kolizję przejściową. **Test:** styleframe plus ciągły przebieg, z kontrolą bbox i odczytu w docelowym rozmiarze. Słownik nie zastępuje tego etapu.

### 3. Rozdziel timing, spacing i kształt toru

Timing wybiera, kiedy dzieje się rzecz. Spacing mówi, jak zmienia się położenie między sample. Temporal interpolation steruje postępem, spatial interpolation geometrią. Speed to pochodna przebiegu, a nie drugi zapis położenia. **Kontrprzykład:** wygładzenie każdego klucza powoduje zatrzymanie w punktach, przez które obiekt miał przejechać. **Test:** znacznik pośredni z niezerową prędkością, wykres pozycji i pochodnej; jeden wyraźny stop dopiero w uzasadnionym miejscu. Szczegółowe mechanizmy AE i parametry są w CRAFT C.

### 4. Modeluj znaczenie ruchu zamiast rozrzucać efekty

Anticipation przygotowuje uwagę, overshoot przekracza cel, follow-through opóźnia wygaszenie reakcji, overlap rozdziela fazy części. To nie cztery nazwy tego samego bounce. Logo instytucji może wymagać twardego settle, a miękka maskotka deformacji. **Kontrprzykład:** deformacja chronionego logotypu narusza brief nawet wtedy, gdy wygląda płynnie. **Test:** porównanie stanu końcowego do assetu oraz uzasadnienie każdego akcentu jednym zdaniem. Usunąć efekt, który nie wspiera funkcji sceny.

### 5. Traktuj render order, alfa i kolor jako dane

Precomp, collapse transformations, matte, maska i adjustment layer definiują różne granice obliczeń. Nie można zastąpić ich jednym polem `group`. Alfa określa pokrycie, a straight/premultiplied określa także reprezentację RGB. Linear light, gamut i bit depth są odrębnymi pojęciami. **Kontrprzykład:** poprawny kontur na czarnym tle może dać ciemną obwódkę na białym. **Test:** ta sama miękka krawędź na trzech tłach, osobno RGB/alfa, przed i po resize/grade. [Nuke Premult H07](https://learn.foundry.com/nuke/content/reference_guide/merge_nodes/premult.html) wspiera konkretną zależność dla Nuke; przeniesienie do adaptera wymaga jego testu.

### 6. Oddziel rytm muzyczny od sygnału i moment akcentu od startu

Beat, downbeat i onset są różnymi opisami. Amplituda nie jest tożsama z pulsem, onset nie przesądza o pierwszej części taktu, a wykrycie słów nie zapewnia semantycznego akcentu. **SOURCED H04/H05:** dokumentacja librosa rozróżnia beat tracking oparty na onset strength i tempie od peak-picking onsets oraz ich backtrack do minimum energii. [Beat tracking](https://librosa.org/doc/0.11.0/generated/librosa.beat.beat_track.html), [onset](https://librosa.org/doc/0.11.0/generated/librosa.onset.onset_detect.html).

**DERIVED:** planować przybycie obiektu na beat, cofając start o jego attack time. Offset naprawia przesunięcie stałe; drift wymaga korekty relacji zegarów lub tempa; variable tempo wymaga cue map. **Kontrprzykład:** metronomiczny grid położony na rubato jest zły mimo poprawnego pierwszego beatu. **Test:** początek/środek/koniec i odsłuch całej frazy, z ręczną korektą i jej provenance.

### 7. Wybierz backend według operacji i ograniczeń

SVG/GSAP dobrze opisują precyzyjny ruch grafiki 2D, React/Remotion ułatwia sceny zależne od frame, Canvas/Pixi pozwalają sterować wieloma elementami, Three/WebGL opisują geometrię i shadery, Blender wykonuje pełną scenę 3D, FFmpeg składa/filtruje/koduje wynik. To zakresy decyzji, nie automatyczne deklaracje dostępności lub identyczności z AE. HyperFrames oraz Motion Canvas mają własne modele i granice API — odczytane pliki i wersje są w BACKENDS.

**Kontrprzykład:** glow o tej samej nazwie w dwóch backendach może operować w innym kolorze, progu i domenie alfa. CSS transition uruchamiana zegarem ściennym nie jest jeszcze deterministycznym renderem klatki. **Test:** capability report przypisuje wierny/przybliżony/hybrydowy/unsupported; porównywać fixture, nie logo biblioteki.

### 8. Zachowaj właściciela czasu i zatwierdzone decyzje

FrameMotion dostaje scenę i granice; nie zwiększa długości całego filmu, bo potrzebuje wygodniejszego hold. Prośba o zmianę długości wraca do ownera. Zmiana assetu/tekstu unieważnia zależne zatwierdzenia, zachowując historię. **SOURCED H06:** PROV rozróżnia encje, działania i relacje rewizji; reguła akceptacji pozostaje naszą adaptacją. [PROV Primer](https://www.w3.org/TR/prov-primer/).

**Kontrprzykład:** niezmienny filename ukrywa nowy plik; sam hash nie mówi, czy różnica jest semantycznie istotna. **Test:** zmiana jednej zależności wskazuje właściwy zestaw wyników, pozostawiając pozostałe locks. W razie stale request odświeżyć od ownera, a nie retry attach bez końca.

## Co wnosi poszerzenie poza After Effects

AE daje wzorzec autorskiej osi warstw i precompów. Fusion uczy widocznej topologii compositingu. Apple Motion pokazuje rozdział behavior od keyframe i dobór parametrów szablonu. Cinema 4D wnosi instancje oraz pola wpływu, Blender geometrię, kamerę, render i bake. Nuke uwidacznia kanały i alpha-domain, a Houdini rozróżnia stan solvera od cache obrazu. Z tych modeli wyprowadzamy **jawne grafy, wersjonowane adaptery i testy**, a nie jeden nowy monolityczny renderer.

Praktyczna zasada: jeśli obraz zależy od głębokiej interakcji światła, materiału, geometrii lub solvera, wybierz workflow hybrydowy i zachowaj projekt natywny. Jeśli zależy głównie od układu, krzywych i dokładnego tekstu, backend 2D może być prostszy do sprawdzenia. Ani 3D, ani shader nie podnosi automatycznie jakości komunikatu.

## Granice dowodu i prawa

SOURCED oznacza poparte odczytanym źródłem, DERIVED własne przykłady i adaptację, PRACTITIONER relację nazwanego autora o jego praktyce, Unknown brak dostatecznego dowodu. Osobno zapisywana jest metoda: dokumentacja, kod, opublikowany test autora, własny test. Transkrypcja lub tekst kursu nie są obejrzanym filmem; render stanu testowego nie jest testem percepcji. W tym researchu własne testy dotyczą danych i analityki. Natywne renderowanie, ciągłe odtwarzanie i odsłuch: NOT_RUN.

Materiały tutorialowe przełożono na oryginalne receptury; nie kopiowano kursów, projektów ani cudzych assetów. Licencja kodu nie rozstrzyga licencji fontów, modeli i muzyki. Remotion i GSAP wymagają kontroli dokładnych warunków zastosowania — nie oznaczono ich zbiorczo jako MIT ani „zawsze za darmo”. Wszystkie mutable API/licence/version trzeba sprawdzić ponownie przed wdrożeniem. Użyte źródła są w SOURCE-LEDGER.json/CSV; nieudane próby i ograniczenia pozostają widoczne.
