from app.agents.prompts import INSURANCE_SYSTEM_PROMPT, clipped_policy_text
from app.providers.base import LLMProvider


class PolicySummaryAgent:
    def __init__(self, provider: LLMProvider):
        self.provider = provider

    async def run(self, document_text: str) -> str:
        prompt = f"""
Create a plain-English insurance policy summary for a consumer.
Include: policy type if obvious, who/what is covered, major coverage categories, limits/deductibles when visible,
important duties, renewal/cancellation notes, and a concise "what this means for you" section.

Policy text:
{clipped_policy_text(document_text)}
"""
        return await self.provider.analyze(prompt, INSURANCE_SYSTEM_PROMPT)

