"""Added needs_search_update field

Revision ID: a35b01e181b2
Revises: 1245c32b25c6
Create Date: 2024-01-18 21:51:46.613260

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a35b01e181b2'
down_revision = '1245c32b25c6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('service_content_anime', sa.Column('needs_search_update', sa.Boolean(), nullable=False))
    op.add_column('service_content_characters', sa.Column('needs_search_update', sa.Boolean(), nullable=False))
    op.add_column('service_content_companies', sa.Column('needs_search_update', sa.Boolean(), nullable=False))
    op.add_column('service_content_people', sa.Column('needs_search_update', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('service_content_people', 'needs_search_update')
    op.drop_column('service_content_companies', 'needs_search_update')
    op.drop_column('service_content_characters', 'needs_search_update')
    op.drop_column('service_content_anime', 'needs_search_update')
    # ### end Alembic commands ###
