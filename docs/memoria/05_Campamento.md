# Campamento y Edificaciones Especializadas

> Túnel Casmas Huaraz PA14 · Generado con `uv run pa14` desde `datos/parametros.toml`. **No editar a mano.**

## 1. Criterios Generales y Marco Normativo de Edificaciones

El campamento base y satélite del proyecto **Túnel Casmas Huaraz PA14** (5.538 km a 3,850 m s.n.m.) han sido dimensionados para alojar a **346 trabajadores** en operación continua 24/7 (régimen 14×7), cubriendo un área edificada total de **11,482.5 m²** y un área de terreno proyectada de **17,223.8 m²** a través de **38 edificaciones y áreas operativas especializadas (EDIF-01 a EDIF-38)**.

### 1.1 Normativa Técnica Aplicable
- **Reglamento Nacional de Edificaciones (RNE - Perú):**
  - **Norma G.050 (Seguridad durante la Construcción):** Instalaciones provisionales, servicios higiénicos, vestuarios y comedores.
  - **Norma A.010 (Condiciones Generales de Diseño y Cap. X Estacionamientos):** Alturas libres mínimas ($H \ge 2.30\text{ m}$), ventilación e iluminación; dimensionamiento y radios de giro para camionetas ($2.50 \times 5.00\text{ m}$) y buses ($3.50 \times 12.00\text{ m}$).
  - **Norma A.060 (Industria y Almacenes):** Aplicable a la Nave Taller (EDIF-10 y EDIF-29), Bodegas de Repuestos (EDIF-11 y EDIF-33) y Patio de Maquinaria Pesada (EDIF-26), con altura libre de $7.0\text{ m}$, tecle de 15 Tn y radios de giro $\ge 15.0\text{ m}$.
  - **Norma A.070 (Hospedaje y Comedores):** Ratios de $1.20\text{ m}^2/\text{cama}$ (+ 20% circulación) en dormitorios y $1.50\text{ m}^2/\text{comensal pico}$ en comedores.
  - **Norma A.080 (Oficinas):** Ratio de $8.0\text{ m}^2/\text{puesto de trabajo}$ para gerencia y supervisión técnica.
  - **Norma IS.010 (Instalaciones Sanitarias):** Dotación de $129\text{ L/pax/día}$ en sierra y 1 aparato sanitario cada 10 trabajadores.
  - **Norma EM.010 (Instalaciones Eléctricas):** Iluminación (300 lux oficinas, 500 lux talleres) y tableros IP65.
- **D.S. N° 024-2016-EM / D.S. N° 023-2017-EM (Seguridad Minera a 3,850 m s.n.m.):**
  - Aislamiento térmico obligatorio (paneles termoacústicos con alma de poliuretano) y calefacción limpia.
  - En el Campamento Satélite (CAMP2), los dormitorios (EDIF-03) integran directamente los servicios higiénicos, duchas calientes y casilleros (lockers) por módulo para evitar exposición a la intemperie a 3,850 msnm.
  - Tópico médico de atención 24/7 (Art. 157) con camillas de reposo, balones de oxígeno medicinal y ambulancia Tipo II.
  - Lampistería central en Portal A (EDIF-22) y lampistería satélite en garita Portal B (EDIF-36) con autorrescatadores (Art. 97).
- **Ley N° 30299 / SUCAMEC:** Polvorines de superficie independientes (EDIF-23 en Portal A y EDIF-28 en Portal B) con parapetos de tierra, radio de seguridad de 300 m y casetas de vigilancia armada exclusiva 24/7 (EDIF-37 y EDIF-38).
- **D.Leg. 1278 (Gestión Integral de Residuos Sólidos):** Centros CAT de acopio (EDIF-18 y EDIF-33) y compostaje (EDIF-19).
- **MTC EG-2013 (Sección 104 - Campamentos y Patios de Maquinaria):** Emplazamiento seguro, estabilización de plataformas y drenaje pluvial perimetral.

## 2. Clasificación por Grupos Funcionales (EDIF-01 a EDIF-38)

