from datetime import datetime
from uuid import UUID

from app.schemas._base import StrictModel, StrictORMModel
from app.schemas.pallet import PalletDetailOut


class ShipmentCreate(StrictModel):
    destination: str = "Venezuela"
    carrier: str | None = None
    reference: str | None = None
    notes: str | None = None


class ShipmentOut(StrictORMModel):
    id: UUID
    center_id: UUID | None
    destination: str
    carrier: str | None
    reference: str | None
    status: str
    notes: str | None
    closed_at: datetime | None
    shipped_at: datetime | None
    created_at: datetime


class ShipmentDetailOut(StrictModel):
    id: UUID
    center_id: UUID | None
    destination: str
    carrier: str | None
    reference: str | None
    status: str
    notes: str | None
    closed_at: datetime | None
    shipped_at: datetime | None
    created_at: datetime
    pallets: list[PalletDetailOut]
