"""Generación de un archivo AutoLISP (.lsp) con los planos básicos del proyecto.

Uso en AutoCAD: APPLOAD → cargar ``PA14_dibujos.lsp`` → escribir un comando:
PA14_UBICACION, PA14_SECCION, PA14_CAMPAMENTO, PA14_POLVORIN, PA14_SANEAMIENTO,
PA14_BOTADERO o PA14_TODO.

Posicionamiento (sin configurar nada a mano):
- Unidades forzadas: metros (INSUNITS=4), decimal (LUNITS=2), grados (AUNITS=0).
- PA14_UBICACION dibuja en coordenadas UTM reales (WGS84 18L): X = Este, Y = Norte.
- Los detalles (sección, campamento, ...) van en una franja fija al sur del plano
  de ubicación. No se pide punto de inserción; al final se hace ZOOM extensión.
"""

import unicodedata
from dataclasses import dataclass
from pathlib import Path

ARCHIVO = "PA14_dibujos.lsp"
SEPARACION = 20.0  # m entre dibujos de detalle
DESFASE_DETALLES = 1000.0  # m al sur del punto más bajo del plano de ubicación
ANCHO_MAX_FILA_CAMP = 80.0  # m, distribución del campamento
CALLE_CAMP = 6.0  # m entre edificaciones

CAPAS = {
    "PA14-CONTORNO": 7,
    "PA14-EJE": 1,
    "PA14-TEXTO": 2,
    "PA14-COTA": 1,
    "PA14-EDIFICACION": 4,
    "PA14-CERCO": 6,
    "PA14-RUMAS": 30,
    "PA14-GALIBO": 5,
    "PA14-OBRAS-ARTE": 8,
}

_LIBRERIA = r"""
;;; ---------------------------------------------------------------- libreria PA14
(setq *ox* 0.0 *oy* 0.0)
(defun pa14:capa (nom col)
  (if (not (tblsearch "LAYER" nom))
    (entmake (list '(0 . "LAYER") '(100 . "AcDbSymbolTableRecord")
                   '(100 . "AcDbLayerTableRecord") (cons 2 nom) '(70 . 0)
                   (cons 62 col) '(6 . "Continuous")))))
(defun pa14:p (x y) (list (+ *ox* x) (+ *oy* y) 0.0))
(defun pa14:pline (pts blgs cerrado capa / ent)
  (setq ent (list '(0 . "LWPOLYLINE") '(100 . "AcDbEntity") (cons 8 capa)
                  '(100 . "AcDbPolyline") (cons 90 (length pts))
                  (cons 70 (if cerrado 1 0))))
  (foreach par (mapcar 'list pts blgs)
    (setq ent (append ent
                (list (cons 10 (list (+ *ox* (car (car par))) (+ *oy* (cadr (car par)))))
                      (cons 42 (cadr par))))))
  (entmake ent))
(defun pa14:rect (x y w h capa)
  (pa14:pline (list (list x y) (list (+ x w) y) (list (+ x w) (+ y h)) (list x (+ y h)))
              '(0.0 0.0 0.0 0.0) T capa))
(defun pa14:linea (x1 y1 x2 y2 capa)
  (entmake (list '(0 . "LINE") (cons 8 capa) (cons 10 (pa14:p x1 y1)) (cons 11 (pa14:p x2 y2)))))
(defun pa14:texto (x y alt txt capa)
  (entmake (list '(0 . "TEXT") (cons 8 capa) (cons 10 (pa14:p x y)) (cons 40 alt) (cons 1 txt))))
(defun pa14:cota (x1 y1 x2 y2 x3 y3 txt / capa)
  (setq capa (getvar "CLAYER"))
  (setvar "CLAYER" "PA14-COTA")
  (if (and txt (/= txt ""))
    (command "_.DIMLINEAR" "_non" (pa14:p x1 y1) "_non" (pa14:p x2 y2) "_T" txt "_non" (pa14:p x3 y3))
    (command "_.DIMLINEAR" "_non" (pa14:p x1 y1) "_non" (pa14:p x2 y2) "_non" (pa14:p x3 y3)))
  (setvar "CLAYER" capa))
(defun pa14:cota-ang (vx vy x1 y1 x2 y2 x3 y3 txt / capa)
  (setq capa (getvar "CLAYER"))
  (setvar "CLAYER" "PA14-COTA")
  (if (and txt (/= txt ""))
    (command "_.DIMANGULAR" "" "_non" (pa14:p vx vy) "_non" (pa14:p x1 y1) "_non" (pa14:p x2 y2) "_T" txt "_non" (pa14:p x3 y3))
    (command "_.DIMANGULAR" "" "_non" (pa14:p vx vy) "_non" (pa14:p x1 y1) "_non" (pa14:p x2 y2) "_non" (pa14:p x3 y3)))
  (setvar "CLAYER" capa))
(defun pa14:dim-estilo (esc txt-alt asz)
  (setvar "DIMSCALE" esc)
  (setvar "DIMTXT" txt-alt)
  (setvar "DIMASZ" asz)
  (setvar "DIMEXE" (* txt-alt 0.5))
  (setvar "DIMEXO" (* txt-alt 0.3))
  (setvar "DIMGAP" (* txt-alt 0.3))
  (setvar "DIMDEC" 2)
  (setvar "DIMTAD" 1))
(defun pa14:unidades ()
  (setvar "INSUNITS" 4)   ; metros
  (setvar "LUNITS" 2)     ; decimal
  (setvar "LUPREC" 3)     ; 0.000
  (setvar "AUNITS" 0)     ; grados decimales
  (setvar "ANGBASE" 0.0)  ; 0 grados = Este
  (setvar "ANGDIR" 0)     ; antihorario
  (pa14:dim-estilo 1.0 0.22 0.18))
(defun pa14:origen (x y) (setq *ox* x *oy* y))
(defun pa14:inicio ()
  (setq *pa14-eco* (getvar "CMDECHO"))
  (setvar "CMDECHO" 0)
  (command "_.UCS" "_W")  ; siempre sobre el sistema universal (UTM)
  (pa14:unidades)
  (pa14:capas)
  (pa14:origen 0.0 0.0))
(defun pa14:fin ()
  (command "_.ZOOM" "_E")
  (setvar "CMDECHO" *pa14-eco*)
  (princ "\nPA14: dibujo terminado.")
  (princ))
"""


