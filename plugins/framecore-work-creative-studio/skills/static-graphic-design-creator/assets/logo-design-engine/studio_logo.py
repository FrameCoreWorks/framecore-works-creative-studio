#!/usr/bin/env python3
"""Project-local adapter for the pinned Logo Design tools. Python 3.8+, no install.

The reusable engine is bundled; real company marks are a separate reference corpus.
Build reports distinguish generated files from visual approval and render capability.
"""
import argparse
import contextlib
import hashlib
import io
import json
from pathlib import Path
import runpy
import shutil
import sys
import xml.etree.ElementTree as ET

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
import svglib
import render_png
import svg_audit

PIN = "0ecf52e9a4b3ac92b714f7cc6e3148ab8c774134"
SOURCE = "https://github.com/kaankiziltug/logo-design-skill"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def json_file(path, value):
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def new_directory(value):
    path = Path(value).resolve()
    if path == ROOT or ROOT in path.parents:
        raise ValueError("Outputs must be in the project, outside the bundled engine.")
    path.mkdir(parents=True, exist_ok=False)
    return path


def source_svg(value, base):
    path = (base / value).resolve()
    if path.suffix.lower() != ".svg" or not path.is_file():
        raise ValueError("Expected an existing local SVG: " + str(path))
    raw = path.read_text(encoding="utf-8")
    # Restrict this automated build to self-contained SVG artwork. This is not a
    # general SVG sanitizer; review unfamiliar input before invoking native tools.
    if "<!doctype" in raw.lower() or "<!entity" in raw.lower():
        raise ValueError("SVG declarations/entities are not accepted by the build adapter.")
    root = ET.fromstring(raw)
    if svglib.local(root.tag) != "svg":
        raise ValueError("The root must be SVG.")
    for elem in root.iter():
        if svglib.local(elem.tag).lower() in {"script", "foreignobject", "style"}:
            raise ValueError("Build requires self-contained SVG without active content or CSS blocks.")
        for key, value in elem.attrib.items():
            key = svglib.local(key).lower()
            lower = value.lower().strip()
            if key.startswith("on") or (key in {"href", "src"} and not value.startswith("#")):
                raise ValueError("Build does not accept events or external/embedded file references.")
            if "@import" in lower or ("url(" in lower and not lower.startswith("url(#")):
                raise ValueError("Build does not accept external CSS resources.")
    return path


def corpus_path(value):
    """Verify a separately obtained original corpus without copying it into Studio."""
    if not value:
        return None
    path = Path(value).resolve()
    if (path / "skills/logo-design/assets/library/svg").is_dir():
        path = path / "skills/logo-design/assets/library/svg"
    manifest = json.loads((ROOT / "reference-corpus.json").read_text())
    for item in manifest["files"]:
        file = path / item["file"]
        if not file.is_file() or sha(file) != item["sha256"]:
            raise ValueError("Reference corpus differs from the reviewed pin: " + item["file"])
    return path


def tool(name, args, corpus=None, allow_raster=True):
    previous_argv = sys.argv
    previous_corpus = svglib.LIBRARY_SVG_DIR
    previous_render = render_png.render
    captured = io.StringIO()
    try:
        if corpus:
            svglib.LIBRARY_SVG_DIR = str(corpus)
        if not allow_raster:
            render_png.render = lambda *args, **kwargs: None
        elif name == "concept_sheet" and "--greyscale" in args:
            # CairoSVG ignores this upstream sheet's feColorMatrix. Do not silently
            # deliver coloured artwork as greyscale; use a browser or report missing PNG.
            render_png.render = (lambda *a, **k: previous_render(*a, **dict(k, backend="chrome"))) if render_png.find_chrome() else (lambda *a, **k: None)
        sys.argv = [str(SCRIPTS / (name + ".py"))] + list(args)
        with contextlib.redirect_stdout(captured):
            try:
                runpy.run_path(sys.argv[0], run_name="__main__")
            except SystemExit as exc:
                if exc.code not in (0, None):
                    raise ValueError(name + " failed: " + str(exc.code))
        return captured.getvalue()
    finally:
        sys.argv = previous_argv
        svglib.LIBRARY_SVG_DIR = previous_corpus
        render_png.render = previous_render


def probe():
    return {
        "engine": "logo-design", "upstream_version": "1.4.4", "commit": PIN,
        "python": sys.version.split()[0], "source_tools": len(list(SCRIPTS.glob("*.py"))),
        "catalog_records": len(json.loads((ROOT / "assets/library/catalog.json").read_text())),
        "bundled_reference_svg_count": 0,
        "svg_html_tools": "available", "render_backends_detected": render_png.available_backends(),
        "html_screenshot_browser_detected": bool(render_png.find_chrome()),
        "greyscale_sheet_requires": "Chromium-family browser (SVG feColorMatrix)",
        "render_execution": "not_run", "host_registration": "not_checked",
        "automatic_dependency_installation": False, "automatic_network_access": False,
    }


