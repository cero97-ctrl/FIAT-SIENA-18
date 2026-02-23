#!/usr/bin/env python3
import os
import zipfile
import datetime
import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="Create a zip backup of the project.")
    parser.add_argument("--output-dir", default="backups", help="Directory to store backups.")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    project_name = os.path.basename(project_root)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"{project_name}_backup_{timestamp}.zip"

    output_dir = os.path.join(project_root, args.output_dir)
    os.makedirs(output_dir, exist_ok=True)

    zip_path = os.path.join(output_dir, zip_filename)

    print(f"📦 Creando backup: {zip_path}")

    # Directorios a excluir (sistema, git, entornos, temporales)
    EXCLUDE_DIRS = {
        '.git', '.tmp', '__pycache__', 'venv', 'env', '.venv', 'agent_env',
        '.vscode', '.idea', args.output_dir, 'backups'
    }

    # Archivos a excluir
    EXCLUDE_FILES = {
        '.DS_Store', 'Thumbs.db', zip_filename
    }

    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(project_root):
                # Modificar dirs in-place para saltar carpetas excluidas
                dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

                for file in files:
                    if file in EXCLUDE_FILES:
                        continue
                    if file.endswith('.pyc'):
                        continue

                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, project_root)

                    zipf.write(file_path, arcname)

        print(f"✅ Backup creado exitosamente ({os.path.getsize(zip_path) / 1024 / 1024:.2f} MB).")

    except Exception as e:
        print(f"❌ Error creando backup: {e}")
        if os.path.exists(zip_path):
            os.remove(zip_path)
        sys.exit(1)


if __name__ == "__main__":
    main()
