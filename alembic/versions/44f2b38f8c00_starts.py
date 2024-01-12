"""starts

Revision ID: 44f2b38f8c00
Revises: aba2b9d7c794
Create Date: 2024-01-11 00:22:42.401160

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '44f2b38f8c00'
down_revision: Union[str, None] = 'aba2b9d7c794'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
