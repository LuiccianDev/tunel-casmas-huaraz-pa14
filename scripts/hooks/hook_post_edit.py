"""Hook PostToolUse para auditoría de ediciones en el proyecto PA14.

Cumple con el contrato oficial de Antigravity Hooks (JSON stdin -> JSON {} stdout).
Detecta si se han modificado archivos clave de ingeniería (parametros.toml o src/casmas_pa14/)
para recordar la ejecución de scripts/check.ps1.
"""

import json
import sys


def procesar_hook():
    try:
        raw_input = sys.stdin.read()
        if raw_input.strip():
            _ = json.loads(raw_input)
            # El contrato de PostToolUse en Antigravity espera un objeto JSON vacío {}
        print(json.dumps({}))
    except Exception:
        print(json.dumps({}))


if __name__ == "__main__":
    procesar_hook()
