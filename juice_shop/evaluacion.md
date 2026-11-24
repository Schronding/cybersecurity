# **Práctica de Laboratorio: Evaluación No Invasiva de Seguridad en Aplicaciones Web y Gestión de Riesgos (NIST CSF 2.0)**

**Asignatura:** Temas Selectos de Seguridad de la Información  
**Entorno de Laboratorio:** OWASP Juice Shop (Despliegue Local Aislado)  
**Enfoque:** Análisis dinámico de seguridad (DAST), validación no invasiva y reporte ejecutivo-técnico basado en gestión de riesgos.

## **Parte 1: Guía de Práctica para el Estudiante**

### **1\. Objetivos de Aprendizaje**

Al finalizar esta práctica, el estudiante será capaz de:

> 1. Desplegar un entorno de pruebas controlado mediante contenedores locales utilizando **OWASP Juice Shop**.  
> 2. Configurar y operar herramientas de análisis automatizado basado en plantillas (**Nuclei**) y proxies de inspección web (**OWASP ZAP**) bajo criterios de control de ruido y tasa de peticiones.  
> 3. Aplicar criterios metodológicos de **validación no invasiva** para confirmar fallas de inyección SQL mediante **sqlmap**, evitando la exfiltración de datos o la alteración de la integridad del sistema.  
> 4. Documentar hallazgos técnicos y estimar su nivel de riesgo asociándolos a las funciones y categorías del marco **NIST Cybersecurity Framework (CSF) 2.0**.

### **2\. Reglas de Alcance y Seguridad (Reglas de Compromiso)**

