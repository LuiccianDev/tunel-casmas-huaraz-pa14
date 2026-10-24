"""Hook PreToolUse para proteger el entorno del proyecto PA14.

Valida que los comandos de terminal utilicen siempre el entorno de uv
y bloquea comandos peligrosos o ejecuciones directas de python/pip fuera de uv.
Cumple con el contrato oficial de Antigravity Hooks (JSON stdin -> JSON stdout).
"""

import json
import re
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
        command_line = args.get("CommandLine", "").strip()

        if tool_name == "run_command" and command_line:
            # Detectar comandos de python/pip aislados fuera de uv
            # Permite uv run, uv pip, uv add, uvx, etc.
            linea_limpia = command_line.strip()

            # Patrones prohibidos directos: "python ...", "pip install ...", "py ..."
            patron_prohibido = r"^(python|pip|py)\s+"
            if re.match(patron_prohibido, linea_limpia, re.IGNORECASE):
                # Si no está precedido por 'uv run'
                decision = {
                    "decision": "deny",
                    "reason": (
                        "Violación de entorno en PA14: Se detectó ejecución directa de Python/pip. "
                        "Usa siempre 'uv run' (ej. 'uv run python ...', 'uv run pytest', 'uv run pa14')."
                    ),
                }
                print(json.dumps(decision))
                return

        # Para todos los demás comandos permitidos
        print(json.dumps({"decision": "allow"}))
    except Exception:
        # En caso de error inesperado, permitir para no bloquear el flujo
        print(json.dumps({"decision": "allow"}))


if __name__ == "__main__":
    procesar_hook()
