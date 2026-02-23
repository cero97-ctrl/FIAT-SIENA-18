#!/usr/bin/env python3
import argparse
import os
import sys
import json
import glob
import shutil

try:
    import yaml
except ImportError:
    yaml = None
    print("⚠️  PyYAML no instalado. La descripción de directivas será limitada.", file=sys.stderr)

# Añadir el directorio actual al path para importar chat_with_llm
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from chat_with_llm import chat_openai, chat_anthropic, chat_gemini
except ImportError:
    print(json.dumps({"status": "error", "message": "No se pudo importar chat_with_llm.py."}), file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Generar README.md automáticamente.")
    parser.add_argument("--name", required=True, help="Nombre del proyecto.")
    args = parser.parse_args()

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    directives_dir = os.path.join(project_root, "directives")
    readme_path = os.path.join(project_root, "README.md")

    # 1. Recopilar contexto del proyecto
    directives = []
    if os.path.exists(directives_dir):
        for f in glob.glob(os.path.join(directives_dir, "*.yaml")):
            filename = os.path.basename(f)
            description = ""
            if yaml:
                try:
                    with open(f, 'r', encoding='utf-8') as yf:
                        data = yaml.safe_load(yf)
                        description = data.get('goal', 'Sin descripción')
                except Exception as e:
                    description = f"(Error leyendo YAML: {e})"
            
            entry = f"- **{filename}**: {description}" if description else f"- {filename}"
            directives.append(entry)

    structure = []
    # Escaneo limitado de estructura para dar contexto al LLM
    for root, dirs, files in os.walk(project_root):
        # Ignorar carpetas ruidosas
        if any(x in root for x in [".git", ".tmp", "__pycache__", ".gemini", "venv", "env"]):
            continue

        level = root.replace(project_root, '').count(os.sep)
        indent = ' ' * 4 * (level)
        structure.append(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            if not f.startswith("."):
                structure.append(f"{subindent}{f}")

    # Limitar el tamaño de la estructura para no saturar el prompt
    structure_str = "\n".join(structure[:60])

    # 2. Construir Prompt
    prompt = f"""Actúa como un Technical Writer experto. Genera un archivo README.md profesional para el siguiente proyecto.

NOMBRE DEL PROYECTO: {args.name}

ESTRUCTURA DE ARCHIVOS (Resumen):
{structure_str}

DIRECTIVAS DISPONIBLES (Capacidades del Agente):
{chr(10).join(directives)}

REQUISITOS:
1. Usa formato Markdown estándar.
2. Incluye secciones: Título, Descripción, Instalación (asume Python/Conda), Uso (menciona execution/run_agent.py) y Capacidades.
3. Sé conciso pero informativo.
4. Devuelve ÚNICAMENTE el contenido del markdown, sin bloques de código ```markdown envolventes si es posible.
"""

    messages = [{"role": "user", "content": prompt}]

    # 3. Llamar al LLM
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

    content = response.get("content", "")

    # Limpieza de formato Markdown
    if content.startswith("```markdown"):
        content = content.replace("```markdown", "", 1)
    elif content.startswith("```"):
        content = content.replace("```", "", 1)
    if content.endswith("```"):
        content = content[:-3]

    # 4. Guardar archivo (con backup)
    if os.path.exists(readme_path):
        shutil.move(readme_path, readme_path + ".bak")
        print(f"ℹ️  README.md existente respaldado como README.md.bak")

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content.strip())

    print(json.dumps({"status": "success", "message": "README.md generado exitosamente."}))


if __name__ == "__main__":
    main()
