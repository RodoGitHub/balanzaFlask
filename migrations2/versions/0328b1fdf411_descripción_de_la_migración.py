"""Descripción de la migración

Revision ID: 0328b1fdf411
Revises: 01bfc6a918ca
Create Date: 2025-03-08 22:35:47.332869

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0328b1fdf411'
down_revision = '01bfc6a918ca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('detalle_venta', schema=None) as batch_op:
        batch_op.alter_column('factura_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('detalle_venta', schema=None) as batch_op:
        batch_op.alter_column('factura_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###