| Grupo Funcional | Recintos (EDIF) | Cant. | Área Techada (m²) | % del Total | Alcance Normativo y Operativo |
|---|---|---|---|---|---|
| **Residencia y Habitabilidad** | `EDIF-01, EDIF-02, EDIF-03, EDIF-12, EDIF-34` | 5 | **2,724.0 m²** | 23.7 % | Residencia y Habitabilidad normativo RNE / DS 024 / MTC / SUCAMEC. |
| **Comedor y Alimentación** | `EDIF-04, EDIF-05, EDIF-17` | 3 | **279.5 m²** | 2.4 % | Comedor y Alimentación normativo RNE / DS 024 / MTC / SUCAMEC. |
| **Administración y Documentos** | `EDIF-06, EDIF-07` | 2 | **900.0 m²** | 7.8 % | Administración y Documentos normativo RNE / DS 024 / MTC / SUCAMEC. |
| **Salud y Bienestar** | `EDIF-08, EDIF-09, EDIF-13, EDIF-35` | 4 | **696.0 m²** | 6.1 % | Salud y Bienestar normativo RNE / DS 024 / MTC / SUCAMEC. |
| **Maquinaria y Mantenimiento** | `EDIF-10, EDIF-26, EDIF-29` | 3 | **2,075.0 m²** | 18.1 % | Maquinaria y Mantenimiento normativo RNE / DS 024 / MTC / SUCAMEC. |
| **Almacenes y Logística** | `EDIF-11, EDIF-33` | 2 | **270.0 m²** | 2.4 % | Almacenes y Logística normativo RNE / DS 024 / MTC / SUCAMEC. |
| **Agua y Saneamiento** | `EDIF-14, EDIF-15, EDIF-16, EDIF-32` | 4 | **940.0 m²** | 8.2 % | Agua y Saneamiento normativo RNE / DS 024 / MTC / SUCAMEC. |
| **Residuos y Ambiente** | `EDIF-18, EDIF-19` | 2 | **646.0 m²** | 5.6 % | Residuos y Ambiente normativo RNE / DS 024 / MTC / SUCAMEC. |
| **Energía y Combustible** | `EDIF-20, EDIF-21, EDIF-30, EDIF-31` | 4 | **920.0 m²** | 8.0 % | Energía y Combustible normativo RNE / DS 024 / MTC / SUCAMEC. |
| **Operación y Portales** | `EDIF-22` | 1 | **468.0 m²** | 4.1 % | Operación y Portales normativo RNE / DS 024 / MTC / SUCAMEC. |
| **Seguridad y Explosivos** | `EDIF-23, EDIF-28` | 2 | **250.0 m²** | 2.2 % | Seguridad y Explosivos normativo RNE / DS 024 / MTC / SUCAMEC. |
| **Vigilancia y Transporte** | `EDIF-24, EDIF-25, EDIF-27, EDIF-36, EDIF-37, EDIF-38` | 6 | **1,314.0 m²** | 11.4 % | Vigilancia y Transporte normativo RNE / DS 024 / MTC / SUCAMEC. |
| **TOTAL CONSTRUIDO** | **EDIF-01 a EDIF-38** | **38** | **11,482.5 m²** | **100.0 %** | **Infraestructura total en ambos campamentos.** |

## 3. Distribución Geográfica por Campamentos

### 3.1 Campamento 1 — Principal (Portal A / Entrada — 248 personas)
- **Área construida:** **8,931.0 m²**
- **Infraestructura centralizada:**
  - **EDIF-01:** Pabellón de Dormitorios Staff e Ingeniería (73 pax).
  - **EDIF-02:** Pabellón de Dormitorios Obreros A y B (175 pax).
  - **EDIF-04:** Comedor Principal y Cocina Central (248 comensales en 2 turnos).
  - **EDIF-06:** Oficinas Administrativas, Gerencia y Auditorio SSOMA.
  - **EDIF-08:** Tópico Médico Central 24/7 y Ambulancia Tipo II.
  - **EDIF-10:** Nave Taller Mecánico Principal (3 bahías para jumbos, scoops y volquetes).
  - **EDIF-11:** Almacén Central de Repuestos e Insumos Críticos.
  - **EDIF-12:** Lavandería Industrial y Ropería.
  - **EDIF-13:** Módulo Recreativo, SUM y Gimnasio.
  - **EDIF-14 / 15 / 16 / 17:** Planta de Saneamiento Completa (Pozo profundo 5 L/s, PTAP con reservorio 120 m³, PTAR MBBR y Trampas de grasa).
  - **EDIF-18 / 19:** Manejo Ambiental (Centro CAT de residuos y Trincheras de compostaje).
  - **EDIF-20 / 21:** Energía y Combustible (Casa de fuerza 2500 kVA y Estación de diésel 20,000 gal).
  - **EDIF-22:** Change-House y Lampistería Portal A.
  - **EDIF-23:** Polvorín de Superficie SUCAMEC Portal A.
  - **EDIF-24:** Garita de Control y Balanza de Pesaje 80 Tn.
  - **EDIF-25:** Playa de Estacionamiento de Vehículos Livianos y Buses (800 m²).
  - **EDIF-26:** Patio de Parqueo y Maniobras de Maquinaria Pesada (1,500 m²).
  - **EDIF-37:** Caseta de Seguridad y Custodia de Polvorín Principal (12 m²).

