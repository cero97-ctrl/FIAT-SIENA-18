#!/usr/bin/env python3
import argparse
import os
import sys
import json
import ast

# Añadir el directorio actual al path para importar chat_with_llm
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from chat_with_llm import chat_openai, chat_anthropic, chat_gemini
except ImportError:
    print(json.dumps(
        {"status": "error", "message": "No se pudo importar chat_with_llm.py. Asegúrate de que existe en execution/."}), file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Añadir docstrings automáticamente a código Python.")
    parser.add_argument("--file", required=True, help="Ruta del archivo a documentar.")
    args = parser.parse_args()

    file_path = args.file

    if not os.path.exists(file_path):
        print(json.dumps({"status": "error", "message": f"Archivo no encontrado: {file_path}"}))
        sys.exit(1)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_code = f.read()
    except Exception as e:
        print(json.dumps({"status": "error", "message": f"Error leyendo archivo: {e}"}))
        sys.exit(1)

    # 1. Análisis previo para ahorrar tokens
    try:
        tree = ast.parse(original_code)
        missing_docs = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                if not ast.get_docstring(node):
                    missing_docs.append(node.name)

        if not missing_docs:
            print(json.dumps({"status": "success", "message": "El archivo ya está completamente documentado."}))
            sys.exit(0)

    except SyntaxError:
        print(json.dumps({"status": "error", "message": "El archivo tiene errores de sintaxis y no se puede procesar."}))
        sys.exit(1)

    # 2. Generación con LLM
    prompt = f"""Actúa como un Ingeniero de Software Senior experto en Python.
Tu tarea es añadir docstrings (formato Google Style) al siguiente código.

REGLAS:
1. Solo añade docstrings a las funciones y clases que NO los tengan.
2. NO cambies la lógica, nombres de variables ni el código funcional.
3. Devuelve ÚNICAMENTE el código Python completo y válido.
4. No uses bloques de markdown.

CÓDIGO A DOCUMENTAR ({file_path}):
{original_code}
"""

    messages = [{"role": "user", "content": prompt}]

    response = {}
    if os.getenv("OPENAI_API_KEY"):
        response = chat_openai(messages, model="gpt-4o")
    elif os.getenv("ANTHROPIC_API_KEY"):
        response = chat_anthropic(messages, model="claude-3-5-sonnet-20240620")
    elif os.getenv("GOOGLE_API_KEY"):
        response = chat_gemini(messages)
    else:
        print(json.dumps({"status": "error", "message": "No se encontraron API Keys configuradas en .env"}))
        sys.exit(1)

    if "error" in response:
        print(json.dumps({"status": "error", "message": response["error"]}))
        sys.exit(1)

    new_code = response.get("content", "")

    # Limpieza de respuesta
    if new_code.startswith("```python"):
        new_code = new_code.replace("```python", "", 1)
    elif new_code.startswith("```"):
        new_code = new_code.replace("```", "", 1)
    if new_code.endswith("```"):
        new_code = new_code[:-3]

    new_code = new_code.strip()

    # 3. Validación de seguridad (Sintaxis)
    try:
        ast.parse(new_code)
    except SyntaxError as e:
        print(json.dumps({"status": "error", "message": f"El código generado tiene errores de sintaxis: {e}"}))
        sys.exit(1)

    # 4. Guardado
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_code)
        print(json.dumps({"status": "success",
              "message": f"Se añadieron docstrings a {len(missing_docs)} elementos en {file_path}."}))
    except Exception as e:
        print(json.dumps({"status": "error", "message": f"Error escribiendo archivo: {e}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
