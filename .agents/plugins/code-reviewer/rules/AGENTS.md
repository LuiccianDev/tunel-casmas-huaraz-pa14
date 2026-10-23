# Reglas de Revisión de Código, Clean Code y Arquitectura (Graphify-First)

Al momento de revisar código, refactorizar o auditar la calidad en el proyecto **Túnel Casmas Huaraz PA14**, el asistente DEBE aplicar estrictamente las siguientes directivas:

---

## 1. Prohibición de Búsquedas Ciegas y Uso de Graphify MCP
* **NUNCA** utilices búsquedas de texto completas iterativas ni leas archivos enteros a ciegas para entender dependencias.
* Utiliza **SIEMPRE** el servidor MCP de Graphify (`graphify_graphify`) para auditar la red de dependencias y el estado arquitectónico consumiendo mínimos tokens.
* Si el grafo no existe, inicialízalo de inmediato:
  ```powershell
  uvx --from graphifyy graphify update .
  ```

---

## 2. Estándares Estrictos de Clean Code y Modularidad (Anti-Espagueti)
1. **Principio de Responsabilidad Única (SRP):**
   * Separación tajante entre cálculo (`modulos/`), persistencia/presentación (`excel.py`, `lisp.py`) y orquestación (`main.py`).
   * Prohibido crear archivos "todoterreno". Si un módulo crece más allá de 400-500 líneas, debe dividirse en un subpaquete limpio (como `src/casmas_pa14/lisp_campamento/`).
2. **Cero Números Mágicos (Hardcoding):**
   * Bloqueo inmediato a cualquier intento de introducir constantes numéricas no documentadas o calculadas estáticamente en el código. Toda constante debe leerse de `parametros.toml` o de `ctx`.
3. **Nombrado Expresivo:**
   * Nombres en español técnico, consistentes con la jerga de ingeniería de túneles y carreteras.

---

## 3. Protocolo de Cierre y Verificación Obligatoria
Antes de dar por finalizada cualquier refactorización o cambio de código, el revisor debe exigir la ejecución exitosa de:
```powershell
uv run ruff check --fix .
uv run ruff format .
uv run pytest -q
.\scripts\check.ps1 -Fast
```
Y si hubo cambios estructurales en módulos, actualizar el grafo con `uvx --from graphifyy graphify update .`.
