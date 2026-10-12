# Print-ready PDF

Checked 2026-10-12; provisional. The printer's own specification always wins: these are the common values Polish and European print shops publish, used as a starting point and as questions to ask. Formats and bleed defaults by product are in the [format and print presets](../../static-graphic-design-creator/references/format-and-print-presets.md); the evidence states (concept, reviewed raster, production master) are in [production and delivery](production-and-delivery.md). A file is "print-ready" only when it matches the named printer's specification and passed that printer's preflight or proof; Studio's own check is a preflight, not that confirmation.

## Ask the printer first

Before laying out a print file, get (or ask the user to get) the shop's file requirements, usually a PDF or web page called something like "przygotowanie plików do druku":

1. finished size (trim) and number of pages, single pages or spreads;
2. bleed per side, and whether crop marks are wanted (many online printers want none);
3. standard and colour: PDF/X-1a, PDF/X-4 or "any PDF", the ICC profile for the paper (coated, uncoated, newsprint), and whether RGB is accepted;
4. total ink limit (TAC);
5. minimum effective resolution, minimum line weight and safe margin;
6. how spot colours, white ink, varnish, foil or die lines are delivered (named spot colours on a separate layer, overprint, separate file);
7. file naming and upload route; whether a proof is offered.

Record the answers in the delivery notes. A missing answer stays Unknown and is listed as a remaining check.

## What a correct file contains

