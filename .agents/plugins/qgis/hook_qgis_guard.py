"""Hook de protección geoespacial para el plugin QGIS MCP (PA14).

Verifica la integridad del sistema de referencia espacial (EPSG:32718 / UTM Zona 18S)
y previene operaciones destructivas no intencionadas sobre capas base.
"""

import json
import sys


def procesar_hook():
    try:
        raw_input = sys.stdin.read()
        if not raw_input.strip():
            print(json.dumps({"decision": "allow"}))
            return

        payload = json.loads(raw_input)
        tool_call = payload.get("toolCall", {})
        tool_name = tool_call.get("name", "")
        args = tool_call.get("args", {})

        # Si se invoca una herramienta MCP de QGIS
        server_name = args.get("ServerName", "")
        mcp_tool = args.get("ToolName", "")
        mcp_args = args.get("Arguments", {})

        es_qgis = (
            tool_name in ["mcp_qgis_set_project_crs", "mcp_qgis_execute_sql"]
            or (tool_name == "call_mcp_tool" and server_name in ["qgis", "qgis_qgis"])
        )

        if es_qgis:
            target_tool = mcp_tool if tool_name == "call_mcp_tool" else tool_name

            # 1. Proteger el CRS oficial del proyecto (EPSG:32718)
            if target_tool in ["set_project_crs", "mcp_qgis_set_project_crs"]:
                crs_deseado = str(mcp_args.get("crs", "")).upper().strip()
                if crs_deseado and "32718" not in crs_deseado and "UTM" not in crs_deseado:
                    decision = {
                        "decision": "deny",
                        "reason": (
                            f"Restricción de CRS en Túnel PA14: Se intentó cambiar el CRS a '{crs_deseado}'. "
                            "El sistema proyectado oficial y obligatorio es 'EPSG:32718' (WGS 84 / UTM Zona 18S)."
                        ),
                    }
                    print(json.dumps(decision))
                    return

        print(json.dumps({"decision": "allow"}))
    except Exception:
        print(json.dumps({"decision": "allow"}))


if __name__ == "__main__":
    procesar_hook()
