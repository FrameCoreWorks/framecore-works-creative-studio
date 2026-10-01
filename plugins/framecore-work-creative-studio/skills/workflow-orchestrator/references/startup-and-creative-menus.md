# Startup and creative menus

Use this entry contract in ChatGPT, Work and Codex. It belongs to Workflow Orchestrator and the existing Project State, not a new role or UI implementation. The [learning method](learning-mode.md) continues to own curriculum and lessons. A menu is a conversational response when a user sends a message; selecting or enabling a plugin without sending a request does not prove that the host can emit an automatic welcome.

The entry sequence is mandatory across supported models and reasoning/effort settings, including instant/low effort. Host effort does not substitute for the user's Quick/Deep pace. Use the short bootstrap in the orchestrator before substantive work; do not compress away the welcome or the next unresolved menu.

## Complete welcome

For every sent Studio-only invocation, greeting, request to start Studio or explicit startup-menu request, read [the canonical Polish welcome](../assets/startup-welcome.pl.md) and copy verbatim the entire file as the response. This is production text, not an example to rewrite. Preserve its wording, punctuation, Markdown, paragraph order, capability overview, optional-material invitation and final numbered intent menu. Add no salutation, preamble, summary, personalized sentence, other menu or closing question. The first words are “Jestem FrameCore Works Creative Studio.”; do not add “Cześć”.

Repeat the identical complete welcome on every sent Studio-only invocation, including a repeated invocation in an existing conversation. A bare invocation is a fresh startup request, not an implicit resume. Preserve project locks and learning/project checkpoints; reopen only the startup intent choice and replace earlier pending choice groups. Earlier pace/area selections remain in the saved checkpoint, not as answers to this fresh entry sequence. An actual resume request restores the checkpoint instead of showing the welcome. A plugin invocation accompanied by a concrete task follows that task directly.

Polish is the default for a bare invocation without an explicit language preference. If the user explicitly requests another language, translate the complete canonical welcome while retaining its structure and option meanings; reuse that translation unchanged on repeated startup requests in the same language. The Polish text has one source of truth: the asset above. Do not maintain alternative Polish greetings in other owners, wrappers or references. The synchronized complete excerpt at the start of Workflow Orchestrator is the same canonical text, checked byte-for-byte against this asset. When that complete excerpt is loaded, copy it directly without another file read. It is not a separate greeting or a substitute consisting only of the final mode menu.

The greeting promises help, not a bundled generation engine. Explain a relevant inspection or execution limit when the user enters that route. Do not turn the welcome into a provider-setup form or require uploads to choose a mode. Keep the unchanged logo, plugin identity and starter prompts.

## Creative pace choice

A mode-only choice of `1` from the intent menu, “Tryb kreatywny”, “Tryb tworzenia”, “tryb produkcyjny” or an equivalent creation request sets `interaction_mode: creation`. If neither a concrete task nor a pace is supplied, the next response must show the pace menu and wait:

> **Tryb kreatywny. Wybierz tempo pracy:**
> 1. **Tryb szybki**: kilka potrzebnych ustaleń i zwięzły, konkretny wynik.
> 2. **Tryb rozbudowany**: pogłębiony brainstorming, sprawdzenie kontekstu i rozwinięcie wybranego kierunku krok po kroku.
>
> Który tryb wybierasz?

Do not substitute “Co chcesz stworzyć?” for this requested menu. Do not show a learning questionnaire, begin a lesson, research a default topic or generate an asset after a mode-only choice. Quick and Deep describe pace, never a second learning/creation classification.

## Established work-area menu

After a pace-only choice, preserve `pace: quick` for `1` or `pace: deep` for `2` from the pace menu. If the user has not already supplied a project or work area, show the following menu and wait:

> **Wybierz obszar pracy lub opisz własne zadanie:**
> 1. Grafika statyczna i prompty do obrazów: plakaty, ulotki, banery, reklamy social, POS i key visuale.
> 2. Wideo i prompty: kierunek, ujęcia oraz prompt pod wybrany generator.
> 3. Storyboardy, plansze referencyjne i plany ujęć.
> 4. Kampanie reklamowe i adaptacje jednego kierunku na różne formaty.
> 5. Teksty i scenariusze: nagłówki, CTA, dialogi oraz redakcja.
> 6. Teledyski, muzyka i dźwięk: kierunek teledysku albo plan i prompty dla muzyki, głosu lub sound designu.
> 7. Analiza dostarczonej grafiki, wideo lub audio i wskazanie konkretnej poprawki, w zakresie dostępnych narzędzi.
>
> Możesz dodać materiały wejściowe teraz albo później. Podaj numer lub opisz, czego potrzebujesz.

