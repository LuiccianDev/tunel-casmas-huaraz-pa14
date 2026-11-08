# =============================================================================
#  PA14 TOOLCHAIN DOCTOR — Diagnostico Integral del Entorno y Servidores MCP
#  Proyecto: Tunel Casmas - Huaraz PA14
#  Uso:
#    .\scripts\doctor.ps1
# =============================================================================

[CmdletBinding()]
param()

$ErrorActionPreference = "Continue"

Write-Host ""
Write-Host "=======================================================================" -ForegroundColor Cyan
Write-Host "         TUNEL CASMAS - HUARAZ PA14 :: TOOLCHAIN DOCTOR               " -ForegroundColor Cyan
Write-Host "=======================================================================" -ForegroundColor Cyan
Write-Host ""

$ProjectRoot = Split-Path -Parent $PSScriptRoot
if (-not $ProjectRoot) { $ProjectRoot = Get-Location }

$Results = @()

function Record-Check {
    param(
        [string]$Category,
        [string]$Item,
        [string]$Status, # OK, WARN, OFFLINE, ERROR
        [string]$Details
    )
    $script:Results += [PSCustomObject]@{
        Categoria = $Category
        Componente = $Item
        Estado = $Status
        Detalles = $Details
    }
}

# -----------------------------------------------------------------------------
# 1. ENTORNO PYTHON Y DEPENDENCIAS
# -----------------------------------------------------------------------------
Write-Host "[1/6] Verificando Entorno Python & Gestor UV..." -ForegroundColor Yellow

try {
    $uvVersion = (uv --version 2>$null)
    if ($uvVersion) {
        Record-Check "Python" "Gestor uv" "OK" $uvVersion.Trim()
    } else {
        Record-Check "Python" "Gestor uv" "ERROR" "uv no se encuentra en el PATH"
    }
} catch {
    Record-Check "Python" "Gestor uv" "ERROR" $_.Exception.Message
}

$venvPath = Join-Path $ProjectRoot ".venv"
if (Test-Path $venvPath) {
    Record-Check "Python" "Entorno Virtual" "OK" ".venv detectado en la raiz"
} else {
    Record-Check "Python" "Entorno Virtual" "WARN" ".venv no existe. Ejecuta 'uv sync'"
}

$tomlPath = Join-Path $ProjectRoot "datos/parametros.toml"
if (Test-Path $tomlPath) {
    $tomlSize = (Get-Item $tomlPath).Length
    Record-Check "Datos" "parametros.toml" "OK" "$([math]::Round($tomlSize/1KB, 1)) KB (Fuente unica de verdad)"
} else {
    Record-Check "Datos" "parametros.toml" "ERROR" "Archivo critico no encontrado"
}

# -----------------------------------------------------------------------------
# 2. AUTOCAD & CIVIL 3D GATEWAY (PUERTO 5055)
# -----------------------------------------------------------------------------
Write-Host "[2/6] Verificando AutoCAD AI Gateway & MCP..." -ForegroundColor Yellow

$GatewayUrl = "http://localhost:5055/context/info"
$GatewayToken = if ($env:AUTOCAD_GATEWAY_TOKEN) { $env:AUTOCAD_GATEWAY_TOKEN } else { "pa14-autocad-token-casmas-2026" }

try {
    $headers = @{ "X-Gateway-Token" = $GatewayToken }
    $response = Invoke-RestMethod -Uri $GatewayUrl -Headers $headers -Method Get -TimeoutSec 2 -ErrorAction Stop
    $docName = $response.activeDocument
    $ver = $response.version
    Record-Check "AutoCAD" "Gateway HTTP (5055)" "OK" "En linea: CAD $ver · Doc: $docName"
} catch {
    Record-Check "AutoCAD" "Gateway HTTP (5055)" "OFFLINE" "No responde en localhost:5055. Carga la DLL con NETLOAD en AutoCAD."
}

$xmlStandards = Join-Path $ProjectRoot "diseno_vial/PA14_DG2018_MTC_Roadway_Design_Standards.xml"
if (Test-Path $xmlStandards) {
    $xmlDate = (Get-Item $xmlStandards).LastWriteTime.ToString("yyyy-MM-dd HH:mm")
    Record-Check "AutoCAD" "Estandar DG-2018 XML" "OK" "Sincronizado ($xmlDate)"
} else {
    Record-Check "AutoCAD" "Estandar DG-2018 XML" "WARN" "Falta generar XML. Ejecuta 'uv run python diseno_vial/generar_dg2018.py'"
}

# -----------------------------------------------------------------------------
# 3. QGIS MCP SERVER (PUERTO 9876)
# -----------------------------------------------------------------------------
Write-Host "[3/6] Verificando Servidor QGIS MCP..." -ForegroundColor Yellow