* **Aislamiento estricto:** Todas las pruebas deben dirigirse exclusivamente a la instancia local (http\://localhost:3000 o \[http\://127.0.0.1:3000\](http\://127.0.0.1:3000)). Queda estrictamente prohibido dirigir herramientas de escaneo hacia direcciones IP externas o dominios públicos.  
* **Principio de mínima invasividad:** El objetivo de una auditoría de validación es **demostrar la existencia** de una vulnerabilidad, no explotarla. En pruebas de inyección SQL, queda prohibida la extracción de tablas, volcado de credenciales o modificación de registros; la prueba debe detenerse en cuanto se confirme la condición lógica o temporal que evidencia el fallo.

### **3\. Preparación del Entorno Base (OWASP Juice Shop)**

Para garantizar un entorno reproducible y limpio, se recomienda el despliegue mediante Docker:

> 1. **Verificación de requisitos:** Asegúrese de contar con Docker Engine activo en su máquina anfitriona o máquina virtual de laboratorio (ej. Kali Linux, Ubuntu o Parrot OS).  
> 2. **Despliegue de la aplicación:** Descargue la imagen oficial bkimminich/juice-shop y publíquela en el puerto local 3000:  
>    Bash  
>    docker pull bkimminich/juice-shop  
>    docker run \--rm \-p 127.0.0.1:3000:3000 bkimminich/juice-shop

> 3. **Comprobación:** Abra un navegador web en \[http\://127.0.0.1:3000\](http\://127.0.0.1:3000) y verifique que la interfaz de la tienda cargue correctamente.

### **4\. Desarrollo de los Módulos Técnicos**

#### **Módulo 1: Instalación y Uso Controlado de Nuclei**

**Nuclei** es un motor de escaneo rápido basado en plantillas YAML diseñadas para detectar configuraciones erróneas, exposiciones de archivos sensibles y vulnerabilidades conocidas (CVE) de manera determinista.

> 1. **Instalación:**  
   * **Vía gestor de paquetes (Linux/macOS):** Utilice el gestor de su distribución (por ejemplo, sudo apt update && sudo apt install nuclei en distribuciones basadas en Debian/Kali, o brew install nuclei en macOS).  
   * **Vía binarios oficiales / Go:** Alternativamente, descargue el binario precompilado desde el repositorio oficial de *ProjectDiscovery* en GitHub y añádalo a su variable de entorno PATH.  
   * **Actualización de plantillas:** Ejecute la actualización del repositorio local de plantillas (nuclei \-update-templates) antes de iniciar la evaluación.  
> 2. **Metodología de Configuración y Ejecución:**  
   * **Delimitación por etiquetas y severidad:** En lugar de lanzar miles de plantillas indiscriminadamente, configure filtros por categorías relevantes para aplicaciones web (como exposiciones, cabeceras de seguridad, tecnologías detectadas o niveles de severidad *low*, *medium*, *high*).  
   * **Control de tráfico:** Configure parámetros de limitación de tasa (*rate-limit*) y concurrencia baja para evitar saturar el servidor local y simular buenas prácticas en entornos productivos.  
   * **Exportación de evidencia:** Habilite la salida estructurada (formato JSON o Markdown) para conservar trazabilidad de las peticiones y respuestas HTTP que dispararon cada regla.  
> 3. **Entregables del Módulo 1:**  
   * Captura de la versión instalada y del repositorio de plantillas actualizado.  
   * Lista de los hallazgos identificados (ej. ausencia de cabeceras de seguridad, exposición de rutas de administración o divulgación de información), diferenciando los hallazgos reales de posibles falsos positivos.

#### **Módulo 2: Instalación y Uso de OWASP ZAP (Zed Attack Proxy)**

**OWASP ZAP** es una herramienta de pruebas dinámicas de seguridad de aplicaciones (DAST) que actúa como proxy interceptador entre el navegador y la aplicación web.

> 1. **Instalación:**  
   * **Vía gestor de paquetes o instalador oficial:** Instale mediante el paquete de su distribución (sudo apt install zaproxy), mediante Flatpak/Snap, o descargando el instalador multiplataforma desde el sitio oficial de *ZAP (zaproxy.org)*.  
> 2. **Metodología de Evaluación:**  
   * **Fase 1 — Reconocimiento Pasivo (Spidering):** Configure su navegador para enrutar el tráfico a través del proxy local de ZAP (por defecto 127.0.0.1:8080). Navegue manualmente por las funcionalidades principales de Juice Shop (registro, inicio de sesión, búsqueda de productos, carrito) y ejecute el *Spider* tradicional y *AJAX Spider* para mapear el árbol de rutas y endpoints API.  
   * **Fase 2 — Análisis de Alertas Pasivas:** Revise la pestaña de *Alertas* generadas únicamente por la inspección del tráfico legítimo (sin enviar tráfico malicioso), observando problemas en cookies (HttpOnly, SameSite), políticas CORS y cabeceras CSP.  
   * **Fase 3 — Escaneo Activo Acotado:** Defina un *Contexto* que incluya únicamente \[http\://127.0.0.1:3000\](http\://127.0.0.1:3000). Configure una política de escaneo activo moderada sobre endpoints específicos y analice el comportamiento de las respuestas HTTP obtenidas.  
> 3. **Entregables del Módulo 2:**  
   * Mapa del sitio (*Site Tree*) capturado tras la exploración manual y automatizada.  
   * Tabla comparativa entre al menos 3 alertas obtenidas en modo pasivo y 2 alertas identificadas durante el análisis activo, explicando la causa raíz a nivel HTTP.

#### **Módulo 3: Instalación y Validación No Invasiva de Inyecciones SQL con sqlmap**

**sqlmap** es una herramienta automatizada para detectar y evaluar fallas de inyección SQL. En auditorías profesionales, su uso debe restringirse estrictamente a la **confirmación técnica** del vector sin comprometer la confidencialidad de los datos almacenados.

> 1. **Instalación:**  
   * **Vía gestor de paquetes o Python:** Instale mediante sudo apt install sqlmap en sistemas basados en Debian/Kali, brew install sqlmap en macOS, o clonando el repositorio oficial en Python 3\.  
> 2. **Criterios de Validación No Invasiva:**  
   * **Identificación de puntos de entrada:** A partir del mapeo realizado en OWASP ZAP, identifique parámetros de consulta o cuerpos JSON en endpoints de búsqueda o autenticación que interactúen con la base de datos subyacente (SQLite en el caso de Juice Shop).  
   * **Selección de técnicas seguras:** Limite la evaluación a técnicas de detección lógica (como inyección booleana o basada en errores) mediante el ajuste de nivel (--level) y riesgo (--risk) en sus valores mínimos (1), evitando pruebas que generen carga excesiva o alteren el estado de la base de datos.  
   * **Límite de alcance (No exfiltración):** Utilice únicamente indicadores de identificación de infraestructura (como la detección del gestor de base de datos o banner básico) y **no utilice** banderas de enumeración de tablas, columnas o volcado de registros.  
   * **Modo por lotes y control de tráfico:** Emplee ejecución no interactiva controlada y retardos entre peticiones cuando sea necesario para observar el comportamiento determinista de la aplicación ante entradas anómalas.  
> 3. **Entregables del Módulo 3:**  
   * Evidencia de la petición HTTP analizada (parámetro vulnerable identificado a través de ZAP).  
   * Registro de salida donde la herramienta confirma el tipo de motor de base de datos y la técnica de detección empleada, acompañado de una explicación teórica de por qué el parámetro no sanitizado permite alterar la consulta SQL original.

## **Parte 2: Plantilla de Reporte Técnico Alineado a NIST CSF 2.0**

*Instrucciones para el estudiante: Utilice la siguiente estructura para redactar el informe final de la práctica.*

### **\[NOMBRE DE LA INSTITUCIÓN / MATERIA\]**

### **INFORME DE EVALUACIÓN DE VULNERABILIDADES WEB (ENTORNO DE LABORATORIO)**

| Campo | Detalle |
| :---- | :---- |
| **Proyecto / Sistema Evaluado** | OWASP Juice Shop (Instancia Local) |
| **Versión del Documento** | 1.0 |
| **Fecha de Evaluación** | \[DD/MM/AAAA\] |
| **Equipo Auditor (Estudiantes)** | \[Nombres y Matrículas\] |
| **Marco de Referencia** | NIST Cybersecurity Framework (CSF) 2.0 & OWASP Top 10 |

#### **1\. Resumen Ejecutivo y Gobernanza (Función NIST CSF 2.0: *Govern \- GV*)**

*Describa brevemente el propósito de la evaluación, el enfoque no invasivo aplicado y el estado general de postura de seguridad observado en la aplicación.*

* **Alineación con Gobernanza (GV.RM \- Gestión de Riesgos y GV.OV \- Supervisión):** Explique cómo los resultados de esta evaluación técnica alimentan la toma de decisiones de la organización para priorizar inversiones en seguridad y establecer políticas de desarrollo seguro.  
* **Resumen de Hallazgos por Severidad:**  
  * Crítica: \[X\] \| Alta: \[X\] \| Media: \[X\] \| Baja: \[X\] \| Informativa: \[X\]

#### **2\. Alcance, Inventario y Metodología (Función NIST CSF 2.0: *Identify \- ID*)**

* **Inventario de Activos Evaluados (ID.AM \- Gestión de Activos):**  
  * **Aplicación:** OWASP Juice Shop (Arquitectura SPA Angular \+ Backend Node.js/Express \+ Base de datos SQLite).  
  * **Endpoint Objetivo:** \[http\://127.0.0.1:3000\](http\://127.0.0.1:3000)  
* **Metodología Aplicada (ID.RA \- Evaluación de Riesgos):**  
  1. Reconocimiento y análisis basado en plantillas (Nuclei).  
  2. Inspección de tráfico proxy, análisis pasivo y activo acotado (OWASP ZAP).  
  3. Validación lógica no invasiva de inyección SQL (sqlmap).

#### **3\. Modelo de Estimación de Riesgo**

Para calcular el nivel de riesgo de cada vulnerabilidad identificada, se combinará la severidad técnica base (**CVSS v3.1 / v4.0**) con el **Impacto Operativo** y la **Probabilidad de Explotación** en el contexto de la aplicación:

$$Riesgo=Probabilidad\times Impacto$$

| Nivel de Riesgo | Rango CVSS Ref. | Criterio de Priorización y Tiempo de Remediación Sugerido |
| :---- | :---- | :---- |
| **Crítico** | 9.0 – 10.0 | Compromiso total de confidencialidad, integridad o disponibilidad; explotación trivial sin autenticación. **Remediación inmediata (\< 48 h).** |
| **Alto** | 7.0 – 8.9 | Acceso no autorizado a datos sensibles o ejecución de lógica privilegiada. **Remediación prioritaria (\< 7 días).** |
| **Medio** | 4.0 – 6.9 | Exposición parcial de información o debilidades que requieren condiciones específicas para ser explotadas. **Remediación planificada (\< 30 días).** |
| **Bajo** | 0.1 – 3.9 | Debilidades de endurecimiento (*hardening*) o faltantes de defensa en profundidad con impacto directo limitado. **Ciclo regular de mantenimiento.** |

#### **4\. Matriz Consolidada de Hallazgos y Mapeo a NIST CSF 2.0**

| ID | Título del Hallazgo | Herramienta | Clasificación (OWASP / CWE) | CVSS / Riesgo Estimado | Función y Categoría NIST CSF 2.0 Impactada |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **VULN-01** | *\[Ej. Inyección SQL en búsqueda de productos\]* | OWASP ZAP / sqlmap | A03:2021 / CWE-89 | **9.8 (Crítico)** | **Protect (PR.PS)**: Seguridad de Plataformas y Desarrollo Seguro |
| **VULN-02** | *\[Ej. Ausencia de cabeceras de seguridad HTTP\]* | Nuclei / ZAP | A05:2021 / CWE-693 | **4.3 (Medio)** | **Protect (PR.PS / PR.IR)**: Configuración Segura y Resiliencia |
| **VULN-03** | *\[Ej. Exposición de rutas o información de depuración\]* | Nuclei | A01:2021 / CWE-200 | **5.3 (Medio)** | **Identify (ID.RA)** / **Protect (PR.DS)**: Protección de Datos |

#### **5\. Ficha Técnica Detallada de Vulnerabilidades**

*(Duplique esta ficha por cada vulnerabilidad documentada en la tabla anterior).*

* **ID y Nombre:** VULN-01 — \[Nombre descriptivo de la vulnerabilidad\]  
* **Componente / Endpoint Afectado:** \[Ej. GET /rest/products/search\]  
* **Herramienta(s) de Detección:** \[Nuclei / OWASP ZAP / sqlmap\]  
* **Estimación del Riesgo:**  
  * **Vector CVSS:** \[Ej. CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H\]  
  * **Probabilidad:** \[Alta / Media / Baja\] — *Justificación:* \[Explique la facilidad de descubrimiento y ausencia de controles previos\].  
  * **Impacto:** \[Crítico / Alto / Medio / Bajo\] — *Justificación:* \[Explique el efecto sobre la confidencialidad, integridad y disponibilidad de los datos\].  
  * **Nivel de Riesgo Final:** **\[Crítico / Alto / Medio / Bajo\]**  
* **Descripción Técnica y Evidencia No Invasiva:**  
  * Explique el comportamiento anómalo observado en la petición/respuesta HTTP. Adjunte capturas de pantalla recortadas que muestren únicamente la confirmación técnica (sin datos sensibles expuestos).  
* **Recomendación de Remediación:**  
  * Indique la corrección específica a nivel de código o configuración (ej. uso de consultas parametrizadas / *Prepared Statements*, validación estricta de esquemas de entrada, configuración de cabeceras Content-Security-Policy y X-Content-Type-Options).

#### **6\. Plan de Remediación y Mejora Continua (NIST CSF 2.0)**

*Complete la siguiente tabla proponiendo controles concretos para fortalecer el ciclo de vida de la aplicación frente a los hallazgos detectados:*

| Función NIST CSF 2.0 | Categoría Relacionada | Acción de Mejora Propuesta para el Entorno Evaluado |
| :---- | :---- | :---- |
| **Govern (GV)** | GV.SC / GV.RM | Establecer estándares internos de codificación segura y exigir pruebas DAST automatizadas antes de cada despliegue a producción. |
| **Identify (ID)** | ID.RA-01 | Mantener un inventario actualizado de endpoints API y ejecutar escaneos periódicos con plantillas actualizadas de Nuclei. |
| **Protect (PR)** | PR.PS-01 / PR.DS | Implementar consultas parametrizadas en el ORM/controlador de base de datos, endurecer cabeceras HTTP y aplicar el principio de mínimo privilegio en el usuario de BD. |
| **Detect (DE)** | DE.CM-09 | Configurar registros centralizados (*logging*) y alertas en WAF/SIEM ante patrones anómalos de consulta o tasas elevadas de errores HTTP 500/400. |
| **Respond (RS)** | RS.MA / RS.MI | Definir un procedimiento de contención rápida (bloqueo de reglas en WAF o deshabilitación temporal de endpoints vulnerables) ante alertas activas. |
| **Recover (RC)** | RC.RP-01 | Verificar la integridad de las copias de seguridad de la base de datos y validar el restablecimiento limpio tras aplicar los parches de seguridad. |

### 

### **Rúbrica de Evaluación (Para uso del Instructor)**

| Criterio | Excelente (100%) | Satisfactorio (80%) | Insuficiente (\< 60%) |
| :---- | :---- | :---- | :---- |
| **Configuración y Uso de Herramientas (35%)** | Instala y opera Nuclei, ZAP y sqlmap siguiendo criterios de control de tráfico y alcance local sin errores. | Opera las herramientas correctamente, pero omite ajustes de control de tasa o filtrado de ruido. | Ejecución desordenada, fuera de alcance o sin evidencia clara de configuración. |
| **Validación No Invasiva (25%)** | Confirma la inyección SQL y demás hallazgos deteniéndose en la detección lógica sin exfiltrar datos. | Confirma los hallazgos con evidencia parcial o falta de claridad en la explicación del vector. | Realiza volcado innecesario de datos o no logra demostrar técnicamente la falla. |
| **Estimación de Riesgo y NIST CSF 2.0 (30%)** | Calcula correctamente CVSS/Riesgo y mapea cada hallazgo con precisión a las 6 funciones del NIST CSF 2.0. | Asigna severidades razonables, pero el mapeo a las categorías de NIST CSF 2.0 es superficial. | Confunde severidad con riesgo o utiliza referencias obsoletas sin integrar Gobernanza (GV). |
| **Calidad del Reporte y Remediación (10%)** | Redacción ejecutiva y técnica clara, con remediaciones accionables a nivel de código y arquitectura. | Reporte estructurado, aunque con recomendaciones genéricas de mitigación. | Reporte incompleto, desorganizado o carente de recomendaciones técnicas. |

