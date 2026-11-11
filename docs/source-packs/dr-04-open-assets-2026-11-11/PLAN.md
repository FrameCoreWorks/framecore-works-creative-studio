# DR-04 Open Assets — Research Plan

Data: 2026-11-11 (Europe/Warsaw). Hipson: **T-0007**, lead `codex`.

## Goal

Zbadać trwałe rozszerzenia legalnego pozyskiwania mediów. Specyfikacja: [PROMPT.md](PROMPT.md), niezmieniana. Wynik to pakiet badań i propozycja dla Claude, głównego architekta, bez implementacji.

## Metoda i granice

Superpowers 7.0.2: using-superpowers, writing-plans (adaptacja do researchu), dispatching-parallel-agents, verification-before-completion. Badanie jest już autoryzowane; nie ma bramki ponownej akceptacji planu ani zatwierdzania wdrożenia. Repozytoria czytane przez GitHub connector, dokumentacja i prawa przez web. Nie uruchamiamy pobranego kodu, nie instalujemy, nie pobieramy binariów, nie wysyłamy prywatnych materiałów. Testy produktu NOT_RUN. Własny walidator bada tylko strukturę artefaktów.

Jedyny zapis w tym katalogu; każdy agent ma wyłączny własny podkatalog. Przed edycją istniejących własnych plików dated backup. Shared, inne badania, repo i INDEX.json tylko do odczytu. Claude CLI pominięte zgodnie z upoważnieniem (wcześniejszy OAuth401), bez próby logowania/fallbacku. Brak zapisu LESSONS/MODEL-ROUTING w Shared; obserwacje tylko w tym pakiecie.

## Role i artefakty

| Rola | Wykonawca żądany | Zapis | Wynik |
|---|---|---|---|
| Plan, źródła przekrojowe, synteza | bieżąca sesja Codex, bez zmiany modelu | katalog główny/evidence | REPORT, katalog CSV/JSON, ADAPTER_DESIGNS, TEST_PLAN, BACKLOG, IMPLEMENTATION_HANDOFF |
| Baseline | GPT-6.1 Sol / high | baseline/ | kod/kontrakt/prawa/limity i commit pin |
| Audio/wideo | GPT-6.1 Sol / high | audio_video/ | katalog, źródła, pełne karty, realne rekordy |
| Visual/data | GPT-6.1 Sol / high | visual_data/ | katalog, źródła, pełne karty, realne rekordy |
| Świeża recenzja | GPT-6 Astra / high | review/ | kontrola dowodów i kompletności, bez akceptacji architektury |

Agenci uruchomieni rzeczywiście przez collaboration, nie przez Hipson assign. Sesje pomocnicze nie wymagają obsługi użytkownika, wyniki wracają do tego wątku; pozostają zapisem i po zakończeniu są nieaktywne. Model requested i narzędziowo observed rozróżniamy w RUN_LOG.

## Kroki i kryteria

- [x] Przeczytać pełny prompt, zasady modeli, właściwe skills i lokalne AGENTS.
- [x] Utworzyć własny task Hipsona z acceptance/checks oraz rzeczywisty swarm.
- [x] Baseline: pin Open Assets/Studio/Toolbox; przeczytać provider index/manifests/schema/runtime/adapters/tests; odróżnić repo, instalację i wykonanie.
- [x] Katalog: 20–30 sensownych źródeł/rozszerzeń jako cel, bez dopisywania słabych; status nowości, ranking, trzy osie, pełne źródła. 8–10 deep jeśli materiał to uzasadnia.
- [x] Dla najlepszych odczytać 2–3 rekordy, gdy dostępne, bez pobierania binariów. Utrzymać jawne luki i Unknown.
- [x] Synteza: pokrycie luk, projekty adapterów zgodne z istniejącym kontraktem/polityką praw, małe próby NOT_RUN, backlog z wejściami/wyjściami/właścicielem/zależnościami/limitami/błędami/kosztem/testem.
- [x] Świeża recenzja i korekty w granicach materiału; uzgodnić aktualność i nie mieszać host readiness z dokumentacją.
- [x] Sprawdzić integralność, zgodność CSV/JSON, źródła i niezmienność promptu; acknowledge wszystkich zakończonych przydziałów. Przygotować końcowy Hipson close z pełnym zadeklarowanym checkiem bez force; rezultat końcowego gate zapisuje centralny rejestr T-0007.

## Review focus

1. Usługa bez konta ≠ prawa do wszystkich plików; wymagane eligibility per asset.
2. Statyczny katalog ≠ kompatybilny adapter API; nowy format ≠ obsługa dekodera.
3. Metadane/licencja API ≠ licencja obrazu/dźwięku; SA/NC/ND/custom jawne.
4. Blokada endpointu ≠ zgoda na alternatywne proxy/retry; zachować aktualny blockade stop.
5. Kontrola dokumentów ≠ download/decode/odsłuch/wygląd ani potwierdzenie architektury.

Weryfikacja końcowa: `python3 verify_artifacts.py`, wykonana też przez Hipson. Akceptacja dokumentacyjna nie oznacza testu produktu.
