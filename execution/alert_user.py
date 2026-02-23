#!/usr/bin/env python3
import sys
import time


def main():
    """
    Emite una alerta audible y visual para notificar al usuario.
    Sigue el protocolo definido en README.md.
    """
    if len(sys.argv) < 2:
        print("Usage: python3 execution/alert_user.py [success|waiting|error]")
        sys.exit(1)

    alert_type = sys.argv[1].lower()

    # Feedback visual
    icons = {"success": "✅", "waiting": "⏳", "error": "❌"}
    icon = icons.get(alert_type, "🔔")
    print(f"\n{icon} ALERT: {alert_type.upper()}\n")

    # Feedback auditivo (System Bell)
    # Se usa print("\a") que es cross-platform para la terminal.
    try:
        if alert_type == "success":
            print("\a", end="", flush=True)
        elif alert_type == "waiting":
            # Doble beep para llamar la atención
            print("\a", end="", flush=True)
            time.sleep(0.5)
            print("\a", end="", flush=True)
        else:
            # Triple beep rápido para errores
            for _ in range(3):
                print("\a", end="", flush=True)
                time.sleep(0.2)
    except Exception:
        pass  # Fallback silencioso si falla el audio


if __name__ == "__main__":
    main()
