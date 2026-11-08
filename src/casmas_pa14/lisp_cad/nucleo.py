"""Primitivas AutoLISP (entmake), capas CAD y motor de compilación de PA14_dibujos.lsp."""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass
from pathlib import Path

ARCHIVO = "PA14_dibujos.lsp"
SEPARACION = 20.0  # m entre dibujos de detalle
DESFASE_DETALLES = 1000.0  # m al sur del punto más bajo del plano de ubicación

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
    "PA14-MUROS": 7,
    "PA14-TABIQUES": 8,
    "PA14-MOBILIARIO": 2,
    "PA14-APARATOS": 3,
    "PA14-PUERTAS": 3,
    "PA14-VENTANAS": 4,
    "PA14-ESTRUCTURA": 1,
    "PA14-ESCALERAS": 7,
    "PA14-MEMBRETE": 7,
    "PA14-SIMBOLOS": 1,
    "PA14-HATCH": 8,
    "PA14-TALADROS": 1,
    "PA14-ALIVIO": 2,
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
(defun pa14:circulo (x y r capa)
  (entmake (list '(0 . "CIRCLE") (cons 8 capa) (cons 10 (pa14:p x y)) (cons 40 r))))
(defun pa14:arco (x y r a1 a2 capa)
  (entmake (list '(0 . "ARC") (cons 8 capa) (cons 10 (pa14:p x y)) (cons 40 r)
                 (cons 50 (/ (* a1 3.141592653589793) 180.0))
                 (cons 51 (/ (* a2 3.141592653589793) 180.0)))))
(defun pa14:texto (x y alt txt capa)
  (entmake (list '(0 . "TEXT") (cons 8 capa) (cons 10 (pa14:p x y)) (cons 40 alt) (cons 1 txt))))
(defun pa14:texto-cen (x y alt txt capa)
  (entmake (list '(0 . "TEXT") (cons 8 capa) (cons 10 (pa14:p x y)) (cons 11 (pa14:p x y))
                 (cons 40 alt) (cons 1 txt) '(72 . 1) '(73 . 2))))
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
(defun pa14:pedir-origen (msg / pt)
  (setq pt (getpoint (strcat "\n" msg " [Clic en pantalla o ENTER para 0,0]: ")))
  (if pt
    (pa14:origen (car pt) (cadr pt))
    (pa14:origen 0.0 0.0)))
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


def _circulo(x, y, r, capa="PA14-SIMBOLOS") -> str:
    return f'(pa14:circulo {_n(x)} {_n(y)} {_n(r)} "{capa}")'


def _arco(x, y, r, a1, a2, capa="PA14-PUERTAS") -> str:
    return f'(pa14:arco {_n(x)} {_n(y)} {_n(r)} {_n(a1)} {_n(a2)} "{capa}")'


def _texto_cen(x, y, alt, texto, capa="PA14-TEXTO") -> str:
    return f'(pa14:texto-cen {_n(x)} {_n(y)} {_n(alt)} {_txt(texto)} "{capa}")'


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
