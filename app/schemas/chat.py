from typing import Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    prompt: str = Field(min_length=1)

    system: Optional[str] = Field(
        default=None,
        description="Системная инструкция для модели"
    )

    max_history: int = Field(
        default=10,
        ge=0,
        le=100,
        description="Количество сообщений из истории"
    )

    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Креативность модели"
    )


class ChatResponse(BaseModel):
    answer: str