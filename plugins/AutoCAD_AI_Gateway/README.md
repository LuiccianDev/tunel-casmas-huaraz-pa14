# AutoCAD AI Gateway — Documentación Técnica y Guía de Uso

**Versión:** 1.0.0  
**Target Framework:** .NET 10 (`net10.0-windows`)  
**Plataforma Host:** Autodesk AutoCAD 2027 (x64)  
**Tecnología:** C# / AutoCAD Managed .NET API (`acmgd`, `acdbmgd`, `accoremgd`)

---

## 1. Propósito y Contexto del Proyecto

El **AutoCAD AI Gateway** es un plugin nativo para Autodesk AutoCAD 2027 que actúa como un puente de comunicación bidireccional entre Modelos de Inteligencia Artificial (agentes de desarrollo, scripts externos) y la sesión activa de AutoCAD.

### ¿Por qué surgió esta solución?
1. **Limitaciones de AutoLISP puro:** Las rutinas tradicionales de AutoLISP ejecutadas mediante archivos `.lsp` no pueden interactuar de forma transparente con comandos definidos por plugins externos compilados o herramientas complejas de terceros como **YQArch** (arrojando errores de *"Unknown command"* al ejecutarse desde la función `(command)`).
2. **Automatización en Tiempo Real:** Permite a una IA o a un proceso en segundo plano "teclear" comandos directamente en AutoCAD, dibujar geometrías paramétricas, alternar vistas y controlar capas sin intervención manual del usuario.

---

## 2. Arquitectura Interna del Gateway

El plugin implementa una arquitectura desacoplada basada en un servidor HTTP embebido y un despachador seguro de hilos hacia el motor de AutoCAD:

```
[ Agente IA / Script Python ]
              │
              │  HTTP POST /execute (JSON Payload)
              ▼
    [ HttpListener (8080) ]  ───> Hilo en Segundo Plano (Thread Pool)
              │
              ▼
   [ ConcurrentQueue<string> ] ───> Almacén Concurrente (Thread-Safe)
              │
              ▼
    [ Application.Idle ]      ───> Despacho al Hilo Principal (UI Thread)
              │
              ▼
 [ SendStringToExecute ]      ───> Inyección con Auto-Cancelación (\x03\x03)
              │
              ▼
     [ Consola AutoCAD ]      ───> Dibuja entidades / Ejecuta YQArch
```

### Componentes Clave:
* **`Main.cs`:** Punto de entrada que implementa `IExtensionApplication`. Inicializa el plugin, escribe mensajes de diagnóstico en la línea de comandos de AutoCAD y expone los comandos de consola `AI_START_SERVER` y `AI_STOP_SERVER`.
* **`HttpGateway.cs`:**
  * **Servidor HTTP:** Implementado con `System.Net.HttpListener` escuchando en `http://localhost:8080/`. Cuenta con soporte de encabezados CORS para llamadas locales.
  * **Cola Concurrente (`ConcurrentQueue<string>`):** Protege contra condiciones de carrera si la IA envía múltiples ráfagas de comandos antes de que AutoCAD termine un ciclo de renderizado.
  * **Sincronización de Hilo UI (`Application.Idle`):** AutoCAD es una aplicación de un solo hilo principal para su interfaz y base de datos. Ningún comando puede ejecutarse directamente desde el hilo de red. El gateway se suscribe al evento `Application.Idle`, inyecta la cola acumulada y se desuscribe inmediatamente (`-= _idleHandler`) para prevenir ciclos infinitos.
  * **Mecanismo de Auto-Cancelación Defensiva:** Cada comando inyectado es envuelto entre dobles secuencias `\x03\x03` (`Ctrl+C` / `ESC`). Esto cancela cualquier comando interactivo que haya quedado congelado o en espera de datos, asegurando que el cursor del usuario siempre quede libre.

---

## 3. Requisitos de Instalación y Entorno

* **Sistema Operativo:** Windows 10/11 (64 bits).
* **AutoCAD:** Autodesk AutoCAD 2027 (requiere compatibilidad binaria estricta con .NET 10).
* **Entorno de Compilación:** SDK de .NET 10.0 (x64) instalado en `C:\Program Files\dotnet\sdk\10.x`.
* **Herramientas de Desarrollo:** VS Code con extensión C# / C# Dev Kit o Visual Studio 2022/2026.

---

## 4. Guía de Compilación e Implementación Paso a Paso

### Paso 1: Compilación de la Librería (.dll)
Abre una terminal de PowerShell en el directorio del proyecto y compila en modo optimizado `Release`:

```powershell
cd plugins/AutoCAD_AI_Gateway
dotnet build -c Release
```

*El archivo binario resultante se generará en:*  
`plugins/AutoCAD_AI_Gateway/bin/Release/net10.0-windows/AutoCAD_AI_Gateway.dll`

### Paso 2: Cargar el Plugin en AutoCAD
1. Abre **AutoCAD 2027**.
2. Asegúrate de tener al menos un dibujo abierto (`Drawing1.dwg`).
3. En la línea de comandos, escribe:
   ```
   NETLOAD
   ```
