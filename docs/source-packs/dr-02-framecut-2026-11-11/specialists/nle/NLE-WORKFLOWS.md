# DR-02 — profesjonalny workflow NLE, audio i finishing

Data badania: **2026-11-11**. Zakres: DaVinci Resolve jako główny punkt odniesienia, Premiere Pro, Final Cut Pro, Media Composer oraz współpraca z Pro Tools, Nuke i Baselight. To wkład specjalistyczny do raportu FrameCut. Propozycje agentowe są **DERIVED**, przeznaczone do RFC nad istniejącym FrameCut v1 / `fc_core.py`; nie są opisem zaimplementowanych funkcji.

**SOURCED** oznacza ustalenie z otwartego tekstu dokumentacji lub kodu. **DERIVED** — własną syntezę/propozycję. **Unknown** — brak wystarczającego dowodu. Nie wykonano montażu ani renderowania, nie uruchomiono pobranego kodu. Wszystkie testy mediów i aplikacji: **NOT_RUN**. Rejestr pełnych URL, autorów, dat, wersji, locatorów i ograniczeń: [sources.json](sources.json). Opisy filmów na stronie szkoleniowej odczytano; filmów nie oglądano.

## 1. Zmiana wersji zmienia granice założeń

**SOURCED.** Oficjalna strona produktu prezentuje Resolve 21 i dodatkową **Photo page**. Siedem stron wymienionych w briefie pozostaje użytecznym opisem postprodukcji filmowej, ale nie jest już pełną listą stron aktualnego produktu. Materiały szkoleniowe producenta nadal opisują Resolve 20. [N01][N02]

Release note z 8 września 2026 opisuje Resolve 21.1 i integrację z asystentami Claude, Claude Code i ChatGPT Codex, m.in. analizę projektu, organizację mediów, ustawienia oraz batch rendering. Jest to deklaracja producenta, nie wynik próby tej integracji. Nie dowodzi pełnego API wszystkich operacji timeline ani jakości narracyjnej automatycznego highlight edit. [N07]

Lokalny oficjalny `Developer/Scripting/README.txt` ma datę **18 sierpnia 2025**, SHA-256 `e12622ca53930058ac41a7bfe027c12369cef62e0ddafe9a3f5027b0a5fbe337`. Potwierdza historyczny zakres API, ale nie wersję uruchomionej aplikacji. Snapshot nie może przesłonić zmian 21.1. [N08]

**DERIVED — decyzja FrameCut:** przy połączeniu z NLE zbieraj `host_version`, edycję/licencję, listę faktycznie dostępnych metod, wersję adaptera, OS i profil eksportu. Nie instaluj ani nie przełączaj aplikacji automatycznie tylko dlatego, że test capability nie przeszedł. Sam parametr `--model`, otwarcie SDK, odczyt katalogu albo informacja marketingowa nie jest sprawdzoną sesją montażową.

## 2. Pipeline: co montażysta rozstrzyga na każdym etapie

Poniższy kontrakt jest **DERIVED**, oparty na workflow szkoleniowym Resolve, turnoverach Adobe, organizacji bibliotek Apple i kontroli synchronizacji Avid. Kolejne etapy mogą zachodzić równolegle, ale właściciel nadrzędnego montażu i rewizja muszą pozostać jednoznaczne. [N03][N05][N12][N15][N19]

