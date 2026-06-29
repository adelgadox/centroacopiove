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

#### OTP / Autenticación en dos pasos (2FA)

| # | Tarea | Descripción | Complejidad | Estado |
|---|-------|-------------|-------------|--------|
| 10 | Activar capa `pyotp` | Uncomment `pyotp==2.9.0` en `requirements.txt`; aplicar la capa opcional del boilerplate | 🟢 | ⬜ Pendiente |
| 11 | Endpoints TOTP backend | `POST /v1/auth/totp/setup` (genera secret + QR), `POST /v1/auth/totp/verify` (activa), `POST /v1/auth/totp/disable` | 🟠 | ⬜ Pendiente |
| 12 | Columnas en `users` (migración `004_users_totp`) | `totp_secret` (Fernet-encrypted), `totp_enabled`, `totp_backup_codes` (hashed) | 🟡 | ⬜ Pendiente |
| 13 | Guard en login flow | Si `totp_enabled`, el login devuelve `requires_totp: true`; el cliente envía el código TOTP en un segundo paso antes de recibir el JWT | 🟠 | ⬜ Pendiente |
| 14 | UI de configuración OTP | Pantalla en `/dashboard/settings/security`: mostrar QR para escanear con app (Google Auth, Authy), campo de verificación, opción de desactivar, mostrar códigos de recuperación | 🟠 | ⬜ Pendiente |
| 15 | UI del segundo factor en login | Pantalla intermedia que pide el código de 6 dígitos (o un código de recuperación) cuando `requires_totp: true` | 🟡 | ⬜ Pendiente |

> **Nota de seguridad:** el `totp_secret` se almacena cifrado con Fernet (ya disponible en `app.utils.crypto`). Los códigos de recuperación se generan una vez, se muestran al usuario y se almacenan hasheados (bcrypt). El OTP es opcional por usuario; coordinadores y voluntarios pueden activarlo voluntariamente. El `national_admin` debería tenerlo obligatorio (enforce en middleware).
