#!/usr/bin/env python3
import os
import ast
import sys
import json


def audit_file(filepath):
    """
    Analiza un archivo Python individual buscando problemas comunes.
    """
    issues = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        lines = content.splitlines()

        # 1. Análisis de Texto (Línea por línea)
        for i, line in enumerate(lines):
            # Líneas muy largas (PEP8 sugiere 79, aquí somos laxos con 120)
            if len(line) > 120:
                issues.append({
                    "line": i + 1,
                    "severity": "low",
                    "type": "style",
                    "message": f"Línea demasiado larga ({len(line)} > 120 caracteres)"
                })

            # Marcadores de deuda técnica
            if "TODO" in line or "FIXME" in line:
                issues.append({
                    "line": i + 1,
                    "severity": "info",
                    "type": "debt",
                    "message": "Marcador TODO/FIXME detectado"
                })

        # 2. Análisis de Árbol de Sintaxis Abstracta (AST)
        try:
            tree = ast.parse(content)

            for node in ast.walk(tree):
                # Falta de Docstrings en funciones y clases
                if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                    if not ast.get_docstring(node):
                        # Ignorar funciones privadas/mágicas simples si se desea, aquí reportamos todo
                        issues.append({
                            "line": node.lineno,
                            "severity": "medium",
                            "type": "doc",
                            "message": f"Falta docstring en '{node.name}'"
                        })

                # Cláusulas except vacías (Bare except)
                if isinstance(node, ast.ExceptHandler):
                    if node.type is None:
                        issues.append({
                            "line": node.lineno,
                            "severity": "high",
                            "type": "risk",
                            "message": "Uso de 'except:' desnudo (captura todo). Usa 'except Exception:' como mínimo."
                        })

        except SyntaxError as e:
            issues.append({
                "line": e.lineno,
                "severity": "critical",
                "type": "syntax",
                "message": f"Error de Sintaxis: {e.msg}"
            })

    except Exception as e:
        issues.append({
            "line": 0,
            "severity": "error",
            "type": "io",
            "message": f"No se pudo leer el archivo: {str(e)}"
        })

    return issues


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    report = {}
    total_issues = 0

    # Directorios a ignorar
    ignore_dirs = {'.git', '.tmp', '__pycache__', 'venv', 'env', '.venv', '.gemini'}

    for root, dirs, files in os.walk(project_root):
        # Filtrar directorios ignorados
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, project_root)

                file_issues = audit_file(filepath)
                if file_issues:
                    report[rel_path] = file_issues
                    total_issues += len(file_issues)

    # Salida JSON estructurada
    output = {
        "status": "success",
        "total_issues": total_issues,
        "files_scanned": len(report),
        "details": report
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
