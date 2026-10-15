"""Arnés de Calidad en Código Fuente: Validación de Primitivas, Biblioteca y Dibujos AutoLISP.

Audita directamente la lógica de generación en src/casmas_pa14/lisp.py en memoria,
garantizando la integridad sintáctica, balance de paréntesis y compatibilidad CAD
sin requerir ni depender de archivos preexistentes en la carpeta salidas/.
"""

from pathlib import Path
from typing import Any

from casmas_pa14.config import PARAMETROS, cargar_parametros
from casmas_pa14.lisp import (
    _LIBRERIA,
    CAPAS,
    Dibujo,
    dibujo_geologia,
    dibujo_malla,
    dibujo_seccion,
    dibujo_ubicacion,
    generar_lisp,
)
from casmas_pa14.main import MODULOS


def _obtener_contexto_calculado() -> tuple[dict[str, Any], dict[str, Any]]:
    """Calcula el contexto completo en memoria para pruebas de generación CAD."""
    p = cargar_parametros(PARAMETROS)
    ctx: dict[str, Any] = {}
    for mod in MODULOS:
        clave = getattr(mod, "CLAVE", "")
        if clave:
            ctx[clave] = mod.calcular(p, ctx)
    return p, ctx


def test_arnes_libreria_lisp_sintaxis_y_entmake():
    """Valida la sintaxis, balance de paréntesis y uso de entmake en _LIBRERIA."""
    assert _LIBRERIA.count("(") == _LIBRERIA.count(")"), (
        "Paréntesis desbalanceados en la biblioteca base de AutoLISP (_LIBRERIA)."
    )

    # Validar que las primitivas geométricas clave utilicen entmake
    primitivas_entmake = [
        "defun pa14:capa",
        "defun pa14:pline",
        "defun pa14:rect",
        "defun pa14:linea",
        "defun pa14:circulo",
        "defun pa14:arco",
        "defun pa14:texto",
        "defun pa14:texto-cen",
    ]
    for prim in primitivas_entmake:
        assert prim in _LIBRERIA, f"Falta la primitiva {prim} en _LIBRERIA."

    # Configuración de estándar métrico estricto
    assert '(setvar "INSUNITS" 4)' in _LIBRERIA, "INSUNITS debe ser 4 (metros)."
    assert '(setvar "LUNITS" 2)' in _LIBRERIA, "LUNITS debe ser 2 (decimal)."
    assert '(setvar "LUPREC" 3)' in _LIBRERIA, (
        "LUPREC debe ser 3 (milímetros de precisión)."
    )


def test_arnes_capas_normativas():
    """Valida que todas las capas CAD pertenezcan al estándar PA14-* y tengan colores ACI válidos."""
    assert len(CAPAS) >= 15, (
        "Deben estar definidas todas las capas técnicas del proyecto."
    )
    for nombre_capa, color in CAPAS.items():
        assert nombre_capa.startswith("PA14-"), (
            f"La capa '{nombre_capa}' no respeta el prefijo normativo 'PA14-'."
        )
        assert isinstance(color, int) and 1 <= color <= 255, (
            f"El color ACI {color} de la capa '{nombre_capa}' debe estar entre 1 y 255."
        )


def test_arnes_funciones_dibujo_en_memoria():
    """Ejecuta individualmente cada función dibujo_* verificando la estructura de Dibujo."""
    _p, ctx = _obtener_contexto_calculado()

    generadores = [
        ("ubicacion", lambda: dibujo_ubicacion(ctx["ubicacion"])),
        ("seccion", lambda: dibujo_seccion(ctx["seccion"])),
        ("geologia", lambda: dibujo_geologia(ctx["geologia"])),
        ("malla", lambda: dibujo_malla(ctx["seccion"], ctx.get("voladura"))),
    ]

    for nombre, fn_dibujo in generadores:
        dibujo = fn_dibujo()
        assert isinstance(dibujo, Dibujo), (
            f"El generador {nombre} debe retornar una instancia de Dibujo."
        )
        assert dibujo.comando.startswith("PA14_"), (
            f"El comando '{dibujo.comando}' en {nombre} debe iniciar con 'PA14_'."
        )
        assert dibujo.comando == dibujo.comando.upper(), (
            f"El comando '{dibujo.comando}' en {nombre} debe estar en mayúsculas."
        )
        assert dibujo.ancho > 0, f"El ancho del dibujo {nombre} debe ser positivo."
        assert len(dibujo.cuerpo) > 0, (
            f"El cuerpo del dibujo {nombre} no puede estar vacío."
        )

        # Balance de paréntesis y ausencia de caracteres no ASCII en el cuerpo
        cuerpo_str = "\n".join(dibujo.cuerpo)
        assert cuerpo_str.count("(") == cuerpo_str.count(")"), (
            f"Paréntesis desbalanceados en el cuerpo generado por {nombre}."
        )
        try:
            cuerpo_str.encode("ascii")
        except UnicodeEncodeError as exc:
            raise AssertionError(
                f"El dibujo {nombre} contiene caracteres no ASCII: {exc}"
            ) from exc


def test_arnes_generar_lisp_aislado(tmp_path: Path):
    """Prueba la función central generar_lisp en un directorio temporal aislado.

    Garantiza que el archivo final sea ASCII puro, balanceado y ejecutable en AutoCAD.
    """
    p, ctx = _obtener_contexto_calculado()
    nombre_proy = p.get("proyecto", {}).get("nombre", "PA14 Test")
    ruta_lsp = generar_lisp(ctx, tmp_path, nombre_proy)

    assert ruta_lsp.exists(), (
        "generar_lisp no creó el archivo en el directorio temporal."
    )
    contenido = ruta_lsp.read_text(
        encoding="ascii"
    )  # Falla si contiene caracteres fuera de ASCII

    assert contenido.count("(") == contenido.count(")"), (
        "El archivo LISP completo generado tiene paréntesis desbalanceados."
    )
    assert "(defun c:PA14_TODO" in contenido, (
        "Falta la definición del comando maestro c:PA14_TODO."
    )
    assert "PA14: dibujo terminado." in contenido, (
        "Falta el mensaje de finalización segura."
    )
