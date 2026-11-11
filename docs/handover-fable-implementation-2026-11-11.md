# Implementation handover for Fable 5.2: research intake 9–11 November 2026

Date: 2026-11-11. Origin: Cloud Code (Claude), Change-ID `CC-20261111-01`. Baseline: Studio `main` `0924a098848850eb43ba8d39bcb2db1209d31b52`, package 1.174.1, Toolbox catalog 1.12.0, Open Assets 0.5.0.
Receiver: a Claude Fable 5.2 (`claude-fable-5-2`) session working on `main` in all three repositories.

This is the single work order that replaces reading the 19 documentation commits pushed by ChatGPT Work and Codex between 2026-11-09 and 2026-11-11 one by one. It records Claude's preliminary assessment of every proposal, the owner decisions it still needs, and an ordered, testable implementation plan. It is a temporary handover: the last step of the plan removes it with the others.

**Authorization boundary.** Nothing here is implemented yet. Work marked *owner decision* waits for Kamil's answer in the project thread. No paid step (paid APIs, video generation, Deep Research via API, rented GPU) without Kamil's explicit "tak". Repository rules in [AGENTS.md](../AGENTS.md#current-rules-consolidated-2026-10-24) and Toolbox `CLAUDE.md` apply unchanged: main only, no force push, rebase plus full checks before push, no deletion of shared-package paths, ledger entry and trailers on every commit.

## 1. What was delivered (inventory)

| Commits | Material | Kind |
| --- | --- | --- |
| 6877d5d, ff0b7be, 10b9dcc, f0a42c5, 8ee1e06, 264c38b, 018da66, 2ec907e, ae19cde, 2942af9, ee0bae6, 46f37c1, 4611c9c, de4c70f | [Crème de la Crème handover](handover-creme-de-la-creme-2026-11-09.md), sections 1–14 | Research queue (9 repos), Motion Graphics task, workspace assessment, case studies |
| 6179d81, ff0b7be, 10b9dcc, 1eea5dd | [Map companion handover](handover-map-motion-companion-2026-11-09.md) + Astra map pack | Proposal for a separate map plugin; Lemo-Opuscar Toolbox review |
| 264c38b | `source-packs/11-free-video-effects/` | 11 Remotion effect briefs, author/licence unknown |
| ae19cde, 2942af9, a0375f5, 869ef9a | `source-packs/claude-token-efficiency-2026-11-10/`, `billion-context-2026-11-11/`, `anthropic-workspace-2026-11-11/` | Account-wide Claude workspace assessment |
| a0375f5 | [FrameCut/FrameMotion handover](handover-framecut-framemotion-2026-11-11.md) + `source-packs/framecut-framemotion-2026-11-11/` | 58 decision cards, 18 worked studies, launch proposals |
| 869ef9a, 0924a09 | [Deep Research handover](handover-deep-research-2026-11-11.md) + `dr-01`…`dr-06` packs | DR-01 motion, DR-02 editing, DR-03 motion resources, DR-04 Open Assets providers, DR-06 YouTube series (DR-05 = duplicate) |

Older handovers still in the tree: `handover-claude-code-2026-10-27.md`, `audit-repairs-and-handover-2026-10-24.md`. All shared-package files are unchanged since 1.174.1; every commit was documentation only.

## 2. Assessment of every proposal

Status words: **WDROŻYĆ** (implement), **ZMIENIĆ** (implement in a narrower or different form), **ODŁOŻYĆ** (defer, keep the decision), **ODRZUCIĆ** (reject, record why). "Source check" names what Claude re-read at the upstream on 2026-11-11; everything else relies on the handover text and stays to be verified by the receiver.

### 2.1 Studio knowledge and Motion Graphics

| # | Proposal | Verdict | Reason (project rules) |
| --- | --- | --- | --- |
| K1 | DR-01, DR-02 and the craft packet: conditional craft decisions for motion and editing (path vs timing, alpha/colour order, room tone, trims, conform, captions) | **ZMIENIĆ** | Valuable, but written for a future FrameMotion/FrameCut repository that does not exist. Absorb only corrections and missing decisions into the existing owners (`motion-craft.md`, `after-effects-craft.md`, `editor-craft.md`, `editor-handoff.md`). No new contracts/, adapters/ or repo. |
| K2 | Review correction SR-01: compose the complete scene per subframe before temporal integration (motion blur) | **WDROŻYĆ** | Concrete correctness rule; check whether `motion-craft.md`/motion-quality code assumes the opposite. |
| K3 | Review correction R01: FrameCut withholds EDL/OTIO for the whole complex sequence rather than exporting a supported subset | **WDROŻYĆ after verification** | Check the actual exporter (`fc_core.py`, `fc_render.py`, `framecut.py` mention EDL/OTIO). If it silently exports a subset today, this is a real defect fix with a regression test. |
| K4 | Exact-copy contract for Polish diacritics: NFC/NFD, grapheme clusters, font glyph preflight, "Zażółć gęślą jaźń." fixture (DR-01 P0-3, DR-03 P0-01) | **WDROŻYĆ** | Matches the owner's motion QA rules. `motion-review/acceptance.py` already normalizes NFC; add a missing-glyph/tofu and NFD fixture only where a gap is shown. |
| K5 | Rational FPS and seek determinism checks (0,100,20,100 sequence; 30000/1001) | **ZMIENIĆ** | Add as tests to existing motion-quality/FrameCut code if not covered; no new `core/time.*` module. |
| K6 | Review-termination policy (max two creative review rounds, technical failure never waived) | **ODŁOŻYĆ to Kamil** | Changes existing review rules (owner's QA standard). Present as a proposal; do not change `output-critic-iteration` without "tak". |
| K7 | Launch-capability matrix and FrameCut/FrameMotion extraction architecture (PLAN, DESIGN, LAUNCH-DECISIONS) | **ODŁOŻYĆ** | Kamil 2026-11-08: separate plugins are planning only until he says "startujemy". Preserve the decisions in `docs/roadmap.md`; build nothing. |
| K8 | YouTube/VideoLyrics scope and DR-06 (episode sidecar, series bible, pilot formats) | **ODŁOŻYĆ** | No full viewing/listening was done (0 complete films), FrameMotion repo absent. Keep the one durable lesson (separate "what code produces" from "strength of evidence") and the sidecar idea in roadmap. |
| K9 | DR-03 motion resources (30 candidates): small helpers (seeded `noiseAt`, settled-capture policy, static bloom/outline/CRT whitelist) | **ZMIENIĆ** | Only P0-02 (live-clock negative fixture) and P0-05 (seeded noise helper spec) fit current owners; the rest waits for real need. No new dependencies or Toolbox entries. |
| M1 | Ultra Skills: implement 30 motion effects (section 9, owner-authorized implementation task) | **ZMIENIĆ** | The full 30 prompts are behind a paywall; licence unknown. Implement only from what is legally accessible: original recipes inspired by the 11-free set. |
| M2 | 11-free-video-effects: Frame Break, Headlines, one shared device component (Orbit + Phone Screens) | **WDROŻYĆ** | Atlas already covers dolly-zoom, zoom-through, shatter, ui-scroll, bar-grow, camera-orbit, crane-tilt, terminal-run, typewriter, stamp-impact (checked). These three are the real composition gaps. Original code only, no copied prompts. |
| M3 | Higgsfield: reference-guided 3D reconstruction in code | **ODŁOŻYĆ** | Conflicts with the recorded guard "never draw realistic objects or hands in code" (`generated-motion-assets.md`). A pilot needs GPU time and a reference image; decision for Kamil. At most one note: stylized environments only, guard stays. |
| M4 | Generative Icons / useAnimations (decision delegated to Claude) | **ZMIENIĆ: knowledge only** | Decision: no Toolbox entry, no dependency, no A/B test now. Add 3–4 sentences to the existing Lottie card in `motion-toolkit-runtime-cards.md`: a matching family of many icons may come from Generative Icons (MIT, source check: LICENSE MIT at `1cc0ad0`) as raw dotLottie with explicit frame selection; simple accents are authored directly; useAnimations is not a transparent overlay (opaque white cut-outs) and its React wrapper has no seek. |
| D1 | Design Canvas: style cards, palettes, comparison boards | **ODRZUCIĆ** | Source check: no LICENSE file at `51a367d` (404). Studio already has the 200-code graphic catalogue, brand kit and DESIGN.md. Nothing copyable; no gap shown. |
| C1 | Cinematic Director: material-specific product lighting (glossy, transparent, matte) and symptom → cause → repair | **WDROŻYĆ (small)** | MIT. Add only missing decisions to `cinematography` / `product-films.md` in original wording, if the comparison shows a gap. |
| C2 | Drama Skills: prop hand-off and script-event coverage checks | **ZMIENIĆ** | MIT. Add one check to existing storyboard/shot-sequence QA only if Studio misses a deliberate prop-continuity error. No second orchestrator. |
| C3 | Claude AI Music Skills: mono-fold/phase and lyric-pronunciation readiness | **ZMIENIĆ** | CC0. One line in audio workbook or Earshot docs if absent. Reject its universal "-14 LUFS everywhere". |
| C4 | ElevenLabs Skills: text normalization, chunk seams, dubbing checks | **ODŁOŻYĆ** | Requires API key; Voice Narration companion owns voice. Knowledge note only if a real defect appears. |
| C5 | Vork knowledge (rational clocks, structured warnings, render passes) | **ODRZUCIĆ as a source** | Custom non-open-source licence (source check: "vork Preview License… It is not open source"). Studio already has a master frame clock. Do not cite or adapt its text. |
| C6 | Cinecode knowledge (READY/renderFrame contract, per-shot rerender, QA scripts) | **ODŁOŻYĆ** | MIT, but 51 of its 58 styles come from Lemo, already adapted as Studio's 66-look film-style library. Compare only `qc.py`/`words_check.py` against motion-review if time allows. |

### 2.2 Toolbox (each entry follows Toolbox `CLAUDE.md`: owner names the repo, reject gate, review, owner "tak", isolated install test)

| # | Candidate | Verdict | Evidence |
| --- | --- | --- | --- |
| T1 | Shader Skills (`gokayfem/shader-skills` `a56e773`) | **Qualify → ADD proposal** | Source check: ships `.claude-plugin/plugin.json` and `marketplace.json`, MIT, v2.0.0, HEAD unchanged. Strongest new candidate. Needs a review, isolated install test and one rendered comparison for the improvement gate before Kamil's "tak". |
| T2 | TasteSkill update 2.1.5 → 2.5.1 (`f6b7657`) | **Review → owner decision** | Source check: 2.5.1 declares a Stop hook (`gate.mjs`, timeout 600 s) that runs node at session stop and writes `.taste-skill/` files. Hooks that change what Claude does need Kamil's explicit approval. Keep 2.1.5 until then. |
| T3 | Lemo-Opuscar (re-review) | **Re-review** | Source check: HEAD moved to `9eb7739`; it now installs as `claude plugin install lemo-opuscar@lemolab`, but README still says "the agent installs the rest" and writes `~/lemo-opuscar`. Check unpinned dependency installs against the reject gate before any verdict. |
| T4 | Cinecode (`67f9807`) | **ODRZUCIĆ (NO ADD)** | Source check: README installs by `git clone` of a moving branch into `~/.claude/skills`; SKILL.md declares UserPromptSubmit, Stop and PreToolUse hooks that search the home directory. Fails the reject gate. Record a review with `Status: rejected`. |
| T5 | Vork | **ODRZUCIĆ (NO ADD)** | No SKILL.md or plugin manifest, needs Vulkan/Metal GPU, non-open licence; HEAD moved to `011e3f1` since the reviewed pin. Fails eligibility and self-contained rules. |
| T6 | ComfyUI MCP, Seedance, WebGPU skill, Claude Animated Shorts, Remotion Skills, HyperFrames | **ODRZUCIĆ** (already excluded by the screening) | Keep the screening decisions; record them in `repo-reviews-rejected` memory, not in Toolbox. |
| T7 | Generative Icons, useAnimations | **NO ADD** | See M4. |

### 2.3 Open Assets

| # | Proposal | Verdict | Reason |
| --- | --- | --- | --- |
| O1 | DR-04: NASA audio inside the existing NASA adapter (smallest scope) | **WDROŻYĆ (P2, owner decision)** | Fits the existing contract and licence policy; max 3 results / 6 metadata GET / ≤5 MiB per the DR-04 test scope. |
| O2 | Iconify (SVG) and Fontsource (fonts) as new asset types | **ODŁOŻYĆ** | Needs new formats and rights policy (OFL/RFN, per-icon notices). Not stabilization work. |
| O3 | Archive.org subcollections, multi-creator music, stock alpha video | **ODŁOŻYĆ** | Rights per item unresolved in the research itself. |

### 2.4 Separate tracks (not this repository package)

| # | Proposal | Verdict | Reason |
| --- | --- | --- | --- |
| W1 | Account-wide Claude token-efficiency policy, Grill Me, Agent Browser, Find Skills, Lance Martin talk | **WDROŻYĆ FIRST (Phase W)** | Kamil 2026-11-11 made this the first task of the package: review and propose token saving and management across his Claude workspace, locally on the Mac and in the cloud, with no loss for creative work. Personal configuration stays out of the public repo. |
| W2 | billion-context | **ODRZUCIĆ** | Rewrites Claude Code settings, disables native auto-compaction, auto-updates by default, MIT plus mandatory attribution clause, HEAD already moved to `c26c31a`. Too intrusive for a measured gain. |
| W3 | Anthropic repos (claude-plugins-official, knowledge-work-plugins, skills) | **Part of Phase W** | Shortlist belongs to W1. Many are already installed in Kamil's sessions (superpowers, plugin-dev, design, marketing). |
| W4 | Marketing Psychology, Chief of Staff skills | **ODŁOŻYĆ** | Source repositories unidentified; do not substitute same-named skills. |
| P1 | Map companion plugin (vector reveal, route, aerial; worldwide data) | **ODŁOŻYĆ to Kamil** | A new plugin is a big step during stabilization. If Kamil starts it, it gets its own thread: research report first (providers, rights), no implementation in this package. The Astra/Warsaw prototype is one option, not the architecture. |

## 3. Owner decisions needed before or during the work

1. **Scope of this package** (decided order: Phase W workspace token saving first, then A–D; the map plugin and FrameMotion/FrameCut split stay outside).
2. **Cleanup of temporary material.** The roadmap's owner instruction (2026-11-10) authorizes removing all development handovers and source packs once their decisions are preserved. Recommendation: first copy the DR-01…DR-06 and craft packs to the Mac knowledge mirror (`framecore-studio-wiedza/research/`), then delete from the tree; Git history keeps everything.
3. **TasteSkill 2.5.1 Stop hook:** approve the update or keep 2.1.5.
4. **Shader Skills:** "tak" for the isolated install test and one comparison render (free, local), then a separate "tak" for admission.
5. **Review rounds policy (K6):** adopt "max two creative rounds, technical failures never waived" or keep current rules.
6. **Higgsfield pilot and map plugin:** defer (recommended) or start in separate threads.
7. **Open Assets NASA audio (O1):** include in this package or defer.

## 4. Implementation plan for Fable 5.2

Work one repository and one phase at a time. Each phase is its own commit (or release) on `main` after the checks in section 5.

### Phase 0: intake guard (no commit)

1. `git fetch origin main --tags` in all three repositories; compare heads with the baselines above. Read AGENTS.md, CLAUDE.md, `docs/roadmap.md`, newest ledger entries, project memory `MEMORY.md`.
2. **Mandatory independent re-analysis of the original handovers (owner requirement, Kamil 2026-11-11).** Before any implementation, read again in full, at the source in this repository: every original handover listed in section 1 (`handover-creme-de-la-creme-2026-11-09.md`, `handover-map-motion-companion-2026-11-09.md`, `handover-framecut-framemotion-2026-11-11.md`, `handover-deep-research-2026-11-11.md`, `handover-claude-code-2026-10-27.md`, `audit-repairs-and-handover-2026-10-24.md`) and their supporting packs in `docs/source-packs/` (each DR packet's README/REPORT, IMPLEMENTATION_HANDOFF, REVIEW; the craft packet's PLAN, DESIGN, LAUNCH-DECISIONS, decision cards; the 11-free, Astra map, token-efficiency, billion-context and Anthropic intakes). Re-check decisive upstream claims at the upstream repository itself (tree, SKILL.md, `.claude-plugin`, licence, hooks), not from report text. Section 2 of this file is Claude Opus 5.5's **preliminary** assessment: confirm, correct or overturn each verdict with evidence, add anything it missed, and present the resulting table to Kamil in Polish before Phase A. Do not delete any original handover or pack until this re-analysis is done and its decisions are preserved (Phase D).
3. Re-check Kamil's answers to section 3 in the project thread. Skip phases he declined.
4. Measure budgets before any skill edit: `workflow-orchestrator/SKILL.md` is **31,994 / 32,000 bytes** at baseline, so this package must not touch it; total skill descriptions ≤ 7,800 characters (validator already warns about the budget).

### Phase W (first, owner priority 2026-11-11): token saving and management in the Claude workspace

Kamil's words: first of all review the implementation proposals for the Claude workspace, locally on the Mac and in the cloud: ways to save and manage tokens, **without any loss for creative work**. This phase runs right after Phase 0 and before Phases A–E.

Read in full: Crème handover section 11 (all subsections), `source-packs/claude-token-efficiency-2026-11-10/` (complete Polish report), `source-packs/billion-context-2026-11-11/REVIEW.md`, `source-packs/anthropic-workspace-2026-11-11/REVIEW.md`, Cinecode's context-protocol material listed in section 12 B, and the owner's existing standing rules (project instructions, `~/.claude/CLAUDE.md` on the Mac, account preferences "OSZCZĘDZANIE TOKENÓW").

1. **Inventory, two surfaces separately.** Mac (Claude desktop Code/Cowork, local CLI, `~/.claude/` user instructions, settings, enabled plugins/skills, hooks, MCP servers, plugin count loaded per session) via the approved Mac folders or Remote Control; cloud (Claude Code cloud environment, setup script, project instructions, project memory, MCP connectors). Note what is account-wide, project-only, machine-only or session-only. Read bounded excerpts; never copy secrets, conversations or client data into a repo.
2. **Diagnose real waste** with evidence: duplicated instructions across account/project/CLAUDE.md/memory, always-loaded large files, many enabled plugins and MCP servers whose tool lists load every session, repeated full test suites, verbose tool output, repeated full-file reads, oversized memory files.
3. **Propose, do not apply yet:** a short common policy text, exact per-surface changes (which plugins/MCP to disable per project, what to move from always-loaded instructions into on-demand skills/references, test-rerun rules), and decisions on candidates: native features first; ccusage, Context Mode, QMD, RTK, Serena/LSP, Grill Me, Agent Browser, Find Skills, Anthropic repo items as optional; billion-context, Claude-Mem, Caveman rejected or cautionary (see W2). No compressors stacked, no hidden model or effort downgrade.
4. **Creative-quality guard (hard rule):** never shorten or compress briefs, exact copy, full prompts, references, camera/light/motion/timing, sound or visual QA (frames every 0.5 s, safe areas). Savings come from technical noise and duplication only. Any change that touches creative routing needs a before/after on the same creative task.
5. **Measure before claiming:** one small pilot, one change at a time, same task/model/effort; record tokens where the host exposes them (`/cost`, `/context`, usage page), retries, time and output quality. No percentage promised in advance; no paid benchmark without Kamil's "tak".
6. **Present to Kamil in Polish** step by step: what Fable can change itself (repo files, cloud setup script, Mac files in approved folders) and what Kamil must click (account settings, connectors). Apply only after his "tak". Save the approved personal configuration to the Mac (`/Volumes/Codex&Claude/Claude/srodowisko/`) and project memory, not to the public repository; give rollback steps.

### Phase A: knowledge corrections in existing owners (Studio patch or minor release)

Files (all existing): `skills/hyperframes-workflow/references/motion-craft.md`, `after-effects-craft.md`, `motion-toolkit-runtime-cards.md`, `product-films.md`; `skills/opencut-video-studio/references/editor-craft.md`, `editor-handoff.md`; `skills/cinematography/…` reference that owns light; storyboard/shot-sequence QA reference; audio workbook reference.

1. K2: add the "compose the whole scene per subframe, then integrate" rule with its two-sample counterexample in original wording.
2. K3: read the EDL/OTIO export code. If a complex sequence exports a partial subset silently, change it to refuse with an explicit reason and add a regression test (red first, then green). If it already refuses, record "already covered".
3. K4/K5: add missing fixtures to existing tests: NFD input, missing glyph → BLOCKED, seek order 0,100,20,100 equality, 240 frames at 30000/1001 = 8.008 s. Only where the current suite lacks them.
4. K1: compare DR-01/DR-02 cards with `motion-craft.md`/`editor-craft.md`; add only conditional decisions with their counterexample, replacing any universal timing, LUT or room-tone rule that the research shows is wrong. Keep the owner's motion style rules (1–1.5 s holds, push-in and hold, white + Oxanium) untouched.
5. M4, C1, C2, C3: the short notes listed in section 2.1, each with a one-line source attribution (MIT/CC0) and no copied text.
6. Maintenance-mode trigger in ledger and commit: "bounded task opened by the owner (research intake 2026-11-11)"; show each case before and after.

Release rules apply because the shared package changes: synchronize the three plugin manifests, root marketplace version, version markers, `python3 scripts/build_install_manifest.py`, `python3 scripts/package_release.py`, CHANGELOG entry.

### Phase B: three motion recipes (Studio minor release)

Owner-authorized under section 9 of the Crème handover and the 2026-11-07 Motion Graphics exception.

1. Frame Break (character crosses the poster frame; mask, front/back occlusion, tiles), Headlines (perspective wall, columns in opposite directions, reading holds), and one device component shared by Orbit and Phone Screens.
2. Add them to the existing technique atlas and brief index of `hyperframes-workflow`, in HyperFrames first (Studio's main route), with editable copy, palette, fonts, timings, easing, dimensions and seed; state derived from the frame clock.
3. Evidence per recipe: one 1080×1920 render and, if relevant, a separately composed 1920×1080; frames every 0.5 s across the whole timeline; text visible, unclipped, inside safe area (9:16: top 10 %, bottom 20 %), readable long enough; first/last frame, backward seek, measured duration/FPS/dimensions with ffprobe. Report what was checked. Sound: NOT_RUN unless added.
4. Do not reproduce Ultra Skills prompts or the 11-free text; credit the sources by link in the ledger only.

### Phase C: Toolbox (Toolbox repository, separate commits)

1. T4 and T5: write `reviews/cinecode.md` and `reviews/vork.md` from `reviews/TEMPLATE.md` with `Status: rejected` and the one-line reason; no manifest change. Run the Toolbox checks.
2. T1 (after Kamil's "tak"): clone Shader Skills at `a56e773` into a temporary folder, review as data, write the review with the Improvement evidence table, run the isolated install test from Toolbox `CLAUDE.md`, render one original procedural scene with and without it. Add the entry only after a second "tak".
3. T2: write the delta review of TasteSkill 2.5.1 (Stop hook, `gate.mjs`, written files, network); ask Kamil; update the pin only after "tak".
4. T3: Lemo re-review at the current HEAD; verdict ADD / CONDITIONAL / NO ADD with the reject-gate reason.

### Phase D: preserve decisions and clean up (Studio, documentation commit)

1. Write the durable outcomes into maintained places: `docs/roadmap.md` (decisions K6–K9, M3, P1, W1, with dates and reasons; FrameMotion/FrameCut and map plugin as planning items), Toolbox reviews, project memory (`repo-reviews-rejected`, `MEMORY.md` STAN after any release).
2. If Kamil approved decision 2, copy the research packs to the Mac mirror first and verify md5.
3. Delete from the tree: all `docs/handover-*.md` development handovers (including this file, `handover-claude-code-2026-10-27.md`, after moving any active audit finding out of `audit-repairs-and-handover-2026-10-24.md`), and all `docs/source-packs/*` listed in section 1. Keep `verification/*.json` receipts, shared-package handoff templates and anything named "handoff" inside `plugins/`.
4. Fix incoming links: `grep -rn "handover-\|source-packs/" docs AGENTS.md CLAUDE.md README.md verification` must return only commit-pinned history links. Update the roadmap's "Temporary handovers" section to say the cleanup is done and where the plan lives.

### Phase E (only if Kamil approves): Open Assets O1

NASA audio inside the existing NASA adapter of `framecore-open-assets`, with the DR-04 limits (≤3 results, ≤6 metadata GET, ≤5 MiB, licence per asset, stop on 401/403/429). Then update Studio's Open Assets pin.

## 5. Checks before every push

Studio:

```bash
node plugins/framecore-work-creative-studio/scripts/validate-studio.mjs
mkdir -p "$HOME/tmp-checks" && TMPDIR="$HOME/tmp-checks" OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 bash scripts/check_all.sh
```

Codex sessions recorded that `/tmp` below 2 GiB breaks `framecut_development_test.py` and that multithreaded audio maths can stall; the environment line above avoids both. Use `bash scripts/check_all.sh --fast` while editing, the full run once before push. Release: the steps in AGENTS.md "Verification and publication".

Toolbox: the five commands in its `CLAUDE.md` ("Checks before every commit") plus the isolated install test for a new or updated entry.

Then `git fetch origin main`, `git rebase origin/main`, rerun the failed or affected checks, `git push origin HEAD:main`. Finish with `git ls-remote --heads origin` and report anything beyond `main` and `gh-pages`.

## 6. Risks

- **Scope creep.** The packets propose a whole FrameMotion/FrameCut product. The project is in stabilization; only Phases A–B change Studio behaviour. Anything else needs Kamil's words.
- **Budgets.** `workflow-orchestrator/SKILL.md` has 6 bytes left. New routing text goes into references, never into that file or new skills.
- **Licences.** Vork (non-open), Design Canvas (no licence), 11-free (unknown), Ultra Skills (gated) must not be copied. Only MIT/Apache/BSD/CC0 ideas in original wording.
- **Evidence.** The research has zero complete viewings or listening sessions and no native NLE runs. Keep NOT_RUN; a passing validator is not a finished film. Behaviour changes are not "working in Work" until tested there.
- **Moving upstreams.** Vork, Lemo and billion-context moved after their reviews; re-pin before any Toolbox decision.
- **Concurrent sessions.** Codex may push docs; re-check the head before each commit and renumber CC IDs on rebase.

## 7. Provenance

Read at the source in this intake: every handover named in section 1, the FrameCut/FrameMotion LAUNCH-DECISIONS and REVIEW-STATUS, all five DR implementation handoffs, the 11-free assessment, the Anthropic intake headings, the ledger entries CW-20261110-03 … CX-20261111-03 and the roadmap diff. Upstream spot checks on 2026-11-11 (HEADs via `git ls-remote`, files via raw GitHub): Vork LICENSE, Cinecode README and SKILL hooks, Design Canvas LICENSE absence, TasteSkill 2.5.1 Stop hook, Shader Skills manifests and licence, Lemo README install, Generative Icons LICENSE. Not read in full: the 74,000 lines of research data (catalog JSON, ledgers, cards), the token-efficiency report body, DR-06 catalog. No upstream code was executed, nothing installed, no paid call.
