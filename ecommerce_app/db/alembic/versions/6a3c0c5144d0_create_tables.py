"""Create tables

Revision ID: 6a3c0c5144d0
Revises: f2dfdf2f4409
Create Date: 2023-10-07 23:27:11.249821

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a3c0c5144d0'
down_revision: Union[str, None] = 'f2dfdf2f4409'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('categories',
    sa.Column('category_id', sa.INTEGER(), server_default=sa.text("nextval('categories_category_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('category_id', name='categories_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('products',
    sa.Column('product_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('price', sa.REAL(), autoincrement=False, nullable=False),
    sa.Column('category_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.category_id'], name='products_category_id_fkey'),
    sa.PrimaryKeyConstraint('product_id', name='products_pkey')
    )
    op.create_table('sales',
    sa.Column('sale_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('product_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('quantity', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('sale_date', sa.DATE(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['products.product_id'], name='sales_product_id_fkey'),
    sa.PrimaryKeyConstraint('sale_id', name='sales_pkey')
    )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
