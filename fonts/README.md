# Bundled fonts

Eighteen static fonts in six families, each with the full Polish alphabet, typographic quotes („ ”), dashes, the ellipsis, non-breaking and thin spaces, currency signs, arrows and basic maths. They exist so that exact text in a graphic or a video is set in a real, licensed typeface on any host with Python and Pillow, without depending on the fonts a sandbox happens to have.

| Family | Styles (name to use) | Good for |
| --- | --- | --- |
| Inter | `Inter Regular`, `Inter SemiBold`, `Inter Bold`, `Inter Black` | neutral sans: interfaces, body text, prices, legal lines, small print |
| Archivo | `Archivo Regular`, `Archivo Bold`, `Archivo Condensed ExtraBold`, `Archivo Expanded Black` | posters and sale headlines; condensed for long words in narrow columns, expanded for short loud words |
| Bricolage Grotesque | `Bricolage Grotesque Regular`, `Bricolage Grotesque Bold`, `Bricolage Grotesque Condensed ExtraBold` | characterful display: lifestyle, events, friendly brands |
| Fraunces | `Fraunces Regular`, `Fraunces SemiBold`, `Fraunces Black` | soft display serif: food, craft, culture, premium |
| Anton | `Anton` | tall condensed impact: one-word headlines, big prices |
| Source Serif 4 | `Source Serif 4 Regular`, `Source Serif 4 SemiBold`, `Source Serif 4 Bold` | reading serif: long copy, menus, programmes, print body text |

The [static compositor](../../../static-graphic-design-creator/assets/static-render/README.md) finds them by these names (`--fonts-list` prints them); the [motion renderer](../../../hyperframes-workflow/assets/motion-render/README.md) takes a file with `--font` and `--font-bold`, for example `skills/pipeline-core/assets/fonts/archivo/Archivo-Bold.ttf`.

## Choosing

Pick by the job, not by habit: one family for headlines and Inter or Source Serif 4 for the rest is usually enough. Long Polish words (`Najnowocześniejszy`, `Bezpieczeństwo`) need a condensed face or a smaller size in a 9:16 column; the tools stop rather than crop a word that does not fit. A brand's own fonts win whenever the user supplies the files and has the right to use them; Studio does not download or substitute commercial fonts.

## Licence and provenance

Every family is under the SIL Open Font License 1.1; its `OFL.txt` sits in the family folder and must travel with the font files. None of the sources declares a Reserved Font Name, so these modified versions keep their names. The files were made by [scripts/build_fonts.py](https://github.com/FrameCoreWorks/framecore-works-creative-studio/blob/main/scripts/build_fonts.py) from [google/fonts](https://github.com/google/fonts) at commit `bd8f81ddb5c74d5c8897b36ad88b440266245103`: static instances of the variable sources at the coordinates in [fonts.json](fonts.json), subset to Latin with Latin Extended-A, keeping kerning, ligatures, marks, localized forms, fractions and the figure, case and superscript features, with hinting removed. `fonts.json` records each source's and each file's SHA-256. The OFL lets anyone use the fonts in any design, including commercial work; the fonts themselves may not be sold on their own.