| Etap | Decyzja, którą trzeba podjąć | Artefakt wyjściowy i kontrola |
|---|---|---|
| Brief | Co widz ma wiedzieć/czuć; co jest obowiązkowe; do jakiego delivery pracujemy? | Jedna referencja do briefu Studio; delivery profile, constraints, owners. FrameCut nie tworzy drugiego intake. |
| Ingest | Które pliki są oryginałami, które proxy; jak sprawdzić kompletność? | Inwentarz plików, hash, wielkość, czas, kanały, rate, TC/reel, camera/log/RAW. Weryfikacja kopii; zachowane oryginały i log braków. |
| Logging/selects | Który dubel realizuje intencję; co jest tylko technicznie poprawne? | Markery i notatki z uzasadnieniem; selects/stringout zawierający również alternatywy, reakcje i kontekst. ASR jest indeksem, nie oceną tonu. |
| Assembly | Jaką kolejność informacji budujemy? | Szkielet scen; pełne wypowiedzi, ważne reakcje i dźwięk odniesienia. Jeszcze bez kosztownego dopieszczania każdego kadru. |
| Rough cut | Gdzie widz gubi sens, uwagę albo orientację? | Rewizja z czasowymi grafikami/muzyką; uwagi do ruchu, emocji, czasu i przestrzeni. Nie skracaj ciszy automatycznie. |
| Fine cut | Czy miejsce cięcia służy zmianie informacji, działaniu lub emocji? | Dopracowane trimy, J/L-cuty, continuity; jawne decyzje o retime, crop, przejściach, grafice i dźwięku. |
| Picture lock | Jaka dokładnie rewizja obrazu jest podstawą pracy downstream? | Hash/revision timeline, timebase, start TC, frame count, reference movie, accepted locks; lista jawnie otwartych VFX/tempów. |
| Turnovers | Co odbiorca musi zachować edytowalne, a co ma być baked? | Osobne pakiety sound/color/VFX, zgodne source IDs, ranges i handles; test importu przed dużą partią. |
| Sound/color/VFX | Co wymaga specjalistycznej decyzji i narzędzi? | Stemsy/mix, grade/graded shots, VFX z handles; wersja źródłowego locku w każdym manifeście. |
| Conform | Czy finalny montaż odtwarza zatwierdzone źródła, timing i efekty? | Relink do oryginałów, porównanie cut-by-cut z reference; raport mismatch i zatwierdzonych odstępstw. |
| QC | Czy plik jest technicznie poprawny i czy film działa? | Dwa raporty: pomiary/decode oraz ogląd+odsłuch w czasie rzeczywistym. Brak błędów parsera nie zastępuje żadnego z nich. |
| Delivery | Jakie dokładnie warianty są odbierane? | Master, wersje językowe/aspect/HDR/SDR, captions, stemsy, checksums, manifest profili; ponowny odczyt gotowych plików. |
| Archive | Czy inny operator odtworzy projekt za rok? | Projekt natywny, interchange, source manifest, oryginały lub jawnie określony zakres, zależności/fonty/LUT/OCIO, exporty i raport restore. |

### Ingest: trzy obiekty, których nie należy utożsamiać

**DERIVED.** `asset` to niezmienny plik/essence z hashem; `source_clip` to interpretacja źródła (kanały, TC, rate, input transform); `timeline_instance` to konkretne użycie zakresu źródłowego, z własnym położeniem i efektami. Dwa użycia tego samego WAV nie są dwoma nowymi nagraniami. Proxy może być alternatywną reprezentacją tego samego assetu, ale nie jego bezwarunkowym zamiennikiem przy finishingu.

Źródła Apple rozdzielają library database, media, cache i generated media. Dlatego backup projektu nie jest automatycznie backupem kamerowych oryginałów. Przeniesienie biblioteki z external media wymaga zebrania także zewnętrznych zależności. [N15] W Resolve clone palette służy kontroli kopii danych, a Media page przygotowaniu metadanych i synchronizacji. [N01]

**DERIVED.** Warunek dopuszczenia proxy: udokumentowana zgodność zawartości, mapy czasu, audio i interpretacji koloru. Nie wystarczy zbieżna nazwa pliku. Przy relink: hash/asset ID → reel+source TC+duration → ręczne rozstrzygnięcie kolizji. Nigdy cicha decyzja „pierwszy plik o tej nazwie”.

## 3. Siedem filmowych stron Resolve i ich odpowiedzialność

Opis funkcji jest **SOURCED**, przypisanie artefaktów FrameCut **DERIVED**. [N01][N02][N03][N04][N05]

