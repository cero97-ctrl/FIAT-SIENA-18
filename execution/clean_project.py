#!/usr/bin/env python3
import os
import shutil
import sys


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    print(f"🧹 Limpiando proyecto en: {project_root}")

    # 1. Limpiar .tmp/
    tmp_dir = os.path.join(project_root, ".tmp")
    if os.path.exists(tmp_dir):
        print("   - Limpiando .tmp/ ...")
        for filename in os.listdir(tmp_dir):
            file_path = os.path.join(tmp_dir, filename)
            try:
                # Mantener .gitkeep si existe
                if filename == ".gitkeep":
                    continue

                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"     ⚠️ Error borrando {file_path}: {e}")

    # 2. Limpiar __pycache__ y otros artefactos de Python
    print("   - Eliminando cachés de Python (__pycache__, .pytest_cache) ...")
    for root, dirs, files in os.walk(project_root):
        # Modificar dirs in-place para evitar recorrer directorios eliminados
        if "__pycache__" in dirs:
            path = os.path.join(root, "__pycache__")
            try:
                shutil.rmtree(path)
                dirs.remove("__pycache__")
            except Exception as e:
                print(f"     ⚠️ Error borrando {path}: {e}")

        if ".pytest_cache" in dirs:
            path = os.path.join(root, ".pytest_cache")
            try:
                shutil.rmtree(path)
                dirs.remove(".pytest_cache")
            except Exception as e:
                print(f"     ⚠️ Error borrando {path}: {e}")

    # 3. Limpiar reportes y backups específicos
    files_to_clean = ["WEEKLY_REPORT.md", "README.md.bak"]
    print("   - Eliminando reportes antiguos y backups ...")
    for f in files_to_clean:
        f_path = os.path.join(project_root, f)
        if os.path.exists(f_path):
            try:
                os.remove(f_path)
                print(f"     Eliminado: {f}")
            except Exception as e:
                print(f"     ⚠️ Error borrando {f}: {e}")

    print("✨ Limpieza completada.")


if __name__ == "__main__":
    main()
