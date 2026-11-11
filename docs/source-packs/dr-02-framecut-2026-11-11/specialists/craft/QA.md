# Sprawdzenie pakietu warsztatowego

Data: 2026-11-11. Jedna ograniczona pętla review: sprawdzenie kompletności, źródeł i oznaczenia własnej syntezy; poprawka precyzji mapy retimingu R15 na uwagę hosta.

## Wynik

- PASS: 100 unikalnych identyfikatorów G001–G100.
- PASS: 18 receptur R01–R18, każda ma dokładnie 11 wymaganych pól.
- PASS: 13 źródeł C01–C13, wszystkie wykorzystane, wszystkie wymagane pola JSON obecne.
- PASS: brak niezdefiniowanych identyfikatorów [Cnn].
- PASS: receptury i przykłady jawnie DERIVED; testy mediów NOT_RUN.
- PASS: mapa poradnik → umiejętność → ćwiczenie → ograniczenie.
- NOT_RUN: uruchomienie NLE, kompilacja FrameCut, benchmark, ogląd i odsłuch mediów.
- PARTIAL: weryfikacja aktualnych możliwości produktów jest ograniczona do podanych wersji i tekstów; nie dowodzi lokalnej instalacji.

To strukturalny i redakcyjny QA dokumentów, nie certyfikat działania opisanych pipeline’ów. Stop: stop_sufficient dla przydzielonego modułu badawczego.

## Manifest aktualnej rewizji

```json
{
  "glossary_count": 100,
  "glossary_unique": 100,
  "recipes_count": 18,
  "recipe_fields": [
    11,
    11,
    11,
    11,
    11,
    11,
    11,
    11,
    11,
    11,
    11,
    11,
    11,
    11,
    11,
    11,
    11,
    11
  ],
  "sources_count": 13,
  "practitioner": 7,
  "documentation": 6,
  "missing_refs": [],
  "unused_source_ids": [],
  "GLOSSARY.md": {
    "sha256": "ab54fce8a0cd21919b2f3143c4dbf213ee2e2e5dcc32bdca90c8c094200a79b6",
    "bytes": 28869,
    "words": 4329
  },
  "RECIPES.md": {
    "sha256": "9678f3a3b43908d068417dc1ea26ecb34f78694f3354215469467f32c0343e26",
    "bytes": 44776,
    "words": 5652
  },
  "CRAFT.md": {
    "sha256": "850f0da0701b7c6518c31f8d7747072ffbf44fe6740725fb53868039ee44afac",
    "bytes": 15201,
    "words": 2040
  },
  "sources.json": {
    "sha256": "a53b4c3f355063934939c630ee52c4738a95b6ff31852fbf177ee6e3b5b52f8a",
    "bytes": 16070,
    "words": 1629
  }
}
```

## Granice

Czytano teksty źródeł, nie oglądano przywołanych filmów. Podręcznik BMD przeczytano w wskazanych sekcjach. Apple 429 i Polska Światłoczuła timeout nie zostały wykorzystane jako dowód treści. DAWG dostępny tylko jako landing page pozostaje poza rejestrem wykorzystanych źródeł. Dokładne zasady delivery, NLE oraz stan repozytorium należą do pozostałych części raportu hosta.
