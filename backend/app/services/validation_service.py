"""Business rules for intake validation (WHO Guidelines for Medicine Donations, 3rd ed.).

All rules live here — never in routers or repositories.
"""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING, Any

from app.schemas.intake import BoxDraft

if TYPE_CHECKING:
    from app.models.product_type import ProductType

_DEFAULT_SHELF_LIFE: dict[str, int] = {
    "MEDICINE": 365,
    "FOOD": 180,
    "WATER": 180,
    "MEDICAL_SUPPLY": 0,
    "HYGIENE": 0,
    "TOOL": 0,
    "RESCUE_GEAR": 0,
    "OTHER": 0,
}

_MEDICINE_REQUIRED_FIELDS = ("inn_name", "form", "strength")


def validate_box(box: BoxDraft, product_type: ProductType | Any, capture_date: date) -> str | None:
    """Returns a reject_reason string if the box should be REJECTED, else None."""

    # Controlled substances: always blocked
    if product_type.is_controlled:
        return "Producto controlado: no se acepta en centros de acopio."

    min_days = product_type.min_shelf_life_days or _DEFAULT_SHELF_LIFE.get(product_type.category, 0)

    if min_days > 0:
        if not box.expiry_date:
            return f"Fecha de caducidad requerida para categoría {product_type.category}."
        remaining = (box.expiry_date - capture_date).days
        if remaining < min_days:
            return (
                f"Vida útil insuficiente: {remaining} días restantes, "
                f"mínimo requerido {min_days} días."
            )

    # Medicine-specific required fields on the ProductType
    if product_type.category == "MEDICINE":
        missing = [f for f in _MEDICINE_REQUIRED_FIELDS if not getattr(product_type, f)]
        if missing:
            return f"Campos obligatorios faltantes en el tipo de producto: {', '.join(missing)}."
        if not box.batch:
            return "Número de lote (batch) obligatorio para medicamentos."

    return None
