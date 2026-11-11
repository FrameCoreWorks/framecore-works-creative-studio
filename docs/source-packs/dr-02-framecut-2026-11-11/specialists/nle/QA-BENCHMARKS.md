# DR-02 — QA, pięć benchmarków i round-trip

Data: **2026-11-11**. Dokument jest specyfikacją badań i akceptacji, nie raportem z wykonanych testów. Wszystkie benchmarki, rendery, pomiary audio/wideo, próby NLE i wymiany mają status **NOT_RUN**. Nie wygenerowano mediów testowych i nie uruchomiono pobranego kodu. Walidacja kompletności tego dokumentu jest osobną czynnością i nie zamienia NOT_RUN na PASS.

Źródła [Nxx] są opisane z URL, wersją i locatorem w [sources.json](sources.json). Własne kryteria oznaczono **PROJEKTOWE / DERIVED**; normy i udokumentowane zachowania **ŹRÓDŁOWE / SOURCED**. Specyfikacja ma rozszerzać istniejący FrameCut v1 / `fc_core.py`, a nie udawać nowy, już wdrożony silnik.

## 1. Co oznacza pozytywny wynik

Nie ma jednego testu „film poprawny”. Potrzebne są co najmniej cztery niezależne poziomy:

| Poziom | Pytanie | Dowód |
|---|---|---|
| Struktura | Czy plan, source ranges i zależności są spójne? | Validator JSON/IR, hashes, revision guards, source bounds, track/role maps |
| Wykonanie | Czy backend wykonał plan w spodziewanej wersji i konfiguracji? | Log operacji, read-back NLE, manifest renderu, kod zakończenia, rzeczywiste pliki |
| Jakość techniczna | Czy rezultat ma właściwy czas, obraz, dźwięk i format? | Pełny decode, pomiary z tolerancjami, frame/event comparison, metadata i odbiorczy import |
| Jakość redakcyjna i percepcyjna | Czy sens, emocja, rytm, ciągłość, ruch i miks są właściwe? | Ogląd i odsłuch w czasie rzeczywistym, komentarze z timecode i decyzja review |

**DERIVED.** PASS jest stanem danego kryterium w danej konfiguracji, nie obietnicą uniwersalnej kompatybilności. `render_complete=true` nie znaczy `delivery_accepted=true`. Wynik algorytmu wykrywania black/silence/cuts tworzy kandydatów do oceny, nie samodzielną decyzję o błędzie.

## 2. Wspólna definicja czasu i tolerancji

### 2.1 Kontrakt pomiaru

**PROJEKTOWE.** Dla każdego run zapisz:

`run_id`, `benchmark_id`, `fixture_revision`, `source_hashes`, `plan_revision`, `backend/version`, `adapter/version/commit`, `OS`, `fps_num/fps_den`, `start_timecode`, `drop_frame_flag`, `audio_sample_rate`, `source_time_mapping`, `timeline_range=[in,out)`, `color_profile`, `alpha_mode`, `render_profile`, `expected_counts`, `measurement_tool/version`, `decode_log`, `reviewer`, `status`, `limitations`.

Nie porównuj długości wyłącznie z zaokrąglonego `format.duration`. Oracle to liczba klatek lub rational duration oraz jawna mapa PTS/source frames. Audio ma własną siatkę próbek, lecz nie drugi niezależny zegar montażu. Zasada zaokrąglania granicy do próbek musi być deterministyczna i opisana; zaokrąglaj absolutne granice, nie dodawaj setek osobno zaokrąglonych długości.

### 2.2 Tolerancje wspólne

