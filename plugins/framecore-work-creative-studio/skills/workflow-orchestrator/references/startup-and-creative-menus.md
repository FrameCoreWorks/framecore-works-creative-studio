# Startup and creative menus

Use this entry contract in ChatGPT, Work and Codex. It belongs to Workflow Orchestrator and the existing Project State, not a new role or UI implementation. The [learning method](learning-mode.md) continues to own curriculum and lessons. A menu is a conversational response when a user sends a message; selecting or enabling a plugin without sending a request does not prove that the host can emit an automatic welcome.

The entry sequence is mandatory across supported models and reasoning/effort settings, including instant/low effort. Host effort does not substitute for the user's Quick/Deep pace. Use the short bootstrap in the orchestrator before substantive work; do not compress away the welcome or the next unresolved menu.

## Automatic response language

<!-- BEGIN STARTUP LANGUAGE POLICY -->
Select the response language before choosing or translating the welcome. Use this order:

1. Follow the user's explicit response-language preference, including a still-active preference from this conversation. A new explicit preference replaces the earlier one.
2. Otherwise use the language of the current user-authored conversational text. Ignore quoted material, attachments, repository content, the Studio name/link and numeric choice tokens as language signals.
3. For a bare invocation or number-only answer, use the host's response/UI language only when actually supplied in the active context. Do not claim access to hidden ChatGPT or Codex settings.
4. If no host language is available, use the most recent meaningful user conversation language. A bare invocation or numeric answer does not reset that language.
5. Only when every signal is unavailable, use English as a provisional fallback. Switch as soon as a reliable user-language signal appears; do not insert a language-selection question before the welcome.

Never infer language from country, location, nationality, the plugin's Polish author, a localized asset, or the English repository. A user does not need to request translation. For English or Polish, copy verbatim the entire file for the selected language, using its embedded excerpt when loaded. For any other language, translate the complete English welcome automatically. Preserve the identity, all six capability bullets, paragraph order, tool-availability qualification, optional-material invitation, Markdown, option numbers and meanings, and final reply instruction. Keep the brand name unchanged. Add no introduction, summary, other menu or closing question.

Repeat the identical complete welcome on every sent Studio-only invocation while the selected language remains the same. Reuse an available complete translation unchanged. When the language changes, deliver the full welcome in the new language; never reuse the old language merely because a checkpoint or translation exists. Apply the same language selection to subsequent pace/area menus and learning onboarding. Translate displayed labels and descriptions, preserving option order, reply tokens and their active state mapping. Concrete tasks and actual resume requests still bypass the welcome and retain checkpoints.
<!-- END STARTUP LANGUAGE POLICY -->

## Complete welcome

For every sent Studio-only invocation, greeting, request to start Studio or explicit startup-menu request, deliver the complete welcome in the automatically selected language. [The English source](../assets/startup-welcome.en.md) and [approved Polish translation](../assets/startup-welcome.pl.md) have synchronized complete excerpts near the start of Workflow Orchestrator. When a matching excerpt is loaded, use it without another file read. For another language, translate the entire English source, never a mode-selection summary. These are production content sources, not a fixed language default. The first sentence identifies FrameCore Works Creative Studio in the selected language. Show exactly one complete welcome without extra text and stop for the intent answer.

A bare invocation is a fresh startup request, not an implicit resume. Preserve project locks and learning/project checkpoints; reopen only the startup intent choice and replace earlier pending choice groups. Earlier pace/area selections remain in the saved checkpoint, not as answers to this fresh entry sequence. An actual resume request restores the checkpoint instead of showing the welcome. A plugin invocation accompanied by a concrete task follows that task directly. Repetition preserves the full welcome and selected language under the policy above, not a hardcoded Polish response.

The approved Polish asset remains the sole source of Polish wording. Its embedded projection and the English source projection are checked byte-for-byte. Keep both excerpts before general QA and routing, and keep the embedded language policy synchronized with this reference. No owner, wrapper or README may override it with a fixed Polish default or require an explicit translation request.

