"""Generador paramétrico de los 2 archivos AutoLISP (.lsp) para el Campamento 1 y Campamento 2.

Produce exactamente 2 archivos consolidados en ``salidas/lisp/``:
1. ``salidas/lisp/PA14_campamento_1.lsp``:
   - ``PA14_CAMPAMENTO_1``: Dibuja el Master Plan del Campamento 1 Principal + sus 23 plantas detalladas en grilla.
   - ``PA14_MASTER_CAMP1``: Dibuja únicamente el Master Plan General urbanístico del Campamento 1.
   - ``PA14_EDIF_XX``: Comandos individuales para cada edificación del Campamento 1.
2. ``salidas/lisp/PA14_campamento_2.lsp``:
   - ``PA14_CAMPAMENTO_2``: Dibuja el Master Plan del Campamento 2 Satélite + sus 15 plantas detalladas en grilla.
   - ``PA14_MASTER_CAMP2``: Dibuja únicamente el Master Plan General urbanístico del Campamento 2.
   - ``PA14_EDIF_XX``: Comandos individuales para cada edificación del Campamento 2.
"""

from __future__ import annotations

import shutil
import unicodedata
from pathlib import Path

from ..lisp import (
    _LIBRERIA,
    CAPAS,
    Dibujo,
    _n,
    _txt,
)
from .base import (
    LIBRERIA_CAMPAMENTO,
    Lienzo,
    membrete,
)
from .plantas import (
    planta_almacen_central,
    planta_change_house,
    planta_comedor,
    planta_edif_01,
    planta_edif_02,
    planta_edif_03,
    planta_edif_33,
    planta_lavanderia,
    planta_oficinas,
    planta_recreacion_sum,
    planta_taller_mecanico,
    planta_topico_medico,
)
from .procesos import (
    planta_casa_fuerza,
    planta_caseta_polvorin,
    planta_edif_14,
    planta_edif_15,
    planta_edif_16,
    planta_edif_17,
    planta_edif_18,
    planta_edif_19,
    planta_edif_24,
    planta_edif_25,
    planta_edif_26,
    planta_edif_27,
    planta_edif_32,
    planta_edif_36,
    planta_estacion_combustible,
    planta_polvorin_sucamec,
)

ARCHIVO_CAMP1 = "PA14_campamento_1.lsp"
ARCHIVO_CAMP2 = "PA14_campamento_2.lsp"


_PLANTAS_SIMPLES = {
    "EDIF-02": planta_edif_02,
    "EDIF-03": planta_edif_03,
    "EDIF-04": planta_comedor,
    "EDIF-05": planta_comedor,
    "EDIF-08": planta_topico_medico,
    "EDIF-09": planta_topico_medico,
    "EDIF-11": planta_almacen_central,
    "EDIF-12": planta_lavanderia,
    "EDIF-13": planta_recreacion_sum,
    "EDIF-16": planta_edif_16,
    "EDIF-17": planta_edif_17,
    "EDIF-18": planta_edif_18,
    "EDIF-23": planta_polvorin_sucamec,
    "EDIF-28": planta_polvorin_sucamec,
    "EDIF-33": planta_edif_33,
    "EDIF-34": planta_lavanderia,
    "EDIF-35": planta_recreacion_sum,
    "EDIF-37": planta_caseta_polvorin,
    "EDIF-38": planta_caseta_polvorin,
}

_PLANTAS_CON_EQUIPO = {
    "EDIF-10": planta_taller_mecanico,
    "EDIF-14": planta_edif_14,
    "EDIF-15": planta_edif_15,
    "EDIF-19": planta_edif_19,
    "EDIF-20": planta_casa_fuerza,
    "EDIF-21": planta_estacion_combustible,
    "EDIF-22": planta_change_house,
    "EDIF-24": planta_edif_24,
    "EDIF-25": planta_edif_25,
    "EDIF-26": planta_edif_26,
    "EDIF-27": planta_edif_27,
    "EDIF-29": planta_taller_mecanico,
    "EDIF-30": planta_estacion_combustible,
    "EDIF-31": planta_casa_fuerza,
    "EDIF-32": planta_edif_32,
    "EDIF-36": planta_edif_36,
}


