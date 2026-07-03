import csv
import io
import re
from typing import List, Dict

HEBREW_RE = re.compile(r"[\u0590-\u05FF]")
LATIN_RE = re.compile(r"[A-Za-z]")


def fix_mojibake(text: str) -> str:
    if not text:
        return ""
    # Common Google CSV mojibake: UTF-8 decoded as latin/cp1252.
    if "×" in text or "â" in text:
        for enc in ("latin1", "cp1252"):
            try:
                return text.encode(enc).decode("utf-8")
            except Exception:
                pass
    return text


def is_hebrew(text: str) -> bool:
    return bool(HEBREW_RE.search(text or ""))


def is_english(text: str) -> bool:
    return bool(LATIN_RE.search(text or "")) and not is_hebrew(text)


def normalize_sentences_from_csv(csv_text: str) -> List[Dict[str, str]]:
    csv_text = fix_mojibake(csv_text or "")
    reader = csv.reader(io.StringIO(csv_text))
    sentences = []

    for raw_row in reader:
        row = [fix_mojibake(c.strip()) for c in raw_row if c and c.strip()]
        if len(row) < 2:
            continue

        joined = " ".join(row).lower()
        if any(h in joined for h in ["english", "hebrew", "sentence", "translation"]):
            continue

        a, b = row[0], row[1]
        if is_english(a) and is_hebrew(b):
            en, he = a, b
        elif is_hebrew(a) and is_english(b):
            en, he = b, a
        else:
            # Prefer column with more latin words as English.
            en, he = (a, b) if len(re.findall(r"[A-Za-z]+", a)) >= len(re.findall(r"[A-Za-z]+", b)) else (b, a)

        if len(en.split()) >= 2:
            sentences.append({"english_text": en, "hebrew_text": he})

    return sentences
