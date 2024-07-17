"""Create cities table

Revision ID: e52908f2027d
Revises: 
Create Date: 2024-07-17 15:32:56.142432

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e52908f2027d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'cities',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('city', sa.String, unique=True),
        sa.Column('views', sa.Integer, default=0)
    )


def downgrade():
    op.drop_table('cities')