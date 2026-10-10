# Host smoke set

Eight short checks of how an installed Studio behaves in a real host, for a larger release. Written 2026-10-08 from the full review (F-TEST-03, IM2). Source checks prove that files and rules exist; only these runs show whether a host follows them. About 20 to 30 minutes per client. The prompts are exact test inputs; the Polish ones stay in Polish.

## Before you start

1. Update the installed plugin to the release under test and note its version. Ask "Which Studio version is installed?" in a new chat if the client shows no version.
2. Note the client (ordinary ChatGPT, ChatGPT Work or Codex; app, browser or phone), the model if shown and the reasoning setting.
3. Note whether code execution and web search are available in that client, as far as you can see.
4. Run every case in a **new chat**, unless the case says to continue. Do not correct or help Studio between steps.
5. Startup (cases 1 and 2) is tested separately in ordinary ChatGPT and in ChatGPT Work: one does not prove the other.

## Cases

### SM1. Startup in English

```text
Use FrameCore Works Creative Studio.
```

In a chat whose earlier messages, if any, are in English. **Pass:** the complete English welcome as in `assets/startup-welcome.en.md`: the introduction, all six capability bullets, the materials sentence and the numbered choice 1, 2 or 3, and nothing added before or after it. **Fail:** a shortened welcome, only the modes, another menu, or a different language.

### SM2. Startup in Polish

```text
Użyj FrameCore Works Creative Studio.
```

**Pass:** the complete Polish welcome as in `assets/startup-welcome.pl.md`, same structure as SM1. **Fail:** English, a shortened welcome or an extra menu.

### SM3. A direct task skips the welcome

```text
Use FrameCore Works Creative Studio. Write three headline options for an ad for a reusable water bottle for runners. Keep each under 40 characters.
```

**Pass:** three headlines under 40 characters, no welcome and no mode menu. **Fail:** the welcome or a menu before the work.

### SM4. A video request gets one short route choice

```text
Użyj FrameCore Works Creative Studio. Zrób 15-sekundowy film promocyjny mojej aplikacji do nauki słówek. Mam trzy zrzuty ekranu.
```

**Pass:** one short choice between a prompt for a video generator and a finished MP4 built from code here with the screenshots; no long intake form; no video claimed yet. **Fail:** generator prompts only, or a video claimed before the choice.

### SM5. The code route delivers a file

Continue SM4: choose the MP4 from code and attach three screenshots (any app screenshots you may share).

**Pass with code execution:** an MP4 download link, the `.motion.json` contract and the `.render.py` script; the critique score reported, with an improvement round when it found something. **Pass without code execution:** the contract and the motion player link, with no MP4 claimed. **Fail:** an MP4 claimed without a file, or a toy beep soundtrack.

### SM6. Sound for the rendered video

Continue SM5:

```text
Dodaj do tego filmu dźwięk i muzykę zaprojektowane przez Studio.
```

**Pass with code execution:** an MP4 with sound, the cue table, the timing status (checked, with every hit judged) and loudness in LUFS. **Pass without numpy or ffmpeg:** a clear statement that sound could not be mixed here and the alternatives. **Fail:** a claimed sound mix without a file, or a timing pass with no cue judged.

### SM7. An interactive version is offered once

```text
Użyj FrameCore Works Creative Studio. Rozpisz storyboard 20-sekundowej reklamy kawy w 5 ujęciach, z czasem każdego ujęcia.
```

**Pass:** the complete storyboard as a table, then one short optional offer of an interactive version that says what could be explored. **Fail:** no storyboard, the offer instead of the storyboard, or several offers.

### SM8. Research that cannot run

Switch web search off in the client if it allows, then:

```text
Use FrameCore Works Creative Studio. Write a video prompt for the newest Kling model for a 5-second shot of a cyclist at sunrise.
```

**Pass:** one short sentence that current sources could not be checked, a useful prompt built on stable craft with the model-specific parts marked unverified, and no invented version features. **Fail:** invented current features presented as checked, or a refusal with nothing usable. If web search cannot be switched off, record that and whether research ran.

## Recording the run

Copy [the template](../verification/host-smoke-template.json) to `verification/host-smoke-<version>-<client>-<date>.json` and fill one entry per case: what was observed, the result and the evidence (screenshot names, file names and hashes). Results:

- `PASS_REPORTED` or `FAIL_REPORTED` when the owner or a tester reports what they saw;
- `PASS_OBSERVED` or `FAIL_OBSERVED` when the reviewer inspected the transcript or files themselves;
- `PARTIAL` when some pass criteria were met, with the missing ones named;
- `NOT_RUN` for a case that was skipped, with the reason.

`python3 scripts/check_host_smoke.py` checks every filled record. A passing source check never changes a case's result; host behavior is only what a run shows.

## Related

The [motion benchmark](motion-benchmark/README.md) compares the quality of motion videos across hosts and models with eight blind briefs; it needs the owner's review and has not been run yet.
