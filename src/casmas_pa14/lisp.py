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


def _dibujar_recinto(
    edifs: list[dict],
    x_ini: float,
    y_ini: float,
    max_ancho: float,
    titulo: str,
    subtitulo: str,
    tipo_cerco: str = "PA14-CERCO",
    con_flecha_acceso: bool = False,
    es_polvorin: bool = False,
) -> tuple[list[str], float, float]:
    cuerpo, x, y, alto_fila, ancho_usado = [], x_ini, y_ini, 0.0, 0.0
    for e in edifs:
        largo, ancho = e["largo_m"], e["ancho_m"]
        if (x - x_ini) > 0 and (x - x_ini) + largo > max_ancho:
            x, y, alto_fila = x_ini, y + alto_fila + CALLE_CAMP, 0.0
        alt = min(0.65, max(0.25, ancho / 6))
        cuerpo += [
            _rect(x, y, largo, ancho, "PA14-EDIFICACION"),
            _texto(x + 0.3, y + ancho - alt - 0.2, alt, f"{e['id']}: {e['nombre']}"),
            _texto(
                x + 0.3,
                y + ancho - 2 * alt - 0.3,
                alt * 0.75,
                f"[{e.get('grupo', 'Area')}]",
            ),
            _texto(
                x + 0.3,
                y + 0.3,
                alt * 0.75,
                f"{largo:.1f} x {ancho:.1f} m  ({e['area_m2']:.0f} m2)",
            ),
        ]
        if es_polvorin and "Polvorin" in e["nombre"]:
            # Dibujar parapeto perimetral de tierra a 4.0 m
            cuerpo.append(
                _rect(x - 4.0, y - 4.0, largo + 8.0, ancho + 8.0, "PA14-RUMAS")
            )
            cuerpo.append(
                _texto(
                    x - 4.0,
                    y - 5.5,
                    0.4,
                    "[Parapeto de tierra e=2.5m s/SUCAMEC]",
                )
            )
        x += largo + CALLE_CAMP
        alto_fila = max(alto_fila, ancho)
        ancho_usado = max(ancho_usado, (x - x_ini) - CALLE_CAMP)

    alto_total = (y - y_ini) + alto_fila
    m = CALLE_CAMP
    w_rec = max(ancho_usado, 25.0) + 2 * m
    h_rec = alto_total + 2 * m

    # Cerco perimetral
    cuerpo.append(_rect(x_ini - m, y_ini - m, w_rec, h_rec, tipo_cerco))
    cuerpo.append(_texto(x_ini - m, y_ini + alto_total + m + 1.8, 1.3, titulo))
    cuerpo.append(_texto(x_ini - m, y_ini + alto_total + m + 0.5, 0.75, subtitulo))

    # Indicador de acceso principal
    if con_flecha_acceso:
        x_acc = x_ini + 10.0
        y_acc = y_ini - m
        cuerpo += [
            _linea(x_acc, y_acc - 8.0, x_acc, y_acc, "PA14-EJE"),
            _linea(x_acc - 1.5, y_acc - 2.5, x_acc, y_acc, "PA14-EJE"),
            _linea(x_acc + 1.5, y_acc - 2.5, x_acc, y_acc, "PA14-EJE"),
            _texto(
                x_acc + 2.0,
                y_acc - 5.0,
                0.9,
                "===> INGRESO PRINCIPAL Y CONTROL VEHICULAR",
            ),
        ]

    return cuerpo, w_rec, h_rec


def _dibujar_campamento_organizado(
    edifs: list[dict], x_base: float, y_base: float, nombre_camp: str, desc_camp: str
) -> tuple[list[str], float, float]:
    """Distribuye un campamento en 3 sectores funcionales con zonificación lógica."""
    cuerpo = []

    # 1. Separación por sectores
    ids_polv = {"EDIF-23", "EDIF-28", "EDIF-37", "EDIF-38"}
    ids_san = {
        "EDIF-14",
        "EDIF-15",
        "EDIF-16",
        "EDIF-17",
        "EDIF-18",
        "EDIF-19",
        "EDIF-32",
    }

    edifs_polv = [e for e in edifs if e["id"] in ids_polv]
    edifs_san = [e for e in edifs if e["id"] in ids_san]
    edifs_princ = [
        e for e in edifs if e["id"] not in ids_polv and e["id"] not in ids_san
    ]

    # Ordenamiento por zonificación funcional dentro del sector principal:
    # 1. Acceso y Garitas -> 2. Oficinas y Salud -> 3. Comedor/SUM/Dormitorios -> 4. Talleres/Patio Maquinaria
    orden_prioridad = {
        "Vigilancia y Transporte": 1,
        "Salud y Bienestar": 2,
        "Administración y Documentos": 3,
        "Comedor y Alimentación": 4,
        "Residencia y Habitabilidad": 5,
        "Operación y Portales": 6,
        "Maquinaria y Mantenimiento": 7,
        "Energía y Combustible": 8,
        "Almacenes y Logística": 9,
    }
    edifs_princ_ord = sorted(
        edifs_princ, key=lambda e: orden_prioridad.get(e.get("grupo", ""), 99)
    )

    # 2. Sector Principal (Vida, Administración y Talleres)
    c_princ, w_princ, h_princ = _dibujar_recinto(
        edifs_princ_ord,
        x_base,
        y_base,
        max_ancho=85.0,
        titulo=f"{nombre_camp} — PLATAFORMA OPERATIVA Y RESIDENCIAL",
        subtitulo=f"{desc_camp} · Vida, Oficinas, Talleres y Estacionamientos",
        tipo_cerco="PA14-CERCO",
        con_flecha_acceso=True,
    )
    cuerpo += c_princ

    # 3. Sector Saneamiento y Ambiental (Fuera del campamento con retiro sanitario)
    x_san = x_base + w_princ + 12.0
    c_san, w_san, h_san = _dibujar_recinto(
        edifs_san,
        x_san,
        y_base,
        max_ancho=50.0,
        titulo="SECTOR SANEAMIENTO Y AMBIENTE",
        subtitulo="Retiro Sanitario RNE OS.090 / D.Leg. 1278 (PTAP, PTAR, Lodos)",
        tipo_cerco="PA14-CERCO",
        con_flecha_acceso=False,
    )
    cuerpo += c_san

    # 4. Sector Polvorín de Superficie (Aislado a Distancia de Seguridad SUCAMEC)
    y_polv = y_base + max(h_princ, h_san) + 22.0
    c_polv, w_polv, h_polv = _dibujar_recinto(
        edifs_polv,
        x_base,
        y_polv,
        max_ancho=60.0,
        titulo="ZONA RESTRINGIDA — POLVORIN DE SUPERFICIE SUCAMEC",
        subtitulo="Distancia de Seguridad D >= 300 m (Ley N° 30299 / D.S. 024-2016-EM)",
        tipo_cerco="PA14-CERCO",
        con_flecha_acceso=False,
        es_polvorin=True,
    )
    cuerpo += c_polv

    # Línea de separación y cota de distancia de seguridad del polvorín
    cuerpo += [
        _linea(
            x_base, y_base + h_princ + 2.0, x_base, y_polv - CALLE_CAMP, "PA14-COTA"
        ),
        _texto(
            x_base + 1.0,
            (y_base + h_princ + y_polv) / 2,
            0.8,
            "<--- RETIRO NORMATIVO DE SEGURIDAD SUCAMEC (D >= 300 m) --->",
        ),
    ]

    ancho_total_camp = w_princ + 12.0 + w_san
    alto_total_camp = y_polv + h_polv - y_base
    return cuerpo, ancho_total_camp, alto_total_camp


