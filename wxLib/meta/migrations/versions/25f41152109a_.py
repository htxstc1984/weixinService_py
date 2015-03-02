"""empty message

Revision ID: 25f41152109a
Revises: None
Create Date: 2014-12-22 14:01:48.492000

"""

# revision identifiers, used by Alembic.
revision = '25f41152109a'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('theme_collection',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('desc', sa.Text(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('template_dir', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vote_action',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('openid', sa.Unicode(length=30), nullable=False),
    sa.Column('schema_id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.Column('voteDate', sa.Unicode(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vote_schema',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('schemaname', sa.Unicode(length=255), nullable=False),
    sa.Column('desc', sa.Text(), nullable=False),
    sa.Column('fromDate', sa.Unicode(length=30), nullable=False),
    sa.Column('toDate', sa.Unicode(length=30), nullable=False),
    sa.Column('createDate', sa.Unicode(length=30), nullable=False),
    sa.Column('lastDate', sa.Unicode(length=30), nullable=True),
    sa.Column('creator', sa.Unicode(length=255), nullable=False),
    sa.Column('picurl', sa.Unicode(length=255), nullable=True),
    sa.Column('mutiable', sa.Integer(), nullable=False),
    sa.Column('mutimax', sa.Integer(), nullable=False),
    sa.Column('retry', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vote_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('schema_id', sa.Integer(), nullable=False),
    sa.Column('itemtitle', sa.Unicode(length=255), nullable=False),
    sa.Column('itemdesc', sa.Text(), nullable=False),
    sa.Column('picurl', sa.Unicode(length=255), nullable=True),
    sa.ForeignKeyConstraint(['schema_id'], ['vote_schema.id'], ),
    sa.PrimaryKeyConstraint('id', 'schema_id')
    )
    op.create_table('theme_collection_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('collect_id', sa.Integer(), nullable=False),
    sa.Column('openid', sa.Unicode(length=30), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['collect_id'], ['theme_collection.id'], ),
    sa.PrimaryKeyConstraint('id', 'collect_id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('theme_collection_item')
    op.drop_table('vote_item')
    op.drop_table('vote_schema')
    op.drop_table('vote_action')
    op.drop_table('theme_collection')
    ### end Alembic commands ###