# Instalacja modułów w ChatGPT Work

Scalony audyt procesu i obecnego zapisu. **Nie wykonywano nowych instalacji ani aktualizacji.** Obejmuje 17 pozycji marketplace Toolbox, 21 kandydatów paczek, 42 własne entry files w sześciu paczkach, 59 składników runtime i dodatkowy przegląd wszystkich 15 upstreamów.

## Źródło, zapis, odkrycie i wykonanie

| Etap | Dowód wymagany do zaliczenia |
|---|---|
| 1. Wybór | Zadanie, moduł, host, zakres uprawnień i istniejąca tożsamość pluginu. |
| 2. Źródło | Jeden pełny commit, licencja, manifest i wszystkie wymagane pliki z hashami; prawdziwy parser YAML/JSON. |
| 3. Paczka | Zachowane ścieżki względne, zasoby, autorstwo; rozdzielone hooks, CLI, MCP i zależności runtime. |
| 4. Natywny zapis | Odpowiednia droga Plugin Creator/Skill Creator; ten sam plugin przy aktualizacji, aktualny release guard, ochrona prywatnych dodatków. |
| 5. Odczyt zapisu | Rzeczywiste ID, release, diagnostyka i pełna lista plików; porównanie oczekiwanych bajtów. |
| 6. Nowa rozmowa | Odkrycie i odczyt faktycznie zainstalowanego skilla, nie deklaracja poprzedniej rozmowy. |
| 7. Runtime | Faktyczne wersje narzędzi i kontrola braków w bieżącym środowisku; osobno modele, browser i credentials. |
| 8. Zadanie | Wykonany mały przykład z adekwatnym QA. Sam zapis i discovery nie wystarczają. |

Aktualizacja zachowuje tożsamość, logo, starter prompts, połączenia i prywatne dodatki. Odpowiedź utracona po zapisie wymaga odczytu stanu przed retry. Usunięcia muszą dotyczyć dokładnie zaobserwowanych ścieżek. Wycofanie wersji wymaga przygotowania poprzednio zweryfikowanej treści jako kontrolowanej aktualizacji; nie usuwa się przy tym nowszych danych użytkownika. Tych operacji nie wykonano w audycie.

## Wszystkie paczki