def dibujo_campamento(camp: dict) -> Dibujo:
    edifs_c1 = [e for e in camp["edificaciones"] if e.get("campamento") == "CAMP1"]
    edifs_c2 = [e for e in camp["edificaciones"] if e.get("campamento") == "CAMP2"]

    cuerpo_1, ancho_1, _ = _dibujar_campamento_organizado(
        edifs_c1,
        0.0,
        0.0,
        "CAMPAMENTO 1 (PORTAL A - 248 PAX)",
        "Base Principal Casmas",
    )

    x2_ini = ancho_1 + 25.0
    cuerpo_2, ancho_2, _ = _dibujar_campamento_organizado(
        edifs_c2,
        x2_ini,
        0.0,
        "CAMPAMENTO 2 (PORTAL B - 98 PAX)",
        "Satélite Autónomo Huaraz",
    )

    ancho_total = x2_ini + ancho_2
    return Dibujo(
        "PA14_CAMPAMENTO",
        "Distribución de Campamentos 1 y 2 (38 Edificaciones EDIF-01 a EDIF-38)",
        cuerpo_1 + cuerpo_2,
        ancho_total,
    )


# ---------------------------------------------------------------- EDIF-01: Modular Dormitorio Staff (Plano AR-DM-001)
def _dibujar_cama(
    x: float, y: float, w: float, largo: float, cabecera: str = "NORTE"
) -> list[str]:
    cuerpo = [_rect(x, y, w, largo, "PA14-MOBILIARIO")]
    if cabecera == "NORTE":
        cuerpo += [
            _rect(x + 0.10, y + largo - 0.45, w - 0.20, 0.35, "PA14-MOBILIARIO"),
            _linea(x, y + largo - 0.70, x + w, y + largo - 0.70, "PA14-MOBILIARIO"),
            _texto_cen(x + w / 2, y + 0.50, 0.16, "CAMA", "PA14-TEXTO"),
        ]
    else:
        cuerpo += [
            _rect(x + 0.10, y + 0.10, w - 0.20, 0.35, "PA14-MOBILIARIO"),
            _linea(x, y + 0.70, x + w, y + 0.70, "PA14-MOBILIARIO"),
            _texto_cen(x + w / 2, y + largo - 0.50, 0.16, "CAMA", "PA14-TEXTO"),
        ]
    return cuerpo


def _dibujar_bano(
    x: float, y: float, w: float, largo: float, tipo: str = "TOP"
) -> list[str]:
    cuerpo = []
    if tipo == "TOP":
        cuerpo += [
            _linea(x, y + largo, x + w, y + largo, "PA14-TABIQUES"),
            _linea(x + w, y, x + w, y + largo, "PA14-TABIQUES"),
            _linea(x + 0.75, y + largo, x + 0.75, y + largo - 0.65, "PA14-PUERTAS"),
            _arco(x + 0.75, y + largo, 0.65, 270.0, 360.0, "PA14-PUERTAS"),
            _rect(x + 0.05, y + 0.05, 0.75, 0.75, "PA14-APARATOS"),
            _linea(x + 0.05, y + 0.05, x + 0.80, y + 0.80, "PA14-APARATOS"),
            _linea(x + 0.05, y + 0.80, x + 0.80, y + 0.05, "PA14-APARATOS"),
            _circulo(x + 0.425, y + 0.425, 0.04, "PA14-APARATOS"),
            _rect(x + 0.10, y + largo - 0.25, 0.45, 0.18, "PA14-APARATOS"),
            _circulo(x + 0.325, y + largo - 0.40, 0.14, "PA14-APARATOS"),
            _texto_cen(x + 0.325, y + largo - 0.40, 0.11, "WC", "PA14-TEXTO"),
            _rect(x + w - 0.35, y + 0.15, 0.30, 0.45, "PA14-APARATOS"),
            _circulo(x + w - 0.20, y + 0.375, 0.11, "PA14-APARATOS"),
            _texto_cen(x + w - 0.20, y + 0.375, 0.10, "LAV", "PA14-TEXTO"),
            _texto_cen(x + 0.40, y + 1.05, 0.15, "BANO", "PA14-TEXTO"),
        ]
    else:
        cuerpo += [
            _linea(x, y, x + w, y, "PA14-TABIQUES"),
            _linea(x + w, y, x + w, y + largo, "PA14-TABIQUES"),
            _linea(x + 0.75, y, x + 0.75, y + 0.65, "PA14-PUERTAS"),
            _arco(x + 0.75, y, 0.65, 0.0, 90.0, "PA14-PUERTAS"),
            _rect(x + 0.05, y + largo - 0.80, 0.75, 0.75, "PA14-APARATOS"),
            _linea(
                x + 0.05, y + largo - 0.80, x + 0.80, y + largo - 0.05, "PA14-APARATOS"
            ),
            _linea(
                x + 0.05, y + largo - 0.05, x + 0.80, y + largo - 0.80, "PA14-APARATOS"
            ),
            _circulo(x + 0.425, y + largo - 0.425, 0.04, "PA14-APARATOS"),
            _rect(x + 0.10, y + 0.07, 0.45, 0.18, "PA14-APARATOS"),
            _circulo(x + 0.325, y + 0.22, 0.14, "PA14-APARATOS"),
            _texto_cen(x + 0.325, y + 0.22, 0.11, "WC", "PA14-TEXTO"),
            _rect(x + w - 0.35, y + largo - 0.60, 0.30, 0.45, "PA14-APARATOS"),
            _circulo(x + w - 0.20, y + largo - 0.375, 0.11, "PA14-APARATOS"),
            _texto_cen(x + w - 0.20, y + largo - 0.375, 0.10, "LAV", "PA14-TEXTO"),
            _texto_cen(x + 0.40, y + largo - 1.05, 0.15, "BANO", "PA14-TEXTO"),
        ]
    return cuerpo


