from typing import Optional


class AppError(Exception):
    """Базовое исключение доменного слоя."""
    def __init__(self, message: str = "Application error"):
        self.message = message
        super().__init__(message)


class NotFoundError(AppError):
    """Объект не найден в системе."""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message)


class UnauthorizedError(AppError):
    """Ошибка аутентификации (неверный логин/пароль)."""
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message)


class ForbiddenError(AppError):
    """Нет прав доступа."""
    def __init__(self, message: str = "Forbidden"):
        super().__init__(message)


class ConflictError(AppError):
    """Конфликт данных (например, уже существует)."""
    def __init__(self, message: str = "Conflict"):
        super().__init__(message)


class ExternalServiceError(AppError):
    """Ошибка внешнего сервиса (OpenRouter, API и т.д.)."""
    def __init__(
        self,
        message: str = "External service error",
        service: Optional[str] = None,
    ):
        self.service = service
        super().__init__(message)