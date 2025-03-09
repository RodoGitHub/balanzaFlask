"""empty message

Revision ID: 01bfc6a918ca
Revises: 7b0939807b58
Create Date: 2025-02-26 21:00:05.975680

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01bfc6a918ca'
down_revision = '7b0939807b58'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.alter_column('nombre_usuario',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=80),
               existing_nullable=False)
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=255),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)
        batch_op.alter_column('nombre_usuario',
               existing_type=sa.String(length=80),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)

    # ### end Alembic commands ###
