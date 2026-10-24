# Code Reviewer & Anti-Spaghetti (`code-reviewer`)

Plugin de auditoría estructural, prevención de código espagueti y optimización de contexto mediante análisis arquitectónico previo.

## Contenido del Paquete

### Subagentes Especializados (`agents/`)
- **`auditor_qa` (`auditor-qa-pa14`)**: Subagente auditor de Clean Code, ejecutor del ciclo `check.ps1`, custodio de la sincronización en cascada de los READMEs (*Living Documentation*) y auditoría con Graphify MCP.

### Reglas (`rules/AGENTS.md`)
- Flujo obligatorio *Graphify-First* antes de refactorizar o auditar módulos.
- Verificación del Principio de Responsabilidad Única (SRP) y separación estricta entre cálculo y presentación.
- Prohibición de búsquedas ciegas y uso preferencial del servidor MCP `graphify_graphify`.

### Skills (`skills/`)
- **`clean-code`**: Auditoría de Clean Code, principio de responsabilidad única (SRP), eliminación de antipatrones espagueti y refactorización guiada.
- **`thermo-nuclear-code-quality-review`: Auditoría exhaustiva de mantenibilidad, simplificación estructural (*code judo*), control de tamaño de archivos y eliminación de ramificaciones ad-hoc.
