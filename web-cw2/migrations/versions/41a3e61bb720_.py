"""empty message

Revision ID: 41a3e61bb720
Revises: 
Create Date: 2020-12-30 01:51:08.712881

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41a3e61bb720'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('order_user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_orders_order_user_id_users'), 'users', ['order_user_id'], ['user_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_orders_order_user_id_users'), type_='foreignkey')
        batch_op.drop_column('order_user_id')

    # ### end Alembic commands ###