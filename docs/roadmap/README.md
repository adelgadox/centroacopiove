# Acopio — Roadmap

## Progreso general

```mermaid
pie title Tareas completadas (52 tareas)
    "Listas" : 32
    "Pendientes" : 20
```

| Fase | Nombre | Listas | Pendientes | Progreso |
|------|--------|-------:|-----------:|----------|
| 0 | [Scaffolding + multi-tenant + roles](phase-00-scaffolding.md) | 9 | 5 | 🟡 64% |
| 1 | [Catálogo e intake con validaciones](phase-01-catalog-intake.md) | 8 | 0 | ✅ 100% |
| 2 | [Caja homogénea, QR y etiqueta](phase-02-box-qr-label.md) | 6 | 0 | ✅ 100% |
| 3 | [Tarima, envío y manifiesto](phase-03-pallet-shipment-manifest.md) | 9 | 0 | ✅ 100% |
| 4 | [Panel agregado nacional + endurecimiento + OTP](phase-04-national-dashboard-hardening.md) | 0 | 15 | ⬜ 0% |
| **Total** | | **32** | **20** | **🟡 62%** |

> Las tareas 1 y 2 de Fase 0 (Envs + aplicar migración) requieren acción manual con DB activa.

---

## Dependencias entre fases

```
Fase 0 ─► Fase 1 ─► Fase 2 ─► Fase 3 ─► Fase 4
                └──────────────► (panel agregado usa datos de 1–3)
```

Fase 4 (offline/PWA y endurecimiento) puede solaparse con 2–3 según prioridad mediática.

---

## Notas de edición

Cada fase vive en su propio archivo bajo `docs/roadmap/`. Al editar:

- Actualiza el archivo de fase con el cambio de tarea (✅ Done / 🟡 In progress / ⬜ Pendiente).
- Actualiza los totales y el pie chart en este índice al completar o agregar tareas.
- Nuevas fases: archivo `phase-NN-<slug>.md` + fila en la tabla de arriba.
