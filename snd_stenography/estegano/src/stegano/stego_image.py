"""
Módulo: stego_image.py
Descripción: Ocultación y extracción de información en imágenes usando la técnica LSB.

ADVERTENCIA ACADÉMICA Y AVISO LEGAL:
Este script ha sido desarrollado EXCLUSIVAMENTE para la clase de Temas Selectos de Seguridad de la Información (ENES Juriquilla). 

1. Uso Ético: La esteganografía es un arma de doble filo. El uso de estas técnicas para exfiltrar datos corporativos, evadir censura en contextos ilegales, o distribuir material ilícito está estrictamente prohibido y penado por la ley.
2. Consentimiento: Solo ejecuta estos scripts en archivos sobre los cuales tengas derechos de autor plenos o permiso explícito.
3. Seguridad Operacional (OPSEC): Estos scripts utilizan implementaciones básicas (como LSB secuencial) para facilitar el aprendizaje. NO son seguros contra técnicas modernas de estegoanálisis. NO los utilices para proteger información sensible real; un analista intermedio podría extraer el mensaje fácilmente.
4. Criptografía: La esteganografía oculta la existencia del mensaje, no su contenido. En escenarios reales, la información debe ser cifrada (ej. AES-256) antes de ser incrustada. Estos scripts no incluyen cifrado por defecto para aislar el aprendizaje esteganográfico.
""" 

import argparse
from pathlib import Path
from PIL import Image
from typing import Generator

# Delimitador para saber dónde termina el mensaje oculto.
DELIMITER = "#####"


def text_to_bits(text: str) -> str:
    """Convierte una cadena de texto a su representación en bits (8 bits por carácter)."""
    return "".join(format(ord(char), '08b') for char in text)


def bits_to_text(bits: str) -> str:
    """Convierte una cadena de bits de vuelta a texto."""
    chars = [chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8)]
    return "".join(chars)

def hide_data(carrier_path: str, secret_data: str, output_path: str) -> None:
    """
    Oculta texto dentro de una imagen mediante LSB y la guarda como PNG (sin pérdida).
    Refactorizado para utilizar acceso directo a memoria (.load()) evitando métodos obsoletos.
    """
    if not Path(carrier_path).exists():
        raise FileNotFoundError(f"No se encontró la imagen portadora: {carrier_path}")

    # Preparamos el mensaje con el delimitador final
    full_message = secret_data + DELIMITER
    secret_bits = text_to_bits(full_message)

    with Image.open(carrier_path) as img:
        # Convertimos a RGB para estandarizar (por si es RGBA, L, etc.)
        img = img.convert("RGB")
        width, height = img.size
        
        # Capacidad: 3 bits por píxel (R, G, B)
        max_bits = width * height * 3
        if len(secret_bits) > max_bits:
            raise ValueError(f"Mensaje demasiado grande. Se necesitan {len(secret_bits)} bits, "
                             f"pero la imagen solo soporta {max_bits} bits.")
        
        # SOLUCIÓN ARQUITECTÓNICA: Usamos .load() para crear un mapa de acceso a píxeles
        # Esto es O(1) en acceso a memoria y evita el DeprecationWarning de getdata()
        pixel_map = img.load()
        
        bit_idx = 0
        bits_len = len(secret_bits)
        
        # Iteramos espacialmente sobre la imagen en coordenadas (x, y)
        for y in range(height):
            for x in range(width):
                if bit_idx < bits_len:
                    # Extraemos los valores RGB actuales del píxel
                    r, g, b = pixel_map[x, y]
                    
                    # 1. Modificamos el canal ROJO (R)
                    if bit_idx < bits_len:
                        r = (r & ~1) | int(secret_bits[bit_idx])
                        bit_idx += 1
                    
                    # 2. Modificamos el canal VERDE (G)
                    if bit_idx < bits_len:
                        g = (g & ~1) | int(secret_bits[bit_idx])
                        bit_idx += 1
                        
                    # 3. Modificamos el canal AZUL (B)
                    if bit_idx < bits_len:
                        b = (b & ~1) | int(secret_bits[bit_idx])
                        bit_idx += 1
                        
                    # Inyectamos el nuevo píxel modificado directamente en la memoria
                    pixel_map[x, y] = (r, g, b)
                else:
                    break # Optimización: Salir del bucle en X si ya ocultamos todo
            
            if bit_idx >= bits_len:
                break # Optimización: Salir del bucle en Y si ya ocultamos todo
        
        # IMPORTANTE OPSEC: Guardar como PNG para evitar compresión con pérdida (Lossy)
        # Si usáramos JPEG, la compresión destruiría nuestros bits menos significativos.
        if not output_path.lower().endswith(".png"):
            print("[!] Advertencia: Forzando extensión .png para evitar corrupción por compresión.")
            output_path = str(Path(output_path).with_suffix('.png'))
            
        img.save(output_path, format="PNG")
        print(f"[*] ¡Éxito! Mensaje oculto guardado en: {output_path}")

