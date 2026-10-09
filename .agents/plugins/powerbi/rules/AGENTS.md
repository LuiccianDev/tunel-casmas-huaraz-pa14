# Directivas del Plugin Power BI Modeling MCP

Este plugin gobierna la interacción del asistente con modelos semánticos de **Microsoft Power BI** (Power BI Desktop, proyectos PBIP/TMDL y Microsoft Fabric) a través del servidor oficial **Power BI Authoring MCP Server**.

---

## 1. Conexión y Protocolo de Inicio

1. **Conexión Obligatoria Previa:**
   - Antes de realizar cualquier cálculo, consulta o modificación, el asistente DEBE asegurarse de que la conexión al modelo esté activa.
   - Si se trabaja con **Power BI Desktop**, el archivo `.pbix` debe estar abierto en la máquina local.
   - En proyectos **PBIP / TMDL**, apuntar a la ruta de la carpeta de definición del modelo.
   - Conectar explícitamente mediante la herramienta de conexión (`connection_operations`):
     - Ejemplo: *"Conectar a '[Nombre del Archivo]' en Power BI Desktop"*.

2. **Aceptación de Licencia:**
   - El servidor está configurado con `--accept-eula` y `PBI_MODELING_MCP_ACCEPT_EULA: true` para operar sin interrupciones.

---

## 2. Buenas Prácticas de Modelado y DAX

1. **Inspección Previa (No Asumir Esquemas):**
   - El asistente NUNCA debe inventar nombres de tablas, columnas o medidas.
   - Siempre debe consultar la estructura del modelo (`database_operations`, `table_operations` o `column_operations`) antes de redactar o modificar medidas.

2. **Creación y Modificación de Medidas DAX:**
   - Utilizar `measure_operations` para agregar o actualizar fórmulas DAX.
   - Seguir las convenciones estándar de formato DAX (saltos de línea para legibilidad, uso de variables `VAR` / `RETURN`).
   - Validar las medidas ejecutando consultas DAX de prueba mediante `dax_query_operations` (`EVALUATE ...`).

3. **Integridad del Modelo:**
   - Crear relaciones explícitas con cardinalidad y dirección de filtro correctas mediante `relationship_operations`.
   - Evitar relaciones bidireccionales innecesarias para preservar el rendimiento del motor tabular VertiPaq.
   - Aplicar el evaluador de mejores prácticas del modelo para detectar columnas no utilizadas o medidas redundantes.

---

## 3. Catálogo de Herramientas y Protocolo Multiplexor (Skill: powerbi-modeling-tools)

1. **Catálogo Extendido (21 Herramientas Multiplexoras):**
   - Para consultar el desglose exhaustivo de las 21 herramientas compuestas (`connection_operations`, `measure_operations`, `table_operations`, etc.), operaciones y esquemas de payload, consulta la skill oficial `powerbi-modeling-tools` ubicada en `skills/powerbi-modeling-tools/SKILL.md`.

2. **Estructura de Llamadas Multiplexoras:**
   - Toda llamada al servidor debe empaquetar los parámetros en un objeto `request` con el atributo obligatorio `operation`:
     - Crear/Actualizar: `definitions: [...]`
     - Eliminar/Consultar: `references: [...]`
     - Mover medidas entre tablas: `moveDefinitions: [...]` (nunca usar `Update` para reasignar tabla).

3. **Operaciones Transaccionales Seguras:**
   - En cambios masivos de medidas, columnas o tablas, configurar siempre `options: { "useTransaction": true, "continueOnError": false }` para evitar que el modelo quede en un estado corrupto o inconsistente.

