import re
from difflib import SequenceMatcher


def normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = text.replace("i'd", "i would")
    text = text.replace("i'm", "i am")
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def accuracy(expected: str, spoken: str) -> float:
    a = normalize_text(expected)
    b = normalize_text(spoken)
    if not a or not b:
        return 0.0
    return round(SequenceMatcher(None, a, b).ratio() * 100, 2)
