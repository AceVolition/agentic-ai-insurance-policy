from fastapi import APIRouter, Depends

from app.agents.supervisor import PolicyAnalysisSupervisor
from app.core.auth import get_current_user
from app.core.config import Settings, get_settings
from app.models.schemas import AnalysisRecord
from app.providers.factory import get_llm_provider
from app.services.supabase_client import SupabaseService

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("/run/{policy_id}", response_model=AnalysisRecord)
async def run_analysis(
    policy_id: str,
    user: dict = Depends(get_current_user),
    settings: Settings = Depends(get_settings),
):
    supabase = SupabaseService(settings)
    policy = await supabase.get_policy_for_user(policy_id, user["id"])
    supervisor = PolicyAnalysisSupervisor(get_llm_provider(settings), supabase)
    await supervisor.run({"user_id": user["id"], "policy_id": policy_id, "file_url": policy["file_url"]})
    rows = await supabase.select_rows("analyses", {"policy_id": f"eq.{policy_id}"}, order="created_at.desc", limit=1)
    return rows[0]


@router.get("/{policy_id}", response_model=AnalysisRecord | None)
async def get_analysis(
    policy_id: str,
    user: dict = Depends(get_current_user),
    settings: Settings = Depends(get_settings),
):
    supabase = SupabaseService(settings)
    await supabase.get_policy_for_user(policy_id, user["id"])
    rows = await supabase.select_rows("analyses", {"policy_id": f"eq.{policy_id}"}, order="created_at.desc", limit=1)
    return rows[0] if rows else None

