# simple-app

Простое REST API на Flask, упакованное в Docker. Тестовое задание на позицию DevOps.

Приложение хранит пользователей в памяти и отвечает на HTTP запросы в формате JSON. Рядом лежат: bash-скрипт диагностики сервера, Docker и Docker Compose файлы, CI на GitHub Actions, Ansible для развертывания на сервере и Makefile с удобными командами.

## Требования

- Python 3.12 или новее
- Docker и Docker Compose v2
- Ansible (только для развертывания на сервер)
- make

## Быстрый старт

Локально:

```
make install
make run
```

Приложение слушает на http://localhost:5000

Через Docker Compose:

```
make compose-up
curl http://localhost:5000/health
make compose-down
```

## API

GET / — приветствие

```
curl http://localhost:5000/
{"message": "Hello, World!"}
```

GET /health — проверка живости, всегда 200

```
curl http://localhost:5000/health
{"status": "ok"}
```

GET /api/users — список пользователей

```
curl http://localhost:5000/api/users
{"users": []}
```

POST /api/users — создать пользователя. Вернет 201, при ошибке валидации 400

```
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "email": "alice@example.com"}'
{"id": 1, "name": "Alice", "email": "alice@example.com"}
```

GET /api/users/1 — получить пользователя. Если нет — 404

```
curl http://localhost:5000/api/users/1
```

PUT /api/users/1 — обновить пользователя

```
curl -X PUT http://localhost:5000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Bob"}'
```

DELETE /api/users/1 — удалить пользователя

```
curl -X DELETE http://localhost:5000/api/users/1
{"message": "User deleted"}
```

## Скрипт диагностики сервера

Скрипт scripts/server-info.sh показывает информацию о системе (hostname, ОС, ядро, uptime), использование CPU, памяти и диска, запущенные Docker контейнеры и проверяет доступность сервисов по HTTP.

```
# только информация о системе
./scripts/server-info.sh

# плюс проверка сервисов
./scripts/server-info.sh http://localhost:5000/health http://localhost:8080/health

# справка
./scripts/server-info.sh --help
```

Если хотя бы один сервис недоступен, скрипт вернет код 1. Это удобно для использования в мониторинге и CI.

## Тесты

```
make test
```

Или напрямую:

```
pytest app/tests/ -v
```

Тесты можно запустить и в Docker:

```
docker compose run --rm tests
```

## Линтинг

```
make lint
```

Проверяет Python код через ruff и bash-скрипты через shellcheck.

## Развертывание через Ansible

1. Впишите адрес своего сервера в ansible/inventory.ini:

```
[webservers]
app-server-1 ansible_host=1.2.3.4 ansible_user=ubuntu
```

2. Проверьте playbook и запустите:

```
make ansible-check   # проверка синтаксиса
make ansible-dry     # пробный прогон без изменений
make ansible-run     # развертывание
```

Playbook сам установит Docker на сервер, скопирует файлы проекта в /opt/simple-app, запустит docker compose и проверит, что приложение отвечает на /health.

Порт и число воркеров можно поменять в ansible/playbook.yml (переменные app_port и gunicorn_workers).

## CI

При push или pull request в ветку main GitHub Actions автоматически: ставит зависимости, гоняет shellcheck и pytest, проверяет синтаксис Ansible, собирает Docker образ, запускает контейнер и проверяет /health.
