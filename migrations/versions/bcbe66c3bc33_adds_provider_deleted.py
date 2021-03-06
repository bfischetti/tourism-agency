"""adds provider deleted

Revision ID: bcbe66c3bc33
Revises: 7e5f9464c79e
Create Date: 2019-05-02 12:23:41.602889

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bcbe66c3bc33'
down_revision = '7e5f9464c79e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('provider', sa.Column('deleted', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('provider', 'deleted')
    # ### end Alembic commands ###
