"""Built-in review analysis engine (no model file needed).

It reads a review the way a person would: it understands negation ("not good"),
intensity ("extremely slow", "LOVE it!!!"), contrast ("nice but broke in a week"),
common review idioms ("waste of money"), star mentions ("2/5"), emoji, and which
topics (delivery, quality, price ...) the customer is happy or unhappy about.

It also powers the explanations (highlighted evidence + topics) shown next to a
Keras model's verdict, so the UI looks the same with or without the model.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field

from .lexicon_data import (
    ASPECTS,
    BOOSTERS,
    CLAUSE_BREAKS,
    CONTRAST,
    EMOTES,
    FRAGMENT_SPLITTERS,
    LIKE_PRECEDERS,
    NEGATORS,
    PHRASES,
    STEM_BLOCK,
    VALENCE,
)

NEGATION_FACTOR = -0.85
CONTRAST_BEFORE = 0.6
CONTRAST_AFTER = 1.4
MAX_PHRASE_WORDS = max(len(p.split()) for p in PHRASES)
HIGHLIGHT_MIN = 0.8  # |score| needed for a word to be highlighted as evidence

_EMOTICON = r"(?::|;|=)'?-?(?:\)|\(|D(?![A-Za-z])|P(?![A-Za-z])|p(?![A-Za-z])|/(?![/A-Za-z])|\|)|<3"
_WORD = r"[A-Za-z][A-Za-z’']*(?:-[A-Za-z]+)*"
_TOKEN_RE = re.compile(
    rf"(?P<emo>{_EMOTICON})|(?P<word>{_WORD})|(?P<num>\d+(?:[./]\d+)?)|(?P<nl>\n+)|(?P<other>[^\w\s])",
    re.UNICODE,
)

_STAR_PATTERNS = [
    (re.compile(r"\b(\d(?:\.\d)?)\s*(?:/|out of)\s*5\b", re.I), 1),
    (re.compile(r"\b([1-5])\s*-?\s*stars?\b", re.I), 1),
    (re.compile(r"\b(one|two|three|four|five)\s*-?\s*stars?\b", re.I), 2),
    (re.compile(r"\b(\d{1,2})\s*/\s*10\b"), 3),
]
_WORD_NUM = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
_STAR_SCORE = {1: -3.4, 2: -2.0, 3: 0.0, 4: 2.0, 5: 3.4}


@dataclass
class Token:
    text: str
    low: str
    start: int
    end: int
    kind: str  # word | num | emo | other | nl
    value: float = 0.0          # sentiment contribution after modifiers
    span_start: int | None = None  # highlight start (extended back over a negator)
    span_end: int | None = None
    consumed: bool = False      # part of a multi-word phrase already scored
    self_negated: bool = False  # phrase already contains its own negation ("not worth it")
    sentence: int = 0
    fragment: int = 0


@dataclass
class Analysis:
    probabilities: dict[str, float]
    compound: float
    highlights: list[dict] = field(default_factory=list)
    aspects: list[dict] = field(default_factory=list)
    signal: float = 0.0        # how much sentiment evidence was found


def _norm(word: str) -> str:
    return word.lower().replace("’", "'")


def _lookup(word: str) -> float | None:
    """Sentiment value of a word, tolerating simple inflections."""
    v = VALENCE.get(word)
    if v is not None:
        return v
    if word in STEM_BLOCK or len(word) < 5:
        return None
    for suffix in ("ly", "ing", "ed", "es", "s", "d"):
        if word.endswith(suffix):
            base = word[: -len(suffix)]
            if len(base) < 3:
                continue
            for cand in (base, base + "e"):
                if cand in VALENCE:
                    return VALENCE[cand] * 0.95
            if len(base) > 3 and base[-1] == base[-2] and base[:-1] in VALENCE:  # stopped -> stop
                return VALENCE[base[:-1]] * 0.95
    return None


def tokenize(text: str) -> list[Token]:
    tokens: list[Token] = []
    for m in _TOKEN_RE.finditer(text):
        kind = m.lastgroup or "other"
        raw = m.group()
        tokens.append(Token(raw, _norm(raw), m.start(), m.end(), kind))
    return tokens


def _is_break(tok: Token) -> bool:
    return tok.kind == "nl" or tok.low in CLAUSE_BREAKS or tok.low in CONTRAST


def _score_phrases(tokens: list[Token]) -> None:
    """Find multi-word idioms first so their words aren't scored one by one."""
    words = [t.low for t in tokens]
    i = 0
    while i < len(tokens):
        hit = None
        if tokens[i].kind == "word":
            for n in range(min(MAX_PHRASE_WORDS, len(tokens) - i), 1, -1):
                window = tokens[i : i + n]
                if any(t.kind != "word" for t in window):
                    continue
                key = " ".join(words[i : i + n])
                if key in PHRASES:
                    hit = (n, PHRASES[key])
                    break
        if hit:
            n, score = hit
            tokens[i].value = score
            tokens[i].span_start, tokens[i].span_end = tokens[i].start, tokens[i + n - 1].end
            for t in tokens[i + 1 : i + n]:
                t.consumed = True
            tokens[i].consumed = False
            tokens[i].kind = "phrase"
            tokens[i].self_negated = any(
                w in NEGATORS or w.endswith("n't") for w in words[i : i + n]
            )
            i += n
        else:
            i += 1


