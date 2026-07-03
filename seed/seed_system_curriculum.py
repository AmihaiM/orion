import json
from pathlib import Path
from services.supabase_client import get_supabase


def main():
    sb = get_supabase()
    data = json.loads(Path(__file__).with_name("system_curriculum_seed.json").read_text(encoding="utf-8"))
    for ex in data:
        inserted = sb.table("exercises").insert({
            "title": ex["title"],
            "level": ex["level"],
            "unit": ex["unit"],
            "source_type": "system",
            "visibility": "system",
        }).execute().data[0]
        rows = []
        for i, s in enumerate(ex["sentences"], start=1):
            rows.append({
                "exercise_id": inserted["id"],
                "sentence_order": i,
                "english_text": s["en"],
                "hebrew_text": s["he"],
            })
        sb.table("sentences").insert(rows).execute()
        print(f"Seeded {ex['title']} ({len(rows)} sentences)")

if __name__ == "__main__":
    main()