| Kryterium | Tolerancja | Pochodzenie i granica |
|---|---|---|
| Frame count w kontrolowanym CFR masterze | **0 klatek różnicy** względem orakla | PROJEKTOWE; nie przenosić wprost na pakiety z leader/preroll, jeśli ich zakres jest osobno zdefiniowany |
| Edity/ranges/caption bounds | **0 klatek niezamierzonego przesunięcia** | PROJEKTOWE; jawne offsety kreatywne i dozwolone rounding opisane w planie |
| PTS | Monotoniczne w kolejności prezentacji; oczekiwana siatka czasu | PROJEKTOWE; DTS przy B-frames nie jest tym samym co PTS |
| Syntetyczny audio impulse po bezstratnym cięciu PCM | **≤1 próbka** na zdarzenie względem jawnego rounding | PROJEKTOWE; dotyczy ścieżki bez resamplingu, retime i kodowania stratnego |
| A/V sync na realnych klapsach/twarzach | Cel **≤0.5 klatki** błędu względem ręcznie wskazanego zdarzenia | PROJEKTOWE, nie uniwersalny próg percepcji ani broadcast norm. Przy granicy lokalizuj niepewność zdarzenia i odsłuchaj |
| Drift | Brak rosnącego błędu; pomiary początek/środek/koniec i punkty po ripple | PROJEKTOWE; wszystkie punkty muszą spełnić swój limit, nie wystarcza średnia |
| Gaps/black/duplicate frames | Brak **nieplanowanych** zdarzeń | PROJEKTOWE; fade-to-black, freeze i nocne ujęcie mają allowlistę ranges |
| Audio clipping | Brak nieplanowanych clipped samples; true-peak ceiling według wybranego profilu | PROJEKTOWE; peak sample i true peak to różne wielkości |
| Channel layout | Dokładne mapowanie kanałów i polaryzacji względem fixture | PROJEKTOWE; napis „stereo” nie dowodzi poprawnej kolejności L/R |
| Kolor bez transformu w lossless fixture | Identyczne próbki przy tym samym pixel format/dekoderze | PROJEKTOWE; dla lossy/zmiany przestrzeni nie wymagaj byte equality |
| Test znanego transformu koloru | Golden reference i **≤1 code value** w ustalonym integer pixel format, poza jawnie opisanym ditheringiem | PROJEKTOWE; nie jest tolerancją artystycznego matching ani certyfikacją HDR |
| Metadane delivery | Dokładna zgodność z profilem: rate, dimensions, primaries/transfer/matrix/range, channels, captions | PROJEKTOWE; porównaj także piksele i odsłuch |
| Odtwarzalność | Pełny decode bez błędów oraz odtworzenie w docelowym odbiorniku | PROJEKTOWE; jeden player i poprawny nagłówek nie wystarczą |

### 2.3 Loudness: profil wybieramy, nie zgadujemy

**ŹRÓDŁOWE:** EBU R128-2023 podaje −23 LUFS; tolerancja QC ±0.2 LU uwzględnia pomiar, a ±1 LU ma inny warunek zastosowania, np. live. Ceiling −1 dBTP dotyczy produkcji linear audio; dystrybucja może wymagać niższego. [N27] Nie używaj historycznej wartości ±0.5 z changelogu jako automatycznie aktualnego kryterium.

**PROJEKTOWE:** na potrzeby benchmarków definiujemy przykładowy profil `bench_stereo_v1`: PCM stereo 48 kHz/24-bit, integrated −16 LUFS z zakresem akceptacji ±0.2 LU, true peak ≤−1.5 dBTP. To **testowy wybór**, nie specyfikacja YouTube, podcastów, kina czy reklam. Alternatywnie test ma jawnie wybrany profil odbiorcy, wtedy tamte parametry zastępują profil benchmarku. Dla B2 reklamy broadcast należy odrębnie sprawdzić odbiorcze wymagania short-form; samo R128 nie zamyka specyfikacji.

Każdy wynik podaje zakres, weighting/gating, routing i wersję miernika. EBU Mode definiuje M=0.4 s, S=3 s, I gated; testy zgodności miernika z Tech3341 nie są testami jakości miksu. [N28] Podręcznik Fairlight 20 s.617 ma rozbieżny opis Short=30 s; nie używamy go jako definicji. [N04]

## 3. B1 — wywiad, B-roll i J/L-cuty

**Status: NOT_RUN.**

**Cel:** utrzymać sens wypowiedzi, naturalne oddechy i ciągłość pomieszczenia, a B-roll wykorzystać do informacji lub świadomego pokrycia cięć.

**Dane — projekt fixture:** 8 min wywiadu CFR 25/1, oddzielny mono WAV 48 kHz/24-bit, camera scratch, 10 B-roll shots po 5–15 s, room tone, jedna błędna transkrypcja zawierająca negację, identyczne nazwy dwóch plików w różnych folderach. Własne lub odpowiednio licencjonowane źródła; źródła nie zostały pobrane ani wygenerowane. Dodać osobną syntetyczną kopię timing z widocznym frame ID i impulsem w znanych punktach.