| Strona | Model pracy | Co powinno przejść przez FrameCut |
|---|---|---|
| Media | Przygotowanie źródeł, biny/metadane, synchronizacja, kopie | Asset manifest, log braków, channel map, proxy map, sync evidence. |
| Cut | Szybkie przeglądanie i składanie; source tape, podwójny timeline, sync bin | Szybka selekcja i assembly z zachowaniem pochodzenia każdego fragmentu. Nie redukuj roli do shortsów. |
| Edit | Precyzyjne operacje ścieżek, trim, multicam, napisy i efekty | Wersjonowany plan i operacje, jasno określone ścieżki objęte zmianą i konfliktami. |
| Fusion | Node-based compositing i motion | Zlecenie konkretnego shotu/sceny; wejścia, zakres, alpha, camera/transform i handles. Nadrzędny timing nadal należy do FrameCut. |
| Color | Korekcja, matching, look, color management i finishing obrazu | Input/working/output, shot IDs, approved looks, raport conform; oddziel techniczne transformy od intencji estetycznej. |
| Fairlight | Dialogue edit, ADR, sound design, mixing, routing, mastering | Channel maps, DX/MX/FX, automatyka, buses/stems, metryki i odsłuch. |
| Deliver | Profile renderu i kolejka zadań | Zlecenie eksportu, status zadania, dokładny profil, checksums i niezależny QC wynikowych plików. |

Photo w 21 jest dodatkową stroną dla fotografii. Nie należy na siłę dodawać jej jako obowiązkowego kroku każdej produkcji filmowej. [N01]

## 4. Cztery NLE: różnice decyzji, nie ranking przycisków

| Obszar | Resolve | Premiere Pro | Final Cut Pro | Avid Media Composer |
|---|---|---|---|---|
| Organizacja | Projekt/media pool/biny/timelines; postprodukcja w jednym środowisku | Projekty/biny/sequences; Productions dzieli duży projekt na współpracujące projekty | Library → events → clips/projects; managed lub external media | Biny, master clips i sequences; silna rola organizacji materiału oraz shared bins |
| Logika montażu | Track-based Edit; szybkie assembly Cut | Track-based sequences; source/target i nesting wymagają jawnego zarządzania | Magnetic Timeline; układ połączeń i roles ma znaczenie semantyczne, nie jest tylko wyglądem ścieżek | Source/Record, segment edits, single-/dual-roller trim; sync locks działają na ścieżkach |
| Kluczowe ryzyko ripple | Niewłaściwy zakres ścieżek i niezależne elementy downstream | Rozbieżne source patching/targeting i sync-lock; ukryte nested dependencies | Błędne kotwiczenie connected clip może przenieść właściwą grafikę wraz z niewłaściwym fragmentem | Sync lock może dodać filler lub oddziaływać na inne segmenty; lock i sync lock to różne rzeczy |
| Produkcja zespołowa | Wspólna logika projektu; szczegóły współbieżności wymagają testu danego hosta | Productions: prawo zapisu związane z project lock, pozostałe projekty można odczytywać | Świadome kopiowanie/exchange projektów i bibliotek; wspólne media nie dowodzą równoczesnego zapisu tej samej biblioteki | Shared bin locking; nawet zielona ikona nie zawsze dowodzi posiadania locku |
| Synchronizacja | Dailies z timecode lub audio; jawne mapowanie kanałów | W profesjonalnym turnover workflow preferowane multicam source sequences zamiast Merge Clips | Multicam/synced clips; role-based components mogą zmieniać downstream routing | Synchronizacja i kontrola out-of-sync, head/tail reference, zachowanie track relationships |
| Finishing | Color, Fusion i Fairlight w jednym projekcie zmniejszają liczbę przekazań | Lumetri + Dynamic Link/After Effects/Audition lub zewnętrzny turnover | Role/stems, Motion templates, FCPXML do partnerów | AAF do sound, conform i kolor w Avid lub zewnętrznym finishingu |
| Koszt wymiany | Natywne `.drt/.drp/.dra` utrzymują kontekst Resolve; eksport ogólny wymaga conform | XML i AAF przenoszą różne podzbiory; efekty mogą przejść jako nieinterpretowane dane | FCPXML nie zastępuje natywnej library; Motion dependencies muszą być dostępne albo baked | Link-only AAF nie transportuje mediów; consolidate wymaga handles |

Podstawa **SOURCED**: Resolve [N03][N05]; Premiere [N11][N12]; FCP [N13][N14][N15][N18]; Avid [N19][N20]. Oceny ryzyka i wybór praktyki dla FrameCut są **DERIVED**.

### Trzy konkretne konsekwencje dla agenta

