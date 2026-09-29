# Narzędzia dodatkowe: ChatGPT, Work i Codex

Stan wiedzy: **29.09.2026**. Studio pomaga dobrać i skonfigurować wybraną ścieżkę. Samo zainstalowanie Studio daje wiedzę i instrukcje, nie konta dostawców ani kredyty. Możesz pracować wyłącznie nad pomysłami, storyboardami i promptami.

## 1. Wybierz sposób dostępu

| Ścieżka | Co podłączasz | Gdzie można jej użyć |
|---|---|---|
| Gotowa aplikacja/plugin | Istniejącą integrację z katalogu i, jeśli wymagane, konto dostawcy | ChatGPT Chat, Work lub obsługiwany klient Codexa, zależnie od konkretnej integracji i konta |
| Własny MCP | Udokumentowany serwer narzędzi i jego autoryzację | Codex z obsługą MCP; w ChatGPT tylko przy dostępnej i dozwolonej konfiguracji własnych aplikacji |
| CLI | Program dostawcy uruchamiany w środowisku z terminalem | Zwykle lokalny Codex; instalacja w chwilowym środowisku Work nie zapewnia stałego dostępu z telefonu |
| API/SDK | Integrację kodową, klucz i rozliczenie API | Codex lub inny właściwy runtime; sam klucz nie tworzy aplikacji w ChatGPT |
| Strona dostawcy | Ręczną pracę z promptem i plikami | Przeglądarka użytkownika |

