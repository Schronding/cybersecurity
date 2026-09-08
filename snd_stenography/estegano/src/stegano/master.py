"""
Módulo: master.py
Descripción: Interfaz unificada (CLI) para el stack de herramientas de esteganografía.
Este módulo actúa como el orquestador central del proyecto, permitiendo al usuario interactuar
con los diferentes módulos especialistas (imagen, audio, video) a través de una única interfaz.

ADVERTENCIA ACADÉMICA Y AVISO LEGAL:
Este script ha sido desarrollado EXCLUSIVAMENTE para la clase de Temas Selectos de Seguridad de la Información (ENES Juriquilla). 

1. Uso Ético: La esteganografía es un arma de doble filo. El uso de estas técnicas para exfiltrar datos corporativos, evadir censura en contextos ilegales, o distribuir material ilícito está estrictamente prohibido y penado por la ley.
2. Consentimiento: Solo ejecuta estos scripts en archivos sobre los cuales tengas derechos de autor plenos o permiso explícito.
3. Seguridad Operacional (OPSEC): Estos scripts utilizan implementaciones básicas (como LSB secuencial) para facilitar el aprendizaje. NO son seguros contra técnicas modernas de estegoanálisis. NO los utilices para proteger información sensible real; un analista intermedio podría extraer el mensaje fácilmente.
4. Criptografía: La esteganografía oculta la existencia del mensaje, no su contenido. En escenarios reales, la información debe ser cifrada (ej. AES-256) antes de ser incrustada. Estos scripts no incluyen cifrado por defecto para aislar el aprendizaje esteganográfico.
"""

import argparse
import sys
from typing import Any

# El diseño es MODULAR: cada script especialista se importa aquí.
try:
    import stego_image
    import stego_audio
    import stego_video
except ImportError as e:
    print(f"[-] Error de importación: {e}")
    print("Asegúrate de que 'stego_image.py', 'stego_audio.py' y 'stego_video.py' estén en el mismo directorio.")
    sys.exit(1)


def main() -> None:
    """
    Función principal que parsea los argumentos de la terminal y 
    actúa como despacho hacia los módulos especialistas.
    """
    # Se utiliza argparse para construir una Interfaz de Línea de Comandos (CLI) robusta.
    parser = argparse.ArgumentParser(
        description="Stack Educativo de Esteganografía LSB - ENES Juriquilla",
        epilog="Ejemplo: uv run master.py ocultar --tipo imagen -a foto.png -m 'hola' -o salida.png"
    )
    
    subparsers = parser.add_subparsers(dest="action", required=True, help="Acción a realizar")

    # ==========================================
    # Subcomando: OCULTAR
    # ==========================================
    hide_parser = subparsers.add_parser("ocultar", help="Oculta un mensaje en un archivo portador")
    hide_parser.add_argument("-t", "--tipo", choices=["imagen", "audio", "video"], required=True, 
                             help="Tipo de archivo portador (determina qué módulo de la biblioteca usaremos)")
    hide_parser.add_argument("-a", "--archivo", required=True, help="Ruta del archivo original (portador)")
    hide_parser.add_argument("-m", "--mensaje", required=True, help="Mensaje secreto a ocultar")
    hide_parser.add_argument("-o", "--salida", required=True, help="Ruta del archivo modificado que contendrá el mensaje")

    # ==========================================
    # Subcomando: EXTRAER
    # ==========================================
    extract_parser = subparsers.add_parser("extraer", help="Extrae un mensaje de un archivo esteganográfico")
    extract_parser.add_argument("-t", "--tipo", choices=["imagen", "audio", "video"], required=True, 
                                help="Tipo de archivo (para utilizar el algoritmo de extracción correcto)")
    extract_parser.add_argument("-a", "--archivo", required=True, help="Ruta del archivo que contiene el mensaje oculto")

    args: argparse.Namespace = parser.parse_args()

    try:
        if args.action == "ocultar":
            print(f"[*] Iniciando proceso de ocultación en {args.tipo.upper()}...")
            if args.tipo == "imagen":
                stego_image.hide_data(args.archivo, args.mensaje, args.salida)
            elif args.tipo == "audio":
                stego_audio.hide_data(args.archivo, args.mensaje, args.salida)
            elif args.tipo == "video":
                stego_video.hide_data(args.archivo, args.mensaje, args.salida)
                
        elif args.action == "extraer":
            print(f"[*] Iniciando proceso de extracción de {args.tipo.upper()}...")
            secreto: str = ""
            if args.tipo == "imagen":
                secreto = stego_image.extract_data(args.archivo)
            elif args.tipo == "audio":
                secreto = stego_audio.extract_data(args.archivo)
            elif args.tipo == "video":
                secreto = stego_video.extract_data(args.archivo)
            
            print(f"\n[+] ==========================================")
            print(f"[+] Mensaje recuperado con éxito:")
            print(f"[+] {secreto}")
            print(f"[+] ==========================================\n")

    except ValueError as ve:
        print(f"\n[-] Error de validación de datos: {ve}")
    except FileNotFoundError as fnfe:
        print(f"\n[-] Error de archivo no encontrado: {fnfe}")
    except Exception as e:
        print(f"\n[-] Error inesperado durante la operación: {e}")


if __name__ == "__main__":
    main()