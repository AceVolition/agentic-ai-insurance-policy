INSURANCE_SYSTEM_PROMPT = (
    "You are an expert insurance policy analysis assistant. Explain policy language in plain English, "
    "avoid legal advice, flag uncertainty, and base every answer only on the provided policy text."
)


def clipped_policy_text(text: str, limit: int = 28000) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + "\n\n[Policy text clipped for token budget.]"

