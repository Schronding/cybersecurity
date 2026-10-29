# REPORTE TÉCNICO DE EVALUACIÓN DE VULNERABILIDADES DE RED

- **Para:** Coordinación de Tecnologías de la Información y Comunicaciones – ENES Juriquilla
- **Elaborado por:** Equipo de Auditoría de Ciberseguridad / Licenciatura en Tecnología (Brayan Coronel Ramírez)
- **Asignatura:** Temas Selectos de Ciberseguridad – ENES Juriquilla, UNAM
- **Fecha de Evaluación:** 28 de octubre de 2026
- **Clasificación del Documento:** Confidencial – Uso Interno

---

## 1. Resumen Ejecutivo

Durante el periodo de evaluación del 28 de octubre de 2026 se llevó a cabo un análisis de seguridad no destructivo sobre el segmento de red `132.248.248.0/24`. El objetivo principal fue identificar activos informáticos que ejecutan servicios de transferencia de hipertexto (HTTP/HTTPS), inventariar las versiones de software en producción y detectar riesgos derivados de versiones obsoletas o al final de su vida útil (EOL) de intérpretes backend (PHP), así como configuraciones inseguras en servidores web.

**Hallazgos clave:**

- **Total de IPs escaneadas:** 256 direcciones IP (bloque `132.248.248.0/24`), identificando 48 hosts activos durante la fase de descubrimiento.
- **Servicios web activos (HTTP/HTTPS):** 36 direcciones IP con al menos un puerto web abierto (`80`, `443`, `8080`, `8443` u `8888`) en el descubrimiento inicial, de las cuales 34 respondieron durante el escaneo de versiones (`resultados_versiones.xml`) y 35 durante la evaluación de vulnerabilidades de PHP (`php2shell_scan`).
- **Sistemas con versiones de PHP al final de su vida útil (EOL):** 4 sistemas reportados por el análisis automatizado (`132.248.248.115` con PHP `7.3.33`, `132.248.248.152` con PHP `5.4.16`, `132.248.248.175` con PHP `8.0.30` y `132.248.248.128` con coincidencia heurística `2.9.5` en el cuerpo de respuesta HTTP).
- **Vulnerabilidades críticas/altas detectadas:** 2 vulnerabilidades de ejecución remota de código (`CVE-2026-109618` y `CVE-2026-109619`, ambas con `CVSS: 9.2`) presentes en los 4 hosts señalados (8 instancias reportadas en total), además de exposición de archivos de diagnóstico y respaldo (`/phpinfo.php`, `/info.php`, `/backup/`, `/logs/`) y listado de directorios habilitado en múltiples servidores.

---

## 2. Alcance y Metodología (Scope)

La evaluación se limitó estrictamente al análisis no intrusivo de la subred objetivo mediante comparación remota de versiones y encabezados, sin ejecutar pruebas de explotación ni sondeos destructivos.

- **Direcciones IP evaluadas:** Subred `132.248.248.0/24` (256 direcciones IP en barrido inicial; 36 direcciones IP consolidadas en el archivo de objetivos `ips_web.txt`).
- **Puertos analizados:** `80/tcp`, `443/tcp`, `8080/tcp`, `8443/tcp` y `8888/tcp`.

**Metodología aplicada:**

1. **Fase 1 – Descubrimiento de servicios web (16:37:59 – 16:38:08 CST):** Escaneo TCP SYN (`-sS`) sin resolución DNS (`-n`) filtrando puertos abiertos (`--open`) mediante el comando:

   ```bash
   nmap -p 80,443,8080,8443,8888 --open -sS -n -oG descubrimientos_web.txt 132.248.248.0/24
   ```

   Completado en 8.07 segundos.

2. **Fase 2 – Identificación de versiones y fingerprinting (16:56:04 – 17:21:27 CST):** Detección de versiones de servicios (`-sV`), recolección de cabeceras HTTP y enumeración de rutas web sobre la lista depurada `ips_web.txt` mediante el comando:

   ```bash
   nmap -sV --script=http-headers,http-enum -p 80,443,8080,8443,8888 -iL ips_web.txt -oX resultados_versiones.xml
   ```

   Completado en 1522.79 segundos.

