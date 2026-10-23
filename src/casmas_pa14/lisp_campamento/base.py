"""Primitivas CAD de alto nivel para los planos de arquitectura del campamento.

Solo presentación (sin cálculos de ingeniería): un ``Lienzo`` con transformaciones
locales (traslación + giro ortogonal), muros con vanos reales (puertas, ventanas,
portones), tabiques, achurados, ejes estructurales, membrete y bloques de
mobiliario/equipos dibujados a escala real en metros.
"""

from __future__ import annotations

import math
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass

from ..lisp import _n, _txt

CAPA_TXT = "PA14-TEXTO"
# Relación ancho/alto media de un carácter en la fuente txt.shx (solo presentación)
ANCHO_CARACTER = 0.92
H_TXT_MIN = 0.07

# Función adicional de la librería: texto centrado con rotación (grupo 50)
LIBRERIA_CAMPAMENTO = r"""
(defun pa14:texto-rot (x y alt ang txt capa)
  (entmake (list '(0 . "TEXT") (cons 8 capa) (cons 10 (pa14:p x y)) (cons 11 (pa14:p x y))
                 (cons 40 alt) (cons 1 txt) (cons 50 (/ (* ang 3.141592653589793) 180.0))
                 '(72 . 1) '(73 . 2))))
"""


@dataclass
class Vano:
    """Abertura en un muro.

    ``centro`` se mide en coordenada global (X en muros horizontales, Y en verticales).
    ``tipo``: P (puerta), P2 (puerta doble), V (ventana), PO (portón seccional),
    PC (portón corredizo), A (acceso libre), VE (ventanilla de atención).
    ``hacia``: en cerramientos "in"/"out"; en tabiques "+"/"-" (lado de mayor/menor
    coordenada perpendicular).
    """

    centro: float
    ancho: float
    tipo: str = "P"
    bisagra: str = "izq"
    hacia: str = "in"
    etiqueta: str = ""


