"""Script para la descarga y exportación segura en modo solo lectura
de los archivos de Google Drive (UNIDAD 2) al repositorio local.
Garantiza cero modificaciones en Google Drive.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

GDRIVE_CLI = (
    r"C:\Users\DAVID\.gemini\config\plugins\gdrive\skills\gdrive\scripts\gdrive.cmd"
)
OUTPUT_DIR = Path("docs/entradas/drive_unidad2")

ARCHIVOS_MANIFEST = [
    # Binarios (.xlsx directos)
    {
        "id": "1lzhXHQvGIcmt5F7GhP8Sr_0J3VTQxLny",
        "nombre": "coordenadas_utm_tunel.xlsx",
        "tipo": "download",
        "dominio": "Ubicacion y Geodesia",
    },
    {
        "id": "1LKo5grbDMbr5QdpeSUCYH5g2oa9HjnHJ",
        "nombre": "geomecanica_portal.xlsx",
        "tipo": "download",
        "dominio": "Geomecanica Portal",
    },
    {
        "id": "1TwFMUmf6x_XEYKtXGJbfIlz7sBn6HOBs",
        "nombre": "angulo_banquetas_qslope.xlsx",
        "tipo": "download",
        "dominio": "Estabilidad Taludes Q-slope",
    },
    {
        "id": "1GKwDcfNkIKsXb19kBsTx7bcTjsK70ba2",
        "nombre": "malla_1_disparo.xlsx",
        "tipo": "download",
        "dominio": "Perforacion y Voladura",
    },
    {
        "id": "1fmvD9j6vt7ck2Ehe9FDhQ0I8WW1r2kQ_",
        "nombre": "malla_2_alivio.xlsx",
        "tipo": "download",
        "dominio": "Perforacion y Voladura",
    },
    {
        "id": "1g1p8uX4qho_d6sqxNQorLwpstGRbSnJM",
        "nombre": "progresivas_unidades_geologicas.xlsx",
        "tipo": "download",
        "dominio": "Geologia y Trazado",
    },
    {
        "id": "1NVqWEkHN2DZvVoEFiwsoUurbljQP087h",
        "nombre": "rendimientos_equipos.xlsx",
        "tipo": "download",
        "dominio": "Rendimientos de Flota",
    },
    {
        "id": "1Piyj7nNlarAFUhqjRtpEpq59M6uF1DjL",
        "nombre": "ciclo_carguio_acarreo.xlsx",
        "tipo": "download",
        "dominio": "Carguio y Acarreo",
    },
    {
        "id": "1iGFpU3zw8QzjCQTFq-TZpJFMg9fEQPi9",
        "nombre": "tiempos_vias_acceso.xlsx",
        "tipo": "download",
        "dominio": "Tiempos y Accesos",
    },
    # Google Sheets (exportación a .xlsx)
    {
        "id": "1pJ3qQnuhieGWgvnHXgyiWn-f5ViYLTjiePYm2dVGb3M",
        "nombre": "diseno_voladura_modelo_matematico_konya.xlsx",
        "tipo": "export",
        "dominio": "Voladura Konya",
    },
    {
        "id": "1zOyNlzrxZZRYssSwzLJIHF21G55R_9whUUW45qSPHl4",
        "nombre": "catalogo_tecnico_explosivos.xlsx",
        "tipo": "export",
        "dominio": "Explosivos y Detonacion",
    },
    {
        "id": "1arW5QsWjCDrVcqNq1inpaS-034rFII0oOb1bWf5oPug",
        "nombre": "diseno_sostenimiento_fronton.xlsx",
        "tipo": "export",
        "dominio": "Sostenimiento Fronton",
    },
    {
        "id": "1MdplFahB9IX9JxW7eoGDXBh-_8y8sUBVZ2zHAhRcwg0",
        "nombre": "voladura_afrontonamiento.xlsx",
        "tipo": "export",
        "dominio": "Voladura Afrontonamiento",
    },
    {
        "id": "1arR4Q02xLxwMEgh_1Y2b5tzdX2gYUr82ckDVcqs_KuI",
        "nombre": "calculo_carguio_acarreo_tunel.xlsx",
        "tipo": "export",
        "dominio": "Carguio y Acarreo",
    },
    {
        "id": "1pKBR5RnocvIv4GTqPsC3_H-7og30oqiMSh2DFVAzC3U",
        "nombre": "diseno_accesos_banquetas_mov_tierra.xlsx",
        "tipo": "export",
        "dominio": "Movimiento de Tierras",
    },
    {
        "id": "17aCWjuscQhD6EeDudXmKORD7VwV0fsbSjIgqmAvOrng",
        "nombre": "maquinaria_rendimiento_equipos.xlsx",
        "tipo": "export",
        "dominio": "Maquinaria y Rendimiento",
    },
    {
        "id": "1Qdyk_2IgjNaHaa__BIS9Z2WUQQD_DzNAOt4SXtv8YKc",
        "nombre": "dimensiones_assembly_accesos.xlsx",
        "tipo": "export",
        "dominio": "Assemblies y Secciones Accesos",
    },
    {
        "id": "1TDm5EWEHaFlmOybf2TBsBH6KGz1kGJ3U324AoG8Igu4",
        "nombre": "mov_tierra_acceso_banquetas.xlsx",
        "tipo": "export",
        "dominio": "Accesos a Banquetas",
    },
    {
        "id": "1HbAXZ_-4mMmvdKSxhIqXX6U_k045FMOUk229Smeq10o",
        "nombre": "mov_tierra_acceso_botadero.xlsx",
        "tipo": "export",
        "dominio": "Acceso a Botadero",
    },
    {
        "id": "1nctJgdtyWoxnLuso5WhJVgukGvhqAUFP3V8rrmeZhyM",
        "nombre": "mov_tierra_acceso_tunel.xlsx",
        "tipo": "export",
        "dominio": "Acceso al Tunel",
    },
    {
        "id": "10fUz5_YLZAZigvxO4yOw__AbbD2zvrc-RbSml9Bn-Xc",
        "nombre": "banquetas_portal_b.xlsx",
        "tipo": "export",
        "dominio": "Banquetas Portal B",
    },
]


def extraer_todo() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    resultados = []

    print(
        f"[INFO] Iniciando extracción segura de {len(ARCHIVOS_MANIFEST)} archivos de Google Drive..."
    )

    for item in ARCHIVOS_MANIFEST:
        dest_path = OUTPUT_DIR / item["nombre"]
        fid = item["id"]
        tipo = item["tipo"]

        if dest_path.exists() and dest_path.stat().st_size > 0:
            print(
                f"[SKIP] Ya existe: {item['nombre']} ({dest_path.stat().st_size} bytes)"
            )
            resultados.append(
                {
                    **item,
                    "status": "EXISTENTE",
                    "bytes": dest_path.stat().st_size,
                    "path": str(dest_path),
                }
            )
            continue

        print(f"[FETCH] Descargando {item['nombre']} (ID: {fid}) vía {tipo}...")
        if tipo == "download":
            cmd = [GDRIVE_CLI, "readonly", "download", fid, "--out", str(dest_path)]
        else:
            cmd = [
                GDRIVE_CLI,
                "readonly",
                "export",
                fid,
                str(dest_path),
                "--format",
                "xlsx",
            ]

        try:
            subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=180)
            size = dest_path.stat().st_size if dest_path.exists() else 0
            print(f"       -> OK: {dest_path.name} ({size} bytes)")
            resultados.append(
                {**item, "status": "DESCARGADO", "bytes": size, "path": str(dest_path)}
            )
        except Exception as e:
            print(f"       -> ERROR al procesar {item['nombre']}: {e}")
            resultados.append(
                {**item, "status": "ERROR", "error": str(e), "path": str(dest_path)}
            )

    manifest_file = OUTPUT_DIR / "manifest.json"
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)

    print(f"\n[OK] Manifiesto guardado en: {manifest_file}")


if __name__ == "__main__":
    extraer_todo()