@dataclass
class Dibujo:
    comando: str  # sin "C:"
    descripcion: str
    cuerpo: list[str]
    ancho: float  # extensión en X (para PA14_TODO)


def _txt(texto: str) -> str:
    """Cadena LISP segura: sin tildes (AutoCAD ANSI) y con comillas escapadas."""
    plano = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return '"' + plano.replace("\\", "/").replace('"', "'") + '"'


def _n(x: float) -> str:
    return f"{x:.3f}"


def _rect(x, y, w, h, capa) -> str:
    return f'(pa14:rect {_n(x)} {_n(y)} {_n(w)} {_n(h)} "{capa}")'


def _texto(x, y, alt, texto, capa="PA14-TEXTO") -> str:
    return f'(pa14:texto {_n(x)} {_n(y)} {_n(alt)} {_txt(texto)} "{capa}")'


def _linea(x1, y1, x2, y2, capa) -> str:
    return f'(pa14:linea {_n(x1)} {_n(y1)} {_n(x2)} {_n(y2)} "{capa}")'


def _cota(x1, y1, x2, y2, x3, y3, txt="") -> str:
    txt_lisp = _txt(txt) if txt else '""'
    return f"(pa14:cota {' '.join(_n(v) for v in (x1, y1, x2, y2, x3, y3))} {txt_lisp})"


def _cota_angular(vx, vy, x1, y1, x2, y2, x3, y3, txt="") -> str:
    txt_lisp = _txt(txt) if txt else '""'
    return f"(pa14:cota-ang {' '.join(_n(v) for v in (vx, vy, x1, y1, x2, y2, x3, y3))} {txt_lisp})"


def _hatch_cunetas(v: float, e: float, ac: float, hc: float, b: float) -> list[str]:
    """Rayado a 45° para las cunetas izquierda y derecha (capa PA14-OBRAS-ARTE)."""
    x0, y0, w, h = v, e - hc, ac, hc
    c_min = y0 - x0 - w
    c_max = (y0 + h) - x0
    paso = (c_max - c_min) / 11
    lineas = []
    for i in range(1, 11):
        c = c_min + i * paso
        x_top = (y0 + h) - c
        y_vert = x0 + c
        x_hyp = (y0 - (h / w) * x0 - c) / (1.0 - h / w)
        y_hyp = x_hyp + c
        pts = []
        if x0 <= x_top <= x0 + w:
            pts.append((x_top, y0 + h))
        if y0 <= y_vert <= y0 + h:
            pts.append((x0, y_vert))
        if x0 <= x_hyp <= x0 + w and y0 <= y_hyp <= y0 + h:
            pts.append((x_hyp, y_hyp))
        if len(pts) == 2:
            (x1, y1), (x2, y2) = pts[0], pts[1]
            lineas.append(_linea(x1, y1, x2, y2, "PA14-OBRAS-ARTE"))
            lineas.append(_linea(b - x1, y1, b - x2, y2, "PA14-OBRAS-ARTE"))
    return lineas


