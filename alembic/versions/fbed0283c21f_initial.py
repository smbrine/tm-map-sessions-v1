"""initial

Revision ID: fbed0283c21f
Revises: 
Create Date: 2024-06-02 19:16:36.911030

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "fbed0283c21f"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = (
    None
)
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "feature_types",
        sa.Column(
            "id", sa.Integer(), nullable=False
        ),
        sa.Column(
            "name",
            sa.String(length=255),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "sessions",
        sa.Column(
            "user_id",
            sa.BigInteger(),
            nullable=False,
        ),
        sa.Column(
            "id", sa.UUID(), nullable=False
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "features",
        sa.Column(
            "session_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "type_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "name", sa.String(), nullable=True
        ),
        sa.Column(
            "id", sa.UUID(), nullable=False
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["sessions.id"],
        ),
        sa.ForeignKeyConstraint(
            ["type_id"],
            ["feature_types.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_features_type_id"),
        "features",
        ["type_id"],
        unique=False,
    )
    op.create_table(
        "geometries",
        sa.Column(
            "feature_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "id", sa.UUID(), nullable=False
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["feature_id"],
            ["features.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "points",
        sa.Column(
            "geometry_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "latitude",
            sa.Numeric(precision=7, scale=4),
            nullable=False,
        ),
        sa.Column(
            "longitude",
            sa.Numeric(precision=7, scale=4),
            nullable=False,
        ),
        sa.Column(
            "id", sa.UUID(), nullable=False
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["geometry_id"],
            ["geometries.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("points")
    op.drop_table("geometries")
    op.drop_index(
        op.f("ix_features_type_id"),
        table_name="features",
    )
    op.drop_table("features")
    op.drop_table("sessions")
    op.drop_table("feature_types")
    # ### end Alembic commands ###
