"""center geo: add country_code and state_name to centers

Revision ID: 003_center_geo
Revises: 002_acopio_core_schema
Create Date: 2026-06-29
"""

import sqlalchemy as sa
from alembic import op

revision = "003_center_geo"
down_revision = "002_acopio_core_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("centers", sa.Column("country_code", sa.String(2), nullable=True))
    op.add_column("centers", sa.Column("state_name", sa.String(), nullable=True))
    op.create_check_constraint(
        "ck_centers_country_code",
        "centers",
        "country_code IS NULL OR country_code ~ '^[A-Z]{2}$'",
    )
    op.create_index("ix_centers_country_code", "centers", ["country_code"])


def downgrade() -> None:
    op.drop_index("ix_centers_country_code", table_name="centers")
    op.drop_constraint("ck_centers_country_code", "centers", type_="check")
    op.drop_column("centers", "state_name")
    op.drop_column("centers", "country_code")
