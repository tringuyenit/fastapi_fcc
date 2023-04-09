"""create posts table

Revision ID: 8420f00d053e
Revises: 
Create Date: 2023-03-28 10:03:16.904210

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8420f00d053e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts",
                    sa.Column("id", sa.Integer, nullable=False, primary_key=True),
                    sa.Column("title", sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
