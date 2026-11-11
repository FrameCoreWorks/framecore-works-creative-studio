# Lead spot-check — DR-03
2026-11-11. Odczyt przez GitHub connector, niezależnie od opisu agenta runtime. **CODE_INSPECTED**, wykonanie **NOT_RUN**.

1. [EffectPass.js](https://github.com/pmndrs/postprocessing/blob/a1f103559d15cf56cbcbb15d4373711b09418f3f/src/passes/EffectPass.js): render przyjmuje deltaTime; linia 575 zwiększa material.time przez deltaTime*timeScale. Potwierdza, że sam render(delta) nie stanowi arbitrary absolute seek. Nie stwierdza, że wszystkie efekty są niemożliwe do adaptacji.
2. [GlitchFilter.ts](https://github.com/pixijs/filters/blob/e9d1ca987864f121680bb0d7e9612c05b37748de/src/glitch/GlitchFilter.ts): uSeed ma publiczny getter/setter, ale rozmiary, shuffle i offsets wołają Math.random (245,259,281,298). Potwierdza wąski wniosek: ustawienie seed uniformu nie seeduje całej geometrii. Nie wykonano filmu.
3. [Cargo.toml](https://github.com/thx/resvg-js/blob/9de8ddd9dd62293006d849dd846a3b91ba992f23/Cargo.toml): patch resvg do git rev 3495d870 oraz woff2-rs branch fix-total-compressed-size. To sygnał do kontroli Cargo.lock/release artefact, nie dowód, że prebuilt npm binary pobierze branch w runtime.

Te odczyty nie potwierdzają wyglądu, alpha ani zgodności hosta. Źródła także znajdują się w rejestrze runtime (R04_SRC02, R05_SRC02, R09_SRC04). Plan przyszłych testów musi to rozdzielać.

