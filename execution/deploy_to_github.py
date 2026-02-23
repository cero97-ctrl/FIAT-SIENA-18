#!/usr/bin/env python3
import argparse
import subprocess
import sys
import os


def run_command(command, check=True):
    """Ejecuta un comando de shell e imprime la salida."""
    try:
        print(f"Running: {' '.join(command)}")
        result = subprocess.run(command, check=check, text=True, capture_output=True)
        if result.stdout:
            print(result.stdout.strip())
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando: {' '.join(command)}")
        print(f"   Detalle: {e.stderr.strip()}")
        if check:
            sys.exit(1)
        return None


def main():
    parser = argparse.ArgumentParser(description="Automatizar git add, commit y push.")
    parser.add_argument("--message", required=True, help="Mensaje del commit.")
    parser.add_argument("--remote", help="URL del repositorio remoto (opcional).")
    parser.add_argument("--branch", default="main", help="Rama destino.")

    args = parser.parse_args()

    # 1. Verificar si es un repo git
    if not os.path.exists(".git"):
        print("⚠️  No se detectó repositorio git. Inicializando...")
        run_command(["git", "init"])
        # Renombrar rama master a main si es necesario
        run_command(["git", "branch", "-M", args.branch], check=False)

    # 2. Configurar Remote si se provee
    if args.remote:
        remotes = run_command(["git", "remote"], check=False) or ""
        if "origin" in remotes.split():
            print(f"ℹ️  Actualizando remote 'origin' a {args.remote}")
            run_command(["git", "remote", "set-url", "origin", args.remote])
        else:
            print(f"➕ Añadiendo remote 'origin': {args.remote}")
            run_command(["git", "remote", "add", "origin", args.remote])

    # 3. Git Add
    print("📦 Añadiendo archivos...")
    run_command(["git", "add", "."])

    # 4. Git Commit
    # Verificar si hay cambios para commitear
    status = run_command(["git", "status", "--porcelain"], check=False)
    if not status:
        print("✨ No hay cambios pendientes para commitear.")
    else:
        print(f"💾 Creando commit: '{args.message}'")
        run_command(["git", "commit", "-m", args.message])

    # 5. Git Push
    # Verificar si existe remote origin antes de intentar push
    remotes = run_command(["git", "remote"], check=False) or ""
    if "origin" not in remotes.split():
        print("❌ Error: No se ha configurado el repositorio remoto 'origin'.")
        print("   💡 Ejecuta el script nuevamente incluyendo: --remote <URL_DEL_REPO>")
        sys.exit(1)

    print(f"🚀 Subiendo a {args.branch}...")
    try:
        run_command(["git", "push", "-u", "origin", args.branch])
        print("✅ Despliegue completado exitosamente.")
    except SystemExit:
        print("❌ Falló el push. Verifica tus credenciales o la URL del remoto.")
        sys.exit(1)


if __name__ == "__main__":
    main()
