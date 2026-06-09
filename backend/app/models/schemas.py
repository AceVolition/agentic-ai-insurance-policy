from typing import Any

from pydantic import BaseModel, EmailStr, Field


class AuthRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class AuthResponse(BaseModel):
    user: dict[str, Any] | None = None
    session: dict[str, Any] | None = None


class PolicyRecord(BaseModel):
    id: str
    user_id: str
    file_url: str
    insurance_type: str | None = None
    uploaded_at: str | None = None
    signed_url: str | None = None


class AnalysisRecord(BaseModel):
    id: str
    policy_id: str
    summary: str | None = None
    exclusions: Any = None
    risks: Any = None
    denial_explanations: Any = None
    created_at: str | None = None
    appeal_recommendations: Any = None
    policy_comparison: Any = None


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=3000)


class ChatResponse(BaseModel):
    id: str
    response: str
    created_at: str | None = None

