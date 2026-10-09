<#
.SYNOPSIS
    Script rápido para compilar la solución de integración de AutoCAD (Gateway + MCP).
.DESCRIPTION
    Este script navega a la carpeta de plugins y ejecuta el comando de compilación
    en modo 'Release'.
#>

Write-Host "Iniciando la compilación de la Solución de AutoCAD (Gateway + MCP)..." -ForegroundColor Cyan

# Definir la ruta relativa a la carpeta de plugins basándose en la ubicación de este script
$pluginsDir = Join-Path $PSScriptRoot "..\plugins"

# Ejecutar el comando de compilación apuntando a la carpeta (detectará automáticamente la solución .slnx)
dotnet build "$pluginsDir" -c Release

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n¡Compilación Exitosa!" -ForegroundColor Green
    Write-Host "Los archivos .dll están listos en sus respectivas carpetas bin/Release/." -ForegroundColor DarkGray
} else {
    Write-Host "`nError en la compilación. Revisa los mensajes de arriba." -ForegroundColor Red
    Write-Host "(Nota: Si el error dice que el archivo está bloqueado, recuerda CERRAR AutoCAD antes de compilar)." -ForegroundColor Yellow
}
