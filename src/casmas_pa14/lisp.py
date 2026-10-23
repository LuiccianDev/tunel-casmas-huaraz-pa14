"""Generación de un archivo AutoLISP (.lsp) con los planos básicos del proyecto.

Uso en AutoCAD: APPLOAD → cargar ``PA14_dibujos.lsp`` → escribir un comando:
PA14_UBICACION, PA14_SECCION, PA14_GEOLOGIA o PA14_TODO.

Posicionamiento (sin configurar nada a mano):
- Unidades forzadas: metros (INSUNITS=4), decimal (LUNITS=2), grados (AUNITS=0).
- PA14_UBICACION dibuja en coordenadas UTM reales (WGS84 18L): X = Este, Y = Norte.
- Los detalles (sección, perfil geológico) van en una franja fija al sur del plano
  de ubicación. No se pide punto de inserción; al final se hace ZOOM extensión.
"""

import math
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
        _cota(0.0, 0.0, v, 0.0, v / 2, -1.15, f"{v:.2f} m"),
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
        _cota(0.0, 0.0, b, 0.0, x_eje, -1.75, f"{b:.2f} m"),
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
            -2.40,
            0.20,
            f"A = {sec['area_m2']:.2f} m2   R = {sec['radio_m']:.2f} m   "
            f"Galibo = {wg:.2f} x {hg:.2f} m",
        ),
    ]
    return Dibujo("PA14_SECCION", "Sección típica del túnel", cuerpo, b + 4)


# ---------------------------------------------------------------- 02 - Corte Geologico Longitudinal (5556 m)
def dibujo_geologia(geo: dict) -> Dibujo:
    """Corte geologico longitudinal del tunel (L = 5,556 m).

    Dibuja el perfil esquematico del macizo rocoso, el eje y rasante de excavacion
    del tunel, los contactos litologicos inclinados (buzamiento), las etiquetas
    de tipo de roca, RMR, Q-Slope y las cotas de progresiva (Km 0+000 a Km 5+556).
    """
    cuerpo = []
    tramos = geo.get("tramos", [])
    if not tramos:
        return Dibujo("PA14_GEOLOGIA", "Corte Geologico Longitudinal", [], 100.0)

    prog_ini = min(t["progresiva_inicio"] for t in tramos)
    prog_fin = max(t["progresiva_fin"] for t in tramos)
    longitud = prog_fin - prog_ini

    y_top = 220.0
    y_bot = -60.0
    y_tunel = 0.0
    h_exc = 9.58  # altura de excavacion

    # 1. Contorno general del macizo rocoso
    cuerpo.append(_rect(prog_ini, y_bot, longitud, y_top - y_bot, "PA14-CONTORNO"))

    # 2. Eje rasante y linea de clave del tunel
    cuerpo.append(_linea(prog_ini, y_tunel, prog_fin, y_tunel, "PA14-EJE"))
    cuerpo.append(
        _linea(prog_ini, y_tunel + h_exc, prog_fin, y_tunel + h_exc, "PA14-GALIBO")
    )
    cuerpo.append(
        _texto(
            prog_ini - 240.0,
            y_tunel + 2.0,
            12.0,
            "RASANTE DEL TUNEL",
            "PA14-TEXTO",
        )
    )
    cuerpo.append(
        _texto(
            prog_ini - 240.0,
            y_tunel + h_exc,
            10.0,
            "CLAVE (EXCAVACION)",
            "PA14-TEXTO",
        )
    )

    # 3. Encabezado del plano longitudinal
    cuerpo.append(
        _texto(
            prog_ini,
            y_top + 25.0,
            22.0,
            "PERFIL GEOLOGICO LONGITUDINAL - TUNEL TRASANDINO PA14 (L = 5,556.00 m)",
            "PA14-TEXTO",
        )
    )
    cuerpo.append(
        _texto(
            prog_ini,
            y_top + 8.0,
            12.0,
            "Escala Horizontal 1:1 (metros) | Contactos Litologicos, Buzamiento, RMR y Q-Slope",
            "PA14-TEXTO",
        )
    )

    # 4. Tramos litologicos y contactos geologicos
    for t in tramos:
        x_ini = t["progresiva_inicio"]
        x_fin = t["progresiva_fin"]
        l_tramo = x_fin - x_ini
        x_mid = (x_ini + x_fin) / 2.0
        tipo = t.get("tipo_roca", "")
        rmr = t.get("rmr", 0)
        q_slope = t.get("q_slope", 0.0)

        # Contacto litologico inclinado (buzamiento aparente ~70 deg)
        dx_buz = 45.0
        if x_ini > prog_ini:
            cuerpo.append(
                _linea(
                    x_ini - 10.0,
                    y_bot,
                    x_ini + dx_buz,
                    y_top,
                    "PA14-ESTRUCTURA",
                )
            )

        # Marca de progresiva en la base
        cuerpo.append(_linea(x_ini, y_bot, x_ini, y_bot - 15.0, "PA14-EJE"))
        cuerpo.append(
            _texto_cen(
                x_ini,
                y_bot - 30.0,
                10.0,
                f"KM {x_ini / 1000.0:.3f}",
                "PA14-TEXTO",
            )
        )

        # Litologia y geomecanica en la parte superior
        cuerpo.append(_texto_cen(x_mid, y_top - 35.0, 14.0, tipo, "PA14-TEXTO"))
        cuerpo.append(
            _texto_cen(
                x_mid,
                y_top - 60.0,
                10.0,
                f"RMR = {rmr} | Q-Slope = {q_slope:.3f}",
                "PA14-TEXTO",
            )
        )

        # Cota de longitud del tramo
        cuerpo.append(
            _cota(
                x_ini,
                y_bot - 55.0,
                x_fin,
                y_bot - 55.0,
                x_mid,
                y_bot - 70.0,
                f"L={l_tramo:.1f}m",
            )
        )

    # Cierre de la progresiva final
    cuerpo.append(_linea(prog_fin, y_bot, prog_fin, y_bot - 15.0, "PA14-EJE"))
    cuerpo.append(
        _texto_cen(
            prog_fin,
            y_bot - 30.0,
            10.0,
            f"KM {prog_fin / 1000.0:.3f}",
            "PA14-TEXTO",
        )
    )

    return Dibujo(
        "PA14_GEOLOGIA",
        "Corte Geologico Longitudinal del Tunel (0+000 a 5+556)",
        cuerpo,
        longitud + 400.0,
    )


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


