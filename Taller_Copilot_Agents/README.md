
---

# Agente Administrativo – Microsoft Copilot Studio

Este proyecto corresponde a una actividad académica en la clase de **Inteligencia Artificial**, donde se diseñó un **agente conversacional** en [Microsoft Copilot Studio](https://copilotstudio.microsoft.com/) orientado a brindar **asistencia administrativa básica**.  
El objetivo fue aprender a crear **agentes inteligentes** que apoyen en la gestión de trámites internos, consultas frecuentes y organización de procesos, sin reemplazar la intervención directa del personal administrativo.

---

## Objetivo del Proyecto
- Diseñar un **agente de IA** que interactúe de manera clara y eficiente con los usuarios.  
- Permitir que el agente proporcione **información general sobre trámites administrativos** y procesos internos.  
- Integrar **acciones automáticas** como el envío de correos con instrucciones o la generación de formatos en Excel.  

---

## Funcionalidades del Agente
- **Preguntas guiadas**: El agente solicita datos básicos como nombre, documento, área y tipo de trámite.  
- **Orientación en procesos**: Explica cómo solicitar constancias, permisos, certificaciones o actualizaciones de datos.  
- **Gestión de solicitudes frecuentes**: Ofrece respuestas rápidas sobre horarios de atención, correos de contacto y requisitos documentales.  
- **Acciones automáticas (Flujo)**:  
  - Enviar un correo con los pasos del trámite.  
  - Generar un archivo con la información solicitada.  



## Pasos para la Creación

1. **Creación del Agente**  
   - Se utilizó Copilot Studio para crear el agente **“Asistente Administrativo”**.  
   - Se configuraron intenciones para reconocer solicitudes como “¿cómo pido una constancia laboral?” o “quiero actualizar mis datos”.
  
     <img width="1131" height="658" alt="image" src="https://github.com/user-attachments/assets/c43b2949-54c2-4a85-9110-f9ba6a36f296" />


2. **Diseño del Tema**  
   - Se definieron preguntas guiadas para recopilar información básica del usuario y dirigirlo al proceso adecuado.
  
     <img width="1043" height="360" alt="image" src="https://github.com/user-attachments/assets/4798f0fd-0c66-48c1-a4fc-7b4277ff89e0" />


3. **Base de Conocimiento**  
   - Se creó el archivo [`procesos.txt`] con información sobre trámites administrativos: constancias, permisos, certificaciones y actualizaciones de datos.
<img width="1193" height="185" alt="image" src="https://github.com/user-attachments/assets/a7c99a80-a58b-45b7-9392-8ccc003b8e47" />

4. **Flujos (Acciones Automáticas)**  
   - Se diseñó un flujo para enviar un correo con instrucciones detalladas.  
   - Se configuró la generación de un archivo Excel con los datos del trámite.
  
   - <img width="1190" height="484" alt="image" src="https://github.com/user-attachments/assets/4148c7a0-c5b8-4a5b-a516-c99c052f8d2c" />


5. **Temas**  
   - Se incluyeron temas como “Solicitud de constancia laboral”, “Permisos y vacaciones”, “Actualización de datos personales” y “Certificaciones académicas”.

---

## Tecnologías y Herramientas
- **Microsoft Copilot Studio** – Creación del agente conversacional.  
- **Power Automate (Flujos)** – Automatización de envío de correos y generación de archivos.  
- **GitHub** – Documentación del proyecto.  

---

## Lecciones Aprendidas
- Cómo estructurar un **agente administrativo** con temas y preguntas personalizadas.  
- Uso de **bases de conocimiento** para responder de manera consistente.  
- Integración de **flujos automáticos** para apoyar procesos administrativos reales.  

---

## Próximos Pasos
- Ampliar la base de conocimiento con más trámites administrativos.  
- Integrar APIs externas para validar información en tiempo real.  
- Añadir autenticación para que cada usuario pueda consultar el estado de sus solicitudes.  

