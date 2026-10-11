# Animate voice-over timing in Polish and other languages

The [Animate engine](../../references/animate-engine.md) is bundled byte for byte from its source, and its voice tool (`tools/voice.mjs` with `tools/voice_words.py`) recognises English only: it loads the `small.en` model, asks for English, and matches words after dropping every letter outside a–z, so ą, ę, ł, ó, ś, ź and ż never match. For a Polish voice-over, keep the engine's own tool for the lines and the audio, then let [`retime.py`](retime.py) set the word times:

```bash
node tools/voice.mjs pieces/<name>                              # lines placed, voice/voice.wav written (engine)
python3 retime.py pieces/<name> --language pl                   # Polish word times into voice.json
node tools/build.mjs pieces/<name>                              # rebuild so VOICE carries the new times (engine)
```

| Source of the times | When | Command |
| --- | --- | --- |
| Times you already have | the text-to-speech service returned word or character timings, or a transcript tool did | `--heard words.json` with `[{w, t0, t1}]` (or `word`/`text`, `start`/`end`) in seconds on the `voice.wav` timeline |
| Local recognition | Python with `faster-whisper` installed | default; `--model small` (multilingual; never a `.en` model for Polish) |
| Estimate | no recogniser, or `--estimate` | each line's time spread over its words by syllables, with a pause after commas and full stops; one-letter words (w, z) and numbers are weighted like speech |

Matching keeps every letter, so a recognised word lands on the script's word; a word the recogniser missed or misheard (rz for ż) is placed between its matched neighbours and keeps `"est": true`. Line times never change, only the words inside them. `voice.json` records `wordTiming` (language, source, matched words); report estimated times as estimated, and look at the cues on the contact sheet before calling them in sync.

Exit codes: 0 written; 2 no `voice.json` with lines (run `tools/voice.mjs` first) or an unreadable `--heard` file.
