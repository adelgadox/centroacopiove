### Fase 2 — Caja homogénea, QR y etiqueta ⬜

> Sellar cajas homogéneas e imprimirlas.
> Criterios de aceptación: una caja sellada genera QR + etiqueta; escanear el QR abre la ficha pública sin login y sin tocar la DB en caliente (cache hit).

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