| Paczka | Wersja źródła | Entry | Stan źródła i zapisanych zasobów |
|---|---|---:|---|
| toolbox | 1.6.1 | 1 | LOCAL_COMPONENT_CHECK_PASS |
| animate | 0.4.0 | 1 | [7e5eb56feb2d](https://github.com/cth9191/animate/tree/7e5eb56feb2dd573f890e1b7b34748af43d58263); 106/107 oczekiwanych ścieżek zapisanych; 1/1 entry identycznych bajtowo |
| motion-designer | 1.2.0 | 1 | [7d0b8bb78ddd](https://github.com/kaventro/motion-designer/tree/7d0b8bb78ddd2c91c57db9d1e83fcf711304bdb8); 58/58 oczekiwanych ścieżek zapisanych; 0/1 entry identycznych bajtowo |
| logo-design | 1.4.5 | 1 | [734090317a21](https://github.com/kaankiziltug/logo-design-skill/tree/734090317a2155c5bf1ae8bd4cc85c6848a0128f); Brak dowodu własnego zapisu pluginu; inne drogi instalacji Unknown |
| antislop | 3.2.23 | 6 | [5ca57fe37c60](https://github.com/miqdadbadjuber/anti-slop/tree/5ca57fe37c60670064abf3beae775e3dad6687a1); 9/9 oczekiwanych ścieżek zapisanych; 6/6 entry identycznych bajtowo |
| hallmark | 2.0.0 | 1 | [7ec868225c6c](https://github.com/Nutlope/hallmark/tree/7ec868225c6caa040558c321ee0fefa0e73f83a8); Brak dowodu własnego zapisu pluginu; inne drogi instalacji Unknown |
| brag | 0.5.0 | 2 | [669ab9286aa2](https://github.com/latent-spaces/brag/tree/669ab9286aa28b6c3ee30e75f181ee74319d012a); Brak dowodu własnego zapisu pluginu; inne drogi instalacji Unknown |
| nateherk-design | 0.3.1 | 1 | [75d81f74e836](https://github.com/nateherkai/scroll-craft/tree/75d81f74e83692add18cd7a8a8e078b8a887a579); 24/24 oczekiwanych ścieżek zapisanych; 1/1 entry identycznych bajtowo |
| sepia | 0.12.4 | 6 | [fb06be76abea](https://github.com/Nanako0129/sepia/tree/fb06be76abeae7dd606960a32f2b10c1d1798e0d); 26/26 oczekiwanych ścieżek zapisanych; 6/6 entry identycznych bajtowo |
| web-quality-skills | 2.0.0 | 6 | [afa8da942115](https://github.com/addyosmani/web-quality-skills/tree/afa8da942115f2961fdbfa80807ea0b232ff6c00); 16/16 oczekiwanych ścieżek zapisanych; 6/6 entry identycznych bajtowo |
| marketing-skills | 2.13.0 | 52 | [e85f3cbc2e4a](https://github.com/coreyhaines31/marketingskills/tree/e85f3cbc2e4a79bf33b2a12e9bdd9087d414735b); Brak dowodu własnego zapisu pluginu; inne drogi instalacji Unknown |
| wondelai-ux-design | 1.8.0 | 11 | [c172996495be](https://github.com/wondelai/skills/tree/c172996495bed0fcd26896a9416b2093fd7073f0); 85/85 oczekiwanych ścieżek zapisanych; 11/11 entry identycznych bajtowo |
| taste-skill | 2.1.5 | 1 | [12af471f627f](https://github.com/Leonxlnx/taste-skill/tree/12af471f627f866411b4bd785b19646d3672784c); 39/39 oczekiwanych ścieżek zapisanych; 1/1 entry identycznych bajtowo |
| hairline | 0.5.1 | 2 | [37d2e78dcb33](https://github.com/lucasmarkes/hairline/tree/37d2e78dcb333ab30c3338e28ed4a690364ea014); 14/14 oczekiwanych ścieżek zapisanych; 2/2 entry identycznych bajtowo |
| huashu-art-motion | 1.2.0 | 1 | [8a0d7d72ca65](https://github.com/alchaincyf/huashu-art-motion/tree/8a0d7d72ca65fcce6f8ba82c4a6c8dfe35b8422c); 474/491 oczekiwanych ścieżek zapisanych; 1/1 entry identycznych bajtowo |
| anatomy | 0.0.0 | 1 | [e9488296a442](https://github.com/wheresryan22/anatomy/tree/e9488296a44211c42701ff71705b7901470ec78f); 130/130 oczekiwanych ścieżek zapisanych; 1/1 entry identycznych bajtowo |
| rea | 6.5.0 | 1 | CONFIRMED_DEFECT DIST-001/DIST-002 |
| brand-kit | 1.0.1 | 1 | DIST-003: subtitle exceeds current maximum |
| framecore-work-creative-studio | 1.167.1 | 37 | LOCAL_COMPONENT_CHECK_PASS |
| voice-narration | 1.0.2 | 1 | DIST-003: subtitle exceeds current maximum |
| framecore-open-assets | 0.4.1 | 1 | LOCAL_COMPONENT_CHECK_PASS |

Liczba zgodnych ścieżek i rozmiarów nie jest dowodem zgodności wszystkich bajtów. Odczytano i porównano 37 aktywnych entry w 11 zapisanych zewnętrznych pluginach: 36 identycznych bajtowo, wszystkie 37 z identycznym body. Odczytano też siedem istotnych callerów. Nowe discovery i wykonanie zadań dla tych modułów: NOT_RUN.

## Warunki i granice piętnastu modułów zewnętrznych

| Moduł | Warunek instalacji i wykonania |
|---|---|
| animate | Brakuje sample.png Riso. Node 18+, Playwright/Chromium i ffmpeg. Zapis nie instaluje tych programów. |
| motion-designer | Body identyczne; dwa cudzysłowy naprawiają YAML. Node 22+, Chromium, ffmpeg i Python; funkcje macOS są odrębne. |
| logo-design | Pełny folder ma 1462 pliki, w tym bibliotekę SVG. Zachować LICENSE i TRADEMARKS. Python bez dodatkowych pakietów nie zapewnia renderera SVG. |
| antislop | Sześć zgodnych entry. Pythonowy checker kontrastu i stdio MCP to odrębne możliwości; zapis skilli nie aktywuje serwera MCP. |
| hallmark | Skill może być dostępny także jako osobista umiejętność. Pomocnicze screenshoty wymagają Node/przeglądarki; brak wpisu own-plugin nie oznacza braku skilla. |
| brag | Dwa skille. Render zależy od Node i narzędzi HyperFrames. Zapis źródła nie instaluje runtime ani mediów. |
| nateherk-design | Zapisany scroll-craft. Wytworzenie i sprawdzenie strony zależy od projektu i narzędzi przeglądarkowych. |
| sepia | Sześć entry, identyczne bajtowo. Zachować wspólne referencje i rozróżnienie operacji; slash-command hosta nie jest natywną funkcją Work. |
| web-quality-skills | Sześć entry. Statyczna analiza nie zastępuje Lighthouse, pomiaru wydajności ani przeglądarkowego audytu dostępności. |
| marketing-skills | 52 skille; 410 plików w folderach. Część wymaga root tools poza folderami skills. Konto reklamowe, API i publikacja mają odrębne granice. |
| wondelai-ux-design | Dokładnie 11 wybranych skilli UX, nie całe repo. Opcjonalne polecenia innych skilli nie dowodzą ich instalacji. |
| taste-skill | Natywna nazwa skilla design-taste-frontend. Inspector wymaga Node/przeglądarki; wyszukiwanie assetów wymaga osobnej rzeczywistej próby. |
| hairline | Dwa skille i wspólne zasoby. Node dla build/validate, przeglądarka dla look; fallback bez browsera musi jawnie ograniczyć QA. |
| huashu-art-motion | Brakuje 17 zasobów, w tym sześciu fontów wymaganych przed ready. Python/uv, Playwright Chromium i ffmpeg; oba standardowe bootstrapy statycznie trafiają w błąd. |
| anatomy | Zapisany skill root i 130 oczekiwanych ścieżek. Node 20.10+ i Chromium dla kontroli; publiczna publikacja społecznościowa jest odrębną operacją. |

Zasoby upstream: 93/93 entry zgodne z Git blob, 92/93 poprawne YAML. Pełny semantyczny odczyt 13 entry; pozostałe mają przegląd ukierunkowany i ekstrakcję mechaniczną. Własne repozytoria pozostają osobno w inwentarzu 2986 plików. Szczegółowe ścieżki, dowody i granice per moduł zawiera Instalacja-15-modulow-upstream.json.

## Wyszukiwanie Vercel i natywna instalacja

Docelowy przebieg: dopasowanie istniejącego Studio → katalog rozszerzeń/Toolbox → search → opis i ryzyka wyniku → wybór właściciela → przypięte źródło, licencja i pełne zasoby → odpowiednia natywna droga Work → odczyt zapisu → nowa rozmowa → właściwe zadanie. Nie tworzyć duplikatu z samej nazwy; sprawdzić źródło i tożsamość istniejącej instalacji.

Vercel CLI instaluje pliki dla obsługiwanych lokalnych agentów. Samo npx skills add lub kopiowanie do katalogu roboczego nie zapisuje osobistego skilla na koncie Work. Platforma ma odrębne drogi zarządzania skillami i prywatnymi pluginami. Finder Studio błędnie uogólnia ograniczenie CLI do braku możliwości trwałego zapisu w Work (INSTALL-01). Potrzebne jest jawne przejście do dostępnej drogi natywnej, odpowiednie do rodzaju paczki.

Wykonano search typography, describe i read jednej pozycji. Nie uruchomiono instalatora. Poprawić również walidację kształtu JSON (INSTALL-02) oraz spiąć commit tekstu, licencji, zasobów i późniejszych bajtów instalacji (INSTALL-03). Ocena katalogu i popularność nie są gwarancją bezpieczeństwa.

## Własne moduły skillowe

| Paczka | Skill | Ścieżka źródłowa |
|---|---|---|
| brand-kit | brand | `studio/plugins/brand-kit/skills/brand/SKILL.md` |
| framecore-work-creative-studio | asset-manifest | `studio/plugins/framecore-work-creative-studio/skills/asset-manifest/SKILL.md` |
| framecore-work-creative-studio | audio-production-director | `studio/plugins/framecore-work-creative-studio/skills/audio-production-director/SKILL.md` |
| framecore-work-creative-studio | brief-architect | `studio/plugins/framecore-work-creative-studio/skills/brief-architect/SKILL.md` |
| framecore-work-creative-studio | caption-studio | `studio/plugins/framecore-work-creative-studio/skills/caption-studio/SKILL.md` |
| framecore-work-creative-studio | character-design | `studio/plugins/framecore-work-creative-studio/skills/character-design/SKILL.md` |
| framecore-work-creative-studio | cinematography | `studio/plugins/framecore-work-creative-studio/skills/cinematography/SKILL.md` |
| framecore-work-creative-studio | commercial-video-campaign-director | `studio/plugins/framecore-work-creative-studio/skills/commercial-video-campaign-director/SKILL.md` |
| framecore-work-creative-studio | commercial-visual-campaign-director | `studio/plugins/framecore-work-creative-studio/skills/commercial-visual-campaign-director/SKILL.md` |
| framecore-work-creative-studio | copy-voice | `studio/plugins/framecore-work-creative-studio/skills/copy-voice/SKILL.md` |
| framecore-work-creative-studio | creative-music-video-director | `studio/plugins/framecore-work-creative-studio/skills/creative-music-video-director/SKILL.md` |
| framecore-work-creative-studio | creative-video-producer | `studio/plugins/framecore-work-creative-studio/skills/creative-video-producer/SKILL.md` |
| framecore-work-creative-studio | delivery-documentation | `studio/plugins/framecore-work-creative-studio/skills/delivery-documentation/SKILL.md` |
| framecore-work-creative-studio | ecommerce-campaign-strategy-director | `studio/plugins/framecore-work-creative-studio/skills/ecommerce-campaign-strategy-director/SKILL.md` |
| framecore-work-creative-studio | hipson-adapter | `studio/plugins/framecore-work-creative-studio/skills/hipson-adapter/SKILL.md` |
| framecore-work-creative-studio | humanizer | `studio/plugins/framecore-work-creative-studio/skills/humanizer/SKILL.md` |
| framecore-work-creative-studio | hyperframes-workflow | `studio/plugins/framecore-work-creative-studio/skills/hyperframes-workflow/SKILL.md` |
| framecore-work-creative-studio | image-prompt-architect | `studio/plugins/framecore-work-creative-studio/skills/image-prompt-architect/SKILL.md` |
| framecore-work-creative-studio | instruction-packet-factory | `studio/plugins/framecore-work-creative-studio/skills/instruction-packet-factory/SKILL.md` |
| framecore-work-creative-studio | marketing | `studio/plugins/framecore-work-creative-studio/skills/marketing/SKILL.md` |
| framecore-work-creative-studio | opencut-video-studio | `studio/plugins/framecore-work-creative-studio/skills/opencut-video-studio/SKILL.md` |
| framecore-work-creative-studio | output-critic-iteration | `studio/plugins/framecore-work-creative-studio/skills/output-critic-iteration/SKILL.md` |
| framecore-work-creative-studio | pipeline-core | `studio/plugins/framecore-work-creative-studio/skills/pipeline-core/SKILL.md` |
| framecore-work-creative-studio | producer-ai-task-builder | `studio/plugins/framecore-work-creative-studio/skills/producer-ai-task-builder/SKILL.md` |
| framecore-work-creative-studio | reference-pack-curator | `studio/plugins/framecore-work-creative-studio/skills/reference-pack-curator/SKILL.md` |
| framecore-work-creative-studio | remotion-video-production | `studio/plugins/framecore-work-creative-studio/skills/remotion-video-production/SKILL.md` |
| framecore-work-creative-studio | research-evidence | `studio/plugins/framecore-work-creative-studio/skills/research-evidence/SKILL.md` |
| framecore-work-creative-studio | screenplay-story-architect | `studio/plugins/framecore-work-creative-studio/skills/screenplay-story-architect/SKILL.md` |
| framecore-work-creative-studio | static-graphic-design-creator | `studio/plugins/framecore-work-creative-studio/skills/static-graphic-design-creator/SKILL.md` |
| framecore-work-creative-studio | storyboard-board-architect | `studio/plugins/framecore-work-creative-studio/skills/storyboard-board-architect/SKILL.md` |
| framecore-work-creative-studio | storyboard-sequence-architect | `studio/plugins/framecore-work-creative-studio/skills/storyboard-sequence-architect/SKILL.md` |
| framecore-work-creative-studio | storytelling | `studio/plugins/framecore-work-creative-studio/skills/storytelling/SKILL.md` |
| framecore-work-creative-studio | studio-workstyle-profile | `studio/plugins/framecore-work-creative-studio/skills/studio-workstyle-profile/SKILL.md` |
| framecore-work-creative-studio | tool-routing-cost | `studio/plugins/framecore-work-creative-studio/skills/tool-routing-cost/SKILL.md` |
| framecore-work-creative-studio | ugc | `studio/plugins/framecore-work-creative-studio/skills/ugc/SKILL.md` |
| framecore-work-creative-studio | video-prompt-architect | `studio/plugins/framecore-work-creative-studio/skills/video-prompt-architect/SKILL.md` |
| framecore-work-creative-studio | workflow-orchestrator | `studio/plugins/framecore-work-creative-studio/skills/workflow-orchestrator/SKILL.md` |
| framecore-work-creative-studio | workflow-self-improvement | `studio/plugins/framecore-work-creative-studio/skills/workflow-self-improvement/SKILL.md` |
| voice-narration | narrate | `studio/plugins/voice-narration/skills/narrate/SKILL.md` |
| rea | rea | `toolbox/plugins/rea/skills/rea/SKILL.md` |
| toolbox | toolbox | `toolbox/plugins/toolbox/skills/toolbox/SKILL.md` |
| framecore-open-assets | open-assets | `open-assets/plugins/framecore-open-assets/skills/open-assets/SKILL.md` |

## Runtime: osobna warstwa

Poniższe wersje pochodzą z audytowanego rejestru, nie są deklaracją tego, co jest obecnie zainstalowane w każdej sesji Work. Pełny probe wszystkich 59 składników: NOT_RUN. Naprawiać tylko faktycznie brakujące lub uszkodzone elementy, z uwzględnieniem systemu, architektury i istniejącego środowiska.

| Składnik | Rodzaj | Wersja zadeklarowana w rejestrze |
|---|---|---|
| HyperFrames CLI | npm | 0.8.181 |
| Remotion | npm | 4.0.537 |
| Animate Engine | animate | 0.4.0 |
| Manim Community | python_module | 0.22.0 |
| Blender bpy | python_module | 5.2.2 |
| FFmpeg | binary | 6.1.1 |
| FFprobe | binary | 6.1.1 |
| imageio-ffmpeg | python_module | 0.6.0 |
| imageio-ffmpeg bundled FFmpeg | ffmpeg_fallback | 7.0.2 |
| PySceneDetect | python_module | 0.7.2 |
| OpenCV | python_module | 4.12.0.88 |
| Auto-Editor | binary | 29.3.1 |
| librosa | python_module | 1.0.0 |
| PyWhisperCpp (whisper.cpp) | python_module | 1.5.1 |
| Whisper tiny multilingual | model | Unknown |
| DeepFilterNet | binary | 0.5.6 |
| ImageMagick | binary | 6.9.12-98 |
| Inkscape | binary | 1.2.2 |
| CairoSVG | python_module | 2.9.1 |
| Pillow | python_module | 12.3.0 |
| NumPy | python_module | 2.3.5 |
| Matplotlib | python_module | 3.10.8 |
| FontTools | python_module | 4.61.1 |
| Tesseract OCR | binary | 5.3.4 |
| pytesseract | python_module | 0.3.13 |
| Polish OCR tessdata_fast | model | 4.1.0 |
| React | npm | 19.2.0 |
| React DOM | npm | 19.2.0 |
| GSAP | npm | 3.14.2 |
| Three.js | npm | 0.186.0 |
| React Three Fiber | npm | 9.8.1 |
| PixiJS | npm | 8.22.0 |
| D3 Scale | npm | 4.0.2 |
| Lottie Web | npm | 5.13.0 |
| Mediabunny | npm | 1.61.1 |
| @remotion/cli | npm | 4.0.537 |
| @remotion/renderer | npm | 4.0.537 |
| @remotion/three | npm | 4.0.537 |
| Cairo | library | Unknown |
| Pango | library | Unknown |
| ManimPango | python_module | 0.7.0 |
| Pycairo | python_module | 1.29.2 |
| LaTeX | binary | Unknown |
| dvisvgm | binary | 3.2.1 |
| Typst | binary | 0.15.0 |
| lxml | python_module | 6.1.3 |
| Python | python | 3.12.14 |
| Python for Manim | python | 3.12.15 |
| Python for Blender bpy | python | 3.13.16 |
| Node.js | binary | 24.19.0 |
| npm | binary | 11.9.0 |
| npx | binary | 11.9.0 |
| TypeScript | npm | 5.9.3 |
| esbuild | npm | 0.28.2 |
| uv | binary | 0.12.23 |
| Micromamba | binary | 2.9.0 |
| Playwright | npm | 1.56.1 |
| Chromium / Headless Shell for Animate | browser | 141.0.7390.37 |
| Chrome Headless for other renders | browser | 152.0.7977.30 |

Earshot jest launcherem w Toolbox z osobnym silnikiem i modelami, nie nowym osobnym pluginem. Awesome Opus Videos to 703 rekordy wiedzy/linków już w Studio. Superpowers ma katalogową drogę domyślną; w tym audycie dostępna jest również osobna prywatna instalacja GitHub 7.0.2 zamówiona przez właściciela. Źródłowy zakaz automatycznego fallbacku nie unieważnia wyraźnej decyzji użytkownika.

Dokładne rekordy: Instalacja-modulow-Work.json. Starsze statusy niepobranego upstream w dowodach domenowych opisują etap wcześniejszy; powyższe zestawienie uwzględnia późniejszy odczyt wszystkich 15 źródeł.
