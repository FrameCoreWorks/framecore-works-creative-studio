# Improvement plan, October 2026

Based on a full audit of package 1.54.0 on 2026-10-10: six independent read-only reviews (entry and orchestration, static and visual, video and story, motion graphics, copy/marketing/audio/research/delivery, infrastructure), each scoring client readiness 1–5 with file-level evidence. The owner uses Studio daily for paid client work; the plan orders work by its effect on client-ready output and on the speed of safe improvement. Ratings are judgments from source reading plus container runs; no case has been executed in a host.

## Progress

| Items | State | Release |
| --- | --- | --- |
| 0.1 to 0.5, 0.7, 0.8 | done | 1.55.0 |
| 0.6 | description budget done; orchestrator headroom still open (31,986 of 32,000 bytes after 1.56.0), moved to Phase 5.3 | 1.55.0 |
| 0.9 | done: harness, 15-case suite, first run on 1.55.0 (12 of 15, all three failures resolved), [results](host-evals.md) | 1.56.0 (repository) |
| 1.1 to 1.7 | done: fonts and exact-copy compositor, presets, image probe, Polish copy standard and checker, channel and marketing-rules snapshots, claim-ledger rules column, direct production | 1.56.0 |
| Phase 2 | next | |

## Diagnosis

| Theme | Finding | Evidence |
| --- | --- | --- |
| No real-output evidence | 204 planned evaluation cases, 0 executed; no runner; some specs already stale (LM01 expects a two-option welcome) | `P/scripts/validate-studio.mjs:393,420`; `P/evals/learning-mode-cases.json:36` |
| Static work under-invested | The owner's main domain stops at a prompt or one generated raster: no exact Polish copy, logo and price over an image, no print PDF, no vector logo, no platform or print presets, no measuring tool | capability card has no static capability; `text-image-generation-policy.md:9,19`; `deliverable-profiles.md:16` |
| Polish language and market missing | No rules or checks for „” quotes, en dash, non-breaking spaces, one-letter words at line ends, Ty/Pan register, brand declension; no channel character limits; no Omnibus, RODO or Allegro coverage | copy-voice `human-voice.md:51`; `campaign-production.md:25` |
| No client business layer | Nothing for quotes, offers, intake forms, revision rounds, change orders, concept presentation, licence scope (pola eksploatacji), acceptance protocol, client emails, case studies | package-wide search |
| Motion gates miss the owner's known failures | The Python renderer crops overflowing words silently; critique scores an empty 9:16 frame 100; acceptance drops readability errors; a 13 s sound mix takes 2.5 min (a 1-second moving average done by direct convolution) | `render.py:396`; `critique.py:322,349`; `acceptance.py:113,141,154`; `music.py:507` |
| Motion looks templated | Seven scene kinds, system fonts, short-side type scale (empty vertical frames), fade-out/fade-in resets, no lower thirds, charts, photo hero or brand kit | `render.py:64-73`; `motion-styles/styles.json` |
| Video skills produce memos, not deliverables | No Studio-run tool in the group; contradictory hook timing; no speech-rate budgets; no generator dialect cards; no storyboard PDF, shot list XLSX, AV script, treatment or creator brief with usage rights | capability card; `campaign-direction-method.md:89` vs `ugc/.../formats-scripts-and-disclosure.md:41` |
| Routing and token cost | Orchestrator entry at 31,979 of 32,000 bytes; two route tables; 37 descriptions at 7,696 of about 8,000 characters with no total check; English-only triggers; 55–75 KB of policy before craft; stale two-option text in three files | `workflow-orchestrator/SKILL.md`; `studio-integration-policy.md:26` |
| Slow, error-prone releases | About 18 hand edits and a second records commit per release; no `--fast` test tier; no CI guard against unbumped package changes; a legacy suite with 134 known errors still gates releases | ledger; `.github/workflows/` |

## Phases

Each phase ships as one or more releases with the full checks. Effort: S under half a day, M one to two days, L more.

### Phase 0. Foundation and quick fixes (first)

