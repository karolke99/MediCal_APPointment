"""empty message

Revision ID: a24da8f9bfca
Revises: 
Create Date: 2023-11-18 17:01:18.272849

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a24da8f9bfca'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('doctors',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.String(length=64), nullable=False),
    sa.Column('last_name', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('specializations',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('doctors_specializations',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('doctor_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('specialization_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['doctor_id'], ['doctors.id'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['specialization_id'], ['specializations.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('doctors_specializations')
    op.drop_table('specializations')
    op.drop_table('doctors')
    # ### end Alembic commands ###