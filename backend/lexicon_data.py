"""Word lists for the built-in review analysis engine.

Scores are on a roughly -3.5 .. +3.5 scale (negative = unhappy customer).
Edit freely: this file is plain data, no code.
"""

# --------------------------------------------------------------------------
# Single-word sentiment values
# --------------------------------------------------------------------------
_POSITIVE = {
    "amazing": 3.0, "awesome": 3.1, "excellent": 3.2, "fantastic": 3.2, "great": 2.8,
    "perfect": 3.2, "outstanding": 3.2, "superb": 3.2, "wonderful": 3.0, "brilliant": 3.0,
    "incredible": 3.0, "phenomenal": 3.2, "exceptional": 3.0, "flawless": 3.0, "stunning": 2.8,
    "love": 3.0, "loved": 3.0, "loves": 3.0, "loving": 2.5, "adore": 3.0, "adored": 3.0,
    "best": 2.9, "better": 1.6, "good": 2.0, "nice": 1.8, "happy": 2.5, "pleased": 2.2,
    "satisfied": 2.0, "satisfying": 2.0, "satisfactory": 1.2, "delighted": 3.0, "thrilled": 3.0,
    "impressed": 2.5, "impressive": 2.5, "recommend": 2.2, "recommended": 2.2,
    "helpful": 2.2, "friendly": 2.0, "courteous": 2.0, "polite": 1.6, "professional": 1.8,
    "knowledgeable": 1.8, "attentive": 1.8, "trustworthy": 2.0, "legit": 1.6,
    "fast": 1.6, "quick": 1.6, "quickly": 1.5, "prompt": 1.8, "promptly": 1.8, "swift": 1.6,
    "speedy": 1.8, "timely": 1.6, "early": 0.8,
    "easy": 1.8, "effortless": 2.2, "smooth": 1.8, "seamless": 2.2, "intuitive": 2.0,
    "user-friendly": 2.2, "convenient": 1.8, "handy": 1.8, "useful": 1.8,
    "comfortable": 2.0, "comfy": 2.0, "sturdy": 2.0, "durable": 2.1, "solid": 1.8,
    "reliable": 2.2, "premium": 1.8, "well-made": 2.4, "top-notch": 3.0, "high-quality": 2.6,
    "beautiful": 2.6, "gorgeous": 2.8, "stylish": 2.0, "sleek": 1.8, "elegant": 2.2,
    "lovely": 2.4, "cute": 1.6, "fresh": 1.5, "crisp": 1.6, "spotless": 2.0, "clean": 1.2,
    "delicious": 3.0, "tasty": 2.4, "yummy": 2.5, "flavorful": 2.2, "flavourful": 2.2,
    "worthwhile": 2.0, "affordable": 1.8, "inexpensive": 1.2, "bargain": 2.0,
    "fine": 1.0, "decent": 1.2, "okay": 0.4, "ok": 0.4, "alright": 0.5, "acceptable": 0.6,
    "enjoy": 2.3, "enjoyed": 2.3, "enjoying": 2.3, "enjoyable": 2.3, "fun": 2.0,
    "glad": 2.0, "excited": 2.0, "exceeded": 2.4, "ideal": 2.2, "superior": 2.4,
    "powerful": 1.8, "responsive": 1.8, "accurate": 1.6, "quiet": 1.0, "lightweight": 1.2,
    "spacious": 1.4, "thank": 1.5, "thanks": 1.5, "thankful": 2.0, "appreciate": 2.0,
    "appreciated": 2.0, "kudos": 2.0, "bravo": 2.2, "wow": 2.2, "yay": 2.2, "cool": 1.6,
    "neat": 1.6, "super": 2.2, "favorite": 2.4, "favourite": 2.4, "pleasant": 2.0,
    "refreshing": 1.8, "winner": 2.4, "gem": 2.2, "improved": 1.6, "improvement": 1.2,
    "success": 1.6, "successful": 1.8, "safe": 1.2, "secure": 1.2, "authentic": 1.2,
    "well": 0.8, "nicely": 1.8, "perfectly": 3.0, "beautifully": 2.8, "flawlessly": 3.0,
    "wonderfully": 3.0, "happily": 2.0, "like": 1.2, "liked": 1.8, "likes": 1.4,
    "positive": 1.6, "relieved": 1.2, "pros": 1.0,
}

