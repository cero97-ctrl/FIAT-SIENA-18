#!/usr/bin/env python3
import subprocess
import sys
import os


def run_step(script_name, description):
    print(f"\n🔄 {description}...")
    # Asumimos que los scripts están en el mismo directorio que este
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script_name)

    try:
        # Ejecutamos el script y esperamos que termine con código 0
        subprocess.run([sys.executable, script_path], check=True)
        print(f"✅ {script_name}: PASÓ")
    except subprocess.CalledProcessError:
        print(f"❌ {script_name}: FALLÓ")
        print("⛔ Se detuvo el proceso debido a errores.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error inesperado ejecutando {script_name}: {e}")
        sys.exit(1)


def main():
    print("🛡️  Iniciando Protocolo de Calidad Pre-Commit")

    run_step("check_dependencies.py", "Verificando dependencias instaladas")
    run_step("format_code.py", "Aplicando formato estándar (autopep8)")
    run_step("audit_codebase.py", "Auditando calidad del código")
    run_step("run_tests.py", "Ejecutando pruebas unitarias")
    run_step("check_system_health.py", "Verificando integridad del framework")

    print("\n✨ Todo limpio. El proyecto está listo para 'git commit'.")


if __name__ == "__main__":
    main()
