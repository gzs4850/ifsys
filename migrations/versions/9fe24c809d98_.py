"""empty message

Revision ID: 9fe24c809d98
Revises: 06ed1926db7e
Create Date: 2017-08-17 09:04:02.652000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9fe24c809d98'
down_revision = '06ed1926db7e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('avl_dept',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dept_code', sa.String(length=64), nullable=False),
    sa.Column('dept_name', sa.String(length=32), nullable=False),
    sa.Column('status', sa.String(length=10), nullable=True),
    sa.Column('ts', sa.DateTime(), nullable=True),
    sa.Column('useage', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column(u'auto_result', sa.Column('diff', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column(u'auto_result', 'diff')
    op.drop_table('avl_dept')
    # ### end Alembic commands ###
