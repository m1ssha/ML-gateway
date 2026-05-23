#!/bin/sh
set -e
echo "▶ Применение миграций Alembic..."
alembic upgrade head
echo "▶ Запуск Backend-сервиса..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8001 --workers 2 --loop uvloop --http httptools
