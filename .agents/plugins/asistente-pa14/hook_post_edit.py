"""Hook de post-edición para el plugin asistente-pa14."""

import json
import sys


def procesar_hook():
    try:
        raw_input = sys.stdin.read()
        if raw_input.strip():
            _ = json.loads(raw_input)
        print(json.dumps({}))
    except Exception:
        print(json.dumps({}))


if __name__ == "__main__":
    procesar_hook()
