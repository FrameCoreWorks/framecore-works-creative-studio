# Independent review of the advanced motion supplement

Reviewer: motion research worker, requested Astra/high; backend identity not independently attested. Date: 2026-11-11. Scope: read-only review of the specialist's eight cards, analytic fixture, recorded results and review/gate metadata. No specialist file was edited. Root is separately executing/verifying the analytic fixture.

Reviewed in full:
- research/motion-specialist/export/advanced-motion-decision-cards.md
- research/motion-specialist/verify-calculations.py
- research/motion-specialist/calculation-results.json
- research/motion-specialist/REVIEW.md
- research/motion-specialist/gate.json

The reviewed document identifies SHA-256 d510efec959a8a935f7ab8fa9ee9997659e5091adefcb124a5f1b94364d0d358 in its own review record. This review concerns the text read before the clarification below, especially line 71.

## Verdict

Suitable as a bounded research supplement, with **one material wording clarification required before its blur procedure becomes an implementation recipe**. The demonstrated calculations are internally consistent under their stated assumptions. They do not establish AE, browser, Blender or codec parity, and the supplement correctly says so.

## Finding SR-01 — Specify compositing inside each temporal sample

Location: research/motion-specialist/export/advanced-motion-decision-cards.md:71.

The proposed sequence says to evaluate, accumulate, then composite. This can be read as averaging each layer first and compositing those averages. With changing alpha, occlusion or backdrop, that is not generally equivalent to integrating the final scene over time.

An original two-sample counterexample, in linear RGB with an opaque background and equal temporal weights:

| Sample | Foreground | Background | Per-sample source-over result |
|---|---|---|---|
| t0 | opaque blue | red | blue (0,0,1) |
| t1 | fully transparent | green | green (0,1,0) |

The average of the composited samples is (0,0.5,0.5). Averaging the foreground's associated color gives (0,0,0.5), with average alpha 0.5; averaging the background gives (0.5,0.5,0). Compositing these averages gives (0.25,0.25,0.5). The difference follows from the product of time-varying background and foreground transmission. This is an analytic deduction, not a rendered experiment. The source-over relationship is supported by [W3C Compositing and Blending, §5.1](https://www.w3.org/TR/compositing-1/#simplealphacompositing).

Requested clarification: evaluate geometry, visibility, masks and compositing for the complete scene at each subframe, then integrate the resulting samples. Separately accumulating layers is a bounded optimization that needs stated assumptions and a comparison fixture. If “evaluate the scene” already intended complete per-sample compositing, make that explicit and remove the ambiguous ordering.

Priority: medium for future implementation guidance; this does not invalidate the constant-velocity shutter arithmetic or claim a defect in a shipped renderer.

## Equations and scoped claims checked

- **Affine pivot compensation:** P′ = P + RS(A′−A) follows by equating the old and new point transforms. The stated clockwise screen convention, scale, numeric position and test-point result agree. The exclusion of parent/skew/camera effects is explicit. Preserving a world matrix when reparenting requires an invertible parent; the document correctly flags singular transforms.
- **Alpha arithmetic:** the stated associated RGB, correct source-over and both misinterpretation examples agree with the given foreground, background and alpha. Nonblack matte handling is not reduced to blind division. The background is opaque and the color domain is explicitly linear.
- **sRGB arithmetic:** the reported 0.735356983 encoding of linear 0.5, approximate 188 code value, and 0.214041140 decoding of encoded 0.5 agree with the bounded transfer model. The local helper is not a complete extended-gamut signed sRGB implementation; this is acceptable because the fixture only claims its in-range SDR example. [W3C CSS Color 4, sample conversion functions](https://www.w3.org/TR/css-color-4/#color-conversion-code).
- **Shutter:** the 30 fps, 180-degree interval is 1/60 second; at 900 px/s its path span is 15 px, versus 18.75 px at 24 fps. This is a path extent under constant velocity, not a prediction of every renderer's edge profile or adaptive sampling.
- **Pinhole projection:** the 240/160 px widths and 120/80 px lateral displacement magnitudes agree with the declared focal scale and depths. Signed direction, real lens distortion and application sensor conventions are outside the example.
- **Retiming:** 300−30−24=246 source middle frames and 180−30−24=126 output middle frames. The inverse mapping is continuous at the two joins; source coordinate 300 corresponds to the exclusive endpoint, while delivered frames are 0–179. The negative-time example is correctly rejected.
- **Spatial arithmetic:** 5% margins yield 972 usable pixels at width 1080; fitting a hypothetical 1100-pixel title gives approximately 0.883636 scale. The text correctly avoids claiming that this hypothetical font measurement occurred.

The fixture assertions cover selected invariants and example values. Several fields are calculated and recorded without dedicated assertions, including wrong-alpha results, shutter and camera values. They were inspected here, but this is an analytic illustration, not a comprehensive property-test suite or a release gate.

## Compositing and parity review

The precomp discussion correctly treats flattening, backdrop and transform order as separate issues. The official Adobe section supports the described adjustment-layer and effect/mask boundary conditions. Its result depends on renderer and layer settings; the document preserves those limitations instead of claiming that CSS isolation implements AE collapse behavior. [Adobe precomposing and render order](https://helpx.adobe.com/after-effects/desktop/work-with-compositions/precomposing-and-nesting/precomposing-nesting-pre-rendering.html).

The color discussion correctly separates alpha association, working interpretation, preview and delivery. It does not claim that all browser compositing is linear or that a screenshot validates HDR. The font and camera sections also avoid native-parity claims. Blender access failures remain an explicit gap. I did not independently reread all thirteen cited sources; this review rechecked the relevant W3C equations and Adobe render-order passage, alongside the sources already read for the main motion research.

## Limits

No app, renderer, video, font, codec or perceptual experiment was executed in this review. The specialist's text gate is a writing check and does not certify mathematical completeness, visual craft or interoperability. Root's separate fixture verification should retain that distinction. The sole requested change is SR-01; no unrelated expansion is needed.
