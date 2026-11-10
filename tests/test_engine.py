"""Sanity checks for the built-in engine: `python -m pytest tests` (or run this file)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend import lexicon_engine as le  # noqa: E402

CASES = [
    # (review, expected)
    ("The product is excellent and delivery was very fast.", "positive"),
    ("Absolutely love this blender! It crushes ice in seconds.", "positive"),
    ("Terrible experience. The package arrived damaged and support never replied.", "negative"),
    ("Complete waste of money. Stopped working after two days.", "negative"),
    ("This is not good at all.", "negative"),
    ("Not bad, actually works fine for the price.", "positive"),
    ("I wouldn't recommend this to anyone.", "negative"),
    ("Can't complain, does exactly what it says.", "positive"),
    ("It's okay. Nothing special.", "neutral"),
    ("The design is beautiful, but the battery barely lasts half a day.", "neutral"),
    ("I didn't love it, it's not very comfortable.", "negative"),
    ("Wasn't worth it, wouldn't buy again", "negative"),
    ("Did not hate it, actually quite good", "positive"),
    ("Great phone but terrible battery life and slow charging.", "negative"),
    ("Nice screen. Battery is awful. Camera is fine. Overall average.", "neutral"),
    ("I returned it. It broke within a week and the seller ignored me.", "negative"),
    ("Never disappointed with this brand, will buy again!", "positive"),
    ("LOVE IT!!! Highly recommend 😍", "positive"),
    ("Worst purchase ever. Total rip off 😡", "negative"),
    ("It arrived on Tuesday in a brown box.", "neutral"),
    ("2/5 would not buy again", "negative"),
    ("5 stars, works perfectly", "positive"),
    ("The food was cold and the waiter was rude.", "negative"),
    ("Very comfortable and the fit is perfect, super soft.", "positive"),
    ("Not worth the money, feels cheap and flimsy.", "negative"),
    ("It is not only good but great value.", "positive"),
    ("No problems at all, setup was easy.", "positive"),
    ("Doesn't work. Doesn't turn on. Useless.", "negative"),
    ("Meh. It does the job I guess.", "neutral"),
    ("Looks like a nice product", "positive"),
    ("I like it", "positive"),
]

def run():
    ok = 0
    for text, want in CASES:
        r = le.analyze(text)
        got = max(r.probabilities, key=r.probabilities.get)
        pct = r.probabilities[got] * 100
        flag = "OK " if got == want else "BAD"
        ok += got == want
        print(f"{flag} {got:8s} {pct:5.1f}%  (want {want:8s}) c={r.compound:+.2f}  {text[:70]}")
    print(f"\n{ok}/{len(CASES)} correct")
    return ok

def test_cases():
    assert run() >= len(CASES) - 2

if __name__ == "__main__":
    run()
