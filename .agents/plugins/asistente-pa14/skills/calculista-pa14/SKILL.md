---
name: calculista-pa14
description: "Protocolo de cálculo de ingeniería subterránea, reactividad en cadena TOML -> ctx y compilación de fórmulas dinámicas en Excel para el Túnel Casmas Huaraz PA14."
---

# Calculista de Ingeniería PA14

Esta habilidad gobierna el flujo de trabajo de cálculo de los 13 módulos de ingeniería del **Túnel Casmas Huaraz PA14** (geometría, geología, sección tipo, personal, campamento, maquinaria, polvorín, agua, electricidad, cronograma, portales, voladura, sostenimiento y banquetas).

---

## 1. Cadena de Reactividad Integral (Efecto Dominó)

Todo cálculo debe seguir estrictamente este flujo unidireccional y reactivo:

```
[datos/parametros.toml] ──> [mNN_modulo.calcular(p, ctx)] ──> [ctx] ──> [mNN_modulo.libro(r, p)]
         ▲                                                                      │
         └───────────── Única Fuente de Verdad ─────────────────────────────────┘
```

1. **Parámetro de Entrada:** Se documenta en `datos/parametros.toml` con unidad, descripción y fuente normativa. Si es un supuesto, se marca con `(S)`.
2. **Cálculo en Python (`calcular(p, ctx)`):**
   * Lee entradas desde `p["clave"]` o desde módulos previos calculados en `ctx["clave_previa"]`.
   * **Prohibido recalcular** lo que ya calculó otro módulo.
   * Retorna un diccionario `dict` de resultados.
3. **Generación de Libro Excel (`libro(r, p)`):**
   * **Prohibido escribir valores precalculados estáticos.**
   * Las celdas deben escribirse como **fórmulas nativas referenciadas** usando `{Simbolo}`:
     ```python
     formula = "={Q}*{E}/({T}*{Fv})"
     ```
   * El compilador `excel.py` traduce automáticamente `{Simbolo}` a la coordenada de celda (ej. `C15`), garantizando que si el usuario cambia un dato en Excel, todo se recalcule en vivo.

---

## 2. Tipografía y Estándar Visual Institucional de Excel

* **Tamaño de fuente estricto:** `11 pt` en TODO el libro (títulos, encabezados, datos y totales).
* **Encabezados:** Fondo verde institucional (`#2E7D32`), texto en **blanco y negrita**.
* **Totales:** Fondo verde muy suave (`#E8F5E9`), texto en **negrita**.
* **Estructura de tabla estándar:** `Descripción | Símbolo | Valor | Unidad | Fórmula / Fuente`.

---

## 3. Verificación Post-Cálculo
Tras modificar o agregar un cálculo:
```powershell
uv run pytest tests/test_calculos.py -q
uv run pa14
```
