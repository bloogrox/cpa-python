"""empty message

Revision ID: 490176a9d74
Revises: 1658ac79433
Create Date: 2015-06-10 20:43:03.016157

"""

# revision identifiers, used by Alembic.
revision = '490176a9d74'
down_revision = '1658ac79433'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('app',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('app_id', sa.String(length=64), nullable=True),
    sa.Column('icon_url', sa.String(length=512), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('app')
    ### end Alembic commands ###