# ---------------------------------------------------------------- dibujos
def dibujo_seccion(sec: dict) -> Dibujo:
    """Sección típica con veredas, cunetas, calzada con bombeo y cotas normalizadas."""
    b, h, hw = sec["ancho_m"], sec["altura_m"], sec["hastial_m"]
    e = sec["espesor_rasante_m"]
    hr = sec.get("altura_rasante_m", h - e)
    v = sec["vereda_m"]
    berma = sec["berma_m"]
    carril = sec["ancho_carril_m"]
    separador = sec["separador_m"]
    wg, hg = sec["ancho_galibo_m"], sec["altura_galibo_m"]
    ac = sec.get("cuneta_ancho_m", 1.20)
    hc = sec.get("cuneta_prof_m", 0.40)
    bombeo = sec.get("bombeo_pct", 2.0) / 100.0

    x_eje = b / 2
    x_cuneta_izq = v + ac  # 1.95
    x_berma_izq = v + berma  # 2.55
    x_carril_izq = x_berma_izq + carril  # 6.15
    x_separador_der = x_carril_izq + separador  # 7.15
    x_carril_der = x_separador_der + carril  # 10.75
    x_cuneta_der = b - (v + ac)  # 11.35
    x_vereda_der = b - v  # 12.55

    # Bombeo sobre calzada desde cuneta hasta separador
    dy_bombeo = (x_carril_izq - x_cuneta_izq) * bombeo
    y_calzada_eje = e + dy_bombeo

    pts_contorno = f"'((0.0 0.0) ({_n(b)} 0.0) ({_n(b)} {_n(hw)}) (0.0 {_n(hw)}))"
    pts_cuneta_izq = (
        f"'(({_n(v)} {_n(e)}) ({_n(v)} {_n(e - hc)}) ({_n(x_cuneta_izq)} {_n(e)}))"
    )
    pts_cuneta_der = f"'(({_n(x_cuneta_der)} {_n(e)}) ({_n(x_vereda_der)} {_n(e - hc)}) ({_n(x_vereda_der)} {_n(e)}))"

    cuerpo = [
        # 1. Contorno de excavación
        f'(pa14:pline {pts_contorno} \'(0.0 0.0 1.0 0.0) T "PA14-CONTORNO")',
        # 2. Rasante de fondo y divisiones de subbase (y=0 a y=e)
        _linea(0, e, b, e, "PA14-CONTORNO"),
        _linea(v, 0, v, e, "PA14-CONTORNO"),
        _linea(x_berma_izq, 0, x_berma_izq, e, "PA14-CONTORNO"),
        _linea(x_carril_izq, 0, x_carril_izq, e, "PA14-CONTORNO"),
        _linea(x_separador_der, 0, x_separador_der, e, "PA14-CONTORNO"),
        _linea(x_carril_der, 0, x_carril_der, e, "PA14-CONTORNO"),
        _linea(x_vereda_der, 0, x_vereda_der, e, "PA14-CONTORNO"),
        # Galería / ducto en subbase derecha
        _rect(x_carril_der + 0.60, 0.0, 1.20, e, "PA14-CONTORNO"),
        # 3. Veredas y cunetas
        _linea(0, e, v, e, "PA14-OBRAS-ARTE"),
        f'(pa14:pline {pts_cuneta_izq} \'(0.0 0.0 0.0) T "PA14-OBRAS-ARTE")',
        _linea(
            x_cuneta_izq, e, x_carril_izq, y_calzada_eje, "PA14-CONTORNO"
        ),  # calzada izq
        _rect(
            x_carril_izq, y_calzada_eje, separador, 0.20, "PA14-CONTORNO"
        ),  # separador central
        _linea(
            x_separador_der, y_calzada_eje, x_cuneta_der, e, "PA14-CONTORNO"
        ),  # calzada der
        f'(pa14:pline {pts_cuneta_der} \'(0.0 0.0 0.0) T "PA14-OBRAS-ARTE")',
        *_hatch_cunetas(v, e, ac, hc, b),
        _linea(x_vereda_der, e, b, e, "PA14-OBRAS-ARTE"),
        # 4. Gálibo y ejes
        _rect(v, e, wg, hg, "PA14-GALIBO"),
        _linea(x_eje, -0.8, x_eje, h + 0.6, "PA14-EJE"),
        _linea(0, hw, b, hw, "PA14-EJE"),
        # 5. Cotas inferiores (parciales y total)
        _cota(0.0, 0.0, v, 0.0, v / 2, -0.65, f"{v:.2f} m"),
        _cota(
            v,
            0.0,
            x_berma_izq,
            0.0,
            (v + x_berma_izq) / 2,
            -0.65,
            f"{berma:.2f} m",
        ),
        _cota(
            x_berma_izq,
            0.0,
            x_carril_izq,
            0.0,
            (x_berma_izq + x_carril_izq) / 2,
            -0.65,
            f"{carril:.2f} m",
        ),
        _cota(
            x_carril_izq,
            0.0,
            x_separador_der,
            0.0,
            x_eje,
            -0.65,
            f"{separador:.2f} m",
        ),
        _cota(0.0, 0.0, b, 0.0, x_eje, -1.35, f"{b:.2f} m"),
        # 6. Cotas de detalle (cuneta, subrasante y bombeo)
        _cota(
            v,
            e,
            x_cuneta_izq,
            e,
            (v + x_cuneta_izq) / 2,
            e + 0.40,
            f"{ac:.2f} m",
        ),
        _cota(v, e - hc, v, e, v - 0.40, e - hc / 2, f"{hc:.2f} m"),
        _cota(x_eje, 0.0, x_eje, e, x_eje - 0.75, e / 2, f"{e:.2f} m"),
        _cota_angular(
            x_cuneta_der,
            e,
            x_separador_der,
            e,
            x_separador_der,
            y_calzada_eje,
            x_separador_der + 1.20,
            e + dy_bombeo * 0.70,
            f"{sec.get('bombeo_pct', 2.0):.0f}%%d",
        ),
        # 7. Cotas verticales (alturas y gálibo a la izquierda)
        _cota(v, e, v, e + hg, -0.65, e + hg / 2, f"{hg:.2f} m"),
        _cota(
            v,
            e + hg,
            v,
            h,
            -0.65,
            (e + hg + h) / 2,
            f"{h - (e + hg):.2f} m",
        ),
        _cota(0.0, e, 0.0, h, -1.25, (e + h) / 2, f"{hr:.2f} m"),
        _cota(0.0, 0.0, 0.0, h, -1.85, h / 2, f"{h:.2f} m"),
        # 8. Textos
        _texto(0.0, h + 0.80, 0.35, f"SECCION TIPICA - {h:.2f} m x {b:.2f} m"),
        _texto(
            0.0,
            -2.10,
            0.20,
            f"A = {sec['area_m2']:.2f} m2   R = {sec['radio_m']:.2f} m   "
            f"Galibo = {wg:.2f} x {hg:.2f} m",
        ),
    ]
    return Dibujo("PA14_SECCION", "Sección típica del túnel", cuerpo, b + 4)