**Operacje oczekiwane:** inventory/hash → sync → selects z odsłuchem → assembly czterech części wypowiedzi → ripple trim z linked groups → przynajmniej jeden J-cut i L-cut → B-roll overwrite na warstwie obrazu → room-tone fills i crossfades → subtitles → master + captions + DX/reference. Przykładowy output ma **90 s = 2250 klatek**. Grafika/title jest overlay; nie dodaje klatek do długości.

**Jawne zdarzenia testowe:** granica treści dialogu w frame 625, początek odpowiadającego jej obrazu w 637: J-cut o 12 klatek. Inne przejście ma obraz 1150 i zakończenie poprzedniego audio 1160: L-cut o 10 klatek. Manifest rozdziela zamierzony overlap editorial od fizycznego błędu lip-sync. Clip instances, które pokazują mówiącą twarz, nadal muszą spełnić A/V sync.

**Wynik:** wersjonowany projekt, master 2250 klatek, source map każdego słowa/ujęcia, subtitles, cue list i źródła niezmodyfikowane. Musi istnieć jawny powód usunięcia lub pozostawienia pauz.

**Testy:**

| Test | Orakl / akceptacja | Typ |
|---|---|---|
| B1-T1 źródła | Hashy nie zmieniono; kolizja filename nie podmienia dubla | PROJEKTOWE |
| B1-T2 obraz/czas | 2250 frames, cięcia w oczekiwanych granicach, poprawny B-roll po relink | PROJEKTOWE |
| B1-T3 dźwięk | Fizyczny sync wg §2; brak klików, maskowania mowy i nieplanowanej cyfrowej ciszy | Pomiary + ODSŁUCH |
| B1-T4 J/L | Offsety 12/10 frames zachowane; brak automatycznego „naprawienia” ich do zera | PROJEKTOWE |
| B1-T5 subtitles | Treść zachowuje negację, zakresy wewnątrz programu, ręcznie sprawdzony timing | Struktura + OGLĄD/ODSŁUCH |
| B1-T6 narracja | Oceniający potrafi odtworzyć główną myśl; żaden skrót nie odwraca sensu | REVIEW, nie automatyczny score |

**Negatywny test:** wycięcie słowa „nie”, automatyczne usunięcie wszystkich pauz albo relink po nazwie do innego dubla musi dać BLOCKED/FAIL konkretnego kryterium, nawet jeśli czas i LUFS są poprawne.

Źródła mechanizmów: sync i kanały [N03]; dialogue continuity [N04]. Wartości i fixture: DERIVED.

## 4. B2 — produkt/reklama z muzyką i sceną FrameMotion

**Status: NOT_RUN.**

**Cel:** czytelny produkt i obietnica, świadome akcenty muzyczne, integracja grafiki bez utraty prawidłowego czasu/koloru/alpha.

**Dane:** 12 shots produktu: CFR 25/1 i 50/1, chart/neutral reference, muzyka z cue sheet i prawami, VO, logo/font assets, zlecona scena FrameMotion. Master 1920×1080/25, adaptacja 1080×1920/25. Testowy render sceny ma **100 widocznych klatek +12 head/+12 tail =124 klatki**; visible source `[12,112)`, placement `[350,450)`. Alpha mode straight lub premultiplied musi być konkretnie podany. FPS w renderze i kontrakcie muszą być zgodne.

**Operacje:** wybór hero/product/detail przed timeline → montaż do fraz, nie każdego beatu → slow motion z 50→25 z określoną interpretacją → pojedynczy freeze 10 frames → zlecenie i odbiór sceny → compositing → reframing → VO/music automation → grade/matching → captions/legal text → dwie wersje delivery.

**Wynik:** **30 s =750 klatek** w obu aspect ratios. Master nie jest automatycznie cropem wersji pionowej. Freeze ma jawny range w allowliście. Motion version ma asset hash, scene revision, handles, color/alpha i dependency revision. Retime określa source-time mapping oraz sposób odtwarzania audio, nawet gdy audio źródłowe jest wyciszone.

