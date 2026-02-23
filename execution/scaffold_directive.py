#!/usr/bin/env python3
import argparse
import os
import sys

TEMPLATE = """goal: "{goal}"
required_inputs:
  - name: "input_1"
    description: "Descripción del primer input necesario."
steps:
  - step: "Nombre del Paso 1"
    script_to_invoke: "execution/script_name.py"
    description: "Descripción de qué hace este paso."
    inputs:
      - name: "--arg1"
        value: "{{{{input_1}}}}"
expected_outputs:
  - "Descripción del resultado esperado."
edge_cases:
  - case: "Posible error conocido"
    protocol: "Cómo recuperarse del error."
"""


def main():
    parser = argparse.ArgumentParser(description="Genera un esqueleto para una nueva directiva.")
    parser.add_argument("--filename", required=True, help="Nombre del archivo (ej. nueva_tarea.yaml)")
    parser.add_argument("--goal", required=True, help="Objetivo de la directiva")

    args = parser.parse_args()

    # Asegurar extensión .yaml
    filename = args.filename
    if not filename.endswith('.yaml') and not filename.endswith('.yml'):
        filename += '.yaml'

    # Rutas
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    directives_dir = os.path.join(project_root, "directives")
    target_path = os.path.join(directives_dir, filename)

    # Validar existencia
    if os.path.exists(target_path):
        print(f"❌ Error: El archivo '{filename}' ya existe en directives/.")
        sys.exit(1)

    # Crear contenido
    content = TEMPLATE.format(goal=args.goal)

    try:
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Directiva creada exitosamente: directives/{filename}")
        print("   Recuerda editar los pasos y los inputs según tus necesidades.")
    except Exception as e:
        print(f"❌ Error escribiendo archivo: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