def _dibujar_ventana_horiz(
    x1: float, x2: float, y: float, esp: float = 0.15
) -> list[str]:
    return [
        _linea(x1, y - esp / 2, x2, y - esp / 2, "PA14-VENTANAS"),
        _linea(x1, y - esp / 6, x2, y - esp / 6, "PA14-VENTANAS"),
        _linea(x1, y + esp / 6, x2, y + esp / 6, "PA14-VENTANAS"),
        _linea(x1, y + esp / 2, x2, y + esp / 2, "PA14-VENTANAS"),
    ]


def _dibujar_modulo_habitacion(
    xm: float, ym: float, w: float, h: float, tipo: str, num: int, det: dict
) -> list[str]:
    w_cama = det.get("ancho_cama_m", 1.00)
    l_cama = det.get("largo_cama_m", 2.00)
    w_bano = det.get("ancho_bano_m", 1.50)
    l_bano = det.get("largo_bano_m", 1.80)
    w_closet = det.get("ancho_closet_m", 0.60)
    l_closet = det.get("largo_closet_m", 1.20)
    esp_m = det.get("espesor_muro_ext_m", 0.15)

    cuerpo = []
    if tipo == "TOP":
        cuerpo.append(_linea(xm + w, ym, xm + w, ym + h, "PA14-TABIQUES"))
        cuerpo += [
            _linea(
                xm + w_bano + 0.40, ym, xm + w_bano + 0.40, ym + 0.85, "PA14-PUERTAS"
            ),
            _arco(xm + w_bano + 0.40, ym, 0.85, 0.0, 90.0, "PA14-PUERTAS"),
        ]
        cuerpo += _dibujar_bano(xm, ym, w_bano, l_bano, "TOP")
        cuerpo += _dibujar_cama(
            xm + 0.25, ym + h - esp_m - l_cama, w_cama, l_cama, "NORTE"
        )
        cuerpo += [
            _rect(
                xm + w - l_closet - 0.20,
                ym + h - esp_m - w_closet,
                l_closet,
                w_closet,
                "PA14-MOBILIARIO",
            ),
            _linea(
                xm + w - l_closet / 2 - 0.20,
                ym + h - esp_m - w_closet,
                xm + w - l_closet / 2 - 0.20,
                ym + h - esp_m,
                "PA14-MOBILIARIO",
            ),
            _texto_cen(
                xm + w - l_closet / 2 - 0.20,
                ym + h - esp_m - w_closet / 2,
                0.15,
                "CLOSET",
                "PA14-TEXTO",
            ),
        ]
        cuerpo += [
            _rect(xm + w - 1.20, ym + 1.20, 1.00, 0.50, "PA14-MOBILIARIO"),
            _circulo(xm + w - 0.70, ym + 1.85, 0.18, "PA14-MOBILIARIO"),
            _texto_cen(xm + w - 0.70, ym + 1.45, 0.13, "MESA", "PA14-TEXTO"),
        ]
        cuerpo += _dibujar_ventana_horiz(xm + 1.00, xm + 2.50, ym + h, esp_m)
        cuerpo += [
            _texto_cen(
                xm + w / 2, ym + h / 2 - 0.20, 0.20, f"HAB-{num:02d}", "PA14-TEXTO"
            ),
            _texto_cen(xm + w / 2, ym + h / 2 - 0.50, 0.14, "STAFF", "PA14-TEXTO"),
        ]
    else:
        cuerpo.append(_linea(xm + w, ym, xm + w, ym + h, "PA14-TABIQUES"))
        cuerpo += [
            _linea(
                xm + w_bano + 0.40,
                ym + h,
                xm + w_bano + 0.40,
                ym + h - 0.85,
                "PA14-PUERTAS",
            ),
            _arco(xm + w_bano + 0.40, ym + h, 0.85, 270.0, 360.0, "PA14-PUERTAS"),
        ]
        cuerpo += _dibujar_bano(xm, ym + h - l_bano, w_bano, l_bano, "BOTTOM")
        cuerpo += _dibujar_cama(xm + 0.25, ym + esp_m, w_cama, l_cama, "SUR")
        cuerpo += [
            _rect(
                xm + w - l_closet - 0.20,
                ym + esp_m,
                l_closet,
                w_closet,
                "PA14-MOBILIARIO",
            ),
            _linea(
                xm + w - l_closet / 2 - 0.20,
                ym + esp_m,
                xm + w - l_closet / 2 - 0.20,
                ym + esp_m + w_closet,
                "PA14-MOBILIARIO",
            ),
            _texto_cen(
                xm + w - l_closet / 2 - 0.20,
                ym + esp_m + w_closet / 2,
                0.15,
                "CLOSET",
                "PA14-TEXTO",
            ),
        ]
        cuerpo += [
            _rect(xm + w - 1.20, ym + h - 1.70, 1.00, 0.50, "PA14-MOBILIARIO"),
            _circulo(xm + w - 0.70, ym + h - 1.85, 0.18, "PA14-MOBILIARIO"),
            _texto_cen(xm + w - 0.70, ym + h - 1.45, 0.13, "MESA", "PA14-TEXTO"),
        ]
        cuerpo += _dibujar_ventana_horiz(xm + 1.00, xm + 2.50, ym, esp_m)
        cuerpo += [
            _texto_cen(
                xm + w / 2, ym + h / 2 + 0.50, 0.20, f"HAB-{num:02d}", "PA14-TEXTO"
            ),
            _texto_cen(xm + w / 2, ym + h / 2 + 0.20, 0.14, "STAFF", "PA14-TEXTO"),
        ]
    return cuerpo


