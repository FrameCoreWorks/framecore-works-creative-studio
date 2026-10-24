# ElevenLabs through the app's connector

Use this when the user chose ElevenLabs, or when local engines are advised against (a phone app or a cloud session).
The connector runs under the user's own ElevenLabs account; every generation spends their credits. No API key is
asked for, stored or passed to a script.

1. **Check the connector.** If the host's tool list has no ElevenLabs tools (`creative_generate_speech`,
   `creative_list_voices`), say the connector is not connected and offer the script with voice direction instead.
2. **Pick a voice.** Call `creative_list_voices` with the user's own words about the speaker, the language (`pl`
   for Polish) and the use (`advertisement`, `narrative_story`). Pick one and say which; a voice id only ever comes
   from that tool or the user.
3. **One flow per project.** Call `creative_create_flow` once and pass its `flow_id` to every line, so the takes stay
   together and can feed later steps.
4. **Price, then ask.** Call `creative_generate_speech` with `estimate_only: true` for the whole script, tell the user
   the credit cost and the number of takes per line (two by default), and generate only after their yes.
5. **Generate each line** with the text after the lexicon (apply the project's `lexicon.json` the same way the
   launcher does: whole words, case-insensitive), the chosen `voice_id` and the default model unless the user asks
   for another. Poll `creative_get_flow_run_status` with the returned `flow_id` and `session_ids`, waiting the
   suggested interval, until all are completed or one failed. Never call generate again to retry: a second call is
   a second charge. Report a failure and let the user decide.
6. **Bring the chosen take home.** When the host can save files, save each line's chosen take as `<out>/<id>.wav`
   (convert to 16-bit PCM WAV with FFmpeg when it arrives in another format), add the line to `narration.lock.json`
   with `engine: elevenlabs`, the model, the voice id and name, and run `measure`. When the host cannot save files,
   say that the takes stay in the ElevenLabs flow (give its link) and that their length was not measured.
7. **Optional transcription check** with `creative_transcribe_audio` only after the user agrees to upload the takes
   and spend the credits.
