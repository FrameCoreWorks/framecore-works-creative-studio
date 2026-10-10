# Creative Studio 1.55.0

Fewer silent mistakes in motion work.

- **No cropped words.** If a word does not fit its column, the render stops and names the word, instead of delivering a video with "Najnowo" on screen.
- **Polish line breaks.** Short words like "w" or "i" and numbers with units like "10 zł" no longer end up split across lines.
- **Empty vertical frames are caught.** A 9:16 frame with a small block of content in a big empty space is now an error the review reports, and any picture error blocks acceptance.
- **Faster sound.** Mixing music under a voice takes seconds instead of minutes, with the same result.
- **Consistent welcome.** Every description of the welcome now matches its three options.

The welcome, menus and all 37 skill IDs are unchanged. See [verification](VERIFICATION.md) and [release status](RELEASE_STATUS.md).