The greeting promises help, not a bundled generation engine. Explain a relevant inspection or execution limit when the user enters that route. Do not turn the welcome into a provider-setup form or require uploads to choose a mode. Keep the unchanged logo, plugin identity and starter prompts.

## Motion graphics in creative work

The complete welcome offers only Creative Mode and Learning Mode. Code-based motion graphics remains available in the established work-area menu: choose Creative Mode, Expanded Mode, then area `8`. Retain the selected pace and motion work area in the existing `entry_context`; add no new state field. Preserve a runtime explicitly supplied with the answer, such as "8, Remotion".

After area `8`, ask only the missing motion brief. A concrete task uses the existing direct-task rule without making menu completion a prerequisite. Supplied areas, runtimes and pace choices retain the existing skip rules, including Quick Mode. An explicit request to learn motion graphics follows Learning Mode instead of creation.

Use the existing [code-motion workflow](../../hyperframes-workflow/references/code-based-motion-graphics.md). HyperFrames Workflow owns HTML/SVG/GSAP and HyperFrames work; Remotion Video Production owns an explicitly selected React/TypeScript route. Name these as supported routes, not installed tools. Preview, inspection and encoded export depend on actual host capabilities. Selecting the area authorizes no installation, rendering, paid provider, upload or publication. Storyboard approval and existing execution boundaries still apply.

## Creative pace choice

A mode-only choice of `1` from the intent menu, “Tryb kreatywny”, “Tryb tworzenia”, “tryb produkcyjny” or an equivalent creation request sets `interaction_mode: creation`. If neither a concrete task nor a pace is supplied, the next response must show the pace menu in the selected user language and wait. The Polish text below is its approved localized example; translate every label and description for other languages:

> **Tryb kreatywny. Wybierz tempo pracy:**
> 1. **Tryb szybki**: kilka potrzebnych ustaleń i zwięzły, konkretny wynik.
> 2. **Tryb rozbudowany**: pogłębiony brainstorming, sprawdzenie kontekstu i rozwinięcie wybranego kierunku krok po kroku.
>
> Który tryb wybierasz?

Do not substitute “Co chcesz stworzyć?” for this requested menu. Do not show a learning questionnaire, begin a lesson, research a default topic or generate an asset after a mode-only choice. Quick and Deep describe pace, never a second learning/creation classification.

## Established work-area menu

After a pace-only choice, preserve `pace: quick` for `1` or `pace: deep` for `2` from the pace menu. If the user has not already supplied a project or work area, show the following menu in the selected user language and wait. This Polish example fixes option meanings and order, not the response language:

> **Wybierz obszar pracy lub opisz własne zadanie:**
> 1. Grafika statyczna i prompty do obrazów: plakaty, ulotki, banery, reklamy social, POS i key visuale.
> 2. Wideo i prompty: kierunek, ujęcia oraz prompt pod wybrany generator.
> 3. Storyboardy, plansze referencyjne i plany ujęć.
> 4. Kampanie reklamowe i adaptacje jednego kierunku na różne formaty.
> 5. Teksty i scenariusze: nagłówki, CTA, dialogi oraz redakcja.
> 6. Teledyski, muzyka i dźwięk: kierunek teledysku albo plan i prompty dla muzyki, głosu lub sound designu.
> 7. Analiza dostarczonej grafiki, wideo lub audio i wskazanie konkretnej poprawki, w zakresie dostępnych narzędzi.
> 8. Motion graphics z kodu: animowane napisy, logotypy, diagramy i sekwencje graficzne; storyboard, kod i kontrola animacji w HTML/SVG, GSAP, HyperFrames lub Remotion (React/TypeScript). Podgląd i eksport zależą od dostępnych narzędzi.
>
> Możesz dodać materiały wejściowe teraz albo później. Podaj numer lub opisz, czego potrzebujesz.

These eight entries expose the existing creative paths; they are not new owners. Area `8` selects the existing code-motion workflow, preserving the already chosen pace. Area `3` still selects storyboards. Resolve combined entries only when the actual task needs it. For example, after area `3`, ask whether the needed output is a timed sequence or a static board if it is still unclear; do not assume both. After area `1`, ask what graphic/result is needed and reuse supplied copy and references. Choosing an area alone is not a complete brief or generation consent.

