#!/usr/bin/env python3
import subprocess
import sys
import os


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    req_path = os.path.join(project_root, "requirements.txt")

    if not os.path.exists(req_path):
        print(f"❌ Error: No se encontró {req_path}")
        sys.exit(1)

    print(f"🔄 Actualizando dependencias desde: {req_path}")
    print("   Esto puede tardar unos momentos...")

    try:
        # Ejecutar pip install --upgrade -r requirements.txt
        # Usamos sys.executable para asegurar que se usa el pip del entorno actual
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "-r", req_path])
        print("\n✅ Todas las dependencias han sido actualizadas a la última versión compatible.")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error durante la actualización: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
