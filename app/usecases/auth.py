from app.core.security import hash_password, verify_password, create_access_token
from app.core.errors import ConflictError, UnauthorizedError, NotFoundError

from app.repositories.users import UserRepository
from app.db.models import User


class AuthUseCase:
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    async def register(self, email: str, password: str) -> User:
        existing_user = await self._user_repo.get_by_email(email)

        if existing_user:
            raise ConflictError("Email already exists")

        password_hash = hash_password(password)

        user = User(
            email=email,
            password_hash=password_hash,
            role="user",
        )

        return await self._user_repo.create(user)

    async def login(self, email: str, password: str) -> str:
        user = await self._user_repo.get_by_email(email)

        if not user:
            raise UnauthorizedError("Invalid email or password")

        if not verify_password(password, user.password_hash):
            raise UnauthorizedError("Invalid email or password")

        token = create_access_token(
            user_id=user.id,
            role=user.role,
        )

        return token

    async def get_profile(self, user_id: int) -> User:
        user = await self._user_repo.get_by_id(user_id)

        if not user:
            raise NotFoundError("User not found")

        return user