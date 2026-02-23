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
    parser = argparse.ArgumentParser(description="Refactorizar código usando LLM.")
    parser.add_argument("--file", required=True, help="Ruta del archivo a refactorizar.")
    parser.add_argument("--issues", required=True, help="Lista de problemas a corregir.")
    args = parser.parse_args()

    file_path = args.file
    issues = args.issues

    if not os.path.exists(file_path):
        print(json.dumps({"status": "error", "message": f"Archivo no encontrado: {file_path}"}))
        sys.exit(1)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_code = f.read()
    except Exception as e:
        print(json.dumps({"status": "error", "message": f"Error leyendo archivo: {e}"}))
        sys.exit(1)

    prompt = f"""Actúa como un Ingeniero de Software Senior y experto en Python.
Tu tarea es refactorizar el siguiente código para corregir los problemas reportados.

PROBLEMAS DETECTADOS:
{issues}

CÓDIGO ORIGINAL ({file_path}):
{original_code}

INSTRUCCIONES:
1. Devuelve ÚNICAMENTE el código corregido completo.
2. NO incluyas bloques de markdown (```python ... ```) si es posible, solo el código raw.
3. NO incluyas explicaciones ni texto adicional.
4. Mantén la funcionalidad original, solo arregla los problemas mencionados y mejora la calidad (docstrings, tipos, etc).
"""

    messages = [{"role": "user", "content": prompt}]

    # Intentar usar el modelo más capaz disponible (GPT-4o o Claude 3.5 Sonnet)
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

    # Limpieza de Markdown por si el LLM incluye bloques de código
    if new_code.startswith("```python"):
        new_code = new_code.replace("```python", "", 1)
    elif new_code.startswith("```"):
        new_code = new_code.replace("```", "", 1)

    if new_code.endswith("```"):
        new_code = new_code[:-3]

    new_code = new_code.strip()

    # Validación de Sintaxis (Safety Check)
    try:
        ast.parse(new_code)
    except SyntaxError as e:
        print(json.dumps({"status": "error", "message": f"El código generado tiene errores de sintaxis y fue rechazado: {e}"}))
        sys.exit(1)

    # Guardado
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_code)
        print(json.dumps({"status": "success", "message": f"Archivo {file_path} refactorizado exitosamente."}))
    except Exception as e:
        print(json.dumps({"status": "error", "message": f"Error escribiendo archivo: {e}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
