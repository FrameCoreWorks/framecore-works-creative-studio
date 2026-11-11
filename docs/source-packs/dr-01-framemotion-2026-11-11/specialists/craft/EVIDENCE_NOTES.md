# DR-01 craft — granice dowodu i próby nieudane

Data: 2026-11-11.

## Co odczytano

Rejestr `sources.json` zawiera 32 unikalne źródła C01–C32. Odczyt obejmował treść właściwych sekcji, nie tylko wyniki wyszukiwania. C23 to pisemne podsumowania samouczka Iana Robinsona; C24 to tekst strony producenta Fusion, a nie instrukcja kontrolki. C32 to cały krótki plik RST oficjalnego podręcznika Blendera, pobrany do pamięci przez odczyt publicznego URL; nie wykonywano jego treści.

Nie oglądano osadzonych filmów ani animowanych przykładów. Nie pobierano plików ćwiczeń, nie uruchamiano projektów aplikacji i nie testowano renderowania. Własne obliczenia ekspozycji i przykład alfa są DERIVED.

Wyszukiwanie obejmowało angielskie nazwy funkcji oraz polskie pytanie o animowanie tekstu. Polska strona Adobe Learn C23 miała polski interfejs, lecz merytoryczne podsumowania lekcji były po angielsku. Nie deklarujemy polskojęzycznego korpusu równoważnego angielskiemu.

## Próby niezaliczone do źródeł wykorzystanych

| Publiczny adres | Zaobserwowany wynik | Postępowanie |
|---|---|---|
| https://docs.blender.org/manual/en/4.5/render/cycles/render_settings/motion_blur.html | Web: HTTP 402 | Nie przyjęto snippetu; odczytano oficjalny raw jako C32 |
| https://docs.blender.org/manual/en/latest/render/cycles/render_settings/motion_blur.html | Web: HTTP 402 | Jak wyżej; nie liczyć oddzielnie |
| https://docs.blender.org/manual/en/4.5/render/color_management.html | Web: HTTP 402 | Domena koloru oparta na odczytanej dokumentacji AE; brak przypisania Blenderowi |
| https://developer.blender.org/docs/features/render_pipeline/color_management/ | Web: HTTP 402 | Nie przyjęto jako odczytanej dokumentacji implementacji |
| https://www.blender.org/features/rendering/ oraz https://www.blender.org/features/animation/ | Web: HTTP 402 | Nie użyto deklaracji marketingowych |
| https://projects.blender.org/blender/blender-manual/src/branch/main/manual/render/cycles/render_settings/motion_blur.rst | Interfejs web: niedostępny | Raw tego samego oficjalnego repozytorium odczytany jako C32 |
| https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/color_management.rst | HTTP 404 | Nie zgadywano przeniesionej dokumentacji |
| https://documents.blackmagicdesign.com/UserManuals/FusionManual.pdf | Web: przekroczony limit treści, około 64 MB | Nie zaliczono do przeczytanych; inny poradnik sprawdził specjalista receptur R-S11 |
| https://documents.blackmagicdesign.com/UserManuals/Fusion7_Tool_Reference.pdf | Web: przekroczony limit treści, około 15 MB | Nie przyjęto starych snippetów za współczesne parametry Merge |
| https://support.apple.com/guide/motion/behaviors-keyframes-keyframe-editor-motn13746306/mac | HTTP 429, również przy jednej ponownej próbie | Wykorzystano osobno C22; host odczytał pokrewne źródło H10 |
| https://cs.uns.edu.ar/cg/clasespdf/Lasseter.pdf | HTTP 403 | Nie cytowano nieodczytanego PDF |
| https://graphics.pixar.com/library/PrinciplesTradAnim/paper.pdf | Adres niedostępny przez narzędzie | Nie zaliczono do dowodów |
| https://www.siggraph.org/education/materials/HyperGraph/animation/character_animation/principles/lasseter_s94.htm | HTTP 404 | Zastosowano odczytane C27–C28; bez deklaracji lektury Lasseter |
| https://helpx.adobe.com/after-effects/using/motion-blur.html | HTTP 404 | Właściwy aktualny rozdział odczytany jako C19 |

Nie obchodzono logowania ani paywalla. Błąd 402 narzędzia nie został zinterpretowany jako dowód, że dokumentacja Blendera jest płatna.

## Jeden przegląd merytoryczny

Pytanie 1: czy abstrakcja może odwrócić sens działania narzędzia? Wskazano sprzeczność C16 oraz poprawiono skrót opisu Merge Paths: tryb Merge tworzy compound path, inne tryby realizują operacje boolowskie.

Pytanie 2: czy liczba lub rekomendacja jest uniwersalizowana? Parametry przykładowe mają jednostki i status punktu startowego/obliczenia. Rekomendacje IBM są jawnie ograniczone do jego systemu; 24 fps nie stało się warunkiem globalnej płynności.

Pytanie 3: czy opis narzędzia jest mylony z działającą implementacją FrameMotion? Stan FrameMotion pozostaje Unknown; testy natywne NOT_RUN. Pojęcia scene graph, pól i kolejek obliczeń to adaptacje DERIVED.

## Kontrola plików

`VALIDATION.json` wiąże wynik PASS kontroli struktury ze SHA-256 CRAFT.md, GLOSSARY.md i sources.json. Potwierdzono kolejność haseł 1–100, wszystkie wymagane kolumny, 32 rekordy bez duplikacji URL, pola rejestru, obecność znaczników dowodu i kompletność definicji linków.

To kontrola pakietu badawczego dla hosta. Nie stanowi walidacji finalnego renderu ani uruchomienia Studio media delivery gate. Ostateczny pakiet użytkownika i jego kontrolę dostawy koordynuje host. Nie zwiększono liczby źródeł przez powtórne zaliczenie B43, R-S11 ani H10.

