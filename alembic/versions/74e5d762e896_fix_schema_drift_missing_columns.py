"""fix_schema_drift_missing_columns

Revision ID: 74e5d762e896
Revises: 5bcc0594f3de
Create Date: 2025-12-19 01:03:46.218598

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision = "74e5d762e896"
down_revision = "5bcc0594f3de"
branch_labels = None
depends_on = None


def upgrade():
    # ---------- product_media ----------
    with op.batch_alter_table("product_media") as batch:
        batch.add_column(
            sa.Column("public_id", sa.String(), nullable=True)
        )

    # ---------- payments ----------
    with op.batch_alter_table("payments") as batch:
        batch.add_column(
            sa.Column("provider", sa.String(), nullable=True)
        )

    # ---------- orders ----------
    with op.batch_alter_table("orders") as batch:
        batch.add_column(
            sa.Column("currency", sa.String(), nullable=True)
        )


def downgrade():
    with op.batch_alter_table("product_media") as batch:
        batch.drop_column("public_id")

    with op.batch_alter_table("payments") as batch:
        batch.drop_column("provider")

    with op.batch_alter_table("orders") as batch:
        batch.drop_column("currency")
