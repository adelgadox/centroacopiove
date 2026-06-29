"""acopio core schema: centers, product_types, intakes, boxes, pallets, shipments + events

Revision ID: 002_acopio_core_schema
Revises: 001_add_login_lockout
Create Date: 2026-06-29

Notas de diseño
---------------
- Multi-tenant "pool / row-level": una sola DB, `center_id` discrimina por centro.
  El admin nacional consulta sin filtro (center_id NULL en su usuario).
- Se usan columnas String + CHECK constraints en vez de ENUM nativos de Postgres,
  para poder evolucionar los estados sin ALTER TYPE y por consistencia con el
  uso de String en `users.role` del boilerplate.
- Los UUID de PK se generan en Python (default=uuid.uuid4 en los modelos), igual
  que en el modelo User del boilerplate; por eso no llevan server_default.
- La "caja homogenea" queda garantizada por el propio esquema: una Box referencia
  exactamente un product_type_id y tiene un solo batch y una sola expiry_date.
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = "002_acopio_core_schema"
down_revision = "001_add_login_lockout"
branch_labels = None
depends_on = None

# --- Conjuntos de valores permitidos (fuente unica de verdad para los CHECK) ---
CENTER_ROLES = ("national_admin", "coordinator", "volunteer")
PRODUCT_CATEGORIES = (
    "MEDICINE", "MEDICAL_SUPPLY", "FOOD", "WATER",
    "HYGIENE", "TOOL", "RESCUE_GEAR", "OTHER",
)
BOX_STATUSES = ("DRAFT", "SEALED", "SHIPPED", "REJECTED")
PALLET_STATUSES = ("OPEN", "CLOSED", "SHIPPED")
SHIPMENT_STATUSES = ("OPEN", "CLOSED", "SHIPPED")


def _in(col: str, values) -> str:
    listed = ", ".join(f"'{v}'" for v in values)
    return f"{col} IN ({listed})"


def upgrade() -> None:
    # ------------------------------------------------------------------ centers
    op.create_table(
        "centers",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("address", sa.String(), nullable=True),
        sa.Column("contact_name", sa.String(), nullable=True),
        sa.Column("contact_email", sa.String(), nullable=True),
        sa.Column("contact_phone", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_centers_is_active", "centers", ["is_active"])

    # ------------------------------------------------------ users (ALTER, no recrea)
    # Se agrega la pertenencia a centro y el rol de dominio sin tocar `users.role`
    # del boilerplate (user|admin|superadmin), que sigue gobernando el gating de
    # plataforma. national_admin lleva center_id NULL (ve todos los centros).
    op.add_column("users", sa.Column("center_id", UUID(as_uuid=True), nullable=True))
    op.add_column("users", sa.Column("center_role", sa.String(), nullable=True))
    op.create_foreign_key(
        "fk_users_center_id", "users", "centers",
        ["center_id"], ["id"], ondelete="SET NULL",
    )
    op.create_check_constraint(
        "ck_users_center_role", "users",
        f"center_role IS NULL OR {_in('center_role', CENTER_ROLES)}",
    )
    op.create_index("ix_users_center_id", "users", ["center_id"])

    # ----------------------------------------------------------- product_types
    op.create_table(
        "product_types",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("category", sa.String(), nullable=False),
        sa.Column("display_name", sa.String(), nullable=False),
        sa.Column("unspsc_code", sa.String(), nullable=True),
        sa.Column("inn_name", sa.String(), nullable=True),       # nombre generico / INN
        sa.Column("brand", sa.String(), nullable=True),
        sa.Column("strength", sa.String(), nullable=True),       # atributo discriminante (500mg)
        sa.Column("form", sa.String(), nullable=True),           # tableta, jarabe, ...
        sa.Column("gtin", sa.String(), nullable=True),           # codigo de barras (opcional)
        sa.Column("default_unit", sa.String(), nullable=True),
        sa.Column("is_controlled", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        # Override opcional de la vida util minima; NULL = usa el default por categoria
        sa.Column("min_shelf_life_days", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(_in("category", PRODUCT_CATEGORIES), name="ck_product_types_category"),
    )
    op.create_index("ix_product_types_category", "product_types", ["category"])
    op.create_index("ix_product_types_gtin", "product_types", ["gtin"])
    op.create_index("ix_product_types_inn_name", "product_types", ["inn_name"])
    op.create_index("ix_product_types_unspsc_code", "product_types", ["unspsc_code"])

    # --------------------------------------------------------------- shipments
    op.create_table(
        "shipments",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        # NULL = consolidacion nacional (admin nacional); de lo contrario, del centro
        sa.Column("center_id", UUID(as_uuid=True), sa.ForeignKey("centers.id", ondelete="SET NULL"), nullable=True),
        sa.Column("destination", sa.String(), nullable=False, server_default=sa.text("'Venezuela'")),
        sa.Column("carrier", sa.String(), nullable=True),
        sa.Column("reference", sa.String(), nullable=True),       # vuelo / guia
        sa.Column("status", sa.String(), nullable=False, server_default=sa.text("'OPEN'")),
        sa.Column("notes", sa.String(), nullable=True),
        sa.Column("closed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("shipped_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(_in("status", SHIPMENT_STATUSES), name="ck_shipments_status"),
    )
    op.create_index("ix_shipments_center_id", "shipments", ["center_id"])
    op.create_index("ix_shipments_status", "shipments", ["status"])

    # ----------------------------------------------------------------- pallets
    op.create_table(
        "pallets",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("code", sa.String(), nullable=False),                 # va en el QR
        sa.Column("center_id", UUID(as_uuid=True), sa.ForeignKey("centers.id", ondelete="CASCADE"), nullable=False),
        sa.Column("shipment_id", UUID(as_uuid=True), sa.ForeignKey("shipments.id", ondelete="SET NULL"), nullable=True),
        sa.Column("status", sa.String(), nullable=False, server_default=sa.text("'OPEN'")),
        sa.Column("notes", sa.String(), nullable=True),
        sa.Column("closed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(_in("status", PALLET_STATUSES), name="ck_pallets_status"),
    )
    op.create_index("ix_pallets_code", "pallets", ["code"], unique=True)
    op.create_index("ix_pallets_center_id", "pallets", ["center_id"])
    op.create_index("ix_pallets_shipment_id", "pallets", ["shipment_id"])
    op.create_index("ix_pallets_center_status", "pallets", ["center_id", "status"])

    # ----------------------------------------------------------------- intakes
    op.create_table(
        "intakes",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("center_id", UUID(as_uuid=True), sa.ForeignKey("centers.id", ondelete="CASCADE"), nullable=False),
        sa.Column("received_by_user_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("donante_libre", sa.String(), nullable=True),   # texto libre opcional, sin PII
        sa.Column("notes", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_intakes_center_id", "intakes", ["center_id"])

    # ------------------------------------------------------------------- boxes
    op.create_table(
        "boxes",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("code", sa.String(), nullable=False),                 # va en el QR
        sa.Column("center_id", UUID(as_uuid=True), sa.ForeignKey("centers.id", ondelete="CASCADE"), nullable=False),
        sa.Column("product_type_id", UUID(as_uuid=True), sa.ForeignKey("product_types.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("intake_id", UUID(as_uuid=True), sa.ForeignKey("intakes.id", ondelete="SET NULL"), nullable=True),
        sa.Column("pallet_id", UUID(as_uuid=True), sa.ForeignKey("pallets.id", ondelete="SET NULL"), nullable=True),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("unit", sa.String(), nullable=False),
        sa.Column("batch", sa.String(), nullable=True),                 # lote
        sa.Column("expiry_date", sa.Date(), nullable=True),
        sa.Column("weight_kg", sa.Numeric(10, 3), nullable=True),
        sa.Column("status", sa.String(), nullable=False, server_default=sa.text("'DRAFT'")),
        sa.Column("reject_reason", sa.String(), nullable=True),
        sa.Column("sealed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(_in("status", BOX_STATUSES), name="ck_boxes_status"),
        sa.CheckConstraint("quantity > 0", name="ck_boxes_quantity_positive"),
    )
    op.create_index("ix_boxes_code", "boxes", ["code"], unique=True)
    op.create_index("ix_boxes_center_id", "boxes", ["center_id"])
    op.create_index("ix_boxes_product_type_id", "boxes", ["product_type_id"])
    op.create_index("ix_boxes_pallet_id", "boxes", ["pallet_id"])
    op.create_index("ix_boxes_status", "boxes", ["status"])
    op.create_index("ix_boxes_center_status", "boxes", ["center_id", "status"])

    # ----------------------------------------------------- eventos / auditoria
    for entity, fk_table in (("box", "boxes"), ("pallet", "pallets"), ("shipment", "shipments")):
        op.create_table(
            f"{entity}_events",
            sa.Column("id", UUID(as_uuid=True), primary_key=True),
            sa.Column(f"{entity}_id", UUID(as_uuid=True), sa.ForeignKey(f"{fk_table}.id", ondelete="CASCADE"), nullable=False),
            sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
            sa.Column("from_status", sa.String(), nullable=True),
            sa.Column("to_status", sa.String(), nullable=False),
            sa.Column("note", sa.String(), nullable=True),
            sa.Column("ts", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        )
        op.create_index(f"ix_{entity}_events_{entity}_id", f"{entity}_events", [f"{entity}_id"])


def downgrade() -> None:
    for entity in ("shipment", "pallet", "box"):
        op.drop_index(f"ix_{entity}_events_{entity}_id", table_name=f"{entity}_events")
        op.drop_table(f"{entity}_events")

    for idx in (
        "ix_boxes_center_status", "ix_boxes_status", "ix_boxes_pallet_id",
        "ix_boxes_product_type_id", "ix_boxes_center_id", "ix_boxes_code",
    ):
        op.drop_index(idx, table_name="boxes")
    op.drop_table("boxes")

    op.drop_index("ix_intakes_center_id", table_name="intakes")
    op.drop_table("intakes")

    for idx in (
        "ix_pallets_center_status", "ix_pallets_shipment_id",
        "ix_pallets_center_id", "ix_pallets_code",
    ):
        op.drop_index(idx, table_name="pallets")
    op.drop_table("pallets")

    op.drop_index("ix_shipments_status", table_name="shipments")
    op.drop_index("ix_shipments_center_id", table_name="shipments")
    op.drop_table("shipments")

    for idx in (
        "ix_product_types_unspsc_code", "ix_product_types_inn_name",
        "ix_product_types_gtin", "ix_product_types_category",
    ):
        op.drop_index(idx, table_name="product_types")
    op.drop_table("product_types")

    op.drop_index("ix_users_center_id", table_name="users")
    op.drop_constraint("ck_users_center_role", "users", type_="check")
    op.drop_constraint("fk_users_center_id", "users", type_="foreignkey")
    op.drop_column("users", "center_role")
    op.drop_column("users", "center_id")

    op.drop_index("ix_centers_is_active", table_name="centers")
    op.drop_table("centers")
