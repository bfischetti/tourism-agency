"""empty message

Revision ID: 92b4618d8935
Revises: 
Create Date: 2019-02-02 18:49:16.735450

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92b4618d8935'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('label', sa.String(length=80), nullable=True),
    sa.Column('description', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('category_id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('client',
    sa.Column('client_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('passport_number', sa.String(length=80), nullable=True),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('nationality', sa.String(length=80), nullable=True),
    sa.Column('hotel', sa.String(length=200), nullable=True),
    sa.Column('address', sa.String(length=200), nullable=True),
    sa.Column('room_number', sa.String(length=10), nullable=True),
    sa.Column('contact_number', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('client_id')
    )
    op.create_table('currency',
    sa.Column('currency_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('code', sa.String(length=5), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('exchange', sa.Float(precision=20), nullable=True),
    sa.PrimaryKeyConstraint('currency_id')
    )
    op.create_table('promoter',
    sa.Column('promoter_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('first_name', sa.String(length=80), nullable=True),
    sa.Column('last_name', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('promoter_id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('provider',
    sa.Column('provider_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('url', sa.String(length=200), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('phone', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('provider_id')
    )
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('first_name', sa.String(length=80), nullable=True),
    sa.Column('last_name', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('product',
    sa.Column('product_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('stock_price', sa.Float(precision=2), nullable=True),
    sa.Column('selling_price', sa.Float(precision=2), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('billable', sa.Boolean(), nullable=True),
    sa.Column('provider_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['provider_id'], ['provider.provider_id'], ),
    sa.PrimaryKeyConstraint('product_id')
    )
    op.create_table('sale',
    sa.Column('sale_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('total', sa.Float(precision=2), nullable=True),
    sa.Column('discount', sa.Float(precision=2), nullable=True),
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('promoter_id', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('promoter_commission', sa.Float(precision=2), nullable=True),
    sa.Column('user_commission', sa.Float(precision=2), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['client.client_id'], ),
    sa.ForeignKeyConstraint(['promoter_id'], ['promoter.promoter_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('sale_id')
    )
    op.create_table('sold_product',
    sa.Column('sold_product_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('price', sa.Float(precision=2), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('sale_id', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('transfer', sa.Boolean(), nullable=True),
    sa.Column('payment_pending', sa.Boolean(), nullable=True),
    sa.Column('adults', sa.Integer(), nullable=True),
    sa.Column('children', sa.Integer(), nullable=True),
    sa.Column('babies', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['product.product_id'], ),
    sa.ForeignKeyConstraint(['sale_id'], ['sale.sale_id'], ),
    sa.PrimaryKeyConstraint('sold_product_id')
    )
    op.create_table('transaction',
    sa.Column('transaction_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('amount', sa.Float(precision=2), nullable=True),
    sa.Column('exchange', sa.Float(precision=2), nullable=True),
    sa.Column('method', sa.String(length=20), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('is_expense', sa.Boolean(), nullable=True),
    sa.Column('currency_id', sa.Integer(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('sale_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.category_id'], ),
    sa.ForeignKeyConstraint(['currency_id'], ['currency.currency_id'], ),
    sa.ForeignKeyConstraint(['sale_id'], ['sale.sale_id'], ),
    sa.PrimaryKeyConstraint('transaction_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transaction')
    op.drop_table('sold_product')
    op.drop_table('sale')
    op.drop_table('product')
    op.drop_table('users')
    op.drop_table('provider')
    op.drop_table('promoter')
    op.drop_table('currency')
    op.drop_table('client')
    op.drop_table('category')
    # ### end Alembic commands ###