"""Sound direction for one video: analyse the motion contract, then choose sounds and music from the sound base.

Studio does not reuse one fixed set of sounds. For every video it reads the contract (style, motion tempo and easing,
colours, scene kinds, taps, pacing and the brief's own words: goal, audience, message, concept and copy), scores six
moods (calm, bold, playful, technical, organic, editorial) and the pace, and picks for each role the option of
sound-base.json that fits best: how text lands, the music's backbeat, the palette when the style leaves it open,
the key, and the character of the effects (whoosh brightness and strength, click softness, pitch). Near ties are
settled by a seed taken from the video's content, so two similar videos still get different sound, and the same
contract always gets the same. Every choice is written into the contract with its reason and can be overridden.
"""
import json
import os
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
MOODS = ('calm', 'bold', 'playful', 'technical', 'organic', 'editorial')
MINOR_STYLES = {'midnight', 'warm-ink', 'brand-native'}
NEAR_TIE = 0.05


def load_base(path=None):
    with open(path or os.path.join(HERE, 'sound-base.json'), encoding='utf-8') as handle:
        return json.load(handle)


def plain(text):
    """Lower-case text without diacritics (so Polish and English stems match alike)."""
    text = str(text or '').lower().replace('ł', 'l')
    return ''.join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c))


def luminance(colour):
    try:
        value = colour.strip().lstrip('#')
        if len(value) == 3:
            value = ''.join(c * 2 for c in value)
        r, g, b = (int(value[i:i + 2], 16) / 255 for i in (0, 2, 4))
    except (AttributeError, ValueError, IndexError):
        return None
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in (r, g, b)]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def analyze(score, base=None, engine=None):
    """The video's sound profile: pace, mood scores from 0 to 1 and the evidence behind them."""
    base = base or load_base()
    fps = score['fps']['num'] / score['fps']['den']
    scenes = score.get('scenes') or []
    seconds = score['totalFrames'] / fps
    scene_seconds = seconds / max(1, len(scenes))
    motion = dict(engine.motion(score)) if engine else dict(score.get('motion') or {})
    entry = motion.get('entryFrames', 15)
    moods = {m: 0.0 for m in MOODS}
    evidence = []

    def add(weights, scale, why):
        if weights:
            for mood, weight in weights.items():
                moods[mood] += weight * scale
            evidence.append(why)

    style = score.get('style')
    add(base['style_moods'].get(style), 1.0, f'style {style}')
    tempo = plain((score.get('motion') or {}).get('tempo'))
    for word in tempo.replace('_', '-').split('-'):
        add(base['tempo_moods'].get(word.strip()), 0.8, f'motion tempo "{word.strip()}"')
    easings = ' '.join(str(motion.get(k, '')) for k in ('entryEasing', 'exitEasing', 'resolveEasing'))
    if 'Back' in easings or 'Elastic' in easings:
        add({'playful': 0.4}, 1.0, 'overshooting easing')
    light = luminance((score.get('tokens') or {}).get('background'))
    if light is not None and light < 0.05:
        add({'technical': 0.3, 'bold': 0.1}, 1.0, 'dark canvas')
    elif light is not None and light > 0.7:
        add({'calm': 0.1, 'editorial': 0.1}, 1.0, 'light canvas')
    for kind in sorted({scene.get('kind') for scene in scenes if scene.get('kind')}):
        add(base['kind_moods'].get(kind), 0.6, f'{kind} scenes')
    if any((scene.get('params') or {}).get('taps') for scene in scenes):
        add({'technical': 0.3}, 1.0, 'taps on a device')
    words = plain(' '.join(str(score.get(k) or '') for k in ('title', 'goal', 'audience', 'message', 'concept')) + ' ' +
                  ' '.join(str(v) for v in (score.get('copy') or {}).values()))
    tokens = [w for w in ''.join(c if c.isalnum() else ' ' for c in words).split() if w]
    for mood, stems in base['lexicon'].items():
        hits = sorted({w for w in tokens for stem in stems if w.startswith(stem) and (len(stem) > 3 or w == stem)})
        if hits:
            add({mood: 1.0}, 0.25 * min(4, len(hits)), f'words ({", ".join(hits[:4])})')
    top = max(moods.values()) or 1.0
    moods = {m: round(v / top, 3) if top > 0 else 0.0 for m, v in moods.items()}
    if scene_seconds < 2.2 or entry <= 12:
        pace = 'fast'
    elif scene_seconds > 4.0 and entry >= 18:
        pace = 'slow'
    else:
        pace = 'medium'
    return {'pace': pace, 'moods': moods, 'sceneSeconds': round(scene_seconds, 2), 'entryFrames': entry,
            'canvasLuminance': None if light is None else round(light, 3), 'evidence': evidence}


