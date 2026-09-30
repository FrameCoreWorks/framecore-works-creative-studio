# Tryb kreatywny i Tryb nauki

Od wersji 1.2.0 Studio rozpoznaje dwa równorzędne cele pracy:

- **Tryb nauki**: krótki onboarding, osobisty program, lekcja, samodzielne ćwiczenie i omówienie próby.
- **Tryb kreatywny**: dotychczasowy workflow prowadzący do zamówionego materiału; „Tryb tworzenia” pozostaje obsługiwanym aliasem.

Przy każdym wysłaniu samego wywołania wtyczki (wybranie i Enter), powitaniu lub prośbie o menu Studio kopiuje w całości [jeden stały tekst powitania](../skills/workflow-orchestrator/assets/startup-welcome.pl.md). Zaczyna od „Jestem FrameCore Works Creative Studio.”, opisuje możliwości, zaprasza do dodania materiałów, a na dole pokazuje **1. Tryb kreatywny / 2. Tryb nauki**. Nie dodaje „Cześć” i nie parafrazuje tekstu. Ponowne wywołanie powtarza ten sam tekst również w istniejącej rozmowie, zachowując stan wcześniejszych projektów i nauki; konkretna prośba o wznowienie kontynuuje zapisaną pracę. Po samym wyborze kreatywnym pokazuje **1. Tryb szybki / 2. Tryb rozbudowany**, następnie siedem obszarów pracy i dopiero potrzebne pytanie o zadanie. Te kroki obowiązują niezależnie od modelu i nakładu rozumowania hosta. Numer dotyczy tylko nadal oczekującego wyboru; rozwiązane menu wygasa. Dwie grupy wyboru w jednej wiadomości używają cyfr i liter, np. `7, A`. Pierwsza lekcja offline krótko ujawnia ograniczenie researchu. [Kontrakt wejścia](../skills/workflow-orchestrator/references/startup-and-creative-menus.md) obejmuje również wznowienie starszej rozmowy i pomijanie już podanych decyzji.

Jeśli od razu opiszesz projekt albo poprosisz o naukę, Studio przejdzie do właściwej ścieżki bez zbędnych wyborów. Przyciski zależą od faktycznych możliwości hosta; zawsze może działać wybór tekstowy. Quick/Deep nadal określa tempo i głębokość pracy, niezależnie od celu.

## Początek nauki

Studio wykorzystuje informacje, które już podałeś. Dopytuje maksymalnie w sześciu krótkich pytaniach o cel samodzielny, doświadczenie, projekt, narzędzia, czas/budżet oraz preferowaną formę nauki. Możesz odpowiadać krótko, pomijać nieistotne kwestie lub napisać „nie wiem”. Brak programu, sprzętu czy płatnego konta nie blokuje ćwiczeń na papierze lub w tekście.

Przykład: „Chcę samodzielnie projektować plakaty. Poziom zero, 30 minut trzy razy w tygodniu, bez kosztów. Wolę przykłady i ćwiczenia”. Takie kompletne wejście pozwala od razu ułożyć plan i zacząć lekcję.

## Program i lekcje

Plan opisuje cel, kolejność modułów, umiejętności, ćwiczenia, kryteria postępu, narzędzia i ich koszty lub niewiadome, warianty bez renderu oraz orientacyjny nakład pracy. Przy szerokim celu łączy wspólne podstawy, wybrane specjalizacje i projekt przekrojowy. Studio rozpoczyna pierwszą krótką lekcję po planie, chyba że prosisz wyłącznie o plan.

Każda lekcja ma cel, proste wyjaśnienie, definicje potrzebnych terminów, przykład, ćwiczenie i kryteria. Po Twojej próbie otrzymasz omówienie jednej lub dwóch najważniejszych poprawek oraz sprawdzenie zrozumienia. Możesz poprosić o prostsze wyjaśnienie, trudniejszą wersję, kolejny przykład, quiz lub pominięcie tematu. Wyświetlenie lekcji nie oznacza jej ukończenia.

## Zakres

[Mapa kompetencji](../skills/workflow-orchestrator/assets/learning-domains.json) prowadzi do istniejących skilli dla 14 obszarów: grafiki i ilustracji, typografii, opowieści/scenariusza, intencji i wykonania postaci, referencji/tożsamości, storyboardu/sekwencji, kamery/światła, reklamy/wideo, teledysku, tekstu/głosu marki, promptów, audio/muzyki, montażu/animacji oraz kampanii/workflow.

Wsparcie webinaru obejmuje strukturę i materiały, aktorstwa intencję oraz blocking, głosu tempo/pauzy/akcenty, a VFX plan efektu. Studio nie oferuje pełnego kursu techniki transmisji, zaawansowanych symulacji, klinicznego treningu głosu ani zawodowej certyfikacji. Granice są zapisane przy każdej dziedzinie.

## Przełączanie i postęp

„Teraz zrób gotowy rezultat” przełącza do tworzenia bez kolejnych lekcji. „Naucz mnie tego na moim projekcie” uruchamia naukę z zachowaniem kontekstu projektu. Zatwierdzone wersje, teksty i koncept nie zmieniają się od samego przełączenia trybu.

Postęp obejmuje ścieżkę, poziom w danej dziedzinie, bieżący moduł, ukończone/pominięte lekcje, udokumentowane mocne strony, potrzeby ćwiczeń i następny krok. Gdy trwały zapis nie jest dostępny, otrzymasz krótką [Kartę postępu](../skills/workflow-orchestrator/assets/learning-progress.template.md) do skopiowania na przerwę lub do nowej rozmowy. Nie ma gwarancji pamięci ani przeniesienia załączników między hostami.

## Narzędzia i dowody

Wyjaśnienie lub ćwiczenie nie uruchamia generowania, płatnego providera, API/MCP ani uploadu. Dla ćwiczenia z renderem najpierw dostępny jest wariant bez renderowania. Faktyczne wykonanie wymaga osobnego polecenia i spełnienia aktywnych zasad hosta. Subskrypcja ChatGPT nie gwarantuje bezpłatności zewnętrznych usług. Aktualne funkcje i ceny sprawdza się dla konkretnego narzędzia; niewiadome pozostają jawne.

Metoda używa istniejących kompetencji i [materiałów metodycznych z podanymi źródłami](../skills/workflow-orchestrator/references/learning-mode.md#method-evidence). `evals/learning-mode-cases.json` zawiera 16 planowanych scenariuszy. Testy repo sprawdzają strukturę i ochronę kontraktów; nie dowodzą, że host przeprowadził te lekcje ani że nauka była skuteczna.
