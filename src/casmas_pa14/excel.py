"""Escritura de libros Excel con formato uniforme y simple."""

from datetime import date, timedelta
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet

from .modelo import Gantt, Libro, Tabla

_RELLENO_ENCABEZADO = PatternFill("solid", fgColor="1F4E78")
_RELLENO_GANTT = PatternFill("solid", fgColor="2E75B6")
_FUENTE_ENCABEZADO = Font(bold=True, color="FFFFFF")
_LINEA = Side(style="thin", color="A6A6A6")
_BORDE = Border(left=_LINEA, right=_LINEA, top=_LINEA, bottom=_LINEA)
_FILA_INICIAL = 4


def escribir_libro(libro: Libro, carpeta: Path, proyecto: str) -> Path:
    """Crea `carpeta/libro.archivo` con una pestaña por cada Hoja."""
    wb = Workbook()
    wb.remove(wb.active)
    for hoja in libro.hojas:
        ws = wb.create_sheet(hoja.nombre[:31])
        ws["A1"] = proyecto
        ws["A1"].font = Font(bold=True, size=13)
        ws["A2"] = hoja.titulo
        ws["A2"].font = Font(bold=True, size=11, color="1F4E78")
        fila = _FILA_INICIAL
        for tabla in hoja.tablas:
            fila = _escribir_tabla(ws, tabla, fila) + 1
        columnas_gantt = _escribir_gantt(ws, hoja.gantt, fila) if hoja.gantt else []
        _ajustar_anchos(ws)
        for letra in columnas_gantt:
            ws.column_dimensions[letra].width = 4
    carpeta.mkdir(parents=True, exist_ok=True)
    ruta = carpeta / libro.archivo
    wb.save(ruta)
    return ruta


def _escribir_tabla(ws: Worksheet, tabla: Tabla, fila: int) -> int:
    if tabla.titulo:
        ws.cell(fila, 1, tabla.titulo).font = Font(bold=True)
        fila += 1
    for col, nombre in enumerate(tabla.columnas, start=1):
        _encabezado(ws.cell(fila, col, nombre))
    for datos in tabla.filas:
        fila += 1
        for col, valor in enumerate(datos, start=1):
            _celda(ws.cell(fila, col), valor)
    return fila + 1


def _escribir_gantt(ws: Worksheet, gantt: Gantt, fila: int) -> list[str]:
    fin_total = max(fin for _, _, fin in gantt.actividades)
    semanas = (fin_total - gantt.inicio).days // 7 + 1
    fijas = ["Actividad", "Inicio", "Fin", "Días"]
    for col, nombre in enumerate(fijas + [f"S{i + 1}" for i in range(semanas)], 1):
        _encabezado(ws.cell(fila, col, nombre))
    for nombre, inicio, fin in gantt.actividades:
        fila += 1
        for col, valor in enumerate([nombre, inicio, fin, (fin - inicio).days + 1], 1):
            _celda(ws.cell(fila, col), valor)
        for i in range(semanas):
            sem_ini = gantt.inicio + timedelta(days=7 * i)
            celda = ws.cell(fila, len(fijas) + 1 + i)
            celda.border = _BORDE
            if inicio <= sem_ini + timedelta(days=6) and fin >= sem_ini:
                celda.fill = _RELLENO_GANTT
    return [get_column_letter(len(fijas) + 1 + i) for i in range(semanas)]


def _encabezado(celda) -> None:
    celda.fill = _RELLENO_ENCABEZADO
    celda.font = _FUENTE_ENCABEZADO
    celda.border = _BORDE
    celda.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)


def _celda(celda, valor) -> None:
    if isinstance(valor, bool):
        valor = "Sí" if valor else "No"
    celda.value = valor
    celda.border = _BORDE
    if isinstance(valor, float):
        celda.number_format = "#,##0.00"
    elif isinstance(valor, int):
        celda.number_format = "#,##0"
    elif isinstance(valor, date):
        celda.number_format = "dd/mm/yyyy"


def _ajustar_anchos(ws: Worksheet) -> None:
    anchos: dict[int, int] = {}
    for fila in ws.iter_rows(min_row=_FILA_INICIAL):
        for celda in fila:
            if celda.value is None:
                continue
            largo = (
                11 if isinstance(celda.value, date | float) else len(str(celda.value))
            )
            anchos[celda.column] = max(anchos.get(celda.column, 0), largo)
    for col, largo in anchos.items():
        ws.column_dimensions[get_column_letter(col)].width = min(max(largo + 2, 8), 60)
