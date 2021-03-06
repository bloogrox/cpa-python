"""empty message

Revision ID: 3fd66ae1183
Revises: 4baff6cf1bb
Create Date: 2015-06-10 20:53:13.805063

"""

# revision identifiers, used by Alembic.
revision = '3fd66ae1183'
down_revision = '4baff6cf1bb'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('platform',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Enum('iOS', 'Android', name='platform_types'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('platform')
    ### end Alembic commands ###