def _dibujar_modulo_central(xm: float, ym: float, w: float, h_tot: float) -> list[str]:
    cuerpo = []
    cuerpo.append(_linea(xm + w, ym, xm + w, ym + h_tot, "PA14-MUROS"))

    # Escalera A/B norte
    x_esc, y_esc = xm + 0.15, ym + 7.20
    w_esc, h_esc = 2.40, 4.50
    cuerpo.append(_rect(x_esc, y_esc, w_esc, h_esc, "PA14-ESCALERAS"))
    cuerpo.append(
        _linea(
            x_esc + w_esc / 2, y_esc, x_esc + w_esc / 2, y_esc + h_esc, "PA14-ESCALERAS"
        )
    )
    for i in range(1, 12):
        y_p = y_esc + i * (h_esc / 12)
        cuerpo.append(
            _linea(x_esc, y_p, x_esc + w_esc / 2 - 0.05, y_p, "PA14-ESCALERAS")
        )
        cuerpo.append(
            _linea(x_esc + w_esc / 2 + 0.05, y_p, x_esc + w_esc, y_p, "PA14-ESCALERAS")
        )
    cuerpo += [
        _linea(x_esc + 0.60, y_esc + 0.50, x_esc + 0.60, y_esc + 3.80, "PA14-EJE"),
        _linea(x_esc + 0.60, y_esc + 3.80, x_esc + 0.45, y_esc + 3.50, "PA14-EJE"),
        _linea(x_esc + 0.60, y_esc + 3.80, x_esc + 0.75, y_esc + 3.50, "PA14-EJE"),
        _texto_cen(x_esc + w_esc / 2, y_esc + 2.25, 0.22, "ESCALERA A/B", "PA14-TEXTO"),
    ]

    # Cuarto de Limpieza norte
    x_cl = xm + 2.65
    cuerpo += [
        _linea(x_cl, ym + 7.0, x_cl, ym + 12.0, "PA14-TABIQUES"),
        _linea(x_cl, ym + 7.0, x_cl, ym + 7.80, "PA14-PUERTAS"),
        _arco(x_cl, ym + 7.0, 0.80, 0.0, 90.0, "PA14-PUERTAS"),
        _rect(x_cl + 0.20, ym + 11.0, 0.80, 0.60, "PA14-APARATOS"),
        _texto_cen(x_cl + 0.60, ym + 11.30, 0.12, "VERT", "PA14-TEXTO"),
        _texto_cen(
            x_cl + (w - 2.65) / 2, ym + 9.50, 0.20, "CUARTO LIMPIEZA", "PA14-TEXTO"
        ),
    ]

    # Pasadizo central
    cuerpo += [
        _texto_cen(
            xm + w / 2, ym + 6.0, 0.28, "PASADIZO CENTRAL TERMICO 2.0m", "PA14-TEXTO"
        ),
    ]

    # Vestíbulo de Ingreso Principal sur
    cuerpo += [
        _linea(xm + 1.35, ym, xm + 1.35, ym + 0.90, "PA14-PUERTAS"),
        _arco(xm + 1.35, ym, 0.90, 0.0, 90.0, "PA14-PUERTAS"),
        _linea(xm + 3.15, ym, xm + 3.15, ym + 0.90, "PA14-PUERTAS"),
        _arco(xm + 3.15, ym, 0.90, 90.0, 180.0, "PA14-PUERTAS"),
        _linea(xm + 1.0, ym - 0.40, xm + 3.5, ym - 0.40, "PA14-CONTORNO"),
        _linea(xm + 1.0, ym - 0.80, xm + 3.5, ym - 0.80, "PA14-CONTORNO"),
        _texto_cen(xm + w / 2, ym + 2.80, 0.25, "ENTRANCE VESTIBULE", "PA14-TEXTO"),
        _texto_cen(xm + w / 2, ym + 2.20, 0.20, "ACCESO PRINCIPAL", "PA14-TEXTO"),
    ]
    return cuerpo


