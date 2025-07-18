"""Added description to movie table

Revision ID: 105786bc0462
Revises: c2bfb546de20
Create Date: 2025-07-06 00:58:44.890886

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '105786bc0462'
down_revision = 'c2bfb546de20'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(length=500), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('movie_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['movie_id'], ['movie.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('movie', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(length=500), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('movie', schema=None) as batch_op:
        batch_op.drop_column('description')

    op.drop_table('comment')
    # ### end Alembic commands ###
