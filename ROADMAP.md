# Roadmap — Acopio

> App web multi-centro para estandarizar el registro de donaciones en especie y
> generar manifiestos de envío humanitario hacia Venezuela.
> Fases detalladas en `docs/roadmap/`.

## Leyenda de complejidad

| Icono | Significado |
|-------|-------------|
| 🔴 | Alta complejidad |
| 🟠 | Media-alta complejidad |
| 🟡 | Media complejidad |
| 🟢 | Baja complejidad |

## Leyenda de estado

| Icono | Significado |
|-------|-------------|
| ✅ | Listo |
| 🟡 | En progreso |
| ⬜ | Pendiente |

---

### Fase 0 — Scaffolding, multi-tenant y roles ⬜

> Base ejecutable con aislamiento por centro y roles de dominio.

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

---

### Fase 1 — Catálogo e intake con validaciones ⬜

> Registrar donaciones a nivel de ítem y rechazar lo no apto en la puerta.

#### Datos / catálogo

| # | Tarea | Descripción | Complejidad | Estado |
|---|-------|-------------|-------------|--------|
| 1 | Importar UNSPSC (español) | Semilla de categorías/`unspsc_code` desde el dataset UNDP | 🟠 | ⬜ Pendiente |

#### Backend

| # | Tarea | Descripción | Complejidad | Estado |
|---|-------|-------------|-------------|--------|
| 2 | CRUD de `ProductType` | Admin nacional mantiene el catálogo maestro | 🟡 | ⬜ Pendiente |
| 3 | Búsqueda de `ProductType` | Por nombre/INN/GTIN/categoría; base para autocompletado | 🟡 | ⬜ Pendiente |
| 4 | Integración Open Food Facts | Lookup por código de barras (alimentos) → prefill de `ProductType` | 🟠 | ⬜ Pendiente |
| 5 | Endpoint de intake | Crea `Intake` + `Box(DRAFT)` con los ítems recibidos | 🟡 | ⬜ Pendiente |
| 6 | Servicio de validación | Vida útil (≥365 med / ≥180 food), campos obligatorios, bloqueo `is_controlled` | 🔴 | ⬜ Pendiente |

#### Frontend

| # | Tarea | Descripción | Complejidad | Estado |
|---|-------|-------------|-------------|--------|
| 7 | Pantalla de intake mobile-first | Escaneo de código de barras + autocompletado de producto | 🔴 | ⬜ Pendiente |
| 8 | Indicador visual de REJECTED | Mostrar `reject_reason` claramente en la UI | 🟢 | ⬜ Pendiente |

---

### Fase 2 — Caja homogénea, QR y etiqueta ⬜

> Sellar cajas homogéneas e imprimirlas.

#### Backend

| # | Tarea | Descripción | Complejidad | Estado |
|---|-------|-------------|-------------|--------|
| 1 | `Box.code` único + transición DRAFT→SEALED | Genera código único; escribe `BoxEvent` | 🟡 | ⬜ Pendiente |
| 2 | Generación de QR | `qrcode[pil]` apuntando a ficha pública `/b/{code}` | 🟢 | ⬜ Pendiente |
| 3 | Etiqueta de caja PDF A4 multi-etiqueta | ReportLab; endpoint autenticado + rate-limited | 🟠 | ⬜ Pendiente |
| 4 | Ficha pública de caja | Sin PII, cacheable en el edge; ruta `/b/{code}` | 🟡 | ⬜ Pendiente |

#### Frontend

| # | Tarea | Descripción | Complejidad | Estado |
|---|-------|-------------|-------------|--------|
| 5 | Flujo de sellado + vista previa de etiquetas | Confirmación de sellado e impresión de hoja A4 | 🟠 | ⬜ Pendiente |

#### Infra

| # | Tarea | Descripción | Complejidad | Estado |
|---|-------|-------------|-------------|--------|
| 6 | Regla de cache Cloudflare/Vercel | Cache de `/b/{code}` y rutas públicas en el edge | 🟡 | ⬜ Pendiente |

