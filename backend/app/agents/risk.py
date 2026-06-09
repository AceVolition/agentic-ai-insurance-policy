from app.agents.prompts import INSURANCE_SYSTEM_PROMPT, clipped_policy_text
from app.providers.base import LLMProvider


class RiskDetectionAgent:
    def __init__(self, provider: LLMProvider):
        self.provider = provider

    async def run(self, document_text: str) -> str:
        prompt = f"""
Detect user-facing risks in this policy, including high deductibles, low limits, ambiguous language, claim duties,
coverage gaps, cancellation traps, regulatory/compliance concerns, and likely denial triggers.
For each risk, provide severity (Low/Medium/High), why it matters, and a suggested question/action.

Policy text:
{clipped_policy_text(document_text)}
"""
        return await self.provider.analyze(prompt, INSURANCE_SYSTEM_PROMPT)

