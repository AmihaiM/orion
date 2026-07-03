from flask import Blueprint, request, jsonify
import requests
from services.csv_importer import normalize_sentences_from_csv
from services.supabase_client import get_supabase

imports_bp = Blueprint("imports", __name__)

@imports_bp.post("/csv-url")
def import_csv_url():
    data = request.get_json(force=True)
    title = data.get("title", "Untitled Exercise").strip()
    csv_url = data.get("csv_url", "").strip()
    organization_id = data.get("organization_id")
    teacher_id = data.get("teacher_id")
    level = data.get("level", "custom")

    if not csv_url:
        return jsonify({"error": "csv_url_required"}), 400

    r = requests.get(csv_url, timeout=12)
    r.raise_for_status()
    csv_text = r.content.decode("utf-8-sig", errors="replace")
    sentences = normalize_sentences_from_csv(csv_text)
    if not sentences:
        return jsonify({"error": "no_valid_sentences"}), 400

    sb = get_supabase()
    ex = sb.table("exercises").insert({
        "title": title,
        "level": level,
        "source_type": "teacher_custom",
        "visibility": "organization",
        "organization_id": organization_id,
        "created_by_user_id": teacher_id,
        "source_url": csv_url,
    }).execute().data[0]

    rows = []
    for idx, s in enumerate(sentences, start=1):
        rows.append({
            "exercise_id": ex["id"],
            "sentence_order": idx,
            "english_text": s["english_text"],
            "hebrew_text": s["hebrew_text"],
        })
    sb.table("sentences").insert(rows).execute()
    return jsonify({"exercise": ex, "sentences_imported": len(rows)})
