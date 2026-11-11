# DR-03 — plan prób wykonawczych
Status całości: **NOT_RUN**. Fixture i kryteria poniżej są **DERIVED**, nie rezultatem uruchomienia kandydatów. Nie tworzą pozwolenia na instalację. Raport bada dokumenty i kod; ten plan wymaga osobnego autoryzowanego zadania wykonawczego.

## Wspólny kontrakt próby
Jeden 6-sekundowy shot, 180 klatek przy 30/1 fps, niezależne kompozycje 1920×1080 i 1080×1920. Później oddzielny test 30000/1001 fps. Klip referencyjny bez audio ma declared silence; wariant audio używa własnego syntetycznego click-track z onsetami 0.5/1.7/3.1/4.9 s. Każdy wynik niesie: hash wejścia, code SHA, lock hash, renderer/browser/OS/GPU, font hash, seed, ratio fps, dimensions, color space, alpha mode i ustawienia eksportu. Próbki nie są claimem jakości.

Kopia testowa: „Zażółć gęślą jaźń — Łódź, 1 234,56 zł”. Drugi zestaw zawiera NFC/NFD polskie litery, emoji rodzinne z ZWJ, słowo z nonbreaking space i ligaturę „fi”. Font ma potwierdzoną licencję i lokalne bajty. Brak glyphu = kontrolowany błąd albo zaakceptowana lista fallback, nie cicha zamiana.

## Próby i bramki
| ID | Fixture / operacja | Oczekiwane świadectwo | Błędy, których szukać | Ogląd temporalny | Status |
|---|---|---|---|---|---|
| T01 | Jeden konkretny SVG/Lottie/.lottie/.riv/atlas/VDB/glTF z prawami i hashem, import bez sieci | Import/decode wynik + brak niejawnych requests; lista obsługiwanych funkcji | external images/fonts/scripts, ZIP paths, unsupported matte/filter, broken refs | Powolny i normalny playback całego 6 s, porównanie z autorem tylko jeśli zgodny renderer | NOT_RUN |
| T02 | Pozycje 0,1,17,89,179,89,17,0; drugi świeży proces; ten sam seed | Każda powtórzona klatka identyczna w tym samym host/render config dla modułów deklarujących pure seek; różnice jawne | hidden ticker, state history, wall-clock, Math.random | Kontaktówka + blink/diff oraz pełny film, ponieważ hash nie ocenia choreografii | NOT_RUN |
| T03 | Pętla 60 klatek, sekwencja 0..59 ×3, osobno 0 i 60 stanu okresowego | State(t+period)=State(t); brak zduplikowanego hold na szwie; export [0,N) | wrong modulo, N-1 zamiast N duration, jump particles | Odtworzyć 3 pętle 1× i 0.25×, powiększenie seam, zbadać prędkość na granicy | NOT_RUN |
| T04 | Cienkie ukośne krawędzie, soft glow, blur i półprzezroczysty gradient na alfa | PNG RGBA i jawny alpha codec variant; kompozycja na białym/czarnym/magenta bez fringe | opaque white cutout, straight/premultiplied mismatch, filter padding, dropped alpha | Krawędzie w ruchu oglądane 100% i 200%; checkerboard nie wystarcza | NOT_RUN |
| T05 | Polski tekst + NFC/NFD + ZWJ, wejście/reveal/reflow/hold; font delayed i missing | Loaded required face i glyph coverage; graphemes nie rozrywane; dokładna kopia w hold | FOIT/FOUT, tofu, clipping diakrytyków, unstable line wrap, stale async sync | Wszystkie wejścia/wyjścia i readable holds na telefonowej szerokości 360 px | NOT_RUN |
| T06 | Ten sam scenariusz 16:9/9:16, ale jawne layout params i camera framing | Osobne dowody dla każdego formatu, brak crop-u sensu/etykiet | DOM label poza canvas export, safe area, pixel-size scaling | Dwa pełne odtworzenia; nie akceptować pionu z kontaktówki poziomu | NOT_RUN |
| T07 | Procedural glitch/noise/trails/particles, reset+fixed-step replay albo analytic clock | Powtarzalne history buffers lub jawny bake; seed wszystkich RNG | seed pokrywa tylko uniform, random geometry niekontrolowana, bloom history | Całość 1× i 0.25×; flicker/popping/aliasing, intentional glitch vs błąd | NOT_RUN |
| T08 | Rive state machine lub physics: ten sam event log i initial state, rewind/replay | Jawny brak arbitrary seek; replay do t identyczny dla tej wersji i timestep | variable delta, event reorder, float drift, docs/API mismatch | Pełna trajektoria + momenty eventów; nie tylko end frame | NOT_RUN |
| T09 | Onset/caption cue table: próbki → sekundy → master frames | Deterministyczne mapowanie i znany rounding; audio unchanged | hop length, centered window bias, wrong sr, time stretch/offset | Słuchanie z obrazem przez cały klip; +/-1 frame click alignment fixture, nie wymóg rytmu dla muzyki | NOT_RUN |
| T10 | MP4 opaque, PNG sequence alpha, opcjonalny WebM alpha/EXR Blender | ffprobe + actual decode: liczba klatek, PTS monotonic, ratio FPS, dims, audio count; codec availability | container label ≠ support, lost frame, wrong duration, gamma shift | Pełny odkodowany export i porównanie preview/export na tym samym display/color path | NOT_RUN |
| T11 | Asset family versus model-authored geometry, identyczny brief/copy/palette/shot | Rzeczywisty czas setup/adapt/revision; jakość przy tym samym budżecie poprawek | zawyżanie token/cost z elapsed time, nierówne kompozycje/host | Ślepa porównawcza ocena pełnych klipów, brand fit, consistency i editability | NOT_RUN |
| T12 | Proces bez sieci po świadomym prefetch, przerwane init/cancel, cache cold/warm | Przewidywalne errors, cleanup i brak częściowego accepted output | remote font fallback, worker hang, leaked GPU buffers, partial export | Niezależny smoke view po recovery; brak wyniku to failure, nie fallback do innego silnika | NOT_RUN |

