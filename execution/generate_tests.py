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
    print(json.dumps({"status": "error", "message": "No se pudo importar chat_with_llm.py."}), file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Generar tests unitarios automáticamente.")
    parser.add_argument("--file", required=True, help="Ruta del archivo para el cual generar tests.")
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

    filename = os.path.basename(file_path)
    test_filename = f"test_{filename}"
    test_file_path = os.path.join(os.path.dirname(file_path), test_filename)

    prompt = f"""Actúa como un Ingeniero de QA experto en Python.
Tu tarea es escribir una suite de pruebas unitarias (usando `unittest`) para el siguiente código.

CÓDIGO A PROBAR ({filename}):
{original_code}

REQUISITOS:
1. Importa el módulo o las funciones necesarias. Asume que el archivo de test está en el mismo directorio que el código fuente.
2. Cubre los casos de éxito y los casos de error (edge cases).
3. Usa la librería estándar `unittest`.
4. Si el código usa librerías externas o llamadas al sistema (como requests, subprocess, os), usa `unittest.mock` para simularlas.
5. Devuelve ÚNICAMENTE el código Python completo y válido.
6. No uses bloques de markdown.
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

    # Limpieza de Markdown
    if new_code.startswith("```python"):
        new_code = new_code.replace("```python", "", 1)
    elif new_code.startswith("```"):
        new_code = new_code.replace("```", "", 1)
    if new_code.endswith("```"):
        new_code = new_code[:-3]

    new_code = new_code.strip()

    # Validación de Sintaxis
    try:
        ast.parse(new_code)
    except SyntaxError as e:
        print(json.dumps({"status": "error", "message": f"El código generado tiene errores de sintaxis: {e}"}))
        sys.exit(1)

    # Guardado
    try:
        with open(test_file_path, 'w', encoding='utf-8') as f:
            f.write(new_code)
        print(json.dumps({"status": "success", "message": f"Tests generados en {test_file_path}"}))
    except Exception as e:
        print(json.dumps({"status": "error", "message": f"Error escribiendo archivo: {e}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
