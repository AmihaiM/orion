import re
from difflib import SequenceMatcher
from typing import Dict, List


def normalize(text: str) -> str:
    return re.sub(r"[^\w\s']", "", (text or "").lower()).strip()


def accuracy_score(spoken: str, target: str) -> int:
    return int(SequenceMatcher(None, normalize(spoken), normalize(target)).ratio() * 100)


def word_feedback(spoken: str, target: str) -> List[Dict[str, str]]:
    sp = normalize(spoken).split()
    co = normalize(target).split()
    result = []
    for tag, i1, i2, j1, j2 in SequenceMatcher(None, sp, co).get_opcodes():
        if tag == "equal":
            for w in co[j1:j2]:
                result.append({"word": w, "status": "correct"})
        elif tag in ("replace", "delete"):
            for w in co[j1:j2]:
                result.append({"word": w, "status": "wrong"})
        elif tag == "insert":
            # Extra spoken words are not part of target, but may affect score.
            pass
    return result


def fluency_metrics(spoken: str, duration_ms: int = 0, silence_ms: int = 0) -> Dict[str, object]:
    words = len(normalize(spoken).split())
    speech_minutes = max((duration_ms - silence_ms) / 60000, 0.001)
    wpm = int(words / speech_minutes) if words else 0
    silence_ratio = silence_ms / duration_ms if duration_ms else 0
    if wpm >= 75 and silence_ratio <= 0.25:
        status = "excellent"
    elif wpm >= 50 and silence_ratio <= 0.4:
        status = "good"
    else:
        status = "needs_practice"
    return {"words_per_minute": wpm, "silence_ratio": round(silence_ratio, 2), "fluency_status": status}
