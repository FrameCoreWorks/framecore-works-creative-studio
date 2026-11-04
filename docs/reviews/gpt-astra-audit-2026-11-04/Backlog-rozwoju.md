# Proponowany backlog rozwoju

S/M/L opisuje względny zakres: S to lokalna korekta i jej odbiór; M to zmiana kontraktu, kilku komponentów lub pakietu z testem integracyjnym; L to wieloetapowa walidacja, np. pilotaż z ludźmi. To ocena audytowa, bez obietnicy godzin lub terminów. Żadnej poprawki nie wdrożono w tym audycie.

Kolejność: A integralność i bezpieczeństwo; B dystrybucja i instalacja; C spójność instrukcji; D nauka; E nowe przykłady i adaptery; F utrzymanie. B-release-gate oznacza odbiór poprawek wybranych do wydania, porównanie pełnej paczki oraz kontrolę tożsamości i dodatków przed aktualizacją.

| ID | Priorytet | Etap | Rozmiar | Zależności | Spodziewany efekt |
|---|---|---|---|---|---|
| CW-AUD-002 / SEC-002 | P0 | A | M | Brak | Nie tracić poprzedniego poprawnego nagrania po błędzie. |
| CW-AUD-001 / SEC-001 | P1 | A | M | Brak | Zachować publiczną granicę HTTP niezależnie od proxy. |
| CW-AUD-009 / ORCH-01 | P1 | A | M | Brak | Wynik odpowiada właściwemu task, operacji, rewizji i wejściom. |
| CW-AUD-015 / ORCH-07 | P2 | A | M | ORCH-01 | Anulowanie kończy się jawnym statusem bez podwójnej operacji. |
| CW-AUD-036 / ROOT-04 | P2 | A | M | Brak | Usunąć podatny pin i sprawdzić zgodność obrazu/runtime. |
| CW-AUD-042 / UPSTREAM-03 | INFO | B | S | Brak | Zachować jawną normalizację YAML i oryginalne provenance. |
| CW-AUD-005 / DIST-001 | P1 | B | S | Brak | Wykrywać wadliwe YAML przed pakowaniem. |
| CW-AUD-006 / DIST-002 | P1 | B | M | DIST-001 | Udostępniać MCP zgodnie z kontraktem docelowego hosta. |
| CW-AUD-037 / INSTALL-01 | P1 | B | M | Brak | Przejść od znalezionego skilla do właściwej natywnej drogi Work. |
| CW-AUD-040 / UPSTREAM-01 | P1 | B | M | Brak | Przywrócić kompletny bootstrap Huashu i sprawdzić go w Work. |
| CW-AUD-008 / DIST-004 | P2 | B | S | INSTALL-01 | Jedna spójna instrukcja instalacji zewnętrznych modułów w Work. |
| CW-AUD-033 / ROOT-01 | P2 | B | M | B-release-gate | Ujednolicić źródło i zapis Studio z zachowaniem dodatków. |
| CW-AUD-038 / INSTALL-02 | P2 | B | S | Brak | Zwracać kontrolowany błąd na niewłaściwy kształt JSON. |
| CW-AUD-039 / INSTALL-03 | P2 | B | M | INSTALL-01 | Ta sama rewizja źródła, licencji, zasobów i zapisanych bajtów. |
| CW-AUD-041 / UPSTREAM-02 | P2 | B | S | Brak | Przywrócić siódmy styl galerii Animate. |
| CW-AUD-007 / DIST-003 | P3 | B | S | Brak | Zgodność metadanych listingu z wymaganiem platformy. |
| CW-AUD-010 / ORCH-02 | P2 | C | S | Brak | Użytkownik zachowuje wybór dla wszystkich companions. |
| CW-AUD-011 / ORCH-03 | P2 | C | S | ORCH-01 | Dozwolony prywatny handoff przenosi potrzebny kontekst. |
| CW-AUD-012 / ORCH-04 | P2 | C | S | Brak | Ważna zgoda zachowuje zakres między turami. |
| CW-AUD-025 / CR-001 | P2 | C | S | Brak | Odróżniać reklamową deklarację od potwierdzonego faktu. |
| CW-AUD-026 / CR-002 | P2 | C | M | Brak | Chronić poprawne cytaty i terminologię przed linterem. |
| CW-AUD-027 / CR-003 | P2 | C | S | Brak | Oddzielić ofertę, autoryzację, zobowiązanie i rzeczywisty koszt. |
| CW-AUD-028 / CR-004 | P2 | C | S | Brak | Zachować zamierzony kontrapunkt obrazu i dźwięku. |
| CW-AUD-029 / CR-005 | P2 | C | S | Brak | Zachować zakres, wyjątki i Unknown w skrócie UGC. |
| CW-AUD-030 / CR-006 | P2 | C | S | Brak | Przykład FrameCut działa na aktualnej rewizji. |
| CW-AUD-031 / ASSET-001 | P2 | C | S | Brak | Nie mylić dostępności portu z poprawnym HTTP. |
| CW-AUD-032 / ASSET-002 | P2 | C | M | Brak | Zgodność dossier z faktycznie sprawdzonymi typami zasobów. |
| CW-AUD-016 / ORCH-08 | P3 | C | S | Brak | Dokumentowane komendy odpowiadają interfejsowi CLI. |
| CW-AUD-017 / ORCH-09 | P3 | C | S | Brak | Prawidłowy podział tworzenia dokumentu i walidacji manifestu. |
| CW-AUD-018 / LEARN-01 | P2 | D | S | Brak | Rubryka ocenia aktualny kontrakt uruchomienia nauki. |
| CW-AUD-019 / LEARN-02 | P2 | D | M | LEARN-01 | Nie zaliczać bezpodstawnego mastery i złamanych ograniczeń. |
| CW-AUD-021 / LEARN-04 | P2 | D | L | LEARN-01,LEARN-02,LEARN-05 | Zmierzyć samodzielny transfer i trwałość umiejętności u ludzi. |
| CW-AUD-022 / LEARN-05 | P2 | D | M | Brak | Wznawiać naukę z językiem, dostępnością i ograniczeniami. |
| CW-AUD-023 / LEARN-06 | P2 | D | L | LEARN-01,LEARN-02 | Sprawdzić materiały i ocenianie w rzeczywistych zajęciach. |
| CW-AUD-020 / LEARN-03 | P3 | D | S | Brak | Usunąć martwe wskazówki i mylące liczniki. |
| CW-AUD-024 / LEARN-07 | P3 | D | M | LEARN-02,LEARN-05 | Kalibrować istniejący mentoring zamiast dublować moduły. |
| DEV-ASSETS / PROPOSAL | P3 | E | M | Prawa i E0–E4 danej metody | Poszerzyć dostępne rodzaje darmowych materiałów po niezależnej walidacji adapterów. |
| DEV-CREATIVE / PROPOSAL | P3 | E | M | CR-001,CR-002,CR-003,CR-004,CR-005,CR-006 | Mierzyć zgodność briefu i odrębność mechanizmu pomysłu. |
| CW-AUD-003 / SEC-003 | P2 | F | M | Brak | Odtwarzać instalację i wersję modelu głosu. |
| CW-AUD-035 / ROOT-03 | P2 | F | S | Brak | Chronić main bez zmiany ustalonego modelu main-only. |
| CW-AUD-004 / SEC-004 | P3 | F | S | Brak | Ograniczyć zmienność dostarczanych akcji CI. |
| CW-AUD-013 / ORCH-05 | P3 | F | S | Brak | Alias kompatybilności ma prawdziwe uzasadnienie. |
| CW-AUD-014 / ORCH-06 | P3 | F | S | Brak | Odzyskać zapas rozmiaru bez pogorszenia routingu. |
| CW-AUD-034 / ROOT-02 | P3 | F | S | Brak | Skrócić drogę początkującego do właściwej instalacji. |
| DEV-REGRESSION / PROPOSAL | P3 | F | M | Końcowy raport symulacji | Wykrywać regresje zachowania po zmianach. |

## Osobne propozycje rozbudowy

| Zakres | Etap / rozmiar | Zależność | Odbiór |
|---|---|---|---|
| Cztery adaptery kandydatów Open Assets, każdy osobno | E / M na adapter | Prawa i E0–E4 danej metody | Anonimowy search, schema, prawa konkretnego obiektu, timeout, retry, mała próbka i manifest; obecnie zero nowych adapterów. |
| Pięć stałych briefów porównawczych | E / M | Korekty CR-001–006 | Ta sama rubryka przed i po zmianie; zgodność briefu i odrębny mechanizm kierunków; ocena wygenerowanych mediów osobno. |
| Aktualizacja regresyjnego zestawu 110 profili | F / M | Końcowe wyniki obecnego badania | Powtórzyć przypadki krytyczne i graniczne po poprawkach, zachować transkrypty i niezależną ocenę; nie zamieniać checklisty w deklarację niezawodności. |

Kryterium odbioru każdego wpisu znajduje się w Backlog-rozwoju.json/CSV oraz pełnym rejestrze ustaleń. Priorytet nie jest CVSS. Wpis INFO opisuje stan już naprawiony w zapisanej paczce, nie otwartą awarię.
