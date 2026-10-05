#!/usr/bin/env bash
# =============================================================================
#  Script de ejecución de entregables para Túnel Casmas Huaraz PA14
# =============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo -e "\n\033[1;33m>>> Ejecutando pipeline completo PA14...\033[0m"
uv run pa14 "$@"
