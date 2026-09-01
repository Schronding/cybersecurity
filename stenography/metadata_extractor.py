import json
import sys

'''0. This new file is supposed to be the one that will help me 
actually extract the necessary metadata. According to Claude

> The tags exist only in metadatos_nuevos.json, where the script yields 
VideoHandlerSoundHandler — which reads like stock ffmpeg handler names, 
not a planted payload. The encoding bug is genuinely fixed; whether you've 
found the actual hidden message is a separate question.
'''

'''1. Indeed now I have something as an output

"python .\metadata_extractor.py .\metadatos_nuevos.json                    
[+] Pista de acceso reconstruida: VideoHandlerSoundHandler"

What is the following step? '''
def reconstruir_pista_acceso(json_path):
    try:
        # IA: Message - Changed file reading encoding to properly handle BOM (0xff) characters.
        '''2. If utf-8 was created in 1992 and contains most of the used
        signs for the most popular languages, then why utf-16 came around?
        the "16" is just a clever way to say that it continued from 8? 
        (as in binary) or it has a semantic meaning? What are BOM characters?
        I assume BOM means something like Base Object Model. '''
        with open(json_path, 'r', encoding='utf-16') as file:

            data = json.load(file)

        secuencia_mensajes = []


        for stream in data.get("streams", []):
            idx = stream.get("index", 0)

            tags = stream.get("tags", {})

            handler = tags.get("handler_name", "")

            title = tags.get("title", "")

            contenido = title if title else handler

            if contenido:
                secuencia_mensajes.append((idx, contenido))

        secuencia_mensajes.sort(key=lambda x: x[0])


        mensaje_final = "".join([item[1] for item in secuencia_mensajes])
        return mensaje_final

    except Exception as err:
        return f"Error durante la reconstrucción: {str(err)}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        resultado = reconstruir_pista_acceso(sys.argv[1])
        print(f"[+] Pista de acceso reconstruida: {resultado}")
