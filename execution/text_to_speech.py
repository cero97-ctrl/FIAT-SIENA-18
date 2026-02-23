#!/usr/bin/env python3
import argparse
import json
import sys
import os
from gtts import gTTS
from pydub import AudioSegment

def main():
    parser = argparse.ArgumentParser(description="Convertir texto a audio (TTS).")
    parser.add_argument("--text", required=True, help="Texto a convertir.")
    parser.add_argument("--output", required=True, help="Ruta del archivo de salida (.ogg).")
    parser.add_argument("--lang", default="es", help="Código de idioma para la voz (ej: es, en).")
    args = parser.parse_args()

    try:
        # Limpiar un poco el texto de markdown básico para que no lea los asteriscos
        clean_text = args.text.replace("*", "").replace("_", "").replace("`", "")

        # Generar audio con gTTS (Google Text-to-Speech)
        tts = gTTS(text=clean_text, lang=args.lang)
        mp3_path = args.output + ".mp3"
        tts.save(mp3_path)

        # Convertir a OGG (Opus) para Telegram usando pydub/ffmpeg
        sound = AudioSegment.from_mp3(mp3_path)
        sound.export(args.output, format="ogg", codec="libopus")

        # Limpiar archivo intermedio
        if os.path.exists(mp3_path):
            os.remove(mp3_path)

        print(json.dumps({"status": "success", "file_path": args.output}))

    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()