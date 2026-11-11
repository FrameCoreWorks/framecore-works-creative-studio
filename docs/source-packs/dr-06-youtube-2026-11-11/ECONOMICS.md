# Ekonomika — scenariusze do pomiaru

**DERIVED / NOT_RUN.** To własny model planowania małej produkcji. Nie są to dane kosztowe Milo, 3Blue1Brown ani pozostałych kanałów, cennik rynkowy lub oferta. Założona stawka rozliczeniowa **100 PLN za godzinę pracy człowieka** służy wyłącznie porównaniu; nie badano stawek wykonawców. Koszt istniejącego sprzętu, podatki, licencje, aktorzy i płatne usługi są poza sumą, chyba że zostaną jawnie dodane. Nie wyceniono przychodu, RPM ani monetyzacji.

## Model

Koszt pilota = przygotowanie biblioteki + roboczogodziny odcinka + czas maszyny × własna stawka + nabyte zasoby/licencje/usługi.
Koszt kolejnego odcinka = nowe sceny i assety + praca ujęciowa + redakcja/dźwięk/QA + render + poprawki.
Praca równoległa zmniejsza czas kalendarzowy tylko do granicy zależności; nie usuwa roboczogodzin.

| Założenie | A — 2D fabuła | B — explainer | C — stylizowane 3D |
|---|---:|---:|---:|
| Finalny metraż | 5 min | 6 min | 7 min |
| Ujęcia / kompozycje | 36 | 24 | 32 |
| Postaci / głosy | 2 / 2 | 0 / 1 narrator | 1 w kadrze / 2 głosy |
| Nowe duże zasoby po pilocie | 2 rekwizyty, 1 wariant tła | 3 diagramy/typy danych | 1 rekwizyt, 1 wariant planu |
| Udział ujęć korzystających z biblioteki | 70% | 60% | 75% |
| Przygotowanie biblioteki pilota, h człowieka | 60–120 | 24–48 | 100–200 |
| Scenariusz/research/read-through, h | 6–10 | 10–18 | 10–16 |
| Layout/animatic, h | 6–10 | 5–9 | 8–14 |
| Nowe assety i animacja, h | 12–22 | 8–14 | 24–44 |
| Sound/montaż/napisy, h | 6–10 | 5–9 | 8–14 |
| QA i jedna planowa runda poprawek, h | 6–12 | 6–10 | 10–18 |
| Łącznie następny odcinek, h | **36–64** | **34–60** | **60–106** |
| Łącznie pilot, h | **96–184** | **58–108** | **160–306** |
| Praca człowieka kolejny / pilot, PLN przy 100/h | 3600–6400 / 9600–18400 | 3400–6000 / 5800–10800 | 6000–10600 / 16000–30600 |
| Założone godziny maszyny na odcinek | 2–8 | 2–6 | 10–60 |

Udział re-use odnosi się do ujęć z biblioteką, nie do procentu gotowego czasu filmu ani gwarancji oszczędności. Godziny maszyny są hipotezą dla prostych scen; trzeba je zastąpić pomiarem na docelowym urządzeniu. Przy przykładowej wewnętrznej stawce maszyny 1 PLN/h koszt wyniósłby 2–8, 2–6 i 10–60 PLN — nie jest to cena prądu ani render farmy. Dla jednej osoby z 25 h tygodniowo przeznaczonymi na tę produkcję bazowy nakład pracy oznacza około 1,4–2,6 / 1,4–2,4 / 2,4–4,2 tygodnia kolejnego odcinka; czas oczekiwania na akceptację i awarie może wydłużyć kalendarz.

## Wrażliwość zamiast mechanicznego przeliczania klipów

- Nowy obrót bohatera, garderoba albo bliski kontakt wymaga dodatkowego widoku/pozy i testu biblioteki. Nie jest tylko dodatkową sekundą renderu.
- Późna zmiana głosu poza kadrem o zachowanej długości dotyka dźwięku, napisów i eksportu. Zmieniona długość widocznego dialogu może naruszyć visemy, gesty, reakcję partnera, cięcia i cue. Mierzyć obie ścieżki w B04.
- Jeżeli udział poprawianych ujęć wzrośnie z założonej jednej rundy do dwóch, liczyć dodatkowo czas konkretnej poprawki, przeglądu i renderu. Nie podwajać automatycznie całego odcinka.
- Płatny generatywny insert wyceniać osobno: n zleconych prób × stawka operacji + wybór/czyszczenie/conform/QC. Akceptowalny odsetek prób jest Unknown do pomiaru. Cena 15 s nie daje kosztu kompletnego odcinka.
- Biblioteka opłaca się dopiero przy faktycznym re-use. Załóżmy 80 h przygotowania i oszczędność 10 h na każdym następnym odcinku: zwrot nakładu godzinowego to 8 odcinków. Są to liczby przykładowe, a nie wynik badania.

Przed planem sezonu wykonać B01–B04, rejestrować czas aktywnej pracy, oczekiwania, renderu, odrzuconych prób, peak RAM/VRAM i GB cache. B05 ustali, czy jakość całej historii utrzymuje się przy zakładanym koszcie. Dopiero te pomiary pozwolą obiecać kadencję publikacji.
