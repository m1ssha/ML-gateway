# ML Gateway Infrastructure

Данный репозиторий содержит конфигурацию для развёртывания программного шлюза защиты LLM в контейнеризированном виде.

## Быстрый старт

### Предварительные требования
- Docker ≥ 24.0
- Docker Compose ≥ 2.20
- (Опционально) NVIDIA Container Toolkit для GPU ускорения в `ml-service`

### Подготовка
1. Скопируйте шаблон переменных окружения:
   ```bash
   cp infrastructure/.env.example infrastructure/.env
   ```
2. Отредактируйте `infrastructure/.env`, установив надежные пароли и API-ключи.

### Запуск в Production режиме
Система объединяет все сервисы под единым Nginx-прокси на порту 80.
```bash
make prod
```
Доступ к приложению: `http://localhost`

### Запуск в Development режиме
Сервисы запускаются с hot-reload и пробросом портов напрямую.
```bash
make dev
```
- Frontend: `http://localhost:5173`
- Backend API Docs: `http://localhost:8001/docs`
- ML-Service Health: `http://localhost:8000/health`

### Управление
- Остановить систему: `make down`
- Просмотр логов: `make logs`
- Резервное копирование БД: `make backup`
- Полная очистка (с удалением данных!): `make clean`

## Архитектура
- **nginx-gateway**: Reverse-proxy (входная точка).
- **frontend**: Vue 3 SPA.
- **backend**: FastAPI Core.
- **ml-service**: Инференс RuBERT (FastAPI + PyTorch).
- **postgres**: Хранилище сессий.
- **redis**: Кэш диалогов.
