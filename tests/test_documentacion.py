"""Pruebas de integridad documental (Guardián de READMEs y Living Documentation)."""

import json
from pathlib import Path

from casmas_pa14.main import MODULOS

ROOT_DIR = Path(__file__).resolve().parent.parent
README_ROOT = ROOT_DIR / "README.md"
DOC_PROMPTS = ROOT_DIR / "salidas" / "documentos" / "prompts_edificaciones_cad.md"


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
    """Valida que el README raíz documente el puerto oficial 5055 para el canal CAD interactivo."""
    assert README_ROOT.exists(), "El archivo README.md no existe."
    texto = README_ROOT.read_text(encoding="utf-8")
    assert "8080" not in texto, (
        "El archivo README.md contiene referencia al puerto obsoleto 8080. "
        "Debe usar el puerto oficial 5055."
    )
    assert "5055" in texto, (
        "El archivo README.md debe documentar el puerto oficial 5055."
    )


def test_referencia_repositorio_externo_autocad_mcp():
    """Verifica que el README raíz referencie el repositorio oficial desacoplado LuiccianDev/autocad-mcp."""
    assert README_ROOT.exists(), "El archivo README.md raíz no existe."
    texto = README_ROOT.read_text(encoding="utf-8")
    assert "https://github.com/LuiccianDev/autocad-mcp" in texto, (
        "README.md debe documentar el enlace al repositorio oficial desacoplado LuiccianDev/autocad-mcp."
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
    """Verifica que diseno_vial/README.md y README.md raíz documenten el XML DG-2018, su comando y fuente oficial."""
    readme_diseno_vial = ROOT_DIR / "diseno_vial" / "README.md"
    md_local = ROOT_DIR / "docs" / "entradas" / "manual_de_carreteras_dg_2018.md"
    assert readme_diseno_vial.exists(), "El archivo diseno_vial/README.md no existe."
    assert md_local.exists(), (
        "El documento docs/entradas/manual_de_carreteras_dg_2018.md no existe."
    )

    comando = "uv run python diseno_vial/generar_dg2018.py"
    xml_nombre = "PA14_DG2018_MTC_Roadway_Design_Standards.xml"
    url_pdf_dg2018 = "https://drive.google.com/file/d/1kdXJQ1sfLHBTbPC3mbCcYBWaTW8UOO0C/view?usp=sharing"

    for archivo in (README_ROOT, readme_diseno_vial):
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
    """Garantiza que docs/entradas/ no retenga PDFs redundantes y cuente con sus archivos .md e indice_dg2018.md."""
    entradas_dir = ROOT_DIR / "docs" / "entradas"
    indice = entradas_dir / "indice_dg2018.md"
    assert indice.exists(), "El índice rápido docs/entradas/indice_dg2018.md no existe."
    pdfs_residuales = [p.name for p in entradas_dir.glob("*.pdf")]
    assert not pdfs_residuales, (
        f"Existen PDFs redundantes en docs/entradas/ que ya tienen su par .md: {pdfs_residuales}"
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


def test_subagentes_personalizados_pa14():
    """Valida la existencia y formato oficial de los subagentes especializados PA14."""
    agents_workspace = ROOT_DIR / ".agents" / "agents"
    assert agents_workspace.exists(), "La carpeta .agents/agents/ no existe."

    subagentes_esperados = {
        "calculista.md": "calculista-pa14",
        "geologo.md": "geologo-pa14",
        "cad_civil3d.md": "cad-civil3d-pa14",
        "auditor_qa.md": "auditor-qa-pa14",
        "qgis.md": "qgis-pa14",
        "powerbi.md": "powerbi-pa14",
    }

    for archivo, nombre_esperado in subagentes_esperados.items():
        agente_file = agents_workspace / archivo
        assert agente_file.exists(), (
            f"Falta el subagente '{archivo}' en .agents/agents/"
        )

        contenido = agente_file.read_text(encoding="utf-8")
        assert contenido.startswith("---"), (
            f"{archivo} debe iniciar con frontmatter YAML."
        )
        partes = contenido.split("---", 2)
        assert len(partes) >= 3, (
            f"{archivo} debe contener bloque frontmatter YAML cerrado."
        )

        yaml_text = partes[1]
        assert f"name: {nombre_esperado}" in yaml_text, (
            f"{archivo} debe tener 'name: {nombre_esperado}'."
        )
        assert "description:" in yaml_text, f"{archivo} debe tener 'description'."
        assert "mainAgent: true" in yaml_text, (
            f"{archivo} debe tener 'mainAgent: true'."
        )
        assert "subagent: true" in yaml_text, f"{archivo} debe tener 'subagent: true'."


def test_hooks_ciclo_de_vida_antigravity():
    """Verifica la configuración y scripts ejecutables de los hooks de Antigravity."""
    hooks_file = ROOT_DIR / ".agents" / "plugins" / "asistente-pa14" / "hooks.json"
    assert hooks_file.exists(), "El archivo hooks.json de asistente-pa14 no existe."

    datos = json.loads(hooks_file.read_text(encoding="utf-8"))
    assert "pa14-environment-guard" in datos, (
        "hooks.json debe contener el bloque 'pa14-environment-guard'."
    )

    guard = datos["pa14-environment-guard"]
    assert guard.get("enabled") is True
    assert "PreToolUse" in guard
    assert "PostToolUse" in guard

    # Validación de hooks en asistente-pa14
    script_guard = ROOT_DIR / ".agents" / "plugins" / "asistente-pa14" / "hook_guard.py"
    script_post = (
        ROOT_DIR / ".agents" / "plugins" / "asistente-pa14" / "hook_post_edit.py"
    )
    assert script_guard.exists(), "Falta hook_guard.py en asistente-pa14"
    assert script_post.exists(), "Falta hook_post_edit.py en asistente-pa14"

    # Validación de hooks en qgis
    hooks_qgis = ROOT_DIR / ".agents" / "plugins" / "qgis" / "hooks.json"
    assert hooks_qgis.exists(), "El archivo hooks.json de qgis no existe."
    datos_qgis = json.loads(hooks_qgis.read_text(encoding="utf-8"))
    assert "qgis-integrity-guard" in datos_qgis
    assert (
        ROOT_DIR / ".agents" / "plugins" / "qgis" / "hook_qgis_guard.py"
    ).exists(), "Falta hook_qgis_guard.py en qgis"

    # Validación de hooks en powerbi
    hooks_powerbi = ROOT_DIR / ".agents" / "plugins" / "powerbi" / "hooks.json"
    assert hooks_powerbi.exists(), "El archivo hooks.json de powerbi no existe."
    datos_powerbi = json.loads(hooks_powerbi.read_text(encoding="utf-8"))
    assert "powerbi-integrity-guard" in datos_powerbi
    assert (
        ROOT_DIR / ".agents" / "plugins" / "powerbi" / "hook_powerbi_guard.py"
    ).exists(), "Falta hook_powerbi_guard.py en powerbi"
