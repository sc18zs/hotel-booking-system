"""empty message

Revision ID: 139b8a0c6366
Revises: 2a16dc432819
Create Date: 2021-01-02 20:14:30.636205

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '139b8a0c6366'
down_revision = '2a16dc432819'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('hotels', schema=None) as batch_op:
        batch_op.alter_column('address',
               existing_type=sa.VARCHAR(length=500),
               nullable=False)
        batch_op.alter_column('hotel_star',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('hotels', schema=None) as batch_op:
        batch_op.alter_column('hotel_star',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('address',
               existing_type=sa.VARCHAR(length=500),
               nullable=True)

    # ### end Alembic commands ###