#!/usr/bin/env python3
import argparse
import os
import sys
import json
import glob
import subprocess
import datetime

# Añadir el directorio actual al path para importar chat_with_llm
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from chat_with_llm import chat_openai, chat_anthropic, chat_gemini
except ImportError:
    print(json.dumps({"status": "error", "message": "No se pudo importar chat_with_llm.py."}), file=sys.stderr)
    sys.exit(1)


def get_git_activity():
    try:
        # Obtener los últimos 10 commits
        cmd = ["git", "log", "-n", "10", "--pretty=format:%cd | %an | %s"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        return "No se pudo obtener el historial de git."
    except Exception:
        return "Git no está instalado o no es un repositorio."


def main():
    parser = argparse.ArgumentParser(description="Generar reporte semanal del proyecto.")
    args = parser.parse_args()

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    project_name = os.path.basename(project_root)
    directives_dir = os.path.join(project_root, "directives")
    report_path = os.path.join(project_root, "WEEKLY_REPORT.md")

    # 1. Recopilar Contexto
    directives = []
    if os.path.exists(directives_dir):
        for f in glob.glob(os.path.join(directives_dir, "*.yaml")):
            directives.append(os.path.basename(f))

    git_log = get_git_activity()

    # 2. Construir Prompt
    prompt = f"""Actúa como un Project Manager técnico. Genera un Resumen Ejecutivo Semanal para el siguiente proyecto.

NOMBRE DEL PROYECTO: {project_name}
FECHA: {datetime.date.today()}

ACTIVIDAD RECIENTE (Git Log):
{git_log}

CAPACIDADES ACTUALES (Directivas):
{', '.join(directives)}

REQUISITOS DEL REPORTE:
1. Título: Reporte de Estado - {project_name}
2. Resumen de Progreso: Basado en los commits recientes.
3. Capacidades Operativas: Qué puede hacer el agente ahora mismo.
4. Próximos Pasos Sugeridos: Basado en la trayectoria del desarrollo.
5. Formato Markdown profesional.
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

    # Limpieza
    if content.startswith("```markdown"):
        content = content.replace("```markdown", "", 1)
    elif content.startswith("```"):
        content = content.replace("```", "", 1)
    if content.endswith("```"):
        content = content[:-3]

    # 4. Guardar y Mostrar
    try:
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(content.strip())

        print(f"✅ Reporte generado exitosamente en: {report_path}")
        print("-" * 40)
        print(content.strip())
        print("-" * 40)
    except Exception as e:
        print(json.dumps({"status": "error", "message": f"Error escribiendo reporte: {e}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
