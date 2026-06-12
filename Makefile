.PHONY: help install lint test run server-info docker-build docker-run \
        compose-up compose-down compose-logs ansible-check ansible-dry ansible-run

help: ## показать все команды
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "%-15s %s\n", $$1, $$2}'

install: ## установить зависимости
	pip install -r app/requirements.txt

lint: ## проверить качество кода (ruff для Python, shellcheck для Bash)
	ruff check app/
	shellcheck scripts/*.sh

test: ## запустить тесты
	pytest app/tests/ -v

run: ## запустить приложение
	python app/main.py

server-info: ## запустить Bash-скрипт диагностики сервера
	./scripts/server-info.sh

docker-build: ## собрать Docker образ
	docker build -f app.Docker -t simple-app:latest .

docker-run: ## запустить контейнер
	docker run --rm -p 5000:5000 simple-app:latest

compose-up: ## запустить Docker Compose
	docker compose up -d --build

compose-down: ## остановить Docker Compose
	docker compose down

compose-logs: ## просмотреть логи
	docker compose logs -f app

ansible-check: ## проверить Ansible playbook
	ansible-playbook --syntax-check -i ansible/inventory.ini ansible/playbook.yml

ansible-dry: ## dry-run Ansible
	ansible-playbook -i ansible/inventory.ini ansible/playbook.yml --check

ansible-run: ## запустить Ansible playbook
	ansible-playbook -i ansible/inventory.ini ansible/playbook.yml