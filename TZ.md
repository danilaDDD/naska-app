# **Тестовое задание для DevOps junior**

**Цель задания:** Создать простое приложение, упаковать его в Docker контейнер, настроить локальное развертывание через Docker Compose и автоматизировать развертывание с помощью Ansible.

---

## **1\. Описание задачи**

### **1.1. Общая задача**

Задание состоит из двух частей: **обязательной** и **продвинутой**. Качественное выполнение обязательной части — уже хороший результат. Продвинутая часть даёт дополнительные баллы и показывает глубину понимания.

#### **Обязательная часть**

1. **Написать простое приложение** — REST API на Python, которое отвечает на HTTP запросы  
2. **Написать Bash-скрипт** — диагностика сервера и проверка доступности сервисов  
3. **Упаковать в Docker** — создать Dockerfile и собрать образ  
4. **Настроить Docker Compose** — поднять приложение локально  
5. **Оформить коммиты** — следовать Conventional Commits  
6. **Документировать** — написать понятный README

#### **Продвинутая часть (дополнительные баллы)**

7. **Настроить GitHub Actions** — простой pipeline для сборки и тестирования  
8. **Настроить Ansible** — автоматизировать развертывание на серверах  
9. **Создать Makefile** — удобные команды для работы с проектом  
10. **Бонусные задания** — логирование, улучшения Docker, handlers в Ansible

### **1.2. Структура репозитория**

simple-app/  
├── app/  
│   ├── main.py              \# REST API приложение  
│   ├── requirements.txt      \# зависимости Python  
│   └── tests/  
│       └── test\_app.py       \# тесты  
├── scripts/  
│   └── server-info.sh        \# Bash-скрипт диагностики  
├── Dockerfile               \# контейнеризация  
├── docker-compose.yml       \# локальное развертывание  
├── ansible/  
│   ├── playbook.yml         \# Ansible playbook  
│   ├── inventory.ini         \# список серверов  
│   └── roles/  
│       ├── docker/  
│       │   └── tasks/main.yml  
│       └── app/  
│           └── tasks/main.yml  
├── .github/  
│   └── workflows/  
│       └── build.yml        \# GitHub Actions  
├── README.md                \# документация  
└── Makefile                 \# команды  
---

## **2\. Задание 1: Простое приложение**

### **2.1. Требования к приложению**

**Язык:** Python 3.12+

**REST API endpoints:**

GET  /               → {"message": "Hello, World\!"}  
GET  /health        → {"status": "ok"}  
GET  /api/users     → {"users": \[...\]}  
POST /api/users     → создание пользователя  
GET  /api/users/\<id\> → получить пользователя  
DELETE /api/users/\<id\> → удалить пользователя

**Требования:**

* Приложение должно слушать на порту 5000  
* Все endpoints должны возвращать JSON  
* GET /health должен всегда возвращать 200 OK  
* Обработка ошибок при пропущенных полях в POST  
* Корректные HTTP статус коды (201 для создания, 404 для не найденных)

### **2.2. Тесты**

Напишите минимум 5 тестов с использованием pytest:

* Тест GET /  
* Тест GET /health  
* Тест GET /api/users  
* Тест POST /api/users (успешное создание)  
* Тест POST /api/users (ошибка валидации)

---

## **3\. Задание 2: Bash-скрипт для диагностики сервера**

### **3.1. Описание**

Написать скрипт `scripts/server-info.sh`, который собирает информацию о сервере и проверяет доступность сервисов.

### **3.2. Требования к скрипту**

**Скрипт должен:**

* Выводить информацию о системе (hostname, ОС, uptime, kernel)  
* Показывать использование CPU, RAM и дисков  
* Выводить список запущенных Docker-контейнеров (если Docker установлен)  
* Проверять доступность сервисов по HTTP (URL передаются аргументами)  
* Возвращать exit code 1, если хотя бы один сервис недоступен  
* Записывать результат в лог-файл с timestamp

