"""disapproved

Revision ID: 25d997a7d526
Revises: 834eaaaf24f4
Create Date: 2024-01-31 03:03:45.079940

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '25d997a7d526'
down_revision: Union[str, None] = '834eaaaf24f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('certificates', sa.Column('disapproved', sa.Integer(), nullable=True))
    op.add_column('identity', sa.Column('disapproved', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('identity', 'disapproved')
    op.drop_column('certificates', 'disapproved')
    # ### end Alembic commands ###