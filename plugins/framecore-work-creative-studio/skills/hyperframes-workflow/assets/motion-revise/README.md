# Contract revisions

[`revise.mjs`](revise.mjs) changes a delivered motion contract without redesigning it. It is dependency-free (Node.js 20 or newer).

```sh
node revise.mjs diff video.motion.json video-r2.motion.json
node revise.mjs extend video.motion.json --scene outro --frames 60 --out video-r2.motion.json --evidence "User: make the ending two seconds longer"
```

- **`diff`** lists every changed value between two revisions as `path: before → after`, ready to show the user. Exit code 1 when anything differs.
- **`extend`** lengthens (positive `--frames`) or shortens (negative) one scene and moves everything after it by the same amount: later scenes with their holds, captions and cues after the scene's end, and `totalFrames`. Overlaps between scenes and holds that run to the scene's end are preserved. It refuses a change that would empty a scene, hold or caption, never overwrites a file, increments `revision`, and prints the diff. With `--evidence` (the user's request, quoted) the new revision is `approved`; without it, `proposed`. A `runtime.script` name gets the new revision suffix (`video-r1.render.py` becomes `video-r2.render.py`); copy the script under that name. It then lists descriptive text fields that name frames or seconds (`acceptance`, scene `entry`/`action`/`exit`/`transition`, `decisions`); check them and rewrite any the change made wrong.

## How Studio revises a delivered video

When the user asks to change a video that already has a contract:

1. **Start from the existing contract and render script**, the `.motion.json` and the `.render.py` (named in `runtime.script`) that were delivered or uploaded; never rebuild from memory. If no contract is available, ask for it or say that the result is a new design. If the contract is there but the script is not, ask for it once; without it, write a new script and say that unchanged parts may differ by a few pixels.
2. **Change only what was asked.** Keep every other value, including copy, colors, fonts, scene kinds and timing. Timing changes go through `extend` where a shell or code execution is available, or follow its rule by hand: everything after the changed scene moves by the same number of frames.
3. **Increment `revision`.** A direct, complete change request is approval of the new revision: `approved` with evidence quoting it. A change that needs a creative decision is `proposed` until the user approves.
4. **Show what changed** as a short list (was → is), from `diff` or written by hand, and state what stayed the same.
5. **Render with the same script.** Run the previous render script unchanged on the new contract. Change the script only when the request needs something it cannot draw (for example a new scene kind), and then list that change too. Where the previous MP4 is available, compare a frame of an unchanged part with it: it should be pixel-identical. Then run the frame check from the [delivery steps](../single-file-preview/README.md#how-studio-delivers-it).
6. **Keep earlier versions.** Name the files with the revision, for example `video-r2.mp4`, `video-r2.motion.json` and `video-r2.render.py` (the same script under the new name, recorded in `runtime.script`), so each revision's three files belong together and nothing is overwritten.

## Verification boundary

During package preparation, in a Linux development container, `extend` was run on the starter example and on a 6-second contract produced by ordinary ChatGPT on 2026-10-07; every result passed `check-score.mjs`. Host behavior when a user asks for a revision is not verified.