3. **Fase 3 – Evaluación automática de vulnerabilidades en PHP (17:29:02 – 17:29:59 CST):** Verificación no intrusiva de versiones de PHP en los puertos `80` y `443` mediante el comando:

   ```bash
   nmap -p 80,443 --script nmap-php2shell-main/scripts/http-php2shell-version.nse -iL ips_web.txt -oA php2shell_scan
   ```

   Completado en 57.45 segundos.

**Herramientas empleadas:** Nmap Security Scanner v7.991, scripts NSE oficiales (`http-headers`, `http-enum`, `http-server-header`) y el script de auditoría `http-php2shell-version.nse`.

---

## 3. Matriz de Severidad y Clasificación de Riesgo

Los hallazgos se priorizan mediante el estándar CVSS (Common Vulnerability Scoring System) conforme a los criterios operativos de remediación:

| Nivel de Riesgo | Rango CVSS | Criterio de Acción |
| --- | --- | --- |
| **Crítico** | 9.0 – 10.0 | Corrección en un plazo máximo de 24 horas. |
| **Alto** | 7.0 – 8.9 | Corrección en un plazo no mayor a 7 días. |
| **Medio** | 4.0 – 6.9 | Corrección programada en el siguiente ciclo de mantenimiento. |
| **Bajo** | 0.1 – 3.9 | Mejora de hardening recomendada. |

---

## 4. Detalles de Hallazgos y Vulnerabilidades

### Hallazgo 1: Versiones Inseguras o EOL de PHP Susceptibles a Ejecución Remota de Código (`CVE-2026-109618` y `CVE-2026-109619`)

- **Severidad:** CRÍTICA / ALTA (`CVSS: 9.2` – clasificado por el script como `Risk factor: High` y `Upstream severity: CRITICAL - CVSS v4.0 9.2`).
- **Sistemas afectados:** `132.248.248.115`, `132.248.248.152`, `132.248.248.175` (`kneipe.lavis.unam.mx`) y `132.248.248.128` (sujeto a validación manual por detección heurística en cuerpo HTML).
- **Fecha de divulgación de los CVE:** 21 de octubre de 2026 (`2026-10-21`).

**Descripción del riesgo:** Las ramas de PHP `5.4.x`, `7.3.x` y `8.0.x` se encuentran al final de su vida útil (EOL) y carecen de parches oficiales upstream. El script `http-php2shell-version.nse` identificó exposición potencial a dos vulnerabilidades críticas de ejecución remota de código (RCE) no autenticada:

- **`CVE-2026-109618` (RCE vía corrupción por OOM):** El manejo de condiciones de falta de memoria (*out-of-memory*) en PHP puede interrumpir el procesamiento de una petición mientras las estructuras internas de datos están solo parcialmente inicializadas; durante la limpieza de memoria, datos inválidos pueden ser tratados como válidos, permitiendo potencialmente la ejecución remota de código sin autenticación.
- **`CVE-2026-109619` (RCE vía estado global obsoleto):** El estado interno perteneciente a una petición puede sobrevivir después de que su memoria subyacente ha sido liberada; una petición posterior atendida por el mismo proceso *worker* puede reutilizar dicho estado obsoleto antes de que la inicialización normal lo restablezca, derivando potencialmente en ejecución remota de código sin autenticación.

**Desglose técnico por sistema afectado:**

| Dirección IP / Hostname | Puerto | Servidor Web Detectado | Versión PHP Observada | Fuente de Evidencia | Nivel de Confianza |
| --- | --- | --- | --- | --- | --- |
| `132.248.248.115` | `443/tcp` | `Apache/2.4.6 (CentOS) OpenSSL/1.0.2k-fips` | `7.3.33` (EOL) | Cabeceras `X-Powered-By` y `Server` | `MEDIUM` |
| `132.248.248.152` | `443/tcp` | `Apache/2.4.6 (CentOS) OpenSSL/1.0.2k-fips` | `5.4.16` (EOL) | Cabecera `Server` | `MEDIUM` |
| `132.248.248.175` (`kneipe.lavis.unam.mx`) | `443/tcp` | `Apache/2.4.62 (Rocky Linux) OpenSSL/3.5.8` | `8.0.30` (EOL) | Cabecera `X-Powered-By` | `MEDIUM` |
| `132.248.248.128` (`mexpd.liigh.unam.mx`) | `443/tcp` | `Apache/2.4.41 (Ubuntu)` | `2.9.5` (posible falso positivo) | Cuerpo de respuesta HTTP | `HIGH` (heurístico) |