## Dowody i tolerancje
- Pure JS/CPU geometry i identyczna konfiguracja: exact image bytes po dekodowaniu albo exact RGBA hashes są celem determinism probe. Kompresowane MP4 bytes nie muszą być identyczne; porównuje się dekodowane klatki i metadane.
- GPU/font rasterization między różnymi platformami: tolerancję trzeba zadeklarować przed próbą; wyniku „blisko” nie nazywać exact determinism. Drobne różnice raportować liczbowo (count/max/mean), duże oceniać lokalnie, bez zacierania.
- Pixelmatch/SSIM/diff wykrywają zmianę; nie mierzą jakości ruchu. Kontrola metadanych nie potwierdza alfy, seam ani brzmienia.
- H.264 MP4 służy do opaque delivery. PNG RGBA to najprostszy interchange. EXR tylko przez świadomie wybraną ścieżkę float/linear, np. Blender, nie konwersja zwykłego 8-bit PNG pod nazwą HDR.
- WebM VP9 alpha i ProRes 4444 muszą przejść decode/composite w docelowym odbiorniku; format kontenera nie stanowi dowodu alpha support.
- Każdy materiał ma cztery niezależne werdykty baseline Studio: technical, fidelity, composition, temporal. Powtórzyć tylko testy dotknięte zmianą.

## Minimalne pilotaże i stop rule
1. Text+SVG (T01,T02,T04,T05,T06): jedna ścieżka morph i jeden tekst z polskimi znakami.
2. Shader/particles (T02,T03,T04,T07,T10,T12): jeden konkretny efekt z jawnym modelem stanu; glitch nie może dostać deterministic pass przez sam seed.
3. Asset family (T01,T03,T04,T06,T10,T11): 3–6 powiązanych assetów, bez masowego pobierania.
4. Knowledge deltas (T05,T08,T09): jeden kontrakt grapheme, state machine replay albo audio onset; wybrać faktyczną lukę.

Po pierwszej materialnej niezgodności ustalić root cause. Maksymalnie dwa celowane repair rounds w przyszłym zadaniu; brak prawa, brak render path albo brak wartości wobec baseline kończy pilot. Nie instalować automatycznie następnego silnika ani nie zmieniać providerów.

