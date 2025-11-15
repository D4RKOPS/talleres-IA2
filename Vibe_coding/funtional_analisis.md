# Análisis funcional y técnico — **QuickTask**

> Fuente: especificación de requerimientos subida (Resumen y RF/RNF/CA). 

A continuación entrego un análisis estructurado (funcional + técnico) pensado para orientar diseño, estimación y decisiones de implementación del MVP y próximas iteraciones.

---

# 1. Resumen funcional

* **Propósito:** QuickTask es una app para la gestión sencilla y rápida de tareas personales (crear/editar/eliminar/marcar completadas) con enfoque en simplicidad, velocidad y uso en web y dispositivos móviles (web responsiva). 
* **Usuarios:** usuarios autenticados (correo/contraseña) que ven solo sus tareas; recordatorios son opcionales y pueden entregarse por un servicio externo. 
* **Flujo principal (alto nivel):**

  1. Usuario inicia sesión (o utiliza la app anónima si se permite).
  2. Cliente solicita lista de tareas al API; muestra tareas (pendientes/completas).
  3. Usuario crea/edita/elimina/marca una tarea → cliente envía petición POST/PUT/DELETE/PATCH al API.
  4. API persiste en base de datos; notifica al cliente (respuesta inmediata) y devuelve cambio.
  5. (Opcional) Si existe recordatorio programado, un componente de background agenda notificación en el proveedor push/email/SMS.
* **Criterios de aceptación relevantes:** Crear, editar y marcar completadas deben reflejarse inmediatamente en la vista (CA-01..03). Rendimiento objetivo: lista en <2s; operaciones CRUD <1s. 

---

# 2. Análisis de módulos / componentes (arquitectura propuesta)

Arquitectura tipo *3 capas + servicios externos*, modular y preparada para escalar.

## 2.1 Frontend (Cliente)

* **Responsabilidad:** UI/UX, validación mínima, consumo de API REST/GraphQL, manejo de estado local, experiencia responsive.
* **Componentes internos:**

  * Pantalla de lista (filtros: estado, orden por fecha/título).
  * Formulario de creación/edición.
  * Componente de autenticación (login/register).
  * Módulo de notificaciones en cliente (web push / service worker) — opcional.
* **Requisitos no funcionales atendidos:** RNF-01/02 (render rápido con optimizaciones), RNF-03/04 (usabilidad y responsive). 

## 2.2 Backend (API)

* **Responsabilidad:** lógica de negocio, validación de reglas, autorización/autenticación, persistencia, encolado de trabajo para recordatorios.
* **Funciones principales:**

  * Endpoints CRUD (tareas).
  * Endpoints de autenticación (login/register, refresh tokens si aplica).
  * Filtros/ordenamientos paginados.
  * Job scheduler/worker para recordatorios (si se incluye).
* **Escalabilidad:** API stateless; fácil de replicar detrás de load balancer.

## 2.3 Persistencia (Base de datos)

* **Responsabilidad:** almacenamiento persistente de usuarios, tareas, metadatos (timestamps, estado, reminder datetime).
* **Indice lógico de tablas:** `users`, `tasks` (user_id FK, title, description, status, created_at, updated_at, reminder_at, reminder_sent boolean), `sessions` o `tokens` (si se usa persistencia para refresh tokens).

## 2.4 Cache / Cola de trabajos

* **Cache:** Redis para mejorar latencias de lectura (listas frecuentes) y para rate-limiting/session store.
* **Cola de trabajos:** Redis-backed queue (Celery/RQ/Bull) para tareas asíncronas (enviar recordatorios, enviar email, limpiar logs).

## 2.5 Servicio de notificaciones externo

* **Opciones:** Firebase Cloud Messaging (web + móviles), OneSignal, proveedor de email (SendGrid/Mailgun) o push vía navegador.
* **Rol:** envío de notificaciones cuando el reminder vence; se recomienda delegar a tercero para simplicidad y fiabilidad.

## 2.6 Infra / Ops

* **Contenedores:** Docker para reproducibilidad.
* **CI/CD:** GitHub Actions o GitLab CI para pruebas, build y despliegue.
* **Despliegue:** inicialmente VPS/Platform-as-a-Service (Heroku/Render/DigitalOcean App Platform) por presupuesto; luego orquestador (Kubernetes) si escala.
* **Observabilidad:** logs centralizados (ELK/Cloud provider), métricas (Prometheus/Grafana), errores (Sentry).

---

# 3. Tecnologías recomendadas (por componente) y justificación breve

> Elección diseñada para entregar el MVP rápidamente, con buena experiencia dev, rendimiento y fácil crecimiento.

## Frontend

* **Framework:** **React + TypeScript** (Vite como bundler).

  * *Justificación:* gran ecosistema, rápida adopción, componentes reutilizables, TypeScript aporta seguridad de tipos; Vite arranca extremadamente rápido (mejora experiencia dev).
