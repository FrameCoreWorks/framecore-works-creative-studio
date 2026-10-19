# Upscaling a raster image

When a generated or supplied image is too small for its placement, an AI upscaler can enlarge it two to four times. It invents plausible detail; it does not recover detail the source never had. Use it for a background, a photo or an illustration, never as the route to sharp text: exact copy is set afterwards on the [exact-copy compositing](exact-copy-compositing.md) route or regenerated.

## When to upscale

1. Measure first: `python3 ../../output-critic-iteration/scripts/image_probe.py image.png --preset a3` (or `--size WxH` for a screen placement) reports the effective resolution at the trim size. Print targets 300 ppi at the trim size with bleed ([format and print presets](format-and-print-presets.md)); a large poster seen from a distance can accept less when the printer agrees.
2. Prefer a better source: regenerate at the tool's largest size, ask the client for the original file, or set the layout smaller. Upscale only when none of these is available.
3. Enlarge the clean image before text and logos are composited, then composite at the final size.
4. Measure the result again and look at it at 100 % on faces, hands, product edges, fabric and anything with a brand mark: upscalers smear fine texture, sharpen noise into false detail and change small features. A face or a product that changes is a defect; go back to step 2.
5. Report it in the delivery: the source size, the tool and model, the factor and that detail was synthesised. "300 DPI" in a file's metadata is not resolution.

## Upscayl (optional desktop app)

[Upscayl](https://github.com/upscayl/upscayl) is a free, open-source upscaler for Windows, macOS and Linux (AGPL-3.0, Real-ESRGAN with NCNN Vulkan). It runs on the user's computer and needs a Vulkan-capable graphics card; most integrated graphics and plain CPUs do not work. Studio does not run it in chat or in a cloud sandbox: the user upscales locally and sends the result back for measurement and review. How to install it is in the `upscayl` entry of the [recommended extensions](../../workflow-orchestrator/references/extensions.md).

Model licences decide client work (checked 2026-10-19 on OpenModelDB):

| Upscayl model | Licence | Client work |
| --- | --- | --- |
| High Fidelity (HFA2k by Helaman) | CC BY 4.0 | yes, with credit to the model author in the project notes |
| UltraSharp, Ultramix Balanced (Kim2091), Remacri (Foolhardy) | CC BY-NC-SA 4.0 | no: non-commercial use only |
| Upscayl Standard, Upscayl Lite, Digital Art | not stated in the repository | Unknown: do not use for paid work until the licence is confirmed |

Default for paid work: High Fidelity at the smallest factor that reaches the target. Name the model in the delivery. A different upscaler (a host's own image tool, a photo editor) follows the same five steps and its own licence.
