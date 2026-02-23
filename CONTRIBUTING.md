# Guía de Contribución

¡Gracias por tu interés en mejorar esta plantilla! Este documento describe cómo proponer cambios, reportar errores y contribuir al desarrollo del framework.

## Flujo de Trabajo (GitHub Flow)

1.  **Fork** del repositorio.
2.  **Crea una rama** (`git checkout -b feature/mi-mejora`).
3.  **Realiza tus cambios** (código, documentación, directivas).
4.  **Valida** que el sistema siga funcionando.
5.  **Commit** (`git commit -m "Añadir nueva directiva X"`).
6.  **Push** a tu fork (`git push origin feature/mi-mejora`).
7.  **Abre un Pull Request**.

## Estándares del Proyecto

### 1. Directivas (`directives/`)
*   Formato **YAML**.
*   Deben ser atómicas (una tarea principal).
*   Campos obligatorios: `goal`, `steps`, `required_inputs`.
*   Valida la sintaxis antes de subir:
    ```bash
    python execution/validate_directives.py
    ```

### 2. Scripts de Ejecución (`execution/`)
*   **Python 3.10+**.
*   Usa `argparse` para argumentos de línea de comandos.
*   Salida estándar (stdout) preferiblemente en **JSON** para que el agente pueda leerla.
*   Manejo de errores explícito (no dejes que el script explote sin mensaje).
*   **Sin credenciales**: Usa `python-dotenv` y carga desde `.env`.

### 3. Estilo y Limpieza
*   Mantén el repositorio limpio de archivos temporales (usa `.tmp/` para salidas).
*   No subas archivos `.env` o carpetas `__pycache__`.

## Validación Local

Antes de enviar tu PR, ejecuta el chequeo de salud del sistema:

```bash
python execution/check_system_health.py
```

## Reporte de Problemas

Usa la sección de **Issues** de GitHub para reportar bugs o discutir nuevas ideas antes de implementarlas.