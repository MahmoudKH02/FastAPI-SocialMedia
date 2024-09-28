"""create users table

Revision ID: bcf4d6ec45e6
Revises: 03a609816dba
Create Date: 2024-09-28 21:02:27.547518

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bcf4d6ec45e6'
down_revision: Union[str, None] = '03a609816dba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer()),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False,
                  server_default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email")
    )
    

def downgrade() -> None:
    op.drop_table("users")