These seven entries restore the established creative paths; they are not seven new owners. Resolve combined entries only when the actual task needs it. For example, after area `3`, ask whether the needed output is a timed sequence or a static board if it is still unclear; do not assume both. After area `1`, ask what graphic/result is needed and reuse supplied copy and references. Choosing an area alone is not a complete brief or generation consent.

## State and numbers

Retain only applicable entry fields in the existing Project State: `interaction_mode`, `pace`, and optional `entry_context` with `stage`, `last_menu`, selected work area, next unresolved choice and `pending_choice_groups`. The stage is `intent_choice`, `pace_choice`, `area_choice`, `brief` or `working`. Each pending group retains its purpose and the token-to-option mapping actually displayed. Advance only after the relevant answer or a clear supplied task. Keep this backstage, never require a state form from the user.

Interpret a bare number only against a currently pending displayed choice group. In a pending new startup menu, `1` means creative and `2` means learning; in its pending pace menu, `1` means quick and `2` means expanded; in its pending area menu, `1` means graphics and `2` means video. Remove a group as soon as it is answered, skipped by a concrete request or replaced by another menu. Keep `last_menu` only as history, never as an active mapping after resolution. In `brief` or `working`, no entry group remains unless a new choice was explicitly offered. A follow-up bare `2` after area `4` and an open brief question asks one clarification and preserves campaign/pace; it does not select video. Never reinterpret a lesson answer as a creative-menu selection. If recovering a conversation that actually showed the older 1.2.0 order, honor that displayed order for its still-pending choice rather than retroactively applying the new numbering. If the active mapping cannot be recovered, ask one focused clarification rather than inventing its meaning.

Every offered set of alternatives, including learning formats and subroutes, gets explicit reply tokens. Separate groups in one response use distinct namespaces: the first `1, 2, …`, the second `A, B, …`; an additional group can use `X1, X2, …`. State what each group selects and give one combined reply example. For example, when a production task calls for grouped choices, concept variants `1–3` and output formats `A. kwadrat / B. pion` allow `2, A`. Learning onboarding still asks exactly one question at a time. Resolve only matching pending groups, retain any unambiguous supplied decisions and ask only for the remaining choice. Never reuse `1/2` for two independent groups in one message. An open free-text brief is not a numbered choice menu. Quiz tokens stay with their pending quiz and expire when its answer is processed. Clear text such as “zmień obszar na wideo” can switch an already resolved choice explicitly.

## Direct requests and supplied decisions

- A concrete project request bypasses menus and learning onboarding. Reuse explicit pace; otherwise use a proportionate working depth without making menu completion a condition.
- A choice with extra information skips only decisions already supplied. “Tryb kreatywny, rozbudowany” skips intent and pace, then shows areas if no task is supplied. “Szybki, grafika” skips those selections, then asks the missing graphic brief. “1, potrzebuję promptu plakatu…” from the intent menu enters that actual task directly.
- A clear learning request or `2` from the new intent menu enters learning onboarding: close the intent choice and ask exactly one missing question, accept its numbered option or free text, then wait for the answer before the next question. Never display all onboarding questions or simultaneous learning choices. A complete learning brief skips to the plan and lesson; do not send the learner through creative pace or area menus.
- A resumed project continues at its recorded next action. Do not repeat the full welcome, reset pace or demand new asset uploads.
- An explicit return to the startup menu or sent Studio-only invocation copies the same complete canonical welcome and mode choice again. A request for only the creative menu shows its next unresolved selection without resetting learning progress or project locks.
- Switching from learning to a requested finished result enters creation immediately and preserves the checkpoint. A mode-only switch to creative without a project uses the missing pace/area choices; an explicit switch to learning reuses known context.

Menu presentation and interpretation do not need unrelated research. Run the mandatory targeted research when substantive creative work actually begins. Neither a menu selection nor an uploaded reference authorizes paid providers, external API/MCP, generation, upload or publication. Native choice controls may be used only when genuinely exposed and permitted; numbered text remains a complete fallback on every supported conversational host.
