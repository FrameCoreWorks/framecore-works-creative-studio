#!/usr/bin/env python3
"""Embed a motion contract's font files as data URLs, so a local player file shows the same type as the MP4.

  python3 embed_fonts.py video.motion.json video.embedded.motion.json [--font-dir DIR]

A browser does not load fonts from file:// paths next to a local HTML file, so a preview delivered as a file needs the
faces inside the contract. The published player loads bundled files itself and needs no embedding. Each face with a
"file" gains "data"; the file reference stays, so the renderer and the contract still name the same font.
Exit codes: 0 written, 2 a font file was not found or the output exists.
"""
import argparse
import base64
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('studio_render', os.path.join(HERE, 'render.py'))
render = importlib.util.module_from_spec(spec)
spec.loader.exec_module(render)
MIME = {'.ttf': 'font/ttf', '.otf': 'font/otf', '.woff': 'font/woff', '.woff2': 'font/woff2'}


def main(argv=None):
    parser = argparse.ArgumentParser(description="Embed a contract's font files as data URLs for a local preview.")
    parser.add_argument('contract')
    parser.add_argument('out')
    parser.add_argument('--font-dir', action='append', default=[])
    args = parser.parse_args(argv)
    if os.path.exists(args.out):
        sys.stderr.write(f'Output file already exists: {args.out}\n')
        return 2
    with open(args.contract, encoding='utf-8') as handle:
        score = json.load(handle)
    base_dir = os.path.dirname(os.path.abspath(args.contract))
    embedded = []
    try:
        for face in score.get('fonts') or []:
            if face.get('file') and not face.get('data'):
                path = render.font_source({k: v for k, v in face.items() if k != 'data'}, base_dir, args.font_dir)
                with open(path, 'rb') as handle:
                    data = handle.read()
                face['data'] = f"data:{MIME.get(os.path.splitext(path)[1].lower(), 'font/ttf')};base64,{base64.b64encode(data).decode('ascii')}"
                embedded.append({'family': face.get('family'), 'weight': face.get('weight', 400), 'file': face['file'], 'bytes': len(data)})
    except (OSError, RuntimeError, ValueError) as error:
        sys.stderr.write(f'{error}\n')
        return 2
    with open(args.out, 'w', encoding='utf-8') as handle:
        json.dump(score, handle, ensure_ascii=False, indent=2)
        handle.write('\n')
    print(json.dumps({'out': args.out, 'embedded': embedded}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