def _modifiers_before(tokens: list[Token], i: int) -> tuple[float, int | None]:
    """Return (booster multiplier, index of a negator) for the 3 words before i."""
    mult = 1.0
    neg_idx = None
    decay = 1.0
    for back in range(1, 4):
        j = i - back
        if j < 0:
            break
        t = tokens[j]
        if _is_break(t):
            break
        if t.consumed or t.kind == "phrase":
            continue
        if t.kind == "word":
            if t.low in BOOSTERS:
                mult *= 1 + (BOOSTERS[t.low] - 1) * decay
                decay *= 0.8
            elif (t.low in NEGATORS or t.low.endswith("n't")) and neg_idx is None:
                nxt = tokens[j + 1].low if j + 1 < len(tokens) else ""
                if not (t.low == "not" and nxt == "only"):
                    neg_idx = j
    return min(mult, 1.8), neg_idx


def _score_tokens(tokens: list[Token], text: str) -> None:
    has_lower = any(c.islower() for c in text)
    for i, tok in enumerate(tokens):
        if tok.consumed:
            continue
        base: float | None = None
        if tok.kind == "phrase":
            base = tok.value
        elif tok.kind == "emo" or tok.kind == "other":
            base = EMOTES.get(tok.low) if tok.low in EMOTES else EMOTES.get(tok.text)
        elif tok.kind == "word":
            if tok.low == "like":
                prev = tokens[i - 1].low if i else ""
                base = VALENCE["like"] if prev in LIKE_PRECEDERS else None
            else:
                base = _lookup(tok.low)
        if base is None:
            tok.value = 0.0
            continue

        mult, neg_idx = _modifiers_before(tokens, i)
        value = base * mult
        span_start = tok.span_start if tok.span_start is not None else tok.start
        span_end = tok.span_end if tok.span_end is not None else tok.end
        if neg_idx is not None and not tok.self_negated:
            value *= NEGATION_FACTOR
            span_start = min(span_start, tokens[neg_idx].start)
        if tok.kind == "word" and has_lower and tok.text.isupper() and len(tok.text) >= 3:
            value *= 1.15  # SHOUTING
        tok.value, tok.span_start, tok.span_end = value, span_start, span_end


def _apply_contrast(tokens: list[Token]) -> None:
    """'Great screen BUT it died in a week': what follows 'but' matters more."""
    last = None
    for i, t in enumerate(tokens):
        if t.kind == "word" and t.low in CONTRAST:
            last = i
    if last is None:
        return
    for i, t in enumerate(tokens):
        if i < last:
            t.value *= CONTRAST_BEFORE
        elif i > last:
            t.value *= CONTRAST_AFTER


def _assign_clauses(tokens: list[Token]) -> None:
    sentence = fragment = 0
    for t in tokens:
        t.sentence, t.fragment = sentence, fragment
        if t.kind == "nl" or t.low in {".", "!", "?", ";"} or t.low in CONTRAST:
            sentence += 1
            fragment += 1
        elif t.low in CLAUSE_BREAKS or t.low in FRAGMENT_SPLITTERS:
            fragment += 1


