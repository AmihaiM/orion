import re


PASS_THRESHOLD = 85
MAX_ATTEMPTS_PER_SENTENCE = 5


def normalize(text: str) -> list[str]:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s']", "", text)
    return text.split()


def score_sentence(expected_text: str, spoken_text: str) -> dict:
    expected_words = normalize(expected_text)
    spoken_words = normalize(spoken_text)

    if not expected_words:
        return {
            "accuracy_score": 0,
            "passed": False,
            "missing_words": [],
            "extra_words": spoken_words,
        }

    matched = 0
    used_indexes = set()

    for expected_word in expected_words:
        for index, spoken_word in enumerate(spoken_words):
            if index not in used_indexes and expected_word == spoken_word:
                matched += 1
                used_indexes.add(index)
                break

    accuracy_score = round((matched / len(expected_words)) * 100)

    missing_words = [word for word in expected_words if word not in spoken_words]
    extra_words = [word for word in spoken_words if word not in expected_words]

    return {
        "accuracy_score": accuracy_score,
        "passed": accuracy_score >= PASS_THRESHOLD,
        "missing_words": missing_words,
        "extra_words": extra_words,
    }


def praise_message(passed: bool, attempt_number: int, needs_review: bool) -> str:
    if passed:
        return "Excellent! Great speaking. Let's continue 🚀"

    if needs_review:
        return "Good effort. We'll review this sentence again later 💪"

    if attempt_number <= 2:
        return "You're close. Try again — say the full sentence clearly 😊"

    return "Keep going. Focus on the missing words and try once more 💪"


def decide_next_action(passed: bool, attempt_number: int) -> dict:
    if passed:
        return {
            "next_action": "NEXT_SENTENCE",
            "needs_review": False,
        }

    if attempt_number >= MAX_ATTEMPTS_PER_SENTENCE:
        return {
            "next_action": "NEXT_SENTENCE",
            "needs_review": True,
        }

    return {
        "next_action": "RETRY_SENTENCE",
        "needs_review": False,
    }