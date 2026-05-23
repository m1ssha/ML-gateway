.PHONY: up down build logs restart dev prod backup clean

prod:            # Production-режим
	docker compose -f infrastructure/docker-compose.yml --env-file infrastructure/.env up -d --build

dev:             # Development-режим
	docker compose -f infrastructure/docker-compose.dev.yml --env-file infrastructure/.env up --build

down:
	docker compose -f infrastructure/docker-compose.yml -f infrastructure/docker-compose.dev.yml down

logs:
	docker compose -f infrastructure/docker-compose.yml logs -f

restart:
	docker compose -f infrastructure/docker-compose.yml restart

backup:
	./infrastructure/scripts/backup-db.sh

clean:           # Полная очистка (ОСТОРОЖНО: удаляет volumes с данными!)
	docker compose -f infrastructure/docker-compose.yml down -v --remove-orphans
	docker system prune -f
