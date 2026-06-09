from app.agents.prompts import INSURANCE_SYSTEM_PROMPT, clipped_policy_text
from app.providers.base import LLMProvider


class PolicyComparisonAgent:
    def __init__(self, provider: LLMProvider):
        self.provider = provider

    async def run(self, document_text: str) -> str:
        prompt = f"""
Create a comparison checklist a user can apply when shopping for another policy.
Focus on limits, deductibles, exclusions, endorsements, price drivers, and questions that could identify cheaper
or better coverage. Base the checklist only on this policy.

Policy text:
{clipped_policy_text(document_text, 22000)}
"""
        return await self.provider.analyze(prompt, INSURANCE_SYSTEM_PROMPT)

