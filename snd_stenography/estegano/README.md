# Stack Educativo de Esteganografía LSB

Este proyecto es un stack de herramientas de esteganografía desarrollado con fines puramente educativos para la materia de **Temas Selectos de Seguridad de la Información** en **ENES Juriquilla, UNAM**.

El objetivo es enseñar los fundamentos matemáticos y de programación detrás de la ocultación de información mediante la técnica de **Least Significant Bit (LSB)** en diferentes tipos de medios: imágenes, audio y video.

## ⚠️ ADVERTENCIA ACADÉMICA Y AVISO LEGAL

Este software ha sido desarrollado **EXCLUSIVAMENTE** con fines académicos.

1.  **Uso Ético:** La esteganografía es una herramienta de doble filo. El uso de estas técnicas para fines ilícitos está estrictamente prohibido por la ley.
2.  **Seguridad Operacional (OPSEC):** Estas implementaciones son básicas (LSB secuencial) para facilitar el aprendizaje. **NO son seguras** contra técnicas modernas de estegoanálisis. No las utilices para proteger información sensible real.
3.  **Criptografía:** La esteganografía oculta la *existencia* del mensaje, no su *contenido*. En entornos reales, la información debe ser cifrada antes de ser incrustada.

## 🛠️ Características

El stack permite la ocultación y extracción de mensajes de texto en tres tipos de archivos:

*   **Imágenes (`.png`):** Modificación de los bits menos significativos de los canales RGB. Se requiere formato PNG para asegurar que no haya pérdida por compresión.
*   **Audio (`.wav`):** Modificación de los bits menos significos de las muestras de audio PCM.
*   **Video:** Descomposición de frames, inyección de bits LSB y reconstrucción de la secuencia.

## 🚀 Instalación y Uso

El proyecto utiliza `uv` para la gestión de dependencias y entornos virtuales.

### 1. Preparación del entorno

Primero, asegúrate de tener instalado [uv](https://github.com/astral-sh/uv). Luego, inicializa el entorno:

```bash
# Instala las dependencias del proyecto
uv sync
```

### 2. Ejecución con el Script Maestro

La forma más sencilla de interactuar con el stack es a través de `master.py`, que actúa como una interfaz unificada.

#### Ocultar un mensaje

Para ocultar un mensaje en un archivo:

```bash
# Ejemplo en una imagen
uv run scripts/master.py ocultar --tipo imagen -a imagen_original.png -m "Mi mensaje secreto" -o imagen_stego.png

# Ejemplo en un audio
uv run scripts de stego_audio.py ocultar ... (o vía master.py)
uv run scripts/master.py ocultar --tipo audio -a audio_original.wav -m "Mensaje oculto" -o audio_stego.wav
```

#### Extraer un mensaje

Para recuperar el mensaje de un archivo:

```bash
# Ejemplo en una imagen
uv run scripts/master.py extraer --tipo imagen -a imagen_stego.png

# Ejemplo en un audio
uv run scripts/master.py extraer --tipo audio -a audio_stego.wav
```

## 📂 Estructura del Proyecto

*   `scripts/master.py`: Interfaz de línea de comandos (CLI) unificada.
*   `scripts/stego_image.py`: Módulo para esteganografía en imágenes.
*   `scripts/stego_audio.py`: Módulo para esteganografía en audio.
*   `scripts/stego_video.py`: Módulo para esteganografía en video.
*   `AGENTS.md`: Directivas de desarrollo y estándares del proyecto.

## 🎓 Información Académica

*   **Institución:** ENES Juriquilla, UNAM.
*   **Materia:** Temas Selectos de Seguridad de la Información.
