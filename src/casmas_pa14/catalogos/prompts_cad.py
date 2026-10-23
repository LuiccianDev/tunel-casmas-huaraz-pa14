"""Generador automático del catálogo de prompts arquitectónicos CAD para IA.

Produce 'salidas/documentos/prompts_edificaciones_cad.md' de forma dinámica
a partir de los parámetros de diseño calculados en el módulo de campamento (m05).
"""

from pathlib import Path

# Catálogo descriptivo y plantillas de prompts de ingeniería en inglés
CATALOGO_SPECS: dict[str, dict] = {
    "EDIF-01": {
        "titulo": "Pabellón de Dormitorios Staff e Ingeniería",
        "detalles": [
            (
                "Población",
                "73 ingenieros y supervisores (habitaciones unipersonales con baño privado).",
            ),
            (
                "Configuración",
                "Estructura modular de 2 niveles apareada en doble crujía con pasadizo central térmico de 2.0 m y escaleras exteriores de evacuación.",
            ),
            (
                "Normativa",
                "RNE A.070 (Hospedaje) / D.S. 024-2016-EM (Aislamiento térmico a 3,850 msnm).",
            ),
        ],
        "prompt": (
            "[STRICT 2D CAD ARCHITECTURAL BLUEPRINT] Orthogonal 2D floor plan and cross-section layout, "
            "monochromatic black line drawing on pristine white technical drafting grid background. "
            "No 3D, no isometric, no perspective, no photorealism. High-detail architectural CAD blueprint sheet, "
            "technical drafting of a 2-story modular staff dormitory building for mining engineering personnel at "
            "3,850 meters altitude. Dimensions: {largo:.1f} meters length by {ancho:.1f} meters width. Top view: detailed floor plan "
            "showing a 2.0m wide insulated central hallway with single en-suite bedrooms on both sides (each with "
            "private bathroom, shower, work desk, closet, bed, and electric panel heater). Bottom view: cross-section A-A' "
            "showing two modular stories made of 100mm polyurethane insulated sandwich panels, double-glazed windows, "
            "gable roof with anti-freeze rainwater gutters, and exterior steel emergency stairs. Precise CAD linework, "
            "structural grid lines, dimension callouts in meters, black lines on white technical graph paper background, "
            "title block in Spanish. Technical CAD details, wall line weights, door swing arcs, dimension strings, "
            "structural grid markers, title block in Spanish, high contrast schematic engineering drawing, "
            "--ar 16:9 --style raw --v 6.0"
        ),
    },
    "EDIF-02": {
        "titulo": "Pabellón de Dormitorios Obreros A y B",
        "detalles": [
            (
                "Población",
                "175 operadores y obreros (módulos cuádruples con lockers metálicos).",
            ),
            (
                "Configuración",
                "2 plantas modulares con dos alas paralelas y pasadizo central ancho (2.4 m). Incluye baterías de baños integrados en extremos para no exponer al personal al frío exterior. Recorrido de evacuación máximo $\\le 45\\text{ m}$.",
            ),
            (
                "Normativa",
                "RNE A.070 ($1.20\\text{ m}^2/\\text{cama}$ + 20% circ.) / RNE A.130 (Evacuación contra incendios).",
            ),
        ],
        "prompt": (
            "[STRICT 2D CAD ARCHITECTURAL BLUEPRINT] Orthogonal 2D floor plan and cross-section layout, "
            "monochromatic black line drawing on pristine white technical drafting grid background. "
            "No 3D, no isometric, no perspective, no photorealism. Professional architectural CAD drawing of a 2-story "
            "prefabricated workers dormitory pavilion for 175 mine tunnel workers. Dimensions: {largo:.1f} meters length "
            "by {ancho:.1f} meters width. Top view shows two parallel wings with a 2.4m central heated corridor, 4-person "
            "shared bedrooms with two bunk beds and individual lockers, and collective sanitation core at the wings "
            "with hot showers, toilets, and washbasins. Bottom view shows architectural cross-section displaying 2 modular "
            "levels, interior thermal insulation, acoustic ceiling, ventilation louvers, and twin lateral steel evacuation "
            "stairs meeting fire safety egress regulations. Clean CAD line art, dimension strings, door swing arcs, "
            "technical annotations, crisp black vector lines on white drafting grid paper. Technical CAD details, "
            "wall line weights, door swing arcs, dimension strings, structural grid markers, title block in Spanish, "
            "high contrast schematic engineering drawing, --ar 16:9 --style raw --v 6.0"
        ),
    },
    "EDIF-03": {
        "titulo": "Pabellón de Dormitorios Satélite (Frente 2)",
        "detalles": [
            (
                "Población",
                "98 trabajadores asignados al Frente de Excavación 2 (Portal B).",
            ),
            (
                "Característica Clave",
                "**Duchas y Baños 100% integrados en cada módulo** para evitar el choque térmico y la hipotermia a 3,850 msnm (sin necesidad de salir a una change-house desvinculada). Módulos de 4 personas con casilleros térmicos.",
            ),
            (
                "Normativa",
                "RNE A.070 / D.S. 024-2016-EM (Salud e higiene minera en altitud extrema).",
            ),
        ],
        "prompt": (
            "[STRICT 2D CAD ARCHITECTURAL BLUEPRINT] Orthogonal 2D floor plan and cross-section layout, "
            "monochromatic black line drawing on pristine white technical drafting grid background. "
            "No 3D, no isometric, no perspective, no photorealism. High-detail architectural CAD blueprint of an "
            "autonomous 2-story modular dormitory building for 98 tunnel workers at 3,850m elevation. Overall footprint: "
            "{largo:.1f}m length by {ancho:.1f}m width. Plan view: central insulated hallway with 4-person shared thermal rooms, "
            "each room featuring an integrated en-suite heated bathroom with hot shower, toilet, dual sinks, and heated "
            "gear lockers to avoid sub-zero exterior exposure. Section cut A-A' showing 2 modular stories constructed from "
            "100mm polyurethane insulated sandwich panels, sealed double-pane PVC windows, floor heating plenum, and exterior "
            "galvanized steel access stairs. Black ink technical drafting on millimeter grid paper, metric dimensions, Spanish "
            "room annotations. Technical CAD details, wall line weights, door swing arcs, dimension strings, structural grid markers, "
            "title block in Spanish, high contrast schematic engineering drawing, --ar 16:9 --style raw --v 6.0"
        ),
    },
    "EDIF-04": {
        "titulo": "Comedor Principal y Cocina Central",
        "detalles": [
            (
                "Capacidad",
                "124 comensales simultáneos por turno (2 turnos para 248 trabajadores).",
            ),
            (
                "Distribución",
                "Salón comedor con mesas de 6 sillas, barra de autoservicio (baño maría caliente), cocina industrial con campana extractora y cámaras de frío (carnes/vegetales).",
            ),
            (
                "Normativa",
                "RNE A.070 ($1.50\\text{ m}^2/\\text{comensal}$) / NTS N° 142-MINSA (Inocuidad alimentaria).",
            ),
        ],
        "prompt": (
            "[STRICT 2D CAD ARCHITECTURAL BLUEPRINT] Orthogonal 2D floor plan and cross-section layout, "
            "monochromatic black line drawing on pristine white technical drafting grid background. "
            "No 3D, no isometric, no perspective, no photorealism. Architectural CAD blueprint layout of a high-altitude "
            "mining camp main dining hall and industrial kitchen. Dimensions: {largo:.1f} meters length by {ancho:.1f} meters width "
            "({area:.0f} m2). Top-down floor plan layout: dining area with 6-seat tables seating 124 workers, self-service food line "
            "counter with heated trays, dish drop station, handwashing vestibule at entrance. Rear industrial kitchen zone with "
            "stainless steel cooking range, deep fryer, preparation islands, heavy-duty exhaust hood, dry pantry, walk-in cold "
            "storage refrigerator room, and grease trap discharge point. Cross-section view showing hygienic washable panel walls, "
            "insulated ceiling, and grease-vapor ventilation stack. Technical architectural drafting style, millimeter grid background, "
            "dimensions and Spanish room labels. Technical CAD details, wall line weights, door swing arcs, dimension strings, "
            "structural grid markers, title block in Spanish, high contrast schematic engineering drawing, --ar 16:9 --style raw --v 6.0"
        ),
    },
    "EDIF-05": {
        "titulo": "Comedor y Cocina Satélite",
        "detalles": [
            (
                "Capacidad",
                "49 comensales simultáneos por turno (2 turnos para 98 trabajadores).",
            ),
            (
                "Distribución",
                "Salón comedor con mesas compactas de 4 sillas, mostrador de autoservicio de comida caliente, cocina completa con quemadores industriales, mesa de preparación en acero inoxidable y despensa seca/fría.",
            ),
            (
                "Normativa",
                "RNE A.070 ($1.50\\text{ m}^2/\\text{comensal}$) / NTS N° 142-MINSA.",
            ),
        ],
        "prompt": (
            "[STRICT 2D CAD ARCHITECTURAL BLUEPRINT] Orthogonal 2D floor plan and cross-section layout, "
            "monochromatic black line drawing on pristine white technical drafting grid background. "
            "No 3D, no isometric, no perspective, no photorealism. Architectural CAD blueprint layout of a satellite camp "
            "dining room and kitchen facility for 98 personnel. Dimensions: {largo:.1f}m x {ancho:.1f}m ({area:.1f} m2). Floor plan showing: "
            "dining area with tables seating 50 workers simultaneously, heated food buffet counter, dish cleaning area, and "
            "compact commercial kitchen with stainless steel prep tables, gas burner stove, grease extraction hood, and walk-in "
            "reach-in cold refrigerator. Cross section showing hygienic washable walls, insulated insulated ceiling paneling, and "
            "wall-mounted gas convective heaters. Technical CAD vector lines, metric dimension callouts, Spanish labels on white grid. "
            "Technical CAD details, wall line weights, door swing arcs, dimension strings, structural grid markers, title block in "
            "Spanish, high contrast schematic engineering drawing, --ar 16:9 --style raw --v 6.0"
        ),
    },
    "EDIF-06": {
        "titulo": "Edificio de Oficinas Administrativas y Gerencia",
        "detalles": [
            (
                "Distribución",
                "Gerencia de proyecto, sala de reuniones / directorio, oficinas técnicas de topografía y geotecnia, sala de inducción SSOMA para 40 personas, archivo documental y servicios higiénicos dobles.",
            ),
            (
                "Normativa",
                "RNE A.080 ($8.0\\text{ m}^2/\\text{puesto de trabajo}$) / RM 375-2008-TR (Ergonomía).",
            ),
        ],
        "prompt": (
            "[STRICT 2D CAD ARCHITECTURAL BLUEPRINT] Orthogonal 2D floor plan and cross-section layout, "
            "monochromatic black line drawing on pristine white technical drafting grid background. "
            "No 3D, no isometric, no perspective, no photorealism. Detailed architectural CAD plan and section of a corporate "
            "administration and engineering headquarters building for a tunnel construction site. Overall footprint: {largo:.1f}m x {ancho:.1f}m. "
            "Floor plan detailing: executive project manager offices, open-plan engineering workstations for surveyors and geologists, "
            "board conference room with video screens, 40-seat safety induction training auditorium (SSOMA), technical document archive "
            "room, server IT room, and male/female restroom batteries. Cross section showing false ceiling with LED troffers, cable "
            "trays, carpet tile finish, thermal insulated wall panels, and entrance access ramp. Precise black vector CAD drafting, "
            "dimension marks, scale 1:100 representation on white engineering paper. Technical CAD details, wall line weights, door swing "
            "arcs, dimension strings, structural grid markers, title block in Spanish, high contrast schematic engineering drawing, "
            "--ar 16:9 --style raw --v 6.0"
        ),
    },
    "EDIF-07": {
        "titulo": "Oficinas Técnicas de Frente y Supervisión",
        "detalles": [
            (
                "Distribución",
                "Sala de ingeniería técnica de túnel (geólogos, topógrafos, jefes de guardia), oficina del residente de obra Portal B, oficina de la supervisión externa, sala de reuniones para cambio de turno y SSOMA, archivo de planos y baños técnicos.",
            ),
            ("Normativa", "RNE A.080 ($8.0\\text{ m}^2/\\text{puesto de trabajo}$)."),
        ],
        "prompt": (
            "[STRICT 2D CAD ARCHITECTURAL BLUEPRINT] Orthogonal 2D floor plan and cross-section layout, "
            "monochromatic black line drawing on pristine white technical drafting grid background. "
            "No 3D, no isometric, no perspective, no photorealism. Architectural CAD technical blueprint of an on-site field "
            "engineering and technical supervision office building (Portal B). Dimensions: {largo:.1f}m x {ancho:.1f}m. Plan view detailing: "
            "open-concept workspace for tunnel survey engineers and geologists with plotting tables, resident engineer private office, "
            "client supervision office, 20-seat shift-change and safety briefing room, blueprint filing archive, and male/female restrooms. "
            "Detail cross section showing thermal insulation sandwich panel construction, recessed LED troffers, data raceways, and "
            "entrance vestibule. Clean CAD linework, metric dimension strings, Spanish text on drafting paper. Technical CAD details, "
            "wall line weights, door swing arcs, dimension strings, structural grid markers, title block in Spanish, high contrast "
            "schematic engineering drawing, --ar 16:9 --style raw --v 6.0"
        ),
    },
    "EDIF-08": {
        "titulo": "Tópico Médico Central y Sala de Reposo",
        "detalles": [
            (
                "Distribución",
                "Consultorio médico ocupacional, sala de trauma shock con camillas y suministro de oxígeno medicinal (para mal de altura / soroche a 3,850 msnm), sala de reposo con 4 camas clínicas, botiquín de emergencias y estacionamiento techado para Ambulancia Tipo II.",
            ),
            ("Normativa", "D.S. 024-2016-EM Art. 157 (Atención médica 24/7)."),
        ],
        "prompt": (
            "[STRICT 2D CAD ARCHITECTURAL BLUEPRINT] Orthogonal 2D floor plan and cross-section layout, "
            "monochromatic black line drawing on pristine white technical drafting grid background. "
            "No 3D, no isometric, no perspective, no photorealism. Architectural technical blueprint of an occupational "
            "medical health clinic and emergency triage post for high altitude mining operations (3,850m). Dimensions: {largo:.1f}m x {ancho:.1f}m. "
            "Floor plan showing: direct emergency entrance with ambulance parking bay, triage counter, trauma-shock treatment room with "
            "defibrillator and medical oxygen manifolds, doctor's consultation office, 4-bed patient recovery room with curtains, sterile "
            "medicine pharmacy, clinical waste storage, and handicap-accessible bathroom. Cross-section cut showing positive-pressure medical "
            "ventilation, antimicrobial PVC floor coving, and insulated insulated panels. Detailed CAD line art, Spanish labels, dimension "
            "lines, black ink on white grid. Technical CAD details, wall line weights, door swing arcs, dimension strings, structural grid "
            "markers, title block in Spanish, high contrast schematic engineering drawing, --ar 16:9 --style raw --v 6.0"
        ),
    },
    "EDIF-09": {
        "titulo": "Puesto de Primeros Auxilios Satélite",
        "detalles": [
            (
                "Distribución",
                "Tópico de emergencia para atención rápida en el Portal B: camilla de trauma shock, tubos de oxígeno medicinal con mascarillas, camilla rígida de rescate en túnel, botiquín de estabilización de hipotermia/trauma y acceso directo para ambulancia de respaldo.",
            ),
            ("Normativa", "D.S. 024-2016-EM Art. 157."),
        ],
        "prompt": (
            "[STRICT 2D CAD ARCHITECTURAL BLUEPRINT] Orthogonal 2D floor plan and cross-section layout, "
            "monochromatic black line drawing on pristine white technical drafting grid background. "
            "No 3D, no isometric, no perspective, no photorealism. Architectural CAD blueprint of a satellite emergency first aid "
            "post (Puesto de Primeros Auxilios) for an isolated tunnel entrance at 3,850m. Footprint: {largo:.1f}m x {ancho:.1f}m. Top view showing: "
            "emergency ambulance arrival porch, triage examination room with shock trauma stretcher, medical oxygen cylinder station, tunnel "
            "rescue spinal immobilization backboard rack, physician desk, 2 recovery observation beds, medicine locker, and sanitary toilet. "
            "Cross section showing thermal wall panels, clinical washable vinyl flooring, and emergency power battery backup. Technical vector "
            "CAD lines, metric scale, Spanish room titles. Technical CAD details, wall line weights, door swing arcs, dimension strings, "
            "structural grid markers, title block in Spanish, high contrast schematic engineering drawing, --ar 16:9 --style raw --v 6.0"
        ),
    },
    "EDIF-10": {
        "titulo": "Nave de Taller Mecánico Principal",
        "detalles": [
            (
                "Distribución",
                "3 bahías de mantenimiento para maquinaria pesada (Jumbo electrohidráulico, Scoop LHD 6 yd³, volquete 20 m³), fosa de lubricación de $15\\text{ m}$, puente grúa monorriel de 15 Tn, zona de soldadura, banco de tornos y cuarto de aceites. Altura libre interior $H = 7.0\\text{ m}$.",
            ),
            ("Normativa", "RNE A.060 (Industria) / D.S. 024-2016-EM."),
        ],
        "prompt": (
            "[STRICT 2D CAD ARCHITECTURAL BLUEPRINT] Orthogonal 2D floor plan and cross-section layout, "
            "monochromatic black line drawing on pristine white technical drafting grid background. "
            "No 3D, no isometric, no perspective, no photorealism. Structural and architectural CAD blueprint of an industrial "
            "heavy machinery maintenance workshop for tunnel excavation equipment. Dimensions: {largo:.1f}m length by {ancho:.1f}m width, "
            "clearance height 7.0m. Plan view showing: 3 heavy repair bays, 15m long concrete inspection lubrication pit with safety stairs, "
            "15-ton overhead travelling crane beam runway, welding workstation with fume arm, machining lathes corner, tool crib room, and "
            "oil recovery sumps. Cross section displaying heavy steel portal frame structure, corrugated insulated sandwich roofing with "
            "skylights, concrete slab rated for 30-ton axle loads, and 5.0m high industrial rolling doors. Highly accurate CAD line drawing, "
            "dimension strings, annotations in Spanish. Technical CAD details, wall line weights, door swing arcs, dimension strings, "
            "structural grid markers, title block in Spanish, high contrast schematic engineering drawing, --ar 16:9 --style raw --v 6.0"
        ),
    },
    "EDIF-11": {
        "titulo": "Almacén Central de Repuestos e Insumos",
        "detalles": [
            (
                "Distribución",
                "Racks metálicos para brocas, barras de perforación, pernos de anclaje Swellex, malla electrosoldada, mangueras hidráulicas, zona de despacho con mostrador de control y área de almacenamiento seguro para químicos y lubricantes (con cubeto antiderrame).",
            ),
            (
                "Normativa",
                "RNE A.060 / NFPA 30 (Almacenamiento de líquidos inflamables).",
            ),
        ],
        "prompt": (
            "[STRICT 2D CAD ARCHITECTURAL BLUEPRINT] Orthogonal 2D floor plan and cross-section layout, "
            "monochromatic black line drawing on pristine white technical drafting grid background. "
            "No 3D, no isometric, no perspective, no photorealism. Architectural CAD drawing blueprint of a central logistics "
            "warehouse for mining tunnel spare parts and consumables. Dimensions: {largo:.1f}m x {ancho:.1f}m. Floor plan detailing: heavy steel "
            "pallet racking aisles for drill bits, rock bolts, wire mesh, and hydraulic hoses; receiving and dispatch logistics counter with "
            "barcode desk; flammable lubricants containment room with concrete spill berm and fire doors. Cross-section showing 5.5m clear "
            "height, reinforced slab, high-bay LED lighting, and exterior loading dock. Technical black ink CAD vector lines on graph grid "
            "paper, Spanish room labels, metric dimensions. Technical CAD details, wall line weights, door swing arcs, dimension strings, "
            "structural grid markers, title block in Spanish, high contrast schematic engineering drawing, --ar 16:9 --style raw --v 6.0"
        ),
    },
    "EDIF-12": {
        "titulo": "Lavandería Industrial y Ropería",
        "detalles": [
            (
                "Distribución",
                "Zona de recepción de ropa de trabajo sucia (mamelucos térmicos con cintas reflectivas), 4 lavadoras industriales de 30 kg, 4 secadoras a gas GLP, mesas de doblado, estanterías de ropería para entrega de ropa limpia y canaleta de desagüe con trampa de pelusas.",
            ),
            ("Normativa", "RNE G.050 (Higiene y lavado de ropa de trabajo en obra)."),
        ],
        "prompt": (
            "[STRICT 2D CAD ARCHITECTURAL BLUEPRINT] Orthogonal 2D floor plan and cross-section layout, "
            "monochromatic black line drawing on pristine white technical drafting grid background. "
            "No 3D, no isometric, no perspective, no photorealism. Architectural CAD blueprint of an industrial laundry and linen "
            "distribution center for a remote 250-worker camp. Footprint: {largo:.1f}m x {ancho:.1f}m. Floor plan shows: dirty work-overalls intake "
            "window, sorting area, battery of 4 heavy-duty commercial washing machines (30kg), 4 commercial gas clothes dryers with exhaust "
            "ducting, folding tables, numbered clean linen delivery shelving racks, and stainless steel floor drain trenches with lint interceptors. "
            "Cross-section showing sloped non-slip ceramic tile flooring, moisture-resistant ceiling, and ventilation louvers. Precise architectural "
            "drafting, metric dimension lines, crisp CAD lines. Technical CAD details, wall line weights, door swing arcs, dimension strings, "
            "structural grid markers, title block in Spanish, high contrast schematic engineering drawing, --ar 16:9 --style raw --v 6.0"
        ),
    },
    "EDIF-13": {
        "titulo": "Módulo Recreativo, SUM y Gimnasio",
        "detalles": [
            (
                "Distribución",
                "Salón multiusos para eventos y charlas, sala de juegos (mesas de billar, tenis de mesa, futbolines), sala audiovisual con butacas y proyector satelital, gimnasio equipado con máquinas de cardio y pesas, vestuarios y servicios higiénicos.",
            ),
            (
                "Normativa",
                "D.S. 024-2016-EM (Salud ocupacional y bienestar social para prevención de fatiga en régimen 14×7).",
            ),
        ],
        "prompt": (
            "[STRICT 2D CAD ARCHITECTURAL BLUEPRINT] Orthogonal 2D floor plan and cross-section layout, "
            "monochromatic black line drawing on pristine white technical drafting grid background. "
            "No 3D, no isometric, no perspective, no photorealism. Architectural CAD technical blueprint of a recreation center, "
            "gymnasium, and multi-purpose recreational hall for mining staff at 3,850m. Dimensions: {largo:.1f}m x {ancho:.1f}m. Layout includes: "
            "multi-purpose lounge hall for assemblies and leisure, game room with 2 pool tables and ping-pong tables, sound-isolated cinema TV "
            "room with rows of armchairs, full fitness gym room with treadmills, stationary bikes, and free weights, plus restrooms and locker "
            "changing rooms. Cross section showing acoustic suspended ceiling, rubber gym flooring, and insulated facade walls. Professional CAD "
            "lineart, dimensions, Spanish annotations, white grid background. Technical CAD details, wall line weights, door swing arcs, dimension "
            "strings, structural grid markers, title block in Spanish, high contrast schematic engineering drawing, --ar 16:9 --style raw --v 6.0"
        ),
    },
    "EDIF-14": {
        "titulo": "Caseta de Pozo Profundo y Bombeo",
        "detalles": [
            (
                "Distribución",
                "Pozo tubular perforado con electrobomba sumergible de $5.0\\text{ L/s}$, manifold de válvulas de retención y compuerta, macromedidor electromagnético, tablero de control con variador de frecuencia (VFD) y cerco de protección sanitaria.",
            ),
            ("Normativa", "RNE OS.010 (Captación de agua subterránea) / RNE IS.010."),
        ],
        "prompt": (
            "[STRICT 2D CAD ARCHITECTURAL BLUEPRINT] Orthogonal 2D floor plan and cross-section layout, "
            "monochromatic black line drawing on pristine white technical drafting grid background. "
            "No 3D, no isometric, no perspective, no photorealism. Engineering CAD blueprint of a deep water well pumping station building. "
            "Dimensions: {largo:.1f}m length by {ancho:.1f}m width. Plan view showing: drilled water well head with 5 L/s submersible turbine pump, "
            "discharge manifold piping with check valves, magnetic flowmeter, pressure gauges, electrical control panel enclosure with variable "
            "frequency drive (VFD), and chlorine pre-dosing chemical injection port. Cross section showing concrete pump base plinth, overhead "
            "lifting beam for pump maintenance, security door, and sanitary buffer zone. Black ink CAD vector style, technical annotations in "
            "Spanish, metric dimensions. Technical CAD details, wall line weights, door swing arcs, dimension strings, structural grid markers, "
            "title block in Spanish, high contrast schematic engineering drawing, --ar 16:9 --style raw --v 6.0"
        ),
    },
    "EDIF-15": {
        "titulo": "Planta PTAP y Reservorio Regulador (120 m³)",
        "detalles": [
            (
                "Distribución",
                "Tren de tratamiento de agua potable (filtro multimedia de arena-antracita, filtro de carbón activado, sistema de dosificación de hipoclorito de sodio) y reservorio apoyado de concreto armado de $120\\text{ m}^3$ con caseta de válvulas de impulsión y red contra incendios.",
            ),
            (
                "Normativa",
                "RNE OS.020 (Plantas de tratamiento) / D.S. 031-2010-SA (Calidad de agua para consumo humano).",
            ),
        ],
        "prompt": (
            "[STRICT 2D CAD ARCHITECTURAL BLUEPRINT] Orthogonal 2D floor plan and cross-section layout, "
            "monochromatic black line drawing on pristine white technical drafting grid background. "
            "No 3D, no isometric, no perspective, no photorealism. Sanitary engineering CAD blueprint of a Drinking Water Treatment "
            "Plant (PTAP) and 120 m3 reinforced concrete water storage reservoir. Overall area: {largo:.1f}m x {ancho:.1f}m. Top view: enclosed "
            "filtration building housing dual multimedia sand-anthracite pressure filters, activated carbon vessel, sodium hypochlorite "
            "disinfection skids, booster pump set for camp distribution; adjacent circular or rectangular 120m3 potable water storage tank "
            "with valve chamber and dedicated fire hydrant reserve suction. Cross section showing tank water level indicators, baffle walls, "
            "aeration vents, and chemical room drainage. CAD drafting, metric units, annotations in Spanish. Technical CAD details, wall line "
            "weights, door swing arcs, dimension strings, structural grid markers, title block in Spanish, high contrast schematic engineering "
            "drawing, --ar 16:9 --style raw --v 6.0"
        ),
    },
    "EDIF-16": {
        "titulo": "Planta PTAR MBBR y Tratamiento de Aguas Residuales",
        "detalles": [
            (
                "Distribución",
                "Cámara de rejas y desarenador, reactor biológico de lecho móvil (MBBR) con bioportadores de plástico y difusores de burbuja fina, sedimentador secundario de tolva, tanque de desinfección UV/cloro y lechos de secado de lodos estabilizados.",
            ),
            (
                "Normativa",
                "RNE OS.090 (Tratamiento de aguas residuales) / D.S. 004-2017-MINAM (LMP efluentes tratados para riego).",
            ),
        ],
        "prompt": (
            "[STRICT 2D CAD ARCHITECTURAL BLUEPRINT] Orthogonal 2D floor plan and cross-section layout, "
            "monochromatic black line drawing on pristine white technical drafting grid background. "
            "No 3D, no isometric, no perspective, no photorealism. Sanitary and civil engineering CAD blueprint of a Modular Biological "
            "Wastewater Treatment Plant (PTAR MBBR) for 250 occupants. Dimensions: {largo:.1f}m x {ancho:.1f}m. Layout displays: manual and fine mechanical "
            "bar screen chamber, grit chamber, biological aeration tank containing MBBR suspended biofilm carriers with bottom fine bubble "
            "diffusers, aeration blower room, secondary clarifier settling tank with sludge recycle pump, UV disinfection channel, and adjacent "
            "sludge drying sand beds. Cross-section showing submerged water flow levels, air piping, and effluent discharge monitoring flume. "
            "Professional technical CAD lineart, dimension lines, Spanish labels. Technical CAD details, wall line weights, door swing arcs, "
            "dimension strings, structural grid markers, title block in Spanish, high contrast schematic engineering drawing, --ar 16:9 --style raw --v 6.0"
        ),
    },
    "EDIF-17": {
        "titulo": "Trampas de Grasa Industriales pre-PTAR",
        "detalles": [
            (
                "Distribución",
                "Cámara de retención gravimétrica de grasas en concreto armado con recubrimiento epóxico, dos compartimentos con pantallas deflectoras, vertedero de salida con sello hidráulico y tapas herméticas de hierro fundido para limpieza periódica.",
            ),
            (
                "Normativa",
                "RNE IS.010 (Instalaciones sanitarias interiores - trampa de grasa para cocinas comerciales).",
            ),
        ],
        "prompt": (
            "[STRICT 2D CAD ARCHITECTURAL BLUEPRINT] Orthogonal 2D floor plan and cross-section layout, "
            "monochromatic black line drawing on pristine white technical drafting grid background. "
            "No 3D, no isometric, no perspective, no photorealism. Detailed technical CAD blueprint of an industrial two-chamber grease "
            "interceptor tank (trampa de grasa) for kitchen wastewater pre-treatment. Dimensions: {largo:.1f}m x {ancho:.1f}m. Plan view showing: "
            "influent inlet pipe from industrial kitchen, baffle weir plates separating grease floating layer, clean water bottom transfer "
            "baffle, and discharge outlet to sewer collector. Detail section A-A' showing reinforced concrete walls with epoxy protective "
            "coating, grease skimming access hatches with airtight cast-iron covers, and vent pipes. Accurate CAD lines, dimensions in meters, "
            "technical annotations in Spanish. Technical CAD details, wall line weights, door swing arcs, dimension strings, structural grid "
            "markers, title block in Spanish, high contrast schematic engineering drawing, --ar 16:9 --style raw --v 6.0"
        ),
    },
    "EDIF-18": {
        "titulo": "Centro de Acopio Temporal de Residuos Sólidos (CAT)",
        "detalles": [
            (
                "Distribución",
                "Celdas techadas y señalizadas según código de colores NTP 900.058 (peligrosos, metálicos, plásticos, papel/cartón, orgánicos, residuos de túnel/roca), losa de concreto con canaletas perimetrales y trampa de lixiviados, balanza de pesaje y cerco de malla olímpica con portón de acceso para camiones.",
            ),
            ("Normativa", "D.Leg. 1278 (Ley de Gestión Integral de Residuos Sólidos)."),
        ],
        "prompt": (
            "[STRICT 2D CAD ARCHITECTURAL BLUEPRINT] Orthogonal 2D floor plan and cross-section layout, "
            "monochromatic black line drawing on pristine white technical drafting grid background. "
            "No 3D, no isometric, no perspective, no photorealism. Civil and environmental CAD blueprint of a Central Solid Waste Storage "
            "and Segregation Facility (CAT) for a mining construction camp. Dimensions: {largo:.1f}m x {ancho:.1f}m. Plan layout detailing: "
            "segregated roofed storage bays following safety color codes (hazardous waste, industrial scrap metal, plastics, paper-cardboard, "
            "organic waste, oily rags/filters); perimeter concrete containment curb, leachate collection sump tank, truck scale, and "
            "chain-link security fence with 6m rolling truck gate. Cross section cut showing metal canopy roof, concrete impermeable floor "
            "slab, and safety eyewash station. Technical CAD drawing, Spanish annotations. Technical CAD details, wall line weights, door swing "
            "arcs, dimension strings, structural grid markers, title block in Spanish, high contrast schematic engineering drawing, "
            "--ar 16:9 --style raw --v 6.0"
        ),
    },
    "EDIF-19": {
        "titulo": "Área de Compostaje y Manejo de Lodos",
        "detalles": [
            (
                "Distribución",
                "Trincheras de volteo para compostaje aeróbico de residuos orgánicos de cocina y lodos estabilizados de PTAR, losa de concreto impermeabilizado con pendiente hacia canaleta de recirculación, zona de acopio de material estructurante (aserrín/paja) y cubierta semicubierta para protección contra lluvias intensas.",
            ),
            (
                "Normativa",
                "D.Leg. 1278 / RNE OS.090 (Estabilización de lodos de plantas de tratamiento).",
            ),
        ],
        "prompt": (
            "[STRICT 2D CAD ARCHITECTURAL BLUEPRINT] Orthogonal 2D floor plan and cross-section layout, "
            "monochromatic black line drawing on pristine white technical drafting grid background. "
            "No 3D, no isometric, no perspective, no photorealism. Environmental engineering CAD blueprint of an organic waste composting "
            "and sewage sludge stabilization area. Dimensions: {largo:.1f}m x {ancho:.1f}m. Floor plan detailing: three parallel concrete "
            "composting windrow bays with aeration piping beneath, wood chip and structuring material storage bay, curing pile zone, and "
            "perimeter collection channel for runoff leachate returning to treatment. Cross section showing light structural roof shed "
            "protecting piles from mountain rain and snow, impermeable membrane liner, and gravel drainage base. Clean CAD blueprint lines, "
            "Spanish labels, metric dimensions. Technical CAD details, wall line weights, door swing arcs, dimension strings, structural grid "
            "markers, title block in Spanish, high contrast schematic engineering drawing, --ar 16:9 --style raw --v 6.0"
        ),
    },
    "EDIF-20": {
        "titulo": "Casa de Fuerza y Generadores Diésel (2500 kVA)",
        "detalles": [
            (
                "Distribución",
                "2 grupos electrógenos encapsulados insonorizados de 1250 kVA c/u en sincronismo (2500 kVA total), bancada de concreto antisísmica con aisladores de vibración, tablero de transferencia automática (TTA), celda de media tensión (MT), silenciadores hospitalarios y sistema contra incendios por CO₂ / agua nebulizada.",
            ),
            (
                "Normativa",
                "RNE EM.010 (Instalaciones electromecánicas) / Código Nacional de Electricidad (CNE Suministro).",
            ),
        ],
        "prompt": (
            "[STRICT 2D CAD ARCHITECTURAL BLUEPRINT] Orthogonal 2D floor plan and cross-section layout, "
            "monochromatic black line drawing on pristine white technical drafting grid background. "
            "No 3D, no isometric, no perspective, no photorealism. Electromechanical CAD blueprint sheet of a primary diesel power "
            "generation plant (Casa de Fuerza, 2500 kVA) for heavy tunneling operations. Dimensions: {largo:.1f}m length by {ancho:.1f}m width. "
            "Plan view showing: two 1250 kVA acoustic-enclosed diesel generator sets mounted on independent vibration-isolated concrete "
            "inertia blocks, central synchronization and Automatic Transfer Switch (ATS) cabinet line, medium voltage transformer cell, "
            "battery start banks, and double-walled day fuel tanks. Cross section displaying sound-attenuating wall baffles, roof-mounted "
            "exhaust silencers, and overhead electrical cable raceways. Detailed CAD drawing style, metric dimensions, Spanish electrical "
            "labels. Technical CAD details, wall line weights, door swing arcs, dimension strings, structural grid markers, title block in "
            "Spanish, high contrast schematic engineering drawing, --ar 16:9 --style raw --v 6.0"
        ),
    },
    "EDIF-21": {
        "titulo": "Estación de Combustible Diésel (2x10,000 gal)",
        "detalles": [
            (
                "Distribución",
                "2 tanques horizontales aéreos de pared doble de 10,000 galones (75,000 litros total) dentro de cubeto estanco de concreto armado con capacidad para el 110% del tanque mayor, isla de despacho con 2 dispensadores de alto caudal (40 gpm para volquetes y jumbos), techo de protección contra intemperie, sistema de puesta a tierra y extintores rodantes de PQS de 50 kg.",
            ),
            (
                "Normativa",
                "D.S. 052-93-EM (Reglamento de Seguridad para Almacenamiento de Hidrocarburos) / NFPA 30.",
            ),
        ],
        "prompt": (
            "[STRICT 2D CAD ARCHITECTURAL BLUEPRINT] Orthogonal 2D floor plan and cross-section layout, "
            "monochromatic black line drawing on pristine white technical drafting grid background. "
            "No 3D, no isometric, no perspective, no photorealism. Industrial engineering CAD blueprint of a mining camp diesel fueling "
            "station (Estación de Combustible, 20,000 gallons total). Dimensions: {largo:.1f}m x {ancho:.1f}m. Top-down plan view detailing: two "
            "10,000-gallon double-wall steel storage tanks installed inside a reinforced concrete secondary containment dike (cubeto estanco "
            "110% volume), high-speed dual fuel dispensing island for heavy haul trucks and dumpers, truck unloading bay with grounding reel, "
            "fuel oil-water separator interceptor pit, and canopy canopy structure. Section view showing tank saddles, explosion-proof "
            "electrical piping, and grounding rods. Technical CAD draft, metric units, annotations in Spanish. Technical CAD details, "
            "wall line weights, door swing arcs, dimension strings, structural grid markers, title block in Spanish, high contrast schematic "
            "engineering drawing, --ar 16:9 --style raw --v 6.0"
        ),
    },
    "EDIF-22": {
        "titulo": "Casa de Cambio (Change-House) y Lampistería Portal A",
        "detalles": [
            (
                "Distribución",
                "Zona sucia (lockers para ropa de mina mojada/embarrada con sistema de aire caliente para secado rápido), batería de 20 duchas calientes con calentadores a gas, zona limpia (lockers para ropa civil de descanso), y módulo de lampistería con racks de recarga para 100 lámparas mineras LED y entrega de autorrescatadores de oxígeno químico.",
            ),
            (
                "Normativa",
                "D.S. 024-2016-EM Art. 97 (Casa de cambio obligatoria en boca de túnel) / NFPA 701.",
            ),
        ],
        "prompt": (
            "[STRICT 2D CAD ARCHITECTURAL BLUEPRINT] Orthogonal 2D floor plan and cross-section layout, "
            "monochromatic black line drawing on pristine white technical drafting grid background. "
            "No 3D, no isometric, no perspective, no photorealism. Architectural CAD blueprint of a mine portal Change-House and Lamp "
            "Room facility (Casa de Cambio y Lampistería). Dimensions: {largo:.1f}m length by {ancho:.1f}m width ({area:.0f} m2). Top-down floor plan: "
            '"Dirty side" locker room for muddy mining workgear with forced hot air drying racks, central shower block with 20 hot water shower '
            'stalls and non-slip sloped drainage, "Clean side" locker room for civilian clothes, and security-controlled Lampistería room '
            "with charging racks for 100 cordless mining cap lamps and self-rescuer respirator stations. Cross section showing elevated wire "
            "baskets for clothing, steam exhaust fans, and radiant floor heating. Professional vector CAD lineart on white grid, Spanish labels. "
            "Technical CAD details, wall line weights, door swing arcs, dimension strings, structural grid markers, title block in Spanish, "
            "high contrast schematic engineering drawing, --ar 16:9 --style raw --v 6.0"
        ),
    },
    "EDIF-23": {
        "titulo": "Polvorín de Superficie Certificado SUCAMEC (Portal A)",
        "detalles": [
            (
                "Emplazamiento",
                "Aislado a una distancia de seguridad reglamentaria de $\\ge 300\\text{ m}$ del campamento base.",
            ),
            (
                "Distribución",
                "Dos recintos independientes separados por muro cortafuego: Cámara 1 para dinamita y emulsión encartuchada; Cámara 2 para cordón detonante y fulminantes/detonadores electrónicos. Muros de concreto armado de $e=0.30\\text{ m}$, piso antichispa con losas de goma o plomo, puertas blindadas de acero con triple cerradura, pararrayos tipo Franklin y parapeto perimetral de tierra de $H=3.0\\text{ m}$ y $e=2.5\\text{ m}$ en corona.",
            ),
            (
                "Normativa",
                "Ley N° 30299 (SUCAMEC - Explosivos y Materiales Relacionados) / D.S. 024-2016-EM.",
            ),
        ],
        "prompt": (
            "[STRICT 2D CAD ARCHITECTURAL BLUEPRINT] Orthogonal 2D floor plan and cross-section layout, "
            "monochromatic black line drawing on pristine white technical drafting grid background. "
            "No 3D, no isometric, no perspective, no photorealism. High-security civil and mining CAD blueprint of a SUCAMEC-certified "
            "surface explosives magazine (Polvorín de Superficie). Building dimensions: {largo:.1f}m x {ancho:.1f}m. Floor plan detailing: dual "
            "compartmentalized chambers (Chamber 1 for dynamite and watergel emulsions; Chamber 2 for non-electric detonators and detonating "
            "cord) separated by a 300mm fireproof blast wall; anti-spark copper-grounded floor finish, double-leaf armored steel blast doors "
            "with triple security deadbolts, and natural labyrinth ventilation ports with brass mesh screens. Site plan detail shows surrounding "
            "3.0m high compacted earth barricade berm (parapeto) and lightning protection air terminal rod. Professional CAD linework, security "
            "annotations in Spanish, metric dimensions. Technical CAD details, wall line weights, door swing arcs, dimension strings, "
            "structural grid markers, title block in Spanish, high contrast schematic engineering drawing, --ar 16:9 --style raw --v 6.0"
        ),
    },
    "EDIF-24": {
        "titulo": "Garitas de Vigilancia y Balanza de Pesaje 80 t",
        "detalles": [
            (
                "Distribución",
                "Caseta de control patrimonial y vigilancia con visión panorámica 360°, torniquetes de control biométrico para ingreso de personal, sistema de cámaras CCTV, y plataforma metálica de balanza camionera de pesaje dinámico de $18.0\\text{ m} \\times 3.0\\text{ m}$ con capacidad para 80 toneladas con semáforo y talanqueras automáticas.",
            ),
            (
                "Normativa",
                "RNE G.050 / MTC (Control de pesos y dimensiones vehiculares).",
            ),
        ],
        "prompt": (
            "[STRICT 2D CAD ARCHITECTURAL BLUEPRINT] Orthogonal 2D floor plan and cross-section layout, "
            "monochromatic black line drawing on pristine white technical drafting grid background. "
            "No 3D, no isometric, no perspective, no photorealism. Architectural and civil CAD blueprint of a main camp security gatehouse "
            "and 80-ton truck weighbridge scale. Footprint: {largo:.1f}m x {ancho:.1f}m. Plan view showing: guardhouse room with 360-degree observation "
            "windows, security turnstile with biometric fingerprint reader, computer desk for weighing management, surveillance CCTV monitor "
            "racks, and adjacent 18.0m long pitless truck scale platform for 80-ton heavy dumpers, equipped with automated barrier gates, traffic "
            "lights, and wheel alignment curbs. Elevation section showing raised operator view and weather-resistant overhanging roof. Precise "
            "CAD line drawing, dimension strings, Spanish text on grid paper. Technical CAD details, wall line weights, door swing arcs, "
            "dimension strings, structural grid markers, title block in Spanish, high contrast schematic engineering drawing, --ar 16:9 --style raw --v 6.0"
        ),
    },
    "EDIF-25": {
        "titulo": "Playa de Estacionamiento de Vehículos Livianos y Buses",
        "detalles": [
            (
                "Capacidad",
                "20 cajones para camionetas 4x4 ($2.50\\text{ m} \\times 5.00\\text{ m}$) + 4 bahías para buses interurbanos de 45 pasajeros ($3.50\\text{ m} \\times 12.00\\text{ m}$).",
            ),
            (
                "Distribución",
                "Carriles de circulación en doble sentido de $6.0\\text{ m}$ de ancho, radios de giro de $12.0\\text{ m}$, señalización horizontal pintada, topes de llantas de concreto, iluminación con postes solares LED y canaleta pluvial.",
            ),
            ("Normativa", "RNE A.010 (Capítulo X - Estacionamientos)."),
        ],
        "prompt": (
            "[STRICT 2D CAD ARCHITECTURAL BLUEPRINT] Orthogonal 2D floor plan and cross-section layout, "
            "monochromatic black line drawing on pristine white technical drafting grid background. "
            "No 3D, no isometric, no perspective, no photorealism. Civil engineering CAD blueprint layout of a vehicular parking lot for "
            "a mining camp. Dimensions: {largo:.1f}m length by {ancho:.1f}m width ({area:.0f} m2). Plan view detailing: 20 marked parking bays for 4x4 pickup "
            "trucks (2.5m x 5.0m each), 4 long parking bays for 50-passenger interprovincial crew transport buses (3.5m x 12.0m each), 6.0m wide "
            "central two-way asphalt circulation lanes with directional pavement arrows, concrete wheel stops, perimeter curb drainage "
            "channels, and solar LED lighting pole locations. Technical CAD drafting, crisp black lines on millimeter grid paper, dimensions "
            "and Spanish signage. Technical CAD details, wall line weights, door swing arcs, dimension strings, structural grid markers, "
            "title block in Spanish, high contrast schematic engineering drawing, --ar 16:9 --style raw --v 6.0"
        ),
    },
    "EDIF-26": {
        "titulo": "Patio de Parqueo y Maniobras de Maquinaria Pesada",
        "detalles": [
            (
                "Capacidad",
                "Estacionamiento y maniobra para 2 Jumbos de perforación electrohidráulica, 2 Scooptrams LHD subterráneos, 6 volquetes mineros de 20 m³, 1 camión mixer de shotcrete y 1 excavadora sobre orugas.",
            ),
            (
                "Configuración",
                "Plataforma estabilizada con subbase de 30 cm de afirmado compactado, radio libre de giro $\\ge 15.0\\text{ m}$, cunetas de coronación y desarenador perimetral.",
            ),
            (
                "Normativa",
                "MTC EG-2013 (Sección 104 - Patios de maquinaria) / RNE A.060.",
            ),
        ],
        "prompt": (
            "[STRICT 2D CAD ARCHITECTURAL BLUEPRINT] Orthogonal 2D floor plan and cross-section layout, "
            "monochromatic black line drawing on pristine white technical drafting grid background. "
            "No 3D, no isometric, no perspective, no photorealism. Civil engineering site plan CAD blueprint of an outdoor heavy tunneling "
            "equipment parking and staging yard. Dimensions: {largo:.1f}m x {ancho:.1f}m ({area:,.0f} m2). Plan shows: designated parking stalls for two "
            "twin-boom jumbo drill rigs, two underground LHD scoops, six 20m3 dump trucks, and shotcrete mixer trucks; central 15.0m turning "
            "radius maneuver circle, reinforced heavy-duty aggregate crushed stone surfacing, perimeter stormwater drainage swales with concrete "
            "sediment traps, and high-mast floodlight towers. Black vector CAD drafting, metric dimension annotations, title in Spanish. "
            "Technical CAD details, wall line weights, door swing arcs, dimension strings, structural grid markers, title block in Spanish, "
            "high contrast schematic engineering drawing, --ar 16:9 --style raw --v 6.0"
        ),
    },
    "EDIF-27": {
        "titulo": "Playa de Estacionamiento y Parqueo Auxiliar",
        "detalles": [
            (
                "Capacidad",
                "8 camionetas técnicas 4x4 de supervisión y guardia + 2 minibuses de traslado de personal + 2 posiciones transitorias para volquetes.",
            ),
            (
                "Distribución",
                "Losa afirmada compactada, demarcación con pintura termoplástica reflectiva, tope-llantas y canaletas pluviales.",
            ),
            ("Normativa", "RNE A.010."),
        ],
        "prompt": (
            "[STRICT 2D CAD ARCHITECTURAL BLUEPRINT] Orthogonal 2D floor plan and cross-section layout, "
            "monochromatic black line drawing on pristine white technical drafting grid background. "
            "No 3D, no isometric, no perspective, no photorealism. Civil engineering CAD blueprint site plan of an auxiliary vehicle parking "
            "lot for a satellite tunnel portal (Portal B). Dimensions: {largo:.1f}m x {ancho:.1f}m ({area:.0f} m2). Plan layout detailing: 8 parking spaces "
            "for 4x4 technical pickup trucks, 2 parking bays for 25-passenger crew minibuses, 2 heavy haul dumper staging slots, 6.0m central "
            "turning driveway with painted circulation directional markings, concrete tire bumpers, and peripheral drainage swale. Accurate "
            "black vector CAD lineart, metric dimensions, Spanish annotations on millimeter grid paper. Technical CAD details, wall line "
            "weights, door swing arcs, dimension strings, structural grid markers, title block in Spanish, high contrast schematic engineering "
            "drawing, --ar 16:9 --style raw --v 6.0"
        ),
    },
    "EDIF-28": {
        "titulo": "Polvorín Satélite Certificado SUCAMEC (Portal B)",
        "detalles": [
            (
                "Emplazamiento",
                "Emplazamiento autónomo en ladera segura a $\\ge 300\\text{ m}$ de las instalaciones habitadas del Campamento 2.",
            ),
            (
                "Distribución",
                "Polvorín de superficie con división interior para dinamita/emulsión y fulminantes de voladura para el Frente 2. Muros blindados de concreto armado de $30\\text{ cm}$, ventilación laberíntica antichispa, puerta de acero blindada y parapeto exterior de tierra de $H=3.0\\text{ m}$.",
            ),
            ("Normativa", "Ley N° 30299 (SUCAMEC)."),
        ],
        "prompt": (
            "[STRICT 2D CAD ARCHITECTURAL BLUEPRINT] Orthogonal 2D floor plan and cross-section layout, "
            "monochromatic black line drawing on pristine white technical drafting grid background. "
            "No 3D, no isometric, no perspective, no photorealism. High-security civil and mining CAD blueprint of a satellite surface "
            "explosives magazine (Polvorín Satélite Portal B) certified under SUCAMEC standards. Dimensions: {largo:.1f}m x {ancho:.1f}m. Floor plan "
            "detailing: dual internal explosive storage chambers with anti-spark conductive rubber floor lining, thick 300mm reinforced concrete "
            "walls, armored steel security door with double high-security padlocks, and angled labyrinth air vent louvers with copper flame-trap mesh. "
            "Exterior detail shows surrounding 3.0m high compacted earth protective barricade berm (parapeto) and grounding copper grid. "
            "Professional CAD drafting, metric units, Spanish security callouts. Technical CAD details, wall line weights, door swing arcs, "
            "dimension strings, structural grid markers, title block in Spanish, high contrast schematic engineering drawing, --ar 16:9 --style raw --v 6.0"
        ),
    },
    "EDIF-29": {
        "titulo": "Nave Taller Mecánico Auxiliar y Lubricación",
        "detalles": [
            (
                "Distribución",
                "2 bahías de mantenimiento preventivo para maquinaria del Frente 2 (cambio de brocas, mangueras hidráulicas y filtros de Jumbo y Scoop), fosa de lubricación de 10 m, tecle eléctrico de 5 Tn sobre viga IPE, banco de ajuste y almacén de aceites.",
            ),
            ("Normativa", "RNE A.060 (Industria y talleres mecánicos)."),
        ],
        "prompt": (
            "[STRICT 2D CAD ARCHITECTURAL BLUEPRINT] Orthogonal 2D floor plan and cross-section layout, "
            "monochromatic black line drawing on pristine white technical drafting grid background. "
            "No 3D, no isometric, no perspective, no photorealism. Architectural and structural CAD blueprint of a satellite heavy equipment "
            "maintenance and lubrication workshop (Taller Auxiliar Portal B). Dimensions: {largo:.1f}m length by {ancho:.1f}m width. Plan view showing: "
            "2 service bays for underground tunneling loaders and drill rigs, 10.0m long reinforced concrete mechanic service pit with safety "
            "grating, 5-ton overhead monorail electric hoist crane beam, workbench tool wall, and lube oil drum storage area with spill "
            "containment pallet. Cross section showing 6.0m clear internal height, rigid steel frame structure, insulated panel roof, and "
            "heavy concrete slab. CAD technical lineart, metric dimensions, Spanish text. Technical CAD details, wall line weights, door swing "
            "arcs, dimension strings, structural grid markers, title block in Spanish, high contrast schematic engineering drawing, "
            "--ar 16:9 --style raw --v 6.0"
        ),
    },
    "EDIF-30": {
        "titulo": "Estación de Combustible Satélite (1x10,000 gal)",
        "detalles": [
            (
                "Distribución",
                "1 tanque horizontal aéreo cilíndrico de doble pared de 10,000 galones diésel D-5 dentro de dique estanco de concreto armado (cubeto 110%), 1 dispensador de alto flujo con cuenta-litros digital, sistema de filtrado de combustible y bandeja receptora de goteo.",
            ),
            ("Normativa", "D.S. 052-93-EM (Seguridad en hidrocarburos)."),
        ],
        "prompt": (
            "[STRICT 2D CAD ARCHITECTURAL BLUEPRINT] Orthogonal 2D floor plan and cross-section layout, "
            "monochromatic black line drawing on pristine white technical drafting grid background. "
            "No 3D, no isometric, no perspective, no photorealism. Civil and mechanical CAD blueprint of an autonomous satellite diesel "
            "fuel storage and dispensing station (10,000 gal). Overall footprint: {largo:.1f}m x {ancho:.1f}m. Plan view showing: one 10,000-gallon "
            "double-walled horizontal steel fuel tank located inside a concrete containment dike basin (cubeto de retención), diesel dispenser "
            "pump island with hose reel and electronic flow meter, truck unloading connection with emergency shut-off valve, and concrete spill "
            "pad with oil interceptor drain. Cross section showing tank concrete saddle foundations, lightning rod, and canopy roof. Precision "
            "CAD drafting, metric units, annotations in Spanish. Technical CAD details, wall line weights, door swing arcs, dimension strings, "
            "structural grid markers, title block in Spanish, high contrast schematic engineering drawing, --ar 16:9 --style raw --v 6.0"
        ),
    },
    "EDIF-31": {
        "titulo": "Casa de Fuerza Satélite y Generadores (1000 kVA)",
        "detalles": [
            (
                "Distribución",
                "1 grupo electrógeno diésel encapsulado insonorizado de 1000 kVA para servicio continuo 24/7 (energía para bombeo de agua de mina, ventilador secundario del túnel e iluminación de campamento), tablero de control con TTA, celda de distribución eléctrica en baja/media tensión y banco de baterías.",
            ),
            ("Normativa", "RNE EM.010 / CNE Suministro."),
        ],
        "prompt": (
            "[STRICT 2D CAD ARCHITECTURAL BLUEPRINT] Orthogonal 2D floor plan and cross-section layout, "
            "monochromatic black line drawing on pristine white technical drafting grid background. "
            "No 3D, no isometric, no perspective, no photorealism. Electromechanical CAD blueprint of an auxiliary diesel power generation "
            "plant (Casa de Fuerza Satélite, 1000 kVA) for tunnel excavation front 2. Dimensions: {largo:.1f}m x {ancho:.1f}m. Plan view showing: "
            "1000 kVA acoustic-enclosed heavy-duty diesel generator set anchored to a vibration-damped concrete foundation pad, main distribution "
            "switchgear board with Automatic Transfer Switch (ATS), fuel day tank with secondary containment, and battery starter racks. Section "
            "view showing acoustic wall panels, radiator hot air exhaust ducting through wall louvers, and ceiling cable ladders. Accurate CAD "
            "vector line drawing, Spanish labels, metric dimensions. Technical CAD details, wall line weights, door swing arcs, dimension "
            "strings, structural grid markers, title block in Spanish, high contrast schematic engineering drawing, --ar 16:9 --style raw --v 6.0"
        ),
    },
    "EDIF-32": {
        "titulo": "Planta Compacta de Saneamiento (PTAP / PTAR Modulares)",
        "detalles": [
            (
                "Distribución",
                "Contenedor marítimo de 40 pies acondicionado como Planta de Tratamiento de Agua Potable (PTAP compacta con filtros multimedia y dosificación química) + Contenedor de 40 pies con sistema de tratamiento biológico de aguas residuales (PTAR MBBR compacta) + reservorio flexible/metálico de agua tratada para los 98 ocupantes del Portal B.",
            ),
            ("Normativa", "RNE OS.020 / RNE OS.090 / D.S. 004-2017-MINAM."),
        ],
        "prompt": (
            "[STRICT 2D CAD ARCHITECTURAL BLUEPRINT] Orthogonal 2D floor plan and cross-section layout, "
            "monochromatic black line drawing on pristine white technical drafting grid background. "
            "No 3D, no isometric, no perspective, no photorealism. Environmental engineering CAD blueprint of a containerized modular water "
            "treatment plant (combined compact PTAP and PTAR). Dimensions: {largo:.1f}m x {ancho:.1f}m. Plan layout detailing: one 40-foot insulated "
            "shipping container housing a compact Potable Water Treatment Plant (multi-media sand and carbon filters, UV sterilizer, chlorine doser) "
            "with a 40 m3 elevated water storage tank; adjacent 40-foot container housing a biological MBBR wastewater treatment system (blowers, "
            "aeration chamber, secondary clarifier, disinfection); and interconnecting insulated piping. Cross section showing structural concrete "
            "foundation slab and frost protection heat tracing. Technical CAD lines, metric scale, Spanish labels. Technical CAD details, wall line "
            "weights, door swing arcs, dimension strings, structural grid markers, title block in Spanish, high contrast schematic engineering "
            "drawing, --ar 16:9 --style raw --v 6.0"
        ),
    },
    "EDIF-33": {
        "titulo": "Bodega de Insumos Críticos y Acopio de Residuos",
        "detalles": [
            (
                "Distribución",
                "Módulo bifuncional dividido en dos áreas independientes: Área A (Bodega de repuestos críticos de avance de perforación, pernos helicoidales y mangueras para no depender de Portal A); Área B (Centro de acopio temporal de residuos sólidos clasificados según NTP 900.058).",
            ),
            ("Normativa", "RNE A.060 / D.Leg. 1278."),
        ],
        "prompt": (
            "[STRICT 2D CAD ARCHITECTURAL BLUEPRINT] Orthogonal 2D floor plan and cross-section layout, "
            "monochromatic black line drawing on pristine white technical drafting grid background. "
            "No 3D, no isometric, no perspective, no photorealism. Architectural CAD blueprint of a dual-purpose logistics storehouse and "
            "hazardous/solid waste segregation shelter (Bodega y Acopio Portal B). Dimensions: {largo:.1f}m x {ancho:.1f}m. Plan view showing: a central "
            "dividing fire partition wall; Section 1: secure tool and spare parts storage with metal shelving racks for tunnel drilling consumables; "
            "Section 2: temporary sorted waste collection depot with color-coded containment bays (hazardous, scrap metal, general waste), concrete "
            "bunded floor, and spill response kit. Cross-section showing insulated steel frame structure, high ventilation louvers, and double "
            "security doors. Technical CAD draft, metric dimensions, Spanish text on grid paper. Technical CAD details, wall line weights, door "
            "swing arcs, dimension strings, structural grid markers, title block in Spanish, high contrast schematic engineering drawing, "
            "--ar 16:9 --style raw --v 6.0"
        ),
    },
    "EDIF-34": {
        "titulo": "Lavandería Satélite y Ropería",
        "detalles": [
            (
                "Distribución",
                "Módulo térmico con 2 lavadoras industriales de 25 kg, 2 secadoras a gas GLP, mesa de doblado y estantes de entrega de ropa de cama y ropa térmica limpia para los 98 trabajadores de guardia del Portal B.",
            ),
            ("Normativa", "RNE G.050."),
        ],
        "prompt": (
            "[STRICT 2D CAD ARCHITECTURAL BLUEPRINT] Orthogonal 2D floor plan and cross-section layout, "
            "monochromatic black line drawing on pristine white technical drafting grid background. "
            "No 3D, no isometric, no perspective, no photorealism. Architectural CAD blueprint of a compact satellite camp laundry facility "
            "(Lavandería Satélite) sized for 100 workers. Dimensions: {largo:.1f}m x {ancho:.1f}m. Floor plan detailing: dirty workwear drop-off hatch, "
            "2 commercial front-load washing machines (25kg capacity), 2 commercial heavy-duty dryers with external lint exhaust vents, stainless "
            "steel folding counter, and clean linen storage shelves. Cross-section showing non-slip waterproof ceramic floor tiles, floor drainage "
            "trough, water supply manifolds, and wall insulation. Clean vector CAD linework on graph paper, metric dimensions, Spanish annotations. "
            "Technical CAD details, wall line weights, door swing arcs, dimension strings, structural grid markers, title block in Spanish, high contrast "
            "schematic engineering drawing, --ar 16:9 --style raw --v 6.0"
        ),
    },
    "EDIF-35": {
        "titulo": "Módulo Recreativo y Sala de Usos Múltiples (SUM)",
        "detalles": [
            (
                "Distribución",
                "Espacio de recreación y salud mental para el personal aislado del Portal B: sala de estar con sillones ergonómicos y pantalla satelital, mesa de billar, mesa de ping-pong, biblioteca/estación de internet y pequeño rincón de ejercicios con caminadora y pesas.",
            ),
            (
                "Normativa",
                "D.S. 024-2016-EM (Bienestar ocupacional en campamentos remotos).",
            ),
        ],
        "prompt": (
            "[STRICT 2D CAD ARCHITECTURAL BLUEPRINT] Orthogonal 2D floor plan and cross-section layout, "
            "monochromatic black line drawing on pristine white technical drafting grid background. "
            "No 3D, no isometric, no perspective, no photorealism. Architectural CAD blueprint of a satellite recreational lounge and "
            "multi-purpose hall (Módulo Recreativo y SUM Portal B). Dimensions: {largo:.1f}m x {ancho:.1f}m. Floor plan shows: leisure lounge area with "
            "comfortable armchairs and wall-mounted satellite TV, recreation zone with a pool table and table tennis table, 4-seat internet "
            "computer desk station, and a small fitness exercise area with cardio machines. Detail cross section showing acoustic wood-slat wall "
            "panels, carpet tile flooring, insulated panel ceiling, and wall-mounted electric convector heaters. Technical CAD line drawing, "
            "metric dimension strings, Spanish text. Technical CAD details, wall line weights, door swing arcs, dimension strings, structural "
            "grid markers, title block in Spanish, high contrast schematic engineering drawing, --ar 16:9 --style raw --v 6.0"
        ),
    },
    "EDIF-36": {
        "titulo": "Garita de Control de Acceso y Lampistería Satélite",
        "detalles": [
            (
                "Distribución",
                "Módulo ubicado en el acceso principal del Portal B. Incluye cabina de vigilancia con control biométrico vehicular/peatonal y sala contigua de lampistería satélite con rack de recarga para 40 lámparas mineras y entrega de autorrescatadores para el turno de perforación del Frente 2.",
            ),
            ("Normativa", "RNE G.050 / D.S. 024-2016-EM Art. 97."),
        ],
        "prompt": (
            "[STRICT 2D CAD ARCHITECTURAL BLUEPRINT] Orthogonal 2D floor plan and cross-section layout, "
            "monochromatic black line drawing on pristine white technical drafting grid background. "
            "No 3D, no isometric, no perspective, no photorealism. Architectural CAD blueprint of a dual entrance security gatehouse and "
            "satellite lamp room (Garita y Lampistería Portal B). Dimensions: {largo:.1f}m x {ancho:.1f}m. Plan view showing: security guard control "
            "office with panoramic inspection windows and biometric badge turnstile; adjacent Lampistería room with wall-mounted battery charging "
            "racks for 40 mining cap lamps and storage lockers for emergency chemical self-rescuers; and vehicular boom barrier gate outside. "
            "Section cut showing raised observation floor, insulated polyurethane sandwich panels, and exterior floodlight bracket. Professional "
            "CAD drafting, metric units, annotations in Spanish. Technical CAD details, wall line weights, door swing arcs, dimension strings, "
            "structural grid markers, title block in Spanish, high contrast schematic engineering drawing, --ar 16:9 --style raw --v 6.0"
        ),
    },
    "EDIF-37": {
        "titulo": "Caseta de Seguridad y Custodia de Polvorín Principal",
        "detalles": [
            (
                "Emplazamiento",
                "Emplazada al pie del parapeto del polvorín (Portal A), con línea visual directa al cerco perimetral de explosivos.",
            ),
            (
                "Distribución",
                "Caseta con vidrio blindado nivel III-A, tronera para defensa, radio transceptor troncalizado VHF/HF, panel de control de reflector piramidal de 1000 W y servicio higiénico completo.",
            ),
            (
                "Normativa",
                "Ley N° 30299 (SUCAMEC - Requisitos de custodia armada in situ 24/7).",
            ),
        ],
        "prompt": (
            "[STRICT 2D CAD ARCHITECTURAL BLUEPRINT] Orthogonal 2D floor plan and cross-section layout, "
            "monochromatic black line drawing on pristine white technical drafting grid background. "
            "No 3D, no isometric, no perspective, no photorealism. Architectural and security CAD blueprint of an armed guard security post "
            "(Caseta de Seguridad) for an explosives magazine. Dimensions: {largo:.1f}m x {ancho:.1f}m. Top view showing: bullet-resistant guard "
            "observation booth, ballistic glass windows, defensive firing port (tronera), surveillance radio communications console, searchlight "
            "directional joystick panel, gun rack, and internal compact private bathroom with shower. Cross section showing reinforced concrete "
            "masonry walls, insulated roof with 360-degree rotating high-power LED searchlight, and perimeter concertina wire tie-in. CAD technical "
            "linework, metric scale, Spanish labels. Technical CAD details, wall line weights, door swing arcs, dimension strings, structural "
            "grid markers, title block in Spanish, high contrast schematic engineering drawing, --ar 16:9 --style raw --v 6.0"
        ),
    },
    "EDIF-38": {
        "titulo": "Caseta de Seguridad y Custodia de Polvorín Satélite",
        "detalles": [
            (
                "Emplazamiento",
                "Emplazada al pie del parapeto del polvorín satélite (Portal B), a 300 m de separación del campamento.",
            ),
            (
                "Distribución",
                "Módulo blindado de vigilancia para guardia armado 24/7 con vidrio de alta seguridad, tronera de defensa, radiocomunicador punto a punto con Portal A y Campamento 2, reflector perimetral y baño privado.",
            ),
            ("Normativa", "Ley N° 30299 (SUCAMEC)."),
        ],
        "prompt": (
            "[STRICT 2D CAD ARCHITECTURAL BLUEPRINT] Orthogonal 2D floor plan and cross-section layout, "
            "monochromatic black line drawing on pristine white technical drafting grid background. "
            "No 3D, no isometric, no perspective, no photorealism. High-security architectural CAD blueprint of an armed guard observation "
            "booth (Caseta de Custodia Polvorín Satélite) for a remote mountain explosives magazine. Dimensions: {largo:.1f}m x {ancho:.1f}m. Plan "
            "view showing: reinforced guard room with ballistic-resistant vision panels, defensive rifle firing port, UHF/VHF communications "
            "console, 360-degree high-lumen perimeter floodlight switchboard, wall gun rack, and compact integrated bathroom. Cross section "
            "showing reinforced concrete block walls, insulated roof with searchlight pedestal, and perimeter security fencing link. Precise black "
            "line CAD technical drafting, metric dimensions, Spanish security labels. Technical CAD details, wall line weights, door swing arcs, "
            "dimension strings, structural grid markers, title block in Spanish, high contrast schematic engineering drawing, --ar 16:9 --style raw --v 6.0"
        ),
    },
}


