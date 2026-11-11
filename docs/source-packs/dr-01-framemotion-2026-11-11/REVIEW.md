# Recenzja i rozstrzygnięcia DR-01

Data: 2026-11-11. **Niezależny werdykt: PASS_WITH_LIMITATIONS.** Host odczytał finalną recenzję, przyjął jej granice dowodu i potwierdził cztery rozwiązane uwagi. Nie pozostała wskazana uwaga blocking/major.

## Co zmieniła recenzja

1. **DR01-R1:** jawna przestrzeń maski `composition-px`, brak widocznej warstwy maski, maskowanie po transformacji oraz extrapolation/visibility w przykładzie JSON.
2. **DR01-R2:** rozdzielenie kontroli `has_alpha` w istniejącym FrameCut od niepotwierdzonego straight/premultiplied i koloru. Uzupełniono audyt, macierz i backlog.
3. **DR01-R3:** benchmark parallax ma boczny truck, określoną kamerę i głębokości; nie wyciąga wniosku o prędkości z nieokreślonego dolly.
4. **DR01-R4:** nazwa testu długiej sekwencji nie sugeruje, że 108000 klatek przy 30000/1001 trwa dokładnie godzinę.

Szczegóły: [niezależny raport](review/INDEPENDENT-REVIEW.md), [findings](review/findings.json), [rozstrzygnięcia hosta](review-resolutions.json).

## Wykonane kontrole i przerwanie

Pierwszy recenzent wykonał ocenę treści, ponowne odczyty źródeł i checkery, lecz sesję przerwano przed zapisem werdyktu. Hipson A-0026 zachowuje wynik częściowy i przyjęcie tego faktu; nie wymuszono PASS. Recenzent wznowienia A-0028 samodzielnie sprawdził finalną treść, cztery źródła pierwotne i historyczne poprawki. Rozdzielił swój zakres od odzyskanych dowodów.

Świeże kontrole recenzenta: 30/30 hashy snapshotu, 56/56 niezależnego checkera oraz 41/41 checkera hosta w trybie draft. Wyniki częściowo się pokrywają i nie stanowią sumy niezależnych dowodów. Host następnie uruchamia pełny check bez draft; rzeczywisty wynik: [VERIFICATION.json](VERIFICATION.json). Zadeklarowana bramka Hipsona T-0005 to `python3 verify_research.py`, wykonywana ponownie przy zamknięciu na aktualnych plikach.

Oryginalny PROMPT.md zachował SHA256. Źródła: 124 rekordy / 121 URL / 117 jednostek po rozpoznanych aliasach, 26 domen. Kontrola transportu: 95/121 odpowiedzi HEAD <400, 26 odpowiedzi Adobe 403; nie są mylone z odrębnymi udokumentowanymi odczytami treści. Wszystkie lokalne odsyłacze, źródłowe ID i przykłady podlegają checkerowi. Datowane kopie poprawek zachowano.

## Granica akceptacji

Akceptacja dotyczy **badania i spójności specyfikacji**, nie działającej integracji ani filmu. Natywne rendery, odtwarzanie w czasie, odsłuch, font rendering i wydajność: **NOT_RUN**. Filmy źródłowe: **NOT_VIEWED**. Sidecar jest propozycją, a brak fontu/requestu celowo daje blocked preflight. Zainstalowany/aktywny runtime nowych wtyczek: Unknown.

Claude pozostaje architektem; nie uruchomiono jego CLI i nie przypisano mu akceptacji. Wdrożenie, instalacje i publikacja wymagają osobnego zlecenia. Nie zmieniono kodu repozytoriów ani konfiguracji.
