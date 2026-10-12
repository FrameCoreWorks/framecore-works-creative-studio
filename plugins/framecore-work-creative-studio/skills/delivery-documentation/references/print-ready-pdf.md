# Print-ready PDF

Checked 2026-10-12; provisional. The printer's own specification always wins: these are the common values Polish and European print shops publish, used as a starting point and as questions to ask. Formats and bleed defaults by product are in the [format and print presets](../../static-graphic-design-creator/references/format-and-print-presets.md); the evidence states (concept, reviewed raster, production master) are in [production and delivery](production-and-delivery.md). A file is "print-ready" only when it matches the named printer's specification and passed that printer's preflight or proof; Studio's own check is a preflight, not that confirmation.

## Principles

- Start from the recipient: the printer, the paper and the finishing (cutting, folding, binding, a sheet people will write on). Profile, bleed, safe margin and the choice of white follow from them.
- A file is a source of truth only after it was checked. Metadata claims ("PDF/X", "300 ppi", "CMYK") are verified against the content, never assumed.
- Report facts (tool output, measurements), inferences and Unknowns separately; name each Unknown and how to resolve it.
- Prefer the smallest correction that fixes the problem; rebuild only when a small one cannot.

## Ask the printer first

Before laying out a print file, get (or ask the user to get) the shop's file requirements, usually a PDF or web page called something like "przygotowanie plików do druku":

1. finished size (trim), page count, single pages or spreads, paper (coated or uncoated) and finishing;
2. bleed per side, and whether crop marks are wanted (many online printers want none);
3. standard and colour: PDF/X-1a, PDF/X-4 or "any PDF", the ICC profile for the paper, whether RGB is accepted and whether the shop converts colours itself;
4. total ink limit (TAC);
5. minimum effective resolution, minimum line weight, minimum type size and safe margin;
6. how spot colours, white ink, varnish, foil or die lines are delivered (named spot colours on a separate layer, overprint, separate file);
7. file naming, upload route, and the proof: when, on which paper, what to check on it.

Record the answers in the delivery notes. A missing answer stays Unknown and is listed as an open point with its owner.

## What a correct file contains

