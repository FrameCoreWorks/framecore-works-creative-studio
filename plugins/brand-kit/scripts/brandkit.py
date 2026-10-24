#!/usr/bin/env python3
"""brand-kit launcher: website evidence, a draft Studio brand kit, and a local catalog of revisions."""
import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import catalog  # noqa: E402
import draft as drafting  # noqa: E402
import site_fetch  # noqa: E402
import style  # noqa: E402


def _write(path, data):
    text = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    if path in (None, '-'):
        sys.stdout.write(text)
    else:
        pathlib.Path(path).write_text(text, encoding='utf-8')


def _read(path):
    return json.loads(pathlib.Path(path).read_text(encoding='utf-8'))


def cmd_extract(args):
    if args.html:
        base = args.base_url or pathlib.Path(args.html).resolve().as_uri()
        collected = {'start_url': base,
                     'pages': [{'url': base, 'status': 'local-file',
                                'html': pathlib.Path(args.html).read_text(encoding='utf-8', errors='replace')}],
                     'stylesheets': [{'url': str(c), 'status': 'local-file',
                                      'css': pathlib.Path(c).read_text(encoding='utf-8', errors='replace')}
                                     for c in args.css]}
    elif args.url:
        collected = site_fetch.collect(args.url, pages=args.pages)
    else:
        raise ValueError('give a URL or --html FILE')
    evidence = style.build_evidence(collected)
    _write(args.out, evidence)
    fetched = sum(1 for p in evidence['pages'] if p['status'] in (200, 'local-file'))
    print(f"pages read: {fetched}/{len(evidence['pages'])}, stylesheets: {len(evidence['stylesheets'])}, "
          f"colours: {len(evidence['colours'])}, fonts: {len(evidence['fonts'])}, logos: {len(evidence['logos'])}",
          file=sys.stderr)


def cmd_draft(args):
    kit, ledger = drafting.draft(_read(args.evidence))
    _write(args.out, kit)
    if args.ledger:
        _write(args.ledger, {'method': 'static-html-css', 'evidence': args.evidence, 'rows': ledger})
    unknown = sum(1 for row in ledger if row['status'] == 'unknown')
    print(f'draft written; {unknown} fields Unknown, see the ledger', file=sys.stderr)


def cmd_save(args):
    rev = catalog.save(_read(args.kit), args.brand, args.root, note=args.note)
    print(f'saved {catalog.slugify(args.brand)} revision {rev}')


def cmd_list(args):
    brands = catalog.list_brands(args.root)
    if args.json:
        _write(None, brands)
    else:
        for b in brands:
            print(f"{b['brand']}  rev {b['latest']}  {b['saved']}  {b['note']}")


def cmd_show(args):
    _write(None, catalog.show(args.brand, args.root, args.rev))


def cmd_diff(args):
    lines = catalog.diff(catalog.show(args.brand, args.root, args.a), catalog.show(args.brand, args.root, args.b))
    print('\n'.join(lines) if lines else 'no changes')


def main(argv=None):
    parser = argparse.ArgumentParser(prog='brandkit.py', description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('extract', help='collect brand evidence from a public website or a saved page')
    p.add_argument('url', nargs='?')
    p.add_argument('--pages', type=int, default=3, help='pages to read, navigation first (max 8)')
    p.add_argument('--html', help='a saved HTML page instead of a URL')
    p.add_argument('--css', action='append', default=[], help='stylesheet files for --html')
    p.add_argument('--base-url', help='the page address for --html, to resolve links')
    p.add_argument('--out', default='evidence.json')
    p.set_defaults(func=cmd_extract)
    p = sub.add_parser('draft', help='draft brand-kit.json and its source ledger from evidence')
    p.add_argument('evidence')
    p.add_argument('--out', default='brand-kit.draft.json')
    p.add_argument('--ledger', default='brand-kit.sources.json')
    p.set_defaults(func=cmd_draft)
    for name, func in (('save', cmd_save), ('list', cmd_list), ('show', cmd_show), ('diff', cmd_diff)):
        p = sub.add_parser(name)
        p.add_argument('--root', help='catalog folder (default BRAND_KIT_ROOT or ~/.framecore-studio/brand-kits)')
        p.set_defaults(func=func)
        if name == 'save':
            p.add_argument('kit')
            p.add_argument('--brand', required=True)
            p.add_argument('--note', default='')
        elif name == 'list':
            p.add_argument('--json', action='store_true')
        else:
            p.add_argument('brand')
            if name == 'show':
                p.add_argument('--rev', type=int)
            else:
                p.add_argument('a', type=int)
                p.add_argument('b', type=int)
    args = parser.parse_args(argv)
    try:
        args.func(args)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f'brandkit: {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