def _taladros_cune(x_cune: float, y_cune: float, r_tal: float) -> list[str]:
    """Genera las entidades del cuñe cilíndrico de 4 secciones y el alivio central."""
    cuerpo: list[str] = [
        _circulo(x_cune, y_cune, 0.18, "PA14-ALIVIO"),
        _texto_cen(x_cune, y_cune - 0.40, 0.20, "ALIVIO D=102mm", "PA14-TEXTO"),
    ]
    for d_sq in (0.25, 0.90):
        for dx, dy in [(-d_sq, -d_sq), (-d_sq, d_sq), (d_sq, -d_sq), (d_sq, d_sq)]:
            cuerpo.append(_circulo(x_cune + dx, y_cune + dy, r_tal, "PA14-TALADROS"))
        cuerpo.append(
            _rect(x_cune - d_sq, y_cune - d_sq, 2 * d_sq, 2 * d_sq, "PA14-SIMBOLOS")
        )

    d2 = 0.50
    for dx, dy in [(0, -d2), (0, d2), (-d2, 0), (d2, 0)]:
        cuerpo.append(_circulo(x_cune + dx, y_cune + dy, r_tal, "PA14-TALADROS"))
    cuerpo.extend(
        [
            _linea(x_cune, y_cune - d2, x_cune + d2, y_cune, "PA14-SIMBOLOS"),
            _linea(x_cune + d2, y_cune, x_cune, y_cune + d2, "PA14-SIMBOLOS"),
            _linea(x_cune, y_cune + d2, x_cune - d2, y_cune, "PA14-SIMBOLOS"),
            _linea(x_cune - d2, y_cune, x_cune, y_cune - d2, "PA14-SIMBOLOS"),
        ]
    )

    d4 = 1.45
    pts_d4 = [
        (-d4, -d4),
        (-d4, 0),
        (-d4, d4),
        (0, -d4),
        (0, d4),
        (d4, -d4),
        (d4, 0),
        (d4, d4),
    ]
    for dx, dy in pts_d4:
        cuerpo.append(_circulo(x_cune + dx, y_cune + dy, r_tal, "PA14-TALADROS"))
    cuerpo.append(_rect(x_cune - d4, y_cune - d4, 2 * d4, 2 * d4, "PA14-SIMBOLOS"))
    return cuerpo


def _taladros_malla(
    b: float, hw: float, radio: float, xc: float, yc: float
) -> list[str]:
    """Genera las entidades de taladros (cuñe de 4 secciones, periferia, arrastre y ayuda)."""
    x_cune, y_cune = xc, hw + 0.60
    r_tal = 0.08
    cuerpo = _taladros_cune(x_cune, y_cune, r_tal)

    y_p = 0.40
    while y_p <= hw:
        cuerpo.append(_circulo(0.20, y_p, r_tal, "PA14-TALADROS"))
        cuerpo.append(_circulo(b - 0.20, y_p, r_tal, "PA14-TALADROS"))
        y_p += 0.60

    r_perif, n_corona = radio - 0.20, 33
    for i in range(1, n_corona):
        ang_rad = math.pi * i / n_corona
        cuerpo.append(
            _circulo(
                xc - r_perif * math.cos(ang_rad),
                yc + r_perif * math.sin(ang_rad),
                r_tal,
                "PA14-TALADROS",
            )
        )

    n_zapateras = 17
    dx_zap = (b - 0.80) / (n_zapateras - 1)
    for i in range(n_zapateras):
        cuerpo.append(_circulo(0.40 + i * dx_zap, 0.20, r_tal, "PA14-TALADROS"))

    for x_ay in [1.20, 2.30, 3.40, 4.50, 8.80, 9.90, 11.00, 12.10]:
        cuerpo.append(_circulo(x_ay, 1.10, r_tal, "PA14-TALADROS"))
        cuerpo.append(_circulo(x_ay, 2.10, r_tal, "PA14-TALADROS"))
    for x_ay in [1.00, 2.20, 3.50, 4.80, 8.50, 9.80, 11.10, 12.30]:
        cuerpo.append(_circulo(x_ay, 3.50, r_tal, "PA14-TALADROS"))

    for r_int, n_int in [(radio - 1.50, 19), (radio - 2.80, 13)]:
        for i in range(1, n_int):
            ang_rad = math.pi * i / n_int
            xt = xc - r_int * math.cos(ang_rad)
            yt = yc + r_int * math.sin(ang_rad)
            if abs(xt - x_cune) > 1.3 or abs(yt - y_cune) > 1.3:
                cuerpo.append(_circulo(xt, yt, r_tal, "PA14-TALADROS"))
    return cuerpo


