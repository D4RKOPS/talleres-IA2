# Base de datos

## 1) Modelo entidad-relación (descripción textual)

Diseño coherente con los requerimientos de QuickTask (gestión personal de tareas, usuarios autenticados y recordatorios opcionales). Mantengo la información mínima necesaria sin añadir características no solicitadas.

**Entidades principales**

* **User**

  * Representa al usuario registrado de la aplicación.
  * Atributos relevantes: `id` (UUID), `email`, `password_hash`, `created_at`, `updated_at`.
  * Restricciones: `email` debe ser único.

* **Task**

  * Representa una tarea perteneciente a un usuario.
  * Atributos relevantes: `id` (UUID), `user_id` (FK → User), `title`, `description`, `is_completed` (boolean), `created_at`, `updated_at`, `reminder_at` (nullable).
  * `reminder_at` guarda el instante programado para recordatorio (opcional según requerimiento).
  * Restricciones: cada `Task` pertenece a exactamente un `User` (relación N:1).

**Relaciones**

* **User 1 — N Task**

  * Un usuario puede tener cero o muchas tareas.
  * Una tarea pertenece a exactamente un usuario.
* No se crean entidades extra (por ejemplo `Reminder` por separado) porque los requerimientos describen recordatorios como atributo de la tarea (opcional). Esto reduce complejidad y es coherente con el documento fuente.

**Atributos de auditoría**

* Tanto `User` como `Task` mantienen campos `created_at` y `updated_at` para trazabilidad.

**Índices y consultas objetivo**

* Consultas frecuentes: obtener lista de tareas por usuario, filtrar por `is_completed`, buscar próximas notificaciones por `reminder_at`.
* Se proponen índices sobre `tasks(user_id)`, `tasks(user_id, is_completed)` y `tasks(reminder_at)` para optimizar las consultas de listas y el scheduler de recordatorios.

---

## 2) Esquema SQL compatible con SQLite

> Notas sobre SQLite:
>
> * SQLite no tiene un tipo `BOOLEAN` nativo; se usa `INTEGER` con valores 0/1.
> * Para UUID se usa `TEXT`.
> * `CURRENT_TIMESTAMP` es usado para valores por defecto de fecha/hora.

```sql
PRAGMA foreign_keys = ON;

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,               -- UUID en formato texto
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    updated_at DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP)
);

-- Tabla de tareas
CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,               -- UUID en formato texto
    user_id TEXT NOT NULL,             -- FK hacia users(id)
    title TEXT NOT NULL,
    description TEXT,
    is_completed INTEGER NOT NULL DEFAULT 0,  -- 0 = false, 1 = true
    reminder_at DATETIME,              -- nullable: fecha/hora del recordatorio
    created_at DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    updated_at DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Índices para optimizar consultas frecuentes
CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks (user_id);
CREATE INDEX IF NOT EXISTS idx_tasks_user_completed ON tasks (user_id, is_completed);
CREATE INDEX IF NOT EXISTS idx_tasks_reminder_at ON tasks (reminder_at);

-- (Opcional) trigger para mantener updated_at en tasks al actualizar filas
CREATE TRIGGER IF NOT EXISTS trg_tasks_updated_at
AFTER UPDATE ON tasks
FOR EACH ROW
WHEN NEW.updated_at <= OLD.updated_at
BEGIN
    UPDATE tasks SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Trigger similar para users.updated_at
CREATE TRIGGER IF NOT EXISTS trg_users_updated_at
AFTER UPDATE ON users
FOR EACH ROW
WHEN NEW.updated_at <= OLD.updated_at
BEGIN
    UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
```

**Comentarios sobre el esquema**

* Uso `ON DELETE CASCADE` para `tasks.user_id` de forma que al eliminar un usuario se limpien sus tareas (útil para pruebas y manejo de cuentas).
* Los triggers mantienen `updated_at` en actualizaciones. En SQLite los triggers de ejemplo actualizan `updated_at` si no fue actualizado por la aplicación; alternativamente la capa de persistencia puede responsabilizarse.
* Para ambientes productivos se recomienda usar una columna `version` o `etag` si se necesita control de concurrencia optimista (no incluido porque no figura en requerimientos).

---

# Arquitectura del sistema (lógica)

A continuación describo la **arquitectura lógica en capas** y las comunicaciones entre componentes, manteniendo sólo lo que aparece en requisitos/diagramas previos.

## Capas lógicas

1. **Capa de Presentación (Client / Frontend)**

   * Tecnología sugerida previamente: *React + TypeScript (Vite)*.
   * Responsabilidades:

     * Interfaz de usuario (lista de tareas, formularios de creación/edición, login).
     * Validación de entrada básica.
     * Manejo de estado local y sincronización con el backend.
     * (Opcional) Service Worker / integración con Web Push para notificaciones.

