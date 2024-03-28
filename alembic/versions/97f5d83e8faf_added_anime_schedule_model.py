"""Added anime schedule model

Revision ID: 97f5d83e8faf
Revises: 78e40095870a
Create Date: 2024-03-28 16:54:27.271165

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97f5d83e8faf'
down_revision = '78e40095870a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('service_schedule_anime',
    sa.Column('anime_id', sa.Uuid(), nullable=True),
    sa.Column('airing_at', sa.DateTime(), nullable=False),
    sa.Column('episode', sa.Integer(), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['anime_id'], ['service_content_anime.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_service_schedule_anime_anime_id'), 'service_schedule_anime', ['anime_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_service_schedule_anime_anime_id'), table_name='service_schedule_anime')
    op.drop_table('service_schedule_anime')
    # ### end Alembic commands ###
