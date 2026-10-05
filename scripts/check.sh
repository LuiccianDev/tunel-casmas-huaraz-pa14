#!/usr/bin/env bash
# =============================================================================
#  Script de verificación integral para Túnel Casmas Huaraz PA14
# =============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo -e "\n\033[1;36m=== [1/4] Formateando código con Ruff ===\033[0m"
uv run ruff format .

echo -e "\n\033[1;36m=== [2/4] Verificando linting con Ruff ===\033[0m"
uv run ruff check --fix .

echo -e "\n\033[1;36m=== [3/4] Ejecutando pruebas unitarias (Pytest) ===\033[0m"
uv run pytest -q

echo -e "\n\033[1;36m=== [4/4] Generando entregables del túnel (PA14) ===\033[0m"
uv run pa14

echo -e "\n\033[1;32m✔ ¡PROYECTO VERIFICADO Y GENERADO EXITOSAMENTE SIN ERRORES!\033[0m\n"
