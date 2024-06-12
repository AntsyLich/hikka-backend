"""Added image_id field

Revision ID: 64b3937057ee
Revises: 68c5c7b598d1
Create Date: 2024-06-01 22:18:22.802673

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64b3937057ee'
down_revision = '68c5c7b598d1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('service_content_manga', sa.Column('image_id', sa.Uuid(), nullable=True))
    op.create_index(op.f('ix_service_content_manga_image_id'), 'service_content_manga', ['image_id'], unique=False)
    op.create_foreign_key(None, 'service_content_manga', 'service_images', ['image_id'], ['id'], ondelete='SET NULL')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'service_content_manga', type_='foreignkey')
    op.drop_index(op.f('ix_service_content_manga_image_id'), table_name='service_content_manga')
    op.drop_column('service_content_manga', 'image_id')
    # ### end Alembic commands ###
