"""Versioned declarative effects. Manifests never contain executable/filter text."""
from functools import lru_cache
from pathlib import Path
from fc_core import fingerprint, integer, keys, number, read_json, require

PICTURE = {'brightness', 'contrast', 'saturation', 'blur', 'grayscale', 'vignette', 'pixelate', 'posterize', 'ordered_dither'}

# 4x4 Bayer thresholds; every cell of the tile is a different brightness cut, so a flat tone becomes a fixed pattern.
BAYER4 = ((0, 8, 2, 10), (12, 4, 14, 6), (3, 11, 1, 9), (15, 7, 13, 5))
AUDIO = {'highpass', 'lowpass', 'denoise'}


@lru_cache(maxsize=1)
def catalogue():
    result = {}
    for path in sorted((Path(__file__).parent / 'effects').glob('*.json')):
        spec = read_json(path)
        keys(spec, ('id', 'version', 'domain', 'parameters', 'steps', 'fixtures'), ('id', 'version', 'domain', 'parameters', 'steps', 'fixtures'))
        from fc_core import identifier
        identifier(spec['id']); integer(spec['version'], 'effect version', 1)
        require(spec['domain'] in ('picture', 'audio'), 'Unknown effect domain')
        require(isinstance(spec['parameters'], dict) and len(spec['parameters']) <= 16, 'Invalid effect parameters')
        for name, limits in spec['parameters'].items():
            identifier(name); keys(limits, ('min', 'max', 'default'), ('min', 'max', 'default'))
            number(limits['min'], name, -100000, 100000); number(limits['max'], name, limits['min'], 100000)
            number(limits['default'], name, limits['min'], limits['max'])
        require(isinstance(spec['steps'], list) and 1 <= len(spec['steps']) <= 16, 'Effect needs 1..16 steps')
        for step in spec['steps']:
            keys(step, ('op', 'value'), ('op', 'value'))
            require(step['op'] in (PICTURE if spec['domain'] == 'picture' else AUDIO), 'Unsupported effect primitive')
            value = step['value']
            if isinstance(value, dict):
                keys(value, ('param',), ('param',)); require(value['param'] in spec['parameters'], 'Unknown parameter binding')
            else:
                number(value, 'effect constant', 0, 1000)
        key = (spec['id'], spec['version'])
        require(key not in result, 'Duplicate effect ID/version')
        require(isinstance(spec['fixtures'], list) and spec['fixtures'], 'Effect requires executable fixtures')
        result[key] = spec
    return result


def resolve(applied, domain=None):
    keys(applied, ('id', 'version', 'params', 'enabled'), ('id', 'version'))
    integer(applied['version'], 'effect version', 1)
    spec = catalogue().get((applied['id'], applied['version']))
    require(spec is not None, 'Unknown effect ID/version', 'unsupported_operation')
    require(domain is None or spec['domain'] == domain, 'Effect domain does not match event')
    require(type(applied.get('enabled', True)) is bool, 'Effect enabled must be boolean')
    supplied = applied.get('params', {})
    require(isinstance(supplied, dict) and set(supplied) <= set(spec['parameters']), 'Unknown effect parameter')
    params = {key: number(supplied.get(key, lim['default']), key, lim['min'], lim['max']) for key, lim in spec['parameters'].items()}
    return spec, [{'op': step['op'], 'value': params[step['value']['param']] if isinstance(step['value'], dict) else step['value']} for step in spec['steps']]


def validate_effects(effects, domain):
    require(isinstance(effects, list) and len(effects) <= 16, 'At most 16 effects per event')
    for effect in effects:
        resolve(effect, domain)


def catalogue_info():
    specs = list(catalogue().values())
    return {'effects': specs, 'catalogue_hash': fingerprint(specs), 'customization': 'Add a versioned JSON manifest using supported primitives and executable fixtures; no scripts or arbitrary filtergraphs.'}


