from app.services.openrouter_client import OpenRouterClient
from app.repositories.chat_messages import ChatMessageRepository
from app.core.config import settings


class ChatUseCase:
    def __init__(
        self,
        message_repo: ChatMessageRepository,
        llm_client: OpenRouterClient,
    ):
        self._message_repo = message_repo
        self._llm_client = llm_client

    async def ask(
        self,
        user_id: int,
        prompt: str,
        system: str | None = None,
        max_history: int = 10,
        temperature: float = 0.7,
        model: str | None = None,
    ) -> str:

        model = model or settings.OPENROUTER_MODEL

        messages: list[dict] = []

        if system:
            messages.append({
                "role": "system",
                "content": system
            })

        history = await self._message_repo.get_last_messages(
            user_id=user_id,
            limit=max_history,
        )

        for msg in history:
            messages.append({
                "role": msg.role,
                "content": msg.content,
            })

        messages.append({
            "role": "user",
            "content": prompt,
        })

        await self._message_repo.add_message(
            user_id=user_id,
            role="user",
            content=prompt,
        )

        answer = await self._llm_client.chat_completions(
            model=model,
            messages=messages,
            temperature=temperature,
        )

        await self._message_repo.add_message(
            user_id=user_id,
            role="assistant",
            content=answer,
        )

        return answer