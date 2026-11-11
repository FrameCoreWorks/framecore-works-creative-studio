# Backlog P0/P1/P2

Wszystkie zadania to propozycje po researchu, **NOT_RUN**. Nie są zleceniem instalacji ani zmianą polityki. Priorytet DERIVED według nowej użyteczności, praw, metadanych, trwałości i kosztu utrzymania; P0 nie oznacza najwyższej popularności. Testy opisuje TEST_PLAN.md.

## B01 · P0 · Potwierdzić zakres kwalifikacji i dokładne pola obecnego kontraktu przed zmianą rejestru.

- Wejścia: baseline/baseline.json; catalog.json; RIGHTS_AND_EVIDENCE.md.
- Wyjścia: decyzja Claude per provider/format; diff plan bez wdrożenia.
- Właściciel: Claude — architekt; Codex — wykonawca przyszłego scope.
- Zależności: brak.
- Błędy: nieuwzględniony host; prawa metadata utożsamione z plikiem; podwójna polityka praw.
- Limity: 0 provider downloads; tylko review dokumentów i dokładnych pól.
- Koszt: 0 zewnętrznych operacji płatnych; nakład pracy Unknown.
- Test akceptacyjny: Każdy przyjęty scope wskazuje existing field/nowe proposed field, właściwy rights_status oraz host NOT_RUN do czasu proof. (T02, T17, T18)
- Status: NOT_RUN.

## B02 · P0 · Zweryfikować małą dozwoloną podkolekcję Internet Archive pod recorded audio/music/video.

- Wejścia: karta Internet Archive; 2–3 real metadata records; historyczne wykluczenie archive.
- Wyjścia: kwalifikacja jednego subsetu; projekt archive.py/registry/dossier i fixtures.
- Właściciel: Codex — adapter po scope approval; Claude — review.
- Zależności: B01.
- Błędy: brak per-file rights; usunięty plik; rotujący nieprzejrzany host; za duży oryginał.
- Limity: 3 records metadata; 1 przyszły plik ≤5 MiB, bez broad crawl i wildcard wszystkich domen.
- Koszt: publiczne odczyty bez opłaty wg dokumentacji; transfer/utrzymanie Unknown.
- Test akceptacyjny: Dopuszczony plik ma stabilny item+filename, jawne prawa i twórcę; plik sąsiedni o niepewnych prawach pozostaje blocked. Żaden existing CDN import nie jest blanket qualification. (T01, T02, T05, T06, T09, T17)
- Status: NOT_RUN.

## B03 · P0 · Rozważyć audio NASA jako najmniejsze rozszerzenie już istniejącego providera.

- Wejścia: nasa.py pinned; NASA media_type=audio docs; item restrictions.
- Wyjścia: propozycja kategorii audio w istniejącym module; fixture review_nasa; oddzielny host proof po zgodzie.
- Właściciel: Codex — przyszły wykonawca; Claude/Studio — odbiór zakresu użycia.
- Zależności: B01.
- Błędy: brak item-specific review; variant >32 MiB; próba reuse photo proof; Earshot reject.
- Limity: 1 search, max3 results, 1 mały audio plik w przyszłej próbie.
- Koszt: 0 opłaty API/download wg publicznej dokumentacji; review praw/utrzymanie Unknown.
- Test akceptacyjny: Bez notatki review_nasa odmowa; proof audio osobny; route do Earshot nie obchodzi jego eligible-only import. (T04, T12, T17, T18)
- Status: NOT_RUN.

## B04 · P0 · Zachować dowody i zgodność Open Assets → Studio → Earshot bez fałszywego rozszerzenia licencji.

- Wejścia: baseline contract/limits; Toolbox source-records.md; ADAPTER_DESIGNS.md.
- Wyjścia: consumer matrix; testy compatibility bez zmiany istniejących nazw; jawne unexecuted_checks.
- Właściciel: Claude — wybór granicy konsumentów; Codex — przyszłe fixtures.
- Zależności: B01.
- Błędy: license/licence rename; SA lub BY1.0 w Earshot; technical-only udaje production; brak trace artifact.
- Limity: local metadata fixtures, 0 live provider requests.
- Koszt: 0 zewnętrznych usług; nakład pracy Unknown.
- Test akceptacyjny: Sidecar i envelope zachowują różne właściwe nazwy; hash_source local_only nie udaje SHA providera; review/SA odrzucone przez obecny Earshot. (T03, T17, T18, T19)
- Status: NOT_RUN.

## B05 · P1 · Zaplanować wąski bezpieczny SVG dla PhyloPic i wybranej kolekcji Iconify.

- Wejścia: karty Iconify/PhyloPic; 3 source records; obecny brak SVG decode.
- Wyjścia: proposal bounded SVG parser + renderer; per-icon notices mapping; schema additions tylko addytywne.
- Właściciel: Claude — architekt formatu; Codex — przyszła implementacja.
- Zależności: B01, B04.
- Błędy: script/event/external reference; nieobsługiwana licencja; kolekcja nadpisuje wyjątek; zbyt złożony SVG.
- Limity: max256 KiB/SVG w spike, max1 raster preview, bez network z renderera i bez instalacji.
- Koszt: API publiczne bez opłaty wg dokumentacji; nowe utrzymanie/QA Unknown.
- Test akceptacyjny: T13 odrzuca aktywne SVG, T16 wybiera właściwą licencję; raster proof nie certyfikuje wektora; jeden istniejący license_policy rozszerzony po review. (T13, T16, T17)
- Status: NOT_RUN.

