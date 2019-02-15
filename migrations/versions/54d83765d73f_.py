"""empty message

Revision ID: 54d83765d73f
Revises: ceb494579c6a
Create Date: 2019-02-14 23:05:16.063127

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54d83765d73f'
down_revision = 'ceb494579c6a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sale', sa.Column('deleted', sa.Boolean(), nullable=True))
    op.add_column('sold_product', sa.Column('deleted', sa.Boolean(), nullable=True))
    op.add_column('transaction', sa.Column('deleted', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('seller_commissions', sa.Float(precision=2), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'seller_commissions')
    op.drop_column('transaction', 'deleted')
    op.drop_column('sold_product', 'deleted')
    op.drop_column('sale', 'deleted')
    # ### end Alembic commands ###