@lru_cache(maxsize=8)
def bayer_bias(width, height, step):
    """An 'L' image of integer offsets (128 = none) the size of the frame: the Bayer tile scaled to +-step/2, pinned to screen coordinates."""
    from PIL import Image
    rows = [bytes(128 + round(((BAYER4[y % 4][x % 4] + 0.5) / 16 - 0.5) * step) for x in range(4)) for y in range(4)]
    wide = [(row * (width // 4 + 1))[:width] for row in rows]
    return Image.frombytes('L', (width, height), b''.join(wide[y % 4] for y in range(height)))


def level_table(levels):
    step = 255 / (levels - 1)
    return [round(round(v / step) * step) for v in range(256)]


def picture(image, effects):
    from PIL import Image, ImageEnhance, ImageFilter
    for effect in effects:
        spec, steps = resolve(effect, 'picture')
        if not effect.get('enabled', True):
            continue
        for step in steps:
            name, value = step['op'], step['value']
            alpha = image.getchannel('A')
            if name in ('brightness', 'contrast', 'saturation'):
                enhancer = {'brightness': ImageEnhance.Brightness, 'contrast': ImageEnhance.Contrast, 'saturation': ImageEnhance.Color}[name]
                image = enhancer(image).enhance(value)
            elif name == 'blur':
                image = image.filter(ImageFilter.GaussianBlur(value))
            elif name == 'grayscale':
                image = Image.blend(image, image.convert('L').convert('RGBA'), value)
            elif name == 'vignette':
                width, height = image.size
                mask = Image.new('L', (128, 128))
                mask.putdata([round(255*max(0, 1-value*((x-63.5)**2+(y-63.5)**2)/(2*63.5**2))) for y in range(128) for x in range(128)])
                black = Image.new('RGBA', image.size, (0, 0, 0, 255))
                image = Image.composite(image, black, mask.resize((width, height), Image.Resampling.BILINEAR))
            elif name == 'pixelate':
                block = round(value)
                if block > 1:
                    width, height = image.size
                    small = image.resize((-(-width // block), -(-height // block)), Image.Resampling.BOX)
                    image = small.resize((small.width * block, small.height * block), Image.Resampling.NEAREST).crop((0, 0, width, height))
            elif name in ('posterize', 'ordered_dither'):
                levels = round(value)
                if levels < 256:
                    from PIL import ImageChops
                    table = level_table(levels)
                    channels = list(image.convert('RGB').split())
                    if name == 'ordered_dither':
                        bias = bayer_bias(image.width, image.height, 255 / (levels - 1))
                        channels = [ImageChops.add(c, bias, 1, -128) for c in channels]
                    image = Image.merge('RGB', [c.point(table) for c in channels]).convert('RGBA')
            image.putalpha(alpha)
    return image


def audio_filters(effects):
    filters = []
    for effect in effects:
        spec, steps = resolve(effect, 'audio')
        if effect.get('enabled', True):
            for step in steps:
                v = format(step['value'], '.12g')
                filters.append({'highpass': f'highpass=f={v}', 'lowpass': f'lowpass=f={v}', 'denoise': f'afftdn=nr={v}'}[step['op']])
    return filters


def check_fixtures():
    from fc_picture import pillow
    Image = pillow()
    checked = []
    for spec in catalogue().values():
        for i, fixture in enumerate(spec['fixtures']):
            applied = {'id': spec['id'], 'version': spec['version'], 'params': fixture.get('params', {})}
            if spec['domain'] == 'picture':
                source = Image.new('RGBA', (8, 8), tuple(fixture['input']))
                for place, colour in fixture.get('paint', {}).items():
                    source.putpixel(tuple(int(n) for n in place.split(',')), tuple(colour))
                actual = picture(source, [applied]).getpixel(tuple(fixture.get('at', [4, 4])))
                expected = fixture['expected']
                require(max(abs(a-b) for a,b in zip(actual, expected)) <= fixture.get('tolerance', 1), f"Effect fixture failed: {spec['id']}:{i}", 'qa_failed')
            else:
                actual = audio_filters([applied])
                require(actual == fixture['expected'], f"Effect fixture failed: {spec['id']}:{i}", 'qa_failed')
            checked.append({'id': spec['id'], 'version': spec['version'], 'fixture': i, 'status': 'PASS'})
    return {'status': 'PASS', 'checks': checked, 'catalogue_hash': catalogue_info()['catalogue_hash']}
