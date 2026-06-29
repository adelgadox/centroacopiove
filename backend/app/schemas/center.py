from datetime import datetime
from uuid import UUID

from app.schemas._base import StrictModel, StrictORMModel


class CenterCreate(StrictModel):
    name: str
    address: str | None = None
    contact_name: str | None = None
    contact_email: str | None = None
    contact_phone: str | None = None


class CenterUpdate(StrictModel):
    name: str | None = None
    address: str | None = None
    contact_name: str | None = None
    contact_email: str | None = None
    contact_phone: str | None = None
    is_active: bool | None = None


class CenterOut(StrictORMModel):
    id: UUID
    name: str
    address: str | None
    contact_name: str | None
    contact_email: str | None
    contact_phone: str | None
    is_active: bool
    created_at: datetime
