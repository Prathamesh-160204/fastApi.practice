"""create cab table

Revision ID: 47253f4d3d2f
Revises: 
Create Date: 2024-08-04 16:43:49.404142

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '47253f4d3d2f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('cab',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
                    sa.Column('Car_Name',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('cab')
    pass
