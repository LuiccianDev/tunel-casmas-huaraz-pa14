"""Escritura de memorias de cálculo en Markdown (solo presentación, sin cálculos)."""

from pathlib import Path

from .modelo import Memoria, Tabla


def _valor(v) -> str:
    """Formato de celda: floats con 3 decimales significativos, bool como Sí/No."""
    if isinstance(v, bool):
        return "Sí" if v else "No"
    if isinstance(v, float):
        return f"{v:,.3f}".rstrip("0").rstrip(".")
    return str(v).replace("|", "/")


def _tabla(t: Tabla) -> list[str]:
    lineas = [f"**{t.titulo}**", ""] if t.titulo else []
    lineas.append("| " + " | ".join(t.columnas) + " |")
    lineas.append("|" + "---|" * len(t.columnas))
    lineas += ["| " + " | ".join(_valor(v) for v in f) + " |" for f in t.filas]
    return [*lineas, ""]


def escribir_memoria(m: Memoria, carpeta: Path, proyecto: str) -> Path:
    """Crea `carpeta/m.archivo` con título, secciones, párrafos y tablas."""
    lineas = [
        f"# {m.titulo}",
        "",
        f"> {proyecto} · Generado con `uv run pa14` desde `datos/parametros.toml`. "
        "**No editar a mano.**",
        "",
    ]
    for titulo, bloques in m.secciones:
        lineas += [f"## {titulo}", ""]
        for b in bloques:
            lineas += _tabla(b) if isinstance(b, Tabla) else [b, ""]
    carpeta.mkdir(parents=True, exist_ok=True)
    ruta = carpeta / m.archivo
    ruta.write_text("\n".join(lineas), encoding="utf-8")
    return ruta
