# Twitter Clone

Корпоративный сервис микроблогов на базе FastAPI.

## Технологии

- **FastAPI** — веб-фреймворк
- **PostgreSQL** — база данных
- **SQLAlchemy** — ORM
- **Alembic** — миграции
- **Nginx** — веб-сервер
- **Docker Compose** — развёртывание

## Запуск

### Требования
- Docker
- Docker Compose

### Команды

```bash
docker compose up -d
```

Приложение будет доступно на `http://localhost`

Swagger документация: `http://localhost/docs`

## API

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | /api/tweets | Создать твит |
| DELETE | /api/tweets/{id} | Удалить твит |
| POST | /api/tweets/{id}/likes | Лайкнуть твит |
| DELETE | /api/tweets/{id}/likes | Убрать лайк |
| GET | /api/tweets | Получить ленту |
| POST | /api/medias | Загрузить медиа |
| GET | /api/users/me | Мой профиль |
| GET | /api/users/{id} | Профиль пользователя |
| POST | /api/users/{id}/follow | Подписаться |
| DELETE | /api/users/{id}/follow | Отписаться |

## Тестирование

```bash
pip install -r requirements/dev.txt
pytest tests/ -v
```

## Авторизация

Все запросы требуют заголовок `api-key` с ключом пользователя.