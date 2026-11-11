# Kontrola podzadania recipes — 2026-11-11

## Wynik

- `RECIPES.md`: 18 kolejnych receptur R01–R18; automatyczna kontrola wykryła w każdej cel, use/not-use, assety, budowę, parametry startowe, operacje, błąd/naprawę, kod, QA i źródła. Około 5778 słów.
- `PROCESS-AND-TUTORIALS.md`: etapy, locks i rewizje, rozdzielenie cue audio, mapa nauki oraz granice inspekcji. Około 2915 słów.
- `sources.json`: poprawny JSON, 20 unikalnych ID oraz głównych URL, wszystkie żądane pola obecne; wszystkie odwołania R-Sxx z obu dokumentów mają rekord. Wszystkie rekordy oznaczają test wykonawczy NOT_RUN.
- Wykonano przegląd treści: wartości liczbowe mają kontekst i status propozycji; proces nie twierdzi, że wtyczki już mają opisane funkcje; filmy i kursy nie zostały przedstawione jako obejrzane.

Kontrola struktury i JSON: **PASS**. Oglądanie renderów, testy aplikacji, fontów, cue audio i backendów: **NOT_RUN**. Dokument nie jest dowodem jakości animacji ani implementacji.

## Ważne ograniczenia

- Odczytano wybrane części PDF Blackmagic, nie całą książkę. Plików ćwiczeń ani filmów nie pobierano.
- Dokumentacja Blender HTML była niedostępna; odczytano oficjalne raw RST. Gałąź main bez commit pin.
- Sprzeczność w ogólnym akapicie Adobe Track Mattes jest zapisana; przyjęto jawne definicje tabeli trybów oraz zaproponowano test 0/50/100%.
- C4D R21 jest uzupełnieniem historycznym rekordu R-S13; nie przedstawiono dawnego ostrzeżenia jako obecnego błędu 2026.
- Większość instrukcji pierwotnych znaleziono po angielsku; wyszukiwanie PL wykonano, lecz nie udawano odczytu polskich filmów lub kursów.
- `git status` nie był dostępny w katalogu bieżącym: nie jest on repozytorium Git. To nie zostało uznane za błąd dokumentów ani za powód modyfikacji repozytorium. Wykonano sprawdzenie plików bez Git.

## Zakres zapisu

Wyłącznie katalog `01-framemotion-after-effects/specialists/recipes`. Nowe dokumenty, bez zmian projektowego kodu, konfiguracji i infrastruktury. Przed poprawką istniejącego dokumentu utworzono kopie w:

- `backups/2026-11-11-083712/RECIPES.md`
- `backups/2026-11-11-084350/sources.json`

Nie instalowano narzędzi, nie uruchamiano pobranego kodu, nie wykonywano prywatnych uploadów, płatności, publikacji, pushu ani deployu. Bez kontaktowania innych sesji CLI; koordynacja w obrębie przydzielonych agentów badawczych.
