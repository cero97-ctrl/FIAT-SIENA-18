#!/usr/bin/env python3
import argparse
import subprocess
import sys


def run_command(command, check=True):
    """Ejecuta un comando de shell y maneja errores."""
    try:
        result = subprocess.run(command, check=check, text=True, capture_output=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        if check:
            print(f"❌ Error ejecutando: {' '.join(command)}")
            print(f"   Detalle: {e.stderr.strip()}")
            sys.exit(1)
        else:
            raise e


def main():
    parser = argparse.ArgumentParser(description="Actualiza el proyecto desde el repositorio plantilla.")
    parser.add_argument("--template-url", required=True, help="URL del repositorio plantilla")
    parser.add_argument("--branch", default="main", help="Rama de la plantilla a usar")

    args = parser.parse_args()

    print(f"🔄 Iniciando actualización desde: {args.template_url} ({args.branch})")

    # 1. Verificar entorno Git
    try:
        run_command(["git", "rev-parse", "--is-inside-work-tree"])
    except SystemExit:
        print("❌ Error: No estás dentro de un repositorio Git.")
        sys.exit(1)

    # 2. Configurar remote 'template'
    remotes = run_command(["git", "remote"])
    if "template" not in remotes.split():
        print("➕ Añadiendo remote 'template'...")
        run_command(["git", "remote", "add", "template", args.template_url])
    else:
        print("ℹ️ Remote 'template' ya existe. Asegurando URL correcta...")
        run_command(["git", "remote", "set-url", "template", args.template_url])

    # 3. Fetch
    print("⬇️ Descargando cambios (fetch)...")
    run_command(["git", "fetch", "template"])

    # 4. Merge
    print(f"🔀 Fusionando template/{args.branch}...")
    try:
        # Permitimos historias no relacionadas por si el proyecto derivado se reinició
        run_command(["git", "merge", f"template/{args.branch}", "--allow-unrelated-histories"], check=False)
        print("✅ Actualización completada exitosamente.")
    except subprocess.CalledProcessError:
        print("\n⚠️  CONFLICTOS DETECTADOS")
        print("   Git ha detenido la fusión automática.")
        print("   ACCIÓN REQUERIDA: Resuelve los conflictos manualmente y ejecuta 'git commit'.")
        sys.exit(1)


if __name__ == "__main__":
    main()