| Item | Common requirement | Notes |
| --- | --- | --- |
| Page size | trim plus bleed on every side | A5 with 3 mm bleed is 154 × 216 mm |
| TrimBox and BleedBox | set on every page | imposition and preflight read sizes from them; PDF/X requires a TrimBox or ArtBox |
| Bleed | 3 mm is the usual default for flyers, posters and cards; roll-ups, large format and books often more | backgrounds and images touching an edge run to the bleed line |
| Safe margin | important text and logos 3 to 5 mm inside the trim (Studio's default 5 mm) | more for bound products and roll-up feet |
| Crop marks | only if asked; outside the bleed, offset at least the bleed width, in a slug | marks inside the bleed print on the product |
| Colour | CMYK converted with the printer's profile, profile embedded as the output intent | coated paper in Poland: ISO Coated v2 (FOGRA39) or PSO Coated v3 (FOGRA51); uncoated: PSO Uncoated v3 (FOGRA52) |
| Total ink (TAC) | about 300 % on coated sheet-fed offset is common; lower on uncoated and newsprint | use the printer's figure |
| Black text | small text and thin lines in 100 % K only | rich black on small type shows misregistration |
| Large black areas | rich black to the printer's recipe (for example C60 M40 Y40 K100) | never 400 % (C100 M100 Y100 K100) |
| White | never set to overprint | white overprint disappears in print |
| Resolution | 300 ppi effective at final size for small formats; large posters seen from distance often 100 to 150 ppi | bitmap line art higher (600 to 1200 ppi) |
| Fonts | embedded (subsets are fine) or converted to outlines | the font licence must allow embedding |
| Lines | thinnest line about 0.25 pt (0.1 mm) unless the printer says otherwise | hairlines may vanish |
| Structure | one file per job, pages in reading order, no passwords, comments, form fields or layers that should not print | |

Spot colours, varnish and foil follow the printer's naming. Do not convert a requested Pantone to CMYK silently, and do not invent spot colours.

## PDF/X in one paragraph

PDF/X is an ISO family of PDF subsets for print exchange. All parts require embedded fonts, an output intent, a TrimBox (or ArtBox), no encryption and a set Trapped key. PDF/X-1a allows only CMYK and spot colour and no live transparency (it is flattened), which suits older workflows. PDF/X-4 keeps live transparency and ICC-based colour and is what many current workflows prefer. Which one to send is the printer's call. A file is PDF/X only when a validating tool (Acrobat Pro preflight, callas pdfToolbox, a DTP application's PDF/X export with its check, or the printer's own preflight) confirms it; Studio's tools do not claim conformance.

## Studio's route

1. Compose: the [static compositor](../../static-graphic-design-creator/assets/static-render/README.md) writes the print PDF at its exact size with bleed and optional crop marks; `--icc` with the printer's profile converts it to CMYK. Its output is a raster page: text is rasterised at the print resolution, so no fonts need embedding, but very small type (about 6 pt and below) is sharper from a vector route.
2. Finish: `print_pdf.py finish file.pdf --trim-mm 148x210 --bleed-mm 3 --icc printer.icc --condition "PSO Coated v3 (FOGRA51)" --out file-print.pdf` sets the TrimBox and BleedBox and embeds the profile as the output intent. It changes no colours.
3. Check: `print_pdf.py check file-print.pdf --bleed-mm 3 --min-ppi 300 --max-tac 300 --require cmyk` reports boxes, bleed per side, effective image resolution, colour spaces, total ink of CMYK images (maximum and 99.9th percentile), font embedding and the output intent, and returns REVISE with each problem. It reads images and fonts placed directly on the page, not inside form XObjects, and does not inspect vector colour operators.
4. Optional external checks where installed: `pdfinfo -box` and `pdffonts` and `pdfimages -list` (poppler), `qpdf --check` for structure.
5. Deliver with the profile used, the checks run and their result, and what remains (printer preflight, proof, PDF/X validation). The tool scripts are in [static-render](../../static-graphic-design-creator/assets/static-render/README.md).

For vector print files (business cards with small type, text-heavy leaflets, multi-page documents), use a route that keeps text as vectors with embedded fonts: ReportLab where Python runs, or a DTP application (Scribus, Affinity Publisher, InDesign) with the printer's PDF/X preset. Converting an existing vector RGB PDF to CMYK needs a colour-managed tool such as Ghostscript (below) or the DTP application; Pillow cannot do it without rasterising.

## Tools to install

| Tool | Used for | Licence | Install | Status in Studio |
| --- | --- | --- | --- | --- |
| Python 3 with Pillow | compose, CMYK conversion of the raster page | HPND (Pillow) | usually present | required |
| pikepdf | page boxes, output intent, preflight (`print_pdf.py`) | MPL-2.0 | `pip install pikepdf` | required for `print_pdf.py` |
| numpy | total ink measurement | BSD-3 | usually present | optional |
| ReportLab | vector PDF with embedded fonts | BSD | `pip install reportlab` | optional route |
| poppler-utils | `pdfinfo -box`, `pdffonts`, `pdfimages -list` | GPL | `brew install poppler`, `apt install poppler-utils` | optional, external command only |
| qpdf | structure check | Apache-2.0 | `brew install qpdf`, `apt install qpdf` | optional |
| Ghostscript | colour-managed conversion of vector PDFs, PDF/X output (`-dPDFX` with `-sColorConversionStrategy=CMYK`, an output ICC profile and a PDF/X definition file), ink coverage (`-sDEVICE=inkcov`, page averages, not the per-pixel maximum) | AGPL-3.0 or a commercial licence from Artifex | `brew install ghostscript`, `apt install ghostscript` | optional, external command only, never bundled or linked; which PDF/X part a version writes is Unknown until checked in that version's documentation |
| Scribus | DTP layout with PDF/X export and preflight | GPL | from scribus.net | optional application for a person |
| ICC profiles | conversion and output intent | ECI profiles may be used and embedded in files; not redistributed | from the printer or eci.org | supplied by the user; Studio does not bundle them |

In a ChatGPT code environment without package installation, `print_pdf.py` may be unavailable: say so, deliver the composed PDF with its known properties and list the checks the printer must run.

## Sources (accessed 2026-10-12)

- [Copy Shop Kraków: general file requirements](https://www.copyshop.krakow.pl/wp-content/uploads/2025/10/ogolne_warunki_wysylanie_plikow_do_druku.pdf) (bleed, marks outside the bleed, fonts).
- [Empir Poznań: preparing work for print](https://www.empir.poznan.pl/wp-content/uploads/2017/01/zasady_przygotowania_prac_do_druku.pdf).
- [FINIDR: print data technical conditions](https://www.finidr.com/wp-content/uploads/sites/5/2021/07/sop-studio-601-print-data-technical-conditions-en.pdf) (PDF/X, total ink).
- [Vogue Polska: publisher technical specification](https://www.vogue.pl/files/pdf/zalacznik_3_specyfikacja_techniczna_wydawcy.pdf) (magazine advertising files).
- [ICC profile registry: PSO Coated v3](https://registry.color.org/profile-registry/PSOcoated_v3) and [ECI downloads](https://eci.org/) (profiles and their terms).
- [Fogra characterisation data](https://11.fogra.org/en/downloads/work-tools/characterisation-data).
- [Ghostscript bug 700931](https://bugs.ghostscript.com/show_bug.cgi?id=700931), quoting the pdfwrite PDF/X documentation (an output ICC profile is required).
