#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

ENV_NAME="agent_env"

echo "🚀 Iniciando configuración automática del Gemini Agent Framework..."

# 1. Verificar Conda
if ! command -v conda &> /dev/null; then
    echo "❌ Error: Conda no está instalado o no está en el PATH."
    exit 1
fi

# 2. Verificar Git
if ! command -v git &> /dev/null; then
    echo "❌ Error: Git no está instalado. Es necesario para inicializar el repositorio."
    exit 1
fi

# 3. Crear Entorno
echo "📦 Creando entorno Conda: $ENV_NAME..."
# Usamos || true para que no falle si el entorno ya existe
conda create --name $ENV_NAME python=3.10 -y || echo "✅  Entorno '$ENV_NAME' detectado. Se reutilizará para este proyecto."

# 4. Activar Entorno (Truco para scripts bash)
echo "🔌 Activando entorno..."
eval "$(conda shell.bash hook)"
conda activate $ENV_NAME

# 5. Instalar Dependencias
echo "⬇️  Instalando dependencias..."
pip install -r requirements.txt

# 6. Ejecutar Inicialización del Proyecto
echo "⚙️  Configurando proyecto..."
read -p "Introduce el nombre de tu nuevo proyecto: " PROJECT_NAME

if [ -z "$PROJECT_NAME" ]; then
    PROJECT_NAME="Nuevo Proyecto"
fi

python execution/init_project.py --name "$PROJECT_NAME" --reset-git

echo ""
echo "✅ ¡Instalación completada!"
echo "⚠️  IMPORTANTE: No olvides editar el archivo .env con tus API Keys."
echo "👉 Para volver a entrar: 'conda activate $ENV_NAME' y luego 'python execution/run_agent.py'"