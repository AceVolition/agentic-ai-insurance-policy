from __future__ import annotations

from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.core.auth import get_current_user
from app.core.config import Settings, get_settings
from app.models.schemas import PolicyRecord
from app.services.supabase_client import SupabaseService

router = APIRouter(prefix="/policies", tags=["policies"])


@router.post("/upload", response_model=PolicyRecord)
async def upload_policy(
    file: UploadFile = File(...),
    user: dict = Depends(get_current_user),
    settings: Settings = Depends(get_settings),
):
    if file.content_type not in {"application/pdf", "application/octet-stream"} and not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only PDF files are supported")

    supabase = SupabaseService(settings)
    await supabase.upsert_user(user["id"], user.get("email"))
    content = await file.read()
    safe_name = (file.filename or "policy.pdf").replace("/", "-").replace("\\", "-")
    path = f"{user['id']}/{uuid4()}-{safe_name}"
    await supabase.upload_policy_pdf(path, content, file.content_type or "application/pdf")
    policy = await supabase.insert_row("policies", {"user_id": user["id"], "file_url": path})
    policy["signed_url"] = await supabase.create_signed_url(path)
    return policy


@router.get("", response_model=list[PolicyRecord])
async def list_policies(
    user: dict = Depends(get_current_user),
    settings: Settings = Depends(get_settings),
):
    supabase = SupabaseService(settings)
    policies = await supabase.select_rows(
        "policies",
        {"user_id": f"eq.{user['id']}"},
        order="uploaded_at.desc",
    )
    for policy in policies:
        policy["signed_url"] = await supabase.create_signed_url(policy["file_url"])
    return policies


@router.get("/{policy_id}", response_model=PolicyRecord)
async def get_policy(
    policy_id: str,
    user: dict = Depends(get_current_user),
    settings: Settings = Depends(get_settings),
):
    supabase = SupabaseService(settings)
    policy = await supabase.get_policy_for_user(policy_id, user["id"])
    policy["signed_url"] = await supabase.create_signed_url(policy["file_url"])
    return policy
