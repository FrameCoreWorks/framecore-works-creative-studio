"""Cue sheet, pronunciation lexicon and narration.lock.json. Standard library only."""
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path

LOCK_NAME = 'narration.lock.json'
VOICE_DESCRIPTION = re.compile(r'^\([^)]*\)')
SAFE_ID = re.compile(r'^[A-Za-z0-9][A-Za-z0-9._-]*$')


class CueError(ValueError):
    pass


@dataclass
class Cue:
    id: str
    text: str
    max_seconds: float
    voice_notes: str | None = None


def load_cues(path):
    try:
        data = json.loads(Path(path).read_text(encoding='utf-8'))
    except (OSError, ValueError) as error:
        raise CueError(f'cannot read cue sheet {path}: {error}') from None
    if isinstance(data, dict):
        data = data.get('lines')
    if not isinstance(data, list) or not data:
        raise CueError(f'cue sheet {path} has no lines')
    cues, seen = [], set()
    for index, item in enumerate(data):
        line_id = str(item.get('id', '')).strip() if isinstance(item, dict) else ''
        if not line_id:
            raise CueError(f'line {index + 1} has no id')
        if not SAFE_ID.match(line_id) or '..' in line_id:
            raise CueError(f'line id {line_id!r} must use only letters, digits, dot, dash and underscore')
        if line_id in seen:
            raise CueError(f'duplicate line id {line_id}')
        seen.add(line_id)
        text = item.get('text')
        if not isinstance(text, str) or not text.strip():
            raise CueError(f'line {line_id} has no text')
        limit = item.get('max_seconds')
        if isinstance(limit, bool) or not isinstance(limit, (int, float)) or limit <= 0:
            raise CueError(f'line {line_id} needs a positive max_seconds')
        cues.append(Cue(line_id, text, float(limit), item.get('voice_notes')))
    return cues


def load_lexicon(path):
    if path is None:
        return {}, None
    raw = Path(path).read_bytes()
    entries = json.loads(raw.decode('utf-8'))
    if not isinstance(entries, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in entries.items()):
        raise CueError(f'lexicon {path} must map words to spoken forms')
    folded = {}
    for key in entries:
        if key.lower() in folded:
            raise CueError(f'lexicon {path} has {folded[key.lower()]} and {key}, which differ only in case')
        folded[key.lower()] = key
    return entries, hashlib.sha256(raw).hexdigest()


def apply_lexicon(text, lexicon):
    """Whole-word, case-insensitive, longest key first; a leading (voice description) is left unchanged."""
    match = VOICE_DESCRIPTION.match(text.lstrip())
    if match:
        offset = len(text) - len(text.lstrip())
        match_end = offset + match.end()
    head, body = (text[:match_end], text[match_end:]) if match else ('', text)
    keys = sorted((k for k in lexicon if k.strip()), key=len, reverse=True)
    if not keys:
        return text
    by_lower = {k.lower(): lexicon[k] for k in keys}
    pattern = re.compile(r'(?<!\w)(' + '|'.join(re.escape(k) for k in keys) + r')(?!\w)', re.IGNORECASE)
    return head + pattern.sub(lambda m: by_lower[m.group(0).lower()], body)


class Lock:
    def __init__(self, out_dir, data):
        self.path = Path(out_dir) / LOCK_NAME
        self.lines = data.get('lines', {})

    @classmethod
    def load(cls, out_dir):
        path = Path(out_dir) / LOCK_NAME
        try:
            data = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
            if not isinstance(data, dict) or not isinstance(data.get('lines', {}), dict):
                raise ValueError('not a lock object')
        except (OSError, ValueError) as error:
            raise CueError(f'cannot read {path}: {error}') from None
        return cls(out_dir, data)

    def set_line(self, line_id, **fields):
        self.lines.setdefault(line_id, {}).update(fields)

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        data = {'version': 1, 'lines': self.lines}
        self.path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
