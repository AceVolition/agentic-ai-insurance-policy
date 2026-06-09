from app.providers.base import LLMProvider


class ClaudeProvider(LLMProvider):
    async def analyze(self, prompt: str, system_prompt: str | None = None) -> str:
        raise NotImplementedError("ClaudeProvider is a pluggable stub for future production use.")


class OpenAIProvider(LLMProvider):
    async def analyze(self, prompt: str, system_prompt: str | None = None) -> str:
        raise NotImplementedError("OpenAIProvider is a pluggable stub for future production use.")


class GeminiProvider(LLMProvider):
    async def analyze(self, prompt: str, system_prompt: str | None = None) -> str:
        raise NotImplementedError("GeminiProvider is a pluggable stub for future production use.")

