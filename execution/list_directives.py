#!/usr/bin/env python3
import os
import glob
import yaml
import sys


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    directives_dir = os.path.join(project_root, 'directives')

    if not os.path.exists(directives_dir):
        print(f"❌ No se encontró el directorio: {directives_dir}")
        sys.exit(1)

    yaml_files = glob.glob(os.path.join(directives_dir, "*.yaml"))

    print("\n🤖 **Capacidades Disponibles (Directivas)**\n")
    print(f"{'DIRECTIVA':<35} | {'OBJETIVO'}")
    print("-" * 35 + "-+-" + "-" * 60)

    directives_list = []

    for filepath in yaml_files:
        filename = os.path.basename(filepath)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                goal = data.get('goal', 'Sin objetivo definido.')
                # Truncar objetivo si es muy largo para visualización limpia
                if len(goal) > 80:
                    goal = goal[:77] + "..."
                directives_list.append((filename, goal))
        except Exception as e:
            directives_list.append((filename, f"Error leyendo archivo: {e}"))

    # Ordenar alfabéticamente
    directives_list.sort(key=lambda x: x[0])

    for name, goal in directives_list:
        print(f"{name:<35} | {goal}")

    print("\n💡 Usa estas directivas como guía para solicitar tareas al agente.")
    print(f"   Total: {len(directives_list)} directivas encontradas.")


if __name__ == "__main__":
    main()