_NEGATIVE = {
    "terrible": -3.2, "horrible": -3.2, "awful": -3.2, "bad": -2.4, "worst": -3.4,
    "worse": -2.2, "poor": -2.2, "poorly": -2.2, "lousy": -2.4, "dreadful": -3.0,
    "atrocious": -3.4, "abysmal": -3.4, "appalling": -3.2, "horrific": -3.4,
    "disappointing": -2.6, "disappointed": -2.6, "disappointment": -2.6, "letdown": -2.4,
    "underwhelming": -2.2, "underwhelmed": -2.2, "overrated": -2.2,
    "useless": -3.0, "worthless": -3.0, "garbage": -3.0, "trash": -2.8, "junk": -2.8,
    "crap": -2.8, "crappy": -2.8, "rubbish": -2.6, "pathetic": -3.0, "shoddy": -2.6,
    "disgusting": -3.2, "disgusted": -3.0, "gross": -2.8, "nasty": -2.8, "filthy": -2.8,
    "hate": -3.0, "hated": -3.0, "hates": -3.0, "dislike": -2.0, "disliked": -2.0,
    "annoying": -2.2, "annoyed": -2.2, "frustrating": -2.6, "frustrated": -2.6,
    "angry": -2.6, "furious": -3.0, "upset": -2.2, "unhappy": -2.4, "dissatisfied": -2.4,
    "unsatisfied": -2.4, "sad": -2.0, "sadly": -1.6, "unfortunately": -1.6,
    "regret": -2.4, "regretted": -2.4, "waste": -2.6, "wasted": -2.6, "wastes": -2.6,
    "scam": -3.4, "fraud": -3.4, "fake": -2.6, "counterfeit": -3.0, "rip-off": -3.2,
    "ripoff": -3.2, "overpriced": -2.4, "expensive": -1.4, "pricey": -1.2, "cheap": -1.2,
    "cheaply": -1.6, "flimsy": -2.4, "fragile": -1.4, "broke": -2.4, "broken": -2.6,
    "breaks": -2.2, "defective": -3.0, "defect": -2.6, "faulty": -2.8, "damaged": -2.6,
    "damage": -2.2, "cracked": -2.4, "scratched": -1.8, "dented": -1.8, "torn": -2.0,
    "ripped": -2.0, "leaking": -2.4, "leaks": -2.2, "leaked": -2.2, "stuck": -1.4,
    "jammed": -1.8, "dead": -2.2, "died": -2.4, "fails": -2.4, "failed": -2.4,
    "failure": -2.6, "failing": -2.2, "fail": -2.4, "malfunction": -2.6,
    "malfunctioning": -2.6, "crash": -2.0, "crashes": -2.2, "crashed": -2.2,
    "freezes": -2.2, "froze": -2.2, "glitch": -2.0, "glitchy": -2.2, "buggy": -2.4,
    "bug": -1.4, "bugs": -1.6, "laggy": -2.2, "lag": -1.8, "slow": -1.8, "slowly": -1.5,
    "sluggish": -2.0, "late": -1.8, "delayed": -2.0, "delay": -1.6, "missing": -2.0,
    "lost": -2.0, "wrong": -2.0, "incorrect": -1.8, "ruined": -3.0, "ruin": -2.6,
    "unusable": -3.0, "unreliable": -2.6, "uncomfortable": -2.4, "painful": -2.4,
    "noisy": -1.8, "smelly": -2.2, "stinks": -2.6, "stink": -2.4, "dirty": -2.2,
    "stale": -2.2, "rotten": -3.0, "bland": -1.8, "tasteless": -2.2,
    "rude": -2.8, "unhelpful": -2.4, "unprofessional": -2.6, "unfriendly": -2.2,
    "ignored": -2.2, "ignoring": -2.2, "refused": -2.0, "careless": -1.8, "lazy": -1.8,
    "incompetent": -3.0, "dishonest": -2.8, "misleading": -2.4, "false": -1.8,
    "lie": -2.4, "lied": -2.6, "lying": -2.6,
    "problem": -1.6, "problems": -1.8, "issue": -1.2, "issues": -1.4, "trouble": -1.6,
    "complaint": -1.6, "complaints": -1.6, "complain": -1.6, "complained": -1.8,
    "hassle": -1.8, "difficult": -1.6, "confusing": -2.0, "complicated": -1.6,
    "cumbersome": -2.0, "clunky": -2.2, "bulky": -1.4, "weak": -1.8,
    "boring": -2.0, "dull": -1.6, "mediocre": -1.4, "subpar": -2.0, "inferior": -2.2,
    "lacking": -1.8, "lack": -1.6, "lacks": -1.8, "worried": -1.4, "concerned": -1.2,
    "ugly": -2.4, "hideous": -3.0, "faded": -1.6, "fading": -1.6, "tacky": -1.8,
    "overheating": -2.2, "overheats": -2.2, "refund": -0.8, "returned": -1.4,
    "returning": -1.2, "cancelled": -1.6, "canceled": -1.6, "avoid": -2.2, "beware": -2.4,
    "unacceptable": -3.0, "outrageous": -2.6, "ridiculous": -2.2, "joke": -2.0,
    "nightmare": -3.0, "disaster": -3.2, "mess": -2.0, "stressful": -2.2,
    "sucks": -3.0, "suck": -2.6, "sucked": -2.8, "negative": -1.6, "cons": -1.0,
    "badly": -2.4, "scratchy": -1.8, "itchy": -1.6, "cheaper": -0.4,
}

