# =============================================================================
#  Watch Harness - Monitor Reactivo en Vivo para Tunel Casmas Huaraz PA14
#  Uso:
#    .\scripts\watch_harness.ps1
#
#  Escucha cambios en:
#    - src/casmas_pa14/
#    - datos/parametros.toml
#    - civil3d/dg2018_datos.toml
#
#  Ejecuta instantaneamente el arnes de codigo fuente en memoria.
# =============================================================================

$ErrorActionPreference = "Continue"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
if (-not $ProjectRoot) { $ProjectRoot = Get-Location }

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " [PA14] WATCH HARNESS ACTIVO - Monitor Reactivo en Vivo   " -ForegroundColor Cyan
Write-Host " Vigilando: src/casmas_pa14, datos, civil3d              " -ForegroundColor DarkCyan
Write-Host " Presiona Ctrl + C para detener el monitor                " -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan

function Ejecutar-Arnes {
    param([string]$Origen)
    
    $Timestamp = Get-Date -Format "HH:mm:ss"
    Write-Host "`n[$Timestamp] Cambio detectado en: $Origen" -ForegroundColor Cyan
    Write-Host ">>> Ejecutando arnes de calidad en codigo fuente..." -ForegroundColor Gray
    
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    $salida = uv run pytest tests/test_arnes_fuente_excel.py tests/test_arnes_fuente_lisp.py -q 2>&1
    $sw.Stop()
    $duracion = [math]::Round($sw.Elapsed.TotalMilliseconds, 0)
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[$Timestamp] [OK] ARNES EN MEMORIA APROBADO (${duracion} ms)" -ForegroundColor Green
    } else {
        Write-Host "[$Timestamp] [ERROR] FALLO EN EL ARNES DE CODIGO FUENTE:" -ForegroundColor Red
        Write-Host ($salida -join "`n") -ForegroundColor Red
        try { [Console]::Beep(800, 300) } catch {}
    }
}

# Ejecucion inicial de verificacion
Ejecutar-Arnes "Inicializacion del entorno"

$Watchers = @()
$RutasVigilar = @(
    (Join-Path $ProjectRoot "src\casmas_pa14"),
    (Join-Path $ProjectRoot "datos"),
    (Join-Path $ProjectRoot "civil3d")
)

$UltimoDisparo = [DateTime]::MinValue
$DebounceMs = 600

foreach ($Ruta in $RutasVigilar) {
    if (Test-Path $Ruta) {
        $Watcher = New-Object System.IO.FileSystemWatcher
        $Watcher.Path = $Ruta
        $Watcher.IncludeSubdirectories = $true
        $Watcher.EnableRaisingEvents = $true
        $Watcher.NotifyFilter = [System.IO.NotifyFilters]'FileName, LastWrite'
        
        $Action = {
            param($source, $eventArgs)
            $Archivo = $eventArgs.FullPath
            # Ignorar temporales o caches
            if ($Archivo -match "__pycache__|\.tmp|\.git|\.pytest_cache") { return }
            
            $Ahora = [DateTime]::Now
            $Diferencia = ($Ahora - $script:UltimoDisparo).TotalMilliseconds
            if ($Diferencia -gt $script:DebounceMs) {
                $script:UltimoDisparo = $Ahora
                Ejecutar-Arnes $eventArgs.Name
            }
        }
        
        Register-ObjectEvent $Watcher "Changed" -Action $Action | Out-Null
        Register-ObjectEvent $Watcher "Created" -Action $Action | Out-Null
        $Watchers += $Watcher
    }
}

try {
    while ($true) {
        Start-Sleep -Seconds 1
    }
} finally {
    Write-Host "`nDeteniendo monitores del arnes..." -ForegroundColor Yellow
    foreach ($w in $Watchers) {
        $w.EnableRaisingEvents = $false
        $w.Dispose()
    }
    Get-EventSubscriber | Where-Object { $_.SourceIdentifier -match "FileSystemWatcher" } | Unregister-Event
    Write-Host "[PA14] Watch Harness detenido." -ForegroundColor Cyan
}
