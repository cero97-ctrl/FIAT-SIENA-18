#!/usr/bin/env python3
import os
import shutil
import argparse
import sys
import subprocess


def main():
    """
    Script de inicialización para nuevos proyectos basados en la plantilla.
    Realiza limpieza de archivos temporales, cachés y prepara el entorno.
    """
    parser = argparse.ArgumentParser(description="Inicializa el proyecto limpiando datos de la plantilla.")
    parser.add_argument("--name", type=str, help="Nombre del nuevo proyecto (actualiza README.md).")
    parser.add_argument("--reset-git", action="store_true",
                        help="Elimina la carpeta .git para iniciar un historial limpio.")

    args = parser.parse_args()

    # Rutas base
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    print(f"🚀 Inicializando proyecto en: {project_root}")

    # 1. Limpiar .tmp/
    tmp_dir = os.path.join(project_root, ".tmp")
    if os.path.exists(tmp_dir):
        print("🧹 Limpiando directorio .tmp/...")
        for filename in os.listdir(tmp_dir):
            file_path = os.path.join(tmp_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"   ⚠️ Error borrando {file_path}: {e}")
        # Crear un .gitkeep para mantener la carpeta
        with open(os.path.join(tmp_dir, ".gitkeep"), "w") as f:
            pass
    else:
        os.makedirs(tmp_dir)
        print("📁 Directorio .tmp/ creado.")

    # 2. Limpiar __pycache__
    print("🧹 Eliminando __pycache__...")
    for root, dirs, files in os.walk(project_root):
        for d in dirs:
            if d == "__pycache__":
                shutil.rmtree(os.path.join(root, d))

    # 3. Configurar .env
    env_path = os.path.join(project_root, ".env")
    if not os.path.exists(env_path):
        print("📝 Creando archivo .env base...")
        with open(env_path, "w") as f:
            f.write("# Configuración del Proyecto\n")
            f.write("# Añade aquí tus claves de API\n")
            f.write("OPENAI_API_KEY=\n")
            f.write("ANTHROPIC_API_KEY=\n")
            f.write("GOOGLE_API_KEY=\n")
    else:
        print("✅ Archivo .env ya existe. Verificando claves faltantes...")
        with open(env_path, "r") as f:
            existing_content = f.read()

        with open(env_path, "a") as f:
            if "GOOGLE_API_KEY" not in existing_content:
                f.write("\nGOOGLE_API_KEY=\n")
                print("   ➕ Añadido GOOGLE_API_KEY")
            if "OPENAI_API_KEY" not in existing_content:
                f.write("OPENAI_API_KEY=\n")
                print("   ➕ Añadido OPENAI_API_KEY")
            if "ANTHROPIC_API_KEY" not in existing_content:
                f.write("ANTHROPIC_API_KEY=\n")
                print("   ➕ Añadido ANTHROPIC_API_KEY")

    # 4. Actualizar Nombre en README.md (si se provee)
    if args.name:
        readme_path = os.path.join(project_root, "README.md")
        if os.path.exists(readme_path):
            print(f"📝 Actualizando nombre del proyecto en README.md a '{args.name}'...")
            with open(readme_path, "r") as f:
                content = f.read()

            # Reemplazo del placeholder estándar
            new_content = content.replace("[Nombre del Proyecto]", args.name)

            with open(readme_path, "w") as f:
                f.write(new_content)

    # 5. Resetear Git (Opcional)
    if args.reset_git:
        git_dir = os.path.join(project_root, ".git")
        if os.path.exists(git_dir):
            print("🔄 Eliminando historial de Git existente...")
            shutil.rmtree(git_dir)
            print("   💡 Ejecuta 'git init' para iniciar un nuevo repositorio.")

    # 6. Validar Framework
    print("\n🔍 Validando integridad del framework...")
    health_script = os.path.join(project_root, "execution", "check_system_health.py")
    directives_script = os.path.join(project_root, "execution", "validate_directives.py")

    proc_health = subprocess.run([sys.executable, health_script])
    proc_directives = subprocess.run([sys.executable, directives_script])

    if proc_health.returncode != 0 or proc_directives.returncode != 0:
        print("\n⚠️  La inicialización finalizó, pero se detectaron errores en el framework.")

    # 7. Iniciar el Agente CLI
    print("\n🚀 Iniciando el Agente Interactivo...")
    run_agent_script = os.path.join(project_root, "execution", "run_agent.py")
    subprocess.run([sys.executable, run_agent_script])

    # Nota: El script run_agent.py toma el control, el mensaje de éxito final se verá al salir.


if __name__ == "__main__":
    main()