VALENCE: dict[str, float] = {**_POSITIVE, **_NEGATIVE}

# Words that must never be derived from another word by stripping a suffix.
STEM_BLOCK = {"lately", "likely", "unlikely", "family", "only", "early", "daily", "really",
              "actually", "mostly", "finally", "totally", "usually", "ready"}

# "like" is only a sentiment word in "I like it"-style contexts, not in "looks like".
LIKE_PRECEDERS = {"i", "we", "they", "you", "really", "also", "definitely", "absolutely",
                  "truly", "totally", "would", "will", "do", "did", "still", "quite", "kinda"}

# --------------------------------------------------------------------------
# Multi-word phrases (checked first, longest match wins)
# --------------------------------------------------------------------------
PHRASES: dict[str, float] = {
    # recommendations
    "highly recommend": 3.4, "would recommend": 2.6, "can't recommend enough": 3.4,
    "cannot recommend enough": 3.4, "would not recommend": -3.2, "wouldn't recommend": -3.2,
    "do not recommend": -3.2, "don't recommend": -3.2, "not recommend": -3.0,
    "can't recommend": -3.0, "cannot recommend": -3.0, "not recommended": -3.0,
    "would buy again": 2.6, "will buy again": 2.6, "buy again": 1.6, "will definitely buy": 2.4,
    "never buy again": -3.2, "will not buy": -2.8, "won't buy": -2.6, "never again": -3.0,
    # value
    "worth every penny": 3.0, "worth the money": 2.2, "worth it": 2.0, "money well spent": 2.6,
    "good value": 2.2, "great value": 2.8, "not worth": -2.4, "not worth it": -2.8,
    "not worth the money": -3.0, "waste of money": -3.4, "waste of time": -3.2,
    "rip off": -3.2, "total waste": -3.4, "complete waste": -3.4, "good for the price": 1.8,
    # function
    "works great": 3.0, "works perfectly": 3.2, "works well": 2.2, "works fine": 1.6,
    "work great": 3.0, "worked great": 3.0, "worked perfectly": 3.2, "worked well": 2.2,
    "stopped working": -3.2, "stopped functioning": -3.2, "doesn't work": -3.0,
    "does not work": -3.0, "didn't work": -3.0, "did not work": -3.0, "not working": -2.8,
    "no longer works": -2.8, "no longer work": -2.8, "won't turn on": -3.0,
    "doesn't turn on": -3.0, "stopped charging": -3.0, "won't charge": -3.0,
    "fell apart": -3.0, "falls apart": -3.0, "fall apart": -2.8, "broke after": -2.8,
    "piece of junk": -3.4, "piece of crap": -3.4, "piece of garbage": -3.4,
    # expectation
    "as described": 1.4, "exactly as described": 2.4, "as expected": 1.2,
    "not as described": -2.6, "not as expected": -2.4, "not what i expected": -2.4,
    "better than expected": 2.8, "exceeded my expectations": 3.0, "exceeded expectations": 3.0,
    "worse than expected": -2.8, "below expectations": -2.4, "could be better": -1.0,
    "could have been better": -1.2, "nothing special": -0.6, "so-so": -0.2, "so so": -0.2,
    "no good": -2.4, "not good enough": -2.4, "not great": -2.0, "not bad": 1.4,
    "not too bad": 1.4, "not that bad": 1.0, "not terrible": 0.8,
    # no-problem family
    "no problem": 1.8, "no problems": 1.8, "no issues": 1.6, "no issue": 1.6,
    "no complaints": 2.0, "can't complain": 1.8, "cannot complain": 1.8, "nothing wrong": 1.5,
    "can't go wrong": 2.8, "can't fault": 2.2, "couldn't be happier": 3.2,
    "not disappointed": 2.0, "never disappointed": 2.4, "never disappoints": 2.6,
    "no regrets": 2.2, "so far so good": 2.0,
    # love / hate
    "love it": 3.2, "love this": 3.2, "loved it": 3.2, "love them": 3.0, "hate it": -3.2,
    "hate this": -3.2, "game changer": 2.6, "game-changer": 2.6, "life saver": 2.8,
    "lifesaver": 2.8, "top notch": 3.0, "five stars": 3.2, "one star": -3.2,
    "highly satisfied": 3.0, "very satisfied": 2.8, "very happy": 3.0, "very disappointed": -3.2,
    "let down": -2.4, "fed up": -2.8, "sick of": -2.4, "took forever": -2.6,
    "customer service was terrible": -3.0, "poor customer service": -3.0,
    "great customer service": 3.0, "excellent customer service": 3.2,
    "terrible customer service": -3.2, "bad customer service": -3.0,
    # delivery
    "fast shipping": 2.4, "fast delivery": 2.4, "quick delivery": 2.4, "quick shipping": 2.4,
    "arrived early": 1.8, "arrived on time": 1.8, "on time": 1.4, "ahead of schedule": 1.6,
    "arrived late": -2.0, "arrived damaged": -3.0, "arrived broken": -3.0,
    "never arrived": -3.0, "never received": -3.0, "didn't arrive": -2.8, "did not arrive": -2.8,
    "still waiting": -2.0, "slow delivery": -2.2, "slow shipping": -2.2,
    # usability
    "easy to use": 2.6, "easy to set up": 2.4, "easy to install": 2.4, "easy to clean": 2.0,
    "easy to assemble": 2.2, "hard to use": -2.2, "difficult to use": -2.2,
    "hard to read": -1.6, "hard to assemble": -2.0, "difficult to assemble": -2.0,
    # durability / battery
    "barely lasts": -2.4, "barely works": -2.6, "hardly works": -2.6, "barely functional": -2.4,
    "doesn't last": -2.4, "didn't last": -2.4, "does not last": -2.4, "drains fast": -2.0,
    "drains quickly": -2.0, "short battery life": -2.2, "poor battery life": -2.6,
    "long battery life": 2.4, "great battery life": 3.0, "lasts long": 2.0,
    "lasts all day": 2.4, "long lasting": 2.2, "long-lasting": 2.2,
    # repeat purchase (negative)
    "would not buy again": -3.0, "wouldn't buy again": -3.0, "won't buy again": -3.0,
    "not buy again": -2.8, "would not buy": -2.8, "wouldn't buy": -2.8, "never buy": -2.8,
    "will never buy": -3.0,
    # too much / too little
    "too small": -1.8, "too big": -1.6, "too large": -1.6, "too tight": -1.8,
    "too loose": -1.8, "too expensive": -2.2, "too heavy": -1.6, "too loud": -1.8,
    "too slow": -2.4, "too hot": -1.4, "not enough": -1.4, "too short": -1.4,
}

