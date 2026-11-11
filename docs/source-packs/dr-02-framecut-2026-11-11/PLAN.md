# DR-02 — plan badania

Data: 2026-11-11. Specyfikacja: PROMPT.md (oryginał bez zmian) + SCOPE-CLARIFICATION.md.

Cel: profesjonalny warsztat montażysty i wiarygodne przełożenie na FrameCut. To artefakt badawczy, nie wdrożenie.

Metoda: Superpowers writing-plans, dispatching-parallel-agents, verification-before-completion; Studio workflow-orchestrator, research-evidence i deep-research-method; Hipson T-0004. Użytkownik polecił wykonać research bez zatrzymywania się na planie.

- [x] Trzy równoległe domeny w rozłącznych specialists/craft, specialists/nle, specialists/repo.
- [x] Root: czas racjonalny, semantyka transakcji, przykłady JSON, kompilacja, handoff.
- [x] Scalić rejestr źródeł i sprawdzić odwołania oraz adresy.
- [x] Macierz wymagań PROMPT → pliki → dowód → luka.
- [x] Niezależna recenzja całej syntezy przez świeżego agenta.
- [x] Własna weryfikacja struktur, obliczeń i przykładów; media/native NOT_RUN.
- [x] Hipson: zapisano wyniki autorów i ich ack; wynik recenzenta zapisuje lead. Świeży check i końcowy status są rejestrowane narzędziem Hipson po zapisaniu artefaktów.

Autorstwo: Codex koordynuje badanie, autorzy pomocniczy zachowują model sesji, bez nadpisania modelu. Model faktycznie raportowany przez CLI: brak wywołania CLI. Claude pozostaje głównym architektem; nie był wywołany i nie zatwierdził propozycji. Końcowa recenzja Codexa nie jest inspekcją Claude.

Ograniczenia: zapis wyłącznie w tym katalogu i własnym temp; nie modyfikować kodu, instalacji, zasad, Shared. Bez instalowania, uruchamiania pobranego kodu, płatnych usług, uploadów, publikacji. Datowane backupy przy edycji własnych istniejących plików.

## Wykonanie i weryfikacja

Trzy domeny dostarczyły komplet; świeży recenzent Codex zamknął jeden major i trzy minor po poprawkach. REVIEW_STATUS: PASS_WITH_LIMITATIONS. Własny verify_research.py zwrócił PASS dla zakresu struktury/odwołań/oryginalnych obliczeń. Native/NLE/media/full external JSON Schema tests NOT_RUN. Hipson T-0004 jest źródłem finalnego statusu zamknięcia.