To nie jest podział „ChatGPT tylko pluginy, Codex tylko API”. Możliwości należy sprawdzić w używanej aplikacji. [Podstawy OpenAI](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt-and-codex), [MCP w Codexie](https://developers.openai.com/codex/mcp), [własne MCP w ChatGPT](https://help.openai.com/en/articles/12584461-developer-mode-and-mcp-apps-in-chatgpt).

## 2. Jakie usługi uwzględnia Studio

Poniższe gotowe integracje potwierdzono w katalogu lub oficjalnej dokumentacji. To lista wybranych usług, nie pełny katalog. Dostępność w konkretnym planie, regionie, telefonie i widoku rozmowy wymaga sprawdzenia. Szczegóły dowodów i ograniczeń zawiera [rejestr źródeł](../skills/tool-routing-cost/references/provider-sources.md).

| Usługa | Główne zastosowanie gotowej integracji | Konto i koszty |
|---|---|---|
| fal | Obraz, wideo, audio, 3D i przetwarzanie mediów | Konto fal; płatne wykonania modeli. Abonament ChatGPT ich nie finansuje. |
| Higgsfield | Generowanie obrazu i wideo, workflow kreatywne | Konto Higgsfield; warunki ścieżki konsumenckiej opisano poniżej. |
| Runway | Generowanie i edycja obrazu, wideo oraz audio | Konto/workspace Runway; właściwy plan i kredyty do sprawdzenia. |
| OpenArt | Generowanie obrazu i wideo | Konto i kredyty OpenArt; wymagany plan: **Unknown**. |
| HeyGen | Wideo z awatarami, głosami i tłumaczeniem | Uprawnienia konta i koszty konkretnej operacji: **Unknown**. |
| Descript | Montaż, transkrypcja, napisy, krótkie klipy | Plan i limity operacji: **Unknown**. |
| Adobe | Obróbka obrazu, materiały graficzne, wideo i dokumenty | Katalog opisuje tryb gościa oraz dodatkowe możliwości po zalogowaniu; warunki operacji trzeba sprawdzić. |
| Adobe Express | Projekty z szablonów i ich edycja | Katalog opisuje bezpłatny start; nie oznacza to bezpłatności wszystkich assetów i eksportów. |
| Canva | Projekty graficzne i prezentacje | Wymagania konta, planu i wybranej funkcji: **Unknown**. |
| Figma | Edytowalne projekty i praca z designem | Zakres dostępu i koszty: **Unknown**. |
| Replit | Budowanie aplikacji i stron | Oddzielna kategoria. Nie należy zakładać, że jest generatorem ujęć wideo. Koszty budowania/hostingu do sprawdzenia. |

**ElevenLabs:** potwierdzone oficjalne narzędzia API/MCP i skille. Gotowa aplikacja w katalogu ChatGPT: **Unknown** w tym przeglądzie. Brak wyniku wyszukiwania nie dowodzi, że taka aplikacja nie istnieje. Przy wyborze trzeba ponowić wyszukiwanie. To samo dotyczy innych nowych usług, np. MuAPI i POYO.

## 3. fal: gotowy plugin lub integracja programistyczna

[Oficjalny plugin fal](https://chatgpt.com/plugins/fal) jest opisany dla ChatGPT i Codexa. Zainstaluj go w obsługiwanym widoku, połącz konto fal i wybierz go w rozmowie. Weryfikację zacznij od wyszukania modeli bez generowania. Wybór konta OAuth w fal przez **Use for MCP** jest niezależny od zwykłego przełącznika konta na stronie. Klucz API wskazuje konto powiązane z tym kluczem. [Instrukcja fal](https://fal.ai/docs/documentation/setting-up/codex-plugin).

W Codexie możesz zamiast gotowego pluginu wybrać inference MCP, API/SDK lub udokumentowane CLI. Nie instaluj równocześnie kilku ścieżek bez potrzeby. Model, schemat wejść i stawkę sprawdź dla konkretnego zadania. [Run MCP](https://fal.ai/docs/documentation/setting-up/mcp), [cennik](https://fal.ai/pricing). MCP do generowania i Platform MCP do administracji/deployu to różne serwery.

Logowanie nie oznacza zakupu abonamentu. fal rozlicza użycie modeli; oferuje też opcjonalne plany kredytowe. Uprawnienia, saldo i rabaty zależą od konta oraz ścieżki, nie od samej nazwy modelu. Nie zakładaj, że rabat strony obejmuje API. [Plany fal](https://fal.ai/docs/documentation/agent/access-and-pricing).

## 4. Higgsfield: dwa odrębne rozliczenia

| Ścieżka | Uwierzytelnienie | Rozliczenie |
|---|---|---|
| Gotowy plugin ChatGPT / MCP / oficjalne CLI | Logowanie do konta Higgsfield | Ścieżka konta konsumenckiego; przewodnik wymaga aktywnego płatnego planu. Aktualne wyjątki trial/free wymagają potwierdzenia. |
| Higgsfield API, konsola **open.higgsfield.ai** | Własne poświadczenia API | Osobne saldo w USD, płatność za użycie; abonament strony nie jest wymagany i nie zastępuje salda API. |

[Połączenie pluginu/MCP](https://higgsfield.ai/creator-hub/help-center/integrations/how-do-i-connect-higgsfield-to-ai-agent), [oficjalne CLI](https://higgsfield.ai/cli), [wyjaśnienie API](https://higgsfield.ai/creator-hub/help-center/integrations/what-is-the-higgsfield-api).

**Open Higgsfield** w powyższej tabeli oznacza oficjalną konsolę API. Projekty `wide-trace/open-higgsfield`, `openhiggsfield.ai` oraz `openhiggsfield.com` mają podobne nazwy, ale nie są tą konsolą. Jeśli chodzi o zewnętrzny projekt, trzeba wskazać jego dokładny adres; uruchomienie interfejsu nie daje darmowego dostępu do modeli.

W źródłach występuje rozbieżność: starszy poradnik Higgsfield ogranicza audio, strony i darmowe wykonania w ChatGPT, natomiast obecnie udostępnione opisy narzędzi obejmują te funkcje oraz pola uprawnień trial/free. Studio ma sprawdzać narzędzie i uprawnienie konkretnego konta, zamiast obiecywać działanie. Nie przenoś automatycznie „Unlimited” ze strony do pluginu lub API.

## 5. Instalacja krok po kroku

**ChatGPT Chat / Work, gotowa integracja:**

1. Otwórz dostępny na swoim koncie katalog **Plugins** lub **Apps**. Wyszukaj usługę i sprawdź wydawcę, zakres oraz wymagania.
2. Wybierz instalację/połączenie i ukończ logowanie w oknie dostawcy, jeśli jest wymagane.
3. W rozmowie wybierz integrację przez `@` lub dostępne menu. Wklejona nazwa nie potwierdza aktywacji.
4. Poproś o obsługiwany odczyt bez generowania. Dopiero potem ustal model, referencje i koszt właściwego zadania.

**Codex, API/MCP/CLI:**

1. Wskaż dokładny klient Codexa i preferowaną ścieżkę. Gdy gotowy plugin jest dostępny i wystarcza, nie trzeba pisać API.
2. Dla MCP/CLI sprawdź oficjalny endpoint/pakiet i sposób logowania. Dla API ustal produkt, konto rozliczeniowe i miejsce prywatnego przechowania sekretu.
3. Konfiguruj tylko wybraną integrację, po poleceniu użytkownika. Zachowaj istniejące ustawienia; nie wpisuj kluczy do czatu ani repozytorium.
4. Zweryfikuj połączenie odczytem, potem osobno uzgodnij płatną operację i przesłanie referencji. Wynik instalacji i wynik generowania to dwa oddzielne potwierdzenia.

Przy instalacji Studio możesz wybrać „mam konto”, „chcę poradnik” lub „pomiń”. Podanie preferencji nie instaluje dodatkowego programu ani nie upoważnia do zakupu, aktywacji triala, uploadu lub generowania. Twoje ustawienia nie trafiają do wspólnego pluginu.

## 6. Najczęstsze blokady

| Problem | Następny krok |
|---|---|
| Plugin jest w katalogu, ale brak narzędzia | Sprawdź instalację, wybór w rozmowie i obsługę danej funkcji w tym kliencie. |
| Logowanie działa, generowanie odrzucone | Sprawdź konto/workspace, plan, saldo i dostęp do modelu. Nie zmieniaj konta ani ścieżki bez uzgodnienia. |
| Referencja jest w ChatGPT, ale serwis jej nie widzi | Ustal obsługiwany transfer. Lokalna ścieżka i identyfikator załącznika nie są publicznym URL-em. |
| Wywołanie zakończyło się timeoutem | Sprawdź istniejący identyfikator zadania. Ponowne wysłanie może naliczyć drugi koszt. |
| Brak integracji lub użytkownik pomija konfigurację | Kontynuuj koncepcję i przygotuj gotowy prompt do ręcznego użycia. |

Niektóre narzędzia wyceny importują pliki referencyjne. Studio sprawdza skutki operacji przed jej użyciem. Wybrana nazwa modelu u różnych dostawców nie gwarantuje takich samych parametrów, cennika ani praw do wyników.
