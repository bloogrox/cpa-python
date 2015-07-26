"""empty message

Revision ID: 4baff6cf1bb
Revises: 490176a9d74
Create Date: 2015-06-10 20:45:19.650709

"""

# revision identifiers, used by Alembic.
revision = '4baff6cf1bb'
down_revision = '490176a9d74'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('offer', sa.Column('app_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'offer', 'app', ['app_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'offer', type_='foreignkey')
    op.drop_column('offer', 'app_id')
    ### end Alembic commands ###
