# Code Reviewer & Anti-Spaghetti (`code-reviewer`)

Plugin de auditoría estructural, prevención de código espagueti y optimización de contexto mediante análisis arquitectónico previo.

## Contenido del Paquete

- **Reglas (`rules/AGENTS.md`)**:
  - Flujo obligatorio *Graphify-First* antes de refactorizar o auditar módulos.
  - Verificación del Principio de Responsabilidad Única (SRP) y separación estricta entre cálculo y presentación.
- **Skills (`skills/`)**:
  - `thermo-nuclear-code-quality-review`: Auditoría exhaustiva de mantenibilidad, simplificación estructural (*code judo*), control de tamaño de archivos y eliminación de ramificaciones ad-hoc.
