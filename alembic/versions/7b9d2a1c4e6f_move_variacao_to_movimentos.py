"""move_variacao_to_movimentos

Revision ID: 7b9d2a1c4e6f
Revises: 2f4b42f6c9d1
Create Date: 2026-05-14 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7b9d2a1c4e6f"
down_revision: Union[str, Sequence[str], None] = "2f4b42f6c9d1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Move product variation data from produtos to movement item rows."""
    op.add_column("compra_produto", sa.Column("tamanho", sa.String(), nullable=True))
    op.add_column("compra_produto", sa.Column("genero", sa.String(), nullable=True))
    op.add_column("venda_item", sa.Column("tamanho", sa.String(), nullable=True))
    op.add_column("venda_item", sa.Column("genero", sa.String(), nullable=True))

    op.execute("""
        UPDATE compra_produto
        SET tamanho = (
            SELECT produtos.tamanho
            FROM produtos
            WHERE produtos.id = compra_produto.produto_id
        )
        WHERE tamanho IS NULL
    """)
    op.execute("""
        UPDATE compra_produto
        SET genero = (
            SELECT produtos.genero
            FROM produtos
            WHERE produtos.id = compra_produto.produto_id
        )
        WHERE genero IS NULL
    """)
    op.execute("""
        UPDATE venda_item
        SET tamanho = (
            SELECT produtos.tamanho
            FROM produtos
            WHERE produtos.id = venda_item.produto_id
        )
        WHERE tamanho IS NULL
    """)
    op.execute("""
        UPDATE venda_item
        SET genero = (
            SELECT produtos.genero
            FROM produtos
            WHERE produtos.id = venda_item.produto_id
        )
        WHERE genero IS NULL
    """)

    op.drop_column("produtos", "genero")
    op.drop_column("produtos", "tamanho")


def downgrade() -> None:
    """Move one known variation back to produtos before removing movement columns."""
    op.add_column("produtos", sa.Column("tamanho", sa.String(), nullable=True))
    op.add_column("produtos", sa.Column("genero", sa.String(), nullable=True))

    op.execute("""
        UPDATE produtos
        SET tamanho = (
            SELECT compra_produto.tamanho
            FROM compra_produto
            WHERE compra_produto.produto_id = produtos.id
              AND compra_produto.tamanho IS NOT NULL
            LIMIT 1
        )
        WHERE tamanho IS NULL
    """)
    op.execute("""
        UPDATE produtos
        SET genero = (
            SELECT compra_produto.genero
            FROM compra_produto
            WHERE compra_produto.produto_id = produtos.id
              AND compra_produto.genero IS NOT NULL
            LIMIT 1
        )
        WHERE genero IS NULL
    """)

    op.drop_column("venda_item", "genero")
    op.drop_column("venda_item", "tamanho")
    op.drop_column("compra_produto", "genero")
    op.drop_column("compra_produto", "tamanho")
