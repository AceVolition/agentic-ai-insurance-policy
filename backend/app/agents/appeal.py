from app.agents.prompts import INSURANCE_SYSTEM_PROMPT, clipped_policy_text
from app.providers.base import LLMProvider


class AppealRecommendationAgent:
    def __init__(self, provider: LLMProvider):
        self.provider = provider

    async def run(self, document_text: str, denial_explanations: str) -> str:
        prompt = f"""
Based on the policy and possible denial explanations, suggest appeal preparation steps.
Include evidence to gather, policy terms to cite, questions for the insurer, and escalation options.
Do not draft a legal filing or promise an outcome.

Denial analysis:
{denial_explanations}

Policy text:
{clipped_policy_text(document_text, 22000)}
"""
        return await self.provider.analyze(prompt, INSURANCE_SYSTEM_PROMPT)

