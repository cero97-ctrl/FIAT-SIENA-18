#!/usr/bin/env python3
import sys
import os
import subprocess
import time
import json

# Colores ANSI para la terminal


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def type_effect(text, delay=0.01):
    """Simula el efecto de escritura de una IA."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print("")


def run_script(script_name, args=[]):
    """Ejecuta un script de la carpeta execution/."""
    script_path = os.path.join("execution", script_name)
    if not os.path.exists(script_path):
        print(f"{Colors.FAIL}❌ Error: Script {script_name} no encontrado.{Colors.ENDC}")
        return

    print(f"{Colors.WARNING}⚙️  Ejecutando {script_name}...{Colors.ENDC}")
    try:
        subprocess.run([sys.executable, script_path] + args)
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}⚠️  Ejecución interrumpida manualmente.{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}Error crítico: {e}{Colors.ENDC}")


def main():
    os.system('cls' if os.name == 'nt' else 'clear')

    print(f"{Colors.HEADER}{Colors.BOLD}🤖 GEMINI AGENT CLI (Simulated Mode){Colors.ENDC}")
    print(f"{Colors.HEADER}======================================{Colors.ENDC}")
    print("Bienvenido a la interfaz de orquestación.")
    print("Tú actúas como el 'Cerebro' (Layer 2). Usa este CLI para invocar herramientas.")
    print(f"Escribe {Colors.BOLD}/help{Colors.ENDC} para ver comandos disponibles o {Colors.BOLD}/exit{Colors.ENDC} para salir.\n")

    while True:
        try:
            # Input del usuario
            user_input = input(f"{Colors.GREEN}You (Orchestrator) > {Colors.ENDC}").strip()

            if not user_input:
                continue

            # Comandos del sistema
            if user_input.lower() in ["/exit", "exit", "quit"]:
                print(f"{Colors.BLUE}Gemini >{Colors.ENDC} Cerrando sesión. ¡Hasta luego!")
                break

            elif user_input.lower() in ["/help", "help"]:
                print(f"\n{Colors.BOLD}Comandos Disponibles:{Colors.ENDC}")
                print("  /list    -> Listar todas las directivas disponibles")
                print("  /memory  -> Listar los recuerdos guardados en la memoria")
                print("  /check   -> Verificar salud del sistema")
                print("  /run [script] [args] -> Ejecutar un script específico")
                print("  /ask [prompt] -> Consultar al LLM real (OpenAI/Anthropic)")
                print("  /telegram -> Iniciar modo escucha de Telegram (Bot)")
                print("  [texto]  -> Simular chat (echo)\n")

            elif user_input.lower() in ["/list", "list"]:
                run_script("list_directives.py")

            elif user_input.lower() in ["/check", "check"]:
                run_script("check_system_health.py")

            elif user_input.lower() in ["/memory", "/memories"]:
                run_script("list_memories.py")

            elif user_input.lower() in ["/telegram", "telegram"]:
                run_script("listen_telegram.py")

            elif user_input.lower().startswith("/run"):
                parts = user_input.split()
                if len(parts) < 2:
                    print(f"{Colors.FAIL}Uso: /run <nombre_script.py> [argumentos]{Colors.ENDC}")
                else:
                    script = parts[1]
                    args = parts[2:]
                    run_script(script, args)

            elif user_input.lower().startswith("/ask") or user_input.lower().startswith("/llm"):
                parts = user_input.split(maxsplit=1)
                if len(parts) < 2:
                    print(f"{Colors.FAIL}Uso: /ask <tu consulta>{Colors.ENDC}")
                    continue
                prompt = parts[1]

                # Conexión con LLM Real
                chat_script = os.path.join("execution", "chat_with_llm.py")

                if os.path.exists(chat_script):
                    sys.stdout.write(f"{Colors.BLUE}Gemini (Thinking...) > {Colors.ENDC}")
                    sys.stdout.flush()

                    # Ejecutar el script de chat capturando la salida
                    proc = subprocess.run(
                        [sys.executable, chat_script, "--prompt", prompt],
                        capture_output=True, text=True
                    )

                    # Borrar mensaje de "Thinking..."
                    print("\r" + " " * 50 + "\r", end="")
                    sys.stdout.write(f"{Colors.BLUE}Gemini > {Colors.ENDC}")

                    try:
                        data = json.loads(proc.stdout)
                        if "error" in data:
                            print(f"{Colors.FAIL}Error API: {data['error']}{Colors.ENDC}")
                        else:
                            type_effect(data.get("content", "No response."))
                    except json.JSONDecodeError:
                        # Fallback si el script falló y no devolvió JSON limpio
                        print(f"{Colors.FAIL}Error script: {proc.stderr or proc.stdout}{Colors.ENDC}")
                else:
                    print(f"{Colors.FAIL}❌ Error: Script execution/chat_with_llm.py no encontrado.{Colors.ENDC}")

            else:
                # Modo Simulado (Default)
                response = f"Recibido: '{user_input}'.\n(Estoy en modo simulado. Si necesitas inteligencia real, usa /ask <pregunta>)"
                sys.stdout.write(f"{Colors.BLUE}Gemini > {Colors.ENDC}")
                type_effect(response)

        except KeyboardInterrupt:
            print(f"\n{Colors.WARNING}Interrupción detectada. Usa /exit para salir.{Colors.ENDC}")
            continue
        except Exception as e:
            print(f"\n{Colors.FAIL}Error inesperado: {e}{Colors.ENDC}")
            continue


if __name__ == "__main__":
    main()