1. **Ripple nie znaczy „przesuń wszystko w prawo”.** W Avid sync-lock obejmuje całe wskazane ścieżki i może wstawić filler dla utrzymania synchronizacji. Dual-roller trim nie ma takiej samej semantyki zmiany długości jak single-roller. [N19] FrameCut musi wymagać jawnej polityki ścieżek, linked groups, anchors oraz materiału crossing edit point; nie wystarcza `delta`.
2. **Przygotowanie sync zależy od turnoveru.** Adobe opisuje utratę metadanych audio przy Merge Clips, a bieżąca dokumentacja AAF mówi wprost o braku obsługi merged clips. [N11][N12] Dla materiału planowanego do Pro Tools wybór sposobu sync musi nastąpić przed montażem kilkuset ujęć.
3. **Role nie są ścieżką.** Apple wykorzystuje roles/subroles do organizacji komponentów audio i eksportu; iXML może dostarczyć nazw subroles. [N14] Adapter nie może dowodzić zachowania DX/MX/FX samym zgodnym indeksem tracku.

## 5. Poprawki po picture lock: utrzymaj historię decyzji

Adobe definiuje change list jako różnice między wersjami sequence potrzebne do aktualizacji sound edit; format należy uzgodnić z odbiorcą. Zaleca test turnover na rzeczywistym materiale na początku produkcji. [N12] Resolve Color Guide wymaga reference movie i kontroli kolejnych cięć podczas conform. [N05]

**DERIVED — procedura rewizji:**

1. Zachowaj `lock_r12`; utwórz `revision_r13` z `parent_revision=r12`, powodem i dokładnym zakresem zmiany.
2. Rozdziel: **picture change** (inna zawartość w tym samym czasie), **duration change** (ripple), **format/grade change**, **sound-only change**. Mogą mieć różny wpływ na downstream.
3. Zapisz old/new source ranges, old/new record ranges, różnicę długości, affected IDs, przeniesione captions/graphics/audio cues, status handles i efekty wymagające rebake.
4. FrameMotion otrzymuje nową długość lub żądanie zachowania długości istniejącej sceny. Nie rozciągaj całego renderu grafiki bez decyzji o rytmie i jakości ruchu.
5. Sound dostaje change list, nowy reference z revision+TC, zaktualizowany AAF i oddzielny wykaz sound-only zmian. Sam nowy full mix nie pozwala automatycznie odtworzyć edytowalnej sesji.
6. Color/VFX otrzymują listę nowych/zastąpionych shotów i wymaganych source handles. Nie podmieniaj pod starym filename nowego obrazu o innej tożsamości.
7. Sprawdź lokalne sąsiedztwo zmiany i wszystkie zależności downstream; przy zmianie długości także koniec programu, tail sync, captions i automatyki.
8. Zaakceptowane niezmienione fragmenty zachowują swoje acceptance records. Nowy lock jest nadawany jawnie; historycznej akceptacji nie przepisuje się na nową treść.

Kontrprzykład: ścieżka muzyki jest celowo zakotwiczona do absolutnego końca emisji. Globalny ripple, choć zachowa relację większości klipów, naruszy ten warunek. Validator powinien zgłosić konflikt między fixed-duration delivery a wstawieniem, zamiast samodzielnie przyciąć końcówkę.

## 6. Audio zawodowe: od intencji sceny do mierzalnego eksportu

**SOURCED.** Dialogue edit obejmuje także production sound i płynne tło między wypowiedziami; nie ogranicza się do odszumiania. Fairlight guide opisuje wykorzystanie lepszego źródła, porządkowanie tracks i uzupełnianie przerw ambience. [N04] Resolve ma udokumentowany preset AAF dla Pro Tools i reference video z burned-in timecode. [N03]

**DERIVED — porządek pracy:**