* **UI / Estilos:** **Tailwind CSS** (rápido para prototipado y responsive).
* **State / data fetching:** **React Query** (o SWR) para caché y sincronización optimista.
* **Build / PWA:** configurar Service Worker (Workbox) para notificaciones web y futuro soporte offline (si se decide).
* **Alternativa ligera:** **SvelteKit** si se quiere footprint aún más pequeño y rendimiento per-component, pero menor ecosistema.

## Backend (API)

* **Principal recomendado:** **FastAPI (Python)** + **Uvicorn / Gunicorn**.

  * *Justificación:* soporte asíncrono nativo, alto rendimiento, tipado con Pydantic que mejora la validación y genera documentación OpenAPI automática (útil para frontend). Mejor elección frente a Flask cuando se espera I/O asíncrono (p. ej. notificaciones, DB async) y se quiere documentación automática.
* **ORM:** **SQLAlchemy (con Alembic para migraciones)** o **Tortoise ORM** si se usa async puro.
* **Alternativa (Node):** **Node.js + NestJS** o **Express + TypeScript** si el equipo prefiere JS/TS en backend; NestJS ofrece estructura y decorators similar a frameworks enterprise.

## Base de datos

* **Producción:** **PostgreSQL**

  * *Justificación:* ACID, índices potentes, JSONB para campos flexibles (si luego se agregan etiquetas/metadata), amplia adopción.
* **Desarrollo / MVP local:** **SQLite** (por simplicidad) o instancia remota gestionada (Heroku Postgres, Supabase).
* **Caching / sessions:** **Redis**.

## Cola / scheduler

* **Worker:** **Celery** (Python) con Redis como broker/ backend de resultados.

  * *Justificación:* maduro y ampliamente usado para jobs/retry/cron; si el equipo usa Node, **BullMQ** es alternativa.

## Autenticación / Seguridad

* **Hashing contraseñas:** **Argon2** o **bcrypt** (Argon2 preferible).
* **Sesiones / tokens:** Cookies seguras con HttpOnly + SameSite o **JWT + refresh tokens** (si se requiere API pública).
* **Transporte:** HTTPS (TLS) obligatorio; HSTS en producción.
* **OAuth/social:** implementar más adelante si se necesita login social.

## Infra & DevOps

* **Contenedorización:** Docker.
* **CI/CD:** GitHub Actions.
* **Despliegue:** Render / DigitalOcean App Platform / Railway para MVP; migrar a EKS/GKE/AKS o Managed Kubernetes si escala.
* **Monitoreo:** Sentry (errores), Prometheus + Grafana (métricas), Loki/ELK para logs.

---

# 4. Riesgos técnicos y mitigaciones

## Riesgo: Ambigüedad sobre multiusuario y recordatorios en MVP

* **Impacto:** afecta diseño de modelo de datos, seguridad y componentes de background.
* **Mitigación:** asumir multiusuario desde inicio (modelo `user_id` en tareas). Implementar feature flag para recordatorios y habilitarlo en iteración posterior. Documentar decisión en backlog. 

## Riesgo: Requerimientos de rendimiento (lista <2s, operaciones <1s)

* **Impacto:** UX mala si no se cumple.
* **Mitigación:** paginación/limit en consultas, índices en DB (index column `user_id`, `status`, `created_at`), usar Redis para cache de listas frecuentemente leídas, optimizaciones en frontend (renderización virtualizada si la lista es muy larga).

## Riesgo: Notificaciones (timing y fiabilidad)

* **Impacto:** usuario no recibe recordatorios.
* **Mitigación:** delegar a proveedor probado (FCM/OneSignal); retry policy en workers; marcar `reminder_sent` y logs de auditoría; permitir reintentos y webhooks de entrega fallida.

## Riesgo: Seguridad (contraseñas, exposición de datos)

* **Mitigación:** Argon2/bcrypt, TLS, validar autorización en cada endpoint (`user_id` vs token), pruebas de penetración básicas, rate-limiting y lockout por intentos fallidos, CORS bien configurado.

## Riesgo: Disponibilidad (99% RNF)

* **Mitigación:** despliegue en infra redundante (managed DB con replicas), health checks, auto-restart de workers, backups diarios y plan de DR.

## Riesgo: Costos / presupuesto limitado

* **Mitigación:** usar servicios PaaS económicos para MVP (Render, Railway), empezar con managed Postgres y Redis pequeños; evitar infra compleja hasta validar uso.

---

# 5. Mapa general de dependencias (diagrama lógico textual)

* **Cliente (React/TS)**

  * depende de → **API REST/GraphQL (FastAPI)**
  * consume → proveedor de autenticación (endpoints auth)
  * opcionalmente registra → **Service Worker / FCM** para web-push

