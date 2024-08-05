"""add_content_column_to_post_table

Revision ID: 9a392c8fe1ef
Revises: 603b4a42c0c7
Create Date: 2024-08-05 19:30:21.550677

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a392c8fe1ef'
down_revision: Union[str, None] = '603b4a42c0c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
