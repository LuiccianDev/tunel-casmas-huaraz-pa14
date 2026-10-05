# =============================================================================
#  Script de verificacion integral para Tunel Casmas Huaraz PA14
# =============================================================================
$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
if (-not $ProjectRoot) { $ProjectRoot = Get-Location }

Push-Location $ProjectRoot
try {
    Write-Host ""
    Write-Host "=== [1/4] Formateando codigo con Ruff ===" -ForegroundColor Cyan
    uv run ruff format .

    Write-Host ""
    Write-Host "=== [2/4] Verificando linting con Ruff ===" -ForegroundColor Cyan
    uv run ruff check --fix .

    Write-Host ""
    Write-Host "=== [3/4] Ejecutando pruebas unitarias (Pytest) ===" -ForegroundColor Cyan
    uv run pytest -q

    Write-Host ""
    Write-Host "=== [4/4] Generando entregables del tunel (PA14) ===" -ForegroundColor Cyan
    uv run pa14

    Write-Host ""
    Write-Host "[OK] PROYECTO VERIFICADO Y GENERADO EXITOSAMENTE SIN ERRORES" -ForegroundColor Green
    Write-Host ""
} finally {
    Pop-Location
}
