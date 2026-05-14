"""add_tamanho_genero_to_produtos

Revision ID: 2f4b42f6c9d1
Revises: 14411d73ef83
Create Date: 2026-05-14 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2f4b42f6c9d1"
down_revision: Union[str, Sequence[str], None] = "14411d73ef83"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("produtos", sa.Column("tamanho", sa.String(), nullable=True))
    op.add_column("produtos", sa.Column("genero", sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("produtos", "genero")
    op.drop_column("produtos", "tamanho")