$qgisOnline = $false
try {
    $tcp = New-Object System.Net.Sockets.TcpClient
    $iar = $tcp.BeginConnect("127.0.0.1", 9876, $null, $null)
    $wait = $iar.AsyncWaitHandle.WaitOne(1000, $false)
    if ($wait) {
        $tcp.EndConnect($iar)
        $qgisOnline = $true
        $tcp.Close()
    }
} catch {
    $qgisOnline = $false
}

if ($qgisOnline) {
    Record-Check "QGIS" "Socket MCP (9876)" "OK" "Servidor QGIS activo en localhost:9876 (EPSG:32718)"
} else {
    Record-Check "QGIS" "Socket MCP (9876)" "OFFLINE" "Puerto 9876 cerrado. Inicia QGIS Desktop y activa el plugin MCP."
}

if ($env:QGIS_MCP_TOKEN) {
    Record-Check "QGIS" "Token Seguridad" "OK" "QGIS_MCP_TOKEN configurado en entorno"
} else {
    Record-Check "QGIS" "Token Seguridad" "WARN" "QGIS_MCP_TOKEN no configurado en entorno del sistema"
}

# -----------------------------------------------------------------------------
# 4. MICROSOFT POWER BI MODELING MCP
# -----------------------------------------------------------------------------
Write-Host "[4/6] Verificando Microsoft Power BI Desktop..." -ForegroundColor Yellow

$pbiProc = Get-Process -Name "PBIDesktop" -ErrorAction SilentlyContinue
if ($pbiProc) {
    $memMB = [math]::Round($pbiProc.WorkingSet64 / 1MB, 0)
    Record-Check "PowerBI" "PBIDesktop.exe" "OK" "En ejecucion (PID: $($pbiProc.Id), RAM: ${memMB} MB)"
} else {
    Record-Check "PowerBI" "PBIDesktop.exe" "OFFLINE" "Power BI Desktop cerrado. Abre el archivo .pbix o carpeta .pbip"
}

# -----------------------------------------------------------------------------
# 5. GRAPHIFY KNOWLEDGE GRAPH
# -----------------------------------------------------------------------------
Write-Host "[5/6] Verificando Grafo de Conocimiento Graphify..." -ForegroundColor Yellow

$graphReport = Join-Path $ProjectRoot "graphify-out/GRAPH_REPORT.md"
if (Test-Path $graphReport) {
    $reportDate = (Get-Item $graphReport).LastWriteTime.ToString("yyyy-MM-dd HH:mm")
    Record-Check "Graphify" "Grafo Local" "OK" "Reporte presente ($reportDate)"
} else {
    Record-Check "Graphify" "Grafo Local" "WARN" "Falta grafo. Ejecuta 'uvx --from graphifyy graphify update .'"
}

# -----------------------------------------------------------------------------
# 6. SUITE DE PRUEBAS Y CALIDAD (RAPIDO)
# -----------------------------------------------------------------------------
Write-Host "[6/6] Verificando Integridad de Codigo (Pytest)..." -ForegroundColor Yellow

try {
    $pytestFast = uv run pytest tests/test_diseno_vial_dg2018.py tests/test_documentacion.py tests/test_arnes_fuente_excel.py -q 2>&1
    if ($LASTEXITCODE -eq 0) {
        Record-Check "Suite" "Pytest Basico" "OK" "Arnes documental y de diseno_vial pasando al 100%"
    } else {
        Record-Check "Suite" "Pytest Basico" "WARN" "Pruebas con advertencias o fallos menores"
    }
} catch {
    Record-Check "Suite" "Pytest Basico" "ERROR" $_.Exception.Message
}

# -----------------------------------------------------------------------------
# TABLA DE RESULTADOS CONSOLIDADOS
# -----------------------------------------------------------------------------
Write-Host ""
Write-Host "=======================================================================" -ForegroundColor Cyan
Write-Host "                     RESUMEN DE DIAGNOSTICO                           " -ForegroundColor Cyan
Write-Host "=======================================================================" -ForegroundColor Cyan
Write-Host ""

foreach ($r in $Results) {
    $color = switch ($r.Estado) {
        "OK"      { "Green" }
        "WARN"    { "Yellow" }
        "OFFLINE" { "Gray" }
        "ERROR"   { "Red" }
        Default   { "White" }
    }
    $badge = "[{0,-7}]" -f $r.Estado
    Write-Host (" {0} {1,-9} :: {2,-24} -> {3}" -f $badge, $r.Categoria, $r.Componente, $r.Detalles) -ForegroundColor $color
}

Write-Host ""
Write-Host "-----------------------------------------------------------------------" -ForegroundColor DarkGray
Write-Host " Sugerencias de Inicio Rapido:" -ForegroundColor Cyan
Write-Host "  * Para compilar plugins C#:     .\scripts\build_plugins.ps1" -ForegroundColor Gray
Write-Host "  * Para verificacion completa:   .\scripts\check.ps1" -ForegroundColor Gray
Write-Host "  * Para verificacion express:    .\scripts\check.ps1 -Fast" -ForegroundColor Gray
Write-Host "=======================================================================" -ForegroundColor Cyan
Write-Host ""
