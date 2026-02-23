#!/usr/bin/env python3
import os
import sys

# Intentar cargar variables de entorno
try:
    from dotenv import load_dotenv, find_dotenv
    # Busca el archivo .env automáticamente en directorios superiores si no está en el actual
    env_file = find_dotenv(usecwd=True)
    if env_file:
        load_dotenv(env_file)
        print(f"📂 Archivo .env cargado desde: {env_file}")
    else:
        print("⚠️ No se encontró archivo .env (se intentará usar variables de entorno del sistema)")
except ImportError:
    print("Nota: python-dotenv no instalado, leyendo variables de entorno del sistema.")

try:
    import google.generativeai as genai
    from google.api_core import exceptions
except ImportError:
    print("❌ Error: La librería 'google-generativeai' no está instalada.")
    print("   Ejecuta: pip install -r requirements.txt")
    sys.exit(1)


def main():
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        print("❌ Error: GOOGLE_API_KEY no encontrada. Asegúrate de tener un archivo .env válido.")
        sys.exit(1)

    print(f"🔑 Usando API Key: {api_key[:4]}...{api_key[-4:]}")
    print("📡 Configurando cliente Gemini...")

    import warnings
    warnings.filterwarnings("ignore")  # Suppress deprecation warnings

    try:
        genai.configure(api_key=api_key)

        try:
            # Intentamos usar gemini-1.5-flash directamente por ser más rápido y moderno
            target_model = 'gemini-1.5-flash'
            print(f"\n🤖 Intentando generar contenido con modelo: {target_model}...")
            model = genai.GenerativeModel(target_model)
            response = model.generate_content("Hola, ¿estás operativo? Responde con un saludo breve.")

        except Exception as e:
            print(f"⚠️ Falló con '{target_model}' ({e})")

            # Intento 2: gemini-flash-latest
            try:
                target_model = 'gemini-flash-latest'
                print(f"🔄 Intentando con fallback: '{target_model}'...")
                model = genai.GenerativeModel(target_model)
                response = model.generate_content("Hola, ¿estás operativo? Responde con un saludo breve.")

            except Exception as e2:
                print(f"⚠️ Falló con '{target_model}' ({e2})")

                # Intento 3: gemini-pro-latest
                try:
                    target_model = 'gemini-pro-latest'
                    print(f"🔄 Intentando con fallback: '{target_model}'...")
                    model = genai.GenerativeModel(target_model)
                    response = model.generate_content("Hola, ¿estás operativo? Responde con un saludo breve.")
                except Exception as e3:
                    # Si todo falla, lanza el último error para que se capture abajo
                    print(f"❌ Todos los intentos fallaron.")
                    raise e3

        print("\n✅ ¡CONEXIÓN EXITOSA!")
        print(f"📝 Respuesta ({target_model}): {response.text}")

    except exceptions.InvalidArgument as e:
        print(f"\n❌ Error de Argumento (posiblemente API Key inválida o modelo no encontrado): {e}")
    except exceptions.PermissionDenied as e:
        print(f"\n❌ Error de Permiso (API Key sin acceso o expirada): {e}")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
