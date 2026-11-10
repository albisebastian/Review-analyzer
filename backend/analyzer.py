"""Ties the engines together and produces the response shown in the UI."""

from __future__ import annotations

import os
import re

from . import lexicon_engine
from .keras_engine import KerasEngine

MAX_CHARS = 5000
# 0 = trust the Keras model completely (default). Raise towards 1 to blend in the
# rule-based engine, which is better at negation and mixed opinions on short texts.
LEXICON_BLEND = min(max(float(os.environ.get("LEXICON_BLEND", "0")), 0.0), 1.0)

LABELS = ("negative", "neutral", "positive")


class ReviewError(ValueError):
    """The submitted text can't be analysed (message is safe to show to the user)."""


def _join(names: list[str]) -> str:
    names = [n.lower() for n in names]
    if len(names) <= 1:
        return "".join(names)
    return ", ".join(names[:-1]) + " and " + names[-1]


def _insight(label: str, aspects: list[dict]) -> str:
    pos = [a["name"] for a in aspects if a["sentiment"] == "positive"]
    neg = [a["name"] for a in aspects if a["sentiment"] == "negative"]
    mixed = [a["name"] for a in aspects if a["mixed"]]
    if label == "positive":
        if pos and neg:
            return f"Happy overall. Praises {_join(pos)}, but flags {_join(neg)}."
        if pos:
            return f"Happy customer. Praises {_join(pos)}."
        if neg:
            return f"Positive overall, though {_join(neg)} drew some criticism."
        return "Happy customer. No specific topic is called out."
    if label == "negative":
        if neg and pos:
            return f"Unhappy overall. Complains about {_join(neg)}, despite liking {_join(pos)}."
        if neg:
            return f"Unhappy customer. Main complaints: {_join(neg)}."
        return "Unhappy customer. No specific topic is called out."
    if pos and neg:
        return f"Mixed feelings. Likes {_join(pos)} but is let down by {_join(neg)}."
    if mixed:
        return f"Balanced opinion, with {_join(mixed)} getting both praise and criticism."
    if pos or neg:
        return "Fairly balanced. Opinions are mild rather than strong."
    return "Neutral. The review states facts or shows little strong emotion."


class ReviewAnalyzer:
    def __init__(self) -> None:
        self.keras = KerasEngine()
        self.keras.load()

    def reload(self) -> dict:
        self.keras.load()
        return self.status()

    def status(self) -> dict:
        k = self.keras.status()
        return {
            "engine": "keras" if k["loaded"] else "builtin",
            "engine_label": "Keras model" if k["loaded"] else "Built-in engine",
            "lexicon_blend": LEXICON_BLEND if k["loaded"] else None,
            "keras": k,
        }

    def analyze(self, text: str) -> dict:
        text = (text or "").replace("\r\n", "\n").strip()
        if len(re.findall(r"[A-Za-z]", text)) < 3:
            raise ReviewError("Please enter a review with at least a few words.")
        if len(text) > MAX_CHARS:
            raise ReviewError(f"That review is too long. Keep it under {MAX_CHARS:,} characters.")

        rules = lexicon_engine.analyze(text)
        if self.keras.ready:
            scores = self.keras.predict(text)
            if LEXICON_BLEND:
                scores = {k: (1 - LEXICON_BLEND) * scores[k] + LEXICON_BLEND * rules.probabilities[k]
                          for k in LABELS}
            engine = "keras"
        else:
            scores, engine = rules.probabilities, "builtin"

        label = max(LABELS, key=lambda k: scores[k])
        return {
            "sentiment": label,
            "percentage": min(round(scores[label] * 100, 1), 99.9),  # never claim 100% certainty
            "engine": engine,
            "insight": _insight(label, rules.aspects),
            "highlights": rules.highlights,
            "aspects": rules.aspects,
            "word_count": len(text.split()),
            # kept for API users; the web UI deliberately shows only the winning sentiment
            "scores": {k: round(v * 100, 1) for k, v in scores.items()},
        }