| # | Change | Files | Effort |
| --- | --- | --- | --- |
| 0.1 | Fix the sound mix speed: cumulative-sum moving average; audit the other convolutions | `hyperframes-workflow/assets/motion-sound/music.py` | S |
| 0.2 | Renderer fails on any overflowing or cropped word; balanced wrapping without Polish one-letter orphans; optional fit-to-width | `motion-render/render.py` | S–M |
| 0.3 | Critique sees emptiness: content fill ratio and headline size per format, thumbnail check on every vertical format; acceptance blocks on any critique error and requires an evidence file for human flags; replace the "good" reference | `motion-review/critique.py`, `acceptance.py`, tests | S |
| 0.4 | Remove stale two-option welcome text; fix LM01; validator assertion | `studio-integration-policy.md:26`, `intake-and-reference-authority.md:9`, orchestrator description, `evals/learning-mode-cases.json` | S |
| 0.5 | Fix contradictions: marketing description vs body; product-film "mandatory research"; CHATGPT_UPDATE readback section and "preserve private provider preferences" vs `provider-setup.md:27` | named files | S |
| 0.6 | Validator: total description budget (warn 7,500, fail 7,800); orchestrator headroom target 29,000 bytes by moving version-reporting phrases to their reference | `validate-studio.mjs`, orchestrator | S–M |
| 0.7 | `scripts/release.py`: one command bumps every marker, regenerates inventory, runs and parses checks, writes scope/release/status/ledger records, packages, commits, pushes fast-forward, prints the Plugin Creator prompt | new | M |
| 0.8 | `check_all.sh --fast` (under one minute) for the edit loop; CI guard against package changes without a version bump; `claude plugin validate` in CI | `scripts/check_all.sh`, `.github/workflows/` | S |
| 0.9 | Host-eval harness: `scripts/host_eval.py` (headless `claude -p` with the plugin, deterministic checks plus an advisory judge), a 15-case starter suite, records under `verification/host-evals/`; runs need the owner's approval of the spend | new, outside the package | M |

### Phase 1. Static graphics and Polish quality

| # | Change | Files | Effort |
| --- | --- | --- | --- |
| 1.1 | Exact-copy production route (`static_render`): generated or supplied background plus exact Polish text in a bundled OFL font, real logo and price; PNG at exact size and PDF with optional bleed; text audit and contrast check; default for client finals with a price, logo or legal line | `static-graphic-design-creator/references/exact-copy-compositing.md`, `assets/static-render/`, capability card, `text-image-generation-policy.md` (two routes), `image-prompt-architect/SKILL.md:22` | L |
| 1.2 | Dated format and print presets: Instagram/Facebook/Meta placements, A-sizes, Polish print-shop defaults (3 mm bleed, FOGRA39/PSO Coated v3, 300 ppi effective), each labelled provisional with a check date | `static-graphic-design-creator/references/format-and-print-presets.md` | S |
| 1.3 | `image_probe.py`: ratio against presets, effective PPI, alpha, phone-size and greyscale previews, contrast, optional OCR diff against locked copy; wire `layer_assets.py inspect` | `output-critic-iteration/scripts/` | M |
| 1.4 | Polish copy standard plus a checker (quotes, dashes, non-breaking spaces, orphans, number/currency/date formats, Ty/Pan consistency), wired into copy review and static/motion text | `copy-voice/references/polish-copy-standard.md`, `scripts/pl_copy_check.py` | M |
| 1.5 | Dated channel copy specs (Meta, Google RSA, TikTok, LinkedIn, Allegro, SEO title/description, email subject/preheader), a character counter and a Copy Pack template; a fresh table satisfies the research gate in Quick mode | `copy-voice/references/channel-copy-specs.md`, `assets/copy-pack.template.md`, research-evidence trigger 2 | M |
| 1.6 | PL/EU compliance column in the claim ledger: Omnibus 30-day lowest price, UOKiK labelling, RODO and marketing consent, AI Act Art. 50, regulated categories; primary sources with check dates, counsel decides | `ecommerce-campaign-strategy-director/templates/…`, linked from copy-voice and marketing | M |
| 1.7 | Direct-production fast path: a complete brief gets one direction and the output in one turn; override the upstream activation and prompt-vs-render rules | `static-graphic-design-creator/SKILL.md` | S |

### Phase 2. Client business layer

