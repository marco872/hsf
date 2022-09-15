"""photo

Revision ID: 606dba4b1c8b
Revises: 30640622f534
Create Date: 2022-09-14 14:41:39.381283

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '606dba4b1c8b'
down_revision = '30640622f534'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('viewrs', sa.Column('profile_pic', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('viewrs', 'profile_pic')
    # ### end Alembic commands ###