4. En el explorador de archivos, navega a la ruta de la `.dll` generada y selecciónala.
5. Si AutoCAD muestra una advertencia de seguridad, haz clic en **"Cargar siempre"** (*Always Load*).

### Paso 3: Iniciar el Servidor de Escucha
En la línea de comandos de AutoCAD, escribe:
```
AI_START_SERVER
```
Verás la confirmación en la consola:
```text
>>> [ON] AI Gateway Server escuchando en http://localhost:8080/
```

*(Si necesitas apagar el servidor temporalmente, ejecuta `AI_STOP_SERVER`).*

---

## 5. Especificación del Endpoint HTTP

### `POST /execute`
Inyecta una cadena de comandos directamente en la línea de órdenes de AutoCAD.

* **URL:** `http://localhost:8080/execute`
* **Método:** `POST`
* **Headers:** `Content-Type: application/json`

#### Formato de Solicitud (JSON):
```json
{
  "command": "_.RECTANG\n0,0\n25,15\n_.ZOOM\nE\n"
}
```

#### Respuestas HTTP:
* **`200 OK`:**
  ```json
  {
    "status": "success",
    "message": "Comando encolado correctamente"
  }
  ```
* **`400 Bad Request`:**
  ```json
  {
    "status": "error",
    "message": "JSON invalido. Se requiere la clave 'command'."
  }
  ```

---

## 6. Ejemplos de Inyección desde Diferentes Lenguajes

### Desde PowerShell:
```powershell
$payload = @{
    command = "_.RECTANG`n0,0`n30,20`n_.ZOOM`nE`n"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8080/execute" -Method Post -ContentType "application/json" -Body $payload
```

### Desde Python:
```python
import requests

url = "http://localhost:8080/execute"
payload = {"command": "_.LINE\n0,0\n50,0\n50,20\n\n_.ZOOM\nE\n"}
response = requests.post(url, json=payload)
print(response.json())
```

### Desde cURL (Terminal Bash / Git Bash):
```bash
curl -X POST http://localhost:8080/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "_.CIRCLE\n0,0\n15\n"}'
```

---

## 7. Reglas y Paradigmas de Seguridad

Para garantizar estabilidad total y evitar bloqueos en AutoCAD, la IA y los desarrolladores deben seguir estos principios:

1. **Prevenir Cuadros de Diálogo Modales (Regla de Oro):**
   * AutoCAD detiene la ejecución si se abre una ventana modal de Windows (ej. selección de archivo, gestor de capas con GUI).
   * **Obligatorio:** Utilizar versiones de consola con el prefijo `-` o `_.-`:
     * Usar `_.-LAYER` en lugar de `LAYER`.
     * Usar `_.-INSERT` en lugar de `INSERT`.
     * Usar `_.-STYLE` en lugar de `STYLE`.
2. **Internacionalización con `_.`:**
   * AutoCAD interpreta comandos en diferentes idiomas. Anteponer `_.` garantiza que `_.LINE` funcione tanto en AutoCAD en inglés como en español (`_` invoca el comando global en inglés, `.` evita alias redefinidos).
3. **Delimitación de Saltos de Línea (`\n`):**
   * Cada pulsación de `Enter` en AutoCAD debe representarse explícitamente con `\n`. Si se omite, AutoCAD permanecerá esperando el siguiente valor de coordenada.
4. **Auto-Cierre Defensivo:**
   * El plugin añade automáticamente dobles caracteres de escape (`\x03\x03`) al final de la orden. Esto garantiza que comandos continuos (como `LINE` o `PLINE`) terminen limpiamente y no capturen el ratón del operador.

---

## 8. Capacidades y Alcance

* [x] **Comandos Nativos:** Generación completa de polilíneas, círculos, cotas, bloques, hatch y textos.
* [x] **Compatibilidad con YQArch:** Ejecución de comandos del toolkit YQArch (muros `WW`, ejes `ZX`, columnas, etc.) sin conflicto de LISP.
* [x] **Expresiones LISP:** Inyección de macros AutoLISP complejas en una sola línea (ej. `(setq pt (list 10 20 0))` o llamadas a funciones cargadas).
* [x] **Navegación:** Control de encuadres (`_.ZOOM`), vistas axonométricas y regeneración de pantalla (`_.REGEN`).

---

## 9. Limitaciones Técnicas y Consideraciones

* **Requiere Documento Activo:** El servidor HTTP rechazará silenciosamente o ignorará comandos si no hay ningún dibujo abierto en AutoCAD (`MdiActiveDocument` es nulo).
* **Entrada Asíncrona:** `SendStringToExecute` coloca los caracteres en el buffer de entrada de AutoCAD; se ejecuta de forma asíncrona tan pronto como AutoCAD termina su tarea actual.
* **Puerto Único Local:** El servidor está enlazado a `http://localhost:8080/`. No debe haber otro servicio (como un servidor web de desarrollo o contenedor Docker) usando el puerto 8080 simultáneamente.
