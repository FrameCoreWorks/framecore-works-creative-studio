# Biblia serii i warsztat odcinka

**DERIVED — projekt procesu dla FrameCore, nie wdrożenie ani opis kosztów badanych autorów.** Punkty odniesienia: [kadry i zakres oglądu](evidence/VIEWING_LOG.md), [metody autorów](production/PRODUCTION_CASES.md), [operacje agentowe](baseline/OPERATION_MAP.md).

## Od celu widza do pełnej historii

W briefie ustalić: dla kogo jest odcinek, jaki ma gatunek, co widz ma poczuć/zrozumieć i co zmieni się między początkiem a końcem. Dla fikcji zapisać cel bohatera, przeszkodę, jego decyzję i konsekwencję. Dla explainera zapisać pytanie, intuicję do sprawdzenia, mechanizm, przykład graniczny i odpowiedź. Dokumentalna rekonstrukcja wymaga osobnej etykiety dla faktu, hipotezy i wyobrażenia.

Scenariusz rozłożyć na beaty: nowa informacja lub zmiana stanu. Każde ujęcie ma pokazać konkretny beat, reakcję albo potrzebną orientację przestrzenną. Jeśli wycięcie ujęcia nic nie zmienia, rozważyć jego usunięcie. Nie przyjmować docelowej liczby cięć na minutę. Badanie pojedynczych klatek nie pozwoliło policzyć rzeczywistego rytmu badanych odcinków.

Dzieci 2–4, dzieci 5–8, widownia rodzinna/młodzieżowa oraz starsi widzowie dostają osobne założenia dotyczące abstrakcji, słownika, strachu i liczby równoległych wątków. Są to hipotezy redakcyjne do sprawdzenia, nie medyczne zalecenia długości ekspozycji. Interpretacja widowni w katalogu nie jest ustawieniem made for kids.

## Biblia jako wersjonowane dane i wzorce

| Część | Obowiązkowa zawartość | Przykład kontroli |
|---|---|---|
| Tożsamość serii | series_id, wersja, właściciel, obietnica, gatunek, odbiorca, języki, granice tonu | Nowy odcinek realizuje obietnicę, ale ma odrębny konflikt i wynik. |
| Bohaterowie | character_id, sylweta, wzajemna skala, proporcje, model sheets, przód/tył/3⁄4/profil, ubrania i warianty | Porównanie tych samych widoków na początku i końcu ujęcia; zmiana stroju tylko jako jawne zdarzenie. |
| Aktorstwo | cecha, pragnienie, lęk, zakres zachowań, expression/pose sheets, gesty, spojrzenia, niedozwolone deformacje | Poza i kierunek uwagi wskazują intencję; agent nie dodaje kiwania bez znaczenia. |
| Rig i kod | id@revision/hash, części SVG/kości/kontrolki, osie i pivots, z-order, jednostki, fonty, seed, wersja renderera | Kontakt ręki z rekwizytem, obrót, skrajna poza, brak zmiany proporcji. |
| Głos | voice_id@revision, wykonawca/podstawa użycia, barwa/intencja, zakres emocji, próbka referencyjna, wymowa | Odsłuch zatwierdzonego take’a i porównanie exact text; brak domyślnego klonowania cudzej osoby. |
| Lokacje | location_id, plan, odległości, skala, oś akcji, wejścia, stałe rekwizyty, światło i warianty | Cięcie zachowuje relację przestrzenną; zmiana strony kadru ma czytelny powód. |
| Obraz i kamera | paleta, kontur, cienie, faktura, plany, ruch kamery, easing, głębia i safe area | Miniatura klatki nadal wyjaśnia relację; ruch prowadzi uwagę do beatu. |
| Reguły świata | możliwości, ograniczenia, skutki zdarzeń, stan wiedzy bohaterów, zasady powrotu do stanu wyjścia | Bohater nie używa wiedzy, której nie zdobył; przedmiot nie wraca bez zdarzenia. |
| Ciągłość | continuity_in/out każdego ujęcia: garderoba, rekwizyt/posiadacz, pozycja/spojrzenie, uszkodzenie, pogoda, pora | Porównanie granic kolejnych ujęć i jawne zdarzenia zmiany stanu. |
| Biblioteka dźwięku | motywy postaci, ambience lokacji, Foley, cisza, zakazane powtórzenia, oddzielne stemy | SFX ma źródło w scenie, a muzyka nie maskuje informacji. |
| Język PL | słownik nazw i odmian, akcent, znaczenie skrótów, wymowa liczb/jednostek, diakrytyka w fontach | „Łódź”, „żółć”, „źdźbło”, nazwa własna i fleksja w naturalnej kwestii; nie tylko automatyczny ASR. |
| Prawa i wydanie | źródła/licencje, zgody głosowe, credits, hash/revision, decyzje publikacyjne | Żaden zasób Unknown nie przechodzi do wydania. |

