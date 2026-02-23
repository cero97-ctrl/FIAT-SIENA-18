#!/usr/bin/env python3
import argparse
import json
import sys
import os

try:
    import speech_recognition as sr
    from pydub import AudioSegment
except ImportError:
    print(json.dumps({"status": "error", "message": "Faltan librerías. Ejecuta: pip install SpeechRecognition pydub"}))
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Transcribir archivo de audio a texto.")
    parser.add_argument("--file", required=True, help="Ruta al archivo de audio.")
    parser.add_argument("--lang", default="es-ES", help="Código de idioma (ej: es-ES, en-US).")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(json.dumps({"status": "error", "message": "Archivo no encontrado"}))
        sys.exit(1)

    # Convertir OGG (Telegram) a WAV (Requerido por SpeechRecognition)
    wav_path = args.file + ".wav"
    try:
        audio = AudioSegment.from_file(args.file)
        audio.export(wav_path, format="wav")
    except Exception as e:
        print(f"Error pydub/ffmpeg: {e}", file=sys.stderr)
        print(json.dumps({"status": "error", "message": f"Error convirtiendo audio (¿Tienes ffmpeg instalado?): {e}"}))
        sys.exit(1)

    r = sr.Recognizer()
    try:
        with sr.AudioFile(wav_path) as source:
            # Escuchar el archivo
            audio_data = r.record(source)
            # Transcribir usando Google Web Speech API (Gratis, soporta español)
            text = r.recognize_google(audio_data, language=args.lang)
            print(json.dumps({"status": "success", "text": text}))
    except sr.UnknownValueError:
        print(json.dumps({"status": "error", "message": "No se pudo entender el audio."}))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
    finally:
        if os.path.exists(wav_path):
            os.remove(wav_path)

if __name__ == "__main__":
    main()