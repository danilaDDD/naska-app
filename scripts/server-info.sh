#!/usr/bin/env bash
#
# server-info.sh — диагностика сервера и проверка доступности сервисов.
#
# Использование:
#   ./scripts/server-info.sh [URL...]
#   ./scripts/server-info.sh --help
#
# Выводит информацию о системе (hostname, ОС, kernel, uptime), использование
# CPU/RAM/дисков, список запущенных Docker-контейнеров и проверяет доступность
# сервисов по HTTP.
#
# Exit codes:
#   0 — все проверки прошли успешно
#   1 — хотя бы один сервис недоступен
#   2 — ошибка использования (неверные аргументы)

set -euo pipefail

CURL_TIMEOUT="${CURL_TIMEOUT:-5}"

usage() {
    cat <<EOF
Использование: $(basename "$0") [OPTIONS] [URL...]

Скрипт диагностики сервера: выводит информацию о системе, ресурсах,
Docker-контейнерах и проверяет доступность сервисов по HTTP.

Аргументы:
  URL...        список URL для проверки доступности (например,
                http://localhost:5000/health). Без URL выводится
                только информация о системе.

Опции:
  -h, --help    показать эту справку и выйти

Примеры:
  $(basename "$0")
  $(basename "$0") http://localhost:5000/health
  $(basename "$0") http://localhost:5000/health http://localhost:8080/health

Exit codes:
  0 — все сервисы доступны
  1 — хотя бы один сервис недоступен
  2 — ошибка использования
EOF
}

error() {
    echo "Ошибка: $1" >&2
}

print_system_info() {
    local os_name="unknown"
    if [[ -r /etc/os-release ]]; then
        # shellcheck source=/dev/null
        os_name="$(. /etc/os-release && printf '%s' "$PRETTY_NAME")"
    fi

    echo "=== Server Diagnostics ==="
    echo "Date:     $(date '+%Y-%m-%d %H:%M:%S')"
    echo "Hostname: $(hostname)"
    echo "OS:       ${os_name}"
    echo "Kernel:   $(uname -r)"
    echo "Uptime:   $(uptime -p | sed 's/^up //')"
    echo ""
}

print_resources() {
    local cores load ram_used ram_total ram_pct disk_used disk_total disk_pct

    cores="$(nproc)"
    load="$(awk '{print $1 ", " $2 ", " $3}' /proc/loadavg)"
    read -r ram_used ram_total ram_pct < <(
        free -m | awk '/^Mem:/ {printf "%.1fG %.1fG %d%%\n", $3/1024, $2/1024, $3*100/$2}'
    )
    read -r disk_used disk_total disk_pct < <(
        df -h / | awk 'NR==2 {print $3, $2, $5}'
    )

    echo "=== Resources ==="
    echo "CPU:      ${cores} cores, load average: ${load}"
    echo "RAM:      ${ram_used} / ${ram_total} (${ram_pct})"
    echo "Disk /:   ${disk_used} / ${disk_total} (${disk_pct})"
    echo ""
}

print_docker_info() {
    echo "=== Docker ==="
    local containers
    if containers="$(docker ps --format 'table {{.ID}}\t{{.Image}}\t{{.Status}}' 2>/dev/null)"; then
        echo "$containers"
    else
        echo "Docker недоступен"
    fi
    echo ""
}

# Возвращает 0, если сервис ответил кодом 2xx, иначе 1
check_service() {
    local url="$1"
    local response http_code time_total time_ms curl_rc reason

    curl_rc=0
    response="$(curl -sS -o /dev/null -w '%{http_code} %{time_total}' \
        --max-time "$CURL_TIMEOUT" "$url" 2>/dev/null)" || curl_rc=$?

    if [[ "$curl_rc" -eq 0 ]]; then
        http_code="${response%% *}"
        time_total="${response##* }"
        time_ms="$(awk -v t="$time_total" 'BEGIN {printf "%d", t * 1000}')"
        if [[ "$http_code" =~ ^2 ]]; then
            echo "[OK]   ${url} (${http_code}, ${time_ms}ms)"
            return 0
        fi
        echo "[FAIL] ${url} (HTTP ${http_code}, ${time_ms}ms)"
        return 1
    fi

    case "$curl_rc" in
        6)  reason="could not resolve host" ;;
        7)  reason="connection refused" ;;
        28) reason="timeout after ${CURL_TIMEOUT}s" ;;
        *)  reason="curl error ${curl_rc}" ;;
    esac
    echo "[FAIL] ${url} (${reason})"
    return 1
}

check_services() {
    local urls=("$@")
    local healthy=0
    local total=${#urls[@]}
    local url

    echo "=== Service Health Checks ==="
    for url in "${urls[@]}"; do
        if check_service "$url"; then
            healthy=$((healthy + 1))
        fi
    done
    echo ""
    echo "Result: ${healthy}/${total} services healthy"

    [[ "$healthy" -eq "$total" ]]
}

main() {
    local urls=()

    while [[ $# -gt 0 ]]; do
        case "$1" in
            -h|--help)
                usage
                exit 0
                ;;
            -*)
                error "неизвестная опция: $1"
                usage >&2
                exit 2
                ;;
            http://*|https://*)
                urls+=("$1")
                ;;
            *)
                error "некорректный URL (ожидается http:// или https://): $1"
                exit 2
                ;;
        esac
        shift
    done

    print_system_info
    print_resources
    print_docker_info

    if [[ ${#urls[@]} -gt 0 ]]; then
        check_services "${urls[@]}"
    fi
}

main "$@"