* **API (FastAPI)**

  * depende de → **PostgreSQL** (persistencia)
  * depende de → **Redis** (cache, sessions, broker)
  * envía trabajos a → **Worker (Celery)** usando Redis
  * llama a → **Proveedor de notificaciones externo (FCM / OneSignal / SendGrid)** para enviar recordatorios
  * usa → **Sentry / Logging service** para errores

* **Worker (Celery)**

  * consume de → Redis (cola)
  * usa → PostgreSQL para marcar `reminder_sent`
  * llama a → proveedor de notificaciones

* **CI/CD**

  * GitHub Actions → construye imágenes Docker → despliega a plataforma (Render/K8s)

* **Observabilidad**

  * API/Worker → Sentry (errores)
  * Logs → ELK / Loki
  * Métricas → Prometheus → Grafana

(Visual: Frontend ↔ API ↔ DB; API ↔ Redis; API → Worker → ProviderPush)

---

# 6. Justificación técnica de elecciones (ejemplos puntuales)

## ¿Por qué **FastAPI** en lugar de **Flask**?

* **Asincronía nativa:** FastAPI está diseñado para async/await, lo que ayuda cuando hay IO concurrencia (colas, llamadas a proveedores externos). Flask tradicional es síncrono; añadir async es posible pero menos natural.
* **Validación y tipado:** Pydantic (FastAPI) obliga/ayuda a definir modelos de entrada/salida con validación automática, reduciendo bugs y tiempo en escribir validaciones.
* **Documentación automática:** OpenAPI/Swagger generada automáticamente facilita integración con frontend (contratos) y pruebas manuales.
* **Rendimiento:** en benchmarks, frameworks ASGI como FastAPI + Uvicorn suelen tener mejor rendimiento que Flask+Gunicorn (wsgi) en escenarios IO-bound.
* **Ecosistema:** madurez y buenas prácticas con soporte para middlewares modernos (CORS, autenticación, rate-limiting).
* **Cuando preferir Flask:** si el equipo ya tiene mucha experiencia en Flask y la app es muy simple y síncrona; pero para futuro crecimiento FastAPI reduce deuda técnica.

## ¿Por qué **React + TypeScript** y **Tailwind**?

* **React + TypeScript:** equilibrio entre productividad y mantenimiento; TypeScript reduce bugs en tiempo de desarrollo.
* **Tailwind:** permite iterar UI rápido y obtener responsive sin escribir muchos CSS personalizados (útil con recursos limitados).

## ¿Por qué **PostgreSQL**?

* **Fiabilidad y flexibilidad:** constraints, joins, índices, JSONB si se necesita campos semi-estructurados. Escala vertical y horizontal razonable para esta app.

## ¿Por qué **Redis + Celery**?

* **Redis:** simple, rápido, multiuso (cache + broker + rate-limiting).
* **Celery:** probado en producción para trabajos programados y retries; importante para reminders que deben ejecutarse en tiempos específicos.

---

# 7. Plan mínimo de implementación (roadmap técnico sugerido)

1. **Sprint 0 (Infra + scaffolding):** repositorios, CI, Docker, base de datos gestionada dev, entorno local.
2. **Sprint 1 (Core MVP):** autenticar (email+pass), CRUD tareas, endpoints básicos, frontend lista + formulario, tests unitarios básicos. Cumplir CA-01..03. 
3. **Sprint 2 (Mejoras UX/perf):** filtros/orden, indices DB, caché listados, optimizaciones frontend.
4. **Sprint 3 (Recordatorios — opt):** diseñar tabla `reminders`, worker + cola, integración con proveedor push/email, pruebas end-to-end.
5. **Sprint 4 (Hardening):** SSL, backups, monitorización, políticas de seguridad, staging env.

---

# 8. Checklist de calidad y seguridad antes de lanzamiento

* [ ] Hashing de contraseñas con Argon2/bcrypt y sal.
* [ ] TLS/HTTPS configurado.
* [ ] Pruebas unitarias para endpoints críticos.
* [ ] Pruebas de integración (auth + CRUD).
* [ ] Políticas CORS y CSP configuradas.
* [ ] Backups automáticos de la BD y plan de restores.
* [ ] Logging y alertas configuradas (Sentry + alertas CPU/errores).
* [ ] Rate limiting e implementación de lockout por intentos fallidos.

---

# 9. Resumen ejecutivo (decisiones clave)

* **Stack recomendado para MVP:** React + TypeScript (Vite) en frontend; FastAPI (Python) en backend; PostgreSQL + Redis; Celery para reminders; FCM/OneSignal como proveedor push. Esta combinación entrega velocidad de desarrollo, rendimiento asíncrono y camino claro para escalar, al mismo tiempo que mantiene costes controlables para un MVP. 

---

