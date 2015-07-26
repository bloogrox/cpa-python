"""index on app_id and icon_url nullable

Revision ID: 24d560ccd3e
Revises: 2e1cff124f7
Create Date: 2015-06-11 17:23:08.127846

"""

# revision identifiers, used by Alembic.
revision = '24d560ccd3e'
down_revision = '2e1cff124f7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_app_app_id'), 'app', ['app_id'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_app_app_id'), table_name='app')
    ### end Alembic commands ###