> **Nota técnica sobre `132.248.248.128`:** El script `http-php2shell-version.nse` reportó la versión `2.9.5` a partir del cuerpo de respuesta HTTP (`HTTP response body`). Sin embargo, los scripts `http-headers` y `http-enum` demuestran que este servidor ejecuta `Apache/2.4.41 (Ubuntu)` y aloja una instancia de WordPress (`https://mexpd.liigh.unam.mx/`), por lo que la cadena `2.9.5` probablemente corresponde a la versión de un componente o plugin en el HTML y requiere verificación interna de la versión real de PHP instalada.

**Evidencias (cabeceras HTTP capturadas):**

Host `132.248.248.115` (`443/tcp`):

```http
Date: Wed, 28 Oct 2026 22:59:46 GMT
Server: Apache/2.4.6 (CentOS) OpenSSL/1.0.2k-fips PHP/7.3.33
X-Powered-By: PHP/7.3.33
Content-Type: text/html; charset=UTF-8
```

Host `132.248.248.152` (`443/tcp`):

```http
Date: Wed, 28 Oct 2026 23:03:15 GMT
Server: Apache/2.4.6 (CentOS) OpenSSL/1.0.2k-fips PHP/5.4.16
Last-Modified: Tue, 29 Sep 2026 00:21:41 GMT
Content-Type: text/html; charset=UTF-8
```

Host `132.248.248.175` (`kneipe.lavis.unam.mx` – `443/tcp`):

```http
Date: Wed, 28 Oct 2026 23:00:17 GMT
Server: Apache/2.4.62 (Rocky Linux) OpenSSL/3.5.8
X-Powered-By: PHP/8.0.30
Content-Type: text/html; charset=UTF-8
```

---

### Hallazgo 2: Exposición de Archivos de Diagnóstico (`phpinfo`), Respaldos y Registros de Servidor

- **Severidad:** ALTA (`CVSS: 7.5`).
- **Sistemas afectados:** `132.248.248.112`, `132.248.248.115`, `132.248.248.121` y `132.248.248.153`.

**Descripción del riesgo:** Mediante el script `http-enum` se detectaron rutas públicamente accesibles que exponen archivos de diagnóstico del intérprete PHP, carpetas de respaldos con listado de directorios y archivos de bitácoras (`logs`), facilitando a un atacante la obtención de rutas absolutas del sistema de archivos, variables de entorno, directivas de `php.ini` y posibles copias de seguridad:

- **`132.248.248.112` (`443/tcp` – `Apache/2.4.41 (Ubuntu)`):** Expone el archivo `/phpinfo.php` (*Possible information file*) y la ruta `/account.php` (*Possible admin folder*).
- **`132.248.248.115` (`443/tcp` – `Apache/2.4.6 (CentOS)`):** Expone el archivo `/info.php` (*Possible information file*) y `/readme.html`.
- **`132.248.248.121` (`443/tcp` – `Apache/2.4.29 (Ubuntu)` / `https://app1.lcgej.unam.mx`):** Plataforma Moodle que expone la carpeta `/backup/` con listado de directorio habilitado (*Backup folder w/ directory listing*), además de archivos internos como `/admin/environment.xml`, `/lib/db/install.xml` y `/lib/thirdpartylibs.xml`.
- **`132.248.248.153` (`443/tcp` – `Apache/2.4.37 (Rocky Linux)` / `https://slugatlas.lavis.unam.mx/`):** Expone el directorio `/logs/` (*Logs*), junto con `/wp-login.php`, `/wp-admin/upgrade.php` y `/readme.html`.

---

### Hallazgo 3: Listado de Directorios Habilitado (*Directory Listing*) y Directorios de Prueba Expuestos

- **Severidad:** MEDIA (`CVSS: 5.3`).
- **Sistemas afectados:** `132.248.248.102`, `132.248.248.107`, `132.248.248.112`, `132.248.248.113`, `132.248.248.115`, `132.248.248.121`, `132.248.248.152`, `132.248.248.153`, `132.248.248.158`, `132.248.248.159`, `132.248.248.165`, `132.248.248.169`, `132.248.248.175` y `132.248.248.177`.

