from app.agents.prompts import INSURANCE_SYSTEM_PROMPT, clipped_policy_text
from app.providers.base import LLMProvider


class ExclusionDetectionAgent:
    def __init__(self, provider: LLMProvider):
        self.provider = provider

    async def run(self, document_text: str) -> str:
        prompt = f"""
Find exclusions, limitations, waiting periods, coverage conditions, and situations where coverage may not apply.
Return a structured plain-English list with each exclusion, the practical impact, and any policy wording to verify.

Policy text:
{clipped_policy_text(document_text)}
"""
        return await self.provider.analyze(prompt, INSURANCE_SYSTEM_PROMPT)

