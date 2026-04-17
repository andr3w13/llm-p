from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.chat import ChatRequest, ChatResponse
from app.api.deps import get_chat_usecase, get_current_user_id, get_chat_repository
from app.usecases.chat import ChatUseCase
from app.core.errors import ExternalServiceError

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def chat(
    data: ChatRequest,
    user_id: int = Depends(get_current_user_id),
    usecase: ChatUseCase = Depends(get_chat_usecase),
):
    try:
        answer = await usecase.ask(
            user_id=user_id,
            prompt=data.prompt,
            system=data.system,
            max_history=data.max_history,
            temperature=data.temperature,
        )

        return ChatResponse(answer=answer)

    except ExternalServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=e.message,
        )


@router.get("/history")
async def get_history(
    user_id: int = Depends(get_current_user_id),
    repo = Depends(get_chat_repository),
):
    messages = await repo.get_last_messages(user_id=user_id, limit=100)

    return [
        {
            "id": msg.id,
            "role": msg.role,
            "content": msg.content,
            "created_at": msg.created_at,
        }
        for msg in messages
    ]


@router.delete("/history", status_code=204)
async def clear_history(
    user_id: int = Depends(get_current_user_id),
    repo = Depends(get_chat_repository),
):
    await repo.delete_user_history(user_id)