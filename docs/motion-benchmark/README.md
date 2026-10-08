# Motion benchmark

A fixed, blind comparison of motion design results across hosts and models that use the same plugin version. It replaces impressions ("model X seems better") with the same eight briefs, the same automatic metrics and a review in which the reviewer does not know which model made which video. Written 2026-10-08 on the owner's request (roadmap: measure first, then close the gaps with tools and rules).

## What is compared

Each run is one host, one model and one reasoning setting, for example `codex-astra6-high`, `codex-sol61-high`, `chatgpt-work-astra6` or `claude-opus55`. Every run uses the same plugin version (record it) and receives the eight prompts in [`briefs.json`](briefs.json) unchanged, each in a new chat or session, with no follow-up messages. The prompts are test inputs: six in Polish and two in English, in their original language; they cover a product film with a device, a type-led manifesto, a counter, a bold promotion, a logo sting, a quote, three steps and an event announcement, in 9:16, 1:1 and 16:9.

## Running it

1. **Record the setup** for each run: host, model, reasoning setting, plugin version, date.
2. **Run the eight briefs.** Paste each prompt as it is into a new chat or session. Do not help, correct or ask for changes; the first delivered answer is the result. If a run cannot deliver a video, that is the result too.
3. **Save what each run delivered** in a folder per run and brief:

   ```text
   benchmark-results/
     codex-astra6-high/
       b1-app-fitness/   video.mp4, video.motion.json, transcript.md (optional), meta.json (optional)
       b2-manifesto/     ...
     claude-opus55/
       ...
   ```

   `meta.json` may hold `{"host": "...", "model": "...", "reasoning": "...", "plugin": "1.34.0", "date": "..."}`.
4. **Make the blind set:** `python3 scripts/motion_benchmark.py blind benchmark-results benchmark-blind`. It runs the craft critique on every contract, reads sound and length with ffprobe, copies every video to `benchmark-blind/videos/<code>.mp4` and writes `scores.csv` and `key.json`. Do not open `key.json`.
5. **Review blind.** Watch the videos brief by brief (same brief side by side) and fill `scores.csv` from 1 (poor) to 5 (excellent): concept (an idea, not only the copy), motion (easing, choreography, transitions), typography (hierarchy, size, spacing), pacing (readable, no dead time, a hook), sound (fit, balance, sync) and overall. Notes are free text.
6. **Summarize:** `python3 scripts/motion_benchmark.py summarize benchmark-results benchmark-blind` writes `summary.md` and `summary.json`: per run the videos delivered, how many have sound, the mean critique score and errors, and the mean of each criterion.

Steps 4 to 6 can be done by Claude Code or Codex in the repository when the result folders are supplied; the review in step 5 is the owner's.

## Reading the result

- A gap in **delivered** or **critique errors** is a process gap: the model skipped steps or ignored the rules. It is closed with stricter delivery steps and tools (the improvement round, checks that fail loudly).
- A gap in **pacing** or **typography** with similar critique scores is a judgement gap the rules do not yet catch: add a rule or a check to the critique, then run the benchmark again.
- A gap in **concept** is a creative gap: it is closed with a concept step (several options against a template) and reference examples.
- A gap in **sound** is unlikely to come from the model, since the sound is designed by the Studio tools; it points to a run that skipped or misused them.

Eight briefs and one reviewer give a direction, not statistical proof; a difference of less than half a point on a 1 to 5 scale is within noise. Re-run after each change that aims to close a gap and compare with the previous summary.

## Records

Keep the summary (not the videos) as `verification/motion-benchmark-<date>.json` with the plugin version and run setups. Owner-reported scores are recorded as reported; source checks and automatic metrics are recorded separately.