def extract_data(stego_path: str) -> str:
    """
    Extrae un mensaje oculto de una imagen leyendo el LSB de cada píxel hasta encontrar el delimitador.
    Refactorizado para utilizar acceso directo a memoria (.load()) evitando métodos obsoletos.
    """
    if not Path(stego_path).exists():
        raise FileNotFoundError(f"No se encontró la imagen: {stego_path}")

    with Image.open(stego_path) as img:
        img = img.convert("RGB")
        width, height = img.size
        
        # SOLUCIÓN: Usamos .load() en lugar de list(img.getdata())
        pixel_map = img.load()
        
        extracted_bits = []
        
        # Iteramos espacialmente sobre la imagen en coordenadas (x, y)
        for y in range(height):
            for x in range(width):
                r, g, b = pixel_map[x, y]
                
                # PASO PASO A NIVEL DE BITS:
                # 'valor & 1': Aplicamos una máscara de bits para aislar el bit menos significativo (LSB).
                # Esto nos permite 'leer' el valor oculto (0 o 1) en cada canal de color.
                extracted_bits.append(str(r & 1))
                extracted_bits.append(str(g & 1))
                extracted_bits.append(str(b & 1))
                
        # Agrupar bits en bloques de 8 para formar bytes/caracteres
        all_bits_str = "".join(extracted_bits)
        extracted_text = ""
        
        for i in range(0, len(all_bits_str), 8):
            byte = all_bits_str[i:i+8]
            # Evitar errores de conversión al final si los bits no son exactos
            if len(byte) < 8:
                break
            
            char = chr(int(byte, 2))
            extracted_text += char
            
            # Verificar si hemos encontrado el delimitador de final de mensaje
            if extracted_text.endswith(DELIMITER):
                return extracted_text[:-len(DELIMITER)]
                
        # Si terminamos de recorrer toda la imagen y no vimos delimitador
        raise ValueError("No se encontró ningún mensaje oculto o está corrupto (¿Se guardó como JPEG?).")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Módulo de Esteganografía LSB en Imágenes (ENES Juriquilla)")
    subparsers = parser.add_subparsers(dest="action", required=True)

    # Subcomando ocultar
    hide_parser = subparsers.add_parser("ocultar", help="Ocultar un mensaje en una imagen")
    hide_parser.add_argument("-i", "--imagen", required=True, help="Ruta de la imagen portadora")
    hide_parser.add_argument("-m", "--mensaje", required=True, help="Mensaje secreto a ocultar")
    hide_parser.add_argument("-o", "--salida", required=True, help="Ruta de la imagen de salida (debe ser .png)")

    # Subcomando extraer
    extract_parser = subparsers.add_parser("extraer", help="Extraer un mensaje de una imagen")
    extract_parser.add_argument("-i", "--imagen", required=True, help="Ruta de la imagen con el mensaje oculto")

    args = parser.parse_args()

    try:
        if args.action == "ocultar":
            hide_data(args.imagen, args.mensaje, args.salida)
        elif args.action == "extraer":
            secreto = extract_data(args.imagen)
            print(f"\n[+] Mensaje recuperado:\n{secreto}\n")
    except Exception as e:
        print(f"[-] Error: {e}")
