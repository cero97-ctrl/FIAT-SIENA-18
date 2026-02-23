#!/usr/bin/env python3
import os
import sys
import yaml
import glob


def validate_directive(filepath):
    """
    Valida un archivo de directiva YAML contra el esquema esperado.
    Retorna una lista de errores encontrados.
    """
    errors = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        return [f"Error de sintaxis YAML: {e}"]

    if not isinstance(data, dict):
        return ["El contenido raíz debe ser un diccionario/objeto."]

    # Campos obligatorios de nivel superior
    required_fields = ['goal', 'steps']
    for field in required_fields:
        if field not in data:
            errors.append(f"Falta el campo obligatorio: '{field}'")

    # Validar steps
    if 'steps' in data:
        if not isinstance(data['steps'], list):
            errors.append("'steps' debe ser una lista.")
        else:
            for i, step in enumerate(data['steps']):
                if not isinstance(step, dict):
                    errors.append(f"El paso #{i+1} no es un objeto.")
                    continue

                # Validar que tenga 'step' (identificador)
                if 'step' not in step:
                    errors.append(f"El paso #{i+1} falta el campo 'step' (identificador).")

                # Validar que tenga una acción definida (lógica o script)
                if 'action' not in step and 'script_to_invoke' not in step:
                    errors.append(
                        f"El paso #{i+1} debe tener 'action' (instrucción texto) o 'script_to_invoke' (ruta script).")

    # Validar required_inputs (si existe)
    if 'required_inputs' in data:
        if not isinstance(data['required_inputs'], list):
            errors.append("'required_inputs' debe ser una lista.")
        else:
            for i, inp in enumerate(data['required_inputs']):
                if not isinstance(inp, dict):
                    errors.append(f"Input #{i+1} en 'required_inputs' no es un objeto.")
                elif 'name' not in inp:
                    errors.append(f"Input #{i+1} en 'required_inputs' falta el campo 'name'.")

    # Validar edge_cases (recomendado, pero verificamos estructura si existe)
    if 'edge_cases' in data and isinstance(data['edge_cases'], list):
        for i, case in enumerate(data['edge_cases']):
            if isinstance(case, dict):
                if 'case' not in case:
                    errors.append(f"Edge case #{i+1} falta descripción 'case'.")

    return errors


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    directives_dir = os.path.join(project_root, 'directives')

    if not os.path.exists(directives_dir):
        print(f"❌ No se encontró el directorio: {directives_dir}")
        sys.exit(1)

    yaml_files = glob.glob(os.path.join(directives_dir, "*.yaml"))

    total_errors = 0
    print(f"🔍 Validando {len(yaml_files)} directivas en {directives_dir}...\n")

    for filepath in yaml_files:
        filename = os.path.basename(filepath)
        errors = validate_directive(filepath)

        if errors:
            print(f"❌ {filename}: FALLÓ")
            for err in errors:
                print(f"   - {err}")
            total_errors += 1
        else:
            print(f"✅ {filename}: OK")

    print("\n" + "="*40)
    if total_errors > 0:
        print(f"🔴 Se encontraron errores en {total_errors} directivas.")
        sys.exit(1)
    else:
        print("🟢 Todas las directivas son válidas.")
        sys.exit(0)


if __name__ == "__main__":
    main()
