import json
import sys

'''0. For what I understand this script is run in the terminal and `json_path`
is the argument that follows with the file name with the metadata. As I used 
```bash
python_script.py .\metadatos.json
```

and they're both in the same folder this should work, but it tells me that 
"[+] Pista de acceso reconstruida: Error durante la reconstrucción: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte" 
'''
def reconstruir_pista_acceso(json_path):
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            '''7. `utf-8` seems to be the one most commonly used in northamerica,
            but what are other type formats?... actually I think that utf-8 is like 
            the latest version of accepted characters, so the "u" might come from 
            universal and it includes all the big languages of humanity (I don't think
            indigenous or historic characters are included though). '''
            data = json.load(file)
        
        secuencia_mensajes = []

        '''1. I have never seen the method `.get()`. For what I understand from
        this line of code below what is saying is that from the `data` variable
        (which are my metadata) I need to check the streams and retrieve the 
        complete information of that specific attribute (that is why we use the
        `[]`). '''
        for stream in data.get("streams", []):
            idx = stream.get("index", 0)
            '''2. What is interesting is that in these `.get()` methods I am using 
            different syntax. In `idx` the zero makes me believe it is a specific row
            (just like in numpy) but `tags` makes me believe is the whole object
            which is being retrieved (what in numpy would be `[:,:]`). '''
            tags = stream.get("tags", {})
            
            # Extracción del nombre del gestor o del título de la pista
            handler = tags.get("handler_name", "")
            '''3. Indeed it seems that it is a way to get json with a combination
            of key, value pairs... but then why do I need to specificy the value format?
            It seems odd for me, as it seems rendundant to have a file that stores specific 
            values with semantic names that it is also asking you to remember the type in the
            value. What I imagine is that this is some type of coertion, so while the original
            object might be of one type I might ask for another when retrieving it. '''
            title = tags.get("title", "")
            
            contenido = title if title else handler
            
            if contenido:
                secuencia_mensajes.append((idx, contenido))
        
        # Ordenación rigurosa basada en el índice de la pista
        secuencia_mensajes.sort(key=lambda x: x[0])
        '''5. How interesting, it seems that it is sorting based on the number of the `idx` so
        indeed it follows a chronological order (or so I expect). '''
        
        # Concatenación de los fragmentos ocultos
        mensaje_final = "".join([item[1] for item in secuencia_mensajes])
        return mensaje_final

    except Exception as err:
        return f"Error durante la reconstrucción: {str(err)}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        resultado = reconstruir_pista_acceso(sys.argv[1])
        print(f"[+] Pista de acceso reconstruida: {resultado}")