| # | Change | Effort |
| --- | --- | --- |
| 2.1 | Offer and quote builder: packages (good/better/best), revision rounds, timeline, payment terms, licence scope, validity; `quote_calc.py` from the owner's own rates, VAT on/off, PLN breakdown, tested | L |
| 2.2 | Client intake form (PL/EN) and commercial fields in the Brief Contract (budget, deadline, approver, rounds, usage); change-order rule | S |
| 2.3 | Concept presentation pack: 2–3 directions with rationale, mockup in context, risk and a numbered decision request | M |
| 2.4 | Feedback consolidation and revision tracker: in-scope revision, bug or change order, round counter | M |
| 2.5 | Client handoff letter with licence scope and pola eksploatacji placeholders, protokół odbioru, AI-assistance disclosure line, file naming and folder convention | M |
| 2.6 | Client brand kit (`brand-kit.json` plus card): colours, fonts with licence, logo files, tone, banned claims, legal lines; read by static, copy, motion and video; host persistence guide (ChatGPT Projects/instructions, CLAUDE.md, AGENTS.md) | M |
| 2.7 | Client email kit in Polish, case-study write-up, campaign plan with KPIs and budget scenarios, brand voice guide | M |

### Phase 3. Premium motion

| # | Change | Effort |
| --- | --- | --- |
| 3.1 | Craft layer: bundled OFL display fonts, tracking and full weights, vertical-first type scale, device shadow and depth, per-word kinetic entries with springs, elements that persist across scenes, motion blur for finals, designed frame 0 | L |
| 3.2 | Commercial scene kinds: lower third, bar/line chart, photo hero with parallax, footage underlay, richer logo sting; three 9:16 ad templates (hook, proof, CTA); brand kit applied automatically; batch variants over copy × format × language | L |
| 3.3 | Social captions: bold active-word preset, consistent platform margins, clause-aware cues, Polish word timing in the Animate voice tool | M |
| 3.4 | Sound tonal balance: presence and air, low-mid control, phone-speaker check, mid/high transient layers on impacts | M |
| 3.5 | One host-first runtime map replacing three tables; retag the brief index and prompt library to scene kinds the Python renderer runs; rewrite the top 20 library records as runnable snippets; 4–6 commercial styles | M |
| 3.6 | Remotion GLTF product turntable template | L |

### Phase 4. Video and story deliverables

| # | Change | Effort |
| --- | --- | --- |
| 4.1 | One shared short-form timing card: hook windows per placement, Polish and English voice-over word budgets for 6/15/20/30/60 s, reading time, end-card hold; cited by every video and copy owner | M |
| 4.2 | Generator dialect cards (Veo, Kling, Seedance, Runway, MiniMax/Hailuo and the owner's tools), consumer surfaces in the snapshot, a refresh cadence, provisional use without browsing | M |
| 4.3 | Executable deliverables: storyboard compositor (PNG/PDF with exact labels), shot list and AV script export (XLSX/CSV/PDF), clip review contact sheet reusing `inspect-encode.py`, prompt-pack export, Python port of the plan checker | L |
| 4.4 | Client templates: AV two-column ad script, concept one-pager, music-video treatment, creator brief with usage, whitelisting and exclusivity, editor step lists (CapCut, Premiere, DaVinci) with EDL/OTIO export; a client-version rule that gathers assumptions in one box | M |
| 4.5 | Consolidate 11 video skills into 6 owners plus UGC, keeping the others as pointer stubs; Polish trigger terms; ad-script ownership | L |

### Phase 5. Routing, persistence and cost

| # | Change | Effort |
| --- | --- | --- |
| 5.1 | One route table with Polish and English triggers; resolve collisions (image prompt, product video entry points, supplied-video review, service businesses) | M |
| 5.2 | Routing evaluation set: 20–30 real Polish requests with and without the Studio name, run by the harness | M |
| 5.3 | Lighter governance payload: method catalog and GEPA out of runtime references, one Project State, research reuse of dated snapshots | M |
| 5.4 | Workflow self-improvement emits change requests as evaluation cases; retire Hipson to a pointer; instruction packets for human vendors (printer, voice talent, subcontractor) | S–M |
| 5.5 | Mascot and stylized character reference; logo craft with SVG wordmark route and brand guide PDF template | L |

## Decisions that belong to the owner

1. Phase order (default: 0, 1, 2, 3, 4, 5).
2. Spending on host-eval runs (estimated USD 2–4 per suite pass on a mid model, under 1 for the release gate subset).
3. Retiring the legacy suite with in-place stubs (AGENTS.md currently requires its baseline).
4. Inputs for the quote builder: rates, VAT status, typical packages.
5. Generators and editors used daily, for the dialect cards and tool routing.
6. Whether teaching means school classes, adult courses or both.

## Working rules

Every change keeps package paths (stubs, never deletions), keeps the protected welcome unless the owner asks, passes the canonical validator and the full suite, ships as a release on `main`, and is recorded in the ledger. ChatGPT Work is `not_tracked`; the owner updates and tests it himself.
