"""valid id and cert

Revision ID: f5d2910e9bd3
Revises: 9526c05e8f8c
Create Date: 2024-01-30 15:29:45.639105

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f5d2910e9bd3'
down_revision: Union[str, None] = '9526c05e8f8c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
