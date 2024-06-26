"""DB con foto de perfil

Revision ID: 0340092a5586
Revises: 
Create Date: 2024-05-27 10:08:53.253589

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0340092a5586'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('fullname', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('role', sa.String(length=5), nullable=True),
    sa.Column('authenticated', sa.Boolean(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('profile_picture', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