## State and numbers

Retain only applicable entry fields in the existing Project State: `interaction_mode`, `pace`, and optional `entry_context` with `stage`, `last_menu`, selected work area, next unresolved choice and `pending_choice_groups`. The stage is `intent_choice`, `pace_choice`, `area_choice`, `brief` or `working`. Each pending group retains its purpose and the token-to-option mapping actually displayed. Advance only after the relevant answer or a clear supplied task. Keep this backstage, never require a state form from the user.

Interpret a bare number only against a currently pending displayed choice group. In a pending new startup menu, `1` means creative and `2` means learning; in its pending pace menu, `1` means quick and `2` means expanded; in its pending area menu, `1` means graphics, `2` means video, `3` means storyboards and `8` means motion graphics. A `3` from the two-option startup menu asks for clarification without selecting motion or changing its mapping. Remove a group as soon as it is answered, skipped by a concrete request or replaced by another menu. Keep `last_menu` only as history, never as an active mapping after resolution. In `brief` or `working`, no entry group remains unless a new choice was explicitly offered. A follow-up bare `2` after area `4` and an open brief question asks one clarification and preserves campaign/pace; it does not select video. Never reinterpret a lesson answer as a creative-menu selection. On actual resume, honor a genuinely still-pending older displayed menu, including the older 1.2.0 order or three-option startup, rather than retroactively applying the new numbering. If the active mapping cannot be recovered, ask one focused clarification rather than inventing its meaning.

Every offered set of alternatives, including learning formats and subroutes, gets explicit reply tokens. Separate groups in one response use distinct namespaces: the first `1, 2, …`, the second `A, B, …`; an additional group can use `X1, X2, …`. State what each group selects and give one combined reply example. For example, when a production task calls for grouped choices, concept variants `1–3` and output formats `A. kwadrat / B. pion` allow `2, A`. Learning onboarding still asks exactly one question at a time. Resolve only matching pending groups, retain any unambiguous supplied decisions and ask only for the remaining choice. Never reuse `1/2` for two independent groups in one message. An open free-text brief is not a numbered choice menu. Quiz tokens stay with their pending quiz and expire when its answer is processed. Clear text such as “zmień obszar na wideo” can switch an already resolved choice explicitly.

## Direct requests and supplied decisions

- A concrete project request bypasses menus and learning onboarding. Reuse explicit pace; otherwise use a proportionate working depth without making menu completion a condition.
- A choice with extra information skips only decisions already supplied. “Tryb kreatywny, rozbudowany” skips intent and pace, then shows areas if no task is supplied. “Szybki, grafika” skips those selections, then asks the missing graphic brief. “1, potrzebuję promptu plakatu…” from the intent menu enters that actual task directly.
- A clear learning request or `2` from the new intent menu enters learning onboarding: close the intent choice and ask exactly one missing question, accept its numbered option or free text, then wait for the answer before the next question. Never display all onboarding questions or simultaneous learning choices. A complete learning brief skips to the plan and lesson; do not send the learner through creative pace or area menus.
- A resumed project continues at its recorded next action. Do not repeat the full welcome, reset pace or demand new asset uploads.
- An explicit return to the startup menu or sent Studio-only invocation delivers the complete welcome and mode choice again in the currently selected user language. A request for only the creative menu shows its next unresolved selection without resetting learning progress or project locks.
- Switching from learning to a requested finished result enters creation immediately and preserves the checkpoint. A mode-only switch to creative without a project uses the missing pace/area choices; an explicit switch to learning reuses known context.

Menu presentation and interpretation do not need unrelated research. Run the mandatory targeted research when substantive creative work actually begins. Neither a menu selection nor an uploaded reference authorizes paid providers, external API/MCP, generation, upload or publication. Native choice controls may be used only when genuinely exposed and permitted; numbered text remains a complete fallback on every supported conversational host.
