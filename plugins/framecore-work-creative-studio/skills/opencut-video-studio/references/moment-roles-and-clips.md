# Moment roles and clips

Studio's own method for cutting a finished film, interview or podcast into short vertical clips, and for overlays timed to a transcript. Written 2026-11-04 after reviewing the Moments, harvest, podcast-clip and talking-head recut guides of the HyperFrames desktop app (0.9.12); nothing is copied from them.

## Roles

Give every window of a film one role. A clip or a new film is assembled from roles, not from timestamps.

| Role | Job | Typical length |
| --- | --- | --- |
| hook | stops the scroll: a claim, a question, a striking image or the result shown first | 1 to 3 s |
| setup | the situation or problem in one line | 2 to 6 s |
| proof | the thing that shows it works: a demo, a number, a before and after, a quote | 3 to 10 s |
| turn | the surprise or the change of mind | 1 to 4 s |
| payoff | what the viewer gets | 2 to 6 s |
| cta | what to do next, with the brand | 1 to 3 s |

## Cutting clips from a finished piece

1. **Read the transcript and the picture together.** List candidate windows where one complete thought starts and ends; reject windows that need earlier context.
2. **Score each candidate** on: does the first second work alone (hook), is there one clear proof, does it end on a payoff and not mid-sentence. Show the user the top three to five with a one-line reason each; the user picks.
3. **Cut each picked window** with a little air (about 0.3 s) before the first word and after the last; reframe to 9:16 on the speaker or the subject.
4. **Write a title and a post description** for each clip through Copy Voice and Humanizer; the on-screen title is exact copy.
5. **Keep a record per clip:** source file, in and out times, role sequence, title, and what was checked.

## Overlays timed to the transcript

For an interview or talking head that needs designed graphics (kinetic titles, lower thirds, data callouts, quotes, side panels, picture-in-picture):

- Place each overlay on the word that introduces it and take it off before the next idea, never mid-word.
- One overlay family per film (type, colour, motion); vary only the content.
- A data callout shows a number the speaker says or a source the user supplies; record the source.
- Keep faces and mouths clear; overlays live in the side or lower safe area unless the format is a takeover ([caption formats](../../caption-studio/references/talking-head-caption-formats.md)).

## Routes

- FrameCut's own renderer handles cuts, reframing, titles and word-timed captions.
- Graphic-heavy overlays can be built as a HyperFrames composition over the cut ([skill map](../../hyperframes-workflow/references/hyperframes-skill-map.md)). The HyperFrames app's own Moments and podcast tools are features of that app and need it and a HeyGen sign-in; Studio does not drive them.

## Evidence

Source review only (2026-11-04). Not yet run through Studio: NOT_RUN.
