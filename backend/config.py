import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

SUPABASE_URL = os.getenv("SUPABASE_URL", "")

SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")