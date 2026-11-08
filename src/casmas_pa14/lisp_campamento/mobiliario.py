"""Bloques de mobiliario, aparatos sanitarios, ejes, columnas y membrete CAD."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .base import Lienzo


def ejes(
    lz: Lienzo, xs: list[float], ys: list[float], largo: float, ancho: float
) -> None:
    """Ejes estructurales numerados (X) y literales (Y) con cadena de cotas parciales."""
    r = 0.32 if min(largo, ancho) >= 6 else 0.24
    hb = r * 0.85
    for i, x in enumerate(xs):
        lz.lin(x, ancho + 0.25, x, ancho + 1.55, "PA14-EJE")
        lz.circ(x, ancho + 1.55 + r, r, "PA14-EJE")
        lz.txt(x, ancho + 1.55 + r, str(i + 1), h=hb)
    for a, b in zip(xs, xs[1:], strict=False):
        if b - a > 0.6:
            lz.cota(a, ancho, b, ancho, (a + b) / 2, ancho + 0.95)
    letras = "ABCDEFGHJKLMNPQRSTUVWXYZ"
    for j, y in enumerate(ys):
        lz.lin(-0.25, y, -1.55, y, "PA14-EJE")
        lz.circ(-1.55 - r, y, r, "PA14-EJE")
        lz.txt(-1.55 - r, y, letras[j % len(letras)], h=hb)
    for a, b in zip(ys, ys[1:], strict=False):
        if b - a > 0.6:
            lz.cota(0.0, a, 0.0, b, -0.95, (a + b) / 2)


def columnas(
    lz: Lienzo,
    xs: list[float],
    ys: list[float],
    tipo: str = "panel",
    interiores: bool = False,
) -> None:
    """Columnas en intersecciones de ejes: 'panel' (tubo 0.15) o 'H' (perfil W 0.30)."""
    x_ext, y_ext = (xs[0], xs[-1]), (ys[0], ys[-1])
    for x in xs:
        for y in ys:
            if not interiores and x not in x_ext and y not in y_ext:
                continue
            if tipo == "H":
                d, tf = 0.30, 0.04
                lz.rect(x - d / 2, y - d / 2, d, tf, "PA14-ESTRUCTURA")
                lz.rect(x - d / 2, y + d / 2 - tf, d, tf, "PA14-ESTRUCTURA")
                lz.rect(x - 0.015, y - d / 2 + tf, 0.03, d - 2 * tf, "PA14-ESTRUCTURA")
            else:
                d = 0.15
                lz.rect(x - d / 2, y - d / 2, d, d, "PA14-ESTRUCTURA")
                lz.lin(x - d / 2, y - d / 2, x + d / 2, y + d / 2, "PA14-ESTRUCTURA")


def cotas_totales(lz: Lienzo, largo: float, ancho: float, sep: float = 2.6) -> None:
    """Cotas generales de largo y ancho por debajo y a la izquierda del perímetro."""
    lz.cota(0.0, 0.0, largo, 0.0, largo / 2, -sep, f"{largo:.2f}")
    lz.cota(0.0, 0.0, 0.0, ancho, -sep - 0.9, ancho / 2, f"{ancho:.2f}")


def membrete(
    lz: Lienzo, edif: dict, largo: float, ancho: float, tipologia: str
) -> None:
    """Rótulo normalizado bajo la caja envolvente del dibujo."""
    wm = max(lz.xmax - lz.xmin, 20.0)
    x0 = lz.xmin
    hm = 3.4
    y0 = lz.ymin - 1.2 - hm
    lz.rect(x0, y0, wm, hm, "PA14-MEMBRETE")
    xa, xb = x0 + wm * 0.60, x0 + wm * 0.82
    lz.lin(xa, y0, xa, y0 + hm, "PA14-MEMBRETE")
    lz.lin(xb, y0, xb, y0 + hm, "PA14-MEMBRETE")
    wa, wb, wc = wm * 0.58, wm * 0.20, wm * 0.16
    filas_a = [
        (f"PROYECTO: TUNEL CASMAS HUARAZ PA14 - {edif['campamento']}", 0.24),
        (f"{edif['id']}: {edif['nombre'].upper()}", 0.26),
        (f"TIPOLOGIA: {tipologia}", 0.17),
        (f"NORMA: {edif['norma']}", 0.15),
    ]
    filas_b = [
        (f"AREA: {edif['area_m2']:.1f} m2", 0.18),
        (f"DIM: {largo:.2f} x {ancho:.2f} m", 0.17),
        (f"GRUPO: {edif['grupo'].upper()}", 0.14),
        ("ALTITUD: 3,850 msnm", 0.15),
    ]
    filas_c = [
        (f"PLANO: {edif['id']}", 0.22),
        ("ESC: 1:100", 0.18),
        ("UNID: METROS", 0.17),
    ]
    for i, (t, h) in enumerate(filas_a):
        lz.txt(x0 + wm * 0.30, y0 + hm - 0.55 - i * 0.75, t, h=h, w_max=wa)
    for i, (t, h) in enumerate(filas_b):
        lz.txt((xa + xb) / 2, y0 + hm - 0.55 - i * 0.75, t, h=h, w_max=wb)
    for i, (t, h) in enumerate(filas_c):
        lz.txt((xb + x0 + wm) / 2, y0 + hm - 0.70 - i * 0.85, t, h=h, w_max=wc)


def cama(
    lz: Lienzo,
    x: float,
    y: float,
    rot: int = 0,
    w: float = 0.90,
    l_c: float = 1.90,
    litera: bool = False,
) -> None:
    """Cama (o camarote) w x l con almohada en la cabecera (v = l)."""
    with lz.caja(x, y, w, l_c, rot):
        lz.rect(0, 0, w, l_c, "PA14-MOBILIARIO")
        lz.rect(0.08, l_c - 0.42, w - 0.16, 0.32, "PA14-MOBILIARIO")
        lz.lin(0, l_c * 0.55, w, l_c * 0.55, "PA14-MOBILIARIO")
        if litera:
            lz.lin(0, 0, w, l_c - 0.5, "PA14-MOBILIARIO")
            lz.lin(w, 0, 0, l_c - 0.5, "PA14-MOBILIARIO")


def inodoro(lz: Lienzo, x: float, y: float, rot: int = 0) -> None:
    """Inodoro 0.40 x 0.65 con tanque contra el muro (v = 0)."""
    with lz.caja(x, y, 0.40, 0.65, rot):
        lz.rect(0, 0, 0.40, 0.18, "PA14-APARATOS")
        lz.circ(0.20, 0.42, 0.19, "PA14-APARATOS")


def lavatorio(lz: Lienzo, x: float, y: float, rot: int = 0) -> None:
    """Lavatorio 0.50 x 0.42 adosado al muro (v = 0)."""
    with lz.caja(x, y, 0.50, 0.42, rot):
        lz.rect(0, 0, 0.50, 0.42, "PA14-APARATOS")
        lz.circ(0.25, 0.24, 0.13, "PA14-APARATOS")
        lz.lin(0.25, 0.04, 0.25, 0.12, "PA14-APARATOS")


def urinario(lz: Lienzo, x: float, y: float, rot: int = 0) -> None:
    """Urinario mural 0.40 x 0.35."""
    with lz.caja(x, y, 0.40, 0.35, rot):
        lz.rect(0, 0, 0.40, 0.10, "PA14-APARATOS")
        lz.arco(0.20, 0.10, 0.20, 0.0, 180.0, "PA14-APARATOS")


def ducha(lz: Lienzo, x: float, y: float, s: float = 0.90, rot: int = 0) -> None:
    """Plato de ducha s x s con sumidero central y diagonales de pendiente."""
    with lz.caja(x, y, s, s, rot):
        lz.rect(0, 0, s, s, "PA14-APARATOS")
        lz.lin(0, 0, s, s, "PA14-APARATOS")
        lz.lin(0, s, s, 0, "PA14-APARATOS")
        lz.circ(s / 2, s / 2, 0.05, "PA14-APARATOS")


def lockers(
    lz: Lienzo,
    x: float,
    y: float,
    n: int,
    rot: int = 0,
    w: float = 0.40,
    d: float = 0.50,
) -> None:
    """Fila de n casilleros metálicos w x d con línea de puerta."""
    with lz.caja(x, y, n * w, d, rot):
        for i in range(n):
            lz.rect(i * w, 0, w, d, "PA14-MOBILIARIO")
            lz.lin(i * w, d - 0.06, (i + 1) * w, d - 0.06, "PA14-MOBILIARIO")


def escritorio(
    lz: Lienzo, x: float, y: float, w: float = 1.40, d: float = 0.70, rot: int = 0
) -> None:
    """Escritorio contra muro (v=0) con silla giratoria al frente."""
    with lz.caja(x, y, w, d + 0.65, rot):
        lz.rect(0, 0, w, d, "PA14-MOBILIARIO")
        lz.rect(w * 0.25, 0.05, w * 0.5, 0.06, "PA14-MOBILIARIO")
        lz.circ(w / 2, d + 0.33, 0.24, "PA14-MOBILIARIO")


def mesa_sillas(
    lz: Lienzo,
    x: float,
    y: float,
    w: float,
    d: float,
    por_lado: int,
    cabeceras: bool = False,
) -> None:
    """Mesa rectangular w x d con sillas 0.42 en los lados largos (y cabeceras)."""
    lz.rect(x, y, w, d, "PA14-MOBILIARIO")
    paso = w / por_lado
    for i in range(por_lado):
        cx = x + paso * (i + 0.5)
        lz.rect(cx - 0.21, y - 0.50, 0.42, 0.42, "PA14-MOBILIARIO")
        lz.rect(cx - 0.21, y + d + 0.08, 0.42, 0.42, "PA14-MOBILIARIO")
    if cabeceras:
        lz.rect(x - 0.50, y + d / 2 - 0.21, 0.42, 0.42, "PA14-MOBILIARIO")
        lz.rect(x + w + 0.08, y + d / 2 - 0.21, 0.42, 0.42, "PA14-MOBILIARIO")


def estante(lz: Lienzo, x: float, y: float, w: float, d: float, n_div: int = 0) -> None:
    """Estantería/rack w x d con divisiones de módulo y diagonal de identificación."""
    lz.rect(x, y, w, d, "PA14-MOBILIARIO")
    lz.lin(x, y, x + w, y + d, "PA14-MOBILIARIO")
    if n_div > 1:
        if w >= d:
            for i in range(1, n_div):
                lz.lin(
                    x + w * i / n_div, y, x + w * i / n_div, y + d, "PA14-MOBILIARIO"
                )
        else:
            for i in range(1, n_div):
                lz.lin(
                    x, y + d * i / n_div, x + w, y + d * i / n_div, "PA14-MOBILIARIO"
                )


def vehiculo(
    lz: Lienzo, x: float, y: float, w: float, l_v: float, etiqueta: str, rot: int = 0
) -> None:
    """Silueta de vehículo en planta (frente en v = l) con cabina, ruedas y rótulo."""
    with lz.caja(x, y, w, l_v, rot):
        lz.pline(
            [
                (0.1, 0),
                (w - 0.1, 0),
                (w, 0.1),
                (w, l_v - 0.3),
                (w - 0.3, l_v),
                (0.3, l_v),
                (0, l_v - 0.3),
                (0, 0.1),
            ],
            True,
            "PA14-MOBILIARIO",
        )
        cab = min(2.2, l_v * 0.28)
        lz.lin(0, l_v - cab, w, l_v - cab, "PA14-MOBILIARIO")
        lz.lin(0.25, l_v - cab * 0.35, w - 0.25, l_v - cab * 0.35, "PA14-MOBILIARIO")
        rw, rl = 0.22, min(0.9, l_v * 0.12)
        for vr in (l_v * 0.12, l_v - cab * 0.6 - rl / 2):
            lz.rect(-rw * 0.5, vr, rw, rl, "PA14-MOBILIARIO")
            lz.rect(w - rw * 0.5, vr, rw, rl, "PA14-MOBILIARIO")
        lz.txt(
            w / 2, (l_v - cab) / 2, etiqueta, h=0.30, w_max=(l_v - cab) * 0.9, ang=90
        )


def tanque_vertical(
    lz: Lienzo, x: float, y: float, r: float, etiqueta: str, e_muro: float = 0.0
) -> None:
    """Tanque/reservorio circular (con muro de espesor e) y escalera marinera."""
    lz.circ(x, y, r, "PA14-APARATOS")
    if e_muro > 0:
        lz.circ(x, y, r - e_muro, "PA14-APARATOS")
    lz.circ(x, y, max(0.3, r * 0.12), "PA14-APARATOS")
    lz.rect(x + r - 0.05, y - 0.25, 0.45, 0.50, "PA14-ESCALERAS")
    lz.txt(x, y - r * 0.5, etiqueta, h=0.22, w_max=r * 1.6)


def grupo_electrogeno(
    lz: Lienzo, x: float, y: float, w: float, l_g: float, etiqueta: str, rot: int = 0
) -> None:
    """Grupo electrógeno sobre bancada antivibratoria con radiador en v = l."""
    with lz.caja(x, y, w + 0.6, l_g + 0.6, rot):
        lz.rect(0, 0, w + 0.6, l_g + 0.6, "PA14-ESTRUCTURA")
        lz.rect(0.3, 0.3, w, l_g, "PA14-APARATOS")
        lz.rect(0.3, 0.3 + l_g * 0.78, w, l_g * 0.22, "PA14-APARATOS")
        for i in range(1, 6):
            yy = 0.3 + l_g * 0.78 + l_g * 0.22 * i / 6
            lz.lin(0.3, yy, 0.3 + w, yy, "PA14-APARATOS")
        lz.circ(0.3 + w / 2, 0.3 + l_g * 0.15, min(0.3, w * 0.15), "PA14-APARATOS")
        lz.txt(0.3 + w / 2, 0.3 + l_g * 0.45, etiqueta, h=0.22, w_max=l_g * 0.6, ang=90)


def escalera(
    lz: Lienzo, x: float, y: float, w: float, l_e: float, paso: float = 0.28
) -> None:
    """Escalera de dos tramos con descanso, huellas y flecha de subida."""
    tramo = (w - 0.10) / 2
    lz.rect(x, y, w, l_e, "PA14-ESCALERAS")
    lz.rect(x + tramo, y, 0.10, l_e - 1.2, "PA14-ESCALERAS")
    n = int((l_e - 1.2) / paso)
    for i in range(1, n + 1):
        yy = y + i * paso
        lz.lin(x, yy, x + tramo, yy, "PA14-ESCALERAS")
        lz.lin(x + tramo + 0.10, yy, x + w, yy, "PA14-ESCALERAS")
    lz.lin(x, y + l_e - 1.2, x + w, y + l_e - 1.2, "PA14-ESCALERAS")
    lz.flecha(x + tramo / 2, y + 0.3, l_e - 1.8, 90, "PA14-ESCALERAS")
    lz.txt(x + w / 2, y + l_e - 0.6, "DESCANSO", h=0.14, w_max=w * 0.8)