**Требования к качеству кода:**

* Корректная обработка аргументов и ошибок  
* Использование функций для логической организации кода  
* Проверка наличия зависимостей (curl, docker)  
* Поддержка флага `--help` с описанием использования  
* Скрипт должен проходить проверку `shellcheck` без ошибок

### **3.3. Использование**

\# Проверка доступности сервисов  
./scripts/server-info.sh http://localhost:5000/health http://localhost:8080/health

\# Справка  
./scripts/server-info.sh \--help

\# Только информация о системе (без URL)  
./scripts/server-info.sh

### **3.4. Пример вывода**

\=== Server Diagnostics \===  
Date:     2026-03-10 15:30:00  
Hostname: app-server-1  
OS:       Ubuntu 24.04 LTS  
Kernel:   6.8.0-51-generic  
Uptime:   5 days, 3:22

\=== Resources \===  
CPU:      4 cores, load average: 0.15, 0.10, 0.05  
RAM:      1.2G / 4.0G (30%)  
Disk /:   12G / 50G (24%)

\=== Docker \===  
CONTAINER ID   IMAGE              STATUS  
a1b2c3d4e5f6   simple-app:latest  Up 2 hours (healthy)

\=== Service Health Checks \===  
\[OK\]   http://localhost:5000/health (200, 12ms)  
\[FAIL\] http://localhost:8080/health (connection refused)

Result: 1/2 services healthy  
---

## **4\. Задание 3: Docker**

### **4.1. Dockerfile**

Создать Dockerfile с требованиями:

* Использовать официальный Python 3.12+ образ  
* Установить зависимости из requirements.txt  
* Скопировать приложение  
* Открыть порт 5000  
* Добавить HEALTHCHECK  
* Запустить приложение через gunicorn или python

### **4.2. Сборка и тестирование**

docker build \-t simple-app:latest .  
docker run \-p 5000:5000 simple-app:latest  
curl http://localhost:5000/health  
---

## **5\. Задание 4: Docker Compose**

### **5.1. docker-compose.yml**

Создать файл docker-compose.yml с требованиями:

* Сервис приложения (простой Flask app)  
* Маппинг портов 5000:5000  
* Переменные окружения (FLASK\_ENV=production)  
* Health check  
* Volumes для синхронизации кода (опционально)

### **5.2. Использование**

docker-compose up \-d  
docker-compose ps  
docker-compose logs \-f app  
curl http://localhost:5000/health  
docker-compose down  
---

**Далее идёт продвинутая часть.** Выполнение этих заданий не обязательно, но даёт значительное преимущество при оценке.

---

## **6\. Задание 5: GitHub Actions CI**

### **6.1. Простой pipeline**

Создать `.github/workflows/build.yml` с этапами:

* Checkout кода  
* Setup Python 3.12  
* Установка зависимостей  
* Линтинг Bash-скриптов (shellcheck)  
* Запуск тестов (pytest)  
* Сборка Docker образа  
* Запуск контейнера и проверка health

### **6.2. Требования**

Pipeline должен срабатывать:

* При push в main ветку  
* При pull request в main ветку

Должны быть steps:

* Install dependencies  
* Lint Bash scripts (shellcheck)  
* Run tests  
* Build Docker image  
* Test container health

### **6.3. Пример шага shellcheck**

\- name: Install shellcheck  
  run: sudo apt-get install \-y shellcheck

\- name: Lint Bash scripts  
  run: shellcheck scripts/\*.sh  
---

## **7\. Задание 6: Ansible для развертывания**

### **7.1. Структура Ansible**

Создать ansible playbook для развертывания приложения на Ubuntu сервере:

**Структура:**

ansible/  
├── playbook.yml          \# основной playbook  
├── inventory.ini          \# хосты  
└── roles/  
    ├── docker/  
    │   └── tasks/main.yml    \# установка Docker  
    └── app/  
        └── tasks/main.yml    \# развертывание приложения

