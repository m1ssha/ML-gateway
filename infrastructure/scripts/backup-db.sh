#!/bin/sh
# Резервное копирование БД в ./backups/
BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
FILENAME="backup_$TIMESTAMP.sql.gz"

mkdir -p "$BACKUP_DIR"

echo "▶ Создание резервной копии базы данных..."
docker compose -f infrastructure/docker-compose.yml --env-file infrastructure/.env exec -T postgres pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" | gzip > "$BACKUP_DIR/$FILENAME"
echo "✅ Резервная копия сохранена: $BACKUP_DIR/$FILENAME"
