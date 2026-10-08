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
- [x] Datos geológicos estructurados (02) → densidad, esponjamiento, K, factor de carga
- [x] Sección definitiva del túnel: ancho y altura (03)
- [x] Altitud real de la obra (3850 msnm, ventilación)
- [x] Confirmar dotación, distancias mínimas y criterios con el docente / norma

## Fase 2 · Entregables
| # | Entregable | Módulo | Excel | Estado |
|---|-----------|--------|-------|--------|
| 01 | Ubicación y coordenadas | `m01_ubicacion` | `01_Ubicacion.xlsx` | [x] oficial |
| 02 | Geología | `m02_geologia` | `02_Geologia.xlsx` | [x] oficial (perfil longitudinal 5,556 m, Q-Slope y zonificación) |
| 03 | Sección del túnel | `m03_seccion` | `03_Seccion.xlsx` | [x] oficial (13.30x9.58 m, gálibo 11.80x5.50 m, verificación MTC) |
| 04 | Personal | `m04_personal` | `04_Personal.xlsx` | [x] oficial (346 pax, MOD/MOI, fórmulas 100% dinámicas SUMIFS en desgloses, totales y %, memoria) |
| 05 | Campamento y edificaciones | `m05_campamento` | `05_Campamento.xlsx` | [x] base |
| 06 | Maquinaria (frente, botadero, campamento) | `m06_maquinaria` | `06_Maquinaria.xlsx` | [x] oficial (fichas técnicas, cálculo de rendimientos teórico y real, tablas Caterpillar/Epiroc) |
| 07 | Polvorín | `m07_polvorin` | `07_Polvorin.xlsx` | [x] base |
| 08 | PETAP, PETAR, pozo y consumo de agua | `m08_agua` | `08_Agua.xlsx` | [x] base |
| 09 | Ventilación y consumo eléctrico | `m09_electricidad` | `09_Electricidad.xlsx` | [x] base |
| 10 | Cronograma | `m10_cronograma` | `10_Cronograma.xlsx` | [x] base |
| 11 | Portales y Banquetas | `m11_portales` | `11_Portales.xlsx` | [x] base |
| 12 | Voladura Konya | `m12_voladura` | `12_Voladura.xlsx` | [x] base |
| 13 | Sostenimiento (Bieniawski / Barton) | `m13_sostenimiento` | `13_Sostenimiento.xlsx` | [x] base |

## Fase 3 · Planos AutoCAD (`PA14_dibujos.lsp`)
- [x] Plano de ubicación general (puntos UTM y traza del eje: `PA14_UBICACION`)
- [x] Sección típica (herradura con cotas)
- [x] Distribución del campamento
- [x] Plantas de polvorines (explosivos y accesorios)
- [x] PETAP (reservorio) y PETAR (tanque séptico)
- [x] Huella del botadero
- [x] Plano arquitectónico EDIF-01: Modular Dormitorio Staff (Planta Nivel 1 y Sección A-A' - AR-DM-001 REV B: comandos `PA14_CAMP1_EDIF01_DORMITORIO`, `PA14_CAMP1_DORMITORIO`, `PA14_EDIF01`)
- [x] Malla de perforación y disparo (`PA14_MALLA`: cuñe cilíndrico de 4 secciones, ayudas, zapateras, corona y cuadro de parámetros)

## Fase 4 · Marco Regulatorio y Armonización Normativa
- [x] Elaboración de `docs/MARCO_REGULATORIO_Y_TECNICO.md` (normativa MTC, SUCAMEC, MINEM, OSINERGMIN, ANA, MINAM, RNE)
- [x] Armonización de `datos/parametros.toml` con citas legales exactas y eliminación de marcas (S) verificadas
- [x] Inclusión de secciones normativas estructuradas ([normativa_mtc], [normativa_sucamec], [normativa_seguridad_subterranea], [normativa_hidrocarburos], [normativa_recursos_hidricos], [normativa_residuos_dme], [normativa_efluentes_ptar], [normativa_saneamiento_rne])
- [x] Corrección de cita reglamentaria en EDIF-16 (D.S. 003-2010-MINAM para efluentes PTAR doméstica)
- [x] Verificación cruzada y conformidad de suite `uv` (`ruff format`, `ruff check`, `pytest`, `pa14`)

## Fase 5 · Cierre
- [x] Revisión de todos los `(S)` restantes (geología por usuario)
- [x] Eliminación de parámetros por defecto en código Python (auditoría arquitectónica TOML)
- [ ] Revisión cruzada de unidades y resultados
- [ ] Informe final / presentación

---

### Notas de Verificación Técnica
- **AutoCAD**: unidades forzadas a metros, plano de ubicación en UTM real (WGS84 18L), detalles con origen fijo al sur; sin punto de inserción manual.
- **03 Sección**: sección real del plano CAD (13.30 x 9.58 m), gálibo 11.80 x 5.50 m, verificación MTC (hoja 'Justificacion MTC') y memoria generada en `docs/memoria/03_Seccion.md`.
- **Marco Regulatorio**: Valores (S) de `[seccion.norma]` (berma 1.20 m según DG-2018 Tabla 304.02, altura sobre vereda 2.40 m según RD 036-2016-MTC/14, longitud de emergencia 500 m) y `[polvorin]` (stock 15 días, rumas 1.50 m, unidades por caja según Ley 30299 / DS 010-2017-IN) plenamente verificados y justificados.
