"""Added the enabled column

Revision ID: f03cfd316fe4
Revises: 203988f07383
Create Date: 2022-01-02 13:23:16.613311

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f03cfd316fe4'
down_revision = '203988f07383'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('enabled', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'enabled')
    # ### end Alembic commands ###