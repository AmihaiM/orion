from supabase import create_client, Client
from app.core.config import get_settings


def get_supabase() -> Client:
    settings = get_settings()
    if not settings.supabase_url or not settings.supabase_service_role_key:
        raise RuntimeError("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY")
    return create_client(settings.supabase_url, settings.supabase_service_role_key)