def dibujo_campamento(camp: dict) -> Dibujo:
    cuerpo, x, y, alto_fila, ancho_usado = [], 0.0, 0.0, 0.0, 0.0
    for e in camp["edificaciones"]:
        largo, ancho = e["largo_m"], e["ancho_m"]
        if x > 0 and x + largo > ANCHO_MAX_FILA_CAMP:
            x, y, alto_fila = 0.0, y + alto_fila + CALLE_CAMP, 0.0
        alt = min(0.8, ancho / 5)
        cuerpo += [
            _rect(x, y, largo, ancho, "PA14-EDIFICACION"),
            _texto(x + 0.3, y + ancho / 2 + 0.1, alt, e["nombre"]),
            _texto(
                x + 0.3,
                y + ancho / 2 - alt - 0.1,
                alt * 0.8,
                f"{largo:.1f} x {ancho:.1f} m",
            ),
        ]
        x += largo + CALLE_CAMP
        alto_fila = max(alto_fila, ancho)
        ancho_usado = max(ancho_usado, x - CALLE_CAMP)
    alto_total = y + alto_fila
    m = CALLE_CAMP
    cuerpo += [
        _rect(-m, -m, ancho_usado + 2 * m, alto_total + 2 * m, "PA14-CERCO"),
        _texto(
            -m, alto_total + m + 1.5, 2.0, "CAMPAMENTO - DISTRIBUCION DE EDIFICACIONES"
        ),
    ]
    return Dibujo(
        "PA14_CAMPAMENTO", "Distribución del campamento", cuerpo, ancho_usado + 2 * m
    )


