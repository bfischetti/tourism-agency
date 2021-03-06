"""remove promoter table

Revision ID: 7e5f9464c79e
Revises: 6d14b34423c7
Create Date: 2019-02-22 23:23:30.967700

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e5f9464c79e'
down_revision = '6d14b34423c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('promoter')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('promoter',
    sa.Column('promoter_id', sa.INTEGER(), nullable=False),
    sa.Column('email', sa.VARCHAR(length=100), nullable=True),
    sa.Column('first_name', sa.VARCHAR(length=80), nullable=True),
    sa.Column('last_name', sa.VARCHAR(length=80), nullable=True),
    sa.PrimaryKeyConstraint('promoter_id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###
