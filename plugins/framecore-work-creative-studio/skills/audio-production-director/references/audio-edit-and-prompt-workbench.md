# Audio, edit rhythm and provider prompt workbench

Use after the user chooses sound-to-picture or picture-to-sound, or when that direction is already clear from the task. Extend the [tempo workbook](audio-to-picture-and-tempo-workbook.md) rather than starting another intake. Current source cards are in [expansion evidence](../../research-evidence/references/reference-audio-expansion-sources.md). The timing examples below are arithmetic and original planning examples; no audio was heard to produce them.

## Separate the decisions

Keep story event, cut point, musical beat and sound onset distinct. They may coincide, but they do not have to. A picture can hold across a musical change; a new sound can announce the next scene before the image cut; silence can make a product contact legible. Determine which event deserves attention before filling the timeline with impacts.

For picture-first, carry the actual inspected intervals or supplied cut list, camera/action changes, protected VO and the target ending. For music-first, carry source track/version, inspected or user-supplied landmarks, pulse basis, phrase changes and usable excerpt boundaries. A target duration is not evidence of source tempo. Unknown tempo does not prevent a qualitative direction or a provisional cue map.

Use one timeline origin and state units. If converting frames, require the real timebase; frame n at a constant rate f occurs at n/f seconds from the chosen origin. Do not assume a nominal fps is sufficient for variable-frame-rate material or interpret timecode frames as decimal fractions. Keep source-file position separate from edit-relative time after trimming.

## Useful rhythm arithmetic with explicit assumptions

For a constant pulse at B beats per minute, one beat lasts 60/B seconds. If a bar has N of those beats, a bar lasts 60N/B. State the beat unit and meter before using a bar count; compound-meter pulse conventions can differ.

Example: a proposed quarter-note pulse at 120 BPM in 4/4 gives 0.5 seconds per beat and 2 seconds per bar. A 25-second target spans 50 beats, or 12.5 bars. It does not require 50 cuts. Decide whether the excerpt begins mid-phrase, ends with a designed cadence/tail, or leaves an intentional unresolved feeling. Do not describe this calculation as an analysis of an uploaded song. Tempo changes and performed drift require actual landmarks instead of one global formula.

## Give every sound layer a job

| Layer | Decision | Typical failure and repair |
|---|---|---|
| Music | Emotional movement, density and which moment earns a change | Generic constant intensity: alter arrangement around one meaningful event |
| Voice/dialogue | Exact wording, delivery and intelligibility priority | Music competes with speech: simplify the arrangement or adjust local level after listening |
| Foley/contact | Which visible touch or material movement is audible | Repeated stock whooshes: replace with a motivated sound or silence |
| Ambience | Place, continuity and acoustic space | Abrupt background jump: plan a continuous bed or an intentional change |
| Silence | What absence makes the viewer notice | Accidental dead gap: identify whether it serves the event before filling it |

Mark cue onset, sustain and tail separately when timing matters. A planned click at a visible contact is a target until the audio and picture are inspected together. Avoid promising sample-accurate synchronization from a text prompt. Speech timing comes from an actual performance or an explicitly estimated read, not only a word count.

## Compile for the selected destination

### Suno interface

Current official help distinguishes Custom lyrics, Styles and Instrumental controls. Put musical direction in the appropriate style field and preserve approved lyrics exactly in the lyrics field when that workflow is selected. Keep a director's cut map separate from sung text. Do not assume that second-by-second directions guarantee timed events or that website controls imply an available public API. If the user wants an instrumental, do not invent lyrics as scaffolding.

### Eleven Music API or website

The API documents prompt and composition-plan routes. Its compose endpoint makes those alternatives mutually exclusive; duration, instrumental and seed controls have mode-specific conditions. Verify the selected model and current schema before emitting executable JSON. The composition guide uses ordered chunks, but a provider-neutral Studio cue map is not itself that request schema. The website need not expose all API fields.

Translate approved cues into the supported structure, retaining exact text and distinguishing hard duration constraints from musical intent. A documented duration control is not evidence that a specific hit, word, cadence or perceived sync landed correctly. Keep licensing review separate from technical generation settings.

### Other user-selected providers

Preserve the sonic brief and research the exact current product/model/surface. Deliver a provider-neutral complete prompt if native syntax is unverified; name the gap. Do not substitute Suno or ElevenLabs controls for a Google or other provider. Use [provider routing and rights](music-provider-routing-and-rights.md) for entry points and asset-level rights checks.

## Handoff to editing

Use the [cue sheet](../assets/av-cue-sheet.template.json) and [music brief](../assets/music-brief.template.md) only to the detail needed. Separate music, VO/dialogue, Foley and ambience tracks when the chosen editor and actual assets permit it. Describe intended ducking as a mix decision, not a performed edit. Adobe's documented auto-ducking creates editable automation; regenerating those keyframes can overwrite manual adjustments. Preserve an existing edit before any authorized regeneration.

Do not prescribe universal LUFS, gain reduction, fades or limiter settings without the destination and actual signal. If the sound is wrong, identify the affected layer and time span, protect working sections, and request the smallest authorized repair. Keep master duration, VO words, product sound identity and licensed-source restrictions intact. Route temporal picture review to Video Prompt Architect, still-image review to Output Critic, and caption timing to Caption Studio with source evidence.
