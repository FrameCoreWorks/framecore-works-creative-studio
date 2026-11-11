# Profesjonalne modele pracy ponad jednym programem

Data: 2026-11-11. **DERIVED** oznacza proponowaną metodę pracy. Natywne sesje programów i porównania renderów: **NOT_RUN**. Ten rozdział uzupełnia szczegółowy warsztat i receptury; nie jest rankingiem zakupowym.

## Wybór modelu do problemu

| Problem twórczy | Model pracy | Co zyskuje autor | Co musi jawnie kontrolować agent | Wierność przeniesienia |
|---|---|---|---|---|
| Logo/type, timing wielu warstw | AE: kompozycje, warstwy, hierarchie, animatory | Czytelny podział na klipy i właściwości | Kolejność efektów, transformacji i rasteryzacji; anchor/parent vs opacity | Transformacje wierne w zawężonym modelu; efekty i font raster przybliżone |
| Łączenie plate, key, roto i render passes | Fusion: przepływ węzłów | Widoczne pochodzenie kanałów i gałęzie obróbki | Co jest obrazem, maską, geometrią i kamerą; punkt przejścia 3D→2D | Hybrydowy workflow; nie spłaszczać DAG do przypadkowej listy CSS |
| Powtarzalna animacja parametrów i szablon FCP | Apple Motion: behaviors + keyframes + rig | Parametryzacja zachowania bez ręcznego kluczowania każdego przebiegu | Efekty złożonego zachowania i kolejność ewaluacji | Przybliżenie lub bake; nazwa behavior nie jest specyfikacją równania |
| Setki klonów reagujących przestrzennie | Cinema 4D: Cloner, Effectors, Fields | Wzór zachowania zamiast ręcznego animowania obiektów | Indeks/pozycja klonu, pole wpływu, czas i cache | Wierny dla jawnej prostej funkcji; hybrydowy dla symulacji/renderu |
| Geometria, światło, kamera i fizyczny materiał | Blender: scena 3D, Geometry/Simulation Nodes, renderer | Relacja głębi, geometrii i światła w jednym świecie | Jednostki, focal length/sensor, color transform, depsgraph i bake | Workflow hybrydowy; web shader nie oznacza równego wyniku Cycles |
| Compositing zależny od kanałów i alpha domain | Nuke: jawne węzły i kanały | Rozdzielenie naprawy matty, RGB oraz transformów koloru | Premult state, edge colors, zero-alpha policy | Wierna algebra w uzgodnionej domenie, render wymaga testu |
| Cząstki/dynamika zależna od historii | Houdini: proceduralne SOP/DOP + cache | Rozdzielenie geometrii, stanu solvera i obrazu | Kroki czasu, seed, wersja solvera, stan i unieważnianie cache | Hybrydowy bake; brak praktycznego prostego CSS odpowiednika |

Podstawy AE/Motion/C4D i Fusion są rozwinięte w `specialists/craft/CRAFT.md` i `specialists/recipes/RECIPES.md`; konkretne źródła i odczyty są w rejestrze. Powyższe decyzje o adapterach są syntezą, nie obietnicą istniejącej funkcji FrameMotion.

## Case: behavior to nie drugi zestaw keyframes

