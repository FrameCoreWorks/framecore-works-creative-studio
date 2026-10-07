# Motion styles

A style is a whole decision: canvas, ink, accent, type, how things move and one signature move the video is remembered by. [`styles.json`](styles.json) holds seven styles as values for the [motion contract](../../references/motion-contract-json.md), so choosing one replaces a round of brand questions without adding any. The styles are adapted from [kaventro/motion-designer](../../../../integrations/kaventro-motion-designer/README.md) (MIT).

| Style | Feel | Good for | Signature in the scene engine |
| --- | --- | --- | --- |
| Brand-native | the brand's own look | a brand with strong tokens | custom |
| Meadow | soft and friendly | finance, health, family | custom (a brand dot) |
| Warm ink | precise and tactile | professional and developer tools | `item-stagger` with its connector |
| Midnight | focused and luminous | technology, dark interfaces, games | `exit: 'sweep'` with the accent as `sweepColor` |
| Field guide | earthy and editorial | outdoors, travel, food | `item-stagger` connector as a route, `end-card` rule |
| Paper and ink | editorial, type-led | statements, design-led brands | oversized `line-reveal` lines; the coloured full stop is custom |
| Color block | bold and playful | consumer launches, social | custom (canvas colour changes) |

## How Studio uses a style

1. **When the brief leaves the look open.** Offer two or three styles that suit the subject (`choosing` in `styles.json`), each in one line of feel and signature. When the user names colours, a font or brand guidelines, those win: a style fills only what the brief leaves open, and Brand-native is the choice when the brand has a strong look.
2. **Apply it by copying values.** Copy the style's `tokens` and `motion` into the contract's `tokens` and `motion`, and record the choice as top-level `"style": "<id>"` and in `decisions.proposed` (or `confirmed` once approved). The contract stays self-contained: a renderer never reads `styles.json`.
3. **Build the signature with the scene kinds it names.** When it says custom, use the nearest kind or say that the signature needs custom code; never claim a move the render does not show.
4. **Music** ranges are starting points for the sound brief, not a rule; the sound policy in [motion sync](../motion-sync/README.md#adding-sound-to-a-delivered-video) still applies.

All text colours meet WCAG 2.x contrast against their background (4.5:1 for `foreground`, 3:1 for `muted` as large text); the tests check this. The fonts are web-safe stacks that the [Python renderer](../motion-render/README.md) resolves to metric-compatible files; a brand font replaces them.

## Style rules from the source

- **An accent with one meaning.** The accent marks now or just changed; new values arrive in it. Do not spend it on decoration.
- **One signature per video** carries more than five effects. Name it in the brief and say why it fits the subject.
- **Restyle the stage, never the subject.** A product's real interface, a logo and approved assets keep their own look; the style dresses what surrounds them.
- **Keep dark backgrounds flat.** Soft gradients on dark canvases band in H.264.

## Verification boundary

During package preparation every style was applied to the `two-statements` example: each contract passed `check-score.mjs` and rendered with the Python renderer. Contrast is computed from the token values. Whether a style suits a given brand is a design judgement, not a test result.
