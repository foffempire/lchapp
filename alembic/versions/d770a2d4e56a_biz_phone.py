"""biz phone

Revision ID: d770a2d4e56a
Revises: e47980edf8af
Create Date: 2024-02-17 00:31:17.730620

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd770a2d4e56a'
down_revision: Union[str, None] = 'e47980edf8af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('business', sa.Column('phone', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('business', 'phone')
    # ### end Alembic commands ###