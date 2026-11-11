# Niezależna recenzja dokumentów DR-04

Data: 2026-11-11. Wynik: **PASS_WITH_LIMITATIONS**. Zakres: **DOCUMENT_REVIEW_ONLY**.

Nie znaleziono otwartych uwag blocking ani major. Trzy drobne uwagi zostały poprawione przez autora i ponownie odczytane przez recenzenta. Wynik pozwala przekazać pakiet badawczy do analizy; nie zatwierdza architektury, wdrożenia, praw plików ani gotowości hosta.

## Zakres i metoda

Przeczytano cały PROMPT.md, zasady modeli wszyscy/codex i przekazane AGENTS. Zastosowano verification-before-completion. Oceniono raport, baseline Markdown/JSON, oba katalogi specjalistyczne i zbiorczy katalog JSON/CSV, karty audio_video/visual_data, rejestr źródeł, rekordy, RANKINGS, RIGHTS_AND_EVIDENCE, ADAPTER_DESIGNS, BACKLOG/backlog.json, TEST_PLAN, IMPLEMENTATION_HANDOFF, GAPS i MANIFEST_EXAMPLE. Odczytano także verify_artifacts.py oraz bieżący VERIFICATION.md (PENDING przed końcowym gate leada).

Własna kontrola wyłącznie dokumentów potwierdziła liczniki, unikatowe ID, powiązania provider–record–source, pełną zgodność wszystkich eksportowanych pól CSV z JSON i SHA-256 oryginalnego promptu. Odczyt lokalnych core.py/runtime.py z cache Open Assets 0.5.0 potwierdził mapowanie sidecara i koperty oraz bramki licencyjne; kodu nie uruchamiano. Nie pobrano binariów ani nie użyto usług płatnych.

## Ustalenia

- Baseline: 15 providerów / 24 pary provider–category. Katalog: 26 pozycji, 10 kart DEEP, 22 wpisy metadanych. Ranking 3/13/6/4 i nowość 23/2/1 są zgodne między danymi i raportem. Nowy provider nie jest tożsamy z nową biblioteką unikatowych plików; dublowanie OpenMoji, fontów i agregatorów ujawniono.
- Źródła: 204 wpisy, 194 unikatowe URL; 196 READ, 6 BLOCKED, 2 INDEXED_EXCERPT. Openverse ma dodatkowy direct_read_status BLOCKED przy INDEXED_EXCERPT, więc licznik głównej klasyfikacji nie jest liczbą wszystkich nieudanych prób. Archive bots zachowuje wcześniejszy READ i bieżący BLOCKED. Rejestr nie udaje listy 204 niezależnie potwierdzonych teraz stron.
- Trzy CORE_CANDIDATE są warunkowe. Konto, klucz, opłata, licencja własna i droga ręczna nie zostały przemycone do głównej kwalifikacji. NASA audio zachowuje review_nasa; Iconify i fonty wymagają nowych kontroli formatu/licencji. Źródła statyczne pozostają odróżnione od publicznych API.
- Prawa metadanych, kolekcji i konkretnego assetu są oddzielone. SA nie staje się CC0; AIC image_id nie dowodzi praw; Fontsource upstream OFL nie zastępuje notice dystrybuowanego wariantu. Jurysdykcja, osoby/marki i redystrybucja pliku pozostają osobnymi warunkami.
- Sidecar zachowuje id/source_page/license; envelope asset_id/source_url/licence. Szablon manifestu jest wyraźnie niewykonywalny, z null dla hash/decode i osobno oznaczonymi propozycjami. Parametry z metadanych nie zostały przedstawione jako pomiar.
- Brak automatic retry/failover, stop po blokadzie, limity pliku i exact-host control odpowiadają opisanemu baseline. Zmiany formatów są propozycjami; testy T01–T20 wszystkie NOT_RUN. Dokumenty nie utożsamiają cache, kodu, AUTHOR_TEST i działającej sesji.

## Uwagi poprawione w trakcie recenzji

| ID | Waga | Plik | Wynik |
|---|---|---|---|
| DR04-R01 | minor | BACKLOG.md / backlog.json | Pexels zastąpiono zbadanym Pixabay Video. |
| DR04-R02 | minor | audio_video/CARDS.md | Naprawiono dwa uszkodzone zapisy „próbie”. |
| DR04-R03 | minor | REPORT.md / priorytety pakietu | Dopisano nadrzędność głównego backlogu; P0 kwalifikacji nie jest automatycznym nakazem implementacji. |

## Wąskie sprawdzenie źródeł pierwotnych

2026-11-11 recenzent odczytał trzy oficjalne strony, bez wywoływania adapterów i pobierania mediów. Potwierdzają odpowiednio strukturę wariantów WOFF/WOFF2/TTF, zakres limitu wyszukiwania 32–999 oraz ISC z wyjątkami MIT w Lucide. Lista wyjątków nie wymienia camera. [Fontsource Font ID](https://fontsource.org/docs/api/font-id), [Iconify search](https://iconify.design/docs/api/search.html), [Lucide license](https://lucide.dev/license).

To sprawdzenie dokumentów nie potwierdza transferu, gotowości rendererów, notice konkretnego pakietu ani praw do wszystkich ikon. Nie powtarzano niedostępnych źródeł i nie szukano obejść blokady.

## Ograniczenia

- DOCUMENT_REVIEW_ONLY: brak akceptacji architektury, implementacji, testu produktu ani potwierdzenia host readiness.
- Recenzent nie powtórzył wszystkich 204 odczytów źródłowych. Sprawdził rejestr, spójność odwołań, karty oraz trzy oficjalne strony w wąskim spot-checku; historyczne READ pozostają dowodem badaczy.
- Brak binarnych pobrań, decode, odsłuchu, oceny artystycznej i niezależnego potwierdzenia praw do konkretnych plików. 22 wpisy to metadane, w tym strony i wyciągi indeksu, nie 22 pobrane pliki.
- NASA: 3 wpisy Artemis bez potwierdzonego NASA ID/API membership. Openverse: zero rekordów, spec tylko INDEXED_EXCERPT i bezpośredni 403.
- Internet Archive ToS i bieżący odczyt bots oraz AIC ToS/licensing pozostają nieodczytane lub zablokowane; nie obchodzono blokad. CLR ma sprzeczności SA i wtórne źródła.
- Iconify i Fontsource są warunkowymi CORE_CANDIDATE; wymagają nowych formatów i rozszerzenia jednej polityki praw. Notice konkretnego pakietu Fontsource do ustalenia.
- Luki no-key recorded SFX, muzyki wielu twórców i stock alpha pozostają otwarte. Manual/optional ani publiczny katalog ich automatycznie nie zamykają.
- W czasie odczytu VERIFICATION.md miał PENDING do końcowego gate rodzica. Końcowy wynik integralności musi zostać zapisany przez leada po tej recenzji.
- Model obserwowany Unknown: potwierdzenie dispatch nie dostarcza niezależnej telemetrii modelu.

Model żądany: `gpt-6-astra`, effort żądany: `high`. Model zaobserwowany: `Unknown: dispatch ack no independent model telemetry`.
