"""VIP

Revision ID: 7a510014e598
Revises: fd7830ba0d52
Create Date: 2024-04-04 15:58:03.390264

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7a510014e598'
down_revision: Union[str, None] = 'fd7830ba0d52'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('business', sa.Column('is_vip', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('business', 'is_vip')
    # ### end Alembic commands ###