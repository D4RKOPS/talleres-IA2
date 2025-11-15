# 📘 Especificación de Requerimientos — *QuickTask*

## 1. Descripción general del sistema

**QuickTask** es una aplicación destinada a la gestión sencilla y rápida de tareas personales. Permite a los usuarios crear, editar, eliminar y marcar tareas como completadas. El enfoque principal del sistema es la simplicidad, velocidad de uso y disponibilidad en dispositivos móviles y web.
El sistema almacenará las tareas del usuario, permitirá organizarlas y ofrecerá recordatorios opcionales.

---

## 2. Actores principales

* **Usuario**: Persona que crea y gestiona tareas personales.
* **Sistema QuickTask**: Plataforma que procesa solicitudes, almacena información y presenta la interfaz al usuario.
* **Servicio de notificaciones** (opcional): Sistema externo usado para enviar recordatorios al usuario.

---

## 3. Requerimientos funcionales (RF)

### Gestión de tareas

1. **RF-01**: El sistema debe permitir al usuario crear una nueva tarea ingresando un título obligatorio y una descripción opcional.
2. **RF-02**: El sistema debe permitir al usuario editar el título y descripción de una tarea existente.
3. **RF-03**: El sistema debe permitir al usuario eliminar una tarea existente.
4. **RF-04**: El sistema debe permitir al usuario marcar una tarea como completada.
5. **RF-05**: El sistema debe mostrar al usuario una lista de todas las tareas creadas, indicando claramente cuáles están completas e incompletas.

### Organización y filtrado

6. **RF-06**: El sistema debe permitir filtrar la lista de tareas por estado (completadas / pendientes).
7. **RF-07**: El sistema debe permitir ordenar las tareas por fecha de creación o por título.

### Recordatorios (opcional)

8. **RF-08**: El sistema debe permitir al usuario activar un recordatorio para una tarea con fecha/hora específica.
9. **RF-09**: El sistema debe enviar una notificación al usuario cuando el recordatorio llegue al tiempo especificado.

### Persistencia y usuarios

10. **RF-10**: El sistema debe permitir almacenar todas las tareas de manera persistente.
11. **RF-11**: El sistema debe permitir autenticación del usuario mediante correo y contraseña (si aplica multiusuario).
12. **RF-12**: El sistema debe mostrar únicamente las tareas asociadas al usuario autenticado.

---

## 4. Requerimientos no funcionales (RNF)

### Rendimiento

1. **RNF-01**: El sistema debe mostrar la lista de tareas en menos de 2 segundos.
2. **RNF-02**: Las operaciones de creación, edición y completado deben procesarse en menos de 1 segundo.

### Usabilidad

3. **RNF-03**: La interfaz debe ser intuitiva y usable sin capacitación previa.
4. **RNF-04**: El diseño debe ser responsive y funcionar correctamente en dispositivos móviles, tabletas y PCs.

### Seguridad

5. **RNF-05**: Las contraseñas deben almacenarse usando hashing seguro.
6. **RNF-06**: La comunicación entre cliente y servidor debe usar HTTPS.

### Disponibilidad

7. **RNF-07**: El sistema debe estar disponible al menos el 99% del tiempo mensual.

### Compatibilidad

8. **RNF-08**: El sistema debe ser compatible con los navegadores actuales (Chrome, Firefox, Edge, Safari).

---

## 5. Criterios de aceptación (CA)

### CA-01 — Crear tarea

* Dado que el usuario se encuentra en la pantalla de tareas,
* Cuando ingresa un título válido y presiona “Crear”,
* Entonces la tarea aparece inmediatamente en la lista con estado “pendiente”.

### CA-02 — Editar tarea

* Dado que el usuario selecciona una tarea existente,
* Cuando modifica el título o descripción y guarda los cambios,
* Entonces la tarea debe actualizarse en la lista mostrando los nuevos valores.

### CA-03 — Marcar tarea como completada

* Dado que el usuario tiene una tarea pendiente,
* Cuando presiona la opción “Marcar como completada”,
* Entonces la tarea debe aparecer como completada y debe diferenciarse visualmente (color, ícono o tachado).

---

## 6. Suposiciones y restricciones

### Suposiciones

* Se asume que cada usuario gestiona únicamente sus propias tareas.
* Se asume que el sistema operará con conexión a Internet (modo offline no contemplado inicialmente).
* Se asume que el servicio de notificaciones será provisto por un tercero confiable.

### Restricciones

* La primera versión solo incluirá funcionalidades básicas de CRUD de tareas.
* El presupuesto limita el uso de servicios de infraestructura complejos.
* La aplicación móvil debe desarrollarse inicialmente como web responsiva (no nativa).

---

## Riesgos o ambigüedades detectadas

* Falta definir si la aplicación será multiusuario desde la primera versión.
* No está claro si los recordatorios serán parte del MVP o una fase posterior.
* No se especifica si habrá categorías, etiquetas o niveles de prioridad.
* Falta aclarar si debe existir sincronización offline.
* No se define límite de almacenamiento o número máximo de tareas.

