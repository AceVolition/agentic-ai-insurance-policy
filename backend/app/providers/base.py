from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    async def analyze(self, prompt: str, system_prompt: str | None = None) -> str:
        """Return model analysis for a prompt."""

