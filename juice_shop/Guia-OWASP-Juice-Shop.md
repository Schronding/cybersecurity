# 📘 Guía de Exploración y Explotación de OWASP Juice Shop 

**Instructor:** Seguridad de Aplicaciones Web **Nivel:** Principiante / Intermedio **Objetivo:** Dominar el ciclo de reconocimiento, análisis y explotación de vulnerabilidades en una aplicación web moderna usando OWASP Juice Shop como laboratorio. 

📦 1. ¿Qué es OWASP Juice Shop? 

OWASP Juice Shop es una tienda de jugos en línea completa, desarrollada con **Node.js, Express, Angular, SQLite/MongoDB/MySQL/PostgreSQL** . Contiene más de **50 vulnerabilidades** basadas en el OWASP Top 10 y categorías modernas (BOLA, SSRF, JWT weak secret, etc.). Está diseñada para ser: - ✅ **Legal** : Corre local o en red privada. - ✅ **Reseteable** : Estado limpio con un comando. - 🏆 **Interactivo** : Incluye un Scoreboard que valida hallazgos automáticamente. 

## ⚙️� 2. Requisitos y Configuración del Entorno 

Hardware/Software Mínimo 

- Docker Desktop / WSL2 (recomendado) o Node.js ≥16 

- Navegador moderno + DevTools 

- Burp Suite Community u OWASP ZAP 

- Terminal con curl/postman/sqlmap 

Despliegue Rápido (Docker) 

docker run -d \ 

--name juice-shop \ -p 3000:3000 \ -e RESET_ON_START=true \ bkimminich/juice-shop 

✅ Acceso: http://localhost:3000 ⏱️� Tiempo de inicio: ~1-2 minutos. Verifica logs: docker logs juice-shop 

### Reset del Entorno 

docker stop juice-shop **&&** docker rm juice-shop 

_# Vuelve a ejecutar el comando anterior (RESET_ON_START=true limpia DB al iniciar)_ 

## 🔍 3. Metodología de Exploración Recomendada 

|Fase|Objetivo|Técnicas|
|---|---|---|
|**1.**<br>**Reconocimiento**|Identificar tecnologías, rutas,<br>servicios expuestos|dirsearch,ffuf, DevTools →<br>Network/Console,/admin|
|**2. Mapeo de**<br>**Aplicación**|Registrar flujos críticos (registro,<br>login, carrito, checkout, perfil,<br>API)|Pruebas manuales + Burp<br>Repeater|
|**3. Análisis**<br>**Estático**|Buscar secretos, config,<br>endpoints ocultos en frontend|F12<br>Sources/Network<br>→<br>,<br>inspeccionar<br>/assets/public/**/*.js|
|**4. Pruebas**|Inyecciones, BOLA, XSS, SSRF,|Burp Intruder/Scanner +|
|**Dinámicas**|auth bypass|payloads manuales|
|**5. Validación**|Confirmar impacto y reportar|Capturas, payloads exactos,<br>estado del Scoreboard|



✅ **Consejo de instructor** : No te saltes el frontend. Angular expone rutas en approuting.module.ts y servicios que revelan endpoints API ocultos (/rest/v1/...). 

## 🎯 4. Catálogo de Vulnerabilidades & Ejercicios Prácticos 

_(Ejemplos basados en Juice Shop v12+. Algunos pueden variar por versión o modo hardened)_ 

|#|Vuln. (OWASP)|Endpoint / Flujos|Payload / Acción|Resultado Esperado|
|---|---|---|---|---|
|1|**SQLi**(A03)|Búsqueda de<br>productos<br>(/api/v1/search?q=)<br>o login|' OR 1=1-- -en<br>campo texto|Listado completo de<br>usuarios/productos|
|2|**BOLA**(A01)|/api/v1/orders/{id}o<br>/api/v1/users/{id}|Iterar IDs:1,2,927,<br>etc.|Acceder a<br>órdenes/perfiles de<br>otros usuarios|
|3|**JWT Weak**<br>**Secret**(A02)|Header<br>Authorization:<br>Bearer <token><br>después del login|Decodificar en<br>jwt.io→ clavet0p-<br>s3cr3t(config por<br>defecto). Firmar<br>token con<br>adminRole=true|Acceso a/admino<br>privilegios elevados|
|4|**XSS Stored**|Crear producto o|<img src=x|Alerta al cargar el|



