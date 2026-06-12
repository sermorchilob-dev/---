"""Add request model

Revision ID: xxxx
Revises: 5955c0e71504
Create Date: 2026-04-10 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'xxxx'  # оставьте свой ID
down_revision = '5955c0e71504'
branch_labels = None
depends_on = None

def upgrade():
    # Создаём таблицу requests
    op.create_table('requests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('customer_name', sa.String(length=100), nullable=False),
        sa.Column('customer_email', sa.String(length=100), nullable=False),
        sa.Column('customer_phone', sa.String(length=20), nullable=True),
        sa.Column('company_name', sa.String(length=200), nullable=True),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.Column('items', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_requests_id'), 'requests', ['id'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_requests_id'), table_name='requests')
    op.drop_table('requests')