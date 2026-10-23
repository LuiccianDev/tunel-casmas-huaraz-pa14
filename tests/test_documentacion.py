"""Pruebas de integridad documental (Guardián de READMEs y Living Documentation)."""

from pathlib import Path

from casmas_pa14.main import MODULOS

ROOT_DIR = Path(__file__).resolve().parent.parent
README_ROOT = ROOT_DIR / "README.md"
README_GATEWAY = ROOT_DIR / "plugins" / "AutoCAD_AI_Gateway" / "README.md"
README_MCP = ROOT_DIR / "plugins" / "AutoCAD_MCP_Server" / "README.md"
DOC_MCP = ROOT_DIR / "docs" / "documentacion_mcp_autocad.md"
DOC_PROMPTS = ROOT_DIR / "salidas" / "documentos" / "prompts_edificaciones_cad.md"
VSCODE_MCP = ROOT_DIR / ".vscode" / "mcp.json"


def test_readme_raiz_contiene_todos_los_modulos():
    """Verifica que cada módulo registrado en main.MODULOS figure en el README raíz."""
    assert README_ROOT.exists(), "El archivo README.md raíz no existe."
    contenido = README_ROOT.read_text(encoding="utf-8")

    for modulo in MODULOS:
        nombre_modulo = modulo.__name__.split(".")[-1]
        dummy_p = {"proyecto": {"nombre": "Test"}}
        dummy_ctx = {}
        try:
            res = modulo.calcular(dummy_p, dummy_ctx)
            libro = modulo.libro(res, dummy_p)
            archivo_excel = libro.archivo
        except Exception:
            archivo_excel = (
                nombre_modulo.replace("m", "")[:2] if len(nombre_modulo) >= 3 else ""
            )

        if archivo_excel:
            assert archivo_excel in contenido, (
                f"El entregable '{archivo_excel}' del módulo '{nombre_modulo}' "
                "no está documentado en la tabla de README.md. ¡Actualiza README.md!"
            )


def test_readmes_usan_puerto_oficial_5055():
    """Valida que todos los READMEs utilicen el puerto oficial 5055 y no el obsoleto 8080."""
    archivos = [README_ROOT, README_GATEWAY, README_MCP, DOC_MCP]

    for archivo in archivos:
        assert archivo.exists(), f"El archivo '{archivo}' no existe."
        texto = archivo.read_text(encoding="utf-8")
        assert "8080" not in texto, (
            f"El archivo '{archivo.name}' contiene referencia al puerto obsoleto 8080. "
            "Debe usar el puerto oficial 5055."
        )
        assert "5055" in texto, (
            f"El archivo '{archivo.name}' debe documentar el puerto oficial 5055."
        )


def test_plugins_readmes_documentan_endpoints_y_herramientas():
    """Verifica que los READMEs de los plugins detallen todos los endpoints y herramientas."""
    assert README_GATEWAY.exists()
    assert README_MCP.exists()

    texto_gateway = README_GATEWAY.read_text(encoding="utf-8")
    endpoints_esperados = [
        "/execute",
        "/context/info",
        "/context/entities",
        "/context/layers",
        "/context/texts",
        "/context/extents",
        "/context/selection",
        "/context/blocks",
        "/civil/status",
        "/civil/surfaces",
        "/civil/surface/elevation",
        "/civil/surface/create",
        "/civil/alignments",
        "/civil/alignment/station-offset",
        "/civil/alignment/point-at-station",
        "/civil/alignment/create",
    ]
    for ep in endpoints_esperados:
        assert ep in texto_gateway, (
            f"El endpoint '{ep}' no está documentado en {README_GATEWAY}. "
            "Actualiza la especificación de endpoints."
        )

    texto_mcp = README_MCP.read_text(encoding="utf-8")
    herramientas_esperadas = [
        "obtener_info_dibujo",
        "leer_objetos_autocad",
        "leer_capas_autocad",
        "leer_textos_autocad",
        "obtener_limites_dibujo",
        "leer_seleccion_autocad",
        "listar_bloques_disponibles",
        "ping_autocad_gateway",
        "ejecutar_comando_autocad",
        "zoom_extension",
        "guardar_dibujo",
        "configurar_entorno_dibujo",
        "verificar_estado_civil3d",
        "listar_superficies_civil3d",
        "consultar_elevacion_terreno",
        "listar_alineamientos_civil3d",
        "consultar_estacion_alineamiento",
        "obtener_coordenada_en_estacion",
        "crear_alineamiento_civil3d",
        "crear_superficie_civil3d",
    ]
    for h in herramientas_esperadas:
        assert h in texto_mcp, (
            f"La herramienta MCP '{h}' no está documentada en {README_MCP}. "
            "Actualiza el catálogo de herramientas."
        )


