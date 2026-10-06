# Creative Studio 1.17.0

Catch layout problems in motion before anyone watches it.

- **Automated frame review.** One command renders the key frames of an animation (start, end, every scene boundary and every reading pause) and checks the text in them: does it leave the frame, is it cut off by a mask, is the contrast high enough under WCAG, does it respect the margins, is it fully visible while it should be read.
- **Contact sheet.** The result is a page of all checked frames with problems marked in red or amber, plus a machine-readable report, so Studio can fix errors before showing you the result.
- It runs where Node.js and a local Chrome or Chromium exist, such as Codex. It checks layout only; watching the full animation is still part of the review.

Startup, the complete welcome and all 37 skill IDs are unchanged. See [verification](VERIFICATION.md) and [release status](RELEASE_STATUS.md).
