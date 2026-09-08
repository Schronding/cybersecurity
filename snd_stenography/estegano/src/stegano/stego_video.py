"""
Módulo: stego_video.py
Descripción: Ocultación y extracción de información en video usando LSB sobre fotogramas y códecs Lossless.

ADVERTENCIA ACADÉMICA Y AVISO LEGAL:
Este script ha sido desarrollado EXCLUSIVAMENTE para la clase de Temas Selectos de Seguridad de la Información (ENES Juriquilla). 

1. Uso Ético: La esteganografía es un arma de doble filo. El uso de estas técnicas para exfiltrar datos corporativos, evadir censura en contextos ilegales, o distribuir material ilícito está estrictamente prohibido y penado por la ley.
2. Consentimiento: Solo ejecuta estos scripts en archivos sobre los cuales tengas derechos de autor plenos o permiso explícito.
3. Seguridad Operacional (OPSEC): Estos scripts utilizan implementaciones básicas (como LSB secuencial) para facilitar el aprendizaje. NO son seguros contra técnicas modernas de estegoanálisis. NO los utilices para proteger información sensible real; un analista intermedio podría extraer el mensaje fácilmente.
4. Criptografía: La esteganografía oculta la existencia del mensaje, no su contenido. En escenarios reales, la información debe ser cifrada (ej. AES-256) antes de ser incrustada. Estos scripts no incluyen cifrado por defecto para aislar el aprendizaje esteganográfico.
"""

import argparse
import cv2
import numpy as np
from pathlib import Path
from typing import Optional

# Delimitador para saber dónde termina el mensaje oculto.
DELIMITER = "#####"

def text_to_bits(text: str) -> str:
    """Convierte una cadena de texto a su representación en bits (8 bits por carácter)."""
    return "".join(format(ord(char), '08b') for char in text)

def hide_data(carrier_path: str, secret_data: str, output_path: str) -> None:
    """
    Oculta texto dentro de un video inyectando bits en el LSB de los fotogramas.
    Utiliza OpenCV y un códec sin pérdida (Lossless) para preservar los datos.
    """
    if not Path(carrier_path).exists():
        raise FileNotFoundError(f"No se encontró el video portador: {carrier_path}")

    # Forzar la extensión .avi para usar un códec sin pérdida soportado por OpenCV
    if not output_path.lower().endswith(".avi"):
        print("[!] Advertencia: Forzando extensión .avi para preservar los bits con un códec Lossless.")
        output_path = str(Path(output_path).with_suffix('.avi'))

    full_message = secret_data + DELIMITER
    secret_bits = text_to_bits(full_message)
    bits_len = len(secret_bits)
    bit_idx = 0

    # Inicializar captura de video
    cap = cv2.VideoCapture(carrier_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    max_bits = total_frames * width * height * 3
    if bits_len > max_bits:
        cap.release()
        raise ValueError(f"Mensaje demasiado grande. Requiere {bits_len} bits, el video soporta {max_bits}.")

    # Inicializar escritor de video (Códec FFV1: Sin pérdida / Lossless)
    fourcc = cv2.VideoWriter_fourcc(*'FFV1')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    print(f"[*] Procesando video. Inyectando {bits_len} bits...")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if bit_idx < bits_len:
            # Aplanamos el fotograma a un array 1D para procesamiento vectorizado rápido
            flat_frame = frame.flatten()
            
            # Calculamos cuántos bits podemos inyectar en ESTE fotograma
            bits_for_frame = min(len(flat_frame), bits_len - bit_idx)
            
            # Convertimos el segmento de bits del mensaje a un array numérico
            bits_array = np.array([int(b) for b in secret_bits[bit_idx:bit_idx+bits_for_frame]], dtype=np.uint8)
            
            # SOLUCIÓN: Cambiamos ~1 por 254. 
            # 254 en binario es 11111110, lo que apaga el bit menos significativo de forma segura para NumPy.
            flat_frame[:bits_for_frame] = (flat_frame[:bits_for_frame] & 254) | bits_array
            
            # Reconstruimos el fotograma a sus dimensiones originales (Alto, Ancho, Canales)
            frame = flat_frame.reshape((height, width, 3))
            bit_idx += bits_for_frame

            out.write(frame)

    cap.release()
    out.release()
    print(f"[*] ¡Éxito! Video esteganográfico guardado en: {output_path}")

def extract_data(stego_path: str) -> str:
    """
    Extrae el mensaje oculto de un archivo de video leyendo el LSB de los fotogramas.
    """
    if not Path(stego_path).exists():
        raise FileNotFoundError(f"No se encontró el video: {stego_path}")

    cap = cv2.VideoCapture(stego_path)
    extracted_bits = []
    
    print("[*] Analizando fotogramas en busca de datos...")
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Aplanamos el fotograma para lectura secuencial
        flat_frame = frame.flatten()
        
        # PASO A PASO A NIVEL DE BITS:
        # flat_frame & 1: Extrae únicamente el valor del bit menos significativo (0 o 1) de cada canal de color.
        frame_bits = (flat_frame & 1).astype(str).tolist()
        extracted_bits.extend(frame_bits)
        
        # Cada cierta cantidad de frames, intentamos decodificar para no cargar todo en memoria
        if len(extracted_bits) > 8000:
            all_bits_str = "".join(extracted_bits)
            extracted_text = ""
            
            for i in range(0, len(all_bits_str), 8):
                byte = all_bits_str[i:i+8]
                if len(byte) < 8:
                    break
                
                extracted_text += chr(int(byte, 2))
                
                if extracted_text.endswith(DELIMITER):
                    cap.release()
                    return extracted_text[:-len(DELIMITER)]

    cap.release()
    raise ValueError("No se encontró ningún mensaje oculto o el video sufrió compresión con pérdida.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Módulo de Esteganografía LSB en Video (ENES Juriquilla)")
    subparsers = parser.add_subparsers(dest="action", required=True)

    hide_parser = subparsers.add_parser("ocultar", help="Ocultar un mensaje en un video")
    hide_parser.add_argument("-i", "--video", required=True, help="Ruta del video portador (.mp4, .avi)")
    hide_parser.add_argument("-m", "--mensaje", required=True, help="Mensaje secreto a ocultar")
    hide_parser.add_argument("-o", "--salida", required=True, help="Ruta del video de salida (será .avi)")

    extract_parser = subparsers.add_parser("extraer", help="Extraer un mensaje de un video")
    extract_parser.add_argument("-i", "--video", required=True, help="Ruta del video con el mensaje oculto")

    args = parser.parse_args()

    try:
        if args.action == "ocultar":
            hide_data(args.video, args.mensaje, args.salida)
        elif args.action == "extraer":
            secreto = extract_data(args.video)
            print(f"\n[+] Mensaje recuperado:\n{secreto}\n")
    except Exception as e:
        print(f"[-] Error: {e}")
