.PHONY: help build up down restart logs clean install-frontend install-backend test lint format

# Variáveis
COMPOSE_FILE = docker-compose.yml
FRONTEND_DIR = frontend
BACKEND_DIR = backend

# Comando padrão
help: ## Mostra esta ajuda
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Docker Compose
build: ## Constrói todas as imagens Docker
	docker-compose -f $(COMPOSE_FILE) build

up: ## Inicia todos os serviços
	docker-compose -f $(COMPOSE_FILE) up -d

down: ## Para todos os serviços
	docker-compose -f $(COMPOSE_FILE) down

restart: ## Reinicia todos os serviços
	docker-compose -f $(COMPOSE_FILE) restart

logs: ## Mostra logs de todos os serviços
	docker-compose -f $(COMPOSE_FILE) logs -f

logs-frontend: ## Mostra logs do frontend
	docker-compose -f $(COMPOSE_FILE) logs -f frontend

logs-backend: ## Mostra logs do backend
	docker-compose -f $(COMPOSE_FILE) logs -f backend

logs-n8n: ## Mostra logs do n8n
	docker-compose -f $(COMPOSE_FILE) logs -f n8n

# Desenvolvimento
install-frontend: ## Instala dependências do frontend
	cd $(FRONTEND_DIR) && npm install

install-backend: ## Instala dependências do backend
	cd $(BACKEND_DIR) && pip install -r requirements.txt

dev-frontend: ## Inicia frontend em modo desenvolvimento
	cd $(FRONTEND_DIR) && npm run dev

dev-backend: ## Inicia backend em modo desenvolvimento
	cd $(BACKEND_DIR) && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Testes e Qualidade
test: ## Executa testes
	@echo "Executando testes..."
	cd $(FRONTEND_DIR) && npm test
	cd $(BACKEND_DIR) && python -m pytest

lint: ## Executa linters
	@echo "Executando linters..."
	cd $(FRONTEND_DIR) && npm run lint
	cd $(BACKEND_DIR) && flake8 .

format: ## Formata código
	@echo "Formatando código..."
	cd $(FRONTEND_DIR) && npm run format
	cd $(BACKEND_DIR) && black .

# Limpeza
clean: ## Remove containers, volumes e imagens não utilizados
	docker-compose -f $(COMPOSE_FILE) down -v
	docker system prune -f
	docker volume prune -f

clean-frontend: ## Limpa cache do frontend
	cd $(FRONTEND_DIR) && rm -rf node_modules package-lock.json

clean-backend: ## Limpa cache do backend
	cd $(BACKEND_DIR) && find . -type d -name "__pycache__" -exec rm -rf {} +
	cd $(BACKEND_DIR) && find . -type f -name "*.pyc" -delete

# Backup e Restore
backup-n8n: ## Faz backup dos workflows do n8n
	@echo "Fazendo backup dos workflows do n8n..."
	cp -r n8n/workflows n8n/workflows-backup/$(shell date +%Y%m%d_%H%M%S)

restore-n8n: ## Restaura workflows do n8n (especificar BACKUP_DATE=YYYYMMDD_HHMMSS)
	@if [ -z "$(BACKUP_DATE)" ]; then \
		echo "Erro: Especifique BACKUP_DATE=YYYYMMDD_HHMMSS"; \
		exit 1; \
	fi
	@echo "Restaurando workflows do n8n..."
	cp -r n8n/workflows-backup/$(BACKUP_DATE) n8n/workflows

# Status e Health Checks
status: ## Mostra status dos serviços
	docker-compose -f $(COMPOSE_FILE) ps

health: ## Verifica saúde dos serviços
	@echo "Verificando saúde dos serviços..."
	@curl -f http://localhost:8000/health || echo "Backend: ❌"
	@curl -f http://localhost:3000 || echo "Frontend: ❌"
	@curl -f http://localhost:5678 || echo "n8n: ❌"

# Produção
prod-build: ## Constrói para produção
	docker-compose -f $(COMPOSE_FILE) -f docker-compose.prod.yml build

prod-up: ## Inicia em modo produção
	docker-compose -f $(COMPOSE_FILE) -f docker-compose.prod.yml up -d

# Utilitários
shell-frontend: ## Abre shell no container frontend
	docker-compose -f $(COMPOSE_FILE) exec frontend sh

shell-backend: ## Abre shell no container backend
	docker-compose -f $(COMPOSE_FILE) exec backend bash

shell-n8n: ## Abre shell no container n8n
	docker-compose -f $(COMPOSE_FILE) exec n8n sh

# Monitoramento
monitor: ## Monitora recursos dos containers
	watch -n 2 'docker stats --no-stream'

# Logs específicos por serviço
logs-db: ## Mostra logs do banco de dados
	docker-compose -f $(COMPOSE_FILE) logs -f postgres

logs-redis: ## Mostra logs do Redis
	docker-compose -f $(COMPOSE_FILE) logs -f redis

logs-elasticsearch: ## Mostra logs do Elasticsearch
	docker-compose -f $(COMPOSE_FILE) logs -f elasticsearch 