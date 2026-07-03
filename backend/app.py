from flask import Flask
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_ANON_KEY
app = Flask(__name__)

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_ANON_KEY
)


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

        return {
            "api": "ok",
            "supabase": "ok"
        }

    except Exception as e:
        return {
            "api": "ok",
            "supabase": "failed",
            "error": str(e)
        }, 500


if __name__ == "__main__":
    app.run(debug=True)
