"""Convierte incrementalmente los archivos PDF de `docs/entradas/` a Markdown (`.md`) con MarkItDown.

Solo procesa los PDFs nuevos o modificados cuyo par `.md` no exista o sea más antiguo,
a menos que se pase el argumento `--force`.

Uso:
    uv run --with "markitdown[pdf]" python scripts/utils/convertir_pdfs.py
    uv run --with "markitdown[pdf]" python scripts/utils/convertir_pdfs.py --force
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
CARPETA_ENTRADAS = RAIZ / "docs" / "entradas"


def limpiar_markdown(texto: str) -> str:
    """Elimina tablas vacías residuales de bordes de página y exceso de saltos de línea."""
    lineas_limpias = []
    for linea in texto.splitlines():
        if re.match(r"^\|\s*(\|\s*)+$", linea) or re.match(
            r"^\|\s*(---\s*\|\s*)+$", linea
        ):
            continue
        lineas_limpias.append(linea)
    resultado = "\n".join(lineas_limpias)
    return re.sub(r"\n{3,}", "\n\n", resultado).strip() + "\n"


def sincronizar_pdfs(forzar: bool = False) -> list[Path]:
    """Busca PDFs en `docs/entradas/` y genera su `.md` si falta o está desactualizado."""
    pdfs = sorted(CARPETA_ENTRADAS.glob("*.pdf"))
    pendientes = []
    for pdf in pdfs:
        md_destino = pdf.with_suffix(".md")
        if (
            forzar
            or not md_destino.exists()
            or pdf.stat().st_mtime > md_destino.stat().st_mtime
        ):
            pendientes.append((pdf, md_destino))

    if not pendientes:
        print(
            f"[OK] Todos los PDFs ({len(pdfs)}) en docs/entradas/ ya tienen su .md actualizado."
        )
        return []

    from markitdown import MarkItDown

    convertidor = MarkItDown()
    convertidos = []
    for pdf, md_destino in pendientes:
        print(f"Convirtiendo {pdf.name} -> {md_destino.name} ...")
        res = convertidor.convert(str(pdf))
        texto_limpio = limpiar_markdown(res.text_content)
        md_destino.write_text(texto_limpio, encoding="utf-8")
        convertidos.append(md_destino)
        print(f"  ✔ {md_destino.name} ({len(texto_limpio):,} caracteres)")
    return convertidos


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    forzar_flag = "--force" in sys.argv
    sincronizar_pdfs(forzar=forzar_flag)
