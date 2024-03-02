"""search suggest

Revision ID: b51ad4bd6d83
Revises: d770a2d4e56a
Create Date: 2024-02-19 11:12:49.516177

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b51ad4bd6d83'
down_revision: Union[str, None] = 'd770a2d4e56a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('search_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('search', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_search_history_id'), 'search_history', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_search_history_id'), table_name='search_history')
    op.drop_table('search_history')
    # ### end Alembic commands ###