| Test | Orakl / akceptacja | Typ |
|---|---|---|
| B2-T1 zegary | 750 frames; motion visible 100, render124; żadnej cichej zmiany czasu | PROJEKTOWE |
| B2-T2 alpha | Poprawny wygląd krawędzi na białym/czarnym/kolorowym tle; brak podwójnej premultiplikacji | Golden fixture + OGLĄD |
| B2-T3 retime | Anchor frames pokrywają się z planem; freeze10 i tylko w dozwolonym range | PROJEKTOWE + OGLĄD ruchu |
| B2-T4 muzyka/VO | Narracja słyszalna, brak pompowania duckingu i pops; loudness wg wybranego profilu | Pomiar + ODSŁUCH |
| B2-T5 kolor | Zgodność transformów i metadanych; matching po cutach, brak clipped logo/packshot | Metadata/scopes + OGLĄD |
| B2-T6 pion/typografia | Produkt i tekst pozostają czytelne w całym ruchu; font/proofreading zgodne | OGLĄD w docelowym rozmiarze |
| B2-T7 zmiana sceny | Wersja 120-frame visible zamiast100 wymaga jawnego rozwiązania delta20 lub rerenderu100 | PROJEKTOWE conflict detection |

**Negatywny test:** FrameMotion zwraca 124 klatki bez podania, czy zawierają handles; albo render jest 30 fps. Import nie może arbitralnie rozciągnąć go do `[350,450)`. Brak kontraktu czasu blokuje automatyczną integrację, ale nie unieważnia zaakceptowanej reszty filmu.

Źródła: zależność color pipeline/Viewer/output [N24], świadomy finishing [N05]. Parametry fixture: DERIVED.

## 5. B3 — multicam z oddzielnym dźwiękiem

**Status: NOT_RUN.**

**Cel:** zweryfikować, że zmiana kamery nie zmienia przypadkiem źródła i ciągłości audio, a sync nie jest oceniony tylko na początku.

**Dane:** 20 min master audio PCM 48 kHz/24-bit, 3 kamery 25 fps z offsetami startu +125 i −37 frames względem umownej osi; jedna kamera ma przerwę nagrania 7 s, jedna błędny TC, jedna kontrolowany clock error 50 ppm. Klaps/flashes na początku, środku i końcu. Odchylenie 50 ppm daje około60 ms w1200s — to własne wyliczenie fixture, nie pomiar urządzenia. Powtarzająca się muzyka/tło utrudnia waveform sync.

**Operacje:** wybór master clock → odczyt TC → porównanie z klapsem/waveform → sync map per segment → angle grouping → assembly → real-time switches → trims → diagnostyka drift → ewentualna, jawna korekta czasowa niezależnego nagrania → turnover z zachowaniem źródeł.

**Wynik:** 20-minutowy programme **30000 klatek**, ciągły master audio, osobne decyzje angle/video i source/audio. Przerwa w kamerze nie tworzy niezamierzonego black; zastępuje ją dostępny kąt zgodnie z planem. Niedostępny kąt jest oznaczony, a nie wypełniony cichym freeze.

| Test | Orakl / akceptacja | Typ |
|---|---|---|
| B3-T1 sync start/mid/end | Wszystkie punkty wg §2; zły TC wykryty mimo formalnie zgodnego timecode label | PROJEKTOWE |
| B3-T2 drift | Przed korektą system ma wykryć narastający błąd; po korekcie bezresztowy trend nie może być ukryty średnią | PROJEKTOWE |
| B3-T3 kąty | Video switches nie przełączają przypadkowo master mic; przerwa7s zgodna z mapą dostępności | PROJEKTOWE |
| B3-T4 sound phase | Brak comb filtering/polarity error po włączeniu dodatkowych mikrofonów | Pomiar pomocniczy + ODSŁUCH |
| B3-T5 trim/ripple | Poprawki zachowują sync groups i długość30000; niewłaściwy lock powoduje konflikt | PROJEKTOWE |
| B3-T6 round-trip | Flattened turnover zachowuje wybrane source takes/ranges, channel maps i source IDs | §8 round-trip |
| B3-T7 redakcja | Kąt służy mówcy/reakcji/działaniu; brak cięcia tylko dlatego, że wykryto zmianę diarization | OGLĄD/ODSŁUCH |

**Negatywny test:** TC zgadza się, ale zegar nagrania dryfuje; algorytm zgłasza sync na podstawie pierwszej sekundy. Taki run musi zawieść B3-T2. Nie „naprawiaj” intentional musical anticipation do klapsa, jeśli zostało osobno zatwierdzone.