| Problem | Decyzja i działanie | Kontrprzykład / kontrola |
|---|---|---|
| Niewyraźny dialog | Posłuchaj izolowanych mikrofonów, wybierz dubel/kanał, sprawdź sync; dopiero potem repair | Dodanie gain do przesterowanego wejścia nie odzyskuje informacji; AI może zmienić spółgłoski. |
| Klik na cięciu | Dopasuj granicę i krótki crossfade w domenie próbek | Długi crossfade nakładający dwie sylaby pogarsza czytelność. |
| Skok ambience | Room tone odpowiadający miejscu i mikrofonowi, płynne przejście; zostaw naturalny oddech | Cyfrowa cisza między zdaniami brzmi sztucznie; loop może ujawnić powtarzający się szczegół. |
| Boom + lav | Oceń fazę i opóźnienie; wybierz jedno źródło lub świadomie wyrównaj/miksuj | Zsumowanie obu może dać comb filtering mimo lepszego mierzonego poziomu. |
| Muzyka zasłania głos | Dobierz fragment i aranżację, gain automation, ewentualnie sidechain/ducking | Ducking przy każdym oddechu może pompować; redukcja całego pasma nie zawsze jest potrzebna. |
| Duża zmienność mowy | Clip gain przed kompresją, następnie EQ/dynamics według problemu | Jeden preset na różne mikrofony pogłębia różnice; zbyt duża kompresja odbiera emocję. |
| SFX/Foley | Spotting po intencji i ruchu, perspektywa, synchronizacja, decay | Synchronizacja maksimum waveform nie zawsze odpowiada percepcyjnemu momentowi zdarzenia. |
| Master i wersje | Jawny routing DX/MX/FX, stemsy, full mix; wspólny start i długość | Sumowanie stems może nie odtwarzać mastera przy nieliniowym processingu wspólnego busa. |

Fairlight może bounce'ować buses do mixu i stems; przewodnik pokazuje osobne DX i M&E oraz sprawdzanie kanałów odsłuchem. [N04] **DERIVED:** manifest stemów musi opisywać punkt pobrania sygnału, channel order, sample rate, bit depth, applied processing oraz to, czy sumowanie ma być sample-identical z full mixem. Jeśli nie — podaj przyczynę i dostarcz referencję.

### Miernik nie wybiera estetyki i nie słyszy błędnego słowa

W profilu EBU R128-2023 target wynosi −23 LUFS, dopuszczenie ±0.2 LU dla QC odnosi się do błędu pomiaru, a ±1 LU do sytuacji, gdy praktyczne trafienie w target jest niemożliwe, np. live. Maksymalny true peak w produkcji linear audio to −1 dBTP; system dystrybucji może wymagać niższego. To nie jest uniwersalny target internetowy. [N27]

Momentary w EBU Mode ma okno 0.4 s, Short-term 3 s, Integrated używa gating. [N28] **Rozbieżność:** Fairlight guide 20 s.617 zawiera opis Short jako 30 s; nie przyjmujemy go jako definicji metryki. Normatywny opis miernika pochodzi z EBU. [N04][N28]

**DERIVED:** raport zawsze zapisuje profil, zakres pomiaru i routing. Mierzyć należy gotowy plik po ostatnim kodowaniu, ponieważ wynik na busie nie dowodzi właściwości zakodowanego delivery. Odsłuch sprawdza artefakty repair, maskowanie, pompowanie, ucięte oddechy, sybilanty, tonalność oraz właściwe znaczenie wypowiedzi.

### Pro Tools jako partner sound department

AAF + audio + reference movie to sensowny interfejs między picture edit a edytowalną sesją sound; wymaga ustalenia handles, kanałów i tego, czy efekty są baked. [N03][N11][N20] Pro Tools posiada language-independent Scripting SDK, ale pobranie szczegółowej dokumentacji prowadzi przez umowę licencyjną. Nie zaakceptowano jej ani nie pobrano SDK. Zakres konkretnych metod w tym badaniu pozostaje **Unknown**. [N23] Własny adapter powinien rozpoczynać się od importu pakietu i walidacji, nie od deklaracji „automatyczny profesjonalny mix”.

## 7. Kolor, VFX i finishing: zachowaj znaczenie pikseli

**SOURCED.** Color management nie usuwa potrzeby balansowania i matching ujęć. Nieznany camera/log może wymagać kontaktu z twórcą; sama etykieta pliku nie musi wystarczyć. [N05] Nuke rozdziela transform wejściowy, working space, Viewer transform i output; Viewer transform służy podglądowi i nie zmienia danych obrazu. [N24]

**DERIVED — kolejność decyzji:**