**Descripción del riesgo:** La ausencia de un archivo índice o la directiva `Options +Indexes` en Apache permite enumerar libremente el contenido de múltiples directorios web:

- **`132.248.248.102` (`app.liigh.unam.mx` – `443/tcp`):** Presenta listado abierto en el directorio raíz `/` (*Root directory w/ listing on 'apache/2.4.7 (ubuntu)'*) y mantiene una instancia adicional de `Apache/2.4.7 (Ubuntu)` escuchando en el puerto no estándar `8888/tcp`.
- **`132.248.248.107` (`443/tcp`):** Listado de directorios activo en `/scripts/` y `/icons/`, además de la ruta `/support/`.
- **`132.248.248.112` y `132.248.248.113` (`443/tcp`):** Listado de directorios activo en `/apps/` (y en `/css/`, `/images/`, `/js/` para `.112`).
- **`132.248.248.121` (`443/tcp`):** Listado de directorios activo en `/backup/`, `/cache/`, `/img/`, `/info/`, `/install/`, `/local/`, `/privacy/` y `/report/`.
- **`132.248.248.169` (`443/tcp`):** Expone carpetas de prueba y scripts de ejemplo en `/examples/` (*Sample scripts*), `/test/` (*Test page*), `/prueba/`, `/contact/` y `/icons/`.
- **`132.248.248.175` (`kneipe.lavis.unam.mx` – `443/tcp`):** Listado de directorios activo en `/css/`, `/icons/`, `/img/` y `/js/`.

---

### Hallazgo 4: Divulgación de Información en Cabeceras HTTP (*Information Disclosure*) y Librerías Criptográficas Obsoletas

- **Severidad:** BAJA a MEDIA (`CVSS: 5.3` según plantilla).
- **Sistemas afectados:** 22 servidores web que exponen versiones exactas en la cabecera `Server` o `X-Powered-By`.

**Descripción del riesgo:** La presencia de los encabezados `X-Powered-By` y `Server` detallados revela la tecnología, distribución del sistema operativo, versión de OpenSSL y versión exacta del entorno de ejecución backend, facilitando la fase de reconocimiento a posibles atacantes:

- **Exposición de `X-Powered-By`:** Detectada en `132.248.248.115` (`PHP/7.3.33`), `132.248.248.153` (`PHP/8.5.12`), `132.248.248.157` (`Express`), `132.248.248.158` (`PHP/8.5.12`), `132.248.248.159` (`PHP/8.5.12`), `132.248.248.175` (`PHP/8.0.30`) y `132.248.248.177` (`PHP/8.2.35`).
- **Servidores con versiones EOL de OpenSSL y Apache en cabeceras `Server`:**
  - `OpenSSL/1.0.2k-fips` con `Apache/2.4.6 (CentOS)` en `132.248.248.115` y `132.248.248.152`.
  - `OpenSSL/1.1.1k` con `Apache/2.4.37 (Rocky Linux)` en `132.248.248.153`, `132.248.248.158`, `132.248.248.159` y `132.248.248.169`.
  - `Apache/2.4.7 (Ubuntu)` en `132.248.248.102` (`app.liigh.unam.mx`).

---

### Hallazgo 5: Exposición de Interfaces Administrativas de Impresoras y Dispositivos Embebidos en el Segmento de Servidores

- **Severidad:** BAJA (`CVSS: 3.7`).
- **Sistemas afectados:** `132.248.248.33`, `132.248.248.57`, `132.248.248.74`, `132.248.248.87`, `132.248.248.103` y `132.248.248.232`.

**Descripción del riesgo:** Se identificaron dispositivos de impresión, sistemas embebidos en tiempo real y consolas de administración compartiendo el mismo segmento de red que los servidores de aplicaciones institucionales y respondiendo por HTTP sin cifrado:

