import pathlib,sys
def rep(path, old, new, count=1):
    p=pathlib.Path(path); t=p.read_text()
    n=t.count(old)
    if n!=count: sys.exit(f'{path}: expected {count} got {n}: {old[:70]!r}')
    p.write_text(t.replace(old,new))
S='skills/'
L=S+'pipeline-core/references/loop-protocol.md'
rep(L,"to the Motion Graphics Workflow (craft critique and frame review)","to the Motion Graphics Workflow (craft critique, frame review and [motion activity](../../hyperframes-workflow/assets/motion-quality/README.md#motion-activity))")
OC=S+'output-critic-iteration/SKILL.md'
rep(OC,"Do not load that craft for unrelated pure typography or abstract graphics, and do not mistake deliberate stylization for a defect.",
"Do not load that craft for unrelated pure typography or abstract graphics, and do not mistake deliberate stylization for a defect. Judge type, colour and layout against the shared [craft rules](../pipeline-core/references/craft-rules.md); for text contrast measure the colour pair with [`contrast_check.py`](../pipeline-core/assets/craft-lint/README.md) (the worst spot over an image is judged by eye), and for HTML, CSS or SVG run `craft_lint.py`.")
HF=S+'hyperframes-workflow/SKILL.md'
rep(HF,"Start from a starter when no project exists:","Start from a starter when no project exists: for a client reel in HyperFrames, a [reel starter](assets/reel-starters/README.md) whose job matches the brief;")
rep(HF,"make at least one improvement round when it finds anything","make at least one improvement round when it finds an error or warning")
rep(HF,"- **Illustrated or hand-made looks**","- **Choosing among the look routes below:** when several fit, choose by the deliverable and say why in one line: a real mechanism with true geometry goes to the Anatomy method above; isometric line art driven by sound to Iso Glow; a painter's look or an explainer channel's grammar to art-style direction (with the Animate engine as its renderer when a shell exists); a whole hand-made film with its own check-ins to the Animate engine.\n- **Illustrated or hand-made looks**")
rep(HF,"follows the shared [craft rules](../pipeline-core/references/craft-rules.md) (caps tracking, accent discipline, no default indigo or trust gradients); run [`craft_lint.py`](../pipeline-core/assets/craft-lint/README.md) on the composition HTML.",
"follows the type, colour and interface sections of the shared [craft rules](../pipeline-core/references/craft-rules.md) (caps tracking, accent discipline, no default indigo or trust gradients); timing and easing come from [motion craft](references/motion-craft.md). Run [`craft_lint.py`](../pipeline-core/assets/craft-lint/README.md) on the composition HTML; a brand colour the lint flags is allowed with `--allow` and noted in the review.")
rep(HF,"| Story, scene order or timed shot cards are unresolved |","| Narrative order is unresolved, or timed shot cards are needed for another owner (this skill's own storyboard stays in the motion contract) |")
rep(HF,"| Songs, lyrics, voice, external audio tools, licensed tracks or supplied audio review |","| Word timing of a supplied song's lyrics, beat grid and audio-reactive envelope | This skill, with [lyric timing](assets/motion-sync/README.md#lyric-timing), [`beats.py`](assets/motion-sync/README.md#analysing-a-supplied-track) and [`audio_envelope.py`](assets/motion-sync/audio_envelope.py) |\n| Music-video concept and song-to-image direction | [Creative Music Video Director](../creative-music-video-director/SKILL.md) |\n| Songs, lyrics, voice, external audio tools, licensed tracks or supplied audio review |")
CR=S+'hyperframes-workflow/references/claude-code-reels.md'
rep(CR,"3. **Build.** `npx hyperframes init <name>`,","3. **Build.** `npx hyperframes init <name>` (or copy a [reel starter](../assets/reel-starters/README.md) when its job fits the brief),")
CS=S+'caption-studio/SKILL.md'
rep(CS,"- Prefer segment-level subtitles for calm editorial work","- For a song, take word and line times from [lyric timing](../hyperframes-workflow/assets/motion-sync/README.md#lyric-timing) with the user's lyrics as the truth; it writes SRT and LRC and lists lines to check by ear.\n- Prefer segment-level subtitles for calm editorial work")
MV=S+'creative-music-video-director/SKILL.md'
rep(MV,"## Treatment\n","When the selected direction is a coded lyric video, beat-synced typography or an animation that reacts to the track (no camera footage), hand the approved treatment to the [Motion Graphics Workflow](../hyperframes-workflow/SKILL.md): it times the lyrics with [lyric timing](../hyperframes-workflow/assets/motion-sync/README.md#lyric-timing), cuts on the beat grid and drives audio-reactive parts with `audio_envelope.py`.\n\n## Treatment\n")
CL=S+'pipeline-core/assets/craft-lint/craft_lint.py'
rep(CL,"    if uses >= 6:\n        add('P1', 'accent-overuse'","    if uses >= 6 and not video:   # a video spreads the accent over many shots; review it per shot by eye\n        add('P1', 'accent-overuse'")
CRM=S+'pipeline-core/assets/craft-lint/README.md'
rep(CRM,"so `viewport-missing`, `full-height-section` and `fixed-width` are skipped there;","so `viewport-missing`, `full-height-section` and `fixed-width` are skipped there, and so is `accent-overuse`, since the accent rule is per shot and the markup holds every shot;")