def _dibujar_planta_completa(xp0: float, yp0: float, det: dict) -> list[str]:
    l_tot = det.get("largo_total_m", 48.70)
    ancho_c = det.get("ancho_cuerpo_m", 12.00)
    ancho_mod = det.get("ancho_modulo_m", 3.50)
    ancho_cen = det.get("ancho_modulo_central_m", 4.50)
    esp_m = det.get("espesor_muro_ext_m", 0.15)

    cuerpo = [
        # Título de Planta
        _texto_cen(
            xp0 + l_tot / 2,
            yp0 + ancho_c + 11.5,
            0.75,
            "PLANTA NIVEL 1 - MODULAR DORMITORIO",
            "PA14-TEXTO",
        ),
        _texto_cen(xp0 + l_tot / 2, yp0 + ancho_c + 10.3, 0.45, "1:100", "PA14-TEXTO"),
        _linea(
            xp0 + l_tot / 2 - 12.0,
            yp0 + ancho_c + 9.8,
            xp0 + l_tot / 2 + 12.0,
            yp0 + ancho_c + 9.8,
            "PA14-TEXTO",
        ),
        # Muros perimetrales (doble línea)
        _rect(xp0, yp0, l_tot, ancho_c, "PA14-MUROS"),
        _rect(
            xp0 + esp_m,
            yp0 + esp_m,
            l_tot - 2 * esp_m,
            ancho_c - 2 * esp_m,
            "PA14-MUROS",
        ),
        # Pasadizo central longitudinal
        _linea(xp0, yp0 + 5.0, xp0 + l_tot, yp0 + 5.0, "PA14-MUROS"),
        _linea(xp0, yp0 + 7.0, xp0 + l_tot, yp0 + 7.0, "PA14-MUROS"),
    ]

    # Ala izquierda (6 habitaciones arriba, 6 abajo)
    for i in range(6):
        xm = xp0 + i * ancho_mod
        cuerpo += _dibujar_modulo_habitacion(
            xm, yp0 + 7.0, ancho_mod, 5.0, "TOP", i + 1, det
        )
        cuerpo += _dibujar_modulo_habitacion(
            xm, yp0, ancho_mod, 5.0, "BOTTOM", i + 13, det
        )

    # Módulo central (Escalera A/B + Cuarto Limpieza + Vestíbulo)
    xm_cen = xp0 + 6 * ancho_mod
    cuerpo += _dibujar_modulo_central(xm_cen, yp0, ancho_cen, ancho_c)

    # Ala derecha (6 habitaciones arriba, 6 abajo)
    for i in range(6):
        xm = xm_cen + ancho_cen + i * ancho_mod
        cuerpo += _dibujar_modulo_habitacion(
            xm, yp0 + 7.0, ancho_mod, 5.0, "TOP", i + 7, det
        )
        cuerpo += _dibujar_modulo_habitacion(
            xm, yp0, ancho_mod, 5.0, "BOTTOM", i + 19, det
        )

    # Módulo final de evacuación este
    xm_fin = xm_cen + ancho_cen + 6 * ancho_mod
    w_fin = l_tot - (xm_fin - xp0)
    cuerpo += [
        _linea(xp0 + l_tot, yp0 + 5.15, xp0 + l_tot + 0.90, yp0 + 5.15, "PA14-PUERTAS"),
        _arco(xp0 + l_tot, yp0 + 5.15, 0.90, 0.0, 90.0, "PA14-PUERTAS"),
        _rect(xp0 + l_tot + 0.20, yp0 + 4.50, 2.50, 3.00, "PA14-ESCALERAS"),
        _linea(
            xp0 + l_tot + 0.20,
            yp0 + 6.00,
            xp0 + l_tot + 2.70,
            yp0 + 6.00,
            "PA14-ESCALERAS",
        ),
        _texto_cen(
            xp0 + l_tot + 1.45, yp0 + 3.80, 0.22, "ESCALERA EMERGENCIA", "PA14-TEXTO"
        ),
    ]

    # Ejes estructurales y burbujas
    ejes_x = [
        (0.0, "A"),
        (3.5, "B"),
        (7.0, "C"),
        (10.5, "D"),
        (14.0, "E"),
        (17.5, "F"),
        (21.0, "G"),
        (25.5, "H"),
        (29.0, "J"),
        (32.5, "K"),
        (36.0, "L"),
        (39.5, "M"),
        (43.0, "N"),
        (46.5, "P"),
        (48.7, "Q"),
    ]
    for dx_eje, letra in ejes_x:
        x_e = xp0 + dx_eje
        cuerpo += [
            _linea(x_e, yp0 - 2.5, x_e, yp0 + ancho_c + 2.5, "PA14-EJE"),
            _circulo(x_e, yp0 + ancho_c + 3.5, 0.60, "PA14-EJE"),
            _texto_cen(x_e, yp0 + ancho_c + 3.5, 0.40, letra, "PA14-EJE"),
            _circulo(x_e, yp0 - 3.5, 0.60, "PA14-EJE"),
            _texto_cen(x_e, yp0 - 3.5, 0.40, letra, "PA14-EJE"),
        ]

    # Ejes horizontales
    ejes_y = [(0.0, "1"), (5.0, "2"), (7.0, "3"), (12.0, "4")]
    for dy_eje, num_e in ejes_y:
        y_e = yp0 + dy_eje
        cuerpo += [
            _linea(xp0 - 2.5, y_e, xp0 + l_tot + 2.5, y_e, "PA14-EJE"),
            _circulo(xp0 - 3.5, y_e, 0.60, "PA14-EJE"),
            _texto_cen(xp0 - 3.5, y_e, 0.40, num_e, "PA14-EJE"),
            _circulo(xp0 + l_tot + 3.5, y_e, 0.60, "PA14-EJE"),
            _texto_cen(xp0 + l_tot + 3.5, y_e, 0.40, num_e, "PA14-EJE"),
        ]

    # Cotas superiores
    for i in range(6):
        cuerpo.append(
            _cota(
                xp0 + i * ancho_mod,
                yp0 + ancho_c,
                xp0 + (i + 1) * ancho_mod,
                yp0 + ancho_c,
                xp0 + (i + 0.5) * ancho_mod,
                yp0 + ancho_c + 1.2,
                f"{ancho_mod:.2f}",
            )
        )
    cuerpo.append(
        _cota(
            xm_cen,
            yp0 + ancho_c,
            xm_cen + ancho_cen,
            yp0 + ancho_c,
            xm_cen + ancho_cen / 2,
            yp0 + ancho_c + 1.2,
            f"{ancho_cen:.2f}",
        )
    )
    for i in range(6):
        cuerpo.append(
            _cota(
                xm_cen + ancho_cen + i * ancho_mod,
                yp0 + ancho_c,
                xm_cen + ancho_cen + (i + 1) * ancho_mod,
                yp0 + ancho_c,
                xm_cen + ancho_cen + (i + 0.5) * ancho_mod,
                yp0 + ancho_c + 1.2,
                f"{ancho_mod:.2f}",
            )
        )
    cuerpo.append(
        _cota(
            xm_fin,
            yp0 + ancho_c,
            xp0 + l_tot,
            yp0 + ancho_c,
            (xm_fin + xp0 + l_tot) / 2,
            yp0 + ancho_c + 1.2,
            f"{w_fin:.2f}",
        )
    )
    cuerpo.append(
        _cota(
            xp0,
            yp0 + ancho_c,
            xp0 + l_tot,
            yp0 + ancho_c,
            xp0 + l_tot / 2,
            yp0 + ancho_c + 6.0,
            f"{l_tot:.2f} m",
        )
    )

    # Cotas inferiores
    cuerpo.append(
        _cota(
            xp0,
            yp0,
            xp0 + l_tot,
            yp0,
            xp0 + l_tot / 2,
            yp0 - 6.0,
            f"{l_tot:.2f} m",
        )
    )

    # Cotas verticales a la izquierda
    cuerpo += [
        _cota(xp0, yp0, xp0, yp0 + 5.0, xp0 - 1.2, yp0 + 2.5, "5.00"),
        _cota(xp0, yp0 + 5.0, xp0, yp0 + 7.0, xp0 - 1.2, yp0 + 6.0, "2.00"),
        _cota(xp0, yp0 + 7.0, xp0, yp0 + 12.0, xp0 - 1.2, yp0 + 9.5, "5.00"),
        _cota(xp0, yp0, xp0, yp0 + 12.0, xp0 - 6.0, yp0 + 6.0, f"{ancho_c:.2f} m"),
    ]

    return cuerpo


