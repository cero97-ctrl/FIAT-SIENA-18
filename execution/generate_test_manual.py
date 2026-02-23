#!/usr/bin/env python3
import os
import sys
import subprocess

# Intentar importar fpdf, instalar si no existe
try:
    from fpdf import FPDF
except ImportError:
    print("📦 Instalando librería 'fpdf' para generar el manual...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "fpdf"])
    from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Manual Técnico - Fiat Siena 1.8 (Motor GM Powertrain)', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 6, title, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 5, body)
        self.ln()

def create_manual():
    # Definir rutas
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    docs_dir = os.path.join(project_root, "docs")
    os.makedirs(docs_dir, exist_ok=True)
    output_file = os.path.join(docs_dir, "manual_siena_18.pdf")

    pdf = PDF()
    pdf.add_page()

    # --- CONTENIDO TÉCNICO REAL DEL SIENA 1.8 ---
    
    pdf.chapter_title("1. Especificaciones del Motor")
    pdf.chapter_body(
        "Motor: GM Powertrain 1.8L 8 Válvulas\n"
        "Combustible: Nafta / Gasolina\n"
        "Orden de Encendido: 1 - 3 - 4 - 2\n"
        "Relación de Compresión: 9.4:1\n"
        "Potencia: 105 CV a 5400 RPM\n"
        "Ralentí: 850 +/- 50 RPM"
    )

    pdf.chapter_title("2. Pares de Apriete (Torques)")
    pdf.chapter_body(
        "IMPORTANTE: Respetar el orden de apriete en espiral desde el centro hacia afuera.\n\n"
        "Tapa de Cilindros (Culata):\n"
        " - 1ra Etapa: 25 Nm\n"
        " - 2da Etapa: 60 grados\n"
        " - 3ra Etapa: 60 grados\n"
        " - 4ta Etapa: 30 grados\n\n"
        "Bielas: 25 Nm + 30 grados\n"
        "Bancadas: 50 Nm + 45 grados + 15 grados\n"
        "Volante Motor: 35 Nm + 30 grados + 15 grados"
    )

    pdf.chapter_title("3. Fluidos y Mantenimiento")
    pdf.chapter_body(
        "Aceite de Motor: 5W30 Sintético (Recomendado: Selenia K o equivalente API SN).\n"
        "Capacidad de Aceite: 3.5 Litros (con filtro).\n"
        "Líquido Refrigerante: Paraflu UP (Rojo) al 50% con agua desmineralizada.\n"
        "Líquido de Frenos: DOT 4.\n"
        "Correa de Distribución: Reemplazar cada 60.000 km o 3 años."
    )

    pdf.chapter_title("4. Diagnóstico de Fallas Comunes")
    pdf.chapter_body(
        "Falla: Ralentí inestable o tirones al acelerar.\n"
        "Causa Probable: Cuerpo de mariposa sucio o descalibrado.\n"
        "Solución: Limpiar cuerpo de mariposa y realizar aprendizaje electrónico.\n\n"
        "Falla: Motor gira pero no arranca (Luz de inyección encendida).\n"
        "Causa Probable: Sensor de RPM (Sensor de cigüeñal) dañado o cable cortado.\n"
        "Solución: Verificar resistencia del sensor (debe estar entre 800 y 1200 Ohms)."
    )

    pdf.chapter_title("5. Presión de Neumáticos")
    pdf.chapter_body(
        "Uso Normal (Sin carga):\n"
        " - Delanteros: 28 PSI\n"
        " - Traseros: 28 PSI\n\n"
        "Con Carga Completa:\n"
        " - Delanteros: 32 PSI\n"
        " - Traseros: 35 PSI"
    )

    pdf.output(output_file)
    print(f"✅ Manual generado exitosamente en: {output_file}")
    print("   Ahora puedes probar la ingesta con: /ingestar manual_siena_18.pdf")

if __name__ == "__main__":
    create_manual()