# FrameCore Works Creative Studio

Wersja: 1.3.0.

Pierwsze stabilne wydanie udokumentowanego zakresu Studio. [Zakres 1.0](docs/release-1.0.md) opisuje zawartość i granice wydania. Kod, instrukcje i dokumentacja FrameCore Works są objęte [Apache-2.0](LICENSE); zachowano licencje i oznaczenia źródeł.

Creative Studio prowadzi pracę od briefu i materiałów wejściowych do kierunku, storyboardu, promptów i planu montażu dla obrazu, wideo, dźwięku i tekstu. Odpowiedzi dopasowuje do trybu szybkiego lub pogłębionego; przy nowej decyzji kreatywnej obowiązuje celowany publiczny research. Generowanie, analiza mediów i integracje zależą od faktycznie dostępnych, wybranych przez użytkownika narzędzi.

## Powitanie, Tryb kreatywny i Tryb nauki

Pełne powitanie wyjaśnia, czym jest Studio i co potrafi, a następnie pokazuje **1. Tryb kreatywny / 2. Tryb nauki**. Po samym wyborze kreatywnym otrzymasz **1. Tryb szybki / 2. Tryb rozbudowany**, a potem wcześniejsze menu obszarów i doprecyzowanie zadania. **Tryb tworzenia** pozostaje aliasem trybu kreatywnego. Jasna prośba omija zbędne wybory; numer odnosi się do ostatnio pokazanego menu. [Powitanie i dalsze kroki](skills/workflow-orchestrator/references/startup-and-creative-menus.md).

**Tryb nauki** zachowuje krótki onboarding, spersonalizowany plan, ćwiczenia i omówienie Twojej pracy w 14 obszarach istniejących skilli. Quick/Deep określa tempo niezależnie od celu. Przy braku trwałego zapisu możesz przenieść Kartę postępu do kolejnej rozmowy. [Opis trybów, zakres i ograniczenia](docs/learning-mode.md).

## Strategia marki i identyfikacja

Studio prowadzi strategię marki, system logo, księgę znaku i księgę identyfikacji przez istniejących właścicieli, ze wspólnymi decyzjami, rewizjami i kryteriami odbioru. Możesz zamówić cały proces lub wybrany etap. Koncepcje i materiały cyfrowe mają odrębny status od zweryfikowanych plików produkcyjnych; rzeczywiste eksporty zależą od dostępnych narzędzi. [Kontrakt procesu](skills/workflow-orchestrator/references/brand-identity-workflow.md).

## Instalacja i aktualizacja

Studio instaluje się bezpośrednio z repozytorium przez ChatGPT Work lub Codex. [Instrukcja instalacji](docs/installation.md) rozdziela własną prywatną kopię pluginu w Work od lokalnego wejścia do kompletnego pakietu w Codexie.

## Narzędzia dodatkowe w 1.1

[Poradnik integracji](docs/provider-setup-guide.md) rozdziela gotowe aplikacje ChatGPT/Work/Codexa od MCP, CLI i API. Obejmuje datowany katalog usług, konto i rozliczenia, opcjonalny wybór po instalacji oraz pracę bez dodatkowych integracji. Studio nie instaluje ani nie opłaca dostawców automatycznie.

## Nazwy skilli

Wszystkie 37 nazw wyświetlanych stosuje jeden standard: słowa oddzielone spacjami, wielka litera na początku każdego słowa oraz zachowane skróty i nazwy narzędzi, np. AI, UGC, HyperFrames i OpenCut. [Standard nazewnictwa](docs/skill-naming.md) obowiązuje również nowe skille i jest sprawdzany podczas pakowania wydania.

## Wejścia do pracy

