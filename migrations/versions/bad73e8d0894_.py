"""empty message

Revision ID: bad73e8d0894
Revises: 485c025529b8
Create Date: 2018-07-04 17:00:09.520873

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bad73e8d0894'
down_revision = '485c025529b8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('eo_api_env',
    sa.Column('envID', sa.Integer(), nullable=False),
    sa.Column('envName', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('envID')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('eo_api_env')
    # ### end Alembic commands ###