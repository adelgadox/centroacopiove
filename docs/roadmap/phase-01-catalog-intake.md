### Fase 1 — Catálogo e intake con validaciones ⬜

> Registrar donaciones a nivel de ítem y rechazar lo no apto en la puerta.
> Criterios de aceptación: un medicamento con <1 año de vida útil o sin lote no se puede sellar; un `is_controlled` se bloquea; alimentos con <6 meses se marcan. Tests de cada regla.

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
