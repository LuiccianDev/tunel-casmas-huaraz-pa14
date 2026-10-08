# Guía de Uso de Graphify — Proyecto Túnel Casmas Huaraz PA14

Esta guía resume qué es **Graphify**, cómo está integrado en este repositorio y cómo aprovecharlo tanto desde la consola como dentro del asistente de IA (Antigravity).

---

## 1. ¿Qué es Graphify?

[Graphify](https://github.com/Graphify-Labs/graphify) es un motor que convierte cualquier base de código, documentación, esquemas y archivos en un **Grafo de Conocimiento (Knowledge Graph)** navegable y estructurado, sin depender de almacenes vectoriales externos (*no vector store*).

En este proyecto, Graphify genera:
* **`graphify-out/graph.html`**: Visualizador interactivo 2D/3D navegable desde el navegador.
* **`graphify-out/graph.json`**: Grafo de entidades y relaciones (AST + semántica).
* **`graphify-out/GRAPH_REPORT.md`**: Informe de auditoría con "God Nodes" (módulos clave), conexiones inesperadas y preguntas clave de arquitectura.

---

## 2. Integración en el Proyecto

Siguiendo las reglas de `AGENTS.md`:
* **Instalación Aislada**: Se instaló con `uv tool install graphifyy`. No contamina el `pyproject.toml` del proyecto.
* **Integración Antigravity**:
  * Regla activa: `.agents/rules/graphify.md` (indica al asistente consultar el grafo antes de responder preguntas complejas de arquitectura).
  * Flujo de trabajo: `.agents/workflows/graphify.md` y habilidad en `.agents/skills/graphify/SKILL.md`.
  * Servidor MCP: configurado en `~/.gemini/config/mcp_config.json` para que el asistente pueda consultar el grafo de forma nativa.

---

## 3. Comandos de Uso Diario

### A. Abrir el Visualizador Interactivo en tu Navegador
Simplemente abre el archivo generado en tu navegador web favorito (Chrome, Edge, etc.):
```powershell
Start-Process "graphify-out\graph.html"
```
*Puedes hacer clic en los nodos (`m01_ubicacion`, `m03_seccion`, `lisp.py`), ver cómo se conectan y explorar clusters de dependencias.*

### B. Actualizar el Grafo tras Modificar Código
Cuando agregues o modifiques módulos (`m14_ventilacion.py`, etc.), regenera el grafo de forma ultra rápida (solo analiza AST sin consumir tokens):
```powershell
uvx --from graphifyy graphify extract . --code-only
uvx --from graphifyy graphify cluster-only .
```
O simplemente:
```powershell
uvx --from graphifyy graphify update .
```

### C. Consultas Rápidas desde la Terminal (CLI)
Para encontrar cómo se relacionan componentes sin abrir los archivos:
```powershell
# 1. Consultar un concepto o función
uvx --from graphifyy graphify query "seccion"

# 2. Encontrar el camino más corto entre dos componentes
uvx --from graphifyy graphify path "m02_geologia" "m13_sostenimiento"

# 3. Explicar un nodo
uvx --from graphifyy graphify explain "generar_lisp"
```

### D. Usar Graphify desde el Chat con el Asistente
Puedes invocar el comando de barra directamente en la conversación:
* `/graphify .` — Analiza todo el repositorio y genera el informe completo.
* O simplemente preguntarle al asistente: *"¿Cómo se conecta el módulo de voladura con el módulo de secciones según el grafo de conocimiento?"* El asistente consultará automáticamente el grafo generado.

---

## 4. Estado Actual del Grafo del Túnel PA14

Al realizar la primera extracción estructural:
* **Nodos detectados:** 341 entidades (funciones, clases, constantes y módulos).
* **Conexiones (aristas):** 807 relaciones de llamadas, importaciones y dependencias.
* **Comunidades:** 21 clusters de arquitectura identificados.
* **Archivos clave (God Nodes):** `lisp.py`, `m06_maquinaria.py`, `excel.py`, `m03_seccion.py`.