1. Zidentyfikuj format, transfer/primaries/matrix, data range, camera/log/RAW i transformy już zapisane w pikselach. Brak danych = Unknown, nie automatyczne Rec.709.
2. Ustal working space i metodę zarządzania kolorem; podaj konfigurację OCIO/ACES, DRT albo CST wraz z wersją.
3. Oddziel normalizację techniczną od looku: transform wejściowy ≠ kreatywny LUT; LUT nie odtwarza całego grade z kluczami, maskami i trackingiem.
4. Conform do oryginałów. Potwierdź shot ID, source/time range, retime, crop/scaling, orientation i pozostałe transformy.
5. Skoryguj ekspozycję, balans i kontrast; dobierz shot anchors dla scen, dopasuj pozostałe ujęcia w kontekście montażu.
6. Oceniaj twarze i obiekty w kontekście intencji oświetlenia. Nie każda twarz ma mieć ten sam odcień lub poziom waveform.
7. Stosuj look na stabilnej bazie; sprawdź temporal consistency, maski i trackery w ruchu.
8. Wymieniaj VFX z jawnym color space, alpha mode, rozmiarem, pixel aspect, frame range i handles. EXR z alphą wymaga zgodnej interpretacji straight/premultiplied.
9. Oceniaj każdą docelową wersję SDR/HDR na właściwym torze monitoringowym. Zmiana output transform nie daje automatycznego zatwierdzenia artystycznego trim pass.
10. Sprawdź obrazy i metadane finalnego pliku: poprawny tag nie naprawia źle przeliczonego obrazu; poprawny wygląd w jednym playerze nie dowodzi poprawnego tagowania.

| Narzędzie specjalistyczne | Potwierdzona rola | Granica dla FrameCut |
|---|---|---|
| Resolve Color/Fairlight/Fusion | Zintegrowane obszary finishingu, gradingu, audio i VFX [N01] | Pozostaw decyzje timeline w jednym ownerze; stan stron nie tworzy konkurencyjnych briefów. |
| Nuke | Węzłowe przetwarzanie, Python CLI: `-t`, `nuke.execute`, render zakresów; opis w wersji 14.0 [N25] | Backend shotów, nie automatycznie zamiennik całego editorial. Potrzebuje Nuke/runtime/licencji; bieżącej zgodności 16.x nie dowiedziono. |
| Baselight / Editions | Wspólne dane grade i Truelight; v7 Editions dla Avid/Nuke pozwala odczytać/renderować grades, edycja ma inny zakres licencji [N26] | BLG to współpraca w określonym ekosystemie. Nie dowodzi interpretacji BLG przez FFmpeg ani bezstratnego transferu do każdego color engine. |
| Pro Tools | Sound post oraz SDK automatyzacji [N23] | Zachowaj źródłowe audio i edytowalny turnover; nie spłaszczaj sesji przed uzgodnieniem potrzeb miksera. |

**Kontrprzykład z dokumentacji:** Lumetri zapisany w XML może być ignorowany przez system color, lecz wrócić do Premiere i nałożyć się na już wyrenderowany grade. [N12] Round-trip musi sprawdzać obraz i stack efektów; samo zachowanie metadanych efektu nie znaczy zachowania jego wykonania.

## 8. Skryptowanie: potwierdzony zakres i warunki wykonania

| Platforma | Co odczytano | Czego z tego nie wolno wywnioskować | Decyzja adaptera |
|---|---|---|---|
| Resolve | Python/Lua oraz workflow integration JS według Studio page. Lokalny README: `GetVersion`, `AppendToTimeline` z source frames/recordFrame/trackIndex, `ImportTimelineFromFile`, `DeleteClips(..., ripple)`, track locks, render queue/status; `-nogui` nadal uruchamia Resolve. [N06][N08] | API nie jest niezależną biblioteką renderującą; lista metod z 2025 nie dowodzi wszystkich operacji w 21.1. | Capability probe, staging timeline, read-back po mutacji, render status i plikowe QC. Siedem klasycznych nazw w starym `OpenPage` nie dowodzi braku Photo w 21. |
| Premiere Pro | UXP DOM; wywołania metod asynchroniczne, minimum version per member. `SequenceEditor` od 25.6: insert/overwrite/remove-ripple/clone. `Project.executeTransaction` jest undoable; `lockedAccess` chroni stan callbacku. [N09][N10][N34] | Nie jest headless rendererem bez Premiere. Istnienie action nie dowodzi wszystkich ripple edge cases. | Jedna operacja FrameCut → kontrolowany compound action; błąd/false → przerwij i odczytaj rzeczywisty stan. Pinuj minimum wersji metod, nie tylko major hosta. |
| Final Cut Pro | FCPXML wymienia media/timing/decyzje; nie pełną library. Workflow Extension wymaga container macOS app. SDK obserwuje sequence/range/playhead i potrafi przesunąć playhead. [N13][N16][N17] | Odczyt proxy timeline nie dowodzi API dowolnego trim/insert/roll. Stara dokumentacja Apple Events Final Cut 7 nie jest dowodem aktualnego FCP. | Generowanie/odczyt FCPXML oraz weryfikacja w FCP; extension dla kontekstu i feedbacku. Dodatkowe mutacje: Unknown do osobnego potwierdzenia. |
| Avid Media Composer | Extensions SDK integruje narzędzia z projektem/binem/timeline; AMA/AVX/Open I/O mają odrębne funkcje, a komercyjne użycie toolkitów podlega licencji. [N21][N22] | Ogólna strona SDK nie dowodzi otwartego Python DOM ani konkretnej metody ripple. MediaCentral API nie jest automatycznie API desktopowego timeline. | Najpierw AAF/EDL i walidacja w docelowym MC; Extensions jako osobny spike po dostępie do właściwej dokumentacji/licencji. |

