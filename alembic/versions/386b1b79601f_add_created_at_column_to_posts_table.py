"""add created_at column to posts table

Revision ID: 386b1b79601f
Revises: 0a925bc98f1d
Create Date: 2024-09-28 22:12:44.678739

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '386b1b79601f'
down_revision: Union[str, None] = '0a925bc98f1d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, 
                                    server_default=sa.text('NOW()')))


def downgrade() -> None:
    op.drop_column("posts", "created_at")