Źródła: Resolve sync [N03], Premiere multicam vs merged clips [N11][N12], Avid sync locks [N19]. Tolerancje: DERIVED.

## 6. B4 — screen recording VFR i adaptacja formatu

**Status: NOT_RUN.**

**Cel:** prawidłowy czas tutorialu, czytelność interfejsu i zachowanie synchronizacji podczas przejścia z nieregularnych timestampów do CFR.

**Dane:** 6-minutowy screen recording VFR z rzeczywistymi PTS i różnymi odstępami, VO48kHz, klik/flash w znanych chwilach, mały tekst, kursor, dwie zmiany rozdzielczości w osobnych źródłach. Metadane `r_frame_rate` i `avg_frame_rate` mogą nie opisywać samodzielnie rozkładu klatek. Fixture ma także 30s statycznego ekranu i długą ciszę podczas operacji — obie oznaczone jako treść celowa.

**Operacje:** inspect timestamps → map source-time intervals → decyzja CFR30/1 → trwała mapa VFR→CFR → usunięcie oczekiwania z zachowaniem wyjaśnienia → pointer/callout overlays → ręcznie uzasadnione zoom/reframe → captions → 16:9 master i pionowa wersja z zaplanowaną zmianą układu.

**Wynik:** wersja **180s =5400 klatek CFR30/1**, z kontrolą logicznego porządku instrukcji. Oczekiwanie może być skrócone przez elipsę albo speed-up, ale krok użytkownika i wymagany rezultat muszą pozostać zrozumiałe. Output VO nie zmienia tempa przypadkowo wraz z wideo.

| Test | Orakl / akceptacja | Typ |
|---|---|---|
| B4-T1 czas | 5400 frames; mapowanie PTS zachowuje oczekiwane chwile klik/flash w tolerancji §2 | PROJEKTOWE |
| B4-T2 VFR | Raport liczby duplicated/dropped frames i ich przyczyn; brak dzielenia source index przez nominalny FPS jako jedynej mapy | PROJEKTOWE |
| B4-T3 statyczne fragmenty | Nie są błędami freeze/silence, jeżeli zapisane w allowliście i zachowują sens | PROJEKTOWE + REVIEW |
| B4-T4 reframing | Wszystkie istotne kontrolki widoczne w chwili użycia; kursor i callout zgodne | OGLĄD ruchu |
| B4-T5 napisy | Czytelność na docelowym ekranie, brak zasłonięcia przycisku w chwili kliku | OGLĄD |
| B4-T6 reset/relink | Odtworzenie mapy z fixture revision daje identyczne klatki zdarzeń | PROJEKTOWE |
| B4-T7 sens | Osoba może wykonać instrukcję; żaden usunięty krok nie jest koniecznym warunkiem kolejnego | REVIEW |

**Negatywny test:** utrzymanie nominalnego30fps przez reinterpretację bez zachowania PTS powoduje przesunięcie kliku względem VO. Nawet jeżeli finalny plik ma poprawny `avg_frame_rate`, B4-T1 musi wykryć błąd.

Mechanika VFR/FFmpeg jest rozwinięta w technicznym wkładzie głównym. Powyższe fixture, mapowanie oraz progi są DERIVED; dokumenty NLE nie służą tu jako fałszywy dowód parametru FFmpeg.

## 7. B5 — długi montaż, drift i ripple w środku

**Status: NOT_RUN.**

**Cel:** ujawnić kumulację zaokrągleń, zmianę zegara i niepełne propagowanie rewizji.

**Dane:** programme **180000 klatek przy30000/1001**, czyli **6006s =100min6s**; 48kHz PCM ma przy tej długości **288288000 próbek**. 1klatka odpowiada1601.6 próbki — lokalne rounding do1602 nie może być powtarzane bez kompensacji. Około1000 edit events, source23.976/25/29.97/30/50/59.94 z jawną polityką konwersji; mono/stereo/5.1; subtitles co kilka sekund, marker co minutę i impulse/flash co5min. Jedno ujęcie ma speed ramp, jedna scena FrameMotion oraz shoty z approved locks.

**Operacje:** ingest → normalizacja map czasu → assembly → conform → checkpoint r1 → **insert90klatek w frame90000** → jawne split crossing items i ripple właściwych tracks → propagation captions/audio/graphics → cache invalidation tylko zależnych fragmentów → r2 export → undo → reapply tej samej operation ID.

