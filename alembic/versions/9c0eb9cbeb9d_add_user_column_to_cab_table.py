"""add user column to cab table

Revision ID: 9c0eb9cbeb9d
Revises: 47253f4d3d2f
Create Date: 2024-08-04 17:07:40.833472

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c0eb9cbeb9d'
down_revision: Union[str, None] = '47253f4d3d2f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('cab',sa.Column('User',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('cab','User')
    pass
