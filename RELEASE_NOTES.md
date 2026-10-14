# Creative Studio 1.77.0

Fixes from an external code review.

- **Safer renders.** A motion file can only use images, fonts and sounds from its own project folder.
- **Clearer offers.** Hourly and daily lines show the real quantity and rate, and discounts are shown.
- **Fewer false alarms and misses.** Clip review, the voice-over timer, the on-image text check and the Polish copy check each fix a case they got wrong.
- **Versioned files are safe.** `spot.v2` exports no longer overwrite `spot.v1`.

The welcome, menus and all 37 skill IDs are unchanged. See [verification](VERIFICATION.md) and [release status](RELEASE_STATUS.md).