def generar_prompts_cad(ctx: dict, carpeta_salida: Path, proyecto: str) -> Path:
    """Genera el catálogo técnico de prompts arquitectónicos CAD en formato Markdown.

    Args:
        ctx: Diccionario de contexto con resultados calculados del proyecto.
        carpeta_salida: Directorio donde se escribirá el archivo Markdown.
        proyecto: Nombre del proyecto túnel.

    Returns:
        Path del archivo Markdown generado.
    """
    carpeta_salida.mkdir(parents=True, exist_ok=True)
    archivo_salida = carpeta_salida / "prompts_edificaciones_cad.md"

    edificaciones = ctx.get("campamento", {}).get("edificaciones", [])
    total_area = sum(e.get("area_m2", 0.0) for e in edificaciones)

    pob_total = ctx.get("personal", {}).get("total", 346)
    pob_camp1 = ctx.get("campamento", {}).get("pob_camp1", 248)
    pob_camp2 = ctx.get("campamento", {}).get("pob_camp2", 98)

    # Separar en Campamento 1 y Campamento 2
    camp1_edifs = [e for e in edificaciones if e.get("campamento") == "CAMP1"]
    camp2_edifs = [e for e in edificaciones if e.get("campamento") == "CAMP2"]

    lineas: list[str] = [
        "# Catálogo de Prompts Arquitectónicos CAD para las 38 Edificaciones del Proyecto",
        "",
        f"**Proyecto:** {proyecto} (L = 5.539 km · 3,850 m s.n.m.)  ",
        f"**Población Total:** {pob_total} trabajadores (Régimen 14×7)  ",
        f"**Campamentos:** Campamento 1 Principal (Portal A - {pob_camp1} pax) y "
        f"Campamento 2 Satélite (Portal B - {pob_camp2} pax)  ",
        "**Marco Normativo:** Reglamento Nacional de Edificaciones (RNE), D.S. 024-2016-EM (Seguridad Minera), "
        "Ley N° 30299 (SUCAMEC), D.Leg. 1278 (Residuos Sólidos), MTC EG-2013.",
        "",
        "---",
        "",
        "## Guía de Uso Profesional para Generación CAD con IA (Midjourney v6, DALL-E 3, SDXL)",
        "",
        "Para garantizar que los motores de Inteligencia Artificial generen **planos técnicos arquitectónicos "
        "ortogonales en 2D con fondo blanco y líneas negras** (evitando renders 3D, perspectivas distorsionadas "
        "o sombras artísticas), todos los prompts de este catálogo han sido estandarizados bajo la siguiente "
        "estructura de ingeniería:",
        "",
        "### 1. Parámetros de Formato y Visualización",
        "- **Modo de Dibujo:** *Strict 2D Orthogonal Technical CAD Drafting* (Doble vista en lámina: Planta de distribución arriba + Sección de elevación transversal abajo).",
        "- **Estilo Gráfico:** *Monochromatic Black Vector Lineart on Clean White Background* (Líneas negras nítidas sobre fondo blanco limpio con cuadrícula milimétrica suave).",
        "- **Simbología Normalizada:** Muros cortados con grosor/hachurado, arcos de apertura de puertas, módulos de ventanas, cotas acotadas en metros y ejes estructurales.",
        "- **Aislamiento Térmico:** Paneles sándwich PIR de 100 mm y cerchas a dos aguas diseñados para heladas a 3,850 m s.n.m.",
        "",
        "### 2. Consejos para Cada Motor de IA:",
        "* **Para Midjourney v6:** Copia el prompt en inglés tal cual. Ya incluye los modificadores `--ar 16:9 --style raw --v 6.0` y exclusiones negativas para forzar plano 2D.",
        '* **Para DALL-E 3 / ChatGPT Plus:** Si utilizas ChatGPT, puedes anteponerle: *"Genera un plano técnico CAD 2D exactamente como se describe a continuación:"* antes de pegar el prompt en inglés.',
        "* **Negative Prompts (Exclusiones Universales):** `no 3D, no render, no photorealism, no perspective view, no artistic shadows, no realistic photos, no color fills`.",
        "",
        "---",
        "",
    ]

    def _render_bloque_edificacion(edif: dict) -> list[str]:
        eid = edif["id"]
        spec = CATALOGO_SPECS.get(eid, {})
        titulo = spec.get("titulo", edif.get("nombre", eid))
        largo = edif.get("largo_m", 0.0)
        ancho = edif.get("ancho_m", 0.0)
        area = edif.get("area_m2", 0.0)
        grupo = edif.get("grupo", "")

        bloque: list[str] = [
            f"### {eid}: {titulo}",
            f"- **Grupo:** {grupo}",
            f"- **Dimensiones:** ${largo:.1f}\\text{{ m}} \\times {ancho:.1f}\\text{{ m}}$ (Área techada: **${area:,.1f}\\text{{ m}}^2$**)",
        ]

        for clave_detalle, valor_detalle in spec.get("detalles", []):
            bloque.append(f"- **{clave_detalle}:** {valor_detalle}")

        prompt_tpl = spec.get("prompt", "")
        if prompt_tpl:
            prompt_texto = prompt_tpl.format(
                largo=largo,
                ancho=ancho,
                area=area,
            )
            bloque.extend(
                [
                    "",
                    "> **Prompt en Inglés (Optimizado 2D - Fondo Blanco):**",
                    "> ```text",
                    f"> {prompt_texto}",
                    "> ```",
                ]
            )

        bloque.extend(["", "---", ""])
        return bloque

    # PARTE 1
    lineas.append(
        f"# PARTE 1: CAMPAMENTO 1 — PRINCIPAL (PORTAL A / CASMAS — {pob_camp1} PAX)"
    )
    lineas.append("")
    lineas.append("---")
    lineas.append("")
    for ed in camp1_edifs:
        lineas.extend(_render_bloque_edificacion(ed))

    # PARTE 2
    lineas.append(
        f"# PARTE 2: CAMPAMENTO 2 — SATÉLITE AUTÓNOMO (PORTAL B / HUARAZ — {pob_camp2} PAX)"
    )
    lineas.append("")
    lineas.append("---")
    lineas.append("")
    for ed in camp2_edifs:
        lineas.extend(_render_bloque_edificacion(ed))

    # TABLA RESUMEN
    lineas.append("## Resumen Cuantitativo de las 38 Edificaciones")
    lineas.append("")
    lineas.append(
        "| ID | Nombre de la Edificación | Campamento | Grupo Funcional | Largo (m) | Ancho (m) | Área (m²) |"
    )
    lineas.append("|:---|:---|:---:|:---|:---:|:---:|:---:|")

    for ed in edificaciones:
        eid = ed["id"]
        nom = ed.get("nombre", eid)
        camp = ed.get("campamento", "")
        grp = ed.get("grupo", "")
        lg = ed.get("largo_m", 0.0)
        anc = ed.get("ancho_m", 0.0)
        ar = ed.get("area_m2", 0.0)
        lineas.append(
            f"| **{eid}** | {nom} | {camp} | {grp} | {lg:.1f} | {anc:.1f} | {ar:,.1f} |"
        )

    lineas.append(
        f"| **TOTAL** | **{len(edificaciones)} Edificaciones Especializadas** | | | | | **{total_area:,.1f} m²** |"
    )
    lineas.append("")

    archivo_salida.write_text("\n".join(lineas), encoding="utf-8")
    return archivo_salida