def choose(options, profile, seed, allowed=None):
    """The option fitting the profile best: mood match, plus or minus its pace; near ties settled by the seed.
    Returns (name, fit, reason)."""
    ranked = []
    for name, option in options.items():
        if allowed is not None and name not in allowed:
            continue
        weights = option.get('moods') or {}
        fit = sum(profile['moods'].get(m, 0) * w for m, w in weights.items()) / (sum(weights.values()) or 1)
        pace = option.get('pace')
        if pace:
            fit += 0.15 if pace == profile['pace'] else -0.2 if profile['pace'] != 'medium' else 0
        ranked.append((round(fit, 4), name))
    ranked.sort(key=lambda item: (-item[0], item[1]))
    best = ranked[0][0]
    ties = [name for fit, name in ranked if best - fit <= NEAR_TIE]
    name = ties[seed % len(ties)]
    weights = options[name].get('moods') or {}
    leading = sorted(weights, key=lambda m: -profile['moods'].get(m, 0) * weights[m])[:2]
    reason = f'fits {" and ".join(leading)}' + (f'; chosen by seed among {", ".join(ties)}' if len(ties) > 1 else '')
    return name, next(fit for fit, n in ranked if n == name), reason


def kit_of(palette):
    import music
    return music.PALETTES.get(palette, music.PALETTES['studio'])['kit']


def lerp(limits, k):
    low, high = limits
    return round(low + (high - low) * max(0.0, min(1.0, k)), 3)


def direct(score, profile, seed, base=None, fixed_palette=None, overrides=None):
    """Choices for every role, with reasons. `fixed_palette` is the style's own palette when the style sets one;
    `overrides` ({role: option}) wins over any choice."""
    base = base or load_base()
    overrides = dict(overrides or {})
    roles = base['roles']
    moods = profile['moods']
    choices = {}

    def take(role, allowed=None, salt=0):
        if role in overrides:
            choices[role] = {'option': overrides[role], 'why': 'set by the user'}
            return overrides[role]
        name, fit, why = choose(roles[role]['options'], profile, seed + salt, allowed)
        choices[role] = {'option': name, 'fit': fit, 'why': why}
        return name

    if fixed_palette and 'palette' not in overrides:
        palette = fixed_palette
        choices['palette'] = {'option': palette, 'why': f'the style {score.get("style")} sets its own music'}
    else:
        palette = take('palette', salt=1)
    style = score.get('style')
    if 'key' in overrides:
        key = overrides['key']
        choices['key'] = {'option': key, 'why': 'set by the user'}
    else:
        dark = (profile.get('canvasLuminance') is not None and profile['canvasLuminance'] < 0.05)
        minor = style in MINOR_STYLES or (dark and moods['technical'] + moods['bold'] > moods['calm'] + moods['playful'])
        roots = base['keys']['minor' if minor else 'major']
        key = f'{roots[(seed // 7) % len(roots)]} {"minor" if minor else "major"}'
        choices['key'] = {'option': key, 'why': ('a minor key: ' + ('the style is dark' if style in MINOR_STYLES else 'dark, technical or bold')) if minor else 'a major key for a light mood'}
    character = base['character']
    energy = (moods['bold'] + moods['technical'] + moods['playful'] - moods['calm']) / 2
    spread = character['pitch_spread_semitones']
    char = {
        'whooshBrightness': lerp(character['whoosh_brightness'], 0.5 + energy / 2),
        'whooshIntensity': lerp(character['whoosh_intensity'], 0.4 + moods['bold'] * 0.6),
        'clickSoftness': lerp(character['click_softness'], moods['calm'] - moods['bold'] * 0.5),
        'pitchSemitones': (seed // 13) % (2 * spread + 1) - spread,
    }
    return {'profile': profile, 'choices': choices, 'character': char, 'palette': palette, 'key': key}
