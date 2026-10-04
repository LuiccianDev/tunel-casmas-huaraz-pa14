# Planificación y control de tareas — Túnel Casmas Huaraz PA14

Leyenda: `[x]` hecho · `[/]` en curso · `[ ]` pendiente.

## Fase 0 · Base del proyecto
- [x] Entorno `uv` + Python 3.12 + Ruff + pytest
- [x] `README.md`, `AGENTS.md`, `.gitignore`
- [x] Parámetros centralizados en `datos/parametros.toml`
- [x] Generador de Excel con formato único
- [x] Generador AutoLISP
- [ ] `git init` y primer commit

## Fase 1 · Datos reales (reemplazar supuestos `(S)`)
- [x] Coordenadas reales de portales e instalaciones (01)
- [ ] Datos geológicos estructurados (02) → densidad, esponjamiento, K, factor de carga
- [ ] Sección definitiva del túnel: ancho y altura (03)
- [x] Altitud real de la obra (3850 msnm, ventilación)
- [ ] Confirmar dotación, distancias mínimas y criterios con el docente / norma

## Fase 2 · Entregables
| # | Entregable | Módulo | Excel | Estado |
|---|-----------|--------|-------|--------|
| 01 | Ubicación y coordenadas | `m01_ubicacion` | `01_Ubicacion.xlsx` | [x] oficial |
| 02 | Geología | `m02_geologia` | `02_Geologia.xlsx` | [ ] espera datos |
| 03 | Sección del túnel | `m03_seccion` | `03_Seccion.xlsx` | [ ] espera datos |
| 04 | Personal | `m04_personal` | `04_Personal.xlsx` | [x] oficial (346 pax, MOD/MOI, memoria) |
| 05 | Campamento y edificaciones | `m05_campamento` | `05_Campamento.xlsx` | [x] base |
| 06 | Maquinaria (frente, botadero, campamento) | `m06_maquinaria` | `06_Maquinaria.xlsx` | [x] base |
| 07 | Polvorín | `m07_polvorin` | `07_Polvorin.xlsx` | [x] base |
| 08 | PETAP, PETAR, pozo y consumo de agua | `m08_agua` | `08_Agua.xlsx` | [x] base |
| 09 | Ventilación y consumo eléctrico | `m09_electricidad` | `09_Electricidad.xlsx` | [x] base |
| 10 | Cronograma | `m10_cronograma` | `10_Cronograma.xlsx` | [x] base |

## Fase 3 · Planos AutoCAD (`PA14_dibujos.lsp`)
- [x] Plano de ubicación general (puntos UTM y traza del eje: `PA14_UBICACION`)
- [x] Sección típica (herradura con cotas)
- [x] Distribución del campamento
- [x] Plantas de polvorines (explosivos y accesorios)
- [x] PETAP (reservorio) y PETAR (tanque séptico)
- [x] Huella del botadero
- [ ] Malla de perforación (cuando haya diseño con geología)

## Fase 4 · Cierre
- [ ] Revisión de todos los `(S)` restantes
- [ ] Revisión cruzada de unidades y resultados
- [ ] Informe final / presentación

- [x] AutoCAD: unidades forzadas a metros, plano de ubicacion en UTM real (WGS84 18L), detalles con origen fijo al sur; sin punto de insercion manual.
- [x] 03 Seccion: seccion real del plano CAD (13.30 x 9.58 m), galibo 11.80 x 5.50 m, verificacion MTC (hoja 'Justificacion MTC') y memoria generada en docs/memoria/03_Seccion.md.
- [ ] Verificar en el texto oficial los valores (S) de [seccion.norma] (berma, altura sobre vereda, zonas de emergencia).
