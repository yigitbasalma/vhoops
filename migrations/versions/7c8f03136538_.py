"""empty message

Revision ID: 7c8f03136538
Revises: 286f44efa1e1
Create Date: 2021-02-10 21:29:37.253354

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7c8f03136538'
down_revision = '286f44efa1e1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('alerts', sa.Column('alert_count', sa.Integer(), server_default='1', nullable=True))
    op.drop_column('alerts', 'count')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('alerts', sa.Column('count', mysql.INTEGER(display_width=11), server_default=sa.text("'1'"), autoincrement=False, nullable=True))
    op.drop_column('alerts', 'alert_count')
    # ### end Alembic commands ###