---

### Fase 3 — Tarima, envío y manifiesto ⬜

> Consolidar y producir el documento que habilita el envío.

#### Backend

| # | Tarea | Descripción | Complejidad | Estado |
|---|-------|-------------|-------------|--------|
| 1 | `Pallet` CRUD + agregar cajas | Agregar cajas `SEALED` por escaneo; transición `OPEN→CLOSED` | 🟡 | ⬜ Pendiente |
| 2 | Etiqueta de tarima PDF | QR + conteo/lista de cajas | 🟠 | ⬜ Pendiente |
| 3 | `Shipment` CRUD + agregar tarimas | Transición `OPEN→CLOSED→SHIPPED` | 🟡 | ⬜ Pendiente |
| 4 | Manifiesto/packing list | WeasyPrint + Jinja2: tarima→cajas anidado + totales + columnas estándar | 🔴 | ⬜ Pendiente |
| 5 | Generación de manifiesto encolada en ARQ | Operación cara → siempre asíncrona | 🟠 | ⬜ Pendiente |
| 6 | Congelar a SHIPPED | Cajas + tarimas pasan a `SHIPPED` al despachar | 🟡 | ⬜ Pendiente |

#### Frontend

| # | Tarea | Descripción | Complejidad | Estado |
|---|-------|-------------|-------------|--------|
| 7 | Tablero de paletizado | Escaneo de cajas a tarima + vista de estado | 🟠 | ⬜ Pendiente |
| 8 | Consolidación de envío | Agregar tarimas al envío + generar manifiesto | 🟠 | ⬜ Pendiente |
| 9 | Descarga de manifiesto + etiquetas de tarima | UI de descarga con estado de generación | 🟢 | ⬜ Pendiente |

---

### Fase 4 — Panel agregado nacional y endurecimiento ⬜

> Visibilidad nacional + resiliencia mediática.

#### Backend

| # | Tarea | Descripción | Complejidad | Estado |
|---|-------|-------------|-------------|--------|
| 1 | Consultas agregadas | Stock por categoría/INN/strength, por centro y total | 🟠 | ⬜ Pendiente |
| 2 | Endpoint público "qué falta / qué sobra" | Solo lectura, cacheable en edge | 🟡 | ⬜ Pendiente |
| 3 | PWA + captura offline | Sync diferido tolerante a red intermitente | 🔴 | ⬜ Pendiente |

#### Frontend

| # | Tarea | Descripción | Complejidad | Estado |
|---|-------|-------------|-------------|--------|
| 4 | Dashboard nacional (admin) | Agregado visual de stock por categoría y centro | 🟠 | ⬜ Pendiente |
| 5 | Página pública de necesidades | "Qué falta" sin login; cacheable | 🟡 | ⬜ Pendiente |

#### Infra / seguridad

| # | Tarea | Descripción | Complejidad | Estado |
|---|-------|-------------|-------------|--------|
| 6 | Cloudflare-only mode activado | `CLOUDFLARE_ONLY=true`; bloqueo directo a Railway URL | 🟡 | ⬜ Pendiente |
| 7 | WAF + rate limiting afinados | Reglas Cloudflare para rutas críticas | 🟡 | ⬜ Pendiente |
| 8 | Turnstile en formularios públicos | Anti-bot en intake y otros forms públicos | 🟢 | ⬜ Pendiente |
| 9 | Spend caps Vercel + alertas | Anti-EDoS presupuestario | 🟢 | ⬜ Pendiente |

---

### Dependencias entre fases

```
Fase 0 ─► Fase 1 ─► Fase 2 ─► Fase 3 ─► Fase 4
                └──────────────► (panel agregado usa datos de 1–3)
```

Fase 4 (offline/PWA y endurecimiento) puede solaparse con 2–3 según prioridad mediática.
