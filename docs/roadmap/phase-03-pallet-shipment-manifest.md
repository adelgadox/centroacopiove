### Fase 3 — Tarima, envío y manifiesto ✅

> Consolidar y producir el documento que habilita el envío.
> Criterios de aceptación: un envío cerrado produce un manifiesto correcto y reproducible; solo cajas `SEALED` en tarimas y solo tarimas `CLOSED` en envíos; despacho congela estados.

#### Backend

| # | Tarea | Descripción | Complejidad | Estado |
|---|-------|-------------|-------------|--------|
| 1 | `Pallet` CRUD + agregar cajas | Agregar cajas `SEALED` por escaneo; transición `OPEN→CLOSED` | 🟡 | ✅ Done |
| 2 | Etiqueta de tarima PDF | QR + conteo/lista de cajas | 🟠 | ✅ Done |
| 3 | `Shipment` CRUD + agregar tarimas | Transición `OPEN→CLOSED→SHIPPED` | 🟡 | ✅ Done |
| 4 | Manifiesto/packing list | WeasyPrint + Jinja2: tarima→cajas anidado + totales + columnas estándar | 🔴 | ✅ Done |
| 5 | Generación de manifiesto encolada en ARQ | Operación cara → siempre asíncrona | 🟠 | ✅ Done |
| 6 | Congelar a SHIPPED | Cajas + tarimas pasan a `SHIPPED` al despachar | 🟡 | ✅ Done |

#### Frontend

| # | Tarea | Descripción | Complejidad | Estado |
|---|-------|-------------|-------------|--------|
| 7 | Tablero de paletizado | Escaneo de cajas a tarima + vista de estado | 🟠 | ✅ Done |
| 8 | Consolidación de envío | Agregar tarimas al envío + generar manifiesto | 🟠 | ✅ Done |
| 9 | Descarga de manifiesto + etiquetas de tarima | UI de descarga con estado de generación | 🟢 | ✅ Done |
