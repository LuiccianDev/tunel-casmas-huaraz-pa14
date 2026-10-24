"""Hook de protección y calidad DAX para el plugin Power BI MCP (PA14).

Verifica que las operaciones de modificación estructural en el modelo tabular
utilicen transacciones atómicas seguras y valida consistencia sintáctica básica en DAX.
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

        # Si se invoca una herramienta MCP de Power BI
        server_name = args.get("ServerName", "")
        mcp_tool = args.get("ToolName", "")
        mcp_args = args.get("Arguments", {})

        es_powerbi = (
            tool_name.startswith("mcp_powerbi")
            or (tool_name == "call_mcp_tool" and "powerbi" in server_name)
        )

        if es_powerbi:
            target_tool = mcp_tool if tool_name == "call_mcp_tool" else tool_name

            # Validar transaccionalidad en operaciones sobre medidas o tablas
            if target_tool in ["measure_operations", "table_operations"]:
                options = mcp_args.get("options", {})
                if options and options.get("useTransaction") is False:
                    decision = {
                        "decision": "deny",
                        "reason": (
                            "Regla de Integridad Power BI PA14: Las operaciones de modificación sobre el modelo "
                            "tabular deben ejecutarse con 'useTransaction: true' para prevenir inconsistencias."
                        ),
                    }
                    print(json.dumps(decision))
                    return

                # Validación básica de balance de paréntesis en expresiones DAX
                definitions = mcp_args.get("definitions", [])
                for item in definitions:
                    exp = item.get("expression", "")
                    if exp and exp.count("(") != exp.count(")"):
                        decision = {
                            "decision": "deny",
                            "reason": (
                                f"Error de Sintaxis DAX en la medida '{item.get('name', 'desconocida')}': "
                                "Paréntesis desbalanceados detectados en la expresión DAX antes de enviar al modelo."
                            ),
                        }
                        print(json.dumps(decision))
                        return

        print(json.dumps({"decision": "allow"}))
    except Exception:
        print(json.dumps({"decision": "allow"}))


if __name__ == "__main__":
    procesar_hook()
