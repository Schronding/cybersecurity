# **Guía de Estudio: OWASP Juice Shop para Estudiantes de Ciberseguridad**

Esta guía tiene como objetivo orientar a los estudiantes de **Temas Selectos de Ciberseguridad** en la exploración sistemática de vulnerabilidades dentro del entorno controlado de OWASP Juice Shop. Se enfoca en la comprensión de los fallos subyacentes más que en la ejecución mecánica de comandos.

**Índice**

[**Guía de Estudio: OWASP Juice Shop para Estudiantes de Ciberseguridad	1**](#heading=)

[1\. Preparación del Entorno y Metodología	1](#heading=)

[2\. Progresión de Desafíos (Niveles 1-3)	1](#heading=)

[Nivel 1: Vulnerabilidades de "Baja Colgante"	1](#heading=)

[Nivel 2: Manipulación de Lógica y Parámetros	2](#heading=)

[Nivel 3: Explotación de Vulnerabilidades del OWASP Top 10	2](#heading=)

[3\. Sección Especial: Inyección SQL (SQLi)	2](#heading=)

[Conceptos para Practicar	2](#heading=)

[Retos Sugeridos (Sin Soluciones)	2](#heading=)

[4\. Consejos para el Éxito	3](#heading=)

## **1\. Preparación del Entorno y Metodología**

Antes de comenzar con los retos, es fundamental establecer un flujo de trabajo profesional:

* **Reconocimiento Pasivo:** Navega por la aplicación como un usuario normal. Identifica las funcionalidades principales (registro, búsqueda, carrito, administración).  
* **Herramientas de Interceptación:** Configura un proxy (como Burp Suite o OWASP ZAP). Observa cómo viajan los datos entre el cliente y el servidor.  
* **Análisis de Código Fuente:** Juice Shop es una aplicación Single Page (SPA). Inspecciona los archivos .js cargados en el navegador para encontrar rutas ocultas o lógica de validación en el cliente.

## **2\. Progresión de Desafíos (Niveles 1-3)**

Para estudiantes de ciberseguridad, se recomienda seguir una curva de aprendizaje que va desde la observación de errores comunes hasta la manipulación activa de la lógica del servidor.

### **Nivel 1: Vulnerabilidades de "Baja Colgante"**

* **Enfoque:** Errores de configuración y falta de higiene en la exposición de datos.  
* **Habilidades a desarrollar:** Inspección de elementos DOM, lectura de comentarios en el código fuente (main.js, vendor.js) y descubrimiento de rutas por fuerza bruta o adivinación lógica.  
* **Ejemplo de objetivo:** Localizar el tablero de puntuación o encontrar archivos de configuración expuestos accidentalmente.

### **Nivel 2: Manipulación de Lógica y Parámetros**

* **Enfoque:** Intercepción de tráfico y alteración de peticiones simples.  
* **Habilidades a desarrollar:** Uso básico de Proxies de Interceptación (Burp/ZAP). El estudiante debe aprender a modificar valores en el cuerpo de la petición (JSON) o en las cabeceras antes de que lleguen al servidor.  
* **Ejemplo de objetivo:** Realizar compras con precios modificados o calificar productos bajo la identidad de otro usuario mediante la alteración de IDs.

### **Nivel 3: Explotación de Vulnerabilidades del OWASP Top 10**

* **Enfoque:** Vulnerabilidades críticas que requieren payloads específicos.  
* **Habilidades a desarrollar:** Inyección de scripts (XSS), inyecciones de bases de datos (SQLi) y bypass de autenticación. Aquí el estudiante debe entender cómo el servidor procesa las entradas y cómo evadir filtros mal implementados.  
* **Ejemplo de objetivo:** Acceder a cuentas administrativas o ejecutar scripts en el navegador de otros usuarios (simulado) para el robo de sesiones.

## **3\. Sección Especial: Inyección SQL (SQLi)**

La inyección SQL en Juice Shop es particularmente educativa porque utiliza una base de datos **SQLite**, lo que requiere adaptar algunos payloads tradicionales.

### **Conceptos para Practicar**

Para resolver los retos de SQLi, los estudiantes deben investigar y aplicar los siguientes conceptos:

1. **Tautologías:** Utilizar condiciones que siempre resultan verdaderas (ej. OR 1=1) para saltar comprobaciones lógicas.  
2. **Comentarios de SQL:** Identificar cómo terminar una consulta prematuramente para ignorar el resto del código original (investigar el uso de \-- en SQLite).  
3. **UNION-Based SQLi:** Aprender a unir resultados de una consulta legítima con datos de otras tablas del sistema (como sqlite\_master).  
4. **Error-Based SQLi:** Forzar errores en la base de datos que revelen información sobre la estructura de las tablas o versiones del software.

### **Retos Sugeridos (Sin Soluciones)**

* **Login de Administrador:** El reto clásico de entrar a la cuenta con mayor privilegio sin conocer la contraseña. Enfócate en el campo de "Email".  
* **Búsqueda de Productos:** Algunos campos de búsqueda no filtran caracteres especiales. Intenta manipular la consulta para que devuelva productos que no deberían estar visibles.  
* **Inyección en el Feedback:** Explora si los formularios de contacto o reseñas guardan información de manera insegura que pueda ser explotada al ser consultada posteriormente.

## **4\. Consejos para el Éxito**

* **No saltes niveles:** Los retos de 1 estrella enseñan las bases necesarias para los de 5 o 6 estrellas.  
* **Lee la documentación de SQLite:** Muchas funciones de bases de datos estándar (como las de MySQL o PostgreSQL) no funcionan igual en SQLite.  
* **Revisa el Score Board:** Úsalo para identificar qué retos pertenecen a qué categoría, pero intenta no mirar las pistas externas a menos que sea estrictamente necesario.