- **Impresoras multifuncionales:** `132.248.248.33` (`Kyocera MFP httpd 0.0.1` en `80/tcp` y `443/tcp`), `132.248.248.57` (`RapidLogic httpd 1.1` – *Sharp MX-2700N printer* en `80/tcp`) y `132.248.248.74` (*HP LaserJet CP1205nw or P1606 http config* en `80/tcp` y `8080/tcp`).
- **Sistemas embebidos / middleware / gestión:** `132.248.248.87` (*The Knopflerfish HTTP Server* OSGi en `8080/tcp`), `132.248.248.103` (*Segger embOS/IP httpd* en `80/tcp`) y `132.248.248.232` (interfaz web en `80/tcp`, `443/tcp` y `8443/tcp` que redirige a `/doc/index.html` y devuelve respuestas `401 Unauthorized` ante enumeración de carpetas).

---

## 5. Plan de Remediación y Recomendaciones

Para mitigar los riesgos identificados se recomiendan las siguientes acciones técnicas priorizadas:

1. **Actualización de intérprete PHP y sistemas operativos base (prioridad crítica – plazo máximo de 24 a 72 horas):**
   - Actualizar las instancias de PHP en `132.248.248.115` (`PHP 7.3.33`), `132.248.248.152` (`PHP 5.4.16`) y `132.248.248.175` (`PHP 8.0.30`) a ramas de la serie `8.x` con soporte oficial de seguridad activo y parches contra `CVE-2026-109618` y `CVE-2026-109619`.
   - Planificar la migración de los servidores que aún operan sobre CentOS 7 (`Apache/2.4.6`, `OpenSSL/1.0.2k-fips`) y Ubuntu 14.04 (`Apache/2.4.7`) hacia distribuciones con soporte vigente.
   - Realizar pruebas de compatibilidad del código web en un entorno de desarrollo antes del despliegue en producción.

2. **Endurecimiento de configuración (hardening de PHP):**
   - Editar el archivo `php.ini` en todos los servidores en producción para aplicar las siguientes directivas de seguridad:

   ```ini
   expose_php = Off
   display_errors = Off
   allow_url_fopen = Off
   allow_url_include = Off
   disable_functions = exec,passthru,shell_exec,system,proc_open,popen,curl_exec,parse_ini_file
   ```

3. **Eliminación de archivos sensibles y desactivación de listado de directorios (prioridad alta):**
   - Eliminar o restringir inmediatamente el acceso público a `/phpinfo.php` en `132.248.248.112` y `/info.php` en `132.248.248.115`.
   - Bloquear el acceso web al directorio `/backup/` en `132.248.248.121`, al directorio `/logs/` en `132.248.248.153`, y a los directorios `/examples/`, `/test/` y `/prueba/` en `132.248.248.169`.
   - Deshabilitar el listado de directorios en Apache (especialmente en la raíz de `132.248.248.102`) configurando `Options -Indexes` dentro de los bloques `<Directory>` correspondientes.

4. **Ocultamiento de cabeceras del servidor:**
   - En **Apache**, agregar o modificar las directivas `ServerTokens Prod` y `ServerSignature Off` en `httpd.conf` o `apache2.conf`.
   - En **Nginx** (`132.248.248.61`, `132.248.248.157`, `132.248.248.233`), agregar la directiva `server_tokens off;` en el bloque `http` de la configuración global.
   - En aplicaciones **Node.js / Express** (`132.248.248.157`), deshabilitar la cabecera `X-Powered-By: Express` mediante `app.disable('x-powered-by')`.

5. **Segmentación de red para dispositivos de impresión y sistemas embebidos:**
   - Reubicar las impresoras (`132.248.248.33`, `132.248.248.57`, `132.248.248.74`) y los dispositivos embebidos (`132.248.248.87`, `132.248.248.103`, `132.248.248.232`) en una VLAN administrativa restringida mediante listas de control de acceso (ACL).

---

## 6. Anexo: Inventario Consolidado de los 36 Activos Web Evaluados

La siguiente tabla resume la totalidad de las 36 direcciones IP detectadas en `descubrimientos_web.txt` / `ips_web.txt` y sus resultados en los escaneos posteriores:

