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
from .master_plan import dibujo_master_campamento
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
