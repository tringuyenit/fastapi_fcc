"""add content column to posts table

Revision ID: 5550b1874f37
Revises: 8420f00d053e
Create Date: 2023-03-28 10:12:58.426691

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5550b1874f37'
down_revision = '8420f00d053e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