### **7.2. Что должен делать playbook**

**Role: docker/tasks/main.yml**

* Обновить apt cache  
* Установить Docker и docker-compose  
* Включить демон Docker  
* Добавить текущего пользователя в группу docker

**Role: app/tasks/main.yml**

* Создать директорию /opt/simple-app  
* Скопировать файлы приложения на сервер  
* Скопировать docker-compose.yml  
* Запустить `docker-compose up -d`  
* Проверить, что контейнер запущен  
* Проверить health endpoint

### **7.3. Инвентори**

ansible/inventory.ini:

\[webservers\]  
app-server-1 ansible\_host=10.0.1.10 ansible\_user=ubuntu

### **7.4. Использование**

\# Проверка синтаксиса  
ansible-playbook \--syntax-check \-i ansible/inventory.ini ansible/playbook.yml

\# Dry-run  
ansible-playbook \-i ansible/inventory.ini ansible/playbook.yml \--check

\# Запуск  
ansible-playbook \-i ansible/inventory.ini ansible/playbook.yml

\# С verbose логированием  
ansible-playbook \-i ansible/inventory.ini ansible/playbook.yml \-vvv  
---

## **8\. Задание 7: Git и Conventional Commits**

### **8.1. Требования к коммитам**

Все коммиты должны следовать [Conventional Commits](https://www.conventionalcommits.org/ru/v1.0.0/) на русском языке:

**Типы:**

* `feat:` — новая функция  
* `fix:` — исправление  
* `docs:` — документация  
* `test:` — тесты  
* `chore:` — обслуживание

**Примеры:**

git commit \-m "feat: добавить REST API приложение"  
git commit \-m "feat: добавить Bash-скрипт диагностики сервера"  
git commit \-m "feat: добавить Dockerfile"  
git commit \-m "feat: добавить docker-compose.yml"  
git commit \-m "feat: добавить Ansible playbook"  
git commit \-m "test: добавить тесты для endpoints"  
git commit \-m "docs: добавить README с примерами"  
---

## **9\. Задание 8: Документация**

### **9.1. README.md**

README должен содержать:

1. **Описание** — что это такое  
2. **Требования** — Python 3.12+, Docker, Ansible  
3. **Быстрый старт**:  
   * Локальный запуск приложения  
   * Запуск через Docker Compose  
4. **API endpoints** — описание с примерами curl  
5. **Bash-скрипт** — описание, примеры использования  
6. **Тестирование** — как запустить тесты  
7. **Ansible развертывание** — шаги по развертыванию  
8. **Структура проекта** — описание файлов  
9. **Troubleshooting** — решение проблем

### **9.2. Примеры в README**

\# Локальный запуск  
pip install \-r app/requirements.txt  
python app/main.py

\# Docker Compose  
docker-compose up \-d

\# Тесты  
pytest app/tests/ \-v

\# Диагностика сервера  
./scripts/server-info.sh http://localhost:5000/health

\# Ansible  
ansible-playbook \-i ansible/inventory.ini ansible/playbook.yml  
---

## **10\. Makefile**

Создать Makefile с удобными командами:

help:           \# показать все команды  
install:        \# установить зависимости  
lint:           \# проверить качество кода (flake8/ruff для Python, shellcheck для Bash)  
test:           \# запустить тесты  
run:            \# запустить приложение  
server-info:    \# запустить Bash-скрипт диагностики сервера  
docker-build:   \# собрать Docker образ  
docker-run:     \# запустить контейнер  
compose-up:     \# запустить Docker Compose  
compose-down:   \# остановить Docker Compose  
compose-logs:   \# просмотреть логи  
ansible-check:  \# проверить Ansible playbook  
ansible-dry:    \# dry-run Ansible  
ansible-run:    \# запустить Ansible playbook  
---

## **11\. Примеры использования**

### **11.1. Локальная разработка**

git clone \<repo\>  
cd simple-app

\# Установить и запустить  
make install  
make run

\# В другом терминале \- тесты  
make test

\# Линтинг  
make lint

\# Проверить  
curl http://localhost:5000/health

\# Диагностика сервера  
make server-info

### **11.2. Docker Compose**

make docker-build  
make compose-up  
make compose-logs

curl http://localhost:5000/api/users

make compose-down

### **11.3. Ansible развертывание**

\# Проверить конфиг  
make ansible-check

\# Dry-run  
make ansible-dry

\# Запустить  
make ansible-run  
---

## **12\. Критерии оценки**

### **✅ Обязательная часть**

* Приложение запускается и отвечает на HTTP запросы  
* Все 5+ тестов проходят  
* Bash-скрипт запускается, корректно обрабатывает аргументы и ошибки, выводит информацию о системе  
* Bash-скрипт проходит проверку shellcheck без ошибок  
* Dockerfile собирается и контейнер запускается  
* Docker Compose поднимает приложение  
* Коммиты следуют Conventional Commits  
* README содержит полную документацию

### **📈 Продвинутая часть**

* GitHub Actions pipeline срабатывает и проходит (включая shellcheck)  
* Ansible playbook запускается без ошибок  
* Ansible правильно:  
  * Устанавливает Docker  
  * Копирует файлы приложения  
  * Запускает docker-compose  
  * Проверяет health endpoint  
* Makefile с удобными командами

### **🌟 Дополнительные критерии качества**

* Хорошее покрытие тестами (граничные случаи)  
* Обработка ошибок в приложении  
* Правильные HTTP статус коды  
* Оптимизированный Dockerfile (slim образы)  
* Bash-скрипт использует функции, логирование в файл, цветной вывод  
* Ansible использует переменные и jinja2 шаблоны  
* Добавлены Ansible handlers (перезагрузка Docker)  
* Проверка синтаксиса Ansible в pipeline  
* Структурированный и читаемый код  
* Хорошая обработка ошибок в Ansible

---

## **13\. Бонусные задания**

### **13.1. Логирование**

Добавить структурированное логирование в приложение:

import logging  
logger \= logging.getLogger(\_\_name\_\_)

@app.route('/api/users', methods=\['POST'\])  
def create\_user():  
    logger.info("Creating new user")  
    \# ...

### **13.2. Переменные в Ansible**

Использовать переменные в playbook:

vars:  
  app\_port: 5000  
  docker\_image: simple-app:latest  
  app\_dir: /opt/simple-app

### **13.3. Handlers в Ansible**

Добавить handlers для перезагрузки сервисов:

handlers:  
  \- name: restart docker  
    systemd:  
      name: docker  
      state: restarted

### **13.4. Улучшения Docker**

* Multi-stage builds  
* .dockerignore файл  
* Non-root пользователь

---

## **14\. Срок и формат сдачи**

### **14.1. Что нужно сдать**

1. **GitHub репозиторий** с полным исходным кодом

### **14.2. Что проверяют**

1. Репозиторий клонируется без ошибок  
2. `make install` устанавливает зависимости  
3. `make lint` проходит без ошибок (shellcheck \+ flake8/ruff)  
4. `make test` запускает все тесты успешно  
5. `make server-info` выводит информацию о системе  
6. `make compose-up` поднимает приложение  
7. `curl http://localhost:5000/health` возвращает 200 OK  
8. GitHub Actions pipeline срабатывает и проходит  
9. `ansible-playbook ansible/playbook.yml` запускается успешно  
10. После Ansible приложение доступно на сервере  
11. Все коммиты в формате Conventional Commits  
12. README понятен и полон

---

## **15\. Контакты и вопросы**

Если у вас возникли вопросы:

* Напишите в чат ХХ.ru. Задавайте смело — это нормально\!  
* Документация официальная лучше

---

Удачи\! Это хороший старт в DevOps.   
Помните: главное не идеальное решение, а понимание того, что вы делаете\!

