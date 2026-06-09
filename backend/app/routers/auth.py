from fastapi import APIRouter, Depends

from app.core.config import Settings, get_settings
from app.models.schemas import AuthRequest, AuthResponse
from app.services.supabase_client import SupabaseService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=AuthResponse)
async def signup(payload: AuthRequest, settings: Settings = Depends(get_settings)):
    supabase = SupabaseService(settings)
    result = await supabase.signup(payload.email, payload.password)
    user = result.get("user")
    if user:
        await supabase.upsert_user(user["id"], user.get("email"))
    return {"user": user, "session": result.get("session")}


@router.post("/login", response_model=AuthResponse)
async def login(payload: AuthRequest, settings: Settings = Depends(get_settings)):
    supabase = SupabaseService(settings)
    result = await supabase.login(payload.email, payload.password)
    user = result.get("user")
    if user:
        await supabase.upsert_user(user["id"], user.get("email"))
    return {"user": user, "session": result}

