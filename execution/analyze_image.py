#!/usr/bin/env python3
import argparse
import json
import os
import sys

# Intentar cargar variables de entorno
try:
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv(usecwd=True))
except ImportError:
    pass

try:
    import google.generativeai as genai
    import PIL.Image
except ImportError:
    print(json.dumps({"status": "error", "message": "Faltan librerías. Ejecuta: pip install google-generativeai pillow"}))
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Analizar una imagen usando IA (Vision).")
    parser.add_argument("--image", required=True, help="Ruta local a la imagen.")
    parser.add_argument("--prompt", default="Describe esta imagen técnicamente.", help="Pregunta sobre la imagen.")
    args = parser.parse_args()

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print(json.dumps({"status": "error", "message": "Falta GOOGLE_API_KEY en .env"}))
        sys.exit(1)

    if not os.path.exists(args.image):
        print(json.dumps({"status": "error", "message": f"Imagen no encontrada: {args.image}"}))
        sys.exit(1)

    try:
        genai.configure(api_key=api_key)
        
        # Usamos gemini-1.5-flash que es excelente para visión y rápido
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        img = PIL.Image.open(args.image)
        
        # Contexto de sistema para enfocarlo en mecánica
        system_context = "Eres SienaExpert-1.8, un mecánico experto. Analiza la imagen buscando componentes de auto, fallas visibles, fugas o códigos de error."
        full_prompt = f"{system_context}\n\nConsulta del usuario: {args.prompt}"

        response = model.generate_content([full_prompt, img])
        
        print(json.dumps({
            "status": "success",
            "description": response.text
        }))

    except Exception as e:
        print(json.dumps({
            "status": "error",
            "message": str(e)
        }))

if __name__ == "__main__":
    main()