# Projekty rozszerzeń — do analizy Claude

Status: **DERIVED / NOT_RUN**. Nie napisano ani nie zainstalowano adapterów. Właścicielem decyzji architektonicznej pozostaje Claude. Nazwy plików poniżej oznaczają proponowane miejsca w repo, nie pliki utworzone w tym badaniu.

Punktem odniesienia jest [contract.md](https://github.com/FrameCoreWorks/framecore-open-assets/blob/889471fcdbc2216ddc465715eff0e82784d5b8ee/plugins/framecore-open-assets/skills/open-assets/references/contract.md), [runtime.py](https://github.com/FrameCoreWorks/framecore-open-assets/blob/889471fcdbc2216ddc465715eff0e82784d5b8ee/plugins/framecore-open-assets/scripts/runtime.py) i [core.py](https://github.com/FrameCoreWorks/framecore-open-assets/blob/889471fcdbc2216ddc465715eff0e82784d5b8ee/plugins/framecore-open-assets/scripts/core.py), odczyt 2026-11-11. Szczegóły endpointów i rekordy: karty specjalistów oraz katalog.

## Zachowany przepływ

`query → search(client, query, category, limit) → details/licence → variants → core.asset()/license_policy() → signed search → explicit verify/download → core.download()/decode() → .asset.json → framecore-task-result/1 → Studio`

1. Sprawdzić znany provider, kategorię, 1–240 znaków query i limit 1–5 wyników. Nie dodać automatycznej federacji jako fallbacku.
2. Użyć `Client.json/get` i istniejącej polityki domen. Wariant URL pochodzi z udokumentowanego pola odpowiedzi/manifestu; nie zgadywać CDN.
3. Ustalić prawa dokładnie wybranego obiektu/pliku. Zachować `blocked` dla Unknown/NC/ND, `review_sa` dla SA, `review_nasa`/`review_jurisdiction` gdzie właściwe. Nie nadpisywać statusu przez preferencję użytkową ani ranking.
4. Zapisać niezmieniony podpisany wynik. Download wiąże go z lokalnym state, hostem, fingerprintem runtime i datą <24 h. Zmiana wariantu/URL/wersji wymaga nowego wyniku, nie edycji podpisanego pliku.
5. Zweryfikować rzeczywisty plik i zapisać sidecar oraz istniejący envelope. Readiness musi powstać na rzeczywistym hoście/providerze/kategorii. Technical-only proof nie otwiera użycia produkcyjnego.
6. Studio otrzymuje lokalny media file, sidecar, envelope i `unexecuted_checks`; FrameMotion/FrameCut używają pliku, Toolbox/Earshot wykonuje autoryzowane dalsze operacje audio. Open Assets nie przejmuje montażu ani generowania.

## Macierz projektów

| Projekt | Minimalny zakres | Mapowanie i zależności | Warunek wejścia / rozstrzygnięcie |
|---|---|---|---|
| NASA audio | rozszerzyć istniejący `nasa.py`, manifest i testy o `audio`; bez nowego providera | `nasa_id` → `id`, creator/description/links z API; `media_type=audio`, warianty z asset manifest | `EXISTING_NEW_CATEGORY`; zachować `review_nasa`, potwierdzić prawa nagrania i rozmiar wariantu. Oddzielny proof audio. |
| Internet Archive | nowy `archive.py` tylko wybrana dozwolona podkolekcja, nie blanket Archive | search ID → metadata/files → plik original/derivative z czytelnym powiązaniem praw; item creator, licenseurl i description zachowane | wcześniejsze wykluczenie wymaga ponownego uzasadnienia. Licencja item nie może automatycznie objąć cudzych załączników. Hosty/redirecty i 32 MiB często ograniczają materiał. |
| Iconify | wąska kolekcja z potwierdzonymi prawami, np. Lucide po wyjątkach, nie wszystkie kolekcje naraz | API collection/prefix/name + wersja i źródłowe notices; mapping SVG do graphics dopiero po zgodzie na format | nowy bezpieczny tor SVG i rozszerzenie istniejącego parsera licencji. ISC/MIT kodu nie utożsamiać z licencją dowolnego zbioru ikon; wyjątki Feather per element. |
| PhyloPic SVG | rozszerzyć istniejący `phylopic.py` o jawny wektorowy wariant | zachować UUID i prawa konkretnej sylwetki; raster pozostaje odrębnym wariantem | nowy format, nie nowa kolekcja. SA zachowuje bramkę. Zależność od toru SVG; nie rejestrować proof dla SVG na podstawie PNG. |
| Fontsource / Google Fonts | Fontsource jako dokumentowane API metadanych, repo fontów jako wersjonowane źródło praw; deduplikacja wspólnych rodzin | family + version + subset + weight + style + format; sidecar z pełnym notices/OFL i RFN; nie nazwać fontu grafiką | osobna nowa kategoria/font decoder oraz rozszerzenie jednej polityki licencji, do decyzji Claude. Google Fonts Developer API z key poza core; repo statyczne osobno. |
| Wyzowl SFX Kit | oficjalny wersjonowany manifest `sounds.json`; wyszukiwanie lokalne po tagach, exact WAV URL z manifestu | rekord ID/path + commit + duration/tags/sync.at; CC0 powiązane z manifestem | nowy static-manifest adapter, nie API serwisu. Rozszerza synthetic SFX, nie recorded. Nie uruchamiać generatora z repo. |
| AIC | nowy provider zdjęć/reprodukcji tylko jeśli zamknięte luki warunków i hosta | `is_public_domain` oraz `image_id` rozpatrywane oddzielnie; IIIF wariant wyłącznie wg dokumentacji | OPTIONAL: image_id występuje też przy obiektach chronionych; historyczne Work 403. Nie traktować tego jako nowoczesnej ilustracji. |
| Openverse | tylko discovery → źródło pierwotne → kwalifikowany istniejący/nowy adapter | origin URL/ID i attribution zachować; nie pobierać dowolnej domeny z agregatora | OPTIONAL: prawa i dostęp ponownie rozstrzyga źródło; brak ogólnego downloadera arbitrary URLs, nie dodawać wildcard dla całego Internetu. |
| Kuratorowane paczki/strony | np. NPS/CLR/Blender: manual intake lub oddzielny zatwierdzony static manifest | zachować asset source i specyficzne LICENSES/credits; manifest lokalny nie jest oficjalnym API | bez udokumentowanego maszynowego katalogu nie trafiają do core API. Nie scrapować HTML jako obejścia. Paczki ze sprzecznymi prawami pozostają w review/blocked. |

Powyższe są projekty do rozważenia, a nie identycznie pilne implementacje. Kolejność określa BACKLOG; ranking katalogu ma pierwszeństwo dla kwalifikacji konkretnego źródła.

## Kontrola plików i rzeczywiste ograniczenia

| Obszar | Obecny kod — CODE_INSPECTED | Wymagana decyzja/rozszerzenie — DERIVED |
|---|---|---|
| URL/redirect | HTTPS, bez credentials/fragmentu, port 443, review domen, do 5 redirectów; każda domena sprawdzana | wypisać exact hosts z realnych rekordów; podpisane URL nie stają się trwałym ID. Nie dopisywać hostu po 403. |
| MIME/rozszerzenie | HTML nagłówkiem/prefixem odrzucane; decode według magic bytes, potem zgodność medium z kategorią | `application/octet-stream` samo nie dowodzi błędu; po decode opisać MIME mismatch. SVG/HTML aktywne nie wchodzą dzisiejszym dekoderem. |
| Limity | JSON 8 MiB, media 32 MiB; timeout socket 25 s, odczyt 60 s; 30 logical get/Client; obraz 40 MP | nie podnosić limitów globalnie dla jednej paczki. Preferować mniejszy oficjalny wariant; brak wariantu → odmowa. |
| Audio/wideo | ffprobe 30 s, ffmpeg full decode 90 s, 2 threads, whitelist local file/pipe i formatów | pełna długość pliku nie ma osobnego limitu sekund. FPS, sample rate, channels, dimensions, alpha/pixel format nie są obecnie zapisane w zwracanym verification; proponować addytywnie, nie udawać istniejących pól. |
| ZIP | ≤100 entries, suma uncompressed ≤128 MiB, CRC, decode rastrów; nie ekstrahuje | brak ekstrakcji oznacza brak zapisu path traversal dziś. Przy przyszłej ekstrakcji: reject absolute/.. paths, symlinks, nested archives, ratio bomb i limit CPU; nie otwierać .blend/skryptów. Dzisiejsza obecność `.blend` to unverified member. |
| Hash i oryginał | lokalny SHA-256, advertised SHA/bytes porównywane, hash_source provider/local_only, nowe ścieżki | duplikaty porównywać po SHA tylko po pobraniu; ID/title to wskazówki. Nie usuwać oryginału, nie zastępować nowym URL, oddzielać transformację jako derived output. |
| SVG/font/3D | nieobsługiwane jako native media | SVG: zakaz scripts/events/external refs, bounded parser/raster preview do testu. Font: bez instalacji systemowej, validate tables i exact file licence. 3D: oddzielny importer bez wykonania kodu i pełen manifest plików. Wszystko propozycje NOT_RUN. |

## Cache i blokady

Zachować **brak automatic retry**. 401/403/429/challenge/network policy blockade kończą wywołanie i powstrzymują dalszą federację; nie kontynuować pod innym providerem jako ukryty failover. Dla rzeczywiście przejściowego błędu można rozważyć najwyżej jedną dodatkową próbę ręcznie, z nazwaną hipotezą i poszanowaniem Retry-After. Nie jest to zgoda na powtarzanie blokady.

Obecny cache JSON: exact URL + Accept, max-age ≤1 dzień, no-store/no-cache/private blokują reuse, stale ETag może revalidate, `--fresh` pomija. Last-Modified jest rejestrowany, nie oznacza zaimplementowanego If-Modified-Since. Media to lokalny jawny output. Dla static manifests zachować commit/version oraz provenance źródła. Nie budować drugiego cache mediów ani drugiego rejestru praw.

Publiczne GitHub REST ma bez uwierzytelnienia 60 requests/h/IP, a search ma własne ograniczenia. To oddzielne od kosztów/usług konta użytego przez connector podczas researchu; odczyt connectora nie dowodzi anonimowej gotowości adaptera. Uwzględnić seryjność, warunkowe GET i stop po rate limit. [GitHub rate limits](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api), [best practices](https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api), odczyt 2026-11-11, DOCUMENTED. Nie przenosić zalecanego tam exponential retry do Open Assets, którego własny kontrakt jest bardziej restrykcyjny.

## Nazwy sidecara i envelope

Zachować sidecar: `provider`, `id`, `source_page`, `creator`, `license`, `license_url`, `attribution`, `rights_status`, `retrieved_utc`, `selected_variant`, `sha256`, `bytes`, `response_headers`, `verification`, `downloaded_utc`, `host`, `model`, `runtime_version`, `fingerprint`, `search_utc`, `search_query`, `task_id`, `trace_sha256`, `hash_source` oraz bramki praw.

W envelope odpowiadają im m.in. `asset.provider`, `asset.asset_id`, `asset.source_url`, `asset.licence`, `asset.credits.creator`, `asset.retrieval`, `outputs[].sha256`, `verification_evidence`, `unexecuted_checks`. Nie przepisywać `license` na `licence` w sidecarze. Propozycje nowych pól to addytywne `verification.fps`, `sample_rate`, `channels`, `alpha_mode` i `pixel_format` oraz provenance wersji repo/manifestu; wymagają schema/consumer review. Szablon `MANIFEST_EXAMPLE.json` jest materiałem projektowym, nie wykonywalnym podpisanym wynikiem ani realnym pobraniem.