# --------------------------------------------------------------------------
# Modifiers
# --------------------------------------------------------------------------
NEGATORS = {
    "not", "no", "never", "none", "nothing", "neither", "nor", "cannot", "cant", "dont",
    "doesnt", "didnt", "isnt", "wasnt", "arent", "werent", "wont", "wouldnt", "couldnt",
    "shouldnt", "havent", "hasnt", "hadnt", "aint", "without", "barely", "hardly",
    "scarcely", "nobody", "nowhere",
}

BOOSTERS = {
    "extremely": 1.5, "incredibly": 1.4, "insanely": 1.4, "exceptionally": 1.4,
    "absolutely": 1.4, "completely": 1.4, "utterly": 1.5, "totally": 1.3, "thoroughly": 1.3,
    "really": 1.3, "very": 1.3, "highly": 1.3, "remarkably": 1.3, "super": 1.3, "so": 1.25,
    "truly": 1.25, "seriously": 1.25, "too": 1.2, "especially": 1.2, "particularly": 1.2,
    "definitely": 1.2, "quite": 1.1, "pretty": 1.1, "most": 1.1, "damn": 1.3, "freaking": 1.3,
    # diminishers
    "slightly": 0.6, "somewhat": 0.7, "bit": 0.7, "little": 0.7, "kinda": 0.7, "sorta": 0.7,
    "fairly": 0.85, "rather": 0.9, "mildly": 0.6, "marginally": 0.6, "relatively": 0.85,
}

