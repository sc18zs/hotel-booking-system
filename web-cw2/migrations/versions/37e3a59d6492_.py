"""empty message

Revision ID: 37e3a59d6492
Revises: 1da6f4ecaa6f
Create Date: 2021-01-02 23:24:19.833890

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37e3a59d6492'
down_revision = '1da6f4ecaa6f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.drop_column('arrive_time')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('arrive_time', sa.TIME(), nullable=True))

    # ### end Alembic commands ###