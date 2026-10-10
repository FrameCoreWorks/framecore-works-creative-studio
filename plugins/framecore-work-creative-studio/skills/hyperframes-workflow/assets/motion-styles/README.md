# Motion styles

A style is a whole decision: canvas, ink, accent, type, how things move and one signature move the video is remembered by. [`styles.json`](styles.json) holds eleven styles as values for the [motion contract](../../references/motion-contract-json.md), so choosing one replaces a round of brand questions without adding any. The styles are adapted from [kaventro/motion-designer](../../../../integrations/kaventro-motion-designer/README.md) (MIT).

| Style | Feel | Good for | Signature in the scene engine |
| --- | --- | --- | --- |
| Brand-native | the brand's own look | a brand with strong tokens | custom |
| Meadow | soft and friendly | finance, health, family | custom (a brand dot) |
| Warm ink | precise and tactile | professional and developer tools | `item-stagger` with its connector |
| Midnight | focused and luminous | technology, dark interfaces, games | `exit: 'sweep'` with the accent as `sweepColor` |
| Field guide | earthy and editorial | outdoors, travel, food | `item-stagger` connector as a route, `end-card` rule |
| Paper and ink | editorial, type-led | statements, design-led brands | oversized `line-reveal` lines; the coloured full stop is custom |
| Color block | bold and playful | consumer launches, social | `params.background` with `backgroundWipe` on every scene |
| Sale poster | loud, retail, price-first | promotions, sales, price announcements | condensed Archivo at weight 800, the price last in the accent |
| Editorial serif | warm, crafted, editorial | food, craft, culture, premium | Fraunces lines, the accent on one word |
| Product light | clean, precise, modern product | apps, SaaS, product demos | `device` with real screens and a `counter` |
| Bold grotesque | energetic, youthful, event-like | events, festivals, lifestyle brands | stacked condensed Bricolage Grotesque, `contentScale` 1.2 in 9:16 |

## How Studio uses a style

1. **When the brief leaves the look open.** Offer two or three styles that suit the subject (`choosing` in `styles.json`), each in one line of feel and signature. When the user names colours, a font or brand guidelines, those win: a style fills only what the brief leaves open, and Brand-native is the choice when the brand has a strong look.
2. **Apply it by copying values.** Copy the style's `tokens`, `motion` and, when it has them, `fonts` into the contract's `tokens`, `motion` and `fonts`, and record the choice as top-level `"style": "<id>"` and in `decisions.proposed` (or `confirmed` once approved). The contract stays self-contained: a renderer never reads `styles.json`.
3. **Build the signature with the scene kinds it names.** When it says custom, use the nearest kind or say that the signature needs custom code; never claim a move the render does not show.
4. **Music** ranges are starting points for the sound brief, not a rule; the sound policy in [motion sync](../motion-sync/README.md#adding-sound-to-a-delivered-video) still applies.

All text colours meet WCAG 2.x contrast against their background (4.5:1 for `foreground`, 3:1 for `muted` as large text); the tests check this. The first seven styles use web-safe stacks that the [Python renderer](../motion-render/README.md) resolves to metric-compatible files. The four commercial styles name [bundled OFL fonts](../../../pipeline-core/assets/fonts/README.md) in `fonts`, which the player and the renderer load from the same files. A brand font replaces either.

## Style rules from the source

- **An accent with one meaning.** The accent marks now or just changed; new values arrive in it. Do not spend it on decoration.
- **One signature per video** carries more than five effects. Name it in the brief and say why it fits the subject.
- **Restyle the stage, never the subject.** A product's real interface, a logo and approved assets keep their own look; the style dresses what surrounds them.
- **Keep dark backgrounds flat.** Soft gradients on dark canvases band in H.264.

## Verification boundary

During package preparation every style was applied to the `two-statements` example: each contract passed `check-score.mjs` and rendered with the Python renderer. Contrast is computed from the token values. Whether a style suits a given brand is a design judgement, not a test result.