def _planta_polvorin(d: dict, x0: float, titulo: str) -> tuple[list[str], float]:
    c = d["config"]
    muro, sp = c["espesor_muro_m"], c["separacion_pared_m"]
    li, ai = d["largo_int_m"], d["ancho_int_m"]
    cuerpo = [
        _rect(x0, 0, li + 2 * muro, ai + 2 * muro, "PA14-CONTORNO"),
        _rect(x0 + muro, muro, li, ai, "PA14-CONTORNO"),
    ]
    restantes = d["rumas"]
    for fila in range(c["filas"]):
        # fila 0 junto al muro inferior, fila 1 junto al muro superior
        y = muro + sp if fila == 0 else muro + ai - sp - c["caja_ancho_m"]
        for i in range(min(d["rumas_por_fila"], restantes)):
            x = x0 + muro + sp + i * (c["caja_largo_m"] + c["separacion_rumas_m"])
            cuerpo.append(
                _rect(x, y, c["caja_largo_m"], c["caja_ancho_m"], "PA14-RUMAS")
            )
        restantes -= d["rumas_por_fila"]
    cuerpo += [
        _cota(x0, 0, x0 + li + 2 * muro, 0, x0 + li / 2, -1.0),
        _cota(x0, 0, x0, ai + 2 * muro, x0 - 1.0, ai / 2),
        _texto(x0, ai + 2 * muro + 1.0, 0.4, titulo),
        _texto(
            x0,
            -2.2,
            0.25,
            f"{d['cajas']} cajas - {d['rumas']} rumas de {d['cajas_por_ruma']}",
        ),
    ]
    return cuerpo, li + 2 * muro


def dibujo_polvorin(pol: dict) -> Dibujo:
    cuerpo, ancho = _planta_polvorin(pol["explosivos"], 2.0, "POLVORIN DE EXPLOSIVOS")
    x1 = 2.0 + ancho + 8.0
    cuerpo2, ancho2 = _planta_polvorin(pol["accesorios"], x1, "POLVORIN DE ACCESORIOS")
    return Dibujo(
        "PA14_POLVORIN", "Plantas de polvorines", cuerpo + cuerpo2, x1 + ancho2
    )


def dibujo_saneamiento(agua: dict) -> Dibujo:
    lr, lt, at = agua["lado_reservorio_m"], agua["largo_ts_m"], agua["ancho_ts_m"]
    xt = 2.0 + lr + 8.0
    cuerpo = [
        _rect(2.0, 0, lr, lr, "PA14-CONTORNO"),
        _cota(2.0, 0, 2.0 + lr, 0, 2.0 + lr / 2, -1.0),
        _cota(2.0, 0, 2.0, lr, 1.0, lr / 2),
        _texto(2.0, lr + 1.0, 0.4, "PETAP - RESERVORIO"),
        _texto(2.0, -2.2, 0.25, f"V = {agua['v_reservorio_m3']:.1f} m3"),
        _rect(xt, 0, lt, at, "PA14-CONTORNO"),
        _linea(xt + lt * 2 / 3, 0, xt + lt * 2 / 3, at, "PA14-CONTORNO"),
        _cota(xt, 0, xt + lt, 0, xt + lt / 2, -1.0),
        _cota(xt, 0, xt, at, xt - 1.0, at / 2),
        _texto(xt, at + 1.0, 0.4, "PETAR - TANQUE SEPTICO"),
        _texto(
            xt, -2.2, 0.25, f"V = {agua['v_tanque_m3']:.1f} m3 (2 camaras 2/3 - 1/3)"
        ),
    ]
    return Dibujo("PA14_SANEAMIENTO", "PETAP y PETAR", cuerpo, xt + lt)


def dibujo_botadero(maq: dict) -> Dibujo:
    lado = maq["lado_botadero_m"]
    cuerpo = [
        '(setvar "DIMSCALE" 10.0)',
        _rect(0, 0, lado, lado, "PA14-CERCO"),
        _cota(0, 0, lado, 0, lado / 2, -5.0),
        '(setvar "DIMSCALE" 1.0)',
        _texto(0, lado + 3.0, 3.0, "BOTADERO (DME)"),
        _texto(0, -12.0, 2.0, f"Area = {maq['area_botadero_m2']:.0f} m2"),
    ]
    return Dibujo("PA14_BOTADERO", "Huella del botadero", cuerpo, lado)


