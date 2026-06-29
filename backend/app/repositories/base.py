from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy import Select
from sqlalchemy.orm import Session

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """Abstract base for all repositories."""

    def __init__(self, db: Session) -> None:
        self.db = db


class TenantRepository(BaseRepository[T]):
    """Base for domain repositories that enforce center_id scoping.

    Every query must go through scoped() — this is the anti-cross-tenant-leak guard.
    national_admin passes center_id=None to bypass filtering and see all centers.
    """

    def scoped(self, stmt: Select, center_id: UUID | None) -> Select:
        if center_id is None:
            return stmt
        return stmt.where(self.model.center_id == center_id)  # type: ignore[attr-defined]
