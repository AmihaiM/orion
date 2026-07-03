from flask import Blueprint, jsonify, request
from services.supabase_client import get_supabase

curriculum_bp = Blueprint("curriculum", __name__)

@curriculum_bp.get("/exercises")
def list_exercises():
    sb = get_supabase()
    org_id = request.args.get("organization_id")
    q = sb.table("exercises").select("id,title,level,source_type,visibility,created_at").order("created_at", desc=True)
    if org_id:
        q = q.or_(f"organization_id.eq.{org_id},visibility.eq.system")
    res = q.execute()
    return jsonify(res.data)

@curriculum_bp.get("/exercises/<exercise_id>/sentences")
def exercise_sentences(exercise_id):
    sb = get_supabase()
    res = sb.table("sentences").select("id,sentence_order,english_text,hebrew_text").eq("exercise_id", exercise_id).order("sentence_order").execute()
    return jsonify(res.data)
