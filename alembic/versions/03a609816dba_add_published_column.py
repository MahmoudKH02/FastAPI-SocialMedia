"""add published column

Revision ID: 03a609816dba
Revises: f005717808b9
Create Date: 2024-09-28 20:48:58.032967

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '03a609816dba'
down_revision: Union[str, None] = 'f005717808b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published", sa.Boolean, nullable=False, server_default='true'))


def downgrade() -> None:
    op.drop_column("posts", "published")
