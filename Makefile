.DEFAULT_GOAL := help

.PHONY: help install migrate mock-data run docker-run docker-run-mock-data lint format typecheck test test-unit test-functional check ci docker-build

help:
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "%-22s %s\n", $$1, $$2}'

install: ## Установить зависимости проекта и зависимости для разработки
	uv sync --all-groups

migrate: ## Применить миграции базы данных
	uv run python manage.py migrate

mock-data: ## Загрузить мок-данные для ручного тестирования
	uv run python manage.py load_mock_data

run: ## Запустить локальный сервер разработки
	uv run python manage.py runserver

docker-run: ## Запустить сервер в Docker
	docker compose up --build

docker-run-mock-data: ## Запустить сервер в Docker и загрузить мок-данные
	docker compose up --build -d
	docker compose run --rm web python manage.py load_mock_data
	docker compose logs -f web

lint: ## Запустить проверки Ruff
	uv run ruff check .

format: ## Отформатировать код через Ruff
	uv run ruff format .

typecheck: ## Запустить проверку типов mypy
	uv run mypy django_cash_flow_manager manage.py

test: ## Запустить все тесты с расчетом покрытия
	uv run pytest tests_functional tests

test-unit: ## Запустить юнит-тесты
	uv run pytest tests --no-cov

test-functional: ## Запустить функциональные тесты
	uv run pytest tests_functional --no-cov

check: ## Запустить системные проверки Django
	uv run python manage.py check

ci: lint typecheck check test ## Запустить основной локальный контроль качества

docker-build: ## Собрать Docker-образ локально
	docker build -t django-cash-flow-manager:local .
