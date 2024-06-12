"""Added year field to manga

Revision ID: 0fa4c5e9a39b
Revises: 64b3937057ee
Create Date: 2024-06-01 22:19:18.660641

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0fa4c5e9a39b'
down_revision = '64b3937057ee'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('service_content_manga', sa.Column('year', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_service_content_manga_year'), 'service_content_manga', ['year'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_service_content_manga_year'), table_name='service_content_manga')
    op.drop_column('service_content_manga', 'year')
    # ### end Alembic commands ###