## B06 · P1 · Ocenić Fontsource/Google Fonts repo jako jedną deduplikowaną ścieżkę fontów.

- Wejścia: karty Fontsource i Google Fonts; OFL original text; family/variant metadata.
- Wyjścia: font capability proposal; per-family source+notices; readonly validation plan bez instalacji systemowej.
- Właściciel: Claude — decyzja kategorii; Codex — przyszły adapter.
- Zależności: B01, B04.
- Błędy: OFL traktowane jak media CC0; brak RFN/notices; mieszane licencje rodziny; mirror counted twice.
- Limity: 1 rodzina, 2 variants metadata, 1 font ≤1 MiB w przyszłej próbie.
- Koszt: publiczny katalog bez opłaty; transfer, utrzymanie i review licencji Unknown.
- Test akceptacyjny: Rozdzielone użycie tekstu od redystrybucji font file; oryginał i wersja zachowane; Developer API z key nie udaje core. (T15, T17, T19)
- Status: NOT_RUN.

## B07 · P1 · Ocenić Wyzowl SFX Kit jako wersjonowany static manifest do synthetic motion SFX.

- Wejścia: sounds.json pinned; CC0 record/prawa; 2–3 manifest entries.
- Wyjścia: static-manifest mapping do istniejącego sfx; nowość opisana jako synthetic; plan cache/commit update.
- Właściciel: Codex — przyszły adapter; Claude — priorytet użytkowy.
- Zależności: B01, B04.
- Błędy: synthetic udaje recorded; run generator zamiast download; repo license bez asset scope; brak wariantu.
- Limity: wybrane entries, żadnego klonowania całego repo; max1 WAV ≤5 MiB w spike.
- Koszt: 0 opłaty assetów CC0; utrzymanie static manifest Unknown.
- Test akceptacyjny: Manifest/revision i plik mają powiązane prawa; exact URL/ID; T12 i T17 po zgodzie, generator nigdy uruchamiany przez downloader. (T01, T06, T12, T17)
- Status: NOT_RUN.

## B08 · P1 · Utrzymać jawny nierozwiązany recordedSFX/stock-alpha gap i porównać koszt alternatywnych ograniczeń.

- Wejścia: rankingi AUDIO_VIDEO; manual NPS/CLR; OPTIONAL Freesound/Pixabay Video.
- Wyjścia: decyzja użytkownika: pozostać no-key/manual albo osobny authorized optional scope; bez zmiany core policy.
- Właściciel: Claude + użytkownik.
- Zależności: B02.
- Błędy: przemycenie abonamentu; ciche konto/key; brak zgody na scraping; paczkę NC oznaczono free.
- Limity: tylko review; 0 usług płatnych/credentials/download.
- Koszt: OPTIONAL usługi mogą wymagać opłat/zgód; dokładny koszt zgodnie z kartą lub Unknown.
- Test akceptacyjny: Wybór nie deklaruje że wszystkie luki są pokryte; brak danych pozostaje Unknown, brak instalacji i automatycznego zakupu. (T02, T20)
- Status: NOT_RUN.

## B09 · P2 · Rozwinąć PBR/HDRI/3D dopiero po natywnej walidacji formatu i pakietów.

- Wejścia: baseline: Poly Haven/ambientCG oraz ich niewspierane formaty (bez nowej karty katalogu); baseline decoder limits.
- Wyjścia: format capability proposal; bounded archive/import plan; map semantic roles i color space.
- Właściciel: Claude — architekt; Codex — przyszły format worker.
- Zależności: B01, B04.
- Błędy: preview uznane za model; ZIP traversal/bomb; aktywny blend/script; EXR nieobsługiwane.
- Limity: 1 asset bundle bounded do istniejących limitów lub osobno zatwierdzony scope, bez Blender scripts.
- Koszt: prawa i access zależne od źródła; nowe dekodery/utrzymanie Unknown.
- Test akceptacyjny: Każdy plik/wariant osobno weryfikowany, project members nie stają się approved przez sam CRC/raster decode. (T08, T12, T14, T17)
- Status: NOT_RUN.

## B10 · P2 · Rozpatrzyć AIC/Openverse i inne źródła uzupełniające po zamknięciu luk praw/dostępu.

- Wejścia: OPTIONAL i MANUAL_REFERENCE_ONLY cards; blocked-source log; real protected/public records.
- Wyjścia: item/origin-based decision; no unqualified arbitrary downloader.
- Właściciel: Claude — architekt/research owner.
- Zależności: B01, B02.
- Błędy: image_id udaje PD; agregator udaje origin; HTTP403 jest obchodzone; mały przyrost coverage.
- Limity: metadata-only do czasu dopuszczenia; brak masowego indeksowania.
- Koszt: 0 dla potwierdzonych public reads; commercial/heavy access i praca Unknown gdzie brak warunków.
- Test akceptacyjny: Nowość uzasadniona bez dopełniania muzeami; exact origin licence + documented automation + real-host proof przed dodaniem do core. (T01, T02, T09, T10, T18)
- Status: NOT_RUN.
