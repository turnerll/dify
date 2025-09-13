# 222.place Matchmaking Platform Makefile
# Convenient commands for development and deployment

.PHONY: help up down logs build clean test seed backup restore

# Default target
.DEFAULT_GOAL := help

# Variables
COMPOSE_FILE := docker-compose.yml
PROJECT_NAME := 222place

help: ## Show this help message
	@echo "222.place Matchmaking Platform Commands"
	@echo "======================================"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

up: ## Start all services
	@echo "🚀 Starting 222.place services..."
	docker-compose -f $(COMPOSE_FILE) up -d
	@echo "✅ Services started! Check status with 'make status'"
	@echo "🌐 Web app: http://localhost:3000"
	@echo "🔧 API: http://localhost:5000"
	@echo "📊 Grafana: http://localhost:3001 (admin/admin)"

down: ## Stop all services
	@echo "🛑 Stopping 222.place services..."
	docker-compose -f $(COMPOSE_FILE) down

build: ## Build all services
	@echo "🔨 Building 222.place services..."
	docker-compose -f $(COMPOSE_FILE) build

rebuild: ## Rebuild and restart all services
	@echo "🔄 Rebuilding and restarting services..."
	docker-compose -f $(COMPOSE_FILE) down
	docker-compose -f $(COMPOSE_FILE) build --no-cache
	docker-compose -f $(COMPOSE_FILE) up -d

logs: ## Show logs for all services
	docker-compose -f $(COMPOSE_FILE) logs -f

logs-api: ## Show API logs
	docker-compose -f $(COMPOSE_FILE) logs -f api

logs-web: ## Show web logs
	docker-compose -f $(COMPOSE_FILE) logs -f web

logs-db: ## Show database logs
	docker-compose -f $(COMPOSE_FILE) logs -f db

status: ## Show status of all services
	@echo "📊 Service Status:"
	docker-compose -f $(COMPOSE_FILE) ps
	@echo ""
	@echo "🔍 Health Checks:"
	@curl -s http://localhost:5000/health | jq . 2>/dev/null || echo "API: Not responding"
	@curl -s http://localhost:3000/api/health | jq . 2>/dev/null || echo "Web: Not responding"

shell-api: ## Open shell in API container
	docker-compose -f $(COMPOSE_FILE) exec api bash

shell-db: ## Open PostgreSQL shell
	docker-compose -f $(COMPOSE_FILE) exec db psql -U postgres -d matchmaking_db

seed: ## Seed database with sample data
	@echo "🌱 Seeding database with sample data..."
	docker-compose -f $(COMPOSE_FILE) exec api python -c "
	import asyncio
	from seed_data import seed_database
	asyncio.run(seed_database())
	"
	@echo "✅ Database seeded successfully!"

test: ## Run smoke tests
	@echo "🧪 Running smoke tests..."
	@chmod +x scripts/smoke_test.sh
	@./scripts/smoke_test.sh

test-api: ## Run API tests
	docker-compose -f $(COMPOSE_FILE) exec api pytest tests/ -v

clean: ## Clean up containers, networks, and volumes
	@echo "🧹 Cleaning up..."
	docker-compose -f $(COMPOSE_FILE) down -v --remove-orphans
	docker system prune -f
	@echo "✅ Cleanup complete!"

clean-all: ## Clean everything including images
	@echo "🧹 Deep cleaning (WARNING: removes all data)..."
	docker-compose -f $(COMPOSE_FILE) down -v --remove-orphans --rmi all
	docker system prune -af
	@echo "✅ Deep cleanup complete!"

backup: ## Backup database
	@echo "💾 Creating database backup..."
	@mkdir -p backups
	docker-compose -f $(COMPOSE_FILE) exec -T db pg_dump -U postgres matchmaking_db > backups/backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "✅ Backup created in backups/"

restore: ## Restore database from backup (usage: make restore BACKUP=backup_file.sql)
	@if [ -z "$(BACKUP)" ]; then \
		echo "❌ Please specify backup file: make restore BACKUP=backup_file.sql"; \
		exit 1; \
	fi
	@echo "📥 Restoring database from $(BACKUP)..."
	docker-compose -f $(COMPOSE_FILE) exec -T db psql -U postgres -d matchmaking_db < $(BACKUP)
	@echo "✅ Database restored!"

dev: ## Start development environment
	@echo "🛠️ Starting development environment..."
	docker-compose -f $(COMPOSE_FILE) up -d db redis qdrant
	@echo "✅ Development services started!"
	@echo "Run 'cd api && python app.py' for API development"
	@echo "Run 'cd web && npm run dev' for web development"

install: ## Install development dependencies
	@echo "📦 Installing dependencies..."
	@if [ -f "api/requirements.txt" ]; then \
		echo "Installing Python dependencies..."; \
		cd api && pip install -r requirements.txt; \
	fi
	@if [ -f "web/package.json" ]; then \
		echo "Installing Node.js dependencies..."; \
		cd web && npm install; \
	fi
	@echo "✅ Dependencies installed!"

format: ## Format code
	@echo "🎨 Formatting code..."
	@if command -v black >/dev/null 2>&1; then \
		black api/; \
	else \
		echo "Black not installed, skipping Python formatting"; \
	fi
	@if [ -f "web/package.json" ]; then \
		cd web && npm run lint --if-present; \
	fi

setup: ## Initial setup (run once)
	@echo "🔧 Initial setup..."
	@if [ ! -f ".env" ]; then \
		cp .env.example .env; \
		echo "📝 Created .env file from .env.example"; \
		echo "⚠️  Please edit .env with your configuration"; \
	fi
	@mkdir -p scripts backups logs
	@echo "✅ Setup complete!"

ssl: ## Generate self-signed SSL certificates
	@echo "🔒 Generating SSL certificates..."
	@mkdir -p certs
	openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
		-keyout certs/222place.key \
		-out certs/222place.crt \
		-subj "/C=US/ST=Local/L=Local/O=222place/CN=localhost"
	@echo "✅ SSL certificates created in certs/"

monitor: ## Open monitoring dashboard
	@echo "📊 Opening monitoring dashboard..."
	@if command -v open >/dev/null 2>&1; then \
		open http://localhost:3001; \
	elif command -v xdg-open >/dev/null 2>&1; then \
		xdg-open http://localhost:3001; \
	else \
		echo "Visit http://localhost:3001 for Grafana dashboard"; \
	fi

# Development helpers
api-dev: ## Start API in development mode
	cd api && python app.py

web-dev: ## Start web in development mode  
	cd web && npm run dev

# Update helpers
update: ## Pull latest images
	docker-compose -f $(COMPOSE_FILE) pull

upgrade: ## Upgrade and restart services
	@echo "⬆️ Upgrading services..."
	make update
	make down
	make up
	@echo "✅ Upgrade complete!"