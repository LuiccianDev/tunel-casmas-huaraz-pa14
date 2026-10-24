"""Hook de pre-ejecución para el plugin asistente-pa14."""

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
            linea_limpia = command_line.strip()
            # Bloquear invocaciones directas de python/pip sin uv
            patron_prohibido = r"^(python|pip|py)\s+"
            if re.match(patron_prohibido, linea_limpia, re.IGNORECASE):
                decision = {
                    "decision": "deny",
                    "reason": (
                        "Violación de entorno en PA14: Se detectó ejecución directa de Python/pip. "
                        "Usa siempre 'uv run' (ej. 'uv run python ...', 'uv run pytest', 'uv run pa14')."
                    ),
                }
                print(json.dumps(decision))
                return

        print(json.dumps({"decision": "allow"}))
    except Exception:
        print(json.dumps({"decision": "allow"}))


if __name__ == "__main__":
    procesar_hook()
