# Creative Studio 1.37.0

Checks that tell the truth about what they checked.

- **No pass without a picture.** If the video review could not see the frames (a missing file, the wrong size, a renderer that cannot draw here), it now says the review is incomplete instead of showing a perfect score.
- **No pass without a sound.** A sound cue that is silent is reported as missing, not as perfectly in time.
- **Changes keep sound and picture together.** Lengthening a scene moves its sound cues too, and the music is planned again before the next mix, keeping the choices you made.
- **Lighter video review.** Only the frames under review are decoded, so longer videos no longer risk running out of memory.

These fixes come from an external audit of the repository; every finding was reproduced before it was fixed. Startup, menus and all 37 skill IDs are unchanged. See [verification](VERIFICATION.md) and [release status](RELEASE_STATUS.md).
