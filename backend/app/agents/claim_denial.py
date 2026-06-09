from app.agents.prompts import INSURANCE_SYSTEM_PROMPT, clipped_policy_text
from app.providers.base import LLMProvider


class ClaimDenialExplanationAgent:
    def __init__(self, provider: LLMProvider):
        self.provider = provider

    async def run(self, document_text: str) -> str:
        prompt = f"""
Explain common claim denial reasons that could arise from this policy.
Map each reason to the relevant exclusion, duty, deadline, limit, or condition when visible.
Use plain English and include what documentation a user may need to challenge or clarify the denial.

Policy text:
{clipped_policy_text(document_text)}
"""
        return await self.provider.analyze(prompt, INSURANCE_SYSTEM_PROMPT)

