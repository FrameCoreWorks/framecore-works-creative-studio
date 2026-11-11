# Weryfikacja DR-02 — zakres dowodów

Data: 2026-11-11. NATIVE_TESTS: NOT_RUN. Wszystkie rendery, native NLE round-trips, pomiary mediów, ogląd i odsłuch: **NOT_RUN**.

## Własne sprawdzenia

- Oryginalny `PROMPT.md` zachował SHA-256 `8b00ad1f655ffefbf27a626d3f00d762042b06fe546c5d60c79400a25a1f2a7d`, zgodny z początkowym snapshotem Hipsona.
- Parser AST odczytał trzy własne skrypty badawcze (`build_examples.py`, `assemble_sources.py`, `verify_research.py`). W pierwszej próbie generator przykładów miał brakujący nawias; po ustaleniu przyczyny poprawiono go i wykonano poprawną generację. Historia zachowana w backups.
- Ponowny odczyt 14 wybranych plików installed cache dał 14 zgodnych hashy wobec przypiętych dowodów publicznego main. Nie jest to pełna kwalifikacja pakietu ani test aktywnej sesji.
- `verify_research.py` jest własnym ograniczonym weryfikatorem raportu: wymagane pliki, identyfikatory i użycie źródeł, lokalne odnośniki, liczba haseł/receptur, kształt 14 rodzin intencji, native envelopes, negatywne przypadki pól, dokładny rachunek czasu i rozmiary artefaktów. Nie importuje pobranego kodu i nie uruchamia FrameCut/NLE.
- Funkcja sprawdzająca RFC obsługuje wyłącznie ograniczony podzbiór konstrukcji użytych w tym schemacie. Nie jest implementacją pełnego JSON Schema. Pełna walidacja standardowym zewnętrznym validatoriem: **NOT_RUN**; nie instalowano zależności.
- Wynik końcowego polecenia i liczby zapisano w `VERIFICATION-RESULT.json`. Hipson uruchamia tę samą kontrolę ponownie przed zamknięciem.

## Źródła i adresy

`SOURCE-LEDGER.json` i CSV scalają rejestry czterech domen. Każdy rekord ma źródło, metodę odczytu, zakres wspieranych twierdzeń, decyzję, kontrprzykład, plan testu i ograniczenia. Wielokrotne wykorzystanie tego samego dokumentu nie jest niezależnym potwierdzeniem. Identyfikatory rekordów i liczby URL nie są rankingiem jakości.

`LINK-CHECK.json` sprawdza dostępność adresu metodą bounded GET (nagłówki i pierwsze 256 bajtów), bez pobierania całych PDF. HTTP error albo timeout podczas ponownego sprawdzania nie dowodzi, że wcześniejszy udokumentowany odczyt był niemożliwy. Status takiego adresu pozostaje jawny; nie zamieniono go w HTTP_OK. Dokument lokalny SDK ma osobny zakres i nie jest adresem publicznego źródła web.

## Recenzja i poprawki

Świeży recenzent Codex sprawdził pełny prompt, raporty, schemat/przykłady i wykonał niezależne kontrole źródeł. Nie jest to review Claude; Claude nie został wywołany i nie zatwierdził architektury.

Major R1: błędne twierdzenie, że native ripple nie aktualizuje automatycznie `sequence.duration`. Odczyt `fc_edit.shift` wykazał `seq['duration'] += delta`; poprawiono tabelę oraz generator i JSON. Dalsze doprecyzowania: scope/dependents dla operacji RFC, CFR-only slip, spójne +90 frames w B5. Hipson finding `F-0001` zachowuje historię zgłoszenia i naprawy. Pełny werdykt: `REVIEW.md` oraz `specialists/review/REVIEW.md`.

## Co pozostaje nieweryfikowane

Testy autora są przeczytanymi specyfikacjami, nie własnym PASS. Pięć benchmarków to kompletne plany prób, nie pomiary wydajności ani jakości. Nie potwierdzono native import/export żadnego NLE, lokalnych wersji uruchomionych aplikacji, profesjonalnego HDR, pitch-preserving ramp, multicam i przyszłych osobnych pluginów. Hash/valid JSON/frame count nie dowodzą sensu, tonu, ruchu, rytmu ani słyszalnej jakości.