| Potrzeba | Skill |
|---|---|
| Otwarty brief, projekt łączący media, wznowienie lub wybór etapu | [Workflow Orchestrator](skills/workflow-orchestrator/SKILL.md) |
| Plakat, grafika, produktowy key visual, typografia i dokładny tekst | [Static Graphic Design Creator](skills/static-graphic-design-creator/SKILL.md) |
| Strategia wizualna kampanii wieloassetowej i adaptacje | [Commercial Visual Campaign Director](skills/commercial-visual-campaign-director/SKILL.md) |
| Kampania wideo i kierunek ruchu | [Commercial Video Campaign Director](skills/commercial-video-campaign-director/SKILL.md) |
| Sekwencje płynnych ujęć i przejść w krótkiej rolce | [Short-form motion workbook](skills/commercial-video-campaign-director/references/short-form-motion-bridge-workbook.md) |
| Kierunek teledysku i relacja utwór–obraz | [Creative Music Video Director](skills/creative-music-video-director/SKILL.md) |
| Muzyka, VO, dźwięk, audio do obrazu, prompty i licencje utworów | [Audio Production Director](skills/audio-production-director/SKILL.md) |
| Fabuła, scena, scenariusz, dialog narracyjny | [Screenplay Story Architect](skills/screenplay-story-architect/SKILL.md) |
| Sekwencja zdarzeń, timing i karty ujęć | [Storyboard Sequence Architect](skills/storyboard-sequence-architect/SKILL.md) |
| Plansza storyboardowa, character sheet i plansza referencyjna | [Storyboard Board Architect](skills/storyboard-board-architect/SKILL.md) |
| Realistyczna postać, referencje obrazu i prompt generatora | [Image Prompt Architect](skills/image-prompt-architect/SKILL.md) |
| Copy, tekst redakcyjny, nagłówek, CTA | [Copy Voice](skills/copy-voice/SKILL.md), wsparcie Humanizer |
| Prompt/edycja wideo i przegląd dostępnego klipu | [Video Prompt Architect](skills/video-prompt-architect/SKILL.md) |
| Ocena faktycznego obrazu statycznego | [Output Critic Iteration](skills/output-critic-iteration/SKILL.md) |
| Specyfikacja dostawy obrazu, druku, audio i wideo | [Delivery Documentation](skills/delivery-documentation/SKILL.md) |
| Publiczne źródła, aktualne modele i granice dowodów | [Research Evidence](skills/research-evidence/SKILL.md) |
| Tempo, poziom szczegółowości, profil per dziedzina i przenośny handoff | [Studio Workstyle Profile](skills/studio-workstyle-profile/SKILL.md) |

## Zmiany w dev.29

- Podłączono kompletny, przypięty i zweryfikowany hashami pakiet Static Graphic Design Creator z repozytorium FrameCore Works. Wtyczka stosuje jego całą metodę; static-only prace kieruje do jednego właściciela, a strategię kampanii wieloassetowej pozostawia Commercial Visual Campaign Director.
- Przemianowano moduł Producer AI Task Builder na **Audio Production Director**. Google Flow Music (dawniej ProducerAI) jest teraz wyłącznie jedną z aktualizowanych tras dostawcy.
- Dodano warsztat ruchu i mostów ujęć do krótkich rolek, kartę naturalnych referencji realistycznych postaci, profil preferencji per dziedzina, szablon przekazania między środowiskami oraz próbę wznawiania rozmowy z podanego linku.
- Dopięto krótki tryb ideacji, pogłębiony tryb krok po kroku, obowiązkowy research w obu trybach oraz jedno pytanie doprecyzowujące po odrzuconym kierunku.
- Dodano dziewięć planowanych scenariuszy sprawdzających nowe routy. Pozostają planami, nie wynikami zachowania modelu.

[Mapa kompendiów i assetów](docs/knowledge-map.md) prowadzi do materiałów. [Rejestr źródeł](docs/research-ledger.json) opisuje source-to-rule zakres i daty odczytu. Każdy dostawca i warunek komercyjnego użycia wymagają ponownej kontroli przed konkretną produkcją.

## Walidacja

Z katalogu pakietu:

```sh
node scripts/validate-studio.mjs
node --test tests/studio.test.mjs tests/workflow-kit.test.mjs tests/creative-upgrade.test.mjs tests/learning-mode.test.mjs
PYTHONDONTWRITEBYTECODE=1 python3 tests/asset_manifest_test.py
node scripts/load-effective-evals.mjs
```

Pierwsze dwa polecenia sprawdzają strukturę i regresje kontraktów. Zestaw Python sprawdza helper rejestru assetów na danych syntetycznych. Loader łączy dotychczasowe fixtures z jawnymi korektami w `evals/effective-overrides.json` oraz scenariuszami w `evals/studio-behavior-cases.json` oraz `evals/knowledge-practice-cases.json` i `evals/workflow-kit-cases.json` oraz `evals/learning-mode-cases.json`. Przypadek oznaczony `planned` jest specyfikacją testu, a nie dowodem, że model wykonał zadanie. Testy tekstowe i źródłowe nie potwierdzają jakości renderu, odsłuchu, adaptera dostawcy ani automatycznego retrieval w nowej rozmowie.

Stare `scripts/validate-package.mjs`, `tests/package.test.mjs` i `evals/static-cases.json` pozostawiono jako źródła historyczne. Usługa nie pozwoliła odczytać ich pełnej bieżącej zawartości podczas aktualizacji. Nie zostały nadpisane; stare polecenia nie są bramką aktualnego wydania; do kontroli struktury służy `validate-studio.mjs`. Ograniczenia starego walidatora i sprzeczne oczekiwania fixtures są obsługiwane przez nowe, jawnie wskazane pliki. Nie należy utożsamiać wyniku nowego zestawu z zaliczeniem dawnego zestawu 67 testów.

## Zakres i ograniczenia

