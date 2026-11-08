#!/usr/bin/env bash
# =============================================================================
#  Script de verificación integral para Túnel Casmas Huaraz PA14
# =============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo -e "\n\033[1;36m=== [1/5] Formateando código con Ruff ===\033[0m"
uv run ruff format .

echo -e "\n\033[1;36m=== [2/5] Verificando linting con Ruff ===\033[0m"
uv run ruff check --fix .

echo -e "\n\033[1;36m=== [3/5] Sincronizando XML de criterios Civil 3D (DG-2018) ===\033[0m"
uv run python diseno_vial/generar_dg2018.py

echo -e "\n\033[1;36m=== [4/5] Ejecutando pruebas unitarias (Pytest) ===\033[0m"
uv run pytest -q

echo -e "\n\033[1;36m=== [5/5] Generando entregables del túnel (PA14) ===\033[0m"
uv run pa14

echo -e "\n\033[1;32m✔ ¡PROYECTO VERIFICADO Y GENERADO EXITOSAMENTE SIN ERRORES!\033[0m\n"
