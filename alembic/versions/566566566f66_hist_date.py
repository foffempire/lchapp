"""hist date

Revision ID: 566566566f66
Revises: 836968a3320a
Create Date: 2024-01-20 23:25:21.439657

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '566566566f66'
down_revision: Union[str, None] = '836968a3320a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
