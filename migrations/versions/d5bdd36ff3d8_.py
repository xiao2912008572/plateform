"""empty message

Revision ID: d5bdd36ff3d8
Revises: 35d32350efea
Create Date: 2018-07-04 17:38:45.345596

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd5bdd36ff3d8'
down_revision = '35d32350efea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('eo_api_env', sa.Column('projectID', sa.Integer(), nullable=True))
    op.drop_constraint('eo_api_env_ibfk_1', 'eo_api_env', type_='foreignkey')
    op.create_foreign_key(None, 'eo_api_env', 'eo_project', ['projectID'], ['projectID'])
    op.drop_column('eo_api_env', 'pid')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('eo_api_env', sa.Column('pid', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'eo_api_env', type_='foreignkey')
    op.create_foreign_key('eo_api_env_ibfk_1', 'eo_api_env', 'eo_project', ['pid'], ['projectID'])
    op.drop_column('eo_api_env', 'projectID')
    # ### end Alembic commands ###