def dibujo_malla(sec: dict, vol: dict | None = None) -> Dibujo:
    """Malla de perforacion y voladura mecanizada (cuñe de 4 secciones, ayudas y periferia)."""
    b, h, hw = sec["ancho_m"], sec["altura_m"], sec["hastial_m"]
    radio = b / 2.0
    xc, yc = radio, hw

    cuerpo = []
    pts_contorno = f"'((0.0 0.0) ({_n(b)} 0.0) ({_n(b)} {_n(hw)}) (0.0 {_n(hw)}))"
    cuerpo.append(f'(pa14:pline {pts_contorno} \'(0.0 0.0 1.0 0.0) T "PA14-CONTORNO")')
    cuerpo.append(_linea(xc, -1.0, xc, h + 1.0, "PA14-EJE"))
    cuerpo.append(_linea(-1.0, hw, b + 1.0, hw, "PA14-EJE"))
    cuerpo.extend(_taladros_malla(b, hw, radio, xc, yc))
    cuerpo.append(_cota(0.0, 0.0, b, 0.0, xc, -1.80, f"B={b:.2f}m"))
    cuerpo.append(_cota(0.0, 0.0, 0.0, hw, -1.80, hw / 2, f"hw={hw:.2f}m"))
    cuerpo.append(_cota(0.0, 0.0, 0.0, h, -3.20, h / 2, f"H={h:.2f}m"))

    # 8. Cuadro de Datos de Perforacion
    x_cuadro = b + 3.0
    y_cuadro = h
    w_cuadro = 8.8
    h_cuadro = 9.2
    cuerpo.append(
        _rect(x_cuadro, y_cuadro - h_cuadro, w_cuadro, h_cuadro, "PA14-CONTORNO")
    )
    cuerpo.append(
        _texto(
            x_cuadro + 0.5,
            y_cuadro - 0.8,
            0.32,
            "PARAMETROS DE MALLA DE PERFORACION",
            "PA14-TEXTO",
        )
    )
    cuerpo.append(
        _linea(
            x_cuadro,
            y_cuadro - 1.1,
            x_cuadro + w_cuadro,
            y_cuadro - 1.1,
            "PA14-CONTORNO",
        )
    )

    taladros_tot = sec["taladros"]
    avance_disparo = sec["avance_disparo_m"]
    area_exc = sec["area_m2"]
    burden_val = vol.get("inputs", {}).get("burden_m", 1.25) if vol else 1.25
    esp_val = vol.get("inputs", {}).get("espaciamiento_m", 1.75) if vol else 1.75

    lineas_datos = [
        f"Seccion tunel: Herradura ({b:.2f} x {h:.2f} m)",
        f"Area de excavacion: {area_exc:.2f} m2",
        f"Taladros de diseno: {taladros_tot} und",
        "Arranque: Cune quemado cilindrico (4 secc.)",
        "Alivio: 1 taladro D = 102 mm (4 pulg)",
        "Produccion: D = 45 mm (broca integral)",
        "Longitud barreno: 3.66 m (12 pies Sandvik)",
        f"Avance efectivo: {avance_disparo:.2f} m/disparo (90%)",
        f"Burden teorico Konya: B = {burden_val:.2f} m",
        f"Espaciamiento Konya: S = {esp_val:.2f} m",
        "Espaciamiento periferico: E = 0.60 m",
        "Taco inerte: T = 0.80 m (detritus compactado)",
        "Explosivo: Emulsion / ANFO (q=1.60 kg/m3)",
    ]

    for idx, linea_txt in enumerate(lineas_datos):
        cuerpo.append(
            _texto(
                x_cuadro + 0.5,
                y_cuadro - 1.7 - (idx * 0.52),
                0.22,
                linea_txt,
                "PA14-TEXTO",
            )
        )

    return Dibujo(
        "PA14_MALLA",
        "Malla de Perforacion y Disparo - Seccion Herradura (Drill & Blast)",
        cuerpo,
        b + w_cuadro + 8.0,
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
        dibujo_malla(ctx["seccion"], ctx.get("voladura")),
        dibujo_geologia(ctx["geologia"]),
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
        '(princ "\\nPA14 cargado. Escriba PA14_TODO o PA14_GEOLOGIA.")',
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