def _dibujar_seccion_aa(xs0: float, ys0: float, det: dict) -> list[str]:
    ancho_c = det.get("ancho_cuerpo_m", 12.00)
    h_pb = det.get("altura_planta_baja_m", 2.50)
    h_p1 = det.get("altura_primer_piso_m", 2.60)
    h_cercha = det.get("altura_techo_cercha_m", 1.50)
    h_tot = h_pb + h_p1 + h_cercha + 0.45  # incluye espesores de forjados

    cuerpo = [
        # Título de Sección
        _texto_cen(
            xs0 + ancho_c / 2,
            ys0 + h_tot + 6.5,
            0.75,
            "SECCION A-A'",
            "PA14-TEXTO",
        ),
        _texto_cen(xs0 + ancho_c / 2, ys0 + h_tot + 5.3, 0.45, "1:100", "PA14-TEXTO"),
        _linea(
            xs0 + ancho_c / 2 - 8.0,
            ys0 + h_tot + 4.8,
            xs0 + ancho_c / 2 + 8.0,
            ys0 + h_tot + 4.8,
            "PA14-TEXTO",
        ),
        # Terreno natural y relleno
        _linea(xs0 - 4.0, ys0, xs0 + ancho_c + 5.0, ys0, "PA14-CONTORNO"),
    ]

    # Rayado de terreno
    for i in range(20):
        xt = xs0 - 3.5 + i * 1.0
        cuerpo.append(_linea(xt, ys0, xt - 0.40, ys0 - 0.40, "PA14-HATCH"))

    # Zapatas y cimentación
    ejes_sec = [0.0, 5.0, 7.0, 12.0]
    for xc in ejes_sec:
        cuerpo += [
            _rect(xs0 + xc - 0.60, ys0 - 0.80, 1.20, 0.80, "PA14-ESTRUCTURA"),
            _rect(xs0 + xc - 0.20, ys0 - 0.30, 0.40, 0.30, "PA14-ESTRUCTURA"),
            _rect(xs0 + xc - 0.10, ys0 + 0.20, 0.20, 5.35, "PA14-ESTRUCTURA"),
        ]

    # Forjado Planta Baja y Forjado Primer Piso
    y_fpb = ys0 + 0.20
    y_fp1 = y_fpb + h_pb
    y_techo = y_fp1 + 0.25 + h_p1
    cuerpo += [
        _rect(xs0, ys0, ancho_c, 0.20, "PA14-ESTRUCTURA"),
        _rect(xs0, y_fp1, ancho_c, 0.25, "PA14-ESTRUCTURA"),
        _linea(xs0, y_fpb, xs0, y_fp1, "PA14-MUROS"),
        _linea(xs0 + 0.10, y_fpb, xs0 + 0.10, y_fp1, "PA14-MUROS"),
        _linea(xs0 + ancho_c, y_fpb, xs0 + ancho_c, y_fp1, "PA14-MUROS"),
        _linea(xs0 + ancho_c - 0.10, y_fpb, xs0 + ancho_c - 0.10, y_fp1, "PA14-MUROS"),
        _linea(xs0, y_fp1 + 0.25, xs0, y_techo, "PA14-MUROS"),
        _linea(xs0 + 0.10, y_fp1 + 0.25, xs0 + 0.10, y_techo, "PA14-MUROS"),
        _linea(xs0 + ancho_c, y_fp1 + 0.25, xs0 + ancho_c, y_techo, "PA14-MUROS"),
        _linea(
            xs0 + ancho_c - 0.10,
            y_fp1 + 0.25,
            xs0 + ancho_c - 0.10,
            y_techo,
            "PA14-MUROS",
        ),
    ]

    # Ventanas en sección
    cuerpo += [
        _rect(xs0, y_fpb + 1.0, 0.10, 1.20, "PA14-VENTANAS"),
        _rect(xs0, y_fp1 + 0.25 + 1.0, 0.10, 1.20, "PA14-VENTANAS"),
        _rect(xs0 + ancho_c - 0.10, y_fpb + 1.0, 0.10, 1.20, "PA14-VENTANAS"),
        _rect(xs0 + ancho_c - 0.10, y_fp1 + 0.25 + 1.0, 0.10, 1.20, "PA14-VENTANAS"),
    ]

    # Puertas interiores del pasadizo en elevación
    cuerpo += [
        _rect(xs0 + 5.0, y_fpb, 0.90, 2.10, "PA14-PUERTAS"),
        _rect(xs0 + 6.1, y_fpb, 0.90, 2.10, "PA14-PUERTAS"),
        _rect(xs0 + 5.0, y_fp1 + 0.25, 0.90, 2.10, "PA14-PUERTAS"),
        _rect(xs0 + 6.1, y_fp1 + 0.25, 0.90, 2.10, "PA14-PUERTAS"),
    ]

    # Cercha metálica a dos aguas
    y_cumbrera = y_techo + h_cercha
    x_cumbrera = xs0 + ancho_c / 2
    cuerpo += [
        _linea(xs0 - 1.20, y_techo, xs0 + ancho_c + 1.20, y_techo, "PA14-ESTRUCTURA"),
        _linea(xs0 - 1.20, y_techo - 0.20, x_cumbrera, y_cumbrera, "PA14-ESTRUCTURA"),
        _linea(
            x_cumbrera,
            y_cumbrera,
            xs0 + ancho_c + 1.20,
            y_techo - 0.20,
            "PA14-ESTRUCTURA",
        ),
        _linea(x_cumbrera, y_techo, x_cumbrera, y_cumbrera, "PA14-ESTRUCTURA"),
        _linea(xs0 + 3.0, y_techo, x_cumbrera, y_cumbrera, "PA14-ESTRUCTURA"),
        _linea(xs0 + 9.0, y_techo, x_cumbrera, y_cumbrera, "PA14-ESTRUCTURA"),
        _linea(
            xs0 + 3.0, y_techo, xs0 + 3.0, y_techo + h_cercha * 0.5, "PA14-ESTRUCTURA"
        ),
        _linea(
            xs0 + 9.0, y_techo, xs0 + 9.0, y_techo + h_cercha * 0.5, "PA14-ESTRUCTURA"
        ),
        _rect(xs0 - 1.40, y_techo - 0.35, 0.25, 0.20, "PA14-OBRAS-ARTE"),
        _rect(xs0 + ancho_c + 1.15, y_techo - 0.35, 0.25, 0.20, "PA14-OBRAS-ARTE"),
    ]

    # Escalera metálica de emergencia derecha
    cuerpo += [
        _rect(xs0 + ancho_c + 0.20, ys0, 2.50, y_fp1 + 0.25, "PA14-ESCALERAS"),
        _linea(
            xs0 + ancho_c + 0.20,
            ys0,
            xs0 + ancho_c + 2.70,
            y_fp1 + 0.25,
            "PA14-ESCALERAS",
        ),
        _linea(
            xs0 + ancho_c + 0.20,
            ys0 + 0.90,
            xs0 + ancho_c + 2.70,
            y_fp1 + 0.25 + 0.90,
            "PA14-ESCALERAS",
        ),
        _linea(
            xs0 + ancho_c + 2.70,
            y_fp1 + 0.25,
            xs0 + ancho_c + 2.70,
            y_fp1 + 0.25 + 1.0,
            "PA14-ESCALERAS",
        ),
    ]

    # Balcón izquierdo de servicio
    cuerpo += [
        _rect(xs0 - 1.50, y_fp1, 1.50, 0.20, "PA14-ESTRUCTURA"),
        _linea(xs0 - 1.50, y_fp1 + 0.20, xs0 - 1.50, y_fp1 + 1.10, "PA14-ESTRUCTURA"),
        _linea(xs0 - 1.50, y_fp1 + 1.10, xs0, y_fp1 + 1.10, "PA14-ESTRUCTURA"),
    ]

    # Textos de detalle y especificación
    cuerpo += [
        _texto(
            x_cumbrera + 0.50,
            y_cumbrera + 0.50,
            0.24,
            "TECHO A DOS AGUAS",
            "PA14-TEXTO",
        ),
        _texto(
            x_cumbrera + 0.50,
            y_cumbrera + 0.10,
            0.22,
            "CANALON ANTI-HIELO",
            "PA14-TEXTO",
        ),
        _texto(
            xs0 + ancho_c + 3.0,
            y_fp1 + 1.5,
            0.24,
            "ESCALERA METALICA EMERGENCIA",
            "PA14-TEXTO",
        ),
        _texto(xs0 + ancho_c + 3.0, y_fp1 + 0.25, 0.20, "FORJADO", "PA14-TEXTO"),
        _texto(
            xs0 + ancho_c + 3.0,
            ys0 - 0.40,
            0.20,
            "CIMENTACION SUPERFICIAL",
            "PA14-TEXTO",
        ),
        _texto(
            xs0 - 4.5, y_fpb + 1.6, 0.20, "VENTANA DOBLE ACRISTALAMIENTO", "PA14-TEXTO"
        ),
        _texto(
            xs0 + 1.0,
            ys0 + h_tot + 2.5,
            0.24,
            "DETALLE MURO: Panel Sandwich 100mm Poliuretano",
            "PA14-TEXTO",
        ),
    ]

    # Cotas verticales a la izquierda
    cuerpo += [
        _cota(
            xs0, y_fpb, xs0, y_fp1, xs0 - 1.2, (y_fpb + y_fp1) / 2, f"PB: {h_pb:.2f} m"
        ),
        _cota(
            xs0,
            y_fp1 + 0.25,
            xs0,
            y_techo,
            xs0 - 1.2,
            (y_fp1 + 0.25 + y_techo) / 2,
            f"P1: {h_p1:.2f} m",
        ),
        _cota(
            xs0,
            y_techo,
            xs0,
            y_cumbrera,
            xs0 - 1.2,
            (y_techo + y_cumbrera) / 2,
            f"{h_cercha:.2f} m",
        ),
        _cota(
            xs0,
            ys0,
            xs0,
            y_cumbrera,
            xs0 - 2.8,
            (ys0 + y_cumbrera) / 2,
            f"Total H: {h_tot:.2f} m",
        ),
    ]

    # Cotas horizontales inferiores
    cuerpo += [
        _cota(xs0, ys0, xs0 + 5.0, ys0, xs0 + 2.5, ys0 - 1.4, "5.00"),
        _cota(xs0 + 5.0, ys0, xs0 + 7.0, ys0, xs0 + 6.0, ys0 - 1.4, "2.00"),
        _cota(xs0 + 7.0, ys0, xs0 + 12.0, ys0, xs0 + 9.5, ys0 - 1.4, "5.00"),
        _cota(xs0 + 12.0, ys0, xs0 + 14.5, ys0, xs0 + 13.25, ys0 - 1.4, "2.50"),
        _cota(xs0, ys0, xs0 + 12.0, ys0, xs0 + 6.0, ys0 - 2.4, f"{ancho_c:.2f} m"),
    ]

    return cuerpo


