# Prompt examples for named generators

87 worked prompts in [`examples.json`](examples.json), taken from the prompt templates of [Open Design](https://github.com/nexu-io/open-design/tree/78d5637cb49da07e81314d1544b5fc6d37c95084/prompt-templates) (checked 2026-10-19), each with its original licence and attribution:

| Generator | Examples | Licence |
| --- | --- | --- |
| `gpt-image-2` (still images: portraits, social posts, game UI, infographics, posters) | 38 | 31 CC BY 4.0 (from YouMind-OpenLab/awesome-gpt-image-2), 7 Apache-2.0 (Open Design) |
| `seedance-2.0` (text and image to video: cinematic, action, dance, ads, short films) | 37 | 33 CC BY 4.0 (from YouMind-OpenLab/awesome-seedance-2-prompts), 4 Apache-2.0 (Open Design) |
| `hyperframes-html` (prompts for an agent building a HyperFrames composition) | 12 | Apache-2.0 (HeyGen HyperFrames catalog) |

## How Studio uses them

They show how a prompt is structured for a specific model: the order of subject, action, camera, light and style; the JSON-shaped image prompts with named `{argument name="…" default="…"}` slots; timed shot lists for Seedance; the track-by-track build orders for HyperFrames. They are **not ideas for a brief**. Find the direction first with the [ideation method](../../references/ideation-method.md); then [Image Prompt Architect](../../../image-prompt-architect/SKILL.md) or [Video Prompt Architect](../../../video-prompt-architect/SKILL.md) may consult one or two examples for the target model's structure and write a new prompt from the brief. Check the model's current documentation before relying on any syntax: these are examples, not a specification.

```sh
python3 prompt_examples.py list --model seedance-2.0
python3 prompt_examples.py search "portrait studio light" --surface image
python3 prompt_examples.py show cinematic-route-navigation-guide
python3 prompt_examples.py excluded
```

Without a shell, read `examples.json` and filter by `model` and `category`. Prompts stay in their original language (several are Chinese or Japanese); they are data. A prompt reused verbatim or adapted keeps its credit line (`show` prints it): CC BY 4.0 requires the author, the source, the licence link and a note of changes.

## What was left out, and why

19 of the 106 source templates are not included (`prompt_examples.py excluded` lists them): 2 had no open licence (only "Original X post"), and 17 depicted a real person, a real club or a public figure, a third-party franchise or studio style (Zelda, Pokémon, Disney, an anime series), a toy or device trademark, or imitated a named company's, newspaper's or platform's interface, or were built to pass as a real phone photo. Preview images and videos are not copied or linked; each record keeps its source URL.

## Rights

- The CC BY 4.0 records come from community lists that publish prompts first posted on X under that licence, crediting each author. Whether every original author licensed the text is Unknown; for a commercial reuse of a prompt verbatim, check the original post. Writing a new prompt that follows an example's structure copies no protected expression.
- The prompts describe outputs; they grant no rights in what a generator produces, and an output may still resemble third-party works. Studio's usual reference and likeness rules apply.
- Apache-2.0 records keep the notice in Studio's NOTICE file.