def dibujo_ubicacion(ub: dict) -> Dibujo:
    """Puntos del proyecto en coordenadas UTM reales (X = Este, Y = Norte)."""
    puntos = ub["puntos"]
    pe, ps = puntos["PE"], puntos["PS"]
    cuerpo = [_linea(pe["este"], pe["norte"], ps["este"], ps["norte"], "PA14-EJE")]
    for pt in puntos.values():
        x, y = pt["este"], pt["norte"]
        cuerpo += [
            _rect(x - 15.0, y - 15.0, 30.0, 30.0, "PA14-CONTORNO"),
            _texto(x + 25.0, y + 25.0, 30.0, pt["nombre"]),
            _texto(
                x + 25.0,
                y - 15.0,
                18.0,
                f"E {x:.2f}  N {y:.2f}  Z {pt['cota']:.0f} m",
            ),
        ]
    xs = [pt["este"] for pt in puntos.values()]
    return Dibujo(
        "PA14_UBICACION",
        "Plano de ubicacion - UTM WGS84 18L",
        cuerpo,
        max(xs) - min(xs) + 500.0,
    )


# ---------------------------------------------------------------- archivo
def _origenes(ub: dict, detalles: list[Dibujo]) -> list[tuple[float, float]]:
    """Origen fijo de cada detalle: franja al sur del plano de ubicación."""
    puntos = ub["puntos"].values()
    x0 = min(pt["este"] for pt in puntos)
    y0 = min(pt["norte"] for pt in puntos) - DESFASE_DETALLES
    origenes, dx = [], 0.0
    for d in detalles:
        origenes.append((x0 + dx, y0))
        dx += d.ancho + SEPARACION
    return origenes


def generar_lisp(ctx: dict, carpeta: Path, proyecto: str) -> Path:
    ubicacion = dibujo_ubicacion(ctx["ubicacion"])
    detalles = [
        dibujo_seccion(ctx["seccion"]),
        dibujo_campamento(ctx["campamento"]),
        dibujo_polvorin(ctx["polvorin"]),
        dibujo_saneamiento(ctx["agua"]),
        dibujo_botadero(ctx["maquinaria"]),
    ]
    dibujos = [ubicacion, *detalles]
    origenes = [(0.0, 0.0), *_origenes(ctx["ubicacion"], detalles)]
    lineas = [
        f";;; {_txt(proyecto)[1:-1]} - generado con `uv run pa14`. NO EDITAR A MANO.",
        ";;; APPLOAD -> cargar este archivo -> comandos: "
        + ", ".join(d.comando for d in dibujos)
        + ", PA14_TODO",
        ";;; Unidades: metros. Coordenadas UTM WGS84 zona 18L (X = Este, Y = Norte).",
        _LIBRERIA,
        "(defun pa14:capas ()",
        *[f'  (pa14:capa "{n}" {c})' for n, c in CAPAS.items()],
        ")",
    ]
    todo = ["\n(defun c:PA14_TODO ()", "  (pa14:inicio)"]
    for d, (ox, oy) in zip(dibujos, origenes, strict=True):
        nombre = d.comando.lower().replace("pa14_", "pa14:d-")
        lineas += [f"\n;;; {_txt(d.descripcion)[1:-1]}", f"(defun {nombre} ()"]
        lineas += [f"  {c}" for c in d.cuerpo]
        lineas += [
            ")",
            f"(defun c:{d.comando} () (pa14:inicio)"
            f" (pa14:origen {_n(ox)} {_n(oy)}) ({nombre}) (pa14:fin))",
        ]
        todo += [f"  (pa14:origen {_n(ox)} {_n(oy)})", f"  ({nombre})"]
    todo += [
        "  (pa14:fin))",
        '(princ "\\nPA14 cargado. Escriba PA14_TODO.")',
        "(princ)",
    ]
    carpeta.mkdir(parents=True, exist_ok=True)
    ruta = carpeta / ARCHIVO
    contenido = "\n".join(lineas + todo) + "\n"
    contenido_ascii = (
        unicodedata.normalize("NFKD", contenido)
        .encode("ascii", "ignore")
        .decode("ascii")
    )
    ruta.write_text(contenido_ascii, encoding="ascii")
    return ruta
