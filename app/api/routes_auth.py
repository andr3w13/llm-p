from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic

from app.usecases.auth import AuthUseCase
from app.api.deps import get_auth_usecase, get_current_user_id

from app.core.errors import ConflictError, UnauthorizedError, NotFoundError

router = APIRouter()


@router.post("/register", response_model=UserPublic)
async def register(
    data: RegisterRequest,
    usecase: AuthUseCase = Depends(get_auth_usecase),
):
    try:
        user = await usecase.register(
            email=data.email,
            password=data.password,
        )
        return user

    except ConflictError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )


@router.post("/login", response_model=TokenResponse)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    usecase: AuthUseCase = Depends(get_auth_usecase),
):
    try:
        token = await usecase.login(
            email=form.username,
            password=form.password,
        )

        return TokenResponse(access_token=token)

    except UnauthorizedError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/me", response_model=UserPublic)
async def me(
    user_id: int = Depends(get_current_user_id),
    usecase: AuthUseCase = Depends(get_auth_usecase),
):
    try:
        user = await usecase.get_profile(user_id)
        return user

    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
