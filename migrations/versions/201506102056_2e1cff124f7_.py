"""empty message

Revision ID: 2e1cff124f7
Revises: 3fd66ae1183
Create Date: 2015-06-10 20:56:11.980060

"""

# revision identifiers, used by Alembic.
revision = '2e1cff124f7'
down_revision = '3fd66ae1183'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('app', sa.Column('platform_id', sa.Integer(), nullable=True))
    op.create_unique_constraint('_app_id_platform_id_uc', 'app', ['app_id', 'platform_id'])
    op.create_foreign_key(None, 'app', 'platform', ['platform_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'app', type_='foreignkey')
    op.drop_constraint('_app_id_platform_id_uc', 'app', type_='unique')
    op.drop_column('app', 'platform_id')
    ### end Alembic commands ###