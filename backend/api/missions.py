from flask import Blueprint, jsonify
from database.supabase_client import get_supabase

bp = Blueprint("missions", __name__, url_prefix="/api/missions")


@bp.get("")
def list_missions():
    sb = get_supabase()
    res = sb.table("missions").select("id,title,status").limit(20).execute()
    return jsonify(res.data)
