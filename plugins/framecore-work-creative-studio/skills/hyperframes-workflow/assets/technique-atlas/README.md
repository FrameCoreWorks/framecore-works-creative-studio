# Motion technique atlas

`atlas.json` names 637 motion techniques in English: what each does, when to use it, its family (principles, entrance, emphasis, type, transitions, camera, data, UI, explainer, shape, texture, generative, depth, loop, caption), level, purposes, media, the techniques that pair with it, and the HyperFrames registry blocks whose names match it. `atlas.py` looks one up by the name a brief or a client used.

```sh
python3 atlas.py "morph match cut"
python3 atlas.py --family transitions --purpose attention --media "short form"
python3 atlas.py match-cut --json
```

## How to use it

A named technique in a brief (for example "morph match cut" or "light sweep") is resolved in this order:

1. **HyperFrames registry first.** `npx hyperframes catalog <words>`; the atlas lists registry candidates found by name at the pinned registry commit (104 of 637 techniques have one). A name match is a candidate, not a proof: read the block before adding it.
2. **The atlas as a vocabulary and a motion preview.** It says what the technique does and when it fits; its card (and for 128 techniques a rendered clip) shows the motion. Use it to agree on the word with the client and to choose pairings, never as the idea: the idea comes from the brief.
3. **Write the motion yourself** in the composition, from the brief's copy, sizes and timing. Do not copy card code: card prompts carry the author's own coordinates and copy, and the cards cite third-party concept sources whose licences differ.

## Source and licence

Projected from [gongnyang/awesome-ai-motion](https://github.com/gongnyang/awesome-ai-motion) at commit `1e3c249073c61b42ceb556d7800f628d565d9312` (2026-09-30): the English card text only (`en`, Latin-script `aka`, `oneLinerEn`, `useWhenEn`, `pairsWith`, family, level, purposes, media, render status). No code, clips, prompts, fonts or GSAP files are copied.

MIT License, Copyright (c) 2026 gongnyang. Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Registry names come from [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) (Apache-2.0) at commit `86521b94f592bcf0ca86aba63068893cf658af16`, the commit Studio pins for HyperFrames 0.8.149 (454 registry items). The repository script `scripts/build_technique_atlas.py` rebuilds the file from both pinned checkouts; the source repository had two commits when it was pinned, so a newer commit is checked before the pin moves.