|#|Vuln. (OWASP)|Endpoint / Flujos|Payload / Acción|Resultado Esperado|
|---|---|---|---|---|
||(A03)|reseña con<br>nombre/cuerpo|onerror=alert(doc<br>ument.cookie)>|detalle del producto|
|5|**SSRF**(A09)|Subir logo/imagen<br>en perfil<br>(/api/v1/user/update<br>)|URL:<br>http://localhost:300<br>0/admino<br>http://169.254.169.<br>254/latest/meta-<br>data/iam/security-<br>credentials/(en<br>cloud)|Fetch interno o<br>metadata de instancia|
|6|**Path Traversal**<br>(A01)|/rest/product/<br>image?name=../../<br>etc/passwdo<br>/assets/public/image<br>s/..|Leer archivos del<br>servidor|Contenido de<br>package.json,.env,<br>logs|
|7|**Sensitive Data**<br>**Exposure**(A02)|/api/v1/userso<br>DevTools →<br>Application →<br>LocalStorage|Ver tokens, claves<br>API en JS bundle<br>(secret: 'juice-<br>shop')|Extracción de<br>credenciales/configs|
|8|**CSP Bypass /**<br>**Angular**<br>**Binding**(A05)|Input que permite<br>{{constructor.constr<br>uctor('alert(1)')()}}|En campos que<br>renderizan<br>HTML/JS sin<br>sanitizar|Ejecución JS en<br>contexto del<br>navegador|



✅ **Tips de explotación** : - El Scoreboard (/score-board) se actualiza automáticamente. Si un ejercicio no puntúa, revisa si el modo hardened=true oculta pistas o requiere pasos secuenciales. - Muchos fallos requieren **estado previo** : crear usuario, agregar al carrito, completar checkout, subir avatar. 

## 5. Herramientas Recomendadas y Uso Específico 

|Herramienta|Propósito en Juice Shop|
|---|---|
|**Burp Suite**|Interceptación de peticiones, Intruder para brute force,<br>Scanner automatizado|
|**Browser DevTools**|Análisis de SPA (Angular routes, XHR/fetch,<br>localStorage, cookies)|
|**SQLmap**<br>**f**|Automatizar SQLi en endpoints expuestos:sqlmap -u<br>"http://localhost:3000/api/v1/search?q=test" --batch<br>f|
|**ffuf / dirsearch**|Descubrir endpoints ocultos:ffuf -u<br>http://localhost:3000/FUZZ -w|



|Herramienta|Propósito en Juice Shop|
|---|---|
||/usr/share/seclists/Discovery/Web-Content/common.txt|
|**jwt_tool / jwt.io**|Decodificar, crackear secret, firmar tokens con roles<br>alterados|
|**Postman/Insomnia**|Probar APIs REST en/api/v1/, verificar respuestas JSON,<br>estados HTTP|



## 🎯 6. Buenas Prácticas de Laboratorio 

1. **Aísla el entorno** : Usa Docker o Vagrant. Evita dependencias externas (ej. servicios de email por defecto apuntan a localhost). 

2. **Documenta paso a paso** : Endpoint → Método → Headers/Payload → Response → Impacto → Captura. 

3. **No modifies datos críticos permanentemente** : El reset es tu mejor amigo. 

4. **Combina manual + automatizado** : Los scanners pierden contexto; las pruebas manuales descubren lógica de negocio. 

5. **Valida antes de explotar** : Confirma que el dato afectado pertenece a Juice Shop (ej. no ../etc/passwd genérico, sino /app/package.json). 

## 🏆 7. Validación: El Scoreboard y Certificación Interna 

- Accede a: http://localhost:3000/score-board 

- Los puntos se otorgan al detectar la vulnerabilidad (ej. abrir alert XSS, devolver JSON inyectado, cargar imagen desde SSRF). 

- **Modo Hardened** (HARDENED=true): Oculta pistas en el Scoreboard y desactiva algunos fallos para entornos de producción simulados. 

- ✅ Meta instructor: Completa al menos 15 ejercicios antes de pasar a pentest con reporte formal. 

## 🎯 8. Siguientes Pasos & Evaluación 

### ✅ Checklist de Verificación 

- ☐Desplegar Juice Shop con Docker y verificar acceso localhost:3000 

- ☐Mapear 5 rutas críticas (auth, productos, carrito, perfil, API) 

- ☐Explotar 1 vuln por categoría OWASP Top 10 

- ☐Generar reporte PDF/Markdown con evidencia 

- ☐Puntuar >20% en Scoreboard sin modo hardened 

### 📚 Material Complementario 

- OWASP Top 10 2021: https://owasp.org/www-project-top-ten/ 

- Juice Shop Docs & GitHub: https://github.com/juice-shop/juice-shop 

- PortSwigger Web Security Academy (gratis) 

- TryHackMe: Web Fundamentals / OWASP Top 10 

## 🎯 Nota del Instructor 

_“La diferencia entre un tester novato y uno experto no es la cantidad de herramientas, sino la capacidad de seguir el flujo de datos: desde el input del usuario, pasando por validaciones, queries/serialización, hasta la respuesta al cliente. Juice Shop premia la curiosidad estructural. No busques solo ‘payloads’, busca patrones en rutas, nombres de variables y respuestas HTTP.”_ 

