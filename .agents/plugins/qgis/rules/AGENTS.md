# Directivas del Plugin QGIS MCP (Conexión Segura)

Este plugin gobierna la interacción del asistente con el software SIG **QGIS Desktop** (versiones 3.28 a 4.x) a través del servidor oficial **QGIS MCP**.

---

## 1. Protocolo de Conexión y Seguridad

1. **Autenticación Obligatoria:**
   - La comunicación con el socket TCP interno de QGIS está protegida por el token de seguridad `pa14-qgis-token-casmas-2026` inyectado mediante la variable `QGIS_MCP_TOKEN`.
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
