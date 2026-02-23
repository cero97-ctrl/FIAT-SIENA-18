#!/usr/bin/env python3
import sys
import os
import json
import argparse

# Añadir el directorio actual al path para importar chat_with_llm
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import speech_recognition as sr
except ImportError:
    print(json.dumps(
        {"status": "error", "message": "Librería 'SpeechRecognition' no encontrada. Instala: pip install SpeechRecognition PyAudio"}), file=sys.stderr)
    sys.exit(1)

try:
    from chat_with_llm import chat_gemini, chat_openai, chat_anthropic
except ImportError:
    print(json.dumps({"status": "error", "message": "No se pudo importar chat_with_llm.py"}), file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Interfaz de voz para el agente.")
    parser.add_argument("--provider", choices=["openai", "anthropic", "gemini"],
                        default="gemini", help="Proveedor de IA.")
    args = parser.parse_args()

    r = sr.Recognizer()

    print("🎤 Iniciando interfaz de voz...")
    print("   (Asegúrate de tener un micrófono conectado)")

    try:
        with sr.Microphone() as source:
            print("   Ajustando ruido ambiental... (espera 1s)")
            r.adjust_for_ambient_noise(source, duration=1)
            print("🗣️  ¡Escuchando! Di algo...")

            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=10)
                print("⏳ Procesando audio...")

                # Usar Google Speech Recognition (gratis, no requiere API key extra para pruebas básicas)
                text = r.recognize_google(audio, language="es-ES")
                print(f"📝 Transcripción: '{text}'")

                # Enviar al agente
                print(f"🤖 Enviando a {args.provider}...")

                messages = [{"role": "user", "content": text}]

                response = {}
                if args.provider == "gemini":
                    response = chat_gemini(messages)
                elif args.provider == "openai":
                    response = chat_openai(messages)
                elif args.provider == "anthropic":
                    response = chat_anthropic(messages)

                if "content" in response:
                    print(f"\n🤖 Agente: {response['content']}\n")
                elif "error" in response:
                    print(f"\n❌ Error del Agente: {response['error']}\n")

            except sr.WaitTimeoutError:
                print("❌ Tiempo de espera agotado. No se detectó voz.")
            except sr.UnknownValueError:
                print("❌ No se pudo entender el audio.")
            except sr.RequestError as e:
                print(f"❌ Error del servicio de reconocimiento: {e}")

    except OSError as e:
        print(f"❌ Error de dispositivo de audio: {e}")
        print("   Asegúrate de tener PyAudio instalado correctamente.")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")


if __name__ == "__main__":
    main()
