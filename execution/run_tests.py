#!/usr/bin/env python3
import sys
import os
import subprocess
import unittest


def run_with_pytest():
    print("🧪 Ejecutando tests con pytest...")
    try:
        # Run pytest on the project root
        # sys.executable asegura que usamos el python del entorno actual
        result = subprocess.run([sys.executable, "-m", "pytest"], check=False)
        return result.returncode
    except Exception as e:
        print(f"❌ Error ejecutando pytest: {e}")
        return 1


def run_with_unittest(start_dir):
    print(f"🧪 Ejecutando tests con unittest (discover en {start_dir})...")

    # Descubrir tests que coincidan con test_*.py
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir, pattern="test_*.py")

    if suite.countTestCases() == 0:
        print("⚠️  No se encontraron tests con el patrón 'test_*.py'.")
        return 0

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return 0 if result.wasSuccessful() else 1


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    # Verificar si pytest está instalado
    try:
        import pytest
        has_pytest = True
    except ImportError:
        has_pytest = False

    if has_pytest:
        sys.exit(run_with_pytest())
    else:
        sys.exit(run_with_unittest(project_root))


if __name__ == "__main__":
    main()
