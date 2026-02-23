#!/usr/bin/env python3
import argparse
import os
import sys
import json

# Añadir el directorio actual al path para importar chat_with_llm
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from chat_with_llm import chat_openai, chat_anthropic, chat_gemini
except ImportError:
    print(json.dumps({"status": "error", "message": "No se pudo importar chat_with_llm.py."}), file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Explicar código paso a paso usando IA.")
    parser.add_argument("--file", required=True, help="Ruta del archivo a explicar.")
    args = parser.parse_args()

    file_path = args.file

    if not os.path.exists(file_path):
        print(json.dumps({"status": "error", "message": f"Archivo no encontrado: {file_path}"}))
        sys.exit(1)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code_content = f.read()
    except Exception as e:
        print(json.dumps({"status": "error", "message": f"Error leyendo archivo: {e}"}))
        sys.exit(1)

    prompt = f"""Actúa como un Ingeniero de Software Senior y Profesor. Explica el siguiente código Python paso a paso.
Céntrate en la lógica, el flujo de datos y el propósito de las funciones clave.

CÓDIGO A EXPLICAR ({os.path.basename(file_path)}):
{code_content}

FORMATO DE SALIDA:
Markdown. Usa encabezados para separar secciones (Resumen, Análisis Detallado, Conclusión).
"""

    messages = [{"role": "user", "content": prompt}]

    # Llamada al LLM (Priorizando Gemini por solicitud explícita)
    response = {}
    if os.getenv("GOOGLE_API_KEY"):
        response = chat_gemini(messages)
    elif os.getenv("OPENAI_API_KEY"):
        response = chat_openai(messages, model="gpt-4o")
    elif os.getenv("ANTHROPIC_API_KEY"):
        response = chat_anthropic(messages, model="claude-3-5-sonnet-20240620")
    else:
        print(json.dumps({"status": "error", "message": "No se encontraron API Keys configuradas en .env"}))
        sys.exit(1)

    if "error" in response:
        print(json.dumps({"status": "error", "message": response["error"]}))
        sys.exit(1)

    content = response.get("content", "")
    print(content)


if __name__ == "__main__":
    main()
