"""hist date5

Revision ID: 199b6a2d9774
Revises: fcb485b8391c
Create Date: 2024-01-21 01:35:18.921964

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '199b6a2d9774'
down_revision: Union[str, None] = 'fcb485b8391c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sub_history', sa.Column('date_created', sa.Date(), server_default=sa.text('now()'), nullable=False))
    op.drop_column('sub_history', 'date_updated')
    op.add_column('sub_price', sa.Column('date_created', sa.Date(), server_default=sa.text('now()'), nullable=False))
    op.drop_column('sub_price', 'date_updated')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sub_price', sa.Column('date_updated', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False))
    op.drop_column('sub_price', 'date_created')
    op.add_column('sub_history', sa.Column('date_updated', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False))
    op.drop_column('sub_history', 'date_created')
    # ### end Alembic commands ###