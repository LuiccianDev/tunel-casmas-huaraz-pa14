"""Arnés de Calidad en Código Fuente: Validación de Libros, Hojas y Fórmulas Excel en Memoria.

Audita directamente la lógica de los módulos en src/casmas_pa14/modulos/ y src/casmas_pa14/excel.py
sin requerir ni depender de archivos preexistentes en la carpeta salidas/.
"""

import re
from pathlib import Path
from typing import Any

import pytest

from casmas_pa14.config import PARAMETROS, cargar_parametros
from casmas_pa14.excel import _resolver_formulas, escribir_libro
from casmas_pa14.main import MODULOS
from casmas_pa14.modelo import COLUMNAS_PARAMETRO, Libro


class DummyCelda:
    """Simula una celda de openpyxl para pruebas unitarias de fórmulas en memoria."""

    def __init__(self, valor: Any = None) -> None:
        self.value = valor
        self.number_format = "General"


def test_arnes_resolver_formulas_detecta_simbolo_no_resuelto():
    """El compilador de fórmulas debe fallar si un símbolo no existe en mapa_simbolos."""
    celda = DummyCelda()
    celdas_formulas = [(celda, "={SIMBOLO_INEXISTENTE}*2+1")]
    mapa_rangos: dict[str, str] = {}
    mapa_simbolos = {"OTRO_SIMBOLO": "C10"}

    with pytest.raises(
        ValueError, match="Fórmula contiene símbolos o tokens no resueltos"
    ):
        _resolver_formulas(celdas_formulas, mapa_rangos, mapa_simbolos)


def test_arnes_resolver_formulas_sustitucion_correcta():
    """Verifica la resolución exitosa en memoria de rangos y símbolos."""
    celda1 = DummyCelda()
    celda2 = DummyCelda()
    celdas_formulas = [
        (celda1, "=SUM({RANGO_COSTOS})"),
        (celda2, "={Q_DISP}*{FACTOR_SEG}"),
    ]
    mapa_rangos = {"RANGO_COSTOS": "D5:D15"}
    mapa_simbolos = {"Q_DISP": "C8", "FACTOR_SEG": "C9"}

    _resolver_formulas(celdas_formulas, mapa_rangos, mapa_simbolos)
    assert celda1.value == "=SUM(D5:D15)"
    assert celda2.value == "=C8*C9"


def test_arnes_modulos_generan_libros_validos_en_memoria(tmp_path: Path):
    """Audita todos los módulos de main.MODULOS en orden de dependencias.

    Garantiza:
    1. Retorno de objeto Libro válido con archivo .xlsx.
    2. Nombres de hojas válidos (1 a 31 caracteres, no vacíos ni duplicados).
    3. Tablas consistentes con columnas de tipo string no vacías.
    4. Cero tokens huérfanos o sintaxis rota en fórmulas dinámicas.
    5. Serialización limpia en tmp_path sin excepciones de openpyxl.
    """
    p = cargar_parametros(PARAMETROS)
    ctx: dict[str, Any] = {}

    assert len(MODULOS) >= 10, (
        "Deben estar registrados al menos los módulos base del proyecto."
    )

    for modulo in MODULOS:
        nombre_mod = modulo.__name__.split(".")[-1]
        clave = getattr(modulo, "CLAVE", "")
        assert clave, f"El módulo {nombre_mod} debe definir su atributo CLAVE."

        resultado = modulo.calcular(p, ctx)
        assert isinstance(resultado, dict), (
            f"El módulo {nombre_mod}.calcular() debe retornar un diccionario."
        )
        ctx[clave] = resultado

        libro = modulo.libro(resultado, p)
        assert isinstance(libro, Libro), (
            f"El módulo {nombre_mod}.libro() debe retornar un objeto Libro."
        )
        assert libro.archivo.endswith(".xlsx"), (
            f"El archivo del libro en {nombre_mod} debe terminar en .xlsx (recibido: {libro.archivo})."
        )
        assert len(libro.hojas) > 0, (
            f"El libro de {nombre_mod} debe contener al menos una hoja."
        )

        nombres_hojas: set[str] = set()
        for hoja in libro.hojas:
            nombre = hoja.nombre.strip()
            assert nombre, f"Hoja con nombre vacío encontrada en {nombre_mod}."
            assert len(nombre) <= 31, (
                f"El nombre de hoja '{nombre}' en {nombre_mod} supera el límite de 31 caracteres de Excel."
            )
            assert nombre not in nombres_hojas, (
                f"Nombre de hoja duplicado '{nombre}' en el libro de {nombre_mod}."
            )
            nombres_hojas.add(nombre)

            for idx_t, tabla in enumerate(hoja.tablas):
                assert len(tabla.columnas) > 0, (
                    f"Tabla {idx_t} en hoja '{nombre}' ({nombre_mod}) no tiene columnas."
                )
                assert all(isinstance(c, str) and c.strip() for c in tabla.columnas), (
                    f"Columnas inválidas en tabla {idx_t} de hoja '{nombre}' ({nombre_mod})."
                )

                # Auditoría de tabla_parametros:
                if tabla.columnas == COLUMNAS_PARAMETRO:
                    for fila in tabla.filas:
                        assert len(fila) >= 5, (
                            f"Fila incompleta en tabla_parametros ({nombre_mod}/{nombre}): {fila}"
                        )
                        val = fila[2]
                        # Si la fuente o el valor indican fórmula dinámica:
                        if isinstance(val, str) and val.startswith("="):
                            # Verificar que no contenga tokens rotos
                            tokens_rotos = re.findall(r"\{[^{}]*\}", val)
                            for token in tokens_rotos:
                                assert re.match(r"^\{[A-Za-z0-9_]+\}$", token), (
                                    f"Token con sintaxis rota '{token}' en valor de {nombre_mod}: {val}"
                                )

        # Serialización en directorio temporal para probar compilación del motor Excel
        nombre_proy = p.get("proyecto", {}).get("nombre", "PA14 Test")
        ruta_salida = escribir_libro(libro, tmp_path, nombre_proy)
        assert ruta_salida.exists(), (
            f"No se pudo escribir el libro de {nombre_mod} en {tmp_path}."
        )
        assert ruta_salida.stat().st_size > 0, (
            f"El libro generado de {nombre_mod} está vacío."
        )
