from app.agents.prompts import INSURANCE_SYSTEM_PROMPT, clipped_policy_text
from app.providers.base import LLMProvider
from app.services.pdf_parser import extract_text_from_pdf


class PDFParsingAgent:
    def __init__(self, provider: LLMProvider):
        self.provider = provider

    async def run(self, pdf_content: bytes) -> dict[str, str]:
        text = extract_text_from_pdf(pdf_content)
        if not text.strip():
            raise ValueError("No readable text could be extracted from the PDF.")

        prompt = f"""
Identify the likely insurance type from this extracted policy text.
Return one short label such as Homeowners, Renters, Auto, Small Business, Health, Life, or Unknown.

Policy text:
{clipped_policy_text(text, 6000)}
"""
        insurance_type = await self.provider.analyze(prompt, INSURANCE_SYSTEM_PROMPT)
        return {"document_text": text, "insurance_type": insurance_type.strip().splitlines()[0][:80]}

