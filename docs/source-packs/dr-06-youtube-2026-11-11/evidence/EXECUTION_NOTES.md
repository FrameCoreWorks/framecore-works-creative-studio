# Notatki wykonania i ograniczenia kontroli

- Sprawdzono oryginalny PROMPT przez SHA256. Żaden skrypt zadania nie edytował nadrzędnego INDEX, konfiguracji, runtime lub repo produktu. Nie przeprowadzano globalnego audytu cudzych zmian w workspace.
- Po przerwaniu tury utracony stan functions.store spowodował utworzenie dziewięciu nowych własnych dokumentów w omyłkowym katalogu workspace/undefined. Wykryto to przy bezpośrednim odczycie REPORT.md. Wszystkie dziewięć przeniesiono do właściwego DR-06, bez nadpisywania istniejących plików; pusty omyłkowy katalog usunięto. To odstępstwo od zamierzonego zakresu zapisu zostało naprawione, ale historia zapisu nie była bezbłędna. Weryfikacja po naprawie potwierdziła obecność wszystkich dziewięciu plików i brak katalogu omyłkowego.
- Pierwszy draft walidatora wskazał niedokończony COVERAGE oraz link wewnątrz historycznej kopii. Finalny walidator wyłącza katalogi backupów; nie pomija linków w aktualnych dokumentach.
- CUA pokazał pojedyncze kadry i publiczne metadane; nie dostarczył odsłuchu ani pełnego seansu. Screenshoty są w historii narzędzi hosta, bez niezależnego archiwum obrazów w pakiecie. Recenzent jawnie zaakceptował tylko zakres kontroli dokumentów.
- Web proxy nie odczytał ponownie trzech adresów GitHub API. Bezpośredni publiczny odczyt API przez Python stdlib potwierdził wszystkie przypięte SHA i daty w BASELINE_RECHECK.json; nie uruchomiono kodu tych repozytoriów.
- Hipson przypisania rejestrują rzeczywistych agentów uruchomionych osobno. Po przerwaniu dwóch wznowiono przez followup_task; samo send_message nie uruchamiało zakończonej tury.
- Wszystkie benchmarki produkcyjne pozostają NOT_RUN. Sprawdzenie pakietu nie oznacza akceptacji architekta, działania adapterów lub gotowości do publikacji filmu.
