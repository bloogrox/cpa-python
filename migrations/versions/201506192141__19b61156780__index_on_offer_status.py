"""index on offer.status

Revision ID: 19b61156780
Revises: 204f620bda
Create Date: 2015-06-19 21:41:46.469805

"""

# revision identifiers, used by Alembic.
revision = '19b61156780'
down_revision = '204f620bda'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_offer_status'), 'offer', ['status'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_offer_status'), table_name='offer')
    ### end Alembic commands ###
