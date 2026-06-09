import httpx

from app.core.config import Settings
from app.providers.base import LLMProvider


class DeepSeekProvider(LLMProvider):
    def __init__(self, settings: Settings):
        self.settings = settings

    async def analyze(self, prompt: str, system_prompt: str | None = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        async with httpx.AsyncClient(timeout=90) as client:
            response = await client.post(
                self.settings.deepseek_api_url,
                headers={
                    "Authorization": f"Bearer {self.settings.deepseek_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.settings.deepseek_model,
                    "messages": messages,
                    "temperature": 0.2,
                },
            )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()