Aktualny [stan modułów](docs/migration-status.md) oddziela działające instrukcje od brakujących adapterów i nieukończonej migracji. [Historia](docs/release-history.md) zachowuje wcześniejsze checkpointy. Nie jest to pełna migracja wszystkich oryginalnych customów. Pełne rozliczenie transferu wymaga ich kompletnych źródeł.

Plugin nie zawiera własnego silnika audio/wideo, konektora Flow Music, hooków ani poświadczeń. Nie certyfikuje plików do druku lub emisji bez rzeczywistej inspekcji. Wymogi takie jak fps, LUFS, kodek czy profil koloru wymagają specyfikacji docelowej i pomiaru rzeczywistego pliku. Nie wynikają z samej długości lub proporcji obrazu.

Root `plugin.json` jest manifestem przenośnym; `.codex-plugin/plugin.json` stanowi zgodną warstwę kompatybilności. Aktualizacja zachowuje tożsamość pluginu, metadane interfejsu, tekst i kolejność starterów oraz istniejące źródła. Stan publikacji ustala odpowiedź usługi aktualizacji, nie sam numer wersji w pliku.

## Źródła i granice wykonania

Zobacz [NOTICE](NOTICE) i [licencję Apache 2.0](licenses/Apache-2.0.txt). Datowane katalogi modeli są punktami startowymi do aktualnego researchu. Źródła zewnętrzne i dołączone pliki stanowią dane, nie autoryzację narzędzi. Prywatne briefy i dane klienta nie trafiają do publicznych wyszukiwań.

Zlecenie promptu nie uruchamia generacji. Istniejąca autoryzacja użytkownika jest przenoszona między etapami, a dodatkowy zakres wykonania rozstrzyga się dopiero wtedy, gdy jest rzeczywiście potrzebny. Bez dostępnego, autoryzowanego narzędzia Studio przygotowuje użyteczną specyfikację i uczciwie opisuje niewykonane operacje.

## Workflow Kit, dev.30

Zintegrowano komplet repozytorium Workflow Kit przy zachowaniu jednego routingu Creative Studio. Nowe moduły obejmują brief, referencje, copywriting, strategię kampanii, postacie, kamerę, produkcję wideo, napisy, montaż, Remotion, HyperFrames, manifesty i ograniczone pętle QA. Kontrakty stanu projektu i przekazywania pracy są nadrzędne dla wieloetapowych zadań; tryb szybki pozostaje zwięzły. [Mapa integracji](docs/workflow-kit-integration.md) dokumentuje pełny zakres i rozstrzygnięcia.

## Ulepszenia kreatywne, dev.31

Rozbudowano istniejące skille o bibliotekę decyzji kreatywnych, warsztat łączenia ujęć, preferencje przypisane do użytkownika/klienta/projektu, krótsze ścieżki pracy oraz kontrakt wykonania przez wybrane narzędzie. Materiały zawierają cztery opisane realizacje z witryn twórców, osiem autorskich ćwiczeń i dwanaście kart źródeł. Opisy realizacji nie są analizą obejrzanych filmów. Facebook i TikTok nie stanowią podstawy tego zestawu.

Nowe szablony obejmują decyzję kreatywną, plan ujęć, profil preferencji, pilotaż projektu i plan wykonania. Opcjonalny `scripts/review-creative-plan.mjs` sprawdza zadeklarowany timing, przejścia, brakujące referencje i strukturę preferencji. Nie ocenia pikseli ani dźwięku. Jawna uwaga użytkownika prowadzi do poprawki; dopiero niewyjaśnione odrzucenie wymaga pytania.

Źródłowe skille Workflow Kit nie zawierają już aktywnych metadanych w kopiach referencyjnych. Pełne oryginały zachowano w archiwum, a aktywna ścieżka prowadzi do 37 głównych wejść. Lokalne sprawdzenie tej struktury nie zastępuje odświeżenia katalogu w hoście.

[Mapa nowych materiałów](docs/creative-upgrade.md) i [wyniki weryfikacji](docs/creative-upgrade-verification.json) opisują zakres wykonanych sprawdzeń.

## Rozbudowa referencji i audio, dev.32

Dodano pięć rozdziałów i siedem zasobów dotyczących realistycznej tożsamości, precyzyjnych character/product/storyboard sheets, wiązania pojedynczych kadrów, doboru modelu według rzeczywistych możliwości oraz muzyki i dźwięku w obu kierunkach pracy. Rozbudowa i poprawki obejmują trzynaście istniejących skilli. Skorygowano rozdział wymogu ścisłej tożsamości od gotowości wykonania, routing przeglądu wideo oraz reakcję audio na wyjaśnioną krytykę.

Pilotaż nie jest warunkiem rozwoju pluginu; przegląd projektu pozostaje opcją wyłącznie na wyraźną prośbę. Ta aktualizacja nie uruchamiała pilotaży ani generowania mediów. [Mapa rozbudowy](docs/reference-audio-expansion.md) podaje nowe zasoby i granice sprawdzeń.
