"""Creating missing tables

Revision ID: f9509cce3bf4
Revises: 
Create Date: 2025-04-02 12:28:03.243272

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f9509cce3bf4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('heroes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('super_name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('powers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('heropowers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hero_id', sa.Integer(), nullable=True),
    sa.Column('power_id', sa.Integer(), nullable=True),
    sa.Column('strength', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['hero_id'], ['heroes.id'], ),
    sa.ForeignKeyConstraint(['power_id'], ['powers.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('hero_id', 'power_id', name='unique_hero_power')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('heropowers')
    op.drop_table('powers')
    op.drop_table('heroes')
    # ### end Alembic commands ###