### 3.2 Campamento 2 — Satélite Autónomo (Portal B / Salida — 98 personas)
- **Área construida:** **2,551.5 m²**
- **Infraestructura satélite de total autonomía operativa:**
  - **EDIF-03:** Pabellón de Dormitorios Satélite con duchas/servicios integrados (98 pax).
  - **EDIF-05:** Comedor y Cocina Satélite (98 comensales en 2 turnos).
  - **EDIF-07:** Oficinas Técnicas de Frente y Supervisión Portal B.
  - **EDIF-09:** Puesto de Primeros Auxilios Satélite y Ambulancia de Respaldo.
  - **EDIF-27:** Playa de Estacionamiento y Parqueo Auxiliar Portal B (400 m²).
  - **EDIF-28:** Polvorín Satélite Certificado SUCAMEC (100 m² con parapetos).
  - **EDIF-29:** Nave Taller Mecánico Auxiliar y Lubricación (200 m²).
  - **EDIF-30:** Estación de Combustible Satélite (200 m², tanque 10,000 gal).
  - **EDIF-31:** Casa de Fuerza Satélite y Generadores (120 m², grupo 1000 kVA).
  - **EDIF-32:** Planta Compacta de Saneamiento Modular PTAP/PTAR (180 m²).
  - **EDIF-33:** Bodega de Insumos Críticos y Acopio de Residuos CAT Satélite (120 m²).
  - **EDIF-34:** Lavandería Satélite y Ropería (40 m²).
  - **EDIF-35:** Módulo Recreativo y Sala de Usos Múltiples (120 m²).
  - **EDIF-36:** Garita de Control de Acceso y Lampistería Satélite (30 m²).
  - **EDIF-38:** Caseta de Seguridad y Custodia de Polvorín Satélite (12 m²).

## 4. Dimensionamiento Sanitario y Ambiental (Pozo, PTAP, PTAR y Trampas de Grasa)

- **EDIF-14 (Caseta de Pozo Profundo - CAMP1):** Captación subterránea con caudal de diseño de $5.0\text{ L/s}$, electrobomba sumergible y tubería de impulsión de $\varnothing 3''$.
- **EDIF-15 (Planta PTAP y Reservorio 120 m³ - CAMP1):** Tratamiento mediante filtración multimedia y cloración por inyección dosificada; reservorio de concreto armado de $120\text{ m}^3$ que garantiza regulación horaria y reserva contra incendios.
- **EDIF-16 (Planta PTAR MBBR - CAMP1):** Sistema de lodos activados con bioportadores de lecho móvil (MBBR), sedimentador secundario y cámara de desinfección UV/cloro, con efluente cumpliendo los Estándares de Calidad Ambiental (ECA) para agua (D.S. 004-2017-MINAM).
- **EDIF-17 (Trampas de Grasa - CAMP1):** Unidades de retención gravimétrica de grasas y aceites provenientes de la cocina industrial antes del ingreso al colector biológico.
- **EDIF-32 (Saneamiento Compacto - CAMP2):** Módulos compactos contenerizados de potabilización (PTAP 2 L/s) y tratamiento biológico compacto (PTAR MBBR 1.5 L/s) para los 98 ocupantes del Portal B.

## 5. Dimensionamiento de Estacionamientos y Patios de Maniobra de Maquinaria

