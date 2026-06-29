### Fase 0 — Scaffolding, multi-tenant y roles ⬜

> Base ejecutable con aislamiento por centro y roles de dominio.
> Criterios de aceptación: un `coordinator` solo ve datos de su `center_id`; el `national_admin` ve todos; ningún endpoint consulta sin `scoped()`. Test de fuga entre centros.

#### Infra y base de datos

| # | Tarea | Descripción | Complejidad | Estado |
|---|-------|-------------|-------------|--------|
| 1 | Envs Railway + Vercel | Configurar variables de entorno: Railway (backend, Postgres, Redis) y Vercel (front) | 🟢 | ⬜ Pendiente |
| 2 | Migración `002_acopio_core_schema` | Aplicar `alembic upgrade head` con el esquema base de dominio | 🟢 | ⬜ Pendiente |

#### Backend

| # | Tarea | Descripción | Complejidad | Estado |
|---|-------|-------------|-------------|--------|
| 3 | Modelos SQLAlchemy | `Center`, `ProductType`, `Intake`, `Box`, `Pallet`, `Shipment`, `*Event` | 🟠 | ⬜ Pendiente |
| 4 | Extender `User` | Agregar `center_id` + `center_role` al modelo y al schema | 🟡 | ⬜ Pendiente |
| 5 | `tenant_scope` dependency | Dependency que devuelve `center_id` del usuario o `None` si es `national_admin` | 🟡 | ⬜ Pendiente |
| 6 | `TenantRepository.scoped()` | Extender `BaseRepository` con filtrado por `center_id` | 🟡 | ⬜ Pendiente |
| 7 | CRUD de `Center` | Endpoints solo para `national_admin`; alta y gestión de centros | 🟡 | ⬜ Pendiente |
| 8 | Alta de usuarios por `coordinator` | Endpoint para que coordinadores inviten voluntarios a su centro | 🟡 | ⬜ Pendiente |

#### Frontend

| # | Tarea | Descripción | Complejidad | Estado |
|---|-------|-------------|-------------|--------|
| 9 | Layout + login NextAuth | Layout base, pantalla de login, sesión con `center_role` | 🟡 | ⬜ Pendiente |
| 10 | Guard de rutas por rol | Middleware que protege rutas según `center_role` | 🟡 | ⬜ Pendiente |
| 11 | Selector de centro (admin nacional) | UI para que `national_admin` cambie el contexto de centro | 🟢 | ⬜ Pendiente |
