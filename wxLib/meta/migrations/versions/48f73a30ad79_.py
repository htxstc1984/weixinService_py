"""empty message

Revision ID: 48f73a30ad79
Revises: 39561cfbf89c
Create Date: 2014-12-24 10:02:52.218000

"""

# revision identifiers, used by Alembic.
revision = '48f73a30ad79'
down_revision = '39561cfbf89c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('theme_collection_item', schema=None) as batch_op:
        batch_op.add_column(sa.Column('createDate', sa.Unicode(length=30), nullable=True))

    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('theme_collection_item', schema=None) as batch_op:
        batch_op.drop_column('createDate')

    ### end Alembic commands ###