def test_mcp_configuraciones_y_binarios_alineados():
    """Valida la consistencia de los binarios y configuración MCP (.dll en .vscode/mcp.json y READMEs)."""
    assert VSCODE_MCP.exists(), "El archivo .vscode/mcp.json no existe."
    texto_vscode = VSCODE_MCP.read_text(encoding="utf-8")
    assert "AutoCAD_MCP_Server.dll" in texto_vscode, (
        ".vscode/mcp.json debe apuntar al ensamblado AutoCAD_MCP_Server.dll."
    )

    texto_mcp = README_MCP.read_text(encoding="utf-8")
    assert "${workspaceFolder}" in texto_mcp, (
        "El README de AutoCAD_MCP_Server debe documentar la configuración con ${workspaceFolder}."
    )
    assert "AutoCAD_MCP_Server.dll" in texto_mcp, (
        "El README de AutoCAD_MCP_Server debe documentar el uso de AutoCAD_MCP_Server.dll."
    )


def test_prompts_cad_autogenerados_con_38_edificaciones():
    """Verifica que el catálogo de prompts CAD autogenerado contenga las 38 edificaciones (EDIF-01 a EDIF-38)."""
    assert DOC_PROMPTS.exists(), (
        f"El archivo '{DOC_PROMPTS}' no existe. Ejecuta 'uv run pa14' para generarlo."
    )
    texto = DOC_PROMPTS.read_text(encoding="utf-8")
    for i in range(1, 39):
        codigo = f"EDIF-{i:02d}"
        assert codigo in texto, (
            f"El código '{codigo}' no figura en el catálogo autogenerado de prompts CAD."
        )


def test_documentacion_civil3d_dg2018():
    """Verifica que civil3d/README.md y README.md raíz documenten el XML DG-2018, su comando y fuente PDF."""
    readme_civil3d = ROOT_DIR / "civil3d" / "README.md"
    pdf_local = ROOT_DIR / "docs" / "entradas" / "manual_de_carreteras_dg_2018.pdf"
    assert readme_civil3d.exists(), "El archivo civil3d/README.md no existe."
    assert pdf_local.exists(), (
        "El PDF oficial docs/entradas/manual_de_carreteras_dg_2018.pdf no existe."
    )

    comando = "uv run python civil3d/generar_dg2018.py"
    xml_nombre = "PA14_DG2018_MTC_Roadway_Design_Standards.xml"
    url_pdf_dg2018 = "https://drive.google.com/file/d/1kdXJQ1sfLHBTbPC3mbCcYBWaTW8UOO0C/view?usp=sharing"

    for archivo in (README_ROOT, readme_civil3d):
        texto = archivo.read_text(encoding="utf-8")
        assert comando in texto, (
            f"El comando '{comando}' no está documentado en {archivo}."
        )
        assert xml_nombre in texto, (
            f"El archivo '{xml_nombre}' no está documentado en {archivo}."
        )
        assert url_pdf_dg2018 in texto, (
            f"El enlace al PDF de referencia DG-2018 no está documentado en {archivo}."
        )


