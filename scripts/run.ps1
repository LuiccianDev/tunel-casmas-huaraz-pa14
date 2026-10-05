# =============================================================================
#  Script de ejecucion de entregables para Tunel Casmas Huaraz PA14
# =============================================================================
$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
if (-not $ProjectRoot) { $ProjectRoot = Get-Location }

Push-Location $ProjectRoot
try {
    Write-Host ""
    Write-Host ">>> Ejecutando pipeline completo PA14..." -ForegroundColor Yellow
    uv run pa14 $args
    Write-Host ""
} finally {
    Pop-Location
}
