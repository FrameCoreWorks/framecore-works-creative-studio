"""Align a known script to timed speech: the script is the authority on spelling, speech recognition on timing.

Needleman-Wunsch over normalised words (case, punctuation and diacritics folded for matching only). A matched script word takes the
heard word's times; a script word between two matched neighbours is interpolated by its length; a script word without an anchor on
both sides stays untimed and is reported. Nothing is guessed silently, and a script that barely matches the speech is refused."""
from __future__ import annotations

import difflib
import re
import unicodedata

from fc_core import FrameCutError, require

MAX_WORDS = 6000          # the alignment table is quadratic
MATCH_THRESHOLD = 0.72    # similarity needed to anchor two words; words of one or two letters must be equal
GAP = -0.4
MIN_WORD_SECONDS = 0.04

_FOLD = str.maketrans({"ł": "l", "Ł": "l", "ø": "o", "Ø": "o", "đ": "d", "Đ": "d", "ß": "ss"})


def fold(word):
    """Matching key: NFKC, casefold, no marks (so ą matches a), no punctuation."""
    text = unicodedata.normalize("NFKC", word).translate(_FOLD).casefold()
    text = "".join(c for c in unicodedata.normalize("NFD", text) if not unicodedata.combining(c))
    return re.sub(r"[^\w]+", "", text, flags=re.UNICODE)


def similarity(a, b):
    if not a or not b:
        return 0.0
    if a == b:
        return 1.0
    if min(len(a), len(b)) <= 2:
        return 0.0
    return difflib.SequenceMatcher(None, a, b).ratio()


def pairs(script_keys, heard_keys):
    """Global alignment; returns {script index: heard index} for anchored words, in order."""
    n, m = len(script_keys), len(heard_keys)
    score = [[0.0] * (m + 1) for _ in range(n + 1)]
    move = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        score[i][0], move[i][0] = i * GAP, 1
    for j in range(1, m + 1):
        score[0][j], move[0][j] = j * GAP, 2
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            s = similarity(script_keys[i - 1], heard_keys[j - 1])
            options = (score[i - 1][j - 1] + (2 * s - 1 if s >= MATCH_THRESHOLD else -1.0), score[i - 1][j] + GAP, score[i][j - 1] + GAP)
            best = max(range(3), key=lambda k: options[k])
            score[i][j], move[i][j] = options[best], best
    found, i, j = {}, n, m
    while i > 0 or j > 0:
        step = move[i][j] if i > 0 and j > 0 else (1 if i > 0 else 2)
        if step == 0:
            if similarity(script_keys[i - 1], heard_keys[j - 1]) >= MATCH_THRESHOLD:
                found[i - 1] = j - 1
            i, j = i - 1, j - 1
        elif step == 1:
            i -= 1
        else:
            j -= 1
    return found


def align_script(heard, script, minimum=0.6):
    """`heard`: timed words (text, start, end); `script`: the known text. Returns {'words': [...], 'report': {...}}."""
    tokens = script.split()
    require(tokens, "The script has no words")
    timed = [w for w in heard if w.get("start") is not None and w.get("end") is not None]
    require(timed, "The transcript has no word timing to align to")
    require(len(tokens) <= MAX_WORDS and len(timed) <= MAX_WORDS, f"Script or transcript exceeds {MAX_WORDS} words; align it in parts", "resource_limit")
    script_keys = [fold(t) for t in tokens]
    heard_keys = [fold(w["text"]) for w in timed]
    found = pairs(script_keys, heard_keys)
    words = []
    for index, token in enumerate(tokens):
        word = {"id": f"s{index:06d}", "text": token, "start": None, "end": None, "verbatim": token, "alignment": "unaligned",
                "speaker": None, "confidence": None}
        if index in found:
            source = timed[found[index]]
            word.update(start=source["start"], end=source["end"], verbatim=source["text"], alignment="matched",
                        confidence=source.get("confidence"), speaker=source.get("speaker"))
        words.append(word)
    # Unmatched words between two anchors share the gap in proportion to their length; the others stay untimed.
    anchors = [i for i, w in enumerate(words) if w["alignment"] == "matched"]
    for left, right in zip(anchors, anchors[1:]):
        gap = list(range(left + 1, right))
        if not gap:
            continue
        begin, finish = words[left]["end"], words[right]["start"]
        span = finish - begin
        if span < MIN_WORD_SECONDS * len(gap):
            continue
        total = sum(max(1, len(fold(tokens[i]))) for i in gap)
        spare = span - MIN_WORD_SECONDS * len(gap)   # every word gets a minimum, the rest is shared by length
        cursor = begin
        for i in gap:
            share = MIN_WORD_SECONDS + spare * max(1, len(fold(tokens[i]))) / total
            words[i].update(start=round(cursor, 3), end=round(cursor + share, 3), alignment="interpolated")
            cursor += share
    matched = sum(1 for w in words if w["alignment"] == "matched")
    interpolated = sum(1 for w in words if w["alignment"] == "interpolated")
    unaligned = [{"index": i, "text": w["text"]} for i, w in enumerate(words) if w["alignment"] == "unaligned"]
    extra = [timed[j]["text"] for j in range(len(timed)) if j not in set(found.values())]
    coverage = round((matched + interpolated) / len(words), 4)
    report = {"status": "aligned", "script_words": len(words), "heard_words": len(timed), "matched": matched, "interpolated": interpolated,
              "coverage": coverage, "matched_share": round(matched / len(words), 4), "unaligned": unaligned[:50],
              "unaligned_total": len(unaligned), "heard_not_in_script": extra[:50], "heard_not_in_script_total": len(extra),
              "needs_review": coverage < 0.85 or bool(unaligned)}
    require(matched / len(words) >= minimum,
            f"Only {round(100 * matched / len(words))}% of the script matched the speech ({matched} of {len(words)} words); check that the script is "
            f"what was said or fix the transcript (first unmatched: {', '.join(w['text'] for w in words if w['alignment'] != 'matched')[:120]})", "qa_failed")
    return {"words": words, "report": report}
