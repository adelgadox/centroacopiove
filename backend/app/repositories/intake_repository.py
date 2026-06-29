from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.box import Box
from app.models.intake import Intake
from app.repositories.base import TenantRepository


class IntakeRepository(TenantRepository[Intake]):

    def __init__(self, db: Session) -> None:
        super().__init__(db)
        self.model = Intake

    def find_all(self, center_id: UUID | None) -> list[Intake]:
        stmt = self.scoped(select(Intake), center_id).order_by(Intake.created_at.desc())
        return list(self.db.execute(stmt).scalars())

    def find_by_id(self, intake_id: UUID, center_id: UUID | None) -> Intake | None:
        stmt = self.scoped(
            select(Intake).where(Intake.id == intake_id), center_id
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def save_intake(self, intake: Intake) -> Intake:
        self.db.add(intake)
        self.db.flush()
        return intake

    def save_box(self, box: Box) -> Box:
        self.db.add(box)
        return box

    def commit(self) -> None:
        self.db.commit()

    def boxes_for_intake(self, intake_id: UUID) -> list[Box]:
        stmt = select(Box).where(Box.intake_id == intake_id).order_by(Box.created_at)
        return list(self.db.execute(stmt).scalars())