**DERIVED — semantyczne poziomy obsługi:**

- **Wierny odpowiednik:** tylko operacja z potwierdzonym mapowaniem czasu/ścieżek i pozytywnym fixture w danej wersji backendu. Na dzień researchu nie nadano takiego statusu żadnemu wykonanemu testowi.
- **Przybliżenie:** np. zastąpienie specjalistycznego transition prostym cross-dissolve, wyłącznie jako jawna propozycja.
- **Hybrydowy:** FrameCut utrzymuje edytowalne decyzje, NLE/DAW/finishing renderuje efekty, wraca manifest + reference + QA.
- **Brak potwierdzonego praktycznego odpowiednika:** nieopisane API, niedostępny plugin lub wymaganie jakości nieosiągalne w wybranej trasie. Fallback: zachowaj projekt i przygotuj konkretny turnover, bez cichej utraty funkcji.

**DERIVED — retry i koszt:** read-only queries mogą mieć ograniczony retry na przejściowy błąd. Mutacje wymagają idempotency key/revision guard i read-back przed ponowieniem. Przerwany render nie jest gotowym artefaktem. Runtime NLE, komercyjne plugins i licencje to warunki dostępności; nie uruchomiono zakupów, triali ani płatnych usług.

## 9. Mapa szkoleń: umiejętność → ćwiczenie → dowód opanowania

Własne ćwiczenia poniżej są **DERIVED**; nie są kopiami kursów. Status wykonania wszystkich: **NOT_RUN**. „Odczyt” dotyczy tekstu wskazanego źródła, a nie obejrzenia jego filmów.

