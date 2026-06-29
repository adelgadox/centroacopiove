from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.center import Center
from app.repositories.base import BaseRepository


class CenterRepository(BaseRepository[Center]):

    def __init__(self, db: Session) -> None:
        super().__init__(db)
        self.model = Center

    def find_all(self, active_only: bool = False) -> list[Center]:
        stmt = select(Center)
        if active_only:
            stmt = stmt.where(Center.is_active.is_(True))
        return list(self.db.execute(stmt).scalars().all())

    def find_by_id(self, center_id: UUID) -> Center | None:
        return self.db.get(Center, center_id)

    def save(self, center: Center) -> Center:
        self.db.add(center)
        self.db.commit()
        self.db.refresh(center)
        return center

    def commit(self) -> None:
        self.db.commit()