2. **Capa de API / Controladores (Backend – entrada)**

   * Tecnología sugerida: *FastAPI* (ASGI).
   * Responsabilidades:

     * Exponer endpoints REST (o GraphQL) para autenticación y CRUD de tareas.
     * Autorización/Autenticación (validar que `user_id` del token coincide con recursos).
     * Validación de payloads (Pydantic models).
     * Paginación, filtros y sorting en endpoints `GET /tasks`.

3. **Capa de Lógica de Negocio / Servicios**

   * Componentes ejemplo: `AuthService`, `TaskService`.
   * Responsabilidades:

     * Implementar reglas del dominio (crear/editar/marcar completada).
     * Encapsular transacciones y llamadas a la capa de persistencia.
     * Encolar trabajos asíncronos (enviar recordatorio) cuando corresponda.

4. **Capa de Persistencia / Data Access Layer (DAL)**

   * Interfaz con la base de datos SQLite (o Postgres en producción).
   * Responsabilidades:

     * Mapear entidades a tablas (ORM o SQL directo).
     * Ejecutar queries optimizadas (uso de índices).
     * Controlar transacciones.
   * En aplicaciones concurrentes o en producción se recomienda reemplazar SQLite por PostgreSQL; el esquema SQL es compatible pero algunos comportamientos (concurrent writes) difieren.

5. **Capa de Background / Workers (Asíncrona)**

   * Función: ejecutar tareas diferidas y scheduling (ej. enviar recordatorios).
   * Tecnologías posibles: Celery (Python) o alternativas; Redis como broker.
   * Comunicación:

     * La capa de negocio encola jobs en Redis (o tabla de schedule).
     * Worker toma jobs y hace llamadas a proveedores externos (p. ej. FCM o servicio de email).
     * Worker actualiza `tasks.reminder_at` o marca `reminder_sent` si se decide mantener tal campo (en este diseño `reminder_at` en `tasks` es suficiente; el worker puede marcar logs en DB).

6. **Servicios externos**

   * Proveedor de notificaciones (FCM, OneSignal, mail provider).
   * Servicio de identidad externo (opcional, si se habilita OAuth).

## Flujo de comunicación (resumen)

* **Usuario (Browser / Mobile)** ↔ **API (FastAPI)**

  * Comunicación vía HTTPS. Frontend obtiene token/session tras login y luego realiza llamadas CRUD.
* **API** ↔ **DAL / Base de datos (SQLite / Postgres)**

  * Consultas parametrizadas, transacciones, uso de índices. API es stateless.
* **API** → **Queue (Redis)**

  * Para trabajos asíncronos (recordatorios) la API encola jobs con payload mínimo (task_id, user_id, reminder_at).
* **Worker** ↔ **Queue (Redis)**

  * Worker consume jobs, ejecuta envío a proveedor externo y actualiza la BD si es necesario.
* **Worker** → **Proveedor de notificaciones**

  * Llamada HTTP / SDK para entregar push o email.
* **Observabilidad / Logging**

  * API y Worker envían logs y errores a sistemas de monitorización (Sentry/Prometheus) — recomendado, no obligatorio.

## Diagrama lógico (texto)

```
[Frontend React] <--HTTPS--> [API FastAPI] <--SQL--> [SQLite / Postgres]
                                      |
                                      +--> [Redis (cache/queue)]
                                      |           ^
                                      |           |
                                      v           |
                                  [Worker (Celery)] 
                                      |
                                      v
                           [Proveedor de Notificaciones (FCM / Email)]
```

## Consideraciones de coherencia con requisitos

* El modelo relacional (`users` — `tasks`) respeta que cada usuario ve **solo** sus tareas (la capa de negocio / autorización debe filtrar por `user_id` en todas las consultas).
* `reminder_at` es opcional en `tasks` (nullable), que refleja "recordatorios opcionales" del requerimiento.
* El esquema permite listados rápidos por usuario y filtros por estado (`is_completed`), con índices propuestos para objetivos de rendimiento (`lista < 2s`, operaciones CRUD rápidas).
* SQLite es compatible con el SQL provisto; para producción concurrida se recomienda Postgres y mínimos cambios en DDL (tipos y triggers).

---

## Entregables adicionales que puedo proporcionar ahora (elige uno)

* DDL adaptado para **PostgreSQL** (si piensas desplegar en producción).
* Scripts de **migración** (Alembic) y ejemplo de modelo ORM (SQLAlchemy / Pydantic).
* Ejemplos de consultas SQL típicas (listar tareas, próximas notificaciones, marcar completada).
* Diagrama ER visual (PNG / PlantUML ER) generado a partir del modelo.