def _despachar_planta(
    lz: Lienzo,
    cod_id: str,
    largo: float,
    ancho: float,
    det01: dict,
    eq_edif: dict,
) -> str:
    """Ejecuta el trazado arquitectónico/estructural específico de cada edificación y devuelve su tipología."""
    if cod_id == "EDIF-01":
        return planta_edif_01(lz, largo, ancho, det01)
    if cod_id in ("EDIF-06", "EDIF-07"):
        return planta_oficinas(lz, largo, ancho, es_central=(cod_id == "EDIF-06"))
    if cod_id in _PLANTAS_CON_EQUIPO:
        return _PLANTAS_CON_EQUIPO[cod_id](lz, largo, ancho, eq_edif)
    return _PLANTAS_SIMPLES.get(cod_id, planta_caseta_polvorin)(lz, largo, ancho)


def dibujo_edificacion(
    edif: dict,
    edif01_detalle: dict | None = None,
    equipamiento: dict | None = None,
) -> Dibujo:
    """Genera el objeto Dibujo AutoLISP completo para una edificación específica (EDIF-01 a EDIF-38)."""
    cod_id = edif["id"]
    num_str = cod_id.split("-")[1]
    comando = f"PA14_EDIF_{num_str}"
    largo = float(edif["largo_m"])
    ancho = float(edif["ancho_m"])
    det01 = edif01_detalle or {}
    if cod_id == "EDIF-01" and det01:
        largo = float(det01.get("largo_total_m", largo))
        ancho = float(det01.get("ancho_cuerpo_m", ancho))

    eq_edif = (equipamiento or {}).get(cod_id, {})
    lz = Lienzo()
    tipologia = _despachar_planta(lz, cod_id, largo, ancho, det01, eq_edif)
    membrete(lz, edif, largo, ancho, tipologia)

    return Dibujo(
        comando=comando,
        descripcion=f"{cod_id} - {edif['nombre']} ({edif['campamento']})",
        cuerpo=lz.cmds,
        ancho=max(lz.xmax - lz.xmin, 20.0) + 6.0,
    )


# =============================================================================
# MASTER PLANS DE LOS 2 CAMPAMENTOS (CAMP1 PRINCIPAL Y CAMP2 SATÉLITE)
# =============================================================================