def _star_bonus(text: str) -> tuple[float, list[dict]]:
    total, marks = 0.0, []
    for pattern, mode in _STAR_PATTERNS:
        for m in pattern.finditer(text):
            raw = m.group(1).lower()
            if mode == 1:
                stars = round(float(raw))
            elif mode == 2:
                stars = _WORD_NUM[raw]
            else:
                stars = round(float(raw) / 2)
            stars = max(1, min(5, stars))
            score = _STAR_SCORE[stars]
            total += score
            if abs(score) >= HIGHLIGHT_MIN:
                marks.append({"start": m.start(), "end": m.end(),
                              "polarity": "positive" if score > 0 else "negative"})
    return total, marks


def _aspects(tokens: list[Token]) -> list[dict]:
    frag_score: dict[int, float] = {}
    sent_score: dict[int, float] = {}
    for t in tokens:
        frag_score[t.fragment] = frag_score.get(t.fragment, 0.0) + t.value
        sent_score[t.sentence] = sent_score.get(t.sentence, 0.0) + t.value

    found: dict[str, list[float]] = {}
    for t in tokens:
        if t.kind not in {"word", "phrase"}:
            continue
        for name, keywords in ASPECTS.items():
            if t.low in keywords:
                score = frag_score[t.fragment]
                if abs(score) < 0.5:  # nothing said in this fragment: use the sentence mood
                    score = sent_score[t.sentence] * 0.7
                found.setdefault(name, []).append(score)

    out = []
    for name, scores in found.items():
        # one entry per fragment would double-count repeated keywords
        uniq = sorted(set(round(s, 2) for s in scores))
        has_pos = any(s >= 0.8 for s in uniq)
        has_neg = any(s <= -0.8 for s in uniq)
        total = sum(uniq)
        if has_pos and has_neg:
            sentiment, mixed = "neutral", True
        elif total >= 0.8:
            sentiment, mixed = "positive", False
        elif total <= -0.8:
            sentiment, mixed = "negative", False
        else:
            sentiment, mixed = "neutral", False
        out.append({"name": name, "sentiment": sentiment, "mixed": mixed, "_w": abs(total)})
    out.sort(key=lambda a: -a["_w"])
    for a in out:
        a.pop("_w")
    return out[:6]


def _probabilities(compound: float, pos_mass: float, neg_mass: float) -> dict[str, float]:
    mixed = 0.0
    if pos_mass >= 1.2 and neg_mass >= 1.2:
        mixed = min(pos_mass, neg_mass) / max(pos_mass, neg_mass)
    k = 3.6
    z_pos = k * compound
    z_neg = -k * compound
    z_neu = 1.0 - 3.2 * abs(compound) + 2.2 * mixed
    m = max(z_pos, z_neg, z_neu)
    exps = [math.exp(z - m) for z in (z_neg, z_neu, z_pos)]
    s = sum(exps)
    neg, neu, pos = (e / s for e in exps)
    return {"negative": neg, "neutral": neu, "positive": pos}


def analyze(text: str) -> Analysis:
    tokens = tokenize(text)
    _score_phrases(tokens)
    _score_tokens(tokens, text)
    _assign_clauses(tokens)

    raw_pos = sum(t.value for t in tokens if t.value > 0)
    raw_neg = -sum(t.value for t in tokens if t.value < 0)

    _apply_contrast(tokens)
    total = sum(t.value for t in tokens)

    star_total, star_marks = _star_bonus(text)
    total += star_total
    raw_pos += max(star_total, 0)
    raw_neg += max(-star_total, 0)

    exclam = min(text.count("!"), 4)
    if total:
        total *= 1 + 0.07 * exclam
    compound = total / math.sqrt(total * total + 18.0)

    highlights = list(star_marks)
    for t in tokens:
        if abs(t.value) >= HIGHLIGHT_MIN and not t.consumed and t.span_start is not None:
            highlights.append({
                "start": t.span_start,
                "end": t.span_end,
                "polarity": "positive" if t.value > 0 else "negative",
            })
    highlights.sort(key=lambda h: h["start"])
    merged: list[dict] = []
    for h in highlights:  # drop overlaps
        if merged and h["start"] < merged[-1]["end"]:
            continue
        merged.append(h)

    return Analysis(
        probabilities=_probabilities(compound, raw_pos, raw_neg),
        compound=compound,
        highlights=merged,
        aspects=_aspects(tokens),
        signal=raw_pos + raw_neg,
    )