**Wynik:** r2 ma **180090 klatek**, czas6009.003s i288432144 próbek przy48kHz. Delta to90klatek =3.003s =144144próbki. Ponowne podanie tej samej idempotency key nie wydłuża drugi raz programu. Undo odtwarza semantykę r1 (zależnie od backendu niekoniecznie identyczne bajty kontenera).

| Test | Orakl / akceptacja | Typ |
|---|---|---|
| B5-T1 arytmetyka | Dokładne powyższe counts; brak kumulacji rounding | PROJEKTOWE, obliczenia rational |
| B5-T2 drift | Anchor events na początku/5min/…/końcu oraz obu stronach insert spełniają §2 | PROJEKTOWE |
| B5-T3 ripple | Każdy dependent item po insertion zmienia record time o90, chyba że ma jawną politykę fixed-time | PROJEKTOWE |
| B5-T4 crossing items | Klip/automation/caption przecinający frame90000 podlega jawnej regule split/extend/conflict | PROJEKTOWE |
| B5-T5 locks | Accepted fixed ranges nie są zmienione cicho; konflikt zgłoszony przed mutacją | PROJEKTOWE |
| B5-T6 cache | Niezmienione fragmenty zachowują dependency hash; żadnego stale render w changed span | PROJEKTOWE |
| B5-T7 idempotence/undo | Retry tej samej op nie zmienia state drugi raz; undo odtwarza expected semantic diff | PROJEKTOWE |
| B5-T8 outage | Po przerwanym renderze status incomplete; resume z checkpointu nie akceptuje częściowego pliku | PROJEKTOWE |
| B5-T9 creative review | Lokalna poprawka i nowe przejścia działają w kontekście całej sekwencji | OGLĄD/ODSŁUCH pełnego programu |

**Negatywny test:** dźwięk przesunięto144180próbek (90×1602) zamiast144144. Powstałe36próbek różnicy mają zostać wykryte w syntetycznym oracle; dopuszczenie0.5klatki realnego lip-sync nie może zamaskować precyzyjnego błędu arytmetyki fixture.

Źródła potwierdzają potrzebę sync relationships i tail check [N19] oraz kontroli reference podczas conform [N05]. Wszystkie liczby i polityki w tym benchmarku są DERIVED.

## 8. EDL, XML, FCPXML, AAF i OTIO: przenoszony model i strata

### 8.1 Cztery poziomy, których nie wolno zlać

**DERIVED:** osobno sprawdzamy (1) co potrafi format, (2) co eksportuje dany NLE, (3) co mapuje konkretna wersja adaptera, (4) co importuje/renderuje odbiorca. Dowód działania jednego poziomu nie pokrywa następnego. Zachowanie XML efektu jako opaque metadata nie jest jego wykonaniem.

| Format / trasa | Sensowna zawartość i zastosowanie | Potwierdzona granica | Sposób zachowania intencji |
|---|---|---|---|
| CMX3600 EDL | Czytelna lista eventów, reel/source/record TC, podstawowy conform | OTIO adapter: brak multi-video i nesting, brak ogólnych A/V effects; rate trzeba przekazać, default24; reelname default8. To opis adaptera, nie wszystkich EDL dialects. [N32] | Osobne EDL dla wybranych tracks, jawny rate/DF, mapa długich reel IDs i reference movie; flatten/bake z raportem |
| FCP7 XML / `xmeml` | Track-based interchange dla montażu i relink; używany także przez Premiere | Efekty NLE mogą nie być zrozumiałe downstream, np. Lumetri round-trip. [N12] README `otio-fcp-adapter` deklaruje brak transitions, ale sprawdzony kod ma reader/writer transitions; deklaracje są rozbieżne. [N33][N35] | Fixture dla konkretnego dissolve i rates, XML translation report, zachowana kopia native sequence; nie deklarować globalnego braku ani pełnego wsparcia |
| FCPXML | FCP media/resources/story elements, compound/multicam, metadata | Apple: nie opisuje całej library. `otio-fcpx-xml-adapter` README nie deklaruje transitions/effects/retime. [N13][N31] | Najpierw najmniejszy wspólny podzbiór, role map i references; nie traktować FCPXML jako FCP7 XML pod innym rozszerzeniem |
| AAF | Composition/media do sound lub conform; link/copy/consolidate/embedded według eksportera | Premiere: merged clips unsupported; Windows embedded AAF>2GB fail; inne importery poza Avid MC/PT nie były testowane przez Adobe. [N11] OTIO AAF: effects no, linear speed read-only. [N30] | Audio source+handles, dry i wet jeśli potrzebne, channel map, BiTC; użyj osobnego media folder gdy wymaga tego profil |
| OTIO `.otio` | Edytowalna reprezentacja timing/struktury/odwołań dla narzędzi pipeline | Native adapters to JSON i bundling; inne formaty są osobnymi plugins o różnym utrzymaniu. [N29] JSON nie dostarcza runtime efektów/fontów ani samych mediów w każdym wariancie | Pinuj schema/core/adapter, przechowuj pełne proprietary metadata i loss report; rendering jako odrębna warstwa |