| IP | Hostname / Dominio Identificado | Puertos Abiertos | Servidor / Software Detectado | Observaciones Principales |
| --- | --- | --- | --- | --- |
| `132.248.248.33` | N/A | `80`, `443` | `Kyocera MFP httpd 0.0.1` (`KM-MFP-http/V0.0.1`) | Impresora multifuncional en red. |
| `132.248.248.37` | N/A | `8080` (en descubrimiento) | `http-proxy` (tabla) | Activo en descubrimiento inicial; inactivo en `-sV` y `php2shell_scan`. |
| `132.248.248.57` | N/A | `80` (`443` cerrado en `-sV`) | `RapidLogic httpd 1.1` (*Sharp MX-2700N printer*) | Impresora Sharp en red. |
| `132.248.248.61` | N/A | `80`, `443` | `nginx/1.18.0 (Ubuntu)` | Expone versión de Nginx y SO en cabecera `Server`. |
| `132.248.248.62` | `www.campusjuriquilla.unam.mx` (Redirect) | `80`, `443` | `Apache httpd` | Sitio WordPress (`/wp-login.php`, `/wp-json`, `/servicios/`, cookies `breakdance_*`). |
| `132.248.248.74` | N/A | `80`, `8080` | `HP LaserJet CP1205nw or P1606 http config` | Impresora HP con consola HTTP en puertos `80` y `8080`. |
| `132.248.248.87` | N/A | `80`, `8080` | `tcpwrapped` (`80`), `Knopflerfish httpd` (`8080`) | Servidor HTTP OSGi Knopflerfish en puerto `8080`. |
| `132.248.248.95` | N/A | `443`, `8080` (descubrimiento) | `https` (`443`), `http-proxy` (`8080`) | No respondió en `-sV`; activo en `443/tcp` durante `php2shell_scan`. |
| `132.248.248.101` | `liigh.unam.mx` (PTR) | `80`, `443` | `Apache httpd` | Sitio WordPress con cabeceras de seguridad (`HSTS`, `CSP`, `X-Frame-Options`). |
| `132.248.248.102` | `app.liigh.unam.mx` (PTR) | `443`, `8888` | `Apache/2.4.7 (Ubuntu)` | Listado de directorio raíz (`/`) habilitado en `443/tcp` y servicio en `8888/tcp`. |
| `132.248.248.103` | N/A | `80` | `Segger embOS/IP httpd` (`embOS/IP`) | Dispositivo embebido en tiempo real (filtró `80/tcp` en `php2shell_scan`). |
| `132.248.248.107` | N/A | `80`, `443` | `Apache/2.4.62 (Rocky Linux) OpenSSL/3.5.8` | Listado de directorios en `/icons/` y `/scripts/`; carpeta `/support/`. |
| `132.248.248.112` | N/A | `80`, `443` | `Apache/2.4.41 (Ubuntu)` | Expone `/phpinfo.php`, `/account.php`, cookie `OSTSESSID` y listado en `/apps/`. |
| `132.248.248.113` | N/A | `80`, `443` | `Apache/2.4.41 (Ubuntu)` | Listado de directorios en `/apps/`. |
| `132.248.248.115` | N/A | `80`, `443` | `Apache/2.4.6 (CentOS) OpenSSL/1.0.2k-fips PHP/7.3.33` | **VULNERABLE (`CVE-2026-109618` / `109619`)**; expone `/info.php` y PHP `7.3.33` EOL. |
| `132.248.248.121` | `app1.lcgej.unam.mx` (Redirect) | `80`, `443` | `Apache/2.4.29 (Ubuntu)` (Moodle) | Expone `/backup/` con listado de directorios y archivos XML de Moodle. |
| `132.248.248.128` | `mexpd.liigh.unam.mx` (Header Link) | `80`, `443` | `Apache/2.4.41 (Ubuntu)` (WordPress) | **Reportado en `php2shell_scan`** (`Observed PHP version: 2.9.5` en cuerpo HTTP). |
| `132.248.248.131` | `enfermedadesraras.liigh.unam.mx` (Link) | `80`, `443` | `Apache/2.4.41 (Ubuntu)` (WordPress) | Expone `/wp-login.php`, `/wp-admin/upgrade.php` y `/readme.html`. |
| `132.248.248.137` | N/A | `80`, `443` | `Apache/2.4.52 (Ubuntu)` (DokuWiki) | Redirige a `/doku.php?id=start`; expone `/README` y `/lib/`. |
| `132.248.248.138` | `mendvar.liigh.unam.mx` (SSL Host) | `80`, `443` | `Apache/2.4.41 (Ubuntu)` | Expone versión de Apache y SO en cabecera `Server`. |
| `132.248.248.152` | N/A | `80`, `443` | `Apache/2.4.6 (CentOS) OpenSSL/1.0.2k-fips PHP/5.4.16` | **VULNERABLE (`CVE-2026-109618` / `109619`)**; ejecuta PHP `5.4.16` EOL. |
| `132.248.248.153` | `slugatlas.lavis.unam.mx` (Redirect) | `80`, `443` | `Apache/2.4.37 (Rocky Linux) OpenSSL/1.1.1k` (`PHP/8.5.12`) | Sitio WordPress; expone directorio `/logs/` y cabecera `X-Powered-By`. |
| `132.248.248.154` | N/A | `80`, `443` | `Apache/2.4.41 (Ubuntu)` | Expone versión de servidor web en cabecera `Server`. |
| `132.248.248.157` | N/A | `80`, `443` | `nginx/1.18.0 (Ubuntu)` (`X-Powered-By: Express`) | Aplicación Express detrás de Nginx; expone `X-Instance-ID`. |
| `132.248.248.158` | `varelab.lavis.unam.mx` (Header Link) | `80`, `443` | `Apache/2.4.37 (Rocky Linux) OpenSSL/1.1.1k` (`PHP/8.5.12`) | Sitio WordPress (`/wordpress/`); expone `X-Powered-By` y listado en `/icons/`. |
| `132.248.248.159` | `limaco.lavis.unam.mx` (Redirect) | `80`, `443` | `Apache/2.4.37 (Rocky Linux) OpenSSL/1.1.1k` (`PHP/8.5.12`) | Sitio WordPress; expone `X-Powered-By` y listado en `/icons/`. |
| `132.248.248.165` | `lavis.unam.mx` (PTR) | `80`, `443` | `Apache/2.4.63 (Rocky Linux) OpenSSL/3.5.8` | Listado en `/icons/` y carpeta `/servicios/`. |
| `132.248.248.168` | N/A | `80`, `443` | `Apache/2.4.62 (Rocky Linux) OpenSSL/3.0.7` | Expone versión de Apache y OpenSSL en cabecera `Server`. |
| `132.248.248.169` | N/A | `80`, `443` | `Apache/2.4.37 (Rocky Linux) OpenSSL/1.1.1k` | Expone `/examples/`, `/test/`, `/prueba/`, `/contact/` y listado en `/icons/`. |
| `132.248.248.175` | `kneipe.lavis.unam.mx` (PTR) | `443` | `Apache/2.4.62 (Rocky Linux) OpenSSL/3.5.8` (`PHP/8.0.30`) | **VULNERABLE (`CVE-2026-109618` / `109619`)**; PHP `8.0.30` EOL y listado en `/css/`, `/img/`, `/js/`. |
| `132.248.248.177` | N/A | `80`, `443` | `Apache/2.4.62 (Rocky Linux) OpenSSL/3.5.8` (`PHP/8.2.35`) | Instancia Matomo Analytics (`MATOMO_SESSID`); expone `X-Powered-By: PHP/8.2.35`. |
| `132.248.248.232` | N/A | `80`, `443`, `8443` | Servicio HTTP embebido (redirige a `/doc/index.html`) | Interfaz web de dispositivo de red/cámara con puertos `80`, `443` y `8443` abiertos. |
| `132.248.248.233` | N/A | `80`, `443` | `nginx` | Configurado sin revelar número de versión en cabecera `Server: nginx`. |
| `132.248.248.239` | N/A | `80`, `443` | `http` / `https` | Puertos abiertos sin firma de versión ni cabeceras devueltas ante sondeo estándar. |
| `132.248.248.248` | N/A | `80`, `443` | `http` / `https` | Puertos abiertos sin firma de versión devuelta. |
| `132.248.248.249` | N/A | `80`, `443` | `http` / `https` | Puertos abiertos sin firma de versión devuelta. |

---

## 7. Control de Firmas y Responsables

| Rol | Nombre | Firma |
| --- | --- | --- |
| **Auditor de Ciberseguridad** | Brayan Coronel Ramírez / Dr. Ulises Mora Álvarez | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ |
| **Recibido por (TI)** | Responsables de Infraestructura TI – ENES Juriquilla | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ |
