"""
Módulo: stego_audio.py
Descripción: Ocultación y extracción de información en archivos de audio WAV usando LSB.

ADVERTENCIA ACADÉMICA Y AVISO LEGAL:
Este script ha sido desarrollado EXCLUSIVAMENTE para la clase de Temas Selectos de Seguridad de la Información (ENES Juriquilla). 

1. Uso Ético: La esteganografía es un arma de doble filo. El uso de estas técnicas para exfiltrar datos corporativos, evadir censura en contextos ilegales, o distribuir material ilícito está estrictamente prohibido y penado por la ley.
2. Consentimiento: Solo ejecuta estos scripts en archivos sobre los cuales tengas derechos de autor plenos o permiso explícito.
3. Seguridad Operacional (OPSEC): Estos scripts utilizan implementaciones básicas (como LSB secuencial) para facilitar el aprendizaje. NO son seguros contra técnicas modernas de estegoanálisis. NO los utilices para proteger información sensible real; un analista intermedio podría extraer el mensaje fácilmente.
4. Criptografía: La esteganografía oculta la existencia del mensaje, no su contenido. En escenarios reales, la información debe ser cifrada (ej. AES-256) antes de ser incrustada. Estos scripts no incluyen cifrado por defecto para aislar el aprendizaje esteganográfico.
"""

import argparse
from pathlib import Path
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


def modify_samples_lsb(samples, secret_bits: str) -> Generator:
    """
    Generador que modifica el bit menos significativo (LSB) de cada muestra de audio
    para incrustar los bits del mensaje secreto.
    """
    bit_idx = 0
    bits_len = len(secret_bits)

    for sample in samples:
        # Convertimos la muestra a entero de 16 bits para manipulación
        # Nota: Se asume audio de 16-bit de ejemplo
        sample_int = int(sample)
        
        if bit_idx < bits_len:
            # PASO A PASO A NIVEL DE BITS:
            # 1. 'sample_int & ~1': Aplicamos una máscara de bits para asegurar que el bit menos significativo
            #    (LSB) sea 0. '~1' es la negación de '00000001', resultando en '11111110'. Al hacer el AND,
            #    el último bit siempre se convierte en 0, preservando los otros 15 bits originales.
            # 2. '| int(secret_bits[bit_idx])': Aplicamos una operación OR con el bit de nuestro mensaje (0 o 1).
            #    Si el bit es 1, el LSB se vuelve 1; si es 0, se queda en 0.
            sample_int = (sample_int & ~1) | int(secret_bits[bit_idx])
            bit_idx += 1
        
        yield sample_int


def hide_data(carrier_path: str, secret_data: str, output_path: str) -> None:
    """
    Oculta texto dentro de un archivo de audio .wav mediante LSB.
    """
    import wave
    import struct
    import array

    if not Path(carrier_path).exists():
        raise FileNotFoundError(f"No se encontró el archivo de audio: {carrier_path}")

    with wave.open(carrier_path, 'rb') as wav_in:
        params = wav_in.getparams()
        n_frames = params.nframes
        n_channels = params.nchannels
        total_samples = n_frames * n_channels

        # Preparamos el mensaje con el delimitador final
        full_message = secret_data + DELIMITER
        secret_bits = text_to_bits(full_message)

        if len(secret_bits) > total_samples:
            raise ValueError(f"Mensaje demasiado grande. Se necesitan {len(secret_bits)} bits, "
                             f"pero el audio solo soporta {total_samples} bits.")

        frames = wav_in.readframes(n_frames)
        
        # Convertimos bytes a una lista de enteros de 16 bits de forma eficiente
        original_samples_array = array.array('h')
        original_samples_array.frombytes(frames)
        original_samples_list = original_samples_array.tolist()
        
        # Modificamos las muestras
        new_samples = list(modify_samples_lsb(original_samples_list, secret_bits))
        
        # Si sobran muestras, las mantenemos intactas
        if len(new_samples) < len(original_samples_list):
            new_samples.extend(original_samples_list[len(new_samples):])
            
        # Escribimos el nuevo archivo
        with wave.open(output_path, 'wb') as wav_out:
            wav_out.setparams(params)
            # Empaquetamos de nuevo a bytes
            new_array = array.array('h', new_samples)
            wav_out.writeframes(new_array.tobytes())
            
        print(f"[*] ¡Éxito! Mensaje oculto guardado en: {output_path}")

def extract_data(stego_path: str) -> str:
    """
    Extrae un mensaje oculto de un archivo .wav leyendo el LSB de cada muestra.
    """
    import wave
    import array
    from pathlib import Path

    if not Path(stego_path).exists():
        raise FileNotFoundError(f"No se encontró el archivo: {stego_path}")

    with wave.open(stego_path, 'rb') as wav_in:
        n_frames = wav_in.getnframes()
        frames = wav_in.readframes(n_frames)
        
        # SOLUCIÓN: Usamos 'array' igual que en hide_data para evitar el cálculo manual
        # de canales y muestras requerido por struct.unpack
        samples_array = array.array('h')
        samples_array.frombytes(frames)
        samples = samples_array.tolist()
        
        extracted_bits = []
        for sample in samples:
            # PASO A PASO A NIVEL DE BITS:
            # 1. 'sample & 1': Aplicamos una máscara de bits para aislar el bit menos significativo (LSB).
            #    La máscara '1' (00000001) realiza un AND que devuelve 1 si el bit es 1, o 0 si es 0.
            extracted_bits.append(str(sample & 1))
            
        all_bits_str = "".join(extracted_bits)
        extracted_text = ""
        
        # El delimitador de tu módulo global
        DELIMITER = "#####"
        
        for i in range(0, len(all_bits_str), 8):
            byte = all_bits_str[i:i+8]
            if len(byte) < 8:
                break
            
            char = chr(int(byte, 2))
            extracted_text += char
            
            if extracted_text.endswith(DELIMITER):
                return extracted_text[:-len(DELIMITER)]
                
        raise ValueError("No se encontró el delimitador de final de mensaje.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Módulo de Esteganografía LSB en Audio (ENES Juriquilla)")
    subparsers = parser.add_subparsers(dest="action", required=True)

    hide_parser = subparsers.add_parser("ocultar", help="Ocultar un mensaje en un audio")
    hide_parser.add_argument("-i", "--imagen", required=True, help="Ruta del audio portador")
    hide_parser.add_argument("-m", "--mensaje", required=True, help="Mensaje secreto a ocultar")
    hide_parser.add_argument("-o", "--salida", required=True, help="Ruta del archivo de salida")

    extract_parser = subparsers.add_parser("extraer", help="Extraer un mensaje de un audio")
    extract_parser.add_argument("-i", "--imagen", required=True, help="Ruta del audio con el mensaje")

    args = parser.parse_args()

    try:
        if args.action == "ocultar":
            hide_data(args.imagen, args.mensaje, args.salida)
        elif args.action == "extraer":
            secreto = extract_data(args.imagen)
            print(f"\n[+] Mensaje recuperado:\n{secreto}\n")
    except Exception as e:
        print(f"[-] Error: {e}")