class Lienzo:
    """Acumulador de entidades AutoLISP con transformaciones locales y caja envolvente."""

    def __init__(self, h_txt: float = 0.18) -> None:
        self.cmds: list[str] = []
        self.h_txt = h_txt
        self._tf: list[tuple[float, float, int]] = [(0.0, 0.0, 0)]
        self.xmin = self.ymin = math.inf
        self.xmax = self.ymax = -math.inf

    # ------------------------------------------------------------ transformación
    def _t(self, u: float, v: float) -> tuple[float, float]:
        x0, y0, r = self._tf[-1]
        if r == 0:
            x, y = u, v
        elif r == 90:
            x, y = -v, u
        elif r == 180:
            x, y = -u, -v
        else:
            x, y = v, -u
        return x0 + x, y0 + y

    def _p(self, u: float, v: float) -> tuple[float, float]:
        x, y = self._t(u, v)
        self.xmin, self.xmax = min(self.xmin, x), max(self.xmax, x)
        self.ymin, self.ymax = min(self.ymin, y), max(self.ymax, y)
        return x, y

    @property
    def giro(self) -> int:
        """Giro acumulado del sistema local (0, 90, 180 o 270 grados)."""
        return self._tf[-1][2]

    @contextmanager
    def local(self, u: float, v: float, rot: int = 0) -> Iterator[None]:
        """Sistema local con origen en (u, v) y giro ortogonal antihorario ``rot``."""
        x, y = self._t(u, v)
        self._tf.append((x, y, (self.giro + rot) % 360))
        try:
            yield
        finally:
            self._tf.pop()

    @contextmanager
    def caja(
        self, x: float, y: float, w: float, h: float, rot: int = 0
    ) -> Iterator[None]:
        """Coloca un bloque canónico w x h girado ``rot`` con su esquina inf-izq en (x, y)."""
        rot %= 360
        ox, oy = {0: (x, y), 90: (x + h, y), 180: (x + w, y + h), 270: (x, y + w)}[rot]
        with self.local(ox, oy, rot):
            yield

    # ---------------------------------------------------------------- primitivas
    def lin(self, u1: float, v1: float, u2: float, v2: float, capa: str) -> None:
        """Línea simple."""
        x1, y1 = self._p(u1, v1)
        x2, y2 = self._p(u2, v2)
        self.cmds.append(f'(pa14:linea {_n(x1)} {_n(y1)} {_n(x2)} {_n(y2)} "{capa}")')

    def rect(self, u: float, v: float, w: float, h: float, capa: str) -> None:
        """Rectángulo cerrado (LWPOLYLINE)."""
        if w <= 0 or h <= 0:
            return
        x1, y1 = self._p(u, v)
        x2, y2 = self._p(u + w, v + h)
        xa, ya = min(x1, x2), min(y1, y2)
        self.cmds.append(
            f'(pa14:rect {_n(xa)} {_n(ya)} {_n(abs(x2 - x1))} {_n(abs(y2 - y1))} "{capa}")'
        )

    def circ(self, u: float, v: float, r: float, capa: str) -> None:
        """Círculo."""
        x, y = self._p(u, v)
        self._p(u - r, v - r)
        self._p(u + r, v + r)
        self.cmds.append(f'(pa14:circulo {_n(x)} {_n(y)} {_n(r)} "{capa}")')

    def arco(
        self, u: float, v: float, r: float, a1: float, a2: float, capa: str
    ) -> None:
        """Arco antihorario de a1 a a2 (grados, sistema local)."""
        x, y = self._p(u, v)
        g = self.giro
        self.cmds.append(
            f"(pa14:arco {_n(x)} {_n(y)} {_n(r)} {_n((a1 + g) % 360)} "
            f'{_n((a2 + g) % 360)} "{capa}")'
        )

    def pline(self, pts: list[tuple[float, float]], cerrado: bool, capa: str) -> None:
        """Polilínea de segmentos rectos."""
        glob = [self._p(u, v) for u, v in pts]
        lp = " ".join(f"({_n(x)} {_n(y)})" for x, y in glob)
        bl = " ".join("0.0" for _ in glob)
        cer = "T" if cerrado else "nil"
        self.cmds.append(f"(pa14:pline '({lp}) '({bl}) {cer} \"{capa}\")")

    def txt(
        self,
        u: float,
        v: float,
        texto: str,
        h: float | None = None,
        w_max: float | None = None,
        ang: float = 0.0,
        capa: str = CAPA_TXT,
    ) -> None:
        """Texto centrado, auto-ajustado a ``w_max`` y siempre legible (no invertido)."""
        alt = self.h_txt if h is None else h
        if w_max is not None and texto:
            alt = min(alt, w_max / (len(texto) * ANCHO_CARACTER))
        alt = max(H_TXT_MIN, alt)
        x, y = self._p(u, v)
        a = (ang + self.giro) % 360
        if 90 < a <= 270:
            a = (a + 180) % 360
        if a == 0:
            self.cmds.append(
                f'(pa14:texto-cen {_n(x)} {_n(y)} {_n(alt)} {_txt(texto)} "{capa}")'
            )
        else:
            self.cmds.append(
                f'(pa14:texto-rot {_n(x)} {_n(y)} {_n(alt)} {_n(a)} {_txt(texto)} "{capa}")'
            )

    def txt_izq(self, u: float, v: float, texto: str, h: float | None = None) -> None:
        """Texto justificado a la izquierda (sin giro)."""
        alt = self.h_txt if h is None else h
        x, y = self._p(u, v)
        self._p(u + len(texto) * alt * ANCHO_CARACTER, v + alt)
        self.cmds.append(
            f'(pa14:texto {_n(x)} {_n(y)} {_n(alt)} {_txt(texto)} "{CAPA_TXT}")'
        )

    def cota(
        self,
        u1: float,
        v1: float,
        u2: float,
        v2: float,
        u3: float,
        v3: float,
        t: str = "",
    ) -> None:
        """Cota lineal (DIMLINEAR) en capa PA14-COTA."""
        pts = [self._p(u1, v1), self._p(u2, v2), self._p(u3, v3)]
        nums = " ".join(f"{_n(x)} {_n(y)}" for x, y in pts)
        tl = _txt(t) if t else '""'
        self.cmds.append(f"(pa14:cota {nums} {tl})")

    def achurado(
        self,
        u: float,
        v: float,
        w: float,
        h: float,
        paso: float,
        capa: str = "PA14-HATCH",
    ) -> None:
        """Rayado a 45 grados recortado al rectángulo (u, v, w, h)."""
        if w <= 0 or h <= 0 or paso <= 0:
            return
        c = -w + paso / 2
        while c < h:
            pts = []
            for px, py in ((0.0, c), (w, w + c), (-c, 0.0), (h - c, h)):
                if -1e-9 <= px <= w + 1e-9 and -1e-9 <= py <= h + 1e-9:
                    pts.append((px, py))
            pts = sorted(set((round(a, 6), round(b, 6)) for a, b in pts))
            if len(pts) >= 2:
                (a1, b1), (a2, b2) = pts[0], pts[-1]
                self.lin(u + a1, v + b1, u + a2, v + b2, capa)
            c += paso

    def puntos(
        self, u: float, v: float, w: float, h: float, paso: float, capa: str
    ) -> None:
        """Trama de puntos (círculos r=0.04) para gravas, rellenos o biomedios."""
        ny, nx = max(1, int(h / paso)), max(1, int(w / paso))
        for i in range(nx):
            for j in range(ny):
                desf = paso / 2 if j % 2 else 0.0
                uu = u + paso / 2 + i * paso + desf
                if uu < u + w:
                    self.circ(uu, v + paso / 2 + j * paso, 0.04, capa)

    def flecha(
        self, u: float, v: float, largo: float, rot: int = 0, capa: str = "PA14-EJE"
    ) -> None:
        """Flecha de sentido de circulación (cuerpo + punta) en dirección ``rot``."""
        with self.local(u, v, rot):
            p = min(0.9, largo * 0.3)
            self.lin(0, 0, largo, 0, capa)
            self.pline(
                [(largo - p, p * 0.45), (largo, 0), (largo - p, -p * 0.45)], True, capa
            )


