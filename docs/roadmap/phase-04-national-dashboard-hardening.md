### Fase 4 — Panel agregado nacional y endurecimiento ⬜

> Visibilidad nacional + resiliencia mediática.
> Criterios de aceptación: el agregado refleja el stock real de todos los centros; las rutas públicas resisten picos vía cache; el acceso directo a la URL de Railway queda bloqueado.

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