# Words after which the writer's real opinion usually follows ("great, BUT it broke").
CONTRAST = {"but", "however", "nevertheless", "nonetheless"}

# Boundaries that stop a negation / aspect from leaking into the next clause.
CLAUSE_BREAKS = {".", "!", "?", ";", ",", ":", "\n", "(", ")", "—", "–"}
FRAGMENT_SPLITTERS = {"and", "&", "while", "whereas", "though", "although", "yet", "plus", "also"}

# --------------------------------------------------------------------------
# Emoji / emoticons
# --------------------------------------------------------------------------
EMOTES = {
    "😍": 3.0, "🥰": 3.0, "🤩": 3.0, "❤": 2.5, "❤️": 2.5, "💖": 2.5, "😊": 2.2, "😀": 2.2,
    "😃": 2.2, "😄": 2.4, "😁": 2.2, "👍": 2.2, "👏": 2.0, "🔥": 1.8, "⭐": 1.5, "🌟": 1.8,
    "💯": 2.4, "🙂": 1.4, "😉": 1.0, "😎": 1.6, "🙏": 1.0, "✅": 1.4, "👌": 1.6, "😻": 2.8,
    "😢": -2.0, "😭": -1.6, "😡": -3.0, "😠": -2.8, "👎": -2.4, "😞": -2.2, "😔": -2.0,
    "😤": -2.0, "🤬": -3.0, "😒": -1.8, "🙁": -1.6, "☹": -1.8, "💔": -2.4, "🤮": -3.0,
    "🤢": -2.6, "😩": -2.2, "😫": -2.2, "❌": -1.6, "😖": -2.2, "🥵": -1.4, "💩": -2.8,
    ":)": 1.8, ":-)": 1.8, "=)": 1.8, ":d": 2.4, ":-d": 2.4, ";)": 1.2, ";-)": 1.2, "<3": 2.4,
    ":p": 1.0, ":(": -1.8, ":-(": -1.8, "=(": -1.8, ":'(": -2.2, ":/": -1.0, ":-/": -1.0,
}

# --------------------------------------------------------------------------
# Topics (aspects) customers talk about
# --------------------------------------------------------------------------
ASPECTS: dict[str, set[str]] = {
    "Delivery": {
        "delivery", "delivered", "deliver", "shipping", "shipped", "ship", "arrived", "arrive",
        "arrival", "package", "packaging", "packed", "courier", "dispatch", "dispatched",
        "parcel", "shipment", "box", "tracking",
    },
    "Quality": {
        "quality", "build", "built", "material", "materials", "durable", "durability",
        "sturdy", "flimsy", "craftsmanship", "stitching", "broke", "broken", "defective",
        "defect", "faulty", "cracked", "scratched", "damaged", "cheaply", "solid", "fragile",
        "construction", "well-made", "high-quality",
    },
    "Value": {
        "price", "priced", "pricing", "cost", "value", "money", "expensive", "cheap",
        "affordable", "worth", "overpriced", "deal", "pricey", "bargain", "penny",
    },
    "Service": {
        "service", "support", "staff", "seller", "representative", "agent", "response",
        "replied", "reply", "warranty", "refund", "return", "returned", "returns",
        "manager", "team", "helpline",
    },
    "Performance": {
        "performance", "works", "working", "worked", "work", "speed", "battery", "lag",
        "laggy", "crash", "crashes", "crashed", "powerful", "reliable", "runs", "charge",
        "charging", "sound", "signal", "screen", "camera", "display",
    },
    "Design": {
        "design", "designed", "looks", "look", "looked", "color", "colour", "colors",
        "colours", "style", "stylish", "sleek", "appearance", "aesthetic", "finish",
    },
    "Comfort & fit": {
        "comfort", "comfortable", "comfy", "fit", "fits", "fitting", "size", "sizing",
        "soft", "cushion", "tight", "loose",
    },
    "Ease of use": {
        "easy", "setup", "set-up", "install", "installation", "instructions", "interface",
        "app", "intuitive", "simple", "user-friendly", "assemble", "assembly", "manual",
    },
    "Taste": {
        "taste", "tasted", "tastes", "tasty", "flavor", "flavour", "fresh", "delicious",
        "bland", "stale", "portion", "food", "meal",
    },
}