# ============================================================================ muros
def _segmentos(
    ini: float, fin: float, huecos: list[tuple[float, float]]
) -> list[tuple[float, float]]:
    """Tramos macizos de [ini, fin] descontando los huecos."""
    segs, cur = [], ini
    for a, b in sorted(huecos):
        if a > cur:
            segs.append((cur, min(a, fin)))
        cur = max(cur, b)
    if cur < fin:
        segs.append((cur, fin))
    return [(a, b) for a, b in segs if b - a > 1e-6]


def _puerta(
    lz: Lienzo, a: float, b: float, v_in: float, v_out: float, vano: Vano, adentro: bool
) -> None:
    """Hoja(s) y arco(s) de barrido de una puerta batiente en el sistema local del muro."""
    w = b - a
    hojas = (
        [(a, w / 2, True), (b, w / 2, False)]
        if vano.tipo == "P2"
        else [(a, w, True) if vano.bisagra == "izq" else (b, w, False)]
    )
    for hx, r, en_a in hojas:
        if adentro:
            vb = v_in
            self_v = vb + r
            a1, a2 = (0.0, 90.0) if en_a else (90.0, 180.0)
        else:
            vb = v_out
            self_v = vb - r
            a1, a2 = (270.0, 360.0) if en_a else (180.0, 270.0)
        lz.lin(hx, vb, hx, self_v, "PA14-PUERTAS")
        lz.arco(hx, vb, r, a1, a2, "PA14-PUERTAS")


def _simbolo_vano(
    lz: Lienzo, a: float, b: float, v0: float, esp: float, vano: Vano, adentro: bool
) -> None:
    """Dibuja el símbolo del vano entre a y b en un muro que ocupa v en [v0, v0+esp]."""
    v1 = v0 + esp
    t = vano.tipo
    if t == "V":
        lz.lin(a, v0, b, v0, "PA14-VENTANAS")
        lz.lin(a, v1, b, v1, "PA14-VENTANAS")
        vm = v0 + esp / 2
        lz.lin(a, vm - 0.015, b, vm - 0.015, "PA14-VENTANAS")
        lz.lin(a, vm + 0.015, b, vm + 0.015, "PA14-VENTANAS")
    elif t in ("P", "P2"):
        _puerta(lz, a, b, v1, v0, vano, adentro)
    elif t == "VE":
        lz.lin(a, v0 + esp / 2, b, v0 + esp / 2, "PA14-VENTANAS")
        lz.rect(a, v1, b - a, 0.35, "PA14-MOBILIARIO")
    elif t == "PO":
        n = max(3, int((b - a) / 0.35))
        paso = (b - a) / n
        for i in range(0, n, 2):
            lz.lin(
                a + i * paso,
                v0 + esp / 2,
                a + (i + 1) * paso,
                v0 + esp / 2,
                "PA14-PUERTAS",
            )
    elif t == "PC":
        lz.rect(a, v0 - 0.12, b - a, 0.06, "PA14-PUERTAS")
        lz.lin(b, v0 - 0.15, 2 * b - a, v0 - 0.15, "PA14-PUERTAS")
    if vano.etiqueta:
        lz.txt(
            (a + b) / 2, v0 - 0.45, vano.etiqueta, h=0.14, w_max=max(b - a, 2.5) * 1.6
        )


