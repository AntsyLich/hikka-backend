"""Added avatar image relation to user

Revision ID: 70f0240158f7
Revises: 0d153972952b
Create Date: 2023-12-22 23:17:48.064569

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70f0240158f7'
down_revision = '0d153972952b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('service_users', sa.Column('avatar_image_id', sa.Uuid(), nullable=True))
    op.create_index(op.f('ix_service_users_avatar_image_id'), 'service_users', ['avatar_image_id'], unique=False)
    op.create_foreign_key(None, 'service_users', 'service_images', ['avatar_image_id'], ['id'], ondelete='SET NULL')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'service_users', type_='foreignkey')
    op.drop_index(op.f('ix_service_users_avatar_image_id'), table_name='service_users')
    op.drop_column('service_users', 'avatar_image_id')
    # ### end Alembic commands ###
