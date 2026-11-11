# Przebieg DR-04 i obserwacje modeli

Data: 2026-11-11, strefa użytkownika Europe/Warsaw. Zlecenie: niezależne DR-04, bez scalania z czterema innymi badaniami. Hipson **T-0007**, project równy dokładnie katalogowi DR-04, lead `codex`, approved=true na podstawie zlecenia. Oryginalny prompt SHA-256: `a6f93b1f72b909d0ead07a1ca5f06f83645361942dec830971348ca282451fe1`.

## Role i modele

| Rola | Model requested | Client settings | Model observed |
|---|---|---|---|
| Lead, plan i synteza | model bieżącej sesji zachowany | bez zmiany | dokładna nazwa wariantu niedostępna w odpowiedzi narzędzia; nie zgadujemy |
| baseline (A-0023) | gpt-6.1-sol | fork none, reasoning_effort high | collaboration zaakceptowało przydział i zwróciło nazwę zadania; brak osobnej telemetrii backend model |
| audio_video (A-0024) | gpt-6.1-sol | fork none, high | jw.; zapisano 3 JSON, przerwano przed CARDS |
| visual_data (A-0025) | gpt-6.1-sol | fork none, high | jw.; pełny pakiet + poprawka etykiet dowodów |
| audio_completion | gpt-6.1-sol | fork none, high; odzyskanie tego samego scope | jw.; bez fallbacku na inny model, dokończenie po przerwaniu sesji |
| fresh_review (A-0032) | gpt-6-astra | fork none, high | odczytać stan/zakres w review/REVIEW.md; samo accepted dispatch nie jest pomiarem backend model |

Pierwszy rzeczywisty swarm uruchomiono przez collaboration równolegle w trzech rozłącznych podkatalogach. Hipson assign jedynie zarejestrował przydziały. Po celowym przerwaniu turnu sesje agentów nie były już aktywne; pliki pozostały. Lead użył `lead.resume`, odczytał stan i powołał audio_completion wyłącznie do brakującego tekstu i znaczników. Użytkownik nie miał obsługiwać tych sesji.

## Zapis postępów i korekt

1. Odczytano pełny PROMPT.md, sekcje wszyscy/codex ZASADY-MODELI, lokalne AGENTS i Superpowers 7.0.2: using-superpowers, writing-plans, dispatching-parallel-agents, verification-before-completion. Plan zapisano w PLAN.md, dostosowany do researchu.
2. Hipson task.open o 07:38 UTC, następnie in_progress. Początkowy assign z absolutnym scope został odrzucony walidacją; poprawiono na rozłączne ścieżki względne. Nie użyto force ani zmiany uprawnień.
3. Baseline dostarczył przypięty kod i 76 wpisów źródeł. Lead przeczytał contract/core/runtime i raport, potwierdził exact field names i limity. A-0023 finish+ack.
4. W visual_data wykryto zbyt mocne OWN_TEST przy odczycie metadanych; specjalista wykonał dated backups i poprawił na DOCUMENTED/CODE_INSPECTED z record_read. Dodano review_depth i read_status. Lead sprawdził referencje JSON i przyjął A-0025.
5. Root odczytał oryginalne CC BY/SA, CC0/PDM, OFL oraz GitHub rate/cache docs; niezależnie sprawdził dokumentację Iconify/Fontsource i NASA API. Rootowy IA bots read nie udał się; zapisano ograniczenie, bez obejścia.
6. Po przerwaniu około etapu syntezy odzyskano stan przez lead.resume. Audio completion uzupełnił CARDS i jawne źródła BLOCKED/INDEXED_EXCERPT. Nie powtórzono download/testów produktu.
7. assemble_artifacts.py najpierw wykrył różnicę pola rank/ranking między specjalistami (KeyError, bez finalnych plików); po dated backup poprawiono normalizację. To błąd składania dokumentów, nie produktu.
8. Zapisano raport, rankingi/coverage, backlog, projekty adapterów, plan 20 prób NOT_RUN, source register, real records, manifest design i handoff. Końcowy checker i świeża recenzja mają osobne artefakty; ich zakres nie obejmuje działania providerów.

## Obserwacje do ewentualnych lekcji

- Dowód: poprawka visual_data oddziela odczyt rekordu od testu wykonawczego. W następnych packetach warto narzucić tę semantykę już w schemacie katalogu. To lokalna obserwacja, nie zmiana stałej zasady.
- Dowód: baseline znalazł 5 technical-only spośród historycznych ścieżek Work. Count provider×category nie może zastąpić produkcyjnego rights/readiness proof.
- Dowód: przerwanie nie utraciło JSON, lecz brakował CARDS. Wczesny zapis danych umożliwił dokończenie zakresu bez ponownego badania i bez zmiany modelu.
- Ustawienia requested/accepted nie dają niezależnego backend model telemetry. Obserwacja jakości dotyczy artefaktów, nie benchmarku porównawczego modeli.

Claude CLI nie uruchomiono zgodnie z wyjątkiem po wcześniejszym OAuth401. Nie logowano, nie robiono fallbacku, nie wysłano wiadomości do innych czatów. Shared, jego LESSONS/MODEL-ROUTING i główny INDEX.json są tylko do odczytu w tym zleceniu, więc obserwacje i handoff pozostają w DR-04.

Końcowa korekta ewidencji: pierwsza lokalna komenda poprawy minor uwag zakończyła się NameError przed zapisem; druga komenda wykonała zmiany. Hipson event142 jawnie koryguje zbyt wczesną deklarację z event138. Nie pominięto błędu ani nie użyto force.

Finalny odbiór recenzji A-0032: PASS_WITH_LIMITATIONS, 0 open blocking/major, 3 minor fixed. Lead powtórzył pełny verify_artifacts.py z exit0 (26/10/22/204, oryginalny prompt niezmieniony). Wszystkie 4 przydziały finish+ack. Końcowy Hipson close uruchomi zadeklarowany check ponownie; jego status jest źródłem prawdy o zamknięciu ledger.