def _huella_master_edif(lz: Lienzo, e: dict, x: float, y: float) -> None:
    """Dibuja la huella urbanística de una instalación en el Master Plan según su tipología real."""
    cid = e["id"]
    w = float(e["largo_m"])
    h = float(e["ancho_m"])

    if cid in ("EDIF-24", "EDIF-25", "EDIF-26", "EDIF-27"):
        # T3: Plataforma vial / parqueo abierto (sin muros de edificio)
        lz.rect(x, y, w, h, "PA14-OBRAS-ARTE")
        lz.lin(x + 0.5, y + h / 2, x + w - 0.5, y + h / 2, "PA14-EJE")
        n_b = max(3, int(w // 3.5))
        wb = (w - 1.0) / n_b
        for i in range(n_b):
            lz.rect(x + 0.5 + i * wb, y + 0.4, wb - 0.2, h * 0.30, "PA14-MOBILIARIO")
            lz.rect(
                x + 0.5 + i * wb,
                y + h * 0.70 - 0.4,
                wb - 0.2,
                h * 0.30,
                "PA14-MOBILIARIO",
            )
    elif cid in (
        "EDIF-14",
        "EDIF-15",
        "EDIF-16",
        "EDIF-17",
        "EDIF-18",
        "EDIF-19",
        "EDIF-21",
        "EDIF-30",
        "EDIF-32",
    ):
        # T4: Planta cercada con malla olímpica y unidades de proceso (tanques/reactores)
        lz.rect(x, y, w, h, "PA14-CERCO")
        if cid in ("EDIF-15", "EDIF-16", "EDIF-32"):
            r_t = min(h * 0.32, 3.2)
            lz.circ(x + w - r_t - 1.2, y + h / 2, r_t, "PA14-APARATOS")
            lz.rect(
                x + 0.8, y + 0.8, max(2.0, w - 2 * r_t - 2.8), h - 1.6, "PA14-APARATOS"
            )
        elif cid in ("EDIF-21", "EDIF-30"):
            lz.rect(x + 0.8, y + h * 0.45, w - 1.6, h * 0.45, "PA14-MUROS")
            lz.rect(x + 1.4, y + h * 0.52, w - 2.8, h * 0.30, "PA14-APARATOS")
        else:
            lz.rect(
                x + 0.6, y + 0.6, max(1.0, w - 1.2), max(1.0, h - 1.2), "PA14-APARATOS"
            )
    elif cid == "EDIF-02":
        # T1 Doble Pabellón Paralelo (Pabellón A y Pabellón B)
        h_ala = (h - 3.2) / 2
        for ya in (y, y + h_ala + 3.2):
            lz.rect(x, ya, w, h_ala, "PA14-EDIFICACION")
            lz.rect(x + 0.20, ya + 0.20, w - 0.40, h_ala - 0.40, "PA14-MUROS")
            lz.lin(x, ya + h_ala / 2, x + w, ya + h_ala / 2, "PA14-ESTRUCTURA")
        lz.rect(x - 0.80, y - 0.80, w + 1.60, h + 1.60, "PA14-OBRAS-ARTE")
    else:
        # T1 / T2: Edificación techada con muros perimetrales, cumbrera y vereda
        lz.rect(x, y, w, h, "PA14-EDIFICACION")
        lz.rect(
            x + 0.20, y + 0.20, max(0.4, w - 0.40), max(0.4, h - 0.40), "PA14-MUROS"
        )
        lz.lin(x, y + h / 2, x + w, y + h / 2, "PA14-ESTRUCTURA")
        lz.rect(x - 0.70, y - 0.70, w + 1.40, h + 1.40, "PA14-OBRAS-ARTE")

    lz.txt(x + w / 2, y + h * 0.62, f"{cid}: {e['nombre']}", h=0.42, w_max=w - 0.6)
    lz.txt(
        x + w / 2,
        y + h * 0.34,
        f"{w:.1f}x{h:.1f}m ({e['area_m2']:.0f} m2)",
        h=0.36,
        w_max=w - 0.6,
    )


def dibujo_master_campamento(
    codigo_camp: str,
    titulo_camp: str,
    edifs_camp: list[dict],
    poblacion_pax: int,
) -> Dibujo:
    """Genera el Master Plan General urbanístico de un Campamento (CAMP1 o CAMP2) con zonificación."""
    num_c = "1" if codigo_camp == "CAMP1" else "2"
    comando = f"PA14_CAMP_{num_c}"

    edifs_polvorin = [
        e for e in edifs_camp if e["id"] in ("EDIF-23", "EDIF-28", "EDIF-37", "EDIF-38")
    ]
    edifs_internas = [e for e in edifs_camp if e not in edifs_polvorin]

    z1 = [
        e
        for e in edifs_internas
        if e["grupo"]
        in (
            "Administración y Documentos",
            "Salud y Bienestar",
            "Vigilancia y Transporte",
        )
        and e["area_m2"] <= 650
    ]
    z2 = [
        e
        for e in edifs_internas
        if e["grupo"] in ("Residencia y Habitabilidad", "Comedor y Alimentación")
    ]
    z3 = [
        e
        for e in edifs_internas
        if e["grupo"]
        in (
            "Maquinaria y Mantenimiento",
            "Almacenes y Logística",
            "Operación y Portales",
        )
        or (e["grupo"] == "Vigilancia y Transporte" and e["area_m2"] > 650)
    ]
    z4 = [e for e in edifs_internas if e not in z1 and e not in z2 and e not in z3]

    zonas = [
        ("ZONA I: CONTROL DE ACCESO, ADMINISTRACION Y SALUD OCUPACIONAL", z1),
        ("ZONA II: RESIDENCIA TERMICA, HABITABILIDAD Y COMEDOR CENTRAL", z2),
        (
            "ZONA III: MAESTRANZA, TALLERES, LOGISTICA, CHANGE-HOUSE Y PATIO DE MANIOBRAS",
            z3,
        ),
        (
            "ZONA IV: ENERGIA, ESTACION DE DIESEL (RET. 15m), PTAP/PTAR Y GESTION AMBIENTAL",
            z4,
        ),
    ]

    lz = Lienzo()
    margen_x = 14.0
    sep_x = 8.5
    via_ancho = 8.0
    y_cursor = 14.0
    max_x_usado = 125.0

    for nom_zona, lista_z in zonas:
        if not lista_z:
            continue
        y_via = y_cursor - via_ancho / 2
        x_cursor = margen_x
        alto_fila = max(float(e["ancho_m"]) for e in lista_z)
        for e in lista_z:
            _huella_master_edif(lz, e, x_cursor, y_cursor)
            x_cursor += float(e["largo_m"]) + sep_x
        max_x_usado = max(max_x_usado, x_cursor + margen_x)
        # Vía afirmada transversal con eje y flechas de sentido
        lz.lin(margen_x - 4.0, y_via, max_x_usado - 8.0, y_via, "PA14-EJE")
        lz.flecha(margen_x + 2.0, y_via + 1.2, 5.0, 0, "PA14-EJE")
        lz.txt_izq(
            margen_x,
            y_via - 1.2,
            f"=== {nom_zona} (VIA INTERNA AFIRMADA A = 6.00 m + CUNETAS PLUVIALES) ===",
            h=0.60,
        )
        y_cursor += alto_fila + 18.0

    ancho_camp = max_x_usado
    alto_camp = y_cursor + 6.0

    # Avenida troncal Norte-Sur y Cerco Perimétrico General con Rosa Náutica
    lz.rect(0.0, 0.0, ancho_camp, alto_camp, "PA14-CERCO")
    lz.rect(-1.50, -1.50, ancho_camp + 3.00, alto_camp + 3.00, "PA14-OBRAS-ARTE")
    lz.lin(margen_x - 4.0, 0.0, margen_x - 4.0, alto_camp, "PA14-EJE")
    lz.flecha(margen_x - 4.0, 4.0, 8.0, 90, "PA14-EJE")
    lz.circ(ancho_camp - 8.0, alto_camp - 8.0, 3.0, "PA14-SIMBOLOS")
    lz.flecha(ancho_camp - 8.0, alto_camp - 10.5, 5.0, 90, "PA14-SIMBOLOS")
    lz.txt(ancho_camp - 8.0, alto_camp - 4.0, "N", h=0.80)

    lz.cota(
        0.0,
        0.0,
        ancho_camp,
        0.0,
        ancho_camp / 2,
        -5.0,
        f"{ancho_camp:.1f} m (FRENTE CAMPAMENTO {codigo_camp})",
    )
    lz.cota(
        0.0,
        0.0,
        0.0,
        alto_camp,
        -6.0,
        alto_camp / 2,
        f"{alto_camp:.1f} m (FONDO CAMPAMENTO {codigo_camp})",
    )

    # Complejo Externo Aislado de Explosivos SUCAMEC (Retiro normativo >= 300 m)
    if edifs_polvorin:
        x_polv = ancho_camp + 26.0
        w_box = 52.0
        h_box = 36.0
        lz.rect(x_polv, 10.0, w_box, h_box, "PA14-CERCO")
        lz.lin(ancho_camp, 28.0, x_polv, 28.0, "PA14-EJE")
        lz.cota(
            ancho_camp,
            28.0,
            x_polv,
            28.0,
            (ancho_camp + x_polv) / 2,
            31.5,
            "RETIRO >= 300 m (SUCAMEC LEY 30299)",
        )
        lz.txt(
            x_polv + w_box / 2,
            10.0 + h_box - 2.8,
            f"COMPLEJO AISLADO DE EXPLOSIVOS Y CUSTODIA ARMADA ({codigo_camp})",
            h=0.60,
            w_max=w_box - 4.0,
        )
        xp_i = x_polv + 5.0
        for ep in edifs_polvorin:
            wp = float(ep["largo_m"])
            hp = float(ep["ancho_m"])
            lz.rect(xp_i, 16.0, wp, hp, "PA14-EDIFICACION")
            lz.rect(xp_i - 1.5, 16.0 - 1.5, wp + 3.0, hp + 3.0, "PA14-OBRAS-ARTE")
            lz.txt(
                xp_i + wp / 2,
                16.0 + hp / 2,
                f"{ep['id']}: {ep['nombre']}",
                h=0.38,
                w_max=max(wp + 2.0, 8.0),
            )
            xp_i += wp + 9.0
        ancho_camp_total = x_polv + w_box + 10.0
    else:
        ancho_camp_total = ancho_camp + 10.0

    # Membrete General del Master Plan del Campamento
    area_tot_edif = sum(e["area_m2"] for e in edifs_camp)
    lz.rect(0.0, -18.5, ancho_camp, 10.5, "PA14-MEMBRETE")
    lz.txt_izq(
        3.0,
        -10.8,
        f"MASTER PLAN ARQUITECTONICO Y VIAL: {titulo_camp.upper()} ({codigo_camp})",
        h=1.05,
    )
    lz.txt_izq(
        3.0,
        -13.4,
        f"POBLACION DE DISENO: {poblacion_pax} TRABAJADORES | TOTAL INSTALACIONES: {len(edifs_camp)} | AREA CONSTRUIDA: {area_tot_edif:,.1f} m2",
        h=0.72,
    )
    lz.txt_izq(
        3.0,
        -15.9,
        "NORMATIVA: RNE G.050, A.010, A.060, A.070, A.080, OS.020, OS.090 / D.S. 024-2016-EM / D.S. 052-93-EM / LEY 30299 SUCAMEC (3,850 msnm)",
        h=0.62,
    )

    return Dibujo(
        comando=comando,
        descripcion=f"Master Plan General {codigo_camp} - {titulo_camp}",
        cuerpo=lz.cmds,
        ancho=ancho_camp_total,
    )


# =============================================================================
# ESCRITURA DE ARCHIVOS .LSP (2 ARCHIVOS CONSOLIDADOS CON GRILLA DINÁMICA)
# =============================================================================


def _serializar_archivo_campamento(
    cmd_maestro: str,
    titulo_camp: str,
    dibujo_master: Dibujo,
    dibujos_edifs: list[Dibujo],
    proyecto: str,
    cols_grilla: int = 5,
) -> str:
    """Genera un único archivo .lsp consolidado para un Campamento (Master Plan + sus edificaciones)."""
    cods_lista = ", ".join(d.comando for d in dibujos_edifs)
    lineas = [
        f";;; {_txt(proyecto)[1:-1]} - {_txt(titulo_camp)[1:-1]}",
        ";;; Generado dinamicamente con `uv run pa14` desde datos/parametros.toml.",
        f";;; APPLOAD -> cargar este archivo -> escribir comando principal: {cmd_maestro}",
        ";;; Comandos disponibles en este archivo:",
        f";;;   - {cmd_maestro:<19} : Dibuja el Master Plan + todas las {len(dibujos_edifs)} plantas detalladas en grilla",
        f";;;   - {dibujo_master.comando:<19} : Dibuja solo el Master Plan General urbanistico",
        f";;;   - Individuales        : {cods_lista}",
        _LIBRERIA,
        LIBRERIA_CAMPAMENTO,
        "(defun pa14:capas ()",
        *[f'  (pa14:capa "{n}" {c})' for n, c in CAPAS.items()],
        ")",
    ]

    todo_cmd = [
        f"\n(defun c:{cmd_maestro} (/ pt bx by)",
        "  (pa14:inicio)",
        f'  (setq pt (getpoint "\\nPrecise punto de insercion para {cmd_maestro} [Clic en pantalla o ENTER para 0,0]: "))',
        "  (if pt (setq bx (car pt) by (cadr pt)) (setq bx 0.0 by 0.0))",
    ]

    # Calcular espaciado dinámico de columnas y filas para que ninguna lámina se solape
    paso_col_x = max(72.0, max((d.ancho for d in dibujos_edifs), default=60.0) + 10.0)
    paso_fila_y = -52.0
    posiciones: list[tuple[Dibujo, float, float]] = [(dibujo_master, 0.0, 210.0)]

    for idx, d_ed in enumerate(dibujos_edifs):
        col = idx % cols_grilla
        row = idx // cols_grilla
        ox = col * paso_col_x
        oy = 135.0 + row * paso_fila_y
        posiciones.append((d_ed, ox, oy))

    for d, ox, oy in posiciones:
        fn_name = d.comando.lower().replace("pa14_", "pa14:d-")
        lineas += [f"\n;;; {_txt(d.descripcion)[1:-1]}", f"(defun {fn_name} ()"]
        lineas += [f"  {c}" for c in d.cuerpo]
        lineas += [
            ")",
            f'(defun c:{d.comando} () (pa14:inicio) (pa14:pedir-origen "Precise punto de insercion para {d.comando}") ({fn_name}) (pa14:fin))',
        ]
        todo_cmd += [
            f"  (pa14:origen (+ bx {_n(ox)}) (+ by {_n(oy)}))",
            f"  ({fn_name})",
        ]

    todo_cmd += [
        "  (pa14:fin))",
        f'(princ "\\n{cmd_maestro} cargado: Escriba {cmd_maestro} para dibujar todo el campamento y sus {len(dibujos_edifs)} edificaciones.")',
        "(princ)\n",
    ]

    contenido = "\n".join(lineas + todo_cmd)
    return (
        unicodedata.normalize("NFKD", contenido)
        .encode("ascii", "ignore")
        .decode("ascii")
    )


def generar_lisp_campamento(ctx: dict, carpeta: Path, proyecto: str) -> list[Path]:
    """Genera exactamente los 2 archivos consolidados: PA14_campamento_1.lsp y PA14_campamento_2.lsp."""
    camp = ctx["campamento"]
    per = ctx["personal"]
    edifs = camp["edificaciones"]
    det01 = camp.get("edif01_detalle", {})
    equip = camp.get("equipamiento", {})

    edifs_c1 = [e for e in edifs if e["campamento"] == "CAMP1"]
    edifs_c2 = [e for e in edifs if e["campamento"] == "CAMP2"]

    dibujos_c1 = [dibujo_edificacion(e, det01, equip) for e in edifs_c1]
    dibujos_c2 = [dibujo_edificacion(e, det01, equip) for e in edifs_c2]

    master_c1 = dibujo_master_campamento(
        "CAMP1",
        "Campamento 1 Principal - Portal Entrada (Portal A)",
        edifs_c1,
        per.get("camp1_total", 248),
    )
    master_c1.comando = "PA14_MASTER_CAMP1"

    master_c2 = dibujo_master_campamento(
        "CAMP2",
        "Campamento 2 Satelite - Portal Salida (Portal B)",
        edifs_c2,
        per.get("camp2_total", 98),
    )
    master_c2.comando = "PA14_MASTER_CAMP2"

    carpeta.mkdir(parents=True, exist_ok=True)

    # Limpiar archivos antiguos o subcarpetas sueltas si existían
    sub_edif = carpeta / "edificaciones"
    if sub_edif.exists():
        shutil.rmtree(sub_edif, ignore_errors=True)
    for ant in ("PA14_campamento_edificaciones.lsp", "PA14_dormitorio_personal.lsp"):
        ruta_ant = carpeta / ant
        if ruta_ant.exists():
            ruta_ant.unlink()

    ruta_c1 = carpeta / ARCHIVO_CAMP1
    ruta_c1.write_text(
        _serializar_archivo_campamento(
            "PA14_CAMPAMENTO_1",
            "CAMPAMENTO 1 PRINCIPAL (PORTAL ENTRADA - 248 PAX) + EDIFICACIONES",
            master_c1,
            dibujos_c1,
            proyecto,
            cols_grilla=5,
        ),
        encoding="ascii",
    )

    ruta_c2 = carpeta / ARCHIVO_CAMP2
    ruta_c2.write_text(
        _serializar_archivo_campamento(
            "PA14_CAMPAMENTO_2",
            "CAMPAMENTO 2 SATELITE (PORTAL SALIDA - 98 PAX) + EDIFICACIONES",
            master_c2,
            dibujos_c2,
            proyecto,
            cols_grilla=5,
        ),
        encoding="ascii",
    )

    return [ruta_c1, ruta_c2]
