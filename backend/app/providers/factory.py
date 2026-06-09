from app.core.config import Settings
from app.providers.base import LLMProvider
from app.providers.deepseek import DeepSeekProvider
from app.providers.stubs import ClaudeProvider, GeminiProvider, OpenAIProvider


def get_llm_provider(settings: Settings) -> LLMProvider:
    provider = settings.llm_provider.lower()
    if provider == "deepseek":
        return DeepSeekProvider(settings)
    if provider == "claude":
        return ClaudeProvider()
    if provider == "openai":
        return OpenAIProvider()
    if provider == "gemini":
        return GeminiProvider()
    raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")

