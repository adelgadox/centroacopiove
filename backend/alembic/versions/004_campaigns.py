"""campaigns: global event/campaign entity + FK in intakes and shipments

Revision ID: 004_campaigns
Revises: 003_center_geo
Create Date: 2026-06-29

Campaigns are global (no center_id) — created by national_admin so every
center can contribute to the same humanitarian event.
campaign_id is nullable on both intakes and shipments to keep backward
compatibility with data recorded before this migration.
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

revision = "004_campaigns"
down_revision = "003_center_geo"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "campaigns",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("destination_country", sa.String(2), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "destination_country IS NULL OR destination_country ~ '^[A-Z]{2}$'",
            name="ck_campaigns_destination_country",
        ),
    )
    op.create_index("ix_campaigns_is_active", "campaigns", ["is_active"])
    op.create_index("ix_campaigns_destination_country", "campaigns", ["destination_country"])

    op.add_column("intakes", sa.Column("campaign_id", UUID(as_uuid=True), nullable=True))
    op.create_foreign_key(
        "fk_intakes_campaign_id", "intakes", "campaigns",
        ["campaign_id"], ["id"], ondelete="SET NULL",
    )
    op.create_index("ix_intakes_campaign_id", "intakes", ["campaign_id"])

    op.add_column("shipments", sa.Column("campaign_id", UUID(as_uuid=True), nullable=True))
    op.create_foreign_key(
        "fk_shipments_campaign_id", "shipments", "campaigns",
        ["campaign_id"], ["id"], ondelete="SET NULL",
    )
    op.create_index("ix_shipments_campaign_id", "shipments", ["campaign_id"])


def downgrade() -> None:
    op.drop_index("ix_shipments_campaign_id", table_name="shipments")
    op.drop_constraint("fk_shipments_campaign_id", "shipments", type_="foreignkey")
    op.drop_column("shipments", "campaign_id")

    op.drop_index("ix_intakes_campaign_id", table_name="intakes")
    op.drop_constraint("fk_intakes_campaign_id", "intakes", type_="foreignkey")
    op.drop_column("intakes", "campaign_id")

    op.drop_index("ix_campaigns_destination_country", table_name="campaigns")
    op.drop_index("ix_campaigns_is_active", table_name="campaigns")
    op.drop_table("campaigns")
