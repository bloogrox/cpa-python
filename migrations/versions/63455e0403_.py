"""empty message

Revision ID: 63455e0403
Revises: 1eff6b068e
Create Date: 2015-06-09 17:48:24.114860

"""

# revision identifiers, used by Alembic.
revision = '63455e0403'
down_revision = '1eff6b068e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('offer', sa.Column('status', sa.String(length=10), nullable=True))
    op.alter_column('offer', 'payout',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('offer', 'payout',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=True)
    op.drop_column('offer', 'status')
    ### end Alembic commands ###
