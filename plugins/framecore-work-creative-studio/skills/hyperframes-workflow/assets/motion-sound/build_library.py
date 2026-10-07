#!/usr/bin/env python3
"""Measure the bundled sound library and write library.json.

Every sound is a recording released under CC0 (see library/SOURCES.md). For each file this records its
family, source, SHA-256, duration, the time of its transient (`onset_ms`, first sample above half the peak)
and of its loudest moment (`peak_ms`, 10 ms windows), and its level around that moment (`level_db`), so the
mixer can put the audible hit exactly on a frame and play every variant of a family at the same loudness.
Requires Python 3.8+ and ffmpeg; no Python packages.

  python build_library.py            # rewrites library.json next to this file
  python build_library.py --check    # exits 1 when library.json does not match the files
"""
import array
import hashlib
import json
import math
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RATE = 48000

# family: (description, alignment point, files as (folder, regular expression))
FAMILIES = {
    'whoosh': ('air movement of a swung object: transitions, sweeps, wipes, pushes', 'peak', [('oga-swishes', r'swish-\d+\.wav')]),
    'thud': ('soft low landing: end cards, logos, a heavy result settling', 'onset', [('kenney-impact', r'impactSoft_(medium|heavy)_\d+\.ogg')]),
    'knock': ('dry wooden knock: a line, card or item landing', 'onset', [('kenney-impact', r'impactWood_(light|medium)_\d+\.ogg')]),
    'ting': ('bright glass, metal or plate accent: a highlight, a final value, a reveal', 'onset', [('kenney-impact', r'impact(Glass|Metal|Plate)_light_\d+\.ogg')]),
    'click': ('short mechanical click: a tap or a button press', 'onset', [('kenney-interface', r'click_\d+\.ogg'), ('kenney-ui', r'(click\d|mouseclick\d)\.ogg')]),
    'release': ('the release of a press, a few frames after the click', 'onset', [('kenney-ui', r'mouserelease\d\.ogg')]),
    'tick': ('very short tick: counters and fast repeated steps', 'onset', [('kenney-interface', r'tick_\d+\.ogg')]),
    'switch': ('mechanical switch or toggle: a state change', 'onset', [('kenney-interface', r'(switch|toggle)_\d+\.ogg')]),
    'scroll': ('ratchet of a scroll wheel: scrolling content', 'onset', [('kenney-interface', r'scroll_\d+\.ogg')]),
}
SOURCES = {
    'kenney-impact': 'Kenney, Impact Sounds 1.0 (CC0)',
    'kenney-interface': 'Kenney, Interface Sounds 1.0 (CC0)',
    'kenney-ui': 'Kenney, UI Audio (CC0)',
    'oga-swishes': 'artisticdude, Swishes Sound Pack, OpenGameArt (CC0)',
}


def decode(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', str(RATE), '-f', 'f32le', '-'],
                         check=True, capture_output=True).stdout
    samples = array.array('f')
    samples.frombytes(raw)
    return samples


def measure(path):
    x = decode(path)
    peak = max((abs(v) for v in x), default=0.0)
    onset = next((i for i, v in enumerate(x) if abs(v) >= 0.5 * peak), 0)
    window = RATE // 100
    energies = [sum(v * v for v in x[i:i + window]) for i in range(0, max(1, len(x) - window + 1), window // 2)]
    loudest = max(range(len(energies)), key=energies.__getitem__) if energies else 0
    centre = loudest * (window // 2) + window // 2
    span = x[max(0, centre - RATE // 40):centre + RATE // 40]
    rms = math.sqrt(sum(v * v for v in span) / max(1, len(span)))
    return {'duration_ms': round(len(x) / RATE * 1000, 1), 'onset_ms': round(onset / RATE * 1000, 1),
            'peak_ms': round(centre / RATE * 1000, 1), 'peak_db': round(20 * math.log10(peak + 1e-12), 1),
            'level_db': round(20 * math.log10(rms + 1e-12), 1)}


def build():
    sounds = []
    for family, (_, align, patterns) in FAMILIES.items():
        for folder, pattern in patterns:
            for name in sorted(os.listdir(os.path.join(HERE, 'library', folder)), key=lambda n: [int(t) if t.isdigit() else t for t in re.split(r'(\d+)', n)]):
                if not re.fullmatch(pattern, name):
                    continue
                path = os.path.join(HERE, 'library', folder, name)
                with open(path, 'rb') as handle:
                    digest = hashlib.sha256(handle.read()).hexdigest()
                stem = re.sub(r'\.(ogg|wav)$', '', name)
                sounds.append({'id': f'{family}/{folder}/{stem}', 'family': family, 'file': f'library/{folder}/{name}', 'source': SOURCES[folder],
                               'license': 'CC0-1.0', 'sha256': digest, 'align': align, **measure(path)})
    return {'schema_version': 1, 'id': 'studio-cc0-1', 'sample_rate_measured': RATE,
            'families': {name: {'use': text, 'align': align} for name, (text, align, _) in FAMILIES.items()}, 'sounds': sounds}


if __name__ == '__main__':
    target = os.path.join(HERE, 'library.json')
    data = build()
    text = json.dumps(data, indent=1, ensure_ascii=False) + '\n'
    if '--check' in sys.argv:
        same = os.path.exists(target) and open(target, encoding='utf-8').read() == text
        print('library.json matches the files' if same else 'library.json is out of date')
        sys.exit(0 if same else 1)
    with open(target, 'w', encoding='utf-8') as handle:
        handle.write(text)
    print(f"{len(data['sounds'])} sounds in {len(data['families'])} families")