**SOURCED — istotne kontrprzykłady:**

- Avid link-only AAF nie kopiuje mediów; consolidate kopiuje użyte zakresy z handles, video mixdown spłaszcza. [N20]
- Premiere umożliwia clean copies obok renderowanych audio clip effects; kierunek do Pro Tools i kierunek do Media Composer wymagają innego podejścia do channelization. [N11]
- AAF adapter README deklaruje markers/nesting/transitions read/write, ale brak effects i brak write linear speed. Samo wsparcie AAF przez NLE nie rozszerza tego adaptera. [N30]
- FCP7 adapter zawiera `transition_for_element` i `_build_transition_item`, a reader tworzy SMPTE_Dissolve. Istnienie kodu przeczy prostemu odczytowi README „transitions no”, lecz nie dowodzi poprawnego round-trip wszystkich transitions. [N35]

### 8.2 Co renderować i czego nie wyrzucać

**DERIVED.** Wersję baked przygotuj dla efektu, którego druga strona nie potrafi wiarygodnie odtworzyć: compositing, plugin-specific transitions, nieprzenośny retime/optical flow, stabilizacja, title/Motion/MOGRT z zależnościami, specjalistyczny grade albo audio repair. Zachowaj:

- źródło oraz wersję edytowalną;
- baked media z dokładnym visible range i handles;
- manifest efektu, render settings, color/alpha/channel interpretation;
- reference z datą i rewizją;
- loss report: co spłaszczono, co pominięto, co pozostaje Unknown.

Nie bake'uj automatycznie wszystkich kamerowych plików przed color, bo odebrałoby to odbiorcy kontrolę RAW/log i mogłoby nałożyć output transform zbyt wcześnie. Nie traktuj suchego WAV jako audialnie równoważnego wersji z approved repair. Wybór dry/wet jest częścią turnover contract.

### 8.3 Plan round-trip z minimalnym fixture

**Status wszystkich tras: NOT_RUN.** W czystym projekcie zbudować 60s fixture CFR25 i osobny wariant30000/1001, źródła z hash/TC/reel i frame ID. Fixture zawiera: video+mono+stereo, gap, J/L, marker, nested/compound, multicam, centered i edge dissolve, crop/position/rotation, keyframes opacity, freeze, linear retime, speed curve, subtitles, LUT/color transform, audio gain/pan/plugin, długi/kolizyjny reel ID i media relink.

1. Zapisz native baseline oraz referencyjny render z timecode i source ID.
2. Wyeksportuj jedną konkretną trasę, zachowaj exporter settings i translation warnings.
3. Jeśli pośrodku jest OTIO, pinuj oddzielnie core oraz każdy adapter; wykonaj `A→OTIO→B`, a nie tylko udawany round-trip JSON→JSON.
4. Importuj do nowego projektu z takim samym profilem czasu i koloru; zbierz błędy i rzeczywiste track/role/source mappings.
5. Porównaj strukturę: event count, source in/out, record in/out, rate, anchors, transition ranges, channel mapping. Identyfikatory mogą zostać zregenerowane — porównaj znaczenie, nie sam ciąg znaków.
6. Porównaj render frame-by-frame i w czasie rzeczywistym. Golden reference wymaga identycznych warunków interpretacji; kolor i kompresja nie mogą maskować błędu timing.
7. Wykonaj małą zmianę w B (np. roll+4frames), eksport B→A i sprawdź jej semantykę oraz brak dodatkowych strat.
8. Odtwórz pakiet po relokacji mediów. Nowy import nie może korzystać przypadkiem ze starego cache/proxy dostępnego w pierwotnej lokalizacji.

