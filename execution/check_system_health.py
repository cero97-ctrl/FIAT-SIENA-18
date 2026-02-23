#!/usr/bin/env python3
import sys
import os
import importlib.util

def check_python_version():
    required_version = (3, 10)
    current_version = sys.version_info
    if current_version < required_version:
        print(f"❌ Python {required_version[0]}.{required_version[1]}+ requerido. Tienes {current_version.major}.{current_version.minor}")
        return False
    print(f"✅ Python {current_version.major}.{current_version.minor} detectado.")
    return True

def check_env_file():
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    if not os.path.exists(env_path):
        print("❌ Archivo .env no encontrado. Ejecuta 'cp .env.example .env' o crea uno.")
        return False
    
    # Verificar contenido básico
    has_keys = False
    with open(env_path, 'r') as f:
        content = f.read()
        if "API_KEY" in content:
            has_keys = True
    
    if has_keys:
        print("✅ Archivo .env encontrado y parece configurado.")
    else:
        print("⚠️  Archivo .env existe pero no parece tener API KEYS configuradas.")
    return True

def check_directories():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    required_dirs = ["directives", "execution", ".gemini", ".tmp"]
    missing = []
    for d in required_dirs:
        if not os.path.exists(os.path.join(root, d)):
            missing.append(d)
    
    if missing:
        print(f"❌ Directorios faltantes: {', '.join(missing)}")
        # Intentar crear .tmp si falta, ya que es temporal
        if ".tmp" in missing:
            os.makedirs(os.path.join(root, ".tmp"))
            print("   🔧 Directorio .tmp/ recreado automáticamente.")
            missing.remove(".tmp")
        
        if missing: return False
    
    print("✅ Estructura de directorios correcta.")
    return True

def check_dependencies():
    # Lista de importaciones críticas para el funcionamiento base
    libs = ["dotenv", "yaml", "requests", "chromadb", "google.generativeai"]
    missing = []
    for lib in libs:
        if importlib.util.find_spec(lib) is None:
            missing.append(lib)
    
    if missing:
        print(f"❌ Dependencias faltantes: {', '.join(missing)}")
        print("   Ejecuta: pip install -r requirements.txt")
        return False
    print("✅ Dependencias críticas detectadas.")
    return True

def main():
    print("🔍 Iniciando Chequeo de Salud del Sistema...\n")
    checks = [
        check_python_version(),
        check_directories(),
        check_env_file(),
        check_dependencies()
    ]
    
    if all(checks):
        print("\n🚀 Todo listo. El sistema está saludable.")
        sys.exit(0)
    else:
        print("\n⚠️  Se encontraron problemas. Revisa los logs anteriores.")
        sys.exit(1)

if __name__ == "__main__":
    main()