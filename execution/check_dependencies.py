#!/usr/bin/env python3
import sys
import os
import importlib.metadata


def main():
    # Path to requirements.txt
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    req_path = os.path.join(project_root, "requirements.txt")

    if not os.path.exists(req_path):
        print(f"❌ Error: No se encontró {req_path}")
        sys.exit(1)

    print(f"🔍 Verificando dependencias desde: {req_path}")

    with open(req_path, "r", encoding="utf-8") as f:
        # Parse simple requirements (ignoring comments and empty lines)
        # Se limpia la versión (==, >=, etc) para obtener solo el nombre
        requirements = [
            line.strip().split("==")[0].split(">=")[0].split("<=")[0].split(">")[0].split("<")[0].strip()
            for line in f
            if line.strip() and not line.startswith("#")
        ]

    # Get installed packages (normalized names)
    installed = {dist.metadata["Name"].lower().replace("_", "-") for dist in importlib.metadata.distributions()}

    missing = []
    for req in requirements:
        if req.lower().replace("_", "-") not in installed:
            missing.append(req)

    if missing:
        print(f"❌ Faltan {len(missing)} dependencias:")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\n🛠  Para solucionar, ejecuta: pip install -r requirements.txt")
        sys.exit(1)
    else:
        print("✅ Todas las dependencias están instaladas correctamente.")
        sys.exit(0)


if __name__ == "__main__":
    main()