**SOURCED H10:** Apple opisuje składanie wpływu behavior i keyframes na tę samą właściwość, z określoną kolejnością operacji. [Apple, Combining behaviors with keyframes](https://support.apple.com/en-gb/guide/motion/motn13743116/mac), wersja dokumentacji live, dokładny numer aplikacji Unknown.

**DERIVED:** w specyfikacji zapisać bazową ścieżkę i modulację osobno: `position = authoredPath(t) + lowFrequencyOffset(t)`. Randomize na każdym sample nie może stać się nieskontrolowanym drżeniem liter. Jeżeli eksport nie potrafi odtworzyć behavior, bake wartości z częstotliwością wystarczającą dla zakładanej krzywej, a potem porównaj międzyklatkowe próbki do motion blur. **Kontrprzykład:** przy symulacji kolizji prosty wzór sumy offsetów nie zachowuje kontaktów; wymaga bake albo natywnego wykonania. **Test:** zmienić tylko amplitudę offsetu, potwierdzić niezmienione punkty głównej trajektorii/impactów; brak testu medialnego tutaj.

## Case: pole wpływu i klony

**SOURCED H09:** MoGraph Cache zapisuje transformacje klonów z wpływem effectorów; dokumentacja wymienia Delay, Team Render oraz wolny podgląd jako sytuacje do bake. Zastosowanie cache proxy do złożonego obiektu może nie oddawać dokładnie jego kolizji. [Maxon, MoGraph Cache, C4D 2026](https://help.maxon.net/c4d/2026/en-us/Content/html/TMOGRAPH_CACHE.html).

**DERIVED:** agent projektuje „fala odsłania siatkę danych”, a nie „animuj 500 obiektów”. Dane to stabilne `instance_id`, układ pozycji i pole `weight(x,t)`. Kolor/skala/opóźnienie są funkcjami tej wagi. **Kontrprzykład:** indeks instancji zmienia się po usunięciu jednej komórki, więc animacja wszystkich następnych przesuwa fazę. Użyć stabilnych identyfikatorów, a kolejność uznać za zamierzoną część danych. **Test:** usunięcie jednego punktu nie przelosowuje reszty, chyba że brief żąda reflow.

## Case: compositing jest operacją na danych obrazu

**SOURCED H07:** w Nuke `Premult` mnoży RGB przez alpha, a typowy Merge oczekuje tej reprezentacji. Dokumentacja zaleca rozpakowanie premultiplication przed odpowiednią korekcją i ponowne premult przed Merge. [Foundry, Premult](https://learn.foundry.com/nuke/content/reference_guide/merge_nodes/premult.html).

**DERIVED:** specyfikacja nie może przechowywać wyłącznie „PNG ma alpha”. Musi podawać interpretację kanałów na wejściu i wyjściu operacji. Dla premult over: `Co = Cs + Cd*(1−As)` i `Ao = As + Ad*(1−As)`. Tu Cs/Cd są już premult i w tej samej przestrzeni roboczej. **Kontrprzykład:** ponowne mnożenie już premult RGB przyciemnia krawędzie; automatyczne unpremult przy alpha≈0 może spotęgować śmieci RGB. **Test:** syntetyczna czerwona warstwa alpha=0.5 nad niebieskim nieprzezroczystym tłem daje premult RGB=(0.5,0,0.5), alpha=1 w liniowej domenie; to test algebraiczny, nie wyglądu zakodowanego sRGB. Przyjęta polityka alpha=0: RGB=0 dla tego fixture.

## Case: bake nie znaczy „zapisz MP4”

**SOURCED H08:** Houdini odróżnia cache SOP/geometrii od stanu DOP; ograniczona pamięć może usuwać wcześniejsze klatki. [SideFX, Caching simulations, nagłówek 22.0](https://www.sidefx.com/docs/houdini/dyno/cache).

**DERIVED:** trzy warstwy cache mają inne klucze i zastosowania: (1) solver checkpoint pozwala wznowić symulację, (2) geometry bake pozwala ponownie ustawić kamerę, (3) RGBA frame cache pozwala ponownie skompresować film. Zmiana kamery unieważnia (3), ale niekoniecznie (1)/(2); zmiana seed unieważnia wszystkie zależne warstwy. **Kontrprzykład:** cache geometrii nie wystarcza, jeśli shading czy motion blur wymagają velocity, deformacji lub subframes, których nie zapisano. **Test:** seek 0→150→30→150 i porównanie stanu transformacji; resume po przerwaniu w połowie; osobno ocenić sample shutter. To specyfikacja, NOT_RUN.

## Transfer między modelami bez utraty intencji

Oryginalna specyfikacja kreatywna powinna mówić: „znak odsłania się zgodnie z konstrukcją, główna część czytelna przy cue, potem spokój”. Adapter może zrealizować to Trim Paths, maską w SVG albo natywnym node graph. **Kryterium wierności** to zachowana geometria, kolejność ujawniania, impact, reading hold i prawa assetów; nie identyczna nazwa efektu. Ograniczenia backendu ujawniamy przed buildem.

Gdy brakuje odpowiednika: zachować editable native project i prerender RGBA wraz z color/alpha/profile/handles. Jeśli odbiorca nie wspiera alpha lub trybu koloru, owner wybiera wspólnie zatwierdzone spłaszczenie albo zmianę backendu. Sam agent nie dodaje tła, nie zmienia długości filmu i nie podmienia fontu, by pozornie zamknąć zadanie.
