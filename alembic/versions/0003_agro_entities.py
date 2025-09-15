"""agro entities: farms, crops, investors, devices, readings

Revision ID: 0003_agro_entities
Revises: 0002_auth_jwt
Create Date: 2025-09-14 00:00:02
"""
from alembic import op
import sqlalchemy as sa


revision = "0003_agro_entities"
down_revision = "0002_auth_jwt"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Farms
    op.create_table(
        "farms",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("owner_id", sa.BigInteger(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("location", sa.String(255), nullable=True),
        sa.Column("hectares", sa.Numeric(10, 2), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_farms_owner_id", "farms", ["owner_id"])

    # Crops
    op.create_table(
        "crops",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("variety", sa.String(120), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
    )

    # Farm <-> Crops (many-to-many)
    op.create_table(
        "farm_crops",
        sa.Column("farm_id", sa.BigInteger(), sa.ForeignKey("farms.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("crop_id", sa.BigInteger(), sa.ForeignKey("crops.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("planted_on", sa.Date(), nullable=True),
        sa.Column("area_hectares", sa.Numeric(10, 2), nullable=True),
    )

    # Investors
    op.create_table(
        "investors",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("email", sa.String(320), nullable=True),
        sa.Column("phone", sa.String(50), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )

    # Farm <-> Investors (many-to-many)
    op.create_table(
        "farm_investors",
        sa.Column("farm_id", sa.BigInteger(), sa.ForeignKey("farms.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("investor_id", sa.BigInteger(), sa.ForeignKey("investors.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("invested_on", sa.Date(), nullable=True),
    )

    # IoT Devices on a farm
    op.create_table(
        "devices",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("farm_id", sa.BigInteger(), sa.ForeignKey("farms.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("kind", sa.String(50), nullable=True),  # sensor, pump, camera, etc.
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_devices_farm_id", "devices", ["farm_id"])

    # Sensor readings
    op.create_table(
        "readings",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("device_id", sa.BigInteger(), sa.ForeignKey("devices.id", ondelete="CASCADE"), nullable=False),
        sa.Column("captured_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("metric", sa.String(50), nullable=False),   # e.g., temperature, moisture
        sa.Column("value", sa.Float(), nullable=False),
        sa.Column("unit", sa.String(20), nullable=True),
    )
    op.create_index("ix_readings_device_id", "readings", ["device_id"])
    op.create_index("ix_readings_captured_at", "readings", ["captured_at"])


def downgrade() -> None:
    op.drop_index("ix_readings_captured_at", table_name="readings")
    op.drop_index("ix_readings_device_id", table_name="readings")
    op.drop_table("readings")

    op.drop_index("ix_devices_farm_id", table_name="devices")
    op.drop_table("devices")

    op.drop_table("farm_investors")
    op.drop_table("investors")

    op.drop_table("farm_crops")
    op.drop_table("crops")

    op.drop_index("ix_farms_owner_id", table_name="farms")
    op.drop_table("farms")
