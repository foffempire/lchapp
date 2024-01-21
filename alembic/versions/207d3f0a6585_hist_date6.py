"""hist date6

Revision ID: 207d3f0a6585
Revises: 199b6a2d9774
Create Date: 2024-01-21 01:42:21.079416

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '207d3f0a6585'
down_revision: Union[str, None] = '199b6a2d9774'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sub_price', sa.Column('date_updated', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False))
    op.drop_column('sub_price', 'date_created')
    op.alter_column('subscriptions', 'date_created',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.Date(),
               existing_nullable=False,
               existing_server_default=sa.text('now()'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('subscriptions', 'date_created',
               existing_type=sa.Date(),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=False,
               existing_server_default=sa.text('now()'))
    op.add_column('sub_price', sa.Column('date_created', sa.DATE(), server_default=sa.text('now()'), autoincrement=False, nullable=False))
    op.drop_column('sub_price', 'date_updated')
    # ### end Alembic commands ###