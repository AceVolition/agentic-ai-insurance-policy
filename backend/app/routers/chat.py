from fastapi import APIRouter, Depends

from app.agents.prompts import INSURANCE_SYSTEM_PROMPT
from app.core.auth import get_current_user
from app.core.config import Settings, get_settings
from app.models.schemas import ChatRequest, ChatResponse
from app.providers.factory import get_llm_provider
from app.services.supabase_client import SupabaseService

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/{policy_id}", response_model=ChatResponse)
async def chat_about_policy(
    policy_id: str,
    payload: ChatRequest,
    user: dict = Depends(get_current_user),
    settings: Settings = Depends(get_settings),
):
    supabase = SupabaseService(settings)
    policy = await supabase.get_policy_for_user(policy_id, user["id"])
    analysis_rows = await supabase.select_rows(
        "analyses",
        {"policy_id": f"eq.{policy_id}"},
        order="created_at.desc",
        limit=1,
    )
    pdf_content = await supabase.download_policy_pdf(policy["file_url"])
    # Reuse the parser here so follow-up answers stay grounded in the uploaded policy.
    from app.services.pdf_parser import extract_text_from_pdf

    document_text = extract_text_from_pdf(pdf_content)
    analysis = analysis_rows[0] if analysis_rows else {}
    provider = get_llm_provider(settings)
    prompt = f"""
Answer the user's follow-up question using only the policy text and stored analysis below.
If the answer is not present, say what is missing and suggest what to ask the insurer.

Stored analysis:
Summary: {analysis.get("summary", "")}
Exclusions: {analysis.get("exclusions", "")}
Risks: {analysis.get("risks", "")}
Claim denial explanations: {analysis.get("denial_explanations", "")}

Policy text:
{document_text[:18000]}

User question:
{payload.message}
"""
    response_text = await provider.analyze(prompt, INSURANCE_SYSTEM_PROMPT)
    chat = await supabase.insert_row(
        "chats",
        {
            "user_id": user["id"],
            "policy_id": policy_id,
            "message": payload.message,
            "response": response_text,
        },
    )
    return {"id": chat["id"], "response": response_text, "created_at": chat.get("created_at")}