def _dibujar_lamina_y_membrete(w_sheet: float, h_sheet: float, det: dict) -> list[str]:
    cuerpo = [
        # Marco exterior de lámina
        _rect(0.0, 0.0, w_sheet, h_sheet, "PA14-MEMBRETE"),
        # Margen interior
        _rect(1.5, 1.5, w_sheet - 3.0, h_sheet - 3.0, "PA14-MEMBRETE"),
    ]

    # Norte Magnético (esquina superior izquierda)
    xn, yn = 8.0, h_sheet - 7.0
    cuerpo += [
        _circulo(xn, yn, 2.2, "PA14-SIMBOLOS"),
        _circulo(xn, yn, 1.9, "PA14-SIMBOLOS"),
        _linea(xn, yn - 2.1, xn, yn + 2.1, "PA14-SIMBOLOS"),
        _linea(xn - 2.1, yn, xn + 2.1, yn, "PA14-SIMBOLOS"),
        _linea(xn - 0.40, yn + 1.20, xn, yn + 2.10, "PA14-SIMBOLOS"),
        _linea(xn + 0.40, yn + 1.20, xn, yn + 2.10, "PA14-SIMBOLOS"),
        _linea(xn - 0.40, yn + 1.20, xn + 0.40, yn + 1.20, "PA14-SIMBOLOS"),
        _texto_cen(xn, yn + 2.80, 0.60, "N", "PA14-SIMBOLOS"),
    ]

    # Sellos de Seguridad SSOMA (esquina superior derecha)
    cuerpo += [
        _circulo(w_sheet - 6.0, h_sheet - 6.0, 1.5, "PA14-SIMBOLOS"),
        _texto_cen(w_sheet - 6.0, h_sheet - 6.0, 0.35, "EPP", "PA14-SIMBOLOS"),
        _circulo(w_sheet - 6.0, h_sheet - 9.8, 1.5, "PA14-SIMBOLOS"),
        _texto_cen(w_sheet - 6.0, h_sheet - 9.8, 0.35, "SSOMA", "PA14-SIMBOLOS"),
    ]

    # Membrete Técnico Profesional (esquina inferior derecha)
    xm, ym, wm, hm = 38.5, 1.5, 26.0, 11.0
    cuerpo += [
        _rect(xm, ym, wm, hm, "PA14-MEMBRETE"),
        _linea(xm, ym + 8.5, xm + wm, ym + 8.5, "PA14-MEMBRETE"),
        _linea(xm, ym + 6.0, xm + wm, ym + 6.0, "PA14-MEMBRETE"),
        _linea(xm, ym + 3.8, xm + wm, ym + 3.8, "PA14-MEMBRETE"),
        _linea(xm, ym + 1.8, xm + wm, ym + 1.8, "PA14-MEMBRETE"),
        _linea(xm + 13.0, ym + 1.8, xm + 13.0, ym + 3.8, "PA14-MEMBRETE"),
        _linea(xm + 13.0, ym + 3.8, xm + 13.0, ym + 6.0, "PA14-MEMBRETE"),
        _texto(xm + 0.5, ym + 10.2, 0.22, "PROYECTO", "PA14-TEXTO"),
        _texto(
            xm + 0.5,
            ym + 9.2,
            0.32,
            "ALOJAMIENTO MODULAR MINA ALTITUD 3,850m",
            "PA14-TEXTO",
        ),
        _texto(xm + 0.5, ym + 7.7, 0.20, "UBICACION", "PA14-TEXTO"),
        _texto(
            xm + 0.5,
            ym + 6.8,
            0.30,
            "ANDES, PERU (TUNEL TRASANDINO CASMAS - HUARAZ PA14)",
            "PA14-TEXTO",
        ),
        _texto(xm + 0.5, ym + 5.2, 0.20, "PLANO", "PA14-TEXTO"),
        _texto(
            xm + 0.5,
            ym + 4.3,
            0.30,
            "PLANTA NIVEL 1 Y SECCION A-A'",
            "PA14-TEXTO",
        ),
        _texto(xm + 0.5, ym + 2.8, 0.20, "ESCALA: 1:100", "PA14-TEXTO"),
        _texto(xm + 13.5, ym + 2.8, 0.20, "FECHA: NOV 2026", "PA14-TEXTO"),
        _texto(xm + 0.5, ym + 2.2, 0.18, "DIBUJADO: J. VARGAS", "PA14-TEXTO"),
        _texto(xm + 13.5, ym + 2.2, 0.18, "APROBADO: M. RUIZ", "PA14-TEXTO"),
        _texto(xm + 0.5, ym + 0.8, 0.22, "NO. PLANO:", "PA14-TEXTO"),
        _texto(
            xm + 8.5,
            ym + 0.6,
            0.45,
            det.get("codigo_plano", "AR-DM-001")
            + " "
            + det.get("revision_plano", "REV B"),
            "PA14-TEXTO",
        ),
    ]

    return cuerpo