| Trasa | Priorytet / cel | Osobne kryterium straty |
|---|---|---|
| Resolve → AAF → Pro Tools → mix/stems → Resolve | P0 sound turnover | source metadata, channels, handles, sync, dry/wet, identyczny start/duration |
| Premiere → FCP7 XML → Resolve → XML+graded media → Premiere | P0 color conform | właściwy take, transformy, retime; brak podwójnego Lumetri/look |
| FCP → FCPXML → Resolve → FCPXML → FCP | P1 editorial exchange | story connections, compound/multicam, roles, missing Motion dependencies |
| Avid → AAF → Resolve → AAF/render → Avid | P1 finishing | reel/TC, track sync/filler, relink, handles i media folder |
| Każdy wspierany exporter → OTIO adapter → docelowy NLE | P0 dla wybranego adaptera FrameCut | jawny loss report, nie „format wspierany” jako wynik całej trasy |
| NLE → EDL → reconform | P1 awaryjny conform | rate/DF, reel collisions, track flattening, unsupported effects |

## 9. Ogląd i odsłuch: protokół osobny od pomiarów

**DERIVED.** Najpierw review ciągłe w normalnym tempie bez panelu z metrykami: sens wypowiedzi, emocja, rytm, orientacja przestrzenna, ruch, relacja obrazu i audio. Następnie review punktowe: każda granica trim/retime, krytyczne transitions, twarze, logo/legal text, captions, alpha edges, frame przed/po zmianie rewizji. Na końcu odtworzenie gotowego delivery w warunkach odbioru.

Raport punktowy zapisuje `timecode/range`, `symptom`, `expected_intent`, `severity`, `suggested_fix`, `owner`, `accepted_or_rejected`. Nie zamieniaj subiektywnej decyzji na fałszywie obiektywny score0–100. Contact sheet pomaga znaleźć kompozycję/coverage, ale nie ocenia judder, optical-flow artefacts, timing gestu czy pompowanie miksu. Transkrypcja nie odtwarza ironii i intonacji.

| Review | Pytania |
|---|---|
| Narracja | Czy widz otrzymuje informacje we właściwej kolejności? Czy elipsa nie usuwa przyczyny? Czy cytat zachowuje sens? |
| Emocja i rytm | Czy pauza/reakcja ma dość czasu? Czy muzyka nie narzuca niewłaściwego znaczenia? Czy zostawić ujęcie dłużej? |
| Ciągłość | Czy kierunek ruchu, eyeline, pozycje i hand props są zrozumiałe? Jeśli złamane — czy jest cel? |
| Ruch i kolor | Czy retime/track/maska działa przez cały shot? Czy exposure/white balance skacze na granicy? |
| Audio | Czy głos jest zrozumiały, room tone ciągły, repair naturalny; czy mono/downmix zachowuje treść? |
| Napisy/grafika | Czy treść, timing i długość ekspozycji są czytelne? Czy tekst nie zasłania informacji? |

## 10. Wymagane artefakty z przyszłego run

**DERIVED.** `fixture_manifest.json`, `timeline_before.json`, `timeline_after.json`, `operations.jsonl`, `capabilities.json`, `render_manifest.json`, `technical_qc.json`, `roundtrip_diff.json`, `loss_report.json`, `review_notes.md` i `delivery_manifest.json`. Proponowane nazwy nie są dowodem ich istnienia ani zatwierdzonym zakresem plików repozytorium.

Minimalny rekord wyniku (przykład danych, nie wykonany wynik):

```json
{
  "benchmark_id": "B5",
  "status": "NOT_RUN",
  "fixture_revision": null,
  "source_hashes": [],
  "backend_version": null,
  "technical_checks": [],
  "realtime_review": {"status": "NOT_RUN", "reviewer": null},
  "reason": "Research dostarcza specyfikację; media, aplikacje i rendery nie były uruchamiane."
}
```

Gotowość wdrożeniowa wymaga wyboru pierwszej konkretnej trasy/wersji, utworzenia legalnych fixture, uruchomienia pomiarów i review. Brak błędów dokumentacyjnych nie zastępuje tych działań.