| Źródło i locator | Konkretna umiejętność | Własne ćwiczenie i warunek ukończenia | Zakres sprawdzenia |
|---|---|---|---|
| Editor’s Guide 20, rozdz.1–3 [N03] | Assembly, refinement, wybór dubla, split edits | Zmontuj jedną scenę w dwóch rytmach; uzasadnij trzy różnice bez zmiany sensu | Odczyt spisu treści; szczegóły dramaturgii rozwija osobny rozdział craft |
| Editor’s Guide 20, s.267–270 [N03] | Dailies sync, kanały scratch/production | Zsynchronizuj dwie kamery i rejestrator; wskaż dowód start/end i używany mikrofon | Odczyt właściwego fragmentu |
| Editor’s Guide 20, rozdz.4 i 7 [N03] | Multicam, speed changes, freeze | Zachowaj ciągły master audio podczas zmian kąta; odróżnij retime i interpretację FPS | Spis treści; dalsze wykonanie/lektura ćwiczeń wymagane |
| Editor’s Guide 20, s.548–551,608–610 [N03] | Turnover AAF, BiTC, ponowny odczyt eksportu | Wyeksportuj reference i AAF do czystego projektu; porównaj źródła i sync | Tekst rozdziałów, bez wykonania |
| Fairlight 20, s.82; rozdz.2 [N04] | Dialogue editing i ciągłość ambience | Zmontuj rozmowę z różnymi mikrofonami; słuchacz nie powinien słyszeć niezamierzonych zmian tła | Odczyt s.82; pozostałe ćwiczenia wskazane w TOC |
| Fairlight 20, rozdz.8–10, s.616–618,627–629 [N04] | Routing, automation, full mix/stems, pomiar | Dostarcz DX/MX/FX/full mix z jawnymi buses, kanałami i metrykami | Odczyt TOC i wskazanych stron; definicje metryk korygowane EBU |
| Colorist Guide 20, s.151–154,164–165,176 [N05] | Offline reference, conform, camera originals, ograniczenia automatyki | Wykryj podmieniony take, błędny TC i podwójny transform w kontrolowanym projekcie | Odczyt właściwych fragmentów |
| Blackmagic Training: Multicam Editing, Color Management, Fairlight, Fusion [N02] | Kolejny etap nauki narzędzi w ruchu | Po obejrzeniu odtwórz ćwiczenie na własnych mediach i zapisz wersję Resolve | **Odczyt opisów; filmy nieobejrzane**, brak własnych timestampów |
| Adobe Best Practices, s.6–7,59–60,117–120 [N12] | Productions, multicam sync i zawodowy turnover | Przygotuj dwa projekty w Production i turnover bez utraty source audio metadata | Odczyt PDF; dokument 2022, landing page 2026 |
| Apple Audio Roles, s.5–9; Media Management, s.4–7 [N14][N15] | Semantyczny routing i zależności library | Nadaj iXML/subroles, wydaj stems i odtwórz bibliotekę po odłączeniu original location | Odczyt fragmentów; white papers 2020 |
| Avid Editing Guide 2025.x, s.493,633; shared-bin caveat s.304 [N19] | Trim/sync locks i współpraca | Wstaw 24 klatki w środek sequence; sprawdź filler i tail sync na różnych locks | Odczyt fragmentów; bez UI |
| EBU R128 i Tech3341 [N27][N28] | Rozdzielenie targetu, tolerancji pomiaru i metryki | Zmierz ten sam plik niezależnymi miernikami i wyjaśnij różnice | Odczyt norm; sygnałów testowych nie wykonano |
| Foundry color workflow i Nuke CLI [N24][N25] | Viewer vs output; zakres renderu shotu | Ten sam patch/render przy ustalonej OCIO config, kontrola alphę i frame count | Tekst dokumentacji; brak renderu |
| FilmLight Editions [N26] | Oddzielenie przenoszenia grade od baked media | Porównaj reference BLG/render w docelowym hostcie | Tekst producenta; nie odbyto kursu ani trialu |

## 10. Pokrycie i luki tego wkładu

| Zakres | Status |
|---|---|
| Ingest → archive, cztery NLE, siedem stron + aktualizacja Photo | SYNTHESIS_COMPLETE, źródła przeczytane w oznaczonym zakresie |
| Audio, color, VFX/finishing, post-lock changes | SYNTHESIS_COMPLETE; monitor, odsłuch, render i zgodność delivery NOT_RUN |
| Resolve API | Lokalny dokument 2025 + aktualne strony 21/21.1; aktualny runtime Unknown |
| Premiere API | UXP docs, konkretne klasy/metody; runtime NOT_RUN |
| FCP API | Wymiana i ograniczone timeline interactions potwierdzone; pełne mutacje Unknown |
| Avid API / Pro Tools methods | Istnienie SDK potwierdzone; szczegółowe API za dodatkowym dostępem/licencją nieprzeczytane |
| Szkolenia wideo | Wyłącznie opisy; żadnego twierdzenia o obejrzeniu |
| Źródła praktyków | Ten wkład opiera się na dokumentacji producentów; niezależną praktykę i dramaturgię rozwija specjalista craft |
| Testy mediów, NLE, round-trip, benchmarks | NOT_RUN; kompletna specyfikacja w [QA-BENCHMARKS.md](QA-BENCHMARKS.md) |

Otwarte wdrożeniowo: feature probes per host, trial turnover z realnymi źródłami, mapowanie frame/time/channel/role, polityka baked effects, wersje OCIO/LUT/fonts, arbitraż post-lock zmian i kontrakt restore. Nie dopisano tutaj implementacji do repozytorium ani nie zmieniono istniejących skilli.
