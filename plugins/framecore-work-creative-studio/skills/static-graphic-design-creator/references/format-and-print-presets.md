# Format and print presets

Checked 2026-10-10; provisional. The machine-readable list is [presets.json](../assets/static-render/presets.json), which the [static compositor](../assets/static-render/README.md) and the [image probe](../../output-critic-iteration/scripts/image_probe.py) read; channel copy limits are in the [channel specs snapshot](../../research-evidence/references/channel-specs-snapshot.md). Confirm in the ad manager's preview or with the print shop before a paid or printed final.

## Screens

| Placement | Pixels | Ratio | Keep text inside |
| --- | --- | --- | --- |
| Instagram or Facebook feed post or ad | 1080 × 1350 | 4:5 | 64 px margins |
| Square post, carousel card | 1080 × 1080 | 1:1 | 64 px margins |
| Stories, Reels cover or ad | 1080 × 1920 | 9:16 | below the top 14 %, above the bottom 35 %, 6 % from the sides |
| Link preview, landscape ad | 1200 × 628 | 1.91:1 | 48 px margins |
| LinkedIn square, landscape | 1200 × 1200, 1200 × 628 | 1:1, 1.91:1 | 48 px margins |
| YouTube thumbnail | 1280 × 720 | 16:9 | bottom-right corner covered by the duration |
| Pinterest pin | 1000 × 1500 | 2:3 | 48 px margins |
| Slide, screen | 1920 × 1080 | 16:9 | 5 % margins |

## Print

| Format | Trim (mm) | Typical use |
| --- | --- | --- |
| A6, A5, A4, DL | 105 × 148, 148 × 210, 210 × 297, 99 × 210 | flyers, leaflets, menus, invitations |
| A3, A2, B2, 50 × 70 cm | 297 × 420, 420 × 594, 500 × 707, 500 × 700 | posters |
| A1, B1, 70 × 100 cm | 594 × 841, 707 × 1000, 700 × 1000 | large posters (100 to 150 ppi effective is common) |
| Business card | 90 × 50 (Polish), 85 × 55 (EU) | |
| Roll-up | 850 × 2000 | 5 mm or more bleed and a bottom zone hidden in the stand; ask the shop |

Defaults: 3 mm bleed on each side, 300 ppi effective at the trim size with bleed, text at least 5 mm inside the trim. Colour: Studio's files are RGB unless the user supplies the print shop's ICC profile (coated paper in Poland is usually FOGRA39 or PSO Coated v3, uncoated PSO Uncoated v3). Say which in the delivery. A print-ready claim needs the shop's own specification; these defaults are a starting point.

In ordinary-language intake, offer the familiar names (a whole printer sheet A4, half a sheet A5, a larger A3; a normal post or a phone story) and keep millimetres and pixels for the specification.
