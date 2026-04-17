import httpx

from app.core.config import settings
from app.core.errors import ExternalServiceError


class OpenRouterClient:
    def __init__(self):
        self._base_url = settings.OPENROUTER_BASE_URL
        self._api_key = settings.OPENROUTER_API_KEY

        self._headers = {
            "Authorization": f"Bearer {self._api_key}",
            "HTTP-Referer": settings.OPENROUTER_SITE_URL,
            "X-Title": settings.OPENROUTER_APP_NAME,
            "Content-Type": "application/json",
        }

    async def chat_completions(
        self,
        model: str,
        messages: list[dict],
        temperature: float = 0.7,
    ) -> str:
        url = f"{self._base_url}/chat/completions"

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    url,
                    json=payload,
                    headers=self._headers,
                    timeout=30.0,
                )
            except httpx.RequestError as e:
                raise ExternalServiceError(
                    message=f"OpenRouter request failed: {str(e)}",
                    service="openrouter",
                )

        if response.status_code >= 400:
            raise ExternalServiceError(
                message=f"OpenRouter error: {response.status_code} - {response.text}",
                service="openrouter",
            )

        data = response.json()

        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError):
            raise ExternalServiceError(
                message="Invalid response format from OpenRouter",
                service="openrouter",
            )