Parametry biblijne rozdzielić na twarde locki (tożsamość, skala, prawa, głos), warianty (strój, emocja, światło) i decyzje ujęciowe (poza, kamera). Zmiana wspólnego assetu tworzy nową rewizję i listę zależnych ujęć; nie nadpisuje istniejącego pliku.

## Proces i bramki

1. Brief i format → biblia v0 + trzy różne zalążki odcinków. Człowiek ocenia, czy format zniesie serię.
2. Research faktów → rejestr tez i źródeł. Fikcyjne reguły odróżnić od twierdzeń o świecie.
3. Scenariusz → read-through z rzeczywistymi pauzami, polską wymową i kontrolą związku przyczynowego. Wersjonować każdą kwestię osobno.
4. Storyboard → animatic z roboczym dźwiękiem. Sprawdzić całość, reakcje i zakończenie przed pracochłonną animacją.
5. Assety/rigging → testy póz i kontaktu → layout → animacja ujęć. Równolegle można przygotować odrębne lokacje i Foley po zatwierdzeniu wejść.
6. Compositing i sound → conform w jednym master timeline → QC → pakiet publikacji. Osobny pełny odsłuch i seans obrazu.
7. Retrospektywa pilota → pomiar rzeczywistego czasu na etap i odrzuconych prób → korekta budżetu kolejnego odcinka. W tym researchu etapów tych nie wykonano.

## Timing-first, voice-first, music-first

| Podejście | Dobre zastosowanie | Lock i koszt późnej zmiany |
|---|---|---|
| Timing-first | Bezsłowny gag, kontakt, pauza i reakcja; wstępny animatic | Beat i czytelność ruchu ustalają długość. Dźwięk dopasowuje się do cue. Dialog dodany później może złamać scenę. |
| Voice-first | Narracja wiedzy i dialog | Zatwierdzony take wyznacza akcenty, pauzy, visemy i napisy. Zmiana słowa może pozostać lokalna; dłuższa kwestia wymaga decyzji o ripple. |
| Music-first | Piosenka, taniec, odcinek podporządkowany frazie muzycznej | Tempo, metrum, frazy i długość ustalone przed animacją. Zmiana tempa dotyka wielu gestów i cięć. |
| Hybryda | Krótka mowa w scenie wizualnej | Beat ma okno, głos musi się w nim zmieścić albo zmienia się rewizja montażu. Nie ściskać automatycznie take’a kosztem naturalności. |

Re-use obejmuje przygotowane rigi, cykle, tła i motywy, ale w każdym ujęciu zmieniają się intencja, gest, relacja i kadr według historii. Celowa animacja ograniczona wymaga czytelnych póz, trafnej reakcji i dźwięku. Samo dodanie ciągłego ruchu tła nie naprawi brakującego beatu.

## Zmiana jednej kwestii

Zmiana tekstu tworzy nową wersję line_id i nowy take. Jeżeli narrator jest poza kadrem i długość się mieści, zmieniają się stem, napisy i finalny miks; render obrazu może pozostać ten sam. Gdy widać usta, odświeżyć visemy i gesty powiązane z akcentami. Gdy zmienia się długość, montażysta zatwierdza nową pozycję na masterze; statyczny lokalny render sąsiedniego ujęcia nie musi być ponownie liczony tylko dlatego, że przesunął się w odcinku. Dokładny DAG, rounding audio i stale revision: [CONTRACTS](baseline/CONTRACTS.md).
