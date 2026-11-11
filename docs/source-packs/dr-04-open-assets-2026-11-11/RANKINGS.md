# Rankingi i pokrycie kandydatów

Data 2026-11-11. Wszystkie decyzje DERIVED; każdy host NOT_RUN. Pełne osie, warunki i źródła są w catalog.json/CSV i kartach. CORE_CANDIDATE jest warunkowy, nie oznacza gotowej integracji. OUT_OF_CORE z kart specjalistów jest w zbiorczym katalogu pod OPTIONAL z zachowaniem przyczyny. P0_RESEARCH_ONLY oznacza rozstrzygnięcie przed implementacją.

## CORE_CANDIDATE (3)

| Kandydat | Nowość | Media / dostęp | Prawa i ograniczenie |
|---|---|---|---|
| NASA Image and Video Library — audio | EXISTING_NEW_CATEGORY | audio, sfx / DOCUMENTED_PUBLIC_API | REVIEW_REQUIRED_PER_ASSET |
| Iconify | NEW_PROVIDER | graphics, icons, svg / PUBLIC_API | CONDITIONAL: wybrane ikony po weryfikacji upstream, obsłudze notice i rozbudowie tej samej polityki praw; SA i Unknown poza automatycznym zakresem. |
| Fontsource | NEW_PROVIDER | fonts, typography / PUBLIC_API_CDN | CONDITIONAL: pilotaż OFL-1.1 po ustaleniu wersjonowanego LICENSE/copyright tego pliku i rozszerzeniu polityki oraz formatu fontów. |

## OPTIONAL (13)

| Kandydat | Nowość | Media / dostęp | Prawa i ograniczenie |
|---|---|---|---|
| Internet Archive — wybrane kolekcje | NEW_PROVIDER | audio, music, sfx, video / DOCUMENTED_PUBLIC_API | CONDITIONAL_PER_ASSET |
| Wyzowl SFX Kit | NEW_PROVIDER | sfx / OFFICIAL_VERSIONED_REPOSITORY | CC0_DECLARED |
| CLR Music | NEW_PROVIDER | sfx, audio, music / OFFICIAL_STATIC_RELEASE_PACKS | REVIEW_REQUIRED_PER_ASSET |
| Freesound | NEW_PROVIDER | sfx, audio / DOCUMENTED_AUTHENTICATED_API | CONDITIONAL_PER_ASSET |
| Lots of Sounds | NEW_PROVIDER | sfx, audio, music / DOCUMENTED_AUTHENTICATED_API | CC0_DECLARED |
| Pixabay Video | NEW_PROVIDER | video / DOCUMENTED_AUTHENTICATED_API | PROPRIETARY_REVIEW_REQUIRED |
| Google Fonts Files | NEW_PROVIDER | fonts, typography / STATIC_REPOSITORY | CONDITIONAL: pliki pojedynczych rodzin ze zweryfikowaną OFL-1.1 i provenance. Apache-2.0/UFL poza pilotem. |
| Openverse | NEW_PROVIDER | photos, graphics, audio, discovery / PUBLIC_DISCOVERY_API | ORIGIN_REQUIRED: licencja, twórca, wariant i automatyzacja do ponownego ustalenia u dostawcy oryginału. |
| Art Institute of Chicago | NEW_PROVIDER | graphics, photos, cultural-heritage, iiif / PUBLIC_API_IIIF | CONDITIONAL: is_public_domain=true i jawne prawa konkretnego obrazu; formalne Image Licensing i ToS nieodczytane (403). is_public_domain=false odrzucić niezależnie od image_id. |
| PhyloPic — wariant SVG | EXISTING_NEW_CATEGORY | graphics, silhouettes, svg / PUBLIC_API_EXISTING_ADAPTER_EXTENSION | CONDITIONAL: CC0/PDM i obsługiwane CC BY z wymaganym twórcą, licencją i atrybucją; SA/NC wg istniejącego filtra. |
| Smithsonian Open Access | NEW_PROVIDER | photos, graphics, cultural-heritage, 3d / STATIC_DATASET_S3; KEYED_API_SEPARATE | CONDITIONAL: oznaczenie CC0 dla danego zasobu 2D/3D; CC0 metadanych nie świadczy o dostępności ani prawach do medium. |
| OpenMoji — wydania autora | DUPLICATE_MIRROR | graphics, icons, emoji, svg, png / STATIC_RELEASE_REPOSITORY | REVIEW_REQUIRED: CC BY-SA 4.0 dla grafiki, warunki adaptacji i atrybucji wymagają ręcznej decyzji. |
| Unsplash | NEW_PROVIDER | photos, contemporary-stock / KEYED_API; MANUAL_WEBSITE | CONDITIONAL: własna licencja Unsplash dla darmowych zdjęć i odrębne prawa wizerunku/marek; Unsplash+ wyłączony. |

