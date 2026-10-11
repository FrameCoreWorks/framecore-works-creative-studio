#!/usr/bin/env python3
"""Write public/sample-product.glb: an original synthetic jar (body, label band, lid) as a glTF 2.0 binary.

It stands in for the client's product model so the turntable renders out of the box; replace it with the approved
model of the real product. Standard library only: python3 tools/make_sample_glb.py [out.glb]
"""
import json
import math
import struct
import sys
from pathlib import Path

SEGMENTS = 64


def lathe(profile, arc=360):
    """Positions, normals and triangle indices of a profile [(radius, y)] turned around the y axis through `arc`
    degrees, centred on the front (+z)."""
    positions, normals, indices = [], [], []
    rows = len(profile)
    for j, (r, y) in enumerate(profile):
        # The profile normal from its neighbours (smooth shading along the curve).
        r0, y0 = profile[max(0, j - 1)]
        r1, y1 = profile[min(rows - 1, j + 1)]
        tr, ty = r1 - r0, y1 - y0
        nr, ny = ty, -tr
        length = math.hypot(nr, ny) or 1
        nr, ny = nr / length, ny / length
        for i in range(SEGMENTS + 1):
            a = math.radians(-90 - arc / 2 + arc * i / SEGMENTS)
            positions += [r * math.cos(a), y, -r * math.sin(a)]
            normals += [nr * math.cos(a), ny, -nr * math.sin(a)]
    for j in range(rows - 1):
        for i in range(SEGMENTS):
            a, b = j * (SEGMENTS + 1) + i, (j + 1) * (SEGMENTS + 1) + i
            indices += [a, b, a + 1, a + 1, b, b + 1]
    return positions, normals, indices


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'public/sample-product.glb'
    parts = {
        # The label covers only the front, so the turn is visible on a round jar.
        'body': ([(0.0, 0.0), (0.42, 0.0), (0.5, 0.06), (0.52, 0.2), (0.52, 1.02), (0.47, 1.12), (0.4, 1.16), (0.0, 1.16)], [0.84, 0.55, 0.16, 1], 0.25, 0.0, 360),
        'label': ([(0.528, 0.42), (0.528, 0.8)], [0.97, 0.94, 0.88, 1], 0.7, 0.0, 150),
        'lid': ([(0.0, 1.14), (0.44, 1.14), (0.46, 1.16), (0.46, 1.34), (0.44, 1.36), (0.0, 1.36)], [0.27, 0.2, 0.16, 1], 0.45, 0.1, 360),
    }
    blob, views, accessors, meshes, materials, nodes = bytearray(), [], [], [], [], []
    for name, (profile, colour, roughness, metalness, arc) in parts.items():
        positions, normals, indices = lathe(profile, arc)
        first = len(accessors)
        for data, kind, target in ((positions, 'VEC3', 34962), (normals, 'VEC3', 34962), (indices, 'SCALAR', 34963)):
            fmt = '<%dH' % len(data) if kind == 'SCALAR' else '<%df' % len(data)
            raw = struct.pack(fmt, *data)
            while len(blob) % 4:
                blob.append(0)
            views.append({'buffer': 0, 'byteOffset': len(blob), 'byteLength': len(raw), 'target': target})
            blob += raw
            accessor = {'bufferView': len(views) - 1, 'componentType': 5123 if kind == 'SCALAR' else 5126, 'count': len(data) // (1 if kind == 'SCALAR' else 3), 'type': kind}
            if accessor['componentType'] == 5126 and data is positions:
                accessor['min'] = [min(data[k::3]) for k in range(3)]
                accessor['max'] = [max(data[k::3]) for k in range(3)]
            accessors.append(accessor)
        materials.append({'name': name, 'pbrMetallicRoughness': {'baseColorFactor': colour, 'roughnessFactor': roughness, 'metallicFactor': metalness}, 'doubleSided': True})
        meshes.append({'name': name, 'primitives': [{'attributes': {'POSITION': first, 'NORMAL': first + 1}, 'indices': first + 2, 'material': len(materials) - 1}]})
        nodes.append({'name': name, 'mesh': len(meshes) - 1})
    while len(blob) % 4:
        blob.append(0)
    gltf = {'asset': {'version': '2.0', 'generator': 'FrameCore Studio make_sample_glb.py (original synthetic sample)'}, 'scene': 0,
            'scenes': [{'nodes': list(range(len(nodes)))}], 'nodes': nodes, 'meshes': meshes, 'materials': materials,
            'accessors': accessors, 'bufferViews': views, 'buffers': [{'byteLength': len(blob)}]}
    text = json.dumps(gltf, separators=(',', ':')).encode()
    text += b' ' * (-len(text) % 4)
    data = struct.pack('<III', 0x46546C67, 2, 12 + 8 + len(text) + 8 + len(blob)) + struct.pack('<II', len(text), 0x4E4F534A) + text + struct.pack('<II', len(blob), 0x004E4942) + bytes(blob)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    print(f'{out} {len(data)} bytes')


if __name__ == '__main__':
    main()
