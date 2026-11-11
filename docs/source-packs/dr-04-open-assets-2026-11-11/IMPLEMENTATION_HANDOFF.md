# IMPLEMENTATION_HANDOFF — DR-04 dla Claude

Data: 2026-11-11. Właściciel architektury: **Claude**. Status: **materiał do analizy; brak akceptacji architektury i brak implementacji**. Hipson **T-0007** śledzi ukończenie badania, nie gotowość providerów.

## Katalog pakietu

`. (katalog tego pakietu; zob. PORTABILITY.md)`

Zacznij od REPORT.md i baseline/BASELINE.md, potem catalog.json/RANKINGS.md, ADAPTER_DESIGNS.md, BACKLOG.md, TEST_PLAN.md i review/REVIEW.md. Dane źródłowe: sources.json i records.json; pełne karty w audio_video/CARDS.md i visual_data/CARDS.md. PROMPT.md pozostaje oryginałem.

## Co ustalono

- 15 aktualnych providerów / 24 ścieżki; pięć historycznych prób Work tylko technical-only. Cache 0.5.0 odpowiada przypiętemu pakietowi, aktywna rejestracja klienta Unknown.
- 26 kandydatów/rozszerzeń: 3 warunkowe core, 13 optional, 6 manual/reference, 4 rejected; 10 deep, 22 wpisy metadanych. Nowe provider product tests i wszystkie host readiness NOT_RUN.
- Najmniejszy scope: NASA audio w istniejącym adapterze, z zachowaniem review_nasa i oddzielnego proof. Trzy przykłady Artemis to strony, nie potwierdzone rekordy images-api.
- Iconify i Fontsource wymagają bezpiecznych nowych formatów oraz rozszerzenia **tej samej** polityki praw dla ikon/font software. Static Google Fonts i Wyzowl to osobne drogi dostępu; nie przedstawiać ich jako gotowych API adapterów.
- RecordedSFX, muzyka wielu twórców i stock alpha pozostają nierozwiązane w pełnych warunkach core. Archive trzeba zawęzić do dozwolonej podkolekcji i powiązać prawa item/file. Nie awansować go na podstawie dawnego pojedynczego decode.

## Decyzje do podjęcia

1. Wybrać jeden pierwszy scope: NASA audio albo review wąskiej podkolekcji Archive. P0 Archive oznacza kwalifikację, nie polecenie implementacji.
2. Czy SVG ma być nowym weryfikowanym wariantem graphics? Określić static subset, ograniczenia parsera/renderera i obsługę per-icon notices; najpierw jedna kolekcja. Nie wykonywać zewnętrznych refs ani skryptów.
3. Czy fonts otrzymuje osobny typ w istniejącym kontrakcie? Ustalić OFL/RFN, wersje, glyph coverage, dystrybucję bez instalacji systemowej i źródłowe notices.
4. Zachować różnicę pól sidecar/envelope i granice Earshot: `eligible`, CC0/PDM/BY2+; SA, BY1.0, NASA review i technical-only nie są obecnie dopuszczonym importem. Nie zmieniać gate w ramach adaptowania pojedynczego providera.
5. Wybrać sposób obsługi źródeł manual i OPTIONAL z kluczem/kosztem. Te warunki nie rozszerzają zgód użytkownika; badanie ich nie aktywuje.

## Konkretny scope małej przyszłej próby

Po review i wymaganej zgodzie: jedna kategoria/prowider, max3 wyniki, max6 metadata GET, jeden oficjalny wariant preferowany ≤5 MiB, bez podnoszenia globalnych limitów, rzeczywisty host/model i nowy output. Licencja per asset, hash/decode, sidecar/envelope oraz poprawna odmowa na negatywnym rekordzie. Stop po 401/403/429/challenge/egress blockade. T01–T20 w TEST_PLAN.md są specyfikacją, nie wynikami.

## Otwarte braki

Aktualne ToS IA i AIC nieodczytane w pełni; Openverse bez rzeczywistych rekordów; NPS/CLR/Blender bez potwierdzonego kompletnego API tej kolekcji; exact legal notice dystrybucji Fontsource wymaga sprawdzenia przed plikiem; nowe SVG/font/HDR/3D dekodery nie istnieją w badanym runtime. Prawa wizerunku, marki, jurisdiction i jakość artystyczna muszą zostać rozstrzygnięte per use.

## Prompt do dalszej pracy

> Przeczytaj pakiet DR-04 w katalogu tego pakietu wskazanym powyżej, zaczynając od REPORT.md, baseline/BASELINE.md, review/REVIEW.md i ADAPTER_DESIGNS.md. Jako główny architekt oceń trzy warunkowe CORE_CANDIDATE oraz P0 backlog, zachowując istniejący contract, license_policy i blockade stop. Rozdziel decyzję architektoniczną, implementację i test wykonawczy. Zaproponuj najmniejszy konkretny scope pierwszej próby; nie traktuj Hipson done ani kontroli dokumentów jako dowodu działania produktu. Nie zmieniaj konfiguracji, nie instaluj i nie aktywuj OPTIONAL bez właściwego zlecenia.

Nie wysłano tego promptu do innego czatu. Materiał pozostaje w katalogu DR-04; w tym zleceniu Shared był tylko do odczytu.
