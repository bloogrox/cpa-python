"""empty message

Revision ID: dfbbfa65e7
Revises: 3a85cbe62ce
Create Date: 2015-06-08 20:47:55.719441

"""

# revision identifiers, used by Alembic.
revision = 'dfbbfa65e7'
down_revision = '3a85cbe62ce'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('offer_event', sa.Column('created', sa.DateTime(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('offer_event', 'created')
    ### end Alembic commands ###
