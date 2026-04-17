# LLM FastAPI Service

Серверное приложение на FastAPI для работы с большой языковой моделью (LLM) через OpenRouter.

---

## Функции

- Регистрация пользователей
- Аутентификация и авторизация через JWT
- Авторизация через Swagger (OAuth2)
- Отправка запросов к LLM через OpenRouter
- Сохранение истории сообщений в SQLite
- Получение и удаление истории сообщений

---

## Структура проекта

```
app/
├── api/            # HTTP-слой
├── core/           # Общие компоненты и инфраструктура
├── db/             # Слой работы с БД
├── repositories/   # Репозитории
├── services/       # Внешние сервисы
├── usecases/       # бизнес-логика приложения
├── schemas/        # Pydantic-схемы
```

---

## Установка и запуск

### 1. Клонирование проекта

```
git clone <https://github.com/andr3w13/llm-p>
cd llm-p
```

---

### 2. Установка зависимостей

```
uv sync
```

---

## Настройка

Создайте файл `.env` в корне проекта:

```
APP_NAME=llm-p
ENV=local

JWT_SECRET=your_secret_key
JWT_ALG=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

SQLITE_PATH=./app.db

OPENROUTER_API_KEY=your_api_key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=mistralai/mistral-nemo
OPENROUTER_SITE_URL=http://localhost
OPENROUTER_APP_NAME=llm-fastapi-openrouter
```

---

## Запуск приложения

```
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

После запуска откройте Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## Демонстрация работы

---

### Регистрация пользователя

POST `/auth/register`

```
[images/register.png]
```

---

### Логин и получение JWT

POST `/auth/login`

```
[images/login.png]
```

---

### Авторизация через Swagger

Нажать кнопку **Authorize** и вставить полученный JWT токен.

```
[images/auth_1.png]
```

```
[images/auth_2.png]
```

---

### Отправка запроса к LLM

POST `/chat`

Пример запроса:

```
{
  "prompt": "Tell me a funny joke about programmers",
  "system": "string",
  "max_history": 10,
  "temperature": 0.7
}
```

```
[images/chat.png]
```

---

### Получение истории сообщений

GET `/chat/history`

```
[images/history.png]
```

---

### Очистка истории

DELETE `/chat/history`


```
[images/clear_history.png]
```

```
[images/history_cleared.png]
```