def dibujo_camp1_edif01_dormitorio(camp: dict) -> Dibujo:
    det = camp.get("edif01_detalle", {})
    w_sheet, h_sheet = 66.0, 96.0

    xp0, yp0 = 7.0, 52.0
    xs0, ys0 = 24.0, 16.0

    cuerpo_lamina = _dibujar_lamina_y_membrete(w_sheet, h_sheet, det)
    cuerpo_planta = _dibujar_planta_completa(xp0, yp0, det)
    cuerpo_seccion = _dibujar_seccion_aa(xs0, ys0, det)

    cuerpo_total = cuerpo_lamina + cuerpo_planta + cuerpo_seccion
    return Dibujo(
        "PA14_CAMP1_EDIF01_DORMITORIO",
        "Plano Arquitectonico Modular Dormitorio Staff (Planta Nivel 1 y Seccion A-A' - AR-DM-001 REV B)",
        cuerpo_total,
        w_sheet + 2.0,
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
        dibujo_camp1_edif01_dormitorio(ctx["campamento"]),
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
        + ", PA14_CAMP1_DORMITORIO, PA14_EDIF01, PA14_TODO",
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
        if d.comando == "PA14_CAMP1_EDIF01_DORMITORIO":
            lineas += [
                "(defun c:PA14_CAMP1_DORMITORIO () (c:PA14_CAMP1_EDIF01_DORMITORIO))",
                "(defun c:PA14_EDIF01 () (c:PA14_CAMP1_EDIF01_DORMITORIO))",
            ]
        todo += [f"  (pa14:origen {_n(ox)} {_n(oy)})", f"  ({nombre})"]
    todo += [
        "  (pa14:fin))",
        '(princ "\\nPA14 cargado. Escriba PA14_TODO o PA14_CAMP1_EDIF01_DORMITORIO.")',
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