| Item | Common requirement | Notes |
| --- | --- | --- |
| Boxes | TrimBox = finished size; BleedBox = trim plus bleed; MediaBox holds the bleed and any crop marks | state the trim in mm and pt (1 pt = 0.3528 mm); PDF/X requires a TrimBox or ArtBox |
| Bleed | 3 mm is the usual default; some printers, roll-ups, large format and books ask 5 mm or more | backgrounds and images touching an edge run to the bleed line; colour running past the trim line into the bleed is correct, colour stopping at the trim is the error |
| Safe margin | important content 3 to 5 mm inside the trim on flat products (Studio's default 5 mm); 5 to 10 mm for folded, bound or handled products | check the top, bottom and side edges separately |
| Crop marks | only if asked; outside the bleed, offset at least the bleed width, never over content | 100 % K or registration colour, as the printer says |
| Colour | CMYK converted with the printer's profile, profile embedded as the output intent; no RGB, ICC-based RGB or spot colours that were not ordered | coated paper: ISO Coated v2 (FOGRA39) or PSO Coated v3 (FOGRA51); uncoated and writing paper: PSO Uncoated v3 (FOGRA52) |
| Total ink (TAC) | about 300 % on coated sheet-fed offset is common; lower on uncoated and newsprint | check vectors and images; use the printer's figure |
| Black text | small text and thin lines in 100 % K only | rich black on small type shows misregistration; whether black overprints is the printer's setting |
| Large black areas | rich black to the printer's recipe (for example C60 M40 Y40 K100) | never 400 % (C100 M100 Y100 K100) |
| White | never set to overprint | white overprint disappears in print |
| Light tints, thin lines | tints below about 5 % of one ink and lines under about 0.25 pt (0.1 mm) may not print | a 0 pt line is a device hairline; check on a proof |
| Resolution | 300 ppi effective at final size for small formats; large posters seen from distance often 100 to 150 ppi, as a stated decision | effective ppi is pixels divided by placed size, not the resolution tag; bitmap line art 600 to 1200 ppi |
| Transparency | none unless needed; PDF/X-1a requires it flattened, PDF/X-4 keeps it | soft masks, blend modes and alpha can flatten or rasterise badly at the printer |
| Fonts | embedded (subsets are fine) or converted to outlines; the licence must allow embedding | outlines print safely but block late text edits, so keep the editable source |
| Type size | at least about 6 pt; more for white or reversed text on colour | |
| Attachments, metadata | no embedded files (including C2PA or Content Credentials, in `/Names /EmbeddedFiles` or the catalog's `/AF`); Title, Author and Subject set on purpose, generator names removed when not wanted | |
| Structure | one file per job, pages in reading order, no passwords, comments, form fields or layers that should not print | |

Spot colours, varnish and foil follow the printer's naming. Do not convert a requested Pantone to CMYK silently, and do not invent spot colours. Do not convert RGB to CMYK without the printer's request and profile: conversion changes the look and the profile is a decision.

## PDF/X in one paragraph

PDF/X is an ISO family of PDF subsets for print exchange. All parts require embedded fonts, an output intent, a TrimBox (or ArtBox), no encryption and a set Trapped key, and the Info dictionary declares the part in `GTS_PDFXVersion` (PDF/X-1a:2001 pairs the version `PDF/X-1:2001` with `GTS_PDFXConformance` `PDF/X-1a:2001`). PDF/X-1a allows only CMYK and spot colour, no transparency and no embedded files, on PDF 1.3 or 1.4, and is the safest choice for older workflows. PDF/X-4 keeps live transparency, ICC-based colour and layers; not every printer accepts it. Which one to send is the printer's call. A file is PDF/X only when a validating tool (Acrobat Pro preflight, Enfocus PitStop, callas pdfToolbox, a DTP application's PDF/X export with its check, or the printer's own preflight) confirms it; a declaration in the file proves nothing, and Studio's tools do not claim conformance.

## Check every file

1. Boxes: MediaBox, TrimBox, BleedBox, bleed in mm per side, safe margin per edge.
2. Colour: no RGB, ICC-based RGB or unordered spot colours; total ink of vectors and images; output intent.
3. Transparency and blend modes.
4. Images: colour space and effective ppi.
5. Fonts: embedded or outlined, none missing.
6. Attachments and metadata: no C2PA or other embedded files.
7. PDF/X declaration and Trapped.
8. Render comparison with the previous version: only the intended changes.
9. Content: spelling, dates, phone numbers, figures, agreement with the client's data.
10. Rights to logos, photographs and trademarks.

`print_pdf.py check` covers points 1 to 7 (the safe margin needs the eye or a render), `print_pdf.py compare` covers point 8, point 9 needs reading against the source, and point 10 is not a technical question.

## Studio's route

1. Compose: the [static compositor](../../static-graphic-design-creator/assets/static-render/README.md) writes the print PDF at its exact size with bleed and optional crop marks; `--icc` with the printer's profile converts it to CMYK. Its output is a raster page: text is rasterised at the print resolution, so no fonts need embedding, but very small type (about 6 pt and below) is sharper from a vector route.
2. Finish: `print_pdf.py finish file.pdf --trim-mm 148x210 --bleed-mm 3 --icc printer.icc --condition "PSO Coated v3 (FOGRA51)" --out file-print.pdf` sets the TrimBox and BleedBox and embeds the profile as the output intent. It changes no colours.
3. Check: `print_pdf.py check file-print.pdf --bleed-mm 3 --min-ppi 300 --max-tac 300 --require cmyk` (or `--require x1a`) walks each page and the form XObjects drawn on it and reports boxes, bleed per side, effective image resolution, colour spaces of images and vector paint, spot colours, total ink of CMYK images and vector colours, transparency, the thinnest stroked line, fonts, embedded files and `/AF`, the output intent, the declared PDF/X version, Trapped, the producer and the SHA-256; it returns REVISE with each problem and lists what to confirm. It does not inspect patterns or annotation appearances.
4. Compare: `print_pdf.py compare previous.pdf new.pdf --region x0,y0,x1,y1` (mm from the page's top-left, needs `pdftoppm`) reports where pixels changed and exits 1 when anything changed outside the intended region.
5. Optional external checks where installed: `pdfinfo -box`, `pdffonts`, `pdfimages -list` (poppler), `qpdf --check` for structure.
6. Deliver with the profile used, the checks run and their result, the SHA-256 and what remains (printer preflight, proof, PDF/X validation).

For vector print files (business cards with small type, text-heavy leaflets, multi-page documents), use a route that keeps text as vectors with embedded fonts: ReportLab where Python runs, or a DTP application (Scribus, Affinity Publisher, InDesign) with the printer's PDF/X preset. Converting an existing vector RGB PDF to CMYK needs a colour-managed tool such as Ghostscript (below) or the DTP application; Pillow cannot do it without rasterising.

## Generator exports and edits without a source

- An image or layout generator may change layout, colour and copy between exports even when asked to "only fix X". Compare every new export with the previous one (`compare`), then walk the list of intended changes, not only what you happened to notice.
- Judge colour from the CMYK values in the file, not from an RGB preview.
- When no editable source exists (an outlined PDF from a generator), small fixes can be made at the PDF operator level: map the blocks (start, end, operator, bounding box after applying the CTM with the q/Q stack; a page is often one form XObject with thousands of path operators); to remove an element cut only its path and painting operators and keep state operators (`k`, `K`, `w`, `i`) the next elements rely on; to move a block wrap it in a `cm` translation and its inverse, allowing for the form's own scale (often 0.1, which makes a naive shift ten times wrong); save with pikepdf (`compress_streams=True`), never by compressing raw streams by hand; compare the renders before and after, and accept only changes inside the intended area. Operator indices are valid for one file only and must be re-mapped for each version. Studio bundles no tool for this; test any script on a file whose result is known first, where a no-op edit must reproduce the render exactly.
- Do not use operator edits for text that must stay editable or for larger redesigns; those need the source (AI, SVG, InDesign, HTML).

## Versions and handoff

- Name files by project, format, version, bleed and profile, for example `<project>_A2_v03_print_5mm_FOGRA39.pdf`.
- Record the SHA-256 of each version (`check` prints it) and a short delta against the previous one.
- Mark rejected versions as rejected so nobody takes them for the final.
- Hand over the final file, its SHA-256, the preflight result, the open points and the owner of each: paper profile and output intent, bleed and marks, the accepted PDF/X part, whether the printer converts colours, rights to logos, photographs and trademarks, and the proof (when, on which paper, what to check).

## Tools to install

| Tool | Used for | Licence | Install | Status in Studio |
| --- | --- | --- | --- | --- |
| Python 3 with Pillow | compose, CMYK conversion of the raster page, render comparison | HPND (Pillow) | usually present | required |
| pikepdf | page boxes, output intent, preflight (`print_pdf.py`) | MPL-2.0 | `pip install pikepdf` | required for `print_pdf.py` |
| numpy | total ink of images | BSD-3 | usually present | optional |
| ReportLab | vector PDF with embedded fonts | BSD | `pip install reportlab` | optional route |
| poppler-utils | `pdftoppm` for `compare`; `pdfinfo -box`, `pdffonts`, `pdfimages -list` | GPL | `brew install poppler`, `apt install poppler-utils` | optional, external command only |
| qpdf | structure check | Apache-2.0 | `brew install qpdf`, `apt install qpdf` | optional |
| Ghostscript | colour-managed conversion of vector PDFs, PDF/X output (`-dPDFX` with `-sColorConversionStrategy=CMYK`, an output ICC profile and a PDF/X definition file), ink coverage (`-sDEVICE=inkcov`, page averages, not the per-pixel maximum) | AGPL-3.0 or a commercial licence from Artifex | `brew install ghostscript`, `apt install ghostscript` | optional, external command only, never bundled or linked; which PDF/X part a version writes is Unknown until checked in that version's documentation |
| Scribus | DTP layout with PDF/X export and preflight | GPL | from scribus.net | optional application for a person |
| ICC profiles | conversion and output intent | ECI profiles may be used and embedded in files; not redistributed | from the printer or eci.org | supplied by the user; Studio does not bundle them |

In a ChatGPT code environment without package installation, `print_pdf.py` may be unavailable: say so, deliver the composed PDF with its known properties and list the checks the printer must run.

## Avoid

- Converting RGB to CMYK without the printer's request and profile.
- Adding transparency where it is not needed.
- Trusting a declaration in the metadata.
- Leaving attachments and generator metadata in the file.
- Correcting without comparing renders before and after.
- Claiming conformance with a standard without validation in a tool made for it.
- Judging colour from an RGB preview.

## Sources (accessed 2026-10-12)

- [Copy Shop Kraków: general file requirements](https://www.copyshop.krakow.pl/wp-content/uploads/2025/10/ogolne_warunki_wysylanie_plikow_do_druku.pdf) (bleed, marks outside the bleed, fonts).
- [Empir Poznań: preparing work for print](https://www.empir.poznan.pl/wp-content/uploads/2017/01/zasady_przygotowania_prac_do_druku.pdf).
- [FINIDR: print data technical conditions](https://www.finidr.com/wp-content/uploads/sites/5/2021/07/sop-studio-601-print-data-technical-conditions-en.pdf) (PDF/X, total ink).
- [Vogue Polska: publisher technical specification](https://www.vogue.pl/files/pdf/zalacznik_3_specyfikacja_techniczna_wydawcy.pdf) (magazine advertising files).
- [ICC profile registry: PSO Coated v3](https://registry.color.org/profile-registry/PSOcoated_v3) and [ECI downloads](https://eci.org/) (profiles and their terms).
- [Fogra characterisation data](https://11.fogra.org/en/downloads/work-tools/characterisation-data).
- [Ghostscript bug 700931](https://bugs.ghostscript.com/show_bug.cgi?id=700931), quoting the pdfwrite PDF/X documentation (an output ICC profile is required).
- The owner's general print-file handover of 2026-10-12 (principles, checklist, operator-level edits, generator exports, versioning); not stored in the repository.