def _muro_local(
    lz: Lienzo,
    largo: float,
    esp: float,
    capa: str,
    vanos: list[tuple[float, Vano]],
    recorte: bool,
    v0: float = 0.0,
    achurar: bool = False,
    signo_in: int = 1,
) -> None:
    """Muro a lo largo de +u entre v0 y v0+esp con vanos (s_centro, Vano)."""
    huecos = [(s - vn.ancho / 2, s + vn.ancho / 2) for s, vn in vanos]
    ini_in, fin_in = (esp, largo - esp) if recorte else (0.0, largo)
    for a, b in _segmentos(0.0, largo, huecos):
        lz.lin(a, v0, b, v0, capa)
        if achurar:
            lz.achurado(a, v0, b - a, esp, 0.12)
    for a, b in _segmentos(ini_in, fin_in, huecos):
        lz.lin(a, v0 + esp, b, v0 + esp, capa)
    for (a, b), (_, vn) in zip(huecos, vanos, strict=True):
        lz.lin(a, v0, a, v0 + esp, capa)
        lz.lin(b, v0, b, v0 + esp, capa)
        adentro = (vn.hacia in ("in", "+")) == (signo_in > 0)
        _simbolo_vano(lz, a, b, v0, esp, vn, adentro)


def cerramiento(
    lz: Lienzo,
    largo: float,
    ancho: float,
    esp: float,
    capa: str,
    vanos: dict[str, list[Vano]] | None = None,
    achurar: bool = False,
) -> None:
    """Muro perimetral de esquinas limpias con vanos por lado (S, E, N, O)."""
    vanos = vanos or {}
    lados = {
        "S": (0.0, 0.0, 0, largo, lambda c: c),
        "E": (largo, 0.0, 90, ancho, lambda c: c),
        "N": (largo, ancho, 180, largo, lambda c: largo - c),
        "O": (0.0, ancho, 270, ancho, lambda c: ancho - c),
    }
    for clave, (ox, oy, rot, lon, conv) in lados.items():
        locales = [(conv(vn.centro), vn) for vn in vanos.get(clave, [])]
        with lz.local(ox, oy, rot):
            _muro_local(lz, lon, esp, capa, locales, recorte=True, achurar=achurar)


def tabique(
    lz: Lienzo,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    vanos: list[Vano] | None = None,
    esp: float = 0.10,
    capa: str = "PA14-TABIQUES",
    achurar: bool = False,
) -> None:
    """Tabique ortogonal centrado en el eje (x1,y1)-(x2,y2) con vanos en coord. global."""
    vanos = vanos or []
    horizontal = abs(y2 - y1) < 1e-9
    if horizontal:
        a, b = sorted((x1, x2))
        locales = [(vn.centro - a, vn) for vn in vanos]
        with lz.local(a, y1, 0):
            _muro_local(lz, b - a, esp, capa, locales, False, -esp / 2, achurar, 1)
    else:
        a, b = sorted((y1, y2))
        locales = [(vn.centro - a, vn) for vn in vanos]
        with lz.local(x1, a, 90):
            # en giro 90 el +v local apunta a -X: "+" (mayor X) equivale a afuera
            _muro_local(lz, b - a, esp, capa, locales, False, -esp / 2, achurar, -1)


def cerco_malla(
    lz: Lienzo, largo: float, ancho: float, portones: dict[str, list[Vano]]
) -> None:
    """Cerco perimétrico de malla olímpica con postes cada 2.50 m y portones."""
    cerramiento(lz, largo, ancho, 0.05, "PA14-CERCO", portones)
    huecos = {
        k: [(v.centro - v.ancho / 2, v.centro + v.ancho / 2) for v in vs]
        for k, vs in portones.items()
    }
    paso = 2.5
    for k, lon in (("S", largo), ("N", largo), ("O", ancho), ("E", ancho)):
        n = max(1, round(lon / paso))
        for i in range(n + 1):
            s = i * lon / n
            if any(a - 0.05 < s < b + 0.05 for a, b in huecos.get(k, [])):
                continue
            x, y = {"S": (s, 0.0), "N": (s, ancho), "O": (0.0, s), "E": (largo, s)}[k]
            lz.rect(x - 0.05, y - 0.05, 0.10, 0.10, "PA14-CERCO")
    lz.txt(
        largo / 2,
        -0.45,
        "CERCO MALLA OLIMPICA H=2.40 m C/POSTES TUBO 2in @2.50 m",
        h=0.16,
        w_max=largo,
    )


# ================================================================ ejes y columnas
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


# ======================================================== bloques de mobiliario
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
