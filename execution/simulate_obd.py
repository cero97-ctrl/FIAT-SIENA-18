#!/usr/bin/env python3
import argparse
import json
import random
import time
import sys

# Base de datos de fallas comunes del Siena 1.8 (Motor GM)
COMMON_DTCS = {
    "P0300": "Fallo de encendido aleatorio/múltiple detectado",
    "P0130": "Mal funcionamiento del circuito del sensor de O2 (Sonda Lambda)",
    "P0420": "Eficiencia del sistema de catalizador por debajo del umbral",
    "P0171": "Sistema demasiado pobre (Mezcla de combustible incorrecta)",
    "P0505": "Mal funcionamiento del sistema de control de ralentí (Válvula IAC)",
    "P0340": "Mal funcionamiento del circuito del sensor de posición del árbol de levas"
}

def main():
    parser = argparse.ArgumentParser(description="Simulador de escáner OBD-II para Fiat Siena 1.8.")
    parser.add_argument("--query", choices=["dtc", "rpm", "temp"], required=True, help="Dato a simular.")
    args = parser.parse_args()

    # Simular un pequeño retraso como un escáner real
    time.sleep(random.uniform(0.5, 2.0))

    if args.query == "dtc":
        # 30% de probabilidad de no tener códigos
        if random.random() < 0.3:
            result = {"status": "success", "data": {"codes": []}}
        else:
            # Devolver 1 o 2 códigos aleatorios
            num_codes = random.randint(1, 2)
            codes = random.sample(list(COMMON_DTCS.keys()), num_codes)
            result = {"status": "success", "data": {"codes": {code: COMMON_DTCS[code] for code in codes}}}
    elif args.query == "rpm":
        rpm = random.randint(840, 910)
        result = {"status": "success", "data": {"rpm": rpm}}
    elif args.query == "temp":
        temp = random.randint(88, 95)
        result = {"status": "success", "data": {"coolant_temp": temp}}
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()