# Directivas del Plugin AutoCAD Gateway

Este plugin gobierna el desarrollo, mantenimiento y comunicación segura con el plugin nativo **AutoCAD AI Gateway** (.NET 10 / C#) y su integración con AutoCAD 2027.

---

## 1. Estándares de Código C# y .NET (Clean Code & Best Practices)

1. **Responsabilidad Única (SRP):**
   - El punto de entrada (`Main.cs`) solo registra comandos de AutoCAD e inicializa el ciclo de vida de la extensión (`IExtensionApplication`).
   - La capa de red y despacho (`HttpGateway.cs`) gestiona el servidor HTTP y el encolado seguro de comandos.
   - Si se añade lógica geométrica o de entidades AutoCAD en C#, debe ir en clases de servicio dedicadas bajo `src/Services/`.

2. **Concurrencia y Seguridad de Hilos (Thread Safety):**
   - **Prohibido** modificar directamente el documento activo de AutoCAD (`MdiActiveDocument`) desde los hilos de `HttpListener`.
   - Toda interacción con la base de datos o consola de AutoCAD **debe** canalizarse a través de la cola concurrente (`ConcurrentQueue<string>`) despachada en el evento `Application.Idle` o a través del `Dispatcher` del hilo principal.
   - Los manejadores de eventos (como `_idleHandler`) deben desacoplarse inmediatamente tras la ejecución para evitar bucles infinitos en el hilo UI.

3. **Buenas Prácticas de .NET (.NET 10):**
   - Respetar el contexto de nulabilidad (`#nullable enable`). No ignorar advertencias de tipo nulo (`CS8600`, `CS8602`, `CS8625`).
   - Usar `CancellationToken` y `async/await` estructurado para tareas de red.
   - En caso de compilaciones, usar siempre la configuración `Release`:
     ```powershell
     dotnet build -c Release plugins/AutoCAD_AI_Gateway/AutoCAD_AI_Gateway.csproj
     ```

4. **Documentación de Código (C# Docs):**
   - Todo método o clase pública debe contar con comentarios XML (`/// <summary>`) describiendo parámetros y excepciones posibles.

---

## 2. Protocolo de Comunicación IA <-> AutoCAD

Cuando el asistente interactúa con AutoCAD a través del Gateway, debe apegarse estrictamente a las siguientes reglas:

1. **Endpoint y Transporte:**
   - URL: `http://localhost:8080/execute`
   - Método: `POST`
   - Content-Type: `application/json`
   - Formato Payload:
     ```json
     {
       "command": "_.LINE\n0,0\n20,0\n\n"
     }
     ```

2. **Construcción de Comandos Seguros:**
   - **Comandos en Modo Texto:** Siempre utilizar el prefijo `_.-` para comandos que normalmente abran cuadros de diálogo modales (ej. `_.-LAYER` en lugar de `LAYER`, `_.-INSERT` en lugar de `INSERT`). Si AutoCAD muestra una ventana modal de Windows, la conexión remota se bloqueará hasta que un humano haga clic.
   - **Terminadores de Entrada:** Asegurarse de enviar los saltos de línea `\n` requeridos por cada solicitud de AutoCAD.
   - **Auto-Cancelación:** El Gateway inyecta automáticamente doble código de cancelación `\x03\x03` (`Ctrl+C` / `ESC`) antes y después del comando para garantizar que AutoCAD no quede en estado de espera ("pegado").
   - **Internacionalización:** Usar el prefijo `_.` en los comandos nativos (ej. `_.RECTANG`, `_.LINE`, `_.ZOOM`, `_.PLINE`) para asegurar compatibilidad en versiones de AutoCAD en español o inglés.

3. **Envío de Comandos vía PowerShell:**
   - La IA debe utilizar el patrón estándar:
     ```powershell
     $payload = @{ command = "_.RECTANG`n0,0`n10,10`n_.ZOOM`nE`n" } | ConvertTo-Json
     Invoke-RestMethod -Uri "http://localhost:8080/execute" -Method Post -ContentType "application/json" -Body $payload
     ```
