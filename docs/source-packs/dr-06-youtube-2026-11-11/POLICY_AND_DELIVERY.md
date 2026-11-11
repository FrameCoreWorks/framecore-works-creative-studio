# YouTube — zasady i wydanie odcinka

Stan odczytu: **11 listopada 2026**. Poniżej streszczenie oficjalnej pomocy; nie jest to ocena prawna konkretnego filmu ani gwarancja decyzji platformy. Rejestr: [evidence/policy_sources.json](evidence/policy_sources.json). Żaden materiał nie został przesłany ani opublikowany.

## Cztery odrębne decyzje

| Decyzja | Co wynika ze źródła | Zapis dla odcinka — propozycja DERIVED |
|---|---|---|
| Odbiorca / made for kids | Liczy się zamiar kierowania treści do dzieci i całokształt tematu, języka, postaci, zabawy oraz promocji. Mixed audience może być child-directed; family friendly ani sam styl animacji nie rozstrzygają klasyfikacji. Analytics nie służy do samodzielnego ustalenia tej decyzji. | audience_intent, uzasadnienie czynników, osoba podejmująca decyzję, data, wersja filmu. Wiek projektu w biblii nie zastępuje kwalifikacji. [Y01](https://support.google.com/youtube/answer/9528076?hl=en) |
| Ujawnienie AI | Obowiązek obejmuje realistyczne, znacząco generowane/zmienione osoby, zdarzenia i miejsca. Strona wymienia też generowaną muzykę, a w głównym zestawieniu muzykę będącą głównym przedmiotem filmu. Nierealistyczna animacja i pomoc w scenariuszu są przykładami niewymagającymi ujawnienia. Nie wyciągać z tego zwolnienia dla każdego syntetycznego dźwięku w bajce. Samo ujawnienie nie odbiera kwalifikacji do monetyzacji. | Lista operacji AI z rozdzieleniem pisania kodu, renderowania sceny, obrazu, głosu i muzyki. Osobna decyzja o disclosure dla finalnej treści, ze źródłem i datą; przy niejednoznaczności muzyki ponownie sprawdzić pomoc dla wybranej publikacji. [Y02](https://support.google.com/youtube/answer/14328491?hl=en) |
| Oryginalność / monetyzacja | Zmiana nazwy repetitious → inauthentic od 15.07.2025 obejmuje treści masowo produkowane i powtarzalne. Wspólne intro i bohaterowie są dopuszczalnymi przykładami, jeśli odcinki mają odrębny sens i historię. Schematy z minimalną zmianą i powtarzanym wynikiem są ryzykiem. Reused content jest odrębną oceną od prawa autorskiego, także przy zgodzie właściciela. Ocena dotyczy kanału i jego treści. | Porównać trzy kolejne odcinki: inny problem, decyzja, konsekwencja i rozwiązanie. Re-use riga nie jest powtórzeniem historii. Zachować dowód autorstwa i pracy redakcyjnej. Brak obietnic YPP lub zasięgu. [Y03](https://support.google.com/youtube/answer/1311392?hl=en) |
| Prawa do materiałów | Pozwolenie/licencja, właściwy wyjątek lub potwierdzony public domain to różne podstawy. Sam credit nie zastępuje praw. Prawa do opracowań i twórczości AI zależą od jurysdykcji; biblioteka lub licencja nie gwarantuje braku roszczenia Content ID. | Dla każdego obrazu, fontu, modelu, głosu, muzyki i kodu: właściciel, źródło, konkretne warunki, zakres komercyjny i modyfikacji, credit, dowód zgody. Unknown blokuje wydanie tego zasobu. [Y04](https://support.google.com/youtube/answer/2797466?hl=en) |

Dodatkowo aktualna pomoc Y03 obejmuje manipulacyjne, wymienne historie zagrożenia i niespójne klipy AI bez łuku narracyjnego. Wyłącza z monetyzacji kanały z personami AI udającymi ludzkich ekspertów doradzających w tematach zdrowia, prawa, finansów lub polityki. To odrębna granica przy projektowaniu explainerów. [Y03, odczyt 11.11.2026](https://support.google.com/youtube/answer/1311392?hl=en)

Ustawienie made for kids ogranicza m.in. komentarze, powiadomienia, ekrany końcowe oraz reklamy spersonalizowane. Publikacyjny plan nie może zależeć od tych funkcji. W tym badaniu nie odczytywano prywatnych ustawień cudzych kanałów. [Y05](https://support.google.com/youtube/answer/9527654?hl=en)

YouTube opisuje jakość treści dziecięcych przez adekwatność do wieku, ciekawość, kreatywność i czytelne historie. Jako ryzyka wskazuje m.in. mylące obietnice edukacyjne, splątane wątki, nieczytelny dźwięk i brak początku, środka lub końca. To kryteria odbioru własnego pilota, a nie dowód, że wybrany kanał łamie zasady. [Y06](https://support.google.com/youtube/answer/10774223?hl=en)

## Profil pliku i pakiet wydania

Dla proponowanego pilota 1080p SDR: MP4, H.264 progressive High, 4:2:0, oznaczone BT.709, audio AAC 48 kHz stereo, Fast Start. Zachować FPS projektu. Oficjalna tabela rekomenduje 8 Mb/s dla 1080p 24/25/30 i 12 Mb/s dla 48/50/60; są to wskazówki eksportu, nie uniwersalny limit. Standardowy player ma proporcję 16:9, ale przyjmuje inne. Profil mezzanine i alpha dla ujęć są odrębnymi decyzjami produkcyjnymi. [Y07](https://support.google.com/youtube/answer/1722171?hl=en)

**DERIVED, NOT_RUN:** dostawa zawiera finalny plik z hashem i rewizją projektu, poprawione napisy SRT/VTT, miniaturę, tytuł i opis zgodne z treścią, credits i manifest praw, decyzje audience/AI, chapter markers tylko jeśli pomagają. Po zmianie dialogu ponownie generować napisy i sprawdzać ich zgodność z dokładnym take’em.

Odbiór techniczny mierzy dekodowanie całości, rozmiar, liczbę klatek lub PTS, FPS, sample rate, brak pustych/utraconych klatek, clipping, synchronizację i faktyczny czas końca. Odbiór twórczy wymaga obejrzenia i odsłuchu całego mastera: czy historia się domyka, dialog jest zrozumiały, puenta czytelna, a miniatura nie obiecuje innego filmu. Sam status render_complete nie wystarcza.
