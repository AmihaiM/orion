from flask import Flask, jsonify
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY

app = Flask(__name__)

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

@app.get("/")
def home():
    return {
        "product": "Orion",
        "service": "sle-api",
        "version": "0.1.0",
        "goal": "Learner completes one Mission end-to-end"
    }


@app.get("/health")
def health():
    try:
        supabase.table("organizations").select("id").limit(1).execute()
        return {"api": "ok", "supabase": "ok"}
    except Exception as e:
        return {"api": "ok", "supabase": "failed", "error": str(e)}, 500


@app.get("/missions")
def list_missions():
    try:
        res = (
            supabase
            .table("exercises")
            .select("id,title,level,unit,source_type,visibility,created_at")
            .order("created_at", desc=True)
            .execute()
        )

        return jsonify({
            "missions": res.data or []
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.get("/missions/<mission_id>")
def get_mission(mission_id):
    try:
        mission_res = (
            supabase
            .table("exercises")
            .select("id,title,level,unit,source_type,visibility,created_at")
            .eq("id", mission_id)
            .single()
            .execute()
        )

        sentences_res = (
            supabase
            .table("sentences")
            .select("id,sentence_order,english_text,hebrew_text,difficulty,tags")
            .eq("exercise_id", mission_id)
            .order("sentence_order")
            .execute()
        )

        return jsonify({
            "mission": mission_res.data,
            "sentences": sentences_res.data or []
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)