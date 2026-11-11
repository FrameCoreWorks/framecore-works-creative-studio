# DR-03 — odrzucenia, duplikaty i reference-only
Data: 2026-11-11. „Odrzucono” dotyczy zakresu tego researchu/admission; nie ocenia ogólnej jakości produktu. Nie przywracamy usuniętych wpisów i nie zmieniamy katalogów.

| Zasób/klasa | Status | Powód i dowód | Co może wrócić później |
|---|---|---|---|
| useAnimations jako nowy renderer/Toolbox tool | ALREADY_COVERED; bez nowej admission | Znany reported test, raw JSON możliwy istniejącym Lottie route; interactive wrapper nie dowodzi arbitrary seek. [Sekcja 14](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/4611c9c4ed44579b8a2c0224c9276d955fccd8d6/docs/handover-creme-de-la-creme-2026-11-09.md) | On-demand asset A/B z T11; każda ikona alpha/renderer QA |
| Generative Icons jako nowość i offline authoring | ALREADY_COVERED; nie przyjmować twierdzenia offline authoring | Znany source/asset version split, sign-in dla draft/build, brak integration tests. Ten sam handover | Gotowa rodzina assetów może oszczędzić pracę; nie automatyczny MCP |
| GL transitions jako odkrycie nowego katalogu | ALREADY_COVERED | Aktywny [Toolbox review](https://github.com/FrameCoreWorks/framecore-works-toolbox/blob/adc8094f8e087889e4337c99dd0d267ae1b11a51/reviews/gl-transitions.md) | Konkretna nowa technika, po pinu i per-shader rights |
| PixelFX jako nowa biblioteka | ALREADY_COVERED | Aktywny [review](https://github.com/FrameCoreWorks/framecore-works-toolbox/blob/adc8094f8e087889e4337c99dd0d267ae1b11a51/reviews/pixelfx.md); font galerii nie jest objęty MIT | Bounded production pilot istniejącej pozycji; nie dublować fontu |
| GSAP/Pixi/Three skills w całości | ALREADY_COVERED | GSAP/Three w manifest; Pixi adapted w Studio source ledger | Tylko konkretna luka typu graphemes/RNG/async fonts |
| Kolejny pełny HTML→film engine (Vawe) | REJECT dla obecnej rekomendacji dependency; KNOWLEDGE_ONLY discovery | [Odczytana dokumentacja](https://vawe.dev/docs/determinism) deklaruje virtual clock i seek-based rendering. Te cele już mają Studio/HyperFrames i motion-launch-videos. Nie sprawdzano kodu/licencji/install. | Targeted source inspection tylko gdy istniejący adapter ma wykazaną lukę; dokumentacja nie jest benchmarkiem |
| blender-agent-skills / ffmpeg-skill / iso-glow jako „brakujące nowe” wpisy | Znane, usunięte z aktywnego katalogu | Odczytane reviews B13–B15; user/catalog decisions i manual/desktop requirements | Osobna decyzja właściciela; obecny research nie jest rollbackiem |
| Pinterest i niesprawdzone galerie autora | REFERENCE_ONLY | Open Assets README/provider index wyłącza Pinterest z production-licensed sources | Konkretne dzieło z ustalonymi prawami przez właściwego autora |
| Shadertoy jako hurtowy shader pack | REFERENCE_ONLY / rights Unknown | Próba odczytu [terms](https://www.shadertoy.com/terms) zwróciła 402; nie przeczytano umowy i nie wybrano dzieła z licence | Per-shader prawa i code inspection; nie przypisywać całej galerii licencji biblioteki |
| Forki/repacki powyższych | DUPLICATE/FORK — reguła selekcji, bez sztucznej listy nazw | Brak wykazanej delty; canonical upstream pierwszeństwo | Tylko udokumentowana naprawa lub capability, z historią upstream |

Dodatkowe ograniczenia assetów i rejected leads znajdują się w agents/assets/CARDS.md oraz sources.json. URL z nieudaną odpowiedzią lub sam wynik wyszukiwarki nie liczy się jako przeczytane źródło. Nie zebrano nazw słabych kandydatów wyłącznie dla osiągnięcia liczby.