- **EDIF-25 (Playa de Estacionamiento Livianos y Buses - CAMP1, 800 m²):** Diseñado conforme a la norma RNE A.010 (Cap. X). Incluye 20 cajones de $2.50 \times 5.00\text{ m}$ para camionetas 4x4 de staff, supervisión y visitas, más 4 bahías de $3.50 \times 12.00\text{ m}$ para buses interurbanos de cambio de guardia (14x7) con calles de circulación de $6.00\text{ m}$ y radio de giro adecuado.
- **EDIF-26 (Patio de Parqueo de Maquinaria Pesada - CAMP1, 1,500 m²):** Ubicado estratégicamente contiguo a la Nave Taller (EDIF-10) y la Estación de Combustible (EDIF-21). Plataforma estabilizada con subbase granular de $0.30\text{ m}$ y losa/afirmado para soportar cargas por eje de volquetes de 20 m³, Jumbos electrohidráulicos y Scooptrams LHD, con radio libre de giro $\ge 15.00\text{ m}$ y canaletas perimetrales conectadas a trampa de hidrocarburos.
- **EDIF-27 (Playa de Estacionamiento y Parqueo Auxiliar - CAMP2, 400 m²):** Destinado al Frente 2 (Portal B). Cuenta con 8 cajones para camionetas técnicas, 2 bahías para minibuses de traslado de guardia y zona de parqueo transitorio para 2 volquetes y cargador frontal.

## 6. Autonomía Logística y Polvorín Satélite del Frente 2 (Portal B)

Debido a la longitud del túnel ($L = 5.538\text{ km}$) a través de un macizo cordillerano escarpado, la comunicación vial superficial entre el Portal A y el Portal B tomaría más de 2.5 horas por trocha carrozable de alta montaña. Por tanto, conforme a las mejores prácticas de ingeniería de túneles y normativas SUCAMEC / D.S. 024-2016-EM:

- **Polvorín Satélite (EDIF-28, 100 m²) y Caseta de Custodia (EDIF-38, 12 m²):** Almacenamiento directo de emulsión encartuchada, dinamita y accesorios de voladura con parapetos perimetrales de tierra, distanciamiento de seguridad normativo de 300 m y vigilancia armada permanente in situ.
- **Mantenimiento y Combustible Local (EDIF-29 y EDIF-30):** Permite el mantenimiento preventivo diario (cambio de brocas, mangueras hidráulicas, lubricación) y repostaje de diésel sin desplazar la maquinaria pesada al Portal A, evitando tiempos muertos y sobrecostos de traslado.
- **Energía Continua Satélite (EDIF-31):** Generador diésel de 1000 kVA insonorizado que garantiza bombeo de achique, iluminación del frente y habitabilidad continua en el Campamento 2.

## 7. Servicios de Habitabilidad y Bienestar en Campamento 2

Con el fin de asegurar el confort térmico y la salud de los trabajadores en condiciones de alta montaña (3,850 msnm), el diseño de habitabilidad del Campamento 2 contempla:

- **Duchas y Cambio Térmico Integrado en Dormitorios (EDIF-03):** Los trabajadores se cambian y asean dentro de los mismos módulos climatizados de dormitorios, evitando el choque térmico de desplazarse a la intemperie hacia una nave change-house desvinculada.
- **Lavandería Satélite (EDIF-34, 40 m²):** Equipamiento industrial de lavado y secado continuo para la ropa térmica y de trabajo de los 98 ocupantes.
- **Módulo Recreativo y SUM (EDIF-35, 120 m²):** Espacio de relajación y esparcimiento con televisor satelital, internet y área de lectura para prevenir el estrés por aislamiento en régimen 14×7.
- **Garita y Lampistería Satélite (EDIF-36, 30 m²):** Módulo de control de accesos al Portal B que aloja el rack de carga para 40 lámparas mineras y entrega de autorrescatadores.

## 8. Sistema de Seguridad Integral y Custodia de Polvorines

Conforme a la Ley N° 30299 (SUCAMEC) y el D.S. 024-2016-EM, la seguridad patrimonial y de explosivos se estructura en dos niveles:

- **Control de Accesos a Campamentos (EDIF-24 y EDIF-36):** Garitas en los ingresos vehiculares con control biométrico, registro de visitas y pesaje de camiones en balanza de 80 t en el Portal A.
- **Custodia Exclusiva 24/7 de Polvorines (EDIF-37 y EDIF-38):** Casetas de vigilancia blindadas ubicadas a pie de parapeto de los polvorines (aislados a 300 m del campamento), dotadas de radio troncalizado, reflector perimetral y guardia armado continuo.
