---
name: auditor-normativo
description: "Protocolo de trazabilidad y consulta eficiente de normas técnicas peruanas (DG-2018 MTC, DS 024-2016-EM, RNE, SUCAMEC) mediante rangos de líneas sin quemar tokens."
---

# Auditor Normativo Peruano (PA14)

Esta habilidad asegura que cada parámetro, fórmula o dimensión adoptada en el proyecto cuente con respaldo en la legislación y normativa técnica peruana vigente, optimizando el consumo de tokens.

---

## 1. Marco Normativo Oficial del Proyecto

| Norma | Ámbito de Aplicación | Archivo de Consulta (`docs/entradas/`) |
|---|---|---|
| **MTC DG-2018** | Diseño geométrico de carretera, calzada, peraltes, sobreanchos y banquetas | `manual_de_carreteras_dg_2018.md` |
| **DS 024-2016-EM** | Seguridad y salud ocupacional en minería (ventilación, refugios, polvorines) | `decreto_supremo_024_2016_em.md` |
| **RNE (Perú)** | Edificaciones de campamento (A.010, A.070, A.080) e instalaciones sanitarias (OS.010 a OS.090) | Documentación técnica en `docs/entradas/` |
| **Directiva SUCAMEC** | Polvorines principales, auxiliares y distancias de seguridad (barricadas) | Parámetros en `m07_polvorin.py` y `parametros.toml` |
| **Modelo de Konya** | Fórmulas de burden, espaciamiento, taco y mallas de voladura subterránea | `ejemplo_resolucion_modelo_konya.md` |

---

## 2. Protocolo de Ahorro de Tokens (Zero Blind Search)

1. **Prohibido leer archivos PDF directamente.**
2. **Consulta Rápida por Coordenadas:**
   * Antes de abrir `manual_de_carreteras_dg_2018.md`, consulta primero:
     👉 [`docs/entradas/indice_dg2018.md`](../../../../docs/entradas/indice_dg2018.md)
   * Localiza la tabla o artículo de interés y abre **únicamente el rango de líneas** requerido (`StartLine` a `EndLine`, ~40-60 líneas).
3. **Marcado de Supuestos:**
   * Si un parámetro no figura de forma explícita en la norma, debe documentarse en `datos/parametros.toml` agregando la marca `(S)` y avisando al usuario en la memoria de cálculo.