def test_entradas_pdf_tienen_markdown_e_indice():
    """Garantiza que todo PDF en docs/entradas/ tenga su versión .md convertida y exista indice_dg2018.md."""
    entradas_dir = ROOT_DIR / "docs" / "entradas"
    indice = entradas_dir / "indice_dg2018.md"
    assert indice.exists(), "El índice rápido docs/entradas/indice_dg2018.md no existe."
    for pdf in entradas_dir.glob("*.pdf"):
        md_par = pdf.with_suffix(".md")
        assert md_par.exists(), (
            f"El archivo '{pdf.name}' no tiene su versión Markdown '{md_par.name}'. "
            "Ejecuta: uv run --with 'markitdown[pdf]' python scripts/utils/convertir_pdfs.py"
        )


def test_estructura_plugins_antigravity():
    """Valida que todos los plugins en .agents/plugins/ cumplan el esquema oficial de Antigravity 2.0."""
    import json

    agents_dir = ROOT_DIR / ".agents"
    plugins_json = agents_dir / "plugins.json"
    skills_json = agents_dir / "skills.json"
    assert plugins_json.exists(), "El archivo .agents/plugins.json no existe."
    assert skills_json.exists(), "El archivo .agents/skills.json no existe."

    plugins_dir = agents_dir / "plugins"
    assert plugins_dir.exists(), "El directorio .agents/plugins no existe."

    campos_permitidos = {
        "name",
        "displayName",
        "version",
        "description",
        "logo",
        "suggestedPrompts",
        "disabled",
    }
    plugins_esperados = {
        "asistente-pa14",
        "autocad-gateway",
        "code-reviewer",
        "graphify",
        "powerbi",
        "qgis",
    }
    carpetas = {p.name for p in plugins_dir.iterdir() if p.is_dir()}
    assert plugins_esperados.issubset(carpetas), (
        f"Faltan plugins esperados en .agents/plugins/: {plugins_esperados - carpetas}"
    )

    for plugin_path in sorted(p for p in plugins_dir.iterdir() if p.is_dir()):
        manifest_file = plugin_path / "plugin.json"
        readme_file = plugin_path / "README.md"
        assert manifest_file.exists(), f"Falta plugin.json en {plugin_path.name}"
        assert readme_file.exists(), f"Falta README.md en {plugin_path.name}"

        data = json.loads(manifest_file.read_text(encoding="utf-8"))
        campos_extra = set(data.keys()) - campos_permitidos
        assert not campos_extra, (
            f"Campos no soportados en {plugin_path.name}/plugin.json: {campos_extra}"
        )
        assert data.get("name") == plugin_path.name, (
            f"El campo 'name' en {plugin_path.name}/plugin.json debe coincidir con la carpeta."
        )
        assert data.get("displayName"), (
            f"Falta 'displayName' en {plugin_path.name}/plugin.json"
        )
        assert data.get("version"), f"Falta 'version' en {plugin_path.name}/plugin.json"
        assert data.get("description"), (
            f"Falta 'description' en {plugin_path.name}/plugin.json"
        )

        logo_rel = data.get("logo")
        assert logo_rel, f"Falta 'logo' en {plugin_path.name}/plugin.json"
        assert (plugin_path / logo_rel).exists(), (
            f"El archivo de logo '{logo_rel}' no existe en {plugin_path.name}"
        )

        prompts = data.get("suggestedPrompts", [])
        assert isinstance(prompts, list) and len(prompts) == 3, (
            f"{plugin_path.name}/plugin.json debe tener exactamente 3 'suggestedPrompts'."
        )

        rules_dir = plugin_path / "rules"
        if rules_dir.exists():
            archivos_reglas = [f.name for f in rules_dir.iterdir() if f.is_file()]
            assert archivos_reglas == ["AGENTS.md"], (
                f"En {plugin_path.name}/rules/ solo debe existir 'AGENTS.md' "
                f"(encontrado: {archivos_reglas})."
            )

        skills_dir = plugin_path / "skills"
        if skills_dir.exists():
            for skill_folder in (s for s in skills_dir.iterdir() if s.is_dir()):
                skill_md = skill_folder / "SKILL.md"
                assert skill_md.exists(), (
                    f"Falta SKILL.md en {plugin_path.name}/skills/{skill_folder.name}"
                )
