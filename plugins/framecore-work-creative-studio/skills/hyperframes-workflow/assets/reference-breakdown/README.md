# Reference breakdown

[`breakdown.py`](breakdown.py) turns a reference animation into a map you can build from, in one command. It is adapted from the breakdown script of [huashu-art-motion](https://github.com/alchaincyf/huashu-art-motion) by alchaincyf (MIT, notice in [LICENSE.upstream](LICENSE.upstream)); the method around it is in [art-style and explainer motion direction](../../references/art-and-explainer-motion-direction.md#breaking-down-a-reference).

```sh
python3 breakdown.py --video reference.mp4 --out breakdown/
```

It needs FFmpeg, NumPy and Pillow (Studio's environment check installs them in its virtual environment) and writes:

| Output | Read it for |
| --- | --- |
| `cuts.json` | the first frame of every new shot, in frames and seconds; the grid the cuts fit (`start = t0 + k × step`, the worst residual, outliers) with BPM candidates if a step is an eighth or a quarter note; the moving area of each segment |
| `sheet_N.jpg` | contact sheets at 4 fps, 30 frames each: how many segments, what each one is |
| `transitions/TNN.jpg` | each cut from 2 frames before its start, every second frame, 15 cells: the transition mechanism, which a 4 fps sheet always flattens into "some wipe" |
| `motion-heatmap.jpg` | per segment, the largest per-pixel change in red over its first frame, with the moving share: what keeps a "still" scene alive |
| `keyframes.jpg`, `ref/segNN.png` | the last clean frame of each segment (3 frames before the next cut): the composition map and references |

A still segment has a mean frame difference under 2, a transition 10 to 40. The defaults (`--thresh 5`, `--debounce 12` frames) suit most edits; a large movement inside a shot can register as a cut, so the grid fit tolerates 20 % outliers and lists them. A cut grid is only a candidate tempo: confirm it on the soundtrack with [`beats.py`](../motion-sync/README.md#analysing-a-supplied-track). The video's own frame rate is kept, so frame numbers are the shared language of the spec.

Analyse only footage the user owns or may study. The output is for learning a mechanism and rebuilding it for a new subject; never copy the frames into a delivery.

Verified on 2026-10-18 in a Linux container (`tests/reference_breakdown_test.py`): on a synthetic 30 fps clip with 8 shots of 20 frames, all 7 cuts were found at their first frame, the grid fitted a 20-frame step with 0.03-frame residual (90 BPM if the step is a quarter note), and every output was written. Real reference films were not run during preparation.
