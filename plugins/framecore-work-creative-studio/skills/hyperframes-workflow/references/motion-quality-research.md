# Motion quality research, 2026-10-04

Evidence snapshot, not a model ranking. Public model attribution is normally the creator's claim. No paid model runs or controlled Claude versus OpenAI comparison were performed. No source videos are redistributed.

## Five useful viewing cases

| Case and viewing source | Observed value | Evidence boundary |
| --- | --- | --- |
| [15-second reel by Stephan Livera](https://x.com/stephanlivera/status/2103315922098470926), discovered through [Specimen & Signal](https://specimen-and-signal.vercel.app/) | Large type, limited palette, geometric chapter changes, repeated circular motif and held end card. | Thirty sampled frames across 15 seconds inspected. Author attribution to Opus 5.5; prompt credited to shneural. Not a full temporal/audio review. |
| [Grok Bot product film](https://www.reddit.com/r/vibecoding/comments/1wqb6yk/opus_55_created_me_a_30second_motion_graphics/) | Mascot division explains multiple roles, then tool use and overnight work; the ending has room to read. Small interface labels still need mobile inspection. | Thirty sampled frames inspected. Creator reports Opus 5.5, a revised 30-second cut after a too-fast 15-second version and corrected brand treatment. |
| [Everything Is Motion](https://www.reddit.com/r/ClaudeAI/comments/1wsup4y/motion_design_showreel_with_sonnet_55_on_par_with/) | Sampled browser scenes show scale changes, geometric tiling, reflective materials and emphatic type. | Selected browser frames at approximately 1, 26, 48 and 86 seconds inspected, not continuous whole-film or audio review. Sonnet 5.5 attribution and WebGL/WebAudio method are creator claims. |
| [Reddit motion reel](https://www.reddit.com/r/ClaudeCode/comments/1wtapu5/sonnet_55_built_a_30_s_motiongraphics_reel_same/) | Distinct chapters, community mosaic, ranking, thread graph and large word treatments; some scenes are visually crowded. | Thirty sampled frames inspected. Sonnet 5.5 author reports builders, reviewers and selective repairs. The headline cost comparison is not a paired model run. |
| [PROMPTOWY showreel](https://quantslant.com/claude-opus-5-5-motion-graphics/) | Consistent restrained palette, type scale, project cards and diagrams tied to actual project context. Small labels lose prominence at reduced viewing size. | Thirty frames sampled at two-second intervals. Creator reports prior brand/project memory and later variations. This is not a context-free one-shot experiment. |

These are a curated set for learning, not the world's five objectively best films. Frame samples establish visual observations; playback occurring in the browser does not establish that every frame or the audio was inspected.

A further technical reference is [mexicat's P(doom) renderer](https://github.com/mexicat/pdoom-video): a time-driven three.js lyric film, treatment, audio-analysis data, render commands and documented sampling tradeoffs. Read the separate rights for code, fonts, song and lyrics. Its [published video](https://www.youtube.com/watch?v=5EoO5413dBY) was located but not visually reviewed in this research.

## What the model evidence supports

Official announcements confirm [Opus 5.5](https://www.anthropic.com/claude-opus-5-5) and [Sonnet 5.5](https://www.anthropic.com/claude-sonnet-5-5). The announcements describe coding/design improvements and selected demonstrations. They do not isolate motion-design quality against GPT-6 Astra under equal prompts, assets, runtimes, budgets and review conditions.

[Claude Design](https://www.anthropic.com/news/claude-design-anthropic-labs) combines a model with brand context, editable controls and visual iteration. That suggests a useful workflow pattern, not a causal proof about model weights. Public information does not reveal enough training detail to attribute the difference to a particular dataset or training recipe.

[MotionBench methodology](https://motionbenchmark.com/methodology) is a draft and its September collection predates these 5.5 releases; the public set is unranked. [Contra's methodology](https://contralabs.com/research/methodology) offers useful blind practitioner review, but pooled results across studies are not a controlled motion comparison.

Working inference: stronger examples benefit from complete direction, useful context, persistent coding, shared timing, actual renders and selective repair. The model may contribute, but this research cannot quantify its independent share. Selection bias, hidden iteration, effort and tool access are confounders. Never claim this package equals or beats Claude without measured evidence.

## Why workflow is a credible part of the explanation

Anthropic's [frontend harness study](https://www.anthropic.com/engineering/harness-design-long-running-apps) describes generic defaults, overly generous self-evaluation and improvement from explicit design criteria plus an evaluator inspecting the actual interface. It also reports higher cost, diminishing returns and cases where a middle iteration was preferable to the last. This is evidence about an experimental frontend workflow, not a motion-model ranking. Studio adopts concrete criteria and bounded output review, not its expensive iteration counts or a new agent architecture.

Anthropic's [design skill discussion](https://claude.com/blog/improving-frontend-design-through-skills) and OpenAI's [frontend design guidance](https://developers.openai.com/blog/designing-delightful-frontends-with-gpt-5-4) both emphasize supplied design direction and context. The latter concerns an older model and web interfaces, so it cannot establish Astra's motion performance. Together they support improving the production instructions rather than attributing every visual difference to undocumented training data.

## Additional source libraries

- [Motion Graphics Prompt Bank](https://github.com/cindyxu1030/motion-graphics-prompt-bank): 57 prompts with GIFs, author-declared prompt/render pairs; CC BY-NC-SA 4.0. Link-only here because the commercial reuse restriction is incompatible with unrestricted Studio reuse.
- [Prompt-VFX](https://inthepond.github.io/prompt-vfx/) and [source](https://github.com/inthepond/prompt-vfx): 162 effects with prompt/build associations; no redistribution license confirmed. Reference only.
- [Li-Evan gallery](https://li-evan.github.io/awesome-opus-5.5-video-prompts/): curator reports 334 entries. [Rights](https://github.com/Li-Evan/awesome-opus-5.5-video-prompts#rights-and-takedown) distinguish curator CC BY material from third-party prompts/media.
- [Skillry gallery](https://skillry.dev/ai-videos/opus-5-5): curator reports 475 entries including remakes. [Source credits](https://github.com/yihui-dev/awesome-opus5-5-videos#credits) retain creators' prompt/media rights despite MIT code.
- [Remotion Prompt Showcase](https://www.remotion.dev/prompts): community prompt/render examples, including a [map route](https://www.remotion.dev/prompts/travel-route-on-map-with-3d-landmarks) and [headline treatment](https://www.remotion.dev/prompts/news-article-headline-highlight). No general redistribution permission confirmed.

Counts are dated discovery signals, overlap between catalogs is expected. Source pairing is not local reproduction. The bundled Specimen records preserve explicit permission and provenance in [SOURCE-NOTICE](../assets/motion-prompt-library/SOURCE-NOTICE.md).

## Tool decisions

Adopt optional [Paper Shaders](https://github.com/paper-design/shaders) material control and [Tone.js](https://github.com/Tonejs/Tone.js) offline sound cues. Paper 0.0.81 was reviewed at commit 43cd68db79fa0b1759f72ffc941b3238e2a3954c; Apache-2.0 applies from 0.0.77, older releases differ. Tone 15.1.22 is MIT. Adapters use injected installed libraries; no library source is vendored or installed.

Defer additional full engines: [Motion Canvas](https://github.com/motion-canvas/motion-canvas) overlaps current explainer routes; [Anime.js](https://github.com/juliangarnier/anime) overlaps GSAP; [Rive](https://github.com/rive-app/rive-wasm) needs a real .riv authoring workflow. Consider them only for a supplied project or a requirement the current toolkit cannot meet. More engines alone do not improve art direction.