def initialize(out):
    dest = new_directory(out)
    spec = {
        "brand": "", "brief": "", "criteria": "", "adjectives": [],
        "brand_color": "#161616", "greyscale": True, "final": False,
        "concepts": [{"name": "", "symbol": "artwork.svg", "idea": "", "rationale": []}],
        "recommendation": "", "next_steps": [],
    }
    json_file(dest / "presentation-spec.json", spec)
    shutil.copyfile(ROOT / "templates/brand-guidelines-template.md", dest / "brand-guidelines.md")
    (dest / "README.md").write_text(
        "# Logo project\n\nFill presentation-spec.json from the agreed brief. Create the requested artwork.svg "
        "in this project; no logo is supplied or selected by this initializer. Add distinct concepts only "
        "when requested. Run studio_logo.py build presentation-spec.json --out review-01. The output "
        "folder must be new. Review actual variants; a tool report is not approval.\n", encoding="utf-8")
    return {"project": str(dest), "artwork": "not_created", "brief": "requires_user_context"}


def build(spec_path, out, raster="off", corpus=None):
    spec_path = Path(spec_path).resolve()
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    if not spec.get("brand") or not spec.get("brief") or not spec.get("criteria"):
        raise ValueError("Set brand, brief and criteria from the approved task before building.")
    concepts = spec.get("concepts")
    if not isinstance(concepts, list) or not concepts:
        raise ValueError("At least one requested concept is required.")
    fields = ("symbol", "lockup", "avatar", "stacked", "symbol_on_dark", "symbol_on_tile",
              "lockup_on_dark", "lockup_on_tile", "stacked_on_dark", "stacked_on_tile")
    paths = []
    for concept in concepts:
        if not concept.get("name") or not any(concept.get(k) for k in ("symbol", "lockup", "avatar")):
            raise ValueError("Each concept needs a name and local symbol, lockup or avatar SVG.")
        for key in fields:
            if concept.get(key):
                file = source_svg(concept[key], spec_path.parent)
                concept[key] = str(file)
                if file not in paths:
                    paths.append(file)
    backends = render_png.available_backends() if raster != "off" else []
    if raster == "required" and not backends:
        raise ValueError("Raster output requested, but no existing renderer is detected; no dependency installed.")
    dest = new_directory(out)
    copied = {}
    for i, file in enumerate(paths, 1):
        target = dest / ("input-%02d.svg" % i)
        shutil.copyfile(file, target)
        copied[str(file)] = target.name
    for concept in concepts:
        for key in fields:
            if concept.get(key):
                concept[key] = copied[concept[key]]
    json_file(dest / "presentation-spec.json", spec)
    primary = [str(dest / (c.get("symbol") or c.get("avatar") or c["lockup"])) for c in concepts]
    log = []
    names = [c["name"] for c in concepts]
    sheet_args = primary + ["--names"] + names + ["--notes"] + [c.get("idea", "") for c in concepts]
    sheet_args += ["--title", spec["brand"], "-o", str(dest / "concepts.svg")]
    if spec.get("greyscale", True):
        sheet_args += ["--greyscale"]
    log.append(tool("concept_sheet", sheet_args, allow_raster=raster != "off" and bool(backends)))
    log.append(tool("preview_sheet", primary + ["--names"] + names + ["--name", spec["brand"],
                    "--brand-color", spec.get("brand_color", "#161616"), "-o", str(dest / "preview.html")], corpus))
    log.append(tool("presentation_board", [str(dest / "presentation-spec.json"), "-o", str(dest / "presentation.html")]))
    audits = [svg_audit.audit(str(dest / copied[str(p)]), None) for p in paths]
    json_file(dest / "audit.json", {"advisory_only": True, "visual_approval": "not_run", "results": audits})
    raster_records = []
    for index, master in enumerate(primary, 1):
        variant = dest / ("variants-%02d" % index)
        args = [master, "--out-dir", str(variant), "--name", "logo-%02d" % index,
                "--title", spec["brand"], "--mono", spec.get("brand_color", "#161616")]
        avatar = concepts[index - 1].get("avatar")
        if avatar:
            args += ["--favicon-source", str(dest / avatar)]
        if raster != "off" and backends:
            args += ["--png", "512", "--web-icons"]
        log.append(tool("export_variants", args))
        if raster != "off":
            wanted = [variant / name for name in ("favicon.ico", "favicon-16.png", "favicon-32.png",
                      "favicon-48.png", "apple-touch-icon.png", "icon-192.png", "icon-512.png",
                      "maskable-512.png", "site.webmanifest", "head-snippet.html")]
            wanted.extend(svg.with_name(svg.stem + "-512.png") for svg in variant.glob("logo-%02d-*.svg" % index))
            missing = [p.name for p in wanted if not p.is_file()]
            raster_records.append({"concept": index, "status": "complete" if not missing else "incomplete",
                                   "missing": missing})
    if raster != "off":
        raster_records.append({"file": "concepts.png", "status": "complete" if (dest / "concepts.png").is_file() else "incomplete"})
    (dest / "tool-log.txt").write_text("\n".join(log), encoding="utf-8")
    shutil.copyfile(ROOT / "templates/brand-guidelines-template.md", dest / "brand-guidelines-template.md")
    incomplete = any(item["status"] != "complete" for item in raster_records)
    report = {
        "engine_commit": PIN, "source_spec_sha256": sha(spec_path), "requested_raster": raster,
        "status": "incomplete" if incomplete else "built", "visual_approval": "not_run",
        "audit_is_certification": False, "brand_guidelines": "template_requires_completion",
        "reference_corpus": "not_embedded", "raster": raster_records,
        "inputs": [{"path": str(p), "sha256": sha(p)} for p in paths],
        "files": [{"path": str(p.relative_to(dest)), "sha256": sha(p)}
                  for p in sorted(dest.rglob("*")) if p.is_file()],
    }
    json_file(dest / "delivery.json", report)
    if raster == "required" and incomplete:
        raise ValueError("Requested raster outputs are incomplete; see " + str(dest / "delivery.json"))
    return {"directory": str(dest), "status": report["status"], "files": len(report["files"]),
            "visual_approval": "not_run"}


