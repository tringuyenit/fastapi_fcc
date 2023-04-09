"""add last few column to posts table

Revision ID: a60c47665a3c
Revises: 6fd1590b9963
Create Date: 2023-03-28 10:39:37.078508

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a60c47665a3c'
down_revision = '6fd1590b9963'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published",
                                     sa.Boolean,
                                     nullable=False,
                                     server_default="TRUE")
                  )
    op.add_column("posts", sa.Column("created_at",
                                     sa.TIMESTAMP(timezone=True),
                                     nullable=False,
                                     server_default=sa.text("NOW()"))
                  )
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_table("posts", "created_at")
    pass
