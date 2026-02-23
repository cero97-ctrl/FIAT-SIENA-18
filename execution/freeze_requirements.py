#!/usr/bin/env python3
import subprocess
import sys
import os


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    req_path = os.path.join(project_root, "requirements.txt")

    print(f"❄️  Congelando dependencias en: {req_path}")

    try:
        # Ejecutar pip freeze
        # Usamos sys.executable para asegurar que se usa el pip del entorno actual
        result = subprocess.run(
            [sys.executable, "-m", "pip", "freeze"],
            capture_output=True,
            text=True,
            check=True
        )

        requirements = result.stdout

        with open(req_path, "w", encoding="utf-8") as f:
            f.write(requirements)

        count = len(requirements.strip().splitlines())
        print(f"✅ requirements.txt actualizado con {count} paquetes.")

    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando pip freeze: {e}")
        sys.exit(1)
    except IOError as e:
        print(f"❌ Error escribiendo en {req_path}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