def search(args, corpus):
    # Native filters are preserved. JSON records make unavailable corpus paths explicit.
    if "--format" in args or any(a.startswith("--format=") for a in args):
        raise ValueError("Adapter search always returns JSON; use native search_library.py for other formats.")
    if "--summary" in args or "--list-values" in args:
        return tool("search_library", args, corpus).strip()
    result = tool("search_library", args + ["--format", "json"], corpus)
    start = result.find("[")
    if start < 0:
        raise ValueError("Search did not return records: " + result)
    rows = json.loads(result[start:])
    for row in rows:
        file = row["file"]
        row["local_svg"] = str(corpus / file) if corpus else None
        row["source_url"] = SOURCE + "/blob/" + PIN + "/skills/logo-design/assets/library/svg/" + file
        row["rights"] = "Separate trademark rights; reference study only, not an output asset licence."
    return {"records": rows, "corpus_attached": bool(corpus), "notice": result[:start].strip()}


def gallery(out, corpus):
    dest = new_directory(out)
    html = (ROOT / "assets/library/gallery.html").read_text(encoding="utf-8")
    html = html.replace('src="svg/${d.file}"', 'src="' + corpus.as_uri() + '/${d.file}"')
    html = html.replace('<h1>', '<p>Private reference study. Trademark SVG files remain in the separately '
                        'obtained original checkout. Do not redistribute this gallery with those files.</p><h1>', 1)
    (dest / "gallery.html").write_text(html, encoding="utf-8")
    shutil.copyfile(ROOT / "TRADEMARKS.md", dest / "TRADEMARKS.md")
    return {"gallery": str(dest / "gallery.html"), "external_corpus": str(corpus), "svg_copied": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("probe")
    init = sub.add_parser("init")
    init.add_argument("directory")
    maker = sub.add_parser("build")
    maker.add_argument("spec")
    maker.add_argument("--out", required=True)
    maker.add_argument("--raster", choices=("off", "optional", "required"), default="off")
    lookup = sub.add_parser("search", add_help=False)
    lookup.add_argument("--reference-library")
    lookup.add_argument("args", nargs=argparse.REMAINDER)
    attach = sub.add_parser("verify-corpus")
    attach.add_argument("directory")
    check = sub.add_parser("catalog-check")
    check.add_argument("directory")
    view = sub.add_parser("gallery")
    view.add_argument("--out", required=True)
    view.add_argument("--reference-library", required=True)
    args, extra = parser.parse_known_args()
    if extra and args.command != "search":
        parser.error("unrecognized arguments: " + " ".join(extra))
    try:
        if args.command == "probe":
            value = probe()
        elif args.command == "init":
            value = initialize(args.directory)
        elif args.command == "build":
            value = build(args.spec, args.out, args.raster)
        elif args.command == "verify-corpus":
            value = {"corpus": str(corpus_path(args.directory)), "verified_files": 1432,
                     "copied": False, "rights_granted": False}
        elif args.command == "catalog-check":
            value = {"result": tool("build_catalog", ["--check"], corpus_path(args.directory)).strip()}
        elif args.command == "gallery":
            value = gallery(args.out, corpus_path(args.reference_library))
        else:
            value = search(extra + args.args, corpus_path(args.reference_library))
        print(json.dumps(value, indent=2, ensure_ascii=False))
        return 0
    except (ValueError, OSError, ET.ParseError, KeyError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