## MANUAL_REFERENCE_ONLY (6)

| Kandydat | Nowość | Media / dostęp | Prawa i ograniczenie |
|---|---|---|---|
| National Park Service — Yellowstone i Natural Sounds | NEW_PROVIDER | sfx, audio, video / OFFICIAL_STATIC_HTML_INDEX | REVIEW_REQUIRED_PER_ASSET |
| Blender Open Movies | NEW_PROVIDER | video, audio / OFFICIAL_STATIC_FILM_CATALOGUE | REVIEW_REQUIRED_PER_ASSET |
| Mixkit | NEW_PROVIDER | sfx, music, video / MANUAL_CATALOGUE | PROPRIETARY_REVIEW_REQUIRED |
| Sonniss #GameAudioGDC | NEW_PROVIDER | sfx, audio / OFFICIAL_STATIC_RELEASE_PACKS | PROPRIETARY_REVIEW_REQUIRED |
| Open Peeps | NEW_PROVIDER | graphics, illustrations, characters / MANUAL_LIBRARY | CONDITIONAL: autorska biblioteka CC0 ze strony projektu, z zachowaniem pochodzenia poszczególnych komponentów. |
| Quaternius | NEW_PROVIDER | 3d, rigs, animation, textures / MANUAL_PACKS | CONDITIONAL: część dawnych paczek deklaruje CC0; QAL ma ograniczenie redystrybucji. Ustalić dokładną paczkę i licencję; QAL poza automatyczną polityką. |

## REJECTED (4)

| Kandydat | Nowość | Media / dostęp | Prawa i ograniczenie |
|---|---|---|---|
| BBC Sound Effects / RemArc | NEW_PROVIDER | sfx, audio / MANUAL_CATALOGUE | BLOCKED_COMMERCIAL |
| Free To Use | NEW_PROVIDER | music / DOCUMENTED_PUBLIC_API | BLOCKED_COMMERCIAL_FREE_TIER |
| unDraw | NEW_PROVIDER | graphics, illustrations, svg / MANUAL_WEBSITE | MANUAL_ONLY: użycie ilustracji w konkretnym projekcie według własnych warunków autora; integracja i budowa zbioru wymagają odrębnej zgody. |
| ShareTextures | NEW_PROVIDER | pbr, textures, 3d / MANUAL_WEBSITE | MANUAL_ONLY: sprawdzić warunki strony i rekord, kwalifikacja automatyczna wyłączona. |

## Podwójne liczenie

OpenMoji static ma status DUPLICATE_MIRROR wobec odpowiedniej kolekcji Iconify; nie jest dodatkową nową biblioteką. Fontsource i Google Fonts to różne drogi dystrybucji tych samych rodzin: porównać rodzinę, wersję i wariant przed liczeniem przyrostu. Internet Archive może zawierać LibriVox/NASA, a Openverse indeksuje Commons i muzea; deduplikacja jest per asset, nie po nazwie serwisu. Statusy ALREADY_COVERED i BASELINE_UNKNOWN są dostępne, lecz żadna pozycja tego finalnego katalogu ich nie otrzymała.
