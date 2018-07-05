"""empty message

Revision ID: 10c6b85c20bf
Revises: e8a7b0a46082
Create Date: 2018-07-04 21:58:48.047581

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10c6b85c20bf'
down_revision = 'e8a7b0a46082'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('eo_api_env_param',
    sa.Column('paramID', sa.Integer(), nullable=False),
    sa.Column('paramKey', sa.String(length=255), nullable=False),
    sa.Column('paramValue', sa.String(length=255), nullable=False),
    sa.Column('envID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['envID'], ['eo_api_env.envID'], ),
    sa.PrimaryKeyConstraint('paramID')
    )
    op.create_table('eo_api_env_param_additional',
    sa.Column('paramID', sa.Integer(), nullable=False),
    sa.Column('paramKey', sa.String(length=255), nullable=False),
    sa.Column('paramValue', sa.String(length=255), nullable=False),
    sa.Column('envID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['envID'], ['eo_api_env.envID'], ),
    sa.PrimaryKeyConstraint('paramID')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('eo_api_env_param_additional')
    op.drop_table('eo_api_env_param')
    # ### end Alembic commands ###
