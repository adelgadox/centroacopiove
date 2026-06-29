from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.product_type import ProductType
from app.repositories.base import BaseRepository


class ProductTypeRepository(BaseRepository[ProductType]):

    def find_all(self, category: str | None = None) -> list[ProductType]:
        stmt = select(ProductType)
        if category:
            stmt = stmt.where(ProductType.category == category)
        return list(self.db.execute(stmt.order_by(ProductType.display_name)).scalars())

    def search(self, q: str, category: str | None = None) -> list[ProductType]:
        term = f"%{q}%"
        stmt = select(ProductType).where(
            or_(
                ProductType.display_name.ilike(term),
                ProductType.inn_name.ilike(term),
                ProductType.gtin.ilike(term),
                ProductType.unspsc_code.ilike(term),
            )
        )
        if category:
            stmt = stmt.where(ProductType.category == category)
        return list(self.db.execute(stmt.order_by(ProductType.display_name).limit(20)).scalars())

    def find_by_id(self, pt_id: UUID) -> ProductType | None:
        return self.db.get(ProductType, pt_id)

    def find_by_gtin(self, gtin: str) -> ProductType | None:
        return self.db.execute(
            select(ProductType).where(ProductType.gtin == gtin)
        ).scalar_one_or_none()

    def save(self, pt: ProductType) -> ProductType:
        self.db.add(pt)
        self.db.commit()
        self.db.refresh(pt)
        return pt

    def commit(self) -> None:
        self.db.commit()
