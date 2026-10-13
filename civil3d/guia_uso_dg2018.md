# Guía de uso: criterios DG-2018 (MTC Perú) en Civil 3D

Todo vive en esta carpeta del proyecto (`civil3d/`). **No se modificó ninguna carpeta global de Civil 3D.**
Para la documentación detallada de arquitectura, consulta [`civil3d/README.md`](./README.md).

- **Versión en Markdown (MarkItDown):** [`docs/entradas/manual_de_carreteras_dg_2018.md`](../docs/entradas/manual_de_carreteras_dg_2018.md)
- **Copia local del PDF:** [`docs/entradas/manual_de_carreteras_dg_2018.pdf`](../docs/entradas/manual_de_carreteras_dg_2018.pdf)
- **Fuente PDF en Google Drive (DG-2018 Carreteras):** [Manual de Carreteras: Diseño Geométrico DG-2018](https://drive.google.com/file/d/1kdXJQ1sfLHBTbPC3mbCcYBWaTW8UOO0C/view?usp=sharing)
- **Fuente PDF en Google Drive (MC-03-16 Túneles):** [Manual de Carreteras: Túneles, Muros y Obras Complementarias](https://drive.google.com/file/d/1IIdtiAq3M-wXH4l8uuyQueE2mOMJV9Xr/view?usp=drive_link)

| Archivo | Función |
|---|---|
| `dg2018_datos.toml` | Datos normativos verificados del DG-2018 (Tablas 202.01, 205.01, 205.03, 302.02, 304.01, 304.03, Art. 302.08, 302.09.03, 303.04 y Figura 304.07) |
| `generar_dg2018.py` | Genera el XML; verifica $R = V^2/(127(p+f))$ contra la Tabla 302.02 y precalcula las tablas automáticas de sobreancho por vehículo |
| `PA14_DG2018_MTC_Roadway_Design_Standards.xml` | Archivo de criterios para Civil 3D |

Regenerar: `uv run python civil3d/generar_dg2018.py`

---

## 1. Cargar en Civil 3D (Alineamiento Principal y Perfil)
1. *Create Alignment - Layout* (o *Alignment Properties*) → pestaña **Design Criteria**.
2. Marcar **Use criteria-based design** y **Use design criteria file**.
3. Botón `...` → examinar y elegir el XML **de esta carpeta** (`civil3d/PA14_DG2018_MTC_Roadway_Design_Standards.xml`).
4. En *Minimum Radius Table* elegir según ubicación de la vía:
   - `DG-2018 MTC eMax 4% - Area urbana`
   - `DG-2018 MTC eMax 6% - Rural con peligro de hielo`
   - `DG-2018 MTC eMax 8% - Rural plano u ondulado`
   - `DG-2018 MTC eMax 12% - Rural accidentado o escarpado`
5. *Attainment Method*: `DG-2018 MTC Bombeo (Crowned Roadway)`.
6. Para perfiles (*Create Profile - Layout* → **Design Criteria**): `DG-2018 MTC Curvas Verticales (Art. 303.04)`.

---

## 2. Cómo crear Offset Alignments y Sobreancho Automático (Sin Errores)

Cuando ejecutas **Alignment → Create Offset Alignment** en Civil 3D, sigue esta configuración exacta para evitar que los sobreanchos salgan deformados o duplicados:

### Paso A — Pestaña *General* (Desfase de Calzada)
- **No. of offsets on left / right**: `1` y `1`.
- **Incremental offset on left / right**: Ingresa el semiancho de tu calzada en tangente:
  - `3.60` m (para calzada de $7.20\text{ m}$)
  - `3.30` m (para calzada de $6.60\text{ m}$)
  - `3.00` m (para calzada de $6.00\text{ m}$)

### Paso B — Pestaña *Widening Criteria* (Sobreancho Automático DG-2018)
1. Marca la casilla **Add widening around curves**.
2. Marca **Use criteria-based design** y verifica que apunte a `PA14_DG2018_MTC_Roadway_Design_Standards.xml`.
3. En **Widening Method**, selecciona uno de los métodos **automáticos por tabla** según tu vehículo de diseño (Tabla 202.01 DG-2018):
   - **`DG-2018 MTC Tabla Sobreancho: Omnibus 2 ejes B2 / Camion 2 ejes C2 (L=8.25m)`** *(Recomendado para camiones C2 y buses B2)*
   - **`DG-2018 MTC Tabla Sobreancho: Omnibus 3 ejes B3-1 / Camion 3 ejes C3 (L=9.95m)`** *(Para camiones C3 y buses de 3 ejes)*
   - **`DG-2018 MTC Tabla Sobreancho: Omnibus 2 ejes B2 con vuelo delantero (L=10.55m)`** *(Considerando vuelo frontal completo)*
   - **`DG-2018 MTC Tabla Sobreancho: Semirremolque articulado T2S1 / T3S2 (L=12.50m)`** *(Para tráileres y semirremolques)*
4. **Configuración crítica en el cuadro inferior para evitar bordes deformes:**
   - **Apply Widening To**: **`Inside Only`** (Solo borde interior). El Art. 302.09.03 del DG-2018 establece que el sobreancho total de la calzada ($n=2$ carriles) se desarrolla en el **borde interior de la curva**. Si eliges *Both Sides*, Civil 3D ensanchará ambos lados simultáneamente duplicando el ancho.
   - **Normal Lane Width**: `7.2m` (o `6.6m` / `6.0m`, que representa el ancho total de la calzada de 2 carriles en la tabla).
   - **Number of Lanes (Left / Right)**: `1`.

> **¿Por qué elegir `Tabla Sobreancho` en lugar de `Formula`?**
> - El método **`Tabla Sobreancho`** aplica automáticamente la restricción del Art. 302.09.03 del DG-2018: **si el sobreancho calculado es menor a $0.40\text{ m}$, se asigna $0.0\text{ m}$** (no se ensancha innecesariamente en curvas de gran radio), y no requiere digitar manualmente la distancia entre ejes `{wl}`.
> - Si prefieres el cálculo continuo sin tabla, puedes elegir **`DG-2018 MTC Formula Sobreancho: ...`**, que ya lleva la longitud $L$ del vehículo integrada en la ecuación sin depender de `{wl}`.

---

## 3. Trazabilidad Normativa (Verificada con el PDF `DG-2018`)

| Contenido | Estado |
|---|---|
| Radios mínimos redondeados (4 tablas, 30–130 km/h) | **Oficial**: Tabla 302.02 (pág. 129) |
| Visibilidad de parada ($D_p$) y adelantamiento ($D_a$) | **Oficial**: Tablas 205.01 (pág. 104) y 205.03 (pág. 109) |
| Parámetro $K$ (curvas verticales convexas y cóncavas) | **Oficial**: Art. 303.04.03 y 303.04.04 (págs. 178–182, Figuras 303.06–303.08) |
| Sobreancho $S_a = n(R-\sqrt{R^2-L^2}) + \frac{V}{10\sqrt{R}}$ y $S_{a,\min} = 0.40\text{ m}$ | **Oficial**: Art. 302.09.03, Figura 302.18B (pág. 161), Tabla 302.20 (pág. 162) y Tabla 202.01 (pág. 27) |
| Longitud de transición $L_t = \frac{e}{i_{p,\max}} B$ ($i_{p,\max} = 1.8 - 0.01V$) | **Oficial**: Art. 302.08 (pág. 152), Tabla 304.01 ($B = 3.60\text{ m}$) y Tabla 304.03 (bombeo $2.0\%$) |
| Discretización intermedia de peralte $e(R)$ | `(S)` Discretización numérica de los ábacos de las Figuras 302.02–302.05 (págs. 130–131) |

Nota: en la Tabla 302.02, fila 6 % a 80 km/h (pág. 129), el manual imprime 252.9 m y la fórmula da 252.0 m.
Se respetó el valor impreso (255 m redondeado).

## 4. Banquetas — Figura 304.07, pág. 203 (modelar en el Assembly, no en el XML)
El XML de criterios no controla taludes ni banquetas; se hacen con subassemblies (`DaylightBench`
o Subassembly Composer). Parámetros (en `[banquetas]` del TOML):

| Elemento | Valor |
|---|---|
| Corte que exige banqueta | altura > 7.00 m |
| Altura entre banquetas sucesivas | 10.00 m |
| Ancho de banqueta en corte | 3.00 m, pendiente transversal 2 % |
| Pendiente longitudinal máx. de banqueta | 3 % (usar la del camino si es menor) |
| Banqueta en ladera (P ≥ 20 %) | ancho mín. 3.00 m, pendiente 4 %, talud 3:1 (V:H) |
| Cambio de talud en relleno | escalón V = 1.00 m, H = 1.50 m |
| Banquetas | sembradas en todo su ancho, con senderos de acceso para mantenimiento liviano |
