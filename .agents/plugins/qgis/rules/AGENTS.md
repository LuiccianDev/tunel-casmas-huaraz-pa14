# Directivas del Plugin QGIS MCP (Conexión Segura)

Este plugin gobierna la interacción del asistente con el software SIG **QGIS Desktop** (versiones 3.28 a 4.x) a través del servidor oficial **QGIS MCP**.

---

## 1. Protocolo de Conexión y Seguridad

1. **Autenticación Obligatoria y Seguridad Zero-Secrets:**
   - La comunicación con el socket TCP interno de QGIS está protegida por un token de seguridad administrado localmente mediante la variable de entorno `QGIS_MCP_TOKEN`.
   - **Regla Zero-Secrets:** NUNCA exponer contraseñas ni el token `QGIS_MCP_TOKEN` dentro de los archivos de configuración (`mcp_config.json`, `.vscode/mcp.json`). El proceso del servidor MCP (`uvx ... qgis-mcp-server`) hereda esta variable de entorno de forma automática desde el sistema operativo.
   - Los parámetros de red `QGIS_MCP_HOST` (`localhost`) y `QGIS_MCP_PORT` (`9876`) se configuran en el bloque `env` del cliente o se dejan por defecto.
   - Si el plugin de QGIS no tiene este token configurado o no se encuentra iniciado (*Start Server*), las llamadas fallarán con error de autenticación o conexión rechazada.

2. **Verificación de Enlace Inicial (Liveness):**
   - Antes de iniciar cualquier serie de operaciones geoespaciales, el asistente debe invocar la herramienta `ping`.
   - Se debe verificar que la respuesta sea `{"pong": true}` antes de continuar con la creación o modificación de capas.

---

## 2. Buenas Prácticas Geoespaciales y de Operación

1. **Inspección Previa de Capas:**
   - NUNCA asumir la existencia o nombres de capas en el proyecto activo.
   - Consultar siempre las capas cargadas en el proyecto antes de intentar leerlas, editarlas o añadir datos sobre ellas.

2. **Sistemas de Coordenadas de Referencia (CRS / SRC):**
   - En el proyecto del Túnel Casmas Huaraz PA14, verificar explícitamente el sistema de coordenadas de las capas y del proyecto.
   - En proyectos peruanos, la referencia estándar en coordenadas métricas planas es **WGS 84 / UTM Zona 18S (EPSG:32718)**, o en coordenadas geográficas **WGS 84 (EPSG:4326)**. Toda reproyección o cálculo de distancia/área métrica debe garantizar el uso del SRC proyectado correspondiente.

3. **Operaciones No Destructivas:**
   - Al realizar transformaciones, buffers, intersecciones o reclasificaciones, preferir siempre generar **nuevas capas vectoriales en memoria o archivos derivados**, evitando sobrescribir fuentes de datos originales (`.shp`, `.gpkg`, `.geojson`) sin confirmación explícita del usuario.

---

## 3. Catálogo de Herramientas y Patrones de Ejecución (Skill: qgis-mcp-tools)

1. **Catálogo Extendido (125 Herramientas):**
   - Para consultar el desglose exhaustivo de endpoints, recursos (`qgis://`) y prompts integrados, consulta la skill oficial `qgis-mcp-tools` ubicada en `skills/qgis-mcp-tools/SKILL.md`.

2. **Edición Transaccional Vectorial:**
   - Toda modificación de atributos o geometrías sobre capas existentes debe seguir la secuencia transaccional:
     `start_editing` -> `add_features` / `update_features` / `update_feature_geometry` -> `commit_edits` (o `rollback_edits` si se detecta error).

3. **Geoprocesamiento Pesado y Segundo Plano:**
   - Algoritmos que tomen más de 55 segundos deben lanzarse mediante `start_processing_job` y monitorearse con `get_processing_job` para evitar desconexiones por tiempo de espera en el socket.

