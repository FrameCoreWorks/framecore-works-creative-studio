# DR-01 — proces zawodowy, feedback i mapa nauki

Data badania: **2026-11-11**. Zakres: warsztat i proponowana adaptacja do FrameMotion. Tekst nie potwierdza aktualnej implementacji wtyczek. Własne przykłady i procedury są **DERIVED**. Przeczytano dokumentację, artykuły i wskazany fragment transkrypcji; **żaden film ani płatny kurs nie został obejrzany, żaden tutorial nie został odtworzony w programie**. Wszystkie proponowane ćwiczenia: **NOT_RUN**.

## P-STAGES — najpierw ustalić, co oceniamy

**PRACTITIONER / SOURCED:** Ryan Plummer rozdziela materiał koncepcyjny, storyboard/styleframes, animatic oraz rough animation. Jego tekst dopuszcza iteracje między etapami. Nie jest to liniowa lista wymagana dla każdej produkcji. [R-S14 — A Guide to Completing Your Motion Design Project](https://schoolofmotion.com/blog/guide-completing-motion-design-project).

**PRACTITIONER / SOURCED:** Joey Korenman w odczytanym fragmencie transkrypcji *Making Giants* przedstawia zarówno start od idei, jak i start od wizualnego eksperymentu, dla którego szuka kontekstu. To opis jego filmu, nie dowód, że próba nowego efektu sama tworzy dobrą historię. Przeczytano transkrypcję 00:11–04:58; wideo **NOT_VIEWED**. [R-S15 — Making Giants, Part 1](https://schoolofmotion.com/blog/making-giants-idea).

Poniższy przebieg jest własną propozycją dla agentów. Oddziela pytania, które warto rozwiązać wcześnie, od decyzji zależnych od rzeczywistego odtwarzania. Nie jest opisem działania obecnego Creative Studio.

| Etap | Pytanie do rozstrzygnięcia | Praktyczny produkt pracy | Co zatrzymuje przejście dalej |
|---|---|---|---|
| 1. Brief | Co widz ma zrozumieć lub zrobić? | Jedno zdanie celu, odbiorca, treść obowiązkowa, format, rola sceny, ograniczenia marki | Brak rozróżnienia celu od efektu typu „zrób dynamicznie” |
| 2. Research wizualny | Jaki język ruchu pasuje do przekazu? | Kilka referencji z opisem konkretnej zasady: kierunek, pauza, masa, hierarchia; źródło i prawa | Referencja oceniona wyłącznie jako „ładna”, bez wskazania użytecznej decyzji |
| 3. Koncept | Jaka czynność niesie znaczenie? | Warianty zapisane czasownikami, np. „porządkuje”, „łączy”, „odsłania”; jeden wybrany motyw | Koncept wymaga nieprawdziwego obrazu produktu lub danych |
| 4. Styleframes | Jak ma wyglądać obraz przed, w trakcie i po akcji? | Kluczowe stany w docelowym aspekcie, realna typografia, test najtrudniejszej treści | Nieczytelny końcowy komunikat lub brak stanu końcowego |
| 5. Storyboard | Jakie informacje następują po sobie? | Zmiany stanów, kierunek uwagi, kamera, wejście/wyjście scen, lokalizacja tekstu | Ciąg atrakcyjnych kadrów bez logicznego przejścia |
| 6. Animatic | Czy sens i czas mieszczą się w przydzielonym odcinku? | Prosty film z docelową lub wyraźnie tymczasową ścieżką audio i cue | Treść wymaga pauzowania, VO się nie mieści, zmiana długości nieuzgodniona z właścicielem timeline |
| 7. Organizacja assetów | Czy to są właściwe wersje materiału? | Manifest ID/hash/revision, fonty, alfa, color space, rights, proxy/original | Brak fontu, nieaktualny napis, brak prawa do wykorzystania pliku |
| 8. Blocking | Czy najważniejsze działanie jest czytelne bez efektów? | Główne pozycje i momenty impact, placeholder secondary motion | Ruch nie wynika ze zdarzenia lub kilka dominant konkuruje równocześnie |
| 9. Krzywe i overlap | Czy pacing i spacing mają zamierzony charakter? | Wartości i prędkości; ustalone pauzy, overshoot i settle | Szarpnięcie poza zamierzonym kontaktem, brak stabilnego końca |
| 10. Compositing | Czy elementy należą do tego samego obrazu? | Poprawne matte, ostrość, ekspozycja, cień, grain; osobny podgląd alfa | Kontury, halo, niepasujący blur, banding lub błędny kolor |
| 11. Dźwięk | Czy dźwięk wzmacnia hierarchię i nie zakrywa mowy? | Cue muzyczne, VO, SFX, mix właściwy dla odbiorcy i kanału | Błędne słowo, drift, podmieniona wersja audio, nieczytelna mowa |
| 12. QA i delivery | Czy oddawany plik spełnia uzgodnioną intencję i kontrakt? | Obejrzany render, manifest zależności, wynik QA, projekt edytowalny lub jawny zakres spłaszczenia | Techniczne błędy, niezachowane locks, nieprzetestowany eksport podany jako „gotowy” |

Nie zaczynaj compositingu od glow i grain. Najpierw pokaż, że cel końcowy, staging i timing działają. Również nie odkładaj dźwięku całkowicie na koniec: VO i mapa fraz pomagają ustalić animatic, a finalny mix następuje po stabilizacji obrazu. Etap 11 dopracowuje istniejącą relację obrazu z dźwiękiem.

**Praktyczny przykład DERIVED.** W scenie produktu ma być widoczna nazwa i jedna cecha. Jeżeli styleframe ma zbyt małą etykietę, korekta brzmi „powiększ produkt / zmień kadr”, a nie „dodaj więcej ruchu”. Jeżeli animatic nie daje czasu na tę cechę, korekta dotyczy narracji lub długości przydzielonego slotu. Jeżeli dopiero finalny render pokazuje halo, korekta dotyczy compositingu. Dzięki temu agent nie zmienia zaakceptowanej palety w odpowiedzi na wadę alfy.

### Kierunek ruchu jako mała specyfikacja

Zapisz trzy cechy oraz ich widoczne konsekwencje. Przykładowe „spokojny, precyzyjny, techniczny” może oznaczać: jeden ruch dominujący; brak sprężyn w danych; wyraźny hold końcowego stanu; krótkie odpowiedzi elementów zależnych od zdarzenia. Przykładowe „miękki, przyjazny, sprężysty” może pozwalać na łagodny overshoot sylwetki i opóźniony detal, ale nadal wymaga stabilnego tekstu. To decyzje konkretnej marki, nie reguły gatunku.

Dodaj zakazy wynikające z briefu: „logo bez deformacji”, „wartości bez overshoot”, „kamera nie ujawnia tylnej strony produktu”. Pozwalają wybrać R01, R07 i R04 bez późniejszego arbitralnego „upiększania”.

## P-LOCKS — jak przyjmować feedback i zachować akceptację

**DERIVED.** Akceptacja dotyczy identyfikowalnej wersji i zakresu. Zdanie „wygląda dobrze” bez rewizji nie może automatycznie blokować wszystkich przyszłych zmian. Zapis akceptacji powinien zawierać:

```json
{
  "lock_id": "style-hero-03",
  "revision": "scene-014-r3",
  "scope": ["hero.end_pose", "brand.palette", "copy.exact_text"],
  "approved_by": "user",
  "evidence": "approval-message-id-or-local-record",
  "depends_on": ["product-art@sha256:EXAMPLE", "font-file@sha256:EXAMPLE"],
  "excluded": ["animation.curves", "audio.sfx"],
  "status": "accepted"
}
```

Wartości hash w przykładzie są placeholderami, nie obliczonymi skrótami. Akceptowany finalny pose nie ustanawia automatycznie akceptacji czasu wejścia. Akceptacja 16:9 nie zatwierdza automatycznie 9:16. Zamiana pliku na identyczne bajty pod inną ścieżką wymaga aktualizacji locatora, nie wymyślonej zmiany kreatywnej; zmiana treści powinna wskazać zależne wyniki do ponownej oceny.

| Rodzaj feedbacku | Poprawna interpretacja | Dopuszczalna zmiana | Zachowane elementy |
|---|---|---|---|
| „Za wolno wchodzi” | Problem czasu lub odczuwanej prędkości, do obejrzenia | Długość lead-in, krzywa, odległość ruchu | Treść, kolor, geometria logo |
| „Nie widzę, co to za produkt” | Problem staging / ekspozycji / czytelności | Kadrowanie, światło, czas pełnej ekspozycji | Prawdziwy kształt produktu i tekst etykiety |
| „Podpis ma być dłużej” | Wydłużenie hold, zależne od slotu montażowego | Środek lower third po zgodzie timeline owner | Długość i charakter chronionego intro/outro |
| „Nie trafia w muzykę” | Najpierw ustalić, który impact i cue | Offset impactu, lead-in lub mapa cue | Zatwierdzone słowa i montaż, o ile feedback ich nie zmienia |
| „Zmień zdjęcie” | Zmieniono dependency | Materiał i kontrola jego crop/alpha/color | Niezależne zaakceptowane sceny |

**SOURCED, wąski precedens narzędziowy:** AE Responsive Design–Time zachowuje czas chronionych regionów; to inspiracja dla chronionych faz sceny, nie dowód obsługi locks w FrameMotion [R-S04](https://helpx.adobe.com/after-effects/desktop/motion-graphics/add-responsive-design/responsive-design.html). Dokumentacja Motion State rozróżnia kotwice początku i końca klipu; ta różnica powinna przetrwać przekazanie danych [R-S16](https://docs.jakeinmotion.com/motion-state/concepts/timing-and-easing/).

Proponowana karta poprawki: **obserwacja → zakres klatek → dotknięty cel → przyczyna robocza → jedna zmiana → porównanie A/B → wynik → locks zachowane / wymagające nowej decyzji**. Jeżeli kolejna poprawka usuwa błąd, ale łamie zaakceptowany pose, nie należy uznać jej za bezwarunkowo lepszą.

### Jeden właściciel nadrzędnej osi czasu

Proponowany podział: Studio ustala intencję i wymaganą treść; właściciel timeline przydziela [in,out), handles i cue; FrameMotion rozwiązuje ruch w tym zakresie. Samodzielny FrameMotion może być właścicielem własnego projektu, ale musi to jawnie zadeklarować. Zmiana długości jest żądaniem do właściciela, a nie ubocznym efektem lepszego easingu.

Przy zbyt krótkim slocie agent podaje konkretne możliwości: krótsze copy, prostszy ruch, mniejsza liczba akcentów albo prośba o dłuższy zakres. Przy braku funkcji backendu: zachować unsupported field, zgłosić ograniczenie, zaproponować hybrydowy render. Ciche zastąpienie maski luma ostrym clipPath zmienia projekt.

## P-AUDIO — synchronizacja ma kilka zegarów

**SOURCED:** dokumentacja librosa traktuje onset detection i beat tracking jako różne operacje. Beat tracker uwzględnia tempo; `units='frames'` dotyczy kroków analizy audio, nie klatek filmu. Dostępny jest również czas w sekundach i indeksy próbek. [R-S08](https://librosa.org/doc/0.11.0/generated/librosa.beat.beat_track.html), [R-S09](https://librosa.org/doc/0.11.0/generated/librosa.onset.onset_detect.html).

Poniższe rozróżnienie jest proponowanym modelem roboczym; nie wszystkie zdarzenia są automatycznie wykrywalne przez wymienione narzędzia.

| Zdarzenie | Co znaczy dla reżyserii | Czego nie wolno z niego automatycznie wnioskować |
|---|---|---|
| Amplitude/envelope | Siła ciągłej reakcji wizualnej, po normalizacji i ograniczeniu zakresu | Że każde maksimum jest beatem |
| Onset | Początek słyszalnego zdarzenia / ataku | Że jest początkiem taktu, frazy lub słowa |
| Beat | Hipoteza regularnego pulsu muzycznego | Że beat 1 jest downbeatem albo że tempo jest stałe |
| Downbeat | Początek taktu w przyjętym metrum | Że zawsze wypada co cztery detekcje onsetów |
| Phrase / section boundary | Zmiana energii lub znaczenia większego fragmentu | Że musi zawierać duży transient |
| VO cue | Słowo, sylaba, akcent semantyczny, oddech lub pauza | Że ten sam cue jest dobrą chwilą początku i pełnej czytelności tekstu |
| Lyrics cue | Czas słowa lub sylaby w śpiewie, także melizmat | Że alignment mowy poradzi sobie z nim bez odsłuchu |
| Visual impact | Kontakt, maksymalna deformacja, pełne reveal albo zmiana dominanty | Że jest równy pierwszej klatce animacji |

**DERIVED.** Każdy ważny ruch zapisuje co najmniej `start`, `impact`, `settle`, a tekst także `readable_from` i `readable_until`. Przykład: cue na t=5,00 s, lead-in 0,24 s, settle 0,32 s; animacja startuje 4,76 s, akcent osiąga 5,00 s, ustala się 5,32 s. Są to proponowane wartości przykładu. Wybrany beat nie wymusza identycznego impulsu na tekście, kamerze, particles i tle.

Źródłowe czasy audio zachowuj przed kwantyzacją. Przy stałym offset `timeline_time = source_time + offset`. Przy retimingu potrzebna jest jawna mapa czasu, nie pojedynczy offset. Przeliczenie na klatkę używa `fps_num/fps_den` i określonej polityki zaokrąglania. Po kwantyzacji zachowaj residual error w sekundach, aby nie utracić informacji o odchyłce. Jeden celowy offset artystyczny nie naprawia narastającego driftu.

**Test proponowany:** odtwórz początek, środek i koniec fragmentu; sprawdź najmocniejszy impact oraz pauzę bez perkusji. Zmień tempo w drugiej połowie syntetycznego pliku i pokaż, że stała siatka przestaje pasować. Brak pewnego pulsu powinien skutkować ręcznymi cue lub ruchem od fraz, nie przypadkowym BPM. To test planowany **NOT_RUN**.

## P-TUTORIALS — mapa materiałów z poziomem inspekcji

Nie traktuj tej tabeli jako listy obejrzanych kursów. „Uczy” znaczy tutaj: temat jest rzeczywiście objaśniony w przeczytanej warstwie tekstowej. Materiały z samym opisem są w osobnej tabeli i nie tworzą podstawy receptur. Wszystkie linki prowadzą do źródeł, a szczegółowe daty, wersje i granice są w `sources.json`.

| Kolejność nauki i źródło | Co przeczytano i czego użyć | Ćwiczenie własne | Inspekcja / ograniczenie |
|---|---|---|---|
| 1. [R-S14 — Ryan Plummer, proces](https://schoolofmotion.com/blog/guide-completing-motion-design-project) | Tekst o przygotowaniu i rough animation | Zrobić różne kryteria akceptacji styleframe i animatic | ARTICLE_READ; osadzone filmy NOT_VIEWED |
| 2. [R-S15 — Joey Korenman, Making Giants](https://schoolofmotion.com/blog/making-giants-idea) | Fragment transkrypcji 00:11–04:58, start konceptu i zbieranie referencji | Opisać, kiedy proof-of-motion rozwiązuje pytanie, a kiedy tylko odracza koncept | TRANSCRIPT_READ_SELECTED; seria NOT_VIEWED |
| 3. [R-S01 — AE Shape operations](https://helpx.adobe.com/after-effects/desktop/drawing-painting-and-paths/shapes-and-shape-attributes/shape-attributes-paint-operations-path.html) | Trim Paths i porządek operacji | R01, znak z przecinającymi się ścieżkami | DOC_TEXT_READ; tutorial NOT_RUN |
| 4. [R-S02 — AE Text](https://helpx.adobe.com/after-effects/desktop/animating-text/text-animation/animating-text.html) | Warianty animowania tekstu i ograniczenia presetów | R02 ze skrajną długością polskiego copy | DOC_TEXT_READ; font test NOT_RUN |
| 5. [R-S03 — Motion Sequence Text](https://support.apple.com/en-mide/guide/motion/motn1607df2b/mac) | Jednostka sekwencji i zakres | Porównać znak/słowo/wiersz na tym samym zdaniu | DOC_TEXT_READ; playback NOT_RUN |
| 6. [R-S04 — Responsive Design–Time](https://helpx.adobe.com/after-effects/desktop/motion-graphics/add-responsive-design/responsive-design.html) | Ochrona wybranych faz | R03 w trzech długościach | DOC_TEXT_READ; eksport MOGRT NOT_RUN |
| 7. [R-S05 — Apple HIG Motion](https://developer.apple.com/design/human-interface-guidelines/motion.md) | Celowość i przerwanie ruchu interaktywnego | R06 z inputem w połowie przejścia | DOC_MARKDOWN_READ; nie jest poradnikiem AE |
| 8. [R-S06 — AE Track Mattes](https://helpx.adobe.com/after-effects/desktop/work-with-transparency-and-compositing/work-with-track-mattes-and-traveling-mattes/track-mattes-and-traveling-mattes.html) | Typy kanału i inverted | R08 z debug maską | DOC_TEXT_READ; sprzeczne zdanie ogólne odnotowane |
| 9. [R-S11 — Blackmagic VFX Guide](https://documents.blackmagicdesign.com/UserManuals/DaVinci-Resolve-20-Fusion-Visual-Effects.pdf) | Wybrane teksty o trackingu, keyingu i Follower | R13/R14 na własnym syntetycznym materiale | PDF_TEXT_SELECTED; drukowane s.88–90,104–110,112–123,153–155; media NOT_DOWNLOADED |
| 10. [R-S12 — C4D Effectors](https://help.maxon.net/c4d/2026/en-us/Content/html/7443.html) i [R-S13 — Delay](https://help.maxon.net/c4d/2026/en-us/Content/html/OEDELAY.html) | Przestrzenny wpływ i kolejność przetwarzania | R17, potem ograniczony R15 | DOC_TEXT_READ; animowane demonstracje NOT_VIEWED |
| 11. [R-S07 — Motion Particle cells](https://support.apple.com/en-mide/guide/motion/motn7ccaeefa/mac) | Emisja, życie i wygląd po wieku | R10 bez glow, potem porównanie | DOC_TEXT_READ; runtime NOT_RUN |
| 12. [R-S08 — Beat](https://librosa.org/doc/0.11.0/generated/librosa.beat.beat_track.html), [R-S09 — Onset](https://librosa.org/doc/0.11.0/generated/librosa.onset.onset_detect.html), [R-S10 — Motion Audio](https://support.apple.com/en-mide/guide/motion/motn13746bcf/mac) | Trzy różne mechanizmy sterowania dźwiękiem | R11: ręczne cue kontra envelope | DOC_TEXT_READ; żadnej analizy pliku nie wykonano |
| 13. [R-S17 — Evan Abrams, Karaoke Text](https://www.premiumbeat.com/blog/after-effects-video-tutorial-karaoke-text/) | Pisemne kroki pod filmem, warstwy i highlight | R12 ze słowem śpiewanym długo | WRITTEN_STEPS_READ; wideo NOT_VIEWED; materiał z 2014 |
| 14. [R-S16 — Jake In Motion, Timing and Easing](https://docs.jakeinmotion.com/motion-state/concepts/timing-and-easing/) | Dokumentacja autora o czasie i kotwicach | R16 i test skrócenia klipu | AUTHOR_DOC_READ; plugin Premiere, nie kurs AE; nie instalowano |
| 15. [R-S18 — AE Cameras](https://helpx.adobe.com/after-effects/desktop/work-with-layers/camera-layer/cameras-lights-points-interest.html) i [R-S19 — Blender Cameras](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/cameras.rst) | Perspektywa i cel ostrości | R09 i R18 z dwiema głębokościami | DOC_TEXT / RAW_RST_READ; renderer NOT_RUN |
| 16. [R-S20 — Blender Vector Blur](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/compositing/types/filter/blur/vector_blur.rst) | Ograniczenia efektu ekranowego względem odsłonięć | R18: obiekt szybko przechodzi na tle; porównać layers | RAW_RST_READ; nie pobierano obrazów przykładowych |

### Materiały opisowe, nieprzyjęte jako dowód wykonania techniki

| Materiał | Faktyczny odczyt | Dlaczego nie zasila receptury jako sprawdzony tutorial |
|---|---|---|
| [Video Copilot — Advanced Electric FX](https://www.videocopilot.net/tutorials/advanced_electric_fx/) | Publiczna strona, data 2017-05-09 i krótki opis kierunkowej elektryczności / odbić | Wideo **NOT_VIEWED**, brak przeczytanej transkrypcji; projekt niepobrany. Sam opis nie dowodzi kolejności efektów ani ustawień. |
| [Ben Marriott — Master Motion Design](https://www.benmarriott.com/mastermotiondesign) | Publiczny syllabus i opis kursu, m.in. anticipation, workflow, transitions, morphing | Płatne lekcje **NOT_VIEWED**, nie logowano się i nie obchodzono dostępu. Opis kursu nie jest jego instrukcją wykonawczą. |
| [Adobe PL — Animacje tekstu i typografia kinetyczna](https://www.adobe.com/pl/products/aftereffects/text-animation.html) | Polska strona produktowa opisująca animatory, Graph Editor i szablony | Materiał marketingowy, bez potrzebnej precyzji ustawień; nie liczy się jako dodatkowe niezależne potwierdzenie dokumentacji EN. |

Nie zbudowano rankingu nauczycieli. Jake Bartlett jest wykorzystany jako autor czytelnej dokumentacji narzędzia, Evan Abrams jako autor pisemnej lekcji, Korenman jako autor odczytanego fragmentu transkrypcji. Marriott i Video Copilot pozostają konkretnymi kierunkami dalszej nauki o znanym, ograniczonym poziomie weryfikacji.

### Odtwarzalny dziennik wyszukiwania i luki językowe

Zapytania EN obejmowały m.in. `motion design styleframes storyboard animatic process`, `Sequence Text behavior`, `Fusion planar tracker`, `Cinema 4D Fields Plain Effector`, `Jake Bartlett graph editor`, `Evan Abrams karaoke text` i dokumentację librosa. Zapytania PL obejmowały `After Effects animacja typografii tutorial proces po polsku` oraz polską dokumentację / stronę produktu Adobe. Zwrócone polskie kursy, filmy i fragmenty książek nie zostały uznane za przeczytane tylko na podstawie snippetów. To badanie ma więcej pierwotnej treści EN niż PL; nie ma podstaw do deklarowania pełnego pokrycia polskich tutoriali.

Strony HTML dokumentacji Blendera zwracały błędy dostępu. Publiczne surowe pliki RST producenta zostały odczytane przez Python urllib; to odczyt dokumentów, nie uruchomienie pobranego kodu. Gałąź `main` nie została przypięta do commit hash. Duży Fusion19 manual nie przeszedł limitu rozmiaru web; wykorzystano czytelny przewodnik Resolve 20. Z tych braków nie wyciągano wniosków o nieistnieniu funkcji.

## P-QA — jak używać tutorialu bez kopiowania projektu

**DERIVED.** Dobra sesja nauki agenta kończy się własnym ćwiczeniem i zidentyfikowaną granicą zastosowania, nie kolekcją presetów. Minimalna karta zawiera: problem; mechanizm źródła; własne wejście; przewidywany rezultat; kontrprzykład; pomiar lub obserwację; wynik. Nie należy porównywać tylko końcowych stopklatek.

Przykład dla R08: zbudować dwie jednolite plansze oraz monochromatyczną maskę; sprawdzić 0/50/100%, potem pełne przejście i granicę cięcia. Kontrola negatywna: odwrócić maskę i wykazać, że test wykrywa zmianę. Dopiero po tym wrócić do złożonego przejścia brandowego. Przykład dla R11: porównać cue na starcie animacji i cue w impact, odsłuchać oba; nie uznawać maksymalnej amplitudy za prawidłowy cue z definicji.

Proponowana ograniczona pętla kontroli:

1. Zapisz wersję wejścia, locks i kryteria sceny.
2. Obejrzyj wynik w czasie rzeczywistym oraz miejsca ryzyka klatka po klatce; odsłuchaj dźwięk.
3. Wybierz jedną materialną wadę, wskaż zakres i prawdopodobną przyczynę.
4. Zmień najmniejszy zestaw parametrów, który może usunąć wadę.
5. Sprawdź poprawiony zakres oraz zależne sceny i eksport; zachowaj porównanie poprzedniej wersji.
6. Zatrzymaj iterację, jeśli kryteria spełniono; po dwóch nieskutecznych próbach tej samej klasy zmień metodę lub zgłoś ograniczenie. Ten budżet jest propozycją organizacyjną.

Przed delivery sprawdź osobno: prawidłową treść; działanie sceny; stan techniczny pliku; prawa; zgodność z kontraktem; wynik rzeczywistego odtwarzania. Automatyczny test może wykryć złą długość, brak fontu, przepełnienie layoutu czy niestabilny seed. Nie dowodzi, że pauza jest emocjonalnie właściwa albo ruch zrozumiały.

## Pokrycie podzadania i stan dowodu

| Obszar | Co dostarczono | Dowód | Luka |
|---|---|---|---|
| 18 receptur | R01–R18, każda z parametrami, błędem/naprawą, kodem i QA | Własna synteza na podstawie wskazanych mechanizmów | Wszystkie render tests NOT_RUN |
| After Effects | Shapes, tekst, matte, protected time, kamera | Dokumentacja producenta | Nie uruchomiono AE |
| Fusion | Tracking, keying, Follower, node workflow w odpowiednich recepturach | Wybrane strony oficjalnego PDF | Nie przeczytano całej książki; nie odtworzono ćwiczeń |
| Apple Motion | Sequence Text, particle cell, audio | Dokumentacja producenta | Nie uruchomiono Motion |
| Cinema 4D | Fields/Effectors/Delay i przestrzenna organizacja ruchu | Dokumentacja 2026 + jawna historyczna uwaga R21 | Nie zweryfikowano renderu lub obecnych bugów |
| Blender | Kamera/DOF; ograniczenia Vector Blur | Oficjalne RST | Brak commit pin i testu wersji lokalnej |
| Praktycy | Tekst Plummera, fragment transkrypcji Korenmana, dokumentacja Bartletta, kroki Abramsa | Odczytana treść pierwszej strony | Brak obejrzanych tutoriali wideo |
| Audio | Typy cue, impact, offset/drift, relacja VO/lyrics | Dokumentacja + własny model | Brak testu detektorów na realnym audio |
| Proces i feedback | Etapy, locks, zmiany zależności, QA | DERIVED | Nie jest potwierdzonym kontraktem wtyczek |

20 użytecznych źródeł głównych zapisano w `sources.json`; historyczna podstrona Delay jest uzupełnieniem jednego rekordu. Trzy strony opisowe powyżej nie powiększają tego wyniku. Liczbę należy deduplikować po URL przy łączeniu z rejestrami pozostałych specjalistów. Żadne treści źródłowe nie były użyte jako zgoda na instalację, płatność, upload lub publikację.
