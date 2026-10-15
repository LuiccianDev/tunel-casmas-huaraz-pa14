# =============================================================================
#  Script de verificacion integral para Tunel Casmas Huaraz PA14
#  Uso:
#    .\scripts\check.ps1         # Verificacion total + generacion Excel/LISP/XML
#    .\scripts\check.ps1 -Fast   # Verificacion ultrarrapida (~1.5 s: Ruff + XML + Pytest)
# =============================================================================
param(
    [switch]$Fast
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
if (-not $ProjectRoot) { $ProjectRoot = Get-Location }

Push-Location $ProjectRoot
try {
    Write-Host ""
    Write-Host "=== [1/5] Formateando codigo con Ruff ===" -ForegroundColor Cyan
    uv run ruff format .

    Write-Host ""
    Write-Host "=== [2/5] Verificando linting con Ruff ===" -ForegroundColor Cyan
    uv run ruff check --fix .

    Write-Host ""
    Write-Host "=== [3/5] Sincronizando XML de criterios Civil 3D (DG-2018) ===" -ForegroundColor Cyan
    uv run python civil3d/generar_dg2018.py

    Write-Host ""
    Write-Host "=== [4/5] Ejecutando pruebas unitarias y arnés de código fuente (Pytest) ===" -ForegroundColor Cyan
    if ($Fast) {
        uv run pytest tests/test_civil3d_dg2018.py tests/test_documentacion.py tests/test_arnes_fuente_excel.py tests/test_arnes_fuente_lisp.py -q
    } else {
        uv run pytest -q
    }

    if (-not $Fast) {
        Write-Host ""
        Write-Host "=== [5/5] Generando entregables del tunel (PA14) ===" -ForegroundColor Cyan
        uv run pa14
    } else {
        Write-Host ""
        Write-Host "=== [5/5] Modo -Fast activo: se omitio regeneracion de Excel/LISP ===" -ForegroundColor Yellow
    }

    Write-Host ""
    Write-Host "[OK] PROYECTO VERIFICADO Y GENERADO EXITOSAMENTE SIN ERRORES" -ForegroundColor Green
    Write-Host ""
} finally {
    Pop-Location
}
