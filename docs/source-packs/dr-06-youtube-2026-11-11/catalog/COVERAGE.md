# DR-06 — pokrycie katalogu

Odczyt publicznych źródeł 11 listopada 2026. Próba główna zawiera **44 pełne filmy, odcinki i lekcje z 23 kanałów**. W tym 11 publikacji code-based z 5 kanałów i 33 przykłady warsztatu klasycznego z 18 kanałów. Cały katalog ma **60 publikacji z 34 kanałów**. Rozszerzenie obejmuje 13 dodatkowych klasycznych odniesień oraz dwa explainery-devlogi z kodem symulacji w środku i jeden poradnik techniczny HyperFrames. Flagi `main_sample` i `inclusion_class` pozwalają odtworzyć ten podział. 80-sekundowe demo Remotion zostało wykorzystane wyłącznie jako pomocnicza informacja z README i nie jest pozycją katalogu.

Dobór celowy, bez uogólnienia na cały YouTube. W próbie głównej pochodzenie kanałów to PL 4, i18n 19. Segmenty odbiorców na poziomie filmów to adults 15, children 12, family_youth 17. Liczba filmów z polskojęzycznym wydaniem według katalogu wynosi 11. Lokalne wersje PAW Patrol i Bing mają odrębny status od polskich produkcji. Klasyfikacje wieku i techniki są przypisane do dowodów. Wersje bez mowy obejmują m.in. lalkowe Shaun, Reksia i kodowane Milo. Widz dorosły ma w próbie komedię, historię i explainery specjalistyczne.

## Kompletność danych i obserwacji

| Pole | Próba główna 44 | Katalog 60 |
| --- | ---: | ---: |
| Data uploadu ustalona | 33 | 40 |
| Data uploadu Unknown | 11 | 20 |
| Publikacje w oknie 2025-11-11 – 2026-11-11 | 14 | 17 |
| Długość w sekundach ustalona | 12 | 13 |
| Długość Unknown | 32 | 47 |
| Publiczne wyświetlenia ustalone | 33 | 40 |
| Publiczne wyświetlenia Unknown | 11 | 20 |
| Wyświetlenia odczytane na publicznej stronie 2026-11-11 | 11 | 11 |
| Co najmniej jedna użyteczna klatka | 11 | 11 |
| Użyteczna klatka i odczytane napisy | 7 | 7 |

Data uploadu, długość i licznik są równocześnie znane dla 12 pozycji głównych i 12 pozycji całego katalogu. Daty indeksu i liczniki odczytane z wyników wyszukiwania mogą pochodzić z wcześniejszych kopii. Ich data odczytu dotyczy dnia badania. Dwa znane konflikty daty premiery o jeden dzień zapisano wraz z wartością alternatywną. Czas odtwarzacza i czas wersji archiwalnej mogą się różnić. Świeży upload starszej produkcji liczy się jako świeża publikacja. Wydawca lub posiadacz praw często identyfikuje film jako pojedynczy odcinek w opisie, a widoczne kompilacje, zwiastuny, Shorts i materiały o produkcji pozostają poza próbą główną.

Oceniono kadry z 11 filmów. Z 7 filmów wyeksportowano i faktycznie odczytano napisy, w tym dwa automatyczne zapisy PL. Dla opisu struktury skorzystano także z adaptacji lekcji autora i dokumentacji kodu. Pełne odtworzenia w całości i odsłuchy wynoszą po 0. Zakres każdego filmu i timestampy są w katalogu oraz [dzienniku oględzin](../evidence/VIEWING_LOG.md). Dane o retencji, CTR, watch time, kosztach i przychodach są nieznane. Ze względu na różne daty uploadu, wiek filmów, wielkość kanałów i brak jednolitych dat crawlu katalog nie wyprowadza rankingów skuteczności ani wniosków przyczynowych.

## Dowody kodu i otwarte pola

Czternaście publikacji ma źródło wskazujące konkretny udział kodu. Rozkład `code_evidence_scope` to embedded_simulation_code 2, episode_engine_code 2, episode_project_code 1, episode_scene_code 3, full_episode_code_claim_no_public_repo 2, series_scene_code 4. Kod pełnego projektu odcinka, kod pojedynczej sceny i silnik kanału mają osobne pola. Milo dostarcza najbliższego dowodu dla pełnej kodowanej bajki z powracającą postacią. Istnienie animacji potwierdzają publikacje, zakres udziału kodu pozostaje deklaracją autora. Otwarty kod silnika Remotion wiąże się z konkretnymi linkami do explainerów. Publiczny katalog projektu HyperFrames wiąże się z pełnym instruktażem. Repo symulacji CodeParade i Sebastian Lague dowodzi pochodzenia warstwy wizualizacji. Montaż pozostaje nieustalony.

W próbie brakuje polskiego pełnego kodowanego odcinka z powracającymi postaciami i dostępem do kodu produkcyjnego. Brakuje również pełnego odsłuchu oraz publicznego projektu wieloodcinkowej, kodowanej animacji dialogowej z audytem lip sync. Bez kodu danego filmu przyjęto ostrożną klasyfikację lub zapisano Unknown. Niczego nie renderowano ani nie instalowano. Hipotezy zastosowań FrameCore zawierają osobne [karty odcinków](DEEP_DIVES.md).

## Rejestr źródeł katalogu

101 pozycji to zapisy proweniencji, w tym adresy YouTube, otwarte strony twórców, repozytoria i dziennik oględzin. Rekord z błędem odczytu strony lub samym nagłówkiem służy śladowi weryfikacji. Wartość dowodowa zależy od pola, które źródło faktycznie wspiera. Zob. [rejestr katalogu](sources.json).

| Evidence type | Liczba |
| --- | ---: |
| live_youtube_metadata_and_sample | 2 |
| live_youtube_metadata_and_sample_log | 1 |
| opened_corroborating_source | 2 |
| opened_creator_about | 2 |
| opened_creator_case | 1 |
| opened_creator_interview | 1 |
| opened_creator_production_writeup | 1 |
| opened_episode_context | 7 |
| opened_institution_release | 1 |
| opened_primary_context | 18 |
| opened_producer_campaign_faq | 1 |
| opened_source_repository | 4 |
| search_result_metadata | 51 |
| watch_page_access_attempt | 8 |
| watch_page_shell | 1 |
